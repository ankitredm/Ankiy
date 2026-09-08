"""Science / EVS foundation: living and non-living, plants, animals, human
body, food & health, water, air, weather, seasons, Earth & space, environment,
pollution, resources, habitats, simple physical science, cause and effect.

All content is original, age-appropriate explanation-style prose.
"""

from __future__ import annotations


def item(stage: int, kind: str, text: str) -> dict:
    return {"text": text, "category": "science", "stage": stage, "kind": kind}


_LIVING = [
    (1, "living and non-living things",
     "Living things eat, grow, breathe, move by themselves and make more of their own kind. "
     "Plants, animals and people are living things.\n"
     "Non-living things do not eat, grow or breathe on their own. A stone, a chair, water and a "
     "toy car are non-living.\n"
     "Quick check: does it grow and breathe? Then it is living. Remember — a car moves, but it "
     "cannot grow or breathe, so it is non-living!"),
    (2, "plants are living things",
     "Plants are living things even though they do not walk or run. They make their own food "
     "from sunlight, they breathe through tiny pores on their leaves, they grow taller every "
     "season, and they make seeds which grow into new plants."),
    (2, "life processes",
     "All living things do certain things: they take food, they grow, they breathe, they "
     "remove waste from their body, they respond to the world around them, and they reproduce "
     "(make young ones). If something does all these, it is living."),
]

_PLANTS = [
    (1, "parts of a plant",
     "A plant has roots, a stem, leaves, flowers and fruits.\n"
     "Roots hold the plant in the soil and drink water from the ground. The stem carries water "
     "up and holds the plant straight. Leaves make food for the plant using sunlight. Flowers "
     "make fruits, and fruits hold seeds.\n"
     "Try it: touch a soft stem and a woody stem. Which one belongs to a young plant?"),
    (2, "what plants need to grow",
     "Plants need four things: sunlight, water, air and good soil. Without sunlight the leaves "
     "turn pale and the plant becomes weak. Without water the plant dries. Plants also need a "
     "little space to grow, which is why gardeners plant seeds not too close together."),
    (2, "seeds and germination",
     "A seed is a tiny baby plant sleeping inside a coat with its food packed beside it. "
     "When a seed gets water, air and warmth, it wakes up: first a root comes out, then a small "
     "shoot with leaves. This waking up is called germination. Soaked gram or bean seeds "
     "germinate in a few days — try it on wet cotton."),
    (3, "photosynthesis in simple words",
     "How do plants make their food? Leaves work like tiny kitchens. They take in air through "
     "tiny pores, drink water through the roots, and catch sunlight with the green colouring "
     "matter called chlorophyll. Using all three, the leaf cooks sugar for the plant and gives "
     "out oxygen. This food-making process is called photosynthesis. Because of this, plants "
     "feed the world and give us the oxygen we breathe."),
    (3, "kinds of plants",
     "Trees like the banyan and mango are big and strong with woody stems. Shrubs like the "
     "hibiscus are bushy and medium-sized. Herbs like coriander and mint are small and soft. "
     "Climbers like the grapevine climb up with support, and creepers like the pumpkin spread "
     "along the ground."),
    (4, "uses of plants",
     "Plants give us food (rice, wheat, fruits, vegetables), wood for furniture and houses, "
     "cotton for clothes, medicines, paper, rubber, shade, and clean air. Forests also hold the "
     "soil together with their roots and stop floods. This is why planting trees and protecting "
     "forests is one of the best things humans can do."),
]

