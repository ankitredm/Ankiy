"""Tests for the ANKIT 0.1 tokenizer (trained from scratch)."""

from __future__ import annotations

import pytest

from tokenizer.tokenizer import AnkitTokenizer
from tokenizer.train_tokenizer import (
    TokenizerConfig,
    iter_documents,
    resolve_input_paths,
)
from tokenizer import train_tokenizer


@pytest.fixture(scope="module")
def tokenizer():
    """Load the tokenizer trained during the build/test run.

    We train a fresh one in a temp corpus if the saved file is missing, so the
    test never depends on state.
    """
    try:
        return AnkitTokenizer.load()
    except FileNotFoundError:
        # Train a tiny tokenizer on the sample corpus for the test.
        cfg = train_tokenizer.load_config("configs/tokenizer.yaml")
        cfg.tokenizer_file = "tokenizer/_test_tokenizer.json"
        cfg.vocab_file = "tokenizer/_test_vocab.json"
        cfg.report_file = "tokenizer/_test_report.json"
        cfg.vocab_size = 512
        cfg.max_documents = 50
        train_tokenizer.run_training(cfg)
        return AnkitTokenizer.load("tokenizer/_test_tokenizer.json")


def test_tokenizer_has_special_tokens(tokenizer):
    assert tokenizer.vocab_size > 0
    assert tokenizer.bos_id is not None
    assert tokenizer.eos_id is not None
    assert tokenizer.pad_id is not None
    assert tokenizer.unk_id is not None
    # Special tokens must be distinct.
    ids = tokenizer.special_ids.values()
    assert len(ids) == len(set(ids))
    # All four special tokens are present by their actual token strings.
    for token in ("<unk>", "<s>", "</s>", "<pad>"):
        assert token in tokenizer.special_ids
    assert tokenizer.special_ids["<unk>"] == 0  # common convention


def test_encode_text_to_ids(tokenizer):
    ids = tokenizer.encode("The capital of France is Paris.")
    assert isinstance(ids, list)
    assert all(isinstance(i, int) for i in ids)
    assert len(ids) > 0


def test_bos_eos_added(tokenizer):
    ids = tokenizer.encode("hello", add_bos=True, add_eos=True)
    assert ids[0] == tokenizer.bos_id
    assert ids[-1] == tokenizer.eos_id


def test_round_trip(tokenizer):
    text = "The quick brown fox jumps over the lazy dog."
    ids = tokenizer.encode(text)
    decoded = tokenizer.decode(ids)
    # Byte-level BPE adds a leading space; compare content after stripping.
    assert decoded.strip() == text


def test_decode_skips_special_tokens(tokenizer):
    ids = tokenizer.encode("hello world", add_bos=True, add_eos=True)
    decoded = tokenizer.decode(ids)  # skip_special defaults True
    assert "<s>" not in decoded
    assert "</s>" not in decoded


def test_special_tokens_roundtrip_ids(tokenizer):
    """A BOS token must encode/decode deterministically as its id."""
    assert tokenizer.token_to_id("<s>") == tokenizer.bos_id
    assert tokenizer.decode([tokenizer.bos_id, tokenizer.unk_id], skip_special=False) is not None


def test_count_tokens(tokenizer):
    n1 = tokenizer.count_tokens("The cat sat on the mat.")
    n2 = tokenizer.count_tokens("The cat sat on the mat.")
    assert n1 == n2
    assert n1 > 0


def test_resolve_input_paths():
    paths = resolve_input_paths(["data/raw/sample/*.txt"])
    assert len(paths) >= 1
    assert all(p.is_file() for p in paths)


def test_iter_documents_yields_text():
    # A .txt file is read as one document; a .jsonl file yields one per line.
    paths = resolve_input_paths(["data/raw/sample/aesop_fables.txt"])
    docs = list(iter_documents(paths, max_documents=5))
    assert len(docs) == 1  # whole .txt file = 1 document
    assert all(isinstance(d, str) and d for d in docs)

    jsonl_paths = resolve_input_paths(["data/processed/splits/train.jsonl"])
    docs = list(iter_documents(jsonl_paths, max_documents=5))
    assert len(docs) == 5  # .jsonl: 5 documents capped
    assert all(isinstance(d, str) and d for d in docs)


def test_config_from_dict_minimal():
    cfg = TokenizerConfig.from_dict(
        {"name": "t", "version": "1", "algorithm": "bpe", "vocab_size": 1000,
         "input": {"paths": ["x.txt"]}, "special_tokens": ["<unk>", "<s>", "</s>", "<pad>"]}
    )
    assert cfg.vocab_size == 1000
    assert cfg.min_frequency == 2  # default
    assert len(cfg.special_tokens) == 4


def test_config_rejects_non_bpe():
    with pytest.raises(ValueError):
        cfg = TokenizerConfig.from_dict(
            {"name": "t", "version": "1", "algorithm": "wordpiece", "vocab_size": 1000,
             "input": {"paths": ["x.txt"]}}
        )
        train_tokenizer.build_tokenizer(cfg)
