"""Reasoning and comprehension: why/how questions, cause & effect,
classification, sequencing, comparison, simple inference, pattern recognition,
multi-step instructions, simple logic, passage comprehension, and explaining
answers in simple language.

The goal: teach ANKIT to understand and explain, not merely repeat.
"""

from __future__ import annotations


def item(stage: int, kind: str, text: str) -> dict:
    return {"text": text, "category": "reasoning", "stage": stage, "kind": kind}


_WHY_HOW = [
    (2, "Why do we brush our teeth twice a day?",
     "Food bits stick to our teeth after eating. Germs in the mouth eat those bits and make "
     "acids that create holes (cavities) and bad breath. Brushing in the morning and before bed "
     "removes the food bits and keeps germs away, so our teeth stay strong."),
    (2, "How do we know it is going to rain?",
     "Dark heavy clouds gather in the sky, the air becomes cool and humid, and sometimes we feel "
     "a cool wind before the first drops. Farmers, cricket players and event planners all watch "
     "the sky and weather news to plan their day."),
    (3, "Why do leaves look green?",
     "Leaves contain a green colouring matter called chlorophyll. When sunlight falls on a "
     "leaf, the chlorophyll uses the light to make food and reflects the green part of light "
     "back to our eyes. That reflected green is what we see."),
    (3, "How does a seed become a plant?",
     "A seed needs water, air and warmth. Water soaks into the seed and swells it, the coat "
     "splits, and a root pushes down to drink water while a shoot pushes up towards light. The "
     "shoot grows leaves which start making food, and slowly the seedling becomes a plant. This "
     "whole process is germination and growth."),
    (3, "Why should we not throw plastic in rivers?",
     "Plastic does not rot for hundreds of years. In rivers it floats downstream, fish and "
     "turtles may eat it and die, and it blocks drains causing floods. Plastic finally reaches "
     "the sea, where it harms even bigger animals. So plastic belongs in a dustbin and a "
     "recycling bin — never in water."),
    (4, "How do vaccinations protect us?",
     "A vaccine teaches our body's defence system (the immune system) in advance. It shows the "
     "body a weak or harmless form of a germ so the body learns to fight it. Later, if the real "
     "germ attacks, the body already knows how to defeat it quickly, so we do not fall "
     "seriously ill."),
    (4, "Why does an ice cube melt in our hand?",
     "Our hand is warmer than ice. Heat always flows from a warmer thing to a cooler thing. "
     "The heat from our hand travels into the ice, breaking its solid structure, and it turns "
     "into water. The same thing happens on a hot day anywhere on Earth."),
    (4, "How do farmers know when to sow seeds?",
     "Farmers watch the seasons and the rain. Most crops are sown just before the monsoon so "
     "the young plants get plenty of water. They check the soil, the temperature and the "
     "weather forecast. Sowing at the right time decides how good the harvest will be — timing "
     "is everything in farming."),
]

_CLASSIFY = [
    (1, "Sort these: apple, potato, banana, onion. Fruits or vegetables?",
     "Fruits: apple and banana — they are sweet and grow on plants as fruits. Vegetables: "
     "potato and onion — they grow under the ground and are cooked as vegetables. Sorting by a "
     "rule is called classification."),
    (2, "Odd one out: cow, goat, tiger, buffalo. Why?",
     "Tiger is the odd one. Cow, goat and buffalo are domestic animals that give us milk; the "
     "tiger is a wild animal that hunts other animals. Explaining WHY completes the answer."),
    (2, "Odd one out: rose, mango, marigold, lotus. Why?",
     "Mango is the odd one. Rose, marigold and lotus are flowers; mango is a fruit."),
    (3, "Sort these into living and non-living: bus, banyan tree, river, sparrow, book, ant.",
     "Living: banyan tree, sparrow, ant — they grow, breathe and respond. Non-living: bus, "
     "river, book — they do not grow or breathe by themselves. Note: a river 'moves', but "
     "movement alone does not make something living!"),
    (3, "Group these by what they give us: cow, hen, cotton plant, sheep, bee.",
     "Milk: cow. Eggs: hen. Cloth: cotton plant (cotton fibres) and sheep (wool). Honey and "
     "wax: bee. The same sorting rule can group many things at once."),
    (4, "Classify these changes as reversible or irreversible: melting ice, burning paper, "
     "folding paper, baking a roti.",
     "Reversible (can be undone): melting ice (freeze it again), folding paper (unfold it). "
     "Irreversible (cannot be undone): burning paper (becomes ash), baking a roti (dough cannot "
     "come back). Heating, mixing and burning often cause irreversible changes."),
]

