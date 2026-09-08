"""English foundation: vocabulary, spelling, grammar, tenses, sentences,
paragraphs, stories with comprehension, instructions and Q&A.

Class 1-4 progression: stage 1 = letters/sight words/simple sentences,
stage 2 = grammar basics/plural/verbs, stage 3 = tenses/paragraphs,
stage 4 = stronger comprehension/essay-style writing/explanations.
"""

from __future__ import annotations


def item(stage: int, kind: str, text: str) -> dict:
    return {"text": text, "category": "english", "stage": stage, "kind": kind}


# ---------------------------------------------------------------------------
# Vocabulary & spelling (with meaning + usage sentences)
# ---------------------------------------------------------------------------
_VOCAB = {
    1: [
        ("cat", "a small pet animal that says meow"),
        ("dog", "a loyal pet animal that barks"),
        ("sun", "the bright star that gives us light in the day"),
        ("ball", "a round toy we can throw and bounce"),
        ("milk", "a white drink that comes from cows and buffaloes"),
        ("tree", "a tall plant with a trunk and leaves"),
        ("book", "pages with words and pictures that we read"),
        ("fish", "an animal that lives in water and swims"),
        ("bird", "an animal with feathers and wings that can fly"),
        ("hat", "something we wear on our head"),
    ],
    2: [
        ("friend", "a person we like to play and talk with"),
        ("garden", "a place where we grow flowers and vegetables"),
        ("market", "a place where people buy and sell things"),
        ("weather", "what the sky and air are like — sunny, rainy or windy"),
        ("family", "parents, children and relatives who live together or stay close"),
        ("school", "the place where children go to learn"),
        ("happy", "feeling glad, like when we get a gift"),
        ("brave", "not afraid of things that scare others"),
        ("clean", "free of dirt; washed and tidy"),
        ("helpful", "ready to help other people"),
    ],
    3: [
        ("harvest", "to cut and collect the crops from the field"),
        ("journey", "a trip from one place to another"),
        ("rescue", "to save someone from danger"),
        ("fragile", "easily broken, like glass"),
        ("ancient", "very, very old — like ancient monuments"),
        ("generous", "happy to share what we have with others"),
        ("curious", "wanting to know and learn new things"),
        ("explore", "to travel and look for new things or places"),
        ("protect", "to keep someone or something safe"),
        ("grateful", "thanking someone from the heart"),
    ],
    4: [
        ("responsibility", "a duty we must do ourselves, like homework"),
        ("independent", "able to do things by ourselves"),
        ("pollution", "dirt and harmful things mixing into air, water or land"),
        ("nutrition", "the good things in food that keep the body healthy"),
        ("communication", "sharing news and feelings with others"),
        ("observation", "looking at something carefully to learn about it"),
        ("tradition", "a custom passed down in a family or community"),
        ("solution", "the answer that fixes a problem"),
        ("destination", "the place we are travelling to"),
        ("environment", "everything around us — air, water, land, plants, animals"),
    ],
}


def _vocab_items() -> list[dict]:
    out = []
    for stage, entries in _VOCAB.items():
        for word, meaning in entries:
            out.append(item(
                stage, "explanation",
                f"Word: {word}\nMeaning: {meaning}\n"
                f"Sentence: I can use the word '{word}' when I speak and write. "
                f"Example: This is what '{word}' means — {meaning}. "
                f"Try to use '{word}' in your own sentence today.",
            ))
            out.append(item(
                stage, "qa",
                f"Question: What does the word '{word}' mean?\n"
                f"Answer: '{word.capitalize()}' means {meaning}.",
            ))
    # Opposites and similar words (synonyms) by level.
    opposites = [
        (1, "big", "small"), (1, "hot", "cold"), (1, "day", "night"),
        (1, "up", "down"), (1, "open", "close"), (1, "fast", "slow"),
        (2, "happy", "sad"), (2, "loud", "quiet"), (2, "clean", "dirty"),
        (2, "early", "late"), (2, "full", "empty"), (2, "tall", "short"),
        (3, "ancient", "modern"), (3, "brave", "cowardly"), (3, "arrive", "depart"),
        (3, "accept", "refuse"), (3, "visible", "invisible"),
        (4, "temporary", "permanent"), (4, "abundant", "scarce"),
        (4, "expand", "shrink"), (4, "artificial", "natural"),
    ]
    for stage, a, b in opposites:
        out.append(item(
            stage, "qa",
            f"Question: What is the opposite of '{a}'?\nAnswer: The opposite of '{a}' is '{b}'.",
        ))
        out.append(item(
            stage, "qa",
            f"Question: What is the opposite of '{b}'?\nAnswer: The opposite of '{b}' is '{a}'.",
        ))
    synonyms = [
        (2, "happy", "glad"), (3, "smart", "clever"), (3, "begin", "start"),
        (4, "difficult", "hard"), (4, "help", "assist"),
    ]
    for stage, a, b in synonyms:
        out.append(item(
            stage, "qa",
            f"Question: What word means almost the same as '{a}'?\nAnswer: '{b.capitalize()}' means almost the same as '{a}'.",
        ))
    # Spelling drills.
    spell_sets = [
        (1, ["cat", "bat", "mat", "hat", "rat"], "the -at family"),
        (1, ["sun", "fun", "run", "bun"], "the -un family"),
        (2, ["cake", "lake", "make", "take"], "long 'a' with silent e"),
        (2, ["ship", "shop", "fish", "wish"], "the 'sh' sound"),
        (2, ["chin", "chair", "cheese", "march"], "the 'ch' sound"),
        (3, ["knife", "knee", "know", "knit"], "silent 'k'"),
        (3, ["hour", "honest"], "silent 'h'"),
        (4, ["believe", "receive"], "'ie' and 'ei' words"),
        (4, ["island", "answer", "wrong"], "silent letters"),
    ]
    for stage, words, pattern in spell_sets:
        wlist = ", ".join(words)
        out.append(item(
            stage, "exercise",
            f"Spelling practice — {pattern}.\nRead and learn to spell these words: {wlist}.\n"
            f"Cover the words, then try to write each one from memory. Check your spelling. "
            f"Practise the tricky ones three times.",
        ))
    return out


# ---------------------------------------------------------------------------
# Grammar: nouns, pronouns, verbs, adjectives, articles, plurals, prepositions
# ---------------------------------------------------------------------------
def _grammar_items() -> list[dict]:
    out = []
    grammar_notes = [
        (1, "nouns",
         "A noun is a naming word. It names a person, a place, an animal or a thing.\n"
         "Person: mother, teacher, Ravi. Place: school, park, India. Animal: cow, parrot.\n"
         "Thing: book, chair, ball.\nPractice: look around your room and name five nouns."),
        (2, "pronouns",
         "A pronoun takes the place of a noun. Instead of saying 'Ravi is kind. Ravi helps.' "
         "we say 'Ravi is kind. He helps.'\nI, we, you, he, she, it and they are pronouns.\n"
         "Example: Meera is my friend. She sits next to me in class."),
        (2, "verbs",
         "A verb is a doing word. It tells what someone or something does.\n"
         "Run, jump, eat, read, sing and sleep are verbs.\n"
         "Example: The dog barks. 'Barks' is the verb. Birds fly in the sky. 'Fly' is the verb."),
        (2, "adjectives",
         "An adjective describes a noun. It tells us more about a person, place or thing.\n"
         "Words like big, small, red, sweet, tall and soft are adjectives.\n"
         "Example: I have a red ball. 'Red' describes the ball. It is a sweet mango."),
        (3, "articles",
         "We use 'a' or 'an' before a single thing we mention first, and 'the' for something "
         "special or already known.\nUse 'an' before a, e, i, o, u sounds: an apple, an elephant, "
         "an umbrella.\nUse 'a' for other sounds: a ball, a cat, a school.\n"
         "Use 'the' when we know exactly which one: the sun, the Taj Mahal, my best friend the captain."),
        (3, "plurals",
         "Most nouns add -s to become many: one book, two books. Nouns ending in s, x, ch or sh "
         "add -es: bus-buses, box-boxes, bench-benches, dish-dishes.\n"
         "Some nouns change completely: man-men, woman-women, child-children, tooth-teeth, foot-feet.\n"
         "Some stay the same: one sheep, ten sheep; one deer, five deer."),
        (3, "prepositions",
         "Prepositions show where or when. In, on, under, behind, between, near and beside tell "
         "us the position.\nExample: The cat is under the table. The ball is in the box. "
         "The shop is near the school. The pen is on the book."),
        (4, "conjunctions",
         "Conjunctions join words or sentences. 'And' adds, 'but' shows a contrast, 'or' gives a "
         "choice, 'because' gives a reason.\nExample: I like apples and mangoes. "
         "He was tired but happy. Do you want juice or milk? We stayed inside because it was raining."),
        (4, "punctuation",
         "Every sentence ends with a full stop (.). Questions end with a question mark (?). "
         "Strong feelings end with an exclamation mark (!).\nNames, places, days and months start "
         "with capital letters.\nExample: My name is Anita. Where is my bag? What a lovely surprise!"),
        (4, "subject-verb-agreement",
         "The verb must match the subject. One person or thing takes a verb with -s or -es; "
         "many take the plain verb.\nExample: The bird sings. The birds sing. "
         "She reads a book. They read books. He goes to school. They go to school."),
    ]
    for stage, topic, note in grammar_notes:
        out.append(item(stage, "explanation", f"Grammar lesson — {topic}.\n{note}"))

    grammar_qa = [
        (1, "What is a noun? Give two examples.",
         "A noun is a naming word. Examples: 'teacher' and 'school' (also animals and things like 'cow' and 'book')."),
        (2, "In the sentence 'Meera sings a song', which word is the verb?",
         "The verb is 'sings' — it tells what Meera does."),
        (2, "Which word in 'the fluffy cat' is the adjective?",
         "'Fluffy' is the adjective; it describes the cat."),
        (3, "Correct the sentence: 'She go to school.'",
         "The correct sentence is 'She goes to school.' One person takes the verb with -s: goes."),
        (3, "Fill in the blank: I saw ___ elephant at the zoo. (a/an)",
         "We say 'an elephant' because 'elephant' begins with the vowel sound 'e'."),
        (3, "What is the plural of 'box'?",
         "The plural of 'box' is 'boxes'. Nouns ending in x add -es."),
        (3, "What is the plural of 'child'?",
         "The plural of 'child' is 'children'. It changes completely."),
        (4, "Correct the sentence: 'they is my friends'",
         "Correct: 'They are my friends.' 'They' is many people, so we use 'are'."),
        (4, "Join using a conjunction: 'It was raining. We played inside.'",
         "'It was raining, so/because of that we played inside.' Or with 'but' for contrast: 'It was raining, but we still played inside for a while.'"),
        (4, "Where does a question mark go? Add punctuation: 'Where is your book'",
         "'Where is your book?' — a question ends with a question mark."),
    ]
    for stage, q, a in grammar_qa:
        out.append(item(stage, "qa", f"Question: {q}\nAnswer: {a}"))

    # Corrections (learn to fix mistakes).
    corrections = [
        (2, "I has a pen.", "I have a pen."),
        (2, "He are my brother.", "He is my brother."),
        (3, "She don't like rain.", "She doesn't like rain."),
        (3, "The childs are playing.", "The children are playing."),
        (3, "I seen a rainbow.", "I saw a rainbow."),
        (4, "Me and him goes to the park.", "He and I go to the park."),
        (4, "Their going to Delhi tomorrow.", "They're going to Delhi tomorrow."),
        (4, "I did my homeworks.", "I did my homework."),
    ]
    for stage, wrong, right in corrections:
        out.append(item(
            stage, "correction",
            f"Correct the sentence: '{wrong}'\n"
            f"This sentence has a mistake. The correct sentence is: '{right}'\n"
            f"Remember this rule so the mistake does not come back.",
        ))
    return out


