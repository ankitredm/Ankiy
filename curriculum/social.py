"""Social studies foundation: family, community, school, occupations, rules,
geography, directions, maps, India, states and cities, history & culture,
festivals, transport and communication — Class 1-4 level, factual and
respectful. All text is original.
"""

from __future__ import annotations


def item(stage: int, kind: str, text: str) -> dict:
    return {"text": text, "category": "social", "stage": stage, "kind": kind}


_FAMILY_COMMUNITY = [
    (1, "my family",
     "A family is a group of people who love and care for each other. A small or nuclear family "
     "has parents and children. A big or joint family also has grandparents, uncles, aunts and "
     "cousins living together or close by. Grandparents tell us stories and give us lots of "
     "love. Every member of a family helps the others."),
    (1, "helping at home",
     "Everyone in a family works together. Father may cook, mother may go to office, and "
     "children can water plants, arrange their books and keep their room tidy. When everybody "
     "helps, the house runs happily. Helping at home is the first step to responsibility."),
    (2, "neighbours and community",
     "The people living near our house are our neighbours. Good neighbours help each other — "
     "in joy and in emergencies. All the families, shops, school, park and post office together "
     "make our neighbourhood or community. Keeping the neighbourhood clean is everyone's job."),
    (2, "respect for all",
     "Every family is different — some are big, some are small; some celebrate one festival, "
     "some celebrate another; some speak one language, some speak another. We should respect "
     "every family, greet everyone politely, and never make fun of anyone's food, dress, "
     "language or religion. India is strong because of its many different people living together."),
    (3, "rules and responsibilities",
     "Rules keep us safe and fair — walking on the footpath, waiting for our turn, crossing at "
     "the zebra crossing, and not hurting anyone. Responsibilities are the duties we must do "
     "ourselves: finishing homework, keeping promises, and caring for public property like "
     "parks and buses. Good citizens follow rules even when nobody is watching."),
]

_SCHOOL_OCCUPATIONS = [
    (1, "people who help us at school",
     "Teachers teach us. The principal guides the whole school. The librarian helps us find "
     "books. The peon rings the bell, and the gardener cares for the plants. The sweeper keeps "
     "our school clean. We should thank and respect everyone who helps us."),
    (1, "people who help us outside",
     "Doctors treat us when we are ill, and nurses care for patients. Policemen keep us safe "
     "and manage traffic. Firemen put out fires. Farmers grow our food, and postmen deliver "
     "letters. Soldiers guard our borders so we can sleep in peace."),
    (2, "occupations",
     "A farmer grows crops in fields. A baker bakes bread and biscuits. A tailor stitches "
     "clothes. A carpenter makes furniture from wood. A potter shapes clay into pots. A doctor "
     "treats patients, a teacher teaches students, and a driver drives buses and trucks. Every "
     "job is important, and no work is big or small."),
    (3, "from farm to plate",
     "The rice on our plate takes a long journey. A farmer ploughs the field, sows seeds and "
     "waters the crop for months. After harvest, the grain is dried, packed and sent to mills "
     "and markets. Shopkeepers sell it, and at home it is cooked. Many hands feed us — that is "
     "why we should never waste food."),
    (3, "teamwork in community",
     "When a wedding, festival or emergency comes, the whole community works together — some "
     "cook, some decorate, some arrange water and seats. During floods, neighbours rescue each "
     "other and share food. Alone we can do little; together we can do a lot."),
]

