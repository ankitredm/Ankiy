"""Mathematics foundation: Class 1-4, generated progressively.

Topics grow stage by stage:
    stage 1: counting, number recognition, compare, add/subtract within 10,
             shapes, simple patterns
    stage 2: numbers to 100, place value (tens/ones), add/subtract to 100,
             multiplication as repeated addition, tables, money, time, measuring
    stage 3: numbers to 1000, carry/borrow, tables & division facts, fractions
             (halves/thirds/quarters), units (m/cm, kg/g, L), calendar, perimeter
    stage 4: numbers to 10000, bigger multiplication/division (with remainder),
             equivalent fractions, decimals (tenths), factors & multiples,
             multi-step word problems

Exercise numbers are randomised with a fixed seed, then exact duplicates are
removed by build.py. Every topic also emits WORKED EXAMPLES that show the
steps, not just question-answer pairs.
"""

from __future__ import annotations

import random

rng = random.Random(20240501)

_NUM_WORDS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
]

_COUNTABLES = [
    "apples", "mangoes", "bananas", "pencils", "books", "marbles", "balloons",
    "stars", "flowers", "birds", "dogs", "cats", "eggs", "oranges", "toy cars",
    "biscuits", "leaves", "shells", "candles", "buttons",
]

_NAMES = ["Ravi", "Meera", "Aman", "Sita", "Rahul", "Priya", "Arjun", "Neha",
          "Kiran", "Vikram", "Anita", "Sameer", "Pooja", "Ramesh", "Geeta"]


def item(stage: int, kind: str, text: str) -> dict:
    return {"text": text, "category": "math", "stage": stage, "kind": kind}


def _count_word(n: int) -> str:
    return _NUM_WORDS[n] if n < len(_NUM_WORDS) else str(n)


# ---------------------------------------------------------------------------
# Stage 1 — counting, recognition, compare, add/sub within 10, shapes
# ---------------------------------------------------------------------------
def _counting_exercises(n_each: int = 12) -> list[dict]:
    out = []
    for _ in range(n_each):
        n = rng.randint(3, 20)
        thing = rng.choice(_COUNTABLES)
        out.append(item(1, "exercise",
            f"Question: Count the {thing}. There are {n} {thing} in a row. How many {thing} are there?\n"
            f"Answer: Let us count: 1, 2, 3, ... up to {n}. There are {n} {thing}. "
            f"The number {n} is written as '{n}' and read as '{_count_word(n)}'."))
    for _ in range(2):
        n = rng.randint(6, 20)
        thing = rng.choice(_COUNTABLES)
        out.append(item(1, "worked",
            f"Worked example — count and write.\n"
            f"There are {n} {thing} on the table. To count them, we point to each one and say the "
            f"number names in order: one, two, three, four, five, six, seven, eight, nine, ten, "
            f"eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty.\n"
            f"The last number we say while counting is the total. Here the total is {n} {thing}."))
    return out


def _number_recognition(n_each: int = 7) -> list[dict]:
    out = []
    for _ in range(n_each):
        a, b = rng.randint(1, 20), rng.randint(1, 20)
        while b == a:
            b = rng.randint(1, 20)
        bigger, smaller = max(a, b), min(a, b)
        out.append(item(1, "qa",
            f"Question: Which number is bigger, {a} or {b}?\n"
            f"Answer: {bigger} is bigger than {smaller}, because when we count, {bigger} comes after {smaller}. "
            f"We write: {bigger} > {smaller}."))
        out.append(item(1, "qa",
            f"Question: Which number is smaller, {a} or {b}?\n"
            f"Answer: {smaller} is smaller than {bigger}. We write: {smaller} < {bigger}."))
    return out


def _add_sub_within_10(n_each: int = 24) -> list[dict]:
    out = []
    for _ in range(n_each):
        a, b = rng.randint(1, 6), rng.randint(1, 4)
        thing = rng.choice(_COUNTABLES)
        out.append(item(1, "qa",
            f"Question: There are {a} {thing} on a plate. {b} more {thing} are added. How many {thing} now?\n"
            f"Answer: {a} + {b} = {a + b}. There are {a + b} {thing} now."))
    for _ in range(n_each):
        a = rng.randint(3, 10)
        b = rng.randint(1, a - 1)
        thing = rng.choice(_COUNTABLES)
        out.append(item(1, "qa",
            f"Question: There were {a} {thing}. {b} {thing} were taken away. How many are left?\n"
            f"Answer: {a} - {b} = {a - b}. {a - b} {thing} are left."))
    for _ in range(2):
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        out.append(item(1, "worked",
            f"Worked example — adding with fingers and number line.\n"
            f"Find {a} + {b}.\n"
            f"Step 1: Start at {a} on the number line.\n"
            f"Step 2: Jump forward {b} times: {' -> '.join(str(a + i) for i in range(1, b + 1))}.\n"
            f"Step 3: We land on {a + b}. So {a} + {b} = {a + b}.\n"
            f"Check with fingers: hold up {a} fingers, then {b} more, and count them all together."))
    for _ in range(2):
        a = rng.randint(4, 10)
        b = rng.randint(1, a - 1)
        out.append(item(1, "worked",
            f"Worked example — taking away.\n"
            f"Find {a} - {b}.\n"
            f"Step 1: Count out {a} objects.\n"
            f"Step 2: Take away {b} of them.\n"
            f"Step 3: Count what is left. {a - b} objects are left. So {a} - {b} = {a - b}.\n"
            f"Taking away is called subtraction, and the answer is called the difference."))
    return out