_ANIMALS = [
    (1, "animals and their sounds",
     "A cow says moo, a dog says bow-wow, a cat says meow, a lion roars, and a snake hisses. "
     "Animals use their sounds to call each other and warn of danger."),
    (1, "animal homes",
     "A lion lives in a den, a dog lives in a kennel, a horse lives in a stable, a bird lives "
     "in a nest, a bee lives in a hive, a spider weaves a web, and an ant lives in an anthill "
     "under the ground."),
    (2, "wild and domestic animals",
     "Wild animals like lions, tigers, elephants and deer live in forests and take care of "
     "themselves. Domestic animals like cows, goats, hens and dogs live with people and give us "
     "milk, eggs, wool, help and friendship. Wild animals should be watched from far away and "
     "never troubled."),
    (2, "animal food habits",
     "Animals that eat only plants are called herbivores — the cow, goat, deer and elephant. "
     "Animals that eat other animals are carnivores — the lion, tiger and eagle. Animals that "
     "eat both plants and flesh are omnivores — the bear, crow and humans!"),
    (2, "birds",
     "Birds have feathers, two wings, two legs and a beak. Their bones are light and hollow, "
     "which helps them fly. Not every bird flies: the penguin swims instead, and the ostrich "
     "runs very fast. Birds build nests, lay eggs, and feed their babies until they can fly."),
    (3, "insects",
     "Insects are small animals with six legs. Ants, bees, butterflies, houseflies and "
     "mosquitoes are insects. Bees visit flowers, collect nectar and make honey — they also "
     "help plants make fruits by carrying pollen. A butterfly's life goes: egg -> caterpillar "
     "-> pupa (cocoon) -> butterfly. This big change is called metamorphosis."),
    (3, "water animals",
     "Fish breathe with gills instead of lungs, so they take in oxygen from water. They swim "
     "with fins and a tail. A whale lives in water like a fish but is actually a huge mammal "
     "that breathes air and feeds its babies milk."),
    (4, "food chains",
     "Grass is eaten by the grasshopper, the grasshopper by the frog, the frog by the snake, "
     "and the snake by the eagle. This eating order is called a food chain. Every food chain "
     "starts with plants, because plants alone can make food from sunlight. If one link is "
     "removed — say all frogs vanish — the whole chain is disturbed."),
    (4, "endangered animals",
     "Some animals like the tiger, panda and one-horned rhinoceros are becoming very few in "
     "number because forests are being cut and people hunt them. Such animals are called "
     "endangered. National parks and sanctuaries protect them. When a species dies out "
     "completely, it is extinct — like the dinosaurs."),
]

_BODY = [
    (1, "my body and senses",
     "We have five senses and sense organs: eyes to see, ears to hear, nose to smell, tongue "
     "to taste, and skin to touch and feel. Our body also has strong bones inside and muscles "
     "that help us move."),
    (2, "bones and muscles",
     "Inside our body is a frame of 206 bones called the skeleton. It gives the body shape, "
     "holds it up, and protects soft organs — the skull protects the brain and the ribs protect "
     "the heart and lungs. Muscles are attached to bones and pull them to make us move. Milk, "
     "eggs and sunlight keep bones strong."),
    (3, "important organs",
     "The brain is the control room of the body — it thinks and sends messages through nerves. "
     "The heart pumps blood to the whole body, day and night, without rest. The lungs take in "
     "oxygen from air and push out carbon dioxide. The stomach digests food. The kidneys clean "
     "the blood and remove waste as urine."),
    (3, "keeping our body clean",
     "Bathe every day, brush your teeth twice a day, cut your nails weekly, wash hands before "
     "eating and after the toilet, and comb your hair. Cleanliness keeps germs away and "
     "prevents diseases like tooth decay and stomach infections."),
    (4, "how food is digested",
     "Digestion is the journey of food through the body. The mouth chews food and mixes it "
     "with saliva. The food pipe carries it to the stomach, where digestive juices break it "
     "down further. The small intestine takes the good nutrients into the blood. The large "
     "intestine removes the leftover water, and the waste leaves the body. That is why we must "
     "chew properly and eat slowly — digestion starts in the mouth!"),
]

_FOOD_HEALTH = [
    (1, "healthy food",
     "Fruits, vegetables, milk, eggs, dal, rice, roti and nuts help us grow strong and healthy. "
     "Too many toffees, cold drinks and chips are junk food — they fill the tummy but give very "
     "little goodness."),
    (2, "food groups",
     "Energy-giving foods like rice, roti, potato and ghee give us power to play and work. "
     "Body-building foods like milk, dal, eggs and paneer help us grow and repair the body. "
     "Protective foods like fruits and green vegetables protect us from illness. A good thali "
     "has all three groups."),
    (3, "why water is important for the body",
     "More than half of our body is water! Water carries nutrients in the blood, keeps the body "
     "cool through sweat, and removes waste. Drink 6 to 8 glasses of clean water every day. "
     "When we play and sweat, we must drink even more."),
    (4, "balanced diet",
     "A balanced diet has the right amounts of all food groups plus water: roti or rice for "
     "energy, dal or eggs or milk for the body, vegetables and fruits for protection, and a "
     "little oil and ghee. Eating only one kind of food is never balanced. Balanced diet + "
     "exercise + sleep = a healthy body."),
]

