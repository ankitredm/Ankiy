"""Tests for model.config — parsing and validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from model.config import Config


def test_load_ankit_config():
    cfg = Config.load("configs/ankit_0_1.yaml")
    assert cfg.model.vocab_size == 16384
    assert cfg.model.d_model == 512
    assert cfg.model.n_layers == 10
    assert cfg.model.n_heads == 8
    assert cfg.model.context_length == 256
    assert cfg.model.ffn_dim == 2048
    assert cfg.model.head_dim == 64  # 512 / 8


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


# ---------------------------------------------------------------------------
# Curriculum stage configs: one continuous schedule across the 6 stages
# ---------------------------------------------------------------------------
def _stage_config_paths():
    return sorted(Path("configs/curriculum").glob("stage*.yaml"))


def test_all_stage_configs_load_and_share_architecture():
    from model.config import Config

    base = Config.load("configs/ankit_0_1.yaml")
    paths = _stage_config_paths()
    assert len(paths) == 6, "expected exactly 6 curriculum stage configs"
    for path in paths:
        cfg = Config.load(path)
        assert cfg.model.__dict__ == base.model.__dict__, (
            f"{path} must use the SAME ~50M architecture as configs/ankit_0_1.yaml"
        )
        assert cfg.training.output_dir == base.training.output_dir, (
            f"{path} must write to the shared output_dir so stages chain via resume"
        )


def test_stage_steps_increase_monotonically():
    """Stage total_steps are CUMULATIVE targets (3000 -> ... -> 24000).

    Each stage decays cosine to its own horizon; on resume the rebuilt
    LambdaLR recomputes from the new horizon — a cosine warm-restart
    (SGDR-style) schedule across the curriculum.
    """
    from model.config import Config

    steps = [Config.load(path).training.total_steps for path in _stage_config_paths()]
    assert steps == sorted(steps), "stage total_steps must be cumulative/increasing"
    assert len(set(steps)) == 6, "each stage must add training steps"
    assert steps[-1] == 24000, "the final curriculum step should be 24000"


def test_stage_data_paths_are_distinct_and_declared():
    from model.config import Config

    seen = set()
    for path in _stage_config_paths():
        cfg = Config.load(path)
        assert cfg.training.train_data not in seen or len(seen) == 0
        seen.add(cfg.training.train_data)
        assert cfg.training.val_data.endswith("val.bin")
    # Stages 1-6 must point at six different training files.
    assert len(seen) == 6


@pytest.mark.skipif(
    not Path("data/tokenized/curriculum/stage1_train.bin").exists(),
    reason="run scripts/build_curriculum.py + scripts/tokenize_curriculum.py first",
)
def test_stage_data_files_exist():
    from model.config import Config

    for path in _stage_config_paths():
        cfg = Config.load(path)
        assert Path(cfg.training.train_data).exists(), cfg.training.train_data
        assert Path(cfg.training.val_data).exists()
