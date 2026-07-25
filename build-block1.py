#!/usr/bin/env python3
"""build-block1.py — emit the remaining Block 1 sheets (Jul 29 – Aug 2, 2026).

Run:  python3 build-block1.py     (writes the .html files next to this script)
Then: ./print-worksheet.sh <file> --dry-run   # must say 3 pages

Skills this block drills, per PRACTICE-PLAN-2026.md:
  kid1  (3rd) — division with remainders, INTERPRETING the remainder
  kid2 (4th) — adding/subtracting fractions with UNLIKE denominators
Every answer below was worked by hand.
"""
import importlib.util, pathlib

_spec = importlib.util.spec_from_file_location(
    "make_sheet", pathlib.Path(__file__).with_name("make-sheet.py"))
make_sheet = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(make_sheet)
build = make_sheet.build
HERE = pathlib.Path(__file__).parent

TRAIN  = dict(main='#b45309', muted='#a1866a', border='#f0d9b5', factbg='#fdf6ec', factbar='#d97706', keyborder='#f2e2c8')
STARS  = dict(main='#1e3a8a', muted='#7d8bb0', border='#c7d2fe', factbg='#eef2ff', factbar='#4f46e5', keyborder='#d5dcf7')
VOLC   = dict(main='#9f1239', muted='#a97b88', border='#fbcfe0', factbg='#fff1f5', factbar='#e11d48', keyborder='#f8d9e4')
PARKS  = dict(main='#166534', muted='#7b9c86', border='#c3e6cd', factbg='#f0faf3', factbar='#16a34a', keyborder='#d3ecda')
BODY   = dict(main='#7c2d12', muted='#a98274', border='#f3d5c4', factbg='#fdf4ee', factbar='#ea580c', keyborder='#f5e0d3')

SHEETS = {}

