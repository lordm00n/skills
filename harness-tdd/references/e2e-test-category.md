# E2E testing category

Use E2E tests only when the change affects Web UI or Electron desktop UI behavior. Do not add or run E2E tests for pure backend logic, CLI behavior, library code, data transforms, or other changes that can be covered by unit or integration tests.

## Tooling

Use `agent-browser` CLI for every E2E test.

Verify the installed version before starting. The Chrome remote-debugging approval wait described below requires agent-browser 0.39.0 or newer:

```bash
agent-browser --version
```

If a command fails unexpectedly, run `agent-browser doctor` before retrying.

Before testing a Web UI, load the current browser workflow guide:

```bash
agent-browser skills get core
```

Before testing an Electron desktop UI, load the Electron-specific guide:

```bash
agent-browser skills get electron
```

The CLI serves skill content matching the installed version, so always follow the loaded guide where it differs from remembered usage.

## Session and connection

Always use your own named session for the whole task. The default (unnamed) session is a single browser shared with every other agent on the machine and persists across conversations, so working in it can hijack another agent's page or something the human left open.

Before the first browser command, check for an existing session that can be reused:

```bash
agent-browser session list
```

If a suitable active session already exists for this task, reuse it by setting `AGENT_BROWSER_SESSION` to its name. Otherwise derive a new stable session id:

```bash
export AGENT_BROWSER_SESSION="$(agent-browser session id --scope worktree --prefix e2e)"
```

Keep the same session for every command in the task.

Attach only once. `--auto-connect` and `--cdp` are connection setup for the first command in a session, not flags to repeat on every command. After a session is attached, later commands in that session run against the same browser without a connection flag. Repeating `--auto-connect` can trigger another Chrome remote-debugging approval prompt and can create a competing session.

Choose the connection mode once, in this order of preference:

1. **Reuse**: an already attached named session (see above) needs no new connection at all.
2. **Managed browser (default)**: when the test does not need the user's existing login state, let agent-browser launch its own browser. No Chrome approval prompt is involved:

   ```bash
   agent-browser open <url>
   ```

3. **Attach to the user's running Chrome (`--auto-connect`)**: only when the test needs the login state of the Chrome the user already has open. This is a single, standalone human-intervention boundary:
   - Before running it, tell the user that Chrome may show an "Allow debugging this browser?" prompt and that they should click **Allow** promptly. On agent-browser 0.39.0+ the handshake is held open for about 20 seconds; on older versions it gave up after about 2 seconds, before a human could react.
   - Make sure Chrome is already running and that "Allow remote debugging for this browser instance" is enabled at `chrome://inspect/#remote-debugging`.
   - Run exactly one attach attempt, for example `agent-browser --auto-connect open <url>`. Do not silently retry a failed attach: each new attempt shows the prompt again. If it fails, ask the user whether they approved the prompt (or are ready to), then retry once.
   - There is no supported way to approve this prompt automatically. It is a Chrome security gate shown before the debugging connection exists, so the debugging client cannot click it.
4. **Dedicated debugging profile (`--cdp`)**: when the test needs a persistent login state but must run unattended or repeatedly, start a separate Chrome yourself with a non-default data directory and connect to its port. A Chrome started this way shows no approval prompt, and the wait for the port can be as long as needed:

   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --remote-debugging-port=9222 \
     --user-data-dir="$HOME/.chrome-debug-profile" \
     <url>
   agent-browser --cdp 9222 open <url>
   ```

   Since Chrome 136, `--remote-debugging-port` is ignored for the default Chrome data directory, so the non-default `--user-data-dir` is required. Log in once inside this dedicated profile and reuse it across runs. Note that a remote debugging port exposes full browser control on localhost: only use it on a trusted machine, and close this Chrome when done.

When several sessions share one Chrome over `--cdp <port>`, add `--pin-tab` to the first command of each session so each session sticks to its own tab.

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
2. Set up the named session and connection as described above (reuse first, attach at most once).
3. Open the target page (if the attach command did not already open it) with `agent-browser open <url>`.
4. Create the screenshot directory and capture the initial state, for example `agent-browser screenshot e2e/<subject>-<YYYY-MM-DD>/01-before.png`.
5. Use `agent-browser snapshot -i` to find interactive elements.
6. Interact with the UI using refs from the latest snapshot, such as `click`, `fill`, `press`, or `select`.
7. Re-run `agent-browser snapshot -i` after navigation, form submits, modal opens, or dynamic re-renders because refs become stale after page changes.
8. Capture key intermediate and final screenshots in the same screenshot directory.
9. When the E2E check is complete, close only your own session with `agent-browser close` if no other task needs it. Never use `close --all` unless every session on the machine is yours to close. Browsers attached through `--cdp` or `--auto-connect` are externally owned and are not killed by closing the session.

## Electron desktop UI flow

1. Load `agent-browser skills get electron` before starting.
2. Set up a named session as described above, then connect to the Electron app once, using the Electron guide's current instructions.
3. Use `agent-browser snapshot -i` to inspect the current window.
4. Interact with visible UI elements through `agent-browser` commands in the same session, without repeating the connection setup.
5. Re-snapshot after each window change, navigation, dialog, or dynamic re-render.
6. Capture key screenshots into `e2e/<subject>-<YYYY-MM-DD>/` using the same naming pattern as Web UI tests.
7. Close only your own session when done, and record the tested app/window state in the final response so the user can connect the screenshots to the scenario.