# ---------------------------------------------------------------------------
# Tenses + sentence formation
# ---------------------------------------------------------------------------
def _tense_items() -> list[dict]:
    out = [
        item(3, "explanation",
             "Grammar lesson — the three simple tenses.\n"
             "1. Present tense tells what happens now: I play in the park.\n"
             "2. Past tense tells what already happened: I played in the park yesterday.\n"
             "3. Future tense tells what will happen later: I will play in the park tomorrow.\n"
             "The action is the same; only the time changes."),
        item(3, "explanation",
             "Grammar lesson — present continuous tense.\n"
             "Use is/am/are + verb-ing to say what is happening right now.\n"
             "I am reading. She is writing. They are playing. We are eating lunch.\n"
             "Example: Look! The rain is falling. The children are making paper boats."),
        item(4, "explanation",
             "Grammar lesson — past continuous tense.\n"
             "Use was/were + verb-ing to say what was going on for some time in the past.\n"
             "I was studying when my friend called. They were playing when it started to rain.\n"
             "It sets the scene of a story: The sun was shining. The birds were singing."),
    ]
    tense_drills = [
        (3, "eat", "eats", "ate", "will eat"),
        (3, "play", "plays", "played", "will play"),
        (3, "write", "writes", "wrote", "will write"),
        (3, "go", "goes", "went", "will go"),
        (4, "bring", "brings", "brought", "will bring"),
        (4, "teach", "teaches", "taught", "will teach"),
        (4, "sing", "sings", "sang", "will sing"),
    ]
    for stage, base, present, past, future in tense_drills:
        out.append(item(
            stage, "exercise",
            f"Verb practice with '{base}' in three tenses.\n"
            f"Present: Every day, Ravi {present} with his friends.\n"
            f"Past: Yesterday, Ravi {past} with his friends.\n"
            f"Future: Tomorrow, Ravi {future} with his friends.\n"
            f"Notice how the verb changes with time: {present} -> {past} -> {future}.",
        ))
        out.append(item(
            stage, "qa",
            f"Question: What is the past tense of '{base}'?\nAnswer: The past tense of '{base}' is '{past}'.",
        ))
    sentence_tips = item(
        2, "explanation",
        "How to make a good sentence.\n"
        "A sentence needs three things: (1) a capital letter at the start, (2) a naming word and a "
        "doing word, (3) a full stop at the end.\n"
        "Start simple: 'The dog runs.' Then add details: 'The brown dog runs fast in the garden.'\n"
        "Read your sentence aloud. If it sounds complete, it is a sentence."
    )
    out.append(sentence_tips)
    for stage, subject, verb, place in [
        (1, "The cat", "drinks milk", "in the kitchen"),
        (1, "The bird", "sings", "on the tree"),
        (2, "My sister", "reads a story", "every night"),
        (2, "We", "plant seeds", "in the garden"),
        (3, "The farmer", "waters the crops", "in the morning"),
        (4, "My friend and I", "cleaned the classroom", "after school"),
    ]:
        out.append(item(
            stage, "example",
            f"Example sentence: '{subject} {verb} {place}.'\n"
            f"This sentence has a naming part ('{subject.lower()}'), a doing part ('{verb}') "
            f"and extra details ('{place}'). Try changing one part to make your own new sentence.",
        ))
    return out


# ---------------------------------------------------------------------------
# Paragraph writing + instructions + explanations
# ---------------------------------------------------------------------------
def _paragraph_items() -> list[dict]:
    out = [
        item(3, "explanation",
             "Writing lesson — how to write a paragraph.\n"
             "A paragraph is a group of sentences about ONE idea.\n"
             "1. Start with a topic sentence that tells the main idea.\n"
             "2. Add two or three sentences with details.\n"
             "3. End with a closing sentence.\n"
             "Keep the sentences in order and do not mix in other ideas."),
        item(3, "example",
             "Example paragraph — My School.\n"
             "My school is a happy place. It has big classrooms, a library and a playground. "
             "My teacher teaches us new things every day with patience. During the lunch break, "
             "I play with my friends under the banyan tree. I learn something new at school every "
             "single day, and that is why I love my school."),
        item(3, "example",
             "Example paragraph — My Favourite Season.\n"
             "My favourite season is winter. The weather is cool and pleasant, so I can play "
             "outside for a long time. I wear my warm jacket and drink hot milk in the morning. "
             "In January we fly kites on the terrace. Winter also brings fresh green peas and "
             "carrots, which I love to eat."),
        item(4, "example",
             "Example paragraph — Why We Should Save Water.\n"
             "Water is precious because we cannot live without it. We use it for drinking, cooking "
             "and washing, and farmers need it for crops. Yet many people waste water by leaving "
             "taps open. We should close taps properly, reuse water for plants, and repair leaking "
             "pipes. If everyone saves water today, there will be enough for tomorrow."),
        item(4, "example",
             "Example paragraph — My Best Friend.\n"
             "My best friend is kind and honest. When I forget my pencil, she lends me hers. "
             "When I feel sad, she tells me funny stories to make me smile. We study together and "
             "help each other with difficult sums. A good friend makes every day brighter, and I "
             "try to be a good friend to her too."),
    ]
    instructions_sets = [
        (1, "How to wash your hands.",
         ["Wet your hands with clean water.",
          "Take soap and make foam.",
          "Rub between the fingers and under the nails for twenty seconds.",
          "Wash off all the soap with water.",
          "Dry your hands with a clean towel."]),
        (2, "How to plant a seed.",
         ["Fill a small pot with soil.",
          "Make a hole about two fingers deep.",
          "Put the seed inside and cover it gently with soil.",
          "Sprinkle a little water every day.",
          "Keep the pot where it gets sunlight, and watch for the first small leaf."]),
        (3, "How to make a paper boat.",
         ["Take a rectangular sheet of paper.",
          "Fold it in half from top to bottom.",
          "Fold the top corners down to the middle crease.",
          "Fold the bottom strips up, one in front and one behind.",
          "Open the folded shape carefully and press the middle to form a boat."]),
        (4, "How to study for a test.",
         ["Make a list of all the topics in the test.",
          "Find your notes for each topic and read them once fully.",
          "Close the book and write down what you remember.",
          "Check what you missed and read those parts again.",
          "Practise a few questions from each topic, and sleep well the night before."]),
    ]
    for stage, title, steps in instructions_sets:
        steps_text = "\n".join(f"Step {i}: {s}" for i, s in enumerate(steps, 1))
        out.append(item(
            stage, "instructions",
            f"{title}\nFollow these steps in order:\n{steps_text}\n"
            "Instructions work best when we follow the steps in the same order, one by one.",
        ))
    explanations = [
        (2, "Why do we wear clothes?",
         "We wear clothes to protect our body from heat, cold, rain and dust. Clothes also keep us "
         "clean and modest. In summer we wear light cotton clothes because they let air pass. In "
         "winter we wear woollen clothes because they keep the body warm."),
        (3, "Why do we need food?",
         "Food gives our body energy to play, study and grow. Food also helps the body repair "
         "itself when we get a small cut or feel weak. That is why we should eat proper meals and "
         "not skip breakfast."),
        (4, "Why should we not talk to strangers or accept things from them?",
         "We do not know a stranger's name, home or intentions. For our own safety, we should never "
         "go anywhere with a stranger or accept gifts or food from them. If a stranger troubles us, "
         "we should immediately tell our parents or a teacher we trust."),
        (4, "How does a letter reach another city?",
         "We write the address clearly on the envelope and drop it in a post box. The post office "
         "collects the letters, sorts them city by city, and sends them by train or plane. Postmen "
         "in the other city deliver the letter to the address written on it."),
    ]
    for stage, q, a in explanations:
        out.append(item(stage, "qa", f"Question: {q}\nAnswer: {a}"))
    return out


