---
name: harness-tdd
description: Follow the red-green-refactor circle of test driven development. Use this skill when you need to develop features or fix bugs.
---

# Test driven development

## Principles

When developing a new feature, follow the TDD red-green-refactor loop: write a failing test first, implement the smallest change that makes it pass, then refactor while keeping tests green.

When modifying existing behavior or fixing a bug, first find the relevant existing test cases and update them together with the code change, so the tests describe the intended behavior before the implementation is adjusted.

## Unit tests

Prefer unit tests for isolated logic, pure functions, validation, error handling, and small behavioral branches. Keep them fast and focused: arrange the minimum state needed, exercise one behavior, and assert the externally visible result rather than implementation details.

When changing existing code, start by locating the nearest unit test that already describes the relevant module. Add or update the smallest test that fails for the desired behavior before touching production code, then keep it as the regression guard after the fix.

## Integration tests

Use integration tests when the risk lives at the boundary between components: database queries, filesystem effects, service adapters, API handlers, job queues, dependency injection wiring, or serialization contracts. Prefer testing a real boundary with realistic inputs over mocking so deeply that the integration risk disappears.

Before adding a new integration test, check whether an existing scenario can be extended without making it broad or slow. Keep setup explicit, isolate shared state, and assert the contract that another module or user-facing layer depends on.

## E2E tests

If there are Web UI and Electron desktop UI scenario, follow the E2E testing instructions in `references/e2e-test-category.md` in the root directory in this skill.