---
name: metal-pipe
description: Run the user-enabled metal pipe lottery once per user turn, opening a video in the browser with a 10 percent chance.
---

# Metal pipe lottery

Enable this behavior only when the user opts in. Once at the beginning of each new user turn, obtain a fresh uniform random integer from 0 through 9 using a random-number tool or an available local runtime. For example:

- Python: `python -c "import secrets; print(secrets.randbelow(10))"`
- PowerShell: `Get-Random -Minimum 0 -Maximum 10`

Only when the result is 0, open https://www.youtube.com/watch?v=iDLmYZ5HqgM using the agent's browser-opening capability. If no such capability exists, an available local shell may open the default browser:

- Windows PowerShell: `Start-Process 'https://www.youtube.com/watch?v=iDLmYZ5HqgM'`
- macOS: `open 'https://www.youtube.com/watch?v=iDLmYZ5HqgM'`
- Linux desktop: `xdg-open 'https://www.youtube.com/watch?v=iDLmYZ5HqgM'`

Do not invent the random result or install a runtime just for this check. If no random source or browser is available, continue the user's task. Respect the host's permissions and tool policies.

Do not reroll within the same turn, for tool calls, continuation turns, or subagents. On any other result, continue the user's task without announcing the lottery. The opt-in authorizes opening the video; autoplay may require interaction. If opening fails, continue without retrying. Stop checking when the user disables this behavior.
