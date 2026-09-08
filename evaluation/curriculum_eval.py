"""ANKIT 0.1 — Class 1-4 curriculum evaluation suite.

Two complementary, deterministic measurements:

1. LOSS MODE  (``--mode loss``)
   Per-category mean loss on the HELD-OUT test split (data/curriculum/
   test.jsonl). Teacher-forced next-token loss per category shows WHERE the
   model is strong or weak (math vs hinglish vs science ...) and is the
   primary signal at base-LM scale.

2. GENERATION MODE  (``--mode generate``)
   100 hand-written tasks (evaluation/tasks/curriculum_tasks.jsonl) across
   ten categories. The model completes ``Question: ...\\nAnswer:`` greedily
   (top_k=1) and the answer is matched against accepted answers. This is a
   strict quiz score: useful to compare a model BEFORE vs AFTER training.

Run:
    python -m evaluation.curriculum_eval --ckpt checkpoints/ankit_0_1_50m/step_24000
    python -m evaluation.curriculum_eval --baseline            # untrained model
    python -m evaluation.curriculum_eval --mode both --ckpt ...

Everything is deterministic: greedy decoding, fixed seeds, fixed task lists.
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
import torch.nn.functional as F  # noqa: E402

from model import AnkitModel  # noqa: E402
from model.config import Config  # noqa: E402
from tokenizer.tokenizer import AnkitTokenizer  # noqa: E402
from training.checkpoint import load_checkpoint_model  # noqa: E402

DEFAULT_TASKS = Path("evaluation/tasks/curriculum_tasks.jsonl")
DEFAULT_TEST = Path("data/curriculum/test.jsonl")
DEFAULT_TOKENIZER = "tokenizer/ankit_tokenizer.json"
DEFAULT_CONFIG = "configs/ankit_0_1.yaml"

CATEGORIES = [
    "english_vocab", "english_grammar", "english_comprehension", "hinglish",
    "math", "word_problems", "science", "social", "reasoning", "instructions",
]

_PUNCT_TABLE = str.maketrans({ch: " " for ch in string.punctuation})


def normalize(text: str) -> str:
    """Lowercase, replace punctuation with spaces, collapse whitespace."""
    text = text.lower().translate(_PUNCT_TABLE)
    return " ".join(text.split())


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------
def load_model(ckpt: str | None, config_path: str, device: str, baseline_seed: int):
    """Load a trained ANKIT checkpoint, or build a fresh baseline model."""
    if ckpt:
        model, config = load_checkpoint_model(ckpt, device=device)
        print(f"Loaded checkpoint: {ckpt} (step config from meta.json)")
        return model, config
    config = Config.load(config_path)
    # Use the REAL tokenizer vocab so the baseline matches trained models.
    tok = AnkitTokenizer.load(DEFAULT_TOKENIZER)
    config.model.vocab_size = tok.vocab_size
    torch.manual_seed(baseline_seed)
    model = AnkitModel(config.model).to(device)
    print(f"Built UNTRAINED baseline model (seed {baseline_seed}) — "
          f"{model.num_parameters():,} parameters.")
    return model, config


# ---------------------------------------------------------------------------
# Loss mode — per-category held-out loss
# ---------------------------------------------------------------------------
@torch.no_grad()
def category_losses(
    model: AnkitModel,
    tokenizer: AnkitTokenizer,
    test_path: Path,
    device: str,
    context_length: int,
) -> dict:
    """Mean per-token NLL per category on the held-out test split."""
    if not test_path.exists():
        raise FileNotFoundError(
            f"{test_path} not found. Run scripts/build_curriculum.py first."
        )
    rows = [json.loads(line) for line in test_path.read_text(encoding="utf-8").splitlines()
            if line.strip()]

    model.eval()
    nll_by_cat: dict[str, list[float]] = defaultdict(list)
    tok_by_cat: dict[str, int] = defaultdict(int)

    for row in rows:
        category = row.get("category", "unknown")
        ids = tokenizer.encode(row["text"], add_bos=True, add_eos=True)
        if len(ids) < 2:
            continue
        # Chunk long texts into context-length windows.
        for start in range(0, len(ids) - 1, context_length):
            chunk = ids[start:start + context_length + 1]
            if len(chunk) < 2:
                continue
            x = torch.tensor([chunk[:-1]], dtype=torch.long, device=device)
            y = torch.tensor([chunk[1:]], dtype=torch.long, device=device)
            logits = model(x)
            loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)), y.reshape(-1), reduction="sum"
            )
            nll_by_cat[category].append(float(loss.item()))
            tok_by_cat[category] += y.numel()

    results = {}
    total_nll, total_tok = 0.0, 0
    for category in sorted(nll_by_cat):
        nll = sum(nll_by_cat[category])
        toks = tok_by_cat[category]
        total_nll += nll
        total_tok += toks
        results[category] = {
            "loss_per_token": nll / toks,
            "tokens": toks,
            "documents": len(rows_by_category(rows, category)),
        }
    results["overall"] = {"loss_per_token": total_nll / total_tok, "tokens": total_tok}
    return results


def rows_by_category(rows: list[dict], category: str) -> list[dict]:
    return [r for r in rows if r.get("category") == category]


# ---------------------------------------------------------------------------
# Generation mode — deterministic quiz
# ---------------------------------------------------------------------------
@torch.no_grad()
def run_generation_quiz(
    model: AnkitModel,
    tokenizer: AnkitTokenizer,
    tasks_path: Path,
    device: str,
    max_new_tokens: int = 24,
) -> dict:
    if not tasks_path.exists():
        raise FileNotFoundError(f"Task file not found: {tasks_path}")
    tasks = [json.loads(line) for line in tasks_path.read_text(encoding="utf-8").splitlines()
             if line.strip()]

    model.eval()
    per_category: dict[str, dict[str, int]] = defaultdict(lambda: {"correct": 0, "total": 0})
    details = []

    for task in tasks:
        ids = tokenizer.encode(task["prompt"], add_bos=True, add_eos=False) or \
            [tokenizer.bos_id]
        x = torch.tensor([ids], dtype=torch.long, device=device)
        out = model.generate(
            x, max_new_tokens=max_new_tokens, temperature=1.0, top_k=1, seed=0
        )
        continuation = out[0, x.shape[1]:].tolist()
        answer = tokenizer.decode(continuation, skip_special=True)
        answer = answer.split("\n")[0].strip()  # take just the answer line

        target = normalize(task["ideal"])
        produced = normalize(answer)
        if task.get("match", "contains") == "exact":
            correct = produced == target
        else:
            correct = any(normalize(acc) in produced for acc in task.get("accept", [task["ideal"]]))

        category = task["category"]
        per_category[category]["total"] += 1
        per_category[category]["correct"] += int(correct)
        details.append({
            "id": task["id"], "category": category, "correct": bool(correct),
            "expected": task["ideal"], "generated": answer,
        })

    results = {}
    total_correct = total = 0
    for category in CATEGORIES:
        if category not in per_category:
            continue
        c, t = per_category[category]["correct"], per_category[category]["total"]
        total_correct += c
        total += t
        results[category] = {"correct": c, "total": t, "accuracy": c / t if t else 0.0}
    results["overall"] = {
        "correct": total_correct, "total": total,
        "accuracy": total_correct / total if total else 0.0,
    }
    return {"summary": results, "details": details}


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def print_report(mode: str, results: dict, elapsed: float) -> None:
    print(f"\n{'=' * 62}\nANKIT 0.1 curriculum evaluation — {mode} mode\n{'=' * 62}")
    if "loss" in results:
        print(f"{'category':<24}{'loss/token':>12}{'tokens':>10}")
        print("-" * 46)
        for category, data in results["loss"].items():
            if category == "overall":
                continue
            print(f"{category:<24}{data['loss_per_token']:>12.4f}{data['tokens']:>10,}")
        overall = results["loss"]["overall"]
        print("-" * 46)
        print(f"{'OVERALL':<24}{overall['loss_per_token']:>12.4f}{overall['tokens']:>10,}")
    if "generate" in results:
        print(f"\n{'category':<24}{'correct':>9}{'total':>7}{'accuracy':>10}")
        print("-" * 50)
        for category, data in results["generate"]["summary"].items():
            if category == "overall":
                continue
            print(f"{category:<24}{data['correct']:>9}/{data['total']:<5}"
                  f"{data['accuracy'] * 100:>9.1f}%")
        overall = results["generate"]["summary"]["overall"]
        print("-" * 50)
        print(f"{'OVERALL':<24}{overall['correct']:>9}/{overall['total']:<5}"
              f"{overall['accuracy'] * 100:>9.1f}%")
    print(f"{'=' * 62}\n({elapsed:.1f}s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate ANKIT on the Class 1-4 curriculum.")
    parser.add_argument("--ckpt", default=None, help="Checkpoint dir (default: latest in output dir).")
    parser.add_argument("--baseline", action="store_true",
                        help="Evaluate an UNTRAINED model instead of a checkpoint.")
    parser.add_argument("--baseline-seed", type=int, default=1337)
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Config for the baseline model.")
    parser.add_argument("--tokenizer", default=DEFAULT_TOKENIZER)
    parser.add_argument("--tasks", default=str(DEFAULT_TASKS))
    parser.add_argument("--test", default=str(DEFAULT_TEST))
    parser.add_argument("--mode", choices=["loss", "generate", "both"], default="both")
    parser.add_argument("--max-new-tokens", type=int, default=24)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--save", default=None, help="Write JSON results to this file.")
    args = parser.parse_args()

    from training.checkpoint import latest_checkpoint

    ckpt = args.ckpt
    if not args.baseline and ckpt is None:
        latest = latest_checkpoint("checkpoints/ankit_0_1_50m")
        ckpt = str(latest) if latest else None
        if ckpt is None:
            print("[warn] no checkpoint found; evaluating the untrained baseline instead.")
            args.baseline = True

    device = args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
    model, config = load_model(ckpt, args.config, device, args.baseline_seed)
    tokenizer = AnkitTokenizer.load(args.tokenizer)
    if model.config.vocab_size != tokenizer.vocab_size:
        raise SystemExit(
            f"Model vocab {model.config.vocab_size} != tokenizer vocab "
            f"{tokenizer.vocab_size}. Retrain the tokenizer or use the "
            "matching checkpoint."
        )

    t0 = time.time()
    results: dict = {}
    if args.mode in ("loss", "both"):
        print("Computing per-category held-out loss ...")
        results["loss"] = category_losses(
            model, tokenizer, Path(args.test), device, config.model.context_length
        )
    if args.mode in ("generate", "both"):
        print("Running generation quiz (greedy, deterministic) ...")
        results["generate"] = run_generation_quiz(
            model, tokenizer, Path(args.tasks), device, args.max_new_tokens
        )
    elapsed = time.time() - t0

    label = "untrained baseline" if args.baseline else str(ckpt)
    print(f"\nModel: {label}")
    print_report(args.mode, results, elapsed)

    if args.save:
        payload = {
            "model": label,
            "params": model.num_parameters(),
            "mode": args.mode,
            "results": results,
            "elapsed_seconds": round(elapsed, 2),
        }
        Path(args.save).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Results written to {args.save}")


if __name__ == "__main__":
    main()
