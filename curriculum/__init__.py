"""ANKIT 0.1 — Class 1–4 curriculum data builders.

This package generates the from-scratch educational training corpus:

    English    -> vocabulary, spelling, grammar, tenses, sentences,
                  paragraphs, stories, instructions, comprehension
    Hinglish   -> natural Roman-script Hindi-English conversation & explanation
    Maths      -> counting -> geometry/word problems, with worked examples
    Science    -> EVS: living/non-living, plants, animals, body, water, ...
    Social     -> family, community, India, maps, festivals, transport, ...
    Reasoning  -> why/how, classification, sequencing, inference, patterns

Design rules (see the project README):
  - everything is OUR OWN original text — no scraped or copyrighted content;
  - items are progressive (stage 1 = Class 1 ... stage 4 = Class 4);
  - each item carries: text, category, stage (1-4), kind, difficulty;
  - build.py assembles stages, dedupes, and splits train/val/test
    deterministically (the evaluation suite uses its OWN hand-written tasks,
    never corpus items, so evaluation stays honestly held-out).

Usage:
    python scripts/build_curriculum.py            # writes data/curriculum/
"""

from curriculum.build import build_all, collect_stats

__all__ = ["build_all", "collect_stats"]
