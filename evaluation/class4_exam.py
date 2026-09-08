"""ANKIT 0.1 — Class 4 EXAMINATION runner.

This is an EXAM, not a training run:
  - the checkpoint is loaded read-only; nothing is ever optimized,
  - the model's state-dict fingerprint is taken BEFORE and AFTER the exam and
    must be identical (hard proof that no training occurred),
  - every question is checked against the training corpus with an 8-gram
    anti-memorization test; any overlap is reported,
  - answers are generated greedily (top_k=1), fully deterministic.

Grading is strict and automatic:
  - objective modes: numeric / numeric_max / numeric_sequence / match_any /
    match_all / min_matches / one_word_any (word-boundary, normalized),
  - open-ended: multi-component rubrics with partial credit — a single echoed
    keyword never earns full marks.

Usage:
    python -m evaluation.class4_exam --ckpt checkpoints/demo_50m/step_120
    python -m evaluation.class4_exam --verbose          # print every answer
"""

from __future__ import annotations

import argparse
import json
import re
import string
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch  # noqa: E402

from evaluation.curriculum_eval import load_model, normalize  # noqa: E402
from training.provenance import state_dict_fingerprint  # noqa: E402

DEFAULT_TASKS = Path("evaluation/tasks/class4_exam.jsonl")
DEFAULT_CORPUS_DIR = Path("data/curriculum")
EXTRA_SOURCES = [Path("evaluation/tasks/curriculum_tasks.jsonl")]

SECTION_TITLES = {
    "english": "English",
    "hinglish": "Hinglish",
    "math": "Mathematics",
    "science": "Science/EVS",
    "social": "Social Studies",
    "reasoning": "Reasoning",
    "instructions": "Instruction following",
    "writing": "Writing",
}

_NGRAM = 8  # words per anti-memorization shingle


# ---------------------------------------------------------------------------
# Grading primitives
# ---------------------------------------------------------------------------
_NUM_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


def extract_numbers(text: str) -> list[float]:
    """All numbers in the text (commas stripped), in order of appearance."""
    return [float(m.group(0).replace(",", "")) for m in _NUM_RE.finditer(text)]


def contains_term(haystack_norm: str, term_norm: str) -> bool:
    """Word-boundary substring match on normalized text."""
    pattern = r"(?<!\w)" + re.escape(term_norm) + r"(?!\w)"
    return re.search(pattern, haystack_norm) is not None


def _component_matches(component: dict, raw: str, norm: str) -> bool:
    if "min_words" in component:
        return len(norm.split()) >= component["min_words"]
    if "min_sentences" in component:
        sentences = len(re.findall(r"[.!?]+", raw))
        return sentences >= component["min_sentences"]
    if "all" in component:
        return all(contains_term(norm, t) for t in component["all"])
    if "any" in component:
        return any(contains_term(norm, t) for t in component["any"])
    raise ValueError(f"Unknown rubric component: {component}")


def grade_answer(grade: dict, raw_answer: str) -> float:
    """Return credit in {1.0 (correct), 0.5 (partial), 0.0 (incorrect)}."""
    first_line = raw_answer.strip().splitlines()[0] if raw_answer.strip() else ""
    norm = normalize(first_line)
    # Numbers must come from the RAW line: normalize() replaces '.' with a
    # space, which would destroy decimals like 2.5.
    raw_nums = extract_numbers(first_line)

    mode = grade["mode"]
    if mode == "numeric":
        nums = raw_nums
        target = float(grade["answer"])
        ok = any(abs(n - target) < 1e-6 for n in nums)
        if not ok and grade.get("terms"):
            ok = any(contains_term(norm, normalize(t)) for t in grade["terms"])
        return 1.0 if ok else 0.0

    if mode == "numeric_max":
        nums = raw_nums
        return 1.0 if nums and abs(max(nums) - float(grade["answer"])) < 1e-6 else 0.0

    if mode == "numeric_sequence":
        nums = raw_nums
        expected = [float(x) for x in grade["answer"]]
        return 1.0 if nums == expected else 0.0

    if mode == "match_any":
        ok = any(contains_term(norm, normalize(t)) for t in grade["terms"])
        return 1.0 if ok else 0.0

    if mode == "match_all":
        ok = all(contains_term(norm, normalize(t)) for t in grade["terms"])
        return 1.0 if ok else 0.0

    if mode == "min_matches":
        hits = sum(1 for t in grade["terms"] if contains_term(norm, normalize(t)))
        return 1.0 if hits >= grade["min"] else 0.0

    if mode == "one_word_any":
        words = norm.split()
        if len(words) != 1:
            return 0.0
        return 1.0 if any(words[0] == normalize(t) for t in grade["terms"]) else 0.0

    if mode == "rubric":
        components = grade["components"]
        matched = sum(1 for c in components if _component_matches(c, first_line, norm))
        frac = matched / len(components)
        if frac >= 0.99:
            return 1.0
        if frac >= 0.5:
            return 0.5
        return 0.0

    raise ValueError(f"Unknown grading mode: {mode}")


