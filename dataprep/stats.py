"""Dataset statistics.

We report honest numbers about the corpus so we never over-claim size. The
"tokens" figure here is a *word-level approximation* (split on whitespace) used
as a sanity check. The real token count comes after the tokenizer in Phase 4;
this file does not pretend to be that.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Sequence


def _word_count(text: str) -> int:
    return len(text.split())


def char_count(text: str) -> int:
    return len(text)


def compute_stats(
    documents: dict[str, list[str]],  # keys: train/val/test
    source_files: int = 0,
    cleaned_before_filter: int = 0,
    filtered_out: int = 0,
    exact_removed: int = 0,
    near_removed: int = 0,
) -> dict:
    """Aggregate statistics across all splits."""
    all_texts = [t for split in documents.values() for t in split]

    total_chars = sum(char_count(t) for t in all_texts)
    total_words = sum(_word_count(t) for t in all_texts)
    all_words = []
    for t in all_texts:
        all_words.extend(t.split())

    # Vocabulary estimate (word-level, lowercased) for a sense of size.
    vocab = Counter(w.lower() for w in all_words)
    n_unique_words = len(vocab)

    per_split: dict[str, dict] = {}
    for name, docs in documents.items():
        chars = sum(char_count(t) for t in docs)
        words = sum(_word_count(t) for t in docs)
        per_split[name] = {
            "documents": len(docs),
            "characters": chars,
            "words": words,
            "approx_tokens": words,  # word-level approximation
        }

    return {
        "splits": per_split,
        "total_documents": len(all_texts),
        "total_characters": total_chars,
        "total_words": total_words,
        "approx_tokens_word_level": total_words,
        "unique_words": n_unique_words,
        "source_files_read": source_files,
        "cleaned_before_filter": cleaned_before_filter,
        "filtered_out_documents": filtered_out,
        "docs_after_filter": cleaned_before_filter - filtered_out,
        "exact_duplicates_removed": exact_removed,
        "near_duplicates_removed": near_removed,
        "vocab_diversity_ratio": (
            round(n_unique_words / total_words, 4) if total_words else 0.0
        ),
    }


def save_stats(stats: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(stats, handle, indent=2)


def format_stats(stats: dict) -> str:
    """Human-readable summary for the terminal / report."""
    lines: list[str] = []
    lines.append("DATSET STATISTICS")
    lines.append("=" * 60)
    lines.append(f"Total documents        : {stats['total_documents']:,}")
    lines.append(f"Total characters       : {stats['total_characters']:,}")
    lines.append(f"Total words            : {stats['total_words']:,}")
    lines.append(
        "Approx. tokens (words)  : "
        f"{stats['approx_tokens_word_level']:,}"
    )
    lines.append(
        f"Unique words            : {stats['unique_words']:,} "
        f"(diversity {stats['vocab_diversity_ratio']:.4f})"
    )
    lines.append("-" * 60)
    lines.append(
        f"Cleaned docs            : {stats['cleaned_before_filter']:,}"
    )
    lines.append(
        f"Filtered out            : {stats['filtered_out_documents']:,}"
    )
    lines.append(
        f"After filtering         : {stats['docs_after_filter']:,}"
    )
    lines.append(
        f"Exact dups removed      : {stats['exact_duplicates_removed']:,}"
    )
    lines.append(
        f"Near dups removed       : {stats['near_duplicates_removed']:,}"
    )
    lines.append("-" * 60)
    for name, s in stats["splits"].items():
        lines.append(
            f"{name.upper():5s} : {s['documents']:,} docs | "
            f"{s['characters']:,} chars | {s['words']:,} words"
        )
    return "\n".join(lines)
