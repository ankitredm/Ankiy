"""Train ANKIT 0.1's OWN tokenizer from scratch.

We use the Hugging Face ``tokenizers`` library (allowed infrastructure) but we
train a **brand-new** Byte-Pair Encoding tokenizer on **our own corpus** from
the Phase 3 pipeline. We do not load or copy Qwen, Llama, GPT, etc. tokenizers.

Why byte-level BPE?
- It can represent ANY text (any Unicode, any language) because the base
  "alphabet" is bytes, not fixed characters.
- It learns sub-word units that appear often in OUR corpus, so long common
  words become single tokens (efficient) and rare words become a few chunks.
- It is the same family used by modern LLMs, so it's a good fit for training
  a decoder-only Transformer from scratch.

The endpoint is a ``tokenizer/ankit_tokenizer.json`` file that supports both
``text -> token ids`` and ``token ids -> text``.

Usage:
    python tokenizer/train_tokenizer.py                              # default config
    python tokenizer/train_tokenizer.py --config configs/tokenizer.yaml
    python tokenizer/train_tokenizer.py --config configs/tokenizer.yaml --only-report
"""

from __future__ import annotations

import argparse
import glob
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

import yaml
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import ByteLevel as ByteLevelPreTokenizer
from tokenizers.processors import ByteLevel as ByteLevelProcessor
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.trainers import BpeTrainer

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
@dataclass
class TokenizerConfig:
    name: str
    version: str
    algorithm: str
    vocab_size: int
    input_paths: list[str]
    max_documents: Optional[int]
    special_tokens: list[str]
    min_frequency: int
    show_progress: bool
    output_dir: str
    tokenizer_file: str
    vocab_file: str
    report_file: str

    @classmethod
    def from_dict(cls, data: dict) -> "TokenizerConfig":
        inp = data.get("input", {})
        bpe = data.get("bpe", {})
        special = data.get("special_tokens", ["<unk>", "<s>", "</s>", "<pad>"])
        return cls(
            name=str(data.get("name", "ankit-tokenizer")),
            version=str(data.get("version", "0.1")),
            algorithm=str(data.get("algorithm", "bpe")),
            vocab_size=int(data.get("vocab_size", 16384)),
            input_paths=[str(p) for p in inp.get("paths", [])],
            max_documents=(
                int(inp["max_documents"]) if inp.get("max_documents") else None
            ),
            special_tokens=[str(t) for t in special],
            min_frequency=int(bpe.get("min_frequency", 2)),
            show_progress=bool(bpe.get("show_progress", True)),
            output_dir=str(data.get("output_dir", "tokenizer")),
            tokenizer_file=str(data.get("tokenizer_file", "tokenizer/ankit_tokenizer.json")),
            vocab_file=str(data.get("vocab_file", "tokenizer/vocab.json")),
            report_file=str(data.get("report_file", "tokenizer/tokenizer_report.json")),
        )


def load_config(path: str | Path = "configs/tokenizer.yaml") -> TokenizerConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Tokenizer config not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return TokenizerConfig.from_dict(raw)


# ---------------------------------------------------------------------------
# Corpus reading (from Phase 3 splits or raw .txt)
# ---------------------------------------------------------------------------
def _iter_text_from_file(path: Path) -> Iterable[str]:
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict) and isinstance(obj.get("text"), str):
                    yield obj["text"]
                elif isinstance(obj, str):
                    yield obj
    elif path.suffix.lower() == ".txt":
        raw = path.read_bytes()
        for enc in ("utf-8", "utf-8-sig", "latin-1"):
            try:
                yield raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            yield raw.decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported corpus file type: {path}")


def resolve_input_paths(patterns: list[str]) -> list[Path]:
    """Expand glob patterns into a sorted, de-duplicated list of files."""
    resolved: set[Path] = set()
    for pattern in patterns:
        for match in glob.glob(pattern, recursive=True):
            p = Path(match)
            if p.is_file():
                resolved.add(p.resolve())
    return sorted(resolved)


def iter_documents(paths: list[Path], max_documents: Optional[int]) -> Iterable[str]:
    """Yield text documents, honouring the max_documents cap."""
    count = 0
    for path in paths:
        for doc in _iter_text_from_file(path):
            yield doc
            count += 1
            if max_documents is not None and count >= max_documents:
                return


# ---------------------------------------------------------------------------
# Trainer
# ---------------------------------------------------------------------------
def count_characters(texts: Iterable[str]) -> int:
    return sum(len(t) for t in texts)