_GEOGRAPHY = [
    (2, "directions",
     "The Sun rises in the EAST and sets in the WEST. Stand facing the rising sun: east is in "
     "front, west is behind, north is on your left and south is on your right. The four main "
     "directions are north, south, east and west."),
    (2, "land and water around us",
     "Land comes in many forms: high mountains, flat plains, raised plateaus, and sandy "
     "deserts. Water bodies are oceans (very big), seas, rivers, lakes and ponds. People build "
     "villages, towns and cities on land, and many cities grow near rivers because water is "
     "needed for everything."),
    (3, "maps",
     "A map is a drawing of a place as seen from above. Maps show roads, rivers, mountains, "
     "cities and countries on paper. Blue stands for water, green for plains and forests, "
     "brown for mountains. A map is much smaller than the real place, so map-makers use a "
     "scale: for example, 1 cm on the map may mean 10 km on the ground."),
    (3, "the globe",
     "A globe is a small round model of the Earth. The Earth looks blue from space because "
     "about two-thirds of it is covered with water. Huge land areas are called continents — "
     "there are seven — and the biggest water bodies are the five oceans."),
    (4, "weather, climate and maps of India",
     "Different places in India have different weather: Rajasthan's deserts are hot and dry, "
     "Kashmir's mountains are snowy, Kerala's coast gets heavy monsoon rain, and the Himalayan "
     "slopes stay cool in summer. Physical maps show these mountains, rivers and plains; "
     "political maps show states, their boundaries and capitals."),
]

_INDIA = [
    (1, "our country India",
     "We live in India, our country. India's flag has three colours: saffron at the top, white "
     "in the middle and green at the bottom, with a blue wheel called the Ashoka Chakra in the "
     "centre. New Delhi is the capital of India."),
    (2, "national symbols of India",
     "National animal: the Royal Bengal Tiger. National bird: the peacock. National flower: "
     "the lotus. National fruit: the mango. National tree: the banyan. National anthem: "
     "'Jana Gana Mana', written by Rabindranath Tagore. We stand respectfully when it is sung."),
    (2, "states and cities",
     "India is a big country made of many states. Each state has its own capital city. Some "
     "well-known states and capitals: Maharashtra - Mumbai, Karnataka - Bengaluru, West Bengal "
     "- Kolkata, Tamil Nadu - Chennai, Rajasthan - Jaipur, Uttar Pradesh - Lucknow, Gujarat - "
     "Gandhinagar, Kerala - Thiruvananthapuram. And the national capital is New Delhi."),
    (3, "rivers and mountains of India",
     "The Himalayas stand like a great wall in the north of India; they are the world's "
     "highest mountains. Important rivers flow across the land: the Ganga in the north, the "
     "Yamuna which joins the Ganga at Prayagraj, the Godavari and Krishna in the south, the "
     "Narmada in central India, and the Brahmaputra in the north-east. Rivers give water for "
     "farming and are called the lifelines of India."),
    (3, "languages and unity",
     "People in India speak many languages — Hindi, Bengali, Tamil, Telugu, Marathi, Kannada, "
     "Gujarati, Malayalam, Odia, Punjabi, Assamese and many more. Different foods, dresses and "
     "dances make India colourful. Despite all the differences, we are one nation — this is "
     "called unity in diversity."),
    (4, "our neighbours",
     "India is in the continent of Asia. Its neighbouring countries are Pakistan and "
     "Afghanistan to the north-west, China, Nepal and Bhutan to the north, and Bangladesh and "
     "Myanmar to the east. Sri Lanka lies to the south, across the sea. India is surrounded by "
     "the Arabian Sea on the west, the Bay of Bengal on the east, and the Indian Ocean to the south."),
]

