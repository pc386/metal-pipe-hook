#!/usr/bin/env python3
"""One 10% browser lottery per prompt hook invocation; no prompt data is read."""

import argparse
import os
import secrets
import subprocess
import sys

VIDEO_URL = "https://www.youtube.com/watch?v=iDLmYZ5HqgM"


def open_video():
    if sys.platform == "win32":
        os.startfile(VIDEO_URL)
    elif sys.platform == "darwin" or (
        sys.platform.startswith("linux")
        and (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    ):
        command = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.Popen(
            [command, VIDEO_URL],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cursor", action="store_true", help="Emit Cursor's continue response")
    parser.add_argument("--dry-run", action="store_true", help="Print a roll without opening anything")
    args = parser.parse_args(argv)
    try:
        roll = secrets.randbelow(10)
        if args.dry_run:
            print(f"roll={roll}; would_open={roll == 0}")
        elif roll == 0:
            open_video()
    except OSError:
        pass  # A browser or randomness failure must not block the user's prompt.
    if args.cursor and not args.dry_run:
        print('{"continue":true}')


if __name__ == "__main__":
    main()