_SHAPES_1 = [
    ("circle", "round like a ball or a coin; it has no corners"),
    ("square", "it has 4 equal sides and 4 corners, like a chess board square"),
    ("triangle", "it has 3 straight sides and 3 corners, like a slice of pizza"),
    ("rectangle", "it has 4 sides; opposite sides are equal, like a door"),
    ("star", "it has pointed tips, like stars in the night sky"),
    ("oval", "it looks like a stretched circle, like an egg"),
]


def _shapes_items(n_each: int = 3) -> list[dict]:
    out = []
    for name, desc in _SHAPES_1:
        out.append(item(1, "explanation",
            f"Shape: {name}.\nA {name} is {desc}.\n"
            f"Look around: a {name} can be found on many things at home and school. "
            f"Try drawing a {name} in your notebook."))
        out.append(item(1, "qa",
            f"Question: What shape has {desc.split(' has ')[-1] if ' has ' in desc else desc}?\n"
            f"Answer: That is a {name}."))
    out.append(item(1, "exercise",
        "Shape hunt exercise.\nFind one object for each shape: circle (a coin), square (a stamp), "
        "triangle (a samosa), rectangle (a door). Draw each object and write the name of its shape "
        "under it. Shapes are everywhere once you start looking!"))
    return out


def _patterns_items(n: int = 7) -> list[dict]:
    out = []
    for _ in range(n):
        a, b = rng.choice([(2, 4), (1, 3), (5, 10), (10, 20)])
        seq = [a, b, a, b, a, b]
        nxt = a
        out.append(item(1, "qa",
            f"Question: Continue the pattern: {', '.join(map(str, seq))}, ...\n"
            f"Answer: The pattern repeats {a}, {b} again and again. So the next number is {nxt}. "
            f"Patterns follow a rule; find the rule first, then continue."))
    out.append(item(2, "worked",
        "Worked example — growing patterns.\n"
        "Look at this pattern: 2, 4, 6, 8, ...\n"
        "Step 1: Check the jump between numbers: 4 - 2 = 2, 6 - 4 = 2, 8 - 6 = 2.\n"
        "Step 2: The rule is 'add 2 each time'.\n"
        "Step 3: The next numbers are 10 and 12.\n"
        "Growing patterns can also go backwards: 20, 18, 16, ... here the rule is 'subtract 2'."))
    return out


# ---------------------------------------------------------------------------
# Stage 2 — numbers to 100, place value, add/sub to 100, repeated addition
# ---------------------------------------------------------------------------
def _place_value_items(n_each: int = 14) -> list[dict]:
    out = [
        item(2, "explanation",
            "Place value — tens and ones.\n"
            "In a two-digit number, the left digit counts TENS and the right digit counts ONES.\n"
            "Example: In 47, the digit 4 is in the tens place (4 tens = 40) and 7 is in the ones place (7 ones).\n"
            "So 47 = 40 + 7. This is called the expanded form."),
    ]
    for _ in range(n_each):
        t = rng.randint(1, 9)
        o = rng.randint(0, 9)
        num = 10 * t + o
        out.append(item(2, "qa",
            f"Question: In the number {num}, how many tens and how many ones are there?\n"
            f"Answer: {num} has {t} tens and {o} ones, because {num} = {10 * t} + {o}."))
        out.append(item(2, "qa",
            f"Question: Write the expanded form of {num}.\n"
            f"Answer: {num} = {10 * t} + {o}."))
    out.append(item(3, "explanation",
        "Place value — hundreds, tens and ones.\n"
        "In a three-digit number: the first digit counts HUNDREDS, the second TENS and the third ONES.\n"
        "Example: 356 = 3 hundreds + 5 tens + 6 ones = 300 + 50 + 6.\n"
        "Moving a digit one place to the left makes it TEN times bigger. That is the power of place value."))
    for _ in range(3):
        h, t, o = rng.randint(1, 9), rng.randint(0, 9), rng.randint(0, 9)
        num = 100 * h + 10 * t + o
        out.append(item(3, "qa",
            f"Question: Write {num} in expanded form.\n"
            f"Answer: {num} = {100 * h} + {10 * t} + {o} "
            f"({h} hundreds, {t} tens and {o} ones)."))
    return out


