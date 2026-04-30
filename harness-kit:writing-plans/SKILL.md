---
name: harness-kit:writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

<HARD-GATE>
Refer to the project context produced by `harness-kit:context-acquiring` skill for **this specific requirement** before writing plans.

If you think the context is not enough, then call `harness-kit:context-acquiring` skill again to update the context file for **this specific requirement**
</HARD-GATE>

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/harness-kit/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during harness-kit:brainstorm. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## E2E Strategy Gate

Before drafting any task, locate the spec's `## E2E Strategy` section. One of three outcomes:

- **Section lists `AS-N` scenarios** → for each `AS-N`, schedule an Outside-In task in the plan (see "Outside-In Tasks for E2E" below). These outer tasks wrap normal inner-TDD tasks.
- **Section says `EXEMPT: <reason>`** → proceed with the standard Task Structure only; no Outside-In tasks.
- **Section missing / empty / "TBD"** → STOP. Bounce the spec back to `harness-kit:brainstorm` to fill it in. Do not invent `AS-N` here — that violates the brainstorm → spec → plan ordering.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use harness-kit:execute-plan to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Outside-In Tasks for E2E

Schedule one Outside-In task per `AS-N` listed in the spec's `## E2E Strategy`. Place each Outside-In task **before** the inner-TDD tasks that implement the behavior it covers (so the outer RED is what motivates the inner work).

Each Outside-In task wraps the inner TDD loop — its inner steps reference `harness-kit:test-driven-development` for the unit-level Red-Green-Refactor cycle, and the AS itself drives `harness-kit:e2e-testing`.

````markdown
### Task <N> (Outside-In, AS-<M>): <one-line scenario summary>

**Spec scenario:** AS-<M> from `docs/harness-kit/specs/<spec>.md` → `## E2E Strategy`

**Files:**
- Create or extend: `tests/e2e/<feature>.sh` (`case AS-<M>` branch)
- Inner-loop files: <listed in inner tasks below>

- [ ] **Step 1: Scaffold the e2e script if missing**

If `tests/e2e/<feature>.sh` does not yet exist, copy the template:

```bash
cp ~/.agents/skills/harness-kit:e2e-testing/templates/feature.sh.template tests/e2e/<feature>.sh
chmod +x tests/e2e/<feature>.sh
# replace `<feature>` placeholders inside
```

Also ensure `.gitignore` covers `tests/e2e/.evidence/` per the e2e-testing skill's First-Run Setup.

- [ ] **Step 2: Write the AS-<M> branch (OUTER RED)**

In `tests/e2e/<feature>.sh`'s `case` block, fill in the `AS-<M>)` branch with the Given/When/Then from the spec. Use `${AB_FLAGS}` on every `agent-browser` call. For destructive lines, prefix with `_destructive_gate "<desc>" "<resource>"`.

(Concrete agent-browser commands belong here — load syntax via `agent-browser skills get core` when implementing.)

- [ ] **Step 3: Run the e2e via subagent dispatch (verify OUTER RED)**

Dispatch per `harness-kit:e2e-testing → Subagent Execution`:

> Task tool, subagent_type=`shell`, prompt contains the literal `e2e-subagent` marker plus the path to the e2e-testing SKILL.md and "Run AS-<M>".

Expected: subagent returns JSON with `phase: "OUTER_RED"`, `failing_step` describing where the assertion failed (NOT a connection error). Connection error → see Connection Failure Protocol; not a valid RED.

- [ ] **Step 4: Inner TDD loop (REQUIRED SUB-SKILL: harness-kit:test-driven-development)**

Drive the implementation with unit TDD. The inner loop's RED-GREEN-REFACTOR cycle continues until the outer e2e turns green. Add inner-TDD sub-tasks as needed; do NOT touch `tests/e2e/<feature>.sh` during the inner loop.

- [ ] **Step 5: Re-dispatch e2e (verify OUTER GREEN)**

Same dispatch as Step 3. Expected: JSON with `phase: "OUTER_GREEN"`, `exit_code: 0`, `auto_connect_used: true`, fresh evidence dir under `tests/e2e/.evidence/<feature>/`.

If `phase` is `AWAITING_DESTRUCTIVE_ACK`, follow `harness-kit:e2e-testing/destructive-gate-protocol.md` two-phase flow before proceeding.

- [ ] **Step 6: Commit**

```bash
git add tests/e2e/<feature>.sh <inner-impl-files>
git commit -m "feat(<feature>): AS-<M> <scenario summary>"
```
````

If a single feature has multiple AS-N, you may share the inner-loop tasks across them — order the plan so the first Outside-In task scaffolds the script and exercises the inner loop fully, and later Outside-In tasks for the same feature only add new `case AS-<M>)` branches and re-use the existing implementation.

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
- Refer the general project context produced by `harness-kit:context-acquiring` skill

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. E2E coverage:** For every `AS-N` in the spec's `## E2E Strategy` (when not `EXEMPT`), is there an Outside-In task using the template above? If the spec is `EXEMPT`, did you avoid scheduling any unnecessary e2e tasks?

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/harness-kit/plans/<filename>.md`. Execution:**

**Inline Execution** - Execute tasks in this session using execute-plan, batch execution with checkpoints

- **REQUIRED SUB-SKILL:** Use harness-kit:execute-plan
- Batch execution with checkpoints for review