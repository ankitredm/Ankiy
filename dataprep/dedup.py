"""Deduplication: exact and near-duplicate document removal.

Why deduplicate? Real-world corpora often contain the *same* text many times
(e.g. a quote repeated across pages). Training on repeated text makes the model
memorise instead of learn, and wastes GPU time on boilerplate.

Two levels:

1. **Exact dedup** — hash each fully cleaned document and keep only the first
   copy of identical text. Fast, always on, zero false positives.

2. **Near dedup (MinHash + LSH)** — detect documents that are not identical
   but share most of their content (e.g. an article and its slightly edited
   reprint). We estimate similarity with MinHash signatures and bucket them
   with Locality-Sensitive Hashing so we never compare every pair.

All functions are pure and reproducible given a fixed seed.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass
class DedupConfig:
    exact: bool = True
    near: bool = False
    minhash_perms: int = 128
    lsh_bands: int = 16
    lsh_rows: int = 8
    near_threshold: float = 0.8

    @classmethod
    def from_dict(cls, data: dict) -> "DedupConfig":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def exact_dedup(texts: Sequence[str]) -> tuple[list[str], int]:
    """Drop exact duplicates, preserving first-seen order.

    Returns (kept_texts, num_removed).
    """
    seen: set[str] = set()
    kept: list[str] = []
    removed = 0
    for t in texts:
        key = _sha256(t)
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        kept.append(t)
    return kept, removed


# ---------------------------------------------------------------------------
# MinHash + LSH
# ---------------------------------------------------------------------------
def _h32(text: str) -> int:
    """A stable 32-bit hash of a string token."""
    return int.from_bytes(
        hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()[:8],
        "big",
    )


def minhash_signature(tokens: Iterable[str], perms: int, seed: int = 1337) -> list[int]:
    """Compute a MinHash signature (list of perms ints) for a token set.

    We use a cheap, seed-deterministic random permutation set so the same
    input always gives the same signature (reproducibility).
    """
    import random

    rng = random.Random(seed)
    coeffs = [(rng.randint(0, 2**31 - 1), rng.randint(0, 2**31 - 1)) for _ in range(perms)]

    sig = [2**32 - 1] * perms
    for tok in tokens:
        h = _h32(tok)
        for i, (a, b) in enumerate(coeffs):
            value = (a * h + b) % (2**32 - 1)
            if value < sig[i]:
                sig[i] = value
    return sig


def _jaccard(s1: set[str], s2: set[str]) -> float:
    if not s1 and not s2:
        return 1.0
    inter = len(s1 & s2)
    union = len(s1 | s2)
    return inter / union if union else 0.0


def near_dedup(texts: Sequence[str], config: DedupConfig, seed: int = 1337) -> tuple[list[str], int]:
    """Drop near-duplicate documents using MinHash + LSH.

    Returns (kept_texts, num_removed). Bands and rows are taken from config;
    band * row must equal minhash_perms.
    """
    if config.lsh_bands * config.lsh_rows != config.minhash_perms:
        raise ValueError("lsh_bands * lsh_rows must equal minhash_perms.")

    # Build signatures and token sets once.
    sigs: list[list[int]] = []
    token_sets: list[set[str]] = []
    for t in texts:
        tokens = [w.lower() for w in t.split() if w.isalnum()]
        token_sets.append(set(tokens))
        sigs.append(minhash_signature(tokens, config.minhash_perms, seed))

    bands = config.lsh_bands
    rows = config.lsh_rows
    band_len = len(sigs[0]) // bands

    # LSH: group each signature by its band, find candidate duplicate pairs.
    candidates: set[tuple[int, int]] = set()
    buckets: dict[tuple[int, ...], list[int]] = {}
    for band in range(bands):
        buckets.clear()
        for idx, sig in enumerate(sigs):
            key = tuple(sig[band * band_len : (band + 1) * band_len])
            buckets.setdefault(key, []).append(idx)
        for same in buckets.values():
            for i in range(len(same)):
                for j in range(i + 1, len(same)):
                    a, b = same[i], same[j]
                    key = (min(a, b), max(a, b))
                    candidates.add(key)

    keep_flags = [True] * len(texts)
    removed = 0
    for a, b in sorted(candidates):
        if not keep_flags[a] or not keep_flags[b]:
            continue
        if _jaccard(token_sets[a], token_sets[b]) >= config.near_threshold:
            # Keep the first one seen; remove the later one.
            keep_flags[max(a, b)] = False
            removed += 1

    kept = [t for i, t in enumerate(texts) if keep_flags[i]]
    return kept, removed


def deduplicate(
    texts: Sequence[str], config: DedupConfig, seed: int = 1337
) -> tuple[list[str], int, int]:
    """Run exact then (optionally) near dedup.

    Returns (kept_texts, exact_removed, near_removed).
    """
    exact_removed = 0
    near_removed = 0
    current = list(texts)
    if config.exact:
        current, exact_removed = exact_dedup(current)
    if config.near:
        current, near_removed = near_dedup(current, config, seed)
    return current, exact_removed, near_removed
