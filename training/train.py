"""Train ANKIT 0.1 from randomly initialised weights.

This is the core of the whole project. It:

    1. Loads the model/training config (configs/ankit_0_1.yaml or smoke.yaml).
    2. Loads OUR tokenizer (Phase 4) and OUR tokenized corpus (.bin, Phase 5a).
    3. Builds an AnkitModel from RANDOM weights (never a pretrained checkpoint).
    4. Sets up an optimizer (AdamW) + warmup/cosine LR schedule + grad clipping.
    5. Runs the causal next-token-prediction training loop with optional mixed
       precision, gradient accumulation, validation, checkpointing and resume.
    6. Saves the final model.

ANTI-SHORTCUT GUARANTEES
-----------------------
 - Before training starts we PROVE the model is exactly a fresh random
   initialisation (``training/provenance.verify_fresh_initialization``):
   a reference model is rebuilt from the same seed and every weight is
   compared bit-for-bit. If ANY weight was loaded or modified in between,
   training refuses to start.
 - If a resume path is used, the checkpoint is first verified to be a NATIVE
   ANKIT checkpoint (our own format AND architecture) — see
   ``training.checkpoint.validate_resume_checkpoint``.
 - No pretrained model weights or tokenizer are ever loaded.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

# Make `python training/train.py` work from anywhere: put the repo root on
# sys.path so `model`, `tokenizer` and `training` are importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
import torch.nn.functional as F
from safetensors.torch import load_file

# Use every CPU core we have. Some sandboxes default the intra-op pool to a
# single thread even when multiple cores exist, which would ~2x slow training
# down. Respect an explicit ANKIT_NUM_THREADS, else use all detected cores.
try:
    torch.set_num_threads(int(os.environ.get("ANKIT_NUM_THREADS", str(os.cpu_count() or 1))))
except Exception:  # pragma: no cover - never block training on this
    pass

from model import AnkitModel
from model.config import Config, ModelConfig
from tokenizer.tokenizer import AnkitTokenizer
from training.checkpoint import latest_checkpoint, save_checkpoint, validate_resume_checkpoint
from training.dataset import TokenDataset, collate_batch
from training.provenance import verify_fresh_initialization

# ---------------------------------------------------------------------------
# LR schedule: linear warmup, then cosine decay.
# ---------------------------------------------------------------------------


def build_lr_lambda(warmup_steps: int, total_steps: int):
    """Return a function(step) -> lr scaling factor in [0, 1]."""

    def lr_lambda(step: int) -> float:
        if step < warmup_steps:
            if warmup_steps <= 0:
                return 1.0
            return (step + 1) / warmup_steps
        if step >= total_steps:
            return 0.0
        # Cosine from 1.0 (right after warmup) down to ~0 (at total_steps).
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return 0.5 * (1.0 + math.cos(math.pi * progress))

    return lr_lambda


# ---------------------------------------------------------------------------
# Device / precision helpers — both keyed on the RESOLVED training device,
# never on "does CUDA exist" (they can differ, e.g. device='cpu' on a GPU box).
# ---------------------------------------------------------------------------
def resolve_device(device: str) -> str:
    if device == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        if not torch.cuda.is_available():
            print("[warn] device='cuda' but no GPU; falling back to CPU.")
            return "cpu"
        return "cuda"
    return "cpu"


def resolve_autocast(precision: str, device: str):
    """Return the autocast context manager for the resolved device.

    Autocast is enabled only for bf16/fp16 on CUDA. On CPU we keep full fp32
    (CPU autocast is not part of the training design) and say so loudly if a
    config asks for mixed precision it cannot get.
    """
    if device == "cuda" and precision in ("bf16", "fp16"):
        dtype = torch.bfloat16 if precision == "bf16" else torch.float16
        return torch.autocast(device_type="cuda", dtype=dtype)
    if precision != "fp32":
        print(
            f"[warn] precision='{precision}' requested but device resolved to "
            f"'{device}'; training in full fp32 instead."
        )
    # CPU or fp32: no autocast.
    return torch.autocast(device_type="cpu", enabled=False)


def resolve_grad_scaler(precision: str, device: str) -> "torch.amp.GradScaler | None":
    """GradScaler is needed ONLY for fp16 on the resolved CUDA device.

    fp16 gradients can underflow, hence dynamic loss scaling. bf16 needs no
    scaler, and neither does fp32 or any CPU run. (The old code enabled the
    scaler whenever CUDA *existed* — even when training had resolved to CPU.)
    """
    if device == "cuda" and precision == "fp16":
        return torch.amp.GradScaler(device)
    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
@torch.no_grad()
def evaluate(
    model: AnkitModel,
    loader: torch.utils.data.DataLoader,
    device: str,
    max_batches: int = 0,
) -> float:
    """Compute mean cross-entropy loss over an evaluation dataset.

    ``max_batches`` caps how many validation batches are used per evaluation
    (driven by ``training.eval_steps``); 0 or negative means the full set.
    """
    model.eval()
    total_loss = 0.0
    n_batches = 0
    for x, y in loader:
        if max_batches is not None and max_batches > 0 and n_batches >= max_batches:
            break
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = F.cross_entropy(
            logits.reshape(-1, logits.size(-1)), y.reshape(-1)
        )
        total_loss += loss.item()
        n_batches += 1
    model.train()
    if n_batches == 0:
        return float("nan")
    return total_loss / n_batches


def take_optimizer_step(
    model: AnkitModel,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.LRScheduler | None,
    grad_scaler: "torch.amp.GradScaler | None",
    max_grad_norm: float,
) -> None:
    """One optimizer step over whatever gradients have accumulated.

    Shared by full accumulation windows AND the final partial window at the
    end of an epoch, so incomplete windows are trained on instead of being
    silently dropped.
    """
    if grad_scaler is not None:
        grad_scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
    if grad_scaler is not None:
        grad_scaler.step(optimizer)
        grad_scaler.update()
    else:
        optimizer.step()
    if scheduler is not None:
        scheduler.step()
    optimizer.zero_grad(set_to_none=True)


# ---------------------------------------------------------------------------
# Main training
# ---------------------------------------------------------------------------
def run_training(config: Config) -> None:
    tcfg = config.training
    mcfg = config.model
    device = resolve_device(tcfg.device)

    # ---- reproducibility -------------------------------------------------
    torch.manual_seed(tcfg.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(tcfg.seed)
    os.environ.setdefault("PYTHONHASHSEED", str(tcfg.seed))

    # ---- LOAD OUR TOKENIZER (Phase 4) -----------------------------------
    tokenizer = AnkitTokenizer.load(tcfg.tokenizer_path)
    tokenizer_version = "v0.1"
    print(f"Tokenizer vocab: {tokenizer.vocab_size}")

    # ---- ALIGN model vocab to tokenizer ----------------------------------
    # The model's output head must match the tokenizer's real vocabulary.
    print(f"Model configured vocab: {mcfg.vocab_size}")
    if mcfg.vocab_size != tokenizer.vocab_size:
        print(
            f"[info] model vocab_size {mcfg.vocab_size} != tokenizer "
            f"{tokenizer.vocab_size}. Building model with {tokenizer.vocab_size} "
            "to match the tokenizer (see configs/ankit_0_1.yaml if this differs)."
        )
    mcfg.vocab_size = tokenizer.vocab_size

    # ---- BUILD MODEL FROM RANDOM WEIGHTS ----------------------------------
    # ANTI-SHORTCUT: we start from a fresh model. No pretrained weights.
    print("Building AnkitModel from RANDOM weights (from scratch)...")
    model = AnkitModel(mcfg).to(device)
    print(f"  parameters: {model.num_parameters():,}")

    # ---- DATASETS ---------------------------------------------------------
    # TokenDataset itself raises clear errors for missing / empty / corrupt /
    # too-small .bin files — before any training happens.
    print(f"Loading token data (device={device})...")
    train_ds = TokenDataset(tcfg.train_data, mcfg.context_length)
    val_ds = TokenDataset(tcfg.val_data, mcfg.context_length)
    train_loader = torch.utils.data.DataLoader(
        train_ds,
        batch_size=tcfg.batch_size,
        shuffle=True,
        collate_fn=collate_batch,
        num_workers=0,  # keep it simple and deterministic
    )
    val_loader = torch.utils.data.DataLoader(
        val_ds,
        batch_size=max(1, tcfg.batch_size),  # smallest batch size for val
        shuffle=False,
        collate_fn=collate_batch,
        num_workers=0,
    )
    print(
        f"  train: {len(train_ds):,} examples | "
        f"val: {len(val_ds):,} examples"
    )

    # ---- Optimizer + scheduler -------------------------------------------
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=tcfg.learning_rate,
        weight_decay=tcfg.weight_decay,
        betas=(0.9, 0.95),  # standard for transformer training
    )
    lr_lambda = build_lr_lambda(tcfg.warmup_steps, tcfg.total_steps)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    # ---- Mixed precision (keyed on the RESOLVED device) --------------------
    autocast = resolve_autocast(tcfg.precision, device)
    grad_scaler = resolve_grad_scaler(tcfg.precision, device)

    # ---- Resume support ---------------------------------------------------
    # find_latest returns the most recent "step_N" checkpoint directory.
    start_step = 0
    resumed_from = latest_checkpoint(Path(tcfg.output_dir))
    if resumed_from is not None:
        # Verify this is a NATIVE ANKIT checkpoint whose architecture,
        # context length and tokenizer vocabulary still match this run —
        # BEFORE any weights are loaded.
        meta = validate_resume_checkpoint(resumed_from, config, tokenizer.vocab_size)
        print(f"Resuming from {resumed_from} ...")
        start_step = int(meta["step"])
        model.load_state_dict(load_file(str(resumed_from / "model.safetensors"), device=device))
        optimizer.load_state_dict(
            torch.load(resumed_from / "optimizer.pt", map_location=device, weights_only=False)
        )
        if (resumed_from / "scheduler.pt").exists():
            scheduler.load_state_dict(
                torch.load(resumed_from / "scheduler.pt", map_location=device, weights_only=False)
            )
        print(f"  resumed at step {start_step}")
    else:
        # ANTI-SHORTCUT: prove the weights in memory are EXACTLY a fresh
        # random initialisation for (config, seed) — bit-for-bit against a
        # reference rebuild. If anything was loaded or mutated, refuse.
        _verify_no_pretrained(model, mcfg, tcfg.seed)

    if start_step >= tcfg.total_steps:
        print(
            f"[warn] checkpoint step {start_step} >= total_steps "
            f"{tcfg.total_steps}; nothing left to train. Lower total_steps, "
            "raise it, or use a fresh output_dir."
        )

    # ---- Training loop -----------------------------------------------------
    model.train()
    total_loss_tokens = 0
    total_loss_count = 0
    step = start_step
    micro_batches_in_window = 0  # backward passes since the last optimizer step
    _best_val = [float("inf"), start_step]  # [best val loss, step]
    if start_step > 0:
        # Resuming: keep prior best (if recorded) so best-tracking spans stages.
        best_file = Path(tcfg.output_dir) / "best_val.json"
        if best_file.exists():
            try:
                _best_val = list(json.loads(best_file.read_text()))
            except Exception:
                pass
    t_start = time.time()

    print(
        f"\nTraining {config.name} — {tcfg.total_steps} steps, "
        f"ctx {mcfg.context_length}, batch x accum = "
        f"{tcfg.batch_size}x{tcfg.grad_accumulation_steps}"
    )

    def finish_optimizer_step() -> None:
        """Clip+step+scheduler, then log / validate / checkpoint.

        Shared by complete accumulation windows and the final partial window,
        so both paths behave identically.
        """
        nonlocal step, total_loss_tokens, total_loss_count, micro_batches_in_window
        take_optimizer_step(
            model, optimizer, scheduler, grad_scaler, tcfg.max_grad_norm
        )
        micro_batches_in_window = 0
        step += 1

        # ---- Logging ----
        lr = optimizer.param_groups[0]["lr"]
        avg_loss = total_loss_tokens / max(1, total_loss_count)
        elapsed = time.time() - t_start
        print(
            f"  step {step:>5}/{tcfg.total_steps} | "
            f"loss {avg_loss:.4f} | "
            f"ppl {math.exp(min(avg_loss, 20)):.2f} | "
            f"lr {lr:.2e} | "
            f"{elapsed:.1f}s"
        )
        total_loss_tokens = 0
        total_loss_count = 0

        # ---- Validation ----
        if tcfg.eval_interval > 0 and step % tcfg.eval_interval == 0:
            val_loss = evaluate(
                model, val_loader, device, max_batches=tcfg.eval_steps
            )
            print(f"    [eval] val loss {val_loss:.4f} | ppl {math.exp(min(val_loss, 20)):.2f}")
            # Track the BEST validation checkpoint (model-only, cheap to keep).
            if val_loss == val_loss and val_loss < _best_val[0]:
                _best_val[0] = val_loss
                _best_val[1] = step
                save_checkpoint(
                    Path(tcfg.output_dir),
                    model,
                    optimizer,
                    scheduler,
                    step,
                    config,
                    tokenizer_version="v0.1",
                    seed=config.training.seed,
                    tag="best",
                    tokenizer_vocab_size=tokenizer.vocab_size,
                    save_optimizer=False,
                )
                (Path(tcfg.output_dir) / "best_val.json").write_text(
                    json.dumps([_best_val[0], _best_val[1]]))
                import shutil
                for old_best in Path(tcfg.output_dir).glob("best_step_*"):
                    if old_best.name != f"best_step_{step}":
                        shutil.rmtree(old_best, ignore_errors=True)
                print(f"    [best] new best val loss {val_loss:.4f} (step {step}) -> best_step_{step}")

        # ---- Checkpoint ----
        if tcfg.checkpoint_interval > 0 and step % tcfg.checkpoint_interval == 0:
            _save(model, optimizer, scheduler, step, config, tokenizer.vocab_size)

    while step < tcfg.total_steps:
        for x, y in train_loader:
            if step >= tcfg.total_steps:
                break
            x, y = x.to(device), y.to(device)
            with autocast:
                logits = model(x)
                loss = F.cross_entropy(
                    logits.reshape(-1, logits.size(-1)), y.reshape(-1)
                )
            # For gradient accumulation, scale loss by accumulation steps so
            # every optimizer step optimises the MEAN over its micro-batches.
            loss = loss / tcfg.grad_accumulation_steps

            # Backward (with grad scaler only for fp16 on CUDA).
            if grad_scaler is not None:
                grad_scaler.scale(loss).backward()
            else:
                loss.backward()

            total_loss_tokens += loss.item() * tcfg.grad_accumulation_steps
            total_loss_count += 1
            micro_batches_in_window += 1

            # Accumulate gradients over the configured number of micro-batches.
            if micro_batches_in_window >= tcfg.grad_accumulation_steps:
                finish_optimizer_step()

        # ---- End of epoch: flush the incomplete final accumulation window ----
        # If the data ran out mid-window, the accumulated gradients must STILL
        # produce an optimizer step — silently dropping them would throw away
        # training signal every epoch whenever
        # len(loader) % grad_accumulation_steps != 0.
        if step < tcfg.total_steps and micro_batches_in_window > 0:
            print(
                f"  [accum] end of epoch: applying the final partial "
                f"accumulation window ({micro_batches_in_window} micro-batch"
                f"{'es' if micro_batches_in_window != 1 else ''} of "
                f"{tcfg.grad_accumulation_steps})."
            )
            finish_optimizer_step()

    # ---- Final checkpoint -------------------------------------------------
    # Save the final one unless this exact step was already saved above.
    # (checkpoint_interval == 0 disables mid-run checkpoints entirely.)
    if tcfg.checkpoint_interval <= 0 or step % tcfg.checkpoint_interval != 0:
        _save(model, optimizer, scheduler, step, config, tokenizer.vocab_size)
    print("\nTraining complete.")
    print("Anti-shortcut: model was trained from scratch with our own weights.")


def _save(model, optimizer, scheduler, step, config, tokenizer_vocab_size) -> None:
    ckpt_dir = Path(config.training.output_dir)
    save_checkpoint(
        ckpt_dir,
        model,
        optimizer,
        scheduler,
        step,
        config,
        tokenizer_version="v0.1",
        seed=config.training.seed,
        tokenizer_vocab_size=tokenizer_vocab_size,
    )
    print(f"    [checkpoint] saved to {ckpt_dir}/step_{step}")


def _verify_no_pretrained(model: AnkitModel, config: ModelConfig, seed: int) -> None:
    """Guard against accidentally training from anything but fresh weights.

    Rebuilds a reference model from (config, seed) and compares every
    parameter bit-for-bit with the model about to be trained. See
    ``training/provenance``.
    """
    verify_fresh_initialization(model, config, seed)
    print(
        "[check] verified: every weight matches a fresh random initialisation "
        "for this config+seed — no pretrained or external weights were loaded."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Train ANKIT 0.1 from scratch.")
    parser.add_argument(
        "--config",
        default="configs/ankit_0_1.yaml",
        help="Path to a model/training config YAML.",
    )
    args = parser.parse_args()

    config = Config.load(args.config)
    run_training(config)


if __name__ == "__main__":
    main()
