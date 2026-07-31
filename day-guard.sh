#!/usr/bin/env bash
# day-guard.sh — ONE DAY'S WORTH OF PAPER AT A TIME. Sourced, not run.
#
# Why this exists (2026-07-31, Asif): on 2026-07-28 a single session printed all
# of Block 1 in one go — 20 jobs, 10 days of sheets. Asif's standing instruction:
#
#   "I'll only ask you for one day at a time. I will never ask you for more.
#    Make sure you don't print out more than one day worth at a time."
#
# The rule was already written in AGENTS.md at the time. Prose didn't hold it —
# the same rule had already decayed twice by living only in a doc. So it lives
# here, in the code path that actually reaches `lp`.
#
# Two guards, both refusing BEFORE anything is sent to the printer:
#
#   A. NEVER PRINT AHEAD. A sheet dated later than today is refused. That is
#      precisely what the bulk run did.
#   B. ONE TARGET DAY PER CALENDAR DAY. Once you've printed for July 31 today,
#      printing for August 1 today is refused. A full day is word + logic +
#      drills, so this allows several files — as long as they're all the same day.
#   C. THIS DAY'S PAPER ALREADY EXISTS. If the ledger already has a print for
#      the target day, refuse — the morning job is FIND THE STACK, not print.
#
# Guard C was added 2026-07-31, same day as A and B, because A and B alone would
# NOT have stopped the two duplicate mornings they were written in response to.
# Jul 29 and Jul 30 each reprinted a day that was already in the stack, on that
# day, one day at a time — clean under A and clean under B. Asif spotted the hole
# immediately ("we already printed aug 1 and aug 2 i guess"): the Jul 28 bulk run
# put paper on the shelf through Aug 2, so Aug 1 and Aug 2 mornings were lined up
# to repeat it exactly. "One day at a time" and "don't print what already exists"
# are two different rules and both are needed.
#
# Escape hatch: --override-day-guard. Verbose on purpose. It prints a loud
# warning and records the override in the ledger, so it can never happen quietly.
# A genuine reprint — a kid lost Wednesday's sheet — goes through it, and should:
# that is a deliberate act, not a default.

# The ledger. TRACKED IN GIT (see the header inside it). One line per job sent:
#   <printed_at ISO8601>  <target_day YYYY-MM-DD>  <label>
# CUPS is the authoritative record of what physically came out of the printer;
# this file answers the two questions CUPS can't: which DAY was a job for, and
# does paper for that day already exist.
GUARD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# GUARD_LEDGER lets test-day-guard.sh point at a throwaway copy. Without that seam
# the tests append real-looking rows to the real ledger, and a ledger that claims
# paper exists when it doesn't is worse than no guard at all.
LEDGER="${GUARD_LEDGER:-$GUARD_DIR/print-ledger.tsv}"

# to_iso_day "July 31, 2026" -> 2026-07-31 ; "" -> today
# Accepts the same human format `print-worksheet.sh --date` takes, plus ISO and
# the literal "today". Echoes nothing and returns 1 if it can't parse.
to_iso_day() {
  local raw="$1"
  if [ -z "$raw" ] || [ "$raw" = "today" ]; then
    date +%F
    return 0
  fi
  python3 - "$raw" <<'PY' 2>/dev/null
import sys, datetime
raw = sys.argv[1].strip()
for fmt in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%B %d %Y"):
    try:
        print(datetime.datetime.strptime(raw, fmt).date().isoformat())
        break
    except ValueError:
        continue
else:
    sys.exit(1)
PY
}

# guard_one_day <target_iso_day> <label> <override:0|1>
# Returns 0 to proceed. Exits 2 on a refusal — the caller must not print.
guard_one_day() {
  local target="$1" label="$2" override="${3:-0}"
  # GUARD_TODAY exists so the guards can be tested against a future date without
  # waiting for it (proving the Aug 1 case on Jul 31 is the whole point). It is
  # never set in normal use — leave it unset and this is just `date +%F`.
  local today; today="${GUARD_TODAY:-$(date +%F)}"

  # ISO dates compare correctly as strings, which is the whole point of ISO.
  local violation="" hint=""
  if [ "$target" \> "$today" ]; then
    violation="AHEAD: this sheet is dated $target, which is in the future (today is $today)."
    hint="Print it on the day, not before."
  else
    # Guard C — is there already paper for this day, printed on some EARLIER day?
    # Checked before B because "it's already printed" is the more useful thing to
    # be told. The `printed_at` day must differ from today: rows printed TODAY are
    # this morning's own run, and a full day is four jobs (word + logic + 2 drills)
    # — refusing file #2 of today's set would break the very thing being protected.
    # The stack scenario is always paper printed on an earlier date, which is
    # exactly what this matches.
    local existing="" when=""
    if [ -f "$LEDGER" ]; then
      existing="$(awk -F'\t' -v t="$target" -v d="$today" '$1 !~ /^#/ && $2 == t && $1 !~ "^"d' "$LEDGER" | wc -l | tr -d ' ')"
      when="$(awk -F'\t' -v t="$target" -v d="$today" '$1 !~ /^#/ && $2 == t && $1 !~ "^"d {print $1}' "$LEDGER" | sort | tail -1 | cut -dT -f1)"
    fi
    if [ -n "$existing" ] && [ "$existing" != "0" ]; then
      violation="ALREADY ON PAPER: $existing job(s) for $target were printed (most recently $when)."
      hint="Go look in the stack for the sheet stamped for $target before printing another."
    else
      # Guard B — which OTHER target days have already been printed today?
      local prior=""
      prior="$(awk -F'\t' -v d="$today" -v t="$target" '$1 !~ /^#/ && $1 ~ "^"d && $2 != "" && $2 != t {print $2}' "$LEDGER" 2>/dev/null | sort -u | tr '\n' ' ')"
      if [ -n "$prior" ]; then
        violation="SECOND DAY: you already printed for ${prior% } today. This sheet is for $target."
        hint="One day's worth per day. Come back tomorrow."
      fi
    fi
  fi

  if [ -n "$violation" ]; then
    if [ "$override" = "1" ]; then
      echo "⚠️  DAY GUARD OVERRIDDEN — $violation" >&2
      echo "⚠️  Printing anyway because --override-day-guard was passed. Recording it." >&2
      printf '%s\t%s\t%s\n' "${today}T$(date +%T)" "$target" "OVERRIDE $label" >> "$LEDGER"
      return 0
    fi
    cat >&2 <<EOF

✋ REFUSED — one day's worth of paper at a time.

   $violation

   $hint

   Asif's standing rule: one day at a time, never a batch, never ahead,
   and never a second copy of paper that already exists.
   A full day is word problems + logic + drills — all for the SAME day.

   If this really is a replacement (lost or ruined sheet), that's what the
   escape hatch is for: re-run with --override-day-guard.

EOF
    exit 2
  fi

  # Day part comes from $today (not `date`) so it stays consistent with the day the
  # guards just reasoned about — otherwise a GUARD_TODAY test records rows that look
  # like they were printed on a different day and the harness fails itself.
  printf '%s\t%s\t%s\n' "${today}T$(date +%T)" "$target" "$label" >> "$LEDGER"
  return 0
}
