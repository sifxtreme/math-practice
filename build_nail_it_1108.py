"""build_nail_it_1108.py -- 10 new afternoon problems each for Yusuf (kid2) and Musa (kid1), 2026-11-08.

Asif (2026-11-08, after the morning sheets): "let's just do the 10 new problems for Yusuf, new prompts for Musa,
so that they can nail it down."  Instinct authored the sets in bifrost (family/school/, 11-08):
  Yusuf: yusuf-average-problems (5, "a newcomer joins", like #15) + yusuf-two-price-problems (5, "$d more than")
  Musa:  musa-balance-scale-problems (10, like #11)
No drills today; fluency drills move to the week (Asif, same message).

Every answer is recomputed here from the numbers in the prompt and must match the bifrost key, or the build fails.

    python3 build_nail_it_1108.py <outdir>
Writes <outdir>/{yusuf,musa}-nail-it-2026-11-08-{student,parent-key}.pdf. Never prints.
"""
import html
import sys

from build_exam_practice_1108 import to_pdf
from kids_config import kid_name, kids_by_id

DATE = "Sun 8 Nov 2026"

# --- Yusuf: averages. (named, friends, avg, joiner, joiner_amt, noun, verb_phrase, bifrost answer)
AVG = [
    ("Zaid", 2, 12, "Omar", 24, "marbles", "have an average of 12 marbles each. Then Omar joins them with 24 marbles", 15),
    ("Layla", 4, 10, "Sara", 16, "books", "have an average of 10 books each. Then Sara joins them with 16 books", 11),
    ("Hamza", 3, 20, "Bilal", 10, "points", "scored an average of 20 points each in a game. Then Bilal plays and scores 10 points", 18),
    ("Aisha", 2, 25, "Hana", 33, "cards", "have an average of 25 trading cards each. Then Hana joins them with 33 cards", 27),
    ("Karim", 5, 8, "Dani", 15, "cookies", "baked an average of 8 cookies each. Then Dani joins them with 15 cookies", 9),
]
# --- Yusuf: two prices. (A item, B item, d, ca, cb, total, qa, qb, place, bifrost answer)
PRICE = [
    ("water bottle", "juice box", 3, 2, 3, 21, 4, 1, "At a school store, ", 27),
    ("sandwich", "bag of chips", 5, 4, 1, 35, 2, 6, "At the lunch counter, ", 34),
    ("puzzle book", "pack of stickers", 6, 3, 4, 46, 5, 2, "", 58),
    ("basketball", "tennis ball", 8, 2, 5, 58, 3, 4, "", 66),
    ("paperback book", "comic book", 7, 5, 2, 70, 2, 5, "", 49),
]
PLURAL = {"water bottle": "water bottles", "juice box": "juice boxes", "sandwich": "sandwiches",
          "bag of chips": "bags of chips", "puzzle book": "puzzle books", "pack of stickers": "packs of stickers",
          "basketball": "basketballs", "tennis ball": "tennis balls", "paperback book": "paperbacks",
          "comic book": "comic books"}
# --- Musa: balance. (n_a, a, n_b, b, b_grams, ask_n, bifrost answer grams)  "n_a a weigh the same as n_b b"
BAL = [
    (3, "oranges", 5, "lemons", 60, 4, 400), (2, "melons", 8, "apples", 150, 3, 1800),
    (5, "mangoes", 10, "peaches", 90, 2, 360), (4, "bananas", 12, "strawberries", 30, 6, 540),
    (3, "cantaloupes", 9, "oranges", 120, 2, 720), (2, "pineapples", 6, "pears", 100, 3, 900),
    (6, "apples", 4, "grapefruits", 240, 3, 480), (4, "pears", 10, "plums", 40, 5, 500),
    (3, "papayas", 12, "kiwis", 75, 4, 1200),
]
SING = {"lemons": "lemon", "apples": "apple", "peaches": "peach", "strawberries": "strawberry", "oranges": "orange",
        "pears": "pear", "grapefruits": "grapefruit", "plums": "plum", "kiwis": "kiwi", "watermelons": "watermelon",
        "oranges_": "orange", "melons": "melon", "mangoes": "mango", "bananas": "banana", "cantaloupes": "cantaloupe",
        "pineapples": "pineapple", "papayas": "papaya"}


def pl(n, item):
    return "%d %s" % (n, item if n == 1 else PLURAL[item])


