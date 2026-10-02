# Metal pipe hook

A 10% chance of [metal pipe](https://www.youtube.com/watch?v=iDLmYZ5HqgM) every time you submit a prompt. One Python script, no packages, no model tokens.

Works with local **Codex, Claude Code, Cursor, and GitHub Copilot CLI** through their prompt-submission hooks. The script is agent agnostic; only the hook configuration differs.

## Install

### 1. Download the script

Requires Python 3. No GitHub account or CLI needed.

**macOS / Linux**

```bash
mkdir -p "$HOME/.metal-pipe-hook"
curl -fsSL https://raw.githubusercontent.com/pc386/metal-pipe-hook/main/metal_pipe.py -o "$HOME/.metal-pipe-hook/metal_pipe.py"
python3 "$HOME/.metal-pipe-hook/metal_pipe.py" --dry-run
```

**Windows PowerShell**

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.metal-pipe-hook" | Out-Null
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/pc386/metal-pipe-hook/main/metal_pipe.py' -OutFile "$HOME/.metal-pipe-hook/metal_pipe.py" -ErrorAction Stop
py -3 "$HOME/.metal-pipe-hook/metal_pipe.py" --dry-run
```

The dry run prints a random result without opening the browser.

### 2. Register your agent's hook

The examples below use `/ABSOLUTE/PATH/metal_pipe.py`. Replace it with the full downloaded path, such as `/Users/alex/.metal-pipe-hook/metal_pipe.py` or `/home/alex/.metal-pipe-hook/metal_pipe.py`.

On Windows, replace each command with this form (keeping `--cursor` for Cursor):

```json
"command": "py -3 \"C:/Users/alex/.metal-pipe-hook/metal_pipe.py\""
```

If `python3` or `py` isn't on your agent's PATH, use the full path to your Python executable. Preserve existing settings: merge the new event/handler into your JSON instead of replacing the file. Register this hook once per agent; user and project hooks can both run.

#### Codex

Merge into `~/.codex/hooks.json` for all projects, or `.codex/hooks.json` for one project:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"/ABSOLUTE/PATH/metal_pipe.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Start a new session and review/trust the new hook with `/hooks` in the Codex CLI. Untrusted hooks are skipped; project hook config also requires a trusted project. [Codex hook docs](https://learn.chatgpt.com/docs/hooks)

#### Claude Code

Merge into `~/.claude/settings.json` for all projects, or `.claude/settings.json` for one project:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"/ABSOLUTE/PATH/metal_pipe.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Start a new session and inspect the entry with `/hooks`. Complete the host's normal workspace/hook trust flow if prompted. [Claude Code hook docs](https://code.claude.com/docs/en/hooks)

#### Cursor

Merge into `~/.cursor/hooks.json` for all projects, or `.cursor/hooks.json` for one project:

```json
{
  "version": 1,
  "hooks": {
    "beforeSubmitPrompt": [
      {
        "command": "python3 \"/ABSOLUTE/PATH/metal_pipe.py\" --cursor",
        "timeout": 5
      }
    ]
  }
}
```

Cursor reloads hook configuration automatically. The `--cursor` flag returns `{"continue":true}` so prompt submission proceeds regardless of the lottery result. [Cursor hook docs](https://cursor.com/docs/hooks)

#### GitHub Copilot CLI

Create `~/.copilot/hooks/metal-pipe.json` for all projects, or `.github/hooks/metal-pipe.json` for one repository:

```json
{
  "version": 1,
  "hooks": {
    "userPromptSubmitted": [
      {
        "type": "command",
        "command": "python3 \"/ABSOLUTE/PATH/metal_pipe.py\"",
        "timeoutSec": 5
      }
    ]
  }
}
```

Start a new CLI session. If you set `COPILOT_HOME`, put the user hook in its `hooks` directory instead. [Copilot hook docs](https://docs.github.com/en/copilot/reference/hooks-reference)

## Desktop app tutorials

These instructions are for desktop sessions that run local command hooks. Having a chat app or local file access alone does not enable a prompt hook.

| App / mode | This hook |
| --- | --- |
| Codex desktop, local session | Uses the Codex hook configuration below |
| ChatGPT Work, local-only orchestration and execution | Supported by the documented local hook system; confirm your session actually uses this mode |
| ChatGPT Work with cloud orchestration, including local computer access | Local command hooks are not supported |
| Ordinary ChatGPT chat | No documented installation route for this local prompt hook |
| Claude Desktop, Code tab, Local environment | Uses the Claude Code settings below |
| Claude Chat / Cowork | This tutorial does not establish support for local Claude Code command hooks in these modes |

### ChatGPT / Codex desktop

1. Download the script using [Install](#install). This setup step uses Terminal on macOS/Linux or PowerShell on Windows; afterward you can chat in the GUI.
2. Open your home configuration folder in a file manager. On Windows, paste `%USERPROFILE%\.codex` into File Explorer's address bar. On macOS, press **Cmd+Shift+G** in Finder and enter `~/.codex`. Create the folder if needed.
3. Open or create `hooks.json` in a plain-text editor. Merge in the [Codex configuration](#codex), replacing the script path with your full downloaded path. Save as `hooks.json`, not `hooks.json.txt`.
4. Review the hook once through the documented CLI route: open a terminal, run `codex`, then enter `/hooks`. Inspect and trust the metal-pipe command. Use the same user/configuration directory as the desktop app. The official documentation does not establish a GUI-only trust flow, so this tutorial does not assume a Hooks settings button exists.
5. Return to the desktop app and start a **new local Codex session**. For ChatGPT Work, use this setup only if your environment supports local-only orchestration and execution. Selecting Work or granting local computer access does not by itself establish that condition.
6. Send a normal message. The hook runs independently of the model and may open the video. If it does not, follow [Test from the GUI](#test-from-the-gui) before concluding it failed.

If you only have ordinary ChatGPT chat or cloud-orchestrated Work, this script has no supported per-message installation path there. Use a local Codex session for this tutorial.

Sources: [desktop app](https://learn.chatgpt.com/docs/app), [hook configuration and trust](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks), [local versus cloud hook support](https://learn.chatgpt.com/docs/hooks#managed-hooks-from-requirementstoml).

### Claude Desktop

1. Open Claude Desktop and select the **Code** tab.
2. Choose **Local**, then **Select folder**, and pick a project folder. This tutorial uses native local execution, rather than Cloud, SSH, or WSL.
3. Download the script using [Install](#install).
4. Open the settings folder: on Windows, paste `%USERPROFILE%\.claude` into File Explorer; on macOS, use Finder's **Cmd+Shift+G** and enter `~/.claude`. Create the folder if needed.
5. Open or create `settings.json` in a plain-text editor. Merge in the [Claude Code configuration](#claude-code) with your full script path. Preserve existing settings and save as `settings.json`, not `settings.json.txt`.
6. Start a new **Code → Local** session in your project and complete any normal workspace trust prompts. Desktop and CLI share these hook settings; the CLI is not required to use the Code tab.
7. Send a normal message and follow the checks below. Do not assume this Code-tab configuration also installs the hook into Claude Chat or Cowork.

Sources: [Desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart), [shared desktop settings](https://code.claude.com/docs/en/desktop), [hooks reference](https://code.claude.com/docs/en/hooks).

### Test from the GUI

First, ask the agent in your **local** desktop session:

> Run my installed metal_pipe.py with --dry-run, using its full path and a working Python interpreter. Show me the result. Do not edit the script or hook configuration.

A result such as `roll=7; would_open=False` verifies that the script runs. It does **not** prove that the app invoked the hook automatically.

To test browser launching without waiting for a random hit, ask:

> Load my installed metal_pipe.py with Python's runpy.run_path and call its open_video function once. This is a manual test: open the configured video in my browser, and do not change the lottery odds or hook configuration.

The agent may request the host's normal execution approval. A successful manual test proves browser access from that execution environment, not automatic hook registration.

Finally, start a fresh session and send ordinary messages without asking the agent to run the script. Each registered prompt event has a 10% chance. Ten messages can all miss. If nothing happens, check the config's exact file name, absolute paths, available Python interpreter, session mode, and hook trust state. GUI apps may have a different PATH from your terminal.

These tutorials are based on the linked vendor documentation. The project's automated tests validate the script, not every desktop app/version. Browser autoplay may still require clicking Play.


## Behavior

Each invocation draws one uniform integer from 0 through 9. Only 0 opens the fixed video URL in your default browser. Nothing is sent to a model, and the script does not read, store, or transmit hook input or prompt text. Browser launching is local; the browser then visits YouTube normally.

Hook registration targets submitted prompts, not tool calls or assistant continuations. Frequency follows the host's prompt event semantics. Install only one handler to avoid duplicate rolls.

Windows uses its default URL handler; macOS uses `open`; Linux desktop uses `xdg-open`. Headless Linux skips opening. Browser launch errors do not block the prompt. Browser autoplay may require a click. Cloud/remote hooks run on that remote machine, not your local desktop.

## Check it

```bash
python3 metal_pipe.py --dry-run
python3 -m unittest -v
```

The tests mock browser launching: they check all ten outcomes, dry-run behavior, Cursor's response after a launch failure, and OS command selection without opening tabs. Agent configuration examples follow official docs; host integration still needs to be checked in your installed agent.

## Disable / uninstall

Remove only this command's hook entry from your agent config, then restart the agent. Delete `~/.metal-pipe-hook` if you no longer need the script. To pause it in Codex, disable the entry in `/hooks`.

To stop the lottery, disable its hook configuration.

