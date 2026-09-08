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


def _minimal_config(**training_overrides):
    training = {
        "batch_size": 2,
        "learning_rate": 0.001,
        "total_steps": 10,
        "device": "cpu",
    }
    training.update(training_overrides)
    return {
        "model": {
            "vocab_size": 100,
            "d_model": 32,
            "n_layers": 1,
            "n_heads": 2,
            "context_length": 16,
        },
        "training": training,
    }


def test_validate_rejects_zero_grad_accumulation_steps():
    with pytest.raises(ValueError, match="grad_accumulation_steps"):
        Config.from_dict(_minimal_config(grad_accumulation_steps=0))


def test_validate_rejects_negative_grad_accumulation_steps():
    with pytest.raises(ValueError, match="grad_accumulation_steps"):
        Config.from_dict(_minimal_config(grad_accumulation_steps=-2))


def test_validate_rejects_zero_total_steps():
    with pytest.raises(ValueError, match="total_steps"):
        Config.from_dict(_minimal_config(total_steps=0))


def test_validate_rejects_negative_warmup_steps():
    with pytest.raises(ValueError, match="warmup_steps"):
        Config.from_dict(_minimal_config(warmup_steps=-1))


def test_validate_rejects_negative_intervals():
    with pytest.raises(ValueError, match="interval"):
        Config.from_dict(_minimal_config(checkpoint_interval=-1, eval_interval=0))
    with pytest.raises(ValueError, match="interval"):
        Config.from_dict(_minimal_config(eval_interval=-5))


def test_validate_rejects_negative_eval_steps():
    with pytest.raises(ValueError, match="eval_steps"):
        Config.from_dict(_minimal_config(eval_steps=-1))


def test_validate_accepts_zero_intervals_and_eval_steps():
    # 0 disables mid-run evals/checkpoints and means "full val set" — legal.
    cfg = Config.from_dict(
        _minimal_config(checkpoint_interval=0, eval_interval=0, eval_steps=0)
    )
    assert cfg.training.checkpoint_interval == 0
    assert cfg.training.eval_interval == 0
    assert cfg.training.eval_steps == 0


def test_validate_rejects_bad_max_grad_norm_and_weight_decay():
    with pytest.raises(ValueError, match="max_grad_norm"):
        Config.from_dict(_minimal_config(max_grad_norm=0))
    with pytest.raises(ValueError, match="weight_decay"):
        Config.from_dict(_minimal_config(weight_decay=-0.1))
