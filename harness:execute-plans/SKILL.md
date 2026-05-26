---
name: harness:execute-plans
description: description: Execute an implementation plan from a plan file. Use this skill when the user asks to start development from a plan, execute a roadmap, work through planned tasks, implement checklist items, or continue a previously written plan.
---

# Execute plans

Follow the provided plan file task by task.

1. Read the plan first and identify unchecked tasks and steps.
2. Execute unchecked steps in order.
3. Skip any task or step that is already checked.
4. After completing each step, update the plan file by checking the checkbox of that step.
5. After all steps in a task are complete, check the checkbox of parent task in the plan file.

<HARD-GATE>
Required sub skill: `harness:tdd`.
Use `harness:tdd` for implementation work unless the plan explicitly says the step is documentation-only, planning-only, or otherwise does not involve code behavior.s
</HARD-GATE>