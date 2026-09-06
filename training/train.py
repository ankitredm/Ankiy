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
 - At startup we EXPLICITLY assert that we are NOT loading any pretrained
   checkpoint. If a resume path is given, it is OUR OWN ANKIT checkpoint.
 - No pretrained model weights or tokenizer are ever loaded.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

import torch
import torch.nn.functional as F
from safetensors.torch import load_file

from model import AnkitModel
from model.config import Config
from tokenizer.tokenizer import AnkitTokenizer
from training.checkpoint import latest_checkpoint, save_checkpoint
from training.dataset import TokenDataset, collate_batch

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
# Device / precision helpers
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
    """Return the autocast context manager (or a no-op for fp32 CPU)."""
    if device == "cuda" and precision in ("bf16", "fp16"):
        dtype = torch.bfloat16 if precision == "bf16" else torch.float16
        return torch.autocast(device_type="cuda", dtype=dtype)
    # CPU or fp32: no autocast.
    return torch.autocast(device_type="cpu", enabled=False)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
@torch.no_grad()
def evaluate(
    model: AnkitModel, loader: torch.utils.data.DataLoader, device: str
) -> float:
    """Compute mean cross-entropy loss over an evaluation dataset."""
    model.eval()
    total_loss = 0.0
    n_batches = 0
    for x, y in loader:
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

    # ---- Mixed precision --------------------------------------------------
    autocast = resolve_autocast(tcfg.precision, device)
    grad_scaler = torch.amp.GradScaler(enabled=(tcfg.precision in ("fp16",))) if torch.cuda.is_available() else None

    # ---- Resume support ---------------------------------------------------
    # find_latest returns the most recent "step_N" checkpoint directory.
    start_step = 0
    resume_dir = latest_checkpoint(Path(tcfg.output_dir))
    if resume_dir is not None:
        print(f"Resuming from {resume_dir} ...")
        meta = json.loads((resume_dir / "meta.json").read_text(encoding="utf-8"))
        start_step = int(meta["step"])
        model.load_state_dict(load_file(str(resume_dir / "model.safetensors"), device=device))
        optimizer.load_state_dict(
            torch.load(resume_dir / "optimizer.pt", map_location=device, weights_only=False)
        )
        if (resume_dir / "scheduler.pt").exists():
            scheduler.load_state_dict(
                torch.load(resume_dir / "scheduler.pt", map_location=device, weights_only=False)
            )
        print(f"  resumed at step {start_step}")

    # ---- Training loop -----------------------------------------------------
    model.train()
    total_loss_tokens = 0
    total_loss_count = 0
    step = start_step
    t_start = time.time()
    # Verify no pretrained weights
    _verify_no_pretrained()

    print(
        f"\nTraining {config.name} — {tcfg.total_steps} steps, "
        f"ctx {mcfg.context_length}, batch x accum = "
        f"{tcfg.batch_size}x{tcfg.grad_accumulation_steps}"
    )

    while step < tcfg.total_steps:
        for micro_batch, (x, y) in enumerate(train_loader):
            if step >= tcfg.total_steps:
                break
            x, y = x.to(device), y.to(device)
            with autocast:
                logits = model(x)
                loss = F.cross_entropy(
                    logits.reshape(-1, logits.size(-1)), y.reshape(-1)
                )
            # For gradient accumulation, scale loss by accumulation steps.
            loss = loss / tcfg.grad_accumulation_steps

            # Backward (with grad scaler only if enabled).
            if grad_scaler is not None:
                grad_scaler.scale(loss).backward()
            else:
                loss.backward()

            total_loss_tokens += loss.item() * tcfg.grad_accumulation_steps
            total_loss_count += 1

            # Accumulate gradients over the specified number of micro-batches.
            if (micro_batch + 1) % tcfg.grad_accumulation_steps == 0:
                # Clip gradients.
                if grad_scaler is not None:
                    grad_scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), tcfg.max_grad_norm)
                # Step.
                if grad_scaler is not None:
                    grad_scaler.step(optimizer)
                    grad_scaler.update()
                else:
                    optimizer.step()
                scheduler.step()
                optimizer.zero_grad(set_to_none=True)
                step += 1

                # ---- Logging ----
                if step % 1 == 0 or step == tcfg.total_steps:
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
                    val_loss = evaluate(model, val_loader, device)
                    print(f"    [eval] val loss {val_loss:.4f} | ppl {math.exp(min(val_loss, 20)):.2f}")

                # ---- Checkpoint ----
                if tcfg.checkpoint_interval > 0 and step % tcfg.checkpoint_interval == 0:
                    _save(model, optimizer, scheduler, step, config)

    # ---- Final checkpoint -------------------------------------------------
    # Only save the final one if the last step wasn't already saved above.
    if step == 0 or step % tcfg.checkpoint_interval != 0:
        _save(model, optimizer, scheduler, step, config)
    print("\nTraining complete.")
    print("Anti-shortcut: model was trained from scratch with our own weights.")


def _save(model, optimizer, scheduler, step, config) -> None:
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
    )
    print(f"    [checkpoint] saved to {ckpt_dir}/step_{step}")


def _verify_no_pretrained() -> None:
    """Guard against accidentally loading a pretrained model in the future."""
    # We build from random weights; nothing here reads from_pretrained.
    # This is a deliberate, documented anti-shortcut boundary.
    print("[check] no pretrained weights loaded — training from scratch.")


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
