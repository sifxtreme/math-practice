#!/usr/bin/env bash
# test-day-guard.sh — regression tests for the one-day-at-a-time print guard.
#
# Run it any time you touch day-guard.sh:  ./test-day-guard.sh
# Exits 0 if every case behaves. No printer is involved and the real ledger is
# never written — each case runs against a throwaway copy via GUARD_LEDGER.
#
# The cases below are not hypothetical. Guard C exists because A and B alone
# passed the two duplicate mornings (Jul 29, Jul 30) that the guard was written
# to prevent, and the "full day is four jobs" case exists because the first cut
# of Guard C refused file #2 of the same morning.

set -uo pipefail
cd "$(dirname "$0")"

PASS=0; FAIL=0
SEED="$(mktemp)"; trap 'rm -f "$SEED"' EXIT

# Checksum the real ledger up front so the "was it touched?" check at the end can
# actually FAIL. It used to be `git diff --quiet -- print-ledger.tsv`, which passes
# unconditionally while the file is untracked — a check that cannot fail is not a
# check, and it sat there reporting ✓ while five stray future-dated rows were in
# the file.
LEDGER_SUM_BEFORE="$(shasum print-ledger.tsv | cut -d' ' -f1)"

reset_ledger() { cp print-ledger.tsv "$SEED"; }

# Expected shape of the SEEDED history, so a bad hand-edit is caught rather than
# quietly changing what the guards see. These are the days the Jul 28 bulk run and
# the two duplicate mornings put on paper.
#
# ⚠️ Counts rows PRINTED BEFORE $SEED_ERA_END only, and that filter is the whole
# point. Without it the check counts live prints too, so the first legitimate print
# for any listed day fails it — which is exactly what happened on 2026-08-01, when a
# genuine replacement took 2026-08-01 from 4 rows to 9 and the suite went red for
# doing the right thing. A test that fails on correct behaviour teaches you to stop
# reading it. What this check actually means is "the seeded history is intact", and
# that is now what it measures.
SEED_ERA_END="2026-07-31"    # everything at or after this is live, not seeded

check_ledger_shape() {
  local day want got
  for pair in 2026-07-29:8 2026-07-30:8 2026-07-31:4 2026-08-01:4 2026-08-02:4; do
    day="${pair%:*}"; want="${pair#*:}"
    got="$(LC_ALL=C awk -F'\t' -v t="$day" -v e="$SEED_ERA_END" \
           '$1 !~ /^#/ && $2 == t && $1 < e' print-ledger.tsv | wc -l | tr -d ' ')"
    if [ "$got" = "$want" ]; then PASS=$((PASS+1)); echo "  ✓ $day has $got seeded rows"
    else FAIL=$((FAIL+1)); echo "  ✗ $day has $got seeded rows, expected $want"; fi
  done
}

# check <expect:allow|refuse> <today> <target> <description>
check() {
  local expect="$1" today="$2" target="$3" desc="$4"
  local out rc
  out="$(GUARD_LEDGER="$SEED" GUARD_TODAY="$today" bash -c \
        '. ./day-guard.sh; guard_one_day "$1" "test" 0' _ "$target" 2>&1)"; rc=$?
  local got="allow"; [ "$rc" -ne 0 ] && got="refuse"
  if [ "$got" = "$expect" ]; then
    PASS=$((PASS+1)); printf '  ✓ %s\n' "$desc"
  else
    FAIL=$((FAIL+1)); printf '  ✗ %s\n     expected %s, got %s:\n%s\n' "$desc" "$expect" "$got" "$out"
  fi
}

echo "Guard A — never print ahead"
reset_ledger
check refuse 2026-08-10 2026-08-11 "tomorrow's sheet, printed today"
check refuse 2026-07-31 2026-08-02 "a sheet two days out"

echo
echo "Guard C — don't reprint paper that already exists"
reset_ledger
check refuse 2026-08-01 2026-08-01 "Aug 1 sheet on Aug 1 — already in the Jul 28 stack"
check refuse 2026-08-02 2026-08-02 "Aug 2 sheet on Aug 2 — same"
check refuse 2026-07-31 2026-07-29 "reprinting Jul 29, which was printed twice already"

