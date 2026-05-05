# Spec Document: <subject>

**Date**: YYYY-MM-DD
**Status**: Draft | Under Review | Approved | Superseded
**Author**: <name>

---

## Writing Rules (apply to every section of this document)

These rules apply to the spec body, the Glossary, **and** the companion `test-category.md`. They exist so that a human reviewer can scan the document once and tell whether it's right.

1. **Plain language.** Write what the system does and why, in everyday words. Ban decorative phrasing — both English ("canonical home", "wiring", "hardness", "first line of defense", "the contract is upheld") and Chinese ("守住契约", "兜底", "断网", "红线", "第一道闸"). If a fancy word is the only way to express an idea, rewrite the idea, not the word.
2. **Reviewer-friendly layout.** Prefer short sentences and bullets over dense paragraphs. Tables are fine. Code blocks are fine. Walls of prose that pack three facts into one sentence with commas, or that mix narrative text with stacked backticked identifiers, are not.
3. **Names are introduced once, in the spec body.** Every term used anywhere in this document or in `test-category.md` must first appear, with its meaning, in the prose or tables of this spec. Do not introduce names inside test cases or inside the Glossary itself.
4. **Cite goals, decisions, and sections by their full name.** Inside this document and inside `test-category.md`, cite the protected item the way the spec spells it: write `Goal G<N> (<full goal text from §0>)`, not `G<N>` alone; write `the decision in §<N>.<X> to <short paraphrase>`, not the decision-table cell ID alone. Abbreviations that require flipping back to look up are rejected.
5. **Don't promote obvious names into the Glossary.** See the Glossary rules at the bottom of this template.

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

#### Rules for Glossary entries

The Glossary is for terms whose meaning is **non-obvious or contested in the context of this spec**. It is not a directory of every named thing in the document.

**Include a term only if all three are true**:

1. The term carries a meaning specific to this design that a careful reader of the spec body would *not* be sure of from the name plus surrounding prose.
2. Getting the meaning wrong would change how someone implements, tests, or reviews the feature.
3. The term appears in the spec body (or `test-category.md`) at least once. If you find yourself adding an entry for a term that doesn't appear in the prose, delete it — or move the term into the prose first.

**Do NOT include**:

- **Self-evident names.** If a fluent reader of the spec body can guess the meaning from the name plus one nearby line of prose, skip. The module section that introduces the name is enough.
- **Universally understood terms.** Anything in a reasonable engineer's working vocabulary for the surrounding ecosystem (transport protocols, file formats, common framework primitives, well-known data structures).
- **Internal implementation labels.** Variable names, file names, fixture names, CSS class names, and similar local identifiers. These belong in the module section that owns them.
- **Address-as-term.** Decision IDs, Goal IDs, scenario IDs, or section numbers. These are addresses for navigation, not vocabulary.
- **Restated requirements.** An entry whose Definition just paraphrases what the spec body already said in plain words is noise.

**For each entry that does belong**:

- **Origin**: One line on naming rationale — why this name over the alternatives, or what the name was lifted from. Omit if obvious.
- **Definition**: Precise meaning, including what it is *not* when the boundary is contested. One short paragraph.
- **Usage in this design**: How this term is applied here specifically — which decisions or components hinge on it. Not a generic definition.
- **Scope**: Which sections / modules use the term. Helps the reviewer locate every place the meaning matters.
- **Example**: One concrete instance grounded in this design. Omit when the definition itself is concrete enough.

**Anti-pattern entries to delete**:

- **Name-restating entry.** The entry's Definition is something a fluent reader would already infer from the name (e.g. a type whose body is just `<NounPhrase>` and whose entry says "an instance of `<NounPhrase>`"). Delete — the module section that introduces the name is enough.
- **Generic-concept entry.** The entry explains a widely understood pattern from the surrounding ecosystem (a common framework idiom, a standard data-structure name, a textbook algorithm). If the spec uses it in a non-standard way, document the variation inline in the relevant module section; if it doesn't, no entry is needed.
- **Fixture / asset entry.** Test fixture files, sample data files, or other assets used only for setup. Document these in the test plan or in the module section that owns them.
- **Code-shape entry.** The entry mostly describes the literal type signature or field list. The reader can read the signature in the module section; the Glossary is for meaning, not shape.
- **Address-as-term entry.** Decision IDs, Goal IDs, scenario IDs, or section numbers in the format your spec uses (such as `G<N>`, `Q<N><a-z>`, `AS-<N>`, `§<N>.<X>`). These are addresses for navigation — not vocabulary.
