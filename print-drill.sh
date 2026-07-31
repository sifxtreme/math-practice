#!/usr/bin/env bash
# print-drill.sh — print a math-drills.com PDF through the SAME one-day-at-a-time
# guard as print-worksheet.sh.
#
# Why this exists: the drill leg is half the paper. The 2026-07-28 bulk run was
# 20 jobs — 10 worksheets AND 10 drill PDFs — and the drills went out via a bare
# `lp`, which no guard can see. Guarding only print-worksheet.sh would leave that
# door open. Route drills through here.
#
# Usage:
#   ./print-drill.sh ~/Downloads/multiplication_0301_001.pdf --for kid1 --date today
#   ./print-drill.sh <file.pdf> --date "July 31, 2026" [--printer NAME] [--dry-run]
#   ./print-drill.sh <file.pdf> --override-day-guard      # break the rule (loud)
#
# Grab the PDF the way DRILLS.md says: the non-`qp` link, 2 pages — questions
# then the answer key. Both pages print; page 1 is the kid's, page 2 is yours.

set -uo pipefail

# shellcheck source=day-guard.sh
. "$(cd "$(dirname "$0")" && pwd)/day-guard.sh"

PRINTER="Brother_HL_L2305_series"
DRY=0
STAMP_DATE=""
OVERRIDE_GUARD=0
WHO=""
SRC=""

while [ $# -gt 0 ]; do
  case "$1" in
    --printer) PRINTER="$2"; shift 2 ;;
    --date)    STAMP_DATE="$2"; shift 2 ;;
    --for)     WHO="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --override-day-guard) OVERRIDE_GUARD=1; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)         SRC="$1"; shift ;;
  esac
done

if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "usage: print-drill.sh <drill.pdf> [--for kid1|kid2] [--date DATE] [--dry-run]" >&2
  exit 1
fi

base="$(basename "${SRC%.pdf}")"
label="drill ${WHO:+$WHO }$base"

# A drill PDF carries no Date field to stamp — unlike a generated worksheet, the
# --date here exists purely to tell the guard which day this paper is for.
pages="$(python3 - "$SRC" <<'PY'
import re, sys
raw = open(sys.argv[1], 'rb').read()
c = [int(x) for x in re.findall(rb'/Count\s+(\d+)', raw)]
print(max(c) if c else 0)
PY
)"
echo "Drill '$base': $pages pages (math-drills sheets are 2 — questions, then key)."
if [ "$pages" != "2" ]; then
  echo "WARNING: expected 2 pages. Did you grab the 'qp' (questions-only) link by mistake?" >&2
fi

if [ "$DRY" = "1" ]; then
  echo "[dry-run] would run: lp -d $PRINTER -t \"$label\" \"$SRC\""
  echo "[dry-run] day guard not consulted — it runs only on a real print."
  exit 0
fi

TARGET_DAY="$(to_iso_day "$STAMP_DATE")" || {
  echo "ERROR: couldn't parse --date '$STAMP_DATE' into a calendar day." >&2; exit 1; }
guard_one_day "$TARGET_DAY" "$label" "$OVERRIDE_GUARD"

lp -d "$PRINTER" -t "$label" "$SRC"
echo "Sent to $PRINTER (for $TARGET_DAY)."
