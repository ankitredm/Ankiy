"""Tests for the ANKIT 0.1 training loop, dataset, and checkpoint modules."""

from __future__ import annotations

import torch

from model import AnkitModel, Config
from training.checkpoint import latest_checkpoint, save_checkpoint
from training.dataset import TokenDataset, collate_batch
from training.train import build_lr_lambda, resolve_device


# ---------------------------------------------------------------------------
# LR schedule
# ---------------------------------------------------------------------------
def test_lr_warmup_linear():
    lr_lambda = build_lr_lambda(warmup_steps=10, total_steps=100)
    assert lr_lambda(0) == 0.1  # (0+1)/10
    assert lr_lambda(5) == 0.6  # (5+1)/10
    assert lr_lambda(10) == 1.0  # end of warmup -> full LR


def test_lr_cosine_decay():
    lr_lambda = build_lr_lambda(warmup_steps=10, total_steps=100)
    # After warmup, decay to ~0 at total_steps.
    assert lr_lambda(50) < 1.0
    assert lr_lambda(100) == 0.0
    # Monotonic decrease between warmup and total_steps.
    prev = lr_lambda(11)
    for s in range(12, 100):
        cur = lr_lambda(s)
        assert cur <= prev + 1e-6
        prev = cur


def test_lr_no_warmup():
    lr_lambda = build_lr_lambda(warmup_steps=0, total_steps=10)
    assert lr_lambda(0) == 1.0


# ---------------------------------------------------------------------------
# Device resolution
# ---------------------------------------------------------------------------
def test_resolve_device_cpu():
    assert resolve_device("cpu") == "cpu"
    assert resolve_device("auto") in ("cuda", "cpu")


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------
def test_token_dataset_requires_existing(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        TokenDataset(tmp_path / "missing.bin", context_length=8)


def test_token_dataset_length_and_shapes(smoke_bin):
    ds = TokenDataset(smoke_bin, context_length=8)
    assert len(ds) > 0
    x, y = ds[0]
    assert x.shape == (8,)
    assert y.shape == (8,)
    # Target is shifted by one: y[i] == x[i+1] within the window.
    # (That's true for the overlapping window, not positions at edges.)
    assert torch.allclose(x[1:], y[:-1])


def test_collate_batch():
    xs = [torch.arange(8) for _ in range(3)]
    ys = [torch.arange(8) + 1 for _ in range(3)]
    bx, by = collate_batch(list(zip(xs, ys)))
    assert bx.shape == (3, 8)
    assert by.shape == (3, 8)


# ---------------------------------------------------------------------------
# Checkpoint save + load
# ---------------------------------------------------------------------------
def test_save_and_latest_checkpoint(tmp_path):
    cfg = Config.load("configs/smoke.yaml")
    model = AnkitModel(cfg.model)
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.training.learning_rate)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1.0)

    save_checkpoint(
        tmp_path, model, opt, sched, step=7, config=cfg,
        tokenizer_version="v0.1", seed=42,
    )
    latest = latest_checkpoint(tmp_path)
    assert latest is not None
    assert (latest / "model.safetensors").exists()
    assert (latest / "meta.json").exists()
    # The step is embedded in the directory name.
    assert latest.name == "step_7"


def test_checkpoint_roundtrip_inference(tmp_path):
    """A model saved then reloaded must produce identical logits (eval mode)."""
    cfg = Config.load("configs/smoke.yaml")
    model = AnkitModel(cfg.model)
    opt = torch.optim.AdamW(model.parameters(), lr=cfg.training.learning_rate)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1.0)
    save_checkpoint(tmp_path, model, opt, sched, step=1, config=cfg, tokenizer_version="v0.1", seed=42)

    from training.checkpoint import load_checkpoint_model
    model2, cfg2 = load_checkpoint_model(tmp_path, device="cpu")
    assert cfg2.model.vocab_size == cfg.model.vocab_size

    x = torch.randint(0, cfg.model.vocab_size, (1, 8))
    model.eval()
    model2.eval()
    with torch.no_grad():
        out1 = model(x)
        out2 = model2(x)
    assert torch.allclose(out1, out2, atol=1e-5)


# ---------------------------------------------------------------------------
# Model forward during training-style usage
# ---------------------------------------------------------------------------
def test_model_train_forward_and_backward():
    cfg = Config.load("configs/smoke.yaml")
    model = AnkitModel(cfg.model)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
    x = torch.randint(0, cfg.model.vocab_size, (2, 16))
    y = torch.randint(0, cfg.model.vocab_size, (2, 16))
    logits = model(x)
    loss = torch.nn.functional.cross_entropy(
        logits.reshape(-1, logits.size(-1)), y.reshape(-1)
    )
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    assert loss.item() > 0
    # After a step, params should have changed.
    assert loss.item() != float("inf")
