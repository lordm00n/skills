# Outside-In Task Guideline (E2E-Driven Task)

Use this template for tasks driven by an `AS-N` from `## E2E Strategy` in `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md`.

Each Outside-In task wraps the inner unit-TDD loop:

- The outer Red-Green-Refactor is governed by `harness-kit:e2e` (drives the `AS-N` script branch).
- The inner Red-Green-Refactor is governed by `harness-kit:tdd` (drives the unit work that turns the outer scenario green).

Schedule **one** Outside-In task per `AS-N`. Place it **before** the inner-loop tasks that satisfy it, so the outer RED is what motivates the inner work.

If `## E2E Strategy` is `EXEMPT`, do not use this template — use `task-structure.guideline.md` only.

## Template

````markdown
### Task <N> (Outside-In, AS-<M>): <one-line scenario summary>

**Source spec:** AS-<M> from `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md` → `## E2E Strategy`

**REQUIRED SUB-SKILL (outer):** `harness-kit:e2e` — drives Steps 1, 2, 3, 5 below.
**REQUIRED SUB-SKILL (inner):** `harness-kit:tdd` — drives Step 4 (one or more nested Red-Green-Refactor cycles).

**Files:**
- Create or extend: `tests/e2e/<feature>.sh` (`case AS-<M>` branch)
- Inner-loop files: <listed in inner sub-tasks below; each inner sub-task back-points to its UT-N>

- [ ] **Step 1: Scaffold the e2e script if missing**

If `tests/e2e/<feature>.sh` does not yet exist, copy the template that ships with `harness-kit:e2e`:

```bash
SKILL_DIR=$(dirname "$(readlink -f ~/.agents/skills/harness-kit:e2e/SKILL.md)")
mkdir -p tests/e2e
cp "${SKILL_DIR}/templates/feature.sh.template" "tests/e2e/<feature>.sh"
chmod +x "tests/e2e/<feature>.sh"
# replace `<feature>` placeholders inside the file
```

Also ensure `.gitignore` covers `tests/e2e/.evidence/` per `harness-kit:e2e` § First-Run Setup. The e2e skill refuses to scaffold without this — handle it now, not later.

- [ ] **Step 2: Write the AS-<M> branch (OUTER RED, per `harness-kit:e2e`)**

In `tests/e2e/<feature>.sh`'s `case` block, fill in the `AS-<M>)` branch with the Given/When/Then from the spec. Use `${AB_FLAGS}` on every `agent-browser` call. For destructive lines, prefix with `_destructive_gate "<desc>" "<resource>"`.

Concrete `agent-browser` commands belong here — load the current syntax via `agent-browser skills get core` (and `... electron` for desktop targets) when implementing. Do not invent commands from memory.

- [ ] **Step 3: Run the e2e via subagent dispatch (Verify OUTER RED)**

Dispatch per `harness-kit:e2e` § Subagent Execution:

> Task tool, `subagent_type=shell` (or `generalPurpose` if the subagent must also edit the script), with a prompt that contains the literal `e2e-subagent` marker, the absolute path to `harness-kit:e2e/SKILL.md`, the feature name, and "Run AS-<M>".

Expected JSON report: `phase: "OUTER_RED"`, `failing_step` describing where the assertion failed (NOT a connection error). A connection error is **not** a valid OUTER RED — see `harness-kit:e2e` § Connection Failure Protocol.

- [ ] **Step 4: Inner TDD loop (REQUIRED SUB-SKILL: `harness-kit:tdd`)**

Drive the implementation with unit TDD. Add inner sub-tasks here, each shaped like `task-structure.guideline.md` (RED → Verify-RED → GREEN → Verify-GREEN), each back-pointing to its `UT-K` from `test-category.md`. The inner loop's Red-Green-Refactor cycle continues until the outer e2e turns green.

Do NOT touch `tests/e2e/<feature>.sh` during the inner loop.

- [ ] **Step 5: Re-dispatch e2e (Verify OUTER GREEN, per `harness-kit:e2e`)**

Same dispatch as Step 3. Expected JSON report: `phase: "OUTER_GREEN"`, `exit_code: 0`, `auto_connect_used: true`, fresh evidence dir under `tests/e2e/.evidence/<feature>/`.

If `phase` is `AWAITING_DESTRUCTIVE_ACK`, follow `harness-kit:e2e/reference/destructive-gate-protocol.md` (two-phase flow with `proceed-destructive <ack_token>` re-dispatch) before proceeding.

- [ ] **Step 6: Report task completion (do NOT commit)**

Tell the user, verbatim:

> Task <N> (AS-<M>) complete.
>
> **Spec mapping:** AS-<M> from `harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md` → `## E2E Strategy`
>
> **Files changed:**
> - `tests/e2e/<feature>.sh` (new or modified `case AS-<M>)` branch)
> - `<inner-impl-files>` (modified)
>
> **Verification:** subagent JSON report → `phase: "OUTER_GREEN"`, `exit_code: 0`, `auto_connect_used: true`
>
> **Suggested commit (run yourself if you want it):**
>
> ```bash
> git add tests/e2e/<feature>.sh <inner-impl-files>
> git commit -m "feat(<feature>): AS-<M> <scenario summary>"
> ```
>
> Reply `next` to start the next task, or commit / inspect / change anything first.

Then **stop and wait** for the user before starting the next task.
````

## Sharing Inner Work Across Multiple AS

If a feature has multiple `AS-N`, you may share the inner-loop work across them — order the plan so the first Outside-In task scaffolds the script and exhausts the inner loop, and later Outside-In tasks for the same feature only add new `case AS-<M>)` branches and re-use the existing implementation. Each Outside-In task still gets its own Step 6 report keyed on its own AS.

## Required-Field Checklist

Reject any Outside-In task in `tasks.md` that misses one of these:

- [ ] `**Source spec:**` line names the `AS-N` and the path to `test-category.md`.
- [ ] Both `**REQUIRED SUB-SKILL:**` lines are present and use the literal names `harness-kit:e2e` (outer) and `harness-kit:tdd` (inner).
- [ ] Step 1 references `harness-kit:e2e/templates/feature.sh.template` and the First-Run Setup gitignore gate.
- [ ] Steps 2 and 3 are OUTER RED + Verify-OUTER-RED; Step 4 is the inner loop; Step 5 is Verify-OUTER-GREEN. Order matters — `harness-kit:e2e`'s Iron Law is "no user-visible behaviour code without a failing AS first".
- [ ] Step 6 reports completion via the literal user-facing block above and does not run `git commit`.
- [ ] References to e2e infrastructure use the canonical paths: `harness-kit:e2e/SKILL.md`, `harness-kit:e2e/templates/feature.sh.template`, `harness-kit:e2e/reference/destructive-gate-protocol.md`. Do not paraphrase to `harness-kit:e2e-testing/...`.
