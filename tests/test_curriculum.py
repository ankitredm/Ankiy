"""Tests for the Class 1-4 curriculum builders, splits and stage configs.

The curriculum is fully reproducible from code (no downloaded data), so these
tests rebuild it in a temp directory instead of depending on data/curriculum.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from curriculum.build import (
    STAGE6_KINDS,
    build_all,
    collect_items,
    dedupe,
    split_items,
)

EXPECTED_CATEGORIES = {"english", "hinglish", "math", "science", "social", "reasoning"}


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("curriculum")
    build_all(out)
    return out


def test_build_produces_all_files(built):
    for stage in range(1, 7):
        assert (built / "stages" / f"stage{stage}_train.jsonl").exists()
    assert (built / "val.jsonl").exists()
    assert (built / "test.jsonl").exists()
    assert (built / "tokenizer_corpus" / "train_corpus.jsonl").exists()
    assert (built / "stats.json").exists()


def test_items_have_required_fields_and_content(built):
    rows = _load_jsonl(built / "stages" / "stage5_train.jsonl")
    assert rows, "stage5 must not be empty"
    for row in rows:
        assert set(row) >= {"text", "category", "stage", "kind"}
        assert isinstance(row["text"], str) and len(row["text"]) >= 20
        assert row["category"] in EXPECTED_CATEGORIES
        assert row["stage"] in (1, 2, 3, 4)


def test_no_duplicates_within_a_stage(built):
    """Each stage file must be internally duplicate-free.

    (Items intentionally REPEAT across stages — later stages revise earlier
    classes by design — but never inside one stage's own file.)
    """
    for stage in range(1, 6):
        seen: set[str] = set()
        for row in _load_jsonl(built / "stages" / f"stage{stage}_train.jsonl"):
            key = " ".join(row["text"].split()).lower()
            assert key not in seen, f"duplicate item inside stage{stage}: {key[:60]}"
            seen.add(key)


def test_val_test_disjoint_from_train(built):
    train_texts = {
        " ".join(r["text"].split()).lower()
        for r in _load_jsonl(built / "stages" / "stage5_train.jsonl")
    }
    for split in ("val", "test"):
        for row in _load_jsonl(built / f"{split}.jsonl"):
            key = " ".join(row["text"].split()).lower()
            assert key not in train_texts, f"{split} item leaked from train: {key[:60]}"


def test_val_and_test_cover_all_categories(built):
    for split in ("val", "test"):
        cats = {r["category"] for r in _load_jsonl(built / f"{split}.jsonl")}
        assert EXPECTED_CATEGORIES <= cats, f"{split} missing categories: {EXPECTED_CATEGORIES - cats}"


def test_stages_are_progressive_with_revision(built):
    stats = json.loads((built / "stats.json").read_text(encoding="utf-8"))
    stages = stats["train_stages"]
    # Every stage non-empty.
    for stage in range(1, 7):
        assert stages[f"stage{stage}"]["items"] > 0
    # Stage 5 is the full mixed revision: covers every category.
    cats5 = set(stages["stage5"]["by_category"])
    assert cats5 == EXPECTED_CATEGORIES
    # Stage 6 re-weights exercises: more items than stage 5 (emphasis + rest).
    assert stages["stage6"]["items"] > stages["stage5"]["items"]


def test_hinglish_items_mix_languages(built):
    rows = [r for r in _load_jsonl(built / "stages" / "stage5_train.jsonl")
            if r["category"] == "hinglish"]
    assert rows
    hinglish_markers = ["hai", "kya", "kyu", "kitne", "kitni", "kaam", "kar", "hain",
                        "mujhe", "samjhao", "zarurat", "batao", "kaise", "mein"]
    hits = sum(
        1 for r in rows
        if any(marker in r["text"].lower() for marker in hinglish_markers)
    )
    assert hits >= len(rows) * 0.8, "Hinglish items should genuinely mix Hindi+English"


def test_math_items_include_worked_examples(built):
    rows = [r for r in _load_jsonl(built / "stages" / "stage5_train.jsonl")
            if r["category"] == "math"]
    kinds = {r["kind"] for r in rows}
    assert "worked" in kinds, "math must include worked examples, not just Q&A"
    assert "word_problem" in kinds


def test_split_is_deterministic():
    items, _ = dedupe(collect_items())
    train1, val1, test1 = split_items(items)
    train2, val2, test2 = split_items(items)
    keys = lambda rows: sorted(r["text"] for r in rows)  # noqa: E731
    assert keys(train1) == keys(train2)
    assert keys(val1) == keys(val2)
    assert keys(test1) == keys(test2)


def test_stage6_emphasises_exercises(built):
    stage5 = _load_jsonl(built / "stages" / "stage5_train.jsonl")
    stage6 = _load_jsonl(built / "stages" / "stage6_train.jsonl")
    frac = lambda rows: sum(r.get("kind") in STAGE6_KINDS for r in rows) / len(rows)  # noqa: E731
    assert frac(stage6) > frac(stage5), "stage 6 must weight exercises/quiz kinds higher"


def test_stats_file_matches_files(built):
    stats = json.loads((built / "stats.json").read_text(encoding="utf-8"))
    val_rows = _load_jsonl(built / "val.jsonl")
    assert stats["val"]["items"] == len(val_rows)
    assert stats["test"]["items"] == len(_load_jsonl(built / "test.jsonl"))