_WATER_AIR_WEATHER = [
    (1, "water in our life",
     "We drink water and use it for cooking, bathing, washing clothes and watering plants. "
     "Farmers need water for crops and animals need water to live. Always store drinking water "
     "covered, and never waste it."),
    (2, "three forms of water",
     "Water can be a liquid (water itself), a solid (ice) and a gas (water vapour). Ice melts "
     "into water when warmed, and water becomes vapour when boiled. On cooling, vapour becomes "
     "water again. Nature keeps changing water among these three forms — that is the water "
     "cycle at work."),
    (3, "the water cycle",
     "The sun heats seas, rivers and lakes, and water rises up as invisible vapour. High above, "
     "the vapour cools into tiny droplets that gather as clouds. When the clouds become heavy, "
     "the water falls back as rain or snow. The rain flows into rivers and back to the sea. "
     "Then the cycle starts again. The same water keeps circling the Earth for millions of years!"),
    (2, "air around us",
     "Air is all around us even though we cannot see it. Moving air is wind. Air has oxygen "
     "that we breathe, carbon dioxide that plants use, and other gases. Air fills tyres, helps "
     "kites fly, sails boats, and makes windmills turn. We can feel air when we fan ourselves."),
    (2, "weather",
     "Weather is what the sky and air are like each day — sunny, cloudy, rainy, windy or "
     "stormy. Weather changes from day to day and even within one day. A hot sunny morning can "
     "turn into a rainy afternoon."),
    (3, "seasons",
     "India mainly has three seasons. Summer is hot; days are long and we wear cotton clothes, "
     "drink lots of water and eat juicy fruits like watermelon. The rainy season brings monsoon "
     "showers, puddles, umbrellas, and happy farmers waiting for crops. Winter is cold; we wear "
     "woollens, enjoy the warm sun, and eat fresh carrots, peas and oranges."),
    (3, "keeping water clean",
     "Drinking water must be clean, or it can carry germs that cause diseases like diarrhoea "
     "and typhoid. We can boil water or filter it before drinking, keep pots and buckets "
     "covered, and never let dirty water collect near our homes — stagnant water breeds "
     "mosquitoes that spread malaria and dengue."),
]

_EARTH_SPACE = [
    (2, "the Sun",
     "The Sun is a huge ball of burning gases far away in the sky. It gives us light in the day "
     "and warmth. Without the Sun there would be no day, no plants, and no life on Earth. "
     "Never look directly at the Sun — it can hurt your eyes."),
    (2, "the Moon",
     "The Moon is Earth's closest neighbour in space. It does not make its own light; it only "
     "reflects sunlight like a mirror. The Moon appears to change shape across a month — full "
     "moon, half moon, and no-moon — because we see different sunlit parts as it circles Earth."),
    (3, "our Earth",
     "Earth is our home planet. From space it looks blue because most of its surface is covered "
     "with water. Earth spins on its own axis once a day — that spinning makes day and night. "
     "It also goes around the Sun once a year, which gives us the year and the seasons."),
    (3, "day and night",
     "Day and night happen because the Earth spins like a top. The side facing the Sun has "
     "daytime, while the side away from the Sun has night. One full spin takes 24 hours, so "
     "every place gets day and night in turn."),
    (4, "stars",
     "Stars are giant balls of burning gases, just like our Sun, but very very far away — that "
     "is why they look like tiny twinkling dots. The Sun is actually the nearest star to Earth. "
     "Long ago, sailors used star patterns in the night sky to find directions at sea."),
]

_ENVIRONMENT = [
    (2, "our environment",
     "Environment is everything around us — air, water, soil, plants, animals, and the places "
     "we live in. A clean environment keeps us healthy. We should plant trees, keep our "
     "surroundings clean, and never throw garbage on the road or in rivers."),
    (3, "pollution",
     "Pollution is when harmful things mix into air, water or land. Smoke from vehicles and "
     "factories pollutes the air and makes breathing hard. Garbage and dirty drains pollute "
     "water and spread disease. Loud horns and loudspeakers cause noise pollution, which hurts "
     "our ears and disturbs everyone."),
    (3, "how to reduce pollution",
     "Walk or cycle for short trips, share cars and use buses and trains, plant trees, use both "
     "sides of paper, say no to plastic bags (carry a cloth bag), never throw plastic into "
     "water, and keep taps closed. Small habits of many people make a big difference."),
    (4, "natural resources",
     "Nature gives us free gifts called natural resources: water, air, sunlight, soil, "
     "forests, coal, petroleum and minerals. Some resources like sunlight and wind will never "
     "finish, but coal and petroleum take millions of years to form and can run out. Using "
     "them wisely, and switching to solar and wind energy, protects the future."),
    (4, "habitats",
     "A habitat is the natural home of a plant or animal with everything it needs — food, "
     "water and shelter. A pond is a habitat for fish and frogs; a desert is a habitat for "
     "camels and cactuses; dense forests are habitats for tigers and monkeys. Animals' bodies "
     "suit their habitats: a fish has gills for water, a camel stores fat in its hump for long "
     "desert journeys, and polar bears have thick fur for icy lands."),
    (3, "forests",
     "Forests are green treasures. They give wood, fruits, honey and medicines; they are homes "
     "for countless animals; tree roots hold soil so rain cannot wash it away; and leaves soak "
     "in carbon dioxide and give out oxygen. Cutting entire forests is called deforestation, "
     "and it causes floods, soil loss and homeless animals."),
]

