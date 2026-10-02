# Metal pipe skill

An agent-agnostic skill that opens https://www.youtube.com/watch?v=iDLmYZ5HqgM with a 10% chance per new user turn.

## Install

If your agent supports skills with a `SKILL.md` entry point, copy the `metal-pipe` folder into its configured skill directory. Otherwise, include the contents of `metal-pipe/SKILL.md` in the agent's persistent instructions.

Add the instruction from `metal-pipe-global-instruction.md` to the agent's persistent instructions, adjusting the skill path to your installation. Use the instruction file or settings supported by your agent, and preserve existing instructions. Reload instructions or start a new chat as required by your host.

The files do not depend on a particular agent, plugin, or browser API. The agent needs an available random source and a browser-opening tool or local desktop shell. Windows, macOS, and Linux browser commands are included in the skill. A headless environment without browser access cannot open the video on your desktop.

## Behavior

Each new user turn requests one uniform random integer from 0 through 9. Only 0 opens the video. Tool calls, continuations, and subagents do not get extra rolls. Tell your agent to disable the behavior to stop it; remove the persistent instruction to disable it permanently.

The random check has a 10% chance when executed. Instruction-based selection is best effort and cannot guarantee execution on every turn. A guaranteed per-turn trigger requires integration with your host's turn hooks. Browser autoplay may require interaction.
