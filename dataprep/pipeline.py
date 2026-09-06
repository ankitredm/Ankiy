"""The full dataset preparation pipeline.

Order of operations
-------------------
1. Load ``configs/data.yaml``.
2. Read raw text files from ``data/raw/``.
3. Split each file into clean documents (paragraphs for .txt, lines for .jsonl).
4. Clean + normalise every document.
5. Filter out low-quality documents.
6. Deduplicate (exact, optionally near with MinHash/LSH).
7. Split into train / validation / test.
8. Write splits + a statistics report (+ a human-readable summary).

This is fully deterministic given the same config, raw data and seed, so a
training run is reproducible. It runs on CPU — no GPU needed to prepare data.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

from dataprep import dedup, quality, readers, split, stats


@dataclass
class DataConfig:
    name: str
    version: str
    seed: int
    source: dict
    cleaning: quality.CleaningConfig
    filtering: quality.FilterConfig
    dedup: dedup.DedupConfig
    split: split.SplitConfig
    output: dict

    @classmethod
    def from_dict(cls, data: dict) -> "DataConfig":
        return cls(
            name=json.dumps(data.get("name", "ankit-data")),
            version=str(data.get("version", "0.1")),
            seed=int(data.get("seed", 1337)),
            source=dict(data.get("source", {})),
            cleaning=quality.CleaningConfig.from_dict(data.get("cleaning", {})),
            filtering=quality.FilterConfig.from_dict(data.get("filtering", {})),
            dedup=dedup.DedupConfig.from_dict(data.get("dedup", {})),
            split=split.SplitConfig.from_dict(data.get("split", {})),
            output=dict(data.get("output", {})),
        )


def load_data_config(path: str | Path) -> DataConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data config not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return DataConfig.from_dict(raw)


def _split_text_into_documents(text: str) -> list[str]:
    """Split a .txt file into paragraph-sized documents using blank lines."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    # If there are no blank lines at all, fall back to whole lines.
    if not paragraphs:
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return paragraphs or [text.strip()]


def run_pipeline(config_path: str | Path = "configs/data.yaml") -> dict:
    """Run the whole preparation pipeline. Returns the statistics dict."""
    cfg = load_data_config(config_path)
    t0 = time.time()

    print(f"ANKIT dataset pipeline — {cfg.name} v{cfg.version}")
    print(f"Seed: {cfg.seed}")

    # 1. Read raw docs ----------------------------------------------------
    raw_dir = cfg.source.get("raw_dir", "data/raw")
    print(f"\n[1/7] Reading raw text from {raw_dir} ...")
    raw_docs: list[str] = []
    source_files = 0
    for src, text in readers.iter_raw_documents(raw_dir):
        source_files += 1
        raw_docs.extend(_split_text_into_documents(text))
    print(f"      {source_files} file(s) -> {len(raw_docs)} raw documents")

    # 2. Clean + normalise ------------------------------------------------
    print("[2/7] Cleaning + normalising ...")
    cleaned = [quality.clean_document(d, cfg.cleaning) for d in raw_docs]
    # Drop empties produced by cleaning.
    cleaned = [c for c in cleaned if c]
    n_cleaned = len(cleaned)
    print(f"      {n_cleaned} documents survive cleaning")

    # 3. Filter -----------------------------------------------------------
    print("[3/7] Filtering low-quality documents ...")
    filtered_out = 0
    kept: list[str] = []
    for doc in cleaned:
        reason = quality.should_filter(doc, cfg.filtering)
        if reason:
            filtered_out += 1
            continue
        kept.append(doc)
    print(f"      kept {len(kept)} / filtered {filtered_out}")
    n_after_filter = len(kept)

    # 4. Deduplicate ------------------------------------------------------
    print("[4/7] Deduplicating ...")
    deduped, exact_removed, near_removed = dedup.deduplicate(
        kept, cfg.dedup, seed=cfg.seed
    )
    print(
        f"      exact removed {exact_removed}, "
        f"near removed {near_removed}, remaining {len(deduped)}"
    )

    # 5. Split ------------------------------------------------------------
    print("[5/7] Splitting into train/val/test ...")
    splits = split.split_documents(deduped, cfg.split, seed=cfg.seed)
    for name, docs in splits.items():
        print(f"      {name}: {len(docs)} docs")

    # 6. Write split files ------------------------------------------------
    print("[6/7] Writing output files ...")
    out = cfg.output
    splits_dir = Path(out.get("splits_dir", "data/processed/splits"))
    splits_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    for name, docs in splits.items():
        out_file = splits_dir / f"{name}.jsonl"
        with out_file.open("w", encoding="utf-8") as handle:
            for doc in docs:
                handle.write(json.dumps({"text": doc}, ensure_ascii=False) + "\n")
        written[name] = str(out_file)
        print(f"      wrote {out_file} ({len(docs)} docs)")

    # 7. Statistics ---------------------------------------------------------
    print("[7/7] Computing statistics ...")
    stats_dict = stats.compute_stats(
        splits,
        source_files=source_files,
        cleaned_before_filter=n_cleaned,
        filtered_out=filtered_out,
        exact_removed=exact_removed,
        near_removed=near_removed,
    )
    files_read = len(raw_docs)  # raw doc count
    stats_dict["source_file_count"] = source_files
    stats_dict["raw_documents"] = files_read

    stats_path = Path(out.get("stats_file", "data/stats/stats.json"))
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats.save_stats(stats_dict, stats_path)

    elapsed = time.time() - t0
    stats_dict["elapsed_seconds"] = round(elapsed, 2)
    stats_dict["stats_file"] = str(stats_path)

    print("\n" + stats.format_stats(stats_dict))
    print(f"\nDone in {elapsed:.2f}s. Splits in {splits_dir}.")
    return stats_dict