_HISTORY_CULTURE = [
    (3, "monuments of India",
     "The Taj Mahal at Agra, built by Emperor Shah Jahan in memory of his wife Mumtaz Mahal, "
     "is one of the most beautiful buildings in the world and a Wonder of the World. The Red "
     "Fort in Delhi, the Qutub Minar, the Gateway of India in Mumbai, the Charminar in "
     "Hyderabad and Konark's Sun Temple show the skill of builders from long ago. We must "
     "protect monuments and never write on their walls."),
    (3, "great people of India",
     "Mahatma Gandhi taught the world truth and non-violence and led India's freedom movement; "
     "we call him the Father of the Nation. Jawaharlal Nehru, India's first Prime Minister, "
     "loved children — his birthday is celebrated as Children's Day. Dr. B.R. Ambedkar framed "
     "India's Constitution. Rabindranath Tagore wrote our national anthem, and Dr. A.P.J. Abdul "
     "Kalam, the 'Missile Man', became the President and inspired millions of students."),
    (3, "long, long ago",
     "Thousands of years ago, people lived in caves and hunted animals for food. Slowly they "
     "learnt to farm, keep animals, and build villages near rivers. Great cities grew on the "
     "banks of the Indus river more than 4,000 years ago — one of the world's oldest "
     "civilisations. Kings and kingdoms came and went, and finally, after long struggle, India "
     "became free in 1947."),
    (4, "festivals of India",
     "India celebrates many festivals, each with its own special food, clothes and customs. "
     "Diwali is the festival of lights; Holi welcomes spring with colours; Eid is celebrated "
     "with prayers, sevaiyan and hugs; Christmas celebrates the birth of Jesus Christ with "
     "carols and cakes; Baisakhi and Onam and Pongal are harvest festivals, thanking nature "
     "for food; Durga Puja and Navratri honour the goddess; and Guru Nanak Jayanti marks the "
     "birth of the first Sikh Guru. Festivals are times to share sweets, meet family and "
     "friends, and respect everyone's celebrations."),
    (4, "respecting all communities",
     "India is home to people of many religions and communities — Hindus, Muslims, Christians, "
     "Sikhs, Buddhists, Jains and others. Each community prays in its own way: in temples, "
     "mosques, churches, gurdwaras and other places of worship. Learning about each other's "
     "festivals and customs with respect keeps our country peaceful and strong."),
]

_TRANSPORT_COMM = [
    (1, "means of transport",
     "We travel by road (car, bus, bicycle, auto-rickshaw), by rail (trains), by water (boats "
     "and ships) and by air (aeroplanes and helicopters). An ambulance carries sick people "
     "quickly to hospital, and a fire engine carries firemen with ladders and water."),
    (2, "road safety",
     "Walk on the footpath. Cross the road at the zebra crossing after the traffic light turns "
     "red for vehicles. Look left, then right, then left again before crossing. Never run "
     "across the road or play on it. Wear a helmet on a two-wheeler and a seat belt in a car. "
     "Safety rules are not to trouble us — they are to save our lives."),
    (3, "communication",
     "Communication means sharing news and feelings. Long ago people sent messages by birds, "
     "drums and letters carried by runners. Then came the telegraph, telephone and post. Today "
     "mobile phones and the internet carry messages across the world in seconds, and video "
     "calls let us see faraway family. Even now, nothing feels as special as a handwritten letter."),
    (4, "how transport changed life",
     "In the past, people walked or used bullock carts; a journey of days now takes hours. "
     "Trains and trucks carry grain from farms to faraway cities. Ships carry heavy goods "
     "across oceans, and planes cross countries in a few hours. Good transport connects people, "
     "spreads trade and brings the country together — but it also causes pollution, so cleaner "
     "options like buses, cycles and electric vehicles matter more every year."),
]


def build() -> list[dict]:
    out: list[dict] = []
    for group in (_FAMILY_COMMUNITY, _SCHOOL_OCCUPATIONS, _GEOGRAPHY, _INDIA,
                  _HISTORY_CULTURE, _TRANSPORT_COMM):
        for stage, topic, text in group:
            out.append(item(stage, "explanation", f"{topic.capitalize()}.\n{text}"))
            q = topic[0].upper() + topic[1:]
            out.append(item(stage, "qa",
                            f"Question: {q}\nAnswer: {text}"))
    # Quick recall drills.
    drills = [
        (1, "Question: Who teaches you in school?\nAnswer: Our teachers teach us in school. The principal guides the whole school."),
        (1, "Question: What colour is our national flag?\nAnswer: Our flag has saffron, white and green stripes with a blue Ashoka Chakra in the middle."),
        (2, "Question: Which direction does the sun rise from?\nAnswer: The Sun rises in the east and sets in the west."),
        (2, "Question: What is the national animal of India?\nAnswer: The Royal Bengal Tiger is India's national animal."),
        (2, "Question: Where should we cross a road?\nAnswer: At the zebra crossing, when the traffic light is red for vehicles, looking left-right-left first."),
        (3, "Question: What is a map?\nAnswer: A map is a drawing of a place seen from above, showing roads, rivers, mountains and cities on paper."),
        (3, "Question: What is the capital of India?\nAnswer: New Delhi is the capital of India."),
        (3, "Question: Which mountain range is in the north of India?\nAnswer: The Himalayas are in the north of India — the highest mountains in the world."),
        (4, "Question: Why is the Ganga called the lifeline of northern India?\nAnswer: Because its water is used for farming, drinking and daily life by millions of people living along its banks."),
        (4, "Question: What does 'unity in diversity' mean?\nAnswer: India has many languages, religions, foods and dresses, yet all Indians live together as one nation."),
    ]
    for stage, text in drills:
        out.append(item(stage, "qa", text))

    # -- Expanded parametric practice (foundation-training scale-up) ---------
    out += _states_capitals(n=230)
    out += _national_symbols(n=120)
    out += _occupations_places(n=170)
    out += _festivals_india(n=150)
    out += _landmarks_rivers(n=140)
    out += _civics_community(n=130)
    out += _direction_maps_drills(n=110)
    return out


