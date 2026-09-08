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
    assert cfg.model.n_layers == 10
    assert cfg.training.device in ("cuda", "cpu", "auto")


def test_ankit_config_is_the_50m_target():
    """The ANKIT 0.1 config must build the intended ~50M model.

    Exact expectation (untied head, no biases, vocab 16384, ctx 256):
        token embedding : 16384 * 512        =  8,388,608
        pos  embedding  :   256 * 512        =    131,072
        per block       : 4*512^2 (attn)
                          + 2*512*2048 (ffn)
                          + 2*2*512  (norms) =  3,147,776  x 10 layers
        final norm      :                    =      1,024
        output head     :   512 * 16384      =  8,388,608
        total                                = 48,387,072  (~48.4M)
    """
    from model import AnkitModel

    cfg = Config.load("configs/ankit_0_1.yaml")
    m = AnkitModel(cfg.model)
    n = m.num_parameters()

    assert n == 48_387_072, (
        f"ANKIT 0.1 should be the documented ~48.4M build, got {n:,}. "
        "If you intentionally changed configs/ankit_0_1.yaml, update this "
        "test AND the parameter breakdown comment in the config."
    )
    # Belt-and-braces: the documented target band.
    assert 45_000_000 <= n <= 52_000_000, f"Parameter count {n:,} out of ~50M range"
