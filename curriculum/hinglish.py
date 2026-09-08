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

    return out