def yusuf():
    probs, keys = [], []
    for who, fr, avg, j, amt, noun, story, want in AVG:
        people = fr + 1
        tot = avg * people
        new = tot + amt
        assert new % (people + 1) == 0, who
        ans = new // (people + 1)
        assert ans == want, (who, ans, want)
        probs.append("%s and %s %d friends %s. What is the new average number of %s per person?" % (
            who, "her" if who in ("Layla", "Aisha") else "his", fr, story, noun))
        keys.append(("New average = %d %s" % (ans, noun), [
            "People: %s + %d friends = %d people." % (who, fr, people),
            "Total: %d × %d = %d." % (avg, people, tot),
            "%s adds %d: %d + %d = %d." % (j, amt, tot, amt, new),
            "People now: %d + 1 = %d." % (people, people + 1),
            "New average: %d ÷ %d = <b>%d</b>." % (new, people + 1, ans)]))
    for A, B, d, ca, cb, T, qa, qb, place, want in PRICE:
        b = (T - ca * d) // (ca + cb)
        assert (ca + cb) * b + ca * d == T, A
        a = b + d
        ans = qa * a + qb * b
        assert ans == want, (A, ans, want)
        lead = place + ("a " if place else "A ") + A
        probs.append("%s costs $%d more than a %s. %s and %s cost $%d. How much do %s and %s cost?" % (
            lead, d, B, pl(ca, A)[0].upper() + pl(ca, A)[1:] if not place else pl(ca, A), pl(cb, B), T,
            pl(qa, A), pl(qb, B)))
        keys.append(("$%d" % ans, [
            "Let b = one %s. Then one %s = b + %d." % (B, A, d),
            "%d(b + %d) + %db = %d" % (ca, d, cb, T),
            "%db + %d = %d, so %db = %d, b = $%d; %s = $%d." % (ca + cb, ca * d, T, ca + cb, T - ca * d, b, A, a),
            "%d × %d + %d × %d = %d + %d = <b>$%d</b>." % (qa, a, qb, b, qa * a, qb * b, ans),
            "Check: %d × %d + %d × %d = $%d ✓" % (ca, a, cb, b, T)]))
    return probs, keys


def musa():
    probs, keys = [], []
    for na, a, nb, b, g, q, want in BAL:
        tot = nb * g
        assert tot % na == 0, a
        one = tot // na
        ans = q * one
        assert ans == want, (a, ans, want)
        probs.append("On a balance scale, %d %s weigh the same as %d %s. Each %s weighs %d grams. How much do %d %s weigh?" % (
            na, a, nb, b, SING[b], g, q, a))
        keys.append(("%d %s = %d g" % (q, a, ans), [
            "Known side: %d × %d g = %d g." % (nb, g, tot),
            "%d %s = %d g, so 1 %s = %d ÷ %d = %d g." % (na, a, tot, SING[a], tot, na, one),
            "%d × %d = <b>%d g</b>." % (q, one, ans)]))
    # #10 is the reverse direction (each PEACH known, ask watermelons)
    na, a, nb, b, g, q = 8, "peaches", 2, "watermelons", 250, 3
    tot = na * g
    one = tot // nb
    ans = q * one
    assert ans == 3000
    probs.append("On a balance scale, 8 peaches weigh the same as 2 watermelons. Each peach weighs 250 grams. How much do 3 watermelons weigh?")
    keys.append(("3 watermelons = 3000 g", ["Known side: 8 × 250 g = 2000 g.",
                 "2 watermelons = 2000 g, so 1 watermelon = 2000 ÷ 2 = 1000 g.", "3 × 1000 = <b>3000 g</b>."]))
    return probs, keys


CSS = """@page{size:letter;margin:0.55in 0.6in}body{font:13pt/1.45 Georgia,serif;color:#000}
h1{font:bold 17pt Helvetica,Arial,sans-serif;margin:0 0 2pt}.sub{font:10pt Helvetica,Arial,sans-serif;margin-bottom:10pt}
.p{break-inside:avoid;border-bottom:1px solid #999;padding:6pt 0 0;min-height:2.05in}.p b.n{font-family:Helvetica,Arial;margin-right:6pt}
.ans{margin-top:8pt;font:11pt Helvetica,Arial}.k{break-inside:avoid;margin:0 0 9pt}.k h3{font:bold 12pt Helvetica,Arial;margin:0}
.k div{font-size:11.5pt;margin-left:14pt}h2{font:bold 13pt Helvetica,Arial;margin:10pt 0 2pt;border-bottom:2px solid #000}"""


def page(title, sub, body):
    return "<!DOCTYPE html><html><head><meta charset='utf-8'><title>%s</title><style>%s</style></head><body><h1>%s</h1><div class='sub'>%s</div>%s</body></html>" % (
        html.escape(title), CSS, html.escape(title), sub, body)


def build(out, kid, slug, probs, keys, sections, tip):
    name = kid_name(kids_by_id(), kid)
    body = ""
    for i, p in enumerate(probs):
        for at, label in sections:
            if i == at:
                body += "<h2>%s</h2>" % label
        body += "<div class='p'><b class='n'>%d.</b>%s<div class='ans'>Answer: ______________</div></div>" % (i + 1, html.escape(p))
    s = to_pdf(page("%s · 10 more to nail it" % name, "%s · Name ________ · %s" % (DATE, tip), body), out, slug, "student")
    kb = "".join("<div class='k'><h3>%d. %s</h3>%s</div>" % (i + 1, h, "".join("<div>%s</div>" % l for l in ls))
                 for i, (h, ls) in enumerate(keys))
    k = to_pdf(page("%s · parent key" % name, DATE + " · keep separate from the student sheet", kb), out, slug, "parent-key")
    return s, k


def main():
    out = sys.argv[1]
    yp, yk = yusuf()
    mp, mk = musa()
    assert len(yp) == 10 and len(mp) == 10
    print(*build(out, "kid2", "yusuf-nail-it-2026-11-08", yp, yk,
                 [(0, "A. Someone joins the group"), (5, "B. One costs more than the other")],
                 "Averages: count EVERY person. Prices: write the equation first."))
    print(*build(out, "kid1", "musa-nail-it-2026-11-08", mp, mk, [(0, "Balance scale")],
                 "Find the total on the known side first. Then one fruit. Then the question."))


if __name__ == "__main__":
    main()
