# E2E Test Guideline

Each acceptance scenario describes **one user-visible flow**, written so a non-author can review it without opening the codebase. Every Given / When / Then must be told from the user's seat — what the user does and what the user sees, not what the code does.

## Form

Default to the multi-line shape — Given, When, Then on separate bullets, then Intent:

```markdown
## E2E Strategy

- AS-1:
  - **Given**: <where the user is and what state the app is in, described from the user's POV>
  - **When**: <what the user does — one action: click, type, key press>
  - **Then**: <what the user sees or can do next — visual / textual outcome only, with a wall-clock budget if async>
  - **Intent**: <one sentence — which user-facing goal or value from `design.md` this protects, and what user-visible regression it catches>
- AS-2:
  - **Given**: ...
  - **When**: ...
  - **Then**: ...
  - **Intent**: ...
```

You may collapse to a single inline sentence **only** when the whole scenario stays under ~25 words. When in doubt, multi-line.

If the feature has no user-visible behavior:

```markdown
## E2E Strategy

EXEMPT: <one-line reason — e.g. "pure backend API consumed only by other services", "internal CLI tool with no UI", "build script with no runtime UI">
```

## Hard rule: the Scenario is told from the user's seat

The Given / When / Then describe what the user **does** and what the user **sees**. They never describe internal modules, hooks, state fields, transport channels, CSS variables, or framework lifecycle.

Examples are stated as *shapes* — substitute the names from your own spec:

| Allowed (user-facing) | Not allowed (internal) |
|---|---|
| user clicks the `<button-label>` button | `<ComponentName>` fires `<callback-prop>` |
| the `<area-name>` shows the text `<literal-the-user-reads>` within `<N>ms` | `<ComponentName>` receives `<state.field> === '<value>'` and renders `<css-var>` |
| user presses `<key-combo>` while the cursor is in the `<field-label>` field | document-level `<event>` listener fires with `<modifier>=true` |
| user copies the response, switches apps, pastes — the pasted text equals `<expected-content>` | `<api>.writeText` is called with `<state.path.to.value>` |

If the only way you can write the When / Then is by naming an internal module, state field, transport channel, or CSS class, the scenario is wrong — rewrite it as something a human can see or do.

You may name **fixtures and test setup** (sample config files, mock-server tools, seed data) — those are part of how the scenario is staged, not internals of the system under test.

## Rules for the **Scenario**

1. **One user flow.** One Given (state from user POV) → one When (one user action) → one Then (one observable outcome). Bundling multiple actions into one scenario is a smell — split it.
2. **Only terms already in `design.md`.** Every name you reference must already appear in the spec body or Glossary. If you want to introduce a name in a scenario, add it to the spec first.
3. **Plain language.** Everyday words. Ban decorative phrasing — both English ("wiring", "first line of defense", "muscle memory", "the contract is upheld") and Chinese ("守住契约", "断网", "兜底", "第一道闸", "视觉锚点"). Just describe the user's experience.
4. **Concrete, not abstract.** Quote the literal text or visual cue the user perceives (e.g. `the panel shows the text "<literal>"`). "the response is rendered correctly" is rejected.
5. **Bound the timing.** When the outcome is async, state a wall-clock budget the test should wait within (e.g. "within `<N>ms`"). The reader needs to know what "fast enough" means.

## Rules for the **Intent**

1. **One sentence.** If you need two, the scenario is bundling promises — split it.
2. **Spec anchor by full name.** Cite the protected goal the way the spec spells it: write `Goal G<N> (<full goal text from §0>)`, not `G<N>` alone. The reviewer must not flip back to look up an abbreviation.
3. **User-facing only.** Talk about what the user can do, sees, or is prevented from seeing. Never name internal modules, state fields, transport channels, or CSS variables.
4. **Name the regression.** State the user-visible thing that would silently break if this scenario were deleted.
5. **Plain language.** Same as the Scenario.

## Anti-patterns

Reject these — the example column shows the *shape* of the bad case, not a specific feature:

- **Code-flow narration.** Example shape: `若 <listener> 漏注册，<feature> 失效但 <visual-hint> 还在，造成"假按钮"`. → rewrite as the user-visible regression: `users press <key-combo> and nothing happens, even though the on-screen hint is still shown`.
- **Internal-name leakage.** Example shape: `<ComponentName> 出现绿色 dot ... CSS 颜色对应 <css-var>`. → drop the component name and the CSS variable; the user sees a green dot and the text `<literal>`.
- **Spec-section shorthand.** Example shape: `守住 §<N> Goal G<N> + G<M> 端到端可观测`. → write the names out: `Goal G<N> (<full goal text>) and Goal G<M> (<full goal text>)`.
- **Bundled flow.** Example shape: `click <btn-A> → <env-action> → click <btn-A> again → check error → click <btn-B>` packed into one AS. → split into separate scenarios so a failure pinpoints one user promise.
- **Vacuous intent.** "Tests that the form submits correctly" / "Covers the happy path" / "Ensures the page loads" / "Verifies the API returns 200" → all rejected.
- **New terms.** Coining a name in a scenario (a layout class, a defensive pattern, an internal flag) that isn't in the spec body. Add it to the spec first, or rephrase from the user's POV.
