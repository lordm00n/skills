---
name: harness-kit:finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

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
E2E failing for AS-<M> (<failing_step>). Must fix before completing:

[Show failing_step + evidence_dir]

Cannot proceed with merge/PR until every AS-N in spec returns
OUTER_GREEN.
```

Stop. Do not proceed to Step 2.

**If all AS-N pass:** continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes:
```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

### Step 5.5: Cleanup E2E Evidence (when spec was not EXEMPT)

For Options 1, 2, 4 only. Skip for Option 3 (keep-as-is) — the evidence may still be useful while the branch lives.

If `tests/e2e/.evidence/<feature>/` exists, ask the user:

```text
About to delete:
- tests/e2e/.evidence/<feature>/  (<N> timestamped runs, <total-size>)

These are the e2e screenshots / videos / a11y snapshots collected
during this feature's development. They have already served their
purpose for verification-before-completion. Keeping them means you
can still inspect failure traces later; deleting them frees disk
and keeps the next feature's evidence dir uncluttered.

Reply EXACTLY:
  cleanup-evidence    — delete the directory
  keep                — leave the directory in place

Anything else (silence, "yes", "ok", a different word) is treated
as `keep`.
```

Wait for the literal `cleanup-evidence` reply. Only on that exact word:

```bash
rm -rf tests/e2e/.evidence/<feature>/
```

On `keep`, silence, or any other reply: leave the directory alone and report:

```text
Kept tests/e2e/.evidence/<feature>/ — delete manually when no longer needed.
```

If `tests/e2e/.evidence/<feature>/` does not exist (no e2e was run, or already cleaned), skip silently.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch | Offer Evidence Cleanup |
|--------|-------|------|---------------|----------------|------------------------|
| 1. Merge locally | ✓ | - | - | ✓ | ✓ (Step 5.5) |
| 2. Create PR | - | ✓ | ✓ | - | ✓ (Step 5.5) |
| 3. Keep as-is | - | - | ✓ | - | - (keep) |
| 4. Discard | - | - | - | ✓ (force) | ✓ (Step 5.5) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**
- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Proceed with any AS-N not at OUTER_GREEN (when spec is not EXEMPT)
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Delete `tests/e2e/.evidence/<feature>/` without literal `cleanup-evidence` confirmation

**Always:**
- Verify tests before offering options
- Verify e2e (Step 1.5) before offering options when spec is not EXEMPT
- Present exactly 4 options
- Get typed confirmation for Option 4
- Get typed `cleanup-evidence` confirmation for Step 5.5
- Clean up worktree for Options 1 & 4 only

## Integration

**Called by:**

- **harness-kit:execute-plans** (Step 5) - After all batches complete
