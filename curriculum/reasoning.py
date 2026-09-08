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
    return out
