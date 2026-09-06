"""Text cleaning, normalisation and quality filtering.

This module turns *messy raw text* into *clean text suitable for training an
LLM from scratch*. It is deliberately dependency-light (just stdlib + a bit of
regex) so it runs anywhere.

Two ideas you need to know:

1. **Normalisation** makes text consistent: straighten quotes, collapse stray
   whitespace, remove control characters. It does NOT change the meaning.
2. **Filtering** decides whether a whole *document* is good enough. We drop
   tiny fragments, gigantic dumps, and garbage that would waste GPU time.

Everything is driven by :class:`CleaningConfig` / :class:`FilterConfig`, which
are built from ``configs/data.yaml`` so you never edit this file to tweak the
pipeline.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Regular expressions used throughout. Compiled once for speed.
# ---------------------------------------------------------------------------
_MULTI_SPACE = re.compile(r"[ \t\r\f\v]+")
_MULTI_BLANK = re.compile(r"\n{3,}")
_URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_HTML_RE = re.compile(r"<[^>]+>")
_BULLET_RE = re.compile(r"^\s*[-*•▪‣]\s+", re.MULTILINE)
_NEWLINE_RE = re.compile(r"[\r\n]+")

_CONTROL_RE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]"
)


@dataclass
class CleaningConfig:
    unicode_normalize: str = "NFC"
    remove_control_chars: bool = True
    normalize_newlines: bool = True
    strip_bom: bool = True
    collapse_whitespace: bool = True
    collapse_blank_lines: bool = True
    remove_urls: bool = True
    remove_html: bool = True
    remove_bullet_markers: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "CleaningConfig":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class FilterConfig:
    min_chars: int = 200
    max_chars: int = 100_000
    min_words: int = 40
    max_words: int = 20_000
    min_avg_word_len: float = 3.0
    max_avg_word_len: float = 14.0
    max_repeat_line_ratio: float = 0.40

    @classmethod
    def from_dict(cls, data: dict) -> "FilterConfig":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------
def decode_bytes(raw: bytes | str, encoding: str = "utf-8") -> str:
    """Decode bytes -> str, tolerating a few common encodings / errors."""
    if isinstance(raw, str):
        return raw
    for enc in (encoding, "utf-8-sig", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode(encoding, errors="replace")


def strip_bom(text: str) -> str:
    return text.lstrip("\ufeff")


def normalize_unicode(text: str, form: str = "NFC") -> str:
    return unicodedata.normalize(form, text)


def remove_control_chars(text: str) -> str:
    return _CONTROL_RE.sub("", text)


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def collapse_whitespace(text: str) -> str:
    return _MULTI_SPACE.sub(" ", text)


def collapse_blank_lines(text: str) -> str:
    # Keep a single blank line (paragraph break) where there were several.
    return _MULTI_BLANK.sub("\n\n", text)


def remove_urls(text: str) -> str:
    return _URL_RE.sub(" ", text)


def remove_html(text: str) -> str:
    return _HTML_RE.sub(" ", text)


def remove_bullet_markers(text: str) -> str:
    return _BULLET_RE.sub("", text)


def clean_document(raw: str, config: CleaningConfig) -> str:
    """Run the full cleaning pipeline on a single document's text."""
    text = raw
    if config.strip_bom:
        text = strip_bom(text)
    text = normalize_unicode(text, config.unicode_normalize)
    if config.remove_control_chars:
        text = remove_control_chars(text)
    if config.normalize_newlines:
        text = normalize_newlines(text)
    if config.remove_urls:
        text = remove_urls(text)
    if config.remove_html:
        text = remove_html(text)
    if config.remove_bullet_markers:
        text = remove_bullet_markers(text)
    if config.collapse_whitespace:
        text = collapse_whitespace(text)
    if config.collapse_blank_lines:
        text = collapse_blank_lines(text)
    # Re-collapse whitespace that the earlier steps may have re-introduced
    # around line boundaries.
    text = collapse_whitespace(text)
    text = text.strip()
    return text


# ---------------------------------------------------------------------------
# Quality metrics + filtering
# ---------------------------------------------------------------------------
def _word_list(text: str) -> list[str]:
    return text.split()


def average_word_length(text: str) -> float:
    words = _word_list(text)
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)


def repeat_line_ratio(text: str) -> float:
    """Fraction of lines that are duplicates of an earlier line."""
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if not lines:
        return 0.0
    seen: set[str] = set()
    dup = 0
    for ln in lines:
        if ln in seen:
            dup += 1
        else:
            seen.add(ln)
    return dup / len(lines)


def quality_metrics(text: str) -> dict[str, float]:
    words = _word_list(text)
    return {
        "num_chars": float(len(text)),
        "num_words": float(len(words)),
        "num_lines": float(len([ln for ln in text.split("\n") if ln.strip()])),
        "avg_word_len": average_word_length(text),
        "repeat_line_ratio": repeat_line_ratio(text),
    }


def should_filter(text: str, config: FilterConfig) -> Optional[str]:
    """Return a reason string if the doc should be dropped, else None."""
    n_chars = len(text)
    if n_chars < config.min_chars:
        return f"too_short({n_chars}<{config.min_chars})"
    if n_chars > config.max_chars:
        return f"too_long({n_chars}>{config.max_chars})"

    words = _word_list(text)
    n_words = len(words)
    if n_words < config.min_words:
        return f"too_few_words({n_words}<{config.min_words})"
    if n_words > config.max_words:
        return f"too_many_words({n_words}>{config.max_words})"

    avg_len = average_word_length(text)
    if avg_len < config.min_avg_word_len:
        return f"words_too_short(avg_len={avg_len:.2f})"
    if avg_len > config.max_avg_word_len:
        return f"words_too_long(avg_len={avg_len:.2f})"

    repeat = repeat_line_ratio(text)
    if repeat > config.max_repeat_line_ratio:
        return f"too_repetitive(repeat={repeat:.2f})"

    return None
