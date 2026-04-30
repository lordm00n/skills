# E2E Anti-Patterns

**Load this reference when:** writing or changing a `tests/e2e/<feature>.sh` script, debugging an e2e failure, or tempted to "make the e2e green faster" by softening it.

## Overview

E2E tests verify what the user actually experiences, end-to-end, with real browser/desktop interaction. The moment they verify anything else — a mock, a sleep, a hand-picked CSS path — they stop being e2e and start being theatre.

**Core principle:** If the test could pass while the real user experience was broken, it is not a real e2e.

**Following the Iron Law of `harness-kit:e2e-testing` prevents most of these. The rest are about not weakening the script under pressure.**

## The Iron Laws

```
1. NEVER wait with sleep — wait on the actual UI signal
2. NEVER bypass the accessibility tree — no CSS, no xpath, no pixels
3. NEVER mock the network in an e2e — that's a different test
4. NEVER assert only the happy path — error states are part of the AS
5. NEVER drop --auto-connect — every agent-browser call uses ${AB_FLAGS}
6. NEVER perform a destructive action without the confirmation gate
7. NEVER read credentials from vault / password manager / cookie store
```

## Anti-Pattern 1: `sleep` as a Wait Strategy

**The violation:**

```bash
# ❌ BAD: sleep until you "think" the page is ready
agent-browser navigate https://app.local/login
sleep 3
agent-browser click "@e5"   # the submit button, hopefully
```

**Why this is wrong:**
- Flaky on slow days, slow in CI, false-green on fast days
- Hides real loading bugs (slow API → test still passes after 3s)
- Couples the test to performance instead of correctness

**The fix:**

```bash
# ✅ GOOD: wait on the actual UI signal
agent-browser navigate https://app.local/login
agent-browser wait-for-element "Submit"   # exact API: load via skills get core
agent-browser click "Submit"
```

If the framework primitive can't find the element after a reasonable timeout, **that is the bug**. Surface it instead of papering over it.

### Gate Function

```
BEFORE writing `sleep N`:
  Ask: "What UI signal am I actually waiting for?"
  Use the wait-for-* primitive that matches that signal.
  If no such primitive exists, re-load `agent-browser skills get core` —
  you probably missed it.
```

## Anti-Pattern 2: CSS / xpath / Pixel Fallbacks

**The violation:**

```bash
# ❌ BAD: bypass the a11y tree because "it was easier"
agent-browser click-css "div.btn-primary:nth-of-type(2)"
agent-browser click-xy 412 287
```

**Why this is wrong:**
- Brittle: any CSS refactor breaks the test for reasons unrelated to behavior
- A real user can't "click pixel 412,287" — they click a labelled control
- If a11y can't find it, the **UI has an accessibility bug**. The test caught a real issue. Fix the UI.
- Defeats the entire reason agent-browser uses the accessibility tree

**The fix:**

```bash
# ✅ GOOD: locate by accessible name / role / @eN reference
agent-browser click "Save changes"   # accessible name from the a11y snapshot
```

If the element has no accessible name, add one. That's a product fix, not a test workaround.

### Gate Function

```
BEFORE adding click-css / click-xy / xpath / nth-of-type:
  STOP.
  1. Take an a11y snapshot.
  2. Can you find the element by role + accessible name?
  3. If yes: use that.
  4. If no: file the missing-label as a bug, fix it, then write the test.
  Never weaken the locator strategy because the UI is poorly labelled.
```

## Anti-Pattern 3: Mocking the Network in E2E

**The violation:**

```bash
# ❌ BAD: intercept /api/login so the e2e doesn't need a backend
agent-browser intercept "POST /api/login" --respond '{"ok":true,"token":"x"}'
agent-browser click "Sign in"
agent-browser assert-url-contains "/dashboard"
```

**Why this is wrong:**
- You no longer test what the user experiences — you test the frontend's behavior given a hand-crafted response
- The backend contract drifts and the test stays green
- That's a **component test**, not an e2e. It belongs in unit TDD.

**The fix:**

```bash
# ✅ GOOD: hit the real backend; if the backend is unavailable, see
# Connection Failure Protocol — STOP and ask the user to start it.
agent-browser type "@email-input" "fixture-user@example.com"
agent-browser type "@password-input" "<from fixture vault>"
agent-browser click "Sign in"
agent-browser wait-for-url-contains "/dashboard"
```

If you genuinely need to test "what does the UI do when the API returns 500" — that scenario belongs in the spec as `AS-N`, and is driven by a **server-side fixture / test mode**, not by intercepting requests in the browser. The realism boundary stays at the browser.

### Gate Function

```
BEFORE adding any network interception in an e2e:
  Ask: "Am I testing the UI given a hypothetical response?"
  IF yes:
    STOP — that's a component test, write it in the unit TDD layer.
  Use real backend (or a server-side fixture) for e2e.
```

