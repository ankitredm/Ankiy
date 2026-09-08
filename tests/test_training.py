"""Tests for the ANKIT 0.1 training loop, dataset, and checkpoint modules."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from model import AnkitModel, Config
from training.checkpoint import (
    latest_checkpoint,
    save_checkpoint,
    validate_resume_checkpoint,
)
from training.dataset import TokenDataset, collate_batch
from training.provenance import (
    fresh_model_fingerprint,
    state_dict_fingerprint,
    verify_ankit_checkpoint,
    verify_fresh_initialization,
)
from training.train import (
    build_lr_lambda,
    resolve_autocast,
    resolve_device,
    resolve_grad_scaler,
    run_training,
    take_optimizer_step,
)


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


# ---------------------------------------------------------------------------
# Dataset validation (missing / empty / corrupt / too-small token data)
# ---------------------------------------------------------------------------
def test_token_dataset_rejects_empty_file(tmp_path):
    empty = tmp_path / "empty.bin"
    empty.touch()
    with pytest.raises(ValueError, match="[Ee]mpty"):
        TokenDataset(empty, context_length=8)


def test_token_dataset_rejects_too_small_file(tmp_path):
    # 5 tokens cannot produce a single (context_length=8)+1 window.
    tiny = tmp_path / "tiny.bin"
    np.arange(5, dtype=np.uint16).tofile(str(tiny))
    with pytest.raises(ValueError, match="too small"):
        TokenDataset(tiny, context_length=8)


def test_token_dataset_rejects_corrupt_file(tmp_path):
    # 3 bytes is not a whole number of uint16 ids.
    odd = tmp_path / "odd.bin"
    odd.write_bytes(b"\x01\x02\x03")
    with pytest.raises(ValueError, match="corrupt"):
        TokenDataset(odd, context_length=8)


def test_token_dataset_rejects_bad_context_length(smoke_bin):
    with pytest.raises(ValueError):
        TokenDataset(smoke_bin, context_length=0)


# ---------------------------------------------------------------------------
# eval_steps: cap how many validation batches each eval uses
# ---------------------------------------------------------------------------
def test_evaluate_max_batches_caps_validation():
    cfg = Config.load("configs/smoke.yaml")
    cfg.model.context_length = 16
    model = AnkitModel(cfg.model)
    model.eval()
    vocab = cfg.model.vocab_size
    torch.manual_seed(0)
    # Deliberately different losses per batch so partial means differ.
    batches = [
        (
            torch.randint(0, vocab, (2, 16)),
            torch.randint(0, vocab, (2, 16)),
        )
        for _ in range(4)
    ]

    def _batch_loss(x, y):
        logits = model(x)
        return torch.nn.functional.cross_entropy(
            logits.reshape(-1, vocab), y.reshape(-1)
        ).item()

    per_batch = [_batch_loss(x, y) for x, y in batches]

    from training.train import evaluate

    capped = evaluate(model, batches, "cpu", max_batches=2)
    assert capped == pytest.approx(sum(per_batch[:2]) / 2, rel=1e-5)
    full = evaluate(model, batches, "cpu", max_batches=0)  # 0 = full set
    assert full == pytest.approx(sum(per_batch) / len(per_batch), rel=1e-5)
    # The cap genuinely changed the result for this uneven data.
    assert capped != pytest.approx(full, rel=1e-5)


# ---------------------------------------------------------------------------
# Mixed precision helpers depend on the RESOLVED device (not CUDA existence)
# ---------------------------------------------------------------------------
def test_grad_scaler_depends_on_resolved_device():
    # fp16 on CPU (even on a machine that HAS a GPU) must NOT get a scaler.
    assert resolve_grad_scaler("fp16", "cpu") is None
    # bf16 and fp32 never need a scaler.
    assert resolve_grad_scaler("bf16", "cpu") is None
    assert resolve_grad_scaler("fp32", "cpu") is None
    assert resolve_grad_scaler("bf16", "cuda") is None
    if torch.cuda.is_available():
        assert resolve_grad_scaler("fp16", "cuda") is not None


def test_autocast_disabled_on_cpu():
    # Even with precision='fp16', a CPU-resolved run must stay fp32.
    autocast = resolve_autocast("fp16", "cpu")
    with autocast:
        out = torch.nn.Linear(4, 4)(torch.randn(2, 4))
    assert out.dtype == torch.float32


# ---------------------------------------------------------------------------
# take_optimizer_step: the shared step used by full AND partial windows
# ---------------------------------------------------------------------------
def test_take_optimizer_step_updates_params_and_clears_grads():
    cfg = Config.load("configs/smoke.yaml")
    model = AnkitModel(cfg.model)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-2)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lambda s: 1.0 / (1.0 + s))

    x = torch.randint(0, cfg.model.vocab_size, (2, 16))
    y = torch.randint(0, cfg.model.vocab_size, (2, 16))
    logits = model(x)
    torch.nn.functional.cross_entropy(
        logits.reshape(-1, logits.size(-1)), y.reshape(-1)
    ).backward()

    weight_before = model.lm_head.weight.detach().clone()

    take_optimizer_step(model, optimizer, scheduler, None, max_grad_norm=1.0)

    assert not torch.equal(model.lm_head.weight.detach(), weight_before)
    # set_to_none: gradients are cleared after the step.
    assert all(p.grad is None for p in model.parameters())
    # The LR scheduler advanced (lr now follows lambda(1) = 0.5).
    assert optimizer.param_groups[0]["lr"] == pytest.approx(0.5 * 1e-2)


# ---------------------------------------------------------------------------
# Gradient accumulation: incomplete final windows MUST be applied
# ---------------------------------------------------------------------------
def test_partial_accumulation_window_is_applied(monkeypatch, tiny_run_config):
    """End-of-epoch partial accumulation windows produce a real optimizer step.

    With 50 examples / batch 2 there are 25 micro-batches per epoch, so
    grad_accumulation_steps=4 yields 6 complete windows + 1 leftover
    micro-batch. total_steps=7 is only reachable if that partial window is
    stepped at the end of epoch 1 (the old code silently dropped it, so steps
    could only ever land on multiples of 6 and training would overshoot).
    """
    cfg = tiny_run_config
    assert cfg.training.grad_accumulation_steps == 4
    assert cfg.training.total_steps == 7

    calls: list[int] = []
    original_step = torch.optim.AdamW.step

    def counting_step(self, *args, **kwargs):
        calls.append(id(self))
        return original_step(self, *args, **kwargs)

    monkeypatch.setattr(torch.optim.AdamW, "step", counting_step)
    run_training(cfg)

    assert len(calls) == 7, (
        "expected exactly 7 optimizer steps (6 full windows + the partial "
        f"end-of-epoch window), got {len(calls)}"
    )
    latest = latest_checkpoint(Path(cfg.training.output_dir))
    assert latest is not None and latest.name == "step_7"


# ---------------------------------------------------------------------------
# Real (tiny) CPU training runs end-to-end
# ---------------------------------------------------------------------------
def test_cpu_training_run_completes_and_saves(tiny_run_config, capsys):
    cfg = tiny_run_config
    run_training(cfg)

    latest = latest_checkpoint(Path(cfg.training.output_dir))
    assert latest is not None and latest.name == "step_7"
    meta = json.loads((latest / "meta.json").read_text(encoding="utf-8"))
    assert meta["step"] == 7
    assert meta["checkpoint_format_version"] == 1
    assert meta["tokenizer_vocab_size"] == cfg.model.vocab_size

    out = capsys.readouterr().out
    # The meaningful from-scratch verification must have run and passed.
    assert "fresh random initialisation" in out


def test_cpu_training_eval_and_checkpoint_intervals(tiny_run_config):
    """eval_interval/eval_steps/checkpoint_interval all fire without error."""
    cfg = tiny_run_config
    cfg.training.eval_interval = 2
    cfg.training.eval_steps = 1   # cap each eval to ONE validation batch
    cfg.training.checkpoint_interval = 2
    run_training(cfg)

    out_dir = Path(cfg.training.output_dir)
    saved = sorted(p.name for p in out_dir.iterdir() if p.name.startswith("step_"))
    assert saved == ["step_2", "step_4", "step_6", "step_7"]
    assert (out_dir / "step_7" / "model.safetensors").exists()


# ---------------------------------------------------------------------------
# Checkpoint resume: validation BEFORE loading anything
# ---------------------------------------------------------------------------
def _write_checkpoint(tmp_path, config, step=2):
    model = AnkitModel(config.model)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    save_checkpoint(
        tmp_path, model, optimizer, None, step=step, config=config,
        tokenizer_version="v0.1", seed=config.training.seed,
        tokenizer_vocab_size=config.model.vocab_size,
    )
    return latest_checkpoint(tmp_path)


def test_resume_accepts_compatible_checkpoint(tmp_path, tiny_run_config):
    ckpt = _write_checkpoint(tmp_path, tiny_run_config, step=3)
    meta = validate_resume_checkpoint(
        ckpt, tiny_run_config, tiny_run_config.model.vocab_size
    )
    assert meta["step"] == 3


def test_resume_rejects_architecture_mismatch(tmp_path, tiny_run_config):
    ckpt = _write_checkpoint(tmp_path, tiny_run_config, step=3)
    changed = Config.from_dict(tiny_run_config.to_dict())
    changed.model.d_model = 64  # different architecture than the checkpoint
    with pytest.raises(ValueError, match="architecture"):
        validate_resume_checkpoint(ckpt, changed, tiny_run_config.model.vocab_size)


def test_resume_rejects_context_length_mismatch(tmp_path, tiny_run_config):
    ckpt = _write_checkpoint(tmp_path, tiny_run_config, step=3)
    changed = Config.from_dict(tiny_run_config.to_dict())
    changed.model.context_length = 32
    with pytest.raises(ValueError, match="context_length"):
        validate_resume_checkpoint(ckpt, changed, tiny_run_config.model.vocab_size)


def test_resume_rejects_tokenizer_vocab_mismatch(tmp_path, tiny_run_config):
    ckpt = _write_checkpoint(tmp_path, tiny_run_config, step=3)
    with pytest.raises(ValueError, match="vocab"):
        validate_resume_checkpoint(
            ckpt, tiny_run_config, tiny_run_config.model.vocab_size + 5
        )


def test_resume_rejects_foreign_checkpoint(tmp_path, tiny_run_config):
    foreign = tmp_path / "step_3"
    foreign.mkdir()
    (foreign / "meta.json").write_text("{}", encoding="utf-8")
    with pytest.raises(RuntimeError):
        validate_resume_checkpoint(
            foreign, tiny_run_config, tiny_run_config.model.vocab_size
        )


def test_resume_rejects_unknown_format_version(tmp_path, tiny_run_config):
    ckpt = _write_checkpoint(tmp_path, tiny_run_config, step=3)
    meta = json.loads((ckpt / "meta.json").read_text(encoding="utf-8"))
    meta["checkpoint_format_version"] = 999
    (ckpt / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    with pytest.raises(RuntimeError, match="format"):
        validate_resume_checkpoint(
            ckpt, tiny_run_config, tiny_run_config.model.vocab_size
        )


def test_run_training_refuses_foreign_checkpoint_dir(tiny_run_config):
    """A non-ANKIT 'checkpoint' in output_dir must abort, never load."""
    cfg = tiny_run_config
    out = Path(cfg.training.output_dir)
    (out / "step_3").mkdir(parents=True)
    (out / "step_3" / "meta.json").write_text("{}", encoding="utf-8")
    with pytest.raises(RuntimeError):
        run_training(cfg)


def test_resume_continues_exactly_where_it_left_off(tiny_run_config, monkeypatch):
    """Run 3 steps, 'interrupt', resume: exactly 2 more optimizer steps."""
    cfg = tiny_run_config
    cfg.training.total_steps = 3
    cfg.training.checkpoint_interval = 3
    run_training(cfg)  # fresh run -> step_3 checkpoint

    calls: list[int] = []
    original_step = torch.optim.AdamW.step

    def counting_step(self, *args, **kwargs):
        calls.append(id(self))
        return original_step(self, *args, **kwargs)

    monkeypatch.setattr(torch.optim.AdamW, "step", counting_step)
    cfg.training.total_steps = 5
    run_training(cfg)  # must resume from step 3, NOT restart from scratch

    assert len(calls) == 2
    latest = latest_checkpoint(Path(cfg.training.output_dir))
    assert latest.name == "step_5"
    meta = json.loads((latest / "meta.json").read_text(encoding="utf-8"))
    assert meta["step"] == 5


# ---------------------------------------------------------------------------
# Provenance: fresh-initialization + native-checkpoint verification
# ---------------------------------------------------------------------------
def test_fresh_model_passes_verification(tiny_run_config):
    torch.manual_seed(0)
    model = AnkitModel(tiny_run_config.model)
    verify_fresh_initialization(model, tiny_run_config.model, seed=0)


def test_tampered_weights_fail_verification(tiny_run_config):
    torch.manual_seed(0)
    model = AnkitModel(tiny_run_config.model)
    with torch.no_grad():
        model.token_embedding.embedding.weight[0, 0] += 1e-3
    with pytest.raises(RuntimeError, match="Fresh-initialization"):
        verify_fresh_initialization(model, tiny_run_config.model, seed=0)


def test_wrong_seed_fails_verification(tiny_run_config):
    torch.manual_seed(0)
    model = AnkitModel(tiny_run_config.model)
    with pytest.raises(RuntimeError, match="Fresh-initialization"):
        verify_fresh_initialization(model, tiny_run_config.model, seed=12345)


def test_fingerprint_is_deterministic_and_seed_sensitive(tiny_run_config):
    fp_a = fresh_model_fingerprint(tiny_run_config.model, seed=0)
    fp_b = fresh_model_fingerprint(tiny_run_config.model, seed=0)
    fp_c = fresh_model_fingerprint(tiny_run_config.model, seed=1)
    assert fp_a == fp_b
    assert fp_a != fp_c


def test_fingerprint_does_not_disturb_rng_state(tiny_run_config):
    torch.manual_seed(0)
    before = torch.get_rng_state()
    fresh_model_fingerprint(tiny_run_config.model, seed=99)
    assert torch.equal(torch.get_rng_state(), before)


def test_state_dict_fingerprint_covers_values():
    sd1 = {"w": torch.tensor([1.0, 2.0])}
    sd2 = {"w": torch.tensor([1.0, 2.0])}
    sd3 = {"w": torch.tensor([1.0, 2.5])}
    assert state_dict_fingerprint(sd1) == state_dict_fingerprint(sd2)
    assert state_dict_fingerprint(sd1) != state_dict_fingerprint(sd3)


def test_verify_ankit_checkpoint_rejects_missing_meta(tmp_path):
    with pytest.raises(RuntimeError, match="ANKIT checkpoint"):
        verify_ankit_checkpoint(tmp_path)


def test_verify_ankit_checkpoint_accepts_real_checkpoint(tmp_path, tiny_run_config):
    ckpt = _write_checkpoint(tmp_path, tiny_run_config, step=1)
    meta = verify_ankit_checkpoint(ckpt)
    assert meta["step"] == 1
    assert meta["model_config"]["vocab_size"] == tiny_run_config.model.vocab_size


def test_checkpoint_save_works_with_tied_embeddings(tmp_path, tiny_run_config):
    """tie_embedding=true (the ModelConfig default) shares one storage between
    the token embedding and the lm_head — the checkpoint must still save."""
    cfg = Config.from_dict(tiny_run_config.to_dict())
    cfg.model.tie_embedding = True
    model = AnkitModel(cfg.model)
    assert model.lm_head.weight is model.token_embedding.embedding.weight

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    save_checkpoint(
        tmp_path, model, optimizer, None, step=1, config=cfg,
        tokenizer_version="v0.1", seed=1,
        tokenizer_vocab_size=cfg.model.vocab_size,
    )
    from training.checkpoint import load_checkpoint_model

    model2, cfg2 = load_checkpoint_model(tmp_path, device="cpu")
    assert cfg2.model.tie_embedding is True
    model.eval(); model2.eval()
    x = torch.randint(0, cfg.model.vocab_size, (1, 8))
    with torch.no_grad():
        assert torch.allclose(model(x), model2(x), atol=1e-6)
