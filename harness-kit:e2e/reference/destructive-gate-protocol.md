# Destructive Action Gate — Two-Phase Dispatch Protocol

**Load this reference when:** an AS-N requires a destructive action (delete / send / charge / revoke / force-push / drop / any irreversible call), or you are debugging a destructive-gate round-trip.

The high-level rule lives in `SKILL.md → Browser Session Strategy → Hard Rule 1`. This document is the wire-protocol detail across the script / subagent / parent boundaries.

## Why Two Phases

The Task tool gives the parent and subagent no mid-execution channel — a subagent runs and returns once. To pause for user confirmation, we have to:

1. Phase 1: Subagent runs the script up to the destructive step, the script exits with a sentinel code, the subagent returns a "paused" report.
2. Parent ↔ user: Parent surfaces the request; user replies with an exact ack token.
3. Phase 2: Parent re-dispatches the subagent with the ack token in the env; the script's gate sees the matching token and proceeds.

The unique `ack_token` per pause is what binds user consent to a specific action — re-using a token from an earlier pause must not let a different action through.

## Script Side

The `_destructive_gate` helper is already in `templates/feature.sh.template`. Every destructive line in the script is preceded by a call to it:

```bash
_destructive_gate "Click 'Yes, permanently delete account'" "<fixture-account-id>"
agent-browser ${AB_FLAGS} click "Yes, permanently delete"
```

Helper behavior (re-stated for clarity):

1. Generate a unique `ack_token` of form `${AS}-<short-action-slug>-${TS}`.
2. Read env var `E2E_DESTRUCTIVE_ACK`.
3. If `E2E_DESTRUCTIVE_ACK == ack_token`: `return 0`, the destructive line that follows runs.
4. Otherwise: emit one stdout line in the form

   ```
   DESTRUCTIVE_GATE: action=<description>; url=<current_url>; resource=<resource>; ack_token=<token>
   ```

   then `exit 75` (`EX_TEMPFAIL` — "I haven't failed, I haven't succeeded, I'm waiting for an external condition"). This exit code is what tells the subagent "this was a planned pause, not a failure".

Token format constraints:
- Must contain only `[A-Za-z0-9-]` (so it survives shell quoting and JSON without escaping).
- Must include the AS-N, an action slug, and the timestamp — uniqueness across pauses is mandatory.
- The helper in the template handles this; do not hand-roll the token format.

## Subagent Side

When the subagent runs the script and observes `exit 75` plus a `DESTRUCTIVE_GATE:` line on stdout:

1. Parse the line into `action`, `target_url`, `target_resource`, `ack_token`.
2. Build the JSON report (see `subagent-protocol.md`) with that scenario set to:
   - `phase: "AWAITING_DESTRUCTIVE_ACK"`
   - `exit_code: null`
   - `destructive_pending: { action, target_url, target_resource, ack_token }`
   - `failing_step: null`
3. Return the report. The subagent's run is over for this dispatch.

The subagent must distinguish exit 75 from any other non-zero exit:
- `exit 0` → success path
- `exit 75` → destructive pause (handle as above)
- any other non-zero → real failure (set `phase: "OUTER_RED"`, populate `failing_step`)

## Parent Side

When the parent receives a report with any `AWAITING_DESTRUCTIVE_ACK` scenario:

### Step 1 — Surface to the user, verbatim

```
E2E for <feature> AS-N reached a destructive step:

  Action:   <action>
  URL:      <target_url>
  Resource: <target_resource>

This will run against your live Chrome session — the change will
be real. To proceed, reply EXACTLY:

  proceed-destructive <ack_token>

Anything else (silence, "yes", "ok", a different token) cancels.
```

### Step 2 — Wait for user reply

Only an exact `proceed-destructive <ack_token>` reply (the token must match byte-for-byte) is accepted as consent.

### Step 3a — On accept: re-dispatch (Phase 2)

Re-dispatch the subagent with the SAME `e2e-subagent` marker and an additional instruction (see `subagent-protocol.md → Dispatch Prompt Template` for the exact wording):

> Re-run only AS-N with `E2E_DESTRUCTIVE_ACK=<token>` exported in the script's environment. Do not run any other AS in this re-dispatch.

The subagent runs the script again with `E2E_DESTRUCTIVE_ACK=<token>` set. The helper sees the matching token, returns 0, the destructive line executes, the script continues to completion (or to the next gate).

### Step 3b — On any other reply: re-dispatch with decline

> User declined the destructive action for AS-N. Mark AS-N as `OUTER_RED` with `failing_step "destructive action <action> — user declined"`. Do not re-run AS-N.

The second-phase report comes back with `OUTER_RED` for that AS — that is the correct final state for a declined destructive scenario. The parent surfaces it to the user as a normal RED.

### Step 4 — Append to `destructive_actions_attempted`

After Step 3a's report comes back, the executed action is in `destructive_actions_attempted` (the subagent fills this in automatically because `E2E_DESTRUCTIVE_ACK` was set). The parent does not need to manually patch the report.

## Multiple Gates in One AS

Multiple destructive gates in a single AS produce multiple round-trips — each gate gets its own `ack_token`, each requires its own user ack. The user agreed to delete an account; that does not transitively authorize deleting their org five steps later. This is intentional.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Parent reports `auto_connect_used: false` after re-dispatch | Subagent regenerated env without `${AB_FLAGS}` | Re-dispatch with explicit reminder; check the script template wasn't customised away from `${AB_FLAGS}` |
| User echoes the right action description but a wrong token | Parent prompt didn't include the `ack_token` clearly | Re-prompt with the token in a code block / on its own line |
| `exit 75` but no `DESTRUCTIVE_GATE:` line on stdout | Script bug — gate emitted but parser ate it | Run the script manually, inspect stdout |
| Token doesn't match on Phase 2 | Timestamp `TS` regenerated on second run, so token differs | Pass `E2E_TS=<original>` env var alongside `E2E_DESTRUCTIVE_ACK`, or update the helper to read `TS` from env when present |

The last row deserves attention — `TS="$(date -u +...)"` in the script regenerates per run. The helper in the current template includes `${TS}` in the token, so re-running creates a *different* token. To make Phase 2 work robustly, the parent's re-dispatch instruction should include both env vars:

```bash
E2E_DESTRUCTIVE_ACK=<token> E2E_TS_OVERRIDE=<original-ts> ./tests/e2e/<feature>.sh AS-N
```

…and the template's `TS=...` line becomes:

```bash
TS="${E2E_TS_OVERRIDE:-$(date -u +%Y%m%dT%H%M%SZ)}"
```

This ensures the re-dispatch generates the same `ack_token` and the gate can match. (This refinement is reflected in the latest `templates/feature.sh.template`. If you copied an older version of the template, patch this line.)
