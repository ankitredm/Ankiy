#!/usr/bin/env python3
"""One-command smoke test for the full ANKIT 0.1 pipeline.

Run this on a CLOUD GPU (or any machine) BEFORE a real training run. It verifies
every step in one go, using the tiny smoke config so it finishes in seconds:

    1. Tokenizer works (text -> ids -> text round-trip)
    2. Data pipeline works (tokenized .bin loads into a dataset)
    3. Model forward pass works (correct shapes)
    4. Loss computes (finite, reasonable)
    5. Backward pass + optimizer step work (gradients flow)
    6. Checkpoint saves + reloads (weights round-trip)
    7. Generation works (produces a longer sequence)
    8. Parameter count == actual model

If the smoke test passes, the whole chain is wired correctly; only then should
you launch a larger training run. This script NEVER downloads a pretrained model.

Usage:
    python scripts/smoke_test.py                    # uses configs/smoke.yaml
    python scripts/smoke_test.py --config configs/smoke.yaml
    python scripts/smoke_test.py --verbose          # print more detail
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch

from model import AnkitModel
from model.config import Config
from tokenizer.tokenizer import AnkitTokenizer
from training.dataset import TokenDataset, collate_batch
from training.checkpoint import latest_checkpoint, save_checkpoint

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


def pass_(msg):  # noqa: ANN001
    print(f"{GREEN}PASS{RESET}  {msg}")


def fail(msg):  # noqa: ANN001
    print(f"{RED}FAIL{RESET}  {msg}")
    raise SystemExit(msg)


def warn(msg):  # noqa: ANN001
    print(f"{YELLOW}WARN{RESET}  {msg}")


def run_smoke(config_path: str, verbose: bool = False) -> None:
    config = Config.load(config_path)
    tcfg = config.training
    mcfg = config.model
    device = "cpu"  # smoke tests run on CPU for speed & universality

    torch.manual_seed(tcfg.seed)
    print(f"{BOLD}ANKIT 0.1 — smoke test{RESET} (config: {config_path})")
    print(f"Target steps: {tcfg.total_steps} | ctx: {mcfg.context_length}\n")

    # 1. Tokenizer ---------------------------------------------------------
    print(f"--- 1/8 Tokenizer ---")
    tok = AnkitTokenizer.load(tcfg.tokenizer_path)
    sample = "The capital of France is Paris."
    ids = tok.encode(sample, add_bos=True, add_eos=True)
    back = tok.decode(ids)
    if back.strip() != sample:
        fail(f"Tokenizer round-trip mismatch:\n  in : {sample!r}\n  out: {back!r}")
    if tok.bos_id is None or tok.eos_id is None:
        fail("Tokenizer missing BOS/EOS ids")
    pass_(f"vocab={tok.vocab_size} round-trip OK (BOS={tok.bos_id}, EOS={tok.eos_id})")

    # Align the model's vocab_size to the tokenizer's REAL vocabulary so the
    # embedding can index every token id. (train.py does the same thing.)
    if mcfg.vocab_size != tok.vocab_size:
        warn(
            f"model vocab_size {mcfg.vocab_size} != tokenizer {tok.vocab_size}; "
            f"building model with {tok.vocab_size} for the smoke test."
        )
        mcfg.vocab_size = tok.vocab_size

    # 2. Data pipeline -----------------------------------------------------
    print(f"--- 2/8 Data pipeline ---")
    for name, path in [("train", tcfg.train_data), ("val", tcfg.val_data)]:
        if not Path(path).exists():
            fail(f"Tokenized {name} data not found at {path}. Run "
                 "`python scripts/tokenize_dataset.py` first.")
    train_ds = TokenDataset(tcfg.train_data, mcfg.context_length)
    val_ds = TokenDataset(tcfg.val_data, mcfg.context_length)
    if len(train_ds) == 0:
        fail("Train dataset has 0 examples (corpus too small for one window).")
    x, y = train_ds[0]
    if x.shape != (mcfg.context_length,) or y.shape != (mcfg.context_length,):
        fail(f"Unexpected example shapes x={x.shape} y={y.shape}")
    pass_(f"train={len(train_ds):,} val={len(val_ds):,} examples; shapes OK")

    # 3. Model forward -----------------------------------------------------
    print(f"--- 3/8 Model (random init) ---")
    model = AnkitModel(mcfg).to(device)
    params = model.num_parameters()
    if params <= 0:
        fail("Model has 0 parameters")
    batch_x, batch_y = collate_batch([train_ds[i] for i in range(min(2, len(train_ds)))])
    logits = model(batch_x)
    expected = (batch_x.shape[0], mcfg.context_length, mcfg.vocab_size)
    if tuple(logits.shape) != expected:
        fail(f"Logits shape {tuple(logits.shape)} != expected {expected}")
    pass_(f"params={params:,} forward logits {tuple(logits.shape)}")

    # 4. Loss -------------------------------------------------------------
    print(f"--- 4/8 Loss ---")
    loss = torch.nn.functional.cross_entropy(
        logits.reshape(-1, logits.size(-1)), batch_y.reshape(-1)
    )
    if not torch.isfinite(loss):
        fail("Loss is not finite (NaN/Inf)")
    if loss.item() <= 0:
        fail("Loss is not positive")
    # Random init loss should be near log(vocab) for uniform output.
    expected_init = torch.log(torch.tensor(float(mcfg.vocab_size))).item()
    pass_(f"loss={loss.item():.4f} (random-init expected ~{expected_init:.3f})")

    # 5. Backward + optimizer ----------------------------------------------
    print(f"--- 5/8 Backward + optimizer ---")
    optimizer = torch.optim.AdamW(model.parameters(), lr=tcfg.learning_rate)
    loss.backward()
    grad_count = sum(1 for p in model.parameters() if p.grad is not None)
    if grad_count == 0:
        fail("No gradients produced during backward pass")
    torch.nn.utils.clip_grad_norm_(model.parameters(), tcfg.max_grad_norm)
    optimizer.step()
    optimizer.zero_grad()
    pass_(f"{grad_count}/{sum(1 for _ in model.parameters())} params got gradients; step OK")

    # 6. Checkpoint save + reload -------------------------------------------
    print(f"--- 6/8 Checkpoint save + reload ---")
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        save_checkpoint(tmp, model, optimizer, None, step=1, config=config,
                        tokenizer_version="v0.1", seed=tcfg.seed)
        latest = latest_checkpoint(tmp)
        if latest is None or not (latest / "model.safetensors").exists():
            fail("Checkpoint did not save model.safetensors")
        model.eval()
        before = model(batch_x)
        from training.checkpoint import load_checkpoint_model
        model2, cfg2 = load_checkpoint_model(tmp, device=device)
        model2.eval()
        after = model2(batch_x)
        if not torch.allclose(before, after, atol=1e-5):
            fail("Reloaded checkpoint produced different predictions")
    pass_("checkpoint saved + reloaded; predictions identical")

    # 7. Generation ---------------------------------------------------------
    print(f"--- 7/8 Generation ---")
    prompt = tok.encode("The", add_bos=True, add_eos=False) or [tok.bos_id]
    prompt = torch.tensor([prompt], dtype=torch.long)
    out = model.generate(prompt, max_new_tokens=5, temperature=0.8, seed=1)
    if out.shape[1] <= prompt.shape[1]:
        fail("Generation did not extend the sequence")
    pass_(f"generated {out.shape[1] - prompt.shape[1]} new tokens")

    # 8. Parameter count -----------------------------------------------------
    print(f"--- 8/8 Parameter count ---")
    if params != sum(p.numel() for p in model.parameters()):
        fail("Parameter count mismatch")
    pass_(f"count_parameters consistent: {params:,} ({params/1e6:.2f}M)")

    print(f"\n{GREEN}{BOLD}SMOKE TEST PASSED{RESET} — full pipeline is wired correctly.")
    print(f"{BOLD}Next:{RESET} launch a real training run on a cloud GPU "
          f"(see configs/{config.name}.yaml).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke-test the ANKIT 0.1 pipeline.")
    parser.add_argument(
        "--config",
        default="configs/smoke.yaml",
        help="Path to a config for the smoke run (default: configs/smoke.yaml).",
    )
    parser.add_argument("--verbose", action="store_true", help="Print more detail.")
    args = parser.parse_args()
    run_smoke(args.config, args.verbose)


if __name__ == "__main__":
    main()
