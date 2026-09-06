"""Deterministic train / validation / test splitting."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence


@dataclass
class SplitConfig:
    train_ratio: float = 0.90
    val_ratio: float = 0.05
    test_ratio: float = 0.05
    shuffle: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "SplitConfig":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})

    def validate(self) -> None:
        total = self.train_ratio + self.val_ratio + self.test_ratio
        if abs(total - 1.0) > 1e-9:
            raise ValueError(
                f"Split ratios must sum to 1.0, got {total:.4f} "
                f"(train={self.train_ratio}, val={self.val_ratio}, test={self.test_ratio})"
            )
        if min(self.train_ratio, self.val_ratio, self.test_ratio) < 0:
            raise ValueError("Split ratios must be non-negative.")


def split_documents(
    texts: Sequence[str], config: SplitConfig, seed: int = 1337
) -> dict[str, list[str]]:
    """Split documents into train/val/test with a fixed seed for reproducibility."""
    config.validate()
    indices = list(range(len(texts)))
    if config.shuffle:
        rng = random.Random(seed)
        rng.shuffle(indices)

    n = len(texts)
    n_train = int(round(config.train_ratio * n))
    n_val = int(round(config.val_ratio * n))
    n_test = n - n_train - n_val

    train_idx = indices[:n_train]
    val_idx = indices[n_train : n_train + n_val]
    test_idx = indices[n_train + n_val :]

    return {
        "train": [texts[i] for i in train_idx],
        "val": [texts[i] for i in val_idx],
        "test": [texts[i] for i in test_idx],
    }