# ---------------------------------------------------------------------------
# Anti-memorization check
# ---------------------------------------------------------------------------
def corpus_ngrams(corpus_dir: Path, extra_sources: list[Path]) -> set[tuple]:
    """All {NGRAM}-word shingles from every training/eval-corpus document."""
    grams: set[tuple] = set()
    paths: list[Path] = []
    if corpus_dir.exists():
        paths += sorted(corpus_dir.rglob("*.jsonl"))
    paths += [p for p in extra_sources if p.exists()]
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            texts = []
            if isinstance(row, dict):
                if isinstance(row.get("text"), str):
                    texts.append(row["text"])
                if isinstance(row.get("prompt"), str):
                    texts.append(row["prompt"])
            elif isinstance(row, str):
                texts.append(row)
            for text in texts:
                words = normalize(text).split()
                for i in range(len(words) - _NGRAM + 1):
                    grams.add(tuple(words[i:i + _NGRAM]))
    return grams


def anti_memorization_check(tasks: list[dict], grams: set[tuple]) -> dict:
    """Flag any exam prompt sharing an {NGRAM}-word shingle with the corpus."""
    flagged = []
    for task in tasks:
        words = normalize(task["prompt"]).split()
        hits = [tuple(words[i:i + _NGRAM]) in grams
                for i in range(len(words) - _NGRAM + 1)]
        if any(hits):
            flagged.append(task["id"])
    return {"checked": len(tasks), "shingle_size": _NGRAM,
            "corpus_shingles": len(grams), "flagged_ids": flagged,
            "overlap": len(flagged)}


# ---------------------------------------------------------------------------
# The exam itself
# ---------------------------------------------------------------------------
@torch.no_grad()
def run_exam(model, tokenizer, tasks: list[dict], device: str) -> list[dict]:
    model.eval()
    results = []
    for idx, task in enumerate(tasks, 1):
        ids = tokenizer.encode(task["prompt"], add_bos=True, add_eos=False) or \
            [tokenizer.bos_id]
        x = torch.tensor([ids], dtype=torch.long, device=device)
        out = model.generate(
            x, max_new_tokens=task.get("max_new_tokens", 24),
            temperature=1.0, top_k=1, seed=0,
        )
        continuation = out[0, x.shape[1]:].tolist()
        raw = tokenizer.decode(continuation, skip_special=True)
        answer = raw.strip().splitlines()[0].strip() if raw.strip() else ""
        credit = grade_answer(task["grade"], raw)
        results.append({
            "id": task["id"], "section": task["section"], "skill": task.get("skill", ""),
            "category": task["category"], "type": task["type"],
            "question": task["prompt"], "expected": str(task["grade"].get(
                "answer", task["grade"].get("terms", task["grade"].get("components", "")))),
            "model_answer": answer, "credit": credit,
            "verdict": ("correct" if credit == 1.0 else
                        "partial" if credit == 0.5 else "incorrect"),
        })
        flag = {"correct": "+", "partial": "~", "incorrect": "x"}[results[-1]["verdict"]]
        print(f"  [{idx:>3}/{len(tasks)}] {flag} {task['id']:<10} "
              f"credit={credit:.1f}  ans={answer[:60]!r}")
    return results


