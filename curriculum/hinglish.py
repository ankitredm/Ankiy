"""Hinglish foundation: natural Roman-script Hindi-English conversation and
understanding.

Style rule: Hinglish here is NATURAL code-mixing, not rigid translation.
Sentences freely mix Hindi words (romanised) with English words, the way
real Class 1-4 children hear and speak at home and school:
    "Plants ko sunlight ki zarurat kyu hoti hai?"
    "2 apples the aur 3 apples aur mil gaye, total kitne hue?"
    "Mujhe simple words mein samjhao."
    "Ye kaise kaam karta hai?"
"""

from __future__ import annotations


def item(stage: int, kind: str, text: str) -> dict:
    return {"text": text, "category": "hinglish", "stage": stage, "kind": kind}


def build() -> list[dict]:
    out: list[dict] = []

    # -- Simple everyday Q&A (stage 1-2) ------------------------------------
    simple_qa = [
        (1, "Ye kya hai?", "Ye ek pencil hai. Pencil se hum likhte hain aur drawing banate hain."),
        (1, "Tumhara naam kya hai?", "Mera naam Rahul hai. Main Class 1 mein padhta hoon."),
        (1, "Aaj mausam kaisa hai?", "Aaj mausam sunny hai. Suraj nikla hai aur halki hawa chal rahi hai."),
        (1, "Aapko kaunsa fruit pasand hai?", "Mujhe mango sabse zyada pasand hai. Ye sweet aur juicy hota hai."),
        (1, "Cow humein kya deti hai?", "Cow humein doodh deti hai. Doodh se hum milk, curd aur paneer banate hain."),
        (1, "School kab jate ho?", "Main roz subah school jata hoon. School bag lekar bus stop pe wait karta hoon."),
        (2, "Humi gaon mein kya kya dekh sakte hain?", "Gaon mein khet, tube well, mango trees aur bahut saare animals dekh sakte hain. Log wahan farming karte hain."),
        (2, "Barish hone se kya hota hai?", "Barish se kheton mein paani bharta hai, nadiyan bharti hain aur mausam thanda ho jata hai. Farmers crop ke liye khush hote hain."),
        (2, "TV kaise chalta hai?", "TV electricity se chalta hai. Switch on karte hi screen pe pictures aur sound aate hain."),
        (2, "Doctor kab jaate hain?", "Jab hum bimaar padte hain — bukhar, khansi ya pet dard ho — toh hum doctor ke paas jaate hain. Doctor dawa dete hain aur theek kar dete hain."),
    ]
    for stage, q, a in simple_qa:
        out.append(item(stage, "qa", f"Question: {q}\nAnswer: {a}"))

    # -- Explanation requests ("simple words mein samjhao") ------------------
    explanations = [
        (2, "Mujhe simple words mein samjhao ki barish kaise hoti hai.",
         "Dekho, jab suraj garam hota hai, toh samundar aur nadiyon ka paani vapour ban ke upar uthta hai. "
         "Upar ye vapour thanda hoke chhote chhote paani ke boond jaisa badal banata hai. "
         "Jab ye boondein bahut bhaari ho jaati hain, toh barish ke roop mein gir jaati hain. Simple!"),
        (2, "Mujhe simple words mein samjhao ki humein sabzi kyu khani chahiye.",
         "Sabzi mein vitamins aur minerals hote hain jo humein healthy rakhte hain. "
         "Inse humari eyes sharp rehti hain, body strong banti hai aur bimaariyan humein jaldi nahi lagti. "
         "Isliye har meal mein thodi sabzi zaroor khao."),
        (3, "Ye kaise kaam karta hai — torch?",
         "Torch ke andar batteries hoti hain. Batteries ek chhoti si current deti hai bulb ko, "
         "aur bulb us current se roshni deta hai. Switch off karte hi current band, toh light bhi band. "
         "Matlab: battery + bulb + switch milke torch ka kaam karte hain."),
        (3, "Plants ko sunlight ki zarurat kyu hoti hai?",
         "Plants sunlight se apna khana khud banate hain. Ye process photosynthesis kehlata hai. "
         "Leaves sunlight, paani aur air ko mila ke glucose banati hain, aur hum oxygen bhi dete hain. "
         "Sunlight ke bina plants green nahi reh paate aur dheere dheere murjha jaate hain."),
        (3, "Mujhe simple words mein samjhao ki ghadi kaam kaise karti hai.",
         "Purani ghadi mein chhote chhote gears lage hote hain jo ek ke baad ek ghoomte hain, "
         "aur unke saath haath (hands) bhi ghoomte hain. Bada haath minutes dikhata hai, "
         "chhota haath hours. Aajkal ki ghadi battery ya mobile ki tarah quartz se chalti hai "
         "aur hamesha second minute ghoomti rehti hai."),
        (4, "Mujhe simple words mein samjhao ki rainbow kyu banta hai.",
         "Jab barish ke baad suraj nikalta hai, toh hawa mein paani ki boondein reh jaati hain. "
         "Suraj ki roshni jab in boondon se guzarti hai, toh vo seven colours mein toot jaati hai. "
         "Yehi colours milke aasman mein ek gol arch banate hain — red se lekar violet tak. "
         "Isi ko rainbow kehte hain."),
        (4, "Ye kaise kaam karta hai — fridge?",
         "Fridge ke andar ek gas hoti hai jo heat ko andar se kheench bahar nikalti hai. "
         "Isse andar ka temperature low rehta hai aur khana jaldi kharab nahi hota. "
         "Cold cheezon mein bacteria ki growth slow ho jaati hai, isliye doodh aur sabzi dinon tak fresh rehti hai."),
    ]
    for stage, q, a in explanations:
        out.append(item(stage, "explanation", f"Question: {q}\nAnswer: {a}"))

    # -- Conversations --------------------------------------------------------
    conversations = [
        (1, "Ravi: Mummy, mujhe bhookh lagi hai.\n"
            "Mummy: Beta, kitchen mein fruits rakhe hain. Ek apple kha lo.\n"
            "Ravi: Apple khatta hai!\n"
            "Mummy: Thoda khatta hai, lekin healthy hai. Ismein vitamins hote hain jo tumhe strong banate hain.",
         ),
        (2, "Priya: Papa, school mein aaj science ki class thi.\n"
            "Papa: Achha? Kya seekha aaj?\n"
            "Priya: Teacher ne bataya ki butterfly pehle caterpillar hoti hai. Phir cocoon mein badalti hai.\n"
            "Papa: Wow! Aur cocoon se nikal ke butterfly ban jaati hai. Isko metamorphosis kehte hain.\n"
            "Priya: Haan! Kal main drawing bana ke dikhaungi — egg, caterpillar, cocoon aur butterfly."),
        (2, "Aman: Kal cricket khelenge?\n"
            "Rohit: Haan, par pehle homework complete karna padega.\n"
            "Aman: Theek hai. Main maths finish karke 4 baje tak aa jaunga.\n"
            "Rohit: Main bat lekar park mein wait karunga. Late mat hona!"),
        (3, "Doctor: Batao beta, kya takleef hai?\n"
            "Neha: Sir, subah se pet dard ho raha hai aur man nahi kar raha khane ka.\n"
            "Doctor: Kya tumne bahar ka khaya tha ya zyada ice cream?\n"
            "Neha: Haan sir, do ice cream kha li thi.\n"
            "Doctor: Dekha! Zyada thanda khaane se pet kharab ho jata hai. Ye dawa lo aur paani zyada piyo. "
            "Agle se dhyan rakhna, theek hai?\n"
            "Neha: Ji sir. Thank you!"),
        (3, "Anu: Didi, ye map mein blue colour kya hai?\n"
            "Didi: Blue colour paani dikhata hai — samundar, nadiyan aur lakes.\n"
            "Anu: Aur green?\n"
            "Didi: Green matlab forest aur khet. Brown mountains hoti hain, aur black dots cities.\n"
            "Anu: Matlab chhoti si paper par poora India aa gaya! Kamaal hai."),
        (4, "Grandfather: Beta, aaj kal bacche mobile pe zyada time dete hain.\n"
            "Arjun: Haan dadaji, par hum sirf games nahi khelte. Studies ke liye bhi use karte hain.\n"
            "Grandfather: Achha. Par aankhon ka dhyan rakhna zaroori hai. Har ek ghante mein break lo, "
            "bahar khelo, aur seedhe baith ke padho.\n"
            "Arjun: Bilkul dadaji. Aaj ke baad sirf ek hour use karunga, phir cricket ke liye chale jaaunga."),
    ]
    for stage, convo in conversations:
        out.append(item(stage, "dialogue", f"Conversation:\n{convo}"))

    # -- Maths in Hinglish -----------------------------------------------------
    math_hinglish = [
        (1, "2 apples the aur 3 apples aur mil gaye, total kitne hue?\n"
            "2 + 3 = 5. Total 5 apples hue. Simple addition se answer mil gaya!"),
        (1, "Mere paas 5 toffees thi. Maine 2 apne bhai ko de di. Ab kitni bachi?\n"
            "5 - 2 = 3. Ab mere paas 3 toffees bachi hain."),
        (2, "Ek box mein 6 pencils hain. Aise 3 box hai. Total kitni pencils?\n"
            "6 + 6 + 6 = 18, yaani 6 x 3 = 18. Total 18 pencils hui."),
        (2, "12 laddoo ko 4 bachcho mein barabar baantna hai. Har bachche ko kitne milenge?\n"
            "12 ko 4 se divide karo: 12 ÷ 4 = 3. Har bachche ko 3 laddoo milenge."),
        (3, "Ek pen 15 rupaye ka hai aur ek copy 25 rupaye ki. Dono ka total?\n"
            "15 + 25 = 40. Dono cheezein milke 40 rupaye ki hui."),
        (3, "250 gram doodh aur 750 gram doodh mila ke kitne gram hue? Kitne kilogram bhi batao.\n"
            "250 + 750 = 1000 gram. Aur 1000 gram = 1 kilogram. Total 1 kg doodh hua."),
        (3, "Ek chocolate ki keemat 20 rupaye hai. 5 chocolate lene mein kitne rupaye lagenge?\n"
            "20 x 5 = 100. 5 chocolate ke liye 100 rupaye lagenge."),
        (4, "Ramesh ke paas 100 rupaye the. Usne 45 rupaye ki book aur 30 rupaye ki paint brush kharidi. Kitne rupaye bache?\n"
            "Pehle dono cheezon ka total: 45 + 30 = 75 rupaye. Phir 100 - 75 = 25. "
            "Ramesh ke paas 25 rupaye bache."),
        (4, "Ek class mein 40 students hain. Unme se 3/4 students present the. Kitne students present the?\n"
            "40 ko 4 se divide karo: 10. Phir 3 x 10 = 30. Matlab 30 students present the "
            "aur 40 - 30 = 10 students absent the."),
        (4, "Ek train 60 km har ek ghante mein chalti hai. 3 ghante mein kitni distance cover karegi?\n"
            "60 x 3 = 180. Train 3 ghante mein 180 km chalegi."),
    ]
    for stage, text in math_hinglish:
        out.append(item(stage, "worked", text))

    # -- Science / EVS in Hinglish ---------------------------------------------
    science_hinglish = [
        (1, "Murgi humein kya deti hai? Murgi humein anda deti hai. Ande mein protein hota hai jo body ko strong banata hai."),
        (1, "Pani peene se kya hota hai? Pani pine se humara pet clean rehta hai aur body fresh rehti hai. Roz saaf paani piyo."),
        (2, "Cow, goat aur buffalo ko kya kehte hain? Inko domestic animals kehte hain kyunki ye humare ghar ke paas rehti hain aur humein doodh deti hain. Lion aur tiger wild animals hain."),
        (2, "Ped humein kya kya dete hain? Ped humein oxygen, fruits, wood aur shade dete hain. Isliye ped kaatna galat hai aur ped lagana achha hai."),
        (3, "Water cycle simple words mein: suraj paani ko garam karke vapour banata hai, vapour badal banta hai, badal barish ban ke wapas aate hain. Phir se suraj... yehi cycle chalta rehta hai!"),
        (3, "Human body mein dil kahaan hai aur kya karta hai? Dil chest ke left side mein hota hai. Ye khoon ko poore body mein pump karta hai, din raat bina rukey. Isliye dil sabse mehnati organ hai."),
        (4, "Pollution kya hota hai? Jab dhuan, kachra ya chemicals air aur paani ko ganda kar dete hain, toh use pollution kehte hain. Vehicles ka dhuan air pollution karta hai aur kachra paani ko ganda karta hai. Pollution se bimaariyan badhti hain."),
        (4, "Seasons kyu badalte hain? Earth suraj ke chakkar lagati hai aur thodi tilted rehti hai. Isliye kabhi humara hissa suraj ke paas hota hai (summer) aur kabhi door (winter). Isse seasons bante hain."),
    ]
    for stage, text in science_hinglish:
        out.append(item(stage, "qa", text))

    # -- Understanding / comprehension in Hinglish ------------------------------
    comprehension_hinglish = [
        (2, "Ye chhota passage padho: 'Sita roz subah 6 baje uthti hai. Woh pehle brush karti hai, "
            "phir yoga karti hai. Uske baad breakfast karti hai aur school chali jaati hai.'\n"
            "Question: Sita sabse pehle kya karti hai?\n"
            "Answer: Sita sabse pehle brush karti hai, phir yoga karti hai."),
        (3, "Passage: 'Golu ek chhota kutta hai jo hamesha garden mein khelta hai. Ek din usne "
            "garden mein ek chidiya ka bacha girra dekha. Golu ne chilla kar uska dhyan bada "
            "chidiya ko dikhaya.'\n"
            "Question: Golu ne chidiya ke bachhe ke liye kya kiya?\n"
            "Answer: Golu ne chillakar bade chidiye ka dhyan bachhe ki taraf dikhaya — matlab usne help kiya."),
        (4, "Passage: 'Rekha ka gaon pahadon ke beech hai. Gaon mein school 5 km door hai, "
            "lekin phir bhi Rekha roz padhne jaati hai kyunki woh badi hokar teacher banna chahti hai.'\n"
            "Question: Rekha roz school kyu jaati hai jabki school door hai?\n"
            "Answer: Kyunki Rekha badi hokar teacher banna chahti hai aur padhai ke liye school jaana zaroori hai. "
            "Yeh dikhati hai ki uska goal clear hai."),
    ]
    for stage, text in comprehension_hinglish:
        out.append(item(stage, "comprehension", text))

    # -- Instructions in Hinglish -----------------------------------------------
    instructions_hinglish = [
        (1, "Haath dhona — simple steps:\nStep 1: Pani se haath gile karo.\nStep 2: Soap lo aur foam banao.\n"
            "Step 3: 20 second tak achhe se rub karo.\nStep 4: Sab soap pani se dho do.\nStep 5: Clean towel se sukhao."),
        (2, "School bag ready karna:\nStep 1: Timetable dekho kal kaunse subjects hain.\nStep 2: Uske hisaab se books aur copies nikalo.\n"
            "Step 3: Pencil box, tiffin aur water bottle rakho.\nStep 4: Zip band karo aur bag darwaze ke paas rakh do. Done!"),
        (3, "Ek potted plant ko care kaise karein:\nStep 1: Roz subah thoda pani do — zyada nahi, warna root sad jaata hai.\n"
            "Step 2: Plant ko sunlight wali jagah rakho.\nStep 3: Hafte mein ek baar mitti halki se khurpi se kodo.\n"
            "Step 4: Sukhi patiyaan hatao taaki naya growth ho."),
    ]
    for stage, text in instructions_hinglish:
        out.append(item(stage, "instructions", text))

    # -- Hinglish reasoning -------------------------------------------------------
    reasoning_hinglish = [
        (2, "Agar aaj Monday hai, toh kal kaunsa din hoga? Aaj Monday hai, toh kal Tuesday hoga. Din order mein chalte hain: Monday, Tuesday, Wednesday..."),
        (3, "Radha Ramesh se lambi hai, par Sunita Radha se lambi hai. Sabse lambi kaun hai? "
            "Dekho: Sunita > Radha > Ramesh. Matlab sabse lambi Sunita hai."),
        (3, "Ek bucket mein 8 litre paani hai. Tumne 3 litre nikal liye, phir 2 litre daal diya. Ab kitna paani hai?\n"
            "8 - 3 = 5. Phir 5 + 2 = 7. Ab bucket mein 7 litre paani hai."),
        (4, "Agar sab students library mein jaate hain toh woh shor nahi karte. Mohan library mein hai. "
            "Toh kya Mohan shor kar raha hai?\n"
            "Nahi. Kyunki library mein sab shor nahi karte, aur Mohan library mein hai, "
            "toh Mohan shor nahi kar raha hoga."),
        (4, "Mujhe simple words mein samjhao ki 'save electricity' kyu zaroori hai. "
            "Electricity banane ke liye coal jalti hai, jisse dhuan nikalta hai. "
            "Kam electricity use karenge toh kam coal jalega, air clean rahegi "
            "aur bijli ka bill bhi kam aayega. Fans aur lights band karna bhi desh ki help hai."),
    ]
    for stage, text in reasoning_hinglish:
        out.append(item(stage, "reasoning", text))

    # -- Expanded parametric practice (foundation-training scale-up) ---------
    out += _hinglish_conversation(n=180)
    out += _hinglish_math_word_problems(n=320)
    out += _hinglish_explanations(n=130)
    out += _hinglish_comprehension(instances=18)
    out += _hinglish_instructions_reasoning(n=150)
    out += _hinglish_conversation_extra()
    out += _hinglish_explanations_extra()
    out += _hinglish_two_step_problems()

    return out


