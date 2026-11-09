# NYZ

Multiplayer open-world zombie survival game: DayZ + Project Zomboid, with survival mechanics from Ark. Set in New York City at 1:1 scale. Unreal Engine 5, PC first, 250–300 players per server at launch (500 later if budget allows).

## Before doing anything

Read [docs/GDD.md](docs/GDD.md). It is the main source for the game's design.

## Design-doc rules

- Write every design detail the user gives into `docs/GDD.md` in the same turn. Don't summarize detail away; the user wants it kept thorough.
- When a decision is made, changed or reversed, update the GDD **and** add an entry to `docs/DECISIONS.md` with the date and the reason.
- If a new idea conflicts with something already in the GDD, point out the conflict before writing it down.
- Move answered items out of the GDD's "Open questions" section and into the section they belong in.
- The GDD holds the agreed high-level design. **Each system gets a deeper design pass when we start building it**; update its GDD section (and the decision log) then.

## Lore rules: nothing gets lost between chats

The developer wants the lore saved in extreme detail. These rules apply to every session.

- **Before any lore discussion, read [docs/lore/LORE.md](docs/lore/LORE.md) in full**, plus the most recent lore entries in `docs/DECISIONS.md`. Don't rely on summaries.
- **Lore stays in this private docs repo (NYZ-DOCs, the developer only).** Never copy lore, `docs/DECISIONS.md` or the transcripts into the game repo (NYZ), which volunteers may get.
- **The lore bible is the home of all lore.** The GDD only gets a spoiler-free summary (§23) and gameplay-facing facts. **The truth and the twist never go in the GDD** (volunteers may read it).
- **Record every lore detail the developer gives in the same turn, in full.** Never summarize it away. For key ideas, **keep the developer's own wording** (quote it), then the cleaned-up version. Note the date and **who proposed it** (developer or Claude).
- **Append every lore message from the developer, verbatim, to [docs/lore/developer-words.md](docs/lore/developer-words.md)**, with a one-line note on what it was answering.
- **Record what was rejected or not chosen, and why**, so ideas aren't re-proposed and can be revisited.
- **Claude's proposals that are still waiting for an answer** go in the lore bible under **"Pending proposals"**, with every option, so they survive if the chat ends before the developer replies. Remove them once answered.
- **Keep the two layers separate and labeled:** *the truth* versus *what survivors believe*.
- **When a lore decision changes earlier lore, update every place it appears** (lore bible, GDD §23, notes on older decision-log entries) and log the change. Search the docs for the old wording to find every place.
- **Check new lore against "What the lore has to explain"** in the lore bible and against earlier decisions; point out conflicts before writing.
- **Check names for real-world clashes** (web search: games, films, books, real drugs and brands) before locking them in, and record the result.
- **Every lore decision also gets a `docs/DECISIONS.md` entry.**
- **End of each lore turn:** tell the developer, in one line, what was recorded and where.
- **Raw transcripts** live in `docs/transcripts/`: the full export (`.zip`, from the app's session export) plus a readable Markdown version made with `python tools/transcript_to_md.py <export.zip> <out.md> "<title>"`. When a question is about *why* something was decided or exactly what the developer said, search the `.md` transcripts. **Offer to export a fresh transcript at the end of any session with substantial design or lore work.**

## Map tooling

- `tools/map/` builds the map border from OpenStreetMap data (needs Python with `shapely`). The segment list at the top of `build_border.py` *is* the border definition; outputs go to `docs/map/`.
- Public Overpass servers are often overloaded; `fetch_routes.py` uses Nominatim plus the main OSM API instead. Python's certificate store fails on these hosts here, so fetching goes through `curl`.

## Repos and project layout

- **This folder is the docs repo**, [NYZ-DOCs](https://github.com/NNarwhall/NYZ-DOCs) (private, the developer only).
- **The Unreal 5.8 C++ project is in the `NYZ` subfolder** (`C:\Game Dev Folder\NYZ\NYZ`), which is **its own git repo**, [NYZ](https://github.com/NNarwhall/NYZ), with UE5 ignore and LFS rules. The docs repo ignores that folder. Commit game changes from inside it and docs changes from here.
- Both repos commit as `NNarwhall` with the GitHub noreply address; the developer's GitHub login is saved in Git Credential Manager, so pushes don't ask.
- **Visual Studio:** VS Community 2026 (game, desktop C++ and .NET desktop workloads). Unreal 5.8.4 builds with its MSVC 14.50 toolchain, which is on Epic's preferred list. VS 2022 17.7.6 stays for the old 5.3 project. The launcher copy of Unreal is 5.8.4.
- **Compiling the game:** from PowerShell (Bash breaks on the spaced path), `& "C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\Build.bat" NYZEditor Win64 Development "-Project=C:\Game Dev Folder\NYZ\NYZ\NYZ.uproject" -WaitMutex`. Close the editor first; new C++ classes need a full build, not Live Coding.
- **Headless network check** (works without the source build): server `UnrealEditor.exe "<NYZ.uproject>" -server -nullrhi -nosound -log` (loads the default map, the load-test map), client `UnrealEditor.exe "<NYZ.uproject>" 127.0.0.1 -game -nullrhi -nosound -log`; look for "Join succeeded" in the server log. The `LogPython: Error` lines from the EditorToolset and ToolsetRegistry plugins' startup scripts in these modes are harmless noise.
- **Load-test map** (`/Game/Maps/LoadTestMap`): rebuilt by `Tools/build_load_test_map.py` in the game repo; the run command is in its header. It runs in an editor with no window (`-ExecutePythonScript`), not as a commandlet, where placing actors fails.
- **Load-test bots:** `powershell -ExecutionPolicy Bypass -File "C:\Game Dev Folder\NYZ\NYZ\Tools\run_bots.ps1" -Count N` (works from any folder; Windows blocks `.ps1` files by default, and Bypass allows just that run) starts a headless server (editor program) and N bots running the packaged game (`-bot`); `-Stop` prints the run's server numbers (also added to `Saved/LoadTest/results.txt`) and ends exactly those processes, never the developer's editor. Iris is on (`Config/DefaultEngine.ini`), so the editor must be restarted after that setting changes to join a test server. Logs go to `NYZ/Saved/LoadTest`. After code, content or settings changes, repackage with `-Package` (editor closed: packaging also builds the editor target, which Live Coding blocks; about 5 minutes).
- **Noclip while testing:** console `ServerExec ghost` / `ServerExec walk` when joined to a server (development builds allow cheats on every server); plain `ghost` / `walk` in Play without a server.
- **Unreal MCP:** Unreal's built-in MCP plugin (experimental, editor builds only) serves `http://127.0.0.1:18000/mcp` and starts with the editor (per-user setting in `NYZ/Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini`). Not the default port 8000, which the developer's trading-terminal backend uses. Registered in Claude Code at local scope as `unreal-mcp`. The tools come from the EditorToolset and LiveCodingToolset plugins (enabled 2026-11-08); a session only sees the tools if it started while the editor was running.

## Pending reminders

- **Pick up here (the developer stopped for the night, 2026-11-08):** next is the first **stage 1 load-test runs at 10, 15 and 20 bots** (GDD §24 point 6), with the editor closed and the PC otherwise idle. For each: `run_bots.ps1 -Count N`, let it run a few minutes with every bot in, then `-Stop`; compare the lines in `NYZ/Saved/LoadTest/results.txt` (ignore its first line, 2026-11-08 23:29, from before the Iris and Windows-timer fixes). Then zombies (point 4), then rerun.

- **Engine source build**: the developer is downloading the Unreal 5.8.4 source zip (2026-11-08; suggested location `C:\UE\5.8`). Still to do, before the dedicated-server load test: run `Setup.bat`, `GenerateProjectFiles.bat`, then build.
- **Older Unreal projects exist** in `Documents\Unreal Projects`: "NYZ - Copy" (UE 5.3, C++), "NYZv409" (UE 5.8, Blueprint only), CityTest and RoadTesttttt (UE 5.8). **Nothing carries over** (the developer, 2026-11-08): the new project starts fresh, and NYZv409 stays as a reference backup only.
- **Lore revisit**: the developer wants to revisit the entire lore later in development, not now (said 2026-11-08). Don't start lore work unprompted. When work reaches lore-heavy content (points of interest, safe zones, radio broadcasts), remind them the revisit is still pending.