def _add_sub_100(n_each: int = 18) -> list[dict]:
    out = []
    for _ in range(n_each):
        a = rng.randint(11, 89)
        b = rng.randint(5, 40)
        s = a + b
        if s > 100:
            continue
        out.append(item(2, "qa",
            f"Question: Add {a} + {b}.\n"
            f"Answer: Split into tens and ones: {a} = {a - a % 10} + {a % 10} and {b} = {b - b % 10} + {b % 10}. "
            f"Add the tens, add the ones, then combine: {a} + {b} = {s}."))
    for _ in range(2):
        a = rng.randint(15, 58)
        b = rng.randint(10, 41)
        if a + b > 99:
            continue
        out.append(item(2, "worked",
            f"Worked example — two-digit addition with carrying.\n"
            f"Find {a} + {b}.\n"
            f"Step 1: Write one number below the other, ones under ones, tens under tens.\n"
            f"Step 2: Add the ones column: {a % 10} + {b % 10} = {a % 10 + b % 10}.\n"
            f"Step 3: If that is 10 or more, write the ones digit below and carry 1 to the tens column.\n"
            f"Step 4: Add the tens column including any carried 1.\n"
            f"Final answer: {a} + {b} = {a + b}."))
    for _ in range(2):
        a = rng.randint(41, 99)
        b = rng.randint(12, a - 5)
        out.append(item(2, "worked",
            f"Worked example — two-digit subtraction with borrowing.\n"
            f"Find {a} - {b}.\n"
            f"Step 1: Ones column first: {a % 10} - {b % 10}. "
            f"{'We cannot take ' + str(b % 10) + ' from ' + str(a % 10) + ', so we borrow 1 ten (10 ones) from the tens column.' if a % 10 < b % 10 else 'This works directly.'}\n"
            f"Step 2: Subtract the ones, then the tens.\n"
            f"Final answer: {a} - {b} = {a - b}.\n"
            f"Check: {a - b} + {b} = {a}. Addition and subtraction are opposites — this is how we check our answer."))
    return out


def _multiplication_intro(n: int = 16) -> list[dict]:
    out = [
        item(2, "explanation",
            "Multiplication is fast adding of EQUAL groups.\n"
            "If there are 4 plates with 3 biscuits each, total biscuits = 3 + 3 + 3 + 3 = 12.\n"
            "Instead of adding four times we can multiply: 4 x 3 = 12.\n"
            "We read it as 'four times three equals twelve'."),
    ]
    for _ in range(n):
        groups = rng.randint(2, 6)
        per = rng.choice([2, 3, 4, 5])
        thing = rng.choice(_COUNTABLES)
        total = groups * per
        addition = " + ".join([str(per)] * groups)
        out.append(item(2, "worked",
            f"Worked example — {groups} plates have {per} {thing} each. How many {thing} in all?\n"
            f"Step 1: Write as repeated addition: {addition}.\n"
            f"Step 2: Add step by step: {total}.\n"
            f"Step 3: Same as multiplication: {groups} x {per} = {total}.\n"
            f"There are {total} {thing} in all."))
    tables = [(2, 2), (5, 5), (10, 10), (3, 3), (4, 4)]
    for table, mult in tables:
        facts = [f"{mult} x {i} = {mult * i}" for i in range(1, 11)]
        out.append(item(2, "exercise",
            f"The table of {table}.\n" + "\n".join(facts) +
            f"\nTip: the table of {table} {'jumps in steps of ' + str(table) + '.' if table != 10 else 'just puts a zero after the other number: 10 x 7 = 70.'}"))
        for i in rng.sample(range(1, 11), 6):
            out.append(item(2, "qa",
                f"Question: What is {table} x {i}?\nAnswer: {table} x {i} = {table * i}."))
    return out


def _money_time_measure_2() -> list[dict]:
    out = []
    for _ in range(3):
        price = rng.choice([5, 10, 15, 20, 25])
        count = rng.randint(2, 5)
        out.append(item(2, "qa",
            f"Question: One eraser costs {price} rupees. Ravi buys {count} erasers. How much money does he pay?\n"
            f"Answer: {price} x {count} = {price * count}. Ravi pays {price * count} rupees. "
            f"We write it as Rs. {price * count} (or ₹{price * count})."))
    for _ in range(2):
        given = rng.choice([50, 100])
        price = rng.randint(15, given - 10)
        out.append(item(2, "worked",
            f"Worked example — shopping change.\n"
            f"Meera has Rs. {given}. She buys a toy worth Rs. {price}. How much money comes back?\n"
            f"Step 1: Change = money given - price.\n"
            f"Step 2: {given} - {price} = {given - price}.\n"
            f"Meera gets Rs. {given - price} back. Always count your change before leaving the shop!"))
    out += [
        item(2, "explanation",
             "Telling time — the clock.\n"
             "The clock has a short hand (hours) and a long hand (minutes).\n"
             "When the long hand points to 12, we say 'o'clock': the short hand on 3 means 3 o'clock.\n"
             "When the long hand points to 6, thirty minutes have passed: the short hand between 3 and 4 "
             "with long hand on 6 means half past three."),
        item(2, "qa",
             "Question: If school starts at 8 o'clock in the morning and ends at 2 o'clock in the afternoon, how many hours do you spend in school?\n"
             "Answer: From 8 to 2 is 6 hours (8 to 12 is 4 hours, 12 to 2 is 2 hours; 4 + 2 = 6)."),
        item(2, "explanation",
             "Measuring length.\n"
             "We measure small things in centimetres (cm) with a ruler, like a pencil.\n"
             "Bigger lengths, like a room or a playground, are measured in metres (m).\n"
             "100 centimetres make 1 metre. Estimate first, then measure, and start measuring from zero on the ruler!"),
        item(2, "qa",
             "Question: A pencil is 12 cm and an eraser is 4 cm. How much longer is the pencil?\n"
             "Answer: 12 - 4 = 8. The pencil is 8 cm longer than the eraser."),
    ]
    return out


