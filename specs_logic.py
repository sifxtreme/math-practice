"""The five logic sheets for Jul 29 - Aug 2. Four puzzles per kid (AGENTS.md allows 4-5).

Deliberately varied by REASONING TYPE, not by theme paint. Re-skinning the same
sum-and-difference puzzle five times teaches nothing the second time. Types used:

  working backwards . set overlap . interleaved pattern . substitution/balance
  logic grid . liar puzzle . LCM cycle . weighing . river crossing . elapsed time

Aug 2 is cumulative: it revisits the week's types with nothing naming them.
"""
from math import gcd


def lcm(a, b):
    return a * b // gcd(a, b)


# ---------------------------------------------------------------- Jul 29
l1_pat = [1, 2, 4, 7, 11]          # differences 1,2,3,4 -> next 16, 22
l1_next = [l1_pat[-1] + 5, l1_pat[-1] + 5 + 6]
l1_neither = 12 - (7 + 6 - 3)
l1_lenses = 3 * 2                  # 1 big = 3 small, 1 small = 2 lenses
l1_lens, l1_lamp = 4, 3            # 2L + M = 11, L + M = 7
l1_together = lcm(4, 6)
l1_times = 60 // l1_together

JUL29L = {
    "file": "worksheet-lighthouse-logic.html",
    "title_plain": "Lighthouse Logic",
    "title": "🗼 Lighthouse Logic",
    "sub": "Puzzles from the keepers of the coast — no calculator, just thinking",
    "kid1": [
        {"q": "A lighthouse flashes in a repeating pattern: <b>1, 2, 4, 7, 11, ___, ___</b>. What are the next two numbers, and what is the rule? (Hint: look at the gaps between them, not the numbers themselves.)",
         "fact": "Every lighthouse flashes its own pattern, called its character, so a sailor can tell which one they are looking at.",
         "a": "%d and %d. The gaps grow by one each time." % (l1_next[0], l1_next[1]),
         "steps": "Gaps are 1, 2, 3, 4 &mdash; so the next gaps are 5 and 6. 11 + 5 = <b>%d</b>, then %d + 6 = <b>%d</b>." % (l1_next[0], l1_next[0], l1_next[1])},
        {"q": "There are <b>12</b> boats in the harbour. <b>7</b> have red sails. <b>6</b> carry a lantern. <b>3</b> boats have <b>both</b>. How many boats have <b>neither</b> a red sail nor a lantern?",
         "fact": "A lighthouse lens is built from rings of glass that bend scattered light into one straight beam, visible over 30 km away.",
         "a": "%d boats." % l1_neither,
         "steps": "The 3 both-boats got counted twice, so boats with at least one = 7 + 6 &minus; 3 = 10. Then 12 &minus; 10 = <b>%d</b>. Drawing two overlapping circles makes this obvious." % l1_neither},
        {"q": "Four lighthouses stand on the coast: <b>Gull, Rock, Pine, and Sand</b>. Gull is taller than Rock. Sand is the shortest of all. Pine is taller than Gull. List them from <b>tallest to shortest</b>.",
         "fact": "The Pharos of Alexandria, built over 2,000 years ago, was one of the seven wonders of the ancient world.",
         "a": "Pine, Gull, Rock, Sand.",
         "steps": "Pine &gt; Gull and Gull &gt; Rock chain together into Pine &gt; Gull &gt; Rock. Sand is shortest, so it goes last."},
        {"q": "On a balance, <b>1 big lamp</b> exactly balances <b>3 small lamps</b>. And <b>1 small lamp</b> exactly balances <b>2 lenses</b>. How many <b>lenses</b> would balance <b>1 big lamp</b>?",
         "fact": "Keepers had to wind the clockwork that turned the lens by hand, sometimes every two hours, all night long.",
         "a": "%d lenses." % l1_lenses,
         "steps": "1 big = 3 small. Swap each small for 2 lenses: 3 &times; 2 = <b>%d</b> lenses." % l1_lenses},
    ],
    "kid2": [
        {"q": "Three keepers are on duty and one of them forgot to light the lamp.<br><b>Idris</b> says: \"It wasn't me.\" &nbsp; <b>Anas</b> says: \"It was Bilal.\" &nbsp; <b>Bilal</b> says: \"Anas is lying.\"<br><b>Exactly one</b> of the three is telling the truth. Who forgot?",
         "fact": "Before automation, a keeper's whole job was making sure the light never once went out between dusk and dawn.",
         "a": "Idris forgot.",
         "steps": "Test each. If <b>Idris</b> did it: his own claim is false, Anas is false, Bilal is true &mdash; exactly one truth. &check; If Anas did it: Idris true and Bilal true &mdash; two. &cross; If Bilal did it: Idris true and Anas true &mdash; two. &cross; Only Idris fits."},
        {"q": "<b>30</b> ships pass the lighthouse. <b>18</b> carry cargo, <b>14</b> carry passengers, and <b>5</b> carry both. How many ships carry <b>neither</b>?",
         "fact": "Lighthouses are painted in bold stripes or patterns so they can also be identified in daylight, when the lamp is useless.",
         "a": "%d ships." % (30 - (18 + 14 - 5)),
         "steps": "At least one = 18 + 14 &minus; 5 = 27. Then 30 &minus; 27 = <b>%d</b>. Subtracting the overlap once is the whole trick." % (30 - (18 + 14 - 5))},
        {"q": "On a balance: <b>2 lenses and 1 lamp</b> together weigh <b>11 kg</b>. <b>1 lens and 1 lamp</b> together weigh <b>7 kg</b>. How much does <b>one lens</b> weigh? How much does <b>one lamp</b> weigh?",
         "fact": "A large Fresnel lens can weigh several tonnes yet float so freely on a bath of mercury that one hand can turn it.",
         "a": "Lens %d kg, lamp %d kg." % (l1_lens, l1_lamp),
         "steps": "The first weighing has exactly one extra lens and is 11 &minus; 7 = 4 kg heavier, so a <b>lens = %d kg</b>. Put it back: %d + lamp = 7, so <b>lamp = %d kg</b>." % (l1_lens, l1_lens, l1_lamp)},
        {"q": "One lighthouse flashes every <b>4 seconds</b>, another every <b>6 seconds</b>. They flash together at exactly 12:00:00. How many seconds until they flash together again? How many times will they flash together in the <b>first minute</b>?",
         "fact": "Ships time a lighthouse's flashes with a stopwatch and look the rhythm up in a book to confirm exactly where they are.",
         "a": "Every %d seconds; %d times in the first minute." % (l1_together, l1_times),
         "steps": "Together on shared multiples of 4 and 6: 12, 24, 36, 48, 60. So every <b>%d seconds</b>, and within 60 seconds that is <b>%d</b> times (not counting the 12:00:00 start)." % (l1_together, l1_times)},
    ],
    "kid1_watch": "#2 is the one to watch. The usual answer is 12 &minus; 7 &minus; 6 = &minus;1, or 12 &minus; 13. If he gets a negative or a nonsense number, that is the signal to draw two overlapping circles rather than to explain again.",
    "kid2_watch": "#1 rewards testing all three cases rather than arguing about who seems honest. If he picks an answer without checking the other two, the answer is worth nothing even when it's right &mdash; ask him to prove the other two fail.",
}

