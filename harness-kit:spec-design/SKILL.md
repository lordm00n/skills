---
name: harness-kit:spec-design
description: Design the specification of a feature or a system, and output a spec document. Use this skill when the user wants to design specs of a feature or a system.
---

# Spec Design

## User requirements

```text
$ARGUMENTS
```

## Goal

- Output specs files that contains top-level design decisions and detailed design and test categories.

## Align with user through conversation

<HARD-GATE>
Communicate questions to the user **directly in your response text** — do NOT invoke any question-asking tool or UI.
</HARD-GATE>

<HARD-GATE>
Every question MUST be self-contained with sufficient context:
- **Purpose**: What decision or clarification you need from the user.
- **Meaning**: Explain clearly what the terms in the question actually mean **in the context of the design**.
</HARD-GATE>

Before writing the spec, proactively resolve ambiguities and fill gaps through muti-round conversations:
- Identify unclear requirements or open decisions; ask focused questions to clarify.
- Detect missing information critical to the design (e.g., constraints, stakeholders, success metrics); request it explicitly.
- For every question, present **three** options with a recommended choice clearly marked.

## What spec documents contain

<HARD-GATE>
The spec document **MUST** be concise, well-structured, and easy for humans to review.
</HARD-GATE>

<HARD-GATE>
Keep the spec focused and avoid unnecessary verbosity. **DO NOT** be too long or too noisy to review.
</HARD-GATE>

<HARD-GATE>
Avoid industry-uncommon jargon and specialized terminology. Prefer plain, widely-understood language.
</HARD-GATE>

<HARD-GATE>
When a technical term must be used, define it explicitly on first use with:
- **Origin**: Why this name was chosen.
- **Definition**: What the term means precisely.
- **Usage**: How the term is applied in context.
</HARD-GATE>

### 0. Context & Goals

- State the **problem** this design solves and the **motivation** behind it.
- Define **goals**: What this design aims to achieve.
- Define **non-goals**: What is explicitly out of scope.

### 1. Top-level Design Decisions

- Explain the **architecture** of the design (style, patterns, key trade-offs).
- Explain the **components** of the design and their responsibilities.
- Explain the **interfaces** between components (contracts, protocols).
- Define the core **data model** (entities, relationships, state machine if applicable).
- Give a **flow diagram** of the design using Mermaid syntax.
- Give a **dir tree** of the design showing the target file structure.

### 2. Constraints & Assumptions

- List **technical constraints** (e.g., runtime environment, dependencies, API limits).
- List **business constraints** (e.g., compliance requirements).
- List **assumptions** the design relies on (may become risks if invalidated).

### 3. Detailed Design

- Break down the design into smaller modules.
- Explain the **mechanisms** of each module (how it works internally).
- Explain the **dependencies** between modules.
- Define the **error handling strategy** (error classification, retry, fallback, degradation paths).
- Describe **configuration management** (what is configurable, default values, env vs file).

### 4. Non-functional Requirements

- Explain **performance** targets (latency, throughput, resource budgets) and how they will be achieved.
- Explain **security** considerations (authz, data protection, attack surface).
- Explain **reliability** (fault tolerance, graceful degradation, recovery).
- Explain **observability** strategy (logging, metrics, tracing).
- Address **compatibility** (backward compatibility, migration path, versioning).

### 5. Unit Test Strategy (mandatory in specs)

This section is what `harness-kit:tdd` reads to drive the inner Red-Green-Refactor loop (the inner counterpart of the E2E outer loop). Group scenarios by the modules defined in Section 3 (Detailed Design); within each module list `UT-N` Given/When/Then bullets that name an **observable behavior**, not an implementation detail.

### 6. E2E Strategy Section (mandatory in specs)

This section is what `harness-kit:plan` reads to decide whether to schedule Outside-In tasks via `harness-kit:e2e`.

## Output Spec Documents

Output two files into `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/` dir:

- `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/design.md`
- `{$PROJECT_ROOT_DIR}/harness-kit/specs/<subject-YYYY_MM_DD>/test-category.md`

**Template**:
Refer to `reference/spec.guideline.md` in this skill directory.
