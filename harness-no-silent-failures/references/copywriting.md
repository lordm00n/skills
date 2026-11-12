# Feedback copywriting — how the message itself should read

Read this before writing any user-visible error, hint, toast, dialog, or empty-state text.

## The formula

Every boundary message answers, in this order, as many as apply:

1. **What happened** — in the user's terms, naming the object: `「海报.heic」无法上传`
2. **Why** — the real, human cause, briefly: `目前仅支持 JPG / PNG / WebP 图片`
3. **What to do next** — a concrete action, ideally *on a button*: `[转换并上传]` `[换一张图]`

> ❌ `上传失败（Error 415）`
> ✅ `「海报.heic」暂不支持 — 目前支持 JPG、PNG、WebP。换一张图，或转换为 JPG 后重试。`

## Rules

- **No blame, no scolding.** Not `你输入了非法字符`, but `名称里不能包含 / 和 \\` — describe the constraint, not the user's fault. Never `错误操作`.
- **No jargon, no raw codes alone.** `服务器开小差了` is fine for a generic 500 in a consumer product, too cute for a finance/enterprise one — match the product's existing tone. Developer detail (status codes, trace ids) goes in logs; a trace id may ride along quietly for support.
- **Be specific about limits and objects.** Numbers and names, not vibes: `最多上传 9 张，还可添加 2 张` · `已存在同名文件夹「素材」`.
- **Say it where it happened, in time.** Prevention copy lives before the action (`单张 ≤ 20MB`), errors at the scene, results right after. A message the user has to hunt for is a silent failure with words.
- **Buttons say what they do.** `删除` / `保留草稿` / `升级 Pro`, not `确定` / `是`. Destructive buttons are specific and styled as destructive; the safe option is the default focus.
- **One voice, consistent terms.** If the product calls it 「项目」, the error doesn't call it 「工程」. Reuse the project's glossary and existing message strings; add new strings via its i18n system.
- **Don't over-apologize or over-celebrate.** One `抱歉` at most; success for routine actions needs at most a light confirmation — save enthusiasm for real milestones. No exclamation-mark spam.
- **Uncertainty is stated honestly.** `可能已保存，请刷新确认` beats pretending. If the system doesn't know, neither does the copy.
- **Length:** toast ≤ ~2 short lines and self-sufficient; anything needing explanation or a decision graduates to inline text or a dialog. If it needs a paragraph, it also needs a place to live permanently (help link, banner), not 4 seconds of toast.

## Quick templates (adapt to product tone & language)

| Scenario | Template |
|---|---|
| Unsupported format | `「{file}」暂不支持，支持 {formats}。{补救动作，如：转换为 JPG 后重试}` |
| Over limit | `最多 {limit}，你已选择 {n} 个。请移除 {extra} 个后继续` / `已达上限，删除一个或升级` |
| Quota warning | `{资源}已用 {pct}%，{将满的影响}。{清理 / 升级}` |
| No permission | `你没有{动作}权限（需要{角色}）。请联系{管理员/谁}开通` |
| Session expired | `登录已过期。你的内容已保存，重新登录后继续` |
| Duplicate | `已存在{同名对象}「{name}」，{打开它 / 换个名字}` |
| Network fail | `网络连接失败，{内容}已保留。检查网络后[重试]` |
| Server fail | `服务暂时不可用，稍后再试。[重试]（错误码 {id}，联系客服时请提供）` |
| Partial success | `{ok} 个成功，{fail} 个失败：{逐项原因}。[仅重试失败项]` |
| Empty (first use) | `还没有{对象}。{它能帮你做什么}，[创建第一个]` |
| No results | `没有符合「{query}」的结果，试试{建议}。[清除筛选]` |
| Destructive confirm | `{动作}「{name}」？{后果，如：其 X 条评论也会删除，无法恢复}。[取消] [{动作}]` |
| Coming soon / locked | `「{功能}」{即将上线 / 为 Pro 功能}。{上线通知我 / 升级后立即可用}` |

English equivalents follow the same formula: name the object, state the cause in plain words, put the next action on the button — *"'poster.heic' isn't supported yet. Use a JPG, PNG, or WebP image."*