_PHYSICS = [
    (2, "light and shadow",
     "Light travels in straight lines. When an object blocks light, a dark shape called a "
     "shadow forms behind it. Shadows are longest in the early morning and evening, and short "
     "at noon when the Sun is overhead. A shadow always forms on the side away from the light."),
    (2, "sink and float",
     "Some things float on water — a leaf, a plastic ball, an empty bottle. Heavy or dense "
     "things like a stone and a metal key sink. Shape matters too: a steel plate sinks, but the "
     "same steel shaped like a bowl can float, because of how it pushes water aside. Big ships "
     "float using this idea!"),
    (3, "push and pull — forces",
     "A push or a pull is called a force. We pull a rope in tug-of-war, push a swing, and pull "
     "a drawer open. Forces can move things, stop them, speed them up, slow them down, or "
     "change their direction and shape (squeezing a sponge)."),
    (3, "magnets",
     "A magnet attracts things made of iron — pins, nails, paper clips. Every magnet has two "
     "poles, north and south. Two north poles push each other away, but a north and a south "
     "pole pull together: like poles repel, unlike poles attract. Compass needles are tiny "
     "magnets that always settle pointing north — that is how we find directions!"),
    (4, "simple machines",
     "Simple machines make work easier. A ramp (inclined plane) helps roll heavy loads up. A "
     "see-saw is a lever. A flag goes up with a wheel and rope (pulley). An axe is a wedge, and "
     "a screw is a wound-up ramp. Scissors are two levers with two wedges together!"),
]

_CAUSE_EFFECT = [
    (2, "Why do we feel thirsty on a hot day?",
     "On a hot day we sweat a lot, and the body loses water. Thirst is the body's way of "
     "asking us to refill that water. That is why we must drink more water in summer."),
    (3, "Why do wet clothes dry faster in the sun?",
     "The Sun's heat turns water into vapour, which mixes into the air. More sun and more wind "
     "mean faster drying. On a cloudy humid day, drying is slow for the same reason."),
    (3, "Why does a metal spoon feel hotter than a wooden one in the same soup?",
     "Metal lets heat travel through it quickly, so it feels hot fast. Wood does not let heat "
     "travel easily, so it stays comfortable to hold. Materials that pass heat quickly are "
     "called conductors, and those that do not are insulators."),
    (4, "Why do we wear light colours in summer and dark colours in winter?",
     "Dark surfaces soak up more of the Sun's heat and light surfaces reflect it. Dark clothes "
     "in summer would make us feel hotter, so we wear white and light colours in summer and "
     "dark woollens in winter to stay warm."),
]