# ---------------------------------------------------------------------------
# Stage 3 — to 1000, tables/division, fractions, units, calendar, perimeter
# ---------------------------------------------------------------------------
def _add_sub_1000(n: int = 13) -> list[dict]:
    out = []
    for _ in range(n):
        a = rng.randint(120, 880)
        b = rng.randint(45, 300)
        out.append(item(3, "qa",
            f"Question: Add {a} + {b}.\n"
            f"Answer: Add ones, tens and hundreds one column at a time, carrying when a column reaches 10. "
            f"{a} + {b} = {a + b}."))
    for _ in range(n):
        a = rng.randint(320, 980)
        b = rng.randint(60, 300)
        out.append(item(3, "qa",
            f"Question: Subtract {a} - {b}.\n"
            f"Answer: Subtract ones first, then tens, then hundreds, borrowing from the next place when needed. "
            f"{a} - {b} = {a - b}."))
    out.append(item(3, "worked",
        "Worked example — a three-digit sum with carrying.\n"
        "Find 468 + 275.\n"
        "Step 1: Ones: 8 + 5 = 13. Write 3, carry 1.\n"
        "Step 2: Tens: 6 + 7 = 13, plus carried 1 = 14. Write 4, carry 1.\n"
        "Step 3: Hundreds: 4 + 2 = 6, plus carried 1 = 7.\n"
        "Answer: 468 + 275 = 743."))
    return out


def _division_items(n: int = 16) -> list[dict]:
    out = [
        item(3, "explanation",
             "Division is equal sharing or equal grouping.\n"
             "12 sweets shared equally among 3 friends: each friend gets 12 ÷ 3 = 4 sweets.\n"
             "Division undoes multiplication: because 3 x 4 = 12, we know 12 ÷ 3 = 4.\n"
             "The number being shared is the dividend, the number of groups is the divisor, "
             "and the answer is the quotient."),
    ]
    for _ in range(n):
        divisor = rng.randint(2, 9)
        quotient = rng.randint(2, 10)
        dividend = divisor * quotient
        thing = rng.choice(_COUNTABLES)
        out.append(item(3, "qa",
            f"Question: {dividend} {thing} are shared equally among {divisor} children. How many {thing} does each child get?\n"
            f"Answer: {dividend} ÷ {divisor} = {quotient}, because {divisor} x {quotient} = {dividend}. "
            f"Each child gets {quotient} {thing}."))
    for _ in range(2):
        table = rng.randint(2, 9)
        out.append(item(3, "exercise",
            f"Division practice with the table of {table}.\n"
            + "\n".join(f"{table * i} ÷ {table} = {i}" for i in rng.sample(range(1, 11), 5)) +
            "\nEvery division fact is a multiplication fact read backwards. Learn tables, and division becomes easy!"))
    return out