_SEQUENCE = [
    (2, "Put in order and tell the story: seed, small plant, tree with fruits, sprout.",
     "Correct order: seed -> sprout -> small plant -> tree with fruits.\n"
     "A seed sprouts first, grows into a small plant, then a big tree, and finally the tree "
     "makes flowers and fruits with new seeds. Sequencing means putting things in the order "
     "they happen."),
    (2, "Sequence your morning: brush teeth, wake up, eat breakfast, wear uniform, pack bag.",
     "A sensible order: 1. Wake up. 2. Brush teeth. 3. Wear uniform. 4. Eat breakfast. "
     "5. Pack bag.\nSome steps must come before others — brushing before breakfast, waking "
     "before everything!"),
    (3, "Number these to tell how bread reaches us: baker bakes, wheat is ground into flour, "
     "farmer grows wheat, shop sells bread, flour goes to the bakery.",
     "1. Farmer grows wheat. 2. Wheat is ground into flour. 3. Flour goes to the bakery. "
     "4. Baker bakes bread. 5. Shop sells bread.\nEvery food follows a chain of steps, and "
     "each step depends on the one before."),
    (4, "Sequence the butterfly's life and name each stage.",
     "1. Egg — laid on a leaf. 2. Larva (caterpillar) — hatches and eats leaves, growing fast. "
     "3. Pupa (cocoon/chrysalis) — the resting stage where the body changes. 4. Adult "
     "butterfly — comes out with wings. This complete change of body form is metamorphosis."),
]

_COMPARE = [
    (2, "How is a fish different from a cat?",
     "A fish lives in water, breathes with gills, and has fins and scales. A cat lives on "
     "land, breathes with lungs, and has fur and four legs. Both are animals, both eat food, "
     "and both are living things — comparing means finding similarities AND differences."),
    (3, "Compare a village and a city.",
     "A village has fewer people, open fields, fresh air and quiet life; jobs are mostly "
     "farming. A city has many people, tall buildings, schools, hospitals and markets; jobs "
     "are of many kinds. Both are communities where people live, work and help each other."),
    (3, "Which is heavier: 1 kg of cotton or 1 kg of iron?",
     "Trick question! Both weigh exactly 1 kg. The cotton takes a much bigger bag (space) but "
     "the WEIGHT is the same. Always read such questions carefully."),
    (4, "Compare the Sun and the Moon.",
     "Similarities: both appear as bright round bodies in our sky. Differences: the Sun makes "
     "its own light and heat and is a huge star; the Moon only reflects sunlight and is much, "
     "much smaller, Earth's neighbour. The Sun gives us day; the Moon brightens the night."),
]

_INFERENCE = [
    (3, "Riya came to school with a wet umbrella and wet shoes. What can you guess, and why?",
     "It probably rained on her way to school. We did not SEE the rain, but the wet umbrella "
     "and shoes are clues. Using clues to reach a sensible conclusion is called inference."),
    (3, "A plant in a dark corner is yellow and weak, but the plant near the window is green "
     "and strong. What do you understand?",
     "Plants need sunlight to stay green and healthy. The dark-corner plant could not make "
     "enough food, so it became pale and weak. The comparison of the two plants is the clue."),
    (4, "Every time Aman eats from the street stall he gets a stomach ache, but not when he "
     "eats home food. What can he conclude?",
     "Something about the stall's food — maybe stale food, dirty water or unclean hands — is "
     "causing the stomach ache. Repeated patterns are strong clues. Aman should eat clean, "
     "fresh food and tell his parents."),
    (4, "Footprints of many birds are seen near a broken window with grains scattered around. "
     "What most likely happened?",
     "Most likely birds came to eat the grains, sat on the window sill, and the window broke "
     "— perhaps it was already weak. The clues (footprints, grains, broken glass) fit together "
     "like a small detective story. Inference means the BEST explanation of the clues, not a "
     "wild guess."),
]

