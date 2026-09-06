#!/usr/bin/env python3
"""Print the dataset statistics from a saved stats.json.

Run this after ``scripts/prepare_dataset.py`` to display the stats again
without re-running the (expensive) pipeline.

Usage:
    python scripts/data_stats.py                         # default stats file
    python scripts/data_stats.py --stats data/stats/stats.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dataprep.stats import format_stats

DEFAULT = "data/stats/stats.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Display dataset statistics.")
    parser.add_argument("--stats", default=DEFAULT, help=f"Path to stats.json (default: {DEFAULT}).")
    args = parser.parse_args()

    path = Path(args.stats)
    if not path.exists():
        print(f"Stats file not found: {path}")
        print("Run `python scripts/prepare_dataset.py` first.")
        return

    with path.open("r", encoding="utf-8") as handle:
        stats = json.load(handle)
    print(format_stats(stats))
    if "elapsed_seconds" in stats:
        print(f"\nPipeline took {stats['elapsed_seconds']}s")


if __name__ == "__main__":
    main()
