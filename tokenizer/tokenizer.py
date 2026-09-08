"""Load and use ANKIT 0.1's trained tokenizer.

After ``tokenizer/train_tokenizer.py`` trains a byte-level BPE tokenizer on our
own corpus, this module loads the saved ``tokenizer/ankit_tokenizer.json`` and
exposes a clean, beginner-friendly interface:

    from tokenizer.tokenizer import AnkitTokenizer
    tok = AnkitTokenizer.load()
    ids = tok.encode("The capital of France is", add_bos=True)
    text = tok.decode(ids)

It supports:
    text  ->  list[int]   (encode, optionally with BOS/EOS)
    list[int]  ->  text   (decode)

Nothing here loads a pretrained tokenizer. It only reads the file we trained.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from tokenizers import Tokenizer

# Defaults. Training writes these tokens in this order; ids are recorded in the
# tokenizer report. We hard-code the *token strings* (not magic ids) and always
# look the ids up so it stays correct even if ordering changes.
UNK = "<unk>"
BOS = "<s>"
EOS = "</s>"
PAD = "<pad>"


class AnkitTokenizer:
    """A thin, friendly wrapper around our trained byte-level BPE tokenizer."""

    def __init__(self, tokenizer: Tokenizer) -> None:
        self._tokenizer = tokenizer
        # Cache special-token ids for fast access.
        self._ids: dict[str, int] = {}
        for token in (UNK, BOS, EOS, PAD):
            tid = tokenizer.token_to_id(token)
            if tid is not None:
                self._ids[token] = tid
        self._bos_id = self._ids.get(BOS)
        self._eos_id = self._ids.get(EOS)
        self._pad_id = self._ids.get(PAD)
        self._unk_id = self._ids.get(UNK)

    # -- construction -----------------------------------------------------
    @classmethod
    def load(cls, path: str | Path = "tokenizer/ankit_tokenizer.json") -> "AnkitTokenizer":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(
                f"Tokenizer file not found: {path}. Run "
                "`python tokenizer/train_tokenizer.py` first."
            )
        tokenizer = Tokenizer.from_file(str(path))
        return cls(tokenizer)

    # -- properties --------------------------------------------------------
    @property
    def vocab_size(self) -> int:
        """Number of tokens in the vocabulary."""
        return self._tokenizer.get_vocab_size()

    @property
    def bos_id(self) -> int | None:
        return self._bos_id

    @property
    def eos_id(self) -> int | None:
        return self._eos_id

    @property
    def pad_id(self) -> int | None:
        return self._pad_id

    @property
    def unk_id(self) -> int | None:
        return self._unk_id

    @property
    def special_ids(self) -> dict[str, int]:
        return dict(self._ids)

    # -- main API ----------------------------------------------------------
    def encode(self, text: str, add_bos: bool = False, add_eos: bool = False) -> list[int]:
        """Convert text to a list of token ids."""
        ids = self._tokenizer.encode(text).ids
        if add_bos and self._bos_id is not None:
            ids = [self._bos_id] + ids
        if add_eos and self._eos_id is not None:
            ids = ids + [self._eos_id]
        return ids

    def decode(self, ids: list[int] | tuple[int, ...] | "list[int]", skip_special: bool = True) -> str:
        """Convert a list of token ids back to text.

        ``skip_special=True`` removes BOS/EOS/PAD/UNK markers (the default; this
        is what you want for readable text). Set it False to keep them.
        """
        return self._tokenizer.decode(list(ids), skip_special_tokens=skip_special)

    # -- convenience -------------------------------------------------------
    def token_to_id(self, token: str) -> int | None:
        return self._tokenizer.token_to_id(token)

    def id_to_token(self, token_id: int) -> str:
        return self._tokenizer.id_to_token(token_id)

    def count_tokens(self, text: str) -> int:
        """Number of tokens produced by encoding ``text`` (no special tokens)."""
        return len(self._tokenizer.encode(text).ids)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"<AnkitTokenizer vocab={self.vocab_size:,} "
            f"bos={self.bos_id} eos={self.eos_id} pad={self.pad_id} unk={self.unk_id}>"
        )


def load(path: str | Path = "tokenizer/ankit_tokenizer.json") -> AnkitTokenizer:
    """Entry point alias for convenience."""
    return AnkitTokenizer.load(path)


def align_model_vocab_size(model_config, tokenizer: AnkitTokenizer) -> int:
    """Return the vocab size a model should be built with to match a tokenizer.

    Trained on a tiny corpus a tokenizer may end up *smaller* than a model's
    configured ``vocab_size`` (the merges stop early). For real training the two
    must match, otherwise the model wastes output heads on tokens it never uses
    or, worse, emits ids outside the tokenizer's vocabulary.

    This returns the correct ``vocab_size`` and, if it differs from the config,
    prints a warning so nobody silently trains a mismatched model.
    """
    correct = tokenizer.vocab_size
    configured = int(getattr(model_config, "vocab_size", 0))
    if configured and configured != correct:
        import sys

        print(
            f"[warn] model config vocab_size={configured:,} but tokenizer "
            f"vocab={correct:,}. For training, set the model vocab_size to "
            f"{correct:,} (see configs/ankit_0_1.yaml).",
            file=sys.stderr,
        )
    return correct