_PATTERN = [
    (2, "Find the next shape pattern: circle, square, circle, square, circle, ...",
     "The rule is alternate circle-square. After circle comes square. Pattern rules repeat or "
     "grow."),
    (3, "Complete: 5, 10, 15, 20, __, __. What is the rule?",
     "Next numbers: 25 and 30. The rule is 'add 5 each time' — it is the table of five."),
    (3, "Complete: 27, 24, 21, 18, __, __. What is the rule?",
     "Next numbers: 15 and 12. The rule is 'subtract 3 each time' — the pattern is going "
     "downhill in equal jumps."),
    (4, "Complete: 1, 2, 4, 8, 16, __. What is the rule?",
     "Next number: 32. The rule is 'double each time' — 1x2=2, 2x2=4, 4x2=8, 8x2=16, 16x2=32. "
     "Doubling grows very fast!"),
    (4, "Complete: 1, 1, 2, 3, 5, 8, __. Look carefully at neighbours.",
     "Next number: 13. The rule: add the previous TWO numbers (1+1=2, 1+2=3, 2+3=5, 3+5=8, "
     "5+8=13). This famous pattern is called the Fibonacci pattern — sunflower seeds follow it!"),
]

_MULTISTEP = [
    (2, "Follow the steps: 1. Put your hands up. 2. Clap three times. 3. Touch your toes. "
     "4. Stand straight. What did you do just now?",
     "I followed four steps in order: hands up, three claps, touched my toes, and stood "
     "straight. Doing steps in the given order is following multi-step instructions — each "
     "step matters."),
    (3, "Multi-step problem: Take a number, add 5, then double the result. Start with 7.",
     "Step 1: 7 + 5 = 12. Step 2: double 12 = 24. Answer: 24.\nIn multi-step problems, do one "
     "step at a time and carry each answer into the next step."),
    (4, "Multi-step problem: Riya had 24 rupees. She spent 9 rupees on a pencil and 5 on an "
     "eraser. Then she found 10 rupees in her bag. How much does she have now?",
     "Step 1: 24 - 9 = 15 after the pencil. Step 2: 15 - 5 = 10 after the eraser. Step 3: "
     "10 + 10 = 20 after finding money. Answer: Riya has 20 rupees now."),
    (4, "Multi-step science: A potted plant was left near a window all week, watered daily. "
     "Another was kept in a cupboard, watered daily. Predict the difference and explain in two "
     "steps.",
     "Step 1 (prediction): the window plant grows green and strong; the cupboard plant turns "
     "pale, weak and leans towards any light. Step 2 (explanation): both got water, but only "
     "the window plant got sunlight to make food by photosynthesis — light, not just water, "
     "keeps a plant healthy."),
]