def build() -> list[dict]:
    out: list[dict] = []
    for group in (_LIVING, _PLANTS, _ANIMALS, _BODY, _FOOD_HEALTH,
                  _WATER_AIR_WEATHER, _EARTH_SPACE, _ENVIRONMENT, _PHYSICS,
                  _CAUSE_EFFECT):
        for stage, topic, text in group:
            out.append(item(stage, "explanation", f"{topic.capitalize()}.\n{text}"))
            # A plain question-form version helps question-answer style learning.
            q = topic[0].upper() + topic[1:]
            q = q if q.endswith("?") else f"{q} — explain this in simple words."
            out.append(item(stage, "qa",
                            f"Question: {q.replace(' — explain this in simple words.', '')}\n"
                            f"Answer: {text}"))
    # Extra quick fact drills for early stages.
    facts = [
        (1, "Question: Which animal gives us milk?\nAnswer: The cow and the buffalo give us milk. Goats and camels also give milk."),
        (1, "Question: Name two fruits.\nAnswer: Mango and banana are two fruits. Apples, oranges, guava and papaya are fruits too."),
        (1, "Question: What do we use to see?\nAnswer: We use our eyes to see."),
        (2, "Question: Name the three forms of water.\nAnswer: Solid (ice), liquid (water) and gas (water vapour)."),
        (2, "Question: Which body part helps us hear?\nAnswer: Our ears help us hear."),
        (2, "Question: What does a plant need to grow?\nAnswer: Sunlight, water, air and good soil."),
        (3, "Question: Which organ pumps blood?\nAnswer: The heart pumps blood to the whole body."),
        (3, "Question: What do we call animals that eat only plants?\nAnswer: Herbivores, like the cow, goat and deer."),
        (3, "Question: Why should we not waste water?\nAnswer: Clean water is limited and precious; living things need it every day, so wasting it can cause shortages for everyone."),
        (4, "Question: What is a habitat?\nAnswer: A habitat is the natural home of a plant or animal, with the food, water and shelter it needs."),
        (4, "Question: Name two renewable resources.\nAnswer: Sunlight and wind — they will never run out."),
    ]
    for stage, text in facts:
        out.append(item(stage, "qa", text))

    # -- Expanded parametric practice (foundation-training scale-up) ---------
    out += _animal_facts(n=340)
    out += _body_facts(n=160)
    out += _plant_facts(n=150)
    out += _water_space_facts(n=180)
    out += _health_safety_facts(n=170)
    out += _habitat_environment_facts(n=140)
    out += _cause_effect_science(n=130)
    return out


# ===========================================================================
# Expanded parametric practice — foundation-training scale-up.
# Fact tables x question variants, so the model learns CONCEPTS with several
# phrasings instead of memorising one string.
# ===========================================================================
import random as _random

_rng = _random.Random(20240504)


def _qa(stage: int, q: str, a: str) -> dict:
    return item(stage, "qa", f"Question: {q}\nAnswer: {a}")


def _variants(qs: list[str]):
    """Pick a random question phrasing for a fact."""
    return _rng.choice(qs)


