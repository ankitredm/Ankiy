"""Tests for the Class 4 exam grader (strict scoring, no model needed)."""

from __future__ import annotations

import pytest

from evaluation.class4_exam import (
    anti_memorization_check,
    extract_numbers,
    grade_answer,
    normalize,
)


def test_extract_numbers():
    assert extract_numbers("The answer is 61.") == [61.0]
    assert extract_numbers("Rs. 1,500 and 2.5 kg") == [1500.0, 2.5]
    assert extract_numbers("3/8") == [3.0, 8.0]
    assert extract_numbers("no numbers here") == []


def test_numeric_mode():
    g = {"mode": "numeric", "answer": 61}
    assert grade_answer(g, "34 + 27 = 61") == 1.0
    assert grade_answer(g, "The sum is 61 rupees.") == 1.0
    assert grade_answer(g, "I think it is 16.") == 0.0
    assert grade_answer(g, "") == 0.0


def test_numeric_mode_requires_the_number_not_keywords():
    g = {"mode": "numeric", "answer": 22}
    assert grade_answer(g, "perimeter means distance around") == 0.0
    assert grade_answer(g, "22 cm") == 1.0


def test_numeric_with_terms_fallback():
    g = {"mode": "numeric", "answer": 2.5, "terms": ["2 rupees 50", "two and a half"]}
    assert grade_answer(g, "250 paise make 2.5 rupees") == 1.0
    assert grade_answer(g, "It is 2 rupees 50 paise") == 1.0  # terms fallback
    assert grade_answer(g, "It is 2 rupees") == 0.0


def test_numeric_max_mode():
    g = {"mode": "numeric_max", "answer": 0.8}
    assert grade_answer(g, "0.8 is more than 0.6") == 1.0
    assert grade_answer(g, "0.6 is more") == 0.0


def test_numeric_sequence_mode():
    g = {"mode": "numeric_sequence", "answer": [2, 5, 8]}
    assert grade_answer(g, "2, 5, 8") == 1.0
    assert grade_answer(g, "2, 8, 5") == 0.0  # wrong order
    assert grade_answer(g, "2 and 5") == 0.0


def test_match_any_uses_word_boundaries():
    g = {"mode": "match_any", "terms": ["om"]}
    assert grade_answer(g, "Om is first") == 1.0
    assert grade_answer(g, "Tom is first") == 0.0  # no partial-word credit
    g2 = {"mode": "match_any", "terms": ["rain"]}
    # Word-boundary: "rain" does NOT match inside the word "raining".
    assert grade_answer(g2, "It is raining") == 0.0
    assert grade_answer(g2, "Watch the rain fall") == 1.0


def test_match_any_rain_word_boundary():
    g = {"mode": "match_any", "terms": ["rain", "raining", "rainy"]}
    assert grade_answer(g, "It is raining") == 1.0
    assert grade_answer(g, "It is sunny") == 0.0


def test_match_all_mode():
    g = {"mode": "match_all", "terms": ["doesn", "like mangoes"]}
    assert grade_answer(g, "He doesn't like mangoes.") == 1.0
    assert grade_answer(g, "He doesn't like apples.") == 0.0


def test_min_matches_mode():
    g = {"mode": "min_matches", "terms": ["cow", "dog", "hen", "cat"], "min": 2}
    assert grade_answer(g, "cow and dog") == 1.0
    assert grade_answer(g, "only a cow") == 0.0


def test_one_word_mode_is_strict():
    g = {"mode": "one_word_any", "terms": ["blue"]}
    assert grade_answer(g, "blue") == 1.0
    assert grade_answer(g, "The sky is blue") == 0.0  # more than one word
    assert grade_answer(g, "blueish") == 0.0


def test_rubric_partial_credit():
    g = {"mode": "rubric", "components": [{"any": ["sunlight", "sun"]},
                                          {"any": ["water", "air"]},
                                          {"min_words": 8}]}
    # All components: full credit.
    assert grade_answer(g, "A plant needs sunlight and water to make its own food") == 1.0
    # Two of three components: half credit, not full (keyword echo is not enough).
    assert grade_answer(g, "sunlight and water") == 0.5
    # A single echoed keyword earns only 1/3 -> zero.
    assert grade_answer(g, "sunlight") == 0.0
    # Nothing relevant: zero.
    assert grade_answer(g, "I like plants") == 0.0


def test_rubric_min_sentences():
    g = {"mode": "rubric", "components": [{"min_sentences": 2}, {"any": ["diwali"]},
                                          {"min_words": 6}]}
    assert grade_answer(g, "I like Diwali. We light lamps at home together.") == 1.0
    assert grade_answer(g, "I like Diwali a lot and we light lamps") == 0.5


def test_grader_never_awards_points_for_empty_answers():
    for mode in ({"mode": "numeric", "answer": 5},
                 {"mode": "match_any", "terms": ["blue"]},
                 {"mode": "rubric", "components": [{"any": ["x"]}, {"min_words": 3}]}):
        assert grade_answer(mode, "") == 0.0
        assert grade_answer(mode, "...") == 0.0


def test_anti_memorization_flags_overlap():
    grams = {("the", "quick", "brown", "fox", "jumps", "over", "the", "lazy")}
    tasks = [
        {"id": "ok", "prompt": "Question: a completely different sentence here\nAnswer:"},
        {"id": "bad", "prompt": "Question: the quick brown fox jumps over the lazy dog\nAnswer:"},
    ]
    report = anti_memorization_check(tasks, grams)
    assert report["flagged_ids"] == ["bad"]
    assert report["overlap"] == 1


def test_normalize_matches_eval_harness():
    assert normalize("He doesn't like mangoes.") == "he doesn t like mangoes"
