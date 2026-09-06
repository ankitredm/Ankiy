"""ANKIT 0.1 model package.

Public API:
    AnkitModel  — the full decoder-only Transformer
    ModelConfig / TrainingConfig / Config — config dataclasses
"""

from model.ankit_model import AnkitModel
from model.config import Config, ModelConfig, TrainingConfig
from model.transformer import TransformerBlock

__all__ = [
    "AnkitModel",
    "Config",
    "ModelConfig",
    "TrainingConfig",
    "TransformerBlock",
]