_LOGIC = [
    (3, "All cats have tails. Simba is a cat. What do you know for sure about Simba?",
     "Simba has a tail. If ALL cats have tails and Simba is a cat, then Simba must have a "
     "tail. This step-by-step conclusion is called logical deduction."),
    (3, "Ravi is taller than Amit. Amit is taller than Kishan. Who is shortest?",
     "Kishan is the shortest. Order: Ravi > Amit > Kishan. Lining up facts in order solves "
     "such puzzles quickly."),
    (4, "If today is Friday, what day will it be after 10 days?",
     "A week has 7 days. 10 = 7 + 3, so after one full week it is Friday again, and 3 days "
     "later it is Monday. Answer: Monday."),
    (4, "Meena has 3 red and 5 blue balloons. Without looking, what is the LEAST number of "
     "balloons she must pick to be sure she has at least one red balloon?",
     "She must pick 6. In the worst case, the first 5 picks could all be blue; the very next "
     "(6th) balloon must be red, since only 5 blue ones exist. Thinking of the WORST case "
     "solves 'at least sure' puzzles."),
    (4, "A clock shows 3:00 — the hour hand on 3 and the minute hand on 12. What kind of "
     "angle do the two hands make?",
     "The full clock is a circle of 12 hour-marks. The hands are 3 marks apart, and 3 out of "
     "12 is exactly one quarter of the circle. A quarter of a full turn is a right angle "
     "(90 degrees). At 3 o'clock the clock hands always make a right angle."),
]

_PASSAGES = [
    (3, "Read the passage: 'Bees are small but very important insects. They fly from flower to "
     "flower to collect nectar for making honey. While doing this, yellow pollen sticks to "
     "their bodies and travels with them. When this pollen touches another flower, that flower "
     "can turn into a fruit with seeds.'\n"
     "Q1: Why do bees visit flowers?\nA1: Bees visit flowers to collect nectar, which they use "
     "to make honey.\n"
     "Q2: What happens when pollen touches another flower?\nA2: The flower can turn into a "
     "fruit with seeds.\n"
     "Q3: Why are bees important for farmers?\nA3: Because bees carry pollen between flowers, "
     "which helps plants make fruits and seeds — without this, many crops would not grow."),
    (4, "Read the passage: 'Long ago, people in a village walked hours to fetch water from a "
     "faraway pond. A wise teacher suggested digging a small lake at the edge of the village "
     "to catch the monsoon rain. The whole village worked together for one month and dug the "
     "lake. That year, when the rains came, the lake filled up. Now women and children walk "
     "only five minutes for water, and farmers grow a second crop.'\n"
     "Q1: What problem did the village have?\nA1: People had to walk hours to fetch water from "
     "a faraway pond.\n"
     "Q2: How was the problem solved?\nA2: The whole village dug a small lake at the edge of "
     "the village to catch the monsoon rain.\n"
     "Q3: What changed after the lake was built?\nA3: Water became nearby (five minutes away), "
     "and farmers could grow a second crop.\n"
     "Q4: What does this story teach about solving problems?\nA4: That a community which plans "
     "and works together can solve big problems for everyone."),
    (4, "Read the passage: 'The desert is hot and dry, yet life survives there. The camel "
     "stores fat in its hump, can go days without water, and has long lashes to keep sand out "
     "of its eyes. The cactus stores water in its thick green stem, and its spines stop "
     "animals from eating it.'\n"
     "Q1: How does the camel survive without water for days?\nA1: Its body is built for the "
     "desert — it stores fat in its hump and uses water very carefully.\n"
     "Q2: How does the cactus protect its stored water?\nA2: Its spines (thorns) stop animals "
     "from eating it, and its thick stem holds water.\n"
     "Q3: What is common between the camel and the cactus?\nA3: Both are suited to desert "
     "life — their bodies have special features that help them live with very little water."),
]


def build() -> list[dict]:
    out: list[dict] = []
    groups = (_WHY_HOW, _CLASSIFY, _SEQUENCE, _COMPARE, _INFERENCE, _PATTERN,
              _MULTISTEP, _LOGIC)
    for group in groups:
        for stage, q, a in group:
            out.append(item(stage, "reasoning", f"Question: {q}\nAnswer: {a}"))
    # Passage comprehension: (stage, full_text_with_embedded_questions).
    for stage, text in _PASSAGES:
        out.append(item(stage, "comprehension", text))

    # -- Expanded parametric practice (foundation-training scale-up) ---------
    out += _number_patterns(n=280)
    out += _odd_one_out(n=220)
    out += _analogies(n=180)
    out += _age_relation_riddles(n=150)
    out += _classification_lists(n=140)
    out += _multi_step_instruction_tasks(n=110)
    out += _day_logic(n=110)
    return out