# ===========================================================================
# Expanded parametric practice — foundation-training scale-up.
# ===========================================================================
import random as _random

_rng = _random.Random(20240505)


def _qa(stage: int, q: str, a: str) -> dict:
    return item(stage, "qa", f"Question: {q}\nAnswer: {a}")


def _states_capitals(n: int = 150) -> list[dict]:
    table = [
        ("Uttar Pradesh", "Lucknow"), ("Maharashtra", "Mumbai"), ("Karnataka", "Bengaluru"),
        ("Tamil Nadu", "Chennai"), ("West Bengal", "Kolkata"), ("Gujarat", "Gandhinagar"),
        ("Rajasthan", "Jaipur"), ("Kerala", "Thiruvananthapuram"), ("Bihar", "Patna"),
        ("Odisha", "Bhubaneswar"), ("Assam", "Dispur"), ("Punjab", "Chandigarh"),
        ("Haryana", "Chandigarh"), ("Madhya Pradesh", "Bhopal"), ("Telangana", "Hyderabad"),
        ("Andhra Pradesh", "Amaravati"), ("Goa", "Panaji"), ("Sikkim", "Gangtok"),
        ("Meghalaya", "Shillong"), ("Manipur", "Imphal"), ("Tripura", "Agartala"),
        ("Nagaland", "Kohima"), ("Mizoram", "Aizawl"), ("Arunachal Pradesh", "Itanagar"),
        ("Uttarakhand", "Dehradun"), ("Himachal Pradesh", "Shimla"), ("Jharkhand", "Ranchi"),
        ("Chhattisgarh", "Raipur"),
    ]
    out = []
    for _ in range(n):
        state, capital = _rng.choice(table)
        if _rng.random() < 0.5:
            out.append(_qa(3, _rng.choice([
                f"What is the capital of {state}?",
                f"Name the capital city of {state}.",
            ]), f"The capital of {state} is {capital}."))
        else:
            out.append(_qa(3, _rng.choice([
                f"{capital} is the capital of which Indian state?",
                f"Which state has {capital} as its capital?",
            ]), f"{capital} is the capital of {state}."))
    return out


