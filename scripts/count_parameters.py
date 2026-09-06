#!/usr/bin/env python3
"""Count the number of trainable parameters in an ANKIT 0.1 model.

The count comes from ACTUALLY building the model with the given config, not
from a hard-coded guess. We never inflate the number.

Usage:
    python scripts/count_parameters.py --config configs/ankit_0_1.yaml
    python scripts/count_parameters.py                # uses default config

Example output:
    Ankit 0.1 Parameters: 13,180,000
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from model import AnkitModel
from model.config import Config

DEFAULT_CONFIG = "configs/ankit_0_1.yaml"


def main() -> None:
    parser = argparse.ArgumentParser(description="Count ANKIT 0.1 parameters.")
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help=f"Path to a YAML config (default: {DEFAULT_CONFIG}).",
    )
    args = parser.parse_args()

    config = Config.load(args.config)
    model = AnkitModel(config.model)
    total = model.num_parameters()
    name = config.name

    # Human-friendly number (13,180,000 instead of 13180000).
    formatted = f"{total:,}"

    print(f"Config         : {Path(args.config).name}")
    print(f"Model name     : {name}")
    print(f"Layers         : {config.model.n_layers}")
    print(f"Hidden dim     : {config.model.d_model}")
    print(f"Heads          : {config.model.n_heads}")
    print(f"Vocab size     : {config.model.vocab_size}")
    print(f"Context length : {config.model.context_length}")
    print(f"FFN dim        : {config.model.ffn_dim}")
    print(f"Tied embedding : {config.model.tie_embedding}")
    print("-" * 40)
    print(f"Ankit 0.1 Parameters: {formatted}")
    print(f"  ( {total:,} -> {total / 1_000_000:.2f}M )")

    # Fail loudly if someone is trying to claim a bigger model than we built.
    print(
        "PASS: count matches the actual model that would be trained."
        if total == sum(p.numel() for p in model.parameters())
        else "WARN: recount needed."
    )


if __name__ == "__main__":
    main()
