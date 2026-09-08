#!/usr/bin/env python3
"""Author the ANKIT 0.1 Class 4 EXAM (held-out) as evaluation/tasks/class4_exam.jsonl.

Every question here is independently authored for this exam:
  - fresh passages (not the training stories),
  - fresh numbers (different from the curriculum corpus),
  - fresh wording/situations for equivalent concepts.

No question may overlap the training corpus — the exam runner enforces this
with an n-gram anti-memorization check before grading.

Grading modes (strict, no keyword-only credit):
  numeric          the expected number must appear among the numbers in the answer
  numeric_max      for "which is more" questions: max(extracted) == expected
  numeric_sequence extracted numbers must equal the expected sequence, in order
  match_any        word-boundary match of any accepted term (normalized)
  match_all        ALL accepted terms must appear
  min_matches      at least `min` DISTINCT accepted terms must appear
  one_word_any     the answer must be exactly one accepted word
  rubric           multi-component strict rubric with partial credit:
                     {"any": [...]}, {"all": [...]}, {"min_words": n},
                     {"min_sentences": n} — credit = matched/total
                     (>=0.99 full, >=0.5 half, else 0)

Run:  python evaluation/tasks/build_class4_exam.py
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "class4_exam.jsonl"

PASSAGE_A = (
    "Aarav went to the terrace of his house to fly his new blue kite. His cousin Rahul held "
    "the string while Aarav ran against the wind. The kite climbed higher and higher, above "
    "the neem tree. Suddenly a strong gust snapped the string, and the kite sailed over the "
    "wall and got stuck on a branch. Rahul carefully climbed the tree, holding the branches "
    "firmly, and brought the kite down. Next time we will fly kites on the open ground, far "
    "away from trees, Aarav laughed."
)

PASSAGE_B = (
    "Naina saw a small brown puppy crying near the school gate. It had no collar. She gave it "
    "water from her bottle and made a paper sign: found a brown puppy, call this number. She "
    "stuck the sign near the gate. In the evening, an old man from the next street, Mr. Das, "
    "called. He had been searching everywhere for his puppy, Moti. When Naina returned Moti, "
    "Mr. Das thanked her again and again. Naina walked home feeling warm and happy, because "
    "Moti had reached home safely."
)

PASSAGE_H1 = (
    "Raju roz subah 6 baje uthta hai. Woh sabse pehle ek glass paani peeta hai. Uske baad woh "
    "15 minute yoga karta hai. Phir woh nahata hai aur nashta karta hai. 8 baje Raju school "
    "ke liye nikal jaata hai."
)

PASSAGE_H2 = (
    "Meena ki dadi use roz shaam ko kahaniyan sunati hain. Kahani ke baad dadi garam halwa "
    "banati hain. Meena bhi dadi ki madad karti hai — woh unke liye paani ka glass le aati "
    "hai. Dono saath mein baith ke halwa khate hain."
)


def q(id_: str, section: str, skill: str, category: str, prompt: str, grade: dict,
      max_new_tokens: int = 24, type_: str = "objective") -> dict:
    return {
        "id": id_, "section": section, "skill": skill, "category": category,
        "type": type_, "prompt": prompt, "grade": grade, "max_new_tokens": max_new_tokens,
    }


def rq(prompt: str, passage: str) -> str:
    return f"Read the passage: {passage}\nQuestion: {prompt}\nAnswer:"


ITEMS: list[dict] = []

# ═══════════════════════ ENGLISH ═══════════════════════
ITEMS += [
    q("ENG-V-01", "english", "", "english_vocab",
      "Question: What is the opposite of the word 'heavy'?\nAnswer:",
      {"mode": "match_any", "terms": ["light"]}),
    q("ENG-V-02", "english", "", "english_vocab",
      "Question: What is the opposite of the word 'first'?\nAnswer:",
      {"mode": "match_any", "terms": ["last"]}),
    q("ENG-V-03", "english", "", "english_vocab",
      "Question: What does the word 'brief' mean?\nAnswer:",
      {"mode": "match_any", "terms": ["short", "small time", "quick"]}),
    q("ENG-V-04", "english", "", "english_vocab",
      "Question: What does the word 'damp' mean?\nAnswer:",
      {"mode": "match_any", "terms": ["wet", "moist", "little water"]}),
    q("ENG-V-05", "english", "", "english_vocab",
      "Question: Write another word with nearly the same meaning as 'shut'.\nAnswer:",
      {"mode": "match_any", "terms": ["close"]}),
    q("ENG-S-01", "english", "", "english_spelling",
      "Question: Write the correct spelling of the word 'libary'.\nAnswer:",
      {"mode": "match_any", "terms": ["library"]}),
    q("ENG-S-02", "english", "", "english_spelling",
      "Question: Which is the correct spelling: 'febuary' or 'february'? Write it.\nAnswer:",
      {"mode": "match_any", "terms": ["february"]}),
    q("ENG-S-03", "english", "", "english_spelling",
      "Question: Write the correct spelling of the word 'tomorow'.\nAnswer:",
      {"mode": "match_any", "terms": ["tomorrow"]}),
    q("ENG-S-04", "english", "", "english_spelling",
      "Question: Write the correct spelling of the word 'goverment'.\nAnswer:",
      {"mode": "match_any", "terms": ["government"]}),
    q("ENG-G-01", "english", "", "english_grammar",
      "Question: What is the plural of 'knife'?\nAnswer:",
      {"mode": "match_any", "terms": ["knives"]}),
    q("ENG-G-02", "english", "", "english_grammar",
      "Question: What is the plural of 'mouse'?\nAnswer:",
      {"mode": "match_any", "terms": ["mice"]}),
    q("ENG-G-03", "english", "", "english_grammar",
      "Question: Correct the sentence: 'He don't like mangoes.'\nAnswer:",
      {"mode": "match_all", "terms": ["doesn", "like mangoes"]}),
    q("ENG-G-04", "english", "", "english_grammar",
      "Question: In the sentence 'The baby sleeps quietly', which word is the verb?\nAnswer:",
      {"mode": "match_any", "terms": ["sleeps"]}),
    q("ENG-G-05", "english", "", "english_grammar",
      "Question: Fill in the blank with 'a' or 'an': We saw ___ ox at the fair.\nAnswer:",
      {"mode": "one_word_any", "terms": ["an"]}),
    q("ENG-G-06", "english", "", "english_grammar",
      "Question: What is the past tense of 'drink'?\nAnswer:",
      {"mode": "match_any", "terms": ["drank"]}),
    q("ENG-F-01", "english", "", "sentence_formation",
      "Question: Make a sentence using the word 'garden'.\nAnswer:",
      {"mode": "rubric", "components": [{"any": ["garden"]}, {"min_words": 4}]},
      type_="open"),
    q("ENG-F-02", "english", "", "sentence_formation",
      "Question: Make a sentence using the word 'because'.\nAnswer:",
      {"mode": "rubric", "components": [{"any": ["because"]}, {"min_words": 5}]},
      type_="open"),
    q("ENG-F-03", "english", "", "sentence_formation",
      "Question: Write one sentence about a rainy day.\nAnswer:",
      {"mode": "rubric",
       "components": [{"min_words": 4},
                      {"any": ["rain", "raining", "umbrella", "wet", "cloud", "puddle", "rainy"]}]},
      type_="open"),
    # -- reading comprehension (fresh passages) --
    q("ENG-C-01", "english", "comprehension", "reading_comprehension",
      rq("Where did Aarav fly the kite?", PASSAGE_A),
      {"mode": "match_any", "terms": ["terrace", "roof"]}),
    q("ENG-C-02", "english", "comprehension", "reading_comprehension",
      rq("What happened when the string snapped?", PASSAGE_A),
      {"mode": "match_any", "terms": ["tree", "stuck", "flew", "sailed", "branch"]}),
    q("ENG-C-03", "english", "comprehension", "reading_comprehension",
      rq("Who brought the kite back, and how?", PASSAGE_A),
      {"mode": "rubric",
       "components": [{"any": ["rahul", "cousin"]}, {"any": ["climb", "climbed", "climbing", "tree"]}]},
      type_="open"),
    q("ENG-C-04", "english", "comprehension", "reading_comprehension",
      rq("What did they decide to do next time?", PASSAGE_A),
      {"mode": "rubric",
       "components": [{"any": ["open ground", "away from tree", "far away", "ground", "park", "field"]},
                      {"min_words": 3}]},
      type_="open"),
    q("ENG-C-05", "english", "comprehension", "reading_comprehension",
      rq("Where did Naina find the puppy?", PASSAGE_B),
      {"mode": "match_any", "terms": ["gate", "school"]}),
    q("ENG-C-06", "english", "comprehension", "reading_comprehension",
      rq("How did Naina try to find the owner?", PASSAGE_B),
      {"mode": "match_any", "terms": ["sign", "notice", "poster", "paper", "number"]}),
    q("ENG-C-07", "english", "comprehension", "reading_comprehension",
      rq("Who owned the puppy?", PASSAGE_B),
      {"mode": "match_any", "terms": ["das", "old man"]}),
    q("ENG-C-08", "english", "comprehension", "reading_comprehension",
      rq("How did Naina feel at the end, and why?", PASSAGE_B),
      {"mode": "rubric",
       "components": [{"any": ["happy", "glad", "warm"]}, {"any": ["home", "safe", "safely", "back"]}]},
      type_="open"),
]

# ═══════════════════════ MATHEMATICS ═══════════════════════
ITEMS += [
    q("MTH-AS-01", "math", "", "addition_subtraction",
      "Question: Add: 34 + 27 = ?\nAnswer:", {"mode": "numeric", "answer": 61}),
    q("MTH-AS-02", "math", "", "addition_subtraction",
      "Question: Subtract: 80 - 37 = ?\nAnswer:", {"mode": "numeric", "answer": 43}),
    q("MTH-AS-03", "math", "", "addition_subtraction",
      "Question: Add: 125 + 236 = ?\nAnswer:", {"mode": "numeric", "answer": 361}),
    q("MTH-AS-04", "math", "", "addition_subtraction",
      "Question: Subtract: 503 - 158 = ?\nAnswer:", {"mode": "numeric", "answer": 345}),
    q("MTH-MD-01", "math", "", "multiplication_division",
      "Question: Multiply: 8 x 7 = ?\nAnswer:", {"mode": "numeric", "answer": 56}),
    q("MTH-MD-02", "math", "", "multiplication_division",
      "Question: Multiply: 9 x 6 = ?\nAnswer:", {"mode": "numeric", "answer": 54}),
    q("MTH-MD-03", "math", "", "multiplication_division",
      "Question: Divide: 63 / 9 = ?\nAnswer:", {"mode": "numeric", "answer": 7}),
    q("MTH-MD-04", "math", "", "multiplication_division",
      "Question: Divide: 144 / 12 = ?\nAnswer:", {"mode": "numeric", "answer": 12}),
    q("MTH-FR-01", "math", "", "fractions",
      "Question: A chapati is cut into 8 equal pieces and Ria eats 3 pieces. "
      "What fraction did she eat?\nAnswer:",
      {"mode": "match_any", "terms": ["3 8", "three eighth", "three over eight"]}),
    q("MTH-FR-02", "math", "", "fractions",
      "Question: Which fraction is bigger: 2/3 or 1/3?\nAnswer:",
      {"mode": "match_any", "terms": ["2 3", "two third"]}),
    q("MTH-FR-03", "math", "", "fractions",
      "Question: How many quarters (1/4) make one whole?\nAnswer:",
      {"mode": "numeric", "answer": 4}),
    q("MTH-DE-01", "math", "", "decimals",
      "Question: Write 7/10 as a decimal.\nAnswer:", {"mode": "numeric", "answer": 0.7}),
    q("MTH-DE-02", "math", "", "decimals",
      "Question: Which decimal is more: 0.8 or 0.6?\nAnswer:",
      {"mode": "numeric_max", "answer": 0.8}),
    q("MTH-FM-01", "math", "", "factors_multiples",
      "Question: Write all the factors of 16.\nAnswer:",
      {"mode": "min_matches", "terms": ["1", "2", "4", "8", "16"], "min": 4}),
    q("MTH-FM-02", "math", "", "factors_multiples",
      "Question: Write the first four multiples of 6.\nAnswer:",
      {"mode": "match_all", "terms": ["6", "12", "18", "24"]}),
    q("MTH-FM-03", "math", "", "factors_multiples",
      "Question: What is the smallest factor of 21 that is greater than 1?\nAnswer:",
      {"mode": "numeric", "answer": 3}),
    q("MTH-TM-01", "math", "", "time",
      "Question: The hour hand of a clock is on 7 and the minute hand is on 12. "
      "What time is it?\nAnswer:",
      {"mode": "match_any", "terms": ["7 o clock", "seven o clock", "7 00"]}),
    q("MTH-TM-02", "math", "", "time",
      "Question: School starts at 8:30 in the morning and ends at 3:30 in the afternoon. "
      "How many hours is that?\nAnswer:", {"mode": "numeric", "answer": 7}),
    q("MTH-TM-03", "math", "", "time",
      "Question: If today is Tuesday, what day will it be after 5 days?\nAnswer:",
      {"mode": "match_any", "terms": ["sunday"]}),
    q("MTH-MY-01", "math", "", "money",
      "Question: One pencil costs 12 rupees. Sana buys 3 pencils. How much does she pay?\nAnswer:",
      {"mode": "numeric", "answer": 36}),
    q("MTH-MY-02", "math", "", "money",
      "Question: Irfan had 100 rupees and spent 65 rupees on a book. "
      "How much money is left with him?\nAnswer:", {"mode": "numeric", "answer": 35}),
    q("MTH-MY-03", "math", "", "money",
      "Question: How many rupees are equal to 250 paise?\nAnswer:",
      {"mode": "numeric", "answer": 2.5,
       "terms": ["2 5", "2 rupees 50", "two and a half", "two point five"]}),
    q("MTH-MS-01", "math", "", "measurement",
      "Question: How many centimetres are there in 3 metres?\nAnswer:",
      {"mode": "numeric", "answer": 300}),
    q("MTH-MS-02", "math", "", "measurement",
      "Question: A pumpkin weighs 1500 grams. How many kilograms is that?\nAnswer:",
      {"mode": "numeric", "answer": 1.5, "terms": ["1 500", "1 5", "one and a half"]}),
    q("MTH-GM-01", "math", "", "geometry",
      "Question: How many faces does a cube have?\nAnswer:", {"mode": "numeric", "answer": 6}),
    q("MTH-GM-02", "math", "", "geometry",
      "Question: A rectangle is 8 cm long and 3 cm wide. What is its perimeter?\nAnswer:",
      {"mode": "numeric", "answer": 22}),
    q("MTH-GM-03", "math", "", "geometry",
      "Question: What do we call a shape that has exactly 3 sides?\nAnswer:",
      {"mode": "match_any", "terms": ["triangle"]}),
    q("MTH-WP-01", "math", "", "word_problems",
      "Question: 45 beads are strung equally onto 9 strings. How many beads are on each string?\nAnswer:",
      {"mode": "numeric", "answer": 5}),
    q("MTH-WP-02", "math", "", "word_problems",
      "Question: A pen costs 18 rupees. Ria buys 4 pens and gives the shopkeeper a "
      "100-rupee note. How much change does she get?\nAnswer:",
      {"mode": "numeric", "answer": 28}),
    q("MTH-WP-03", "math", "", "word_problems",
      "Question: A bus can carry 35 students. 120 students are going on a trip. "
      "How many buses are needed so that every student gets a seat?\nAnswer:",
      {"mode": "numeric", "answer": 4}),
    q("MTH-MX-01", "math", "", "multi_step",
      "Question: Ravi had 90 marbles. He gave 24 to his friend and then lost 15. "
      "How many marbles does he have now?\nAnswer:", {"mode": "numeric", "answer": 51}),
    q("MTH-MX-02", "math", "", "multi_step",
      "Question: A farm collects 45 eggs every day. How many eggs does it collect "
      "in one whole week (7 days)?\nAnswer:", {"mode": "numeric", "answer": 315}),
    q("MTH-MX-03", "math", "", "multi_step",
      "Question: A box has 6 rows of candles with 8 candles in each row, plus 9 loose "
      "candles beside it. How many candles in total?\nAnswer:",
      {"mode": "numeric", "answer": 57}),
]

# ═══════════════════════ SCIENCE / EVS ═══════════════════════
ITEMS += [
    q("SCI-01", "science", "", "science_plants",
      "Question: What things does a plant need to make its own food? Name at least two.\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["sunlight", "sun", "solar", "light"]}, {"any": ["water", "air"]}]},
      type_="open"),
    q("SCI-02", "science", "", "science_plants",
      "Question: Which part of a plant takes water from the soil?\nAnswer:",
      {"mode": "match_any", "terms": ["root"]}),
    q("SCI-03", "science", "", "science_animals",
      "Question: What do we call an animal that eats only the flesh of other animals?\nAnswer:",
      {"mode": "match_any", "terms": ["carnivore"]}),
    q("SCI-04", "science", "", "science_human_body",
      "Question: Which organ in our body cleans the blood and removes waste as urine?\nAnswer:",
      {"mode": "match_any", "terms": ["kidney"]}),
    q("SCI-05", "science", "", "science_health",
      "Question: Why do we sweat on a hot day?\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["cool", "cools", "cooling", "cold", "temperature", "heat out"]},
                      {"min_words": 3}]},
      type_="open"),
    q("SCI-06", "science", "", "science_human_body",
      "Question: Which gas do we breathe IN to stay alive?\nAnswer:",
      {"mode": "match_any", "terms": ["oxygen"]}),
    q("SCI-07", "science", "", "science_water_air",
      "Question: When water boils, it turns into ___. Fill in the blank.\nAnswer:",
      {"mode": "match_any", "terms": ["steam", "vapour", "vapor"]}),
    q("SCI-08", "science", "", "science_weather",
      "Question: Which season brings most of the rain to India?\nAnswer:",
      {"mode": "match_any", "terms": ["monsoon", "rainy"]}),
    q("SCI-09", "science", "", "science_earth_space",
      "Question: What is the main source of light and energy for the Earth?\nAnswer:",
      {"mode": "match_any", "terms": ["sun"]}),
    q("SCI-10", "science", "", "science_environment",
      "Question: Name one good way to reduce plastic waste.\nAnswer:",
      {"mode": "match_any",
       "terms": ["reuse", "recycle", "cloth bag", "jute", "carry bag", "refuse", "less plastic"]}),
    q("SCI-11", "science", "", "science_animals",
      "Question: Why does a polar bear have thick fur?\nAnswer:",
      {"mode": "match_any", "terms": ["warm", "cold", "insulat", "protect"]}),
    q("SCI-12", "science", "", "science_animals",
      "Question: What is the baby of a frog called?\nAnswer:",
      {"mode": "match_any", "terms": ["tadpole"]}),
]

# ═══════════════════════ SOCIAL STUDIES ═══════════════════════
ITEMS += [
    q("SOC-01", "social", "", "social_community",
      "Question: Who brings letters to our home from the post office?\nAnswer:",
      {"mode": "match_any", "terms": ["postman", "post man", "postwoman"]}),
    q("SOC-02", "social", "", "social_directions",
      "Question: If east is in front of you, which direction is behind you?\nAnswer:",
      {"mode": "match_any", "terms": ["west"]}),
    q("SOC-03", "social", "", "social_maps",
      "Question: On a map, what does the blue colour usually show?\nAnswer:",
      {"mode": "match_any", "terms": ["water", "river", "sea", "ocean", "lake"]}),
    q("SOC-04", "social", "", "social_india",
      "Question: What is the capital of the state of Maharashtra?\nAnswer:",
      {"mode": "match_any", "terms": ["mumbai"]}),
    q("SOC-05", "social", "", "social_india",
      "Question: Which bird is the national bird of India?\nAnswer:",
      {"mode": "match_any", "terms": ["peacock"]}),
    q("SOC-06", "social", "", "social_geography",
      "Question: Which is the longest river of India?\nAnswer:",
      {"mode": "match_any", "terms": ["ganga", "ganges"]}),
    q("SOC-07", "social", "", "social_history",
      "Question: Who was the first Prime Minister of India?\nAnswer:",
      {"mode": "match_any", "terms": ["nehru"]}),
    q("SOC-08", "social", "", "social_rules",
      "Question: Why do we have rules in school?\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["safe", "safety", "fair", "discipline", "order", "protect"]},
                      {"min_words": 4}]},
      type_="open"),
    q("SOC-09", "social", "", "social_rules",
      "Question: A stranger offers you sweets and asks you to come with him. "
      "What should you do?\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["no", "refuse", "not take", "not accept", "never", "reject"]},
                      {"any": ["tell", "inform", "parents", "teacher", "adult", "family"]}]},
      type_="open"),
    q("SOC-10", "social", "", "social_maps",
      "Question: What is a map?\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["drawing", "picture", "diagram", "sketch", "chart"]},
                      {"any": ["place", "places", "area", "country", "earth", "world"]}]},
      type_="open"),
]

# ═══════════════════════ REASONING ═══════════════════════
ITEMS += [
    q("RSN-P-01", "reasoning", "", "reasoning_patterns",
      "Question: Complete the pattern: 3, 6, 9, 12, ___\nAnswer:",
      {"mode": "numeric", "answer": 15}),
    q("RSN-P-02", "reasoning", "", "reasoning_patterns",
      "Question: Complete the pattern: 40, 36, 32, 28, ___\nAnswer:",
      {"mode": "numeric", "answer": 24}),
    q("RSN-C-01", "reasoning", "", "reasoning_classification",
      "Question: Pick the odd one out and name it: rose, lotus, sunflower, mango\nAnswer:",
      {"mode": "match_any", "terms": ["mango"]}),
    q("RSN-C-02", "reasoning", "", "reasoning_classification",
      "Question: Pick the odd one out and name it: spoon, fork, plate, chair\nAnswer:",
      {"mode": "match_any", "terms": ["chair"]}),
    q("RSN-Q-01", "reasoning", "", "reasoning_sequencing",
      "Question: Put in order: seed, plant, tree with fruits, ___ (what comes after seed?)\nAnswer:",
      {"mode": "match_any", "terms": ["sprout", "sapling", "seedling", "small plant"]}),
    q("RSN-Q-02", "reasoning", "", "reasoning_sequencing",
      "Question: If tomorrow is Thursday, what day is today?\nAnswer:",
      {"mode": "match_any", "terms": ["wednesday"]}),
    q("RSN-CM-01", "reasoning", "", "reasoning_comparison",
      "Question: Asha is 10 years old, Bina is 12 and Chhotu is 9. "
      "Who is the youngest?\nAnswer:", {"mode": "match_any", "terms": ["chhotu"]}),
    q("RSN-E-01", "reasoning", "", "reasoning_cause_effect",
      "Question: Why does an ice cream melt if you keep it in the sun?\nAnswer:",
      {"mode": "match_any", "terms": ["heat", "hot", "warm", "sun", "temperature"]}),
    q("RSN-I-01", "reasoning", "", "reasoning_inference",
      "Question: Smita picks up an umbrella and wears a raincoat before leaving home. "
      "What can you guess about the weather?\nAnswer:",
      {"mode": "match_any", "terms": ["rain"]}),
    q("RSN-L-01", "reasoning", "", "reasoning_logic",
      "Question: All roses are flowers. Some flowers fade quickly. "
      "Can we say that ALL roses fade quickly? Answer yes or no.\nAnswer:",
      {"mode": "one_word_any", "terms": ["no"]}),
    q("RSN-L-02", "reasoning", "", "reasoning_logic",
      "Question: Meena stands behind Ravi in a queue. Ravi stands behind Om. "
      "Who is first in the queue?\nAnswer:", {"mode": "match_any", "terms": ["om"]}),
    q("RSN-M-01", "reasoning", "", "reasoning_multi_step",
      "Question: Start with the number 4. Add 6. Double the result. Subtract 5. "
      "Write only the final number.\nAnswer:", {"mode": "numeric", "answer": 15}),
]

# ═══════════════════════ HINGLISH ═══════════════════════
ITEMS += [
    q("HIN-CV-01", "hinglish", "", "hinglish_conversation",
      "Question: Tumhe bhookh lagi hai. Mummy se politely kya kahoge?\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["khana", "khaana", "food", "nashta", "khane"]},
                      {"any": ["please", "chahiye", "de do", "de dena", "bana do", "banao", "dena"]}]},
      max_new_tokens=32, type_="open"),
    q("HIN-CV-02", "hinglish", "", "hinglish_conversation",
      "Question: Aapka dost bimaar hai. Uske liye ek achhi si line likho.\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["theek", "get well", "aaram", "swasth", "sehat", "jaldi"]},
                      {"min_words": 3}]},
      max_new_tokens=32, type_="open"),
    q("HIN-CV-03", "hinglish", "", "hinglish_conversation",
      "Question: Tum school kab jaate ho — subah ya shaam?\nAnswer:",
      {"mode": "match_any", "terms": ["subah", "morning"]}),
    q("HIN-CO-01", "hinglish", "comprehension", "hinglish_comprehension",
      rq("Raju sabse pehle kya karta hai?", PASSAGE_H1),
      {"mode": "match_any", "terms": ["paani", "pani", "water"]}),
    q("HIN-CO-02", "hinglish", "comprehension", "hinglish_comprehension",
      rq("Raju kitne baje school ke liye nikalta hai?", PASSAGE_H1),
      {"mode": "numeric", "answer": 8}),
    q("HIN-CO-03", "hinglish", "comprehension", "hinglish_comprehension",
      rq("Meena ki dadi shaam ko kya banati hain?", PASSAGE_H2),
      {"mode": "match_any", "terms": ["halwa"]}),
    q("HIN-CO-04", "hinglish", "comprehension", "hinglish_comprehension",
      rq("Meena dadi ke liye kya le aati hai?", PASSAGE_H2),
      {"mode": "match_any", "terms": ["paani", "pani", "water"]}),
    q("HIN-MA-01", "hinglish", "", "hinglish_math",
      "Question: Ek pen 20 rupaye ka hai. 3 pen lene mein kitne rupaye lagenge?\nAnswer:",
      {"mode": "numeric", "answer": 60}),
    q("HIN-MA-02", "hinglish", "", "hinglish_math",
      "Question: Tumhare paas 75 rupaye the. Tumne 30 rupaye ki copy kharidi. "
      "Ab kitne rupaye bache?\nAnswer:", {"mode": "numeric", "answer": 45}),
    q("HIN-MA-03", "hinglish", "", "hinglish_math",
      "Question: 18 aam ko 3 mitron mein barabar baanta gaya. Har mitra ko kitne aam mile?\nAnswer:",
      {"mode": "numeric", "answer": 6}),
    q("HIN-MA-04", "hinglish", "", "hinglish_math",
      "Question: Ek bucket mein 15 litre paani tha. Usme se 6 litre nikal gaye, "
      "phir 4 litre paani daal diya. Ab kitne litre paani hai?\nAnswer:",
      {"mode": "numeric", "answer": 13}),
    q("HIN-SC-01", "hinglish", "", "hinglish_science",
      "Question: Ped humein konsi gas dete hain jise hum saans mein lete hain?\nAnswer:",
      {"mode": "match_any", "terms": ["oxygen", "oksijan"]}),
    q("HIN-SC-02", "hinglish", "", "hinglish_science",
      "Question: Suraj kis disha se ugta hai — purab ya pashchim?\nAnswer:",
      {"mode": "match_any", "terms": ["purab", "purva", "east"]}),
    q("HIN-SC-03", "hinglish", "", "hinglish_science",
      "Question: Barish ke baad aasman mein kabhi kabhi saat rang ka ek gol arch dikhta hai. "
      "Usko kya kehte hain?\nAnswer:",
      {"mode": "match_any", "terms": ["rainbow", "indradhanush", "dhanush"]}),
    q("HIN-SC-04", "hinglish", "", "hinglish_science",
      "Question: Ganda paani peene se humein kya ho sakta hai aur kyu?\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["bimaar", "bimar", "beemar", "sick", "ill"]},
                      {"any": ["germ", "kitanu", "keeda", "bacteria", "gandaki", "infection",
                               "dirt", "ganda", "milav"]},
                      {"min_words": 4}]},
      max_new_tokens=32, type_="open"),
    q("HIN-RE-01", "hinglish", "", "hinglish_reasoning",
      "Question: Agar aaj Saturday hai, toh parso (kal ke agle din) kaunsa din hoga?\nAnswer:",
      {"mode": "match_any", "terms": ["monday", "somvar", "somwar"]}),
    q("HIN-RE-02", "hinglish", "", "hinglish_reasoning",
      "Question: Ramesh Amit se lamba hai, aur Amit Mohan se lamba hai. "
      "Sabse chhota kaun hai?\nAnswer:", {"mode": "match_any", "terms": ["mohan"]}),
    q("HIN-IN-01", "hinglish", "instructions", "hinglish_instructions",
      "Question: Haath dhone ke steps ye the: pehle haath gile karo, phir soap lagao, "
      "phir pani se dho do. Sabse PEHLA step kya tha?\nAnswer:",
      {"mode": "match_any", "terms": ["gile", "gila", "wet", "paani", "pani"]}),
    q("HIN-IN-02", "hinglish", "instructions", "hinglish_instructions",
      "Question: School bag ready karne ka pehla kadam kya hai?\nAnswer:",
      {"mode": "match_any", "terms": ["timetable", "time table", "book", "kitab", "kitaab",
                                      "copy", "pencil", "check"]}),
]

# ═══════════════════════ INSTRUCTION FOLLOWING (English) ═══════════════════════
ITEMS += [
    q("INS-01", "instructions", "instructions", "instruction_following",
      "Question: Write these numbers in order from the smallest to the biggest: 2, 8, 5.\nAnswer:",
      {"mode": "numeric_sequence", "answer": [2, 5, 8]}),
    q("INS-02", "instructions", "instructions", "instruction_following",
      "Question: Answer with only one word: What colour is the sky on a clear day?\nAnswer:",
      {"mode": "one_word_any", "terms": ["blue"]}),
    q("INS-03", "instructions", "instructions", "instruction_following",
      "Question: Name any two domestic animals.\nAnswer:",
      {"mode": "min_matches",
       "terms": ["cow", "dog", "goat", "buffalo", "hen", "cat", "sheep", "camel", "horse",
                 "donkey", "rabbit"], "min": 2}),
    q("INS-04", "instructions", "instructions", "instruction_following",
      "Question: Write only the first letter of the word 'Elephant'.\nAnswer:",
      {"mode": "one_word_any", "terms": ["e"]}),
    q("INS-05", "instructions", "instructions", "instruction_following",
      "Question: Count the letters in the word 'SCHOOL' and write the number.\nAnswer:",
      {"mode": "numeric", "answer": 6}),
    q("INS-06", "instructions", "instructions", "instruction_following",
      "Question: Answer with only the number: 12 + 13 = ?\nAnswer:",
      {"mode": "numeric", "answer": 25}),
]

# ═══════════════════════ WRITING (open-ended, rubric) ═══════════════════════
ITEMS += [
    q("WRT-01", "writing", "", "writing",
      "Question: Write two sentences about your favourite festival.\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["diwali", "holi", "eid", "christmas", "pongal", "onam",
                               "baisakhi", "rakhi", "dussehra", "navratri", "gurpurab", "lohri"]},
                      {"min_words": 6}, {"min_sentences": 2}]},
      max_new_tokens=40, type_="open"),
    q("WRT-02", "writing", "", "writing",
      "Question: Explain in two sentences why we should not waste water.\nAnswer:",
      {"mode": "rubric",
       "components": [{"min_words": 8}, {"any": ["water"]},
                      {"any": ["save", "precious", "limited", "important", "future", "need",
                               "conserve", "life", "live"]}]},
      max_new_tokens=40, type_="open"),
    q("WRT-03", "writing", "", "writing",
      "Question: Aapne apne dost ki pencil kho di. Us se maafi maangte hue do line likho.\nAnswer:",
      {"mode": "rubric",
       "components": [{"any": ["sorry", "maafi", "maaf", "maf"]}, {"any": ["pencil"]},
                      {"min_words": 4}]},
      max_new_tokens=40, type_="open"),
    q("WRT-04", "writing", "", "writing",
      "Question: Write the first three things you do in the morning to get ready for school.\nAnswer:",
      {"mode": "rubric",
       "components": [{"min_words": 5},
                      {"any": ["wake", "brush", "bath", "uniform", "breakfast", "pack", "bag",
                               "fresh", "get up"]}]},
      max_new_tokens=40, type_="open"),
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as handle:
        for item in ITEMS:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    from collections import Counter
    sections = Counter(i["section"] for i in ITEMS)
    skills = Counter(i["skill"] for i in ITEMS if i["skill"])
    print(f"Wrote {len(ITEMS)} exam items to {OUT}")
    print("sections :", dict(sorted(sections.items())))
    print("skills   :", dict(sorted(skills.items())))
    modes = Counter(i["grade"]["mode"] for i in ITEMS)
    print("modes    :", dict(sorted(modes.items())))


if __name__ == "__main__":
    main()
