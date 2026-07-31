#!/usr/bin/env bash
# print-worksheet.sh — render a math worksheet to a clean 3-page PDF and print it.
#
# Why this exists: Chrome's `--headless --print-to-pdf` ignores the page's
# `@page` margins and forces ~1in margins, overflowing the 3-page worksheets to
# 5 pages (each kid's sheet spills its last problem to a 2nd page). This script
# renders a lightly-tightened copy (smaller work boxes + paddings, SAME fonts)
# that fits 3 pages at those fat margins, then prints it. Your source .html is
# untouched — it still prints full-size via Cmd+P.
#
# Usage:
#   ./print-worksheet.sh worksheet-worldcup.html                # render + print ALL pages (incl. answer key)
#   ./print-worksheet.sh worksheet-worldcup.html --dry-run      # render only, don't print
#   ./print-worksheet.sh <file.html> --printer <NAME>           # print to a different printer
#   ./print-worksheet.sh <file.html> --no-key                   # kids' sheets only, skip the answer key
#   ./print-worksheet.sh <file.html> --key-only                 # print ONLY the answer key page (no kid sheets)
#   ./print-worksheet.sh <file.html> --date "July 28, 2026"     # stamp the Date: field at print time
#   ./print-worksheet.sh <file.html> --date today               # same, using today's date
#   ./print-worksheet.sh <file.html> --override-day-guard       # break the one-day-at-a-time rule (loud)
#
# ⚠️ ONE DAY'S WORTH OF PAPER AT A TIME. This script refuses to print a sheet
# dated in the future, and refuses a second target day once you've printed for
# one today. See day-guard.sh for the why and the escape hatch. Reprinting a
# PAST day is fine — that's still one day's worth.
#
# --date stamps the kids' `Date:` fields in the rendered copy only; your source
# .html is never touched. That's the point: reprinting an old sheet used to mean
# hand-editing its Date span first, and a sheet that leaves the printer undated
# is unfilable — you can't tell later which day it was for or whether it was done.
# The answer key is deliberately left undated.
#
# Prints ALL pages by default, answer key included (Asif asked for the key every
# time, 2026-07-26). Pass --no-key for kids' sheets only, or --key-only when the
# sheets are already printed and you just need the key.

set -uo pipefail

# shellcheck source=day-guard.sh
. "$(cd "$(dirname "$0")" && pwd)/day-guard.sh"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PRINTER="Brother_HL_L2305_series"
DRY=0
INCLUDE_KEY=1   # default ON since 2026-07-26 — Asif wants the key every time
KEY_ONLY=0
STAMP_DATE=""
OVERRIDE_GUARD=0
SRC=""

while [ $# -gt 0 ]; do
  case "$1" in
    --printer)  PRINTER="$2"; shift 2 ;;
    --date)     STAMP_DATE="$2"; shift 2 ;;
    --dry-run)  DRY=1; shift ;;
    --override-day-guard) OVERRIDE_GUARD=1; shift ;;
    --both)     INCLUDE_KEY=1; shift ;;   # kept for compatibility; now the default
    --no-key)   INCLUDE_KEY=0; shift ;;   # kids' sheets only
    --key-only) KEY_ONLY=1; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)         SRC="$1"; shift ;;
  esac
done

if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "usage: print-worksheet.sh <worksheet.html> [--dry-run] [--printer NAME] [--both|--key-only]" >&2
  exit 1
fi
if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at: $CHROME" >&2; exit 1
fi

if [ "$STAMP_DATE" = "today" ]; then
  STAMP_DATE="$(date '+%B %-d, %Y')"
fi

TMP="$(mktemp -d)"
base="$(basename "${SRC%.html}")"
PRINTHTML="$TMP/$base-print.html"
PDF="$TMP/$base.pdf"

# 1) Tighten the layout so it fits Chrome-headless's fat margins at 3 pages.
#    Fonts are left alone; only work-box height + vertical spacing shrink.
python3 - "$SRC" "$PRINTHTML" "$STAMP_DATE" <<'PY'
import html as _html
import re, sys
src, out = sys.argv[1], sys.argv[2]
stamp = sys.argv[3] if len(sys.argv) > 3 else ""
h = open(src).read()

# --date: rewrite the kids' Date: spans in the RENDER ONLY (source stays untouched).
# Matches whether the span is empty or already carries a date, so it overrides a
# stale baked-in date rather than doubling up. The answer key has no Date: field,
# so it stays undated automatically — don't add one.
if stamp:
    pat = re.compile(r'(<div>Date:\s*<span>).*?(</span></div>)', re.S)
    h, n = pat.subn(lambda m: m.group(1) + '&nbsp;' + _html.escape(stamp) + m.group(2), h)
    if n == 0:
        sys.stderr.write("WARNING: --date given but no 'Date: <span>' field matched — sheet will print undated.\n")
    else:
        sys.stderr.write("Stamped %d date field(s): %s\n" % (n, stamp))