def _fractions_items() -> list[dict]:
    out = [
        item(3, "explanation",
             "Fractions — equal parts of a whole.\n"
             "When we cut a roti into 2 equal parts, each part is one-half, written 1/2.\n"
             "Cut into 3 equal parts: each part is one-third, 1/3. Cut into 4 equal parts: one-quarter, 1/4.\n"
             "The bottom number (denominator) tells how many equal parts the whole has. "
             "The top number (numerator) tells how many parts we took.\n"
             "Important: the parts must be EQUAL to call them fractions."),
        item(3, "qa",
             "Question: A cake is cut into 4 equal pieces and you eat 1 piece. What fraction did you eat?\n"
             "Answer: You ate 1 out of 4 equal parts, which is 1/4 (one-quarter). 3/4 of the cake is left."),
        item(3, "qa",
             "Question: Which is bigger: 1/2 or 1/4 of the same roti?\n"
             "Answer: 1/2 is bigger. The more pieces we cut a whole into, the smaller each piece becomes. "
             "Two quarters make one half: 1/2 = 2/4."),
        item(3, "worked",
             "Worked example — halves and doubles.\n"
             "Half of 12 mangoes: share 12 into 2 equal groups. 12 ÷ 2 = 6, so half of 12 is 6 mangoes.\n"
             "Double of 6 mangoes means 6 + 6 = 12. Half and double undo each other."),
    ]
    for _ in range(2):
        n = rng.randint(4, 20)
        if n % 2 == 0:
            out.append(item(3, "qa",
                f"Question: What is half of {n}?\nAnswer: Half of {n} is {n // 2}, because {n} ÷ 2 = {n // 2}."))
    out += [
        item(4, "explanation",
             "Equivalent fractions — different names for the same amount.\n"
             "1/2, 2/4, 3/6 and 4/8 all name the same quantity. If we cut every piece of a half "
             "again into two, we get two quarters — the amount of roti did not change, only the "
             "number of pieces.\nRule: multiply (or divide) the top AND bottom by the same number "
             "to get an equivalent fraction."),
        item(4, "qa",
             "Question: Write two fractions equivalent to 1/3.\n"
             "Answer: Multiply top and bottom by 2: 2/6. Multiply by 3: 3/9. So 1/3 = 2/6 = 3/9."),
        item(4, "worked",
             "Worked example — adding fractions with the SAME denominator.\n"
             "Add 1/5 + 2/5.\n"
             "Step 1: Denominators are the same (fifths), so we can add the numerators directly.\n"
             "Step 2: 1 + 2 = 3. Keep the denominator: 3/5.\n"
             "Answer: 1/5 + 2/5 = 3/5. (We NEVER add the denominators — 2/10 would be wrong!)\n"
             "Think: 1 fifth plus 2 fifths is 3 fifths, just like 1 mango + 2 mangoes is 3 mangoes."),
        item(4, "explanation",
             "Decimals — tenths.\n"
             "When one whole is cut into 10 equal parts, each part is one-tenth, written 1/10 or 0.1.\n"
             "Money uses decimals every day: 50 paise = 1/2 rupee = ₹0.50.\n"
             "1.5 means 1 whole and 5 tenths (one and a half). 2.3 means 2 wholes and 3 tenths."),
        item(4, "qa",
             "Question: Write 3/10 as a decimal.\nAnswer: 3/10 = 0.3 (three tenths)."),
        item(4, "qa",
             "Question: Which is more, 0.5 or 0.4?\nAnswer: 0.5 is more. 0.5 = 5 tenths and 0.4 = 4 tenths, and 5 tenths > 4 tenths."),
    ]
    return out


def _measure_calendar_geometry() -> list[dict]:
    out = [
        item(3, "explanation",
             "Units of measurement.\n"
             "Length: millimetres (mm) for tiny things, centimetres (cm) for pencils, "
             "metres (m) for rooms, kilometres (km) for distances between towns. 1 m = 100 cm, 1 km = 1000 m.\n"
             "Weight: grams (g) for light things like a biscuit, kilograms (kg) for heavy things like "
             "a watermelon. 1 kg = 1000 g.\n"
             "Capacity: millilitres (mL) for a spoon of medicine, litres (L) for buckets and bottles. 1 L = 1000 mL."),
        item(3, "qa",
             "Question: A bag weighs 2 kg and a book weighs 500 g. Which is heavier?\n"
             "Answer: Change to the same unit: 2 kg = 2000 g. 2000 g > 500 g, so the bag is heavier."),
        item(3, "qa",
             "Question: A water bottle holds 1 litre. A glass holds 250 mL. How many glasses fill the bottle?\n"
             "Answer: 1 litre = 1000 mL. 1000 ÷ 250 = 4. Four glasses fill the bottle."),
        item(3, "explanation",
             "The calendar.\n"
             "A year has 12 months and about 365 days. A week has 7 days: Monday, Tuesday, Wednesday, "
             "Thursday, Friday, Saturday, Sunday.\n"
             "Months with 31 days: January, March, May, July, August, October, December. "
             "Months with 30 days: April, June, September, November.\n"
             "February has 28 days, and 29 in a leap year."),
        item(3, "qa",
             "Question: If today is Wednesday, what day will it be the day after tomorrow?\n"
             "Answer: Tomorrow is Thursday, and the day after tomorrow is Friday."),
        item(3, "explanation",
             "Shapes and their sides.\n"
             "Triangle: 3 sides and 3 corners (vertices). Square: 4 equal sides, 4 corners. "
             "Rectangle: 4 sides, opposite sides equal. Circle: 0 corners, perfectly round.\n"
             "A corner is called a vertex, and many corners together are vertices."),
        item(3, "qa",
             "Question: How many sides and corners does a square have?\n"
             "Answer: A square has 4 sides and 4 corners (vertices). All its sides are equal in length."),
        item(3, "explanation",
             "Perimeter — the distance around a shape.\n"
             "Walk around the edge of a shape, adding every side: that total distance is the perimeter.\n"
             "For a rectangle: perimeter = 2 x (length + breadth).\n"
             "For a square: perimeter = 4 x side, because all 4 sides are equal."),
        item(3, "worked",
             "Worked example — perimeter of a rectangle.\n"
             "A garden is 6 m long and 4 m wide. Find its perimeter.\n"
             "Step 1: Add the sides: 6 + 4 + 6 + 4 = 20.\n"
             "Step 2: Or use the formula: 2 x (6 + 4) = 2 x 10 = 20.\n"
             "The perimeter of the garden is 20 m. Imagine an ant walking once around the garden — "
             "it walks 20 metres in total!"),
    ]
    for _ in range(2):
        side = rng.randint(3, 12)
        out.append(item(3, "qa",
            f"Question: Find the perimeter of a square with side {side} cm.\n"
            f"Answer: Perimeter of a square = 4 x side = 4 x {side} = {4 * side} cm."))
    return out