# ---------------------------------------------------------------------------
# Short stories with comprehension questions
# ---------------------------------------------------------------------------
_STORIES = [
    (1, "The Thirsty Crow",
     "One hot summer day, a crow was very thirsty. He flew here and there looking for water. "
     "At last he found a pot with a little water at the bottom. His beak could not reach the water. "
     "Then the clever crow had an idea. He picked up small pebbles one by one and dropped them "
     "into the pot. The water rose to the top. The crow drank the water and flew away happily.",
     [("Why was the crow thirsty?", "It was a very hot summer day and the crow had no water to drink."),
      ("How did the crow get the water?", "It dropped small pebbles into the pot one by one, which made the water rise to the top."),
      ("What does this story teach us?", "Thinking calmly and working step by step solves problems. Where there is a will, there is a way.")]),
    (1, "The Lion and the Mouse",
     "A lion was sleeping when a little mouse ran over his paw. The lion caught the mouse. "
     "'Please let me go,' said the mouse. 'One day I may help you.' The lion laughed but let him go. "
     "Some days later, the lion was caught in a hunter's net. He roared loudly. The mouse heard him, "
     "came quickly, and nibbled the ropes until the lion was free. 'You laughed at me once,' said the "
     "mouse, 'but today even a small friend can be a big help.'",
     [("Who caught the lion?", "A hunter's net caught the lion."),
      ("How did the mouse help the lion?", "The mouse nibbled and cut the ropes of the net until the lion became free."),
      ("What do we learn from this story?", "Even small friends can be a big help, so we should be kind to everyone.")]),
    (2, "Meera and the Mango Tree",
     "Meera had planted a mango seed in her garden when she was in Class 1. Every morning she "
     "watered it. In the first year, only a tiny green sprout appeared. Meera's brother teased her, "
     "'Where is the mango?' But Meera did not stop watering the plant. In a few years, the sprout "
     "grew into a young tree with shady branches. One summer, the tree gave its first two mangoes. "
     "Meera shared one with her brother and kept one for herself. It was the sweetest mango she "
     "had ever eaten.",
     [("What did Meera plant?", "Meera planted a mango seed in her garden."),
      ("How long did Meera wait for the mangoes?", "She waited a few years while the sprout grew into a young tree."),
      ("Why was the mango the sweetest for Meera?", "Because she had grown it herself with patience and care every single day.")]),
    (2, "The Honest Woodcutter",
     "A poor woodcutter was cutting a tree near a river. His iron axe slipped from his hands and "
     "fell into the deep water. He sat on the bank and cried, because he could not buy another axe. "
     "The river god appeared and dove into the water. First he brought up a golden axe. 'Is this "
     "yours?' he asked. 'No,' said the woodcutter honestly. Then the god brought a silver axe, but "
     "the woodcutter again said no. At last the god brought up the old iron axe. 'That is mine!' "
     "said the woodcutter happily. The god was pleased with his honesty and gave him all three axes.",
     [("What fell into the river?", "The woodcutter's iron axe fell into the river."),
      ("What did the woodcutter say when he was shown the golden axe?", "He honestly said 'No, that is not mine.'"),
      ("What is this story teaching us?", "Honesty is the best policy, and honest people earn trust and respect.")]),
    (3, "The Ant and the Grasshopper",
     "All summer, the ants worked hard. They collected food grain by grain and stored it in their "
     "underground home. The grasshopper only sang and danced. 'Why work in this sunshine?' he "
     "laughed at the ants. Winter came. The ground was covered with cold frost. The ants stayed "
     "warm inside, eating their stored food. The grasshopper was hungry and cold, with nothing to "
     "eat. The kind ants shared a little food with him and said, 'Next time, work in summer so "
     "winter does not frighten you.'",
     [("What did the ants do all summer?", "The ants worked hard and stored food grain by grain for the winter."),
      ("What happened to the grasshopper in winter?", "He became hungry and cold because he had stored no food."),
      ("What does this story teach us?", "We should work and prepare today so that hard times tomorrow do not trouble us.")]),
    (3, "A Trip to the Village Fair",
     "The annual fair came to Ravi's village in November. Ravi went with his grandmother in the "
     "evening. First they saw the giant wheel turning slowly against the orange sky. Then "
     "Grandmother bought jaggery sweets and a clay whistle for Ravi. Ravi watched a puppet show "
     "that told the story of a brave king. Before going home, they bought bangles for Ravi's "
     "mother and a new spade for the garden. On the way back, Ravi held his grandmother's hand "
     "tightly and promised to visit the fair with her again next year.",
     [("When did the fair come to the village?", "The annual fair came in November."),
      ("What did Grandmother buy for Ravi?", "She bought jaggery sweets and a clay whistle for Ravi."),
      ("Whom did Ravi go with, and how did he feel?", "He went with his grandmother. He felt happy and safe holding her hand, and he promised to come again next year.")]),
    (4, "Kiran's Science Project",
     "Kiran's class was given a science project: grow a bean plant and keep a diary of its growth. "
     "Kiran placed a bean seed on wet cotton in a glass jar near the window. On the third day, the "
     "seed's coat split and a tiny white root came out. By the sixth day, a pale shoot bent upward. "
     "Kiran measured it with a ruler and wrote the height in her diary every day. She noticed that "
     "the shoot always bent towards the window. Her teacher explained that plants grow towards "
     "light because they need it to make food. Kiran got the first prize, but the best prize was "
     "watching life grow under her own careful eyes.",
     [("What was Kiran's science project?", "To grow a bean plant and keep a diary recording its growth every day."),
      ("What did Kiran notice about the shoot?", "The shoot always bent towards the window light."),
      ("Why did the plant bend towards the light?", "Plants grow towards light because they need it to make their food."),
      ("What does this story show about learning?", "Careful observation and patience teach us things that books alone cannot.")]),
    (4, "The Night Train",
     "Aarav was taking his first overnight train journey to his grandmother's town. The train "
     "whistled and slowly left the station at nine o'clock. Aarav watched the city lights slide "
     "past the window until his eyes grew heavy. In the morning, the window showed a different "
     "world: green fields, a winding river, and farmers waving as the train rushed by. When the "
     "train finally stopped, Grandmother was waiting on the platform with a warm smile and a box "
     "of laddoos. Aarav realised that the journey itself had been as wonderful as reaching the "
     "destination.",
     [("When did Aarav's train leave the station?", "The train left the station at nine o'clock at night."),
      ("What did Aarav see from the window in the morning?", "He saw green fields, a winding river, and farmers waving at the train."),
      ("Who was waiting at the station, and with what?", "His grandmother was waiting with a warm smile and a box of laddoos."),
      ("What did Aarav realise about journeys?", "The journey itself can be as wonderful as reaching the destination.")]),
]


def _story_items() -> list[dict]:
    out = []
    for stage, title, story, qas in _STORIES:
        qa_block = "\n".join(f"Q: {q}\nA: {a}" for q, a in qas)
        out.append(item(
            stage, "story",
            f"Story — {title}.\n{story}\n\nLet us think about the story:\n{qa_block}",
        ))
        # Also individual comprehension items so the pattern appears alone.
        for q, a in qas:
            out.append(item(
                stage, "comprehension",
                f"Read this part of the story '{title}': {story}\n"
                f"Question: {q}\nAnswer: {a}",
            ))
    return out


# ---------------------------------------------------------------------------
# Assemble
# ---------------------------------------------------------------------------
def build() -> list[dict]:
    return (
        _vocab_items()
        + _grammar_items()
        + _tense_items()
        + _paragraph_items()
        + _story_items()
        + _spelling_drills()
        + _opposite_synonym_drills()
        + _plural_verb_drills()
        + _article_sentence_drills()
        + _sentence_fix_drills()
        + _everyday_qa_expanded(n=190)
        + _passage_comprehension(instances_per_template=20)
        + _vocab_in_context(n=130)
        + _writing_prompts_expanded(n_per_bank=18)
        + _sequencing_drills(n=70)
        + _everyday_qa_extra()
        + _tense_drills_extra()
    )


# ===========================================================================
# Expanded parametric practice — foundation-training scale-up.
# ===========================================================================
import random as _random

_rng = _random.Random(20240502)

# --- word banks -------------------------------------------------------------
_NOUNS = ["dog", "cat", "bird", "fish", "horse", "cow", "goat", "rabbit",
          "apple", "mango", "banana", "orange", "grape", "tomato", "potato",
          "carrot", "tree", "flower", "leaf", "river", "mountain", "cloud",
          "rain", "sun", "moon", "star", "book", "pen", "pencil", "chair",
          "table", "door", "window", "ball", "kite", "drum", "bell", "cake",
          "bread", "milk", "water", "school", "garden", "market", "hospital",
          "road", "bridge", "train", "bus", "boat"]
_VERBS = ["run", "jump", "sing", "dance", "read", "write", "eat", "drink",
          "play", "sleep", "swim", "fly", "climb", "draw", "paint", "walk",
          "talk", "listen", "help", "wash", "cook", "plant", "water", "open",
          "close", "carry", "throw", "catch", "build", "share"]
_ADJ = ["big", "small", "tall", "short", "long", "fast", "slow", "hot", "cold",
        "sweet", "sour", "soft", "hard", "clean", "dirty", "happy", "sad",
        "brave", "kind", "strong", "bright", "dark", "heavy", "light", "new",
        "old", "young", "round", "sharp", "smooth"]