subs = [
    (r'@page \{ margin: [0-9.]+in; \}', '@page { size: letter; margin: 0.35in; }'),
    (r'line-height: 1\.4;',      'line-height: 1.22;'), # body — biggest space lever
    (r'height: 78px;',            'height: 40px;'),     # .work
    (r'padding: 9px 12px;',       'padding: 5px 11px;'),# .problem
    (r'margin-bottom: 4px;',      'margin-bottom: 2px;'),
    (r'margin: 4px 0 7px 0;',     'margin: 2px 0 3px 0;'),# .qtext
    (r'margin-top: 7px;',         'margin-top: 3px;'),  # .fact
    (r'padding: 4px 8px;',        'padding: 3px 8px;'), # .fact
]
for pat, rep in subs:
    h = re.sub(pat, rep, h)
open(out, 'w').write(h)
PY

expected="$(grep -c 'class="sheet' "$SRC")"

# 2) Render (single-shot, with polling — headless can hang otherwise).
pkill -f "Google Chrome.*headless" 2>/dev/null || true; sleep 1
"$CHROME" --headless=new --disable-gpu --no-sandbox --no-first-run --no-default-browser-check \
  --no-pdf-header-footer --virtual-time-budget=5000 --user-data-dir="$TMP/ud" \
  --print-to-pdf="$PDF" "file://$PRINTHTML" >/dev/null 2>&1 &
for _ in $(seq 1 40); do sleep 1; [ -s "$PDF" ] && sleep 1 && break; done
pkill -f "Google Chrome.*headless" 2>/dev/null || true

if [ ! -s "$PDF" ]; then
  echo "ERROR: render produced no PDF (Chrome may not have launched)." >&2; exit 1
fi

# 3) Page-count guard.
pages="$(python3 - "$PDF" <<'PY'
import re, sys
raw = open(sys.argv[1], 'rb').read()
c = [int(x) for x in re.findall(rb'/Count\s+(\d+)', raw)]
print(max(c) if c else 0)
PY
)"
echo "Rendered '$base': $pages pages (expected $expected)."
if [ "$pages" != "$expected" ]; then
  echo "WARNING: page count != expected — this worksheet's CSS may differ from the template." >&2
  echo "         Inspect the PDF before relying on it: $PDF" >&2
fi

# 4) Choose page range. Default prints EVERYTHING including the answer key (changed 2026-07-26).
#    --no-key drops the last page; --key-only prints just it.
RANGE_ARGS=()
if [ "$KEY_ONLY" = "1" ] && [ "$pages" -ge 1 ]; then
  RANGE_ARGS=(-P "$pages")
  echo "Printing page $pages only (the answer key)."
elif [ "$INCLUDE_KEY" = "0" ] && [ "$pages" -ge 2 ]; then
  RANGE_ARGS=(-P "1-$((pages-1))")
  echo "Printing pages 1-$((pages-1)) (kids' sheets only; answer key suppressed via --no-key)."
fi

# 5) Print (or dry-run).
if [ "$DRY" = "1" ]; then
  # ${arr[@]+...} guard: macOS ships bash 3.2, where `set -u` treats an EMPTY
  # array expansion as unbound and kills the script — which is the default path
  # (no --key-only/--no-key => no page range => empty array), so a plain print
  # died right before `lp` ran, after printing a reassuring "Rendered: 3 pages".
  echo "[dry-run] would run: lp -d $PRINTER ${RANGE_ARGS[@]+${RANGE_ARGS[*]}} -t \"$base\" \"$PDF\""
  echo "PDF kept at: $PDF"
  echo "[dry-run] day guard not consulted — it runs only on a real print."
else
  # ONE DAY'S WORTH AT A TIME. Refuses (exit 2) before anything reaches `lp`.
  # No --date means the sheet is for today; the generated sheets ship with a
  # blank Date field, so there is no baked-in day to read instead.
  TARGET_DAY="$(to_iso_day "$STAMP_DATE")" || {
    echo "ERROR: couldn't parse --date '$STAMP_DATE' into a calendar day." >&2; exit 1; }
  guard_one_day "$TARGET_DAY" "$base" "$OVERRIDE_GUARD"

  lp -d "$PRINTER" ${RANGE_ARGS[@]+"${RANGE_ARGS[@]}"} -t "$base" "$PDF"
  echo "Sent to $PRINTER (for $TARGET_DAY)."
fi
