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

ALL = [JUL29, JUL30, JUL31, AUG1, AUG2]