_OPPOSITES = [
    ("big", "small"), ("tall", "short"), ("long", "short"), ("fast", "slow"),
    ("hot", "cold"), ("sweet", "sour"), ("soft", "hard"), ("clean", "dirty"),
    ("happy", "sad"), ("brave", "afraid"), ("strong", "weak"), ("bright", "dark"),
    ("heavy", "light"), ("new", "old"), ("young", "old"), ("open", "close"),
    ("day", "night"), ("up", "down"), ("in", "out"), ("over", "under"),
    ("early", "late"), ("full", "empty"), ("wet", "dry"), ("thick", "thin"),
    ("wide", "narrow"), ("high", "low"), ("loud", "quiet"), ("rich", "poor"),
    ("smooth", "rough"), ("first", "last"), ("come", "go"), ("give", "take"),
    ("push", "pull"), ("win", "lose"), ("start", "finish"), ("above", "below"),
    ("inside", "outside"), ("more", "less"), ("near", "far"), ("warm", "cool"),
]
_SYNONYMS = [
    ("happy", ["glad", "joyful", "cheerful"]),
    ("sad", ["unhappy", "sorrowful"]),
    ("big", ["large", "huge", "giant"]),
    ("small", ["little", "tiny"]),
    ("fast", ["quick", "speedy"]),
    ("smart", ["clever", "intelligent"]),
    ("pretty", ["beautiful", "lovely"]),
    ("scared", ["afraid", "frightened"]),
    ("tired", ["sleepy", "exhausted"]),
    ("angry", ["mad", "cross"]),
    ("look", ["see", "watch", "peek"]),
    ("shout", ["yell", "scream"]),
    ("help", ["assist", "aid"]),
    ("begin", ["start", "begin"]),
    ("end", ["finish", "stop"]),
    ("gift", ["present"]),
    ("kid", ["child"]),
    ("house", ["home"]),
    ("ill", ["sick", "unwell"]),
    ("brave", ["bold", "fearless"]),
]
_PLURALS = [
    ("cat", "cats"), ("dog", "dogs"), ("book", "books"), ("pen", "pens"),
    ("apple", "apples"), ("bus", "buses"), ("box", "boxes"), ("bench", "benches"),
    ("glass", "glasses"), ("baby", "babies"), ("city", "cities"), ("story", "stories"),
    ("leaf", "leaves"), ("knife", "knives"), ("wolf", "wolves"), ("life", "lives"),
    ("man", "men"), ("woman", "women"), ("child", "children"), ("foot", "feet"),
    ("tooth", "teeth"), ("mouse", "mice"), ("goose", "geese"), ("fish", "fish"),
    ("sheep", "sheep"), ("deer", "deer"), ("ox", "oxen"), ("person", "people"),
]
_ANIMAL_YOUNG = [("dog", "puppy"), ("cat", "kitten"), ("cow", "calf"),
                 ("horse", "foal"), ("sheep", "lamb"), ("goat", "kid"),
                 ("hen", "chick"), ("duck", "duckling"), ("frog", "tadpole"),
                 ("lion", "cub"), ("tiger", "cub"), ("bear", "cub"),
                 ("elephant", "calf"), ("pig", "piglet"), ("butterfly", "caterpillar")]
_ANIMAL_HOMES = [("dog", "kennel"), ("bird", "nest"), ("horse", "stable"),
                 ("cow", "shed"), ("lion", "den"), ("rabbit", "burrow"),
                 ("bee", "hive"), ("spider", "web"), ("ant", "anthill"),
                 ("pig", "sty"), ("hen", "coop"), ("fish", "aquarium")]
_ANIMAL_SOUNDS = [("dog", "barks"), ("cat", "meows"), ("cow", "moos"),
                  ("horse", "neighs"), ("lion", "roars"), ("sheep", "bleats"),
                  ("duck", "quacks"), ("hen", "clucks"), ("snake", "hisses"),
                  ("elephant", "trumpets"), ("frog", "croaks"), ("bee", "buzzes")]
_ONE_WORD_FOR = [
    ("a place where we learn", "school"), ("a place where we treat sick people", "hospital"),
    ("a place where we borrow books", "library"), ("a place where we buy medicines", "pharmacy"),
    ("a person who grows crops", "farmer"), ("a person who treats patients", "doctor"),
    ("a person who teaches students", "teacher"), ("a baby dog", "puppy"),
    ("a baby cat", "kitten"), ("a baby cow", "calf"), ("a group of sheep", "flock"),
    ("a group of lions", "pride"), ("a group of fish", "school"),
    ("a group of birds", "flock"), ("water falling from clouds", "rain"),
    ("the star that gives us light in the day", "sun"),
    ("a place where we keep our money safe", "bank"),
    ("a person who brings us letters", "postman"),
    ("a vehicle that runs on rails", "train"),
    ("a room where we cook food", "kitchen"),
]
_SPELL_WORDS = {
    1: ["cat", "dog", "sun", "hat", "bat", "cup", "bus", "pen", "bag", "bed",
        "fish", "bird", "book", "tree", "star", "milk", "hand", "feet", "nose", "cake"],
    2: ["garden", "friend", "school", "family", "animal", "morning", "evening",
        "yellow", "little", "water", "flower", "monkey", "rabbit", "pencil", "summer", "winter"],
    3: ["beautiful", "birthday", "calendar", "delicious", "elephant", "favourite",
        "grateful", "hospital", "important", "knowledge", "language", "mountain",
        "national", "picture", "question", "remember", "sandwich", "umbrella"],
    4: ["adventure", "beautiful", "celebrate", "community", "curious", "environment",
        "experiment", "gratitude", "hurricane", "imagination", "independent", "observatory",
        "patience", "probability", "responsible", "temperature", "tradition", "wonderful"],
}


def _qa(stage: int, kind: str, q: str, a: str) -> dict:
    return item(stage, kind, f"Question: {q}\nAnswer: {a}")


def _spelling_drills(n: int = 80) -> list[dict]:
    out = []
    for _ in range(n):
        stage = _rng.choice([1, 2, 3, 4])
        word = _rng.choice(_SPELL_WORDS[stage])
        letters = " - ".join(list(word))
        style = _rng.randrange(3)
        if style == 0:
            out.append(_qa(stage, "exercise", f"How do you spell the word '{word}'?",
                           f"The word '{word}' is spelled {letters}."))
        elif style == 1:
            missing = _rng.randrange(len(word))
            blanked = word[:missing] + "_" + word[missing + 1:]
            out.append(_qa(stage, "exercise",
                           f"Fill the missing letter: {blanked} (hint: it means what '{word}' means).",
                           f"The missing letter is '{word[missing]}'. The word is '{word}'."))
        else:
            out.append(_qa(stage, "exercise", f"Write the word '{word}' using capital letters.",
                           f"'{word}' in capital letters is {word.upper()}."))
    return out


def _opposite_synonym_drills(n: int = 140) -> list[dict]:
    out = []
    for _ in range(n):
        style = _rng.randrange(3)
        if style == 0:
            w, opp = _rng.choice(_OPPOSITES)
            flip = _rng.random() < 0.5
            a, b = (w, opp) if not flip else (opp, w)
            out.append(_qa(_rng.choice([1, 2, 3]), "exercise",
                           f"What is the opposite of '{a}'?",
                           f"The opposite of '{a}' is '{b}'."))
        elif style == 1:
            w, syns = _rng.choice(_SYNONYMS)
            s = _rng.choice(syns)
            out.append(_qa(_rng.choice([2, 3, 4]), "exercise",
                           f"What is a synonym for '{w}'? Give a word that means the same.",
                           f"A word that means the same as '{w}' is '{s}'."))
        else:
            thing, group = _rng.choice(_ONE_WORD_FOR)
            out.append(_qa(_rng.choice([2, 3, 4]), "exercise",
                           f"What one word means: {thing}?",
                           f"One word for '{thing}' is '{group}'."))
    return out


def _plural_verb_drills(n: int = 140) -> list[dict]:
    out = []
    for _ in range(n):
        style = _rng.randrange(4)
        if style == 0:
            s, p = _rng.choice(_PLURALS)
            out.append(_qa(_rng.choice([1, 2, 3]), "exercise",
                           f"What is the plural of '{s}'?",
                           f"The plural of '{s}' is '{p}'."))
        elif style == 1:
            s, p = _rng.choice(_PLURALS)
            flip = _rng.random() < 0.5
            one, many = (s, p) if not flip else (p, s)
            verb1, verb2 = ("is", "are") if not flip else ("are", "is")
            out.append(_qa(_rng.choice([1, 2]), "exercise",
                           f"Fill in the blank with 'is' or 'are': This {one} red. These {many} red.",
                           f"This {one} is red. These {many} are red. We use 'is' for one thing and 'are' for many."))
        elif style == 2:
            name = _rng.choice(["Ravi", "Meera", "Anita", "Sameer", "Priya", "Vikram", "Sunita", "Amit"])
            verb = _rng.choice(["play", "read", "sing", "run", "eat", "walk"])
            out.append(_qa(rng_stage := _rng.choice([1, 2]), "exercise",
                           f"Fill in the blank with the correct verb form: {name} ____ (play/read/sing/run) cricket every day. Use '{verb}' with 's'.",
                           f"{name} {verb}s cricket every day. With he, she or a name, we add 's' to the verb."))
        else:
            a = _rng.choice(["I", "You", "We", "They"])
            b = _rng.choice(["He", "She", "It"])
            verb = _rng.choice(["have", "has"])
            out.append(_qa(2, "exercise",
                           f"Fill in the blank with 'have' or 'has': {a} ____ a new book. {b} ____ a new bag.",
                           f"{a} {'have' if a != 'He' and a != 'She' and a != 'It' else 'has'} a new book. "
                           f"{b} has a new bag. Use 'has' with he, she and it."))
    return out


def _article_sentence_drills(n: int = 120) -> list[dict]:
    vowel = "aeiou"
    out = []
    for _ in range(n):
        style = _rng.randrange(3)
        if style == 0:
            w = _rng.choice(_NOUNS)
            art = "an" if w[0] in vowel else "a"
            out.append(_qa(_rng.choice([1, 2]), "exercise",
                           f"Fill in the blank with 'a' or 'an': I see ____ {w}.",
                           f"I see {art} {w}. We use 'an' before a vowel sound and 'a' before a consonant sound."))
        elif style == 1:
            w = _rng.choice(_ADJ + _NOUNS)
            out.append(_qa(_rng.choice([1, 2]), "exercise",
                           f"Fill in the missing letters with 'this' or 'these': ____ is a {w}. (one thing near us)",
                           f"This is a {w}. We say 'this' for one thing and 'these' for many things."))
        else:
            subj = _rng.choice(["The sun", "A bird", "My mother", "The dog", "The baby", "My friend"])
            adv = _rng.choice(["brightly", "sweetly", "quickly", "slowly", "happily", "loudly"])
            out.append(item(_rng.choice([1, 2, 3]), "exercise",
                            f"Question: Make a sentence using '{subj.lower()}' and the word '{adv}'.\n"
                            f"Answer: {subj} { _rng.choice(['shines', 'sings', 'runs', 'moves', 'smiles', 'calls']) } {adv}."))
    return out


