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
#
# Reprinting a PAST day is allowed and unguarded: a kid losing Wednesday's sheet
# is still only one day's worth of paper.
#
# Escape hatch: --override-day-guard. Verbose on purpose. It prints a loud
# warning and records the override in the ledger, so it can never happen quietly.

# The ledger. Machine-local print history, one line per job actually sent:
#   <printed_at ISO8601>  <target_day YYYY-MM-DD>  <label>
# CUPS is the authoritative record of what came out of the printer; this file
# only exists to answer "which day have I already printed for today?".
GUARD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEDGER="$GUARD_DIR/.print-ledger.tsv"

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
  local today; today="$(date +%F)"

  # ISO dates compare correctly as strings, which is the whole point of ISO.
  local violation=""
  if [ "$target" \> "$today" ]; then
    violation="AHEAD: this sheet is dated $target, which is in the future (today is $today)."
  else
    # Which target days have already been printed today?
    local prior=""
    if [ -f "$LEDGER" ]; then
      prior="$(awk -F'\t' -v d="$today" -v t="$target" '$1 ~ "^"d && $2 != "" && $2 != t {print $2}' "$LEDGER" | sort -u | tr '\n' ' ')"
    fi
    if [ -n "$prior" ]; then
      violation="SECOND DAY: you already printed for ${prior% } today. This sheet is for $target."
    fi
  fi

  if [ -n "$violation" ]; then
    if [ "$override" = "1" ]; then
      echo "⚠️  DAY GUARD OVERRIDDEN — $violation" >&2
      echo "⚠️  Printing anyway because --override-day-guard was passed. Recording it." >&2
      printf '%s\t%s\t%s\n' "$(date +%FT%T)" "$target" "OVERRIDE $label" >> "$LEDGER"
      return 0
    fi
    cat >&2 <<EOF

✋ REFUSED — one day's worth of paper at a time.

   $violation

   Asif's standing rule: one day at a time, never a batch, never ahead.
   A full day is word problems + logic + drills — all for the SAME day.

   If today's set is already on paper, the morning job is FIND THE STACK,
   not print. If you genuinely need this, re-run with --override-day-guard.

EOF
    exit 2
  fi

  printf '%s\t%s\t%s\n' "$(date +%FT%T)" "$target" "$label" >> "$LEDGER"
  return 0
}
