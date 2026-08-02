"""verify_public.py — refuse to publish site/ if anything private survived the build.

    python3 build_site.py && python3 verify_public.py

Exit 0 means site/ is safe to deploy. Exit 1 means DO NOT DEPLOY.

WHY THIS IS A SEPARATE PROGRAM
------------------------------
`build_site.py` intends to strip private data. This one checks whether it did. They
are different claims and only the second one is evidence — the same reason
`verify_drills.py` does not import the generator it audits.

The forbidden list is built from `kids.local.json`, so it adapts to whoever runs it,
plus fixed terms that identify a family regardless of whose repo this is.

IT IS MUTATION-TESTED. A deliberately planted name was confirmed to fail it on
2026-08-01 — a gate that cannot fail is not a gate.

⚠️ This checks the OUTPUT, not the intent, and it only knows the strings it is told
about. It is the last line, not the only one: the allow-list in `build_site.py`
(SHEETS) is what actually decides that a file is publishable. A sheet not on that
list is never copied, which is the safe default.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")

# Terms that identify the family regardless of config. Extend rather than remove.
# NOTE: "Watch for:" was here and was WRONG. It appears in 17 sheets as generic
# teaching text inside an answer step ("Watch for: subtracting 230 from 145 first")
# — useful pedagogy, not private. The per-child boxes are `<div class="watch">`,
# which build_site.py removes structurally. Match on structure, not on a phrase that
# also occurs innocently.
# Structural markers only — safe to commit. The terms that are themselves sensitive
# (a school name, an employer) live in private/forbidden-terms.txt, which is
# gitignored, ONE PER LINE.
#
# This is not fussiness. When the history rewrite replaced the school name repo-wide,
# it rewrote this list too, and the gate began banning the word "school" — which
# appears innocently in a dozen worksheets. A scrubber that hardcodes the strings it
# hunts is a scrubber that leaks them and breaks when they change.
FIXED_FORBIDDEN = ["RESULTS.md", "kids.local"]


def _private_terms():
    p = os.path.join(HERE, "private", "forbidden-terms.txt")
    if not os.path.exists(p):
        return []
    with open(p) as f:
        return [ln.strip() for ln in f
                if ln.strip() and not ln.startswith("#")]


def forbidden_terms():
    terms = list(FIXED_FORBIDDEN) + _private_terms()
    local = os.path.join(HERE, "kids.local.json")
    if os.path.exists(local):
        with open(local) as f:
            for k in json.load(f)["kids"]:
                if k.get("name"):
                    terms.append(k["name"])
    return terms


def _structural(doc, pos):
    """True if this occurrence is in markup that says WHOSE sheet it is.

    Header fields, section titles, comments and watch boxes identify an owner.
    Problem and answer prose is a story, and a story character is not a person.
    """
    ctx = doc[max(0, pos - 200):pos]
    return ('section-title' in ctx[-90:] or 'class="meta"' in ctx[-200:]
            or '<!--' in ctx.split('-->')[-1] or 'class="watch"' in ctx[-200:])


def main():
    if not os.path.isdir(SITE):
        print("site/ does not exist — run build_site.py first", file=sys.stderr)
        return 1

    terms = forbidden_terms()
    # Story characters in the logic puzzles legitimately use given names, and one of
    # them may coincide with a child's. A NAME: FIELD is a disclosure; a character in
    # a falconry puzzle is not. So the name check is scoped to the header field and
    # to plain occurrences outside puzzle prose.
    # blank means empty, whitespace, or &nbsp; — anything else is a real name
    name_field = re.compile(r'Name:\s*<span>((?:(?!</span>).)*)</span>')

    files, hits, warns = 0, [], []
    for root, _, names in os.walk(SITE):
        for n in names:
            p = os.path.join(root, n)
            rel = os.path.relpath(p, SITE)
            try:
                doc = open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            files += 1

            for m in name_field.finditer(doc):
                inner = m.group(1).replace("&nbsp;", "").strip()
                if inner:
                    hits.append(f"{rel}: NON-BLANK Name: field -> {inner[:40]!r}")

            for t in terms:
                if t in FIXED_FORBIDDEN or t in _private_terms():
                    if t.lower() in doc.lower():
                        hits.append(f"{rel}: forbidden term {t!r}")
                else:
                    # a child's name: flag only outside puzzle body text
                    # case-INSENSITIVE: a case-sensitive sweep reported 'animations/
                    # index.html: 0 names' on a file containing "id": "kid1-mult".
                    for m in re.finditer(re.escape(t), doc, re.I):
                        ctx = doc[max(0, m.start() - 120):m.start()]
                        # Body-text containers, i.e. places a STORY lives. Kept as an
                        # explicit list because each one was found by this gate failing:
                        # qtext/ans/steps on practice sheets, prompt/scaffold on TEACH
                        # sheets. Add to it rather than loosening _structural().
                        if any(c in ctx for c in ('class="qtext"', 'class="ans"',
                                                  'class="steps"', 'class="prompt"',
                                                  'class="scaffold"', 'class="fact"')) \
                           or "<b>" in ctx[-30:]:
                            continue          # story character, not a disclosure
                        snippet = doc[max(0, m.start()-45):m.start()+25].strip()[-60:]
                        target = hits if _structural(doc, m.start()) else warns
                        target.append(f"{rel}: {t!r} …{snippet!r}")

    print(f"scanned {files} files in site/ against {len(terms)} forbidden terms")
    if warns:
        print(f"\n{len(warns)} name(s) in PUZZLE TEXT — story characters, not a "
              f"disclosure. Listed so the call is yours, not mine:")
        for w in warns[:6]:
            print("  ·", w)
        if len(warns) > 6:
            print(f"  … and {len(warns)-6} more")
    if hits:
        print(f"\n{len(hits)} PROBLEM(S) — DO NOT DEPLOY:\n", file=sys.stderr)
        for h in hits[:30]:
            print("  ✗", h, file=sys.stderr)
        if len(hits) > 30:
            print(f"  … and {len(hits)-30} more", file=sys.stderr)
        return 1
    print("clean — safe to deploy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