def _sentence_fix_drills(n: int = 110) -> list[dict]:
    names = ["rahul", "meera", "arjun", "sita", "aman", "naina"]
    cities = ["delhi", "mumbai", "chennai", "kolkata", "pune", "jaipur"]
    months = ["january", "june", "march", "august", "october", "december"]
    out = []
    for _ in range(n):
        style = _rng.randrange(4)
        if style == 0:  # capitalization
            name = _rng.choice(names); city = _rng.choice(cities)
            wrong = f"{name} lives in {city}."
            out.append(_qa(2, "correction",
                           f"Rewrite this sentence correctly: {wrong}",
                           f"{name.capitalize()} lives in {city.capitalize()}. Names of people and places start with a capital letter."))
        elif style == 1:
            month = _rng.choice(months)
            wrong = f"my birthday is in {month}."
            out.append(_qa(_rng.choice([2, 3]), "correction",
                           f"Rewrite this sentence correctly: {wrong}",
                           f"My birthday is in {month.capitalize()}. A sentence starts with a capital letter, and months also start with one."))
        elif style == 2:  # verb agreement
            sub = _rng.choice([("The birds", "is", "are"), ("My father", "are", "is"),
                               ("The children", "plays", "play"), ("She", "go", "goes"),
                               ("They", "was", "were"), ("The dog", "bite", "bites")])
            out.append(_qa(_rng.choice([2, 3]), "correction",
                           f"Correct the verb in this sentence: {sub[0]} {sub[1]} in the garden.",
                           f"{sub[0]} {sub[2]} in the garden."))
        else:  # jumbled words
            s, p = _rng.choice(_PLURALS)
            art = "an" if s[0] in "aeiou" else "a"
            words = [f"This", f"is", art, "red", s + "."]
            _rng.shuffle(words)
            words_j = " / ".join(words)
            out.append(_qa(_rng.choice([1, 2]), "exercise",
                           f"Arrange the words to make a correct sentence: {words_j}",
                           f"This is {art} red {s}." if art == "a" else f"This is {art} red {s}."))
    return out


def _everyday_qa_expanded(n: int = 110) -> list[dict]:
    bank = [
        ("Where do we buy medicines?", "We buy medicines at a medical store or a pharmacy."),
        ("Where do we post letters?", "We post letters at the post office."),
        ("Where do we go when we are sick?", "We go to a doctor or a hospital when we are sick."),
        ("Where do we borrow books?", "We borrow books from a library."),
        ("Where do children learn?", "Children learn at school."),
        ("Who teaches you in class?", "Our teacher teaches us in class."),
        ("Who catches thieves?", "Police officers catch thieves."),
        ("Who brings us letters and parcels?", "The postman brings us letters and parcels."),
        ("Who drives a bus?", "A bus driver drives a bus."),
        ("Who grows rice and wheat for us?", "Farmers grow rice and wheat for us."),
        ("What do we wear when it rains?", "We wear a raincoat and carry an umbrella when it rains."),
        ("What do we wear in winter?", "We wear warm clothes like sweaters and jackets in winter."),
        ("What do we eat to stay healthy?", "We eat fruits, vegetables, milk, eggs and other fresh food to stay healthy."),
        ("What should we do before eating?", "We should wash our hands with soap before eating."),
        ("What should we say when we get something?", "We should say 'thank you' when we get something."),
        ("What should we say if we hurt someone?", "We should say 'sorry' if we hurt someone."),
        ("How many colours are there in a rainbow?", "There are seven colours in a rainbow."),
        ("Which fruit keeps the doctor away, as the saying goes?", "An apple — the saying goes, 'an apple a day keeps the doctor away'."),
        ("Which meal do we have in the morning?", "We have breakfast in the morning."),
        ("Where does the sun rise?", "The sun rises in the east."),
        ("Where does the sun set?", "The sun sets in the west."),
        ("What comes after Monday?", "Tuesday comes after Monday."),
        ("What comes after Saturday?", "Sunday comes after Saturday."),
        ("How many days are there in a week?", "There are seven days in a week."),
        ("How many months are there in a year?", "There are twelve months in a year."),
        ("Which is the first month of the year?", "January is the first month of the year."),
        ("What do we use to tell time?", "We use a clock or a watch to tell time."),
        ("What do we drink that cows give us?", "We drink milk, which cows give us."),
        ("What covers our body and protects it?", "Our skin covers our body and protects it."),
        ("What do we call water when it freezes?", "We call frozen water ice."),
        ("What do we call water when it boils and rises?", "We call it steam or water vapour."),
        ("Which animal is called the ship of the desert?", "The camel is called the ship of the desert."),
        ("Which is the biggest animal on land?", "The elephant is the biggest animal on land."),
        ("Which bird cannot fly but swims very well?", "The penguin cannot fly but swims very well."),
        ("Which animal has a long trunk?", "The elephant has a long trunk."),
        ("Where do fish live?", "Fish live in water — rivers, lakes, ponds and the sea."),
        ("What do bees make?", "Bees make honey."),
        ("What do we get from hens?", "We get eggs from hens."),
        ("What colour is grass?", "Grass is green."),
        ("What shines in the night sky?", "The moon and the stars shine in the night sky."),
        ("What do we use an umbrella for?", "We use an umbrella to stay dry in rain and to shade ourselves from the sun."),
        ("How do we cross a road safely?", "We cross at the zebra crossing, look left-right-left, and walk when the road is clear."),
        ("Why should we not talk while eating?", "Talking while eating can make us choke, so we should eat quietly."),
        ("What should we do with waste?", "We should put waste in the dustbin and keep our surroundings clean."),
        ("What part of the plant is under the ground?", "The roots of a plant are under the ground."),
        ("What do plants need to grow?", "Plants need sunlight, water, air and soil to grow."),
        ("What do we call the place where we live?", "The place where we live is called our home."),
        ("What do you call your mother's father?", "My mother's father is my grandfather (nana)."),
        ("How many seasons do we have in India?", "India mainly has summer, winter, monsoon (rainy season) and spring."),
        ("What do we use to cut paper?", "We use scissors to cut paper."),
        ("What do we use to write on a blackboard?", "We use chalk to write on a blackboard."),
    ]
    out = []
    for _ in range(n):
        q, a = _rng.choice(bank)
        out.append(_qa(_rng.choice([1, 1, 2, 2, 3]), "qa", q, a))
    return out


# ---------------------------------------------------------------------------
# Parametric reading-comprehension passage factory.
#
# Each template fills a fresh set of slots (names, numbers, objects) and
# derives consistent questions from the SAME slots, so every passage is a
# new, factually-consistent reading exercise.
# ---------------------------------------------------------------------------
_FRUITS = ["mangoes", "bananas", "apples", "oranges", "guavas", "chikoos", "pears", "peaches"]
_BIRDS = ["sparrows", "pigeons", "parrots", "mynahs", "crows", "kingfishers", "ducks"]
_TOYS = ["a red ball", "a blue kite", "a wooden drum", "a toy train", "a soft teddy",
         "a spinning top", "a rainbow slinky", "a frisbee"]
_PLACES_TRIP = ["a dairy farm", "a botanical garden", "a science museum", "a bird sanctuary",
                "a pottery village", "a butterfly park", "an old fort", "a riverside village"]
_SNACKS = ["samosas", "sandwiches", "pakoras", "idlis", "parathas", "banana chips"]
_GAMES = ["kho-kho", "hide and seek", "tag", "carrom", "ludo", "snakes and ladders", "skipping rope"]


def _names2():
    a = _rng.choice(["Aarav", "Diya", "Kabir", "Meera", "Rohan", "Naina", "Aditi", "Ishaan", "Tara", "Manav"])
    b = _rng.choice(["Riya", "Vivaan", "Anaya", "Yash", "Simran", "Nikhil", "Pooja", "Kavya"])
    while b == a:
        b = _rng.choice(["Riya", "Vivaan", "Anaya", "Yash", "Simran", "Nikhil", "Pooja", "Kavya"])
    return a, b


def _tp_park():
    a, b = _names2()
    bird = _rng.choice(_BIRDS)
    n_bird = _rng.randint(3, 12)
    fruit = _rng.choice(_FRUITS)
    n_fruit = _rng.randint(2, 6)
    game = _rng.choice(_GAMES)
    h = _rng.randint(4, 6)
    story = (f"Last Sunday, {a} and {b} went to the park near their house. They saw {n_bird} {bird} "
             f"near the pond. Under a big banyan tree they shared {n_fruit} {fruit}. Then they played "
             f"{game} with their friends until {h} o'clock. While coming home, they picked up all the "
             f"wrappers and threw them in the dustbin to keep the park clean.")
    qas = [
        (f"Where did {a} and {b} go last Sunday?", "They went to the park near their house."),
        (f"How many {bird} did they see near the pond?", f"They saw {n_bird} {bird} near the pond."),
        (f"What did they share under the banyan tree?", f"They shared {n_fruit} {fruit} under the banyan tree."),
        (f"What did the children do to keep the park clean?",
         "They picked up the wrappers and threw them in the dustbin."),
    ]
    return 2, "A Day in the Park", story, qas


