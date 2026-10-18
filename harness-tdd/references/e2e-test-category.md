# E2E testing category

Use E2E tests only when the change affects Web UI or Electron desktop UI behavior. Do not add or run E2E tests for pure backend logic, CLI behavior, library code, data transforms, or other changes that can be covered by unit or integration tests.

## Tooling

Use `agent-browser` CLI for every E2E test. Every `agent-browser` command in the E2E flow must include the `--auto-connect` flag.

Before testing a Web UI, load the current browser workflow guide:

```bash
agent-browser skills get core
```

Before testing an Electron desktop UI, load the Electron-specific guide:

```bash
agent-browser skills get electron
```

Then run the E2E flow with `agent-browser --auto-connect ...` commands.

## Screenshot output

Every E2E test must produce screenshots. Store them under the project root in:

```text
e2e/<subject>-<YYYY-MM-DD>/
```

Choose `<subject>` from the issue, task, or plan title and convert it to lowercase kebab-case. If there is no clear title, derive the subject from the user's request. Use the current local date for `<YYYY-MM-DD>`.

Name screenshots with a two-digit step number and a short state name:

```text
e2e/<subject>-<YYYY-MM-DD>/01-before.png
e2e/<subject>-<YYYY-MM-DD>/02-after-action.png
e2e/<subject>-<YYYY-MM-DD>/03-success.png
```

Capture screenshots at key states: before the interaction, after important user actions, and at the success or failure state that proves the behavior.

## Web UI flow

1. Start the application if it is not already running.
2. Open the target page with `agent-browser --auto-connect open <url>`.
3. Capture the initial state with `agent-browser --auto-connect screenshot e2e/<subject>-<YYYY-MM-DD>/01-before.png`.
4. Use `agent-browser --auto-connect snapshot -i` to find interactive elements.
5. Interact with the UI using refs from the latest snapshot, such as `click`, `fill`, `press`, or `select`.
6. Re-run `agent-browser --auto-connect snapshot -i` after navigation, form submits, modal opens, or dynamic re-renders because refs become stale after page changes.
7. Capture key intermediate and final screenshots in the same screenshot directory.
8. Close the browser session when the E2E check is complete if no other task needs it.

## Electron desktop UI flow

1. Load `agent-browser skills get electron` before starting.
2. Connect to the Electron app using the Electron guide's current instructions.
3. Use `agent-browser --auto-connect snapshot -i` to inspect the current window.
4. Interact with visible UI elements through `agent-browser --auto-connect` commands.
5. Re-snapshot after each window change, navigation, dialog, or dynamic re-render.
6. Capture key screenshots into `e2e/<subject>-<YYYY-MM-DD>/` using the same naming pattern as Web UI tests.
7. Record the tested app/window state in the final response so the user can connect the screenshots to the scenario.
