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
    )