def _tp_market():
    a, b = _names2()
    f1, f2 = _rng.sample(_FRUITS, 2)
    p1 = _rng.randrange(20, 80, 5); p2 = _rng.randrange(15, 60, 5)
    paid = p1 + p2 + _rng.choice([10, 20, 50])
    kg = _rng.randint(1, 3)
    story = (f"On Saturday morning, {a} went to the market with "
             f"{'her' if a.endswith(('a', 'i', 'ya')) else 'his'} "
             f"grandmother. First they bought {kg} kg of {f1} for Rs {p1}. "
             f"Then they bought {f2} for Rs {p2}. At the counter, {a} paid Rs {paid}. The shopkeeper smiled and "
             f"gave back the correct change. On the way home they also bought a small bunch of coriander leaves.")
    qas = [
        ("Where did they go on Saturday morning?", "They went to the market."),
        (f"How much money did the {f1} cost?", f"The {f1} cost Rs {p1}."),
        (f"How much did {a} pay at the counter?", f"{a} paid Rs {paid} at the counter."),
        (f"What did the shopkeeper do after {a} paid?",
         f"The shopkeeper smiled and gave back the correct change of Rs {paid - p1 - p2}."),
    ]
    return 3, "A Trip to the Market", story, qas


def _tp_birthday():
    a, b = _names2()
    age = _rng.randint(6, 11)
    guests = _rng.choice([6, 8, 10, 12, 15])
    toy = _rng.choice(_TOYS)
    cake = _rng.choice(["chocolate", "vanilla", "butterscotch", "strawberry"])
    story = (f"Yesterday was {a}'s birthday. {a} turned {age} years old. In the evening, {guests} friends came "
             f"to the party. Everyone played games in the garden. {b} gifted {a} {toy}. Then everyone sang "
             f"'Happy Birthday' and {a} cut a {cake} cake. {a}'s mother gave {('her' if a.endswith(('a','i','ya')) else 'him')} "
             f"the first piece, but {a} shared the cake with all the friends.")
    qas = [
        (f"How old is {a} now?", f"{a} is {age} years old now."),
        (f"How many friends came to the party?", f"{guests} friends came to the party."),
        (f"What did {b} gift {a}?", f"{b} gifted {a} {toy}."),
        (f"What flavour was the birthday cake?", f"The birthday cake was {cake}."),
    ]
    return 2, "The Birthday Party", story, qas


def _tp_trip():
    a, b = _names2()
    place = _rng.choice(_PLACES_TRIP)
    snack = _rng.choice(_SNACKS)
    n_draw = _rng.randint(2, 5)
    teacher = _rng.choice(["Miss Sharma", "Mr Iyer", "Miss Fernandes", "Mr Gupta", "Miss Rao"])
    story = (f"Last Friday, Class 3 went on a school trip to {place}. {teacher} counted all the children "
             f"before the bus started. On the way, the children sang songs. At {place}, they saw many new "
             f"things and {teacher} answered all their questions. During the lunch break, everyone shared "
             f"{snack}. {a} made {n_draw} drawings of the visit in the sketchbook. Before leaving, the "
             f"children thanked the guides and kept the place neat and clean.")
    qas = [
        (f"Where did Class 3 go on the school trip?", f"Class 3 went to {place}."),
        (f"Who counted the children before the bus started?", f"{teacher} counted all the children."),
        (f"What did the children share during the lunch break?", f"They shared {snack} during the lunch break."),
        (f"How many drawings did {a} make?", f"{a} made {n_draw} drawings of the visit."),
    ]
    return 3, "The School Trip", story, qas


def _tp_puppy():
    a, b = _names2()
    place = _rng.choice(["behind the school gate", "under a parked car", "near the bus stop",
                         "inside an old carton", "beside the garden wall"])
    name = _rng.choice(["Bruno", "Moti", "Sheru", "Ruby", "Golu", "Kalu"])
    food = _rng.choice(["bread and milk", "biscuits", "rice and curd"])
    days = _rng.randint(2, 7)
    story = (f"One rainy evening, {a} found a small puppy crying {place}. The puppy was wet and hungry. "
             f"{a} carried it home carefully. {a}'s family gave the puppy {food} and a warm basket to sleep in. "
             f"After {days} days, the puppy became strong and playful. {b} named the puppy {name}. "
             f"Now {name} wags its tail whenever it sees {a}, and they are the best of friends.")
    qas = [
        ("Where was the puppy found?", f"The puppy was found {place}."),
        (f"What did the family give the puppy to eat?", f"They gave the puppy {food}."),
        (f"Who named the puppy, and what was its name?", f"{b} named the puppy {name}."),
        ("How did the puppy show that it was happy and friendly?",
         f"{name} wagged its tail whenever it saw {a}."),
    ]
    return 3, "The Little Puppy", story, qas


def _tp_rainy():
    a, b = _names2()
    game = _rng.choice(_GAMES)
    n_boat = _rng.randint(2, 6)
    drink = _rng.choice(["hot milk", "warm soup", "ginger tea", "hot chocolate"])
    story = (f"It rained heavily all day on Monday, so {a} and {b} could not go out to play. First they "
             f"finished their homework. Then they played {game} indoors. After that, they made {n_boat} "
             f"paper boats and floated them in a tub of water. In the evening, they watched the rain from "
             f"the window and drank {drink}. {a} said that a rainy day at home can also be a happy day.")
    qas = [
        ("Why could the children not go out to play?", "They could not go out because it rained heavily all day."),
        ("What did the children do first?", "First they finished their homework."),
        (f"How many paper boats did they make?", f"They made {n_boat} paper boats."),
        ("What can we understand about {a}'s day?".replace("{a}", a),
         f"{a} felt that a rainy day at home can also be a happy day."),
    ]
    return 2, "A Rainy Day", story, qas


def _tp_garden():
    a, b = _names2()
    seed = _rng.choice(["tomato", "sunflower", "marigold", "coriander", "chilli", "pumpkin"])
    sprout = _rng.randint(4, 9)
    h0 = _rng.randint(2, 4); h1 = h0 + _rng.randint(2, 5)
    story = (f"In the school garden, {a} and {b} planted {seed} seeds in a small pot. Every morning they "
             f"sprinkled water on the soil and kept the pot in the sunlight. After {sprout} days, a tiny "
             f"green sprout came out of the soil. The children measured the little plant every week. "
             f"In the first week it was {h0} cm tall, and in the second week it grew to {h1} cm. "
             f"{teacher_name()} told them that plants need sunlight, water and air to grow strong.")
    qas = [
        ("What did the children plant in the pot?", f"They planted {seed} seeds in the pot."),
        (f"After how many days did the sprout come out?", f"The sprout came out after {sprout} days."),
        (f"How much did the plant grow from the first week to the second week?",
         f"It grew from {h0} cm to {h1} cm, so it grew {h1 - h0} cm more."),
        ("What three things do plants need to grow strong?",
         "Plants need sunlight, water and air to grow strong."),
    ]
    return 3, "The Little Gardeners", story, qas


def _tp_library():
    a, b = _names2()
    k1 = _rng.choice(["story books", "books about animals", "books about planets", "picture books",
                      "books about kings and queens", "rhyme books"])
    n_books = _rng.choice([2, 3, 4])
    day = _rng.choice(["Monday", "Wednesday", "Friday", "Saturday"])
    story = (f"Every {day}, {a} goes to the library near the market with {b}. The librarian, "
             f"{'Mrs Pillai' if _rng.random() < 0.5 else 'Mr D’Souza'}, helps them find good books. "
             f"This week {a} borrowed {n_books} {k1}. In the library everyone sits quietly and reads. "
             f"{a} returns each book on time and takes great care of it. Last month {a} read the most "
             f"books in the whole class and won a small bookmark as a prize.")
    qas = [
        (f"On which day does {a} go to the library?", f"{a} goes to the library every {day}."),
        (f"What did {a} borrow this week?", f"{a} borrowed {n_books} {k1} this week."),
        ("How do children behave in the library?", "In the library everyone sits quietly and reads."),
        (f"Why did {a} get a bookmark as a prize?",
         f"{a} got the bookmark because {('she' if a.endswith(('a','i','ya')) else 'he')} read the most books in the class last month."),
    ]
    return 3, "A Visit to the Library", story, qas


def _tp_match():
    a, b = _names2()
    t1, t2 = _rng.sample(["Blue Stars", "Red Roses", "Green Rockets", "Golden Lions", "White Tigers"], 2)
    s1 = _rng.randint(2, 9); s2 = _rng.randint(0, 9)
    while s1 == s2:
        s2 = _rng.randint(0, 9)
    win = t1 if s1 > s2 else t2
    story = (f"In the evening, {a} and {b} watched a friendly football match between {t1} and {t2} in the "
             f"ground near their colony. Both teams played very hard. By half time the score was "
             f"{max(s1, s2) - min(s1, s2) if False else s1}-{s2}. In the last minute, {t1 if win == t1 else t2} "
             f"scored the final goal. The match ended {s1}-{s2}, so {win} won the trophy. All the players "
             f"shook hands after the match and shared juice together.")
    qas = [
        ("Which two teams played the match?", f"{t1} and {t2} played the match."),
        (f"What was the final score?", f"The final score was {s1}-{s2}."),
        (f"Which team won the trophy?", f"{win} won the trophy."),
        ("What did the players do after the match?",
         "The players shook hands and shared juice together."),
    ]
    return 4, "The Big Match", story, qas


def teacher_name():
    return _rng.choice(["Miss Sharma", "Mr Iyer", "Mrs Bhatia", "Mr Gupta", "Miss Rao"])


_PASSAGE_TEMPLATES = [_tp_park, _tp_market, _tp_birthday, _tp_trip,
                      _tp_puppy, _tp_rainy, _tp_garden, _tp_library, _tp_match]


def _passage_comprehension(instances_per_template: int = 14) -> list[dict]:
    out = []
    for make in _PASSAGE_TEMPLATES:
        seen_stories = set()
        made = 0
        attempts = 0
        while made < instances_per_template and attempts < instances_per_template * 6:
            attempts += 1
            stage, title, story, qas = make()
            if story in seen_stories:
                continue
            seen_stories.add(story)
            made += 1
            # Multi-question block (paragraph comprehension practice).
            block = "\n".join(f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(qas))
            out.append(item(stage, "comprehension",
                            f"Read the passage '{title}' and answer the questions.\n{story}\n\n{block}"))
            # Exam-style single-question items with the same passage.
            for q, a in _rng.sample(qas, 2):
                out.append(item(stage, "comprehension",
                                f"Read the passage: {story}\nQuestion: {q}\nAnswer: {a}"))
        # vary instances per template deterministically
        _ = title  # keep linters calm
    return out


