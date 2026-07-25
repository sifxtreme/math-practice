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
#   ./print-worksheet.sh worksheet-worldcup.html                # render + print to the Brother
#   ./print-worksheet.sh worksheet-worldcup.html --dry-run      # render only, don't print
#   ./print-worksheet.sh <file.html> --printer <NAME>           # print to a different printer
#   ./print-worksheet.sh <file.html> --both                     # also print the answer key page (default: skip it)
#   ./print-worksheet.sh <file.html> --key-only                 # print ONLY the answer key page (no kid sheets)
#
# Prints only the kids' sheets by default; pass --both to include the answer key,
# or --key-only when the sheets are already printed and you just need the key.

set -uo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PRINTER="Brother_HL_L2305_series"
DRY=0
INCLUDE_KEY=0
KEY_ONLY=0
SRC=""

while [ $# -gt 0 ]; do
  case "$1" in
    --printer)  PRINTER="$2"; shift 2 ;;
    --dry-run)  DRY=1; shift ;;
    --both)     INCLUDE_KEY=1; shift ;;
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

TMP="$(mktemp -d)"
base="$(basename "${SRC%.html}")"
PRINTHTML="$TMP/$base-print.html"
PDF="$TMP/$base.pdf"

# 1) Tighten the layout so it fits Chrome-headless's fat margins at 3 pages.
#    Fonts are left alone; only work-box height + vertical spacing shrink.
python3 - "$SRC" "$PRINTHTML" <<'PY'
import re, sys
src, out = sys.argv[1], sys.argv[2]
h = open(src).read()
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

# 4) Choose page range: kids' sheets only (drop the answer-key = last page) unless --both/--key-only.
RANGE_ARGS=()
if [ "$KEY_ONLY" = "1" ] && [ "$pages" -ge 1 ]; then
  RANGE_ARGS=(-P "$pages")
  echo "Printing page $pages only (the answer key)."
elif [ "$INCLUDE_KEY" = "0" ] && [ "$pages" -ge 2 ]; then
  RANGE_ARGS=(-P "1-$((pages-1))")
  echo "Printing pages 1-$((pages-1)) (kids' sheets; answer key skipped — use --both to include it)."
fi

# 5) Print (or dry-run).
if [ "$DRY" = "1" ]; then
  echo "[dry-run] would run: lp -d $PRINTER ${RANGE_ARGS[*]} -t \"$base\" \"$PDF\""
  echo "PDF kept at: $PDF"
else
  lp -d "$PRINTER" "${RANGE_ARGS[@]}" -t "$base" "$PDF"
  echo "Sent to $PRINTER."
fi
