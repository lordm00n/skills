---
name: harness-kit:docs-round-tripping
description: Reconcile existing spec/plan/design docs with the current codebase after implementation drift, so the written intent matches the shipped code. Trigger whenever the user signals that docs are stale relative to code—even implicitly. Typical cues include: finishing a spec/plan-driven task then vibe coding on top of it, "I manually tweaked the implementation", "the result wasn't satisfying so I changed it directly", "docs/specs are out of date", "docs 和代码不一致了", "把文档和代码同步一下", "回填 spec/plan", "round-trip the docs", "align docs with implementation". Do NOT trigger for writing fresh docs from scratch, for pure code-only changes, or when no prior spec/plan exists.
---

# Harness Kit Docs-round-tripping

When user use  spec/plan-driven AI development workflow like, they might be not satisfied with the result and they want to vibe-coding based on it or manually changed the code.

Your responsibility is to reconcile existing spec/plan/design docs with the current codebase after this kind of **implementation drift**.

## User Input

> The user input is a list of **directory paths** and **file paths** as below:

```text
$ARGUMENTS
```

## Working Process

> You **must** follow the instrctions below **step by step**

### Step1: Construct a file list from user input

Get the directory path and file path user mentioned from arguments:

- If user provide a directory, list all the docs in this directory.
- If user provide a file, just add the file path into the list.
- **At last**: list all the file paths you parse from the user input.

### Step2: Compare the docs content and the current codebase

Through Step1, you get a list of docs, then:

1. Start a loop for the docs list.
2. For each doc, do the following **in order**:
   1. Read the full doc content and extract every **claim it makes about the codebase**, including but not limited to:
      - the feature / behavior the doc describes
      - file paths, modules, classes, functions, components it references
      - public APIs, data shapes, configuration keys, CLI flags it defines
      - architectural decisions, constraints, and trade-offs it records
   2. Locate the corresponding code:
      - If the doc explicitly references file paths or symbols, read those files directly.
      - Otherwise, use semantic search / grep / glob to find the implementation that matches the doc's described feature.
      - If you still cannot find any related code, mark the doc as `unverifiable` and move on — do **not** guess.
   3. Read the **current** implementation of the located code (read the actual files, do not rely on memory).
   4. Compare claim-by-claim — what the doc says vs. what the code actually does — and classify every item into one of:
      - **aligned** — doc still matches the code (record this too, so we know what is verified)
      - **out-of-date** — doc and code disagree on the same item; code is the source of truth
      - **missing-in-doc** — code has behavior / API / file that the doc does not mention
      - **missing-in-code** — doc describes something that no longer exists in the code (removed, renamed, or never built)
   5. Output a **per-doc drift report** **directly in the chat reply** (do **not** write it to any file, do **not** create any temporary / draft / scratch file). The report must use this structure:
      - `doc_path`
      - `verified`: list of aligned items
      - `drifts`: list of `{ category, doc_excerpt, code_evidence (file path + line range), note }`
3. After the loop ends, aggregate every per-doc drift report into a single **drift summary** and present it **in the chat reply only**. The summary must:
   - group findings by `doc_path`
   - highlight all non-`aligned` items first
   - keep the original `doc_excerpt` and `code_evidence` so the user can audit each finding
4. **Hard constraints for this step:**
   - Do **not** modify any doc or any code.
   - Do **not** create, write, or append to any file (no `.md`, no `.json`, no scratch notes on disk). All output of Step 2 lives **only** in the chat conversation.
   - Fixing the drift belongs to Step 3.

### Step3: Fix the drift

> Source-of-truth principle for this skill: **the shipped code is the source of truth, docs are reconciled to match the code.** Only docs are edited in this step; code is **never** edited.

Use the drift summary from Step 2 as input. Then:

1. For every non-`aligned` item, propose a doc-side fix according to its `category`:
   - **out-of-date** → rewrite the affected doc passage so it describes the current code behavior. Cite the `code_evidence` (file path + line range) so the doc stays auditable.
   - **missing-in-doc** → add a new passage to the doc that describes the new code behavior. Place it so it follows the doc's existing structure / heading hierarchy; do **not** restructure unrelated sections.
   - **missing-in-code** → do **not** silently delete from the doc. Ask the user explicitly whether this is:
     - **(a) intentional removal** → remove the passage from the doc (and, if the doc has a changelog-style section, append a one-line "removed: <reason>" entry).
     - **(b) regression** → leave the doc untouched and surface this as a **code-side issue** in the final report. This skill must not fix code.
   - **unverifiable** → skip; just list it in the final report so the user knows it was not auto-fixed.
2. Present **all** proposed fixes to the user **in the chat reply** before touching any file. For each fix show:
   - `doc_path`
   - `category`
   - `current doc text` (the exact excerpt that will be replaced)
   - `proposed doc text` (the exact replacement)
   - `code_evidence` (file path + line range that justifies the change)
3. **Wait for explicit user approval.** Do not start editing until the user replies. The user may:
   - approve all,
   - approve a subset (by `doc_path` and/or by item index),
   - reject,
   - or ask you to revise specific proposed texts — in which case loop back to point 2 with the revised proposals.
4. After approval, apply only the approved edits:
   - Edit **only** files that appear in the docs list from Step 1.
   - Use targeted edits (e.g. `StrReplace`) on the exact `current doc text`; do **not** rewrite whole files.
   - Do **not** touch any source code, config, or test file.
   - Do **not** create new docs unless the user explicitly asked for it.
   - Do **not** "improve", reformat, or refactor parts of the doc that were not in the approved fix list.
5. Run a **re-verification pass**:
   - Re-read each edited doc.
   - For every drift item that was approved + applied, confirm the doc now matches the `code_evidence`.
   - If any approved item still drifts, report it back to the user and stop — do not retry blindly.
6. Output a **final reconciliation report** in the chat reply (no file output). It must contain:
   - `applied`: list of `{ doc_path, category, summary }` for fixes that were applied and re-verified.
   - `skipped`: items the user did not approve, plus all `unverifiable` items.
   - `code_side_issues`: every `missing-in-code` item the user marked as a regression — these are **handed back to the user** as follow-up work outside this skill.
7. **Hard constraints for this step:**
   - Edit **only** docs from the Step 1 list. Never edit code.
   - Never apply any fix before the user approved it.
   - Never silently widen the change set beyond the approved items.
