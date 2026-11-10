# NYZ — Game Design Document

> This file is the main source for the game's design. Update it as soon as something is decided.
> Each change, with the reason for it, also goes in [DECISIONS.md](DECISIONS.md).

**Last updated:** 2026-10-27

---

## 1. Vision

A multiplayer, open-world zombie survival game that blends DayZ, Project Zomboid and Ark.

### Design principle: easy to learn
The game should be enjoyable for an **average player**. Project Zomboid takes a long time to learn, and NYZ should not. When a system could be deeper or simpler, choose the version an average player picks up quickly.

### From DayZ
- **Open world**
- **Engaging PvP**
- **Gear is looted from the world**

### From Project Zomboid
- **Survival simulation, but less deep than Zomboid.** It should be deep enough to matter without a long learning curve (see the design principle above).
- **Zombie horde behavior**

### From Ark
- **Leveling / skill system.** Progress **can be lost on death but recovered** (see §6).
- **Base building**
- **Clans**
- **Crafting**

### Other features
Features beyond the list above may blend mechanics from several games rather than come from a single one.

---

## 2. Fundamentals (decided)

| Topic | Decision |
|---|---|
| Project name | **NYZ** ("New York Z"). This is the **project codename, not the final game name.** Final title: _TBD_ |
| Engine | **Unreal Engine 5.8.** Dedicated servers (§3) need Unreal built from source; the Epic Launcher version can't build them. (Version picked 2026-11-08: the newest one installed.) |
| Team | **Solo developer for now.** Open to unpaid volunteers (friends, or people who share the vision and are committed to it). |
| Multiplayer | **250–300 players per server at launch.** Up to **500** later if the budget allows. (Raised from 100+ on 2026-10-27: 100 players would feel like a ghost town on this map.) |
| Camera | **First person and third person**, switchable like in DayZ |
| Platform | **PC first.** Consoles are a goal for later, not a launch target. |
| Budget | **None for now** (the developer, 2026-11-08). Development uses free tools and free options; anything that costs money (test machines, hosting) waits for free credit or the developer's OK. |

---

## 3. Technical implications of the fundamentals

These aren't design choices. They follow from section 2 and limit everything else.

- **Dedicated, server-authoritative servers.** At 250–300 players, servers have to be dedicated machines, and the server decides the outcome of every action (loot, damage, building). Clients only send input and display the result. This is the main defence against cheating.
- **Replication at 250–300 players is the biggest technical risk in the project.** Most Unreal multiplayer games ship with around 100 players per server; 250–300 is well beyond that, and 500 further still. Unreal's default replication won't handle it as-is. Options to evaluate: **Iris** (UE5's newer replication system), **Replication Graph** (what Fortnite uses for 100 players), and aggressive relevancy/net culling. If one server process can't hold the target, the fallback is splitting the map across several server processes, which is a large engineering project of its own. **This has to be proven early with a load test at 300**, not discovered near the end. _Plan: milestone 1 (§24)._
  - **Player cap is a server setting**, so servers can run lower if the load test or hosting cost demands it.
  - **Players see each other up to 500 m** (the developer, 2026-11-08: "500 m", choosing between 500 m and 1 km). The server sends nobody farther away than that, so a player farther off doesn't show, even through a scope. The server's cost grows with this distance; Unreal's default is 150 m. Set on the test character, so the load test measures it. A starting number, changed after the test if long-range shooting needs more. _Not chosen:_ 1 km (Claude's other option).
  - **How to test without 300 people:** headless bot clients (launched with `-nullrhi -nosound`) connect to a dedicated server and run a simple bot script (move, sprint, loot, shoot). About 20–30 fit on the developer's PC when the bots run the packaged game (measured 2026-11-08, §24); rent several cloud machines for 300. Measure server tick rate, bandwidth per player, and server CPU/memory with Unreal Insights. Simulate lag and packet loss with UE5's network emulation.
- **Zombie count is the hardest number in the game.** Every zombie runs its AI on the server and has to be replicated. That cost multiplies with 250–300 players spread across a map, since more of the map has players near it and so more zombies need full AI. We'll need AI LOD: full AI near players and cheap or dormant AI far away. **Mass Entity** (UE5's crowd framework) is an option for hordes. Target zombie count per server: _TBD_.
- **First and third person.** The third-person camera lets players look over walls and around corners without exposing themselves. DayZ deals with this through first-person-only servers. **Decided: a server setting, "first person only" or "both"; official servers offer both kinds (§17).**
- **Consoles later.** Nothing has to be built for consoles now, but avoid things that are hard to undo: mouse-only UI, performance budgets that only high-end PCs can meet. Console certification and crossplay are each a project of their own.

---

## 4. Team & collaboration