# ─────────────────────────────────────────────────────────────────────────
# Jul 29 — TEACH, faded: guided problem kept, worked example REMOVED.
# Because the example box is gone, this page is back to 5 problems.
# ─────────────────────────────────────────────────────────────────────────
SHEETS['worksheet-trains-teach2.html'] = dict(
    doc_title="Trains — Remainders & Unlike Denominators (day 2)",
    title="🚂 Railway Math", sub="Day 2 — you've seen how this works, now without the example",
    color=TRAIN,
    pages=[
        dict(name='kid1', grade='3rd Grade', problems=[
            dict(text="47 passengers are waiting for a train. Each car seats 6 people. How many cars are needed so that everybody gets a seat?",
                 scaffold=["Divide: 47 ÷ 6 = <span class='blank'></span> remainder <span class='blank'></span>",
                           "The remainder means <span class='blank'></span> people still have no seat.",
                           "Can they be left at the station? <span class='blank'></span>",
                           "So how many cars? <span class='blank'></span>"],
                 fact="A train wheel isn't flat — it's cone-shaped, which is what steers it around a curve without any steering at all."),
            dict(text="A station loads 62 crates onto carts. Each cart holds 8 crates. How many carts get <b>completely full</b>, and how many crates are left on the platform?",
                 fact="Freight trains can be over a mile long — some in Australia run to 4 miles."),
            dict(text="75 students are taking a train to a museum. Each car holds 9 students. Every student must have a seat. How many cars does the school need?",
                 fact="The world's busiest station is Shinjuku in Tokyo — about 3.5 million people pass through it every day."),
            dict(text="A conductor has 40 tickets to sort into books of 6. How many complete books can he make, and how many tickets are left over?",
                 fact="Conductors once punched each ticket with a uniquely shaped hole so no one could reuse it."),
            dict(text="53 suitcases must all be stored, and each luggage rack holds 7. How many racks are used, and how many suitcases are on the last rack?",
                 fact="The first luggage racks were nets, so passengers could see their bags from their seat."),
        ]),
        dict(name='kid2', grade='4th Grade', problems=[
            dict(text="kid2 finishes 1/3 of a train journey before lunch and another 1/4 of it after lunch. What fraction of the journey has he travelled?",
                 scaffold=["Common bottom number: 3 × 4 = <span class='blank'></span>",
                           "Rewrite: 1/3 = <span class='blank'></span> &nbsp; and &nbsp; 1/4 = <span class='blank'></span>",
                           "Add the tops, keep the bottom: <span class='blank'></span>"],
                 fact="The fastest passenger train in service, the Shanghai Maglev, floats above the track on magnets at 267 mph."),
            dict(text="A train is 2/5 full when it leaves the first station. At the next stop, enough people board to fill another 1/3 of the train. What fraction of the train is now full?",
                 fact="Trains are so efficient that moving one ton of freight a mile by rail uses about a quarter of the fuel a truck would."),
            dict(text="A track crew lays 3/8 of a mile of rail on Monday and 1/2 a mile on Tuesday. How much track did they lay in total?",
                 fact="Rails are laid with small gaps because steel expands in summer heat — that's the clackety-clack sound."),
            dict(text="A locomotive starts with 5/6 of a tank of fuel and burns 1/4 of a tank on the trip. What fraction of a tank is left?",
                 fact="A big diesel locomotive holds about 5,000 gallons of fuel — roughly 300 car fill-ups."),
            dict(text="kid2 reads 2/3 of a book on the train and his brother reads a different 1/5 of it. What fraction of the book has been read between them?",
                 fact="Reading on a train makes some people queasy because the eyes say 'still' while the inner ear says 'moving'."),
        ]),
    ],
    key_sub="For the grown-ups — worked steps + what to watch for",
    key=[
        dict(section="3rd Grade — kid1 (remainders)",
             watch="answering with the raw remainder (\"7 r 5\") instead of what the question asked. Don't correct the division — have him read the last sentence out loud again.",
             answers=[
                dict(a="8 cars.", steps="47 ÷ 6 = 7 r 5. Seven full cars, 5 people still standing → round <b>up</b> to <b>8</b>."),
                dict(a="7 full carts, 6 crates left.", steps="62 ÷ 8 = 7 r 6. Asks for <b>completely full</b> → do not round up. <b>7</b> carts, <b>6</b> crates."),
                dict(a="9 cars.", steps="75 ÷ 9 = 8 r 3. Everyone needs a seat → <b>9</b> cars, the last holding 3."),
                dict(a="6 books, 4 tickets left.", steps="40 ÷ 6 = 6 r 4. Complete books only → <b>6</b>, with <b>4</b> spare tickets."),
                dict(a="8 racks; 4 suitcases on the last one.", steps="53 ÷ 7 = 7 r 4. All must be stored → <b>8</b> racks, last one holds <b>4</b>."),
             ]),
        dict(section="4th Grade — kid2 (unlike denominators)",
             watch="adding the bottoms (1/3 + 1/4 = 2/7). If it happens, go back to the pizza picture — you can't count pieces of different sizes. Also check he converted BOTH fractions, not just one.",
             answers=[
                dict(a="7/12 of the journey.", steps="Common bottom 12. 1/3 = 4/12, 1/4 = 3/12. 4/12 + 3/12 = <b>7/12</b>."),
                dict(a="11/15 full.", steps="Common bottom 15. 2/5 = 6/15, 1/3 = 5/15. 6/15 + 5/15 = <b>11/15</b>."),
                dict(a="7/8 of a mile.", steps="8 already works. 1/2 = 4/8. 3/8 + 4/8 = <b>7/8</b>. Good one for spotting you don't always multiply the bottoms."),
                dict(a="7/12 of a tank.", steps="Common bottom 12. 5/6 = 10/12, 1/4 = 3/12. 10/12 − 3/12 = <b>7/12</b>."),
                dict(a="13/15 of the book.", steps="Common bottom 15. 2/3 = 10/15, 1/5 = 3/15. 10/15 + 3/15 = <b>13/15</b>."),
             ]),
    ])

