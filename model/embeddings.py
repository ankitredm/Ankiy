"""Embeddings for ANKIT 0.1.

A decoder-only model turns tokens into vectors and adds a *positional*
signal so the model knows the order of words. We use two simple learned
lookup tables:

    token embedding      : (vocab_size, d_model)
    positional embedding : (context_length, d_model)

Both are ordinary PyTorch ``nn.Embedding`` modules — our own, from random
initialisation. No pretrained embedding is loaded anywhere.
"""

from __future__ import annotations

import torch
from torch import nn

from model.config import ModelConfig


class TokenEmbedding(nn.Module):
    """Map token ids to dense vectors."""

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        return self.dropout(self.embedding(token_ids))


class PositionalEmbedding(nn.Module):
    """Map positions (0..context_length-1) to learned vectors."""

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.embedding = nn.Embedding(config.context_length, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, positions: torch.Tensor) -> torch.Tensor:
        return self.dropout(self.embedding(positions))