# ---------------------------------------------------------------------------
# Stage 4 — bigger numbers, factors/multiples, multi-step problems
# ---------------------------------------------------------------------------
def _big_numbers(n: int = 13) -> list[dict]:
    out = [
        item(4, "explanation",
             "Numbers up to 10,000.\n"
             "10 ones = 1 ten. 10 tens = 1 hundred. 10 hundreds = 1 thousand. 10 thousands = 1 ten-thousand.\n"
             "In 4,725: the 4 counts thousands, 7 counts hundreds, 2 counts tens and 5 counts ones.\n"
             "Reading big numbers in parts helps: 4,725 = four thousand seven hundred twenty-five."),
    ]
    for _ in range(n):
        th = rng.randint(1, 9)
        h = rng.randint(0, 9)
        t = rng.randint(0, 9)
        o = rng.randint(0, 9)
        num = th * 1000 + h * 100 + t * 10 + o
        out.append(item(4, "qa",
            f"Question: In the number {num:,}, which digit is in the hundreds place and what is its value?\n"
            f"Answer: The digit {h} is in the hundreds place, and its value is {h * 100}."))
    return out


def _mult_div_big(n: int = 13) -> list[dict]:
    out = []
    for _ in range(n):
        a = rng.randint(12, 49)
        b = rng.randint(3, 9)
        out.append(item(4, "worked",
            f"Worked example — {a} x {b}.\n"
            f"Step 1: Split {a} into tens and ones: {a} = {a - a % 10} + {a % 10}.\n"
            f"Step 2: Multiply each part: {b} x {a - a % 10} = {b * (a - a % 10)} and {b} x {a % 10} = {b * (a % 10)}.\n"
            f"Step 3: Add the two results: {b * (a - a % 10)} + {b * (a % 10)} = {a * b}.\n"
            f"Answer: {a} x {b} = {a * b}. Splitting big numbers into parts makes multiplication easy."))
    for _ in range(n):
        divisor = rng.randint(3, 9)
        quotient = rng.randint(10, 30)
        remainder = rng.randint(0, divisor - 1)
        dividend = divisor * quotient + remainder
        out.append(item(4, "qa",
            f"Question: Find {dividend} ÷ {divisor}. Write the remainder if any.\n"
            f"Answer: {divisor} x {quotient} = {divisor * quotient}, and {dividend} - {divisor * quotient} = {remainder}. "
            f"So {dividend} ÷ {divisor} = {quotient} remainder {remainder}."
            + (" The remainder is 0 — it divides exactly!" if remainder == 0 else f" The remainder {remainder} is left over.")))
    return out


def _factors_multiples(n: int = 6) -> list[dict]:
    out = [
        item(4, "explanation",
             "Factors and multiples.\n"
             "Factors of a number divide it EXACTLY (no remainder). Factors of 12 are 1, 2, 3, 4, 6 and 12, "
             "because 1x12, 2x6 and 3x4 all make 12.\n"
             "Multiples of a number are its times-table answers. Multiples of 4 are 4, 8, 12, 16, 20, ...\n"
             "Factors are FEW and FINISHED (they stop at the number); multiples go on forever."),
        item(4, "qa",
             "Question: What are the factors of 18?\n"
             "Answer: 1, 2, 3, 6, 9 and 18. Pairs that multiply to 18: 1x18, 2x9 and 3x6."),
        item(4, "qa",
             "Question: Write the first five multiples of 7.\n"
             "Answer: 7, 14, 21, 28, 35 (from the table of 7)."),
    ]
    for _ in range(n):
        num = rng.choice([20, 24, 30, 36, 40, 48])
        facts = sorted({i for i in range(1, num + 1) if num % i == 0})
        out.append(item(4, "exercise",
            f"Find all factors of {num}.\nTry pairs: 1 x {num}, 2 x {num // 2}, ... every pair that "
            f"multiplies to {num} gives two factors.\nAnswer: {', '.join(map(str, facts))}."))
    return out


