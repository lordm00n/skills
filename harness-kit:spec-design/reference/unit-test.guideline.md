# Unit Test Guideline

Use the form below. **Every** test case MUST include both:

1. **Case** — a Given/When/Then sentence describing one observable behavior.
2. **Intent** — one sentence stating, in the context of the current requirement, **what behavior this test pins down and why it matters**. Tie the intent back to a specific goal, constraint, or design decision in the spec; do NOT restate the Given/When/Then.

```markdown
## `<module-name>`

- UT-1:
  - **Case**: <Given/When/Then sentence describing one observable behavior>
  - **Intent**: <Why this case exists in the context of THIS requirement — which goal / constraint / design decision it protects, and what regression it would catch>
- UT-2:
  - **Case**: <an error / boundary / edge case for this module>
  - **Intent**: <Which failure mode or edge condition from the spec this guards against, and why it must not regress>
- UT-3: ...

## `<another-module>`

- UT-4:
  - **Case**: ...
  - **Intent**: ...
- UT-5: ...
```

**Rules for `Intent`**:

- Reference the requirement context — name the goal, constraint, invariant, or design decision (from `design.md`) that this test exists to protect.
- Describe behavior, not implementation — say what user-visible or contract-level guarantee is being pinned, not which functions are called.
- Explain the regression it prevents — what would silently break if this test were deleted.
- Keep it to **one sentence**. If you need more, the test case is probably doing too much and should be split.

**Anti-patterns** (reject these `Intent` lines):

- "Tests that `foo()` returns the correct value." — restates the case, no requirement context.
- "Ensures the function works." — vacuous, no behavior or regression named.
- "Covers the happy path." — no link to a specific goal or constraint.
