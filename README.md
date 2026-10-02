# Metal pipe hook

A **10% chance of [metal pipe](https://www.youtube.com/watch?v=iDLmYZ5HqgM)** every time you send your coding agent a prompt.

One Python file. No packages. No model tokens. Works with local **Codex, Claude Code, Cursor, and GitHub Copilot CLI**.

## Quick start

Requires **Python 3.9+** and a local desktop browser.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/pc386/metal-pipe-hook/main/metal_pipe.py -o metal_pipe.py
python3 metal_pipe.py --install codex
```

### Windows PowerShell

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/pc386/metal-pipe-hook/main/metal_pipe.py -OutFile metal_pipe.py -ErrorAction Stop
py -3 metal_pipe.py --install codex
```

**Use your agent's name:**

| Agent | Install command after downloading |
| --- | --- |
| Codex | `python3 metal_pipe.py --install codex` |
| Claude Code | `python3 metal_pipe.py --install claude` |
| Cursor | `python3 metal_pipe.py --install cursor` |
| GitHub Copilot CLI | `python3 metal_pipe.py --install copilot` |

On Windows, replace `python3` with `py -3`. Run another install command to enable more than one agent.

The installer copies itself to `~/.metal-pipe-hook/metal_pipe.py`, registers a user-level prompt hook, preserves other settings, and creates a timestamped backup before editing existing config. It records the Python interpreter's absolute path. Re-running updates its registration without adding another copy. Keep that Python installation available.

**Restart your agent.** For Codex, open `/hooks` in the CLI and review/trust the new command first. [Desktop app guide →](docs/desktop.md)

## Hear it now

```bash
python3 ~/.metal-pipe-hook/metal_pipe.py --test
```

Windows:

```powershell
py -3 "$HOME/.metal-pipe-hook/metal_pipe.py" --test
```

This requests one browser launch immediately, even while paused. Click Play if your browser blocks autoplay. It tests the script and browser, not automatic hook registration.

## Controls

```bash
python3 ~/.metal-pipe-hook/metal_pipe.py --disable          # Pause every agent
python3 ~/.metal-pipe-hook/metal_pipe.py --enable           # Resume
python3 ~/.metal-pipe-hook/metal_pipe.py --dry-run          # Show a roll; open nothing
python3 ~/.metal-pipe-hook/metal_pipe.py --uninstall codex  # Remove this agent's hook
```

On Windows use `py -3 "$HOME/.metal-pipe-hook/metal_pipe.py"` followed by the same flag. Uninstall each agent you enabled; the shared script and config backups remain on disk. Reinstalling does not clear a pause: use `--enable`.

## Desktop apps

- **Codex desktop:** install `codex`, review/trust via the CLI's `/hooks`, then start a new local GUI session.
- **Claude Desktop:** install `claude`, then use **Code → Local** and choose your project folder.
- **Cursor:** install `cursor`, then use a local Agent chat.
- **ChatGPT:** this is for supported local Codex/local-only Work sessions. Ordinary chat and cloud-orchestrated Work do not have a supported installation path for this script.

See the [GUI walkthrough and troubleshooting](docs/desktop.md) for exact steps and sources. These configurations do not establish support for Claude Chat or Cowork.

## Where it installs

| Agent | User config | Prompt event |
| --- | --- | --- |
| Codex | `~/.codex/hooks.json` | `UserPromptSubmit` |
| Claude Code | `~/.claude/settings.json` | `UserPromptSubmit` |
| Cursor | `~/.cursor/hooks.json` | `beforeSubmitPrompt` |
| Copilot CLI | `~/.copilot/hooks/metal-pipe.json` | `userPromptSubmitted` |

Custom `CODEX_HOME` and `COPILOT_HOME` are respected. Existing malformed JSON is reported instead of overwritten. The installer only manages entries it tagged; remove a previously added manual metal-pipe hook before installing to avoid duplicate rolls.

## Troubleshooting

- **Nothing happens:** run `--test`. If that works, check the agent's hook registration/trust and start a fresh local session. Ten prompts can all miss the lottery.
- **No Python:** install Python 3.9+ and rerun installation using that interpreter. GUI apps need access to the recorded executable.
- **It runs twice:** remove any separate manual/project hook for metal pipe. The installer only manages its own user-level entry.
- **Remote or headless session:** hooks run on that machine. This script cannot open your local browser from a cloud agent; headless Linux skips opening.
- **Config error:** fix the reported JSON file and retry. Backups are beside the original file as `*.metal-pipe-<timestamp>.bak`.

## How it works

Each prompt-hook invocation draws one integer from 0 through 9. Only 0 opens the fixed video URL. No prompt text is read, saved, or transmitted. Normal hook execution stays quiet and browser-launch failures do not block prompts. On Windows the installer uses an encoded PowerShell command to preserve paths with spaces and quotes; it does not change execution policy.

## Development

```bash
python3 -m unittest -v
```

Tests run with temporary config folders and mocked browser launches. They cover lottery outcomes, immediate testing, pause/resume, config preservation, repeat installation, uninstall, malformed config, and Windows/POSIX command quoting. Desktop host integration must still be checked in your installed app.