# ---------------------------------------------------------------- Jul 30
l2_falcon, l2_chick = 9, 3
l2_pat = [2, 5, 4, 7, 6]           # +3, -1, +3, -1 -> 9, 8
l2_next = [9, 8]
l2_combo = 3 * 2 - 1
l2_speed = (240 // 8) * 30
l2_bells = 9 // 3 * 2 * 6          # 3 hoods = 2 gloves; 1 glove = 6 bells
l2_greet = 7 * 6 // 2

JUL30L = {
    "file": "worksheet-falconry-logic.html",
    "title_plain": "Falconry Logic",
    "title": "🦅 Falconry Logic",
    "sub": "Puzzles from the glove and the hood",
    "kid1": [
        {"q": "A falcon is <b>3 times</b> as old as her chick. Together their ages add to <b>12 years</b>. How old is each?",
         "fact": "Falconry is more than 3,000 years old, and UNESCO lists it as a living human heritage.",
         "a": "Falcon %d, chick %d." % (l2_falcon, l2_chick),
         "steps": "Think in parts: the chick is 1 part, the falcon 3 parts, so 4 parts = 12 and one part = 3. Chick <b>%d</b>, falcon 3 &times; 3 = <b>%d</b>." % (l2_chick, l2_falcon)},
        {"q": "A trainer's log reads: <b>2, 5, 4, 7, 6, ___, ___</b>. What comes next, and what is the rule? (Hint: there are <i>two</i> rules taking turns.)",
         "fact": "A falcon wears a hood because a bird that cannot see stays calm — it is a blindfold, not a punishment.",
         "a": "%d and %d. Add 3, then subtract 1, over and over." % (l2_next[0], l2_next[1]),
         "steps": "2 +3&rarr; 5 &minus;1&rarr; 4 +3&rarr; 7 &minus;1&rarr; 6. So next is +3 = <b>%d</b>, then &minus;1 = <b>%d</b>." % (l2_next[0], l2_next[1])},
        {"q": "Three falconers — <b>Hamza, Layla, and Bilal</b> — fly a kestrel, a saker, and a peregrine. The kestrel is the smallest bird and the peregrine is the fastest. Hamza's bird is <b>not</b> the smallest. Layla flies the <b>fastest</b> bird. Who flies which?",
         "fact": "A falcon's eyesight is about eight times sharper than ours — it can spot a pigeon from over a kilometre up.",
         "a": "Layla — peregrine · Hamza — saker · Bilal — kestrel.",
         "steps": "Layla has the fastest, so Layla = peregrine. Hamza is not the smallest, so Hamza &ne; kestrel, and the peregrine is gone &rarr; Hamza = saker. Bilal takes the kestrel."},
        {"q": "A falcon's kit needs <b>one hood</b> (red, green, or brown) and <b>one set of jesses</b> (leather or silk). Every pairing is allowed <b>except</b> brown hood with silk jesses. How many different kits can be made? List them.",
         "fact": "Jesses are the short leather straps on a falcon's legs — the falconer's grip when the bird is on the glove.",
         "a": "%d kits." % l2_combo,
         "steps": "3 hoods &times; 2 jesses = 6, then remove the one banned pairing: <b>%d</b>. They are red-leather, red-silk, green-leather, green-silk, brown-leather." % l2_combo},
    ],
    "kid2": [
        {"q": "Three falconers — <b>Yusuf, Tariq, and Amina</b> — each fly a different bird (peregrine, saker, kestrel) on a different day (Tue, Thu, Sat). Who flies what, and when?<br><b>1.</b> Amina does not hunt on Saturday. &nbsp;<b>2.</b> The peregrine hunts on Saturday. &nbsp;<b>3.</b> Yusuf hunts on Tuesday and does not fly the saker.",
         "fact": "A peregrine in a hunting dive passes 300 km/h, making it the fastest animal on Earth.",
         "a": "Yusuf — kestrel — Tuesday · Amina — saker — Thursday · Tariq — peregrine — Saturday.",
         "steps": "Clue 3 puts Yusuf on Tuesday, so he is not the peregrine (Saturday, clue 2), and not the saker &rarr; <b>Yusuf, kestrel</b>. Clue 1 keeps Amina off Saturday, so she is not the peregrine &rarr; <b>Tariq, peregrine, Saturday</b>. Amina takes the saker on Thursday."},
        {"q": "A falcon covers <b>240 metres in 8 seconds</b> at a steady speed. At that same speed, how far would she travel in <b>30 seconds</b>?",
         "fact": "Falcons have a small bony cone inside each nostril that slows the rushing air, so they can still breathe in a full dive.",
         "a": "%d metres." % l2_speed,
         "steps": "First the rate: 240 &divide; 8 = 30 metres every second. Then 30 &times; 30 = <b>%d m</b>. Find the one-second rate before scaling &mdash; that's the whole method." % l2_speed},
        {"q": "On a balance, <b>3 hoods</b> weigh the same as <b>2 gloves</b>. And <b>1 glove</b> weighs the same as <b>6 bells</b>. How many <b>bells</b> balance <b>9 hoods</b>?",
         "fact": "Bells on a falcon's legs let the falconer hear where the bird has landed when it drops out of sight.",
         "a": "%d bells." % l2_bells,
         "steps": "9 hoods is 3 lots of 3 hoods, so 9 hoods = 3 &times; 2 = 6 gloves. Each glove is 6 bells, so 6 &times; 6 = <b>%d</b>." % l2_bells},
        {"q": "<b>7 falconers</b> meet. Each one greets every other falconer exactly once. How many greetings happen altogether?",
         "fact": "A falcon is flown hungry but never starved — the falconer weighs the bird daily, because a well-fed falcon simply leaves.",
         "a": "%d greetings." % l2_greet,
         "steps": "Each of the 7 greets the other 6 = 42, but that counts every greeting from both sides, so 42 &divide; 2 = <b>%d</b>. Or add 6 + 5 + 4 + 3 + 2 + 1." % l2_greet},
    ],
    "kid1_watch": "#2's answer of \"9, 8\" often arrives as \"9, 12\" — he spots the +3 and misses that the rules alternate. Ask him to say the rule out loud before writing; \"add three take one\" said aloud usually fixes it on its own.",
    "kid2_watch": "#2 is the rate method that comes back on every multi-step rate problem in the word-problem sheets. If he jumps straight to 240 &times; 30 or 240 &divide; 30, the missing idea is \"find one second first\" — that's worth five minutes now, it pays off all week.",
}

# ---------------------------------------------------------------- Jul 31
l3_start = (12 * 2 - 8) + 5        # backwards: end 12, halved, found 8, spent 5
l3_pat_next = [17, 34]
l3_cross = 7
l3_cloth = ((9 * 2) + 6) * 2
l3_cycle = lcm(9, 12)
l3_year = 365 // l3_cycle
l3_weigh = 2

JUL31L = {
    "file": "worksheet-caravan-logic.html",
    "title_plain": "Caravan Logic",
    "title": "🐪 Caravan Logic",
    "sub": "Puzzles from the salt roads",
    "kid1": [
        {"q": "A trader finishes his journey with <b>12 coins</b>. At the last oasis he spent <b>half</b> of everything he had. Before that he found <b>8 coins</b>. Before that he spent <b>5 coins</b> on water. How many coins did he set out with? (Work backwards.)",
         "fact": "Across the Sahara, salt was once traded for gold by weight — salt kept food edible, and nothing else could.",
         "a": "%d coins." % l3_start,
         "steps": "Run it in reverse and flip each step. Ended with 12 after halving &rarr; he had 24. Undo finding 8 &rarr; 16. Undo spending 5 &rarr; <b>%d</b>. Check forwards: 21 &minus; 5 = 16, + 8 = 24, half spent = 12. &check;" % l3_start},
        {"q": "Camel loads are recorded as <b>3, 6, 5, 10, 9, 18, ___, ___</b>. What are the next two? (Hint: two rules, taking turns.)",
         "fact": "A thirsty camel can drink over 100 litres in about ten minutes — roughly a full bathtub.",
         "a": "%d and %d. Double, then subtract 1, over and over." % (l3_pat_next[0], l3_pat_next[1]),
         "steps": "3 &times;2&rarr; 6 &minus;1&rarr; 5 &times;2&rarr; 10 &minus;1&rarr; 9 &times;2&rarr; 18. Next is &minus;1 = <b>%d</b>, then &times;2 = <b>%d</b>." % (l3_pat_next[0], l3_pat_next[1])},
        {"q": "Four oases lie along one road: <b>Zahra, Rimal, Bahr, and Nakhl</b>. Rimal is first. Nakhl is last. Bahr lies <b>between</b> Zahra and Nakhl. What is the order along the road?",
         "fact": "Camel humps store fat, not water. The fat is fuel, and burning it also releases a little water.",
         "a": "Rimal, Zahra, Bahr, Nakhl.",
         "steps": "Rimal 1st and Nakhl 4th leaves places 2 and 3 for Zahra and Bahr. Bahr must sit between Zahra and Nakhl, so Zahra is 2nd and Bahr 3rd."},
        {"q": "A trader must cross a river with a <b>goat</b>, a <b>sack of grain</b>, and a <b>jackal</b>. The boat carries him and only <b>one</b> of them. Left alone together, the jackal eats the goat, and the goat eats the grain. How does he get all three across? Write the trips in order.",
         "fact": "Desert temperatures can swing more than 30 &deg;C between afternoon and night — caravans often travelled after dark.",
         "a": "%d crossings — and the goat comes back." % l3_cross,
         "steps": "Goat over &rarr; return empty &rarr; jackal over &rarr; <b>bring the goat back</b> &rarr; grain over &rarr; return empty &rarr; goat over. The move nobody thinks of is carrying something <i>back</i>."},
    ],
    "kid2": [
        {"q": "You reach a fork. One road leads to the oasis, the other into the dunes. Two guides stand there: one <b>always</b> tells the truth, the other <b>always</b> lies — but you don't know which is which. You may ask <b>one</b> guide <b>one</b> question. What do you ask, and what do you do with the answer?",
         "fact": "Desert guides navigated by star, dune shape and wind direction — a route could be memorised for hundreds of kilometres.",
         "a": "Ask either guide: \"If I asked the <i>other</i> guide which road leads to the oasis, what would he say?\" Then take the <b>other</b> road.",
         "steps": "Both possible guides give the same reply. Ask the truthful one and he honestly reports the liar's lie. Ask the liar and he lies about the truthful one's honest answer. Either way the road named is <b>wrong</b>, so you go the other way. One question does the work of two because it forces the answer through both guides."},
        {"q": "A merchant sells <b>half</b> his cloth, then sells <b>6 more bolts</b>, then sells <b>half of what is left</b>, and finishes with <b>9 bolts</b>. How many bolts did he start with?",
         "fact": "Caravans could run to several thousand camels, moving in a column many kilometres long.",
         "a": "%d bolts." % l3_cloth,
         "steps": "Backwards, flipping each step: 9 is what's left after halving &rarr; 18. Undo selling 6 &rarr; 24. Undo the first halving &rarr; <b>%d</b>. Check: 48 &rarr; 24 &rarr; 18 &rarr; 9. &check;" % l3_cloth},
        {"q": "One caravan leaves every <b>9 days</b>, another every <b>12 days</b>. Both leave today. In how many days do they next leave together? How many times will that happen in a <b>365-day</b> year?",
         "fact": "Timbuktu grew rich as the place where the desert caravan routes met the river trade going south.",
         "a": "Every %d days; %d times in a year." % (l3_cycle, l3_year),
         "steps": "Shared multiples of 9 and 12: 36, 72, 108... so every <b>%d days</b>. Then 365 &divide; 36 = 10 remainder 5 &rarr; <b>%d</b> times (not counting today)." % (l3_cycle, l3_year)},
        {"q": "You have <b>9 sacks</b> that look identical. <b>One</b> is heavier than the rest, which all weigh the same. Using a <b>balance scale</b> (no weights), what is the <b>fewest weighings</b> that always finds the heavy sack? Explain how.",
         "fact": "Merchants carried their own scales and standard weights, because a trusted weight was the only guard against a rigged one.",
         "a": "%d weighings." % l3_weigh,
         "steps": "Split into three groups of 3. <b>Weigh 1:</b> group A against group B. If one side sinks the heavy sack is there; if they balance it is in group C. Either way you now have 3 sacks. <b>Weigh 2:</b> one against another &mdash; if one sinks that's it, if they balance it's the third. Two weighings, always. Weighing them one at a time takes up to 8."},
    ],
    "kid1_watch": "#4 is the classic river crossing and the block is always the same: he will not consider bringing something <i>back</i>. Don't hand him that move — ask \"is he allowed to carry something back across?\" and wait. The moment he realises it's legal, he solves it himself.",
    "kid2_watch": "#1 has no arithmetic in it at all and is the hardest thing on the sheet. A good attempt that doesn't land is fine here. If he's stuck, ask him what happens if he asks the liar about the honest guide, and let him run just that one case.",
}

# ---------------------------------------------------------------- Aug 1
l4_real = "3:55"
l4_rings = sum(range(1, 7))
l4_chimes = len(range(0, 121, 15))
l4_glass = 9
l4_angle = abs((4 * 30 + 20 * 0.5) - (20 * 6))
l4_bells = lcm(lcm(6, 8), 12)
l4_arrive = "1:30"

AUG1L = {
    "file": "worksheet-clocks-logic.html",
    "title_plain": "Clockwork Logic",
    "title": "🕰️ Clockwork Logic",
    "sub": "Puzzles about keeping time",
    "kid1": [
        {"q": "A kitchen clock runs <b>15 minutes slow</b>. It shows <b>3:40</b>. What is the real time?",
         "fact": "Before railways, every town kept its own local time by the sun — noon in one town was not noon in the next.",
         "a": "%s." % l4_real,
         "steps": "Slow means it hasn't caught up yet, so the real time is <b>later</b>: 3:40 + 15 minutes = <b>%s</b>. Ask which way before adding &mdash; that's the whole question." % l4_real},
        {"q": "A tower bell strikes the hour: once at 1 o'clock, twice at 2 o'clock, and so on. How many strikes altogether from <b>1 o'clock through 6 o'clock</b>?",
         "fact": "We split hours into 60 minutes because the Babylonians counted in sixties, more than 4,000 years ago.",
         "a": "%d strikes." % l4_rings,
         "steps": "1 + 2 + 3 + 4 + 5 + 6 = <b>%d</b>. Pair the ends to go faster: (1+6) + (2+5) + (3+4) = 7 + 7 + 7." % l4_rings},
        {"q": "A clock chimes <b>every 15 minutes</b>. How many chimes are there from <b>2:00 to 4:00</b>, counting the chimes at 2:00 and at 4:00 themselves?",
         "fact": "A sundial only works in sunshine, which is why water clocks were invented — they kept counting at night and indoors.",
         "a": "%d chimes." % l4_chimes,
         "steps": "2:00 to 4:00 is 120 minutes, and 120 &divide; 15 = 8 gaps. Counting both ends means <b>%d</b> chimes, not 8 &mdash; fenceposts, not fences." % l4_chimes},
        {"q": "Three friends arrive at the clock tower. <b>Idris</b> arrives before <b>Salma</b>. <b>Yahya</b> arrives after <b>Salma</b>. Who arrived <b>first</b>, and who arrived <b>last</b>?",
         "fact": "The pendulum clock, invented in 1656, was such a leap that it cut a typical clock's daily error from minutes to seconds.",
         "a": "Idris first, Yahya last.",
         "steps": "Idris before Salma, and Salma before Yahya, chains into Idris &rarr; Salma &rarr; Yahya. So <b>Idris</b> first and <b>Yahya</b> last."},
    ],
    "kid2": [
        {"q": "You have a <b>4-minute</b> hourglass and a <b>7-minute</b> hourglass, and nothing else. How do you measure <b>exactly 9 minutes</b>? Write the steps with the times.",
         "fact": "Working out longitude at sea needed a clock that stayed accurate on a rolling ship — the problem stood for decades.",
         "a": "Yes — %d minutes, using four flips." % l4_glass,
         "steps": "Start <b>both</b> at 0. At <b>4 min</b> the small one empties &mdash; flip it. At <b>7 min</b> the big one empties &mdash; flip it. At <b>8 min</b> the small one empties again; the big one has now been running 1 minute, so it holds exactly 1 minute of sand in the bottom. <b>Flip the big one</b> and it runs out at <b>9 minutes</b>. The idea: a part-used glass measures the time it has already run."},
        {"q": "Three bells ring together at noon. One rings every <b>6 minutes</b>, one every <b>8 minutes</b>, one every <b>12 minutes</b>. How many minutes until all three ring together again?",
         "fact": "An atomic clock is so steady it would drift less than a second over millions of years.",
         "a": "%d minutes." % l4_bells,
         "steps": "Find the first number 6, 8 and 12 all divide into. Multiples of 8: 8, 16, <b>24</b>. 24 is divisible by 6 and 12 too, so <b>%d minutes</b>." % l4_bells},
        {"q": "A train arrives at <b>3:45</b>. The journey took <b>1 hour 50 minutes</b>, and before boarding he waited <b>25 minutes</b> at the station. What time did he reach the station?",
         "fact": "Railways forced countries onto standard time — trains cannot run to a timetable if every town keeps its own clock.",
         "a": "%s." % l4_arrive,
         "steps": "Work backwards from the arrival. 3:45 &minus; 1 h 50 min = 1:55 departure. Then 1:55 &minus; 25 min = <b>%s</b>. Undo the journey first, then the wait." % l4_arrive},
        {"q": "At <b>4:20</b>, what is the angle between the hour hand and the minute hand? (Careful: by 4:20 the hour hand has already crept past the 4.)",
         "fact": "A clock face is 360 degrees over 12 hours, so the hour hand moves just half a degree every minute.",
         "a": "%d degrees." % int(l4_angle),
         "steps": "Minute hand: 20 min &times; 6&deg; = 120&deg;. Hour hand: 4 &times; 30&deg; = 120&deg;, plus 20 min &times; 0.5&deg; = 10&deg;, so 130&deg;. Difference = <b>%d&deg;</b>. Answering 20&deg; means forgetting the hour hand drifts." % int(l4_angle)},
    ],
    "kid1_watch": "#3 is the fencepost trap: 120 &divide; 15 = 8 <i>gaps</i> but <b>9</b> chimes. Expect 8. It's the same idea as the leftover-needs-a-box remainder work he's been doing all week — worth naming that out loud, because he'll see they're the same shape.",
    "kid2_watch": "#1 is genuinely hard and #4 catches almost everyone at 20&deg;. Neither is a fluency problem, so don't let a miss here read as a bad day &mdash; note them as puzzles attempted, not skills failed. If he lands the hourglass unaided, that's the strongest reasoning result of the week.",
}

# ---------------------------------------------------------------- Aug 2 (cumulative)
l5_start = (7 * 2) - 4
l5_neither = 20 - (12 + 9 - 4)
l5_tri = [21, 28]
l5_bells = 4 // 2 * 5 * 3
l5_cycle = lcm(15, 20)
l5_weigh = 2

AUG2L = {
    "file": "worksheet-kites-logic-cumulative.html",
    "title_plain": "Kites & Flight — Cumulative Logic",
    "title": "🪁 Kites & Flight",
    "sub": "CUMULATIVE — every puzzle type from this week, shuffled, with nothing telling you which is which",
    "kid1": [
        {"q": "A kite maker ends the day with <b>7 kites</b>. In the afternoon he sold <b>half</b> of everything he had. That morning he built <b>4 new ones</b>. How many did he start the day with?",
         "fact": "Kites were invented in China more than 2,000 years ago, long before anyone thought of flying in one.",
         "a": "%d kites." % l5_start,
         "steps": "Backwards, flipping each step: 7 left after halving &rarr; 14. Undo building 4 &rarr; <b>%d</b>. Check forwards: 10 + 4 = 14, sell half = 7. &check;" % l5_start},
        {"q": "<b>20 kites</b> are flying. <b>12</b> have tails, <b>9</b> have bells, and <b>4</b> have <b>both</b>. How many have <b>neither</b>?",
         "fact": "Before aeroplanes, weather scientists sent thermometers up on kites to find out what the air was doing higher up.",
         "a": "%d kites." % l5_neither,
         "steps": "At least one = 12 + 9 &minus; 4 = 17. Then 20 &minus; 17 = <b>%d</b>." % l5_neither},
        {"q": "A kite competition scores in a pattern: <b>1, 3, 6, 10, 15, ___, ___</b>. What are the next two, and what is the rule?",
         "fact": "The Wright brothers flew their first designs as kites on strings before they ever risked sitting in one.",
         "a": "%d and %d. The gaps go up by one each time." % (l5_tri[0], l5_tri[1]),
         "steps": "Gaps are 2, 3, 4, 5 &mdash; so next gaps are 6 and 7. 15 + 6 = <b>%d</b>, then %d + 7 = <b>%d</b>." % (l5_tri[0], l5_tri[0], l5_tri[1])},
        {"q": "On a balance, <b>2 large kites</b> weigh the same as <b>5 small kites</b>. And <b>1 small kite</b> weighs the same as <b>3 bells</b>. How many <b>bells</b> balance <b>4 large kites</b>?",
         "fact": "Alexander Graham Bell built kites out of hundreds of linked triangles, big enough to lift a person off the ground.",
         "a": "%d bells." % l5_bells,
         "steps": "4 large is double 2 large, so 4 large = 10 small. Each small is 3 bells, so 10 &times; 3 = <b>%d</b>." % l5_bells},
    ],
    "kid2": [
        {"q": "Three fliers — <b>Yusuf, Musa, and Hamza</b> — each fly a different colour kite (red, green, blue) at a different place (hill, beach, park). Who flies which, and where?<br><b>1.</b> Musa does not fly the red kite. &nbsp;<b>2.</b> The blue kite flies at the beach. &nbsp;<b>3.</b> Hamza flies at the hill and not the green kite. &nbsp;<b>4.</b> Yusuf does not fly at the beach.",
         "fact": "A kite climbs because the wind striking its tilted face is pushed downward, and the air pushes back just as hard.",
         "a": "Hamza — red — hill · Musa — blue — beach · Yusuf — green — park.",
         "steps": "Clue 3 puts Hamza on the hill, so not blue (beach, clue 2), and not green &rarr; <b>Hamza, red</b>. Clue 1 rules Musa off red anyway. Clue 4 keeps Yusuf off the beach, so Yusuf isn't blue &rarr; <b>Musa, blue, beach</b> and <b>Yusuf, green</b>, leaving Yusuf the park."},
        {"q": "Two kite festivals run on cycles: one every <b>15 days</b>, the other every <b>20 days</b>. Both are held today. In how many days will they fall on the same day again?",
         "fact": "Kite fighting, where flyers try to cut each other's lines in mid-air, is a serious sport in several countries.",
         "a": "%d days." % l5_cycle,
         "steps": "The first number both 15 and 20 divide into: multiples of 20 are 20, 40, <b>60</b>, and 60 &divide; 15 = 4. So <b>%d days</b>." % l5_cycle},
        {"q": "Someone snapped the big kite's line. <b>Anas</b> says: \"Bilal did it.\" &nbsp;<b>Bilal</b> says: \"I didn't do it.\" &nbsp;<b>Idris</b> says: \"Anas did it.\"<br><b>Exactly one</b> of the three is <b>lying</b>. Who broke the line?",
         "fact": "Benjamin Franklin is said to have flown a kite in a thunderstorm in 1752 to show that lightning is electricity.",
         "a": "Anas broke it.",
         "steps": "Careful &mdash; this time exactly one <b>lies</b>, so two are telling the truth. If <b>Anas</b> did it: Anas lies, Bilal is honest, Idris is honest &mdash; exactly one lie. &check; If Bilal did it: Bilal and Idris both lie &mdash; two. &cross; If Idris did it: Anas and Idris both lie &mdash; two. &cross;"},
        {"q": "You have <b>8 kites</b> that look identical, but <b>one</b> is heavier. Using a <b>balance scale</b>, what is the <b>fewest weighings</b> that is guaranteed to find it?",
         "fact": "In the 1800s, kites carried the first lines across deep gorges — the line pulled a rope, the rope pulled a cable, and the cable carried a bridge.",
         "a": "%d weighings." % l5_weigh,
         "steps": "Split 3 / 3 / 2. <b>Weigh 1:</b> the two 3s. If one side sinks you have 3 left; if they balance you have the 2 left. <b>Weigh 2:</b> from 3, weigh one against another (sinks = that one, balances = the third); from 2, just weigh them. <b>%d</b> either way." % l5_weigh},
    ],
    "kid1_watch": "Cumulative sheet — the point is that nothing says which puzzle is which. #1 is working backwards, #2 is the overlap circles, #3 is a growing-gap pattern, #4 is swapping one thing for another. Watch whether he <i>recognises</i> the type unprompted; that recognition is the whole difference between Solid and Locked.",
    "kid2_watch": "#3 flips the rule from Tuesday's puzzle: exactly one <b>lies</b>, not exactly one tells the truth. If he answers Bilal, he pattern-matched Tuesday instead of reading the line — which is exactly what a cumulative sheet is built to catch. Worth more as a lesson than as a mark.",
}

# ---------------------------------------------------------------- Aug 16 (Block 2 restart)
# Four reasoning types per kid, none of them the type that sat in the same slot on the
# last sheet either kid saw (Aug 1 / Aug 2). kid1 #3 is the classic rate trap — it needs
# no arithmetic at all, which is deliberate on a first sheet back after two weeks off.
l6_start = (11 * 2) - 9 + 6        # backwards: end 11, halved, found 9, gave away 6
l6_neither = 24 - (13 + 11 - 6)
l6_minutes = 3                     # 3 monkeys / 3 mangoes / 3 minutes -> 9 and 9 is still 3
l6_calls = 5 * 4 // 2
l6_cycle = lcm(8, 14)
l6_in5min = 300 // l6_cycle
l6_weigh = 3                       # 3**2 = 9 < 12 <= 27 = 3**3

AUG16L = {
    "file": "worksheet-rainforest-logic.html",
    "title_plain": "Rainforest Logic",
    "title": "🌴 Rainforest Logic",
    "sub": "Puzzles from under the canopy — no calculator, and for one of these you need no arithmetic at all",
    "kid1": [
        {"q": "Nusayba picks a basket of figs. She gives <b>6</b> of them to her brother. Then she finds <b>9</b> more on the path. She shares what she is carrying equally with a friend, keeping <b>half</b>, and ends up with <b>11</b> figs. How many did she pick to start with?",
         "fact": "Fig trees feed more rainforest animals than almost any other tree, because somewhere in the forest a fig is always ripe.",
         "a": "%d figs." % l6_start,
         "steps": "Work backwards, flipping each step. 11 left after halving &rarr; 22 before it. Undo finding 9 &rarr; 13. Undo giving 6 away &rarr; <b>%d</b>. Check forwards: %d &minus; 6 = 13, + 9 = 22, half of 22 = 11. &check;" % (l6_start, l6_start)},
        {"q": "There are <b>24 birds</b> in a clearing. <b>13</b> of them are green. <b>11</b> of them can copy other sounds. <b>6</b> birds can do <b>both</b>. How many birds are <b>neither</b> green nor able to copy sounds?",
         "fact": "A toucan's huge beak is mostly hollow, full of air pockets, and it lets the bird dump heat like a radiator.",
         "a": "%d birds." % l6_neither,
         "steps": "The 6 both-birds got counted twice, so birds with at least one = 13 + 11 &minus; 6 = 18. Then 24 &minus; 18 = <b>%d</b>. Draw two overlapping circles and it goes obvious." % l6_neither},
        {"q": "<b>3 monkeys</b> eat <b>3 mangoes</b> in <b>3 minutes</b>. How long would <b>9 monkeys</b> take to eat <b>9 mangoes</b>? <i>Think before you write. This one is not the calculation it looks like.</i>",
         "fact": "Howler monkeys are the loudest land animal in the Americas — a troop can be heard about 5 km through thick forest.",
         "a": "%d minutes — the same as before." % l6_minutes,
         "steps": "Read it as one monkey and one mango: if 3 monkeys finish 3 mangoes in 3 minutes, then <b>each monkey eats one mango in 3 minutes</b>. Nine monkeys with a mango each still take <b>%d minutes</b> — they are all eating at once. The trap is multiplying by three." % l6_minutes},
        {"q": "<b>5 parrots</b> sit in a tree. Each parrot calls to <b>every other parrot</b> exactly once. How many calls happen altogether?",
         "fact": "Wild parrots appear to use a signature call for each bird, rather like a name, and they learn it as chicks.",
         "a": "%d calls." % l6_calls,
         "steps": "Each of the 5 calls to the other 4, which is 20 &mdash; but that counts every call from both ends, so 20 &divide; 2 = <b>%d</b>. Or add 4 + 3 + 2 + 1." % l6_calls},
    ],
    "kid2": [
        {"q": "Three researchers — <b>Ibrahim, Khadija, and Sumayya</b> — each study a different animal (toucan, jaguar, sloth) from a different camp (Canopy, Ridge, River). Who studies what, and from where?<br><b>1.</b> The researcher at the <b>Canopy</b> camp studies the toucan. &nbsp;<b>2.</b> Ibrahim is not at the River camp, and does not study the sloth. &nbsp;<b>3.</b> Khadija studies the jaguar. &nbsp;<b>4.</b> Sumayya is not at the Ridge camp.",
         "fact": "Sloths climb down to the forest floor only about once a week, and it is the most dangerous trip they make.",
         "a": "Ibrahim — toucan — Canopy · Khadija — jaguar — Ridge · Sumayya — sloth — River.",
         "steps": "Clue 3 gives <b>Khadija the jaguar</b>. Clue 2 then leaves Ibrahim only the toucan, and clue 1 puts the toucan at the Canopy &rarr; <b>Ibrahim, Canopy</b>. Sumayya takes the sloth, and clue 4 keeps her off the Ridge &rarr; <b>Sumayya, River</b>, so Khadija has the Ridge."},
        {"q": "Two frogs call on a steady beat. One calls every <b>8 seconds</b>, the other every <b>14 seconds</b>. They call together at exactly 6:00:00. How many seconds until they call together again? How many times will they call together in the <b>first 5 minutes</b>?",
         "fact": "Poison dart frogs build their poison from what they eat, so the same frog raised in a zoo is completely harmless.",
         "a": "Every %d seconds; %d times in the first 5 minutes." % (l6_cycle, l6_in5min),
         "steps": "Together on the shared multiples of 8 and 14. Multiples of 14 are 14, 28, 42, <b>56</b> &mdash; and 56 &divide; 8 = 7, so <b>%d seconds</b>. Five minutes is 300 seconds, and 56, 112, 168, 224, 280 all fit: <b>%d</b> times (not counting the 6:00:00 start)." % (l6_cycle, l6_in5min)},
        {"q": "Someone let the last canoe drift away.<br><b>Umar</b> says: \"It wasn't me.\" &nbsp;<b>Harun</b> says: \"It was Umar.\" &nbsp;<b>Zaynab</b> says: \"It wasn't Harun.\"<br><b>Exactly one</b> of the three is telling the <b>truth</b>. Who let it drift?",
         "fact": "Rain can take about ten minutes to reach the rainforest floor — the canopy catches it and lets it down leaf by leaf.",
         "a": "Harun let it drift.",
         "steps": "Test all three. If <b>Umar</b> did it: Umar false, Harun true, Zaynab true &mdash; two truths. &cross; If <b>Harun</b> did it: Umar true, Harun false, Zaynab false &mdash; exactly one. &check; If <b>Zaynab</b> did it: Umar true, Harun false, Zaynab true &mdash; two. &cross; Only Harun fits."},
        {"q": "You have <b>12 seed pods</b> that look identical, but <b>one</b> is heavier than the rest. Using a <b>balance scale</b> and no weights, what is the <b>fewest weighings</b> that is guaranteed to find it? Explain your plan.",
         "fact": "A single hectare of Amazon rainforest can hold more than 300 different tree species — more than some whole countries.",
         "a": "%d weighings." % l6_weigh,
         "steps": "Split 4 / 4 / 4. <b>Weigh 1:</b> two of the fours. A sinking side names that four; a balance names the four left out. <b>Weigh 2:</b> split that four 2 / 2 and weigh them. <b>Weigh 3:</b> weigh the last two against each other. <b>%d</b> every time. Two is not enough: each weighing has only 3 outcomes, and 3 &times; 3 = 9 is fewer than 12." % l6_weigh},
    ],
    "kid1_watch": "#3 is the one to sit with. Almost every child answers 9 minutes, and that is the <i>useful</i> mistake &mdash; it means he multiplied instead of reading. Don't tell him; ask \"how many mangoes does one monkey eat?\" and wait. #1 is the first working-backwards puzzle in over two weeks, so if he stalls, ask him to start from the 11 and undo one step at a time.",
    "kid2_watch": "#1 has FOUR clues, not three, and clue 4 is the one that does the last bit of work &mdash; if he stops at three clues he will place the animals correctly and guess the camps. Ask him which clue proved Sumayya's camp. #4 is a step up from the 8-kite version: the answer moves from 2 to 3, and the reason is that 3 &times; 3 = 9 no longer covers 12. If he says 2, that is the sentence to draw out of him.",
}

# ---------------------------------------------------------------- Aug 17
# Theme set by Asif 2026-08-17: immune system, all week. Deliberately NOT a
# repeat of the Aug 16 shapes — the monkeys/mangoes rate trap is replaced by a
# climb-and-slip (different trap, same "don't just multiply" lesson), and kid2's
# weighing puzzle by an off-by-one cut puzzle. Only the logic grid is a staple
# and stays, because it is the one that rewards a written table.
def _first_day(rise, fall, target):
    """Climb-and-slip, simulated. The closed form is a classic off-by-one."""
    pos, day = 0, 0
    while True:
        day += 1
        pos += rise
        if pos >= target:
            return day
        pos -= fall


l7_start = (14 * 2) - 12 + 7        # backwards: end 14, halved, 12 arrived, 7 removed
l7_neither = 30 - (17 + 14 - 8)
l7_day = _first_day(3, 2, 10)
l7_pick = 3 + 1                     # pigeonhole: 3 kinds, so the 4th must repeat
l7_cuts = 42 // 6 - 1
l7_time = l7_cuts * 3

AUG17L = {
    "file": "worksheet-immune-logic.html",
    "title_plain": "Immune System Logic",
    "title": "🦠 Immune System Logic",
    "sub": "Puzzles from the lab — two of these are traps, and the trap is the lesson",
    "kid1": [
        {"q": "A lab counts a batch of white blood cell samples. <b>7</b> are removed as spoiled. Then <b>12</b> more arrive from the clinic. The batch is then split <b>equally</b> between two microscopes, and one microscope receives <b>14</b> samples. How many samples were in the batch to start with?",
         "fact": "A white blood cell can squeeze itself out through the wall of a blood vessel to reach a wound — it changes shape to get there.",
         "a": "%d samples." % l7_start,
         "steps": "Work backwards, flipping every step. One microscope got 14 after an equal split &rarr; 28 before it. Undo the 12 arriving &rarr; 16. Undo the 7 removed &rarr; <b>%d</b>. Check forwards: %d &minus; 7 = 16, + 12 = 28, half of 28 = 14. &check;" % (l7_start, l7_start)},
        {"q": "A tray holds <b>30 samples</b>. <b>17</b> of them show antibodies. <b>14</b> of them show a fever marker. <b>8</b> samples show <b>both</b>. How many samples show <b>neither</b>?",
         "fact": "Your skin is your largest immune organ. Most germs never get past it at all.",
         "a": "%d samples." % l7_neither,
         "steps": "The 8 both-samples got counted twice, so samples with at least one = 17 + 14 &minus; 8 = 22. Then 30 &minus; 22 = <b>%d</b>. Draw two overlapping circles and it goes obvious." % l7_neither},
        {"q": "A patient's antibody level <b>rises 3 units</b> during each day, then <b>falls back 2 units</b> each night. It starts at <b>0</b> and needs to reach <b>10</b>. On which <b>day</b> does it first reach 10? <i>Think it through. This one is not the calculation it looks like.</i>",
         "fact": "After an infection, some antibody-making cells become memory cells and simply wait — sometimes for the rest of your life.",
         "a": "Day %d." % l7_day,
         "steps": "It gains 1 unit a day overall, so 10 days looks right &mdash; and it is wrong. Track it: end of day 1 it is at 3, then 1 overnight. Day 2 &rarr; 4, then 2. By the end of <b>day 7</b> it is at 9, dropping to 7. On <b>day %d</b> it climbs 7 &rarr; 10 and it has <i>arrived</i> &mdash; the night-time fall never happens. The last climb is the one that escapes." % l7_day},
        {"q": "A tray holds vials of <b>3 different vaccines</b>, all mixed together and all looking identical. Without looking, what is the <b>fewest</b> vials you must pick to be <b>certain</b> you have two of the same kind?",
         "fact": "Vaccines are usually kept cold because the harmless germ pieces inside them fall apart when they get warm.",
         "a": "%d vials." % l7_pick,
         "steps": "Think about the unluckiest possible run. You could pick 3 and get one of every kind &mdash; still no pair. But there are only 3 kinds, so the <b>%dth</b> vial has to match one you already hold. <b>%d</b>. The answer is not 2, because \"certain\" means even on your worst day." % (l7_pick, l7_pick)},
    ],
    "kid2": [
        {"q": "Three researchers — <b>Idris, Hafsa, and Zakariya</b> — each study a different cell (T-cell, B-cell, macrophage) in a different lab (North, South, Central). Who studies what, and where?<br><b>1.</b> The researcher in the <b>Central</b> lab studies the macrophage. &nbsp;<b>2.</b> Idris does not study the B-cell. &nbsp;<b>3.</b> Hafsa studies the T-cell. &nbsp;<b>4.</b> Zakariya is not in the North lab.",
         "fact": "A macrophage's name means \"big eater\" — it swallows germs whole and digests them.",
         "a": "Idris — macrophage — Central · Hafsa — T-cell — North · Zakariya — B-cell — South.",
         "steps": "Clue 3 gives <b>Hafsa the T-cell</b>. Clue 2 then leaves Idris only the macrophage, and clue 1 puts the macrophage in <b>Central</b>. Zakariya takes the B-cell. Clue 4 keeps him out of the North &rarr; <b>Zakariya, South</b>, so Hafsa has the North."},
        {"q": "You need to measure exactly <b>4 mL</b> of a solution. You have only a <b>5 mL</b> syringe, a <b>3 mL</b> syringe, and a large bottle of the solution. Neither syringe has any markings on it. How do you do it?",
         "fact": "Doses for children are worked out by body weight, not age — which is why the same medicine comes in different amounts.",
         "a": "Fill 5, pour off 3, keep the 2, then top the 5 up and pour 1 more into the 3.",
         "steps": "<b>1.</b> Fill the 5 mL. <b>2.</b> Pour from it into the 3 mL until the 3 is full &mdash; that leaves exactly <b>2 mL</b> in the 5. <b>3.</b> Empty the 3 mL. <b>4.</b> Tip the 2 mL into the 3 mL syringe. <b>5.</b> Refill the 5 mL. <b>6.</b> Pour from the 5 into the 3 &mdash; it only has room for <b>1 more mL</b>, so exactly <b>4 mL</b> is left behind in the 5. That is your 4."},
        {"q": "A sample was contaminated.<br><b>Anas</b> says: \"It was Bilal.\" &nbsp;<b>Bilal</b> says: \"It wasn't me.\" &nbsp;<b>Ruqayya</b> says: \"It was Anas.\"<br><b>Exactly one</b> of the three is <b>lying</b>. Who contaminated the sample?",
         "fact": "Labs work in sterile cabinets with the air always flowing outward, so nothing from the room can drift onto a sample.",
         "a": "Anas contaminated it.",
         "steps": "Test each one and count the lies. If <b>Anas</b> did it: Anas lies, Bilal tells the truth, Ruqayya tells the truth &mdash; exactly one lie. &check; If <b>Bilal</b> did it: Anas true, Bilal lies, Ruqayya lies &mdash; two. &cross; If <b>Ruqayya</b> did it: Anas lies, Bilal true, Ruqayya lies &mdash; two. &cross; Only Anas fits. Note it is <i>one lie</i> here, not one truth &mdash; read that line twice."},
        {"q": "A <b>42 cm</b> length of tubing must be cut into <b>6 cm</b> pieces. Each cut takes <b>3 minutes</b>. How long does the whole job take?",
         "fact": "Blood for a transfusion is passed through a filter fine enough to catch tiny clots but not the blood cells themselves.",
         "a": "%d minutes." % l7_time,
         "steps": "42 &divide; 6 = <b>7 pieces</b> &mdash; but that is not the number of cuts. Lay it out: the last piece falls free on the cut before it, so 7 pieces need only <b>%d cuts</b>. Then %d &times; 3 = <b>%d minutes</b>. Answering 21 means counting a cut that never happens." % (l7_cuts, l7_cuts, l7_time)},
    ],
    "kid1_watch": "#3 is the one to sit with. Almost every child answers 10 days, and that is the <i>useful</i> mistake &mdash; it means he found the net gain of 1 a day and stopped. Don't tell him; ask \"what is it at the end of day 7, and what happens next morning?\" and wait. #4 is a new shape for him &mdash; the word doing the work is <b>certain</b>. If he says 2, ask him to describe the unluckiest possible run of picks.",
    "kid2_watch": "#1 has FOUR clues and clue 4 is the one that finishes it &mdash; without it Hafsa and Zakariya could swap labs, so if he stops at three clues he will get the cells right and guess the labs. Ask him which clue proved Zakariya's lab. #3 flips last time's puzzle: exactly one is <b>lying</b>, where the rainforest version had exactly one telling the truth. If he answers Harun-style out of habit he has pattern-matched instead of reading. #4 is an off-by-one; 21 is the expected wrong answer and it is worth drawing the 7 pieces to settle it.",
}

# ---------------------------------------------------------------- Aug 18
# Immune-system theme continues (Asif, 2026-08-17). Every shape here is new
# against Aug 16 and Aug 17: no working-backwards for kid1 (he had one
# yesterday), and NO liar puzzle for either kid — that has now run two days
# running and a third would be pattern-matching practice, not reasoning. The
# logic grid stays, because it is the one puzzle that rewards a written table.
l8_shakes = (6 * 5) // 2                # each pair once, not 6 x 5
l8_vial = 32 // 4                       # flask = 3 vials, so flask + vial = 4 vials
l8_flask = 3 * l8_vial
l8_finish = (9 * 60 + 45) + 50 + 25 + 40
l8_half = 12 - 1                        # doubling: full on 12 -> half on 11
l8_quarter = 12 - 2
m8_scan = 3 * 5                         # 6 side-scans, 2 at a time, 5 min a round
m8_pick = 4 * 2 + 1                     # 4 kinds, want 3 alike: worst case 2 each
m8_start = ((7 * 2) + 3) * 2            # replayed forwards in the key

AUG18L = {
    "file": "worksheet-lab-bench-logic.html",
    "title_plain": "Lab Bench Logic",
    "title": "🧫 Lab Bench Logic",
    "sub": "Puzzles from the bench — none of these are the sum they look like",
    "kid1": [
        {"q": "<b>6 researchers</b> meet at the bench. Every researcher shakes hands with every other researcher <b>exactly once</b>. How many handshakes happen altogether?",
         "fact": "Your body's defences learn. The second time a germ shows up, the answer to it is faster and stronger than the first.",
         "a": "%d handshakes." % l8_shakes,
         "steps": "Each of the 6 shakes 5 hands = 30 &mdash; but that counts <i>every handshake twice</i>, once from each side. So 30 &divide; 2 = <b>%d</b>. Or count down the line: 5 + 4 + 3 + 2 + 1 = <b>%d</b>." % (l8_shakes, l8_shakes)},
        {"q": "On a balance, <b>3 vials</b> exactly balance <b>1 flask</b>. A flask and a vial together weigh <b>32 grams</b>. How much does <b>one vial</b> weigh? How much does the flask weigh?",
         "fact": "A neutrophil, the commonest white blood cell, lives less than a day once it leaves the blood.",
         "a": "A vial is %d g; the flask is %d g." % (l8_vial, l8_flask),
         "steps": "Swap the flask for what it balances: a flask <i>is</i> 3 vials, so \"flask + vial\" is <b>4 vials</b> = 32 g. One vial = 32 &divide; 4 = <b>%d g</b>; flask = 3 &times; %d = <b>%d g</b>. Check: %d + %d = 32. &check;" % (l8_vial, l8_vial, l8_flask, l8_flask, l8_vial)},
        {"q": "A test starts at <b>9:45 am</b>. It runs for <b>50 minutes</b>, then cools down for <b>25 minutes</b>, then is scanned for <b>40 minutes</b>. At what time is it finished?",
         "fact": "Much of your immune repair happens while you sleep, which is one reason being ill makes you so tired.",
         "a": "%d:%02d am." % (l8_finish // 60, l8_finish % 60),
         "steps": "One stage at a time: 9:45 + 50 &rarr; <b>10:35</b>; + 25 &rarr; <b>11:00</b>; + 40 &rarr; <b>%d:%02d am</b>. Adding 115 minutes first also works &mdash; if you know that is 1 h <b>55</b>, not 1 h 15." % (l8_finish // 60, l8_finish % 60)},
        {"q": "A dish of bacteria <b>doubles every day</b>. On <b>day 12</b> the dish is completely full. On which day was it <b>half</b> full? And on which day was it a <b>quarter</b> full? <i>Careful — this one is not half of 12.</i>",
         "fact": "In good conditions some bacteria can double in number about every twenty minutes.",
         "a": "Half full on day %d; a quarter full on day %d." % (l8_half, l8_quarter),
         "steps": "Run it backwards: doubling forwards is <i>halving</i> backwards. The day before full it was half full &mdash; <b>day %d</b> &mdash; and one more back, <b>day %d</b>. Day 6 is the expected wrong answer; the last day adds as much as every day before it put together." % (l8_half, l8_quarter)},
    ],
    "kid2": [
        {"q": "Three lab technicians — <b>Yusra, Bilal, and Amina</b> — each run a different test (blood, swab, culture) on a different shift (morning, evening, night). Who runs what, and when?<br><b>1.</b> The <b>culture</b> test is run on the <b>night</b> shift. &nbsp;<b>2.</b> Bilal runs the culture test. &nbsp;<b>3.</b> Yusra does not work the morning shift. &nbsp;<b>4.</b> The <b>blood</b> test is run on the <b>morning</b> shift.",
         "fact": "The spleen filters blood and holds a reserve of white blood cells, ready to be released.",
         "a": "Bilal — culture — night · Yusra — swab — evening · Amina — blood — morning.",
         "steps": "Clue 2 gives <b>Bilal the culture</b>; clue 1 puts him on <b>night</b>. Clue 3 keeps Yusra off the morning and night is taken, so <b>Yusra is evening</b>, leaving Amina the morning. Clue 4 makes morning the blood test &rarr; <b>Amina blood</b>, Yusra swab. Without clue 4 those two could swap."},
        {"q": "A scanner holds only <b>2 slides at a time</b>. Every slide must be scanned on <b>both</b> of its sides, and each scan takes <b>5 minutes</b>. What is the <b>shortest</b> time to finish <b>3 slides</b>? <i>It is less than you think.</i>",
         "fact": "Antiseptic on a cut kills germs — but it kills some of your own repairing cells too, which is why clean water is often enough.",
         "a": "%d minutes." % m8_scan,
         "steps": "Slides A, B, C. <b>Round 1</b>: A-front, B-front. <b>Round 2</b>: A-back, <i>C-front</i> &mdash; this is the move; B comes off half done on purpose. <b>Round 3</b>: B-back, C-back. 3 &times; 5 = <b>%d minutes</b>. The 20-minute trap finishes A and B first, then runs C alone with the scanner half empty." % m8_scan},
        {"q": "A box holds vials of <b>4 different vaccines</b>, all mixed together and all looking identical. Without looking, what is the <b>fewest</b> vials you must pick to be <b>certain</b> you have <b>3 of the same kind</b>?",
         "fact": "Identical twins can accept each other's organs without rejection — their immune systems read them as the same person.",
         "a": "%d vials." % m8_pick,
         "steps": "Ask what the <i>unluckiest</i> run looks like: 2 of every kind &mdash; 4 &times; 2 = <b>8</b> &mdash; and still no set of three. There are only 4 kinds, so vial <b>%d</b> must be a third of something. <b>%d</b>. \"Certain\" means it holds on your worst day." % (m8_pick, m8_pick)},
        {"q": "A tray of samples is sorted. <b>Half</b> of them go to the North lab. Then <b>3</b> are set aside for retesting. Then <b>half</b> of what is left goes to the South lab, and <b>7</b> samples remain on the tray. How many samples were on the tray to start with?",
         "fact": "Breast milk carries the mother's antibodies, so a baby borrows a defence while building its own.",
         "a": "%d samples." % m8_start,
         "steps": "Work backwards, flipping every step. 7 left after half went south &rarr; <b>14</b>. Undo the 3 set aside &rarr; <b>17</b>. That was what remained after half went north, so double it &rarr; <b>%d</b>. Forwards: %d &rarr; %d &rarr; %d &minus; 3 = 14 &rarr; <b>7</b>. &check;" % (m8_start, m8_start, m8_start // 2, m8_start // 2)},
    ],
    "kid1_watch": "#1 and #4 are one lesson in two costumes: the obvious multiplication is the wrong one. Expect <b>30</b> on #1 &mdash; ask him to name the two people in one handshake, then ask how many times he counted it. Expect <b>day 6</b> on #4; the question that fixes it is \"what was it the day before it was full?\" #2 is his first substitution puzzle &mdash; if he stalls: \"the flask <i>is</i> three vials.\" #3 is the careless one.",
    "kid2_watch": "#2 is the one worth sitting with. Nearly everyone answers <b>20 minutes</b>, because they finish one slide before starting the next; the whole idea is taking B off half-done. If he stalls, give him the three rounds on paper, then ask why the scanner is never idle. #3 is yesterday's pigeonhole made harder &mdash; 3 of a kind from 4 kinds &mdash; so <b>5</b> is the expected wrong answer. On #1 watch whether he writes a table. #4 goes wrong when done in his head.",
}

ALL = [JUL29L, JUL30L, JUL31L, AUG1L, AUG2L, AUG16L, AUG17L, AUG18L]
