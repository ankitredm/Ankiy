"""Shared pytest fixtures."""

from __future__ import annotations

import numpy as np
import pytest

from model.config import Config
from tokenizer import train_tokenizer
from tokenizer.tokenizer import AnkitTokenizer


@pytest.fixture
def smoke_bin(tmp_path):
    """A tiny token .bin file with a known token stream."""
    # 40 tokens, ids in [0, 20) — enough to create several 8-wide windows.
    stream = np.arange(0, 40, dtype=np.uint16) % 20
    path = tmp_path / "data.bin"
    stream.tofile(str(path))
    return str(path)


@pytest.fixture(scope="session")
def tiny_tokenizer_path(tmp_path_factory) -> str:
    """Train OUR OWN tiny byte-level BPE tokenizer once, into a temp dir.

    Nothing pretrained is involved: this is exactly what
    ``python tokenizer/train_tokenizer.py`` does, just with a small vocab and
    the committed public-domain sample corpus.
    """
    out_dir = tmp_path_factory.mktemp("tokenizer")
    cfg = train_tokenizer.load_config("configs/tokenizer.yaml")
    cfg.tokenizer_file = str(out_dir / "ankit_tokenizer.json")
    cfg.vocab_file = str(out_dir / "vocab.json")
    cfg.report_file = str(out_dir / "tokenizer_report.json")
    cfg.vocab_size = 512
    cfg.max_documents = 50
    cfg.show_progress = False
    train_tokenizer.run_training(cfg)
    return cfg.tokenizer_file


@pytest.fixture(scope="session")
def tiny_tokenizer(tiny_tokenizer_path) -> AnkitTokenizer:
    return AnkitTokenizer.load(tiny_tokenizer_path)


@pytest.fixture
def tiny_run_config(tmp_path, tiny_tokenizer_path) -> Config:
    """A minimal, fully temp-dir-isolated Config for real (tiny) CPU runs.

    Shape of the default setup:
      - train.bin: 66 tokens -> 50 next-token examples -> 25 batches/epoch
        (batch_size 2, context_length 16)
      - grad_accumulation_steps = 4  => 6 complete windows + 1 leftover
        micro-batch per epoch (exercises the partial-window flush)
      - total_steps = 7              => exactly reachable only if the
        partial final window is applied at the end of epoch 1
    """
    vocab = AnkitTokenizer.load(tiny_tokenizer_path).vocab_size
    ctx = 16
    rng = np.random.default_rng(0)
    train_bin = tmp_path / "train.bin"
    val_bin = tmp_path / "val.bin"
    rng.integers(0, vocab, size=66, dtype=np.int64).astype(np.uint16).tofile(str(train_bin))
    rng.integers(0, vocab, size=30, dtype=np.int64).astype(np.uint16).tofile(str(val_bin))

    return Config.from_dict(
        {
            "model": {
                "vocab_size": vocab,
                "d_model": 32,
                "n_layers": 1,
                "n_heads": 2,
                "context_length": ctx,
                "ffn_dim": 64,
                "dropout": 0.0,
                "tie_embedding": False,
            },
            "training": {
                "batch_size": 2,
                "grad_accumulation_steps": 4,
                "learning_rate": 1e-3,
                "weight_decay": 0.0,
                "warmup_steps": 1,
                "total_steps": 7,
                "checkpoint_interval": 0,  # 0 = only the final checkpoint
                "eval_interval": 0,        # 0 = no mid-run evals
                "eval_steps": 0,           # full val set when evals do run
                "max_grad_norm": 1.0,
                "seed": 7,
                "precision": "fp32",
                "device": "cpu",
                "output_dir": str(tmp_path / "checkpoints"),
                "tokenizer_path": tiny_tokenizer_path,
                "train_data": str(train_bin),
                "val_data": str(val_bin),
            },
        }
    )
