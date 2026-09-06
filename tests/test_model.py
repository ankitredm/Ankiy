"""Tests for the ANKIT 0.1 decoder-only Transformer."""

from __future__ import annotations

import torch

from model import AnkitModel, Config


def _model(ctx_len: int = 16) -> AnkitModel:
    cfg = Config.load("configs/smoke.yaml")
    cfg.model.context_length = ctx_len
    return AnkitModel(cfg.model)


def test_forward_shape():
    model = _model()
    vocab = model.config.vocab_size
    x = torch.randint(0, vocab, (2, 16))
    logits = model(x)
    assert logits.shape == (2, 16, vocab)
    assert logits.dtype == torch.float32


def test_forward_rejects_too_long():
    import pytest

    model = _model(ctx_len=8)
    x = torch.randint(0, model.config.vocab_size, (1, 16))
    with pytest.raises(ValueError):
        model(x)


def test_causal_mask_triangular():
    model = _model()
    mask = model.blocks[0].attn.causal_mask  # 1 = hidden
    visible = mask == 0
    for t in range(12):
        assert int(visible[t, : t + 1].sum()) == t + 1
        # nothing before 0 is visible; nothing after t
        assert int(visible[t, t + 1 :].sum()) == 0


def test_loss_backward_works():
    model = _model()
    vocab = model.config.vocab_size
    x = torch.randint(0, vocab, (2, 16))
    y = torch.randint(0, vocab, (2, 16))
    logits = model(x)
    loss = torch.nn.functional.cross_entropy(
        logits.reshape(-1, vocab), y.reshape(-1)
    )
    loss.backward()
    grads = [p.grad for p in model.parameters() if p.grad is not None]
    assert len(grads) > 0  # at least some parameters got gradients
    assert all(torch.isfinite(g).all() for g in grads)


def test_generation_returns_longer_sequence():
    model = _model()
    prompt = torch.randint(0, model.config.vocab_size, (1, 4))
    out = model.generate(prompt, max_new_tokens=8, seed=1)
    assert out.shape[1] == 4 + 8


def test_num_parameters_reported():
    model = _model()
    total = model.num_parameters()
    assert total > 0
    # Matches the actual sum of parameters in the module.
    assert total == sum(p.numel() for p in model.parameters())


def test_checkpoint_roundtrip(tmp_path):
    """Save then reload the model and verify predictions are identical."""
    model = _model()
    path = tmp_path / "model.pt"
    torch.save(model.state_dict(), path)

    model2 = _model()
    model2.load_state_dict(torch.load(path, weights_only=True))

    # Both must be in eval() so dropout is disabled during the comparison.
    model.eval()
    model2.eval()
    x = torch.randint(0, model.config.vocab_size, (1, 8))
    with torch.no_grad():
        a = model(x)
        b = model2(x)
    assert torch.allclose(a, b, atol=1e-6), "Reloaded model differs from original"
