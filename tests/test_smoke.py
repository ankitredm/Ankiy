"""Tests for the smoke-test plumbing (independent of the full training chain)."""

from __future__ import annotations

import pytest

from model.config import Config


def test_smoke_config_loads():
    cfg = Config.load("configs/smoke.yaml")
    assert cfg.model.n_layers == 2
    assert cfg.model.context_length == 64
    assert cfg.training.total_steps == 20
    assert cfg.training.checkpoint_interval == 5


def test_ankit_config_loads():
    cfg = Config.load("configs/ankit_0_1.yaml")
    assert cfg.model.vocab_size == 16384
    assert cfg.model.n_layers == 6
    assert cfg.training.device in ("cuda", "cpu")


def test_ankit_config_in_target_range():
    """The target model must be in the 10M-100M parameter range we documented."""
    cfg = Config.load("configs/ankit_0_1.yaml")
    # Build the model to get a REAL parameter count.
    from model import AnkitModel
    m = AnkitModel(cfg.model)
    n = m.num_parameters()
    # The config's nominal 13.18M (with vocab 16384) is within 10M-100M.
    assert 10_000_000 <= n <= 100_000_000, f"Parameter count {n:,} out of target range"
