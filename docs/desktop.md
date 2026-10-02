# Desktop app setup

Run the [quick-start installer](../README.md#quick-start) once in Terminal or PowerShell, then use your agent through its GUI. Python 3.9+ is required. Install is user-wide, so you do not need to repeat it per project.

## Codex desktop / ChatGPT

1. Download `metal_pipe.py` with the README's command.
2. Run `python3 metal_pipe.py --install codex` (Windows: `py -3 metal_pipe.py --install codex`). The installer registers the prompt hook in your Codex user configuration.
3. Open Codex CLI under the same user and configuration directory, enter `/hooks`, and review/trust the metal-pipe command. New or changed hooks are skipped until trusted. The documented trust route is CLI-based; this guide does not assume a GUI Hooks button exists.
4. Return to the desktop app and start a new **local Codex session**. Send normal messages; the hook runs independently of the model.
5. Use the test commands below if the video does not open.

ChatGPT Work supports this only where **both orchestration and execution are local**. Selecting Work or granting local computer access does not establish that condition. Local command hooks are not supported with cloud orchestration, even when tools run locally. Ordinary ChatGPT chat has no documented installation route for this hook.

Sources: [desktop app](https://learn.chatgpt.com/docs/app), [hook configuration, trust, and local/cloud support](https://learn.chatgpt.com/docs/hooks).

## Claude Desktop

1. Open Claude Desktop and select **Code**.
2. Select **Local**, then **Select folder**, and choose your project directory.
3. Download `metal_pipe.py` with the README's command and run `python3 metal_pipe.py --install claude` (Windows: `py -3 metal_pipe.py --install claude`). Existing Claude settings are preserved.
4. Start a new **Code → Local** session and complete any normal workspace trust prompts. Desktop and CLI share the hook settings; using the Code tab does not require installing the CLI.
5. Send normal messages or use the test commands below.

This setup is for native local Code sessions. It does not establish command-hook support in Claude Chat or Cowork. Cloud, SSH, and WSL sessions use different execution environments.

Sources: [Desktop quickstart](https://code.claude.com/docs/en/desktop-quickstart), [shared desktop settings](https://code.claude.com/docs/en/desktop), [hooks reference](https://code.claude.com/docs/en/hooks).

## Test from the GUI

Ask your local agent:

> Run my installed ~/.metal-pipe-hook/metal_pipe.py with --test using a working Python interpreter. Open the configured video once. Do not edit any files or change the lottery odds.

The host may ask for normal execution approval. This tests script/browser access. For a silent test, replace `--test` with `--dry-run`.

To check the actual hook, start a fresh session and send ordinary messages without asking the model to run anything. Each registered prompt event has a 10% chance; ten messages can all miss. Check the host's hook registration/trust if manual testing succeeds but automatic use appears inactive.

## Pause or remove it

Ask the agent to run the installed script with `--disable` to pause all agents, or `--enable` to resume. For removal, use `--uninstall codex`, `--uninstall claude`, `--uninstall cursor`, or `--uninstall copilot` as appropriate. The agent must execute the command; merely acknowledging “stop” does not change the hook.

The hook configurations follow official documentation. Automated tests exercise the script and configuration edits; they do not prove compatibility with every desktop app/version. Browser autoplay may require clicking Play.
