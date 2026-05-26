---
name: harness:spec-design
description: Summarize the shared understanding between you and the user into specifications. Use this skill after the user has described their request and confirmed alignment.
---

# Spec design

When alignment is confirmed, write a design document that includes:

1. Goals and non-goals for this request.

2. Architecture diagram in **Mermaid** only when it clarifies components, boundaries, or data flow.

3. Sequence diagram in **Mermaid** when the request involves multi-step flows, async work, external services, or state transitions.s

4. Proposed file tree showing files to create or modify.

5. Acceptance criteria and risk points.

Write the specifications into `${PROJECT_ROOT_DIR}/docs/harness-kit/specs/<subject>-<YYYY-MM-DD>/design.md`.

<HARD-GATE>
The file of specifications **MUST** be within 300 lines.
</HARD-GATE>