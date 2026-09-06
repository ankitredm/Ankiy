"""Tests for model.config — parsing and validation."""

from __future__ import annotations

import pytest

from model.config import Config


def test_load_ankit_config():
    cfg = Config.load("configs/ankit_0_1.yaml")
    assert cfg.model.vocab_size == 16384
    assert cfg.model.d_model == 256
    assert cfg.model.n_layers == 6
    assert cfg.model.n_heads == 8
    assert cfg.model.context_length == 256
    assert cfg.model.ffn_dim == 1024
    assert cfg.model.head_dim == 32  # 256 / 8


def test_load_smoke_config():
    cfg = Config.load("configs/smoke.yaml")
    assert cfg.model.vocab_size == 512
    assert cfg.model.d_model == 64
    assert cfg.model.n_layers == 2


def test_scientific_notation_is_coerced():
    # Ensure "6e-4" (which PyYAML reads as a string) becomes a float.
    data = {
        "model": {
            "vocab_size": 100,
            "d_model": 32,
            "n_layers": 1,
            "n_heads": 2,
            "context_length": 16,
            "ffn_dim": None,
        },
        "training": {
            "batch_size": 2,
            "learning_rate": "6e-4",  # string on purpose
            "device": "cpu",
        },
    }
    cfg = Config.from_dict(data)
    assert isinstance(cfg.training.learning_rate, float)
    assert cfg.training.learning_rate == 0.0006


def test_ffn_dim_defaults_to_4x():
    cfg = Config.load("configs/smoke.yaml")
    assert cfg.model.ffn_dim == 256  # 4 * 64


def test_validate_rejects_non_divisible_heads():
    with pytest.raises(ValueError):
        Config.from_dict(
            {
                "model": {
                    "vocab_size": 100,
                    "d_model": 64,
                    "n_layers": 1,
                    "n_heads": 3,  # 64 / 3 is not whole
                    "context_length": 16,
                    "ffn_dim": 128,
                },
                "training": {"batch_size": 2, "learning_rate": 0.001},
            }
        )


def test_validate_rejects_bad_activation():
    with pytest.raises(ValueError):
        Config.from_dict(
            {
                "model": {
                    "vocab_size": 100,
                    "d_model": 64,
                    "n_layers": 1,
                    "n_heads": 4,
                    "context_length": 16,
                    "activation": "relu",  # not supported
                },
                "training": {"batch_size": 2, "learning_rate": 0.001},
            }
        )