# ─────────────────────────────────────────────────────────────────────────
# Jul 30 — LOGIC day
# ─────────────────────────────────────────────────────────────────────────
SHEETS['worksheet-astronomy-logic.html'] = dict(
    doc_title="Islamic Golden Age Astronomy — Logic & Puzzles",
    title="🔭 House of Wisdom Logic", sub="Brain-teasers from the astronomers of the Islamic Golden Age",
    color=STARS,
    pages=[
        dict(name='kid1', grade='3rd Grade', work_label='SHOW YOUR THINKING', problems=[
            dict(text="Three students charted stars one night: kid1, Idris, and Bilal. Together they charted 14 stars. Idris charted 6 and Bilal charted 3. How many did kid1 chart? Whose number was in the <b>middle</b>?",
                 fact="Al-Sufi drew a star atlas in the year 964 that described the Andromeda Galaxy — over 900 years before telescopes could show what it was."),
            dict(text="An astrolabe is engraved with a ring of numbers: 5, 10, 15, 20, ___, ___ . What are the next two, and what is the rule?",
                 fact="An astrolabe was a handheld computer made of brass. It could tell you the time, find your direction, and locate a star."),
            dict(text="Aisha counted 11 stars through a sighting tube. She saw <b>3 more</b> bright ones than dim ones. How many bright and how many dim? (Hint: try pairs that add to 11.)",
                 fact="Many star names we still use are Arabic — Betelgeuse, Rigel, Aldebaran, Vega."),
            dict(text="Four scholars finished copying a manuscript: Hamza, Layla, Omar, and Zayd. Hamza finished 1st. Zayd finished last. Layla finished ahead of Omar. List all four in order.",
                 fact="Paper reached Baghdad in the 700s, and books became cheap enough that the city had over 100 bookshops."),
            dict(text="kid1 is making an observation kit with one tool — astrolabe, quadrant, or sundial — and one notebook, leather or cloth. How many different kits can he make? List them.",
                 fact="A quadrant measures the angle between the horizon and a star, which tells you how far north or south you are."),
        ]),
        dict(name='kid2', grade='4th Grade', work_label='SHOW YOUR THINKING', problems=[
            dict(text="In a stargazing game, spotting a planet earns 5 points, a bright star earns 2, and a cloudy night <b>costs</b> 3. kid2 spots 3 planets and 4 bright stars but loses 2 nights to clouds. Zaid spots 2 planets, 6 bright stars, and loses 1 night. Who has more, and by how much?",
                 fact="Only five planets can be seen without a telescope: Mercury, Venus, Mars, Jupiter, and Saturn."),
            dict(text="Three astronomers — kid2, Idris, and Hamza — each have one job: measuring, recording, and drawing. Clue 1: kid2 is <b>not</b> the recorder. Clue 2: Hamza is the artist who draws. Who does what?",
                 fact="Al-Battani measured the length of a year as 365 days, 5 hours, 46 minutes, 24 seconds — off by only about 2 minutes."),
            dict(text="An observatory starts with 96 star charts. Each year, half of them are recopied onto fresh paper and the old ones retired. After 4 years, how many of the original charts are left? How many were retired in all?",
                 fact="The Maragheh observatory in Persia had a library of 40,000 books and a staff of astronomers from as far away as China."),
            dict(text="Two brothers recorded moon sightings all month. Together they recorded 28. kid2 recorded <b>8 more</b> than kid1. How many did each record?",
                 fact="The Islamic calendar follows the moon, so its months shift about 11 days earlier each solar year."),
            dict(text="A school of 18 students is split into equal groups of 6 to share telescopes. How many groups? Within one group, each student compares notes with every other student exactly once. How many comparisons happen in that group?",
                 fact="The word 'algebra' comes from al-jabr, the title of a book written in Baghdad around 820."),
        ]),
    ],
    key_sub="For the grown-ups — reasoning included",
    key=[
        dict(section="3rd Grade — kid1",
             answers=[
                dict(a="kid1 charted 5; kid1 is the middle.", steps="14 − 6 − 3 = <b>5</b>. In order: Bilal 3, kid1 5, Idris 6 → kid1 is in the middle."),
                dict(a="25 and 30. Rule: add 5.", steps="Each number goes up by 5. 20 + 5 = 25, 25 + 5 = <b>30</b>."),
                dict(a="7 bright, 4 dim.", steps="Adds to 11, differs by 3. 7 + 4 = 11 and 7 − 4 = 3. So <b>7</b> bright, <b>4</b> dim."),
                dict(a="Hamza, Layla, Omar, Zayd.", steps="Hamza 1st, Zayd 4th. Layla ahead of Omar → Layla 2nd, Omar 3rd."),
                dict(a="6 kits.", steps="3 tools × 2 notebooks = <b>6</b>. (astrolabe-leather, astrolabe-cloth, quadrant-leather, quadrant-cloth, sundial-leather, sundial-cloth.)"),
             ]),
        dict(section="4th Grade — kid2",
             answers=[
                dict(a="kid2 17, Zaid 19. Zaid leads by 2.", steps="kid2: (3×5) + (4×2) − (2×3) = 15 + 8 − 6 = 17. Zaid: (2×5) + (6×2) − (1×3) = 10 + 12 − 3 = 19. 19 − 17 = <b>2</b>."),
                dict(a="Hamza draws, kid2 measures, Idris records.", steps="Hamza draws (Clue 2). kid2 isn't the recorder (Clue 1) and drawing is taken → kid2 measures. Idris records."),
                dict(a="6 charts left; 90 retired.", steps="96 → 48 → 24 → 12 → <b>6</b> after 4 years. Retired: 96 − 6 = <b>90</b>."),
                dict(a="kid1 10, kid2 18.", steps="Take the 8 off first: 28 − 8 = 20, then 20 ÷ 2 = 10 for kid1. kid2 = 10 + 8 = <b>18</b>. Check: 10 + 18 = 28. ✓"),
                dict(a="3 groups; 15 comparisons per group.", steps="18 ÷ 6 = <b>3</b> groups. In a group of 6 (A–F): 5+4+3+2+1 = <b>15</b> pairs."),
             ]),
    ])

