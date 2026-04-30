---
name: harness-kit:finishing-a-development-branch
description: Use when implementation is complete and all tests pass — verifies tests + e2e, sanity-checks the e2e evidence is still gitignored, then reports completion with a suggested commit command. Does NOT merge, push, open PRs, delete branches, remove worktrees, or delete files; those are the user's call.
---

# Finishing a Development Branch

## Overview

Verify the work is actually done (tests + e2e), make sure no e2e artifacts will accidentally enter git, then **report completion and stop**. The branch is left exactly as-is — no merge, no push, no PR, no branch deletion, no worktree removal. Whatever happens next (commit any pending diff, merge, open a PR, discard, or just leave the branch there) is the user's call to drive — usually in plain chat right after this skill ends.

**Core principle:** Verify → Sanity-check → Report → Stop.

**Why minimalist:** branch finishing is the highest-stakes moment in the cycle. Any auto-action here (merge commit, force-push, branch -D, worktree remove) strips the user's last chance to inspect the diff, pick a merge style, wait for CI, or change their mind. Listing a "menu of options" also creates pressure to pick one *now*, when the realistic answer is often "I'll think about it". Defaulting to keep-as-is + reporting is the safest, least surprising behavior.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before reporting completion, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**

```text
Tests failing (<N> failures). Cannot report completion:

[Show failures]

Fix the failures (or revert) before re-invoking this skill.
```

Stop. Don't proceed to Step 1.5.

**If tests pass:** Continue to Step 1.5.

### Step 1.5: Verify E2E (when spec defines AS-N)

Read the feature spec's `## E2E Strategy` section.

**If section is `EXEMPT: <reason>`:** skip to Step 2.

**If section lists `AS-N` scenarios:** for each `AS-N`, dispatch the e2e subagent per `harness-kit:e2e-testing`:

```text
Task tool, subagent_type=shell, prompt contains:
  - literal marker: e2e-subagent
  - skill path:     ~/.agents/skills/harness-kit:e2e-testing/SKILL.md
  - feature:        <feature>
  - scenario:       AS-<M>
```

For each returned JSON report, accept only when:

- `phase: "OUTER_GREEN"`
- `exit_code: 0`
- `auto_connect_used: true`
- `evidence_dir` is set and the directory exists

`AWAITING_DESTRUCTIVE_ACK` triggers the two-phase flow in `harness-kit:e2e-testing/destructive-gate-protocol.md` — complete it before continuing.

**If any AS-N fails:**

```text
E2E failing for AS-<M> (<failing_step>). Cannot report completion:

[Show failing_step + evidence_dir]

Fix the inner loop (per harness-kit:test-driven-development) until
every AS-N in spec returns OUTER_GREEN, then re-invoke this skill.
```

Stop. Do not proceed to Step 2.

**If all AS-N pass:** continue to Step 2.

### Step 2: Sanity-Check E2E Evidence Is Gitignored (when spec was not EXEMPT)

If the spec is `EXEMPT`: skip this step.

Otherwise check that `tests/e2e/.evidence/` is still covered by an active `.gitignore` rule. The original gate for this lives in `harness-kit:e2e-testing` First-Run Setup, but the `.gitignore` may have been edited mid-development, the project structure may have changed, or evidence may have been written to a different location than expected. A late sanity-check costs ~one read and prevents binary artifacts from silently sneaking into the user's next commit.

```bash
# Are any evidence paths currently tracked or unignored?
git check-ignore -v tests/e2e/.evidence/ 2>/dev/null
git ls-files --error-unmatch tests/e2e/.evidence/ 2>/dev/null
```

**If `tests/e2e/.evidence/` is properly ignored AND no evidence path is tracked:** silent OK, continue to Step 3.

**If `.gitignore` does NOT cover the evidence dir, or any evidence file shows up under `git ls-files`:** warn the user before reporting completion:

```text
WARNING: tests/e2e/.evidence/ is not (or no longer) gitignored.

Detected:
- <list the offending paths from git ls-files / git check-ignore output>

This is the runtime evidence directory for e2e (screenshots, videos,
a11y snapshots) — it must NOT enter git. Suggested fix:

  echo 'tests/e2e/.evidence/' >> .gitignore
  git rm -r --cached tests/e2e/.evidence/   # only if files are already tracked

Resolve this before committing the feature, or the commit will pull
binary artifacts in.
```

