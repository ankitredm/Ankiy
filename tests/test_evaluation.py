"""Tests for the curriculum evaluation harness (evaluation/curriculum_eval.py).

Uses a tiny model and a tiny hand-made task/test set in a temp dir; checks
that losses are finite, the quiz scoring works, and BOTH modes are fully
deterministic (same inputs -> identical results).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from evaluation.curriculum_eval import (
    normalize,
    run_generation_quiz,
    category_losses,
)
from model import AnkitModel
from model.config import Config
from tokenizer.tokenizer import AnkitTokenizer


@pytest.fixture
def tiny_eval_model(tiny_tokenizer):
    cfg = Config.load("configs/smoke.yaml")
    cfg.model.vocab_size = tiny_tokenizer.vocab_size
    cfg.model.context_length = 32
    cfg.model.d_model = 32
    cfg.model.n_layers = 1
    cfg.model.n_heads = 2
    cfg.model.ffn_dim = 64
    torch.manual_seed(0)
    return AnkitModel(cfg.model)


@pytest.fixture
def tiny_test_set(tmp_path, tiny_tokenizer):
    rows = [
        {"text": "Question: What is 2 + 2?\nAnswer: 2 + 2 = 4.", "category": "math"},
        {"text": "Question: What is 3 + 3?\nAnswer: 3 + 3 = 6.", "category": "math"},
        {"text": "The sun gives us light and heat in the day.", "category": "science"},
        {"text": "Ped humein oxygen dete hain.", "category": "hinglish"},
    ]
    path = tmp_path / "test.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


@pytest.fixture
def tiny_tasks(tmp_path):
    tasks = [
        {"id": "m1", "category": "math", "prompt": "Question: What is 2 + 2?\nAnswer:",
         "ideal": "4", "accept": ["4"], "match": "contains"},
        {"id": "s1", "category": "science", "prompt": "Question: What gives us light in the day?\nAnswer:",
         "ideal": "the sun", "accept": ["sun"], "match": "contains"},
    ]
    path = tmp_path / "tasks.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for task in tasks:
            handle.write(json.dumps(task) + "\n")
    return path


def test_normalize_strips_case_and_punctuation():
    assert normalize("Hello, World!") == normalize("hello world")
    assert normalize("  2 + 3  = 5. ") == "2 3 5"
    assert normalize("Silver-fox") == normalize("silver fox")


def test_category_losses_are_finite_and_per_category(tiny_eval_model, tiny_tokenizer, tiny_test_set):
    tiny_eval_model.eval()
    results = category_losses(
        tiny_eval_model, tiny_tokenizer, tiny_test_set, "cpu", context_length=32
    )
    assert {"math", "science", "hinglish", "overall"} <= set(results)
    for category, data in results.items():
        assert data["loss_per_token"] > 0.0
        assert data["loss_per_token"] < 100.0  # finite, sane
        assert data["tokens"] > 0
    assert results["overall"]["tokens"] == sum(
        results[c]["tokens"] for c in ("math", "science", "hinglish")
    )


def test_generation_quiz_runs_and_scores(tiny_eval_model, tiny_tokenizer, tiny_tasks):
    out = run_generation_quiz(tiny_eval_model, tiny_tokenizer, tiny_tasks, "cpu")
    assert {"math", "science"} <= set(out["summary"])
    for category in ("math", "science"):
        assert out["summary"][category]["total"] == 1
        assert 0.0 <= out["summary"][category]["accuracy"] <= 1.0
    assert out["summary"]["overall"]["total"] == 2
    assert len(out["details"]) == 2


def test_evaluation_is_deterministic(tiny_eval_model, tiny_tokenizer, tiny_tasks, tiny_test_set):
    tiny_eval_model.eval()
    out1 = run_generation_quiz(tiny_eval_model, tiny_tokenizer, tiny_tasks, "cpu")
    out2 = run_generation_quiz(tiny_eval_model, tiny_tokenizer, tiny_tasks, "cpu")
    assert out1 == out2, "greedy quiz must be fully deterministic"

    loss1 = category_losses(tiny_eval_model, tiny_tokenizer, tiny_test_set, "cpu", 32)
    loss2 = category_losses(tiny_eval_model, tiny_tokenizer, tiny_test_set, "cpu", 32)
    assert loss1 == loss2, "loss mode must be fully deterministic"


def test_real_task_file_loads_and_is_complete():
    tasks_path = Path("evaluation/tasks/curriculum_tasks.jsonl")
    if not tasks_path.exists():  # pragma: no cover
        pytest.skip("task file not committed")
    tasks = [json.loads(line) for line in tasks_path.read_text(encoding="utf-8").splitlines()
             if line.strip()]
    assert len(tasks) >= 100
    required = {"english_vocab", "english_grammar", "english_comprehension", "hinglish",
                "math", "word_problems", "science", "social", "reasoning", "instructions"}
    assert {t["category"] for t in tasks} == required
    for t in tasks:
        assert t["prompt"].rstrip().endswith("Answer:")
        assert t["ideal"] and t["accept"]
        assert all(isinstance(a, str) for a in t["accept"])
        ids = {t["id"] for t in tasks}
        assert len(ids) == len(tasks), "task ids must be unique"
        break