- **Contributor agreement before anyone contributes.** With unpaid volunteers, get a simple written agreement up front that covers who owns the code and art they make, and what they get if the game earns money. This prevents ownership disputes later. Use a standard template, or a lawyer once money is involved.
- **Source control (decided 2026-11-08): Git + Git LFS, in two private GitHub repos.** UE5 projects contain large binary assets, so plain Git won't handle them well; LFS stores those separately.
  - **[NYZ-DOCs](https://github.com/NNarwhall/NYZ-DOCs):** this GDD, the decision log, the lore bible, the transcripts and the map tools. **Only the developer has access**, because the lore's truth and twist are spelled out in the lore bible, the decision log and the transcripts. Volunteers can be given this GDD on its own, since it holds no spoilers.
  - **[NYZ](https://github.com/NNarwhall/NYZ):** the UE5 game project, the repo volunteers would get. Set up with UE5 ignore and LFS rules when the project is created. **Lore never goes in it.**
  - _Not chosen:_ Perforce (the UE industry standard, with a free tier for small teams), and one repo for everything (anyone given access would see the lore, and splitting a repo's history later is messy).

---

## 5. World & setting

- **New York City, the real city.** The wider New York State may come later as **DLC**.
- **1:1 scale in size.** The map matches NYC's real size and layout. Individual details (every building, sign, mailbox) don't have to match the real ones.
- **Naming rule (decided 2026-10-27):** **real NYC neighborhood and street names** are used; **all events are fictional.** **Exception: trademarked or branded names** (e.g., stadiums named after sponsors such as Citi Field or Barclays Center, team-owned names like Yankee Stadium, privately owned landmark buildings) get fictional versions. _To check each landmark before use._
- **Look and feel: an overgrown, beaten-down NYC.** Nature is taking the city back, to the point that **wild animals have returned**, including animals from the north making their way into the city (§22). _Added by the developer, 2026-10-27._
  - _Analysis:_ overgrowth like this takes years, so it implies the outbreak happened years before the game starts. **Decided (lore timeline, 2026-10-27): the game starts 8 years after the outbreak, and the city fell about 6 years before the game** (§23). It also suits procedural generation: vegetation through cracks, vines on buildings and trees in streets can be placed by rules across the whole map.
- **Launch map area: not final yet.**
  - **First rough sketch** (Google Earth, 2026-10-27, [screenshot](images/launch-map-area.webp)): about 782 km² including water. **It's an estimate only, not the layout.** It roughly covered Manhattan, the Bronx, Brooklyn, Queens, part of New Jersey along the Hudson and the western edge of Nassau County, with Staten Island outside.
  - **New Jersey is included**, but not necessarily everything in the sketch. Current extent: see draft v2 below.
  - "Manhattan map" in chat was a slip: the launch map is wider than Manhattan alone.
  - **Current border: draft v2** (below). The full change history is in [docs/map/border-notes.md](map/border-notes.md).
- **Map border: a quarantine wall** along the land edges. It has to make sense in-world, so it follows **major highways or major streets**, never random side streets.
  - **Method:** the border is built from OpenStreetMap road data so it follows the roads exactly. The script is `tools/map/build_border.py` (the segment list at the top is the border definition; fetch roads with `tools/map/fetch_routes.py`). Output: `docs/map/border-draft.geojson`, `docs/map/border-draft.kml` (opens in Google Earth) and `docs/map/preview.html`. View the preview through a local server (`python -m http.server 8765` in `docs/map`, then open `http://127.0.0.1:8765/preview.html`); OpenStreetMap's map tiles don't load when the file is opened directly.
  - **Draft v2 (2026-10-27, current): about 910 km² (351 sq mi) including water** (harbor, Jamaica Bay, a strip of ocean, the Hudson, part of the Sound). **Land only: about 680 km² (about 260 sq mi), ±10%**, about 3× DayZ's Chernarus. The land figure is worked out from known borough and town land areas minus the parts cut out, not measured from the map; an exact figure needs coastline data. Clockwise:
    - **North (Bronx):** from the Hudson at Riverdale, connector to **East 233rd Street**, east past Woodlawn, then the **Hutchinson River Parkway** south. Roughly the city line: Yonkers, Mount Vernon and Pelham are out; **Co-op City and Bay Plaza are in.**
    - **East:** across Pelham Bay Park to the Sound, down the Sound **east of the Throgs Neck Bridge** into Little Neck Bay (Fort Totten in), then the **Cross Island Parkway** briefly, the **Clearview Expressway (I-295)**, **Francis Lewis Blvd**, **Springfield Blvd** and **Rockaway Blvd** along JFK's east edge. Both the Throgs Neck and Whitestone bridges, their highways and **JFK** are in; far-east Queens is out.
    - **South-east:** through Head of Bay to Far Rockaway, then **Beach 9th Street** to the ocean. **The whole Rockaway peninsula is in**, including Breezy Point.
    - **South:** through the ocean and the Lower Bay to Staten Island.
    - **Staten Island:** **Staten Island Expressway** from the Verrazzano to **Clove Road**, then Clove Road north to the Kill Van Kull.
    - **New Jersey:** through Newark Bay and up the Hackensack River, then **Pulaski Skyway → Tonnelle Avenue** (US 1-9) → **Broad Avenue** → **Grand Avenue** → **Fort Lee Road** → **US 1-9** to the GWB, meeting the Hudson north of the bridge. In: Bayonne, Jersey City, Hoboken, Weehawken, Union City, West New York, Guttenberg, Fairview, Cliffside Park, Edgewater, south Fort Lee, Palisades Park. Out: Secaucus, Ridgefield Park, the Meadowlands, north Leonia.
    - **Back north** up the Hudson to Riverdale.
  - **Placeholders still needing a real road:** across Pelham Bay Park; Fort Wadsworth to the Verrazzano.
  - **Connectors** (land stretches without a road, accepted by the developer) are listed in the change list.
- **Staten Island: only a few square miles are in, not the whole island.**
  - Land access still works: **the Verrazzano Bridge is intact** (no destroyed bridge for now).
  - A **boat from Manhattan is faster** than walking to the bridge, so boats are the practical way there.
  - **Draft v1's piece is kept:** north-east corner, St. George to Fort Wadsworth, west to Clove Road. About **22 km² (8.6 sq mi) including the water at its edges.**
- **George Washington Bridge: crossable, never blocked.** The border meets the Hudson north of it.
- **Throgs Neck Bridge, Bronx–Whitestone Bridge and JFK** are inside the map.
- **Pending border changes** are collected in [docs/map/border-notes.md](map/border-notes.md) and applied together in the next draft.
- The developer knows this is extremely hard for a solo developer and plans to rely heavily on AI-assisted development.

### Points of interest collected so far
A running list from other sections; the full points-of-interest pass is still to do.
- **Combat and base locations** (§18): Grand Central Terminal, Yankee Stadium, Barclays Center, Citi Field. _Branded names likely need fictional versions (naming rule above)._
- **Port container yards** (§12): Red Hook, South Brooklyn Marine Terminal, Port Jersey, Brooklyn Navy Yard.
- **Boat-only islands** (§12): e.g., Rikers Island, Governors Island.
- **Diamond District** (§18), **hospitals** (antiviral, §8), **police and military sites**, **one or two gun shops** (§13).
- **Helicopter sites** (§16): Downtown Manhattan, East 34th Street and West 30th Street heliports; hospital helipads; Floyd Bennett Field.
- **Marinas** (§16), **construction and industrial sites** (§14), **bike-share docks** (§16).
- **Safe zones** (§18): 6–7 in unremarkable warehouses and tall buildings (including one in NJ), sites TBD.
- **A fallen Sanctuary** (§18): the ruins of a safe zone that fell; a lore area. Site TBD.
- **The Breach site** (§23): the border neighborhood where the infection first got inside the walls; a lore area. NJ or the Bronx, TBD.

### What 1:1 NYC means (analysis, not decisions)
- **Size:** NYC has about 780 km² of land. DayZ's Chernarus is about 225 km², so the full city is roughly 3.5× larger, and far denser.
- **Buildings:** NYC has around a million buildings, so making all of them enterable isn't realistic. We need a rule for which ones are (DayZ also leaves many buildings closed).
- **Player density:** a 60-player DayZ server is about 0.27 players per km². With about 680 km² of land (border v2 estimate): 100 players ≈ 0.15/km² (half of DayZ, a ghost town); **250 ≈ 0.37/km² (1.4× DayZ); 300 ≈ 0.44/km² (1.6× DayZ)**; 500 ≈ 0.74/km² (2.7× DayZ). Hotspots still matter, because players cluster rather than spreading evenly.
- **How many players the map can take (analysis, 2026-11-08, asked by the developer):** 300 already matches a busy 100-player DayZ server (about 0.44 per km²). NYC also has far more space than its land area suggests: building interiors, several floors, subways and roofs, plus long distances to cross. So **about 500 should still feel good**, livelier rather than crowded. Past **roughly 1 player per km² of land (about 650–700 players)**, hotspots like Manhattan, hospitals and safe zones would get crowded, and quiet early looting would get rare. **The server, not the map, is likely to set the real cap** (load test, §24).
- **Raised again 2026-11-10** (the developer: "do you honestly think 300 is the right amount here? the map is HUGE, and that is math, not actual numbers so players may be more spread than anticipated"). Claude's answer: right that it's math; 300 stays the number we build and test for, and the launch number comes from real tests and playtests, not math (the cap is already a server setting). Spreading out doesn't make a server cheaper overall: player-to-player sending gets cheaper (crowds cost about their size squared, §24), but more zombies are awake (more of the map has someone near it) and memory stays the same (the server loads the whole map). An empty feel is fixed more by design than by numbers: even 500 spread evenly is one player per 1.4 km². Players gather where the game pulls them (the neighborhoods they pick to spawn in, §10; hotspots such as hospitals and safe zones; bridges and tunnels as natural chokepoints).
- **How it can be built:** generate it from real map data (OpenStreetMap: streets, building footprints, heights) with UE5's PCG framework and modular building kits, then hand-detail key locations. A small team can't build 780 km² by hand. OpenStreetMap data is free to use but requires credit in the game.
  - **The developer's direction (2026-11-10): build on NYC's official 3D building models**, made game-ready by a procedural tool, instead of making buildings from footprints and modular kits. In their words: "I want to some how take the 3d models from the nyc official, and make some kind of prodecural generation to give texture, and interiors to the existing 3d models with control of each build if needed. Where the interior will be a selectable option on selected buiildings, or can be mass selected somehow". So:
    - every building keeps its real shape from the city's data;
    - the tool gives each one its outside look (textures) and, where chosen, an interior;
    - any single building can be controlled by hand when needed;
    - **interiors are an option switched on per building**, either one selected building at a time or many at once (mass selection, method to design);
    - streets and everything else still come from OpenStreetMap.
    - Gets its deeper design pass when building starts ("heavy planning", the developer).
    - _Data found 2026-11-10 (not yet downloaded or tried in Unreal):_ NYC's own **3-D Building Model**: every building standing in 2014, free on NYC Open Data, and City Planning offers it as Rhino `.3dm` files by community district. A **CityGML LOD2 version by TU Munich**: over a million buildings with roof shapes, free as CityGML, KML, COLLADA and glTF (glTF imports straight into Unreal), described as a work in progress. The official model shows the city in 2014, so newer buildings are missing. Licences to check before shipping. _Claude's suggestion, not yet checked:_ NYC's free tax-lot data (PLUTO: building class, number of floors, year built) could pick each building's look and interior type automatically.
    - _Source chosen (the developer, 2026-11-10):_ "the buildings come in rhino 3d files from nyc official website" (City Planning's `.3dm` files by community district). _Found the same day:_ Unreal reads Rhino files through Datasmith, but our source-built engine has that reader built without its OpenNURBS library (only Epic's launcher build ships it), so it can't open them. Free routes: McNeel's `rhino3dm` Python library in a script (reads the files, converts their coordinates to the map's, writes them out region by region for Unreal, like the terrain); Blender's free Rhino import add-on (fine for looking at one file, too manual for about 59 districts); or TU Munich's glTF version instead. First step: open one district's file and see what's inside (meshes or surfaces, units, coordinate system).
    - _Script chosen (the developer, 2026-11-10):_ "I guess we can go with a script, as long as its effecient, gets everything in at the right size and place to match terrain". Files already downloaded: `C:\Game Dev Folder\Rhino Files` holds Manhattan community districts 1 (357 MB) and 3 (501 MB, the East Village, with the test block), plus an `MN01_EXPORT.3dm` from 2024. At those sizes the whole city is roughly 59 files and 15–20 GB unzipped (about 55 MB zipped per district).
    - **What's in a district file (MN03, checked 2026-11-10 with `rhino3dm` 8.35, MIT, installed in QGIS's Python):** read in 5 s. Units are US feet in New York's Long Island state-plane coordinates (EPSG 2263); heights are above sea level like the terrain's. 4,685 buildings, each as flat faces (footprint, roofs, walls) with meshes already stored, so nothing needs converting from curved surfaces: 302,000 triangles in all. No building IDs on the faces. Also in the file: road beds, pavement edges, sidewalks, parks, lot lines, contour lines, subway lines and the shoreline, useful for roads later. **Placement checked against our terrain and the OpenStreetMap test block:** building centres within 1.3 m of OpenStreetMap's (median; 4.6 m at most, where the two split buildings differently), and building bases within ±2 m of the terrain (median 0.3 m below), so walls need extending a little into the ground where the terrain dips. **The city's files cover New York City only:** the map's New Jersey towns (Bayonne to Fort Lee, §5 draft v2) and its piece of Nassau County need another source (OpenStreetMap footprints with heights, or New Jersey's own data).
    - **Shells first, kept for the tool (decided 2026-11-10; the developer: "Yes", then "Will our system that turns these buildings into actual textured buildings, and the option to give an interior come later? like is this just the baseline test, or are you gonna use these buildings later for that system").** The texture-and-interior tool comes later, after the server test shows the city's buildings fit. The import is built so its work carries over: a converter (`tools/map/convert_buildings.py`, QGIS's Python) turns each district file into a **building list**, each building kept separate with an ID, its footprint, base and top heights and its faces in map coordinates, with wall bottoms pushed into the ground where the terrain dips. That list is what the tool will read. Unreal gets plain grey meshes made from it, buildings merged into 250 m tiles (one mesh and one map object per tile, not per building, so the editor and server aren't swamped by a million objects); the tool replaces those meshes later. First district: MN03. The grey test block's four blocks keep their places: real buildings there are left out (and marked so in the list) until the test block is retired.
    - **MN03 imported 2026-11-10:** converted in 94 s (92 of them reading the file), 4,685 buildings (291 left out for the test block) in 83 tiles, 238,000 triangles; imported into Unreal in 3 s (`NYZ/Tools/import_buildings.py`, `NYZBuildingImport.cpp`), 4.5 MB of meshes. Checked from a camera: the East Village on its real street grid at real heights, the test block in its gap, Tompkins Square Park open beside it, walls meeting the ground; traces from above land on roofs at 14–30 m and on the streets between. **On the packaged server the district costs about 13 MB** (collision only: a dedicated server keeps no visual mesh data), about 53 bytes per triangle; the map still loads in 6.3 s. _Rough city estimate, from one Manhattan district:_ about 245 such districts' worth of buildings in NYC, so roughly 1.5–3 GB of building collision for the whole map loaded at once (Manhattan's buildings have more faces than the outer boroughs' houses, so likely the low end). Affordable next to the terrain's 1.5 GB; a borough's import will firm it up.
    - **MN01 (the Financial District) imported 2026-11-10:** 1,752 buildings, 273,000 triangles (about three times the East Village's per building) in 85 tiles; converted in 46 s, imported in 3 s. Checked from a camera: the downtown skyline with One World Trade Center to its spire tip (548 m above sea level; a trace lands on its roof at 411 m). Server cost not measured separately (it needs a repackage); at MN03's rate about 14 MB.
    - **All the district files (checked 2026-11-10):** `https://www.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyc-3d-model/nyc_3dmodel_<district>.zip` (mn01–12, bx01–12, bk01–18, qn01–14, si01–02; si03, the South Shore, isn't offered and isn't in the map): **58 files, 7.5 GB zipped**, about 6 to 7 times that unzipped, from 32 MB (bx02) to 389 MB (qn12). Converted one at a time, the unzipped Rhino file can be deleted after conversion; the building list and tiles are about 9 MB a district.
    - **All of Manhattan imported 2026-11-10** (the developer: "Yes, download them"; MN02 and MN04–MN12 downloaded, 731 MB, a few seconds each): **12 districts, 46,500 buildings, 1,045 tiles, 3.5 million triangles**, imported in about a minute. Checked from cameras downtown and over Midtown (the Empire State and Chrysler buildings with their spires, the East River shore). Found on the way, all handled by the converter now: **MN06 was saved in millimetres** with **no stored meshes**, so the converter reads each file's units and, when a file has no meshes, builds the faces from the wall and roof outlines it also carries (a roof outline inside a bigger one at the same height is a courtyard); buildings that land off the map are left out, and a file where most do stops the converter (catches a wrong unit). The converter now takes **6–12 s a district** (it was 100 s, from adding up the point count again for every face), so the whole city converts in about 10 minutes. The importer frees each district's meshes after saving, so its memory grows about 0.14 GB a district (whole city about 12 GB, fits). An editor that has a district's tiles loaded holds their files, so importing over them fails: close the editor first.
    - **Manhattan on the packaged server (2026-11-10):** the NYC map with all of Manhattan's buildings (plus the test block) loads in **6.9 s** and uses **2.2 GB** with no players (peak 2.6 GB while loading), against 1.8 GB before: **about 0.45 GB for Manhattan**, of which 182 MB is the buildings' collision (about 52 bytes a triangle, as in MN03) and the rest the 1,045 tile objects and their physics. _City estimate, firmer:_ Manhattan has 46,500 of NYC's roughly a million buildings but the most detailed ones (75 triangles a building); the outer boroughs' mostly small buildings at an assumed 20–30 triangles each would add roughly 25–30 million triangles, so **the whole city's buildings should cost the server roughly 2–3 GB**, about 4–5 GB with the terrain. Not yet measured: players moving among real buildings (the test starts every 2 km may now sit inside buildings and need re-placing first).
    - **The whole city converted and imported 2026-11-10** (the developer: "Commit, then the city"; the other 46 district files downloaded, 6.7 GB). **The 58 files are not alike**, and the converter now copes with each way they differ: layer names (`Facade Surface`, `Building Facade Surface`, `Surface_Facade`; it matches by keyword), units (MN06 in millimetres), curve types (QN12's footprints partly PolyCurves), footprint layers holding something else (QN01's holds wall outlines: footprints come from the footprint surfaces when the counts disagree and those surfaces have meshes), and stored meshes on none, some or all faces (33 districts have meshes on fewer than 99% of faces, BK04 on 53%; those get every face from the wall and roof outlines, which every file has, because using the meshes silently lost the faces without one). Buildings are kept or left out by the **map border** (`docs/map/border-draft.geojson`), not the terrain's rectangle: about 131,000 are outside it (most of Staten Island, the eastern edge of Queens, the Bronx north of East 233rd Street); SI02 lies wholly outside. A district's check flags a wrong unit if most of it lands over 100 km away. Final conversion: 57 districts, no failures, at most 4.4% of a district's faces not matched to a building (BK10) and at most 10 buildings without faces, about 8 minutes with three conversions at a time.
    - **The whole city on the packaged server (2026-11-10):** about **810,000 buildings in 9,140 tiles, 24.8 million triangles** (imported in 10 minutes, the importer peaking at 15.6 GB). Checked from a camera over Bushwick (a district built from outlines): rowhouse blocks on the real grid, roofs and walls whole.

      | NYC map on the server | Load | Memory, no players | Peak while loading | Building collision |
      |---|---|---|---|---|
      | Bare terrain | 7 s | 1.5–1.8 GB | 1.7 GB | – |
      | + Manhattan | 6.9 s | 2.2 GB | 2.6 GB | 0.18 GB |
      | **+ the whole city** | **13.4 s** | **5.45 GB** | **8.5 GB** | **1.32 GB** |

      **The whole city's buildings cost the server about 3.7 GB**, more than the 2–3 GB estimated: collision came in as predicted (about 53 bytes a triangle), and the 9,140 tile objects and their physics add about 2.4 GB more. A server with the whole map loaded needs about 9 GB free to start (the loading peak) and 5.5 GB to run, before players, zombies and loot. Affordable on one machine, so the whole map can stay loaded on the server for now; the per-object overhead is the thing to watch (interiors, doors and loot would add objects, the test block said about 60 MB a block). Not yet measured: players moving among the buildings, and the editor with the whole city (load around the camera, `follow_camera.py`, 1 mile).
    - **Conflict to settle (pointed out 2026-11-10):** §9's shared grid assumes city buildings are made of grid pieces, so a hole is a missing piece players can patch and claimable buildings can be fortified with the same pieces. The official models are solid shapes at real sizes, not on any grid. _Claude's options for the design pass:_ the tool rebuilds the walls of claimable buildings (houses, brownstones, small shops, some apartments) from grid pieces fitted to the official shape, so the shape is a guide and not the final mesh, while every other building keeps the official mesh as non-claimable (§9 already allows outside assets as non-claimable buildings); or drop the grid for city buildings and patch holes another way. Not decided.
- **Engine side:** UE5's World Partition (streams the map in pieces) and Large World Coordinates (keeps positions precise on big maps) handle the size. The hard parts are content and server load, not the engine's map-size limit.

---

## 6. Character progression & death

### Levels and learned skills
- The character has a **player level**, **skills** and **crafting recipes**. Learning is tied to level, Ark-style.
- **XP comes from doing things:** killing zombies, crafting, building, healing, exploring new places, surviving.
- **Level cap: 100** (placeholder, tuned later).
- **Two separate point types per level, mapped from Ark:**

| Ark | NYZ | What you spend it on |
|---|---|---|
| Stat points | **Skill points** | **Skills:** abilities (e.g., faster bandaging) |
| Engram points | **Recipe points** | **Crafting recipes:** things you can make, including building pieces |

- _Points per level for each type: TBD._
- Both are grouped by category: **Building, Weapons & Repair, Medical, Cooking & Farming, Mechanics (vehicles), Survival** (traps, fishing, tracking).
- **No raw stat points** (health, stamina, carry weight). Skills are abilities, not raw stats. High-level players are stronger because they can do and craft more, not because they're tankier. This keeps PvP fair for new players and makes losing levels on death hurt less.
- **You can't learn everything.** There are fewer total points than things to learn, so players specialize and clans split roles (medic, builder, mechanic).
- **Re-spending points is possible.** _Method: TBD. Not the found-book idea; the developer has a different method in mind._

### On death
- The character **loses everything** (all levels and all learned skills) until the skill journal is recovered.
- Recovery combines two mechanics: the **skill journal** and a **catch-up XP boost**.

### Skill journal
- Stores the character's progress. Reading it after death restores:
  - **60–80% of the player level** (exact % TBD).
  - **100% of learned skills and crafting recipes**, including ones learned above the restored level.
- **Example:** you die at level 80, read the journal, and come back at about level 55. You can still craft things you learned at level 80, but new learning is limited to what a level-55 character can learn and opens up again as you level. _The numbers are placeholders; the system itself is decided._
- **Snapshot:** a journal only holds progress up to the last time you wrote in it. Updating it is a quick writing action.
- **Multiple journals allowed.** Each one is its own snapshot, so every copy has to be updated separately.
- **Waterproof:** getting wet never damages a journal (§11).
- **Ownership (tentative, may revisit):** only the owner can read their journal; anyone who finds it can destroy it.
- **Burying:** with a **shovel**, on any **diggable ground** (dirt, soil). The chance anyone else finds a buried journal is low.
  - _Implication (analysis):_ most of NYC is concrete and asphalt, so diggable ground means parks, yards, empty lots and riverbanks. Parks become valuable hiding spots.

### Catch-up XP boost
- After death, XP gain is boosted until the player gets back to their previous level.
- **Applies from level 1**, including before the journal is found.
- _Rate and details: TBD._

### Open items
- Journal ownership: confirm "owner reads, anyone can destroy" (tentative).
- How is a journal made? (Decide with crafting/items.)
- Can a buried journal be found by anything other than luck (e.g., freshly dug soil visible for a while)?

---

## 7. Survival stats

Built around the "easy to learn" principle: a few stats always on screen, conditions that only appear when you have them, and one clear fix for each.

### Always shown
| Stat | Fix |
|---|---|
| Health | Heals slowly when you're fed, watered and not hurt |
| Food | Eat |
| Water | Drink |
| Stamina | Rest; used up by sprinting, melee and climbing |
| Body temperature | Clothing, shelter, fire; being wet makes you colder |

### Conditions (appear only when you have one)
| Condition | Cause | Fix |
|---|---|---|
| Bleeding | Cuts, gunshots, bites | Bandage or rag |
| Broken limb (arm or leg) | Falls, heavy hits | Splint. Until then, a broken leg means you limp and can't sprint; for a broken arm, see Body-part health |
| Wound infection | Wounds left untreated | Disinfectant or antibiotics |
| Sickness | Rotten food, dirty water | Medicine and rest |
| Cold | Too cold or wet for too long | Warm up, medicine |
| Unconscious | Big hits, bad falls | Wears off after a while. While you're out, other players can restrain or rob you. |
| Zombie infection | Bites (high chance), scratches (low chance) | Rare antiviral. See §8 Zombie infection |

### Mood: stress, boredom, happiness
- **In the game, but much gentler than Zomboid.** They drain **far slower**, and there are **many more ways to fix them**. Players should never end up stressed, bored or unhappy around the clock.
- **Only appears on screen when it starts getting bad**, like conditions.
- **Pace:** a player who eats decent food and spends some time at their base or with friends should rarely see a mood warning. It should take hours of neglect, not minutes.
- **Being near clanmates reduces stress and boredom.** This ties mood to clans and rewards grouping up.

| Mood | Gets worse from | Gets better from | When it's bad |
|---|---|---|---|
| Stress | Fights, zombies close by, getting hurt, being hunted | Being at your base, being near clanmates, cigarettes, alcohol, time away from danger | Shakier aim; stamina recovers slower |
| Boredom | Long idle stretches, repeating the same task | Books and magazines, music (radio, instruments), cards and games, exploring new places, being around other players | Slower XP gain |
| Happiness | Bad food, being wet, cold or sick, long stress or boredom | Good cooked meals, coffee, alcohol, music, comfort items, a comfortable base | **Low:** slower healing. **High:** small XP bonus |

### Nutrients
- **In the game, but less critical than in Zomboid.**
- **Food is counted in calories**, like DayZ.
- **Three food groups tracked in the background:** protein (meat, fish, beans), carbs (bread, rice, pasta, chips), vitamins (fruit, vegetables).
- **No extra bars on the HUD.** There's one status instead:
  - **"Well fed"** (balanced diet): slightly faster healing and stamina.
  - **"Poor diet"** (a group missing for a long time): slightly slower healing and lower maximum stamina.
- **Diet menu:** a deeper menu (e.g., in the character/health screen) shows the three groups and which one is missing.
- **Never lethal on its own.** You fix it by eating the missing group.
- Each food's tooltip shows which groups it covers.
- **Full stomach:** you just can't eat more. No vomiting from overeating.

### Water in NYC
- The rivers around NYC are salt or brackish water and can't be drunk. Exception: the Bronx River is fresh water (it still needs boiling).
- Fresh water sources: bottled water, rain collection, reservoirs (e.g., Central Park), **rooftop water towers**.
- Dirty water must be boiled or purified before drinking.

### Body-part health
- **Separate health per body part.** It's deep, but a good UI makes it easy for a new player to understand. The UI is what makes or breaks this system.
- **Six parts:** head, torso, left arm, right arm, left leg, right leg. Hands go with the arms and feet go with the legs.
- **Total health** is all the parts added together. The "Health" stat above is this total.
- **Head or torso at zero: death.**
- **Arm or leg at zero: "destroyed."** Heavy penalty, and any more damage to that limb spreads to the rest of the body. A **surgery kit** fixes it; the limb comes back with lower maximum health until it fully heals over time.
- **Conditions belong to a body part.** Bleeding on the left arm means you bandage the left arm; a bite can be on the right leg. This matters again for zombie infection.

| Part | When hurt | Worst case |
|---|---|---|
| Head | Blurry vision, ringing ears; head hits can knock you out | Death at zero |
| Torso | Stamina recovers slower | Death at zero |
| Arms | More aim sway, slower reloading and melee | **Broken arm** (see below) |
| Legs | Slower movement | **Broken leg:** you limp and can't sprint until splinted |

#### Broken arm
- **Rifles and other two-handed weapons:** **hip fire only**, with heavy sway. No aiming down the sights.
- **Pistols:** can still be aimed one-handed with the good arm.

#### Handedness
- Chosen at **character creation: left- or right-handed.**
- Players **aren't told why it matters.** They find out when it comes up, e.g. with a broken arm.
- **Gameplay only, for now.** Animations are the same for everyone; only the one-handed pistol animations exist for each hand (needed for the broken-arm rule anyway). Mirrored animations for every weapon would double the animation work and make guns look wrong (ejection port and bolt on the wrong side).

| Situation | Effect |
|---|---|
| Broken **off-hand** arm, using a pistol | Main hand does the work: almost no penalty, a little extra sway |
| Broken **main-hand** arm, using a pistol | Shooting with the off hand: noticeably more sway, slower reloads |
| One-handed melee (knife, machete) | Same pattern as pistols |
| Throwing (grenades, bottles, rocks) | Off-hand throws are shorter and less accurate |

- **First-time hint:** the first time handedness matters, a short message explains it (e.g., *"Your main arm is broken: aiming with your off hand."*). Players still discover it in the moment without being confused.
- **Maybe later:** visible handedness and intentional off-hand aiming (see "Maybe later" near the end of this doc).

#### Treating injuries (UI)
- **HUD:** a small body outline appears when you're hurt. Each part is colored green, yellow, red, or black when destroyed.
- **Health screen:** click a part to see its injuries, then drag a bandage or splint onto it.
- **"Treat" button:** one click uses the best item you have on your most urgent injury. New players never have to learn the details; experienced players can treat each part by hand.
- **Armor per body part** (helmets protect the head, vests the torso, etc.) follows from this. _Designed with items and loot._

### Cut
- **Sleep / fatigue:** cut entirely.
- **Panic:** cut.
- **Body weight:** cut.

---

## 8. Zombies

### Types and speed
- **A few different speeds, based on how fresh the zombie is.**

| Tier | Speed | Where they're found |
|---|---|---|
| **Fresh** (recently turned) | Between a walk and a run. Not a full run | Rare. Near recent deaths, and players' bodies that turned (§10) |
| **Weathered** | Normal walk | Most zombies |
| **Decayed** | Shamble | Common in old, settled areas |
| **Crawler** | Crawl | Any zombie with destroyed legs |

- _Exact speeds per tier: tuning, during development._
- **No regular zombie runs at full speed.** _Implication (analysis): a sprinting player can outrun any regular zombie until stamina runs out._
- **Variants by what they were:** civilian, police, firefighter, military, hospital staff. Clothing decides toughness and loot (military: armor and military gear; police: pistols and ammo). DayZ-style.
- **Special zombies:**
  - **1–2 special types at most.** Not overkill.
  - **Extremely, extremely rare.**
  - **Harder to kill.**
  - Spawn **only at lore areas.**
  - **The two types** (backstory in the [lore bible](lore/LORE.md); kept out of this doc on purpose):
    - **The Patient:** tougher (takes more head damage), and **the only zombie that truly runs** (the exception to "no regular zombie runs at full speed"). Wears a hospital gown and a wristband you can loot. **Sometimes says a word or a sentence in English**, then goes back to incoherent mumbling.
    - **The Host:** slow and very hard to kill, with medical restraints and tubing hanging off it.
  - **Both look clearly different from regular zombies, e.g. mutated.**

### Senses
- **Hearing is the main sense.** Gunshots carry far, car alarms and breaking glass less far, footsteps only close by. Crouching and walking slowly keep you quieter.
- **Footwear changes footstep noise.** Boots are clunkier and louder; sneakers are quieter. This matters most up close and crouched.
  - **The same footstep sound is heard by other players**, so sneakers are also a PvP choice for sneaking up on people.
  - **Boots protect more to balance being louder:** they block more bites to the legs and feet, keep you warmer and last longer. Sneakers are quiet but protect less and wear out faster.
- **Sight:** worse at night, in rain and in fog.

### Hordes (Zomboid-style)
- Noise **pulls zombies together**, and groups **migrate across the city** over time.
- A loud gunfight can bring a horde down on everyone nearby, so noise is both a weapon and a risk in PvP.
- **Cleared areas stay cleared for a while** and refill slowly as hordes wander in. Zombies don't respawn out of thin air.
- **NYC chokepoints:** bridges and tunnels. **Subways:** dark, packed danger zones.

### Killing zombies
- **Only head damage kills.**
- Body shots stagger them and can knock them down.
- **Destroyed legs turn them into crawlers.**

### Zombie infection
- **Bites:** high chance of infection. **Scratches:** low chance.
- **Clothing on the bitten body part can block it** (e.g., a leather jacket protects the arms).
- **Cure: Remisso, a rare antiviral** found in hospitals and labs. Hospitals become high-value PvP hotspots, which also helps player density at 1:1 scale.
- **Delay: Hourglass** (a very rare compound, lab code HG-7) that **delays infection but doesn't cure it.** It buys time to find the antiviral. Very rare or top tier (§12). _Backstory in the lore bible._
- **Dying of infection turns you into a zombie wearing your gear.** Your friends have to put you down. Other deaths may turn your body too (see §10).

### Zombies and bases
- **Noise attracts zombies to bases.**
- **Damage to a base depends on its building-material tier:**
  - **Tier 1:** small and large hordes both take it down easily.
  - **Tier 4:** a small horde can't damage it at all; a large horde wears it down over time.
  - _Tiers 2–3 and exact numbers: designed with base building._
- **Climbing:**
  - **Low fences** (waist-high or lower, the kind you can hobble over): zombies climb over them slowly and sometimes fall.
  - **Fences taller than a person:** zombies can't climb them. The only way through is breaking them, following the material-tier rules above.
  - **Ladders:** zombies can't climb them, so ladders matter in base design.

### Open items
- Zombie count per server (after the load test).
- Day/night behavior (with weather and day/night).

---

## 9. Base building & raiding

### Two ways to build (both in the game)
- **Fortify existing buildings:** claim an apartment, storefront, brownstone or rooftop, then barricade and upgrade its doors and windows.
- **Build from scratch** with snap-together pieces (foundations, walls, floors, doors, stairs) in open spaces: parks, empty lots, rooftops.
- **Concern raised by the developer:** in a decaying, possibly bombed NYC, abandoned buildings would have big open holes that need to be filled in and modeled. That adds a lot of work.
- **Approach: shared grid, "to a degree."** The city's modular building kit and the player building pieces use the **same grid**. A hole in a damaged building is then just a missing grid piece, and players patch it with the same snap walls and floors they build with. No separate patching system and no custom model per hole. Only certain building types are claimable (houses, brownstones, small shops, some apartments).
  - **Must not lock out outside assets.** Models found later (e.g., on Fab) must be addable.
  - **Suggested method:** only structural pieces (walls, floors, door and window openings) follow the grid, since those are what players patch. An outside asset is then either **fitted to the grid** (resized or padded so its walls line up with grid units, a quick job per asset in Unreal or Blender) so it supports patching, or used as a **non-claimable building or prop** (landmarks, unique buildings, decoration) that doesn't need to match the grid.
  - **The grid size must be decided before any building models are made.** Changing it later means remaking them all.

### City buildings can't be destroyed
- Only player-added pieces can be damaged. Raiders have to come through doors, windows and player-built walls.
- Why: destructible city buildings would be an enormous technical cost, both for the server and for 1:1 NYC.
- Side effect: a fifth-floor apartment with one barricaded door is a strong base, which gives players a tactical choice.
- **Rooftop bases reachable only by helicopter are allowed** (§16).

### Material tiers
| Tier | Material | Zombie damage |
|---|---|---|
| T1 | Wood, scrap planks | Any horde breaks it easily |
| T2 | Sheet metal, reinforced wood | Small hordes slowly; large hordes quickly |
| T3 | Brick, concrete blocks | Small hordes barely; large hordes over time |
| T4 | Steel, reinforced concrete | Small hordes can't damage it; large hordes wear it down over a long time |

### Building noise
- **Building attracts zombies, but it isn't extremely loud.**
- **Outside, or at the edge of a building** (a window or door): heard about **1–2 city blocks** away.
- **Fully inside a building:** muffled, heard about **1 city block** away.
- **Distances will be set in meters during map development.** Real NYC blocks vary in size, and the street layout and terrain aim for 1:1, so "a block" depends on where you are.

### Claiming, decay and limits
- A **claim item** placed in the base sets an area where only you and your clan can build.
- **Bases decay if nobody from the clan visits for X days.** Visiting resets the timer. _X: TBD._
- **Each clan has a piece cap**, needed for server load, but it **shouldn't feel limiting** to players. _Number: TBD, after testing._

### Raiding
- Higher tiers need better tools or explosives: sledgehammer and crowbar for T1, power tools for T2–T3, explosives for T4.
- **Raiding should never be easy.** Raid tools and explosives are **hard to find**.
- **Raiding is loud** and attracts hordes, so raiders deal with zombies arriving mid-raid.

### Offline raid protection
- **Default: offline protection.** Bases take much less damage while the whole clan is offline. It only starts 15–30 minutes after the last member logs off, so logging out mid-raid doesn't save a base.
- **Server setting** to switch to: no protection (Rust-style) or set raid hours.

### Locks
- **Code locks** on doors; clanmates get access automatically, **by rank level** (clan-wide or officer and above; see §15).

### Where you can build
- **Player spawn areas: no building.**
- **Chokepoints (bridges, tunnels, subway entrances): building allowed, but with major inconveniences.** Clans can block or hold them, but it mustn't be worth it for every clan to do so.
  - **Hordes travel through chokepoints.** Bridges and tunnels are natural migration routes, so a base there takes constant zombie pressure.
  - **Faster decay**, so holding one means showing up often.
  - **Claiming and storage are allowed.** Building in a dangerous area means being ready to hold it or paying the price, a lesson players learn after one or two tries.
  - _No smaller piece cap for now (see "Maybe later")._
- **Major loot hotspots** (e.g., the biggest hospitals): **no building.** Which hotspots count as major: decided with the map and loot.
- **Smaller loot spots** (small hospitals, clinics, schools, etc.): **building allowed.** **Loot doesn't respawn inside a claimed base's area.** Only the claimed area is affected, not the surroundings, so claiming a clinic doesn't let a clan farm it, and loose pieces don't block anyone's loot.

### Open items
- Decay timer and piece cap numbers.
- Grid size (before any building models are made).

---

## 10. Death & respawn

### Fresh spawns
- **You pick a borough and a neighborhood**, then spawn at a **random point spread throughout that neighborhood.** This makes finding friends quicker on a 1:1 map.
- **Only a few select neighborhoods are spawn neighborhoods.** High-loot neighborhoods are never spawn points.
- No building at spawns (§9).

### Respawning at your base
- **Sleeping bags:** cheap, long cooldown between respawns. **Can't be placed within X distance of another clan's claimed base** (stops players from spawning right next to a base they're raiding). _X: TBD._
- **Beds:** expensive, short cooldown. They also count as comfort items for mood.
- **Both can be shared with clanmates.**

### Your body
- Everything you carried stays on your body. **Anyone can loot it**, including you if you get back in time.
- A body that doesn't turn stays in the world for **2 hours.** Getting back can be difficult on a 1:1 map, and games like Ark give players a lot of time too.
- **Your body may turn into a zombie, depending on how you died.** It doesn't turn instantly. Once it turns, it's a Fresh zombie wearing your gear and it wanders off, so **you may have to track it down** to get your gear back.
- **Rule: your body turns if you were infected when you died, whatever actually killed you.**

| How you died | Turns? |
|---|---|
| Died of zombie infection | Yes |
| Killed by zombies (bitten while dying) | Yes |
| Infected, but killed by a player, a fall, bleeding, etc. | Yes |
| Not infected (player, fall, cold, starvation) | No |
| **Killed by a head hit** | **Never.** Destroying the head stops it, same rule as zombies |

- **Turning time: a random 30–60 minutes.** On a 1:1 map, players need a real chance of getting back to their body in time.
- Tactic this creates: killing an infected enemy with a headshot stops their body from turning and walking off with their gear.
- **Lore will be fitted around these rules** (e.g., only infected people turn).

### Starting kit
- Basic clothes, one bandage, a small snack, a flashlight. (No MetroCard: they've been phased out.)

### Progression on respawn
- Level 1 with the catch-up XP boost until you find your journal (§6).

### Logging out
- **DayZ-style:** your character stays in the world for **30 seconds**, then disappears. A longer timer applies if you were just in a fight, so you can't escape a fight by quitting.
- _Not Rust-style:_ characters don't keep sleeping in the world after logging off. That would clash with offline raid protection (§9).

### Spawn protection
- **Extremely minimal.** It only covers loading in: you can't die while your screen is still black but the server has already loaded you. It ends as soon as you can see and move.

### Open items
- Sleeping bag distance from another clan's base (X).

---

## 11. Inventory

- **Basis: DayZ's grid system, with a grid for each piece of clothing.** **Bags don't use a grid:** they're physical spaces seen in a side cutaway (see Bags below). _Changed 2026-10-27; the basis first gave each bag a grid too._
- **Goal: an upgraded version, so players don't see it as a DayZ copy.** It should be clearly NYZ's own system.
- **Core idea: where and how you pack something matters.** In DayZ, a bandage in your backpack works the same as one in your shirt pocket. In NYZ it doesn't.

### Kept from DayZ
- Every garment has its own pocket grid. Items take up cells and can be rotated.
- Weapons have attachment slots.
- Items have condition levels.
- Items in clothing get damaged when that clothing is hit.
- **Weight:** total carried weight affects stamina, DayZ-style. Nothing finer than that.

### Reach zones: where you carry it sets how fast you can use it
| Zone | What counts | Access |
|---|---|---|
| **Hands** | What you're holding | Instant |
| **Quick reach** | Jacket and pant pockets, belt, chest rig, holsters | Fast, even while walking |
| **Pack** | Backpacks, duffels, bags | You stop, swing the bag around and dig through it. Slow, and you're exposed while you do |

- **The quick bar (hotbar, keys 1–0) stays** and only pulls from quick reach.
- The Treat button (§7) uses supplies in quick reach first. Anything in the pack takes longer.
- Pockets are small, so quick-reach space is the real tension. E.g., a medic keeps bandages on the chest rig; a raider keeps the crowbar on the belt.
- _Analysis:_ Tarkov has a loose version of this (chest rig versus backpack). The time it takes to dig through a pack is what's new.

### Bags: cutaway packing
The developer's idea: you see the bag from the side, as if looking through it, and physically move items around in that space. Items collide in the UI if they don't fit.

- **The view:** opening a bag shows it in cross-section, as if its side were cut away: main compartment, lid, front pocket, side bottle pockets.
- **Pocket tabs** (the developer's idea): a small tab switches the pocket view. It hides the main compartment and its contents and shows a smaller pocket's space instead, for smaller items.
- **Slings** (the developer's idea): bags have sling attachments for primary weapons (crowbar, bat, rifle, etc.). **Better bags have 2 or more slings.**
  - **Every character also has one body sling** over the shoulder, with or without a bag. Bags add their slings on top.
- **Each bag type has its own outline.** The shape is what sets bags apart, not "6×8 versus 8×10". Examples (final list with loot & items):

| Bag | Shape | Good for |
|---|---|---|
| School backpack | Small, upright | Starting out |
| Hiking pack | Tall and deep, with a lid pocket | Lots of small things |
| Duffel | Long and low | Rifles, long tools |
| Messenger bag | Wide and shallow | Flat things, quick access |
| Tactical pack | Medium, with outside pouches | Staying organized |

- **Items keep their real side profile** instead of being rectangles: a bottle has a neck, a pan has a handle, a rifle is long and thin. They either stand up or lie on their side (90° turns).
- **Gravity, no tumbling:**
  - A dropped item falls straight down until it lands on something.
  - While you drag, an outline shows where it will land. If it won't fit (it would stick out of the opening, or it's too long for the bag), the item turns red and a short message says why.
  - Take something out from the bottom and everything above it drops down.
  - _Why no tumbling:_ real physics, where things roll and tip over, feels chaotic and is hard to keep in sync with the server. Straight-down drops still feel physical, and an item always lands in the same place.
- **Hard and soft items:**
  - Hard items (cans, tools, guns, bottles) keep their shape.
  - Soft items (clothes, rags, tarps, sleeping bags) fill whatever gaps are left, like stuffing a shirt around your cans.
- **Pack order is reach.** Things on top come out fast. Something at the bottom takes longer, because your character digs past everything above it. _Times: tuning. The demo used 1 s plus 0.5 s for each item on top._
- **Zip line:** a bag can be packed past its zip line, but then it can't close. Things stick out (visible on your character) and can fall out when you sprint or jump.
- **Stretching** (the developer's idea):
  - Soft bags (canvas, nylon) can bulge a little past their outline for extra room. That can be what lets the zip close.
  - **Stretched bags wear faster** (item condition, see Kept from DayZ).
  - A worn-out bag **rips at the seam** and loses room until it's sewn (crafting).
  - Rigid bags (a tactical pack with a frame, a hard-shell case) don't stretch.
  - **The cost is visible:** the bag's outline bulges, with a short note like "Stretched: wearing faster", so players don't first find out when it rips.
- **Speed versus care:**
  - **Toss in:** one click throws an item in, and it lands wherever it falls. Fast for looting a body under fire, but it wastes space and rattles.
  - **Repack by hand** once you're safe: more fits, and it's quiet.
  - **Auto-pack button:** packs well but not perfectly.
- **Rule: packing by hand is a bonus, never a requirement.** Auto-pack gets about 90% of the way: neat, quiet and padded with your soft items. Packing by hand only buys a little more room. An average player who never packs by hand should still have a fine time.
- **Pockets stay grids.** Pockets are small, so a physical view there would be fiddly for no gain. Pockets (quick reach) are fast and simple; bags (pack) are slow but roomy.

### Rattle: how you pack it sets how loud you are
- Hearing is the zombies' main sense, and other players hear footsteps (§8). The inventory joins in.
- **Hard items with empty space beside them** in a bag (cans, bottles, tools, loose ammo) clatter when you run or jump. In the bag view, loose items visibly shake.
- You quiet them by stuffing soft items into the gaps, or by packing them in a pouch or ammo box.
- When your bag is loud, a small **rattle icon** appears. Its tooltip names the items causing it, so the fix is obvious.
- Packing quietly becomes a sneaking choice, like sneakers versus boots.

### Hidden pockets: what other players can find
- A few garments have **one or two tiny hidden cells:** an inner jacket pocket, a boot stash, a waistband.
- Someone searching you (unconscious, §7, or your body, §10) doesn't see hidden pockets at first. Finding them takes a **slow extra search**. On a knocked-out player that's a race against them waking up and against zombies arriving.
- The natural place for your journal, a door code or a small stash.

### NYC carry gear
- **Shopping carts and rolling suitcases:**
  - Huge storage that you push or pull.
  - You can't sprint, and both hands are busy, so no weapon.
  - Suitcase wheels clatter on the pavement and carts rattle.
  - A very New York image, and a real trade-off for hauling loot across a 1:1 city.
- **Straps on big backpacks:** bulky items (sleeping bag, shovel, bat, rolled tarp) hang on the outside, **visible to everyone.** A shovel on someone's pack hints that they bury journals.
  - **The bat is both bulky gear and a sling item:** it can go on straps or on a sling.
  - **Inside or outside:** a long or bulky item that fits can be shoved into the bag. If it doesn't fit, it still has a place on the outside.
- **Dry bags:** the city is ringed by water, and boats are how you reach Staten Island (§5). Falling in soaks ordinary bags: matches, bandages and books are useless until they dry. A dry bag keeps its contents dry.
- **The skill journal is waterproof** (§6), so water never becomes a way to lose your progress.

### Quality of life
- **Auto-arrange button** for pocket grids and **Auto-pack** for bags (see Bags), so nobody has to pack by hand unless they want to.
- **One-press quick move:** an item goes to its best spot (medicine and ammo to quick reach, everything else to the pack).
- **Works with a controller from day one** (§3: no mouse-only UI). Auto-pack, auto-arrange and a radial menu work on a gamepad. In the bag view, items drop straight down, so you only move an item over its spot and drop it.

### Technical implications (analysis)
- With 300 players, a container's contents are only sent to its owner and to whoever opens it. Everyone else only sees worn or strapped-on gear.
- Rattle only needs recalculating when a bag's contents change, not every frame.
- **Bag packing stays server-authoritative.** The client only sends where an item was dropped and which way it faces. The server works out where it lands with the same straight-down rule, so a cheater can't claim something fits.
- Positions sit on a **fine hidden grid** (around 1 cm), so the client and server always agree.
- **Soft items are cheap:** they have no shape, just a volume that fills leftover space, so nothing squishy has to be simulated.
- **More UI work than a grid.** Grid inventories are a solved problem with ready-made templates; the cutaway bag has to be built from scratch (item outlines, the landing outline, auto-pack). _Not checked yet:_ whether an existing UE5 plugin handles non-rectangular item shapes.
- **Every item needs a side-profile outline**, made once per item.

### Open items
- Final list of bag types and their outlines (with loot & items), including how many slings each has.
- Tuning: dig-out times, how far soft bags stretch, how fast stretched bags wear.

---

## 12. Loot & items

### Item condition
- **4 levels, color-coded:** Pristine → Worn → Damaged → Ruined.
- Condition affects how well an item works (e.g., a damaged rifle jams more; a worn jacket blocks fewer bites).
- **Repair kits** restore condition, but never back to Pristine, so items still wear out over time.

### Where loot spawns: by building type (DayZ-style)
| Place | Loot |
|---|---|
| Apartments, houses | Food, clothes, basic tools. **Guns very rarely** (see below) |
| Bodegas | Snacks, drinks, cigarettes, coffee (a mood item) |
| Pharmacies, clinics | Medicine, bandages |
| Hardware stores | Tools, building materials |
| Police stations | Pistols, ammo, police gear |
| Military zones, National Guard sites | Rifles, armor, explosives |
| Hospitals | Medical supplies, antiviral |
| Port container yards | Ordinary cargo; **smuggled guns** (see below) |

### Port container yards
- **All four ports in the map are in** (all checked inside border v2): **Red Hook Container Terminal** and **South Brooklyn Marine Terminal** (Brooklyn), **Port Jersey** (Bayonne), and the **Brooklyn Navy Yard**.
- **Where the smuggled guns come from:**
  - **Mainly: a customs holding warehouse** at the port, full of weapons seized off ships. One building, heavy loot, an obvious hotspot.
  - **Sometimes: hidden in containers** among ordinary cargo. **Shipping manifests** (paper items found around the yard and in offices) name a container with "suspicious cargo"; reading one marks it on your map.
  - _Not chosen for now:_ the outbreak arriving by ship. Lore may still use the ports.
- **Opening containers takes bolt cutters** (see below). Cutting is loud, which draws zombies (§8) and players.
- **The yard as a place:** stacked containers form a maze with tight lanes, climbable stacks and long sightlines; climbable **gantry cranes** serve as sniper perches and landmarks; **dockworker zombies** (hard hats, hi-vis vests) drop tools (§8 variants); reachable by water.
- Most containers hold ordinary cargo (clothes, electronics, canned food). Guns are the rare jackpot.
- Opened containers stay open until the central economy resets them.
- **Smuggled guns** (gun roster): the AK family, Saiga-12, Uzi, MAC-10, Scorpion, Vector.

### Bolt cutters
- **A rare tool, not a top-tier raid tool**, so the port yards aren't locked to almost everyone.
- Opens container padlocks and seals.
- **Other uses: yes, to be designed.** **Decided:** freeing bikes from bike-share docks (§16). _Ideas:_ padlocks on gates, lockers and storage units; chain-link fences; the locks on roll-down store gates (bodegas, shops); chained doors; freeing a restrained player (§7); removing steering-wheel locks (§16).

### Guns are rare in NYC
- The city has very few gun stores, so guns mostly come from **police and military** sources.
- **Guns can also turn up in apartments and houses, but very rarely.** The rate varies by neighborhood: **neighborhoods with higher crime rates have more** than, say, Manhattan. _Exact rates: TBD; the developer doesn't have exact statistics._
  - _Note (analysis):_ tying gun rates to specific real neighborhoods by crime data can come across as stereotyping the people who live there, and draw criticism. Safer: keep the difference modest, never label neighborhoods in-game, and treat the rates as hidden tuning.
- Consequences: melee matters early, guns are valuable, and police stations and military sites become PvP hotspots.

### Loot tiers by area
- **Spawn neighborhoods:** low-tier loot.
- **Better loot in dangerous places:** Manhattan's core, military sites, and the boat-only islands (Rikers, Governors Island).

### Loot respawning: central economy (DayZ-style)
- The server tracks how many of each item exist in the world and respawns items when the count drops. Rare items stay rare.
- Loot inside a claimed base's area doesn't respawn (§9).

### Rarity: 5 tiers
| Tier | What's in it |
|---|---|
| Common | _Examples, set item by item later:_ food, clothes, basic tools |
| Uncommon | _Examples:_ medicine, building materials |
| Rare | Lower-tier guns |
| Very rare | Higher-tier guns |
| **Extremely rare** (top tier) | **Raid tools, explosives, the antiviral, the machine gun, the .50 cal**, etc. |

- **Gun types and tiers separate rare from very rare.**
- _The top tier's name is a working name._

### Decay
- Food rots, batteries run down, and items dropped on the ground despawn after a while, which keeps the server clean.

### Open items
- Gun spawn rates in homes, by neighborhood type.
- Which item goes in which rarity tier (with weapons and crafting).
- Name of the top rarity tier.
- Bolt cutters: which other uses.

---

## 13. Weapons & attachments

### Weapon families
| Family | Examples | Where found (§12) | Rarity |
|---|---|---|---|
| **Melee** | Pipe, bat, crowbar, kitchen knife, machete, fire axe, sledgehammer | Everywhere | Common to uncommon |
| **Pistols, revolvers** | Police 9mm, revolvers | Police; homes (very rarely) | Rare |
| **Shotguns, hunting rifles** | Pump shotgun, bolt-action | Police, homes | Rare |
| **Military rifles** | Assault rifles, marksman rifles, sniper rifles | Military sites | Very rare |
| **Bows, crossbows** | Recurve bow, crossbow | Sporting goods, crafting | Uncommon to rare |

- **Throwables:** bottles and rocks (to distract zombies), molotovs (crafted), grenades (extremely rare, military).
- **Fictional names:** guns look like real models but have made-up names, which avoids trademark trouble.

### Gun variety: vast
- **A vast selection of guns, even if many are rare or hard to find.** Deep gun customization is a core feature of NYZ.
- _Analysis:_ every gun needs a model, first- and third-person animations (reloads, jams), sounds and attachment fits. That makes guns the biggest art and animation cost in the game for a solo developer. **Practical approach:** build the roster on shared **platforms** (an AR-style family, an AK-style family, a pistol family, etc.) that share animations and rails, so variety comes from variants and customization. Ready-made weapon packs from Fab can fill gaps.

### Noise
- Gunshots attract hordes (§8). From loudest to quietest: shotgun, rifle, pistol, suppressed, then bows and melee.
- So **melee and bows are the main tools against zombies**, and firing a gun is a choice with consequences.

### Melee: quiet, and the core of early survival
- Light and heavy attacks, using stamina.
- **Shove** pushes zombies back, for crowds (Zomboid-style).
- **Stomp** finishes zombies on the ground. Head hits kill (§8).
- One-handed versus two-handed melee follows the broken-arm and handedness rules (§7).

### Ammo and magazines
- **Magazines exist and tie into reach zones (§11):** magazines on the chest rig mean a fast reload; magazines in the pack mean you stop and dig.
- **Refilling magazines is one action** using ammo from quick reach, not a bullet-by-bullet chore.
- **Calibers: more than the ~6 first proposed**, because a vast roster needs them. _Suggested (to confirm): many guns share common calibers, around 10–12 in total, with color-coded ammo boxes and "fits:" tooltips so it stays easy to learn._
- **Ammo crafting is an endgame recipe** (details with crafting).

### Attachments: vast customization
- **Slots:** optic (red dot, low zoom, sniper scope), muzzle (suppressor), underbarrel (grip, flashlight), stock, magazine (extended).
- **Suppressors** cut the noise radius but don't make a gun silent (very rare). An **improvised suppressor** (crafted from a bottle or oil filter) breaks after a few shots.
- **Ghillie wrap slot** on rifles and similar weapons, for camouflage. _Added by the developer._
- **Rails vary:** different rail types fit more attachments, e.g. a one-sided rail versus a two-sided rail. More rail sides means more attachment slots. _Added by the developer._
- Attachments fit by **rail type** (pistol or rifle), not by specific gun.
- _Open:_ the full list of swappable parts (e.g., handguards that set the rail count, barrels, grips), and how to keep deep customization easy to learn. _Suggested:_ the UI only shows parts that fit, compatible slots light up, and there are ready-made presets.

### Handling
- **Recoil and sway.** Sway gets worse with stress (§7), hurt arms (§7) and low stamina.
- **Jams:** the chance rises as condition drops (§12). Clearing a jam is a quick action.
- **Bullet drop at long range** (rooftop shooting across avenues); **no wind**.
- Damage hits body parts (§7); **armor per body part** blocks it (helmet: head; vest: torso).

### Weapon skills stay non-combat
- Skills (§6) cover handling, not damage: faster reloads, faster jam clearing, gun repair, crafting attachments.
- **No "more damage" or "less recoil" skills**, in line with "no raw stat points" (§6), so PvP stays fair for new players.

### Crafting ties
- Recipes: bows, arrows, molotovs, improvised suppressors, upgraded melee (nail bat, spiked pipe).
- **Crafted pipe shotgun:** unreliable, loud, short-ranged. A last-resort gun that doesn't make real guns any less rare.
- **Ammo crafting: endgame.**

### Condition and repair
- Weapons wear down with use. Cleaning kits and repair kits restore them, but never back to Pristine (§12).

### Open items
- Gun roster: **draft v2** in [docs/weapons/gun-roster.md](weapons/gun-roster.md): 56 guns on 19 platforms, 3 oddities, 13 calibers. Waiting for final sign-off. Smuggled guns come from the port container yards (§12).
- **Decided:** **.357 guns also take .38** ammo (true to life, shown in the "fits:" tooltip). The **machine gun and the .50 cal are in the top rarity tier** (§12).
- Full list of swappable gun parts and rail types; how the customization UI stays easy to learn.
- Ammo crafting details (with crafting).

---

## 14. Crafting

### Where you craft: three levels
| Where | Examples | Needs |
|---|---|---|
| **By hand** (anywhere) | Molotovs, improvised suppressor, nail bat, sawed-off (with a hacksaw), splints | Nothing, or a hand tool |
| **Workbench** (placed at your base) | Bows and arrows, pipe shotgun, building pieces (tiers 1–2), repair kits, base furniture | A built workbench |
| **Specialty stations** | **Gunsmith bench** (attachments, gun repair, endgame ammo), **cooking station** (meals), **welder** (tier 3–4 steel pieces), **sewing station** (bag repair, clothing) | Some need **power from a generator**. Generators are loud, which draws zombies (§8) |

### What needs a recipe
- **Every real crafting recipe costs recipe points** (§6). **Simple recipes are very low level and very low cost.**
- **Everyday actions aren't recipes, and every character can do them:** e.g., boiling water, using a shirt as a bandage. Anything that's an action rather than making something.
- **The crafting menu shows every recipe.** Ones you haven't learned are greyed out with "learn at level X", so you can always see what's possible.
- **New characters start with 5–10 recipe points** (exact number: tuning). **All the basic recipes cost 1 point each**, so a fresh spawn can learn splints, a campfire, a torch and similar right away.

### Materials
- **About 12 core urban materials**, possibly more later: wood, scrap metal, cloth/rags, nails, duct tape, pipe, plastic, glass bottles, electronics, chemicals, fuel, mortar/cement.
- **Sources:**
  - **Taking things apart:** furniture gives wood, cars give scrap metal, clothes give rags, and **electronics like computers give some scrap metal and some electronics.** Needs tools (saw, crowbar, wrench).
  - **Trees give wood.** Some areas, like parks, have a lot of them.
  - **Industrial sites and construction sites:** bricks, concrete, mortar, steel, and welders.
- Building materials match the base tiers (§9): wood for tier 1, sheet metal for tier 2, brick and concrete blocks for tier 3, steel for tier 4 (needs the welder and power).

### What crafting can pull from
- **At your base:** your inventory **plus storage containers within a few meters.**
- **Away from your base:** your inventory **plus items on the ground right around you.**

### Time, movement, noise, queues
- **Crafting takes time.** Mostly you stand still, but **anything that could realistically be done while walking can be done while walking.**
- **Loud work makes noise** (hammering, sawing, welding, the generator), following the building-noise rules (§9). **Small recipes make no noise.**
- **Station crafts can be queued** and keep going while you're nearby (Ark-style).

### Crafted item condition
- **Depends on your tools:** a worn saw makes a worn bow.
- **"Craftsman"** (a non-combat skill, §6) makes crafted items come out one condition level higher.

### Items promised by other systems (for now)
| Item | How |
|---|---|
| **Journal** (§6) | A notebook (common loot: bodegas, schools, offices) plus a pen. Writing in it is an action, not a recipe |
| **Bag repair** (§11) | A sewing kit fixes ripped seams by hand; the sewing station does it better |
| **Improvised suppressor** (§13) | A bottle or oil filter plus duct tape, by hand |
| **Pipe shotgun** (§13) | Pipe, nails, a spring and duct tape, at the workbench |
| **Ammo crafting** (§13, endgame) | Gunsmith bench with a **reloading press**, using **spent brass casings** (picked up after firing), primers (rare loot), gunpowder and lead from scrap |
| **Water** (§7) | Rain collectors; boiling over a fire (an action); purification |
| **Comfort items** (§7, mood) | Beds, couches, radios, made at the workbench |

### Clan crafting
- Clanmates can use each other's stations. **Recipes belong to each person**, so the clan's medic makes the medicine.

### Farming
- Gets its own section later. NYC rooftop gardens and community gardens fit the setting.

### Open items
- Which crafts can be done while walking.
- Full recipe list per station.
- Materials beyond the core 12; generator fuel.

---

## 15. Clans

### Size and alliances
- **Cap: 10 members by default; a server setting.** With 250–300 players, unlimited clans turn into "zergs" that run the server.
- **No formal (in-game) alliances, for now.** **Informal alliances agreed by voice are fine** and don't break any rules.

### Creating and joining
- Anyone can create a clan from the menu for free, and invite players who are nearby.
- **Leaving a clan starts a 12-hour cooldown** before joining another, so nobody can hop into a clan for access and then raid it from inside.

### Ranks
| Rank | Can |
|---|---|
| **Leader** | Everything: invite, kick, promote, disband, place the claim item |
| **Officer** | Invite, build, demolish, change door codes, officer-only doors and storage |
| **Member** | Build, use stations, beds and clan-wide doors and storage |

- The leader can switch a few permissions per rank (e.g., "members can demolish"). No custom rank trees.

### Doors and storage by rank
- **When an officer or the leader sets a code lock, they choose who can open it freely:** **everyone in the clan**, or **officers and above**. Clanmates at that level open it without typing the code.
- **The same applies to storage** containers.
- The code itself works like any code lock: anyone who knows it can open it, so it's also how to let an outsider in.

### What clanmates share
- Door access and storage (above), building rights in the claim area (§9), beds and sleeping bags (§10), crafting stations (§14).
- **Mood bonus near clanmates** (§7).

### Seeing each other
- **Name tags only in line of sight**, not through walls. _May change._
- **Clanmates' positions show on the map**, plus shared map markers.
- _Minimap: undecided._

### Friendly fire
- **On by default**, with a server setting to turn it off.

### Talking
- **Proximity voice chat** (DayZ-style): anyone near you hears you, enemies included.
- **Long-range voice needs a walkie-talkie** (an item that runs on decaying batteries, §12).
- **Clan text chat works anywhere.**

### Clan identity: graffiti tags
- Each clan designs a **tag** (emblem) that players **spray-paint on walls** with spray cans, marking bases and territory. Cosmetic only.

### Leaving or getting kicked
- Access ends instantly (doors, storage, beds). Whatever they put in clan storage stays with the clan.

### Solo players
- **Solo play stays viable:** offline raid protection (§9) and small bases. Groups have an edge, but solo isn't a punishment.
- **Maybe:** stronger offline protection for solo players (e.g., less damage taken, or protection starting sooner). _Not decided._

### Open items
- Minimap: yes or no.
- Stronger offline protection for solos: yes or no, and how much.

---

## 16. Vehicles, boats & helicopters

### The streets are jammed
- Abandoned cars clog most streets, bridges and tunnels. Main avenues have a few passable lanes; side streets are often blocked.
- **Driving means planning a route.** Cars don't dominate a city built for walking, and bikes stay valuable.
- **Heavy vehicles can push small wrecks aside.** Big jams stay put.

### Land vehicles
| Vehicle | Why | Rarity |
|---|---|---|
| **Bicycle** | Quiet, no fuel, fits through jams | Common |
| **E-bike, e-scooter** | Faster than a bike, quiet, runs on a battery | Uncommon |
| **Motorcycle, dirt bike** | Fast, weaves through jams, **loud** | Rare |
| **Sedans, yellow taxi** | Basic cars. **Several sedan types**, not one | Uncommon |
| **SUVs, police cruiser** | Tougher; police ones have a light bar. **Several SUV types** | Rare |
| **Van, box truck** | Big storage, slow, can push wrecks | Rare |
| **Ambulance** | Medical loot inside | Rare |
| **Military Humvee** | Armored, pushes wrecks | Very rare |

### Bike-share docks
- Bike-share stations (Citi Bike-style, made-up name) all over the city, with **regular bikes and e-bikes** still locked in their docks.
- **Bolt cutters free them** (§12).

### Charging e-bikes and scooters
- **Generator** at base (§14).
- **Also (confirmed):** **solar panels** as a quiet but slow alternative to the loud generator; **power banks**; charging from a running car; some bike-share docks still trickle-charging from their solar panel, making them contested public charging spots.

### Keys, hotwiring and locks: a modern setting
- **Keys** turn up in the vehicle, in nearby homes or on nearby zombies.
- **Not locked to you automatically.** Locking a vehicle takes a **lock system you have to make or install.**
- **Once a vehicle is hotwired, anyone can start it** (until someone locks it).
- **Modern setting: most modern cars can't be hotwired physically.** They're started through tech instead:
  - **An advanced OBD2 scanner** (key programmer) **can make keys** for a car.
  - **A hacking device starts cars without a key.**
- **Details (confirmed):** older cars hotwire physically (a Mechanics skill, §6); the key programmer needs a blank key fob (dealerships, locksmiths, auto shops); the hacking device is very rare; a key-cutting machine (hardware stores, locksmiths, needs power) copies existing keys for clanmates; locks: a **steering-wheel lock** (cheap; bolt cutters or a hacksaw remove it) and an **immobilizer with an alarm** (crafted from electronics; tampering sets off the alarm, which pulls zombies).

### Parts: DayZ-style, but parts are easier to find
- **Battery, spark plug, radiator, tires, headlights, engine, fuel.** Getting a car running **should be hard.**
- **Parts are not as hard to find as in DayZ:** salvage from the thousands of wrecks, auto-parts stores, mechanic shops.
- _Suggested:_ a vehicle status panel shows which parts are missing or broken, so it stays easy to learn.
- Repairs use repair kits and Mechanics recipes (§14).

### Fuel
- Gas stations, and **siphoning from wrecked cars** with a hose.

### Noise (hearing is the zombies' main sense, §8)
- Loudest to quietest: motorcycles, cars and trucks, e-bikes, bicycles (near silent).
- **Car alarms:** bumping or hitting some parked cars sets off their alarm and pulls zombies.

### Zombies and vehicles
- Running zombies over **damages your vehicle**.
- **Hordes can surround and stop a car.**
- **Zombies can pull you off a bike or motorcycle.**

### Vehicle storage
- Trunks and cargo areas use the **same cutaway packing as bags** (§11), each vehicle with its own trunk outline.

### Vehicle customization: extensive, in tiers like building
- **Tier levels similar to base building (§9).**
- **Engine upgrades:** mostly durability, some speed and power.
- **Armor is the main show.**
- **Armor (confirmed):** pieces like window grates (stop zombie grabs, some bullets), ram plows (push bigger wrecks, which matters on jammed streets), wheel guards and door plates; tiers from scrap and plywood up to welded steel plate (welder and power, §14); armor adds weight, so the vehicle is slower and burns more fuel; counters are the .50 cal, explosives and molotovs; clan graffiti tags as car paint (§15).

### Boats
| Boat | Why | Rarity |
|---|---|---|
| **Kayak, canoe** | Silent, slow, little storage | Uncommon |
| **Rowboat** | Silent, more storage | Uncommon |
| **Inflatable with an outboard motor** | Faster, uses fuel, loud | Rare |
| **Civilian boats, 10–20+ ft** (from marinas) | Bigger and faster; **harder to repair** | Rare |
| **Speedboat, police harbor boat** | Fast, loud, big storage | Very rare |

- Found at **marinas, boathouses** and the ports (§12). NYC has several marinas with 10–20+ ft civilian boats.
- **Civilian types (confirmed):** center-console fishing boat, bowrider, cabin cruiser, pontoon boat, jet ski.
- **Zombies don't swim:** they won't follow you into deep water. Water is safe from zombies, not from players.
- **Swimming is possible but costly:** you get soaked (body temperature, §7), and anything not in a dry bag gets wet (§11).
- _Maybe:_ strong currents in the East River at Hell Gate.

### Helicopters: in from launch
- **In the game from launch, extremely rare to find, and even harder to repair.**
- _Analysis / to decide:_
  - Where: NYC's real heliports (Downtown Manhattan, East 34th Street, West 30th Street), hospital helipads, and the police aviation base at **Floyd Bennett Field** (inside the map).
  - Types: e.g., small civilian, tour helicopter, news helicopter, police; a military one would be the rarest.
- **Rooftop bases that can't be reached on foot are allowed** (decided). The developer's reasoning:
  - Few buildings without a helipad have room to land a helicopter, and **most roofs have clutter** (AC units, water towers, antennas), which makes landing risky.
  - **If the clan loses its helicopter, they're stuck:** they can only respawn up there, with no other way down or back.
  - _Analysis:_ such a base can only be raided by another helicopter owner, or with explosives or a .50 cal from a neighboring roof. Helicopters being extremely rare keeps these bases rare too.
  - **Noise:** a helicopter is the loudest thing in the game and should pull zombies across a wide area.
  - **Server cost:** a cap of a few per server.
  - Flight controls simple enough for an average player.

### Server limits
- **A cap on vehicles per server and per clan.**
- **Abandoned vehicles despawn** after X days unless inside a claimed base (your garage).

### Open items
- Car customization: exact tier materials.
- Hell Gate currents (maybe).
- Deeper detail for keys, locks, charging, armor and boats comes when each is built.
- Helicopters: types, how many per server, flight controls.
- Vehicle caps and the despawn timer (X).

---

## 17. PvP rules

### Anyone, anywhere, anytime
- **Full PvP everywhere, full loot.** Anyone can attack anyone, anywhere, at any time, and everything you carry can be looted (§10).
- _Not adopted:_ PvE or "PvP zones" server types.
- **The one exception: safe zones** (below).

### Safe zones with trading NPCs
- **Safe zones with trading NPCs, where nobody can be hurt.**
- Details (locations, size, rules at the edges) are designed with trading.

### Surrender, restrain, rob (builds on knock-outs, §7)
- **Hands-up gesture** to surrender, or to show you're friendly.
- **Zip ties, handcuffs or rope** restrain a knocked-out or surrendered player. You can then search them (hidden pockets take longer, §11), **escort them** (they walk where you lead), or let them go.
- **Freeing:** a knife cuts zip ties and rope; bolt cutters cut cuffs (§12).
- **Anti-griefing:** a restrained player can **struggle free after about 10–15 minutes.**

### Combat logging
- **While you're in combat, or within 5 minutes of it, "quit to menu" is greyed out** and can't be clicked.
- **Damage from a clanmate doesn't count**, so friendly fire (§15) doesn't lock you in.
- **"Combat" means dealing damage to, or taking damage from, another (non-clan) player.** Fighting zombies doesn't count.
- **Force-quitting** (Alt-F4, pulling the plug) during that window doesn't help: **the character stays in the world until the 5-minute combat timer runs out, then for the regular 30-second leave timer (§10) on top.**

### No kill feed, no killer names
- No kill feed. **The death screen shows only how you died** (e.g., "gunshot to the head"), never who did it. Strangers stay anonymous; only clanmates get name tags (§15).

### No karma or bandit system
- No hero/bandit meter or bounties. Reputation comes from how players behave and from voice chat.

### First person and third person
- **Server setting: "first person only" or "both".** Official servers offer both kinds. (Answers the open question from §3.)

### Anti-cheat
- Server-authoritative design (§3) plus **Easy Anti-Cheat** (free through Epic Online Services, made for Unreal).

### Already decided elsewhere
- Raiding (§9): hard-to-find tools and explosives, offline protection by default, raiding is loud.
- Fresh spawns (§10): only minimal loading protection; low-loot spawn neighborhoods mean they aren't worth hunting.

### Open items
- Safe zones: see §18.

---

## 18. Trading, economy & safe zones

### Currency
- **A standard replacement for the US dollar**, the way modded DayZ servers use rubles. A physical item you carry, so it can be looted when you die (§17).
- _Not chosen:_ cigarettes, batteries or scrap metal as currency.
- **Name: an invented word, not an existing one.**
  - **Decided: "Sanctos Notes"** ("notes" in everyday talk). **The name comes from "sanctuary": the safe zones' own money.** It also has a deeper lore meaning (see the lore bible).
  - _Not chosen:_ Boros, Quarants, Zollars, Scrip.

### Safe zones: 6–7, in unremarkable places
- **No famous or well-known places.** Grand Central, Yankee Stadium, Barclays Center and Citi Field are **for combat and bases**, not safe zones.
- **Two kinds of site:**
  - **Big warehouses**, like parcel-delivery or online-retail distribution centers, whose giant open rooms hold the **main traders**. (Fictional company names, no real brands.)
  - **Random tall buildings** in the city with good space for a safe zone and **good sniping positions** for the overwatch.
- **About 6–7 in total**, because the map is so big: roughly one per borough plus 2–3 more, **including one in New Jersey** and **a small one on the Staten Island piece.**
- **Each safe zone is named "Sanctuary" plus a number** (Sanctuary 1 to 7) (decided 2026-10-27; who runs them is in the lore bible).
  - **Numbered in the order they opened**, so Sanctuary 1 is the oldest.
  - **One number is missing: a Sanctuary that fell.** Its ruins are a lore area and point of interest (§5). With 6–7 active zones plus the fallen one, the numbers run to 7 or 8 (to confirm).
- NPC guards and walls keep zombies out. **In the lore, the guards are mostly ex-military** (including soldiers who had been contracted to the Force), **ex-police and the like** (decided 2026-10-27).
- **Several exits** per zone.
- _Exact sites and how many: TBD._

### Safe zone rules
- **No damage inside, ever** (§17).
- **Hostile marking:** shooting someone near a safe zone marks you **hostile**, and the guards won't let you in for a while (about 10 minutes).
- **Sniper overwatch against campers:**
  - **NPC snipers** are posted at each safe zone and watch for players **camping within a set distance** of it.
  - They start with a **warning shot and a loudspeaker message**. The camper gets **5 seconds to leave** the area.
  - After that, the snipers **target the camper**. Their aim is elite: they **can miss, but rarely**, if you're in their line of sight.
  - **Elite in gameplay, above average in the lore:** in the story they're mostly ex-military whom the group kept training. The game makes them elite so the anti-camping rule works (decided 2026-10-27).
  - **What counts as camping:** staying inside a ring around the zone (about **100–150 m**) for more than **about 60 seconds**; the timer runs faster if you're prone or aiming down sights. **Someone just passing through, or waiting for a friend with no ill intent, never gets shot.**
- **No building near safe zones** (a set radius).

### Bank and storage units
- **Two-step access, like a card and its PIN:**
  - A **physical item linked to your character, or to a clan account** (the "card").
  - **Plus a PIN.**
- **A lost or stolen card is useless without the PIN.** A **replacement card** is sold at any safe zone and cancels the old one. **The fee is expensive**, so it's worth not losing the card or leaving it at base before a safe-zone trip.
- **Money: one account across all safe zones.** Deposit in Brooklyn, withdraw in Queens.
- **Items: a storage unit at each safe zone**, mainly so **solo players** who can't grind out a base still have somewhere safe for a few things.
  - About **50–100 lbs** of items, **for rent** (a recurring fee). Rent keeps money leaving the world and stops abandoned units piling up.
  - **Items stay where you stored them:** you can only take them out at that safe zone. Only money moves between locations.
  - **A storage unit is a service in the safe zone's building** (with the bank), not a room: you can't physically live in it.

### NPC traders
- **Types:** general (food, clothes, basic tools), medical, weapons and ammo, building supplies, mechanic (vehicle parts, bikes, maybe an old car at a steep price).
- Each safe zone has some of these, not all, so different zones are worth visiting.
- **Never sell the top tier** (raid tools, explosives, the antiviral, the machine gun, the .50 cal). Those stay loot-only.
- **Very rare items: tiny stock, steep prices.**
- **Prices move with supply** (tied to the central economy, §12): selling lots of something drops its price; low stock raises it.
- **Services:** repairs (never to Pristine, §12), key copying (§16), possibly paid information such as map intel.

### Valuables
- A loot category whose main use is selling: jewelry, watches, phones, laptops.
- **Point of interest: the Diamond District** (47th Street, Manhattan), with high-value valuables and a hotspot to match.

### Player-to-player trading
- **Inside safe zones:** a **secure trade window** (both put items in, both confirm).
- **Outside safe zones:** drop-and-pick-up, DayZ-style. Risky, so trust matters.
- **Player shops:** a craftable **vending machine** at your base sells items for currency while you're offline. It can be raided like any base part.

### Open items
- Safe zones: exact sites and count (6–7).
- Storage units: rent amount and period; exact weight limit (50–100 lbs).
- **Maybe: rare roaming military patrols** in the world, what's left of the Force's military (the developer's idea, 2026-10-27). How they treat players: TBD.

---

## 19. Weather, day/night & seasons

### Day/night cycle
- **3 real hours of day, 1 real hour of night** (a 4-hour cycle).
- **Real darkness:** the power is out, so there are no streetlights. Light comes from the moon (with phases), fires, generators and flashlights. A lit window at night gives a base away.

### Night
- **Zombies see worse at night** (§8). More of them roam the streets at night, so moving in the dark is a gamble.
- **Flashlights and weapon lights give you away** to other players.
- **Zombies drawn to flashlights: leaning yes** (2026-10-27): zombies can see, so a flashlight will probably draw them. **Final once the lore decides what the infection is** (a virus, a fungus, etc.). The earlier concern still stands: it could make nights much harder than intended, so how strongly a light pulls them gets tuned in the zombie deep pass. _Not adopted: Claude's "no special pull"._
- **Night vision goggles:** military, **very rare.**

### Weather types
| Weather | Effect |
|---|---|
| **Clear** | Normal |
| **Overcast** | Darker nights (no moon) |
| **Rain** | Soaks you (body temperature, §7), fills rain collectors (§14), **muffles noise** so sounds carry less far, cuts sight a little |
| **Thunderstorm** | Like rain; **thunder masks gunshots** for a moment |
| **Harbor fog** | Rolls in off the water; **heavy sight loss** for everyone, worst near the rivers and harbor |
| **Snow** (winter) | Cold, slows movement, **leaves footprints** others can follow (Survival tracking, §6) |
| **Blizzard / heavy snowfall** (winter) | **Rarer than snow.** Very cold, slow going, very low visibility. _Added by the developer._ |
| **Heat wave** (summer) | You get thirsty much faster |

### Seasons
- **Spring, summer, fall and winter cycle**, each about **1–2 real weeks** (a server setting; a server can lock one season).
- Seasons set the temperature range and the weather mix.
- **Winter is the hard season:** clothing, shelter and fire matter much more.
- Seasons tie into farming later (growing seasons).

### Rare weather events
- **Nor'easter:** a rare winter storm. Heavy snow, very cold, almost no visibility. Everyone hunkers down, which makes it a good time to raid.
- **Hurricane with flooding** in low areas (Red Hook, Lower Manhattan, the Rockaways, as during Sandy). _In._
  - _Analysis:_ water levels that change across the map are a big technical job (flooded streets and ground floors, then draining). Worth prototyping early to see what Unreal's water tools can handle.

### Knowing the weather and the time
- **HUD: only a general feel** (e.g., a weather icon and "cold" / "hot").
- **Exact time and temperature need an item:** a **watch** shows the time; a thermometer (or a watch that has one) shows the temperature.
- **Forecasts: two sources.**
  - **Barometer** (a found item): falling air pressure means a storm within hours. The realistic way people forecast without satellites; no broadcaster needed.
  - **Safe-zone radio:** the organized group running the safe zones (§18) broadcasts short-term warnings from someone reading a barometer and the sky. Doubles as a lore channel.
  - _Not chosen:_ automated stations reporting current conditions; no forecasts at all.

### Server cost: low
- The server only tracks the weather state. Rain, fog and snow visuals are drawn on each player's own PC.

### Open items
- Zombies drawn to flashlights: leaning yes; confirm once the infection itself is designed (lore).

---

## 20. Servers: persistence, wipes & admin

### Wipes
- **Official servers wipe every 6 months to a year.** **Progress shouldn't feel like it was for nothing.** _The interval may change after release, based on player feedback._
- Not tied to the season cycle (§19), which turns over every 1–2 months.
- _Rejected:_ wiping once per in-game year (every 1–2 months), and never wiping.

### What a wipe clears and what it keeps
| Wiped | Kept |
|---|---|
| Bases, storage, buried stashes | Character appearance |
| Items, vehicles, helicopters | Clan name and graffiti tag design |
| Bank money and storage units | Stats and achievements (e.g., "survived 3 winters") |
| **Levels and recipes** | |

- Why levels are wiped too: everyone restarts equal, and the journal (§6) plus the catch-up boost make re-leveling quick.

### One server per character
- Your character lives on one server. **No shared character across servers**, which would let players loot an empty server and carry the gear into a busy one.
- You can play on several servers with a separate character on each.

### Restarts
- **Every 6–12 hours**, with warnings at 15, 5 and 1 minutes.
- **Restarts don't count as combat logging** (§17).
- **Everything persists through restarts:** bases, buried items, vehicles, bodies until their timers run out.

### Saving and crashes
- Continuous saving; important changes (building, trades, bank deposits) save immediately. **After a crash, the rollback is seconds to a minute at most.**

### Clutter control
- Base decay when nobody visits (§9), abandoned vehicles despawn (§16), dropped items despawn (§12), bodies last 2 hours (§10), containers reset through the central economy (§12), storage units cost rent (§18).
- **Unused world vehicles move to where players are** _(added by the developer)_: each vehicle the world spawned has a **radius (a few blocks, not a tiny one) and a timer**. If **no player enters that radius before the timer runs out, the vehicle respawns somewhere else.** This stops vehicles piling up in empty parts of the map. _Interpretation:_ applies to world-spawned vehicles nobody has used yet; vehicles players own follow the abandoned-vehicle rule (§16).

### Official and community servers
- **Official servers** run the default settings and the official wipe interval.
- **Community servers** can be rented and change the server settings, including the wipe interval or "never wipe".
- _Later:_ mod support (a big job in Unreal; not in the launch plan).

### Server settings in one place
- All server settings go into **one settings file** with documented defaults when we build: player cap, first-person only, clan cap, friendly fire, offline raid protection mode, day/night length, season length and season lock, vehicle caps, wipe interval, and so on.

### Admin tools
- Kick and ban, spectate, **logs** (kills, raids, trades) for disputes and catching cheaters, and an item spawner for community events.

### Open items
- Vehicle relocation: radius size and timer length.
- Restart interval within 6–12 hours.

---

## 21. Character creation

### Appearance
- **Presets plus a few sliders:** body type (two base bodies), face presets plus a few sliders, skin tones, hair, facial hair, tattoos.
- **Age:** young adult to older adult. Cosmetic only.
- **Voice:** a few voice sets per body type (grunts, pain, the hands-up callout).
- No deep face sculpting: expensive to build, and in first person nobody sees your face much.
- **Appearance carries over through wipes** (§20).

### Handedness
- Left- or right-handed; players aren't told why it matters (§7).

### Occupation: an NYC job before the outbreak
- Each occupation gives **a couple of free recipes or skills (worth about 2–3 points) and one small starting item. Never combat bonuses** (§6).
- **The occupation is the character's "trait":** its identity comes from the skill it gives. There's no separate traits system.
- **You pick your occupation again each time you start a new life** after dying.
- _What each one gives will be refined later._ Starting list:

| Occupation | Free knowledge | Starting item |
|---|---|---|
| Nurse | Basic medical recipes | Extra bandages |
| Mechanic | Vehicle repair basics, hotwiring older cars (§16) | Screwdriver |
| Construction worker | Basic building pieces | Hammer |
| Line cook | Cooking recipes (better meals for mood, §7) | Kitchen knife |
| Firefighter | Fire safety, forcing doors | Fire axe (may be too strong; refine) |
| Bike messenger | Bike repair, faster bike handling | Bike lock |
| Cab driver | Car handling, knows the streets | City map |
| Subway worker | Knows the tunnels (subway map) | Headlamp |
| Dockworker | Container yards (§12): opening seals faster | Work gloves |
| Bodega owner | Better prices at traders (§18) | A little currency |
| Unemployed | No free knowledge, but **+2 extra recipe points** | None |

### Name
- A character name, visible only to clanmates (§15). Strangers stay anonymous (§17).

### Starting outfit
- The starting kit is basic clothes (§10); **you choose its look** from a few civilian outfits (hoodie and jeans, work clothes, office clothes, track suit). Cosmetic only.

### Open items
- Refine what each occupation gives.

---

## 22. Farming, fishing & food sources

### Where you can grow
- **In the ground:** anywhere diggable (parks, backyards, empty lots, community gardens), the same ground rule as burying journals (§6).
- **Raised beds and planters:** crafted and filled with **bags of soil** (hardware stores, garden centers). On **rooftops**, balconies or inside your base. Rooftop farming is the city-style way to farm.
- **Community gardens** start with some overgrown crops and good soil: small contested spots.

### Crops: about 8, tied to the food groups (§7)
| Crop | Food group | Note |
|---|---|---|
| Tomatoes, peppers, leafy greens, squash | Vitamins | The easy fix for a poor diet |
| Potatoes, corn | Carbs | Filling, store well |
| Beans | Protein | **Dried beans from a bodega can be planted** |
| Herbs | (cooking) | Make cooked meals better for mood (§7) |

### Seeds
- Found at garden centers, hardware stores and community gardens, plus dried food from groceries.
- **Harvesting gives seeds back**, so a farm keeps itself going.

### Growing
- **Plant, water, harvest.** Plants show small icons ("needs water", "ready").
- **Water:** rain does it (§19); otherwise a watering can with water from collectors (§14).
- **Crops grow in real time, even while you're offline:** a few real hours to a day, depending on the crop.
- **Compost** made from rotten food (§12 decay) speeds growth.

### Seasons (§19)
- Spring and summer: fast growth. Fall: slower, harvest time. **Winter: outdoor crops die from frost.**
- **Greenhouses** (crafted) protect crops into the cold months.
- **Endgame: indoor grow lights** grow food all year but **need power** (generator or solar, §14). A lit grow room shows from outside at night (§19).

### Risks
- **Crops outside your base can be stolen**, and **zombies trample** fields they wander through.
- Rooftop and indoor farms are safer, at the cost of hauling soil and water up.

### Mood
- Tending a garden **eases boredom and stress a little** (§7).

### Chickens
- **Backyard chickens** can be found and kept in a crafted coop. They give **eggs (protein)**, need feed and water, and can be stolen or eaten by zombies.
- _Maybe later:_ rabbits.

### Fishing: yes
- **Fishing in the rivers, harbor and off piers**, a protein source (Survival skill category, §6).
- _Details to design:_ rods and tackle (sporting goods), bait, fish types, the best spots.

### Wildlife and hunting: yes
Ties to the setting: **wild animals have moved back into the overgrown city** (§5).

**Prey**
| Animal | Where | Gives |
|---|---|---|
| Deer | Parks, Bronx, Staten Island | Lots of meat, hide |
| Wild turkeys | Parks, Staten Island | Meat, feathers (arrows) |
| Geese and ducks | Parks, Jamaica Bay | Meat, feathers |
| Rabbits | Parks, overgrown lots | A little meat |
| Pigeons and rats | Everywhere | Desperation food |

**Dangers**
| Animal | Why |
|---|---|
| Feral dog packs | Former pets gone wild; the most common animal threat |
| Coyotes | Packs, mostly at night |
| Black bears | Coming down from the north through NJ and the Bronx; rare and very dangerous |
| Bobcats | From the north; rare ambush hunters |

- **Rare sightings:** **seals in the harbor** and **a beaver in the Bronx River**. World details, rarely seen.
- **No zombie animals.** Animals run from zombies.
- **What hunting gives:** meat (protein, §7), hides for leather (a leather jacket blocks bites, §8), feathers and sinew for arrows and bowstrings (§14).
- **Gunshots attract zombies, so bows are the hunter's weapon** (§13).
- **Tracking:** footprints in snow (§19) and blood trails, part of the Survival skill (§6).
- **Hunting grounds:** the big parks (Central, Prospect, Pelham Bay, Van Cortlandt, Forest Park), Jamaica Bay and the Staten Island piece.
- **Server cost:** animals use AI like zombies and count toward the same AI limits (§3).

### Server limits
- Crops and coops count toward the clan's building piece cap (§9).

### Open items
- Fishing details.

---

## 23. Lore

**The full lore lives in [docs/lore/LORE.md](lore/LORE.md) (the lore bible).** This section is only a summary.

- **Deep lore.** It shapes the map, the points of interest and several mechanics.
- **Paused on 2026-11-08:** development starts now, and the developer will **revisit the entire lore later in development.** Lore-heavy content (points of interest, safe zones, radio broadcasts) is best built after that revisit. _Earlier plan:_ build the lore before development got far.
- **No cutscenes.** Told through **clues in the world** and **random radio broadcasts** (Project Zomboid-style, adapted to a game that starts years after the outbreak).
- **Origin (decided): it came from outside.** The whole world has fallen, with pockets of survivors and safe zones elsewhere, but most survivors in the city don't know what's going on outside. Direction: researchers came to NYC to study it, the city was walled off and held well for a while, then **it spread inside the walls because of the research**. **Plus a twist** (chosen; the details live only in the lore bible, since players are meant to uncover them).
- **The city was governed by the Force: F.O.R.C.E., the Federal Office of Response and Containment of Epidemics**, a FEDRA-like government created by the federal government. **Its research agency and the military in the city were both under it**; the military built the wall. After the outside fell, it became independent. Military and National Guard sites in the game are what's left of that. **Today its military is far smaller** (many soldiers left once the infection spread inside the walls), and **no wall checkpoints are manned.**
- **When:** the game starts in **year 8** after the outbreak. The city held for about two years, then fell in **year 2**, about **6 years** before the game.
- **Survivors call the moment it got inside the walls "the [neighborhood] Breach"** (neighborhood TBD: NJ or the Bronx). "The fall" is the city's whole collapse that followed.
- **Still to build:** the safe-zone group, the remaining names, the rest of the timeline, radio stations, the infection itself and lore areas (see the lore bible).

---

## 24. Development plan

Milestones in build order. Each system still gets its deeper design pass when we start building it.

### Setup (before milestone 1)
- Visual Studio 2026 and Unreal 5.8.4 (launcher): installed 2026-11-08.
- Unreal 5.8 built from source, needed for dedicated servers (§2): **in progress, 2026-11-09.** Source 5.8.4 at `C:\UE5.8.4 Raw\UnrealEngine-release` (same network version as the launcher's 5.8.4); the developer ran Setup.bat and GenerateProjectFiles.bat; compiling. **The project switches to the source-built engine once it's compiled** (the developer: "yes switch it"): the editor is opened from that engine (double-click `NYZ.uproject`) instead of the Epic launcher; same editor and UI. _Why:_ only a source build makes dedicated servers (needed for the real load-test numbers, stage 2 on cloud machines, and launch), and two engines building the same project overwrite each other's compiled code. _Not chosen:_ keeping the launcher engine for editing plus a separate copy of the project for server builds (two copies to keep in sync).
- The UE5 C++ project: **created 2026-11-08.** A blank C++ project named NYZ (no starter content, raytracing off) at `C:\Game Dev Folder\NYZ\NYZ`, pushed to the [NYZ](https://github.com/NNarwhall/NYZ) repo with UE5 ignore and LFS rules (§4). The docs repo ignores that folder.

### Milestone 1: multiplayer foundation and an early load test (decided 2026-11-08)
- **Noclip for testing** (the developer, 2026-11-08: "generally a noclip is nice for development/testing"). Development builds allow cheat commands on any server, including the load-test server. In the console: `ServerExec ghost` flies through walls where the camera looks (20 m/s, 100 m/s with sprint), `ServerExec walk` lands again. In Play without a server, plain `ghost` and `walk` work. Shipping builds never allow cheats; admin-only commands (§20) replace this in the server pass. Checked by the developer on the load-test server: "It works".
- **Test early, kept small** (Claude's recommendation; the developer: "Early kept small"). The test runs on what the game needs first anyway: **the player character and movement, the dedicated server setup and basic zombies.**
- **Made only for the test:** a **bot script** (bots are the real player character, driven by a script instead of a keyboard) and a **map of plain boxes**.
- **Bare versions only** (the developer, 2026-11-08: "if we are just testing the server limit, why are we going all out on movement"). Each piece gets only what it needs to load the server the way the real thing would. **Its full design pass comes after the test**, when it's built for real. This holds for every system that goes into the test or its reruns.
  - **The test character:** Unreal's standard **Character Movement** (what the template character already uses), walk, sprint and jump at rough speeds, and Unreal's mannequin as the body. Speeds, stances, stamina, falling, swimming, camera details, leaning and footstep noise wait for the movement pass.
  - _Why Character Movement:_ it's the only movement choice the test depends on, since the test measures its cost on the server. Mover, Unreal's newer movement system, is still experimental in 5.8, and its own readme says little work has gone into scaling, so it suits games with few characters.
  - _Not chosen:_ a full movement design pass before the test (Claude's proposal).
  - **Built 2026-11-08:** the test character in C++ (Character Movement with a sprint the server predicts, so sprinting causes no position corrections; rough speeds 3.5 m/s, sprint 6 m/s; the template's over-the-shoulder camera; WASD, mouse, Space, Shift), Unreal's template mannequin with its walk/run animations, and a game mode that spawns it. Checked with a headless server and client on the same PC: the client joins with no spawn or loading errors. The server's tick cap is Unreal's default of 30 per second, which matches the pass bar; actual tick rates are measured in the load test. The developer then played it in the editor as a client of a background server: "Tested and its working." _Not yet:_ gamepad controls, the box map, bots, zombies, the dedicated-server build (needs the source build).
- **Test at both 300 and 500 players** (the developer, 2026-11-08: "lets test both when we do the test wont hurt"): 300 is the launch target, 500 the later goal (§2), and the map should take about 500 comfortably (§5). The 500 run needs more rented machines.
- **The bot test is rerun as systems are added**, to catch the point where the server starts struggling. A full test with the finished systems still comes later.
- **The real map joins milestone 1** (decided 2026-11-09; the developer: "One major thing i think we shouldve done first is map development, because that is going to have a HUGE impact on the server no?", then "Okay, how about getting the whole terrain in, then we can focus on specific areas with buildings and roads etc?"). After the real-server numbers:
  1. **The whole terrain, bare:** real elevation from free survey data, the coastline, water at sea level, the map border (`tools/map`, about 34 × 40 km), set up with World Partition and the real Iris grid bounds. No roads, buildings or foliage yet. Then a bot run on it, measuring the server's memory and load time with the whole map loaded.
     - **Heightmap built 2026-11-09** (`tools/map/build_terrain.py`, one command; details and import settings in `docs/map/terrain-notes.md`): the developer's USGS 1 m tiles from September plus five missing ones, cut to the border's rectangle, **34.5 × 40.6 km at a 2 m grid** (Claude's call; the developer's September terrain used 4.92 m over 40 km; the memory test decided 2 m is affordable: the whole bare terrain costs the server about 1 GB), heights -27 to 133 m, checked 1:1 against known places. Sea level is Unreal Z 0. Open water outside the surveys is a flat -5 m for now; real water depths come in a water pass. _Not yet:_ imported into Unreal.
     - **Import tool written and tested 2026-11-10** (`NYZ/Tools/import_terrain.py` plus the editor-only module `NYZ/Source/NYZEditor`; the developer: "consider performance on the import because that was my issue last time, getting the whole thing in without crashing"). Unreal's own import keeps the whole map in memory until it ends; the tool brings it in one 4 km region at a time and frees each one, continues after a crash, and checks heights in Unreal at six places. Streaming pieces of about 1 km. Iris's grid is widened to cover it (±18 × ±21 km). Runs after the engine switch.
     - **Imported 2026-11-10** into `/Game/Maps/NYC`: all 90 regions in 15 minutes, no crash, the editor peaking at 10.6 GB; heights in Unreal match the heightmap at all six check places. 1.7 GB on disk in 1,366 files. Coloured by height (placeholder) and shown on the editor's World Partition minimap (`NYZ/Tools/style_terrain.py`).
     - **Server on the bare terrain (2026-11-10):** the packaged server loads the whole map (its streaming is off) in **7 s** and uses **1.5 GB** with no players, **1.7 GB** with 40 (the box test map: 0.5 GB). 40 bots spread over the city from 230 starts on land, one every 2 km (`NYZ/Tools/place_test_starts.py`; `run_bots.ps1 -Map /Game/Maps/NYC -Crowd 0`): main thread busy 5.2 / 6.8 / 8.8 / **11.5%** at 10 / 20 / 30 / 40 bots (0.07–0.14 cores, 1.6 KB/s per player), a little under the box map's spread run (13.7%), so bare terrain adds nothing per player. **The 2 m grid is affordable.** Not yet run with zombies on it. _Next:_ the dense block.
  2. **One dense test block** on that terrain: a blockout (plain grey, real collision) of a real NYC block footprint with enterable interiors, doors and placeholder containers as simple network objects, and zombie pathfinding through it. Measured with players and zombies, it sets the **density budget** (how many doors, containers and so on a block can afford), which becomes the limits for the city-building tool (§5: e.g. how many buildings per block can have interiors). _Changed 2026-11-10:_ it was "the template for building out the city"; with the city built from NYC's 3D models by a procedural tool (§5), the blockout only measures.
     - **Kept as a grey blockout, not the real city pipeline (2026-11-10).** The developer: "A real dense block would require heavy planning to be anything like how i want the city to be built ... but this would go way out of line of server testing". Claude: right, so the test block uses no real building models, art or tool: plain boxes with rooms, doors and containers on a real block footprint, enough to measure what interiors, doors, containers and zombie pathfinding cost the server.
     - **Built and measured 2026-11-10.** The block is the real one holding the Russian and Turkish Baths, East 9th to 10th Street between 1st Avenue and Avenue A: 42 buildings from OpenStreetMap (`tools/map/fetch_block.py`), 3 to 10 floors, generated grey by `NYZ/Tools/build_test_block.py`: every floor enterable, a corridor with switchback stairs, rooms of about 5 × 5 m each with a door and 2 crates. **The real block: 209 floors, 880 doors, 1,766 crates.** Three copies of it sit 300 m away, so the map holds 3,520 doors and 7,064 crates as sleeping network objects (dormant: nothing sent until used). Zombies find paths on a navigation mesh over the real block and open doors; bots walk to random crates on every floor and use them, opening doors on the way. A check at server start routes to 200 random crates: about 95% reachable on every floor.
       | Test (NYC map, packaged server) | Main thread busy | Updates/s | Slowest | Sent per player | Server memory |
       |---|---|---|---|---|---|
       | Bare terrain, 40 bots spread over the city | 11.5% | 30.0 | 35 ms | 1.6 KB/s | 1.7 GB |
       | 4 blocks, no players | n/a | n/a | n/a | n/a | 1.7–1.8 GB |
       | 10 / 20 / 30 / 40 bots all in the block | 8.1 / 11.3 / 18.5 / **32.5%** | 29.7–30.0 | 39–96 ms | 3.7–9.1 KB/s | 1.8 GB |
       | Same with 200 zombies awake in its rooms | 25.6 / 36.6 / 67.7 / **68.1%** | 29.9 → **27.8** at 40 | up to **183 ms** | 7.9–20.5 KB/s | 1.9 GB |
     - **What it says (first density budget, rough):**
       - **Sleeping doors and crates cost almost nothing on the main thread.** 40 bots packed into the block cost about what 40 players that close together cost anyway (the crowd cost from point 6 predicts about 40%), whether they were looting or stuck outside the doors.
       - **Memory is the limit for interiors.** The four blocks added about 0.2–0.3 GB to the server, about 60 MB per block of this density (geometry, doors, crates, and the navigation mesh over one block, not separated). With the whole map loaded on the server, the whole city at this density (about a million buildings, so roughly 24,000 blocks like this one's 42) would need far more memory than any server has. So either only a small share of buildings get full interiors, or the server loads only the areas near players (World Partition's server streaming, off today). This feeds the open question of which buildings are enterable (Open questions) and the city-building tool's limits (§5).
       - **Zombies plus a crowd are the CPU limit.** 200 awake zombies on paths add about 0.09% of the main thread each with 10 players and about 0.18% with 40. 40 players plus 200 zombies in one block is the first test where the server slipped below 30 updates a second (27.8, slowest update 183 ms).
     - **Found while building it (settings in `NYZ/Config/DefaultEngine.ini`):** Unreal's default navigation setting copies the shape of every terrain piece in the map as soon as any navigation mesh exists: **17.6 GB on the NYC server** for a mesh over one block. Copying only where mesh is made ("lazy") brings it back to 1.7 GB, and any city-wide navigation mesh needs it. The default 19 cm navigation grid closes 1.2 m doorways, so the mesh uses a 10 cm grid and 30 cm clearance. Doors stop blocking once open, so they can't trap anyone.
     - **Not covered yet:** the copies have no navigation mesh or zombies; doors and crates are placeholders (a count, not loot); no interiors' lighting or detail (they cost the server nothing).
     - **One block is not the city (the developer, 2026-11-10, after walking it):** "you consider a 1 block row of buildings "dense" when later we plan on having this basically times 1000x its nyc of course its dense". Right: "dense" here meant one block with every floor enterable, so the test gives a **price per block**, not a city-scale result. Scaled up, the price says the test's way of building doesn't survive: about 60 MB of server memory per block, and one network object and one map file per door and crate (about 2,650 a block; the four blocks already made the editor's map 11,000 files). So the next test is **city scale**: many blocks, with doors and containers stored lightly (not one object each) and the server loading only the areas near players.
     - **Real map before more tests? (the developer, 2026-11-10; not decided yet):** "is this the next best step? dont think we should just hone the map down (with the systems i said before) and then continue so we have more accurate test results" (the systems: §5's city buildings from NYC's official 3D models with a procedural tool). _Claude's answer:_ yes, rather than a city-scale test on grey copies, which would be thrown away, but in an order that measures as it goes: (1) the official building shells (outside only, no interiors) over the whole map first, which is itself the city-scale test with real data (can the server hold every building's collision?); (2) before the tool makes interiors, settle what the block test showed: doors and containers stored as light data, and whether the server loads only areas near players, since both change what the tool outputs; (3) settle §5's grid conflict with §9 early, since it decides which buildings keep the official mesh; (4) interiors on one district, measured, then wider.
  - _Why:_ what you see (foliage, textures, lighting, how broken a building looks) costs the server nothing; the map costs that matter on the server are collision, interactive objects, zombie pathfinding and memory, and the map should be designed to the server's budget rather than the other way round.
  - _Not chosen:_ building the whole city first (Claude: the big map costs only appear once doors, loot and pathfinding exist, and reworking a finished city to a budget is far costlier than measuring a block first); a dense block on flat ground before the terrain (the developer chose terrain first: everything sits on it, and it answers the map-size memory question early).
- _Why early:_ if 300 players don't fit on one server, the fixes (a different networking system, or splitting the map across servers) change how every system sends its data, so finding out late means reworking all of them (§3).
- _Not chosen:_ testing only after most systems are built, so that nothing is made just for the test (the developer's first understanding). The test-only parts are small, and the bot script is reused for every rerun.
- **Details (Claude's proposal, agreed 2026-11-08; the developer: "All yes i guesss", plus the money change in point 6):**
  1. **Pass bar:** with 300 bots, the server holds 30 updates per second on average and never dips below 20 for more than a moment. Starting numbers, tuned after the first results.
  2. **Test map:** flat, 25 × 25 km (about the real map's land area), plain boxes as buildings, so bots spread out like real players.
     - **Built 2026-11-08** as `/Game/Maps/LoadTestMap`, the project's default map (for the game, the server and the editor's start). One flat ground slab, 25 × 25 km. **15,580 boxes** on a 200 m grid, each 50–150 m wide and 10–60 m tall, so streets are at least 50 m wide. **5 hotspots**, each a 320 m square of 64 boxes 25–30 m wide with 10–15 m alleys, tagged "Hotspot" so the bot script can find them. **500 player starts** on random street corners across the map, one per bot in the 500 run, plus 405 starts for hotspot bots, one on each of the 81 alley crossings in every hotspot (point 3). A sun and sky only so it can be seen in the editor.
     - Made by a script in the game repo (`Tools/build_load_test_map.py`, fixed random seed), so it can be rebuilt or changed in one go. Checked: the ground and boxes block, the headless server loads it by default in about 0.1 s, and a client joins. The developer then played it in the editor (2026-11-08): "works, but when i tried 10 players my pc couldnt really handle it and almost crashed,max i tested was 5". That's expected, not a map problem: every player played in the editor gets its own window drawing the whole game with full lighting, and the PC (i5-13600K, 32 GB, RTX 4070) runs them all. Bots will run with no window or graphics, so they cost far less each. How many fit on this PC is what stage 1 (point 6) measures.
     - **One plain level: no World Partition, no landscape** (Claude's call). _Why:_ the server loads the whole map either way (World Partition's default on servers), and the test measures players and zombies, not map streaming. All 15,900 boxes are drawn as copies of one mesh in 6 actors, so the map is a single 3 MB file. _Not chosen:_ World Partition (splits the map into many small files and adds streaming the test doesn't measure; the real NYC map will use it); a landscape (heavy terrain data for ground that is flat anyway).
     - _Not yet:_ no navigation mesh. The zombies step decides whether they need one to path around the boxes.
  3. **Bots:** walk, sprint and jump along random routes; crowd into a few hotspots (20–50 at once); shoot each other; pick up and drop items; open containers. Vehicles and building in a second round.
     - **Each bot is its own copy of the game with no window or graphics**, joined to the server like a player (Claude's pick, 2026-11-08; the developer: "Yes, here", to building it with this pick). _Why:_ the server sees real connections, so the test measures the cost of sending updates to every player, the main thing it checks. _Not chosen:_ the server running the bots itself (far cheaper, hundreds fit on one PC, but with no connections it skips that cost).
     - **Built 2026-11-08, movement only (bare first version).** A game started with `-bot` drives its own character the way the keyboard would. A roamer walks the street grid to a random corner up to 1 km away, then picks another, so the bots stay spread like their starts. It sprints about a third of the stretches, jumps about every 10 s, and picks a new route if it's stuck for 3 s. It follows the map's grid, so it needs no navigation mesh. Bots run at 60 frames a second, like a player's PC, so each sends as many moves as a player.
     - **Hotspot bots start in the hotspot** and wander its alleys (Claude's call). Half the bots join with `?Hotspot=HotspotN` and start on one of that hotspot's 81 alley crossings, which the map now has as tagged starts. 30 per hotspot by default, Hotspot1 first, so even a small run makes a crowd. _Why:_ walking to a hotspot across the 25 km map would take 15–35 minutes every run.
     - **Run with one command:** `Tools/run_bots.ps1 -Count N` in the game repo starts the server and N bots, one a second, with logs in `Saved/LoadTest`. `-Stop` ends them all. Each bot's log has a line for every new route, to check it moves. The server's player cap is raised from Unreal's default of 16 to 500 for the test; the real cap comes with the server pass.
     - _Not yet:_ shooting, items and containers (those systems don't exist yet); vehicles and building (second round).
     - **Checked 2026-11-08 with 4 bots** (2 in Hotspot1, 2 roaming): all joined; the hotspot bots stayed inside the hotspot, moving from alley crossing to alley crossing; the roamers each walked about 1.4 km along the streets in about 7 minutes; none got stuck; no errors besides Epic's plugin noise.
     - **Found: each bot uses about 1.8 GB of memory** (and about a quarter of one CPU core), because it runs on the editor's program with all its editor parts. With the editor (about 5 GB) and the developer's other programs open, the PC's 32 GB fits only about 8 bots, a few more with the editor closed, still short of stage 1's "few dozen" (point 6). A packaged copy of the game, without the editor parts, should use far less; packaging the game (not the server) works with the launcher's Unreal.
     - **Bots now run the packaged game** (the developer, 2026-11-08: "Yes, package it"). Each bot uses **about 450 MB**, a quarter of before, and about a quarter of one CPU core. With the editor and the developer's other programs open, the PC fits **about 20 bots**; about 30 with the editor closed. Checked with 4 bots: all joined, their network version matches the server's, and the hotspot bots moved. The developer then ran 20 and watched the hotspot crowd from the editor ("I see them now"): the bots used 8.4 GB together, leaving 3.4 GB with the editor and its Play session open, so 20 is about the limit with the editor open. The server still runs on the editor's program (about 1.8 GB) until the engine source build gives us a dedicated server. Packaging takes about 5 minutes (`run_bots.ps1 -Package`, editor closed, output in `Saved/StagedBuilds`); the script refuses to start bots if the code, content or settings changed since the last package, since an older package wouldn't match the server.
  4. **Zombies:** simple server-side zombies (wander, hear, chase, attack); start with a set number around each player and raise it until the server struggles, which gives the zombie count per server (§8). Zombies far from players go dormant.
     - **Bare test zombie, written 2026-11-09** (Claude's plan; the developer: "yes do that"): the same character movement as players (to measure that naive cost first) on the mannequin, driven by its own server-side logic with no AI controller. **Wanders** to random spots within 20 m at 1 m/s; **hears** a player within 30 m (60 m if sprinting) and **chases** at 3 m/s (a walking player at 3.5 m/s stays ahead); **gives up** beyond 80 m; **swings** within 1.5 m but does no damage (no health system yet); **sleeps** with no player within 500 m (no movement work, a check every 2 s). Steers straight at its target with **no pathfinding**, so it can snag on boxes. Seen up to 500 m like players. Server and bots skip its animation, as for players.
     - **Spawning for the test:** the server's `-zombies=N` spawns N zombies 40–150 m around each player as they join (not inside boxes); `run_bots.ps1 -Zombies N` passes it on. The server's stats line and the test summary now include zombies and how many are awake.
     - _Open for the zombie pass:_ the real movement system (Character Movement per zombie won't scale to large hordes: players cost about 0.33% of the main thread each; Mass is the GDD's candidate, §3), pathfinding, how far zombies are seen, zombie art and animation, damage.
  5. **Networking:** try Iris first, Replication Graph as the fallback (§3). Check Iris's status in 5.8's release notes first.
     - **Checked 2026-11-08: Iris is production-ready in 5.8.** Epic's 5.8 release notes call it "production-ready for licensees in UE 5.8", with refined cull-distance handling and serialization. It's still off by default (the engine's `net.Iris.UseIrisReplication` is 0), so the project now **turns it on**: the Iris plugin is enabled in the project file (a first try with only the setting fell back to the old system, because the plugin wasn't loaded), and `Config/DefaultEngine.ini` sets `net.Iris.UseIrisReplication=1` with the registered sub-object list Iris needs. Odd but harmless: the plugin file itself still says beta and sits in the engine's Experimental folder. Server and clients have to match, so the editor needs a restart to join a test server. The first stage 1 runs use Iris; Replication Graph only if Iris falls short.
     - **First Iris result (2026-11-08, 10 bots):** 29.9 updates a second, never under 20, about 1.7 KB/s sent per player (2.3 without Iris), 0.2 CPU cores, 1.8 GB for the server.
     - **Found: Iris's map grid ends at ±10.5 km by default.** Iris decides who gets what from a grid over the map, and pins anything beyond its edge to the edge, so players far apart along the edge can look close. The test map reaches ±12.5 km, so `Config/DefaultEngine.ini` sets the grid to ±13 km. **The real NYC map (about 910 km² with water, §5) spans more than the test map, so it will need its own, larger bounds** (set 2026-11-10 for the terrain: ±18 km east-west, ±21 km north-south).
     - _To recheck on the dedicated server:_ Iris warns that some engine parts load after it starts, which on the editor's program happens late; harmless here, since nothing of ours relies on it.
  6. **Where: free options only.** The developer has no money for this (2026-11-08: "i dont have money").
     - **Stage 1, the developer's PC:** the server plus as many bots as the PC holds (a few dozen), run at several sizes (e.g. 25, 50, 75) to see how the server's cost grows with each player. Free, and it gives an early warning on its own. _Found 2026-11-08:_ bots running on the editor's program fit only about 8 at once; on the packaged game, about 20 with the editor open and 30 with it closed (point 3).
     - **First stage 1 runs (2026-11-09, Iris on, editor closed, the developer watching YouTube on the PC; 3 minutes each with every bot in):**

       | Bots | Updates/s | Slowest update | Time under 20/s | Sent per player | Server CPU | Server memory |
       |---|---|---|---|---|---|---|
       | 10 | 29.9 | 35 ms | 0% | 1.8 KB/s | 0.2 cores | 1.8 GB |
       | 15 | 30.0 | 35 ms | 0% | 1.9 KB/s | 0.2 cores | 1.8 GB |
       | 20 | 30.0 | 41 ms | 0% | 2.0 KB/s | 0.2 cores | 1.8 GB |

       _Reading:_ 20 players pass the bar easily. Data per player creeps up as the hotspot crowd grows (10 bots were in Hotspot1 at 20). **Gap found:** the server is capped at 30 updates a second and sleeps the rest of each update, so updates per second can't show how close it is to its limit, and the CPU figure is averaged over the whole run, startup included. The number that shows growth per player is **how busy the server's main thread is** (its share of each update's 33 ms); not measured yet. With 20 bots, 10.2 GB of memory was still free, so this PC fits about 40 bots with the editor closed.
     - **Stage 1 rerun with the cost numbers (2026-11-09, same setup, YouTube playing; 3 minutes each with every bot in; half the bots crowd into Hotspot1):**

       | Bots | In Hotspot1 | Main thread busy | Server CPU | Updates/s | Slowest update | Time under 20/s | Sent per player |
       |---|---|---|---|---|---|---|---|
       | 0 | 0 | ~4% | 0.06 cores | 30 | | | |
       | 10 | 5 | 9.1% | 0.14 cores | 29.9 | 35 ms | 0% | 1.8 KB/s |
       | 20 | 10 | 13.8% | 0.19 cores | 29.9 | 37 ms | 0% | 2.1 KB/s |
       | 30 | 15 | 23.5% | 0.30 cores | 29.9 | 48 ms | 0% | 2.3 KB/s |
       | 40 | 20 | 46.0% | 0.56 cores | 29.9 | 71 ms | 0.1% | 2.5 KB/s |

       _Reading:_ **the cost grows faster than the player count**: each extra 10 bots added about 5, then 10, then 22 points. That fits the hotspot crowd, where every player near another adds work for both, so the cost goes roughly with the crowd size squared. If that holds, **one crowd of about 30 in the same spot would fill the main thread on its own**, well short of the plan's 20–50 per hotspot and the 300 target. _Caveats:_ the bots run on the same PC as the server (40 bots use about 10 of its 20 CPU threads, plus YouTube), the server is the editor's program rather than a packaged dedicated server, and the bots crowd harder than real players (they push through 10–15 m alleys). So the real numbers will be better, but probably not enough to dismiss this. _Not known yet:_ what the work is, for example the characters' movement and collisions with each other, or Iris deciding what each player gets. Finding out needs a profile of a crowded run (Unreal Insights). Memory: 5 GB was still free with 40 bots.
     - **Profile of the 40-bot run (2026-11-09, Unreal Insights, about 100 s with every bot in; main thread 44% busy, matching the run without the profiler).** Where the main thread's time went, as a share of each update:
       - **Handling incoming player moves, about 16%:** each player sends about 30 moves a second and the server re-runs each one (collision sweeps, floor checks) to check it. Normal Character Movement work, grows with players.
       - **Animating the characters, about 7%:** the server plays every character's walk/run animation and moves each one's ~20 body-part collision shapes to match. Nobody sees it on a server.
       - **Physics bookkeeping, about 8%:** mostly syncing those same body-part shapes (2.8 million updates in 100 s).
       - **Sending updates (Iris), about 10%:** deciding what each player gets and writing it. The part that grows with crowds.
       - **The camera arm, about 1%:** the third-person camera boom ticks on the server too.
       - _Reading:_ about 15% of the 44% is animation and its body shapes, which a server only needs if it checks hits against body parts. One profile can't show which part grows faster than the player count; the next runs (with the cost numbers) will.
       - **Decided: the server skips character animation, the body-part shapes and the camera arm** (the developer, 2026-11-09: "Yes, turn it off", on Claude's suggestion). Only on dedicated servers; players still see full animation. _Open for the shooting pass:_ whether hit checks need body-part shapes on the server (e.g. headshots against the head's shape) or simpler hit zones; if they do, they come back and their cost is measured. _Not chosen:_ keeping them on to test the worst case.
       - **Rerun with animation off on the server (2026-11-09, same setup; a 4-bot profiled check first confirmed animation, body shapes and camera arm are gone from the server):**

         | Bots | In Hotspot1 | Main thread busy (before → after) | Server CPU | Updates/s | Slowest update | Sent per player |
         |---|---|---|---|---|---|---|
         | 10 | 5 | 9.1% → 6.2% | 0.10 cores | 29.9 | 85 ms | 1.8 KB/s |
         | 20 | 10 | 13.8% → 8.4% | 0.12 cores | 30.0 | 35 ms | 2.0 KB/s |
         | 30 | 15 | 23.5% → 14.0% | 0.18 cores | 29.9 | 41 ms | 2.3 KB/s |
         | 40 | 20 | 46.0% → **24.3%** | 0.31 cores | 29.9 | 58 ms | 2.5 KB/s |

         _Reading:_ the cost nearly halved, but it **still grows faster than the player count** (each 10 bots adds about 2, then 6, then 10 points). The 40-bot profile now: **sending updates (Iris) about 10%**, the largest part and unchanged by the fix; **receiving and checking player moves about 8%**; physics and everything else about 5%. One profile can't tell whether the crowd or the total player count drives the growth.
       - **Crowd or player count? (2026-11-09, 40 bots each, profiled):**

         | 40 bots, arranged as | Main thread busy | Iris (sending) | Receiving and checking moves |
         |---|---|---|---|
         | No crowd, all roaming | 17.0% | 6.6% | 5.5% |
         | Two crowds of 10 | 20.1% | 8.1% | 6.4% |
         | One crowd of 20 | 24.3% | 9.9% | 7.8% |

         _Reading:_ **both**. Every player costs about **0.33%** of the main thread on its own (an empty server about 4%), and crowds add on top roughly with their size squared, about **0.017% × (crowd size)²**: a crowd of 20 costs about four times a crowd of 10.
       - **Rough projection to 300 (this setup):** 300 players with 5 hotspots of 30 come to about **180%** of one main thread; 300 spread out with no crowds about **100%**; with no crowds about 290 would fit. **An early warning, not a verdict:** the server here is the editor's program in its development setup and shares the PC with the bots; a real dedicated server build (waiting on the engine source build) will be noticeably faster, but likely not 1.8×. So the per-player costs need cutting: Iris sending updates (the largest part) and checking moves.
       - **Real dedicated server (2026-11-10):** the packaged `NYZServer` built with the source engine, same PC, same bots (packaged game), 40-bot ramps. "Crowded" is the standard test (half the bots in Hotspot1, up to 20 there); "spread" is `-Crowd 0` (everyone roaming); zombies are 10 spawned around each player.

         | Bots | Arranged | Zombies (awake) | Main thread busy | Server CPU | Slowest update | Sent per player | Server memory |
         |---|---|---|---|---|---|---|---|
         | 10 | crowded | 0 | 5.4% | 0.07 cores | 35 ms | 1.8 KB/s | 0.5 GB |
         | 20 | crowded | 0 | 7.2% | 0.09 cores | 36 ms | 2.1 KB/s | 0.5 GB |
         | 30 | crowded | 0 | 10.1% | 0.12 cores | 35 ms | 2.3 KB/s | 0.5 GB |
         | 40 | crowded | 0 | **14.2%** (editor program: 23.3%) | 0.16 cores | 35 ms | 2.6 KB/s | 0.5 GB (editor program: 1.9) |
         | 20 | spread | 0 | 7.2% | 0.09 cores | 36 ms | 1.6 KB/s | 0.5 GB |
         | 40 | spread | 0 | 13.7% | 0.17 cores | 36 ms | 1.6 KB/s | 0.5 GB |
         | 10 | crowded | 100 (100) | 9.2% | 0.11 cores | 35 ms | 4.4 KB/s | 0.6 GB |
         | 20 | crowded | 200 (174) | 16.1% | 0.19 cores | 35 ms | 6.8 KB/s | 0.6 GB |
         | 30 | crowded | 300 (243) | 30.1% | 0.35 cores | 37 ms | 9.8 KB/s | 0.6 GB |
         | 40 | crowded | 400 (317) | **58.3%** | 0.63 cores | 47 ms | 11.8 KB/s | 0.6 GB |
         | 20 | spread | 200 (200) | 14.6% | 0.17 cores | 35 ms | 2.6 KB/s | 0.6 GB |
         | 40 | spread | 400 (351) | **36.8%** | 0.40 cores | 35 ms | 2.6 KB/s | 0.6 GB |

         _Reading:_ **the real server costs about 40% less than the editor program** and a quarter of its memory; 30 updates a second throughout. **Without zombies, crowding hardly matters any more** (13.7% spread against 14.2% crowded at 40): each player costs about **0.33%** of the main thread, an empty server under 1%. So **300 players come to about 100% of one main thread on this PC**, at the limit, whether crowded or spread (bots running on the same PC may inflate this). **Zombies are now the big cost:** each awake zombie costs about 0.04% at 20 players and 0.07% at 40 when spread, and about 0.14% at 40 when crowded; the cost per zombie grows with the player count even spread out (cause not yet profiled) and crowding doubles it. Ten naive zombies per player can't scale to 300 players: confirms the zombie pass needs a lighter system or cheaper sending (§3, point 4). Server memory barely moves with players or zombies (the map is what will count). Spread-out runs were added on the developer's question about how far players will spread (§5).
       - **Faster test (Claude's call, after the developer: "each one of these is costing a lot of time"):** `run_bots.ps1 -Count 40 -Step 10` ramps one server from 10 to 40 bots, measuring each size for 1 minute (the 10 s readings vary by only about ±1 point, so 1 minute gives the same answer as 3), and stops itself with a line per size. It matched the separate runs (6.1, 8.5, 13.9, 23.1% against 6.2, 8.4, 14.0, 24.3%) in **4.8 minutes instead of about 16**. Packaging takes about 40 seconds after the first time.
       - **Three quick cost cuts tried and dropped (2026-11-09, 40 bots, half in one crowd; the developer: "okay lets cut character cost down"):** baseline 23.3% of the main thread; **moves sent at 20 a second instead of 30–45:** 23.5%; **Iris range checks by grid cell instead of exact distance:** 24.4%; **characters sent 20 times a second instead of 30:** 23.9%. Readings vary by about ±1 point, so none saved anything measurable, and **none were kept** (each would have cost a little quality). _Reading:_ the cost is the fixed work per player (handling each incoming packet, Iris's per-connection bookkeeping every update, re-running movement), not how often things are sent. _Also found:_ Unreal's default lets a fast PC send up to 45 moves a second once a server has more than 10 players; our bots send 30, so real players may cost a bit more than the test shows.
       - **Profiling is built into the test script:** `run_bots.ps1 -Count N -Profile` records `Saved/LoadTest/Server.utrace`. Ranked list without opening Insights: `UnrealInsights.exe -OpenTraceFile=<trace> -NoUI -AutoQuit -ExecOnAnalysisCompleteCmd="TimingInsights.ExportTimerStatistics <out.csv> -threads=GameThread -startTime=<s>"`.
     - **Stage 2, the full 300 and 500:** decided when we get there, from free options: **free trial credit** that cloud providers give new accounts (enough for a few hours of test; they usually want a card on file to verify the account, and the terms need checking at the time), or **friends' PCs** each running a few dozen bots. Nothing gets rented without the developer's OK.
     - _Original proposal (changed for money):_ a few hours on paid rented cloud machines, with the server on the kind of machine a real host would rent.
  7. **If it fails:** decide with the numbers in hand (lower player cap, smarter culling, or splitting the map). Nothing decided in advance.
  8. **Also measured:** bandwidth per player and CPU cores per server, for a rough hosting cost per server per month (feeds the business model).
     - **Every run measures the server's real cost** (the developer, 2026-11-09: "include that test everytime. time is money"): how busy its main thread is (its share of each 33 ms update) and the CPU of all its threads, averaged over the same 10 s windows. Updates per second alone can't show cost, because the server is capped at 30 and sleeps out the rest of each update; the first stage 1 runs had to be redone for this. Built into the server's log line and the `-Stop` summary, which refuses to report a run without them. An empty server: main thread about 4% busy, 0.06 cores.
     - **How it's measured (built 2026-11-08, Claude's call):** on the test server, the game mode logs a line every 10 s: players, updates per second, its slowest update, the share of time under 20 a second (the pass bar), and data sent in total and per player. Stopping a test (`run_bots.ps1 -Stop`) sums up the 10 s windows that had every bot in, adds the server's CPU (cores, averaged over the run) and peak memory, prints one line and adds it to `Saved/LoadTest/results.txt`, so runs at different sizes sit side by side. _Why:_ the lines survive the server being stopped and can be watched live in the server's window. _Not chosen for now:_ Unreal's CSV profiler and Unreal Insights, which record far more detail; they're for finding out *why* the server is slow, once a run shows it is.
     - **Baseline without Iris (2026-11-08, 10 bots, the old replication system):** 30 updates a second, about 2.3 KB/s sent per player, 0.2 CPU cores, 1.7 GB for the server.
     - **Found 2026-11-08: Windows 11 slowed the test server.** After about 50 seconds the server dropped from 30 to a steady 21.5 updates a second, with no slow update: Windows 11 coarsens the timer of programs it decides are out of view, so each update waited for its next 15.6 ms tick. Reproduced with the server's window minimized. Fix: the test server and bots opt out of Windows' power throttling at startup (a standard Windows setting; Linux servers don't have this). _Lesson:_ numbers from the developer's PC are also affected by whatever else the PC is doing, so stage 1 runs are best done with the PC otherwise idle.

---

## Systems to design

Each system gets its own section once we design it. Add or remove items as needed.
Ticked = fully designed, nothing left open. Unticked but "decided" = the system is set, with open items still listed in its section.

- [ ] Zombies: decided (§8); open items listed there
- [x] Player survival stats: decided (§7); zombie infection in §8
- [ ] Lore: paused (§23, [lore bible](lore/LORE.md)); to be revisited in full later in development
- [ ] Loot & items: decided (§12); open items listed there
- [ ] Weapons & attachments: decided (§13); open items listed there
- [ ] Inventory: decided (§11); open items listed there
- [ ] Crafting: decided (§14); open items listed there
- [ ] Farming, fishing & food sources: decided (§22); open items listed there
- [x] Wildlife & hunting: decided (§22)
- [ ] Base building & raiding: decided (§9); open items listed there
- [ ] Clans: decided (§15); open items listed there
- [ ] PvP rules: decided (§17); open items listed there
- [ ] Map & world: setting and scale decided, border at draft v2 (§5); regions and points of interest still to do
- [ ] City buildings: NYC's official 3D models made game-ready by a procedural tool (textures, selectable interiors, hand control per building); direction set 2026-11-10 (§5), design pass when building starts; fit with §9's shared grid open
- [ ] Character progression / skills: in progress (§6)
- [ ] Vehicles, boats & helicopters: decided (§16); open items listed there
- [ ] Weather, day/night & seasons: decided (§19); open items listed there
- [ ] Trading, economy & safe zones: decided (§18); open items listed there
- [ ] Servers: persistence, wipes & admin: decided (§20); open items listed there
- [ ] Death & respawn: decided (§6, §10); open items listed in §10
- [ ] Character creation: decided (§21); open items listed there

---

## Maybe later (parked ideas)

Ideas the developer likes but that aren't planned for now. Each notes why it's parked.

- **Visible handedness and intentional off-hand aiming.** Left-handed characters visibly hold weapons left-handed, and any player can deliberately switch to aiming off-hand as a tactic (e.g., around corners). _Parked because:_ it needs mirrored animations for every weapon, which is a lot more animation work. _Conflicts with:_ handedness being hidden from players (§7). If this is ever added, handedness stops being a secret.
- **A smaller piece cap for bases at chokepoints** (bridges, tunnels, subway entrances). _Parked because:_ the other chokepoint inconveniences (hordes, faster decay) may be enough. Revisit if clans lock down too many chokepoints.
- **Scars.** Serious wounds you survive leave visible scars until you die, a survival story told by your body (§21). _Parked because:_ nice to have, not a launch priority.
- **Fragile items in bags.** Glass bottles or scopes with heavy things on top could break when you fall or take a hit. _Parked because:_ it adds a punishment on top of packing. Revisit if packing feels too easy.

---

## Open questions

- Final game name? (NYZ is only the project codename.)
- Is border draft v2 final (§5)? Still needing a real road: across Pelham Bay Park, and Fort Wadsworth to the Verrazzano. Which roads?
- Exact land area of the map: needs coastline data. Current estimate in §5.
- **Terrain beyond the border as scenery?** (raised 2026-11-09; the developer: "not sure yet"). Whether players see real NYC/NJ land past the wall (as DayZ-style maps do) or the world ends at the border. It costs memory on players' PCs only; the server needs collision just inside the playable area. The old 40 km terrain (NYZv409) extends 3–6 km past the border to the west, north and east. Doesn't block the terrain work: the first terrain is cut to the border's rectangle, and an outer low-detail ring can be added later.
- Can one UE5 server process hold 300 players plus zombies? Answered only by the load test (§3).
- Which buildings are enterable? (NYC has about a million.) _How they're chosen is set (2026-11-10, §5): per building in the city-building tool, one at a time or many at once. Which ones is still open._ The test block's numbers (§24 milestone 1 point 2) say memory decides it: about 60 MB on the server per block with every floor enterable, so either a small share of the city gets full interiors or the server loads only areas near players.
- Skill journal details: see §6 Open items.
- Target zombie count per server?
- Business model: buy-to-play, free, other?
