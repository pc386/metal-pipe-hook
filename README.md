# Metal pipe skill

A Codex skill that opens https://www.youtube.com/watch?v=iDLmYZ5HqgM with a 10% chance per new user turn.

## Install

Copy the `metal-pipe` folder into your Codex skills directory (`~/.codex/skills/`). Append the instruction from `metal-pipe-global-instruction.md` to `~/.codex/AGENTS.md`, preserving any existing instructions.

Start a new chat so Codex loads the new global instruction.

## Behavior

Each new user turn requests one random integer from 0 through 9. Only 0 opens the video. Tool calls, continuations, and subagents do not get extra rolls. Tell Codex to disable the behavior to stop it; remove the global instruction to disable it persistently.

The random check has a 10% chance when executed. Skills and global instructions are followed by the model rather than enforced as runtime hooks, so execution on every turn is best effort. Browser autoplay may require interaction.
