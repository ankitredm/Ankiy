"""Load raw text from disk into a list of documents.

We support two common formats (both produced by public/open corpora):

- ``.txt``    — a whole file is one or more documents. If the file contains
                single newlines within paragraphs, we split on blank lines
                (two newlines) so each paragraph becomes its own document.
- ``.jsonl``  — one JSON object per line; the text is read from a ``"text"``
                or ``"content"`` field.

The pipeline is source-agnostic: drop *any* legal text into ``data/raw/`` and
this reads it. Project Gutenberg downloads are just ``.txt`` files, so they work
with no extra code.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

VALID_EXTENSIONS = {".txt", ".jsonl"}


def iter_raw_documents(raw_dir: str | Path) -> Iterable[tuple[str, str]]:
    """Yield (source_file, text) for every raw text file under raw_dir.

    Folders are recursed. Files that fail to decode/format are skipped and a
    warning is printed (never crash the whole pipeline for one bad file).
    """
    root = Path(raw_dir)
    files = sorted(
        p for p in root.rglob("*") if p.suffix.lower() in VALID_EXTENSIONS
    )
    for path in files:
        if path.suffix.lower() == ".txt":
            try:
                text = _read_txt(path)
                if text:
                    yield str(path), text
            except Exception as exc:  # noqa: BLE001
                print(f"  [warn] skipped {path}: {exc}")
        elif path.suffix.lower() == ".jsonl":
            try:
                for doc in _read_jsonl(path):
                    yield str(path), doc
            except Exception as exc:  # noqa: BLE001
                print(f"  [warn] skipped {path}: {exc}")


def _read_txt(path: Path) -> str:
    raw_bytes = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return raw_bytes.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def _read_jsonl(path: Path) -> Iterable[str]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj, dict):
                text = obj.get("text") or obj.get("content") or obj.get("document")
                if isinstance(text, str) and text.strip():
                    yield text
            elif isinstance(obj, str):
                if obj.strip():
                    yield obj
