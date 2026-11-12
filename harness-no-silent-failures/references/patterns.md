# Boundary patterns — scenario → mainstream treatment

Consult this file when implementing a feature: walk each category, ask "can my user reach this?", and apply the treatment. Patterns follow Material Design, Apple HIG, and Ant Design conventions; defer to the project's own design system when it differs.

## Table of contents

1. Unsupported input
2. Limits & quota
3. Validation & format
4. Empty, first-use & no-results
5. Permission, auth & entitlement
6. Conflicts & duplicates
7. Async, network & server errors
8. Destructive & irreversible
9. Availability: flags, plans, maintenance, deprecation
10. Disabled controls

---

## 1. Unsupported input

*Formats, file types, versions, browsers/features, devices, regions, languages the product doesn't handle.*

- **Prevent first.** State supported formats/sizes at the point of choice, before selection: `支持 JPG、PNG、WebP，单张 ≤ 20MB` next to the upload button; set the file picker's `accept` accordingly (but still validate after selection — `accept` is a hint, not enforcement).
- **Validate at selection, not after a long upload.** Wrong type/size is rejected instantly with the reason naming the file: `「海报.heic」暂不支持，请转换为 JPG 后重试` — plus, where feasible, a rescue path: offer in-browser conversion, compression, or trimming instead of a dead end.
- **Feature detection, not assumptions.** If a browser/device lacks a capability (camera, WebGL, clipboard, notifications), detect it and degrade with an explanation + alternative (`当前浏览器不支持扫码，可手动输入编码`), never a button that does nothing.
- **Unsupported links/deep-links/versions:** opening content the app version can't render → say so and offer update / open-in-web, don't crash or blank-screen.

## 2. Limits & quota

*Count, size, length, seats, storage, rate limits, plan quotas.*

- **Show the limit before it's hit:** counters (`3/9`, `120/500 字`), remaining quota in settings/billing, progress bar for storage.
- **Warn on approach, not just arrival:** banner or inline note at ~80% (`存储已用 85%，升级或清理后可继续上传`).
- **At the limit, explain + give the exit:** what the limit is, why (plan? system?), and the two real options — remove something, or upgrade: `免费版最多 3 个项目，删除一个或升级 Pro 后继续` with buttons for both. Never just grey out "New".
- **Partial acceptance:** pasting/adding 15 items when 10 are allowed → accept 10, say so, name what was dropped and why. Don't reject all-or-nothing unless consistency truly requires it — and then say that upfront.
- **Rate limiting:** `操作太频繁，请 30 秒后再试` with the retry actually disabled/counting down, not a vague failure.

## 3. Validation & format

