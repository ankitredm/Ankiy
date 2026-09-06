#!/usr/bin/env python3
"""Download a small, clean, LEGAL corpus for ANKIT 0.1.

Source: Project Gutenberg (https://www.gutenberg.org) — thousands of public
domain books that are freely usable. This script downloads a small set of
*short, public-domain* texts and saves them as plain ``.txt`` files under
``data/raw/gutenberg/``.

IMPORTANT — run this ONLY on a machine with internet access (your cloud GPU or
your own laptop). This sandbox has no internet, so here it is documented but
not exercised. It does NOT download any model — just public-domain text.

After running this, prepare the dataset:

    python scripts/prepare_dataset.py

Usage:
    python scripts/download_gutenberg.py                 # a small default set
    python scripts/download_gutenberg.py --books 74 84   # custom book ids
    python scripts/download_gutenberg.py --output data/raw/gutenberg
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.request import urlopen

# A small selection of short, unquestionably public-domain plain-text works
# (retellings / classics). IDs are Project Gutenberg ebook IDs.
DEFAULT_BOOKS = [
    74,   # The Adventures of Tom Sawyer (Twain)
    76,   # Huckleberry Finn (Twain)
    84,   # Frankenstein (Shelley, 1818)
    1342, # Pride and Prejudice (Austen)
    1661, # Sherlock Holmes: Adventures (Doyle)
    345,  # Dracula (Stoker)
]

BASE_TEMPLATES = [
    "https://www.gutenberg.org/files/{id}/{id}-0.txt",
    "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt",
]

# Gutenberg wraps each book with START/END banner lines; we cut them out.
_START_RE = re.compile(r"\*\*\*\s*START OF TH[EI]S PROJECT GUTENBERG.*?\*\*\*", re.I | re.S)
_END_RE = re.compile(r"\*\*\*\s*END OF TH[EI]S PROJECT GUTENBERG.*?\*\*\*", re.I | re.S)


def fetch_text(book_id: int, verbose: bool = False) -> str:
    """Try several URL patterns until one yields plain text."""
    for template in BASE_TEMPLATES:
        url = template.format(id=book_id)
        if verbose:
            print(f"  trying {url}")
        try:
            with urlopen(url, timeout=30) as resp:
                raw = resp.read()
            text = raw.decode("utf-8", errors="replace")
            # A Gutenberg plain text file contains a START/END banner; if the
            # fetched page is not real text it will be short/HTML-ish.
            if len(text) > 500 and "GUTENBERG" in text.upper():
                return text
        except Exception:  # noqa: BLE001 - try next URL on any failure
            continue
    raise RuntimeError(f"Could not download Gutenberg book id {book_id}.")


def strip_gutenberg_banners(text: str) -> str:
    """Remove Gutenberg's header/footer banner blocks from the body."""
    # Take everything between (and including) START and END banners.
    stripped = text
    m = _START_RE.search(stripped)
    if m:
        stripped = stripped[m.end():]
    m = _END_RE.search(stripped)
    if m:
        stripped = stripped[:m.start()]
    return stripped.strip()


def download(book_ids: list[int], output_dir: str | Path, verbose: bool = True) -> list[Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for book_id in book_ids:
        try:
            body = fetch_text(book_id, verbose=verbose)
            body = strip_gutenberg_banners(body)
            dest = out / f"gutenberg_{book_id}.txt"
            dest.write_text(body, encoding="utf-8")
            written.append(dest)
            if verbose:
                chars = len(body)
                print(f"  saved {dest.name} ({chars:,} chars)")
        except Exception as exc:  # noqa: BLE001
            print(f"  [warn] book {book_id} skipped: {exc}")
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Download legal public-domain text for ANKIT 0.1.")
    parser.add_argument(
        "--books",
        type=int,
        nargs="+",
        default=None,
        help="Gutenberg book IDs (default: a small starter set).",
    )
    parser.add_argument(
        "--output",
        default="data/raw/gutenberg",
        help="Directory to save .txt files (default: data/raw/gutenberg).",
    )
    parser.add_argument("--quiet", action="store_true", help="Less output.")
    args = parser.parse_args()

    books = args.books or DEFAULT_BOOKS
    print(f"Downloading {len(books)} public-domain books to {args.output}")
    files = download(books, args.output, verbose=not args.quiet)
    print(f"\nDone. {len(files)} file(s).")
    if not files:
        print("None downloaded — check internet access and book IDs.")
        sys.exit(1)
    print("Next step: python scripts/prepare_dataset.py")


if __name__ == "__main__":
    main()