def _national_symbols(n: int = 60) -> list[dict]:
    facts = [
        (2, "What is the national animal of India?", "The Royal Bengal Tiger is the national animal of India."),
        (2, "What is the national bird of India?", "The peacock is the national bird of India."),
        (2, "What is the national flower of India?", "The lotus is the national flower of India."),
        (2, "What is the national fruit of India?", "The mango is the national fruit of India."),
        (3, "What is the national tree of India?", "The banyan tree is the national tree of India."),
        (3, "What is the national game of India?", "Hockey is considered the national game of India."),
        (3, "What do the three colours of our flag mean?", "Saffron stands for courage and sacrifice, white for peace and truth, and green for growth and fertility."),
        (3, "What is written at the bottom of our national emblem?", "Satyameva Jayate — 'Truth alone triumphs' — is written below the Lion Capital of Ashoka."),
        (3, "Who wrote our national anthem?", "Rabindranath Tagore wrote our national anthem, 'Jana Gana Mana'."),
        (3, "What is the national anthem of India?", "The national anthem of India is 'Jana Gana Mana', written by Rabindranath Tagore."),
        (3, "What is the national song of India?", "The national song of India is 'Vande Mataram', written by Bankim Chandra Chatterjee."),
        (4, "What is the national aquatic animal of India?", "The Ganges river dolphin is the national aquatic animal of India."),
        (4, "When do we celebrate Independence Day?", "We celebrate Independence Day on 15 August every year."),
        (4, "When do we celebrate Republic Day?", "We celebrate Republic Day on 26 January every year."),
        (4, "Whose birthday is celebrated as Children's Day in India?", "Children's Day is celebrated on 14 November, the birthday of Pandit Jawaharlal Nehru."),
        (4, "Who is called the Father of the Nation in India?", "Mahatma Gandhi is called the Father of the Nation. His birthday, 2 October, is Gandhi Jayanti."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _occupations_places(n: int = 110) -> list[dict]:
    table = [
        ("teacher", 1, "school", "teaches students"),
        ("doctor", 1, "hospital or clinic", "treats sick people"),
        ("farmer", 1, "fields", "grows crops for us"),
        ("postman", 2, "post office", "brings letters and parcels"),
        ("chef", 2, "kitchen or restaurant", "cooks delicious food"),
        ("pilot", 2, "aeroplane", "flies aeroplanes"),
        ("tailor", 2, "tailor shop", "stitches clothes"),
        ("carpenter", 2, "workshop", "makes furniture from wood"),
        ("electrician", 3, "homes and offices", "repairs electrical fittings"),
        ("dentist", 3, "dental clinic", "takes care of our teeth"),
        ("librarian", 3, "library", "manages and issues books"),
        ("firefighter", 3, "fire station", "puts out fires and rescues people"),
        ("police officer", 2, "police station", "catches thieves and keeps us safe"),
        ("fisherman", 2, "sea or river bank", "catches fish for us"),
        ("vet", 4, "animal clinic", "treats sick animals"),
        ("architect", 4, "office and building sites", "designs buildings"),
    ]
    out = []
    for _ in range(n):
        who, stage, where, job = _rng.choice(table)
        style = _rng.randrange(3)
        if style == 0:
            out.append(_qa(stage, f"Where does a {who} work?",
                           f"A {who} works in {where}."))
        elif style == 1:
            out.append(_qa(stage, f"What does a {who} do?",
                           f"A {who} {job}."))
        else:
            out.append(_qa(stage, f"Who {job}s — name the community helper."
                           if job.endswith("s") else f"Who does the work of {job[:-1]}ing? Name the helper.",
                           f"A {who} {job}."))
    return out


def _festivals_india(n: int = 90) -> list[dict]:
    facts = [
        (2, "Which festival is called the festival of lights?", "Diwali is called the festival of lights. We light diyas and share sweets."),
        (2, "Which festival is celebrated with colours?", "Holi is celebrated with colours. People play with gulal and eat gujiya."),
        (2, "Which festival is known for kite flying in January?", "Makar Sankranti is famous for kite flying. People also make til-gud sweets."),
        (3, "Which festival celebrates the birth of Lord Krishna?", "Janmashtami celebrates the birth of Lord Krishna. People make little cradles and do dahi-handi."),
        (3, "Which harvest festival of Tamil Nadu thanks the Sun?", "Pongal is the Tamil harvest festival that thanks the Sun and nature."),
        (3, "Which festival celebrates the bond between brothers and sisters?", "Raksha Bandhan celebrates the bond — sisters tie a rakhi on their brothers' wrists."),
        (3, "What is Eid-ul-Fitr known for?", "Eid-ul-Fitr comes after the holy month of Ramzan. People pray, hug each other and enjoy sewaiyan."),
        (3, "What is Christmas celebrated for?", "Christmas celebrates the birth of Jesus Christ on 25 December. People decorate trees and share gifts."),
        (4, "Why is Dussehra celebrated?", "Dussehra marks the victory of good over evil — Lord Rama's victory over Ravana. Effigies of Ravana are burnt."),
        (4, "What is Onam famous for?", "Onam is Kerala's harvest festival with flower carpets (pookalam), boat races and the grand Onam Sadhya meal."),
        (4, "Why do people celebrate Guru Nanak Jayanti?", "It celebrates the birthday of Guru Nanak Dev Ji, the first Guru of the Sikhs, with prayers and langar."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _landmarks_rivers(n: int = 80) -> list[dict]:
    facts = [
        (3, "In which city is the Taj Mahal?", "The Taj Mahal is in Agra, on the banks of the Yamuna river."),
        (3, "Who built the Taj Mahal and why?", "Emperor Shah Jahan built the Taj Mahal in memory of his wife Mumtaz Mahal."),
        (3, "Which is the longest river in India?", "The Ganga is the longest river flowing within India."),
        (3, "Which river flows through Delhi?", "The Yamuna flows through Delhi."),
        (3, "Which is the highest mountain range in the world?", "The Himalayas are the highest mountain range in the world."),
        (3, "Which ocean lies to the south of India?", "The Indian Ocean lies to the south of India."),
        (3, "What is the capital of India?", "New Delhi is the capital of India."),
        (4, "Which city is called the Pink City?", "Jaipur is called the Pink City."),
        (4, "Which Indian city is called the City of Joy?", "Kolkata is called the City of Joy."),
        (4, "What is the Thar?", "The Thar is a big hot desert in the north-west of India, mostly in Rajasthan."),
        (4, "Which strait or water body separates India from Sri Lanka?", "The Palk Strait separates India from Sri Lanka."),
        (4, "Why are rivers like the Ganga important for farmers?", "River water is used to water the fields, so farming flourishes along the river banks."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _civics_community(n: int = 80) -> list[dict]:
    facts = [
        (1, "Who is the head of a school?", "The principal is the head of a school."),
        (2, "Why do we follow rules on the road?", "Rules keep everyone safe — traffic lights and zebra crossings prevent accidents."),
        (2, "Who keeps our city clean?", "Municipal workers (safai karamcharis) keep our city clean; we must also use dustbins and not litter."),
        (2, "What does a sarpanch do?", "A sarpanch is the head of a village panchayat and helps solve village problems."),
        (3, "What is a family?", "A family is a group of people who live together or stay close, love and care for each other."),
        (3, "What is a neighbourhood?", "A neighbourhood is the area near our home, with the people and places around us."),
        (3, "Why is voting important?", "Voting lets people choose their leaders. Every citizen's vote decides who will make decisions for everyone."),
        (4, "What are fundamental duties in simple words?", "Fundamental duties are the good things every citizen should do — respect the flag and anthem, keep the country clean, protect public property and help others."),
        (4, "What is 'unity in diversity'?", "India has many languages, religions, foods and dresses, yet all Indians live together as one nation."),
        (4, "Why should we respect all jobs and workers?", "Every worker's job helps society — a farmer, a doctor, a sweeper and a teacher all do important work, so all deserve equal respect."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(facts)
        out.append(_qa(stage, q, a))
    return out


def _direction_maps_drills(n: int = 70) -> list[dict]:
    out = []
    for _ in range(n):
        style = _rng.randrange(3)
        if style == 0:
            out.append(_qa(2, _rng.choice([
                "In which direction does the sun rise?",
                "Which direction does the sun rise from?",
            ]), "The sun rises in the east."))
        elif style == 1:
            face = _rng.choice(["east", "west", "north", "south"])
            behind = {"east": "west", "west": "east", "north": "south", "south": "north"}[face]
            out.append(_qa(3, f"If you face {face}, which direction is behind you?",
                           f"If you face {face}, then {behind} is behind you."))
        else:
            out.append(_qa(4, _rng.choice([
                "On a map, which direction is at the top?",
                "Which direction is shown at the top of most maps?",
            ]), "On most maps, north is at the top, south at the bottom, east on the right and west on the left."))
    return out
