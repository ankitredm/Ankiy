"""Tests for tokenizer <-> model vocabulary alignment.

The model's output head and token embedding must cover EXACTLY the tokenizer's
vocabulary: every id the tokenizer can emit must be a valid model input, and
the model must not have output heads for ids the tokenizer can never produce.
"""

from __future__ import annotations

import pytest
import torch

from model import AnkitModel, Config
from tokenizer.tokenizer import align_model_vocab_size


def test_align_returns_tokenizer_vocab(tiny_tokenizer):
    cfg = Config.load("configs/smoke.yaml")
    assert align_model_vocab_size(cfg.model, tiny_tokenizer) == tiny_tokenizer.vocab_size


def test_model_built_with_aligned_vocab_accepts_every_tokenizer_id(tiny_tokenizer):
    cfg = Config.load("configs/smoke.yaml")
    cfg.model.vocab_size = align_model_vocab_size(cfg.model, tiny_tokenizer)
    cfg.model.context_length = 16
    model = AnkitModel(cfg.model)

    # The embedding table must cover every id the tokenizer can emit.
    embedding_rows = model.token_embedding.embedding.num_embeddings
    assert embedding_rows == tiny_tokenizer.vocab_size

    text = "The capital of France is Paris. The quick brown fox jumps."
    ids = tiny_tokenizer.encode(text, add_bos=True, add_eos=True)
    assert ids, "tokenizer produced no ids"
    assert all(0 <= i < embedding_rows for i in ids), "tokenizer id outside model vocab"

    # A real encoded window must run through the model without index errors.
    window = ids[:16] if len(ids) >= 16 else ids + [tiny_tokenizer.pad_id] * (16 - len(ids))
    x = torch.tensor([window], dtype=torch.long)
    logits = model(x)
    assert logits.shape == (1, 16, cfg.model.vocab_size)
    assert torch.isfinite(logits).all()


def test_model_and_tokenizer_roundtrip_consistency(tiny_tokenizer):
    """encode -> model-size check -> decode stays consistent for aligned vocab."""
    cfg = Config.load("configs/smoke.yaml")
    cfg.model.vocab_size = align_model_vocab_size(cfg.model, tiny_tokenizer)
    model = AnkitModel(cfg.model)

    assert model.config.vocab_size == tiny_tokenizer.vocab_size
    text = "hello world"
    ids = tiny_tokenizer.encode(text)
    assert tiny_tokenizer.decode(ids).strip() == text


def test_misaligned_vocab_causes_index_error(tiny_tokenizer):
    """A model SMALLER than the tokenizer vocab cannot embed late ids — this
    is exactly the bug vocab alignment prevents."""
    cfg = Config.load("configs/smoke.yaml")
    cfg.model.vocab_size = tiny_tokenizer.vocab_size - 1
    cfg.model.context_length = 16
    model = AnkitModel(cfg.model)

    # The tokenizer's highest id is outside the (misaligned) model's vocab.
    top_id = tiny_tokenizer.vocab_size - 1
    x = torch.full((1, 16), top_id, dtype=torch.long)
    with pytest.raises(IndexError):
        model(x)
