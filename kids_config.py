"""kids_config.py — who the sheets are for, loaded from a gitignored file.

Shared by `drill_gen.py` and `build_sheets.py` so there is exactly one place a real
name enters the program. Committed code keys on `id` (kid1, kid2); the name is read
here and reaches paper only in the printed `Name:` field.

See README.md "Setting it up for your kids" and `kids.example.json`.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = os.path.join(HERE, "kids.local.json")
EXAMPLE = os.path.join(HERE, "kids.example.json")

_ORDINAL = {1: "1st", 2: "2nd", 3: "3rd"}


def load_kids():
    """Ordered list of kid dicts, real if kids.local.json exists, else placeholders.

    The fallback is deliberately LOUD. A silent one would print a stack of sheets
    addressed to "Kid One" and you would not find out until they were on the table.
    """
    path = LOCAL if os.path.exists(LOCAL) else EXAMPLE
    with open(path) as f:
        kids = json.load(f)["kids"]
    if path == EXAMPLE:
        bar = "=" * 72
        print(f"{bar}\nNOTICE: kids.local.json not found — using placeholder names from\n"
              f"        kids.example.json. Sheets will say 'Kid One' / 'Kid Two'.\n"
              f"        Fix:  cp kids.example.json kids.local.json\n{bar}",
              file=sys.stderr)
    return kids


def kids_by_id():
    return {k["id"]: k for k in load_kids()}


def kid_name(kids, kid_id):
    if kid_id not in kids:
        raise SystemExit(
            f"ERROR: no kid with id '{kid_id}' in your kids file.\n"
            f"       Known ids: {', '.join(sorted(kids)) or '(none)'}\n"
            f"       Drill plans and spec dicts are keyed on those ids.")
    return kids[kid_id]["name"]


def grade_label(kid):
    """3 -> '3rd Grade'. Display only; real difficulty comes from AGENTS.md's pin."""
    g = kid.get("grade")
    if g is None:
        return ""
    return f"{_ORDINAL.get(g, f'{g}th')} Grade"
