# Task Structure Guideline (Inner-Loop Task)

Use this template for tasks driven by unit TDD — one task per coherent behaviour drawn from the `UT-N` list in `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md`.

For Outside-In (e2e) tasks, use `e2e-task.guideline.md` instead. The inner steps of an Outside-In task still follow the inner-loop pattern below.

Every task in `tasks.md` MUST:

1. Carry a back-pointer to the spec `UT-N` it implements.
2. Declare `harness-kit:tdd` as its REQUIRED SUB-SKILL — verbatim, no paraphrasing.
3. End with a "Report task completion" step that **does not** run `git commit`.

## Template

````markdown
### Task <N>: <Component / Behaviour Name>

**Source spec:** UT-<M>[, UT-<M+1>, …] from `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md`

**REQUIRED SUB-SKILL:** `harness-kit:tdd` — drive Steps 1–4 below as one Red-Green-Refactor cycle of that skill.

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`
- Test module README: `tests/exact/path/to/README.md` (create on the first task that lands a test in this directory; update on every subsequent task that adds a `UT-N`)

- [ ] **Step 1: Write the failing test (RED, per `harness-kit:tdd`)**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

If this is the **first** test ever landing in `tests/<module>/`, also scaffold the test-module README (see `harness-kit:tdd/SKILL.md` § Test Module README):

```bash
SKILL_DIR=$(dirname "$(readlink -f ~/.agents/skills/harness-kit:tdd/SKILL.md)")
mkdir -p tests/<module>
cp "${SKILL_DIR}/templates/test-module.README.md.template" "tests/<module>/README.md"
# replace `<module-name>` and other placeholders; fill in the runner install/invocation commands and env-var table for THIS module
```

If the README already exists from an earlier task in the same module, update it: append the new `UT-<M>` row to the **Test cases** table, and add any new env-var or fixture row introduced by this task. Drifted README = task incomplete.

- [ ] **Step 2: Run test to verify it fails (Verify RED)**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation (GREEN, per `harness-kit:tdd`)**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes (Verify GREEN)**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Report task completion (do NOT commit)**

Tell the user, verbatim:

> Task <N> complete.
>
> **Spec mapping:** UT-<M> from `harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md`
>
> **Files changed:**
> - `tests/path/test.py` (new)
> - `tests/path/README.md` (new or updated — UT-<M> row + any new env-var row)
> - `src/path/file.py` (modified)
>
> **Verification:** `pytest tests/path/test.py::test_name -v` → PASS; README's Test cases table covers UT-<M>
>
> **Suggested commit (run yourself if you want it):**
>
> ```bash
> git add tests/path/test.py tests/path/README.md src/path/file.py
> git commit -m "feat: add specific feature"
> ```
>
> Reply `next` to start Task <N+1>, or commit / inspect / change anything first.

Then **stop and wait** for the user before starting the next task. Do not run `git commit` yourself, even if you previously did so in this session.
````

## Required-Field Checklist

Reject any task in `tasks.md` that misses one of these:

- [ ] `**Source spec:**` line names the `UT-N` and the path to `test-category.md`.
- [ ] `**REQUIRED SUB-SKILL:**` line names `harness-kit:tdd` literally.
- [ ] `**Files:**` block lists exact paths (no wildcards, no "etc.") AND includes the test module's `README.md` path.
- [ ] Step 1 explicitly handles the test-module README — scaffold from `harness-kit:tdd/templates/test-module.README.md.template` on first touch, update the **Test cases** / env-var rows on every subsequent task in the same module.
- [ ] Steps 1 and 2 are RED + Verify-RED; Steps 3 and 4 are GREEN + Verify-GREEN. Order matters — `harness-kit:tdd`'s Iron Law is "no production code without a failing test first".
- [ ] Step 5 reports completion via the literal user-facing block above (including the README in `Files changed:`) and does not run `git commit`.
