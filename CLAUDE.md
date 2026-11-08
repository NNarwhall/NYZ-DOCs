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

## Pending reminders

- **Game repo**: this folder is the docs repo ([NYZ-DOCs](https://github.com/NNarwhall/NYZ-DOCs), connected 2026-11-08). The game repo, [NYZ](https://github.com/NNarwhall/NYZ), is still empty: set it up with UE5 ignore and LFS rules **when the UE5 project is created**, before anything is committed to it.
- **Engine source build**: the developer is downloading the Unreal 5.8.4 source zip (2026-11-08; suggested location `C:\UE\5.8`). Still to do, before the dedicated-server load test: check Visual Studio 2022's C++ components, run `Setup.bat`, `GenerateProjectFiles.bat`, then build. The launcher copy is being updated from 5.8.3 to 5.8.4.
- **Lore revisit**: the developer wants to revisit the entire lore later in development, not now (said 2026-11-08). Don't start lore work unprompted. When work reaches lore-heavy content (points of interest, safe zones, radio broadcasts), remind them the revisit is still pending.
