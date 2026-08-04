#!/usr/bin/env bash
# test-print-path.sh — end-to-end test of the WHOLE print path, printer included.
#
# Run it any time you touch print-worksheet.sh, day-guard.sh, or add a new sheet
# type:  ./test-print-path.sh
#
# WHY THIS EXISTS, WHEN test-day-guard.sh ALREADY PASSES
# ------------------------------------------------------
# test-day-guard.sh calls `guard_one_day` directly. That proves the guard's logic
# and nothing about the path that reaches it. On 2026-08-03 it had 23 green cases
# while TWO seam bugs sat in the real path:
#
#   1. print-worksheet.sh rewrote `--date today` from the real clock BEFORE the
#      guard saw it, and
#   2. day-guard.sh's to_iso_day did the same.
#
# So a simulated Aug 8 morning stamped the paper Aug 3, recorded Aug 3 in the
# ledger, and had the guard reason about Aug 8. Nothing in the suite could see it,
# because nothing in the suite went through print-worksheet.sh. `--dry-run` cannot
# see it either — it prints "day guard not consulted" and returns before the guard.
#
# The missing piece was never the guard. It was a way to take the REAL path without
# a printer at the end of it. That is a stub `lp` on PATH, and it is the only thing
# this file does that the other suite does not.
#
# Nothing is printed, and the real ledger is never written — every case runs with
# GUARD_LEDGER pointed at a throwaway copy, checksummed before and after.

set -uo pipefail
cd "$(dirname "$0")"

PASS=0; FAIL=0
SIM="$(mktemp -d)"; trap 'rm -rf "$SIM"' EXIT
mkdir -p "$SIM/bin"

# The stub. `lp` is the last thing print-worksheet.sh does, so intercepting it here
# means every step before it — render, page-count self-check, --date rewrite, all
# three guards, the ledger append — runs exactly as it does on a real morning.
cat > "$SIM/bin/lp" <<'STUB'
#!/usr/bin/env bash
echo "$*" >> "$SIM_LOG"
echo "request id is stub-$$ (1 file(s))"
STUB
chmod +x "$SIM/bin/lp"

export SIM_LOG="$SIM/lp.log"; : > "$SIM_LOG"
export PATH="$SIM/bin:$PATH"
export GUARD_LEDGER="$SIM/ledger.tsv"

LEDGER_SUM_BEFORE="$(shasum print-ledger.tsv | cut -d' ' -f1)"
reset_ledger() { cp print-ledger.tsv "$GUARD_LEDGER"; : > "$SIM_LOG"; }

SHEET="worksheet-facts-drill.html"
[ -f "$SHEET" ] || { echo "generate a sheet first: python3 drill_gen.py --skill facts"; exit 1; }

# case <expect:allow|refuse> <today> <date-arg> <sheet> <desc> [extra args...]
case_() {
  local expect="$1" today="$2" datearg="$3" sheet="$4" desc="$5"; shift 5
  local out rc
  out="$(GUARD_TODAY="$today" ./print-worksheet.sh "$sheet" --date "$datearg" "$@" 2>&1)"; rc=$?
  local got="allow"; [ "$rc" -ne 0 ] && got="refuse"
  if [ "$got" = "$expect" ]; then
    PASS=$((PASS+1)); printf '  ✓ %s\n' "$desc"
  else
    FAIL=$((FAIL+1)); printf '  ✗ %s\n     expected %s, got %s:\n%s\n' "$desc" "$expect" "$got" "$out"
  fi
}

# The check the seam bugs would have failed: the day the guard recorded must be the
# day we simulated. Both bugs left the guard logic correct and the DAY wrong, which
# is why an allow/refuse assertion alone did not catch them.
targets_recorded() {
  awk -F'\t' '$1 !~ /^#/ {print $2}' "$GUARD_LEDGER" \
    | sort | uniq -c | awk '{printf "%s(x%s) ", $2, $1}'
}
expect_targets() {
  local want="$1" desc="$2" got
  got="$(diff <(awk -F'\t' '$1 !~ /^#/ {print $2}' print-ledger.tsv | sort) \
              <(awk -F'\t' '$1 !~ /^#/ {print $2}' "$GUARD_LEDGER" | sort) \
         | grep '^>' | sed 's/^> //' | sort -u | tr '\n' ' ')"
  got="${got% }"
  if [ "$got" = "$want" ]; then PASS=$((PASS+1)); printf '  ✓ %s\n' "$desc"
  else FAIL=$((FAIL+1)); printf '  ✗ %s\n     ledger recorded [%s], wanted [%s]\n' "$desc" "$got" "$want"; fi
}

echo "A requested drill morning — the exact commands AGENTS.md documents"
reset_ledger
case_ allow 2026-08-08 today "$SHEET" "facts sheet, --date today"
case_ allow 2026-08-08 today worksheet-division-drill.html "division drill, same morning"
expect_targets "2026-08-08" "both jobs recorded against the SIMULATED day, not the real one"

echo
echo "The three guards, reached through the real script"
case_ refuse 2026-08-08 "August 9, 2026" "$SHEET" "Guard A — tomorrow's sheet today"
case_ refuse 2026-08-08 "August 7, 2026" "$SHEET" "Guard B — a second target day this morning"
case_ refuse 2026-08-09 "August 8, 2026" "$SHEET" "Guard C — yesterday's paper already exists"

echo
echo "A refusal must stop BEFORE the printer"
JOBS_BEFORE="$(wc -l < "$SIM_LOG" | tr -d ' ')"
case_ refuse 2026-08-09 "August 8, 2026" "$SHEET" "refused reprint"
JOBS_AFTER="$(wc -l < "$SIM_LOG" | tr -d ' ')"
if [ "$JOBS_BEFORE" = "$JOBS_AFTER" ]; then
  PASS=$((PASS+1)); echo "  ✓ nothing reached lp on a refusal"
else
  FAIL=$((FAIL+1)); echo "  ✗ a refused job still called lp"
fi

echo
echo "Override escapes, and is recorded as an override"
reset_ledger
case_ allow 2026-08-08 today "$SHEET" "seed the day"
case_ allow 2026-08-09 "August 8, 2026" "$SHEET" "reprint with the hatch" --override-day-guard
if grep -q "OVERRIDE" "$GUARD_LEDGER"; then
  PASS=$((PASS+1)); echo "  ✓ the override is written to the ledger, not just warned about"
else
  FAIL=$((FAIL+1)); echo "  ✗ override not recorded in the ledger"
fi

echo
echo "Every generated sheet type survives the path"
for f in worksheet-facts-drill.html worksheet-division-drill.html \
         worksheet-multiplication-drill.html worksheet-division-drill-plain.html; do
  [ -f "$f" ] || continue
  reset_ledger
  case_ allow 2026-08-08 today "$f" "$(basename "$f" .html)"
done

echo
echo "The real ledger was not touched by these tests"
if [ "$LEDGER_SUM_BEFORE" = "$(shasum print-ledger.tsv | cut -d' ' -f1)" ]; then
  PASS=$((PASS+1)); echo "  ✓ checksum unchanged"
else
  FAIL=$((FAIL+1)); echo "  ✗ THE REAL LEDGER CHANGED — a test wrote to it"
fi

echo
echo "──────────────────────────────"
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
