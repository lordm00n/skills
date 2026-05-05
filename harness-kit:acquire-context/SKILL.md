---
name: harness-kit:acquire-context
description: Acquire strict context from documents in .agent/ directory of the current project and local wikis, then then produce a self-contained context document. Call this skill when user explicitly signals that you need to output a context document. Do NOT use for isolated one-off questions that don't need project rules or docs.
---

# Acquire Context

**Goal**: Produce a self-contained context document for `harness-kit:spec-design` skill.

## What the context document contains

**Top level summary**:
Main four sections:
1. project internal docs that are relevant to the user requirement.
2. remote docs that are relevant to the user requirement.
3. project rules that are relevant to the user requirement.
4. local wikis that are relevant to the user requirement.

<HARD-GATE>
The context document must contains the **concrete content** of the docs that are relevant to the user requirement, not just the path or description of the docs.
</HARD-GATE>

### Project Internal Docs

**Entry file**: {$PROJECT_ROOT_DIR}/.agents/local-docs-index.md

**Start with the entry and follow the instructions below**:

- Read the entry file to get a list of **directories** that contain project internal docs.

- Each of the directories contains a **index.md** file that reveal the structure of the directory.

- **Progressively disclose** the deeper levels of the directories to read the concrete docs content that are **relevant to the user requirement**.

**A few shot for the instructions**:

For example, the entry file contains a directory called `docs` that contains project internal docs: 

```markdown
docs/
├── index.md
├── sub-docs/
│   ├── example.md 
│   ├── index.md
```

- The index.md located at `docs/index.md` reveals the structure/description of the whole `docs` directory.

- The index.md located at `docs/sub-docs/index.md` reveals the structure/description of the `sub-docs` directory.

- You may read the `docs/index.md` first, then hop to the `docs/sub-docs/index.md` to get the structure/description of the `sub-docs` directory. Then read `docs/sub-docs/example.md` to get the **concrete** content of the `example.md` file (Under the premise that the `example.md` file is relevant to the user requirement).

### Remote Docs

**Entry file**: {$PROJECT_ROOT_DIR}/.agents/remote-docs-index.md

**Start with the entry and follow the instructions below**:

- Read the entry file to get a list of **remote doc items** that contain remote docs.

- Each of the remote doc item contains 
  - a **URL** that points to the remote doc.
  - a **description** field of the remote doc.
  - a **way_to_read** field of the remote doc.

- Follow the **way_to_read** to read the concrete web content that are **relevant to the user requirement** (According to the **description** field).

### Project Rules

**Entry file**: {$PROJECT_ROOT_DIR}/.agents/rules.md

- Read the entry file to get a list of **project rules** that you must obey during development.

### Local Wikis

**Entry file**: ~/wikis/index.md

**Start with the entry and follow the instructions below**:

- The **progressive disclosure** process is the same as the one in **Project Internal Docs** section.

## Output context document

**File name**: `{$PROJECT_ROOT_DIR}/harness-kit/context/<subject>-YYYY_MM_DD.context.md`

If there is no relevant content in any of the sections above, anounce in the template below that there is no relevant content for that section: 

```markdown
## 1. Project Internal Docs

_No in-project docs applied to this task._

<reason for no relevant content>
```

**Template**:
```markdown
# Context Document: <subject>

> Produced by `harness-kit:acquire-context` skill.
> Generated at: YYYY-MM-DD HH:MM:SS
> Requirement: <brief description of user requirement>
> Related PRD: <PRD path if there is one referenced by the user>
---

## 1. Project Internal Docs

> Source: {$PROJECT_ROOT_DIR}/.agents/local-docs-index.md

### 1.1 <Doc Category Name>

**Source**: `path/to/doc/index.md` or `path/to/doc/file.md`

<Relevant content from the project internal docs>
<Include only content that is directly relevant to the user requirement>

### 1.2 <Another Doc Category>

**Source**: `path/to/another-doc/file.md`

<Relevant content>

---

## 2. Remote Docs

> Source: {$PROJECT_ROOT_DIR}/.agents/remote-docs-index.md

### 2.1 <Remote Doc Title>

**Source URL**: <url>
**Description**: <what this remote doc covers>
**Way to Read**: <method used to fetch content>

<Relevant content extracted from the remote doc>
<Summarize or quote key information relevant to the requirement>

### 2.2 <Another Remote Doc>

**Source URL**: <url>
**Description**: <description>
**Way to Read**: <method>

<Relevant content>

---

## 3. Project Rules

> Source: {$PROJECT_ROOT_DIR}/.agents/rules.md

### 3.1 <Rule Category or Name>

<The actual rule text>
<Include rules that are relevant to the current requirement>

### 3.2 <Another Rule>

<Rule text>

---

## 4. Local Wikis

> Source: ~/wikis/index.md

### 4.1 <Wiki Category/Topic>

**Source**: `~/wikis/path/to/wiki/file.md`

<Relevant wiki content>
<Include wiki entries that provide context for the requirement>

### 4.2 <Another Wiki Topic>

**Source**: `path/to/wiki/file.md`

<Relevant content>

---

## Summary

<Brief summary of key points from all sections that are most critical for the user requirement>
```

## Usage Notes

1. **Relevance Filtering**: Only include content that is directly relevant to the user's specific requirement
2. **Progressive Disclosure**: For large doc sets, use the index files to navigate and extract only what's needed
3. **Self-Contained**: The context document should be complete enough that someone can understand the requirement context without accessing the original sources
4. **Timestamps**: Always include generation time for traceability
5. **Source Attribution**: Clearly mark where each piece of information came from
6. **Reason for No Relevant Content**: If there is no relevant content in any of the sections above, anounce in the template below that there is no relevant content for that section.
