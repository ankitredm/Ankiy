#!/usr/bin/env python3
"""Prepare an ANKIT 0.1 dataset from raw text.

This runs the full pipeline defined in ``configs/data.yaml``:

    raw text  ->  clean + normalise  ->  filter  ->  dedup  ->  split
               ->  train/val/test .jsonl  +  statistics report

It is CPU-only and fully deterministic (same config + data + seed => same
output). It never downloads a model or uses a pretrained anything.

Usage:
    python scripts/prepare_dataset.py                          # default config
    python scripts/prepare_dataset.py --config configs/data.yaml
    python scripts/prepare_dataset.py --config configs/data.yaml --only-stats

For the real training corpus, first put legal text into data/raw/ (e.g. run
``python scripts/download_gutenberg.py`` on a machine with internet, or drop
any public/open .txt or .jsonl files into data/raw/), then run this.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make `python scripts/<name>.py` work from anywhere: put the repo root
# on sys.path so project packages (model/, tokenizer/, ...) are importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
from pathlib import Path

from dataprep.pipeline import run_pipeline

DEFAULT_CONFIG = "configs/data.yaml"


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the ANKIT 0.1 dataset.")
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help=f"Path to a data config YAML (default: {DEFAULT_CONFIG}).",
    )
    parser.add_argument(
        "--only-stats",
        action="store_true",
        help="Only print stats from an existing stats.json, do not re-run.",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    stats = run_pipeline(config_path)
    print(f"\nStatistics written to {stats.get('stats_file', 'data/stats/stats.json')}")
    return


if __name__ == "__main__":
    main()
