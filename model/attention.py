"""Causal multi-head self-attention.

This is the "look at other words in the sequence" part of a Transformer.
We implement it ourselves with PyTorch tensor ops (no attention library).

Key idea for a *causal* model: during training a token may only look at
itself and the tokens before it — it must NOT see future tokens (otherwise
it would just copy the answer from later in the sequence). We enforce that
with a triangular mask.
"""

from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F

from model.config import ModelConfig


class CausalSelfAttention(nn.Module):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        assert config.d_model % config.n_heads == 0
        self.n_heads = config.n_heads
        self.head_dim = config.head_dim
        self.dropout = config.dropout
        bias = config.use_bias

        # Four projection matrices: query, key, value, output.
        self.q_proj = nn.Linear(config.d_model, config.d_model, bias=bias)
        self.k_proj = nn.Linear(config.d_model, config.d_model, bias=bias)
        self.v_proj = nn.Linear(config.d_model, config.d_model, bias=bias)
        self.o_proj = nn.Linear(config.d_model, config.d_model, bias=bias)
        self.resid_dropout = nn.Dropout(config.dropout)

        # A reusable causal mask. We register it as a buffer (not a parameter)
        # so it moves to the right device automatically with the model.
        mask = torch.ones(config.context_length, config.context_length)
        mask = torch.triu(mask, diagonal=1)  # 1 above the diagonal (to hide)
        self.register_buffer("causal_mask", mask, persistent=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.shape
        # Project to query/key/value and split into heads.
        # shape: (B, T, n_heads, head_dim) -> (B, n_heads, T, head_dim)
        q = self.q_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        # Scaled dot-product attention:  q @ k^T / sqrt(head_dim)
        att = (q @ k.transpose(-2, -1)) * (self.head_dim ** -0.5)

        # Hide future positions with the causal mask (only the first T positions).
        mask = self.causal_mask[:T, :T]
        att = att.masked_fill(mask.bool(), float("-inf"))

        att = F.softmax(att, dim=-1)
        att = F.dropout(att, p=self.dropout, training=self.training)

        # Combine values:  att @ v
        y = att @ v  # (B, n_heads, T, head_dim)
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.resid_dropout(self.o_proj(y))
        return y
