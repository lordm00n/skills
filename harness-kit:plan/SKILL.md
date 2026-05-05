---
name: harness-kit:plan
description: Plan out the implementation of a feature or bugfix. Use when you have an approved spec from `harness-kit:spec-design` and a context doc from `harness-kit:acquire-context`, and you need to translate them into a per-task implementation plan before touching code.
---

# Writing Plans

## Overview

Translate an approved spec + acquired project context into a two-file implementation plan that an executor can run task-by-task without holding any other context in their head. DRY. YAGNI. TDD. After each task, the executor reports completion to the user — they never commit on the user's behalf.

Assume the executor is a skilled developer who knows almost nothing about our toolset or problem domain, and isn't strong at test design. Document everything: which files to touch for each task, code, tests, docs to check, exact commands and expected output.

## Inputs (read these BEFORE writing the plan)

This skill assumes two upstream artefacts already exist on disk. If either is missing, stop and ask the user to run the upstream skill — do **not** invent the missing content.

| # | Source skill | File path | Why this skill needs it |
|---|---|---|---|
| 1 | `harness-kit:spec-design` | `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/design.md` | Architecture, components, modules, data model, dir tree — drives File Structure + task decomposition. |
| 2 | `harness-kit:spec-design` | `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md` | `UT-N` list (drives inner TDD tasks) and `## E2E Strategy` `AS-N` list / `EXEMPT` flag (drives Outside-In tasks). |
| 3 | `harness-kit:acquire-context` | `{$PROJECT_ROOT_DIR}/harness-kit/context/<subject>-YYYY_MM_DD.context.md` | Project rules, internal docs, remote docs, local wikis relevant to this requirement. |

<HARD-GATE>
Before writing the plan, re-read the context doc (input 3) for **this specific requirement**. If you judge the context insufficient, stop and re-invoke `harness-kit:acquire-context` to refresh the same context file — do not paper over the gap inside the plan.
</HARD-GATE>

The dated slug `<subject-YYYY_MM_DD>` of the plan dir MUST match the spec dir slug exactly, so a reader can pair plan ↔ spec by directory name alone.

## Outputs (what this skill writes)

This skill produces exactly two files, in one new directory:

```
{$PROJECT_ROOT_DIR}/harness-kit/plans/<subject-YYYY_MM_DD>/
├── plan.md     # overview: goal, architecture, file structure, links into tasks.md
└── tasks.md    # the bite-sized executable steps, in order
```

Both files MUST contain explicit back-pointers to their inputs (the spec dir and the context doc) and forward-pointers to the executor / inner skills they delegate to. The exact templates and reference rules live in `reference/plan-structure.guideline.md`.

## Skill Graph (who calls whom)

```
harness-kit:acquire-context ┐
                            ├──► harness-kit:plan ──► plan.md ──► (REQUIRED SUB-SKILL) harness-kit:execute-plan
harness-kit:spec-design ────┘            │
                                         └─► tasks.md ──► (per task, REQUIRED SUB-SKILL)
                                                          ├─ harness-kit:tdd   (inner Red-Green-Refactor)
                                                          └─ harness-kit:e2e   (Outside-In, only when test-category.md lists AS-N)
```

- **Inbound (this skill consumes):** outputs of `harness-kit:acquire-context` and `harness-kit:spec-design`. Listed by exact path in **Inputs** above.
- **Embedded in `plan.md` (the runner):** `harness-kit:execute-plan` — declared in the plan header as the REQUIRED SUB-SKILL the executor must invoke to run the plan task-by-task. Use this exact skill name; do not paraphrase.
- **Embedded in `tasks.md` (per task):** each task names the SUB-SKILL that drives its inner loop, using the canonical skill names:
  - `harness-kit:tdd` for any task whose body is unit-level Red-Green-Refactor (drawn from `UT-N` in `test-category.md`).
  - `harness-kit:e2e` for any Outside-In task wrapping an `AS-N` from `## E2E Strategy`. The Outside-In task's inner steps still hand off to `harness-kit:tdd`.

When you write a skill name into either output file, write it verbatim — `harness-kit:tdd`, `harness-kit:e2e`, `harness-kit:execute-plan`. Do not expand to long forms like "test-driven-development" or "e2e-testing"; the executor matches on the exact name.

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during `harness-kit:spec-design`. If it wasn't, suggest breaking this into separate plans — one per subsystem, each in its own `plans/<sub-subject-YYYY_MM_DD>/` dir paired with its own spec dir. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure — but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently. The exact `## File Structure` block lives in `plan.md` per `reference/plan-structure.guideline.md`.

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task
- A bare skill name with no surrounding instruction (e.g. just `harness-kit:tdd`) — always pair the skill name with the line `**REQUIRED SUB-SKILL:** harness-kit:<name>` and the step the executor takes when invoking it.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Report task completion to the user (do NOT commit)" — step

The plan never tells the executor to run `git commit`. Whether and when to commit is the user's call — the final step of every task only *reports* what changed.

## Reference Files

This SKILL.md is the entry point. Detailed templates and per-task patterns live alongside in `reference/`:

| Reference file | What it specifies |
|---|---|
| `reference/plan-structure.guideline.md` | Output dir layout, `plan.md` header template, the back-pointer block linking plan.md ↔ tasks.md ↔ spec dir ↔ context doc. |
| `reference/task-structure.guideline.md` | The bite-sized task template for unit-TDD-driven tasks (RED → GREEN → REFACTOR → report). Names `harness-kit:tdd` as the REQUIRED SUB-SKILL. |
| `reference/e2e-task.guideline.md` | The Outside-In task template for `AS-N`. Names `harness-kit:e2e` as the REQUIRED SUB-SKILL and shows how the inner loop hands off to `harness-kit:tdd`. |

Always cite these files relative to this skill (e.g. "see `reference/task-structure.guideline.md` of `harness-kit:plan`") so the executor can resolve the path from the skill root.

## Remember

- Exact file paths always — full paths from `{$PROJECT_ROOT_DIR}`, never bare filenames.
- Complete code in every step — if a step changes code, show the code.
- Exact commands with expected output.
- Exact skill names — `harness-kit:tdd`, `harness-kit:e2e`, `harness-kit:execute-plan` — verbatim, no paraphrasing.
- DRY, YAGNI, TDD.
- Both output files cite the spec dir and the context doc by path. The reader of either file should be able to walk back to every input without guessing.