# ===========================================================================
# Expanded parametric practice — foundation-training scale-up.
# ===========================================================================
import random as _random

_rng = _random.Random(20240506)


def _qa(stage: int, kind: str, q: str, a: str) -> dict:
    return item(stage, kind, f"Question: {q}\nAnswer: {a}")


def _number_patterns(n: int = 150) -> list[dict]:
    out = []
    for _ in range(n):
        style = _rng.randrange(5)
        if style == 0:  # +d
            a = _rng.randint(1, 20); d = _rng.randint(2, 9)
            seq = [a + d * i for i in range(5)]
        elif style == 1:  # -d (stays positive)
            d = _rng.randint(2, 9)
            a = _rng.randint(10 + 4 * d, 90)
            seq = [a - d * i for i in range(5)]
        elif style == 2:  # x2
            a = _rng.randint(1, 6)
            seq = [a * 2 ** i for i in range(5)]
        elif style == 3:  # alternating +a -b
            a = _rng.randint(2, 10); b = _rng.randint(1, 8); x = _rng.randint(5, 30)
            seq = [x, x + a, x + a - b, x + 2 * a - b, x + 2 * a - 2 * b]
        else:  # skip counting
            a = _rng.randint(2, 12); k = _rng.choice([5, 10, 25])
            seq = [a * k, (a + 1) * k, (a + 2) * k, (a + 3) * k]
        seq_str = ", ".join(str(x) for x in seq)
        nxt = {"style0": seq[-1] + d if style == 0 else None,
               "s1": seq[-1] - d if style == 1 else None}.get("style0") or \
              (seq[-1] - d if style == 1 else seq[-1] * 2 if style == 2 else None)
        if style in (0, 1):
            nxt = seq[-1] + (d if style == 0 else -d)
            rule = f"add {d}" if style == 0 else f"subtract {d}"
        elif style == 2:
            nxt = seq[-1] * 2
            rule = "double the last number"
        elif style == 3:
            nxt = x + 3 * a - 2 * b - (x + 2 * a - 2 * b) + seq[-1] if False else seq[-1] + a
            rule = f"add {a}, then subtract {b}, and repeat"
        else:
            nxt = seq[-1] + k
            rule = f"skip count in {k}s"
        out.append(_qa(_rng.choice([2, 3, 4]), "pattern",
                       f"Find the next number: {seq_str}, ___",
                       f"The pattern is to {rule}. The next number is {nxt}. ({seq_str}, {nxt})"))
    return out


