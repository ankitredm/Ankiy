"""Training data handling for ANKIT 0.1.

We store each split as one long 1-D array of token ids (uint16). This module
loads it with ``np.memmap`` (so huge corpora don't need to sit in RAM) and
produces fixed-length training examples:

    given a window of ``context_length`` tokens:
        x = tokens[i : i + context_length]      (what the model sees)
        y = tokens[i + 1 : i + context_length + 1]   (the next token to predict)

This is "causal next-token prediction": the target is always the token exactly
one position ahead of the input.

The whole thing runs on CPU; only the training loop (train.py) moves tensors to
the GPU.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset


class TokenDataset(Dataset):
    """A fixed-length next-token dataset from a .bin token stream."""

    def __init__(self, path: str | Path, context_length: int) -> None:
        self.path = str(path)
        self.context_length = context_length
        if not Path(path).exists():
            raise FileNotFoundError(
                f"Token data not found: {path}. Run "
                "`python scripts/tokenize_dataset.py` first."
            )
        # memmap keeps the file on disk while we read windows from it.
        self.data = np.memmap(path, dtype=np.uint16, mode="r")
        # An example needs context_length+1 tokens (input + one target).
        self.num_examples = max(0, len(self.data) - context_length)

    def __len__(self) -> int:
        return self.num_examples

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        if idx < 0 or idx >= self.num_examples:
            raise IndexError(
                f"Index {idx} out of range for dataset of {self.num_examples} examples."
            )
        # Slice a (context_length + 1) window.
        window = self.data[idx : idx + self.context_length + 1]
        x = torch.from_numpy(window[:-1].astype(np.int64))  # input
        y = torch.from_numpy(window[1:].astype(np.int64))   # target (shifted)
        return x, y


def collate_batch(
    batch: list[tuple[torch.Tensor, torch.Tensor]]
) -> tuple[torch.Tensor, torch.Tensor]:
    """Stack a list of (x, y) pairs into a padded batch tensor.

    All examples already have the same length (context_length) because we use a
    fixed window, so stacking is trivial. This exists mainly so the data loader
    has an explicit collate function (and room to add padding later).
    """
    xs = torch.stack([item[0] for item in batch])
    ys = torch.stack([item[1] for item in batch])
    return xs, ys
