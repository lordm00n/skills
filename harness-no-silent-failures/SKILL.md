---
name: harness-no-silent-failures
description: "Ensure no user action ever fails silently. Use this skill whenever you build, add, or modify any user-facing feature — pages, components, forms, uploads, editors, lists, search, payment, import/export, or any API-backed interaction — even if the user never mentions edge cases, error handling, or UX. Also use it when reviewing or fixing UI code that might swallow errors. It forces an inventory of what is supported / not supported / limited, and adds mainstream, friendly feedback (prevention hints, inline errors, toasts, dialogs, empty states, retry) for every boundary a user can hit."
---

# No Silent Failures

## The one principle

**Every user action must produce visible, understandable, recoverable feedback. Nothing a user can do should result in: nothing happening, a spinning loader forever, a mysteriously grey button, cleared input, or a raw error code.**

Users hit boundaries the designer didn't think about: an unsupported file, one item too many, an expired session, a duplicate name, no permission, no network. If the code has no branch for it, the user blames themselves or abandons the product. Your job is to find those branches *before* the user does and give each one a face.

This is not "add more toasts." Good boundary UX, following mainstream design systems (Material Design, Apple HIG, Ant Design) and Nielsen's heuristics #1 (visibility of system status), #5 (error prevention), #9 (help users recognize, diagnose, and recover from errors), has an order:

1. **Prevent** — make the constraint visible before it can be violated
2. **Explain at the moment** — if violated anyway, say what + why + what to do next, right where it happened
3. **Recover** — always offer a next step; never dead-end, never destroy the user's work

## When you are writing or modifying user-facing code

Do these five steps. Do not skip step 1 because the user "didn't ask for it" — that is exactly when this skill matters.

### Step 0 — Reuse what the project already has

Before inventing anything, look at the codebase:

- Find the existing feedback components: toast/snackbar, modal/dialog, alert/banner, empty-state, loading/skeleton, form-error. Use them. A second, home-made toast system is worse than an imperfect consistent one.
- Find the existing copy tone and i18n mechanism. New messages go through the same i18n keys / locale files if the project has them — never hard-code a lone string in a localized app.
- Find existing limits and validators (API schemas, constants, backend error codes) before assuming any limit yourself.

### Step 1 — Build the boundary inventory (think, then code)

For the feature you are about to write, enumerate — at least mentally, and in your final report for non-trivial features — three lists:

| List | Question to ask |
|---|---|
| **Supported** | What formats / values / counts / roles / devices does this *actually* accept? |
| **Not supported** | What will a user plausibly *try* that this does not accept? |
| **Limits** | Max size, count, length, rate, quota, timeout — and what happens at 100%, and at 80%? |

Then walk every user-reachable entry point against the full checklist in `references/patterns.md` — unsupported input, limits, empty, permission, conflicts, async/network, destructive actions, availability. That file maps each scenario to the right mainstream pattern; consult it whenever you meet a scenario you are unsure how to present.

**When the spec is silent about a limit or an unsupported case, do not silently invent product truth.** Either:

- implement the mainstream, reversible default (e.g. accept the file types the backend actually parses) and make the value a named, configurable constant, **and flag it in your final report as an assumption for the user to confirm**, or
- if the choice is destructive, costly, or hard to reverse, ask the user before coding it.

Inventing `MAX_SIZE = 10MB` with no trace is how silent failures are born.

### Step 2 — Choose the lightest pattern that cannot be missed

Severity and timing decide the pattern, not habit:

| Situation | Pattern | Not this |
|---|---|---|
| Constraint knowable in advance | Prevention: helper text, format hint, character counter, `accept` attribute, placeholder example | Letting them submit, then scolding them |
| Field-level mistake | Inline error under the field + red border + focus moves to it | Toast only (gone in 3s, far from the problem) |
| Action result the user needn't act on | Toast / Snackbar (success, or failure with a Retry action) | Modal for trivia |
| Failure needing a decision, or destructive / irreversible | Dialog: consequence + explicit choices (`Convert`, `Delete anyway` / `Cancel`) | Toast; one-click irreversible delete |
| No data / no results / first use | Empty state: what this is + why it's empty + primary CTA | Blank area, or a bare "暂无数据" with no next step |
| System-level condition (offline, maintenance, quota nearly full) | Persistent banner until resolved | Toast that disappears while the condition persists |
| Batch / multi-item operation, some fail | Per-item results: `3 succeeded, 2 failed` + reason per item + `Retry failed only` | One generic "操作失败" hiding the 3 that worked |
| Something is loading | Spinner/skeleton if > ~300ms; disable repeat-submit; always a timeout → error → retry path | Infinite spinner; double-click creates duplicates |