# ─────────────────────────────────────────────────────────────────────────
# Jul 31 — PRACTICE, same two skills, no scaffolding at all
# ─────────────────────────────────────────────────────────────────────────
SHEETS['worksheet-volcano.html'] = dict(
    doc_title="Volcano Math", title="🌋 Volcano Math",
    sub="Word problems from the crater rim", color=VOLC,
    pages=[
        dict(name='kid1', grade='3rd Grade', problems=[
            dict(text="A research team must carry 58 rock samples down the mountain. Each pack holds 8 samples, and every sample must come down. How many packs do they need, and how many samples are in the last one?",
                 fact="Fresh lava can reach 2,100°F — hot enough to melt a copper penny in seconds."),
            dict(text="A visitor centre has 91 helmets to store on shelves of 9. How many shelves are <b>completely full</b>, and how many helmets are left over?",
                 fact="Volcanologists wear silver heat suits that reflect radiant heat, which is why they look like astronauts."),
            dict(text="A museum starts with 342 volcanic rocks, sends 158 to a school, and then collects 96 more on a field trip. How many rocks does it have now?",
                 fact="Pumice is the only rock that floats — it's full of gas bubbles frozen in place."),
            dict(text="An observation post has 7 windows and each window has 8 panes. During an eruption, 19 panes crack. How many panes are still whole?",
                 fact="Volcanic ash isn't soft like fire ash — it's tiny shards of glass, which is why it scratches everything."),
            dict(text="A team of 46 scientists is going up in cable cars that hold 5 people each. Everyone must ride. How many cable cars are needed, and how many people are in the last car?",
                 fact="Mount Etna in Sicily has been erupting on and off for at least 500,000 years."),
        ]),
        dict(name='kid2', grade='4th Grade', problems=[
            dict(text="An ash cloud covers 3/8 of a valley on the first day and another 1/2 of the valley on the second day. What fraction of the valley is covered? What fraction is still clear?",
                 fact="The 1815 eruption of Tambora threw up so much ash that 1816 was called 'the year without a summer' in Europe and North America."),
            dict(text="A lava flow travels 2/3 of a mile in the morning and 1/6 of a mile in the afternoon. How far did it travel that day?",
                 fact="Most lava flows move slower than walking pace — you can usually stroll away from one."),
            dict(text="A monitoring station's battery is 7/10 charged. Overnight it uses 1/4 of a full charge. What fraction of the battery is left?",
                 fact="Seismometers around a volcano can detect movement smaller than the width of a human hair."),
            dict(text="A crater rim trail is 4/5 of a mile long. Aisha hikes 1/3 of a mile and stops. What fraction of a mile is left to walk?",
                 fact="Crater lakes can be more acidic than lemon juice because volcanic gases dissolve into the water."),
            dict(text="Scientists have mapped 5/6 of a lava tube. A cave-in blocks off 1/4 of the whole tube, which they can no longer reach. What fraction of the tube have they mapped and can still reach?",
                 fact="Lava tubes form when the outside of a flow cools into a crust while molten rock keeps running through the middle."),
        ]),
    ],
    key=[
        dict(section="3rd Grade — kid1 (remainders)",
             watch="whether he's now asking himself which way to round WITHOUT being prompted. That's the skill going from Shaky to Solid.",
             answers=[
                dict(a="8 packs; 2 samples in the last one.", steps="58 ÷ 8 = 7 r 2. All must come down → <b>8</b> packs, last holds <b>2</b>."),
                dict(a="10 full shelves, 1 helmet left.", steps="91 ÷ 9 = 10 r 1. <b>Completely full</b> only → <b>10</b> shelves, <b>1</b> helmet over."),
                dict(a="280 rocks.", steps="342 − 158 = 184. Then 184 + 96 = <b>280</b>."),
                dict(a="37 panes whole.", steps="7 × 8 = 56 panes. 56 − 19 cracked = <b>37</b>."),
                dict(a="10 cable cars; 1 person in the last.", steps="46 ÷ 5 = 9 r 1. Everyone rides → <b>10</b> cars, last carries <b>1</b>."),
             ]),
        dict(section="4th Grade — kid2 (unlike denominators)",
             watch="the subtraction ones (3, 4, 5). Same method, and that's the point — if he can add but not subtract, he's memorised a procedure rather than understood common denominators.",
             answers=[
                dict(a="Covered 7/8; 1/8 still clear.", steps="Common bottom 8. 3/8 + 4/8 = <b>7/8</b>. Clear: 8/8 − 7/8 = <b>1/8</b>."),
                dict(a="5/6 of a mile.", steps="Common bottom 6. 2/3 = 4/6. 4/6 + 1/6 = <b>5/6</b>."),
                dict(a="9/20 of the battery.", steps="Common bottom 20. 7/10 = 14/20, 1/4 = 5/20. 14/20 − 5/20 = <b>9/20</b>."),
                dict(a="7/15 of a mile left.", steps="Common bottom 15. 4/5 = 12/15, 1/3 = 5/15. 12/15 − 5/15 = <b>7/15</b>."),
                dict(a="7/12 of the tube.", steps="Common bottom 12. 5/6 = 10/12, 1/4 = 3/12. 10/12 − 3/12 = <b>7/12</b>."),
             ]),
    ])