def _animal_facts(n: int = 240) -> list[dict]:
    table = [
        # (animal, stage, young, home, sound, food, special)
        ("cow", 1, "calf", "shed", "moos", "grass", "gives us milk"),
        ("dog", 1, "puppy", "kennel", "barks", "food we give it", "guards our home"),
        ("cat", 1, "kitten", "house", "meows", "milk and fish", "catches mice"),
        ("hen", 1, "chick", "coop", "clucks", "grains", "gives us eggs"),
        ("goat", 2, "kid", "shed", "bleats", "grass and leaves", "gives us milk"),
        ("horse", 2, "foal", "stable", "neighs", "grass and hay", "runs very fast"),
        ("sheep", 2, "lamb", "fold", "bleats", "grass", "gives us wool"),
        ("duck", 2, "duckling", "pond", "quacks", "small water plants", "swims in water"),
        ("lion", 2, "cub", "den", "roars", "meat of other animals", "is called the king of the jungle"),
        ("frog", 2, "tadpole", "pond", "croaks", "insects", "can live in water and on land"),
        ("rabbit", 2, "bunny", "burrow", "no loud sound", "carrots and green plants", "digs burrows"),
        ("elephant", 3, "calf", "jungle", "trumpets", "leaves, grass and bananas", "is the biggest land animal"),
        ("tiger", 3, "cub", "jungle", "roars", "meat", "is our national animal"),
        ("bee", 3, "larva", "hive", "buzzes", "nectar from flowers", "makes honey"),
        ("camel", 3, "calf", "desert", "grunts", "desert plants", "stores fat in its hump"),
        ("fish", 1, "fry", "water", "makes no sound", "small water plants and worms", "breathes with gills"),
        ("butterfly", 3, "caterpillar", "garden", "makes no sound", "nectar of flowers", "grows from a caterpillar"),
        ("monkey", 2, "infant", "tree", "chatters", "fruits and bananas", "climbs trees very well"),
        ("penguin", 3, "chick", "cold Antarctica", "squawks", "fish", "is a bird that cannot fly but swims well"),
        ("snake", 3, "snakelet", "holes in the ground", "hisses", "small animals and eggs", "crawls without legs"),
        ("sparrow", 2, "chick", "nest", "chirps", "grains and insects", "is a small bird that lives near us"),
        ("pigeon", 1, "squab", "nest", "coos", "grains", "carries messages in old times"),
        ("buffalo", 2, "calf", "shed", "bellows", "grass", "gives us milk"),
        ("donkey", 2, "foal", "shed", "brays", "grass and hay", "carries heavy loads"),
        ("owl", 3, "owlet", "hole in a tree", "hoots", "insects and small rats", "sees clearly at night"),
        ("crow", 1, "chick", "nest", "caws", "grains and food scraps", "is a clever common bird"),
        ("buffalo", 2, "calf", "shed", "bellows", "grass", "gives us milk"),
        ("goose", 2, "gosling", "pond side", "honks", "grains and grass", "swims with its webbed feet"),
        ("kangaroo", 3, "joey", "grassland of Australia", "makes no typical sound", "plants and grass", "carries its baby in a pouch"),
        ("giraffe", 3, "calf", "savanna", "makes low sounds", "leaves of tall trees", "has a very long neck to reach leaves"),
        ("zebra", 3, "foal", "grassland", "barks and snorts", "grass", "has black and white stripes"),
        ("crab", 3, "small crabs", "sea shore", "makes no sound", "small water creatures", "walks sideways"),
        ("squirrel", 2, "kitten", "tree hollow", "chatters", "nuts and fruits", "stores nuts for winter"),
        ("peacock", 2, "chick", "forest and gardens", "screams and dances", "grains and insects", "is our national bird"),
    ]
    out = []
    for _ in range(n):
        row = _rng.choice(table)
        animal, stage, young, home, sound, food, special = row
        style = _rng.randrange(5)
        if style == 0:
            q = _variants([f"What is the young one of a {animal} called?",
                           f"A baby {animal} is called what?"])
            out.append(_qa(stage, q, f"A baby {animal} is called a {young}."))
        elif style == 1:
            q = _variants([f"Where does a {animal} live?", f"What is the home of a {animal}?"])
            out.append(_qa(stage, q, f"A {animal} lives in a {home}."))
        elif style == 2:
            q = f"What sound does a {animal} make?"
            out.append(_qa(stage, q, f"A {animal} {sound}."))
        elif style == 3:
            q = _variants([f"What does a {animal} eat?", f"What is the food of a {animal}?"])
            out.append(_qa(stage, q, f"A {animal} eats {food}."))
        else:
            out.append(_qa(stage, f"Tell one special thing about the {animal}.",
                           f"The {animal} {special}."))
    return out


def _body_facts(n: int = 110) -> list[dict]:
    table = [
        ("heart", 3, "pumps blood to the whole body", "the chest"),
        ("lungs", 3, "help us breathe in oxygen and breathe out carbon dioxide", "the chest"),
        ("brain", 3, "controls all our body parts and helps us think and remember", "the head"),
        ("stomach", 3, "digests the food we eat", "the belly"),
        ("eyes", 1, "help us see", "the face"),
        ("ears", 1, "help us hear", "the sides of the head"),
        ("nose", 1, "helps us smell and breathe", "the face"),
        ("tongue", 1, "helps us taste food", "inside the mouth"),
        ("skin", 2, "covers and protects our whole body", "all over the body"),
        ("bones", 2, "give shape and strength to our body", "inside the body"),
        ("muscles", 4, "help our body move", "all over the body"),
        ("teeth", 1, "help us bite and chew food", "in the mouth"),
        ("kidneys", 4, "clean the blood and remove waste", "near the back of the belly"),
    ]
    out = []
    for _ in range(n):
        organ, stage, job, where = _rng.choice(table)
        style = _rng.randrange(3)
        if style == 0:
            out.append(_qa(stage, _variants([f"What is the work of the {organ}?",
                                             f"What does the {organ} do?"]),
                           f"The {organ} {job}."))
        elif style == 1:
            if organ in ("eyes", "ears", "nose", "tongue"):
                use = {"eyes": "see", "ears": "hear", "nose": "smell", "tongue": "taste"}[organ]
                out.append(_qa(stage, f"Which body part do we use to {use}?",
                               f"We use our {organ} to {use}."))
            else:
                out.append(_qa(stage, f"Where is the {organ} located?",
                               f"The {organ} is in {where}."))
        else:
            out.append(_qa(stage, f"Is the {organ} important for us?",
                           f"Yes, the {organ} is very important — it {job}."))
    return out