## Anti-Pattern 4: Happy-Path-Only Scenarios

**The violation:**

```bash
case "${AS}" in
  AS-1)
    # ❌ BAD: only the success path
    agent-browser type "@email" "user@example.com"
    agent-browser type "@password" "correct"
    agent-browser click "Sign in"
    agent-browser wait-for-url-contains "/dashboard"
    ;;
esac
```

**Why this is wrong:**
- The spec's `AS-1` almost certainly says "and on bad credentials, show an inline error" — happy-only ignores half the scenario
- Bugs in error paths ship silently
- Gives a false sense of coverage

**The fix:**

```bash
case "${AS}" in
  AS-1)  # successful login
    # ... happy path ...
    ;;
  AS-2)  # invalid credentials → inline error
    agent-browser type "@email" "user@example.com"
    agent-browser type "@password" "wrong"
    agent-browser click "Sign in"
    agent-browser wait-for-text "Invalid email or password"
    agent-browser assert-url-contains "/login"   # did NOT navigate away
    ;;
esac
```

Each error/edge state from the spec gets its own `AS-N`.

### Gate Function

```
BEFORE marking AS-N done:
  Re-read the AS in the spec.
  List every observable outcome it describes (success AND failure modes).
  Are all of them asserted?
  IF not: split into multiple AS-N or extend the script branch.
```

## Anti-Pattern 5: Skipping `--auto-connect`

**The violation:**

```bash
# ❌ BAD: just call agent-browser, let it spawn whatever
agent-browser navigate https://app.local
agent-browser click "Sign in"
```

**Why this is wrong:**
- A fresh Chrome is launched — empty cookies, empty logged-in state
- The AS executes against a *different state* than what the user sees in their own browser
- The whole point of this skill's `--auto-connect` design (Q14: B) was to share the user's real Chrome state — bypassing it negates the design
- The subagent's report `auto_connect_used` will be `false`, and the parent agent rejects the report

**The fix:**

```bash
# ✅ GOOD: every call uses ${AB_FLAGS}
AB_FLAGS="--auto-connect"   # already in the skeleton
agent-browser ${AB_FLAGS} navigate https://app.local
agent-browser ${AB_FLAGS} click "Sign in"
```

If a subcommand fails *because* of `--auto-connect`, that is a real bug — re-load `agent-browser skills get core` to find the current flag name (it may have been renamed in a newer agent-browser release). Do NOT drop the flag as a workaround.

### Gate Function

```
BEFORE writing any agent-browser invocation:
  Does it include ${AB_FLAGS}?
  IF no: STOP. Prefix with ${AB_FLAGS}.
BEFORE the subagent returns its JSON report:
  auto_connect_used MUST be true.
  IF false: the subagent has a bug — fix the script before reporting.
```

## Anti-Pattern 6: "Run Everything" Mode

**The violation:**

```bash
# ❌ BAD: invent a "run all" mode in the script
./tests/e2e/login.sh                    # no AS, runs every case
./tests/e2e/login.sh --all
./tests/e2e/login.sh AS-1 AS-2 AS-3
```

**Why this is wrong:**
- Mixes failure attribution: which AS failed in a multi-AS run?
- Iterating all `AS-N` is `harness-kit:finishing-a-development-branch`'s job — it knows the spec list, the script does not
- Encourages skipping individual scenario verification during development

**The fix:**

```bash
# ✅ GOOD: exactly one AS per invocation
./tests/e2e/login.sh AS-1
```

The `case` statement only accepts one `AS-N`. The `*)` branch exits with code 64 ("usage error"). No `--all` flag, no positional list, no default-run-everything.

### Gate Function

```
BEFORE adding any "run multiple" affordance to the script:
  STOP.
  Iteration belongs in the orchestrator (finishing-a-development-branch),
  not the script. Keep the script single-AS.
```

## Anti-Pattern 7: Asserting Just That a Page "Loaded"

**The violation:**

```bash
# ❌ BAD: assert the page rendered, call it tested
agent-browser navigate /dashboard
agent-browser wait-for-element "Dashboard"
# done.
```

**Why this is wrong:**
- The spec said something specific should happen on `/dashboard` — show the user's name, list their orgs, etc.
- "Page rendered" is the lowest possible bar; passes even when the page is empty / showing an error banner / showing the wrong user

**The fix:**

```bash
agent-browser navigate /dashboard
agent-browser wait-for-text "Welcome, ${FIXTURE_USER_NAME}"
agent-browser wait-for-element "Recent activity"
agent-browser assert-text-not-present "Something went wrong"
```

Assert the **specific observable promise** the spec made for that scenario.

### Gate Function

