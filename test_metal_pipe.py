import contextlib
import io
import unittest
from unittest.mock import patch

import metal_pipe


class LotteryTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