# ─────────────────────────────────────────────────────────────────────────
# Aug 1 — PRACTICE, timed
# ─────────────────────────────────────────────────────────────────────────
SHEETS['worksheet-national-parks.html'] = dict(
    doc_title="National Parks Math — Timed", title="🏔️ National Parks Math",
    sub="Timed sheet — steady beats fast, but keep moving", color=PARKS,
    pages=[
        dict(name='kid1', grade='3rd Grade', problems=[
            dict(text="A ranger station has 74 trail maps to hand out in bundles of 8. How many complete bundles can be made, and how many maps are left?",
                 fact="Yellowstone was the first national park anywhere in the world, created in 1872."),
            dict(text="66 campers need tents, and each tent sleeps 7. Everybody needs a spot. How many tents are needed, and how many campers are in the last tent?",
                 fact="A bison can weigh a ton and still outrun a person — they hit 35 mph."),
            dict(text="A visitor centre had 415 postcards, sold 187 over the weekend, then received a delivery of 130. How many postcards now?",
                 fact="The Grand Canyon is a mile deep, and the rock at the bottom is about 1.8 billion years old."),
            dict(text="A trail crew works 9 sections and clears 6 fallen trees from each. A storm then drops 14 more trees across the trail. How many trees is that in total?",
                 fact="Some giant sequoias were already big trees when the Roman Empire fell."),
            dict(text="A shuttle carries 52 hikers in vans that hold 6 each. Every hiker must get a ride. How many vans, and how many hikers ride in the last van?",
                 fact="Park shuttles exist partly because car exhaust was fading the rock colours in some canyons."),
        ]),
        dict(name='kid2', grade='4th Grade', problems=[
            dict(text="A hiking trail is 7/8 of a mile. kid2 walks 1/3 of a mile before stopping for water. How much of the trail is left?",
                 fact="The Appalachian Trail runs about 2,200 miles — most people who try to walk all of it don't finish."),
            dict(text="Rangers clear 2/5 of a trail on Monday and 1/4 of it on Tuesday. What fraction is cleared, and what fraction is still blocked?",
                 fact="A single fallen sequoia can take a crew days to cut through, so most trails route around them instead."),
            dict(text="A water tank at a campsite is 5/6 full. Campers use 3/8 of a full tank overnight. What fraction is left in the morning?",
                 fact="Backcountry water has to be filtered even when it looks clear — the thing that makes you sick is usually invisible."),
            dict(text="A park is 3/4 forest. Of the whole park, 1/6 burned in a fire. If all the burned land was forest, what fraction of the park is forest that did not burn?",
                 fact="Some pine cones only open and release their seeds after a fire, so the forest replants itself."),
            dict(text="Aisha fills 1/2 of her backpack with food and 2/5 of it with gear. What fraction is full, and what fraction is still empty?",
                 fact="The old rule is to carry no more than a fifth of your body weight — most first-time backpackers carry far more."),
        ]),
    ],
    key=[
        dict(section="3rd Grade — kid1",
             watch="time it, but don't announce the clock — pressure changes what you're measuring. Note the finish time and errors in the log.",
             answers=[
                dict(a="9 bundles, 2 maps left.", steps="74 ÷ 8 = 9 r 2. Complete bundles → <b>9</b>, with <b>2</b> spare."),
                dict(a="10 tents; 3 campers in the last.", steps="66 ÷ 7 = 9 r 3. Everyone needs a spot → <b>10</b> tents, last holds <b>3</b>."),
                dict(a="358 postcards.", steps="415 − 187 = 228. Then 228 + 130 = <b>358</b>."),
                dict(a="68 trees.", steps="9 × 6 = 54 cleared. Then 54 + 14 storm trees = <b>68</b>."),
                dict(a="9 vans; 4 hikers in the last.", steps="52 ÷ 6 = 8 r 4. Everyone rides → <b>9</b> vans, last carries <b>4</b>."),
             ]),
        dict(section="4th Grade — kid2",
             watch="problem 4 is the hard one — it needs a subtraction of two fractions where neither bottom divides the other. If he stalls, that's fine; note it and re-teach rather than pushing.",
             answers=[
                dict(a="13/24 of a mile left.", steps="Common bottom 24. 7/8 = 21/24, 1/3 = 8/24. 21/24 − 8/24 = <b>13/24</b>."),
                dict(a="Cleared 13/20; blocked 7/20.", steps="Common bottom 20. 2/5 = 8/20, 1/4 = 5/20. 8/20 + 5/20 = <b>13/20</b>. Blocked: 20/20 − 13/20 = <b>7/20</b>."),
                dict(a="11/24 of the tank.", steps="Common bottom 24. 5/6 = 20/24, 3/8 = 9/24. 20/24 − 9/24 = <b>11/24</b>."),
                dict(a="7/12 of the park.", steps="Common bottom 12. 3/4 = 9/12, 1/6 = 2/12. 9/12 − 2/12 = <b>7/12</b>."),
                dict(a="9/10 full; 1/10 empty.", steps="Common bottom 10. 1/2 = 5/10, 2/5 = 4/10. 5/10 + 4/10 = <b>9/10</b>. Empty: <b>1/10</b>."),
             ]),
    ])

