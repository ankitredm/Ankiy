"""Assemble the Class 1-4 curriculum into stage-wise, deduplicated, split data.

Outputs (under ``data/curriculum/`` by default):

    stages/stage1_train.jsonl ... stage6_train.jsonl   (training stages)
    val.jsonl                                          (held-out validation)
    test.jsonl                                         (held-out test)
    tokenizer_corpus/train_corpus.jsonl                (train-split text only,
                                                        for training the tokenizer)
    stats.json                                         (dataset statistics)

Design decisions:
  - Splits are stratified per (category, stage) and chosen by a stable hash of
    the item text, so rebuilding the curriculum never shuffles val items into
    train and vice versa. The evaluation suite in evaluation/ uses its OWN
    hand-written tasks, fully independent of this corpus.
  - Later stages always contain a REVISION slice of earlier stages, so old
    knowledge keeps being rehearsed (no silent forgetting between stages).
  - Stage 5 is a full mixed revision of Classes 1-4; stage 6 is an
    exercise/QA/reasoning-heavy mix for evaluation + reinforcement rounds.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from curriculum import english, hinglish, mathgen, reasoning, science, social

TRAIN_FRACTION = 0.94
VAL_FRACTION = 0.03
TEST_FRACTION = 0.03

# Revision: each stage N (2-4) keeps this fraction of its slots for earlier
# stages, sampled deterministically. Stage 5 mixes everything; stage 6 mixes
# everything with exercise/QA/reasoning emphasis.
REVISION_FRACTION = 0.20

# Kind emphasis for stage 6 (evaluation + weak-area reinforcement round).
STAGE6_KINDS = {"qa", "exercise", "worked", "word_problem", "reasoning",
                "comprehension", "correction", "inference", "pattern"}


def _hash_float(text: str, salt: str = "") -> float:
    """Deterministic pseudo-random float in [0, 1) from the item text."""
    digest = hashlib.sha1((salt + text).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / float(2 ** 64)


def _normalize_text(text: str) -> str:
    return " ".join(text.split()).strip().lower()


def collect_items() -> list[dict]:
    items: list[dict] = []
    for module in (english, hinglish, mathgen, science, social, reasoning):
        items.extend(module.build())

    # Basic hygiene: no empty/whitespace-only texts; trim edges.
    cleaned = []
    for it in items:
        text = it["text"].strip()
        if len(text) < 20:  # every item must carry real content
            continue
        it["text"] = text
        cleaned.append(it)
    return cleaned


def dedupe(items: list[dict]) -> tuple[list[dict], int]:
    """Exact-duplicate removal (and first-of-near-identical by normalized text)."""
    seen: set[str] = set()
    kept: list[dict] = []
    for it in items:
        key = _normalize_text(it["text"])
        if key in seen:
            continue
        seen.add(key)
        kept.append(it)
    return kept, len(items) - len(kept)


def split_items(items: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Deterministically split into train/val/test, stratified per category+stage."""
    train, val, test = [], [], []
    groups: dict[tuple, list[dict]] = {}
    for it in items:
        groups.setdefault((it["category"], it["stage"]), []).append(it)

    for (category, stage), group in sorted(groups.items()):
        # Sort by hash for a stable pseudo-random order within the group.
        ordered = sorted(group, key=lambda it: _hash_float(it["text"], salt=category))
        n = len(ordered)
        n_val = max(1, round(n * VAL_FRACTION))
        n_test = max(1, round(n * TEST_FRACTION))
        n_train = n - n_val - n_test
        train.extend(ordered[:n_train])
        val.extend(ordered[n_train:n_train + n_val])
        test.extend(ordered[n_train + n_val:])
    return train, val, test