def _plant_facts(n: int = 100) -> list[dict]:
    facts = [
        (1, "Which part of the plant is under the ground?", "The roots are under the ground. They hold the plant and soak water."),
        (1, "Which part of the plant makes food?", "The leaves make food for the plant using sunlight."),
        (2, "What does the stem of a plant do?", "The stem holds the plant upright and carries water from the roots to the leaves."),
        (2, "What do roots do for a plant?", "Roots hold the plant in the soil and absorb water and minerals."),
        (2, "Why are leaves called the food factory of the plant?", "Because leaves make food for the whole plant using sunlight, air and water."),
        (3, "What is photosynthesis?", "Photosynthesis is the process by which green leaves make food using sunlight, water and carbon dioxide, and give out oxygen."),
        (3, "Why do plants need sunlight?", "Plants need sunlight to make their food by photosynthesis. Without sunlight they turn weak and pale."),
        (3, "What parts grow into a new plant?", "A seed grows into a new plant when it gets soil, water and warmth."),
        (4, "What is chlorophyll?", "Chlorophyll is the green colouring matter in leaves that traps sunlight for photosynthesis."),
        (4, "How do insects help plants?", "Insects like bees carry pollen from flower to flower, which helps the plant make fruits and seeds."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _water_space_facts(n: int = 110) -> list[dict]:
    facts = [
        (1, "What is the water we drink called?", "The water we drink is called drinking water, and it should be clean and boiled or filtered."),
        (2, "Name the three forms of water.", "Water has three forms — solid (ice), liquid (water) and gas (water vapour)."),
        (2, "What happens when water is boiled?", "When water is boiled, it turns into steam (water vapour)."),
        (2, "What happens when water is kept in a freezer?", "Water freezes into ice in a freezer."),
        (3, "What is the water cycle?", "The sun turns water into vapour, vapour rises and forms clouds, clouds give rain, and rainwater flows back to rivers. This cycle keeps repeating."),
        (3, "Why does it rain?", "Water vapour rises, cools down and forms clouds. When the water drops in clouds become heavy, they fall as rain."),
        (3, "What are the sources of water?", "Rivers, lakes, ponds, wells, rains, glaciers and springs are sources of water."),
        (3, "Which is the biggest source of light and heat for the Earth?", "The Sun is the biggest source of light and heat for the Earth."),
        (3, "Does the Moon shine with its own light?", "No. The Moon reflects the Sun's light — it has no light of its own."),
        (4, "Why do we have day and night?", "The Earth spins on its axis. The side facing the Sun has day, and the other side has night."),
        (4, "What is a solar eclipse in simple words?", "A solar eclipse happens when the Moon comes between the Sun and the Earth and blocks the Sun's light."),
        (4, "Which is the largest planet of our solar system?", "Jupiter is the largest planet of our solar system."),
        (4, "Which planet is closest to the Sun?", "Mercury is the planet closest to the Sun."),
        (4, "How many planets are there in our solar system?", "There are eight planets in our solar system."),
        (4, "Why is the Earth called the blue planet?", "From space, the Earth looks blue because most of its surface is covered with water."),
        (3, "What is a star?", "A star is a huge ball of burning gas that gives out its own light. The Sun is our nearest star."),
        (4, "Which planet is called the red planet?", "Mars is called the red planet because its soil looks red."),
        (4, "Which planet do we live on?", "We live on the Earth — the only planet known to have life."),
        (4, "What are shooting stars really?", "A 'shooting star' is actually a small rock burning up when it enters the Earth's air."),
        (3, "Why is the moon visible at night?", "The Moon reflects the Sun's light towards us, so we can see it at night."),
        (3, "When is the moon a full moon?", "When the whole bright side of the Moon faces the Earth, we see a full moon — roughly once a month."),
        (2, "Which is bigger — the sun or the moon — as seen by us?", "The Sun and the Moon look about the same size, but the Sun is really much, much bigger — it only looks smaller because it is far away."),
        (4, "What is an orbit?", "An orbit is the curved path one object takes around another in space, like the Earth around the Sun."),
        (4, "How long does the Earth take to go around the Sun?", "The Earth takes about 365 days — one year — to go around the Sun."),
        (4, "How long does the Earth take to spin once?", "The Earth takes about 24 hours — one day — to spin once on its axis."),
        (3, "What is solar energy in simple words?", "Solar energy is the energy we get from sunlight. Solar panels use it to make electricity."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _health_safety_facts(n: int = 110) -> list[dict]:
    facts = [
        (1, "What should we do before eating?", "We should wash our hands with soap before eating."),
        (1, "Why should we brush our teeth?", "Brushing keeps our teeth clean and stops tooth decay. We brush twice a day."),
        (1, "What should we do with fruit before eating it?", "We should wash fruits with clean water before eating them."),
        (2, "Why should we exercise?", "Exercise keeps our body strong, our heart healthy and our mind fresh."),
        (2, "Why is sleep important?", "Sleep gives our body rest and helps us grow. Children need about 8 to 10 hours of sleep."),
        (2, "What should we do when the traffic light is red?", "When the light is red, we must stop. We cross only when it is safe, at the zebra crossing."),
        (2, "Why should we not play on the road?", "The road is for vehicles. Playing there can cause accidents, so we play in parks or playgrounds."),
        (3, "Why should we drink clean water?", "Dirty water carries germs that cause diseases like typhoid and diarrhoea. Clean water keeps us healthy."),
        (3, "What is a balanced diet?", "A balanced diet has all kinds of food — energy-giving grains, body-building proteins like dal and eggs, and protective fruits and vegetables — in the right amounts."),
        (3, "Why should we not eat food that has fallen on the floor?", "Germs stick to food that falls on the floor. Eating it can make us sick."),
        (4, "What are first-aid basics for a small cut?", "Wash the cut with clean water, press with a clean cloth to stop bleeding, and cover it with a clean bandage. Tell an adult."),
        (4, "Why is vaccination important?", "Vaccines protect us from dangerous diseases by making our body ready to fight germs."),
        (4, "Why should we cover our mouth while sneezing?", "Sneezing throws out tiny drops full of germs. Covering the mouth stops these germs from spreading to others."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _habitat_environment_facts(n: int = 90) -> list[dict]:
    facts = [
        (3, "What is a habitat?", "A habitat is the natural home of a plant or animal, with the food, water and shelter it needs."),
        (3, "Where do desert animals like camels live and how do they manage?", "Deserts are hot and dry. Camels store fat in their humps and can stay long without water."),
        (3, "How is a fish suited to live in water?", "A fish has gills to breathe in water, fins to swim and a streamlined body."),
        (3, "Why do polar bears have thick fur?", "Polar bears live in very cold places. Thick fur keeps their body warm."),
        (4, "What is the food chain in simple words?", "A food chain shows who eats whom — grass is eaten by a grasshopper, the grasshopper by a frog, the frog by a snake, and the snake by an eagle."),
        (4, "Why should we not cut trees?", "Trees give us oxygen, food, shade and wood. Their roots hold the soil, and birds nest in them. Cutting trees harms everyone."),
        (4, "What is deforestation and why is it harmful?", "Cutting forests on a large scale is deforestation. It destroys animal homes, causes floods and increases pollution."),
        (4, "What can we do to keep our environment clean?", "Use dustbins, avoid plastic, plant trees, save water and electricity, and keep our surroundings clean."),
        (4, "Why are earthworms called friends of the farmer?", "Earthworms make the soil loose and airy, and their waste makes the soil rich, which helps crops grow."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _cause_effect_science(n: int = 70) -> list[dict]:
    pairs = [
        (2, "Why does ice cream melt in the sun?", "Because the Sun's heat raises its temperature and turns solid ice cream into liquid."),
        (2, "Why do we wear light clothes in summer?", "Light and white clothes do not absorb much heat, so we feel cool and comfortable."),
        (2, "Why do we sweat in summer?", "Sweating cools our body — when sweat dries, it takes away heat from the skin."),
        (3, "Why does a metal spoon become hot in hot tea?", "Metal is a good conductor of heat, so heat travels from the tea to the spoon."),
        (3, "Why do wet clothes dry faster in the sun?", "Sunlight and wind speed up evaporation, so the water in the clothes turns into vapour quickly."),
        (3, "Why do we see lightning before we hear thunder?", "Light travels much faster than sound, so the flash of lightning reaches us before the sound of thunder."),
        (3, "Why do we feel cold near a waterfall or after rain?", "Evaporation is fast there, and evaporating water takes away heat, which cools the air."),
        (4, "Why does a ball thrown up come back down?", "Because gravity pulls every object towards the Earth."),
        (4, "Why do we see our reflection in still water?", "Still water acts like a smooth mirror and reflects light, forming an image."),
        (4, "Why do boats float while a stone sinks?", "A boat's shape holds a lot of air, so it floats; a stone is heavy and dense, so it sinks."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(pairs)
        out.append(_qa(stage, q, a))
    return out