# ─────────────────────────────────────────────────────────────────────────
# Aug 2 — CUMULATIVE. Skills deliberately unlabeled and interleaved.
# This is the sheet that tells you Solid vs Locked.
# ─────────────────────────────────────────────────────────────────────────
SHEETS['worksheet-human-body-mixed.html'] = dict(
    doc_title="Mixed Review — Human Body", title="🫀 Mixed Review",
    sub="Every kind of problem, all shuffled — you decide what each one needs",
    color=BODY,
    pages=[
        dict(name='kid1', grade='3rd Grade', problems=[
            dict(text="A clinic has 8 shelves of first-aid kits with 7 kits on each shelf. During a busy week 23 kits are used. How many kits are left?",
                 fact="Your body makes about 2 million new red blood cells every second."),
            dict(text="69 students need to be seen by the school nurse in groups of 8. Every student must be seen. How many groups are needed, and how many students are in the last group?",
                 fact="The smallest bone in your body is in your ear and is about the size of a grain of rice."),
            dict(text="A hospital ward starts with 254 bandages, uses 137, then restocks 88. How many bandages are on the ward now?",
                 fact="A cut heals from the edges inward, which is why a long thin cut closes faster than a round one the same size."),
            dict(text="A first-aid class starts at 10:20 a.m. It runs 40 minutes, breaks for 15, then runs 35 more. What time does it finish?",
                 fact="CPR chest compressions are done at about 100 beats a minute — the same tempo as a lot of pop songs."),
            dict(text="A box of 45 gloves is shared out at 6 gloves per station. How many stations get a <b>complete</b> set, and how many gloves are left over?",
                 fact="Doctors didn't routinely wash their hands between patients until the mid-1800s, and the doctor who suggested it was mocked for it."),
        ]),
        dict(name='kid2', grade='4th Grade', problems=[
            dict(text="A lab receives 18 trays of 24 test tubes each and shares them equally among 12 benches. How many test tubes does each bench get?",
                 fact="Your blood vessels laid end to end would stretch about 60,000 miles — more than twice around the Earth."),
            dict(text="kid2 drinks 1/3 of a water bottle at breakfast and 2/5 of it at lunch. What fraction has he drunk, and what fraction is left?",
                 fact="You lose about a cup of water a day just by breathing it out."),
            dict(text="A hospital wing is a rectangle 42 metres long and 18 metres wide. What is its floor area? If each ward takes up 54 square metres, how many wards fit?",
                 fact="Hospital corridors are built wide enough for two beds to pass, which is why they feel so oversized."),
            dict(text="A heart beats about 4,200 times an hour. How many times does it beat in 6 hours? If a monitor can store 30,000 beats before it fills up, how many more beats will fit?",
                 fact="Your heart beats roughly 100,000 times a day without you thinking about it once."),
            dict(text="A nurse works 9 hours a day for 14 days. She takes 26 hours of that as training and 15 hours as meetings. How many hours were spent with patients?",
                 fact="Nurses walk about 4–5 miles in a typical hospital shift."),
        ]),
    ],
    key_sub="For the grown-ups — this sheet tells you Solid vs Locked",
    key=[
        dict(section="3rd Grade — kid1 (mixed)",
             watch="this is the real test. The problems are shuffled and nothing says which method to use. Getting a remainder problem right HERE — sitting between a multiplication and an elapsed-time problem — is what moves the skill from Solid to Locked. Errors here after a clean week mean he learned the sheet, not the skill.",
             answers=[
                dict(a="33 kits left.", steps="8 × 7 = 56. Then 56 − 23 = <b>33</b>."),
                dict(a="9 groups; 5 students in the last.", steps="69 ÷ 8 = 8 r 5. Everyone must be seen → <b>9</b> groups, last has <b>5</b>."),
                dict(a="205 bandages.", steps="254 − 137 = 117. Then 117 + 88 = <b>205</b>."),
                dict(a="11:50 a.m.", steps="40 + 15 + 35 = 90 minutes = 1 hr 30. 10:20 + 1:30 = <b>11:50 a.m.</b>"),
                dict(a="7 complete stations, 3 gloves left.", steps="45 ÷ 6 = 7 r 3. <b>Complete</b> sets only → <b>7</b>, with <b>3</b> gloves spare."),
             ]),
        dict(section="4th Grade — kid2 (mixed)",
             watch="problem 2 is the fraction one, buried between a division and an area problem on purpose. If he handles it here without a running start, unlike denominators is Locked.",
             answers=[
                dict(a="36 test tubes per bench.", steps="18 × 24 = 432. Then 432 ÷ 12 = <b>36</b>."),
                dict(a="Drunk 11/15; 4/15 left.", steps="Common bottom 15. 1/3 = 5/15, 2/5 = 6/15. 5/15 + 6/15 = <b>11/15</b>. Left: 15/15 − 11/15 = <b>4/15</b>."),
                dict(a="Area 756 sq m; 14 wards.", steps="42 × 18 = 756. Then 756 ÷ 54 = <b>14</b>."),
                dict(a="25,200 beats; 4,800 more will fit.", steps="4,200 × 6 = 25,200. Then 30,000 − 25,200 = <b>4,800</b>."),
                dict(a="85 hours with patients.", steps="9 × 14 = 126 hours. Then 126 − 26 − 15 = <b>85</b>."),
             ]),
    ])

if __name__ == '__main__':
    for name, spec in SHEETS.items():
        (HERE / name).write_text(build(spec))
        print(f"wrote {name}")