def build_tokenizer(cfg: TokenizerConfig) -> Tokenizer:
    """Create a new byte-level BPE tokenizer and train it on our corpus."""
    if cfg.algorithm != "bpe":
        raise ValueError(f"Only 'bpe' algorithm is supported, got {cfg.algorithm!r}.")

    tokenizer = Tokenizer(BPE())
    tokenizer.pre_tokenizer = ByteLevelPreTokenizer(add_prefix_space=True)

    trainer = BpeTrainer(
        vocab_size=cfg.vocab_size,
        min_frequency=cfg.min_frequency,
        special_tokens=cfg.special_tokens,
        show_progress=cfg.show_progress,
    )

    files = resolve_input_paths(cfg.input_paths)
    print(f"Corpus files ({len(files)}):")
    for f in files:
        print(f"  {f}")

    if not files:
        raise FileNotFoundError(
            "No corpus files found. Run `python scripts/prepare_dataset.py` first "
            "to produce data/processed/splits/train.jsonl."
        )

    # Train the tokenizer directly on the files (tokenizers supports file paths,
    # but we stream documents ourselves so we can count/sample and honor caps).
    texts = iter_documents(files, cfg.max_documents)
    # Consume into a list is not needed; trainer needs an iterator of strings OR
    # file paths. We pass an iterator of text strings via a small adapter.
    tokenizer.train_from_iterator(
        iter_documents_clean(files, cfg.max_documents), trainer=trainer
    )

    # Byte-level BPE needs a post-processor + decoder enabled to round-trip.
    tokenizer.post_processor = ByteLevelProcessor(trim_offsets=True)
    tokenizer.decoder = ByteLevelDecoder()
    return tokenizer


def iter_documents_clean(
    paths: list[Path], max_documents: Optional[int]
) -> Iterable[str]:
    """Same as iter_documents but strips any control chars for tokenizer safety."""
    for doc in iter_documents(paths, max_documents):
        yield "".join(ch for ch in doc if ord(ch) >= 32 or ch in "\n\t")


def run_training(cfg: TokenizerConfig) -> dict:
    """Train the tokenizer, save files, and return a report dict."""
    t0 = time.time()
    print(f"Training tokenizer: {cfg.name} v{cfg.version}")
    print(f"Algorithm: byte-level BPE | vocab target: {cfg.vocab_size}")

    tokenizer = build_tokenizer(cfg)
    vocab = tokenizer.get_vocab()

    # Save the HuggingFace tokenizer JSON (the main artifact).
    out_file = Path(cfg.tokenizer_file)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(out_file))

    # Also save a simple token->id vocab dict (nice for inspection).
    vocab_out = Path(cfg.vocab_file)
    vocab_out.parent.mkdir(parents=True, exist_ok=True)
    with vocab_out.open("w", encoding="utf-8") as handle:
        json.dump(vocab, handle, indent=2, ensure_ascii=False)

    # Special token IDs.
    special_ids = {}
    for special in cfg.special_tokens:
        special_ids[special] = tokenizer.token_to_id(special)

    elapsed = time.time() - t0
    report = {
        "name": cfg.name,
        "version": cfg.version,
        "algorithm": cfg.algorithm,
        "vocab_size": len(vocab),
        "target_vocab_size": cfg.vocab_size,
        "min_frequency": cfg.min_frequency,
        "special_tokens": special_ids,
        "files_read": len(resolve_input_paths(cfg.input_paths)),
        "elapsed_seconds": round(elapsed, 2),
    }

    # Save the report.
    rep_file = Path(cfg.report_file)
    rep_file.parent.mkdir(parents=True, exist_ok=True)
    with rep_file.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    return report


def print_report(report: dict) -> None:
    print("\nTOKENIZER REPORT")
    print("=" * 60)
    print(f"Name           : {report['name']} v{report['version']}")
    print(f"Algorithm      : byte-level BPE")
    print(f"Vocab size     : {report['vocab_size']:,} "
          f"(target {report['target_vocab_size']:,})")
    print(f"Min frequency  : {report['min_frequency']}")
    print("-" * 60)
    for token, tid in report["special_tokens"].items():
        print(f"  {token:8s} -> id {tid}")
    print(f"-" * 60)
    print(f"Files read     : {report['files_read']}")
    print(f"Elapsed        : {report['elapsed_seconds']}s")
    print("=" * 60)
    print("Saved to:", report.get("saved", ""))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Train ANKIT 0.1's own tokenizer.")
    parser.add_argument(
        "--config", default="configs/tokenizer.yaml",
        help="Path to a tokenizer config YAML.",
    )
    parser.add_argument(
        "--only-report", action="store_true",
        help="Just print the saved report, don't retrain.",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.only_report:
        rep = Path(cfg.report_file)
        if rep.exists():
            with rep.open("r", encoding="utf-8") as handle:
                print_report(json.load(handle))
        else:
            print(f"No report at {rep}. Run training first.")
        return

    report = run_training(cfg)
    report["saved"] = f"{cfg.tokenizer_file} + {cfg.vocab_file} + {cfg.report_file}"
    print_report(report)


if __name__ == "__main__":
    main()
