# Plan Structure Guideline

This guideline defines what `harness-kit:plan` writes to disk and how the produced files cross-reference one another, the upstream spec, the upstream context doc, and the downstream sub-skills.

## Output Directory Layout

For a requirement whose spec lives at `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/`, the plan dir MUST use the **identical** dated slug:

```
{$PROJECT_ROOT_DIR}/harness-kit/plans/<subject-YYYY_MM_DD>/
├── plan.md     # overview + index — read this first
└── tasks.md    # ordered, bite-sized tasks — the executor's running script
```

Pairing rule: `plans/<subject-YYYY_MM_DD>/` ↔ `specs/<subject-YYYY_MM_DD>/` share the slug verbatim. A reader who only knows the slug can locate every related artefact.

## Reference Graph (the produced files)

```
specs/<subject-YYYY_MM_DD>/design.md           ◄── plan.md (Source Spec ↑) ──┐
specs/<subject-YYYY_MM_DD>/test-category.md    ◄── plan.md (Source Spec ↑)  │
context/<subject>-YYYY_MM_DD.context.md        ◄── plan.md (Context ↑)      │
                                                                            ▼
                                                                       tasks.md
                                                                            │
                                                                            ├─ each task → spec UT-N / AS-N (back-pointer)
                                                                            ├─ each task → REQUIRED SUB-SKILL: harness-kit:tdd
                                                                            └─ Outside-In task → REQUIRED SUB-SKILL: harness-kit:e2e
                                                                            ▼
                                                                  plan.md declares
                                                                  REQUIRED SUB-SKILL:
                                                                  harness-kit:execute-plan
```

Every arrow above MUST appear as a literal path or skill-name reference in the produced markdown — never as prose like "see the spec". Use the path conventions listed in this guideline.

## `plan.md` — Overview

**Output path:** `{$PROJECT_ROOT_DIR}/harness-kit/plans/<subject-YYYY_MM_DD>/plan.md`

**Role:** human-readable overview. The executor reads `plan.md` once to load context, then drives `tasks.md` step-by-step.

### Required Header

Every `plan.md` MUST start with this header, in this order:

````markdown
# <Feature Name> Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL — invoke `harness-kit:execute-plan` to run this plan task-by-task. Steps in `tasks.md` use checkbox (`- [ ]`) syntax for tracking.

## Source Artefacts

| Role | Path |
|---|---|
| Spec — design | `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/design.md` |
| Spec — test category | `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md` |
| Project context | `{$PROJECT_ROOT_DIR}/harness-kit/context/<subject>-YYYY_MM_DD.context.md` |
| Tasks (this plan) | `./tasks.md` |

## Summary

**Goal:** <one sentence describing what this builds>

**Architecture:** <2-3 sentences mirroring `design.md` § 1 — do NOT re-derive, paraphrase>

**Tech Stack:** <key technologies / libraries pulled from `design.md` and the context doc>
````

Replace every `<...>` with concrete content. None of the table rows are optional — if there is no context doc (e.g. the user explicitly skipped `harness-kit:acquire-context`), state that in plain text below the table rather than dropping the row.

### File Structure Section

After the header, list the files this plan will touch, with one-line responsibility per file. This block is the locked-in decomposition that `tasks.md` then implements.

````markdown
## File Structure

| File | Status | Responsibility |
|---|---|---|
| `path/to/new/module.ts` | new | <one-line responsibility> |
| `path/to/existing/file.ts` | modified | <what changes and why> |
| `tests/path/to/test.ts` | new | <which behaviours it covers, refs UT-1, UT-2> |
| `tests/e2e/<feature>.sh` | new (if AS-N) | <which `AS-N` branches it carries> |
````

### Tasks Section

`plan.md` does **not** inline the task bodies. It points at `tasks.md` and lists the task index so a reader can scan the shape of the work without scrolling through code:

````markdown
## Tasks

The executable steps live in [`./tasks.md`](./tasks.md). Index:

1. Task 1: <one-line summary> — REQUIRED SUB-SKILL: `harness-kit:tdd`
2. Task 2 (Outside-In, AS-1): <scenario summary> — REQUIRED SUB-SKILL: `harness-kit:e2e`
3. Task 3: <one-line summary> — REQUIRED SUB-SKILL: `harness-kit:tdd`
…
````

The index keeps the SUB-SKILL pointer beside each entry so the executor knows which inner skill governs that task before they open `tasks.md`.

## `tasks.md` — Executable Steps

**Output path:** `{$PROJECT_ROOT_DIR}/harness-kit/plans/<subject-YYYY_MM_DD>/tasks.md`

**Role:** the running script the executor walks down. Self-contained per task: an executor reading any single task should not need to scroll up.

### Required Header

Every `tasks.md` MUST start with this header so the file stands on its own when opened directly:

````markdown
# <Feature Name> — Tasks

> Companion to [`./plan.md`](./plan.md). Read `plan.md` once for overview, then execute the tasks below in order.

> **For agentic workers:** REQUIRED SUB-SKILL — `harness-kit:execute-plan`. Each task body further declares its own inner SUB-SKILL (`harness-kit:tdd` or `harness-kit:e2e`); do not skip the declaration line.

## Source Artefacts (mirrored from `plan.md`)

| Role | Path |
|---|---|
| Spec — design | `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/design.md` |
| Spec — test category | `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md` |
| Project context | `{$PROJECT_ROOT_DIR}/harness-kit/context/<subject>-YYYY_MM_DD.context.md` |
| Plan overview | `./plan.md` |
````

The Source Artefacts table is duplicated intentionally: the executor often opens `tasks.md` alone and must be able to walk back to every input without bouncing through `plan.md` first.

### Task Bodies

Two task patterns:

- **Inner-loop task** (drives `harness-kit:tdd`) — see `task-structure.guideline.md` in this `reference/` dir. Each task back-points to one or more `UT-N` from `test-category.md`.
- **Outside-In task** (drives `harness-kit:e2e`, wraps `harness-kit:tdd` inside) — see `e2e-task.guideline.md` in this `reference/` dir. Each task back-points to one `AS-N` from `## E2E Strategy` in `test-category.md`.

### Task Ordering Rule

If `test-category.md` lists any `AS-N`, schedule each `AS-N`'s Outside-In task **before** the inner-loop tasks that satisfy it — the outer RED is what motivates the inner work. If `## E2E Strategy` is `EXEMPT`, all tasks follow `task-structure.guideline.md` only.