def _odd_one_out(n: int = 120) -> list[dict]:
    groups = [
        (["apple", "mango", "banana", "carrot"], "carrot", "carrot is a vegetable; the rest are fruits"),
        (["dog", "cat", "cow", "sparrow"], "sparrow", "sparrow is a bird; the rest are animals/mammals"),
        (["rose", "lotus", "marigold", "mango tree"], "mango tree", "mango tree is a tree; the rest are flowers"),
        (["bus", "car", "cycle", "boat"], "boat", "boat moves on water; the rest run on roads"),
        (["pen", "pencil", "eraser", "apple"], "apple", "apple is a fruit; the rest are stationery items"),
        (["sun", "moon", "star", "lamp"], "lamp", "lamp is made by people; the rest are in the sky"),
        (["parrot", "crow", "bat", "sparrow"], "bat", "bat is a mammal; the rest are birds"),
        (["snake", "lizard", "crocodile", "frog"], "frog", "frog is an amphibian; the rest are reptiles"),
        (["one", "two", "three", "letter"], "letter", "letter is not a number; the rest are numbers"),
        (["Monday", "Tuesday", "January", "Friday"], "January", "January is a month; the rest are days of the week"),
        (["eyes", "ears", "nose", "shoes"], "shoes", "shoes are worn; the rest are body parts"),
        (["Ganga", "Yamuna", "Krishna", "Mount Everest"], "Mount Everest", "Mount Everest is a mountain; the rest are rivers"),
        (["Delhi", "Mumbai", "Chennai", "Nepal"], "Nepal", "Nepal is a country; the rest are Indian cities"),
        (["2", "4", "6", "7"], "7", "7 is an odd number; the rest are even"),
        (["3", "5", "8", "11"], "8", "8 is even; the rest are odd numbers"),
        (["triangle", "square", "circle", "cube"], "cube", "cube is a 3-D solid; the rest are flat (2-D) shapes"),
        (["milk", "curd", "butter", "lemon"], "lemon", "lemon is not a dairy product; the rest come from milk"),
        (["winter", "summer", "monsoon", "Monday"], "Monday", "Monday is a day; the rest are seasons"),
        (["poet", "poem", "story", "letter"], "poet", "poet is a person; the rest are written things"),
        (["walk", "run", "jump", "chair"], "chair", "chair is a thing; the rest are actions (verbs)"),
        (["gold", "silver", "iron", "cloth"], "cloth", "cloth is not a metal; the rest are metals"),
        (["heptagon", "hexagon", "pentagon", "protractor"], "protractor", "protractor is a measuring tool; the rest are shapes"),
        (["sofa", "bed", "table", "garden"], "garden", "garden is outdoors; the rest are furniture in a home"),
        (["cricket", "football", "hockey", "chess"], "chess", "chess is an indoor board game; the rest are field games"),
        (["sewing machine", "needle", "thread", "houseboat"], "houseboat", "houseboat is a boat; the rest are used for stitching"),
        (["Celsius", "kilometre", "litre", "kilogram"], "Celsius", "Celsius measures temperature; the rest measure length, volume and weight"),
        (["byte", "kilobyte", "megabyte", "kilometre"], "kilometre", "kilometre measures distance; the rest measure computer data"),
        (["sunflower oil", "coconut oil", "groundnut oil", "castor oil plant"], "castor oil plant", "it is a plant; the rest are cooking oils"),
        (["Ganga", "Amazon", "Nile", "Everest"], "Everest", "Everest is a mountain; the rest are rivers"),
        (["printer", "keyboard", "mouse", "blackboard"], "blackboard", "blackboard belongs to a classroom; the rest are computer parts"),
        (["mango pickle", "lemon pickle", "chilli pickle", "mango shake"], "mango shake", "mango shake is a drink; the rest are pickles"),
    ]
    out = []
    for _ in range(n):
        items_, odd, why = _rng.choice(groups)
        shuffled = items_[:]; _rng.shuffle(shuffled)
        out.append(_qa(_rng.choice([1, 2, 3]), "reasoning",
                       f"Find the odd one out: {', '.join(shuffled)}",
                       f"'{odd}' is the odd one out because {why}."))
    return out