```
BEFORE writing only an "element exists" assertion:
  Ask: "What did the spec promise the user would see / be able to do?"
  Assert that, not the lowest-bar 'something rendered'.
```

## Anti-Pattern 8: Catching Errors to Keep the Script Green

**The violation:**

```bash
# ❌ BAD: swallow agent-browser failures
agent-browser click "Save" || true
agent-browser wait-for-text "Saved" || echo "warn: not saved, continuing"
```

**Why this is wrong:**
- The script will exit 0 even when the scenario didn't happen
- `harness-kit:verification-before-completion` accepts that exit 0 as proof — silent false positive
- Defeats the entire point of having an exit code at all

**The fix:**

```bash
set -euo pipefail   # already in the skeleton — never weaken it
agent-browser click "Save"
agent-browser wait-for-text "Saved"
```

Let failures propagate. If a step is genuinely optional (e.g. "dismiss tutorial popup if present"), use a guarded check that branches on element presence — but never swallow a failure on an asserted step.

### Gate Function

```
BEFORE adding `|| true`, `2>/dev/null`, `set +e`, or wrapping in a
trap that exits 0:
  STOP.
  Either: the step is truly optional → use an explicit if-element-present check.
  Or: you're hiding a real failure → fix the production code or the script.
  Never weaken set -euo pipefail.
```

## Anti-Pattern 9: Destructive Action Without the Two-Phase Gate

**The violation:**

```bash
# ❌ BAD: AS-4 involves account deletion, scenario just clicks through
case "${AS}" in
  AS-4)  # user deletes their own account
    agent-browser ${AB_FLAGS} click "Settings"
    agent-browser ${AB_FLAGS} click "Delete account"
    agent-browser ${AB_FLAGS} click "Yes, permanently delete"   # KABOOM
    ;;
esac
```

**Why this is wrong:**
- Because of `--auto-connect`, the agent is acting against the **user's real Chrome** — and therefore real accounts, real APIs, real data
- "It's just a test" is exactly the famous-last-words mindset that destroys data
- The user opted into shared-Chrome state; the destructive-action gate is the price they pay back for keeping it safe

**The fix:**

Use the `_destructive_gate` helper from the skill's **Browser Session Strategy → Hard Rule 1** section. The helper, when invoked without `E2E_DESTRUCTIVE_ACK` set, emits a `DESTRUCTIVE_GATE:` marker line and exits 75 (EX_TEMPFAIL). The subagent translates that into an `AWAITING_DESTRUCTIVE_ACK` JSON report; the parent surfaces the request to the user; on `proceed-destructive <token>` the parent re-dispatches with the env var set; the second pass of the helper sees the token and proceeds.

```bash
# ✅ GOOD: every destructive call is preceded by _destructive_gate
case "${AS}" in
  AS-4)
    agent-browser ${AB_FLAGS} click "Settings"
    agent-browser ${AB_FLAGS} click "Delete account"

    _destructive_gate \
      "Click 'Yes, permanently delete account'" \
      "<fixture-account-id>"

    agent-browser ${AB_FLAGS} click "Yes, permanently delete"
    ;;
esac
```

Two-phase walk-through:

| Phase | What happens |
|---|---|
| 1st dispatch | Script runs to `_destructive_gate`, emits the marker, exits 75. Subagent reports `AWAITING_DESTRUCTIVE_ACK` with `ack_token`. |
| Parent ↔ user | Parent surfaces the action / URL / resource and asks for `proceed-destructive <token>`. |
| 2nd dispatch | Parent re-dispatches with `E2E_DESTRUCTIVE_ACK=<token>` exported. Helper sees the matching token, returns 0, the destructive click executes. |
| Final report | Subagent appends the executed action to `destructive_actions_attempted`. |

Multiple gates in one AS = multiple round-trips. Each gets a unique token. That's intentional — the user agreed to delete an account, not "everything from here on".

**Why exit 75 specifically:** `EX_TEMPFAIL` is the conventional Unix code for "I haven't failed, I haven't succeeded, I'm waiting for an external condition". It distinguishes a real test failure (any non-75 non-zero) from a destructive pause.

### Gate Function

```
BEFORE writing any click / submit / API call that, on the user's real
account, would delete / send / charge / revoke / force-push / drop:
  1. Is this AS specifically about the destructive flow?
     IF no: redesign the AS to avoid the destructive call.
     IF yes: continue.
  2. Call `_destructive_gate "<description>" "<resource>"` immediately
     before the destructive line. Never inline-emit the marker by
     hand — use the helper.
  3. Confirm the helper definition exists at the top of the script
     (it should be in the skeleton; if missing, copy it from
     SKILL.md → Hard Rule 1).
  4. The subagent prompt template MUST tell the subagent to:
     - Treat exit 75 as AWAITING_DESTRUCTIVE_ACK, not as failure.
     - Parse the DESTRUCTIVE_GATE line into the JSON `destructive_pending` field.
     - Re-run only the affected AS on second dispatch with E2E_DESTRUCTIVE_ACK set.
  5. After acked execution, append the action to
     destructive_actions_attempted in the final report.

NEVER skip the gate "because the test target is obviously the test
account" — `--auto-connect` means you cannot prove that.
NEVER hand-roll the marker emission — drift from the parser format
will silently cause the parent to reject the report.
```

