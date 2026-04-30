---
name: harness-kit:execute-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the harness-kit:execute-plans skill to implement this plan."

**Note:** Tell your human partner that harness-kit works much better with access to subagents. The quality of its work will be significantly higher if run on a platform with subagent support (such as Claude Code or Codex). If subagents are available, use harness-kit:subagent-driven-development instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed
5. **Hand control back to the user at the task boundary.** The plan's final step of every task is `Report task completion (do NOT commit)` — emit that report verbatim (file list + verification result + suggested commit command) and **stop**. Do not start the next task until the user replies (typically `next`, but they may want to commit, inspect the diff, or revise something first).

**Why the per-task pause:** plans are written assuming the user wants control over commit boundaries — batching, message wording, skipping a commit entirely, etc. Auto-rolling into Task N+1 silently strips that control. Even if the user said "go" once at the start, treat each task as a fresh checkpoint. If the user explicitly says something like "just blast through all of them, don't ask" you can honor that for the remainder of the session.

**Never run on the user's behalf inside this skill:** `git commit`, `git push`, `git merge`, `gh pr create`. Those belong to the user — and the same is true of every other harness-kit skill, including `harness-kit:finishing-a-development-branch`, which only verifies and reports. If the plan accidentally contains a literal `git commit` step, treat it as a `Report task completion` step instead — surface the suggested command, do not run it, and flag the plan bug to the user.

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the harness-kit:finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use harness-kit:finishing-a-development-branch
- That skill will re-verify tests + e2e, sanity-check the e2e evidence is gitignored, then report completion. It will not merge, push, open PRs, or remove anything — whatever the user wants to do next is plain chat after the report.

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Stop at every task boundary — emit the `Report task completion` message and wait for the user before starting the next task
- Never run `git commit` / `git push` / `git merge` / `gh pr create` on the user's behalf
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **harness-kit:writing-plans** - Creates the plan this skill executes
- **harness-kit:finishing-a-development-branch** - Complete development after all tasks
- **harness-kit:test-driven-development** - Follow TDD workflow to develop features.