def build_stages(train: list[dict]) -> dict[int, list[dict]]:
    """Build the six training-stage files from the train split."""
    by_stage: dict[int, list[dict]] = {1: [], 2: [], 3: [], 4: []}
    for it in train:
        by_stage.setdefault(int(it["stage"]), []).append(it)

    stages: dict[int, list[dict]] = {}

    # Stages 1-4: own class + a revision slice of every earlier class.
    for stage in (1, 2, 3, 4):
        own = sorted(by_stage[stage], key=lambda it: _hash_float(it["text"], salt=f"s{stage}"))
        n_rev = int(len(own) * REVISION_FRACTION) if stage > 1 else 0
        earlier: list[dict] = []
        if n_rev:
            for prev in range(1, stage):
                earlier.extend(by_stage[prev])
            earlier = sorted(earlier, key=lambda it: _hash_float(it["text"], salt=f"rev{stage}"))
            # Round-robin across earlier stages so revision is balanced.
            buckets: dict[int, list[dict]] = {p: [] for p in range(1, stage)}
            for idx, it in enumerate(earlier):
                buckets[1 + idx % (stage - 1)].append(it)
            per_bucket = max(1, n_rev // (stage - 1))
            picked: list[dict] = []
            for p in range(1, stage):
                picked.extend(buckets[p][:per_bucket])
            earlier = picked[:n_rev]
        stages[stage] = own + earlier

    # Stage 5: full mixed revision across Classes 1-4 (all train items).
    everything = sorted(train, key=lambda it: _hash_float(it["text"], salt="stage5"))
    stages[5] = everything

    # Stage 6: exercise/QA/reasoning-heavy subset (double weight) + everything,
    # for the evaluation-and-reinforcement round.
    emphasis = [it for it in everything if it.get("kind") in STAGE6_KINDS]
    rest = [it for it in everything if it.get("kind") not in STAGE6_KINDS]
    stages[6] = emphasis + emphasis + rest

    for stage, items in stages.items():
        # Stable pseudo-random shuffle so classes/topics interleave (no long
        # same-category runs, which would bias mini-batches).
        stages[stage] = sorted(items, key=lambda it: _hash_float(it["text"], salt=f"mix{stage}"))
    return stages


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_all(out_dir: str | Path = "data/curriculum") -> dict:
    out_dir = Path(out_dir)
    items = collect_items()
    items, n_dupes = dedupe(items)
    train, val, test = split_items(items)
    stages = build_stages(train)

    _write_jsonl(out_dir / "val.jsonl", val)
    _write_jsonl(out_dir / "test.jsonl", test)
    for stage, rows in stages.items():
        _write_jsonl(out_dir / "stages" / f"stage{stage}_train.jsonl", rows)
    # Tokenizer corpus = train-split text only (tokenizer never sees val/test).
    _write_jsonl(
        out_dir / "tokenizer_corpus" / "train_corpus.jsonl",
        [{"text": it["text"]} for it in train],
    )

    stats = collect_stats(out_dir, n_raw=len(items) + n_dupes, n_dupes=n_dupes)
    return stats


def collect_stats(out_dir: str | Path, n_raw: int = 0, n_dupes: int = 0) -> dict:
    """(Re)compute dataset statistics from whatever files exist in ``out_dir``."""
    out_dir = Path(out_dir)
    stats: dict = {"raw_items": n_raw, "duplicates_removed": n_dupes}

    def _load(path: Path) -> list[dict]:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    for split in ("val", "test"):
        rows = _load(out_dir / f"{split}.jsonl")
        stats[split] = {
            "items": len(rows),
            "chars": sum(len(r["text"]) for r in rows),
            "by_category": dict(Counter(r["category"] for r in rows)),
        }

    stage_stats = {}
    for stage in range(1, 7):
        rows = _load(out_dir / "stages" / f"stage{stage}_train.jsonl")
        stage_stats[f"stage{stage}"] = {
            "items": len(rows),
            "chars": sum(len(r["text"]) for r in rows),
            "by_category": dict(Counter(r["category"] for r in rows)),
        }
    stats["train_stages"] = stage_stats

    corpus = _load(out_dir / "tokenizer_corpus" / "train_corpus.jsonl")
    stats["tokenizer_corpus"] = {"items": len(corpus), "chars": sum(len(r["text"]) for r in corpus)}

    stats_path = out_dir / "stats.json"
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats
