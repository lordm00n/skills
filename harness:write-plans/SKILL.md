---
name: harness:write-plans
description: Write implementation plans for later execution by an independent agent. Use this skill when the user asks to write a plan, split work into tasks, draft an execution plan, create an implementation plan, or make a roadmap before development.
---

# Write plans

Write a plan that a later independent agent can follow to implement the requested change.

Before writing the plan, explore the relevant code paths enough to understand the local patterns:

- Read files the user explicitly mentions.
- Search for related symbols, adjacent modules, and existing implementations that the plan should follow.
- Stop exploring once you have enough context to write concrete implementation tasks.

Do not implement the plan. When using this skill, only create or update the plan file.

The plan must be a task list. Each task should include the files or modules likely involved and 3-6 concrete steps for the later agent to follow.

Per-task template:

```markdown
- [ ] Task 1: {{ description of the task }}

Files/modules: {{ files or modules likely involved }}

Steps:
- [ ] 1. {{ Concrete step }}
- [ ] 2. {{ Concrete step }}
- [ ] 3. {{ Concrete step }}
```

<HARD-GATE>
The plan **MUST** be within 10 tasks.
</HARD-GATE>

Write a plan file to `${PROJECT_ROOT_DIR}/docs/harness-kit/plans/<subject>-<YYYY-MM-DD>.plan.md`.
