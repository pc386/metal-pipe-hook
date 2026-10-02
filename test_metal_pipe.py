import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import metal_pipe


class LotteryTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        patcher = patch.object(metal_pipe, "install_dir", return_value=self.root / "installed")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_only_one_of_ten_results_opens(self):
        for roll in range(10):
            with self.subTest(roll=roll), patch.object(metal_pipe.secrets, "randbelow", return_value=roll) as rng, patch.object(metal_pipe, "open_video") as browser:
                metal_pipe.main([])
                rng.assert_called_once_with(10)
                self.assertEqual(browser.call_count, int(roll == 0))

    def test_dry_run_never_opens(self):
        with patch.object(metal_pipe.secrets, "randbelow", return_value=0), patch.object(metal_pipe, "open_video") as browser, contextlib.redirect_stdout(io.StringIO()) as output:
            metal_pipe.main(["--dry-run"])
            browser.assert_not_called()
            self.assertIn("would_open=True", output.getvalue())

    def test_cursor_continues_after_browser_failure(self):
        with patch.object(metal_pipe.secrets, "randbelow", return_value=0), patch.object(metal_pipe, "open_video", side_effect=OSError), contextlib.redirect_stdout(io.StringIO()) as output:
            metal_pipe.main(["--cursor"])
            self.assertEqual(output.getvalue(), '{"continue":true}\n')

    def test_platform_launchers(self):
        with patch.object(metal_pipe.sys, "platform", "win32"), patch.object(metal_pipe.os, "startfile", create=True) as launch:
            metal_pipe.open_video()
            launch.assert_called_once_with(metal_pipe.VIDEO_URL)
        for platform, command in [("darwin", "open"), ("linux", "xdg-open")]:
            with self.subTest(platform=platform), patch.object(metal_pipe.sys, "platform", platform), patch.dict(metal_pipe.os.environ, {"DISPLAY": ":0"}), patch.object(metal_pipe.subprocess, "Popen") as launch:
                metal_pipe.open_video()
                self.assertEqual(launch.call_args.args[0], [command, metal_pipe.VIDEO_URL])
        with patch.object(metal_pipe.sys, "platform", "linux"), patch.dict(metal_pipe.os.environ, {}, clear=True), patch.object(metal_pipe.subprocess, "Popen") as launch:
            metal_pipe.open_video()
            launch.assert_not_called()

    def test_test_opens_once_without_randomness_even_when_disabled(self):
        with patch.object(metal_pipe, "open_video", return_value=True) as browser, patch.object(metal_pipe.secrets, "randbelow") as rng, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(metal_pipe.main(["--disable"]), 0)
            self.assertEqual(metal_pipe.main(["--test"]), 0)
            browser.assert_called_once()
            rng.assert_not_called()

    def test_disable_and_enable(self):
        with patch.object(metal_pipe, "open_video") as browser, patch.object(metal_pipe.secrets, "randbelow", return_value=0) as rng, contextlib.redirect_stdout(io.StringIO()) as output:
            metal_pipe.main(["--disable"])
            metal_pipe.main(["--cursor"])
            browser.assert_not_called()
            rng.assert_not_called()
            self.assertIn('{"continue":true}', output.getvalue())
            metal_pipe.main(["--enable"])
            metal_pipe.main([])
            browser.assert_called_once()

    def test_test_reports_launch_failure(self):
        with patch.object(metal_pipe, "open_video", side_effect=OSError("no browser")), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(metal_pipe.main(["--test"]), 1)

    def test_installer_preserves_settings_and_is_idempotent(self):
        for agent in metal_pipe.AGENTS:
            with self.subTest(agent=agent):
                config = self.root / (agent + ".json")
                event = {"codex": "UserPromptSubmit", "claude": "UserPromptSubmit", "cursor": "beforeSubmitPrompt", "copilot": "userPromptSubmitted"}[agent]
                other = {"type": "command", "command": "echo unrelated"}
                nested = agent in ("codex", "claude")
                entries = [{"hooks": [other], "matcher": ""}] if nested else [other]
                original = {"unrelatedSetting": True, "hooks": {event: entries, "OtherEvent": []}}
                config.write_text(json.dumps(original), encoding="utf-8")
                with patch.object(metal_pipe, "config_path", return_value=config), contextlib.redirect_stdout(io.StringIO()):
                    metal_pipe.configure(agent)
                    metal_pipe.configure(agent)
                    installed = json.loads(config.read_text())
                    self.assertTrue(installed["unrelatedSetting"])
                    self.assertEqual(installed["hooks"][event][0], entries[0])
                    self.assertEqual(len(installed["hooks"][event]), 2)
                    self.assertEqual((metal_pipe.install_dir() / "metal_pipe.py").read_bytes(), Path(metal_pipe.__file__).read_bytes())
                    self.assertTrue(list(self.root.glob(agent + ".json.metal-pipe-*.bak")))
                    metal_pipe.configure(agent, remove=True)
                    removed = json.loads(config.read_text())
                    if not nested:
                        original["version"] = 1
                    self.assertEqual(removed, original)

    def test_uninstall_preserves_sibling_handler(self):
        config = self.root / "shared.json"
        other = {"type": "command", "command": "echo keep"}
        config.write_text(json.dumps({"hooks": {"UserPromptSubmit": [{"hooks": [other, {"command": metal_pipe.hook_command("codex")}]}]}}))
        with patch.object(metal_pipe, "config_path", return_value=config), contextlib.redirect_stdout(io.StringIO()):
            metal_pipe.configure("codex", remove=True)
        self.assertEqual(json.loads(config.read_text())["hooks"]["UserPromptSubmit"], [{"hooks": [other]}])

    def test_invalid_config_is_not_overwritten(self):
        config = self.root / "broken.json"
        for text in ['{broken', '{"hooks": []}', '{"hooks": {"UserPromptSubmit": "broken"}}']:
            config.write_text(text)
            with patch.object(metal_pipe, "config_path", return_value=config), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(metal_pipe.main(["--install", "codex"]), 1)
            self.assertEqual(config.read_text(), text)

    def test_command_handles_spaces_and_quotes(self):
        import base64
        import shlex
        for platform in ("win32", "linux"):
            with self.subTest(platform=platform), patch.object(metal_pipe.sys, "platform", platform), patch.object(metal_pipe.sys, "executable", "/path with spaces/it's python"), patch.object(metal_pipe, "install_dir", return_value=Path("/path with spaces/it's hook")):
                command = metal_pipe.hook_command("cursor")
                self.assertTrue(metal_pipe.is_ours({"command": command}))
                if platform == "win32":
                    decoded = base64.b64decode(command.split(" -EncodedCommand ")[1]).decode("utf-16-le")
                    self.assertIn("it''s python", decoded)
                    self.assertIn("'--cursor'", decoded)
                else:
                    self.assertEqual(shlex.split(command)[0], "/path with spaces/it's python")
                    self.assertEqual(shlex.split(command)[-1], "--cursor")


if __name__ == "__main__":
    unittest.main()