def _word_problems(n: int = 8) -> list[dict]:
    """One- and two-step word problems. Randomised numbers, worked answers."""

    def marbles() -> tuple[int, str]:
        a, b = rng.randint(15, 60), rng.randint(6, 35)
        name = rng.choice(_NAMES)
        return 3, (
            f"Question: {name} has {a} marbles. Her friend gives {b} more. How many marbles now?\n"
            f"Answer: {a} + {b} = {a + b}. Now there are {a + b} marbles."
        )

    def laddoos() -> tuple[int, str]:
        kids, each = rng.randint(4, 8), rng.randint(3, 9)
        return 3, (
            f"Question: There are {kids * each} laddoos to share equally among {kids} children. "
            f"How many does each get?\n"
            f"Answer: {kids * each} \u00f7 {kids} = {each}. Each child gets {each} laddoos."
        )

    def notebooks() -> tuple[int, str]:
        price = rng.choice([15, 20, 25, 30])
        count = rng.randint(3, 6)
        given = 200
        name = rng.choice(_NAMES)
        return 4, (
            f"Question: {name} buys {count} notebooks at Rs. {price} each and gives Rs. {given} to "
            f"the shopkeeper. How much change does she get back?\n"
            f"Answer: Cost = {count} x {price} = {count * price}. "
            f"Change = {given} - {count * price} = {given - count * price} rupees."
        )

    def benches() -> tuple[int, str]:
        rows = rng.randint(8, 20)
        per = rng.choice([4, 5, 6])
        return 4, (
            f"Question: A hall has {rows} benches. Each bench seats {per} students. "
            f"How many students can sit?\n"
            f"Answer: {rows} x {per} = {rows * per}. {rows * per} students can sit in the hall."
        )

    def picnic_buses() -> tuple[int, str]:
        return 4, (
            "Question: 96 students go for a picnic. Each bus carries 30 students. "
            "How many buses are needed for everyone?\n"
            "Answer: 96 \u00f7 30 = 3 remainder 6. Three buses take 90 students, but 6 students "
            "are left, so one more bus is needed. Total buses = 4. "
            "(In real problems, the remainder matters!)"
        )

    def toffees() -> tuple[int, str]:
        a = rng.randint(80, 150)
        b, c = rng.randint(20, 45), rng.randint(15, 35)
        return 4, (
            f"Question: A shop had {a} toffees. {b} toffees were sold in the morning and {c} in "
            f"the evening. How many are left?\n"
            f"Answer: Sold total = {b} + {c} = {b + c}. Left = {a} - {b + c} = {a - b - c} toffees. "
            f"This is a two-step problem: first add, then subtract."
        )

    def apples() -> tuple[int, str]:
        per_day = rng.choice([35, 45, 60])
        days = rng.randint(5, 9)
        return 4, (
            f"Question: A farmer picks {per_day} apples every day. How many apples in {days} days?\n"
            f"Answer: {per_day} x {days} = {per_day * days} apples in {days} days."
        )

    def pens() -> tuple[int, str]:
        boxes = rng.randint(3, 6)
        per_box = rng.randint(10, 24)
        loose = rng.randint(5, 30)
        return 4, (
            f"Question: A teacher has {boxes} boxes with {per_box} pens each and {loose} extra "
            f"pens. How many pens altogether?\n"
            f"Answer: Pens in boxes = {boxes} x {per_box} = {boxes * per_box}. "
            f"Total = {boxes * per_box} + {loose} = {boxes * per_box + loose} pens."
        )

    base = [marbles, laddoos, notebooks, benches, picnic_buses, toffees, apples, pens]
    makers = (base * 5)[:n]
    rng.shuffle(makers)
    out = []
    for maker in makers:
        stage, text = maker()
        out.append(item(stage, "word_problem", text))
    return out


def _comparison_items(n: int = 7) -> list[dict]:
    out = []
    for _ in range(n):
        a, b = rng.randint(105, 999), rng.randint(105, 999)
        while a == b:
            b = rng.randint(105, 999)
        big, small = max(a, b), min(a, b)
        symbol = ">" if big == a else "<"
        out.append(item(3, "qa",
            f"Question: Compare {a} and {b} using > or <.\n"
            f"Answer: Compare hundreds first, then tens, then ones. {a} {symbol} {b}, "
            f"because {a} is {'more' if a > b else 'less'} than {b}."))
    return out


