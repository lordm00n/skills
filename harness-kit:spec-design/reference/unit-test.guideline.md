# Unit Test Guideline

Each unit test case is **one observable behavior**, written so a human reviewer can scan it in seconds and tell whether it's the right test.

## Form

Default to the multi-line shape — one bullet for Given, When, Then, then Intent on its own line:

```markdown
## `<module-name>`

- UT-1:
  - **Given**: <precondition / inputs, in plain words>
  - **When**: <one action or trigger>
  - **Then**: <one observable result>
  - **Intent**: <one sentence — which goal / constraint / decision from `design.md` this protects, and what would silently break if the test were deleted>
- UT-2:
  - **Given**: ...
  - **When**: ...
  - **Then**: ...
  - **Intent**: ...

## `<another-module>`

- UT-3: ...
```

You may collapse to a single inline sentence **only** when the whole case stays under ~25 words and reads naturally:

```markdown
- UT-N:
  - **Case**: GIVEN <X> WHEN <Y> THEN <Z>
  - **Intent**: ...
```

When in doubt, use the multi-line form.

## Rules for the **Case**

1. **One thought per bullet.** Given / When / Then are three lines, not three commas in one paragraph. No nested clauses, no parentheticals stacking three more facts.
2. **Plain language.** Write what the code is supposed to do in everyday words. Ban decorative phrasing — both English ("wiring", "canonical home", "first line of defense", "the contract is upheld", "happy path coverage") and Chinese ("守住契约", "兜底", "断网", "红线", "第一道闸"). If you need a fancy word to describe the behavior, the spec — not the test — is where it should live.
3. **Only terms already in `design.md`.** Every name you mention (module, type, state value, channel, goal, decision) must already appear in the spec body or Glossary. If a name is missing from the spec, fix the spec first; don't smuggle it in via a test case.
4. **Names verbatim, in backticks.** Match the spec spelling exactly for any module, type, channel, or state value (e.g. `<ModuleName>`, `<channel-name>`, `<TypeName>.<field> === '<value>'`). No paraphrasing, no abbreviating.
5. **Show the data, don't describe it.** When the case hinges on a specific input or output shape, paste the literal value (e.g. `returns <literal-object-or-value>`). "returns the expected result" is rejected.

## Rules for the **Intent**

1. **One sentence.** If you need two, split the test.
2. **Spec anchor by full name.** Cite the protected item the way the spec spells it: write `Goal G<N> (<full goal text from §0>)`, not `G<N>` alone; write `the decision in §<N>.<X> to <short paraphrase>`, not the decision-table cell ID alone. A reviewer should not need a decoder ring.
3. **Behavior or contract, not call chain.** Say what user-visible or contract-level guarantee is pinned. Don't narrate which function calls which.
4. **Name the regression.** State concretely what would silently break if this test were deleted — for the user, or for a downstream contract.
5. **Plain language.** Same rule as Case. No decorative phrasing.

## Anti-patterns

Reject these — the example column shows the *shape* of the bad case, not a specific feature:

- **Dense bilingual / multi-clause paragraph.** Example shape: `GIVEN <subj> stub <method> resolves with <literal>, WHEN <other-component> 经 <bridge> 路径 invoke <channel> with <literal>, THEN <subj> 返回该 result，且 <method> 被以 <args> 调用一次。` → split into Given / When / Then bullets, drop the prose connectives, drop the language switching.
- **Spec-section shorthand.** Example shape: `守住 §<N> Mechanism + Q<N><x> 决策` or `protects G<N>`. → write the name out: `the <specific-mechanism-name> in §<N>` or `the early-return rule introduced in §<N>.<X>`.
- **Internal call-chain narration.** Example shape: `若 <handler> swallow 错误返回 undefined，<consumer> 会进入 <state>，<field>=undefined，引发 NPE`. → describe user-visible or contract-level impact instead: `the UI would render an empty success state` or `downstream consumers would receive an undefined where a <TypeName> is required`.
- **Restated case.** Example shape: `Tests that <fn>(<args>) returns the expected output.` → adds nothing beyond the case; delete or rewrite to name the regression.
- **Vacuous intent.** "Ensures the function works." / "Covers the happy path." / "Tests correctness." → all rejected.
- **New terms.** Introducing a name in a test case (a module name, a state value, a decision ID) when it isn't in the spec body. Move it into the spec first, or rephrase the test to use names that are.
