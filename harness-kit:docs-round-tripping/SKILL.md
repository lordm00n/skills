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

### Step2: Detect drift across the whole docs list (batched, read-only)

> Source-of-truth principle for this skill: **the shipped code is the source of truth, docs are reconciled to match the code.** In this step you only read; you do not edit anything.

> Why batch the detection: reading every doc and its referenced code up front gives you full cross-doc context (e.g. two docs describing the same module), avoids re-reading the same source files multiple times, and lets you build an accurate picture before bothering the user. The approval / edit / re-verify cycle is where we slow down and go per-doc (Step 3).

Using the docs list from Step 1:

1. **Read every doc in the list.** For each one, extract every **claim it makes about the codebase**, including but not limited to:
   - the feature / behavior the doc describes
   - file paths, modules, classes, functions, components it references
   - public APIs, data shapes, configuration keys, CLI flags it defines
   - architectural decisions, constraints, and trade-offs it records
2. **Locate the corresponding code for every claim.**
   - If the doc explicitly references file paths or symbols, read those files directly.
   - Otherwise, use semantic search / grep / glob to find the implementation that matches the described feature.
   - If you still cannot find any related code for a given claim, mark that claim as `unverifiable` — do **not** guess.
   - You may read code files referenced by multiple docs only once and reuse the result; reading order is up to you.
3. **Compare claim-by-claim** — what the doc says vs. what the code actually does — and classify every item into one of:
   - **aligned** — doc still matches the code (record this too, so we know what is verified)
   - **out-of-date** — doc and code disagree on the same item; code is the source of truth
   - **missing-in-doc** — code has behavior / API / file that the doc does not mention
   - **missing-in-code** — doc describes something that no longer exists in the code (removed, renamed, or never built)
4. **Build an internal drift map keyed by `doc_path`.** For each doc store:
   - `verified`: list of aligned items
   - `drifts`: list of `{ category, doc_excerpt, code_evidence (file path + line range), note }`

   This map is what Step 3 consumes. Keep it **in the chat conversation only** (as your working notes). Do **not** write it to any file, and do **not** dump the full map to the user yet — the detailed per-doc breakdown belongs to Step 3 where it is tied to an approval request.
5. **Output only a short scan overview** in the chat reply, so the user can see scope without being buried. The overview should be compact and include at minimum:
   - total docs scanned
   - docs with drift (list their `doc_path` plus per-category counts, e.g. `out-of-date: 2, missing-in-doc: 1`)
   - docs that are fully `aligned` (just the paths)
   - docs / claims marked `unverifiable` (with a one-line reason each)

   Do **not** include `doc_excerpt`, `proposed doc text`, or other per-item details in the overview — they come in Step 3, one doc at a time.

**Hard constraints for this step:**
- Do **not** modify any doc or any code.
- Do **not** create, write, or append to any file (no `.md`, no `.json`, no scratch notes on disk). Everything stays in the chat conversation.
- Do **not** ask the user to approve fixes yet — Step 2 is purely diagnostic.
- Fixing the drift belongs to Step 3.

### Step3: Reconcile docs one at a time (interactive per-doc loop)

> Interaction shape: the user sees **at most one doc's worth of proposed changes at a time.** Even though Step 2 already has the full picture, you walk through docs with drift one by one and only reveal the full detail + ask for approval on the current doc.

Iterate the docs from the Step 2 drift map in the **original Step 1 order**. Skip docs whose entries are fully `aligned` (they need no user interaction — mention them briefly only if it helps the user track progress). For each remaining doc, do the following **in order** and **finish it before moving to the next doc**:

