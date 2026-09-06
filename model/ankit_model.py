"""ANKIT 0.1 — the decoder-only language model.

Everything here is OUR OWN implementation, built from randomly initialised
weights. There is no pretrained checkpoint loaded anywhere in this file.

Architecture summary
--------------------
  token embedding  (vocab_size, d_model)
  positional embedding  (context_length, d_model)
  ┌  N ×  TransformerBlock (pre-norm causal self-attention + feed-forward)
  final LayerNorm
  output head  (d_model -> vocab_size)   [optionally tied to the token embedding]

Forward pass purpose (causal next-token prediction):
    input  : "|  The  capital  of  France  is"
    target : "   capital  of  France  is   Paris"
    The model outputs a score for every token in the vocabulary at each
    position; training pushes the score of the *correct* next token up.
"""

from __future__ import annotations

import torch
from torch import nn

from model.config import ModelConfig
from model.embeddings import PositionalEmbedding, TokenEmbedding
from model.transformer import TransformerBlock


class AnkitModel(nn.Module):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.config = config

        self.token_embedding = TokenEmbedding(config)
        self.position_embedding = PositionalEmbedding(config)
        self.blocks = nn.ModuleList(
            [TransformerBlock(config) for _ in range(config.n_layers)]
        )
        self.final_norm = nn.LayerNorm(config.d_model, eps=config.norm_eps)

        # Output head: map the final hidden state to a score per vocab token.
        if config.tie_embedding:
            # Reuse the token embedding weights so the count stays small.
            self.lm_head = nn.Linear(
                config.d_model, config.vocab_size, bias=config.use_bias
            )
            self.lm_head.weight = self.token_embedding.embedding.weight
        else:
            self.lm_head = nn.Linear(
                config.d_model, config.vocab_size, bias=config.use_bias
            )

        self.apply(self._init_weights)

    # -- initialisation -------------------------------------------------
    def _init_weights(self, module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=self.config.init_std)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=self.config.init_std)

    # -- forward ---------------------------------------------------------
    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        """Return logits of shape (batch, time, vocab_size)."""
        B, T = token_ids.shape
        if T > self.config.context_length:
            raise ValueError(
                f"Sequence length {T} exceeds model context "
                f"{self.config.context_length}. Use a shorter sequence."
            )
        positions = torch.arange(T, device=token_ids.device).unsqueeze(0)
        x = self.token_embedding(token_ids) + self.position_embedding(positions)
        for block in self.blocks:
            x = block(x)
        x = self.final_norm(x)
        logits = self.lm_head(x)
        return logits

    # -- helper: number of trainable parameters ---------------------------
    def num_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    # -- simple generation for smoke tests ---------------------------------
    @torch.no_grad()
    def generate(
        self,
        token_ids: torch.Tensor,
        max_new_tokens: int,
        temperature: float = 1.0,
        top_k: int | None = None,
        top_p: float | None = None,
        repetition_penalty: float = 1.0,
        seed: int | None = None,
    ) -> torch.Tensor:
        """Greedy/temperature sampling used for quick checks.

        The full, polished CLI generator lives in ``generate.py``; this method
        exists so the model can be smoke-tested in isolation.
        """
        self.eval()
        if seed is not None:
            torch.manual_seed(seed)
        for _ in range(max_new_tokens):
            # Only ever feed the most recent context_length tokens.
            window = token_ids[:, -self.config.context_length :]
            logits = self(window)[:, -1, :]  # (B, vocab)

            # Repetition penalty.
            if repetition_penalty != 1.0:
                for i in range(token_ids.shape[1] - 1, -1, -1):
                    logits[0, int(token_ids[0, i])] /= repetition_penalty

            logits = logits.float()
            logits = logits / max(temperature, 1e-5)

            # Top-k filtering.
            if top_k is not None and top_k > 0:
                top_k = min(top_k, logits.size(-1))
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = float("-inf")

            # Top-p (nucleus) filtering.
            if top_p is not None and 0.0 < top_p < 1.0:
                sorted_logits, sorted_idx = torch.sort(logits, descending=True)
                probs = torch.softmax(sorted_logits, dim=-1)
                cum = torch.cumsum(probs, dim=-1)
                mask = cum - probs > top_p
                sorted_logits[mask] = float("-inf")
                logits = sorted_logits.scatter(1, sorted_idx, sorted_logits)

            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            token_ids = torch.cat([token_ids, next_token], dim=1)
        return token_ids