def _analogies(n: int = 90) -> list[dict]:
    pairs = [
        ("Dog is to puppy as cat is to ___", "kitten", "a baby dog is a puppy, so a baby cat is a kitten"),
        ("Cow is to calf as horse is to ___", "foal", "a baby cow is a calf, so a baby horse is a foal"),
        ("Hen is to chick as duck is to ___", "duckling", "a baby hen is a chick, so a baby duck is a duckling"),
        ("Hand is to glove as foot is to ___", "shoe", "we wear a glove on a hand, so we wear a shoe on a foot"),
        ("Fish is to water as bird is to ___", "air/sky", "a fish lives in water, so a bird lives in the air"),
        ("Teacher is to school as doctor is to ___", "hospital", "a teacher works in a school, so a doctor works in a hospital"),
        ("Hot is to cold as happy is to ___", "sad", "hot and cold are opposites, so the opposite of happy is sad"),
        ("Big is to small as tall is to ___", "short", "big and small are opposites, so the opposite of tall is short"),
        ("Sun is to day as moon is to ___", "night", "the sun shines in the day, so the moon shines at night"),
        ("Pen is to write as knife is to ___", "cut", "we write with a pen, so we cut with a knife"),
        ("Water is to drink as bread is to ___", "eat", "we drink water, so we eat bread"),
        ("Book is to read as song is to ___", "sing/listen", "we read a book, so we sing or listen to a song"),
        ("Farmer is to field as chef is to ___", "kitchen", "a farmer works in a field, so a chef works in a kitchen"),
        ("Wings are to bird as legs are to ___", "human/animal", "birds use wings to move, so humans and animals use legs"),
        ("Milk is to cow as wool is to ___", "sheep", "milk comes from a cow, so wool comes from a sheep"),
        ("Bee is to hive as bird is to ___", "nest", "a bee lives in a hive, so a bird lives in a nest"),
        ("Sweet is to sugar as sour is to ___", "lemon/tamarind", "sugar tastes sweet, so lemon tastes sour"),
        ("Rain is to umbrella as sun is to ___", "cap/sunglasses", "we use an umbrella in rain, so we use a cap or sunglasses in the sun"),
        ("Ear is to hear as eye is to ___", "see", "we hear with the ear, so we see with the eye"),
        ("Page is to book as brick is to ___", "wall", "pages make a book, so bricks make a wall"),
    ]
    out = []
    for _ in range(n):
        q, a, why = _rng.choice(pairs)
        out.append(_qa(_rng.choice([2, 3, 4]), "reasoning",
                       f"Complete the analogy: {q}?",
                       f"{a.capitalize()}. Because {why}."))
    return out


def _age_relation_riddles(n: int = 90) -> list[dict]:
    out = []
    for _ in range(n):
        style = _rng.randrange(3)
        if style == 0:  # age after/before
            name = _rng.choice(["Ravi", "Meera", "Aman", "Sita", "Kiran"])
            now = _rng.randint(6, 40); k = _rng.randint(2, 12)
            future = _rng.random() < 0.5
            q = f"{name} is {now} years old now. How old will {name} be after {k} years?" if future else \
                f"{name} is {now} years old now. How old was {name} {k} years ago?"
            a = f"{name} will be {now + k} years old after {k} years ({now} + {k} = {now + k})." if future else \
                f"{name} was {now - k} years old {k} years ago ({now} - {k} = {now - k})."
            out.append(_qa(3, "reasoning", q, a))
        elif style == 1:  # family relations
            rels = [
                ("Your mother's brother", "uncle (mama)"),
                ("Your father's sister", "aunt (bua)"),
                ("Your mother's mother", "grandmother (nani)"),
                ("Your father's father", "grandfather (dada)"),
                ("Your uncle's child", "cousin"),
                ("Your sister's daughter", "niece"),
                ("Your brother's son", "nephew"),
            ]
            rel, ans = _rng.choice(rels)
            out.append(_qa(2, "reasoning", f"What relation is your {rel.lower()} to you?",
                           f"Your {rel.lower()} is your {ans}."))
        else:  # comparing heights/ages
            n1, n2, n3 = _rng.sample(["Om", "Anu", "Ram", "Zoya", "Ved", "Ira"], 3)
            order = [n1, n2, n3]; _rng.shuffle(order)
            tallest, mid, shortest = order
            out.append(_qa(3, "reasoning",
                           f"{tallest} is taller than {mid}, and {mid} is taller than {shortest}. Who is the tallest and who is the shortest?",
                           f"{tallest} is the tallest and {shortest} is the shortest."))
    return out