def _number_facts() -> list[dict]:
    """Number-bond drills: before/after/between, skip counting, missing
    addend, doubles and fact families. Classic Class 1-3 exercises with
    randomised numbers (dedup removes coincidental repeats)."""
    out = []

    def before_after(n: int = 10) -> None:
        for _ in range(n):
            x = rng.randint(2, 98)
            which = rng.choice(["before", "after"])
            if which == "before":
                out.append(item(1, "qa",
                    f"Question: Which number comes just before {x}?\n"
                    f"Answer: {x - 1} comes just before {x}, because we say ... {x - 1}, {x} ... while counting."))
            else:
                out.append(item(1, "qa",
                    f"Question: Which number comes just after {x}?\n"
                    f"Answer: {x + 1} comes just after {x}, because we say ... {x}, {x + 1} ... while counting."))

    def between(n: int = 8) -> None:
        for _ in range(n):
            a = rng.randint(1, 90)
            c = a + rng.choice([2, 2, 2, 10])
            out.append(item(2, "qa",
                f"Question: Which number comes between {a} and {c}?\n"
                f"Answer: {a + (c - a) // 2} comes between {a} and {c}, "
                f"because counting goes {a}, {a + (c - a) // 2}, {c}."))

    def skip_count(n: int = 8) -> None:
        for _ in range(n):
            step, start = rng.choice([(2, 2), (5, 5), (10, 10), (3, 3), (4, 4), (2, 47), (5, 65)])
            seq = [start + step * i for i in range(4)]
            out.append(item(2, "qa",
                f"Question: Skip count by {step}: {', '.join(map(str, seq))}, what comes next?\n"
                f"Answer: Keep adding {step}: {seq[-1]} + {step} = {seq[-1] + step}. "
                f"Skip counting is the same as the table of {step}."))

    def missing_addend(n: int = 10) -> None:
        for _ in range(n):
            total = rng.randint(6, 20)
            a = rng.randint(1, total - 1)
            out.append(item(2, "qa",
                f"Question: Find the missing number: {a} + ? = {total}\n"
                f"Answer: {total} - {a} = {total - a}. So the missing number is {total - a}, "
                f"because {a} + {total - a} = {total}. Missing-number problems are subtraction in disguise."))

    def doubles(n: int = 6) -> None:
        for _ in range(n):
            x = rng.randint(4, 60)
            out.append(item(2, "qa",
                f"Question: What is double {x}?\n"
                f"Answer: Double {x} means {x} + {x} = {2 * x}. And half of {2 * x} is {x}."))

    def fact_family(n: int = 6) -> None:
        for _ in range(n):
            a, b = rng.randint(2, 40), rng.randint(2, 40)
            s = a + b
            out.append(item(2, "exercise",
                f"Fact family for {a}, {b} and {s}:\n"
                f"{a} + {b} = {s}\n{b} + {a} = {s}\n{s} - {a} = {b}\n{s} - {b} = {a}\n"
                f"Four facts from one family! Addition and subtraction always travel together."))

    before_after(); between(); skip_count(); missing_addend(); doubles(); fact_family()
    return out


def _geometry_3d() -> list[dict]:
    """Class 3-4: solid shapes, faces/edges/vertices, and 2D vs 3D."""
    out = [
        item(3, "explanation",
             "Solid (3D) shapes.\n"
             "Flat shapes like squares and circles are 2D - they have only length and breadth. "
             "Solid shapes are 3D - they also have height (depth).\n"
             "A cube (like a dice) has 6 square faces, 12 edges and 8 corners (vertices). "
             "A cuboid (like a brick or a matchbox) also has 6 faces, but they are rectangles. "
             "A sphere (like a football) has no edges or corners at all. "
             "A cylinder (like a can) has 2 round faces and 1 curved surface. "
             "A cone (like a birthday cap) has 1 round face and a pointed tip."),
        item(3, "qa",
             "Question: How many faces, edges and corners does a dice (cube) have?\n"
             "Answer: A cube has 6 faces, 12 edges and 8 corners (vertices). Every face is a square."),
        item(4, "qa",
             "Question: What is the difference between a square and a cube?\n"
             "Answer: A square is a flat 2D shape with 4 equal sides. A cube is a solid 3D shape "
             "with 6 square faces - like a dice. Squares live on paper; cubes take up space."),
        item(4, "qa",
             "Question: Name a solid shape that can roll and one that cannot.\n"
             "Answer: A ball (sphere) and a can (cylinder) can roll. A brick (cuboid) and a dice "
             "(cube) cannot roll - they slide, because of their flat faces."),
        item(4, "worked",
             "Worked example - counting faces of everyday objects.\n"
             "Take a matchbox. Touch each flat surface: top, bottom, front, back, left side, "
             "right side. Count them: 6 faces. Each face is a rectangle. Now count the edges "
             "where two faces meet: 12 edges. Finally the pointy corners: 8 vertices. "
             "Exploring real objects is the best way to learn solid shapes."),
    ]
    return out


def build() -> list[dict]:
    out: list[dict] = []
    # stage 1
    out += _counting_exercises()
    out += _number_recognition()
    out += _add_sub_within_10()
    out += _shapes_items()
    out += _patterns_items()
    # stage 2
    out += _place_value_items()
    out += _add_sub_100()
    out += _multiplication_intro()
    out += _money_time_measure_2()
    out += _number_facts()
    # stage 3
    out += _add_sub_1000()
    out += _division_items()
    out += _fractions_items()
    out += _measure_calendar_geometry()
    out += _geometry_3d()
    out += _comparison_items()
    # stage 4
    out += _big_numbers()
    out += _mult_div_big()
    out += _factors_multiples()
    out += _word_problems(n=28)
    return out