echo
echo "A full day is FOUR jobs — all must pass on a day with no paper yet"
reset_ledger
check allow 2026-08-10 2026-08-10 "1/4 word problems"
check allow 2026-08-10 2026-08-10 "2/4 logic"
check allow 2026-08-10 2026-08-10 "3/4 drill kid1"
check allow 2026-08-10 2026-08-10 "4/4 drill kid2"

echo
echo "Guard B — one target day per calendar day"
check refuse 2026-08-10 2026-08-09 "a second, different day after today's set went out"

echo
echo "Next morning, the day just printed is now protected by C"
check refuse 2026-08-11 2026-08-10 "reprint of yesterday's set"
check allow  2026-08-11 2026-08-11 "today's own set still prints"

echo
echo "Override escapes any guard, and says so"
reset_ledger
# Capture first, grep after. Piping straight into `grep -q` made this case flaky:
# grep exits the moment it matches, the writer dies of SIGPIPE (141), and `set -o
# pipefail` at the top of this file promotes that to the pipeline's status — so a
# PASSING case reported as a failure, about 1 run in 3. The guard was fine; the
# harness was lying.
OVR_OUT="$(GUARD_LEDGER="$SEED" GUARD_TODAY=2026-08-01 bash -c \
          '. ./day-guard.sh; guard_one_day 2026-08-01 "replacement" 1' 2>&1)"
if printf '%s' "$OVR_OUT" | grep -q OVERRIDDEN; then
  PASS=$((PASS+1)); echo "  ✓ --override-day-guard prints a loud warning and proceeds"
else
  FAIL=$((FAIL+1)); echo "  ✗ override did not warn; got: $OVR_OUT"
fi

echo
echo "Date parsing"
reset_ledger
for pair in "July 31, 2026:2026-07-31" "August 1, 2026:2026-08-01" "2026-08-02:2026-08-02"; do
  raw="${pair%:*}"; want="${pair#*:}"
  got="$(GUARD_LEDGER="$SEED" bash -c '. ./day-guard.sh; to_iso_day "$1"' _ "$raw")"
  if [ "$got" = "$want" ]; then PASS=$((PASS+1)); echo "  ✓ '$raw' -> $got"
  else FAIL=$((FAIL+1)); echo "  ✗ '$raw' -> $got (wanted $want)"; fi
done

echo
echo "Seeded ledger has the shape the guards expect"
check_ledger_shape

echo
echo "No stray rows dated after today (a future row would refuse a real print)"
# ⚠️ LC_ALL=C is load-bearing. The threshold is today + "T~", and `~` (0x7E) sorts
# after every digit ONLY under C collation. Under the inherited en_US.UTF-8 locale,
# punctuation is weighted below digits, so "2026-08-01T15:08:54" > "2026-08-01T~"
# compares TRUE and every row printed TODAY is reported as future-dated. That fired
# the first time anything was printed after this suite was written (2026-08-01: four
# real jobs flagged as "leftover test residue"). Same string, same awk, different
# answer per locale — pin it.
STRAY_AWK='$1 !~ /^#/ && $1 > d"T~"'
STRAY="$(LC_ALL=C awk -F'\t' -v d="$(date +%F)" "$STRAY_AWK" print-ledger.tsv | wc -l | tr -d ' ')"
if [ "$STRAY" = "0" ]; then PASS=$((PASS+1)); echo "  ✓ none"
else FAIL=$((FAIL+1)); echo "  ✗ $STRAY future-dated row(s) — leftover test residue:"
     LC_ALL=C awk -F'\t' -v d="$(date +%F)" "$STRAY_AWK" print-ledger.tsv | sed 's/^/     /'; fi

echo
echo "The real ledger was not touched by these tests"
if [ "$(shasum print-ledger.tsv | cut -d' ' -f1)" = "$LEDGER_SUM_BEFORE" ]; then
  PASS=$((PASS+1)); echo "  ✓ checksum unchanged"
else
  FAIL=$((FAIL+1)); echo "  ✗ print-ledger.tsv was modified — a test wrote to the real ledger"
fi

echo
echo "──────────────────────────────"
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
