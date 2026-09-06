#!/usr/bin/env python3
"""Tokenize the processed corpus into training-ready token ID files.

What this does
--------------
1. Loads ANKIT's OWN trained tokenizer (from Phase 4).
2. Reads each split (train / val / test) produced by Phase 3.
3. Encodes every document into token ids, adding BOS/</s> boundaries so the
   model learns document boundaries.
4. Concatenates each split into one long 1-D stream of token ids.
5. Writes the stream as a ``.bin`` file (uint16 numpy array) that can be loaded
   instantly with ``np.memmap`` — the fastest way to feed a GPU during training.

The model uses this file directly in ``training/dataset.py``. No pretrained
tokenizer or model is used anywhere.

Usage:
    python scripts/tokenize_dataset.py                    # default config
    python scripts/tokenize_dataset.py --config configs/ankit_0_1.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from model.config import Config
from tokenizer.tokenizer import AnkitTokenizer


def _load_text(path: Path) -> list[str]:
    """Read a split .jsonl from Phase 3 into a list of document strings."""
    texts: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            import json

            obj = json.loads(line)
            if isinstance(obj, dict) and isinstance(obj.get("text"), str):
                texts.append(obj["text"])
            elif isinstance(obj, str):
                texts.append(obj)
    return texts


def _encode_all(
    tokenizer: AnkitTokenizer, texts: list[str]
) -> np.ndarray:
    """Encode a list of documents into one concatenated uint16 token stream.

    Each document is wrapped with BOS ... EOS so the model learns where
    documents start and end.
    """
    all_ids: list[int] = []
    for text in texts:
        try:
            ids = tokenizer.encode(text, add_bos=True, add_eos=True)
        except Exception as exc:  # noqa: BLE001 - skip a single bad doc
            print(f"  [warn] could not encode a document: {exc}")
            continue
        all_ids.extend(ids)
    if not all_ids:
        raise RuntimeError("No tokens produced — corpus may be empty.")
    arr = np.array(all_ids, dtype=np.uint32)
    if arr.max() > 65535:
        raise RuntimeError(
            f"Token id {arr.max()} exceeds uint16 range. Either the vocab is "
            "larger than 65,536 or encoding produced an invalid id."
        )
    return arr.astype(np.uint16)


def tokenize_split(tokenizer: AnkitTokenizer, src: Path, dst: Path) -> dict:
    """Tokenize one split file into a .bin file. Returns stats."""
    texts = _load_text(src)
    arr = _encode_all(tokenizer, texts)
    dst.parent.mkdir(parents=True, exist_ok=True)
    arr.tofile(str(dst))
    return {
        "source": str(src),
        "destination": str(dst),
        "documents": len(texts),
        "tokens": int(arr.shape[0]),
        "bytes": int(dst.stat().st_size),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Tokenize ANKIT corpus into .bin files.")
    parser.add_argument(
        "--config",
        default="configs/ankit_0_1.yaml",
        help="Path to a model/training config (default: configs/ankit_0_1.yaml).",
    )
    args = parser.parse_args()

    config = Config.load(args.config)
    tcfg = config.training
    print(f"Tokenizing corpus for {config.name}")
    print(f"Tokenizer : {tcfg.tokenizer_path}")
    print(f"Vocab     : {config.model.vocab_size} (config) ")

    tokenizer = AnkitTokenizer.load(tcfg.tokenizer_path)
    print(f"Tokenizer vocab: {tokenizer.vocab_size}")

    sources = {
        "train": tcfg.train_data,
        "val": tcfg.val_data,
        "test": tcfg.test_data,
    }

    # The .bin files live next to train_data. Derive them from the configured
    # train_data path so they're always consistent.
    for split_name, data_path in sources.items():
        # Original .jsonl from Phase 3.
        jsonl_path = Path(f"data/processed/splits/{split_name}.jsonl")
        if not jsonl_path.exists():
            print(f"  [skip] no split file {jsonl_path} — run prepare_dataset.py")
            continue
        out_path = Path(data_path)
        stats = tokenize_split(tokenizer, jsonl_path, out_path)
        print(
            f"  {split_name:<6} {stats['documents']:>4} docs -> "
            f"{stats['tokens']:>7} tokens -> {out_path} ({stats['bytes']:,} bytes)"
        )

    print("Done. Data is ready for training/train.py")


if __name__ == "__main__":
    main()
