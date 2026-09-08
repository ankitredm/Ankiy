"""Configuration for the ANKIT 0.1 model and its training run.

Everything that defines "how big is the model" and "how do we train it" lives
in a YAML file under ``configs/``. We load that YAML here into a plain
dataclass so the rest of the code never sees raw dictionaries or hard-coded
numbers.

The rule is: **no magic numbers scattered through the code**. You change the
model size, the context length, the learning rate, etc. by editing the YAML,
not by editing source files. (For example ``configs/ankit_0_1.yaml``.)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

# ---------------------------------------------------------------------------
# Small helpers.
#
# PyYAML silently reads ``6e-4`` (no decimal point) as a string, which would
# break numeric checks. These helpers coerce any "string that is actually a
# number" back into a real number so a beginner's config file just works.
# ---------------------------------------------------------------------------


def _num(value: Any, cast: type) -> Any:
    """Coerce a value to ``cast`` if it looks like a number (even as a string)."""
    if isinstance(value, str):
        try:
            return cast(value)
        except ValueError:
            return value  # leave it; validation will complain
    return value


def _default_ffn_dim(d_model: int, ffn_dim: Optional[int]) -> int:
    if ffn_dim is not None and ffn_dim > 0:
        return int(ffn_dim)
    return 4 * d_model


@dataclass
class ModelConfig:
    """Architecture hyper-parameters for one ANKIT model."""

    vocab_size: int = 16384
    d_model: int = 256
    n_layers: int = 6
    n_heads: int = 8
    context_length: int = 256
    ffn_dim: Optional[int] = None  # if None -> 4 * d_model
    activation: str = "gelu"  # "gelu" or "silu"
    dropout: float = 0.1
    norm_eps: float = 1e-5
    init_std: float = 0.02
    tie_embedding: bool = True  # tie the output head to the token embedding
    use_bias: bool = False  # bias in linear layers (False = modern convention)

    def __post_init__(self) -> None:
        # Coerce values that PyYAML read as strings back into real numbers.
        self.vocab_size = _num(self.vocab_size, int)
        self.d_model = _num(self.d_model, int)
        self.n_layers = _num(self.n_layers, int)
        self.n_heads = _num(self.n_heads, int)
        self.context_length = _num(self.context_length, int)
        self.ffn_dim = _num(self.ffn_dim, int)
        self.dropout = _num(self.dropout, float)
        self.norm_eps = _num(self.norm_eps, float)
        self.init_std = _num(self.init_std, float)
        # Resolve ffn_dim early so the rest of the code always sees an int.
        self.ffn_dim = _default_ffn_dim(self.d_model, self.ffn_dim)
        self.validate()

    @property
    def head_dim(self) -> int:
        """Size of a single attention head."""
        return self.d_model // self.n_heads

    def validate(self) -> None:
        if self.vocab_size <= 0:
            raise ValueError("ModelConfig.vocab_size must be positive.")
        if self.d_model <= 0:
            raise ValueError("ModelConfig.d_model must be positive.")
        if self.n_layers < 1:
            raise ValueError("ModelConfig.n_layers must be at least 1.")
        if self.n_heads < 1:
            raise ValueError("ModelConfig.n_heads must be at least 1.")
        if self.d_model % self.n_heads != 0:
            raise ValueError(
                f"d_model ({self.d_model}) must be divisible by n_heads ({self.n_heads})."
            )
        if self.context_length < 1:
            raise ValueError("ModelConfig.context_length must be positive.")
        if self.activation not in ("gelu", "silu"):
            raise ValueError(f"Unsupported activation: {self.activation!r}")
        if not (0.0 <= self.dropout < 1.0):
            raise ValueError("ModelConfig.dropout must be in [0, 1).")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModelConfig":
        """Build a config from a dict, ignoring unknown keys for forward-compat."""
        known = {
            key for key in cls.__dataclass_fields__  # type: ignore[attr-defined]
        }
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)


@dataclass
class TrainingConfig:
    """Optimisation / loop settings. Many fields are used later (training)."""

    batch_size: int = 8
    grad_accumulation_steps: int = 1
    learning_rate: float = 6e-4
    weight_decay: float = 0.1
    warmup_steps: int = 100
    total_steps: int = 5000
    checkpoint_interval: int = 500
    eval_interval: int = 100
    eval_steps: int = 50
    max_grad_norm: float = 1.0
    seed: int = 1337
    precision: str = "bf16"  # "fp32", "fp16", "bf16"
    device: str = "cuda"  # "cuda" or "cpu"
    output_dir: str = "checkpoints"
    tokenizer_path: str = "tokenizer/ankit_tokenizer.json"
    train_data: str = "data/tokenized/train.bin"
    val_data: str = "data/tokenized/val.bin"
    test_data: str = "data/tokenized/test.bin"

    def __post_init__(self) -> None:
        # Coerce values that PyYAML read as strings back into real numbers.
        self.batch_size = _num(self.batch_size, int)
        self.grad_accumulation_steps = _num(self.grad_accumulation_steps, int)
        self.learning_rate = _num(self.learning_rate, float)
        self.weight_decay = _num(self.weight_decay, float)
        self.warmup_steps = _num(self.warmup_steps, int)
        self.total_steps = _num(self.total_steps, int)
        self.test_data = str(self.test_data)
        self.checkpoint_interval = _num(self.checkpoint_interval, int)
        self.eval_interval = _num(self.eval_interval, int)
        self.eval_steps = _num(self.eval_steps, int)
        self.max_grad_norm = _num(self.max_grad_norm, float)
        self.seed = _num(self.seed, int)
        self.validate()

    def validate(self) -> None:
        if self.batch_size < 1:
            raise ValueError("TrainingConfig.batch_size must be positive.")
        if self.grad_accumulation_steps < 1:
            raise ValueError(
                "TrainingConfig.grad_accumulation_steps must be at least 1 "
                f"(got {self.grad_accumulation_steps})."
            )
        if self.learning_rate <= 0:
            raise ValueError("TrainingConfig.learning_rate must be positive.")
        if self.total_steps < 1:
            raise ValueError("TrainingConfig.total_steps must be at least 1.")
        if self.warmup_steps < 0:
            raise ValueError("TrainingConfig.warmup_steps must be >= 0.")
        if self.checkpoint_interval < 0 or self.eval_interval < 0:
            raise ValueError(
                "TrainingConfig.checkpoint_interval / eval_interval must be >= 0 "
                "(0 disables the interval)."
            )
        if self.eval_steps < 0:
            raise ValueError(
                "TrainingConfig.eval_steps must be >= 0 (0 = use the full "
                "validation set at every eval)."
            )
        if self.max_grad_norm <= 0:
            raise ValueError("TrainingConfig.max_grad_norm must be positive.")
        if self.weight_decay < 0:
            raise ValueError("TrainingConfig.weight_decay must be >= 0.")
        if self.precision not in ("fp32", "fp16", "bf16"):
            raise ValueError(f"Unsupported precision: {self.precision!r}")
        if self.device not in ("cuda", "cpu", "auto"):
            raise ValueError(f"Unsupported device: {self.device!r}")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrainingConfig":
        known = {key for key in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)


@dataclass
class Config:
    """Top-level config: model + training + a small provenance block."""

    model: ModelConfig
    training: TrainingConfig
    name: str = "ankit-0-1"
    git_commit: str = ""
    dataset_version: str = ""
    tokenizer_version: str = ""
    notes: str = ""

    @classmethod
    def load(cls, path: str | Path) -> "Config":
        """Load a YAML config file into a validated Config object."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with path.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle) or {}
        if not isinstance(raw, dict):
            raise ValueError(f"Config file {path} must contain a YAML mapping.")
        return cls.from_dict(raw)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        model_data = data.get("model", {})
        training_data = data.get("training", {})
        if not model_data:
            raise ValueError("Config is missing the 'model' section.")
        if not training_data:
            raise ValueError("Config is missing the 'training' section.")
        model_cfg = ModelConfig.from_dict(model_data)
        training_cfg = TrainingConfig.from_dict(training_data)
        training_cfg.validate()
        return cls(
            model=model_cfg,
            training=training_cfg,
            name=str(data.get("name", "ankit-0-1")),
            git_commit=str(data.get("git_commit", "")),
            dataset_version=str(data.get("dataset_version", "")),
            tokenizer_version=str(data.get("tokenizer_version", "")),
            notes=str(data.get("notes", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise back to a plain dict (useful for checkpoints/metadata)."""
        return {
            "name": self.name,
            "git_commit": self.git_commit,
            "dataset_version": self.dataset_version,
            "tokenizer_version": self.tokenizer_version,
            "notes": self.notes,
            "model": self.model.__dict__,
            "training": self.training.__dict__,
        }
