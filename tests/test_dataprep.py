"""Tests for the ANKIT 0.1 data preparation pipeline."""

from __future__ import annotations

import json
import random

import pytest

from dataprep import dedup, quality, split
from dataprep.pipeline import run_pipeline


# ---------------------------------------------------------------------------
# Cleaning
# ---------------------------------------------------------------------------
@pytest.fixture
def clean_cfg() -> quality.CleaningConfig:
    return quality.CleaningConfig()


def test_clean_removes_urls_and_html(clean_cfg):
    text = "Hello <b>world</b> visit https://example.com now"
    out = quality.clean_document(text, clean_cfg)
    assert "https" not in out
    assert "<b>" not in out
    assert "Hello world" in out


def test_clean_normalizes_newlines(clean_cfg):
    out = quality.clean_document("line1\r\nline2\rline3", clean_cfg)
    assert "\r" not in out
    assert "\n" in out


def test_clean_collapses_whitespace_and_bom(clean_cfg):
    out = quality.clean_document("\ufeff  A   very  spaced  text  ", clean_cfg)
    assert not out.startswith("\ufeff")
    assert "  " not in out
    assert out.startswith("A very")


def test_filter_too_short():
    cfg = quality.FilterConfig(min_chars=50)
    reason = quality.should_filter("short", cfg)
    assert reason is not None
    assert "too_short" in reason


def test_filter_avg_word_len_too_short():
    # Only lower the word-length bar: disable char/word-count defaults so the
    # avg-length check is the one that fires.
    cfg = quality.FilterConfig(
        min_chars=0, max_chars=100000, min_words=0, max_words=100000,
        min_avg_word_len=3.0, max_avg_word_len=14.0,
    )
    text = "a b c d e f g h i j k l m n o p q r s t u v w x y z a b c d e f g h i"
    reason = quality.should_filter(text, cfg)
    assert reason is not None
    assert "words_too_short" in reason


def test_filter_good_text():
    cfg = quality.FilterConfig(min_chars=20, min_words=5)
    good = "This is a perfectly good and long enough sentence for filtering."
    assert quality.should_filter(good, cfg) is None


# ---------------------------------------------------------------------------
# Dedup
# ---------------------------------------------------------------------------
def test_exact_dedup():
    docs = ["hello world", "hello world", "the quick brown fox", "the quick brown fox"]
    kept, removed = dedup.exact_dedup(docs)
    assert kept == ["hello world", "the quick brown fox"]
    assert removed == 2


def test_minhash_signature_deterministic():
    s1 = dedup.minhash_signature(["a", "b", "c"], 32)
    s2 = dedup.minhash_signature(["a", "b", "c"], 32)
    assert s1 == s2


def test_near_dedup_keeps_distinct():
    cfg = dedup.DedupConfig(near=True, minhash_perms=64, lsh_bands=8, lsh_rows=8)
    texts = ["the quick brown fox jumps over the lazy dog"] * 20
    # All identical tokens across docs -> near dedup removes extras.
    kept, removed = dedup.near_dedup(texts, cfg)
    assert len(kept) <= 5
    assert removed >= 15


def test_dedup_config_validation():
    cfg = dedup.DedupConfig(near=True, minhash_perms=64, lsh_bands=8, lsh_rows=8)
    with pytest.raises(ValueError):
        # 8 * 9 != 64
        dedup.near_dedup(["a b c d"], dedup.DedupConfig(near=True, minhash_perms=64, lsh_bands=8, lsh_rows=9))


# ---------------------------------------------------------------------------
# Split
# ---------------------------------------------------------------------------
def test_split_ratios():
    cfg = split.SplitConfig(train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)
    docs = [f"doc{i}" for i in range(100)]
    out = split.split_documents(docs, cfg, seed=0)
    assert len(out["train"]) == 80
    assert len(out["val"]) == 10
    assert len(out["test"]) == 10


def test_split_reproducible():
    cfg = split.SplitConfig()
    docs = [f"doc{i}" for i in range(50)]
    a = split.split_documents(docs, cfg, seed=42)
    b = split.split_documents(docs, cfg, seed=42)
    assert a == b
    # A different seed should (almost always) produce a different order.
    c = split.split_documents(docs, cfg, seed=1)
    assert a != c


def test_split_validates_sum():
    with pytest.raises(ValueError):
        cfg = split.SplitConfig(train_ratio=0.9, val_ratio=0.2, test_ratio=0.2)
        cfg.validate()


# ---------------------------------------------------------------------------
# End-to-end pipeline (uses the committed public-domain sample)
# ---------------------------------------------------------------------------
def test_pipeline_runs_on_sample():
    stats = run_pipeline("configs/data.yaml")
    # The committed sample should yield documents that survive cleaning/filter.
    assert stats["total_documents"] > 0
    assert stats["total_words"] > 0
    # All three splits present with at least one doc each (or documented empty).
    for name in ("train", "val", "test"):
        assert name in stats["splits"]
    assert stats["total_documents"] == (
        stats["splits"]["train"]["documents"]
        + stats["splits"]["val"]["documents"]
        + stats["splits"]["test"]["documents"]
    )
