# Metal pipe skill

A 10% chance of [metal pipe](https://www.youtube.com/watch?v=iDLmYZ5HqgM) every time you send your agent a message.

## Install

Choose your agent below. Run the commands from the root of the project where you want the skill enabled. These are project installs, not global installs.

You need [GitHub CLI](https://cli.github.com/) signed in with `gh auth login`. This repository is private, so your GitHub account must have access. Bash commands work on macOS, Linux, and Git Bash; a PowerShell version is below.

### Claude Code

```bash
mkdir -p .claude/skills/metal-pipe
gh api repos/pc386/metal-pipe-skill/contents/metal-pipe/SKILL.md -H 'Accept: application/vnd.github.raw+json' > .claude/skills/metal-pipe/SKILL.md
```

Append this to your project's `CLAUDE.md`:

```text
I opt into the metal pipe lottery. At the beginning of each new user turn, read .claude/skills/metal-pipe/SKILL.md and run its 10% lottery once. Do not reroll for tool calls, continuations, or subagents. Stop when I disable it.
```

Start a new Claude Code session. [Skill docs](https://code.claude.com/docs/en/skills) · [Instruction docs](https://code.claude.com/docs/en/memory)

### Codex

```bash
mkdir -p .agents/skills/metal-pipe
gh api repos/pc386/metal-pipe-skill/contents/metal-pipe/SKILL.md -H 'Accept: application/vnd.github.raw+json' > .agents/skills/metal-pipe/SKILL.md
```

Append this to your project's `AGENTS.md`:

```text
I opt into the metal pipe lottery. At the beginning of each new user turn, read .agents/skills/metal-pipe/SKILL.md and run its 10% lottery once. Do not reroll for tool calls, continuations, or subagents. Stop when I disable it.
```

Start a new Codex chat in the project. [Skill docs](https://learn.chatgpt.com/docs/build-skills) · [Instruction docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

### Cursor

```bash
mkdir -p .cursor/skills/metal-pipe
gh api repos/pc386/metal-pipe-skill/contents/metal-pipe/SKILL.md -H 'Accept: application/vnd.github.raw+json' > .cursor/skills/metal-pipe/SKILL.md
```

Append this to your project's `AGENTS.md`:

```text
I opt into the metal pipe lottery. At the beginning of each new user turn, read .cursor/skills/metal-pipe/SKILL.md and run its 10% lottery once. Do not reroll for tool calls, continuations, or subagents. Stop when I disable it.
```

Start a new Agent chat in the project. [Skill docs](https://prod.cursor.com/docs/skills) · [Instruction docs](https://prod.cursor.com/help/customization/rules)

### GitHub Copilot CLI

```bash
mkdir -p .github/skills/metal-pipe
gh api repos/pc386/metal-pipe-skill/contents/metal-pipe/SKILL.md -H 'Accept: application/vnd.github.raw+json' > .github/skills/metal-pipe/SKILL.md
```

Append this to your project's `.github/copilot-instructions.md`:

```text
I opt into the metal pipe lottery. At the beginning of each new user turn, read .github/skills/metal-pipe/SKILL.md and run its 10% lottery once. Do not reroll for tool calls, continuations, or subagents. Stop when I disable it.
```

Start a new Copilot CLI session in the project. [Skill docs](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) · [Instruction docs](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/comparing-cli-features)

### Windows PowerShell

Use this instead of the Bash download commands. Set `$skillDir` to the directory for your agent:

| Agent | `$skillDir` | Append the opt-in instruction to |
| --- | --- | --- |
| Claude Code | `.claude/skills/metal-pipe` | `CLAUDE.md` |
| Codex | `.agents/skills/metal-pipe` | `AGENTS.md` |
| Cursor | `.cursor/skills/metal-pipe` | `AGENTS.md` |
| GitHub Copilot CLI | `.github/skills/metal-pipe` | `.github/copilot-instructions.md` |

```powershell
$skillDir = '.claude/skills/metal-pipe' # Change for your agent
New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
$skillContent = gh api repos/pc386/metal-pipe-skill/contents/metal-pipe/SKILL.md -H 'Accept: application/vnd.github.raw+json'
if ($LASTEXITCODE -ne 0) { throw 'Skill download failed. Check gh auth status and repository access.' }
$skillContent | Set-Content -LiteralPath "$skillDir/SKILL.md" -Encoding utf8
```

Then add the matching opt-in instruction from your agent's section and start a new session. Preserve existing instruction-file content. Install once per agent/project; if multiple agents share `AGENTS.md`, keep only one lottery instruction and point it to one installed skill.

### Other agents

Copy `metal-pipe/SKILL.md` into your agent's supported skills directory and add [the per-turn instruction](metal-pipe-global-instruction.md) to its persistent instructions, with the installed skill path. If it has no skill system, include the skill's body directly in its persistent instructions.

## How it works

One uniform random integer from 0 through 9 per new user turn. A 0 opens the video. The other nine results do nothing. The skill uses an available random source and browser tool, with default-browser commands for Windows, macOS, and Linux.

The per-turn instruction is necessary: installing a skill alone does not make it run on every message. Instruction following is best effort; guaranteed execution requires the host's turn hooks. Local desktop agents can open your browser; headless/cloud agents need a browser tool and cannot automatically open your local browser. Autoplay may require a click.

## Uninstall

Remove the metal pipe opt-in paragraph from your instruction file and delete the installed `metal-pipe` skill folder. Start a new session. You can also tell the agent to stop the lottery in the current chat.