Then continue to Step 3 — the warning is informational, not blocking. The user is in control of whether to fix it now or later.

Disk cleanup of the evidence directory itself is **not** this skill's concern — `tests/e2e/.evidence/` can grow as large as it wants, the user `rm -rf` it whenever they want. The only durable risk is git pollution, which this step covers.

### Step 3: Report Completion

Output a single completion message and stop:

```text
Implementation complete on `<feature-branch>`.

Verified:
- Tests: PASS (<command used>)
- E2E:   <"all AS-N OUTER_GREEN" | "EXEMPT per spec">

Branch is kept as-is — nothing committed, merged, pushed, or removed.

If you have uncommitted changes you want to commit:

  git status                                   # see what's pending
  git add <paths>
  git commit -m "<your message>"

Whatever happens next (commit, merge, PR, discard, or just leave the
branch sitting there) is yours to drive. Tell me what you want to do —
I'm happy to draft merge / push / PR / discard commands on request, but
I won't run any git mutations from inside this skill.
```

Then stop. Do not loop back, do not ask "which option?", do not auto-clean anything else.

## Quick Reference

| Step | What the skill does | What the skill never does |
|------|---------------------|---------------------------|
| 1. Verify Tests | Runs the project's test command | Skips on green-trust ("looks fine") |
| 1.5. Verify E2E (non-EXEMPT) | Dispatches `e2e-subagent` per AS-N, accepts only `OUTER_GREEN` | Trusts older evidence dirs, accepts `auto_connect_used: false` |
| 2. Sanity-check gitignore (non-EXEMPT) | Reads `.gitignore` + `git ls-files` for `tests/e2e/.evidence/`; warns if drift | Deletes evidence files, prompts to clean disk |
| 3. Report completion | Tells the user the branch is verified + kept as-is, suggests a commit if they have a pending diff | Runs `git commit / merge / push / branch -d / worktree remove`, opens PRs, picks merge styles |

## Common Mistakes

**Skipping verification because "tests obviously pass"**
- **Problem:** The whole point of this skill is the verification gate. Skipping it makes the report a lie.
- **Fix:** Always run Step 1 + Step 1.5. If you can't run them, say that explicitly instead of reporting completion.

**Adding back a "which option?" prompt**
- **Problem:** Forces the user to pick one of merge/PR/discard *right now*, when the realistic answer is often "I'll think about it after I look at the diff".
- **Fix:** Just report. The user will tell you what they want next, or do it themselves outside chat.

**Running git mutations on the user's behalf**
- **Problem:** Any of `git merge` / `git push` / `gh pr create` / `git branch -D` / `git worktree remove` strips the user's last chance to inspect or change course.
- **Fix:** Never run them inside this skill. If the user asks for a command in chat after the report, draft it — but they paste/run it.

**Treating the gitignore warning as blocking**
- **Problem:** Refusing to report completion because `.gitignore` drifted hides the actually-good news ("tests + e2e all green") behind a non-blocking config issue.
- **Fix:** Warn loudly, but still report completion. The user decides whether to fix the gitignore now or later.

## Red Flags

**Never:**
- Report completion with failing tests
- Report completion with any AS-N not at OUTER_GREEN (when spec is not EXEMPT)
- Run `git merge` / `git push` / `gh pr create` / `git branch -D` / `git worktree remove` yourself
- Delete anything under `tests/e2e/.evidence/`
- Re-introduce a "pick an option" interactive menu

**Always:**
- Verify tests + e2e (Step 1, Step 1.5) before any "complete" wording
- Sanity-check the `.gitignore` covers `tests/e2e/.evidence/` (Step 2) when non-EXEMPT
- Keep the branch and worktree exactly as the user left them
- Default to suggesting (not running) any git command

## Integration

**Called by:**

- **harness-kit:execute-plans** (Step 3) - After all tasks complete

**Hands control back to:** the user, in plain chat. There is no auto-handoff to merge / PR / archive flows from this skill.