1. **Present this doc's full drift report** in the chat reply, straight from the Step 2 drift map:
   - `doc_path`
   - `verified`: list of aligned items (keep this short; it's context, not the ask)
   - `drifts`: list of `{ category, doc_excerpt, code_evidence (file path + line range), note }`

2. **Propose doc-side fixes for this doc.** For every non-`aligned` item, propose a fix according to its `category`:
   - **out-of-date** → rewrite the affected doc passage so it describes the current code behavior. Cite the `code_evidence` (file path + line range) so the doc stays auditable.
   - **missing-in-doc** → add a new passage to the doc that describes the new code behavior. Place it so it follows the doc's existing structure / heading hierarchy; do **not** restructure unrelated sections.
   - **missing-in-code** → do **not** silently delete from the doc. Ask the user **as part of this doc's approval step** whether this is:
     - **(a) intentional removal** → remove the passage from the doc (and, if the doc has a changelog-style section, append a one-line "removed: <reason>" entry).
     - **(b) regression** → leave the doc untouched and record this as a **code-side issue** to surface in the final report. This skill must not fix code.
   - **unverifiable** → skip; carry it forward so it shows up in the final report.

   For each proposed fix show:
   - `doc_path`
   - `category`
   - `current doc text` (the exact excerpt that will be replaced)
   - `proposed doc text` (the exact replacement)
   - `code_evidence` (file path + line range that justifies the change)

3. **Ask for approval for this doc only, then wait.** Do not touch any file, and do not reveal the next doc's proposals, until the user replies about **this** doc. The user may, for this doc:
   - approve all,
   - approve a subset (by item index),
   - reject,
   - ask you to revise specific proposed texts — in which case loop back to point 2 with revised proposals **for this same doc**,
   - or tell you to stop the whole run — in which case jump to Step 4 with whatever has been processed so far.

4. **Apply only the approved edits to this doc.**
   - Edit **only** this doc file (must be in the Step 1 list).
   - Use targeted edits (e.g. `StrReplace`) on the exact `current doc text`; do **not** rewrite whole files.
   - Do **not** touch any source code, config, or test file.
   - Do **not** create new docs unless the user explicitly asked for it.
   - Do **not** "improve", reformat, or refactor parts of the doc that were not in the approved fix list.

5. **Re-verify this doc immediately.**
   - Re-read the edited doc.
   - For every item that was approved + applied, confirm the doc now matches the `code_evidence`.
   - If any approved item still drifts, report it back to the user for this doc and **stop the loop** — do not retry blindly and do not silently continue to the next doc.

6. **Record outcomes for this doc** (in chat, no file output) so the final report in Step 4 can reconstruct `applied` / `skipped` / `code_side_issues`. Then continue with the next doc.

**Hard constraints for this step:**
- Reveal and request approval for **one doc at a time**; never batch proposals or approvals across multiple docs.
- Step 2's drift map may have been built in one pass, but user-facing output in Step 3 must still flow doc-by-doc.
- If while proposing fixes for a doc you notice the Step 2 findings for it are wrong or incomplete, re-read that doc and its code *for that doc only*, update the drift map entry, and continue — do not redo the whole Step 2 scan, and do not silently drop findings.
- Edit **only** docs from the Step 1 list. Never edit code.
- Never apply any fix before the user approved it for that specific doc.
- Never silently widen the change set beyond the approved items.
- All drift reports, proposed fixes, and outcomes live **only** in the chat reply — no `.md`, no `.json`, no scratch notes on disk.

### Step4: Final reconciliation report

After the per-doc loop finishes (either because every doc with drift has been processed, or because the user told you to stop, or because re-verification failed on a doc), output a single **final reconciliation report** in the chat reply (no file output). It must contain:
- `applied`: list of `{ doc_path, category, summary }` for fixes that were applied and re-verified in Step 3.
- `skipped`: items the user did not approve, plus all `unverifiable` items, plus any docs that were not reached because the run was stopped early.
- `code_side_issues`: every `missing-in-code` item the user marked as a regression — these are **handed back to the user** as follow-up work outside this skill.

This report is purely a recap of what Step 3 already did; it must not introduce new edits or new approvals.
