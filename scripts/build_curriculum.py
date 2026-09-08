#!/usr/bin/env python3
"""Build the Class 1-4 ANKIT curriculum into data/curriculum/.

This generates our OWN original educational corpus (English + Hinglish +
Maths + Science/EVS + Social studies + Reasoning), stage by stage:

    stage 1-4 : Class 1..4 material (each with a revision slice of earlier
                classes, so old knowledge keeps being rehearsed)
    stage 5   : full mixed revision across Classes 1-4
    stage 6   : exercise/QA/reasoning-heavy mix for the evaluation +
                weak-area-reinforcement round

Plus: a stratified, hash-stable validation/test split (disjoint from train),
a tokenizer-training corpus (train split only), and stats.json.

Usage:
    python scripts/build_curriculum.py                 # default output dir
    python scripts/build_curriculum.py --out data/curriculum
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from curriculum.build import build_all  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the ANKIT Class 1-4 curriculum.")
    parser.add_argument("--out", default="data/curriculum", help="Output directory.")
    args = parser.parse_args()

    print(f"Building curriculum into {args.out} ...")
    stats = build_all(args.out)

    total_train = sum(s["items"] for s in stats["train_stages"].values())
    print("\nDone. Curriculum statistics:")
    print(f"  raw items collected      : {stats['raw_items']:,}")
    print(f"  duplicates removed       : {stats['duplicates_removed']:,}")
    print(f"  tokenizer corpus         : {stats['tokenizer_corpus']['items']:,} docs "
          f"({stats['tokenizer_corpus']['chars']:,} chars)")
    for stage in range(1, 7):
        s = stats['train_stages'][f'stage{stage}']
        cats = ", ".join(f"{c}={n}" for c, n in sorted(s["by_category"].items()))
        print(f"  stage{stage} train            : {s['items']:>5} items | {s['chars']:>8,} chars | {cats}")
    for split in ("val", "test"):
        s = stats[split]
        print(f"  {split:<24} : {s['items']:>5} items | {s['chars']:>8,} chars")
    print(f"\nFull stats written to {Path(args.out) / 'stats.json'}")


if __name__ == "__main__":
    main()
