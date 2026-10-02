#!/usr/bin/env python3
"""A 10% browser lottery, with installation and controls for local coding agents."""

import argparse
import base64
import json
import os
from pathlib import Path
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

VIDEO_URL = "https://www.youtube.com/watch?v=iDLmYZ5HqgM"
AGENTS = ("codex", "claude", "cursor", "copilot")
MARKER = "--metal-pipe-hook"


def install_dir():
    return Path.home() / ".metal-pipe-hook"


def config_path(agent):
    home = Path.home()
    return {
        "codex": Path(os.environ.get("CODEX_HOME", home / ".codex")) / "hooks.json",
        "claude": home / ".claude" / "settings.json",
        "cursor": home / ".cursor" / "hooks.json",
        "copilot": Path(os.environ.get("COPILOT_HOME", home / ".copilot")) / "hooks" / "metal-pipe.json",
    }[agent]


def hook_command(agent):
    args = [sys.executable, str(install_dir() / "metal_pipe.py"), MARKER]
    if agent == "cursor":
        args.append("--cursor")
    if sys.platform == "win32":
        # Encoded PowerShell preserves paths with spaces and shell metacharacters.
        script = "& " + " ".join("'" + arg.replace("'", "''") + "'" for arg in args)
        encoded = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
        return "powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -EncodedCommand " + encoded
    return shlex.join(args)


def is_ours(handler):
    command = handler.get("command", "")
    if not isinstance(command, str):
        return False
    if " -EncodedCommand " in command:
        try:
            command = base64.b64decode(command.split(" -EncodedCommand ", 1)[1], validate=True).decode("utf-16-le")
        except (ValueError, UnicodeError):
            return False
    return MARKER in command.split() or ("'" + MARKER + "'") in command.split()


def configure(agent, remove=False):
    path = config_path(agent)
    data = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}
    if not isinstance(data, dict) or not isinstance(data.get("hooks", {}), dict):
        raise ValueError(f"Expected a JSON object and hooks object in {path}")
    if agent in ("cursor", "copilot") and data.get("version", 1) != 1:
        raise ValueError(f"Unsupported hook config version in {path}")
    event = {"codex": "UserPromptSubmit", "claude": "UserPromptSubmit", "cursor": "beforeSubmitPrompt", "copilot": "userPromptSubmitted"}[agent]
    nested = agent in ("codex", "claude")
    hooks = data.setdefault("hooks", {})
    entries = hooks.get(event, [])
    if not isinstance(entries, list):
        raise ValueError(f"Expected a hook list for {event}")
    kept = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Expected hook objects; configuration left unchanged")
        if nested:
            handlers = entry.get("hooks")
            if not isinstance(handlers, list) or any(not isinstance(h, dict) for h in handlers):
                raise ValueError("Expected a handlers list; configuration left unchanged")
            remaining = [h for h in handlers if not is_ours(h)]
            if remaining or not handlers:
                kept.append({**entry, "hooks": remaining})
        elif not is_ours(entry):
            kept.append(entry)
    if not remove:
        handler = {"type": "command", "command": hook_command(agent)}
        handler["timeoutSec" if agent == "copilot" else "timeout"] = 5
        kept.append({"hooks": [handler]} if nested else handler)
        if agent in ("cursor", "copilot"):
            data.setdefault("version", 1)
    if kept:
        hooks[event] = kept
    else:
        hooks.pop(event, None)
    if remove and not path.exists():
        print(f"No {agent} hook installed.")
        return
    # Validate before copying the script or touching the user's config.
    if not remove:
        target = install_dir() / "metal_pipe.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        if Path(__file__).resolve() != target.resolve():
            shutil.copyfile(__file__, target)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(path.name + f".metal-pipe-{time.time_ns()}.bak")
        shutil.copy2(path, backup)
        print(f"Backup: {backup}")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f"{'Removed' if remove else 'Installed'} {agent} hook: {path}")
    if not remove:
        print("Start a new agent session. Codex requires reviewing/trusting the hook with /hooks.")


def open_video():
    if sys.platform == "win32":
        os.startfile(VIDEO_URL)
        return True
    if sys.platform == "darwin" or (
        sys.platform.startswith("linux")
        and (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    ):
        command = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.Popen(
            [command, VIDEO_URL], stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return True
    return False


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--install", choices=AGENTS, help="Install or update a user-level hook")
    actions.add_argument("--uninstall", choices=AGENTS, help="Remove only this agent's hook registration")
    actions.add_argument("--disable", action="store_true", help="Pause all installed metal-pipe hooks")
    actions.add_argument("--enable", action="store_true", help="Resume all installed metal-pipe hooks")
    actions.add_argument("--test", action="store_true", help="Open the video once, even while paused")
    actions.add_argument("--dry-run", action="store_true", help="Print a roll without opening anything")
    parser.add_argument("--cursor", action="store_true", help="Emit Cursor's continue response")
    parser.add_argument(MARKER, action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    paused = install_dir() / "disabled"
    try:
        if args.install or args.uninstall:
            configure(args.install or args.uninstall, remove=bool(args.uninstall))
            return 0
        if args.disable:
            paused.parent.mkdir(parents=True, exist_ok=True)
            paused.touch()
            print("Metal pipe paused for all agents.")
            return 0
        if args.enable:
            paused.unlink(missing_ok=True)
            print("Metal pipe enabled for all agents.")
            return 0
        if args.test:
            if not open_video():
                print("No supported local desktop browser environment found.", file=sys.stderr)
                return 1
            print("Browser launch requested. Click Play if autoplay is blocked.")
            return 0
        if args.dry_run:
            roll = secrets.randbelow(10)
            print(f"roll={roll}; would_open={roll == 0 and not paused.exists()}; paused={paused.exists()}")
        elif not paused.exists() and secrets.randbelow(10) == 0:
            open_video()
    except (OSError, ValueError) as error:
        if args.install or args.uninstall or args.test or args.disable or args.enable or args.dry_run:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        # Hook errors must not block the user's prompt.
    if args.cursor and not args.dry_run:
        print('{"continue":true}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
