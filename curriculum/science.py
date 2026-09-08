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
    return out
