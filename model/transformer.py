"""The Transformer building block (a single decoder layer) and the FFN.

We use the "pre-norm" layout, which is the modern convention:

    x = x + attn(norm(x))
    x = x + ffn(norm(x))

Pre-norm places each LayerNorm *before* the attention / feed-forward. It is
more stable to train than the older post-norm layout.
"""

from __future__ import annotations

import torch
from torch import nn

from model.attention import CausalSelfAttention
from model.config import ModelConfig


class FeedForward(nn.Module):
    """Two linear layers with a non-linearity in between."""

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        bias = config.use_bias
        self.fc1 = nn.Linear(config.d_model, config.ffn_dim, bias=bias)
        self.fc2 = nn.Linear(config.ffn_dim, config.d_model, bias=bias)
        self.dropout = nn.Dropout(config.dropout)
        if config.activation == "gelu":
            self.activation = nn.GELU()
        elif config.activation == "silu":
            self.activation = nn.SiLU()
        else:  # default to GELU (validated in ModelConfig anyway)
            self.activation = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.dropout(self.fc2(self.activation(self.fc1(x))))


class TransformerBlock(nn.Module):
    """One decoder layer: pre-norm attention + pre-norm feed-forward."""

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.norm1 = nn.LayerNorm(config.d_model, eps=config.norm_eps)
        self.attn = CausalSelfAttention(config)
        self.norm2 = nn.LayerNorm(config.d_model, eps=config.norm_eps)
        self.ffn = FeedForward(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-norm attention with residual skip.
        x = x + self.attn(self.norm1(x))
        # Pre-norm feed-forward with residual skip.
        x = x + self.ffn(self.norm2(x))
        return x