def _classification_lists(n: int = 80) -> list[dict]:
    banks = [
        (1, "living things", ["plant", "dog", "bird", "fish", "tree", "human"], "non-living things", ["chair", "rock", "car", "ball", "table"]),
        (1, "colours", ["red", "blue", "green", "yellow", "pink"], "not colours", ["dog", "table", "mango", "pen"]),
        (2, "fruits", ["mango", "banana", "apple", "guava", "papaya"], "vegetables", ["potato", "carrot", "cabbage", "spinach"]),
        (2, "things we wear", ["shirt", "shoes", "cap", "socks", "frock"], "things we eat", ["rice", "milk", "egg", "roti"]),
        (3, "birds", ["sparrow", "parrot", "crow", "peacock", "pigeon"], "insects", ["ant", "bee", "butterfly", "mosquito"]),
        (3, "sources of water", ["river", "well", "rain", "lake", "spring"], "man-made things at home", ["chair", "fan", "cup", "sofa"]),
        (4, "planets", ["Mercury", "Venus", "Earth", "Mars", "Jupiter"], "stars we can name", ["Sun", "Polaris (North Star)"]),
        (4, "renewable resources", ["sunlight", "wind", "rain water"], "non-renewable resources", ["coal", "petrol", "diesel"]),
    ]
    out = []
    for _ in range(n):
        stage, label_a, items_a, label_b, items_b = _rng.choice(banks)
        k = min(3, len(items_a))
        picks = _rng.sample(items_a, k)
        out.append(_qa(stage, "reasoning",
                       f"Name {k} {label_a}.",
                       f"{k} {label_a} are: {', '.join(picks)}."))
    return out


def _multi_step_instruction_tasks(n: int = 70) -> list[dict]:
    tasks = [
        ("Write the numbers 4, 9 and 2 in order from smallest to biggest, then add the smallest and the biggest.",
         lambda a, b, c: (f"In order: {a}, {b}, {c}." if False else f"In order from smallest to biggest: {', '.join(map(str, sorted([a, b, c])))}. "
                          f"The smallest is {min(a, b, c)} and the biggest is {max(a, b, c)}. "
                          f"{min(a, b, c)} + {max(a, b, c)} = {min(a, b, c) + max(a, b, c)}.")),
        ("Take the number 7, double it, and then add 5. What do you get?",
         lambda: f"7 doubled is 14, and 14 + 5 = 19."),
        ("Think of the number of days in a week, add the number of fingers on one hand. What is the total?",
         lambda: f"A week has 7 days and one hand has 5 fingers. 7 + 5 = 12."),
        ("Count how many letters are in the word 'SCHOOL', then tell the first and last letter.",
         lambda: f"'SCHOOL' has 6 letters. The first letter is S and the last letter is L."),
        ("From the word 'RAINY', write the second and fourth letters.",
         lambda: "The word is R-A-I-N-Y. The second letter is A and the fourth letter is N."),
        ("Start at 20 and count back in fives. Write the first three numbers.",
         lambda: "20, 15, 10 — we subtract 5 each time."),
    ]
    out = []
    for _ in range(n):
        style = _rng.randrange(3)
        if style == 0:
            q, fn = _rng.choice(tasks[1:])
            out.append(_qa(_rng.choice([3, 4]), "instructions", q, fn()))
        else:
            a, b, c = _rng.sample(range(1, 50), 3)
            q, fn = tasks[0]
            out.append(_qa(_rng.choice([3, 4]), "instructions", q, fn(a, b, c)))
    return out


def _day_logic(n: int = 60) -> list[dict]:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    out = []
    for _ in range(n):
        style = _rng.randrange(3)
        i = _rng.randrange(7); k = _rng.randint(1, 10)
        if style == 0:
            out.append(_qa(2, "reasoning",
                           f"If today is {days[i]}, what day will it be tomorrow and what day was it yesterday?",
                           f"Tomorrow will be {days[(i + 1) % 7]} and yesterday was {days[(i - 1) % 7]}."))
        elif style == 1:
            out.append(_qa(3, "reasoning",
                           f"If today is {days[i]}, what day will it be after {k} days?",
                           f"{k} days after {days[i]} is {days[(i + k) % 7]}."))
        else:
            out.append(_qa(3, "reasoning",
                           "Which days of the week are called weekend days?",
                           "Saturday and Sunday are the weekend days. Most schools and offices are closed then."))
    return out