- Validate on blur / on submit, not on every keystroke (don't shout at someone mid-typing); validate the whole form on submit and move focus to the first error.
- Message sits **under its field**, states the fix not just the fault: `请输入 11 位手机号` beats `格式错误`.
- Keep the user's input intact and selected/highlighted where helpful; never clear a form because one field is wrong.
- Show format expectations *before* the error: placeholder/helper examples (`如 138****0000`), input masks where mainstream, password rules listed and checked off live.
- Server-side validation errors map back to fields when the API identifies them; unmapped ones become a form-level alert at the top + focus to it.

## 4. Empty, first-use & no-results

Three different states users conflate — treat them differently:

| State | Treatment |
|---|---|
| **First use** (nothing ever created) | Explain what this is for + primary CTA to create the first one; a friendly illustration is mainstream, optional |
| **No search/filter results** | `没有符合「xxx」的结果` + suggest clearing/adjusting filters, one-click `清除筛选`. Distinguish "you have none" from "none match" |
| **Emptied by the user** (deleted all, inbox zero) | Brief positive confirmation (`已全部处理完 🎉` style per product tone), no CTA needed |

A blank white region is never an acceptable empty state. Loading skeletons are not empty states — don't flash "暂无数据" while data is still loading.

## 5. Permission, auth & entitlement

- **Not logged in / session expired mid-work:** preserve what they were doing (draft, form, cart, route intent), explain `登录已过期，请重新登录`, and return them to the same place after login. Losing an hour's form to a silent redirect is the canonical silent failure.
- **No permission (role-based):** if they can see it but can't act, say why and who can help: `你没有删除权限，请联系管理员张三`. If they shouldn't even know it exists, hiding is correct — decide consciously, don't hide by accident.
- **Paid/plan features:** a locked feature should sell, not stump: lock badge + `Pro 功能，升级后可用` + upgrade path. A click that does nothing is the worst of both worlds.
- **System permissions (camera/location/notifications denied):** detect denial, explain what it's needed for, deep-link to settings, and provide the manual fallback.

## 6. Conflicts & duplicates

- **Duplicate name/value on create:** inline `已存在同名项目「xxx」` + actions `换个名字` / `打开已有的` — don't just fail the submit.
- **Already done:** double-submit, repeat like/follow, re-joining — make it idempotent in effect and honest in feedback (`你已报名，无需重复提交`), and disable the button while the request is in flight.
- **Concurrent edit / version conflict:** never silently overwrite the other person. Show `李四刚刚修改了这篇文档` with `查看最新版 / 保留我的副本` choices.
- **Expired/invalid links & stale data:** `链接已过期` + request a new one in place; lists that changed under the user get a `有新内容，点击刷新` pill rather than a silent reshuffle.

## 7. Async, network & server errors

- Every async action: immediate acknowledgement (button loading state, skeleton, optimistic update where safe), then a definite end — success feedback proportionate to importance (a toast for a like is noise; for a payment it's a full confirmation page).
- **Timeout & offline:** explicit message + Retry, and keep the payload so retry is one tap. Offline → banner `当前无网络，内容已保存在本地` where that's true; queue-and-sync if the product promises it.
- **Server errors:** human cause at the level known (`服务器开小差了，稍后再试`), Retry button, and a quiet trace/request id for support. Automatic retry with backoff is fine *behind* visible status, not instead of it.
- **Long operations:** progress with real granularity or an honest indeterminate state + `处理中，可离开此页，完成后通知你` where async completion exists. Never a fake 99%-stuck bar.
- **Optimistic updates that fail must roll back visibly** — revert the UI and say so (`发送失败，已存草稿`), don't leave the phantom state.

## 8. Destructive & irreversible

- Confirm with the object named and consequence stated: `删除「Q3 报告」？其 12 条评论也会删除，无法恢复` — buttons labelled with the action (`删除`), not `确定`.
- Prefer **Undo over confirmation** for low-stakes, recoverable deletes (soft-delete + `已删除 [撤销]` toast, Gmail-style) — it's the mainstream low-friction pattern. Reserve modal confirmations for truly irreversible or wide-blast-radius actions.
- Type-to-confirm / re-auth only for the highest stakes (account deletion, large data wipe) — friction proportional to harm.
- After deletion, confirm outcome and, where relevant, where to find it (`已移入回收站，30 天后清除`).

## 9. Availability: flags, plans, maintenance, deprecation

- **Coming soon / flag off for a visible entry:** label it (`即将上线`) or explain on click; don't ship a dead menu item.
- **Maintenance / degraded service:** advance + live banner with scope and expected recovery; read-only mode should say it's read-only at the top, not fail every save.
- **Deprecated feature/API version:** warn in-product before removal with the migration path and date; after removal, old links explain where it went.
- **Minimum version gates:** `当前版本过低，请升级到 3.2 后使用` with an update button, not a crash or feature silently missing.

## 10. Disabled controls

- Disabled is a last resort. It answers no questions: why? for how long? what do I do? Prefer, in order:
  1. **Enabled + explain on use** — click tells them what's missing (`先选择至少一项才能导出`) and focus jumps to the missing thing.
  2. **Disabled + adjacent reason** — persistent helper text next to/under the control (works on touch, screen readers).
  3. **Disabled + tooltip** — acceptable only as a supplement; tooltips are undiscoverable on touch and for keyboard users if not focusable.
- Loading-disabled is the exception (prevent double-submit) — but show the spinner *in* the button so it's clearly temporary.
- Never disable the only path forward without saying how to enable it.
