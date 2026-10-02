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

### Migrating from metal-pipe-skill

Remove the old metal pipe paragraph from `AGENTS.md`, `CLAUDE.md`, or your other agent instructions. Remove the installed `metal-pipe` skill, or leave it unused. Start a new chat to discard the previous instructions. **Do not run the instruction-based lottery and the hook together:** that would create two chances per prompt.

The repository was renamed from `metal-pipe-skill` to `metal-pipe-hook`. Existing Git clones can update their remote:

```bash
git remote set-url origin https://github.com/pc386/metal-pipe-hook.git
```

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

Unlike the old skill, telling the model to stop does not disable an external command hook; disable the hook configuration instead.

## Skill fallback

For agents without command hooks, the original [metal-pipe skill](metal-pipe/SKILL.md) and [per-turn instruction](metal-pipe-global-instruction.md) remain available. Install them using your agent's skill and instruction system. That fallback relies on model instruction-following and is less reliable than a prompt hook. Use one approach at a time.
