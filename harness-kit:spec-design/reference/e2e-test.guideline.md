# E2E Test Guideline

Use one of the two forms below.

For features with user-visible behavior, **every** acceptance scenario MUST include both:

1. **Scenario** — a Given/When/Then sentence describing one user-visible flow.
2. **Intent** — one sentence stating, in the context of the current requirement, **what user-visible promise this scenario pins down and why it matters**. Tie the intent back to a specific goal, user value, or constraint in the spec; do NOT restate the Given/When/Then.

```markdown
## E2E Strategy

- AS-1:
  - **Scenario**: <Given/When/Then sentence describing one user-visible flow>
  - **Intent**: <Why this scenario exists in the context of THIS requirement — which user-facing goal / value / constraint it protects, and what user-visible regression it would catch>
- AS-2:
  - **Scenario**: <another scenario, e.g. an error / edge state>
  - **Intent**: <Which failure mode or degraded experience from the spec this guards against, and why users must not see it regress>
- AS-3: ...
```

Or, if the feature has no user-visible behavior:

```markdown
## E2E Strategy

EXEMPT: <one-line reason — e.g. "pure backend API consumed only by other services", "internal CLI tool with no UI", "build script with no runtime UI">
```

**Rules for `Intent`**:

- Reference the requirement context — name the user-facing goal, value, constraint, or acceptance criterion (from `design.md`) that this scenario exists to protect.
- Describe user-observable outcome, not implementation — say what the user sees, can do, or is prevented from doing; never name internal modules, functions, or APIs.
- Explain the regression it prevents — what would silently break for the user if this scenario were deleted.
- Keep it to **one sentence**. If you need more, the scenario is probably bundling multiple user promises and should be split.

**Anti-patterns** (reject these `Intent` lines):

- "Tests that the form submits correctly." — restates the scenario, no requirement context.
- "Ensures the page loads." — vacuous, no user-facing promise or regression named.
- "Covers the happy path." — no link to a specific user goal or value.
- "Verifies the API returns 200." — describes a transport detail, not a user-visible outcome.
