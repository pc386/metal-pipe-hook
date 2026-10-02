---
name: metal-pipe
description: Run the user-enabled metal pipe lottery once per user turn, opening a video in the browser with a 10 percent chance.
---

# Metal pipe lottery

The user has opted into this browser surprise. Once at the beginning of each new user turn, draw a fresh integer with PowerShell:

```powershell
Get-Random -Minimum 0 -Maximum 10
```

Only when the result is 0, open https://www.youtube.com/watch?v=iDLmYZ5HqgM in the browser using the available browser-opening tool (such as open_in_codex with a browser target). On Windows, if no browser-opening tool exists, use `Start-Process` with this URL to open the default browser.

Do not invent the random result. Do not reroll within the same turn, for tool calls, continuation turns, or subagents. On any other result, continue the user's task without announcing the lottery. Opening the video is authorized by this opt-in; browser autoplay may still require interaction. If opening fails, continue the task without retrying. Stop checking when the user disables this behavior.
