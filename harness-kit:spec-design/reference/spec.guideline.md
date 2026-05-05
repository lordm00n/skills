# Spec Document: <subject>

**Date**: YYYY-MM-DD
**Status**: Draft | Under Review | Approved | Superseded
**Author**: <name>

---

> The spec contains two files in a diractory.

## Test spec file

Two parts need to be output to `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md`:

1. Unit test Strategy

Refer to the `unit-test.guideline.md` in the `reference` dir of this skill.

2. E2E Strategy Section

Refer to the `e2e-test.guideline.md` in the `reference` dir of this skill.

## Total spec file

Five parts need to be output to `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/design.md`:

### 0. Context & Goals

#### Motivation

<!-- The driving force behind this design. What problem does this design solve? -->

#### Goals

- [ ] <goal-1>
- [ ] <goal-2>

#### Non-goals

- <what-is-explicitly-out-of-scope-1>
- <what-is-explicitly-out-of-scope-2>

---

### 1. Top-level Design Decisions

#### Architecture

<!-- Architecture style, key patterns, and trade-offs made. Why this architecture over alternatives. -->

#### Components

| Component | Responsibility |
|-----------|---------------|
| `<component-name>` | <what-it-does> |

#### Interfaces

| Interface | From | To | Protocol / Contract |
|-----------|------|----|---------------------|
| `<interface-name>` | `<source>` | `<target>` | <description> |

#### Data Model

<!-- Core entities, their relationships, and state transitions if applicable. Use Mermaid for ER diagrams or state machines. -->

#### Flow Diagram

```mermaid
<!-- Mermaid flow diagram showing the high-level architecture and data flow -->
```

#### Directory Tree

```markdown
<project-root>/
├── <dir-1>/
│   ├── <file-or-subdir>
│   └── ...
└── <dir-2>
    └── ...
```

---

### 2. Constraints & Assumptions

#### Technical Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| `<constraint>` | <how-it-affects-design> | <workaround-if-any> |

#### Business Constraints

| Constraint | Impact |
|------------|--------|
| `<constraint>` | <how-it-affects-design> |

#### Assumptions

| Assumption | Risk if Invalidated |
|------------|---------------------|
| `<assumption>` | <what-breaks-if-wrong> |

---

### 3. Detailed Design

#### Module: `<module-name>`

**Responsibility**: <one-line-summary>

**Mechanism**:

<!-- How this module works internally, step by step or via pseudo-code. -->

**Dependencies**: <what-other-modules-it-depends-on>

#### Error Handling Strategy

| Error Category | Example | Handling | User-facing Behavior |
|----------------|---------|----------|----------------------|
| `<category>` | `<example>` | `<retry/fallback/log-and-continue>` | `<error-message-or-graceful-degradation>` |

#### Configuration Management

| Key | Type | Default | Source (env/file/const) | Description |
|-----|------|---------|------------------------|-------------|
| `<config-key>` | `<string\|number\|boolean>` | `<default-value>` | `<source>` | <what-it-controls> |

---

### 4. Non-functional Requirements

#### Performance

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| `<latency/throughput/memory>` | `<value>` | <how-to-measure> |

#### Security

<!-- Authz model, data protection, attack surface analysis, sensitive data handling. -->

#### Reliability

<!-- Fault tolerance strategy, graceful degradation plan, recovery procedures. -->

#### Observability

| Signal | Tool / Format | What is Captured |
|--------|--------------|-------------------|
| Logs | <format> | <key-events> |
| Metrics | <system> | <key-metrics> |
| Traces | <system> | <critical-paths> |

#### Compatibility

<!-- Backward compatibility guarantees, migration path from previous versions, versioning scheme. -->

---

### 5. Test Category

Referr to `{$PROJECT_ROOT_DIR}/specs/<subject-YYYY_MM_DD>/test-category.md`

### Glossary

#### `<term>`

- **Origin**: <why-this-name-was-chosen>
- **Definition**: <precise-meaning — what it is AND what it is NOT>
- **Usage in this design**: <how-applied-in-context, not generic definition>
- **Scope**: <which-component(s)/module(s)/section(s) this term is relevant to>
- **Example**: <concrete-instance-from-the-design-to-ground-the-definition>

---

**Guidelines**:
- Every **non-trivial term** introduced in this spec MUST have an entry here.
- Skip only universally understood terms (e.g., "HTTP", "JSON", "API").
- Each term entry uses the template above. Repeat for as many terms as needed.
- **Origin**: Explain naming rationale — why this term over alternatives.
- **Definition**: Precise, unambiguous meaning — what it is AND what it is NOT.
- **Usage**: How this term is specifically applied within THIS design, not generic definition.
- **Scope**: Which component(s), module(s), or section(s) this term is relevant to.
- **Example**: A concrete instance from the design to ground abstract definitions. Omit only when the term is self-evident from context.