def _vocab_in_context(n: int = 90) -> list[dict]:
    frames = [
        ("{w}", "The old man gave away all his money. He was a {syn} person.", 4),
        ("{w}", "The {w} child shared her lunch with a hungry puppy.", 3),
        ("{w}", "Ria felt {w} when she saw her lost dog come home.", 2),
        ("{w}", "The {w} boy solved the difficult puzzle in two minutes.", 3),
    ]
    out = []
    for _ in range(n):
        w, syns = _rng.choice(_SYNONYMS)
        syn = _rng.choice(syns)
        q = f"In this sentence, what does the word mean: 'The {w} girl helped the old man cross the road.' What does '{w}' mean here?"
        out.append(_qa(_rng.choice([3, 4]), "exercise", q,
                       f"Here '{w}' means '{syn}'. A {w} person is kind and helpful to others."))
    return out


def _writing_prompts_expanded(n_per_bank: int = 12) -> list[dict]:
    topics = [
        ("my pet", ["My pet is a {adj} {animal}.", "It likes to {verb} all day.",
                    "I give it {food} every morning.", "We play together in the evening."]),
        ("my favourite fruit", ["My favourite fruit is the {fruit}.", "It is {adj} and juicy.",
                                "I eat it every day after school.", "It keeps me healthy and strong."]),
        ("my school bag", ["My school bag is {colour}.", "It has {n} pockets and two straps.",
                           "I keep my books, pencils and a water bottle in it.", "I carry it to school every day."]),
        ("the rainy day", ["It was raining since morning.", "I wore my raincoat and boots.",
                           "I sailed a paper boat in the water.", "Then I drank {drink} and read a storybook."]),
        ("my best friend", ["My best friend is {name}.", "We {verb} together every evening.",
                            "We always share our tiffin.", "A good friend makes every day happy."]),
        ("the market", ["The market is full of shops and people.", "We bought {fruit} and fresh vegetables.",
                        "The shopkeeper gave us a discount of five rupees.", "Then we came home by auto."]),
    ]
    colours = ["red", "blue", "green", "purple", "orange", "pink"]
    foods = ["milk and bread", "biscuits", "eggs", "fruits", "dog food"]
    out = []
    for _ in range(n_per_bank):
        topic, frames = _rng.choice(topics)
        vals = {"adj": _rng.choice(_ADJ), "animal": _rng.choice(["dog", "cat", "rabbit", "parrot"]),
                "verb": _rng.choice(_VERBS), "food": _rng.choice(foods),
                "fruit": _rng.choice(_FRUITS[:-1]).rstrip("s"), "colour": _rng.choice(colours),
                "n": _rng.randint(2, 4), "drink": _rng.choice(["hot milk", "warm soup", "hot chocolate"]),
                "name": _rng.choice(["Meera", "Ravi", "Aditi", "Kabir"])}
        sentences = [f.format(**vals).capitalize() for f in frames]
        ans = " ".join(sentences)
        out.append(item(_rng.choice([2, 3, 4]), "writing",
                        f"Question: Write four sentences about {topic}.\nAnswer: {ans}"))
    # letters / applications (fixed exemplars with slots already filled)
    letters = [
        (3, "Write a leave application to your teacher.",
         "To,\nThe Class Teacher,\nSunrise Public School.\n\nRespected Madam,\n"
         "I am {name} of Class 3-A. I had a fever yesterday, so I could not come to school. "
         "Kindly give me leave for one day.\n\nYour obedient student,\n{name}"),
        (4, "Write a letter to your friend inviting them to your birthday party.",
         "{date}\n\nDear {friend},\n"
         "How are you? My birthday falls on this Sunday at 5 o'clock in the evening. "
         "There will be games, cake and lots of fun. Please come to my house with Uncle and Aunty. "
         "We will cut the cake at 6 o'clock.\n\nYour loving friend,\n{name}"),
    ]
    for stage, q, a in letters:
        name = _rng.choice(["Ananya", "Karthik", "Zoya", "Rehan"])
        friend = _rng.choice(["Priya", "Sam", "Ira", "Dev"])
        a = a.replace("{name}", name).replace("{friend}", friend).replace("{date}", "12 March 2026")
        out.append(item(stage, "writing", f"Question: {q}\nAnswer: {a}"))
    return out


def _sequencing_drills(n: int = 45) -> list[dict]:
    routines = [
        ("the parts of the day in order", ["morning", "afternoon", "evening", "night"]),
        ("what you do to get ready for school", ["wake up", "brush your teeth", "take a bath", "wear the uniform", "eat breakfast"]),
        ("how a seed grows", ["put the seed in soil", "water it", "a sprout comes out", "leaves grow", "a plant grows"]),
        ("the life cycle of a butterfly", ["egg", "caterpillar", "pupa", "butterfly"]),
        ("making a sandwich", ["take two bread slices", "apply butter", "put the filling", "cover and cut it"]),
        ("the water cycle", ["water evaporates", "clouds form", "it rains", "water flows back to rivers"]),
    ]
    out = []
    for _ in range(n):
        title, steps = _rng.choice(routines)
        shuffled = steps[:]
        _rng.shuffle(shuffled)
        if shuffled == steps:
            shuffled = steps[::-1]
        out.append(_qa(_rng.choice([2, 3, 4]), "exercise",
                       f"Put these in the correct order ({title}): " + ", ".join(shuffled) + ".",
                       "The correct order is: " + ", ".join(f"{i + 1}) {s}" for i, s in enumerate(steps)) + "."))
    return out


# ---------------------------------------------------------------------------
# Bank extensions (append-style so originals stay untouched).
# ---------------------------------------------------------------------------
_OPPOSITES += [
    ("ascend", "descend"), ("arrive", "depart"), ("accept", "refuse"),
    ("ancient", "modern"), ("brave", "cowardly"), ("bright", "dull"),
    ("cheap", "costly"), ("crooked", "straight"), ("deep", "shallow"),
    ("empty", "full"), ("entrance", "exit"), ("expand", "shrink"),
    ("gentle", "harsh"), ("humble", "proud"), ("increase", "decrease"),
    ("kind", "cruel"), ("lazy", "hardworking"), ("major", "minor"),
    ("polite", "rude"), ("praise", "blame"), ("quiet", "noisy"),
    ("remember", "forget"), ("right", "left"), ("safe", "dangerous"),
    ("sour", "sweet"), ("success", "failure"), ("top", "bottom"),
    ("true", "false"), ("whole", "part"), ("wise", "foolish"),
]
_SYNONYMS += [
    ("brave", ["courageous", "bold"]), ("calm", ["peaceful", "quiet"]),
    ("cold", ["chilly", "freezing"]), ("curious", ["eager", "inquisitive"]),
    ("difficult", ["hard", "tough"]), ("enormous", ["huge", "massive"]),
    ("famous", ["well-known", "renowned"]), ("funny", ["amusing", "humorous"]),
    ("important", ["significant", "vital"]), ("neat", ["tidy", "clean"]),
    ("polite", ["courteous", "well-mannered"]), ("quick", ["fast", "rapid"]),
    ("right", ["correct", "accurate"]), ("strong", ["powerful", "sturdy"]),
    ("brave", ["fearless", "daring"]), ("unhappy", ["sad", "miserable"]),
    ("wise", ["clever", "sensible"]), ("wonderful", ["amazing", "marvelous"]),
]
_PLURALS += [
    ("hero", "heroes"), ("tomato", "tomatoes"), ("potato", "potatoes"),
    ("bus", "buses"), ("watch", "watches"), ("dish", "dishes"),
    ("church", "churches"), ("half", "halves"), ("shelf", "shelves"),
    ("thief", "thieves"), ("loaf", "loaves"), ("calf", "calves"),
    ("day", "days"), ("key", "keys"), ("monkey", "monkeys"),
    ("radio", "radios"), ("photo", "photos"), ("piano", "pianos"),
]
_ONE_WORD_FOR += [
    ("a person who flies an aeroplane", "pilot"),
    ("a person who stitches clothes", "tailor"),
    ("a person who makes furniture", "carpenter"),
    ("a place where we watch plays", "theatre"),
    ("a place where aeroplanes take off and land", "airport"),
    ("a place where trains stop", "railway station"),
    ("a book of maps", "atlas"),
    ("a person who bakes bread and cakes", "baker"),
    ("a young person between childhood and being a grown-up", "teenager"),
    ("a place where dead people are buried", "cemetery"),
    ("a person who acts in plays or films", "actor"),
    ("water in the form of soft white flakes in winter", "snow"),
]
_SPELL_WORDS[3] += ["birthday", "chocolate", "clothes", "country", "different",
                    "direction", "evening", "example", "family", "February",
                    "friendly", "gentle", "holiday", "island", "nature",
                    "October", "particular", "perhaps", "popular", "special",
                    "surprise", "thought", "vegetable", "weather"]
_SPELL_WORDS[4] += ["achievement", "agriculture", "apologise", "athlete",
                    "boundary", "ceremony", "congratulate", "cooperate",
                    "destination", "determined", "encyclopedia", "explanation",
                    "government", "hesitate", "humorous", "illustrate",
                    "immediately", "interfere", "laboratory", "mysterious",
                    "necessary", "parliament", "persuade", "physician",
                    "preferable", "privilege", "recognition", "restaurant",
                    "strength", "sufficient", "symptom", "twilight"]


