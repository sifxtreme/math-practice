"""The five word-problem sheets for Jul 29 - Aug 2, at the STEP UP pin.

kid1's protected skill is interpreting a remainder; kid2's is unlike
denominators. Both appear on every sheet, with the rest of each kid's pinned
spread rotating around them. Aug 2 is the cumulative sheet: one problem per
pinned skill, deliberately unlabeled and out of order, because Solid -> Locked
only counts when nothing signposts the method.

Every number below is COMPUTED, never typed. The key text interpolates the same
variables the assertions in verify_sheets.py check.
"""
from fractions import Fraction as F
from math import ceil


def mixed(f):
    """17/12 -> '1 5/12'. Keeps the key readable for a 3rd/4th grader's parent."""
    if f.denominator == 1:
        return str(f.numerator)
    whole, rem = divmod(f.numerator, f.denominator)
    if whole:
        return "%d %d/%d" % (whole, rem, f.denominator)
    return "%d/%d" % (f.numerator, f.denominator)


def money(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


# ---------------------------------------------------------------- Jul 29
# 53 gauges into boxes of 8; 87 students into vans of 9
w1_full, w1_left = divmod(53, 8)
w1_boxes = ceil(53 / 8)
w1_vans = ceil(87 / 9)
w1_read = 6 * 24 - 18
w1_side = 48 // 6
w1_per = 2 * (6 + w1_side)
y1_a = F(1, 2) + F(1, 3)
y1_b = F(3, 4) - F(2, 5)
y1_c = F(2, 3) + F(3, 4)
y1_d = 36 * 24
y1_e = 45 * 18 - 210

JUL29 = {
    "file": "worksheet-weather.html",
    "title_plain": "Weather Watch",
    "title": "🌦️ Weather Watch",
    "sub": "Storm-chasing word problems — read carefully, the last step is the one that counts",
    "kid1": [
        {"guided": ["53 &divide; 8 = <span class='blank'></span> remainder <span class='blank'></span>",
                    "Boxes that are completely full: <span class='blank'></span>",
                    "The leftover gauges still need a box, so boxes needed: <span class='blank'></span>"],
         "q": "A weather station packs 53 rain gauges into boxes. Each box holds 8. How many boxes are <b>completely full</b>, and how many gauges are left over? Then: how many boxes do they need to carry <b>all</b> of them?",
         "fact": "Raindrops are not tear-shaped. They start round and squash flatter as they fall, more like a tiny burger bun.",
         "a": "%d full boxes, %d left over — but %d boxes to carry them all." % (w1_full, w1_left, w1_boxes),
         "steps": "53 &divide; 8 = <b>%d remainder %d</b>. Those %d leftover gauges still have to go somewhere, so you need one more box: <b>%d</b>." % (w1_full, w1_left, w1_left, w1_boxes)},
        {"q": "87 students travel to the weather museum. Each van seats 9. How many vans does the school need?",
         "fact": "A weather balloon climbs about 30 km before the air gets so thin that it bursts.",
         "a": "%d vans." % w1_vans,
         "steps": "87 &divide; 9 = 9 remainder 6. Nine vans leaves 6 students behind, so the answer is <b>%d</b>, not 9." % w1_vans},
        {"q": "A station records 6 readings every day for 24 days. Later, 18 readings are found to be spoiled and thrown out. How many good readings are left?",
         "fact": "Lightning heats the air around it to about 30,000 &deg;C — roughly five times hotter than the surface of the sun.",
         "a": "%d readings." % w1_read,
         "steps": "6 &times; 24 = 144, then 144 &minus; 18 = <b>%d</b>." % w1_read},
        {"q": "Two rain barrels are collecting water. One is <b>3/4</b> full. The other is <b>5/8</b> full. Which barrel has more water in it? How do you know?",
         "fact": "A single cloud can weigh hundreds of tonnes. The droplets are so tiny that the air holds them up anyway.",
         "a": "The 3/4 barrel.",
         "steps": "Give them the same bottom number: 3/4 = <b>6/8</b>. Now compare 6/8 with 5/8 &mdash; 6 eighths is more."},
        {"q": "A rectangular weather deck covers <b>48 square metres</b>. One side measures <b>6 m</b>. How long is the other side? What is the perimeter all the way around?",
         "fact": "The strongest surface wind gust ever recorded was 408 km/h, on Barrow Island, Australia, in 1996.",
         "a": "Other side %d m; perimeter %d m." % (w1_side, w1_per),
         "steps": "Area = side &times; side, so 48 &divide; 6 = <b>%d m</b>. Perimeter = 6 + %d + 6 + %d = <b>%d m</b>." % (w1_side, w1_side, w1_side, w1_per)},
    ],
    "kid2": [
        {"guided": ["A common bottom number for 2 and 3 is <span class='blank'></span>",
                    "1/2 = <span class='blank'></span>/6 &nbsp; and &nbsp; 1/3 = <span class='blank'></span>/6",
                    "Now add the top numbers only: <span class='blank'></span>"],
         "q": "On Monday 1/2 inch of rain fell. On Tuesday another 1/3 inch fell. How much rain fell over the two days?",
         "fact": "Rain is measured in depth, not volume — 1 inch of rain means the water would sit an inch deep if none drained away.",
         "a": "%s inch." % mixed(y1_a),
         "steps": "Sixths work for both. 1/2 = 3/6 and 1/3 = 2/6, so 3/6 + 2/6 = <b>%s</b>. Add the tops, keep the bottom." % mixed(y1_a)},
        {"q": "A gauge is holding <b>3/4</b> inch of water. Over a hot afternoon, <b>2/5</b> inch evaporates. How much water is left in the gauge?",
         "fact": "Evaporation is why puddles vanish without draining — the water leaves as an invisible gas.",
         "a": "%s inch." % mixed(y1_b),
         "steps": "Twentieths: 3/4 = 15/20 and 2/5 = 8/20. 15/20 &minus; 8/20 = <b>%s</b>." % mixed(y1_b)},
        {"q": "A mountain station measured <b>2/3</b> foot of snow on Monday and <b>3/4</b> foot on Tuesday. What was the total snowfall? Give your answer as a mixed number.",
         "fact": "Every snowflake grows six arms, because of the way water molecules lock together as they freeze.",
         "a": "%s feet (that is %s of a foot)." % (mixed(y1_c), y1_c),
         "steps": "Twelfths: 2/3 = 8/12 and 3/4 = 9/12. 8/12 + 9/12 = %s, which is more than a whole, so <b>%s</b>." % (y1_c, mixed(y1_c))},
        {"q": "A network has <b>36</b> weather stations. Each one sends <b>24</b> readings a day. How many readings arrive in one day?",
         "fact": "Weather forecasts are made by supercomputers solving millions of equations about the air at once.",
         "a": "%s readings." % "{:,}".format(y1_d),
         "steps": "36 &times; 24. Split it: (36 &times; 20) + (36 &times; 4) = 720 + 144 = <b>%s</b>." % "{:,}".format(y1_d)},
        {"q": "A weather balloon climbs at <b>45 metres each minute</b> for <b>18 minutes</b>. Then a downdraft pushes it back down <b>210 metres</b>. How high is the balloon now?",
         "fact": "You see lightning before you hear thunder because light travels about a million times faster than sound.",
         "a": "%d metres." % y1_e,
         "steps": "45 &times; 18 = 810 m climbed. Then 810 &minus; 210 = <b>%d m</b>." % y1_e},
    ],
    "kid1_watch": "#1 and #2 are the same trap twice: the division is easy, the <i>interpretation</i> is the test. Expect \"6 boxes\" and \"9 vans\" — both drop the leftovers on the floor. Ask \"where do the last 5 gauges go?\" and let him fix it himself. On #5, expect the other side right and the perimeter forgotten.",
    "kid2_watch": "Expect 1/2 + 1/3 = 2/5 on #1 — adding tops and bottoms straight across. That is THE error of this whole unit. Don't just correct it; ask whether 2/5 can be right when one day alone was already 1/2. #3 asks for a mixed number, so 17/12 is only half-marks.",
}

# ---------------------------------------------------------------- Jul 30
w2_full, w2_left = divmod(74, 8)
w2_trays = ceil(74 / 8)
w2_drive = 128 * 7 - 245
w2_photo = (12 * 5 - 8) // 4
w2_side = 56 // 7
w2_per = 2 * (7 + w2_side)
y2_a = F(3, 8) + F(1, 6)
y2_q, y2_r = divmod(1246, 5)
y2_c = 4.75 - 1.8
y2_d = 48 * 25
y2_e = 3.5 * 24 - 12.5

JUL30 = {
    "file": "worksheet-mars-rovers.html",
    "title_plain": "Rover Report",
    "title": "🛰️ Rover Report",
    "sub": "Word problems from the surface of Mars",
    "kid1": [
        {"q": "A rover collects 74 rock samples. Each storage tray holds 8. How many trays are <b>completely full</b>? How many trays are needed to store <b>every</b> sample?",
         "fact": "A day on Mars is called a sol, and it lasts about 24 hours 37 minutes — just a little longer than ours.",
         "a": "%d full trays; %d trays to hold them all." % (w2_full, w2_trays),
         "steps": "74 &divide; 8 = %d remainder %d. The %d spare samples need a tray of their own: <b>%d</b>." % (w2_full, w2_left, w2_left, w2_trays)},
        {"q": "A rover drives <b>128 metres</b> a day for <b>7 days</b>. Of that distance, <b>245 metres</b> was backtracking over ground it had already covered. How much new ground did it cover?",
         "fact": "Radio signals take between 4 and 24 minutes to reach Mars, so nobody can steer a rover live — it has to think for itself.",
         "a": "%d metres." % w2_drive,
         "steps": "128 &times; 7 = 896 m driven. Then 896 &minus; 245 = <b>%d m</b> of new ground." % w2_drive},
        {"q": "A rover takes <b>12 photos</b> a day for <b>5 days</b>. The team deletes <b>8</b> blurry ones, then shares the rest equally between <b>4</b> scientists. How many photos does each scientist get?",
         "fact": "Ingenuity, a helicopter the size of a tissue box, made the first powered flight on another planet in 2021.",
         "a": "%d photos each." % w2_photo,
         "steps": "12 &times; 5 = 60, then 60 &minus; 8 = 52, then 52 &divide; 4 = <b>%d</b>. Three steps, in that order." % w2_photo},
        {"q": "One rover's battery is <b>2/3</b> charged. Another is <b>5/9</b> charged. Which rover has more charge left?",
         "fact": "Opportunity was built to last 90 days. It kept working for about 15 years.",
         "a": "The 2/3 rover.",
         "steps": "Ninths for both: 2/3 = <b>6/9</b>. And 6/9 beats 5/9."},
        {"q": "A rectangular solar panel covers <b>56 square feet</b>. One side is <b>7 feet</b> long. How long is the other side, and what is the perimeter?",
         "fact": "Martian dust storms can swallow the entire planet, and the dust settling on solar panels is what finally stopped Opportunity.",
         "a": "Other side %d ft; perimeter %d ft." % (w2_side, w2_per),
         "steps": "56 &divide; 7 = <b>%d ft</b>. Perimeter = 7 + %d + 7 + %d = <b>%d ft</b>." % (w2_side, w2_side, w2_side, w2_per)},
    ],
    "kid2": [
        {"q": "A rover spends <b>3/8</b> of a sol drilling and <b>1/6</b> of a sol driving. What fraction of the sol is that altogether?",
         "fact": "Mars has the tallest volcano in the solar system — Olympus Mons, about 22 km high, nearly three Everests.",
         "a": "%s of a sol." % mixed(y2_a),
         "steps": "24ths work for 8 and 6: 3/8 = 9/24 and 1/6 = 4/24. 9/24 + 4/24 = <b>%s</b>." % mixed(y2_a)},
        {"q": "A rover covers <b>1,246 metres</b> over <b>5 sols</b>, driving the same distance each sol with a little left over. How far each sol, and how much is left over?",
         "fact": "Mars' atmosphere is about 95% carbon dioxide, and so thin that liquid water would boil away almost instantly.",
         "a": "%d metres each sol, remainder %d." % (y2_q, y2_r),
         "steps": "1,246 &divide; 5 = <b>%d remainder %d</b>. Check: %d &times; 5 = %s, plus %d = 1,246. &check;" % (y2_q, y2_r, y2_q, "{:,}".format(y2_q * 5), y2_r)},
        {"q": "A battery holds <b>4.75</b> units of power. Crossing a dune uses <b>1.8</b> units. How much is left?",
         "fact": "Perseverance landed in Jezero Crater in 2021, a place scientists think was a river delta billions of years ago.",
         "a": "%s units." % money(y2_c),
         "steps": "Line up the decimal points and pad the gap: 4.75 &minus; 1.80 = <b>%s</b>. Writing 1.8 as 1.80 is what stops the mistake." % money(y2_c)},
        {"q": "Over <b>48 sols</b>, a rover sends back <b>25 photos</b> each sol. How many photos is that in total?",
         "fact": "Rovers carry their own nuclear battery, which is why they keep working through the freezing Martian night.",
         "a": "%s photos." % "{:,}".format(y2_d),
         "steps": "48 &times; 25. Easiest as 48 &times; 100 &divide; 4 = 4,800 &divide; 4 = <b>%s</b>." % "{:,}".format(y2_d)},
        {"q": "A rover travels at <b>3.5 metres per minute</b> for <b>24 minutes</b>, then reverses <b>12.5 metres</b> to get around a rock. How far from its start is it now?",
         "fact": "Rover wheels are aluminium, and Curiosity's picked up holes from sharp Martian rocks within its first two years.",
         "a": "%s metres." % money(y2_e),
         "steps": "3.5 &times; 24 = 84 m. Then 84 &minus; 12.5 = <b>%s m</b>." % money(y2_e)},
    ],
    "kid1_watch": "#1 is the remainder trap again — third day running. If he now answers 10 trays without being asked twice, that skill is moving from Shaky to Solid; write it in the log. #3 is the operation-order test: deleting before sharing gives 13, sharing before deleting gives 15 &minus; 8.",
    "kid2_watch": "#3 is where decimals bite: 4.75 &minus; 1.8 invites 4.57 or 3.05 if he doesn't pad the 1.8 to 1.80. Make him write the zero. #2's remainder is a real remainder, not a decimal — resist the urge to say 249.2.",
}

# ---------------------------------------------------------------- Jul 31
w3_full, w3_left = divmod(95, 6)
w3_crates = ceil(95 / 6)
w3_bees = 145 * 4 - 96
w3_share = (8 * 9) // 3
w3_side = 63 // 9
w3_per = 2 * (9 + w3_side)
y3_a = F(5, 6) - F(3, 8)
y3_q, y3_r = divmod(2375, 8)
y3_c = 2.4 + 3.75
y3_d = 34 * 56
y3_e = 15 * 12 - 45.5

JUL31 = {
    "file": "worksheet-honeybees.html",
    "title_plain": "The Hive",
    "title": "🐝 The Hive",
    "sub": "Word problems from the beekeeper's yard",
    "kid1": [
        {"q": "A beekeeper has 95 frames to move. Each crate holds 6 frames. How many crates are <b>completely full</b>, and how many crates does she need for <b>all</b> of them?",
         "fact": "Honeycomb cells are hexagons because that shape stores the most honey using the least wax.",
         "a": "%d full crates; %d crates in total." % (w3_full, w3_crates),
         "steps": "95 &divide; 6 = %d remainder %d. The last %d frames still need a crate: <b>%d</b>." % (w3_full, w3_left, w3_left, w3_crates)},
        {"q": "A hive gains <b>145 bees</b> a day for <b>4 days</b>. Over the same period <b>96 bees</b> do not return. What is the change in the hive's population?",
         "fact": "A single worker bee makes about one twelfth of a teaspoon of honey in her whole life.",
         "a": "Up by %d bees." % w3_bees,
         "steps": "145 &times; 4 = 580 gained, then 580 &minus; 96 = <b>%d</b>." % w3_bees},
        {"q": "There are <b>8 hives</b> with <b>9 frames</b> in each. The frames are shared equally between <b>3</b> beekeepers. How many frames does each beekeeper carry?",
         "fact": "Bees tell each other where flowers are by dancing in a figure of eight — the angle points the way.",
         "a": "%d frames each." % w3_share,
         "steps": "8 &times; 9 = 72 frames, then 72 &divide; 3 = <b>%d</b>." % w3_share},
        {"q": "One jar is <b>1/2</b> full of honey. Another is <b>4/10</b> full. Which jar has more honey?",
         "fact": "Honey found sealed in Egyptian tombs was still perfectly good to eat thousands of years later.",
         "a": "The 1/2 jar.",
         "steps": "Tenths: 1/2 = <b>5/10</b>, and 5/10 is more than 4/10."},
        {"q": "A rectangular bee garden covers <b>63 square metres</b>. One side is <b>9 m</b>. Find the other side and the perimeter.",
         "fact": "Bees can see ultraviolet light, so many flowers carry glowing patterns that guide them in like runway lights.",
         "a": "Other side %d m; perimeter %d m." % (w3_side, w3_per),
         "steps": "63 &divide; 9 = <b>%d m</b>. Perimeter = 9 + %d + 9 + %d = <b>%d m</b>." % (w3_side, w3_side, w3_side, w3_per)},
    ],
    "kid2": [
        {"q": "A frame is <b>5/6</b> filled with honey. The beekeeper takes <b>3/8</b> of a frame's worth. What fraction of the frame is still full?",
         "fact": "A strong hive can hold more than 50,000 bees in summer, and the queen may lay 2,000 eggs a day.",
         "a": "%s of the frame." % mixed(y3_a),
         "steps": "24ths: 5/6 = 20/24 and 3/8 = 9/24. 20/24 &minus; 9/24 = <b>%s</b>." % mixed(y3_a)},
        {"q": "A harvest of <b>2,375 grams</b> of honey is poured equally into <b>8</b> jars. How much goes in each jar, and how many grams are left over?",
         "fact": "Bees visit about two million flowers to make a single pound of honey.",
         "a": "%d grams per jar, %d grams left over." % (y3_q, y3_r),
         "steps": "2,375 &divide; 8 = <b>%d remainder %d</b>. Check: %d &times; 8 = %s, plus %d = 2,375. &check;" % (y3_q, y3_r, y3_q, "{:,}".format(y3_q * 8), y3_r)},
        {"q": "One hive produced <b>2.4 kg</b> of honey and another produced <b>3.75 kg</b>. What is the total?",
         "fact": "Bees keep the middle of the hive at about 35 &deg;C all year by shivering to warm it and fanning to cool it.",
         "a": "%s kg." % money(y3_c),
         "steps": "Pad the shorter one: 2.40 + 3.75 = <b>%s kg</b>." % money(y3_c)},
        {"q": "An apiary has <b>34 hives</b>, each holding <b>56 frames</b>. How many frames altogether?",
         "fact": "Beekeepers use smoke because it masks the alarm signal bees release, so the hive stays calm.",
         "a": "%s frames." % "{:,}".format(y3_d),
         "steps": "34 &times; 56 = (34 &times; 50) + (34 &times; 6) = 1,700 + 204 = <b>%s</b>." % "{:,}".format(y3_d)},
        {"q": "A hive yields <b>15 kg</b> of honey a week for <b>12 weeks</b>. The beekeeper sells <b>45.5 kg</b> at the market. How much is left?",
         "fact": "Honey never spoils. Its sugar draws water out of any bacteria that lands in it.",
         "a": "%s kg." % money(y3_e),
         "steps": "15 &times; 12 = 180 kg, then 180 &minus; 45.5 = <b>%s kg</b>." % money(y3_e)},
    ],
    "kid1_watch": "Fourth day on remainders. If #1 comes back as 16 crates first time, with no prompting, that is <b>two clean runs in a row</b> — check the log, because the step-up rule may now be satisfied for this skill.",
    "kid2_watch": "#1 and the Jul 30 sheet's #1 are the same skill in opposite directions (add vs subtract). Getting the add right and the subtract wrong usually means he is finding the common denominator fine but slipping on the borrow.",
}

# ---------------------------------------------------------------- Aug 1 (timed)
w4_full, w4_left = divmod(68, 9)
w4_boats = ceil(68 / 9)
w4_rope = 236 * 3 - 159
w4_share = (6 * 14) // 7
w4_side = 72 // 8
w4_per = 2 * (8 + w4_side)
y4_a = F(7, 10) + F(1, 4)
y4_q, y4_r = divmod(3428, 6)
y4_c = 12.6 - 4.85
y4_d = 62 * 45
y4_e = 8.5 * 14 - 23.5

AUG1 = {
    "file": "worksheet-sailing-ships.html",
    "title_plain": "Under Sail",
    "title": "⛵ Under Sail",
    "sub": "Word problems from the age of sail — this one is TIMED, so work steadily",
    "kid1": [
        {"q": "68 sailors must leave a ship. Each lifeboat holds 9. How many lifeboats are <b>completely full</b>, and how many lifeboats are launched altogether?",
         "fact": "A ship's speed is measured in knots, from the knots tied along a rope that sailors let run out behind them.",
         "a": "%d full boats; %d launched." % (w4_full, w4_boats),
         "steps": "68 &divide; 9 = %d remainder %d. You cannot leave %d sailors aboard, so <b>%d</b> boats go." % (w4_full, w4_left, w4_left, w4_boats)},
        {"q": "A rope-maker produces <b>236 metres</b> of rope a day for <b>3 days</b>. Then <b>159 metres</b> is cut away as damaged. How much good rope is left?",
         "fact": "A big sailing warship needed more than 30 km of rope in its rigging.",
         "a": "%d metres." % w4_rope,
         "steps": "236 &times; 3 = 708 m, then 708 &minus; 159 = <b>%d m</b>." % w4_rope},
        {"q": "<b>6 ships</b> each carry <b>14 crates</b>. The crates are unloaded evenly across <b>7 ports</b>. How many crates does each port receive?",
         "fact": "Tea clippers raced each other from China to London, and the first ship home got the best price for its cargo.",
         "a": "%d crates each." % w4_share,
         "steps": "6 &times; 14 = 84 crates, then 84 &divide; 7 = <b>%d</b>." % w4_share},
        {"q": "One water barrel is <b>3/5</b> full. Another is <b>7/10</b> full. Which barrel holds more?",
         "fact": "Fresh water, not food, usually decided how long a voyage could last.",
         "a": "The 7/10 barrel.",
         "steps": "Tenths: 3/5 = <b>6/10</b>. And 7/10 is more than 6/10."},
        {"q": "A rectangular deck covers <b>72 square metres</b>. One side is <b>8 m</b>. Find the other side and the perimeter.",
         "fact": "Sailors marked time with a sandglass and a bell, ringing it every half hour through a four-hour watch.",
         "a": "Other side %d m; perimeter %d m." % (w4_side, w4_per),
         "steps": "72 &divide; 8 = <b>%d m</b>. Perimeter = 8 + %d + 8 + %d = <b>%d m</b>." % (w4_side, w4_side, w4_side, w4_per)},
    ],
    "kid2": [
        {"q": "A voyage is <b>7/10</b> complete. The next leg adds another <b>1/4</b> of the whole voyage. What fraction is complete now?",
         "fact": "A lateen sail, triangular instead of square, lets a ship sail much closer to the wind — Arab dhows used them for centuries.",
         "a": "%s of the voyage." % mixed(y4_a),
         "steps": "20ths: 7/10 = 14/20 and 1/4 = 5/20. 14/20 + 5/20 = <b>%s</b> &mdash; not quite there yet." % mixed(y4_a)},
        {"q": "<b>3,428 litres</b> of water are shared equally between <b>6</b> barrels. How much goes in each barrel, and how much is left over?",
         "fact": "Working out longitude at sea needed a clock accurate at sea — the problem took decades and a national prize to solve.",
         "a": "%d litres each, %d left over." % (y4_q, y4_r),
         "steps": "3,428 &divide; 6 = <b>%d remainder %d</b>. Check: %d &times; 6 = %s, plus %d = 3,428. &check;" % (y4_q, y4_r, y4_q, "{:,}".format(y4_q * 6), y4_r)},
        {"q": "A hold has <b>12.6 tonnes</b> of cargo. At the first port <b>4.85 tonnes</b> comes off. How much remains?",
         "fact": "Ships carry ballast — heavy weight low down — because an empty ship rides high and tips over more easily.",
         "a": "%s tonnes." % money(y4_c),
         "steps": "Pad it out: 12.60 &minus; 4.85 = <b>%s</b>. The borrow across the decimal point is where this goes wrong." % money(y4_c)},
        {"q": "A fleet of <b>62 ships</b> each carries <b>45 barrels</b>. How many barrels in the fleet?",
         "fact": "The Cutty Sark could cover more than 550 km in a single day with a good wind behind her.",
         "a": "%s barrels." % "{:,}".format(y4_d),
         "steps": "62 &times; 45 = (62 &times; 40) + (62 &times; 5) = 2,480 + 310 = <b>%s</b>." % "{:,}".format(y4_d)},
        {"q": "A ship sails at <b>8.5 nautical miles per hour</b> for <b>14 hours</b>, then a current pushes her back <b>23.5 nautical miles</b>. How far has she actually made good?",
         "fact": "A nautical mile is one minute of latitude, which is why it is slightly longer than a mile on land.",
         "a": "%s nautical miles." % money(y4_e),
         "steps": "8.5 &times; 14 = 119, then 119 &minus; 23.5 = <b>%s</b>." % money(y4_e)},
    ],
    "kid1_watch": "This sheet is <b>timed</b> — note the minutes in the log even if you note nothing else, because the step-up rule needs \"under time AND zero errors,\" and time is the half that never gets recorded. Don't hurry him mid-problem; just write down what it took.",
    "kid2_watch": "Timed sheet. Speed usually costs the decimal problems first (#3) — a rushed 12.6 &minus; 4.85 becomes 8.25 or 7.85. If accuracy holds under time here, decimals are close to Solid.",
}

# ---------------------------------------------------------------- Aug 2 (cumulative)
w5_side = 54 // 6
w5_per = 2 * (6 + w5_side)
w5_full, w5_left = divmod(77, 8)
w5_trips = ceil(77 / 8)
w5_climb = 174 * 5 - 218
w5_mule = (9 * 6 - 12) // 6
y5_a = 38 * 47
y5_b = F(5, 6) - F(1, 4)
y5_q, y5_r = divmod(4215, 7)
y5_d = 9.4 - 3.65
y5_e = 320 * 7 - 465

AUG2 = {
    "file": "worksheet-mountains-cumulative.html",
    "title_plain": "Above the Snow Line — Cumulative",
    "title": "🏔️ Above the Snow Line",
    "sub": "CUMULATIVE — the problems are shuffled and nothing tells you which method to use. That is the test.",
    "kid1": [
        {"q": "A tent floor covers <b>54 square metres</b>. One side is <b>6 m</b>. How long is the other side, and what is the perimeter?",
         "fact": "Everest grows a few millimetres taller every year, because India is still pushing north into Asia.",
         "a": "Other side %d m; perimeter %d m." % (w5_side, w5_per),
         "steps": "54 &divide; 6 = <b>%d m</b>. Perimeter = 6 + %d + 6 + %d = <b>%d m</b>." % (w5_side, w5_side, w5_side, w5_per)},
        {"q": "77 climbers are waiting for a cable car that carries 8 people. How many trips are needed to get everyone up?",
         "fact": "Above about 8,000 m is the \"death zone\", where there is too little oxygen for a body to recover, even resting.",
         "a": "%d trips." % w5_trips,
         "steps": "77 &divide; 8 = %d remainder %d. The last %d climbers still need a ride: <b>%d</b> trips." % (w5_full, w5_left, w5_left, w5_trips)},
        {"q": "One team has climbed <b>5/8</b> of the route. Another has climbed <b>2/3</b>. Which team is further along?",
         "fact": "Mauna Kea in Hawaii is taller than Everest measured from its base — but most of it is under the sea.",
         "a": "The 2/3 team.",
         "steps": "24ths: 5/8 = 15/24 and 2/3 = <b>16/24</b>. 16 beats 15, so 2/3 is further &mdash; only just."},
        {"q": "A team climbs <b>174 metres</b> a day for <b>5 days</b>, then descends <b>218 metres</b> to a safer camp. What height have they gained overall?",
         "fact": "Air cools by about 6.5 &deg;C for every 1,000 m you climb, which is why snow sits on peaks in hot countries.",
         "a": "%d metres." % w5_climb,
         "steps": "174 &times; 5 = 870 m, then 870 &minus; 218 = <b>%d m</b>." % w5_climb},
        {"q": "<b>9 teams</b> each carry <b>6 packs</b>. <b>12 packs</b> are left at base camp. The rest are shared equally between <b>6 mules</b>. How many packs does each mule carry?",
         "fact": "Sherpa climbers' bodies use oxygen more efficiently at altitude — an adaptation built up over thousands of years.",
         "a": "%d packs each." % w5_mule,
         "steps": "9 &times; 6 = 54, then 54 &minus; 12 = 42, then 42 &divide; 6 = <b>%d</b>. Three steps, and the order matters." % w5_mule},
    ],
    "kid2": [
        {"q": "A supply run carries <b>38</b> boxes, each holding <b>47</b> ration packs. How many packs is that?",
         "fact": "K2 is lower than Everest but far deadlier — steeper, stormier, and with no easy route to the top.",
         "a": "%s packs." % "{:,}".format(y5_a),
         "steps": "38 &times; 47 = (38 &times; 40) + (38 &times; 7) = 1,520 + 266 = <b>%s</b>." % "{:,}".format(y5_a)},
        {"q": "A rope is <b>5/6</b> of the way down a cliff. It is then pulled back up by <b>1/4</b> of the cliff's height. How far down is the rope now?",
         "fact": "Climbing ropes are built to stretch. A rope that could not stretch would jolt a falling climber hard enough to injure them.",
         "a": "%s of the way down." % mixed(y5_b),
         "steps": "12ths: 5/6 = 10/12 and 1/4 = 3/12. 10/12 &minus; 3/12 = <b>%s</b>." % mixed(y5_b)},
        {"q": "A <b>4,215 metre</b> ascent is split equally across <b>7</b> days. How far each day, and what is left over?",
         "fact": "Altitude sickness can begin as low as 2,500 m, and the only reliable cure is to go back down.",
         "a": "%d metres a day, remainder %d." % (y5_q, y5_r),
         "steps": "4,215 &divide; 7 = <b>%d remainder %d</b>. Check: %d &times; 7 = %s, plus %d = 4,215. &check;" % (y5_q, y5_r, y5_q, "{:,}".format(y5_q * 7), y5_r)},
        {"q": "A climber carries <b>9.4 kg</b> and drops <b>3.65 kg</b> of gear at a camp. What is the new pack weight?",
         "fact": "Every kilogram carried above 7,000 m costs roughly twice the effort it would at sea level.",
         "a": "%s kg." % money(y5_d),
         "steps": "9.40 &minus; 3.65 = <b>%s kg</b>. Pad the 9.4 to 9.40 first." % money(y5_d)},
        {"q": "A group climbs at <b>320 metres per hour</b> for <b>7 hours</b>, then descends <b>465 metres</b> to camp. What is their height gain for the day?",
         "fact": "Climbers often \"climb high, sleep low\" on purpose — going up to work the body, coming down to recover.",
         "a": "%s metres." % "{:,}".format(y5_e),
         "steps": "320 &times; 7 = 2,240 m, then 2,240 &minus; 465 = <b>%s m</b>." % "{:,}".format(y5_e)},
    ],
    "kid1_watch": "This is the <b>Locked</b> test. All five of his pinned skills are here, shuffled, with nothing naming the method — #2 is the remainder problem sitting between a perimeter question and a fraction comparison. Getting #2 right <i>here</i> is worth more than four right on a sheet where every problem was division. Mark Locked only if he chose the method himself.",
    "kid2_watch": "Same test for the 4th grader — #2 is unlike denominators with no heading announcing it. Watch whether he still reaches for a common denominator when the problem doesn't look like a fractions worksheet. If he adds across the top and bottom here after four clean days, the skill is Shaky, not Solid, and the plan says re-teach rather than push on.",
}

# ---------------------------------------------------------------- Aug 16 (Block 2 restart)
# Nothing printed between Aug 1 and Aug 16 — the Aug 10-16 TEACH day never ran, so this
# is the Block 2 OPENER, not the Sunday cumulative the schedule grid names. Same shape as
# JUL29: a faded TEACH, guided problem #1, no worked example. Each kid's guided problem
# sits on his PROTECTED skill (kid1 remainder interpretation, kid2 unlike denominators),
# which is what "Aug 10 opens with the guided problem again" means in PRACTICE-PLAN-2026.
w6_full, w6_left = divmod(59, 7)
w6_carts = ceil(59 / 7)
w6_towers = ceil(94 / 8)
w6_bricks = 136 * 6 - 87
w6_side = 96 // 8
w6_per = 2 * (8 + w6_side)
y6_a = F(2, 5) + F(1, 3)
y6_b = F(5, 6) - F(2, 9)
y6_c = F(5, 6) + F(3, 4)
y6_d = 47 * 36
y6_rate = 288 // 6
y6_e = y6_rate * 11 - 37

AUG16 = {
    "file": "worksheet-castles.html",
    "title_plain": "Castle Keep",
    "title": "🏰 Castle Keep",
    "sub": "Back after a break — take the first one slowly, the steps are printed for you",
    "kid1": [
        {"guided": ["59 &divide; 7 = <span class='blank'></span> remainder <span class='blank'></span>",
                    "Carts that go out completely full: <span class='blank'></span>",
                    "The leftover stones still need a cart, so carts needed: <span class='blank'></span>"],
         "q": "A mason loads 59 stones onto carts. Each cart holds 7. How many carts go out <b>completely full</b>, and how many stones are left over? Then: how many carts does he need to move <b>every</b> stone?",
         "fact": "Masons carved a personal mark into each stone they cut, because they were paid by the stone.",
         "a": "%d full carts, %d left over — but %d carts to move them all." % (w6_full, w6_left, w6_carts),
         "steps": "59 &divide; 7 = <b>%d remainder %d</b>. Those %d spare stones still have to travel, so one more cart: <b>%d</b>." % (w6_full, w6_left, w6_left, w6_carts)},
        {"q": "94 archers are posted to the towers. Each tower holds 8 archers. How many towers are needed so that <b>every</b> archer has a place?",
         "fact": "An arrow slit is narrow on the outside and wide on the inside, so the archer can swing his aim while staying a tiny target.",
         "a": "%d towers." % w6_towers,
         "steps": "94 &divide; 8 = 11 remainder 6. Eleven towers leaves 6 archers standing in the yard, so the answer is <b>%d</b>, not 11." % w6_towers},
        {"q": "A wall crew lays <b>136 bricks</b> a day for <b>6 days</b>. Then <b>87</b> bricks are found cracked and pulled back out. How many bricks are left in the wall?",
         "fact": "Many castle walls were whitewashed. The Tower of London's keep is called the White Tower for exactly that reason.",
         "a": "%d bricks." % w6_bricks,
         "steps": "136 &times; 6 = 816, then 816 &minus; 87 = <b>%d</b>." % w6_bricks},
        {"q": "Two water barrels stand in the courtyard. One is <b>5/6</b> full. The other is <b>3/4</b> full. Which barrel holds more water? How do you know?",
         "fact": "Most castle moats were dry. A ditch was there to stop attackers tunnelling under the wall, not to hold water.",
         "a": "The 5/6 barrel.",
         "steps": "Give them the same bottom number. Twelfths work: 5/6 = <b>10/12</b> and 3/4 = <b>9/12</b>. Ten twelfths beats nine."},
        {"q": "A rectangular courtyard covers <b>96 square metres</b>. One side measures <b>8 m</b>. How long is the other side? What is the perimeter all the way around?",
         "fact": "The base of a castle wall was often built sloping outward, so a stone dropped from above bounced off it into the attackers.",
         "a": "Other side %d m; perimeter %d m." % (w6_side, w6_per),
         "steps": "Area = side &times; side, so 96 &divide; 8 = <b>%d m</b>. Perimeter = 8 + %d + 8 + %d = <b>%d m</b>." % (w6_side, w6_side, w6_side, w6_per)},
    ],
    "kid2": [
        {"guided": ["A common bottom number for 5 and 3 is <span class='blank'></span>",
                    "2/5 = <span class='blank'></span>/15 &nbsp; and &nbsp; 1/3 = <span class='blank'></span>/15",
                    "Now add the top numbers only, keep the bottom: <span class='blank'></span>"],
         "q": "A cistern is filled in two goes. In the morning <b>2/5</b> of it is filled. In the afternoon another <b>1/3</b> is filled. How much of the cistern is full?",
         "fact": "A castle under siege lost to thirst long before hunger, so the well was usually the first thing dug.",
         "a": "%s of the cistern." % mixed(y6_a),
         "steps": "Fifteenths work for both. 2/5 = 6/15 and 1/3 = 5/15, so 6/15 + 5/15 = <b>%s</b>. Add the tops, keep the bottom." % mixed(y6_a)},
        {"q": "A grain store is <b>5/6</b> full. Over the winter, <b>2/9</b> of the store is eaten. How much grain is left?",
         "fact": "Grain was stored high up and dry, because damp grain rots and a rotten store could end a siege on its own.",
         "a": "%s of the store." % mixed(y6_b),
         "steps": "Eighteenths: 5/6 = 15/18 and 2/9 = 4/18. 15/18 &minus; 4/18 = <b>%s</b>." % mixed(y6_b)},
        {"q": "One quarry sends <b>5/6</b> of a cartload of lime. Another sends <b>3/4</b> of a cartload. How much lime arrives altogether? Give your answer as a <b>mixed number</b>.",
         "fact": "Lime mortar sets slowly and keeps hardening for years, which is why 900-year-old walls are still standing.",
         "a": "%s cartloads (that is %s)." % (mixed(y6_c), y6_c),
         "steps": "Twelfths: 5/6 = 10/12 and 3/4 = 9/12. 10/12 + 9/12 = %s, which is more than a whole, so <b>%s</b>." % (y6_c, mixed(y6_c))},
        {"q": "A castle has <b>47</b> arrow slits. Each one is stocked with <b>36</b> arrows. How many arrows is that altogether?",
         "fact": "A trained longbowman could loose about ten arrows a minute, so a well-stocked slit emptied fast.",
         "a": "%s arrows." % "{:,}".format(y6_d),
         "steps": "47 &times; 36. Split it: (47 &times; 30) + (47 &times; 6) = 1,410 + 282 = <b>%s</b>." % "{:,}".format(y6_d)},
        {"q": "A workshop makes <b>288 arrowheads in 6 days</b>, working at a steady rate. At that same rate, how many would it make in <b>11 days</b>? If <b>37</b> of those fail inspection, how many good arrowheads are there?",
         "fact": "A portcullis was dropped, not lowered — its own weight was the whole point, and winching it back up took several people.",
         "a": "%d arrowheads, %d of them good." % (y6_rate * 11, y6_e),
         "steps": "Find the one-day rate first: 288 &divide; 6 = <b>%d a day</b>. Then %d &times; 11 = <b>%d</b>. Finally %d &minus; 37 = <b>%d</b> good ones." % (y6_rate, y6_rate, y6_rate * 11, y6_rate * 11, y6_e)},
    ],
    "kid1_watch": "It has been over two weeks since the last sheet, so expect the remainder rule to have gone quiet rather than gone missing. #1 prints the steps; #2 does not, and #2 is the real read &mdash; \"11 towers\" means he divided correctly and stopped one step early. Ask \"where do the last 6 archers stand?\" and let him fix it himself. On #5, expect the missing side right and the perimeter forgotten.",
    "kid2_watch": "Expect 2/5 + 1/3 = 3/8 on #1 &mdash; adding straight across the top and bottom. That is THE error of this unit and it is the one most likely to have crept back over the break. Don't just correct it: ask whether 3/8 can be right when the morning alone already filled 2/5. #3 asks for a mixed number, so 19/12 is only half marks. On #5, if he jumps to 288 &times; 11, the missing idea is \"find one day first\".",
}

# ---------------------------------------------------------------- Aug 17
# Block 2 week 2 opens. The Shape column in PRACTICE-PLAN-2026 moves kid1 to
# area/perimeter-with-a-missing-side and kid2 to decimals, so THOSE take the
# guided slot this week — the guided problem always sits on the skill being
# introduced, not on last week's. kid1's old protected skill (remainder
# interpretation) drops to #2 unguided, which is where you read whether it held.
# Theme set by Asif 2026-08-17: immune system, for the whole week.
w7_side = 72 // 9
w7_per = 2 * (9 + w7_side)
w7_full, w7_left = divmod(75, 8)
w7_trays = ceil(75 / 8)
w7_good = 128 * 7 - 94
w7_p_side = (46 - 2 * 14) // 2          # perimeter 46, one side 14 -> other side
w7_area = 14 * w7_p_side
y7_a = F(84, 10) - F(375, 100)          # 8.4 - 3.75, exact
y7_b = 34 * 26
y7_c_full, y7_c_left = divmod(1347, 6)
y7_d = F(3, 8) + F(1, 3)
y7_cost = F(35, 100) * 240
y7_change = 100 - y7_cost

AUG17 = {
    "file": "worksheet-immune-system.html",
    "title_plain": "The Body's Defences",
    "title": "🛡️ The Body's Defences",
    "sub": "Word problems from inside the immune system — the first one has its steps printed for you",
    "kid1": [
        {"guided": ["Area = one side &times; the other side, so 72 &divide; 9 = <span class='blank'></span>",
                    "So the other side measures <span class='blank'></span> cm",
                    "Perimeter = 9 + <span class='blank'></span> + 9 + <span class='blank'></span> = <span class='blank'></span> cm"],
         "q": "A rectangular tray of blood samples covers <b>72 square centimetres</b>. One side measures <b>9 cm</b>. How long is the other side? What is the perimeter all the way around the tray?",
         "fact": "White blood cells are made inside your bones, in the soft marrow at the centre.",
         "a": "Other side %d cm; perimeter %d cm." % (w7_side, w7_per),
         "steps": "Area = side &times; side, so 72 &divide; 9 = <b>%d cm</b>. Perimeter goes all the way round: 9 + %d + 9 + %d = <b>%d cm</b>." % (w7_side, w7_side, w7_side, w7_per)},
        {"q": "A clinic packs 75 vaccine vials into trays. Each tray holds 8. How many trays go out <b>completely full</b>, and how many vials are left over? Then: how many trays are needed to carry <b>every</b> vial?",
         "fact": "A vaccine works by showing your immune system a harmless piece of a germ, so it can practise before the real one arrives.",
         "a": "%d full trays, %d left over — but %d trays to carry them all." % (w7_full, w7_left, w7_trays),
         "steps": "75 &divide; 8 = <b>%d remainder %d</b>. Those %d spare vials still have to travel, so one more tray: <b>%d</b>." % (w7_full, w7_left, w7_left, w7_trays)},
        {"q": "A lab grows <b>128 cell samples</b> a day for <b>7 days</b>. Then <b>94</b> of them are found spoiled and thrown out. How many good samples are left?",
         "fact": "Your body makes billions of new white blood cells every single day, and most of them last only a few days.",
         "a": "%d samples." % w7_good,
         "steps": "128 &times; 7 = 896, then 896 &minus; 94 = <b>%d</b>." % w7_good},
        {"q": "Two vials of serum sit on the bench. One is <b>5/8</b> full. The other is <b>2/3</b> full. Which vial holds more? How do you know?",
         "fact": "Tears and saliva both contain an enzyme that breaks bacteria apart — your eyes and mouth are defending you all day.",
         "a": "The 2/3 vial.",
         "steps": "Same bottom number &mdash; twenty-fourths: 5/8 = <b>15/24</b>, 2/3 = <b>16/24</b>. Sixteen beats fifteen, so the <i>smaller</i>-looking fraction wins."},
        {"q": "A rectangular culture plate has a <b>perimeter of 46 cm</b>. One side measures <b>14 cm</b>. How long is the other side? What is the <b>area</b> of the plate?",
         "fact": "Fever is not the germ hurting you — it is your body turning the heat up on purpose, because most germs breed badly when they are too warm.",
         "a": "Other side %d cm; area %d square cm." % (w7_p_side, w7_area),
         "steps": "Half the perimeter is one of each side: 46 &divide; 2 = <b>23</b>. Then 23 &minus; 14 = <b>%d cm</b>. Area = 14 &times; %d = <b>%d square cm</b>." % (w7_p_side, w7_p_side, w7_area)},
    ],
    "kid2": [
        {"guided": ["Give 8.4 the same number of decimal places as 3.75: <span class='blank'></span>",
                    "Line up the decimal points, then subtract: <span class='blank'></span>",
                    "So the amount still to give is <span class='blank'></span> mL"],
         "q": "A course of medicine is <b>8.4 mL</b> in total. So far <b>3.75 mL</b> has been given. How much is still to be given?",
         "fact": "Antibodies are Y-shaped, and each kind locks onto one specific germ and nothing else — like a key cut for a single door.",
         "a": "%s mL." % money(float(y7_a)),
         "steps": "Pad the short one: 8.4 becomes <b>8.40</b>. Then 8.40 &minus; 3.75 = <b>%s mL</b>. Skipping the padding is what produces 5.65 or 4.75." % money(float(y7_a))},
        {"q": "A researcher prepares <b>34</b> slides, and counts <b>26</b> antibodies on each one. How many antibodies is that altogether?",
         "fact": "Memory cells are why you usually catch chickenpox only once — some of them can still recognise the virus decades later.",
         "a": "%s antibodies." % "{:,}".format(y7_b),
         "steps": "34 &times; 26. Split it: (34 &times; 20) + (34 &times; 6) = 680 + 204 = <b>%s</b>." % "{:,}".format(y7_b)},
        {"q": "A hospital logs <b>1,347</b> cell counts and sorts them into batches of <b>6</b>. How many <b>complete</b> batches are there, and how many counts are left over?",
         "fact": "Your lymph system has no pump of its own. It only moves when you move, which is one reason walking helps you shake off an illness.",
         "a": "%d complete batches, %d left over." % (y7_c_full, y7_c_left),
         "steps": "1,347 &divide; 6 = <b>%d remainder %d</b>. Walk it: 13&divide;6 = 2 r1, bring down 4 &rarr; 14&divide;6 = 2 r2, bring down 7 &rarr; 27&divide;6 = 4 r3. Check: %s + %d = 1,347. &check;" % (y7_c_full, y7_c_left, "{:,}".format(y7_c_full * 6), y7_c_left)},
        {"q": "One study covers <b>3/8</b> of the samples in a freezer. A second study covers another <b>1/3</b> of them. What fraction of the freezer is covered by the two studies together?",
         "fact": "Most of your immune system sits around your gut — the body puts its defences where the outside world comes in.",
         "a": "%s of the freezer." % mixed(y7_d),
         "steps": "Twenty-fourths work for both. 3/8 = 9/24 and 1/3 = 8/24, so 9/24 + 8/24 = <b>%s</b>. Add the tops, keep the bottom." % mixed(y7_d)},
        {"q": "Antibody test strips cost <b>$0.35</b> each. A clinic buys <b>240</b> of them and pays with <b>$100</b>. What do the strips cost altogether, and how much change comes back?",
         "fact": "The thymus, the gland that trains your T-cells, is at its biggest when you are a child and slowly shrinks for the rest of your life.",
         "a": "$%s for the strips; $%s change." % (money(float(y7_cost)), money(float(y7_change))),
         "steps": "240 &times; $0.35 = (240&times;0.3) + (240&times;0.05) = 72 + 12 = <b>$%s</b>. Change: $100 &minus; $%s = <b>$%s</b>." % (money(float(y7_cost)), money(float(y7_cost)), money(float(y7_change)))},
    ],
    "kid1_watch": "#1 prints the steps and <b>#5 does not</b> &mdash; #5 is the real read, and it is the inverse: it hands him the perimeter and asks for a side. Expect 46 &minus; 14 = 32. One question fixes it: \"how many sides does the perimeter go along?\" On #2, remainder interpretation is unguided for the first time this week &mdash; \"9 trays\" means the method held and he stopped a step early. #4's trap is inverted on purpose.",
    "kid2_watch": "This unit lives or dies on <b>padding the short number</b>. #1 prints that step; nothing else does &mdash; expect 4.75 or 5.65 wherever he skips it. #5 stacks a rate, a decimal and a subtraction, and the usual failure is a right answer with a misplaced point ($8.40 or $840 for $84); make him say what it means aloud before writing. #3 has a real remainder &mdash; not 224.5.",
}

# ---------------------------------------------------------------- Aug 18
# THE TRACKS SPLIT HERE (PRACTICE-PLAN-2026, "DECIDED 2026-08-17 by Asif").
# kid1 continues on area/perimeter-with-a-missing-side, and his guided slot moves
# to the HARDER direction — perimeter given, find the side — because that is the
# one Aug 17 left unguided at #5 and flagged as the real read. The area->side
# direction he was guided through yesterday reappears at #5 unguided; that swap is
# the whole design of the day.
# kid2 goes BACK to unlike denominators for the guided slot — he had exactly one
# guided day on it (Aug 16) before the calendar moved him to decimals. Decimals do
# NOT disappear: #4 keeps one, unguided, so Aug 17 is not wasted.
# Theme stays immune system all week (Asif, 2026-08-17).
w8_p_side = (58 - 2 * 11) // 2          # perimeter 58, one side 11 -> other side
w8_area = 11 * w8_p_side
w8_full, w8_left = divmod(92, 6)
w8_racks = ceil(92 / 6)
w8_good = 146 * 8 - 79
w8_side = 108 // 12
w8_per = 2 * (12 + w8_side)
y8_a = F(1, 4) + F(2, 5)
y8_b = F(7, 8) - F(1, 3)
y8_c = 48 * 27
y8_given = F(24, 10) + F(375, 100)      # 2.4 + 3.75, exact
y8_left = F(95, 10) - y8_given          # 9.5 - that
y8_rate = 1455 // 5
y8_total = y8_rate * 9
y8_fold, y8_rem = divmod(y8_total, 8)

AUG18 = {
    "file": "worksheet-white-cells.html",
    "title_plain": "White Cell Patrol",
    "title": "🩸 White Cell Patrol",
    "sub": "Word problems from the blood lab — the first one has its steps printed for you",
    "kid1": [
        {"guided": ["Half the perimeter is one of each side: 58 &divide; 2 = <span class='blank'></span>",
                    "Take away the side you know: <span class='blank'></span> &minus; 11 = <span class='blank'></span> cm",
                    "Area = 11 &times; <span class='blank'></span> = <span class='blank'></span> square cm"],
         "q": "A rectangular sample tray has a <b>perimeter of 58 cm</b>. One side measures <b>11 cm</b>. How long is the other side? What is the <b>area</b> of the tray?",
         "fact": "A cut stops bleeding because tiny cell fragments called platelets pile into the gap and turn sticky.",
         "a": "Other side %d cm; area %d square cm." % (w8_p_side, w8_area),
         "steps": "Halve the perimeter first: 58 &divide; 2 = <b>29</b> &mdash; one long side plus one short side. Then 29 &minus; 11 = <b>%d cm</b>. Area = 11 &times; %d = <b>%d square cm</b>. Answering 47 means the halving was skipped." % (w8_p_side, w8_p_side, w8_area)},
        {"q": "A lab loads 92 blood samples into racks. Each rack holds 6. How many racks are <b>completely full</b>, and how many samples are left over? Then: how many racks are needed to hold <b>every</b> sample?",
         "fact": "Pus is mostly white blood cells that have finished their work — it is a sign the defence turned up.",
         "a": "%d full racks, %d left over — but %d racks to hold them all." % (w8_full, w8_left, w8_racks),
         "steps": "92 &divide; 6 = <b>%d remainder %d</b>. Those %d spare samples still need somewhere to sit, so one more rack: <b>%d</b>." % (w8_full, w8_left, w8_left, w8_racks)},
        {"q": "A lab grows <b>146 cultures</b> a day for <b>8 days</b>. Then <b>79</b> of them are found spoiled and thrown out. How many good cultures are left?",
         "fact": "Your tonsils are lumps of immune tissue placed right at the back of the throat, where swallowed germs go past.",
         "a": "%s cultures." % "{:,}".format(w8_good),
         "steps": "146 &times; 8 = 1,168, then 1,168 &minus; 79 = <b>%s</b>." % "{:,}".format(w8_good)},
        {"q": "Two dishes sit on the bench. One is <b>3/5</b> full. The other is <b>7/12</b> full. Which dish holds more? How do you know?",
         "fact": "Mucus is not waste. It traps dust and germs, and tiny hairs then sweep the whole lot back out.",
         "a": "The 3/5 dish.",
         "steps": "Bigger numbers do not mean a bigger fraction. Sixtieths: 3/5 = <b>36/60</b>, 7/12 = <b>35/60</b>. <b>3/5</b> wins, by one sixtieth."},
        {"q": "A rectangular culture plate covers <b>108 square centimetres</b>. One side measures <b>12 cm</b>. How long is the other side? What is the <b>perimeter</b> all the way around?",
         "fact": "A swollen lump in your neck when you are ill is a lymph node at work — it fills with cells fighting the infection.",
         "a": "Other side %d cm; perimeter %d cm." % (w8_side, w8_per),
         "steps": "Area = side &times; side, so 108 &divide; 12 = <b>%d cm</b>. Perimeter goes all the way round: 12 + %d + 12 + %d = <b>%d cm</b>." % (w8_side, w8_side, w8_side, w8_per)},
    ],
    "kid2": [
        {"guided": ["A common bottom number for 4 and 5 is <span class='blank'></span>",
                    "1/4 = <span class='blank'></span>/20 &nbsp; and &nbsp; 2/5 = <span class='blank'></span>/20",
                    "Now add the top numbers only, keep the bottom: <span class='blank'></span>"],
         "q": "A vial is filled in two goes. In the morning <b>1/4</b> of it is filled. In the afternoon another <b>2/5</b> is filled. How full is the vial?",
         "fact": "Your stomach acid is strong enough to kill most germs you swallow before they ever reach the gut.",
         "a": "%s of the vial." % mixed(y8_a),
         "steps": "Twentieths: 1/4 = 5/20 and 2/5 = 8/20, so 5/20 + 8/20 = <b>%s</b>. Add the tops, keep the bottom." % mixed(y8_a)},
        {"q": "A store of serum is <b>7/8</b> full. Over one week, <b>1/3</b> of the store is used. How much serum is left?",
         "fact": "Blood is a little over half liquid plasma; the red cells, white cells and platelets float in it.",
         "a": "%s of the store." % mixed(y8_b),
         "steps": "Twenty-fourths: 7/8 = 21/24 and 1/3 = 8/24. 21/24 &minus; 8/24 = <b>%s</b>. The bottom number never changes." % mixed(y8_b)},
        {"q": "A store room holds <b>48</b> trays, and each tray carries <b>27</b> slides. How many slides is that altogether?",
         "fact": "A microlitre of blood — far less than a drop — holds roughly 4,000 to 11,000 white blood cells.",
         "a": "%s slides." % "{:,}".format(y8_c),
         "steps": "48 &times; 27. Split it: (48 &times; 20) + (48 &times; 7) = 960 + 336 = <b>%s</b>." % "{:,}".format(y8_c)},
        {"q": "A course of medicine is <b>9.5 mL</b> in total. A nurse gives <b>2.4 mL</b>, then later <b>3.75 mL</b>. How much has been given, and how much is still to come?",
         "fact": "Bone marrow makes about two million red blood cells every second.",
         "a": "%s mL given; %s mL still to come." % (money(float(y8_given)), money(float(y8_left))),
         "steps": "Pad to two places, line up the points. 2.40 + 3.75 = <b>%s</b>. Then 9.50 &minus; %s = <b>%s mL</b>. Skipped padding gives 6.79." % (money(float(y8_given)), money(float(y8_given)), money(float(y8_left)))},
        {"q": "A clinic runs <b>1,455 tests in 5 days</b>, at a steady rate. At that same rate, how many tests would it run in <b>9 days</b>? Those results are filed into folders of <b>8</b> — how many <b>complete</b> folders is that, and how many results are left over?",
         "fact": "White blood cells follow a chemical trail to a wound, moving toward wherever the signal is strongest.",
         "a": "%s tests — %d complete folders, %d left over." % ("{:,}".format(y8_total), y8_fold, y8_rem),
         "steps": "Find one day first: 1,455 &divide; 5 = <b>%d a day</b>. Then %d &times; 9 = <b>%s</b>. Finally %s &divide; 8 = <b>%d remainder %d</b>. Check: %s + %d = %s. &check;" % (y8_rate, y8_rate, "{:,}".format(y8_total), "{:,}".format(y8_total), y8_fold, y8_rem, "{:,}".format(y8_fold * 8), y8_rem, "{:,}".format(y8_total))},
    ],
    "kid1_watch": "Yesterday's guided problem and today's have <b>swapped directions</b>, on purpose. #1 walks him through the hard one &mdash; perimeter in, side out &mdash; and the halving line is the whole lesson; expect <b>47</b> if he treats it like an area problem. #5 is yesterday's <i>guided</i> problem with the scaffolding gone, so it reads whether that stuck. On #2 expect \"15 racks\": right division, one step short.",
    "kid2_watch": "He is back on unlike denominators after only <b>one</b> guided day on it. #1 prints the common-denominator step; <b>#2 does not</b>, and #2 is the real read &mdash; 6/11 there means he added straight across. Ask whether 6/11 can be right when the store started nearly full. #4 is yesterday's decimals unscaffolded: watch the padding. On #5, jumping to 1,455 &times; 9 means \"find one day first\" did not arrive.",
}

# ---------------------------------------------------------------- Oct 12
# First school-year set, maps theme. kid1 runs the STEP UP pin unchanged. kid2
# is on IM Grade 5 Unit 2 at school; each kid2 problem targets one error from his
# marked school packet (logged in private/RESULTS.md, 2026-10-12, not here: per-
# child mistakes stay out of git). Every unguided kid2 problem asks for one
# written sentence of WHY, because blank explanations cost him the most points.
o_good = 128 * 6 - 95
o_boats = ceil(75 / 8)
o_full, o_left = divmod(75, 8)
o_each = (4 * 12 - 18) // 5
o_side = 96 // 8
o_per = 2 * (8 + o_side)
z_strip = 6 * F(17, 5)                  # 6 x 3 2/5
z_small = 54 // 6
z_mtn = 3 * z_small
z_bread = F(8, 5)                       # Khadijah + 4 crew = 5 people
z_route = F(2, 3) * 130
z_area = F(5, 2) * F(3, 4)

OCT12 = {
    "file": "worksheet-mapmakers.html",
    "title_plain": "The Mapmakers",
    "title": "🗺️ The Mapmakers",
    "sub": "Word problems from the map room — write one line of <b>why</b>, not just the number",
    "kid1": [
        {"q": "A map workshop prints <b>128 maps a day</b> for <b>6 days</b>. Then <b>95</b> maps are found smudged and thrown away. How many good maps are left?",
         "fact": "Before printing, every map was copied by hand. One mistake by a tired copier could move a town for hundreds of years.",
         "a": "%d good maps." % o_good,
         "steps": "128 &times; 6 = <b>768</b>, then 768 &minus; 95 = <b>%d</b>." % o_good},
        {"q": "<b>75 explorers</b> must cross a lake. Each boat carries <b>8</b>. How many boats are <b>completely full</b>, and how many explorers are left over? Then: how many boats do they need so <b>nobody</b> is left behind?",
         "fact": "Old maps of unknown seas sometimes showed sea monsters in the empty parts, as a warning that nobody knew what was there.",
         "a": "%d full boats, %d left over — but %d boats so nobody is left." % (o_full, o_left, o_boats),
         "steps": "75 &divide; 8 = <b>%d remainder %d</b>. Those %d explorers still need a boat, so one more: <b>%d</b>." % (o_full, o_left, o_left, o_boats)},
        {"q": "Amina has <b>4 packs</b> of coloured pencils with <b>12</b> in each pack. She gives <b>18</b> to her brother Hamza. She shares the rest <b>equally</b> among <b>5</b> map-colouring friends. How many pencils does each friend get?",
         "fact": "Mapmakers colour seas blue and land green or brown, but there is no rule that says they must. It is a habit that stuck.",
         "a": "%d pencils each." % o_each,
         "steps": "4 &times; 12 = <b>48</b>. 48 &minus; 18 = <b>30</b>. 30 &divide; 5 = <b>%d</b>." % o_each},
        {"q": "Yusra has coloured <b>5/8</b> of her map. Hamza has coloured <b>2/3</b> of his map, which is the same size. Who has coloured more? How do you know?",
         "fact": "Al-Idrisi made a famous world map in the year 1154. It put south at the top, so it looks upside down to us today.",
         "a": "Hamza (2/3).",
         "steps": "Twenty-fourths: 5/8 = <b>15/24</b>, 2/3 = <b>16/24</b>. <b>Hamza</b> wins, by one twenty-fourth. Bigger numbers on the bottom do not mean more."},
        {"q": "A rectangular wall map covers <b>96 square inches</b>. One side is <b>8 inches</b>. How long is the other side? What is the <b>perimeter</b> of the map?",
         "fact": "A globe is the only map with no stretching. Every flat map squashes or stretches some part of the round Earth.",
         "a": "Other side %d in; perimeter %d in." % (o_side, o_per),
         "steps": "Area = side &times; side, so 96 &divide; 8 = <b>%d in</b>. Perimeter goes all the way round: 8 + %d + 8 + %d = <b>%d in</b>." % (o_side, o_side, o_side, o_per)},
    ],
    "kid2": [
        {"guided": ["Whole part: 6 &times; 3 = <span class='blank'></span>",
                    "Fraction part: 6 &times; 2/5 = <span class='blank'></span>/5 = <span class='blank'></span> (as a mixed number)",
                    "Add both parts: <span class='blank'></span> + <span class='blank'></span> = <span class='blank'></span> feet"],
         "q": "Each strip of a long map scroll is <b>3 2/5 feet</b> long. Nuh glues <b>6 strips</b> end to end. How long is the whole scroll?",
         "fact": "Ibn Battuta travelled about 75,000 miles in the 1300s, from Morocco to China, and his travel book was used like a map.",
         "a": "%s feet." % mixed(z_strip),
         "steps": "Break it apart. 6 &times; 3 = <b>18</b>. 6 &times; 2/5 = 12/5 = <b>2 2/5</b>. 18 + 2 2/5 = <b>%s feet</b>. Answering 2 2/5 or 18 2/5 means one part was dropped." % mixed(z_strip)},
        {"q": "The big map shows <b>6 times as many</b> rivers as the small map. The big map shows <b>54 rivers</b>. How many rivers are on the small map? The small map shows <b>3 times as many</b> mountains as rivers. How many mountains is that? <b>Write one sentence: why did you divide first, then multiply?</b>",
         "fact": "The Nile flows north, so on a normal map its water runs up the page, not down.",
         "a": "%d rivers on the small map; %d mountains." % (z_small, z_mtn),
         "steps": "The big map has the <i>bigger</i> number, so the small map is found by dividing: 54 &divide; 6 = <b>%d</b>. Then the mountains are the bigger amount, so multiply: 3 &times; %d = <b>%d</b>. 324 means he multiplied 54 &times; 6." % (z_small, z_small, z_mtn)},
        {"q": "Khadijah and her <b>4</b> crew mates share <b>8 loaves</b> of bread equally on a long voyage. How much bread does each person get? Write it as a fraction and as a mixed number. <b>Write one sentence: how many people are sharing, and how do you know?</b>",
         "fact": "Sailors found their way across open sea by measuring how high the Pole Star sat above the horizon.",
         "a": "%s = %s loaves each." % ("8/5", mixed(z_bread)),
         "steps": "Count everyone: Khadijah + 4 = <b>5 people</b>. 8 &divide; 5 = <b>8/5 = %s</b> loaves. Answering 2 means he divided by 4 and forgot Khadijah." % mixed(z_bread)},
        {"q": "A trade route is <b>130 miles</b> long. A caravan has travelled <b>2/3</b> of the way. How far has it gone? Give the <b>exact</b> answer as a mixed number. Is that more or less than <b>90 miles</b>? <b>Write one sentence: why?</b>",
         "fact": "Caravans stopped at inns called caravanserais, built about one day's walk apart along the Silk Road.",
         "a": "%s miles — less than 90." % mixed(z_route),
         "steps": "130 &divide; 3 = <b>43 1/3</b> (not 43 remainder 1). Two thirds is double that: 86 + 2/3 = <b>%s miles</b>. Less than 90 because 2/3 of 135 is 90, and 130 is less than 135. " % mixed(z_route)},
        {"q": "A map is <b>2 1/2 feet</b> wide and <b>3/4 foot</b> tall. What is its area? Draw and shade a model, or write the multiplication.",
         "fact": "Many maps are drawn so north is at the top, but medieval Christian maps often put east at the top, toward the sunrise.",
         "a": "%s square feet." % mixed(z_area),
         "steps": "2 1/2 = 5/2. 5/2 &times; 3/4 = <b>15/8 = %s square feet</b>. Or break it apart: 2 &times; 3/4 = 6/4 = 1 1/2, and 1/2 &times; 3/4 = 3/8. 1 1/2 + 3/8 = %s. &check;" % (mixed(z_area), mixed(z_area))},
    ],
    "kid1_watch": "The first sheet since August, so read it as a check-in, not a test. On #2 expect \"9 boats\": the right division, one step short. On #4 the numbers are deliberately close (15/24 vs 16/24); \"5/8, because 8 is bigger\" means he compared the bottoms. #5 is area &rarr; side &rarr; perimeter; expect <b>20</b> if he adds one length and one width and stops.",
    "kid2_watch": "Each problem is built from a point he lost on his Lesson 11/14 packets. #1 prints the break-apart steps (he twice <b>dropped the whole part</b>); #5 is the unscaffolded read. Expect <b>324</b> on #2, <b>2</b> on #3 (forgot Khadijah), <b>87</b> on #4 (remainder kept as a whole mile). <b>Grade the WHY sentences</b>: a right number with no sentence is half done.",
}

ALL = [JUL29, JUL30, JUL31, AUG1, AUG2, AUG16, AUG17, AUG18, OCT12]