Detailed recipes per scenario (upload, form, list, editor, payment…) live in `references/patterns.md`. Message wording (what + why + next step, no blame, no jargon) lives in `references/copywriting.md` — read it before writing user-visible strings.

### Step 3 — Implement, observing the hard rules

These exist because each one is a real way users get stranded:

- **Never swallow.** No empty `catch {}`, no bare `return` / `return null` on a user-triggered path, no `console.error` as the only response to a user action. If you catch it, the user hears about it — or it is genuinely not user-relevant (then log it and say why in a comment).
- **Never leave a control mysteriously disabled.** A disabled button must say why, adjacent or on hover/focus (helper text is better than tooltip alone — tooltips don't exist on touch). Often better: keep it enabled, and on click explain why it can't proceed — a disabled control can't even be asked.
- **Never destroy work on failure.** A failed submit keeps the form filled; a failed upload keeps the other files; a failed save keeps the draft (autosave / local draft where the pattern calls for it).
- **Never report total failure for partial success**, and never report success for partial failure.
- **Never show raw technical errors** (`Error 400`, `TypeError: undefined`, stack traces, backend codes alone). Translate to a human cause + action; keep the technical detail in logs. If there's a request/trace id, offer it quietly for support ("错误码 …，联系客服时请提供").
- **Match severity.** Blocking modal only for blocking problems. A toast must not carry information the user *must* act on — it will vanish.
- **Feedback appears where the action happened** (inline / near the trigger), immediately, and persists until addressed when it's an error — errors don't auto-dismiss.
- **Accessible by default:** errors are announced (`aria-live` / role=`alert` where the stack supports it), not conveyed by color alone, focus moves to the first error, and every feedback path is reachable by keyboard. A toast only a mouse-user can see is a silent failure for someone else.
- **Every async path terminates:** loading → success, or loading → error with Retry. Handle timeout and offline explicitly instead of letting the promise hang.
- **Destructive actions** name the object and consequence ("删除「Q3 报告」？删除后无法恢复"), default focus on Cancel, and offer Undo where the mainstream pattern allows it (soft-delete + Undo toast beats confirm-dialog friction for low-stakes deletes).

### Step 4 — Self-audit before you finish

Search the code you touched for silent branches and fix or justify each:

- `catch` blocks that don't surface anything to the user
- early `return`s on validation / permission / quota checks with no UI consequence
- `disabled` without an explanation, buttons that no-op on click
- async calls with no loading, no timeout, no error state
- lists that render nothing when empty; searches with no "no results" state
- inputs with limits (maxlength, file size, count) but no hint or counter
- branches for feature flags / plans / roles that hide UI with no trace — hiding is fine for things the user never had; if they had it, or will look for it, explain ("升级后可用")

Also walk it as a user: *try the wrong file, the 11th item, the duplicate name, the expired session, the offline submit, the double-click.* Each attempt should answer: I see what happened, I know why, I know what to do next.

### Step 5 — Report the boundary coverage

End your reply with a short list (skip it only for a truly trivial change). It is how the user — who admitted they can't foresee every boundary — regains control:

```
边界处理（本次补齐）：
- 不支持 .heic：选择时即提示支持 JPG/PNG/WebP，并提供「仍要上传？先转换」指引
- 超过 9 张：计数器 9/9 变红 + 提示，已选照片不丢失
- 无网络提交：保留表单内容，提示检查网络并提供「重试」
需你确认的假设：
- 单张上限按后端接口的 20MB 实现（常量 MAX_IMAGE_SIZE），产品如有其他口径告诉我即可改
未覆盖 / 建议后续：
- 会话过期后自动保存草稿，现仅提示重新登录
```

Do not bury this in prose, and do not claim coverage you didn't implement.

## Scope notes

- Framework- and library-agnostic: principles and patterns transfer to React/Vue/Svelte/native, Ant Design/Material/shadcn/Element, and (for messages) mobile. Always prefer the project's own design system over these generic recipes when they conflict.
- This skill concerns *user-reachable* boundaries. Internal invariants, programmer errors, and non-user-facing logs should still fail loudly in logs/telemetry — just not in the user's face, and never as a silent UI.
- Don't gold-plate: a two-field internal tool doesn't need quota banners. Scale the inventory to who can actually reach the boundary and what it costs them to hit it unexplained.