def _everyday_qa_extra(n: int = 90) -> list[dict]:
    bank = [
        ("What should we do when we meet someone?", "We should wish them 'good morning' or say hello politely."),
        ("What should we do when someone helps us?", "We should say 'thank you' when someone helps us."),
        ("What do we use to measure our weight?", "We use a weighing scale to measure our weight."),
        ("What do we use to measure length?", "We use a ruler or a measuring tape to measure length."),
        ("Which is the largest bone in our body?", "The thigh bone, called the femur, is the largest bone in our body."),
        ("What protects our brain?", "The skull, a hard bone, protects our brain."),
        ("What is the boiling point of water?", "Water boils at 100 degrees Celsius."),
        ("At what temperature does water freeze?", "Water freezes at 0 degrees Celsius."),
        ("What is the sun?", "The sun is a star that gives the Earth light and heat."),
        ("What is a globe?", "A globe is a small round model of the Earth."),
        ("What is the Earth's only natural satellite?", "The Moon is the Earth's only natural satellite."),
        ("What do we call a young plant just coming out of the seed?", "A sprout or seedling is a young plant just coming out of the seed."),
        ("Which direction is opposite to north?", "South is opposite to north."),
        ("What do we call the times when the sun is neither too high nor too low, right after sunrise and before sunset?", "Those are the morning and evening times."),
        ("What should you do if a stranger offers you sweets?", "We should not take anything from strangers and should tell our parents or teacher."),
        ("What number do we dial for police help in India?", "We dial 112 for emergency help, and 100 connects to the police."),
        ("What number do we dial for an ambulance in India?", "We dial 108 for an ambulance in India."),
        ("What should we do if there is a small fire in the kitchen?", "Tell an adult immediately, turn off the gas, and never pour water on an oil fire."),
        ("Why should we not watch TV too close?", "Watching TV from very close can strain our eyes, so we keep a good distance."),
        ("What is the sound a lion makes called?", "A lion makes a roar."),
        ("What do we call many trees growing together?", "Many trees growing together form a forest."),
        ("What falls from clouds?", "Rain falls from clouds; in winter, snow can fall in cold places."),
        ("What do we call the person who delivers milk?", "The milkman delivers milk to our homes."),
        ("What hangs from the ceiling to give light?", "A light bulb or tube light hangs from the ceiling to give light."),
        ("What do we put on a wound?", "We put antiseptic and a bandage on a wound."),
        ("Which season comes after summer in India?", "The monsoon (rainy) season comes after summer in India."),
        ("What is the rainy season also called?", "The rainy season is also called the monsoon."),
        ("What do farmers grow in fields?", "Farmers grow crops like rice, wheat, vegetables and fruits in fields."),
        ("What is a desert like?", "A desert is very hot and dry with little rain and sand all around."),
        ("Name one animal that carries loads in the desert.", "The camel carries loads and people across the desert."),
        ("What is a neighbourhood shop called?", "A small neighbourhood shop is often called a kirana store."),
        ("What do we call a group of cows?", "A group of cows is called a herd."),
        ("What is a group of wolves called?", "A group of wolves is called a pack."),
        ("What time of day do we eat dinner?", "We usually eat dinner at night."),
        ("What do we call the meal eaten in the middle of the day?", "The meal we eat in the middle of the day is lunch."),
        ("What colour is the sky on a clear day?", "The sky is blue on a clear day."),
        ("What fills the sky at night?", "The moon and many stars fill the sky at night."),
        ("What do we use to see tiny things?", "We use a microscope to see very tiny things."),
        ("What instrument shows us our body's bones in a hospital?", "An X-ray machine shows the bones inside our body."),
        ("What do we call water falling from a tap?", "Water falling from a tap is called tap water or running water."),
        ("Where do we keep our clothes?", "We keep our folded clothes in a cupboard or almirah."),
        ("What covers the head of a person?", "Hair covers a person's head."),
        ("What grows on a plant and later becomes a fruit?", "A flower grows on a plant and later becomes a fruit."),
        ("What part of a plant attracts bees?", "Colourful flowers attract bees."),
        ("What do we call moving air?", "Moving air is called wind."),
        ("What do we light on a birthday cake?", "We light candles on a birthday cake."),
        ("What do we wear on our feet?", "We wear shoes, sandals or slippers on our feet."),
        ("What season brings new leaves and flowers?", "Spring brings new leaves and flowers."),
        ("What is the first meal of the day called?", "The first meal of the day is called breakfast."),
        ("What are the three main meals of the day?", "The three main meals are breakfast, lunch and dinner."),
        ("What must we do after playing outside?", "We must wash our hands and feet after playing outside."),
        ("Why do we have a dustbin at home?", "The dustbin keeps waste in one place so the home stays clean."),
        ("What do we call our father's brother?", "Our father's brother is our uncle (chacha or tau)."),
        ("Who waters the plants in a garden?", "The gardener waters the plants in a garden."),
        ("Who cuts hair?", "A barber or hairdresser cuts hair."),
        ("What do we call stories from long ago with gods and heroes?", "Old stories about gods and heroes are called mythological stories."),
        ("Which animal gives us wool?", "The sheep gives us wool."),
        ("What do we make from cotton?", "We make clothes and fabrics from cotton."),
        ("What do we call the safe path for people to cross a road?", "The safe path to cross a road is the zebra crossing."),
        ("What is a traffic light?", "A traffic light is a signal with red, yellow and green lights that controls vehicles on the road."),
        ("What should you do if you get lost in a crowd?", "Stay in one place, do not wander, and ask a policeman or an announcement for help."),
        ("Why do houses have windows?", "Windows let fresh air and sunlight come inside the house."),
        ("What is the roof of a house?", "The roof is the top covering of a house that protects us from rain and sun."),
        ("What do we call the room where we sleep?", "The room where we sleep is the bedroom."),
        ("Where do we park our cycles at school?", "We park our cycles in the cycle stand at school."),
        ("What sound does a clock make?", "A clock makes tick-tock sounds."),
        ("Which month has the fewest days?", "February has the fewest days — 28 or 29 days."),
        ("How many days does a leap year have?", "A leap year has 366 days."),
        ("Which month comes after July?", "August comes after July."),
        ("In which month do we celebrate Republic Day?", "We celebrate Republic Day in January, on the 26th."),
        ("What is a quarter of an hour?", "A quarter of an hour is 15 minutes."),
        ("How many minutes are there in an hour?", "There are 60 minutes in an hour."),
        ("How many hours are there in a day?", "There are 24 hours in a day."),
        ("What do we use to carry water on a picnic?", "We use a water bottle or a flask to carry water on a picnic."),
        ("What should we keep ready before it starts raining?", "We should keep an umbrella or raincoat ready before it starts raining."),
        ("What do we call tiny drops of water on leaves in the morning?", "Tiny drops of water on morning leaves are called dew."),
        ("What shines bright like silver in the night sky and changes shape?", "The moon shines in the night sky and changes its shape through the month."),
        ("Which animal says 'moo'?", "The cow says 'moo'."),
        ("Which animal loves carrots and hops?", "The rabbit loves carrots and hops."),
        ("What do we call a baby frog?", "A baby frog is called a tadpole."),
        ("What does a tadpole grow into?", "A tadpole grows into a frog."),
        ("What is the opposite of 'day'?", "The opposite of 'day' is 'night'."),
        ("What do we call the colours red, yellow and orange together?", "Red, yellow and orange are warm colours."),
        ("Which colour do we get by mixing red and white?", "Mixing red and white gives pink."),
        ("Which colour do we get by mixing blue and yellow?", "Mixing blue and yellow gives green."),
        ("What do we use to stick paper?", "We use glue or gum to stick paper."),
        ("What do we use to erase pencil marks?", "We use an eraser to remove pencil marks."),
        ("What sharpens a pencil?", "A sharpener sharpens a pencil."),
        ("Where do we write with a pencil on paper mistakes and all?", "We write in a notebook; mistakes can be erased with an eraser."),
    ]
    out = []
    for _ in range(n):
        q, a = _rng.choice(bank)
        out.append(_qa(_rng.choice([1, 2, 2, 3, 3, 4]), "qa", q, a))
    return out


def _tense_drills_extra(n: int = 90) -> list[dict]:
    verbs = [
        ("play", "played", "will play"), ("eat", "ate", "will eat"),
        ("go", "went", "will go"), ("write", "wrote", "will write"),
        ("sing", "sang", "will sing"), ("run", "ran", "will run"),
        ("see", "saw", "will see"), ("buy", "bought", "will buy"),
        ("make", "made", "will make"), ("read", "read", "will read"),
        ("swim", "swam", "will swim"), ("give", "gave", "will give"),
        ("take", "took", "will take"), ("come", "came", "will come"),
        ("drink", "drank", "will drink"), ("fly", "flew", "will fly"),
    ]
    names = ["Ravi", "Meera", "Anita", "Sameer", "Priya", "Vikram", "Sunita", "Amit", "Kiran", "Neha"]
    things = ["a letter", "a song", "a kite", "a story", "cricket", "the drum", "a picture", "chess"]
    out = []
    for _ in range(n):
        v, past, fut = _rng.choice(verbs)
        name = _rng.choice(names)
        thing = _rng.choice(things)
        style = _rng.randrange(3)
        if style == 0:
            out.append(_qa(_rng.choice([2, 3]), "exercise",
                           f"Change into the past tense: {name} {v}s {thing}.",
                           f"In the past tense: {name} {past} {thing}."))
        elif style == 1:
            out.append(_qa(_rng.choice([2, 3]), "exercise",
                           f"Change into the future tense: {name} {v}s {thing} today.",
                           f"In the future tense: {name} will {v} {thing} tomorrow."))
        else:
            out.append(_qa(_rng.choice([3, 4]), "exercise",
                           f"Fill in with the correct form of '{v}': Yesterday {name} ____ {thing}; today {name} {v}s {thing}; tomorrow {name} will ____ {thing}.",
                           f"Yesterday {name} {past} {thing}; today {name} {v}s {thing}; tomorrow {name} will {v} {thing}. "
                           f"Past, present and future are the three tenses."))
    return out