def summarize(results: list[dict]) -> dict:
    by_section: dict[str, list[float]] = defaultdict(list)
    by_skill: dict[str, list[float]] = defaultdict(list)
    for r in results:
        by_section[r["section"]].append(r["credit"])
        if r["skill"]:
            by_skill[r["skill"]].append(r["credit"])

    pct = lambda xs: round(100.0 * sum(xs) / len(xs), 1) if xs else None  # noqa: E731
    summary = {
        "sections": {SECTION_TITLES[s]: pct(v) for s, v in sorted(by_section.items())},
        "skills": {s: pct(v) for s, v in sorted(by_skill.items())},
        "overall": round(100.0 * sum(r["credit"] for r in results) / len(results), 1),
        "counts": {
            "total": len(results),
            "correct": sum(1 for r in results if r["credit"] == 1.0),
            "partial": sum(1 for r in results if r["credit"] == 0.5),
            "incorrect": sum(1 for r in results if r["credit"] == 0.0),
        },
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Class 4 examination for ANKIT 0.1 (read-only).")
    parser.add_argument("--ckpt", default=None,
                        help="Checkpoint dir (default: latest under checkpoints/demo_50m).")
    parser.add_argument("--baseline", action="store_true", help="Examine an untrained model.")
    parser.add_argument("--config", default="configs/ankit_0_1.yaml")
    parser.add_argument("--tokenizer", default="tokenizer/ankit_tokenizer.json")
    parser.add_argument("--tasks", default=str(DEFAULT_TASKS))
    parser.add_argument("--corpus-dir", default=str(DEFAULT_CORPUS_DIR),
                        help="Training-corpus dir for the anti-memorization check.")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--out", default="evaluation/results/class4_exam_results.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    tasks = [json.loads(l) for l in Path(args.tasks).read_text(encoding="utf-8").splitlines()
             if l.strip()]
    print(f"EXAM: {len(tasks)} questions loaded from {args.tasks}")

    ckpt = args.ckpt
    if not args.baseline and ckpt is None:
        from training.checkpoint import latest_checkpoint
        latest = latest_checkpoint("checkpoints/demo_50m")
        ckpt = str(latest) if latest else None
        if ckpt is None:
            raise SystemExit("No checkpoint found under checkpoints/demo_50m.")
    model, config = load_model(ckpt, args.config, args.device, baseline_seed=1337)

    fingerprint_before = state_dict_fingerprint(model.state_dict())
    params = model.num_parameters()

    tokenizer = AnkitTokenizer_load(args.tokenizer)
    if model.config.vocab_size != tokenizer.vocab_size:
        raise SystemExit("Tokenizer/model vocab mismatch — cannot examine.")

    # Anti-memorization gate.
    grams = corpus_ngrams(Path(args.corpus_dir), EXTRA_SOURCES)
    memo = anti_memorization_check(tasks, grams)
    print(f"Anti-memorization: {memo['overlap']}/{memo['checked']} questions share an "
          f"{memo['shingle_size']}-word shingle with the training corpus "
          f"({memo['corpus_shingles']:,} shingles scanned)."
          + (f" FLAGGED: {memo['flagged_ids']}" if memo["flagged_ids"] else ""))

    print("\nRunning the examination (greedy, deterministic, no training) ...")
    t0 = time.time()
    results = run_exam(model, tokenizer, tasks, args.device)
    elapsed = time.time() - t0

    fingerprint_after = state_dict_fingerprint(model.state_dict())
    unchanged = fingerprint_before == fingerprint_after

    summary = summarize(results)
    out = {
        "checkpoint": "untrained baseline" if args.baseline else str(ckpt),
        "parameters": params,
        "no_training_during_exam": unchanged,
        "fingerprint_before": fingerprint_before[:16],
        "fingerprint_after": fingerprint_after[:16],
        "anti_memorization": memo,
        "summary": summary,
        "elapsed_seconds": round(elapsed, 1),
        "results": results,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'=' * 64}\nCLASS 4 EXAMINATION — RESULTS\n{'=' * 64}")
    for section, score in summary["sections"].items():
        print(f"  {section:<24} {score:>6.1f} / 100")
    for skill, score in summary["skills"].items():
        print(f"  [skill] {skill:<17} {score:>6.1f} / 100")
    c = summary["counts"]
    print(f"  {'OVERALL':<24} {summary['overall']:>6.1f} / 100")
    print(f"  correct={c['correct']}  partial={c['partial']}  "
          f"incorrect={c['incorrect']}  total={c['total']}")
    print(f"  model unchanged during exam: {unchanged}")
    print(f"  ({elapsed:.0f}s) — full raw results: {out_path}")


def AnkitTokenizer_load(path: str):
    from tokenizer.tokenizer import AnkitTokenizer
    return AnkitTokenizer.load(path)


if __name__ == "__main__":
    main()