# ===========================================================================
# Expanded parametric practice — foundation-training scale-up.
# Natural Roman Hinglish: Hindi grammar patterns + English academic words,
# exactly jaise ghar aur school mein baat hoti hai.
# ===========================================================================
import random as _random

_rng = _random.Random(20240503)

_HNAMES = ["Ravi", "Priya", "Amit", "Neha", "Rohan", "Pooja", "Vikram", "Sunita",
           "Mohan", "Kavita", "Sameer", "Anita", "Deepa", "Manoj", "Rekha", "Sanjay"]
_HNAMES_F = ["Priya", "Neha", "Pooja", "Sunita", "Kavita", "Anita", "Deepa", "Rekha"]
_HTHINGS = ["apples", "toffees", "marbles", "pencils", "bananas", "biscuits",
            "balloons", "kitabon (books)", "chocolates", "stickers", "oranges", "rubbers"]
_HFRUITS = ["aam (mango)", "seb (apple)", "kela (banana)", "santra (orange)", "angoor (grapes)"]


def _qa(stage: int, kind: str, q: str, a: str) -> dict:
    return item(stage, kind, f"Question: {q}\nAnswer: {a}")


def _hinglish_conversation(n: int = 110) -> list[dict]:
    bank = [
        (1, "Tum aaj school kaise gaye?", "Main bus se school gaya. Bus stop pe mera dost bhi mila, hum saath mein gane gaate hue gaye."),
        (1, "Tumhara best friend kaun hai?", "Mera best friend Rohan hai. Woh hamesha meri help karta hai aur hum roz saath mein khelte hain."),
        (1, "Tumhe kaunsa game pasand hai?", "Mujhe cricket sabse zyada pasand hai. Main apne dost ke saath evening mein batting karta hoon."),
        (1, "Mummy kitchen mein kya banati hai?", "Mummy kitchen mein roti, sabzi aur dal banati hai. Sunday ko kabhi kabhi puri bhi banti hai."),
        (1, "Tum subah uthke kya karte ho?", "Main subah jaldi uthta hoon, brush karta hoon, aur phir thodi si exercise karta hoon."),
        (1, "Barish mein hum kya le jaate hain?", "Barish mein hum raincoat ya umbrella le jaate hain taaki bheege nahi."),
        (2, "Tumhare school mein kaun kaun se subjects padhaye jaate hain?", "Humare school mein English, Maths, Hindi, EVS aur drawing padhate hain. Maths mera favourite subject hai."),
        (2, "Zoo mein kya kya dekha?", "Zoo mein humne lion, monkey, hippo aur rang birange birds dekhe. Lion ko soya hua dekha toh thoda dar bhi laga."),
        (2, "Doctor ke paas kab jaate hain?", "Jab bukhar ya khansi hoti hai, tab doctor ke paas jaate hain. Doctor check karke dawa dete hain."),
        (2, "Kite kaise udte hain?", "Kite hawa ke saath udti hai. Manjha tight rakho, hawa aane pe kite upar chad jaati hai."),
        (2, "Tum ghar pe kaise help karte ho?", "Main apna bag khud set karta hoon, paani ke glass wapas rakhta hoon aur kabhi kabhi sabzi chilata bhi hoon."),
        (2, "Cycle chalana kaise seekhe?", "Pehle training wheels ke saath chalao, balance pakdo, phir dheere dheere bina support try karo. Girna bhi part hai seekhne ka!"),
        (3, "Water cycle simple words mein samjhao.", "Suraj ki garmi se paani vapour ban ke upar jaata hai, wahan badal banta hai, aur badal bhaari hoke barish ban ke gir jaate hain. Phir se wahi cycle chalti rehti hai."),
        (3, "Plants ko sunlight ki zarurat kyu hoti hai?", "Plants sunlight se apna khana khud banate hain — is process ko photosynthesis kehte hain. Bina sunlight ke plant dhire dhire kamzor pad jaata hai."),
        (3, "Humein exercise kyu karni chahiye?", "Exercise se body strong banti hai, dil healthy rehta hai aur mind fresh rehta hai. Isliye roz thodi running ya khelna zaroori hai."),
        (3, "Imli ka taste kaisa hota hai aur kyu?", "Imli khatti hoti hai kyunki usme natural acids hote hain. Aise hi nimbu bhi khatta hota hai."),
        (3, "Library mein kaise behave karna chahiye?", "Library mein sab quietly baith ke padhte hain. zor se baat nahi karte, kitabein pyaar se rakhte hain aur time pe wapas kar dete hain."),
        (4, "Pollution kam kaise kar sakte hain?", "Jyada se jyada trees lagao, public transport use karo, plastic kam karo aur bijli bachao. Chhote chhote steps milkar bada change laate hain."),
        (4, "Rainbow kaise banta hai?", "Barish ke baad jab suraj ki roshni paani ke boondo se guzarti hai, toh light sat rangon mein bikharti hai. Yehi rainbow hai — violet se lekar red tak."),
        (4, "Mujhe simple words mein samjhao ki moon ke phases kyu badalte hain.", "Moon khud roshni nahi deta, woh suraj ki light reflect karta hai. Moon Earth ke chakkar lagata hai, isliye humein har din uska alag shape dikhta hai — kuch din poora chand, kuch din sirf ek kala chand."),
        (4, "Agar dost sad ho toh kya karoge?", "Main usse puchoonga kya hua, uski baat dhyan se sunoonga, aur jitna possible hai help karunga. Kabhi kabhi sirf saath rehna bhi bahut hota hai."),
        (4, "Save water kyu zaroori hai?", "Clean water limited hai. Log, animals aur crops sabko paani chahiye. Isliye tap band karna, leak theek karwana aur paani reuse karna sabki zimmedari hai."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(bank)
        out.append(_qa(stage, "qa", q, a))
    return out


def _hinglish_math_word_problems(n: int = 220) -> list[dict]:
    out = []
    for _ in range(n):
        style = _rng.randrange(6)
        name = _rng.choice(_HNAMES)
        thing = _rng.choice(_HTHINGS)
        if style == 0:  # addition
            a = _rng.randint(6, 60); b = _rng.randint(4, 35)
            out.append(item(2, "word_problem",
                f"Question: {name} ke paas {a} {thing} the. Uske bhai ne {b} {thing} aur de diye. Ab total kitne {thing} hain?\n"
                f"Answer: {a} + {b} = {a + b}. Ab {name} ke paas {a + b} {thing} hain."))
        elif style == 1:  # subtraction
            a = _rng.randint(15, 90); b = _rng.randint(3, a - 2)
            out.append(item(2, "word_problem",
                f"Question: {name} ke paas {a} {thing} the. Usne {b} {thing} apne dost ko de diye. Ab kitne {thing} bache?\n"
                f"Answer: {a} - {b} = {a - b}. Ab {name} ke paas {a - b} {thing} bache hain."))
        elif style == 2:  # multiplication via price
            p = _rng.randint(3, 15); k = _rng.randint(3, 12)
            thing2 = _rng.choice(["pens", "glossy sheets", "candles", "toys", "erasers", "kites"])
            out.append(item(3, "word_problem",
                f"Question: Ek {thing2.rstrip('s')} ki keemat Rs {p} hai. {k} {thing2} lene mein total kitna kharcha aayega?\n"
                f"Answer: {k} × {p} = {k * p}. Total kharcha Rs {k * p} aayega."))
        elif style == 3:  # division/sharing
            k = _rng.randint(2, 9); each = _rng.randint(3, 12)
            total = k * each
            out.append(item(3, "word_problem",
                f"Question: {total} laddus ko {k} bachcho mein barabar baanta gaya. Har bachche ko kitne laddu milenge?\n"
                f"Answer: {total} ÷ {k} = {each}. Har bachche ko {each} laddu milenge."))
        elif style == 4:  # money change
            price = _rng.randrange(15, 90, 5)
            note = _rng.choice([100, 50, 200])
            while note <= price:
                note = _rng.choice([100, 200, 500])
            out.append(item(3, "word_problem",
                f"Question: Ek school bag ka price Rs {price} hai. Mummy ne Rs {note} ka note diya. Dukandaar kitne rupaye wapas dega?\n"
                f"Answer: {note} - {price} = {note - price}. Dukandaar Rs {note - price} wapas dega."))
        else:  # time
            h1 = _rng.randint(7, 10); h2 = h1 + _rng.randint(2, 6)
            out.append(item(3, "word_problem",
                f"Question: {name} ki school {h1} baje start hoti hai aur {h2} baje khatam hoti hai. School kitne ghante ki hoti hai?\n"
                f"Answer: {h1} se {h2} tak matlab {h2 - h1} ghante. School {h2 - h1} ghante ki hoti hai."))
    return out


def _hinglish_explanations(n: int = 90) -> list[dict]:
    bank = [
        (2, "Brush kyu karte hain?", "Brush karne se daanton ka bacteria saaf ho jaata hai. Subah aur raat ko brush karo, warna cavities ho sakti hain aur daant dard karenge."),
        (2, "Humein sabzi kyu khani chahiye?", "Sabzi mein vitamins aur fiber hote hain jo pet ko theek rakhte hain aur body ko strong banate hain."),
        (2, "Suraj zaroori kyu hai?", "Suraj se humein roshni aur garmi milti hai. Plants bhi sunlight se hi apna khana banate hain, isliye suraj ke bina zindagi mushkil hai."),
        (3, "Ice pighalti (melt) kyu hoti hai?", "Ice solid paani hai. Jab garmi badhti hai, toh molecules ki jagah badal jaati hai aur solid liquid ban jaata hai. Isliye ice garam jagah pe pighal jaati hai."),
        (3, "Chhaya (shadow) kaise banta hai?", "Jab koi object roshni ka raasta rok deta hai, toh uske peeche dark area ban jaata hai. Usse shadow kehte hain. Suraj ke saamne khade ho ke dekho!"),
        (3, "Pakshi (birds) kaise udte hain?", "Pakshiyon ke wings hollow halki bones aur feathers hote hain. Wings ko phaila ke aur hawa ko dabaa ke woh upar uth jaate hain."),
        (3, "Compost kya hota hai?", "Sabzi ke chhilke, dry leaves jaise waste ko mitti ke saath sadne dete hain, toh humus banta hai. Usse compost kehte hain — plants ke liye best fertilizer."),
        (4, "Global warming simple words mein kya hai?", "Earth ka average temperature badhna global warming kehlata hai. Iska main reason extra carbon dioxide hai jo factories, gaadiyon aur katte hue trees se aata hai."),
        (4, "Gravity kya hoti hai?", "Gravity Earth ka wo force hai jo sab kuch neeche kheenchta hai. Isliye gira hua ball neeche girta hai, upar nahi jaata."),
        (4, "Mobile phone kaise kaam karta hai?", "Mobile hamari awaaz ko signals mein badalta hai jo tower tak jaate hain. Tower doosre phone tak signal bhejta hai, aur wahan awaaz wapas banti hai."),
        (4, "Photosynthesis ke liye kya chahiye?", "Photosynthesis ke liye sunlight, paani aur carbon dioxide chahiye. Leaves mein chlorophyll hota hai jo inko glucose mein badal deta hai aur oxygen release karta hai."),
        (4, "Earthquake aata kyu hai?", "Earth ki upper layer (crust) plates mein bati hui hai. Jab ye plates move karti hain aur aapas mein takraati hain, toh zameen hil jaati hai — earthquake aata hai."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(bank)
        out.append(_qa(stage, "explanation", q, a))
    return out


def _hinglish_comprehension(instances: int = 12) -> list[dict]:
    templates = []


    def _t_picnic():
        a = _rng.choice(_HNAMES); b = _rng.choice(_HNAMES_F)
        while b == a:
            b = _rng.choice(_HNAMES_F)
        place = _rng.choice(["lake ke paas", "hill top pe", "garden mein", "river bank pe", "farmhouse pe"])
        games = _rng.choice(["lagori", "cricket", "hide and seek", "badminton", "kho-kho"])
        snacks = _rng.choice(["samosa aur juice", "sandwich aur mango panna", "paratha aur achar", "idli aur chutney"])
        n_balls = _rng.randint(2, 6)
        story = (f"Ravivar ko {a} aur {b} apne parivaar ke saath {place} picnic pe gaye. "
                 f"Wahan bachchon ne {games} khela aur bade log food stall se {snacks} laye. "
                 f"{a} ke bag mein {n_balls} balls thi, sabne milkar khela. Shaam ko sabne saath mein "
                 f"gana gaya aur kachra utha ke dustbin mein daala. Wapas jaate waqt sab bahut khush the.")
        qas = [
            (f"{a} aur {b} kahan gaye the?", f"Woh log {place} picnic pe gaye the."),
            (f"Bachchon ne picnic pe kya khela?", f"Bachchon ne {games} khela."),
            (f"{a} ke bag mein kitni balls thi?", f"{a} ke bag mein {n_balls} balls thi."),
            ("Kachra unhone kya kiya?", "Unhone kachra utha ke dustbin mein daala."),
        ]
        return 3, "Family Picnic", story, qas


    def _t_match():
        a = _rng.choice(_HNAMES)
        t1, t2 = _rng.sample(["Blue Stars", "Green Rockets", "Golden Lions", "Red Roses"], 2)
        s1 = _rng.randint(1, 7); s2 = _rng.randint(0, 7)
        while s1 == s2:
            s2 = _rng.randint(0, 7)
        win = t1 if s1 > s2 else t2
        story = (f"Sunday shaam ko {a} ne apne colony ke ground pe football match dekha — {t1} versus {t2}. "
                 f"Dono teams ne accha khela. Final score {s1}-{s2} raha, matlab {win} jeet gaya. "
                 f"{a} ki favourite team {win} hi thi, toh woh khushi se uchhla. Match ke baad dono teams ke players ne "
                 f"haath milaya aur saath mein juice piya.")
        qas = [
            ("Kaun se do teams ne match khela?", f"{t1} aur {t2} ne match khela."),
            ("Final score kya tha?", f"Final score {s1}-{s2} tha."),
            ("Kaun si team jeeti?", f"{win} team jeeti."),
            (f"{a} match ke baad kaisa feel kar raha tha?", f"{a} bahut khush tha kyunki uski favourite team jeeti thi."),
        ]
        return 3, "Colony ka Football Match", story, qas


    def _t_dadi():
        a = _rng.choice(_HNAMES_F)
        fruit = _rng.choice(_HFRUITS)
        k = _rng.randint(3, 9)
        story = (f"{a} roz apni dadi ke saath shaam ki walk pe jaati hai. Aaj dadi ne use {fruit} khilaya aur "
                 f"bachpan ki kahani sunayi. Dadi ne bataya ki unke zamane mein {k} baje sote the aur subah 4 baje uthte the. "
                 f"{a} ne dadi ko phone pe video call karna sikhaya. Dadi bahut khush hui aur boli — ab toh roz video pe baat hogi!")
        qas = [
            (f"{a} roz shaam ko kya karti hai?", f"{a} dadi ke saath shaam ki walk pe jaati hai."),
            ("Dadi ne use kya khilaya?", f"Dadi ne use {fruit} khilaya."),
            (f"Dadi kitne baje sote the?", f"Dadi {k} baje sote the."),
            (f"{a} ne dadi ko kya sikhaya?", f"{a} ne dadi ko phone pe video call karna sikhaya."),
        ]
        return 3, "Dadi ke saath shaam", story, qas


    def _t_train():
        a = _rng.choice(_HNAMES)
        city = _rng.choice(["Dilli", "Mumbai", "Jaipur", "Chennai", "Lucknow", "Pune"])
        n_hr = _rng.randint(4, 14)
        story = (f"{a} pehli baar train se {city} gaya. Platform pe bada crowd tha, isliye Papa ne haam pakad ke rakha. "
                 f"Train {n_hr} ghante ki journey thi. {a} ne window se khet, nadi aur tunnel dekhe. "
                 f"Raatein usne upper berth pe sui. {city} pahunch ke usne station pe ek kulfi khaayi — "
                 f"usse lagta hai train journey uski ab tak ki best trip thi.")
        qas = [
            (f"{a} kahan gaya tha?", f"{a} train se {city} gaya tha."),
            (f"Journey kitne ghante ki thi?", f"Journey {n_hr} ghante ki thi."),
            ("{a} ne window se kya kya dekha?".replace("{a}", a), "Usne window se khet, nadi aur tunnel dekhe."),
            ("Kulfi usne kahan khaayi?", "Station pe kulfi khaayi."),
        ]
        return 4, "Pehli Train Journey", story, qas


    def _t_fancydress():
        a = _rng.choice(_HNAMES)
        dress = _rng.choice(["solar system", "doctor", "butterfly", "soldier", "farmer", "traffic police"])
        prize = _rng.choice(["first", "second", "third"])
        story = (f"School mein fancy dress competition hua. {a} ne {dress} ka costume pehna aur stage pe "
                 f"do lines bold ke sabko impress kar diya. Judges ne use {prize} prize diya. "
                 f"Headmistress ne kaha ki har bachche ne mehnat ki hai, isliye sabko chocolate mili. "
                 f"{a} ne prize ghar laake Mummy-Papa ko dikhaya aur sabne party ki.")
        qas = [
            ("School mein kya competition hua tha?", "School mein fancy dress competition hua tha."),
            (f"{a} ne kya costume pehna tha?", f"{a} ne {dress} ka costume pehna tha."),
            (f"Judges ne {a} ko kya diya?", f"Judges ne {a} ko {prize} prize diya."),
            ("Headmistress ne kya kaha?", "Unhone kaha har bachche ne mehnat ki hai, isliye sabko chocolate mili."),
        ]
        return 3, "Fancy Dress ka Din", story, qas


    def _t_kite():
        a = _rng.choice(_HNAMES)
        n_kite = _rng.randint(2, 8)
        colour = _rng.choice(["peeli (yellow)", "neeli (blue)", "laal (red)", "hari (green)"])
        story = (f"Makar Sankranti ke din chhat pe sab log kite uda rahe the. {a} ne {n_kite} kharide — "
                 f"ek {colour} bhi thi. Shuru mein {a} ki kite kat gayi, par bhaiya ne tarika sikhaya — "
                 f"manjha dheela rakho, phir zor se kheencho! Phir {a} ki kite sabse unchi gayi. "
                 f"Chhat pe mithai bhi baanti gayi aur sabne til-gud ke laddu khaye.")
        qas = [
            ("Kaunsa tyohar tha?", "Makar Sankranti ka tyohar tha."),
            (f"{a} ne kitni kites kharidi thi?", f"{a} ne {n_kite} kites kharidi thi."),
            (f"Kis colour ki kite thi?", f"Ek {colour} kite thi."),
            ("Bhaiya ne kite udane ka kya tarika bataya?", "Bhaiya ne bataya manjha dheela rakho aur phir zor se kheencho."),
        ]
        return 3, "Kite ka Tyohar", story, qas

    templates = [_t_picnic, _t_match, _t_dadi, _t_train, _t_fancydress, _t_kite]
    out = []
    for make in templates:
        seen = set()
        made = 0; tries = 0
        while made < instances and tries < instances * 6:
            tries += 1
            stage, title, story, qas = make()
            if story in seen:
                continue
            seen.add(story); made += 1
            block = "\n".join(f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(qas))
            out.append(item(stage, "comprehension",
                            f"Neeche diya gaya passage padho aur sawalon ke jawab do.\n{story}\n\n{block}"))
            for q, a in _rng.sample(qas, 2):
                out.append(item(stage, "comprehension",
                                f"Read the passage: {story}\nQuestion: {q}\nAnswer: {a}"))
    return out


def _hinglish_instructions_reasoning(n: int = 90) -> list[dict]:
    out = []
    list_banks = [
        ("3 fruits", ["aam (mango)", "seb (apple)", "kela (banana)", "santra (orange)", "angoor (grapes)", "papita (papaya)"]),
        ("3 vehicles", ["bus", "train", "cycle", "scooter", "auto", "aeroplane"]),
        ("3 animals jo paani mein rehte hain", ["machhli (fish)", "mendhak (frog)", "kachhua (turtle)", "dolphin", "whale"]),
        ("3 things jo classroom mein hote hain", ["blackboard", "desk", "chalk", "duster", "map", "globe"]),
        ("3 green vegetables", ["palak (spinach)", "methi", "lauki (bottle gourd)", "bhindi (okra)", "gobhi (cauliflower)"]),
    ]
    for _ in range(n):
        style = _rng.randrange(3)
        if style == 0:
            label, options = _rng.choice(list_banks)
            k = 3
            picks = _rng.sample(options, k)
            out.append(item(2, "instructions",
                f"Question: {label} ke naam batao. Sirf {k} cheezein likho.\n"
                f"Answer: {', '.join(picks)}."))
        elif style == 1:  # one-word answers
            pairs = [
                ("Ek word mein jawab do: Sabse bada planet kaunsa hai?", "Jupiter."),
                ("Ek word mein jawab do: Humein doodh kaun deta hai?", "Cow (gaay)."),
                ("Ek word mein jawab do: Suraj kis disha mein ugta hai?", "East (poorv)."),
                ("Ek word mein jawab do: Barish kis cheez se hoti hai — badal ya taara?", "Badal."),
                ("Ek word mein jawab do: 5 × 3 kitna hota hai?", "15."),
                ("Ek word mein jawab do: Honey kaun banata hai?", "Bee (madhumakhi)."),
                ("Ek word mein jawab do: India ki capital kya hai?", "New Delhi."),
                ("Ek word mein jawab do: Ek hafte mein kitne din hote hain?", "7 (saat)."),
            ]
            q, a = _rng.choice(pairs)
            out.append(item(3, "instructions", f"Question: {q}\nAnswer: {a}"))
        else:  # ordering / multi-step reasoning
            seqs = [
                ("paani bharna", ["nal kholo", "glass pakdo", "glass bharo", "nal band karo"]),
                ("school jaana", ["bag pack karo", "breakfast karo", "shoes pehno", "bus pakdo"]),
                ("plant lagana", ["gamla lo", "mitti bharo", "beej daalo", "paani do"]),
                ("drawing banana", ["paper lo", "pencil se outline banao", "colours bharo", "naam likho"]),
            ]
            label, steps = _rng.choice(seqs)
            shuffled = steps[:]; _rng.shuffle(shuffled)
            if shuffled == steps:
                shuffled = steps[::-1]
            out.append(item(3, "reasoning",
                f"Question: In steps ko sahi order mein likho ({label}): {' , '.join(shuffled)}\n"
                f"Answer: Sahi order: " + " -> ".join(steps) + "."))
    return out


# ---------------------------------------------------------------------------
# Bank extensions for the foundation run.
# ---------------------------------------------------------------------------
def _hinglish_conversation_extra(n: int = 100) -> list[dict]:
    bank = [
        (1, "Aaj tumne kya khaya?", "Aaj maine subah paratha khaya, lunch mein dal-chawal aur shaam ko ek seb khaya. Sab kuch ghar ka khana tha."),
        (1, "Tumhare ghar mein kaun kaun rehte hain?", "Mere ghar mein Mummy, Papa, chhoti behen aur main rehte hain. Dadi bhi kabhi kabhi hamare ghar aati hain."),
        (1, "Tumhe drawing mein kya banana pasand hai?", "Mujhe drawing mein ghar, suraj aur ped banana pasand hai. Kabhi kabhi main pahad aur nadi bhi banata hoon."),
        (1, "School bag mein kya kya rakhte ho?", "Bag mein books, copies, pencil box aur water bottle rakhta hoon. Tiffin bhi ek side mein rakhta hoon."),
        (1, "Subah kaun si cheez sabse pehle karti ho?", "Sabse pehle brush karti hoon, phir haath moonh dhoti hoon aur breakfast karti hoon."),
        (1, "Tumhara favourite colour kya hai?", "Mera favourite colour blue hai. Aasman bhi blue hota hai aur meri cycle bhi blue hai."),
        (2, "Gaon aur shehar mein kya difference hai?", "Gaon mein khet, khaali jagah aur fresh hawa hoti hai; shehar mein badi buildings, schools aur markets hote hain. Dono ki apni khoobi hai."),
        (2, "Jab tum sad ho toh kya karte ho?", "Jab main sad hota hoon, toh apni Mummy se baat karta hoon ya apni favourite book padhta hoon. Thodi der mein mood theek ho jaata hai."),
        (2, "Apne best friend ke baare mein batao.", "Mera best friend Sameer hai. Woh class mein meri saamne baithta hai, maths mein mera help karta hai aur hum lunch time pe saath khelte hain."),
        (2, "Tumne pichle weekend kya kiya?", "Pichle weekend maine Papa ke saath zoo gaya tha. Wahan monkeys aur lions dekhe, aur bahut maza aaya."),
        (2, "Sacchi dosti kya hoti hai?", "Sacchi dost matlab jo achhe kaamon mein saath de, bura waqt mein chhod na jaye aur hamesha sach bole."),
        (2, "Barish mein bahar nikalna theek hai ya ghar rehna?", "Bahut tez barish mein andar rehna better hai, warna bheeg jaoge aur bimaar ho sakte ho. Halki barish mein raincoat pehen ke ja sakte hain."),
        (3, "Humein rozi rozi ki chhoti chhoti aadatein kaise sudharni chahiye?", "Roz thoda thoda sudhaar karo — time pe so jao, subah jaldi utho, homework time pe karo. Chhoti aadatein milke badi discipline banati hain."),
        (3, "Tumhare hisaab se sabse achha subject kaunsa hai aur kyu?", "Mujhe Maths sabse achha lagta hai kyunki usme jab answer sahi nikalta hai toh bahut maza aata hai. Practice karne se sums easy lagne lagte hain."),
        (3, "Naya saal kaise manaya?", "Naye saal pe humne ghar sajaya, sab mithai baanti aur kal calendar pe naye saal ki date likhi. Papa ne bataya naya saal naye sankalp lene ka time hai."),
        (3, "Trees humein kya kya dete hain?", "Trees humein oxygen, chhaya, phal aur lakdi dete hain. Woh birds ko ghar dete hain aur zameen ko mazboot rakhte hain."),
        (3, "Water save karne ke liye kya kya kar sakte ho?", "Brush karte waqt tap band rakho, bucket se nahao pipe se nahi, aur leak hue tap turant theek karwao. Chhote chhote steps se paani bachta hai."),
        (3, "Jab teacher class mein question puchti hain toh kya karna chahiye?", "Dhyan se suno, agar answer pata ho toh haath utha ke bolo. Pata na ho toh baad mein zaroor seekho. Class mein shor nahi karna chahiye."),
        (4, "Time management kya hai aur kyu zaroori hai?", "Time management matlab kaamon ko time dekar plan karna — school, homework, khel aur sona. Isse saara kaam time pe hota hai aur tension nahi hoti."),
        (4, "Agar tumhari class mein koi naya student aaye toh kya karoge?", "Main usse milunga, apna naam bataunga, usse class aur school ghumau nga aur lunch pe saath baithunga. Naye aaye ko welcome feel karana achhi baat hai."),
        (4, "Books padhne se kya fayda hai?", "Books se naye words aur knowledge milti hai, imagination strong hoti hai aur mind sharp rehta hai. Achhi books humein achhe values bhi sikhate hain."),
        (4, "Team mein kaam karna kyu zaroori hai?", "Team mein sabka apna role hota hai — koi akela jitna kaam nahi kar sakta jitna sab milkar kar sakte hain. Team spirit se bade goals poore hote hain."),
        (4, "Internet ka sahi istemal kya hai?", "Internet se hum padhai aur naye cheezein seekh sakte hain, par bina permission kisi ko personal info nahi deni chahiye aur zyada screen time nahi karna chahiye."),
        (4, "Agar koi tumse zyada smart ho toh kaisa feel karna chahiye?", "Usse seekhna chahiye, jalna nahi. Har kisi ki apni khoobi hoti hai — main apni mehnat se aur better ho sakta hoon."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(bank)
        out.append(_qa(stage, "qa", q, a))
    return out


def _hinglish_explanations_extra(n: int = 70) -> list[dict]:
    bank = [
        (2, "Haath dhone se bimaari kyu nahi lagti?", "Haath dhone se germs haath se nikal jaate hain. Khana khane se pehle aur toilet ke baad sabun se haath dhona sabse simple health rule hai."),
        (2, "Humein roz kitna paani peena chahiye?", "Bade log kehte hain roz 6 se 8 glass paani peena chahiye. Paani se body ko cool rakhta hai aur pet saaf rehta hai."),
        (2, "Neend kyu zaroori hai?", "Neend mein hamari body rest karti hai aur dimaag naye cheezein yaad karta hai. Isliye bachchon ko 8-10 ghante ki neend chahiye."),
        (3, "Mujhe samjhao — bandar ped pe kaise chadhta hai?", "Bandar ke haath-pair strong aur pakadne wale (gripping) hote hain, aur poonch balance banati hai. Isliye woh aaram se branch se branch kood jaata hai."),
        (3, "Baraf ke gubbare (ice cubes) tairte kyu hain?", "Ice ka paani se halka hona normal hai — jab paani jamta hai toh uska volume badh jaata hai, isliye ice paani ke upar tirti hai."),
        (3, "Sky blue kyu dikhta hai?", "Hawa mein chhote chhote molecules suraj ki roshni ko baant dete hain. Blue light sabse jyada bikharti hai, isliye sky blue dikhta hai. Simple!"),
        (3, "Kagaz ko recycle kaise karte hain?", "Purane kagaz ko pani aur chemicals ke saath mila ke ghol banate hain, phir usse patla bichha ke naya kagaz banate hain. Isse ped bhi bachte hain."),
        (4, "Bijli ka current kaise ghar tak aata hai?", "Power station mein electricity banti hai, phir bade bade towers ke wires se aati hai, area ke transformer se hokar hamare ghar ke meter se ghar mein pahunchti hai."),
        (4, "Rainbow mein sat rang kaun se hote hain?", "Rainbow mein violet, indigo, blue, green, yellow, orange aur red — VII colours hote hain. Unhe VIBGYOR yaad rakh sakte ho."),
        (4, "Pressure cooker khana jaldi kaise pakata hai?", "Pressure cooker mein bhaap band hoti hai aur pressure badhta hai. Zyada pressure mein paani 100 degree se jyada garam hota hai, isliye khana jaldi pakta hai."),
        (4, "Dhoop mein kali chashma kyu lagate hain?", "Tez dhoop mein UV rays aankhon ko nuksaan pahunchati hain. Kali chashma tez roshni aur UV rays ko rok ke aankhon ko protect karta hai."),
        (4, "Fridge mein khana zyada din kyu tikta hai?", "Fridge mein thandi temperature hoti hai jisme bacteria dheere badhte hain. Isliye doodh aur sabzi zyada din fresh rehte hain."),
    ]
    out = []
    for _ in range(n):
        stage, q, a = _rng.choice(bank)
        out.append(_qa(stage, "explanation", q, a))
    return out


def _hinglish_two_step_problems(n: int = 110) -> list[dict]:
    out = []
    for _ in range(n):
        style = _rng.randrange(3)
        name = _rng.choice(_HNAMES)
        thing = _rng.choice(_HTHINGS)
        if style == 0:  # buy - give
            a = _rng.randint(20, 70); b = _rng.randint(5, 25); c = _rng.randint(3, min(15, a + b - 2))
            out.append(item(4, "word_problem",
                f"Question: {name} ke paas {a} {thing} the. Mummy ne {b} {thing} aur laake diye, phir {name} ne {c} {thing} apne dost ko gift kar diye. Ab kitne {thing} bache?\n"
                f"Answer: {a} + {b} = {a + b}, phir {a + b} - {c} = {a + b - c}. Ab {name} ke paas {a + b - c} {thing} hain."))
        elif style == 1:  # price × k, change
            p = _rng.randrange(5, 20, 5); k = _rng.randint(3, 8)
            total = p * k
            note = 200 if total <= 150 else 500
            out.append(item(4, "word_problem",
                f"Question: Ek notebook ki keemat Rs {p} hai. {name} ne {k} notebooks kharidi aur Rs {note} ka note diya. Dukandaar kitne rupaye lautaega?\n"
                f"Answer: {k} × {p} = Rs {total}. {note} - {total} = Rs {note - total}. Dukandaar Rs {note - total} lautaega."))
        else:  # share then eat
            total = _rng.randint(24, 60); k = _rng.randint(3, 8)
            while total % k != 0:
                total += 1
            each = total // k; eat = _rng.randint(1, min(3, each))
            out.append(item(4, "word_problem",
                f"Question: {total} {thing} ko {k} bachchon mein barabar baanta gaya. {name} ne apne hisse mein se {eat} kha liye. Ab {name} ke paas kitne hain?\n"
                f"Answer: {total} ÷ {k} = {each}. Ab {name} ne {eat} kha liye toh {each} - {eat} = {each - eat}. {name} ke paas {each - eat} {thing} hain."))
    return out
