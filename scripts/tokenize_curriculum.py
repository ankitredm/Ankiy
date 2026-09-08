#!/usr/bin/env python3
"""Tokenize the Class 1-4 curriculum into training-ready .bin files.

Reads the JSONL files produced by ``scripts/build_curriculum.py`` and encodes
them with OUR OWN trained tokenizer into uint16 token streams:

    data/curriculum/stages/stageN_train.jsonl -> data/tokenized/curriculum/stageN_train.bin
    data/curriculum/val.jsonl                 -> data/tokenized/curriculum/val.bin
    data/curriculum/test.jsonl                -> data/tokenized/curriculum/test.bin

Each document is wrapped with BOS ... EOS so the model learns document
boundaries (same convention as scripts/tokenize_dataset.py).

Usage:
    python scripts/tokenize_curriculum.py
    python scripts/tokenize_curriculum.py --tokenizer tokenizer/ankit_tokenizer.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tokenizer.tokenizer import AnkitTokenizer  # noqa: E402

DEFAULT_TOKENIZER = "tokenizer/ankit_tokenizer.json"
DEFAULT_SRC = "data/curriculum"
DEFAULT_DST = "data/tokenized/curriculum"


def _texts_from_jsonl(path: Path) -> list[str]:
    texts: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj, dict) and isinstance(obj.get("text"), str):
                texts.append(obj["text"])
            elif isinstance(obj, str):
                texts.append(obj)
    return texts


def tokenize_split(tokenizer: AnkitTokenizer, src: Path, dst: Path) -> dict:
    """Encode a curriculum JSONL into a .bin stream. Returns stats."""
    texts = _texts_from_jsonl(src)
    if not texts:
        raise RuntimeError(
            f"No documents found in {src}. Run scripts/build_curriculum.py first."
        )
    all_ids: list[int] = []
    for text in texts:
        all_ids.extend(tokenizer.encode(text, add_bos=True, add_eos=True))
    if not all_ids:
        raise RuntimeError(f"Tokenizer produced no tokens for {src}.")
    import numpy as np

    arr = np.array(all_ids, dtype=np.uint32)
    if arr.max() > 65535:
        raise RuntimeError(
            f"Token id {arr.max()} exceeds uint16 range — vocab is too large."
        )
    dst.parent.mkdir(parents=True, exist_ok=True)
    arr.astype(np.uint16).tofile(str(dst))
    return {"documents": len(texts), "tokens": int(arr.shape[0]), "bytes": dst.stat().st_size}


def main() -> None:
    parser = argparse.ArgumentParser(description="Tokenize the ANKIT curriculum.")
    parser.add_argument("--tokenizer", default=DEFAULT_TOKENIZER)
    parser.add_argument("--src", default=DEFAULT_SRC, help="Curriculum JSONL dir.")
    parser.add_argument("--dst", default=DEFAULT_DST, help="Output .bin dir.")
    args = parser.parse_args()

    tokenizer = AnkitTokenizer.load(args.tokenizer)
    src, dst = Path(args.src), Path(args.dst)
    print(f"Tokenizer : {args.tokenizer} (vocab {tokenizer.vocab_size:,})")
    print(f"Reading   : {src}")
    print(f"Writing   : {dst}\n")

    jobs: list[tuple[str, Path, Path]] = []
    for stage in range(1, 7):
        jobs.append((f"stage{stage}_train", src / "stages" / f"stage{stage}_train.jsonl",
                     dst / f"stage{stage}_train.bin"))
    jobs.append(("val", src / "val.jsonl", dst / "val.bin"))
    jobs.append(("test", src / "test.jsonl", dst / "test.bin"))

    total_tokens = 0
    for name, src_path, dst_path in jobs:
        if not src_path.exists():
            print(f"  [skip] {src_path} not found — run scripts/build_curriculum.py")
            continue
        stats = tokenize_split(tokenizer, src_path, dst_path)
        total_tokens += stats["tokens"]
        print(f"  {name:<14} {stats['documents']:>5} docs -> {stats['tokens']:>9,} tokens "
              f"-> {dst_path}")
    print(f"\nDone. Total tokens: {total_tokens:,}")


if __name__ == "__main__":
    main()
