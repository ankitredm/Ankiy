# Sample corpus (for offline pipeline testing only)

This folder contains a **tiny, fully public-domain** set of texts used to
validate the ANKIT 0.1 data pipeline *without internet access*. It is NOT the
real training corpus.

| File | Content | Licence |
| --- | --- | --- |
| `emily_dickinson_poems.txt` | Public-domain poems by Emily Dickinson (d. 1886) | Public domain |
| `aesop_fables.txt` | Aesop's Fables (ancient, public domain) | Public domain |
| `us_history_docs.txt` | US Declaration of Independence, Constitution, Bill of Rights | Public domain |
| `ancient_greek_stories.txt` | Ancient Greek myths (public domain retellings) | Public domain |

**Why it's here** — the sandbox / CI environment has no internet, so a real
corpus download (Project Gutenberg) can't be verified here. By committing a few
public-domain files, `scripts/prepare_dataset.py` and the pytest suite run and
are reproducible locally; the pipeline's *code* is what's tested, not the amount
of data.

**For the real training corpus**, run `scripts/download_gutenberg.py` on a
machine with internet (your cloud GPU) to fetch a larger public-domain set into
`data/raw/gutenberg/`, then run `scripts/prepare_dataset.py` again.
