"""ANKIT 0.1 tokenizer package.

Public API:
    AnkitTokenizer      — load + use the trained tokenizer (text <-> ids)
    load()              — convenience alias for AnkitTokenizer.load()
    train_tokenizer     — the training module (train_tokenizer.py)
"""

from tokenizer.tokenizer import AnkitTokenizer, load

__all__ = ["AnkitTokenizer", "load"]