## Anti-Pattern 10: Reading Credentials From Storage

**The violation:**

```bash
# ❌ BAD: pull the token out of the auth vault to inject as a header
TOKEN=$(agent-browser vault get my-token --raw)
agent-browser ${AB_FLAGS} navigate "https://api.local/?token=${TOKEN}"

# ❌ BAD: scrape the cookie out of the running Chrome
COOKIE=$(agent-browser ${AB_FLAGS} cookies get session)
echo "${COOKIE}"
```

**Why this is wrong:**
- The user typed / pasted the credential into Chrome themselves; the running browser already has it. Reading it out is unnecessary
- Once the credential is in the script's variables, it can leak via `set -x`, evidence files, error traces, accidental `echo`
- Long-term security posture: the agent should never be the path of credential exfiltration, even by accident
- This rule applies to the Chrome password manager, the OS keyring, agent-browser's vault, and any cookie store — same risk, same answer

**The fix:**

```bash
# ✅ GOOD: just navigate; the running Chrome handles auth itself
agent-browser ${AB_FLAGS} navigate https://app.local/dashboard
agent-browser ${AB_FLAGS} wait-for-text "Welcome back"
```

If the AS legitimately requires fresh credentials (e.g. "user logs in with new password"), have the **user** type them into Chrome — the script can drive the form fields, but the values come from a runtime prompt the user answers, never from a stored credential the agent reads.

### Gate Function

```
BEFORE adding any of the following:
  - vault read / get
  - keychain / keyring access
  - cookie read / extract
  - password manager API calls
  - reading any *.cookies, *.json with stored secrets

  STOP.
  Question: does the running Chrome already have what you need?
    Almost always: YES.
  Question: if a fresh credential is genuinely required, can the user
            type it into the page directly?
    Almost always: YES.
  Reading from storage is virtually never the right answer.
```

## When the Script Becomes Too Complex

**Warning signs:**
- One `case` branch is longer than ~80 lines
- Heavy duplication of setup blocks across `AS-N` branches
- You start wanting helper functions

**Consider:**
- Extract setup into a `_setup_<feature>` shell function at the top of the same file (still one file per feature — don't split across files)
- If duplication crosses features, that's a hint the spec lumped two features together — talk to `harness-kit:brainstorm`

**What NOT to do:**
- Add a test framework (Playwright, Vitest, etc.) — Q2 was decided: shell scripts only
- Spawn a sibling `helpers.sh` and source it — keep the feature self-contained for grep-ability

## Quick Reference

| Anti-Pattern | Fix |
|---|---|
| `sleep` as wait | Use `wait-for-*` primitive from `agent-browser skills get core` |
| CSS / xpath / pixel | Locate via a11y; fix the UI's labels if needed |
| Network mocking in e2e | Move to unit TDD; use real backend or server-side fixture for e2e |
| Happy-path only | Add an `AS-N` per spec'd error / edge state |
| Skipping `--auto-connect` | Use `${AB_FLAGS}` on every `agent-browser` call |
| "Run all" mode | Single AS per invocation; iteration belongs to finishing skill |
| "Page loaded" only | Assert the specific observable promise from the spec |
| Swallowed failures | Keep `set -euo pipefail`; let failures propagate |
| Destructive without gate | Add `DESTRUCTIVE_GATE` marker; wait for `proceed-destructive` |
| Reading stored credentials | Don't. The running Chrome already has them, or the user can type them |

## Red Flags

- `sleep` anywhere in the script
- `click-css`, `click-xy`, `xpath`, `nth-of-type`, `nth-child`
- `intercept`, `mock-response`, `--mock`
- A single `AS-N` branch with no failure-mode counterpart in the file
- An `agent-browser` call without `${AB_FLAGS}`
- `|| true`, `set +e`, `2>/dev/null` on an assertion line
- `--all`, `--every`, default-no-arg run-everything
- Any `agent-browser` flag you didn't read in this session via `skills get core`
- `vault get`, `keychain`, `cookies get`, `password-manager`, or any credential read
- A delete / send / charge / revoke / drop / force-push call without a `DESTRUCTIVE_GATE` marker line right above it

## The Bottom Line

**E2E is the contract with the user. Don't soften it.**

If you're tempted to make the script "less strict" so it goes green, you are about to ship a bug with a green check next to it. Stop, restore the strictness, fix the production code instead.
