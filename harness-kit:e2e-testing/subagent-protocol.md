# Subagent Dispatch & Report Protocol

**Load this reference when:** you (parent agent) are about to dispatch the e2e subagent, you (subagent) are about to return your report, or you need to interpret a returned report.

This document is the wire-protocol detail. The behavior rules ("must run in subagent", "marker self-check") live in `SKILL.md → Subagent Execution`.

## Dispatch Prompt Template

The parent agent fills in the placeholders and passes the result as the Task tool's `prompt`. Keep the literal `e2e-subagent` marker on the first line so the subagent's self-check passes.

```
e2e-subagent task for feature `<feature>`.

Read this skill in full, then execute the Outside-In Cycle for the
listed scenarios:
  - Skill: /Users/<you>/.agents/skills/harness-kit:e2e-testing/SKILL.md
  - Spec (## E2E Strategy section): docs/harness-kit/specs/<spec>.md
  - Scenarios to run: AS-1, AS-3
  - Feature: <feature>

When complete, return ONLY a JSON block matching the Subagent Report
Format documented in subagent-protocol.md. Do not include any prose
outside the JSON block. Do not write or modify any file outside
tests/e2e/.
```

For the **second phase** of a destructive-action round-trip, append:

```
This is the destructive re-dispatch for AS-N. Export
E2E_DESTRUCTIVE_ACK=<token> in the script's environment before
running. Do not run any other AS in this re-dispatch.
```

For a **declined** destructive action, append instead:

```
User declined the destructive action for AS-N. Mark AS-N as
OUTER_RED with failing_step "destructive action <action> — user
declined". Do not re-run AS-N.
```

## Subagent Report Format

The subagent returns a single JSON block, nothing else:

```json
{
  "feature": "<feature>",
  "scenarios": [
    {
      "as": "AS-1",
      "exit_code": 0,
      "evidence_dir": "tests/e2e/.evidence/<feature>/<timestamp>-AS-1",
      "phase": "OUTER_GREEN",
      "failing_step": null,
      "destructive_pending": null
    },
    {
      "as": "AS-3",
      "exit_code": 1,
      "evidence_dir": "tests/e2e/.evidence/<feature>/<timestamp>-AS-3",
      "phase": "OUTER_RED",
      "failing_step": "wait-for-text \"Welcome, Alice\" timed out after 5s",
      "destructive_pending": null
    },
    {
      "as": "AS-4",
      "exit_code": null,
      "evidence_dir": "tests/e2e/.evidence/<feature>/<timestamp>-AS-4-pre",
      "phase": "AWAITING_DESTRUCTIVE_ACK",
      "failing_step": null,
      "destructive_pending": {
        "action": "Click 'Yes, permanently delete account'",
        "target_url": "https://app.local/settings/account",
        "target_resource": "<account-id-or-fixture-record>",
        "ack_token": "AS-4-delete-account-2026-04-29T12:34:56Z"
      }
    }
  ],
  "auto_connect_used": true,
  "destructive_actions_attempted": [],
  "notes": "<freeform, ≤3 sentences, only if something the parent must know>"
}
```

## Field Rules

- `phase` ∈ `OUTER_RED`, `INNER_LOOP`, `OUTER_GREEN`, `REFACTOR`, `AWAITING_DESTRUCTIVE_ACK`.
- `exit_code` is `null` only when `phase == AWAITING_DESTRUCTIVE_ACK` (the script paused before completion); otherwise it must be the script's actual exit code.
- `failing_step` is `null` when `exit_code == 0` or when phase is `AWAITING_DESTRUCTIVE_ACK`; otherwise a single short line copied from the script's last assertion message.
- `destructive_pending` is `null` unless `phase == AWAITING_DESTRUCTIVE_ACK`. When present, all four sub-fields are required (`action`, `target_url`, `target_resource`, `ack_token`).
- `auto_connect_used` MUST be `true`. If it is `false`, the subagent has violated the `--auto-connect` rule and the parent should reject the report and re-dispatch with an explicit reminder.
- `destructive_actions_attempted` lists every destructive action the script actually executed in this run (i.e. any action that previously caused an `AWAITING_DESTRUCTIVE_ACK` pause and was subsequently acked and run). Empty array is the normal case for non-destructive features.
- `notes` is for short out-of-band signals only (e.g. `"user attached to default Chrome profile"`, `"connection failure Mode A — Chrome was not running"`). Not for general logs.

## Parent's Handling Rules

| Returned phase | Parent does |
|---|---|
| All `OUTER_GREEN` | Pass report to `harness-kit:verification-before-completion`; mark plan task done |
| Any `OUTER_RED` | Surface `failing_step` to user; treat as inner-loop signal (probably a real bug to fix) |
| Any `AWAITING_DESTRUCTIVE_ACK` | Follow `destructive-gate-protocol.md` — surface to user, get ack, re-dispatch |
| `auto_connect_used: false` | Reject the report; re-dispatch with explicit reminder to use `${AB_FLAGS}` |
| `notes` mentions connection failure | Stop the run; surface the appropriate Mode A / Mode B message from `SKILL.md → Connection Failure Protocol` |

The parent never reads evidence directories itself — the JSON is the contract. If something the parent needs is not in the JSON, the JSON schema is the bug.
