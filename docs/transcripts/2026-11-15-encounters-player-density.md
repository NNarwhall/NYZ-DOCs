# Design pass: encounters and player density (2026-11-15)

Readable transcript: the developer's messages and Claude's replies only. The full export (tool calls, screenshots, metadata) is in the matching .zip.

---

### Developer (2026-11-15 17:58)

Background (from the session that started this one):
NYZ is a multiplayer zombie survival game set in New York City at 1:1 scale (Unreal 5.8), with the docs repo at `C:\Game Dev Folder\NYZ` (read `CLAUDE.md` and `docs/GDD.md` first; follow CLAUDE.md's design-doc rules: record every design detail in the GDD in the same turn, decisions also in `docs/DECISIONS.md`, consult the developer before deciding anything, plain short language, recommended defaults). The launch target is 250–300 players per server, 500 later (GDD §2), on about 680 km² of land (GDD §5). The developer raised on 2026-11-15, for the third time, that 300 players is not enough for the map: "with dense city buildings (not many open fields or sightlines) you might go 10 hours without seeing anybody". The earlier rounds (2026-11-08, 2026-11-10) and the new one are in GDD §5 under "Player density", with Claude's answer (sightlines in a city show maybe a tenth to a twentieth of the area DayZ's fields do, so meetings are several times rarer than density suggests) and five undecided levers; it is also in the GDD's Open questions.

Task:
Run a design pass with the developer on how often players meet on the NYC map, and what to change so the map never feels empty. Read GDD §5 "Player density" (the three rounds and the five levers: where players go via spawns, hotspots and chokepoints; sound carrying further than sight; events that pull people in; a smaller or population-scaled playable area; more players), plus the GDD sections they touch (§10 respawn and spawn neighbourhoods, §18 safe zones, §16 vehicles, §8 zombie noise, §24 server budget and load tests). Bring the developer a short recommendation with options and defaults, ask before deciding, and record the outcome in the GDD (§2 and §5, the Open questions entry moved out once answered) and `docs/DECISIONS.md`. Done when the developer has decided how the game handles encounter rate at 300 players and the docs say so. Docs repo only; commit nothing unless asked; don't touch `tools/map/` or the game repo (another session is working there).

Shared notes folder for this group of sessions (outside the repo; read siblings' notes there, leave hand-over notes or large findings there instead of pasting them into messages): C:\Users\Paul\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\side-session-notes\local_1dbe23da-073e-4997-aa76-7ab845c1d758

### Claude (2026-11-15 17:58)

Reading the GDD sections the player-density question touches; then I'll bring you a short recommendation.

### Developer (2026-11-15 18:03)

Your questions have been answered: "Player count on the NYC map: rough math says 300 spread evenly meet about every 1–3 hours, every 15–40 min where most gather, and 500 only shortens waits by ~40%. What should the launch player count be?"="Make 500 the launch target", "Which ways of pulling players together should NYZ use? I recommend all four."="Spawns + many hotspots,World events,Signs of life from afar", "Should the playable area change with how many players a server has? (A smaller map conflicts with §5's full 1:1 city; bases inside a closed area are the hard part.)"="Whole map always open (Recommended)", "What counts as 'not empty'? A target lets playtests check it: the server would log, per player, the minutes between seeing or hearing another player."="15–30 min, busy areas (Recommended)". You can now continue with these answers in mind.

### Developer (2026-11-15 18:05)

The user answered: "500 players is now the launch target. If the optimized server still can't hold 500 when the game is ready to launch, what happens?"="Hold launch until 500 works", "Server budgets were written for 300 players (zombies: 30% of the main thread, 20 awake per player). Today's costs put 500 players at roughly 2.5× one main thread, so everything must get about 3× cheaper. How should the budgets change?"="Restate them at 500 now (Recommended)", "You didn't pick 'loud sounds carry far'. Players farther than 500 m aren't sent to you at all, so as things stand a gunshot 600 m away would be silent. Which do you want?"="whatever is realistic. maybe without a lot of city  noise it would carry a bit more, idk". Read the answers carefully — they may request clarification, changes, or that you not proceed — and follow what they actually say.

### Claude (2026-11-15 18:07)

Now writing it into the docs.

### Claude (2026-11-15 18:07)

Now §2, §3, §8, §10, §11, §12, §13, §15, §24, Systems to design and Open questions.

### Claude (2026-11-15 18:08)

Adding the decision-log entry and marking the older player-count entries as changed.

### Claude (2026-11-15 18:09)

The encounters design pass is decided and written into the docs repo, mostly under a new "Encounters" section in [GDD.md](docs/GDD.md) §5. Nothing is committed, and the game repo and `tools/map/` are untouched.

**What you decided:**
- **500 players per server at launch, and no launch below 500.** If the server can't hold 500, the launch waits. This went against my pick (keep 300, 500 later).
- **Every server budget is restated at 500.** Zombies keep 30% of the server's main thread. That means about 12 awake per player instead of 20, still about 6,000 in total.
- **The goal:** in the busy parts of the map, you see or hear another player about every 15–30 minutes. The outer boroughs may stay quiet. Playtests will check this with a server log of the minutes between encounters for each player.
- **The whole map is always open** on every server.
- **Pulls toward where players gather:**
  - 2–3 spawn neighbourhoods per borough, none at the far edges, each a short walk from a bridge or hotspot.
  - Good loot spread over many medium hotspots, such as hospitals and police precincts.
  - World events, like supply drops and crashes.
  - Signs of life seen from far: smoke, lit windows, flares.
- **Far gunshots are "whatever is realistic".** My starting numbers, to tune: pistol about 1.5 km, rifle about 3 km, explosions about 5 km. Zombies' hearing distances stay separate, so a rifle doesn't pull hordes from across the city.

**Where it's recorded:**
- **GDD:** also §2, §3, §8 (zombie budget), §10, §12, §13, §15 and §24. World events are added to "Systems to design", and the "Enough players?" open question is removed.
- **Decision log:** a new entry in [DECISIONS.md](docs/DECISIONS.md), with "changed" notes on the older player-count and zombie-budget entries.
- **Other files:** [CLAUDE.md](CLAUDE.md)'s summary line now says 500. [animations-to-make.md](docs/animations-to-make.md) has a new road flare row (THR-005) and world events under "Still to be added".

**Things to know:**
- At today's measured costs, 500 players need roughly 2–2.5 times what one server thread can do. Everything has to get about 3 times cheaper, and with "no launch below 500" that optimizing now gates the launch.
- The 1–3 hour and 15–40 minute meeting estimates are rough math, not measured. The playtest log is what will settle them.
- Who sends the world events waits for the lore revisit, which is still pending.

### Developer (2026-11-15 18:10)

Export it

### Claude (2026-11-15 18:11)

The readable transcript dropped the question dialogs, so your choices were missing. I'm fixing the converter so they're kept.

### Developer (2026-11-15 18:11)

'At today’s measured costs, 500 players need roughly 2–2.5 times what one server thread can do. Everything has to get about 3 times cheaper, and with “no launch below 500” that optimizing now gates the launch.' Can we not just find better servers?

### Developer (2026-11-15 18:11)

for the real thing
