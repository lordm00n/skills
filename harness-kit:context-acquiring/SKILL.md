---
name: harness-kit:context-acquiring
description: Acquire strict, task-specific project context for the `harness-kit` project — read `.agents/rules.md`, `.agents/local-docs-index.md`, `.agents/remote-docs-index.md`, and `~/wikis/index.md` with progressive disclosure, then produce a self-contained context document at `docs/harness-kit/context/YYYY-MM-DD-<topic>.md`. Use this skill whenever the user explicitly asks for "harness-kit context", asks you to acquire / read / update project context, starts a multi-step harness-kit task (planning, designing, implementing), or another harness-kit skill (e.g. `harness-kit:start`, `harness-kit:brainstorm`, `harness-kit:writing-plans`) says project context is required. Do NOT use it for isolated one-off questions that do not need project rules or docs.
---

# Acquire Harness Kit Project Context

This skill produces **one** deliverable: a tightly-scoped, task-specific context document at `docs/harness-kit/context/YYYY-MM-DD-<topic>.md`. Downstream skills (`harness-kit:brainstorm`, `harness-kit:writing-plans`, etc.) read that document instead of re-discovering project context themselves, so it must be self-contained.

The four sources you draw from:

- `{$PROJECT_ROOT_DIR}/.agents/rules.md` — non-negotiable constraints
- `{$PROJECT_ROOT_DIR}/.agents/local-docs-index.md` — index of in-project docs
- `{$PROJECT_ROOT_DIR}/.agents/remote-docs-index.md` — external docs, each with a `description` and a `way_to_read`
- `~/wikis/index.md` — cross-project local knowledge base

## Required Outcome

A single markdown file at `docs/harness-kit/context/YYYY-MM-DD-<topic>.md` that:

1. States the task this context supports, so the document stands alone.
2. Lists every rule from `.agents/rules.md` that constrains the task, with citations.
3. Includes **excerpts** (not just links) from each in-project doc, remote doc, and wiki entry that are actually relevant to the task.
4. Explicitly notes any gaps — missing docs, ambiguous requirements, conflicts — so the next skill knows what to ask.
5. Cites a source for every excerpt: file path with line range, or URL.

Quality over breadth: three on-topic excerpts beat twenty marginal ones. The next skill should be able to act on this document **without re-reading any of the four source indexes**.

**What counts as a citable doc** — only docs you *discovered by walking an index* and that the next skill would not otherwise see. Explicitly **exclude**:

- The four index / meta files themselves (`.agents/local-docs-index.md`, `.agents/remote-docs-index.md`, `.agents/rules.md`, `~/wikis/index.md`). They are this skill's inputs. (Substantive content from `rules.md` belongs in the **Hard Rules** section, not in **In-Project Docs**.)
- Docs the user already attached to the request — anything `@`-mentioned, pasted in the prompt, or visible in `<attached_files>` / `<open_and_recently_viewed_files>` (e.g. a PRD under `docs/prds/`). The downstream skill already has these.
- Docs the host system loads by default — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, files under `.cursor/rules/`, and anything surfaced via `<always_applied_workspace_rules>`.

These are already in the next skill's working set; re-citing them just inflates the document and dilutes the signal.

## Strict Workflow

### 1. Analyse The Request

Before opening any source file, extract:

- **Topic** — a short kebab-case slug used in the filename (e.g. `init-cli`, `template-rendering`).
- **Goal** — one sentence: what is the user trying to accomplish?
- **Keywords** — 3–7 nouns / concepts to filter docs against (e.g. `cli`, `cobra`, `template`, `init`).
- **Task type** — feature, bugfix, refactor, research, etc.

If the request is too vague to extract these reliably, ask **one** targeted clarifying question before proceeding. Do not guess at a topic — the slug becomes the filename and is hard to undo.

Write these four items into a TodoWrite list (or scratch note) and refer back to them throughout the next steps.

### 2. Apply Progressive Disclosure

Always read `rules.md` in full first — it's short, absolute, and frames everything else. Then drill into the other three index files **only as deep as your keywords from step 1 require**. Do not pre-load entire doc trees.

**For the development rules** (read first, in full):

1. Read every line of `{$PROJECT_ROOT_DIR}/.agents/rules.md`. The file is short by design.
2. Mark which rules apply to the current task. A rule that constrains a tech choice (e.g. "use cobra") applies to anything that touches that area, even if the user did not name the tech.
3. Carry every applicable rule into the output document — these are non-negotiable.

**For the in-project local docs**:

1. Read `{$PROJECT_ROOT_DIR}/.agents/local-docs-index.md` to see which sub-index files it lists.
2. For each sub-index whose subject matches your keywords, read it.
3. From those sub-indexes, follow links into concrete doc files only when they map to your keywords.
4. **Filter out already-known docs** before deciding what to cite. Drop any doc that is:
   - The index file itself (`local-docs-index.md` or any sub-index — you used them to navigate, not to cite).
   - Already attached by the user (visible in the user's prompt, `@`-mentions, `<attached_files>`, or `<open_and_recently_viewed_files>`). PRDs under `docs/prds/` are the typical case.
   - Loaded by the host by default (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/*`, `<always_applied_workspace_rules>` content).

   Read these freely if they help your own understanding, but do not include them in the output. The downstream skill already has them.
5. If `local-docs-index.md` lists nothing yet (the file may exist but be effectively empty), record that fact in the output and move on — do not fabricate.

**For the remote docs**:

1. Read `{$PROJECT_ROOT_DIR}/.agents/remote-docs-index.md` to see every entry's URL, `description`, and `way_to_read`.
2. Match each entry's `description` against your keywords. Skip entries that don't match.
3. For each matching entry, fetch its content using **exactly** the method named in `way_to_read`. For example, when `way_to_read` is `Use ` + "`gh`" + ` cli to read the content` and the URL points at a file in a GitHub repo, use:

   ```bash
   gh api "/repos/<owner>/<repo>/contents/<path>" -H "Accept: application/vnd.github.raw"
   ```

   If `way_to_read` names a different tool (e.g. WebFetch, curl), use that tool instead. The field is authoritative — do not substitute.
4. Extract only the sections that match your keywords. Do not paste the whole document into the output.

**For the outside-project local wikis**:

1. Read `~/wikis/index.md` to see what categories exist (each row in the "分类文档" table is a category with its own `index.md`).
2. For each category whose name or description matches your keywords, read its `index.md` (e.g. `~/wikis/env/index.md`).
3. From that sub-index, drill into specific docs only when they map to your keywords.
4. If no category matches, note this in the output and move on.

### 3. Verify Context Completeness

Before writing the output document, run this four-point check:

1. **Coverage** — for each keyword from step 1, can you point to at least one source (rule, doc, or wiki) you've read? If not, list the keyword as a gap.
2. **Conflict** — do any rules contradict an approach the docs suggest? If so, the rule wins; record the conflict under "Open Questions / Gaps" so downstream skills don't re-discover it.
3. **Self-containment** — could a teammate who has never seen the source files act on this document alone? If not, copy more excerpt content into the relevant section.
4. **Strictness** — re-read each excerpt: does it actually serve the task, or did you include it because it was nearby? Cut anything off-topic. A bloated context document defeats the point of this skill.

If a critical gap would block the next skill from making real decisions, ask the user one targeted question rather than shipping a thin document.

## Output Template

Save the document to `docs/harness-kit/context/YYYY-MM-DD-<topic>.md`. Replace every placeholder. Keep the section headings verbatim so downstream skills can parse them.

````markdown
# Context: <topic>

> Produced by `harness-kit:context-acquiring` on <YYYY-MM-DD>
> Source request: <one-sentence summary of what the user asked for>

## Task Summary

<2–3 sentences: goal, scope, success criteria. Must stand alone — assume the reader has not seen the original request.>

## Keywords

`<keyword-1>`, `<keyword-2>`, `<keyword-3>`

## Hard Rules (must obey)

| # | Rule | Source |
|---|------|--------|
| 1 | <verbatim or tightly-paraphrased rule text> | `.agents/rules.md:<line>` |

> Only list rules that apply to this task. If a rule does not apply, omit it. If no rules apply, write: "_No rules from `.agents/rules.md` constrain this task._"

## In-Project Docs

> Only docs **discovered via `.agents/local-docs-index.md`** belong here. Do **not** cite the index file itself, docs the user already attached (e.g. PRDs under `docs/prds/`, `@`-mentioned files), or host-default docs (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*`).

### <doc title>

- Source: `<relative/path/to/file.md>` (lines `<start>-<end>`)
- Why relevant: <one sentence>

<verbatim excerpt or tight summary>

> If no in-project docs apply, write: "_No in-project docs applied to this task._"

## Remote Docs

### <doc title>

- URL: <url>
- Fetched via: `<the exact command you ran, derived from way_to_read>`
- Why relevant: <one sentence>

<verbatim excerpt of the relevant section>

> If no remote docs apply, write: "_No remote docs applied to this task._"

## Wiki References

### <wiki title>

- Source: `~/wikis/<path>`
- Why relevant: <one sentence>

<verbatim excerpt or tight summary>

> If no wiki entries apply, write: "_No wiki entries applied to this task._"

## Open Questions / Gaps

- <gap 1: what's missing, and what would unblock it (a doc to read, a question to ask the user, a decision to make)>

> If there are no gaps, write: "_None._"

## Hand-Off

This context is ready for the next skill (typically `harness-kit:brainstorm` or `harness-kit:writing-plans`). Downstream skills should read this document in full before proceeding.
````

## Anti-Patterns

- **Dumping the whole file** — pasting an entire README forces the next skill to re-filter. Extract only the excerpts the task needs.
- **Re-citing already-known docs** — index files (`local-docs-index.md`, etc.), user-attached docs (e.g. a PRD under `docs/prds/`, `@`-mentioned files), and host-default docs (`AGENTS.md`, `.cursor/rules/*`) are already in the next skill's context. Citing them again wastes tokens and dilutes the signal. Use them to navigate, not to cite.
- **Skipping rules** — `rules.md` is short and absolute. Always read every line.
- **Ignoring `way_to_read`** — the field is authoritative. Don't swap `gh` for WebFetch (or vice-versa) because it feels easier.
- **Inventing content** — if a doc index is empty or a remote URL is unreachable, record that gap. Do not paper over it with plausible-sounding text.
- **Restating the user's prompt** — the Task Summary must add information (scope, success criteria, constraints), not echo the request.
- **Reading the codebase** — that's the brainstorming skill's job. This skill reads docs and rules only.

## Example File Path

For a request like "add an `init` subcommand to the CLI" on 2026-04-28, the output goes to:

```
docs/harness-kit/context/2026-04-28-init-cli.md
```
