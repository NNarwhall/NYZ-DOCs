# Decision Log

Every design decision, newest at the bottom. Don't delete entries. When a decision changes, add a new entry that names the old one.

Format: **Decision**: why. _Rejected: alternatives considered._

---

## 2026-10-27: Fundamentals

- **Engine: Unreal Engine 5.** The developer's choice.
- **Team: solo for now, open to unpaid volunteers** who share the vision and are committed to it.
- **100+ players per server.** Requires dedicated, server-authoritative servers and a scalable replication setup (see GDD §3).
- **First and third person, switchable like DayZ.**
- **PC first, consoles later.** Consoles are a goal, not a launch target.

## 2026-10-27: Core vision

- **Design principle: easy to learn.** It should be enjoyable for an average player. Zomboid's long learning curve is what we avoid.
- **From DayZ:** open world, engaging PvP, gear looted from the world.
- **From Project Zomboid:** survival simulation, but less deep than Zomboid; zombie horde behavior.
- **From Ark:** leveling/skill system whose progress can be lost on death but recovered; base building; clans; crafting.
- **Other features** may blend mechanics from several games.
- **NYZ ("New York Z") is the project codename**, not the final game name.

## 2026-10-27: Death & skill recovery

- **On death, everything is lost** (levels and learned skills) until the skill journal is found.
- **Recovery = catch-up XP boost + skill journal.** _Not chosen: corpse recovery (XP left on your body), which lets other players camp the body._
- **The journal restores 60–80% of player level and 100% of learned skills**, including skills learned above the restored level.
- **Journals can be buried** so others rarely find them.

## 2026-10-27: Skill journal details

- **Restore numbers are placeholders** (60–80%, the 80 → 55 example). The system is what's decided: learned skills are kept in full, and new learning follows the restored level.
- **The journal is a snapshot** of progress as of the last time it was written in.
- **Multiple journals allowed.** _Not chosen: one active journal (suggested to stop players burying many copies). Snapshots already limit the value of extra copies, because each one needs updating._
- **Owner-only reading, anyone can destroy:** tentative, may revisit.
- **Catch-up boost applies from level 1**, before the journal is found.
- **Burying:** with a shovel, on diggable ground (dirt, soil).

## 2026-10-27: Survival stats

- **Five always-shown stats:** health, food, water, stamina, body temperature.
- **Conditions that only appear when you have them:** bleeding, broken leg, wound infection, sickness, cold, unconscious. Zombie infection is decided with zombies.
- **Knock-outs: yes.** Unconscious players can be restrained or robbed.
- **NYC water is a survival problem:** the rivers can't be drunk, fresh water is limited, and dirty water must be boiled or purified.
- **Mood (stress, boredom, happiness): in**, but with far slower drain and many more cures than Zomboid. Never a 24/7 state.
- **Nutrients: in**, less critical than in Zomboid.
- **Cut:** sleep/fatigue (entirely), panic.

## 2026-10-27: Mood, nutrients, body parts, water

- **Mood system adopted as proposed** (GDD §7): shows only when getting bad, takes hours of neglect, and being near clanmates reduces stress and boredom.
- **Nutrients adopted as proposed**: calories plus three background food groups, a single "Well fed" / "Poor diet" status, never lethal, no vomiting from overeating. **Added:** a deeper diet menu showing which group is missing.
- **Separate health per body part: in.** It's deep, but a good UI makes it easy for new players. _Rejected: cutting it as too Zomboid-deep._
- **Body weight: cut.**
- **Rooftop water towers** replace "taps work for a while early on", which has no clear meaning on a persistent server.

## 2026-10-27: Body-part health details and handedness

- **Body-part health adopted as proposed** (GDD §7): six parts; head or torso at zero means death; destroyed limbs fixed with a surgery kit; conditions belong to a part; colored body outline on the HUD; one-click Treat button.
- **"Broken leg" became "Broken limb"**, covering arms and legs.
- **Broken arm:** no proper aiming with rifles or two-handed weapons, but pistols can be aimed one-handed with the good arm. _Changed from the proposal, which blocked proper aiming with all weapons._
- **Handedness (left/right) chosen at character creation.** Players aren't told why it matters and discover it when it comes up.

## 2026-10-27: Hip fire and handedness effects

- **Rifles with a broken arm: hip fire only**, no aiming down the sights.
- **Handedness is gameplay only, for now.** Penalties depend on which arm is hurt, with a first-time hint when it first matters. _Not chosen for now:_ mirrored animations for every weapon (doubles the animation work).
- **Parked in the GDD's "Maybe later" section:** visible handedness and intentional off-hand aiming as a tactic. The developer likes it, but it costs a lot of animation work.

## 2026-10-27: Zombies

- **Several speeds by freshness:** fresh zombies move between a walk and a run; decayed ones shamble. _Changed from the proposal, which had fresh zombies running at full speed._
- **Variants by what they were** (civilian, police, firefighter, military, hospital staff), with toughness and loot matching their clothing.
- **Special zombies: 1–2 types at most**, extremely rare, harder to kill but not overkill, can spawn at lore areas. _Changed from the proposal, which had none._
- **Hearing is the main sense; footwear changes footstep noise** (boots louder, sneakers quieter). _Added by the developer._ Sight is worse at night, in rain and in fog.
- **Hordes as proposed:** drawn by noise, migrate across the city, cleared areas refill slowly; bridges, tunnels and subways matter.
- **Only head damage kills**; destroyed legs make crawlers.
- **Infection:** bites high chance, scratches low, clothing can block it; cured only by a rare antiviral; dying of infection turns you into a zombie wearing your gear.
- **Bases:** noise attracts zombies; how much damage hordes do depends on the building-material tier (tier 1 falls easily; tier 4 resists small hordes completely, large hordes wear it down over time). Zombies can't climb ladders.
- **GDD layout:** the end sections (Systems to design, Maybe later, Open questions) no longer have numbers, so adding system sections doesn't break references.

## 2026-10-27: Footwear and fences

- **Footwear noise is heard by other players too**, not just zombies.
- **Boots protect more to balance being louder** (bites to legs and feet, warmth, durability). Sneakers are quiet but protect less and wear out faster.
- **Fences:** zombies hobble over low fences (waist-high or lower). Fences taller than a person stop them; they can only break through, following the base-material tier rules.

## 2026-10-27: Zombie speed tiers

- **Four tiers adopted as proposed:** Fresh (between a walk and a run), Weathered (walk), Decayed (shamble), Crawler.

## 2026-10-27: Base building & raiding

- **Both ways to build:** fortify existing buildings and build from scratch. The developer raised the extra modeling work of holes in decayed or bombed buildings. _Proposed fix, pending confirmation:_ the city kit and player pieces share one grid, so holes are patched with normal building pieces.
- **City buildings can't be destroyed**; only player-added pieces can.
- **Four material tiers** (wood → sheet metal → brick/concrete block → steel/reinforced concrete).
- **Building noise is moderate:** 1–2 city blocks outside or at a window/door, a muffled 1 block fully inside. _Changed from the proposal, which only said "building is loud."_
- **Claim item, decay when unvisited, piece cap per clan.** The cap mustn't feel limiting.
- **Raiding must never be easy:** raid tools and explosives are hard to find. Raiding is loud and attracts hordes.
- **Offline raid protection by default**, with a server setting for no protection or raid hours.
- **Code locks**, with automatic clan access.
- **No building at player spawns. Chokepoints allowed with major inconveniences.** _Changed from the proposal, which banned building at chokepoints; the developer likes clans being able to hold them, as long as not every clan does._
- **Loot hotspots: undecided.** Either no building, or building allowed with loot respawns blocked near active structures.

## 2026-10-27: Grid, chokepoints, loot hotspots

- **Shared grid confirmed, "to a degree":** outside assets (e.g., Fab) must still be addable. Suggested method: only structural pieces follow the grid; outside assets are either fitted to it or used as non-claimable buildings and props.
- **Chokepoints:** hordes travel through them, and bases there decay faster. **Claiming and storage are allowed.** _Rejected: no claim or storage at chokepoints. If players build somewhere dangerous, they hold it or pay the price._ A smaller piece cap is parked as "maybe later."
- **Major loot hotspots: no building. Smaller ones (small hospitals, clinics, schools): building allowed**, but loot doesn't respawn inside the claimed base's area, and only there. _Rejected: blocking loot respawns in the whole surrounding area, which loose pieces could abuse to grief._

## 2026-10-27: Noise distances

- **Building noise distances will be set in meters during map development**, not as a fixed "1 block = 100 m". Real NYC blocks vary, and streets and terrain aim for 1:1. _Not chosen: 1 block = 100 m._

## 2026-10-27: Death & respawn

- **Fresh spawns:** pick a borough and a neighborhood; random points spread through it. Only a few select spawn neighborhoods; high-loot neighborhoods are never spawns. _Changed from the proposal, which only picked a borough._
- **Sleeping bags** (cheap, long cooldown) **can't be placed within X distance of another clan's claimed base.** _Added by the developer._ **Beds** (expensive, short cooldown). Both shareable with clanmates.
- **Bodies are lootable by anyone** and stay about 30 minutes. **A body may turn into a zombie depending on how you died**, not instantly, and then wanders off with your gear. _Added by the developer._
- **Starting kit:** basic clothes, bandage, snack, flashlight. _Rejected: a MetroCard joke item, since MetroCards have been phased out._
- **Respawn at level 1** with the catch-up boost until the journal is found.
- **Logout: DayZ-style, 30-second timer**, longer after a fight. _Rejected: Rust-style sleepers, which clash with offline raid protection._
- **Spawn protection: extremely minimal**, only covering the black-screen loading moment.

## 2026-10-27: Turning rules

- **A body turns if the player was infected at death**, whatever killed them. A head hit always prevents turning. Lore will be fitted around this.
- **Turning time: random 30–60 minutes**, so players have a real chance of reaching their body on a 1:1 map. _Changed from the proposal of 3–10 minutes._

## 2026-10-27: Skills & progression

- **XP from doing things** (zombies, crafting, building, healing, exploring, surviving). **Level cap 100** (placeholder).
- **Two point types per level, mapped from Ark:** stat points become **skill points** (spent on abilities), and engram points become **recipe points** (spent on crafting recipes). _Changed from the proposal, which had a single pool of learning points._
- **No raw stat points** (health, stamina, carry weight).
- **You can't learn everything**, so players specialize and clans split roles.
- **Re-spending points is possible**, by a method the developer will define. _Rejected: a found "Life Lessons" book._
- The journal restores 100% of both skills and recipes.

## 2026-10-27: Body timer and launch map

- **Bodies that don't turn stay 2 hours.** Getting back is hard on a 1:1 map, and games like Ark give a lot of time. _Changed from 30 minutes; 60 minutes was also suggested._
- **Launch map area outlined in Google Earth:** 782.59 km² including water, 105.69 km perimeter (screenshot in `docs/images/`). It looks like Manhattan, the Bronx, Brooklyn, Queens, a NJ strip along the Hudson and western Nassau, without Staten Island. Exact contents still to be confirmed. "Manhattan map" in chat was a slip.

## 2026-10-27: Map border

- **The Google Earth outline is a rough estimate only**, not the launch layout. _Corrects the entry above._
- **New Jersey is included**, but not necessarily all of the sketched part.
- **The map's land edges are a quarantine wall that follows major highways or major streets**, so the border makes sense in-world.
- **Planned method:** build the border from OpenStreetMap road data, save it as KML/GeoJSON, review it on a preview map.

## 2026-10-27: Border draft v1 and Staten Island

- **Border draft v1 built** from OpenStreetMap: Cross County Parkway, Hutchinson River Parkway, Cross Island Parkway, Staten Island Expressway, Clove Road, New Jersey Turnpike, with water stretches in between. About 1,000 km² including water. Four land stretches are still placeholders (GDD §5).
- **Staten Island: only a few square miles, not the whole island.** _Changed from the suggestion to leave it out at launch._ The Verrazzano Bridge stays intact for now; a boat from Manhattan is the faster way there.

## 2026-10-27: Border review round 1

- **Staten Island piece from draft v1 is kept** (about 8.6 sq mi including edge water).
- **The George Washington Bridge stays crossable**; the border must not run along it.
- **New Jersey gets cut back** to the developer's drawn line (Palisades towns, Weehawken, Hoboken, Jersey City, Bayonne). Details in `docs/map/border-notes.md`.
- **Border changes are batched**: collected in `docs/map/border-notes.md` and applied together, not one at a time.

## 2026-10-27: Border draft v2

- **NJ wall:** Pulaski Skyway → Tonnelle Ave → Broad Ave → Grand Ave → Fort Lee Rd → US 1-9 to the GWB. The developer named Grand, Broad and Tonnelle; the stretch from Tonnelle to the Hackensack had no road in their drawing ("fill in, main roads preferred"), and became the Pulaski Skyway.
- **Breezy Point included.**
- **North Bronx:** roughly the city line via East 233rd St and the Hutch. Yonkers, Mount Vernon and Pelham are out; Co-op City and Bay Plaza are in. The developer's line didn't trace roads, so connectors are accepted there.
- **East Queens:** Clearview Expressway → Francis Lewis Blvd → Springfield Blvd → Rockaway Blvd along JFK, then Head of Bay and Beach 9th St. Throgs Neck and Whitestone bridges, their highways, JFK and the whole Rockaway peninsula are in. _Rejected: keeping the Cross Island Parkway line (too much of Queens)._
- **New border kind, "connector":** a land stretch without a road, accepted by the developer, as opposed to a "placeholder" that still needs a road.
- Result: about 910 km² including water (v1: about 1,000 km²).

## 2026-10-27: Player count raised

- **250–300 players per server at launch; up to 500 later if the budget allows.** _Changes the fundamental "100+ players per server" (entry of 2026-10-27, Fundamentals)._ Why: 100 players would feel like a ghost town on about 680 km² of land; 250–300 gives 1.4–1.6× DayZ's player density.
- Consequences: the load test targets 300; the player cap is a server setting; going past one server process (splitting the map across servers) is the fallback if one process can't hold it.

## 2026-10-27: Setting

- **New York City, real city, 1:1 in size.** Layout and size match; individual buildings and details don't have to.
- **Wider New York State: possible DLC.**
- **Which parts of NYC are in the game:** deferred until after the core gameplay systems.

## 2026-10-27: Map area no longer deferred

- **Which parts of NYC are in the game is now set by the border drafts**, currently draft v2 (GDD §5). _Supersedes the "deferred until after the core gameplay systems" line in the Setting entry above._ Why: the border work went ahead (drafts v1 and v2, entries above), so the deferral no longer holds. Only the two placeholders are still open.

## 2026-10-27: Inventory basis

- **Inventory starts from DayZ's grid system, with a grid for each piece of clothing**, upgraded so players don't see it as a DayZ copy. The developer's choice. Upgrades still being designed (GDD §11).

## 2026-10-27: Inventory upgrades

- **Adopted as proposed** (GDD §11): reach zones (hands, quick reach, pack), rattle from loosely packed hard items, hidden pockets, NYC carry gear (shopping carts and rolling suitcases, straps on big backpacks, dry bags), auto-arrange, one-press quick move, controller support from day one. Why: makes packing a choice that matters, ties the inventory to hearing (§8) and knock-outs (§7), and keeps it easy to learn.
- **Weight stays DayZ-style:** total weight affects stamina, nothing finer.
- **The skill journal is waterproof**, so water never becomes a new way to lose progress.
- **Physical side-view packing for bags:** the developer's idea, under discussion. It would replace the grid for bags.

## 2026-10-27: Cutaway packing for bags

- **Bags use physical side-view packing instead of a grid** (GDD §11). Clothing pockets keep their grids. _Changes the inventory basis (entry "Inventory basis" above), which gave each bag a grid too._ Why: the developer's idea, liked after trying a demo; it makes the inventory clearly NYZ's own. The developer chose to commit to it without a playtest round first.
- **How it works:** each bag type has its own outline; items keep their side profile and stand up or lie on their side; they fall straight down, with an outline showing where they'll land; soft items fill the gaps; pack order sets how long it takes to dig an item out; packing past the zip line stops the bag closing; players choose between Toss in, repacking by hand and Auto-pack.
- **Rule: packing by hand is a bonus, never a requirement.** Auto-pack gets about 90% of the way.
- **Bags can stretch a little but wear faster** (the developer's idea). Worn-out bags rip until sewn; rigid bags don't stretch; the stretch is visible.
- **Rattle now comes from empty space** beside hard items; soft items stuffed into the gaps quiet them.
- _Rejected: tumbling physics (chaotic, hard to keep in sync with the server); heavy items high in the pack draining more stamina (too much for "easy to learn"). Parked in "Maybe later": fragile items._

## 2026-10-27: Pocket tabs and weapon slings

- **Pocket tabs:** a small tab switches the bag view to a smaller pocket, hiding the main compartment and its contents. The developer's idea.
- **Slings on bags for primary weapons** (crowbar, bat, rifle, etc.); better bags have 2 or more. The developer's idea. The bat moves from backpack straps to slings; straps keep bulky gear.
- Open: whether a character without a bag can still sling a weapon.

## 2026-10-27: Body sling and the bat

- **Every character has one body sling** over the shoulder, with or without a bag; bags add their slings on top. _Answers the open item in the entry above._ Why: the starting kit has no bag (GDD §10), and a fresh spawn should still be able to carry a second weapon.
- **The bat is both bulky gear and a sling item:** straps or sling. _Reverses "the bat moves from backpack straps to slings" in the entry above._ The developer's choice.
- **Inside or outside:** a long or bulky item that fits can be shoved into the bag; if it doesn't fit, it still has a place on the outside.

## 2026-10-27: Loot & items

- **Hotbar (keys 1–0) stays** in the inventory system, pulling from quick reach.
- **Item condition: 4 color-coded levels** (Pristine, Worn, Damaged, Ruined); repair kits never restore to Pristine.
- **Loot by building type**, DayZ-style. **Guns come mainly from police and military**, plus **very rare finds in homes, more often in higher-crime neighborhoods** than in, e.g., Manhattan. _Added by the developer._ Exact rates TBD.
- **Loot tiers by area** (low near spawns; high in Manhattan's core, military sites and the boat-only islands) and a **DayZ-style central economy** for respawning.
- **Rarity: 5 tiers.** _Changed from the proposal's 4:_ a new top tier above "very rare" holds raid tools, explosives and the antiviral. Gun tiers separate rare from very rare.
- **Decay:** food rots, batteries run down, dropped items despawn.

## 2026-10-27: Weapons & attachments

- **Adopted as proposed** (GDD §13): five weapon families plus throwables; fictional gun names; noise makes melee and bows the main tools against zombies; melee with shove and stomp; magazines tied to reach zones with one-action refills; bullet drop but no wind; jams by condition; armor per body part; weapon skills stay non-combat (no damage or recoil skills); crafted pipe shotgun; condition and repair.
- **Vast gun selection and deep customization are core features.** _Changed from the proposal's lean setup:_ the developer wants many guns, even if rare. So **calibers go above the proposed ~6** (suggested 10–12 shared calibers, to confirm).
- **Attachments added by the developer:** a **ghillie wrap slot** on rifles, and **rail types that fit more** (e.g., two-sided versus one-sided rails, giving more slots).
- **Ammo crafting as an endgame recipe.** _Added by the developer._

## 2026-10-27: Gun roster review round 1

- **Roster grows to 56 guns** (draft v2, `docs/weapons/gun-roster.md`). The developer asked for 4 more pistols, 4 more revolvers, 3 more SMGs, 2 more shotguns, 2 more military sniper rifles and an AK-47; Claude picked the models, and any can be swapped. Adds two platforms (heavy pistol, single-action revolver) and one caliber (.300 Win Mag).
- **The machine gun (M249-style) and the .50 cal (Barrett-style) are in the top rarity tier**, with raid tools and explosives.
- **.357 guns also take .38 ammo.** Why: true to life, and the "fits:" tooltip keeps it easy to learn. _Not chosen: dropping it for simplicity._
- **Port container yards as the smuggled-gun source:** being explored, not decided.

## 2026-10-27: Port container yards and bolt cutters

- **Smuggled guns come mainly from a customs holding warehouse at the ports, sometimes from containers hidden among cargo** (found via shipping manifests). _Not chosen for now: the outbreak arriving by ship._ Answers the open item in the entry above.
- **All four ports are in:** Red Hook, South Brooklyn Marine Terminal, Port Jersey (Bayonne) and the Brooklyn Navy Yard. All checked inside border v2.
- **Bolt cutters are a rare tool** (not top tier) that opens containers, **with other uses to be designed**. _Added by the developer._

## 2026-10-27: Crafting

- **Three levels of stations** (by hand, workbench, specialty stations; some need generator power), as proposed.
- **Every real crafting recipe costs recipe points**; simple ones are very low level and cost. **Everyday actions (boiling water, using a shirt as a bandage) need no recipe.** _Changed from the proposal, which gave a set of basic recipes free._
- **Materials:** about 12 core materials, maybe more later. Sources: taking things apart (including electronics like computers for scrap metal and electronics), **trees for wood** (parks), and **industrial and construction sites** for bricks, concrete, steel and welders. _Sources added by the developer._
- **Crafting pulls from storage within a few meters only at your base;** elsewhere only from your inventory and items on the ground right around you. _Changed from the proposal, which allowed nearby storage everywhere._
- **Crafts that could realistically be done while walking can be**; the rest need you to stand still. **Small recipes make no noise.** _Added by the developer._ Queues as proposed.
- Tool-based crafted condition plus the Craftsman skill; the promised items list (for now); clan crafting; farming as its own section later.
- **New characters start with 5–10 recipe points; basic recipes cost 1 point each.** Answers the open item about how a fresh spawn learns the basics.

## 2026-10-27: Clans

- **Clan cap: 10 by default, a server setting.** _Changed from the proposed 8._
- **No formal alliances for now; informal voice alliances are fine** and break no rules.
- **12-hour cooldown after leaving a clan.** _Changed from the proposed 24 hours._
- **Three fixed ranks** (Leader, Officer, Member) plus a few per-rank toggles.
- **Doors and storage get rank access levels:** clan-wide, or officer and above. _Added by the developer;_ refines "clanmates get access automatically" (Base building entry). **Clarified:** whoever sets a code lock (officer or leader) chooses whether everyone in the clan or only officers and above open it freely, without typing the code. Same for storage. The code itself still works for anyone who knows it.
- **Name tags only in line of sight** (may change); **clanmates' positions on the map**; minimap undecided. _Changed from tags-up-close-through-anything._
- Friendly fire on (server setting); proximity voice, walkie-talkies for range, clan text chat anywhere; graffiti tags; access ends instantly on leaving.
- **Solo play stays viable; stronger offline protection for solos is a maybe.**

## 2026-10-27: Vehicles, boats & helicopters

- **Jammed streets** (route planning; heavy vehicles push small wrecks), as proposed.
- **Land vehicles as proposed, with several sedan and SUV types.** _Added by the developer._
- **Bike-share docks hold regular bikes and e-bikes;** bolt cutters free them.
- **Vehicles don't lock to you automatically;** locking takes a lock system you make or install. **Once hotwired, anyone can start a vehicle.** _Changed from the proposal's automatic owner lock._
- **Modern setting: modern cars are started through tech, not physical hotwiring:** an advanced OBD2 scanner makes keys, and a hacking device starts cars without a key. _Added by the developer._
- **DayZ-style parts** (battery, spark plug, radiator, tires, headlights, engine, fuel), **but parts are easier to find than in DayZ.** Cars should be hard to get. _Changed from the proposal's four parts._
- Fuel and siphoning, noise and car alarms, zombies vs vehicles, cutaway trunks: as proposed.
- **Extensive vehicle customization in tiers like building;** engine upgrades (mostly durability, some speed and power); **armor is the main show.** _Added by the developer._
- **More boats:** 10–20+ ft civilian boats from NYC's marinas, harder to repair. _Added by the developer._ Zombies don't swim; swimming is costly; Hell Gate currents stay a maybe.
- **Helicopters from launch, extremely rare and even harder to repair.** _Changed from the proposal to park them._ Why: the developer wants them from the start.
- Vehicle caps per server and per clan, and despawn for abandoned vehicles outside bases.

## 2026-10-27: Helicopter-only rooftop bases

- **Bases may be built on roofs that can't be reached on foot.** (See also the next entry.) _Rejected: Claude's suggested rule that a claimed roof must also be reachable by stairs._ Why: few roofs without a helipad have room to land, most roofs are cluttered and risky to land on, and a clan that loses its helicopter is stuck (it can only respawn up there).

## 2026-10-27: Vehicle details confirmed

- **Confirmed as suggested** (GDD §16): e-bike charging (generator, solar panels, power banks, from a running car, docks trickle-charging); keys and locks (physical hotwiring for older cars, key programmer plus blank fobs, very rare hacking device, key-cutting machine for copies, steering-wheel locks, immobilizers with alarms); car armor parts (window grates, ram plows, wheel guards, door plates, scrap-to-steel tiers, weight costs speed and fuel); civilian boat types (center-console, bowrider, cabin cruiser, pontoon, jet ski).
- **Working rule:** the GDD holds the agreed high-level design; each system gets a deeper design pass when building it starts (added to CLAUDE.md).

## 2026-10-27: PvP rules

- **Anyone, anywhere, anytime: full PvP and full loot everywhere.** _Not adopted: PvE or "PvP zones" server types._
- **Safe zones with trading NPCs where nobody can be hurt.** _Changed from "decide with trading": safe zones are decided; details come with trading._
- **Surrender, restrain and rob** as proposed, with a 10–15 minute struggle-free limit.
- **Combat logging: "quit to menu" is greyed out while in combat and for 5 minutes after, unless the damage came from a clanmate.** _Changed from the proposal's 2-minute logout timer._ **Confirmed:** only damage to or from other (non-clan) players counts as combat, not zombies; a force-quitting character stays in the world until the 5-minute combat timer runs out, plus the regular 30-second leave timer.
- No kill feed (death screen shows only the cause); no karma or bandit system; Easy Anti-Cheat.
- **First person: a server setting ("first person only" or "both"); official servers offer both.** Answers the open question in GDD §3.

## 2026-10-27: Trading, economy & safe zones

- **Currency: a standard replacement for the US dollar** (like modded DayZ's rubles), name TBD. _Rejected: cigarettes (Claude's pick), batteries, scrap metal._
- **One safe zone per borough, at a known location, but not Grand Central, Yankee Stadium, Barclays Center or Citi Field: those are for combat and bases.** _Rejected: Claude's four landmark safe zones._
- **Safe zone rules:** no damage inside; hostile marking for shooting near one; several exits; no building nearby. **Added by the developer: NPC snipers** watch for campers near the zone, fire a warning shot and a loudspeaker message, give 5 seconds to leave, then target the camper with elite (rarely missing) aim.
- **A limited bank in safe zones**, opened with a physical item linked to your character or clan account **plus a PIN**, with a storage limit. _Changed from the proposal's "no storage inside."_
- Traders by type, never selling the top tier, very rare items in tiny stock, supply-driven prices, valuables and the Diamond District, a secure trade window in safe zones, drop-trading outside, vending machines at bases, and trader services: all as proposed.

## 2026-10-27: Safe zone details and storage units

- **Currency name: an invented word, not a real one.** "Scrip" doubtful.
- **No famous places for safe zones at all.** _Rejected: Claude's lesser-landmark picks (the Intrepid, Kingsbridge Armory, Brooklyn Army Terminal, the national tennis center)._ Instead: **big warehouses** (distribution-center style, fictional brands) for the main traders, and **random tall buildings** with room and good sniping positions.
- **About 6–7 safe zones, including one in New Jersey.** _Changed from one per borough (4)._ Why: the map is too big for four.
- **Camping rule:** about 60 seconds inside a 100–150 m ring, faster when prone or aiming; nobody waiting innocently gets shot.
- **Replacement bank cards are expensive.** **Money is shared across all safe zones.**
- **Storage units at safe zones, about 50–100 lbs for a fee**, mainly for solo players. Items can only be taken out where they were stored. _Added by the developer._
- **The storage fee is rent** (recurring). _Not chosen: a one-time fee._
- **The Staten Island piece gets a small safe zone**, counted in the 6–7.

## 2026-10-27: Currency name shortlist

- **Leading candidate: "Sanctos Notes."** Still considered: **Boros**, **Quarants**. Not final.
- _Rejected:_ Zollars (the developer: it "sounds hella zesty"), Scrip.

## 2026-10-27: Weather, day/night & seasons

- **3 hours of day, 1 hour of night.** _Changed from the proposal's 3-hour full cycle._
- Zombies see worse at night; more roam at night; NVGs very rare. **Whether zombies are drawn to flashlights is undecided** (could make nights too hard; depends on lore). _(Now leaning yes: see "The safe-zone group, part 1".)_
- **Weather types as proposed, plus blizzard / heavy snowfall, rarer than snow.** _Added by the developer._
- **Seasons cycle** (about 1–2 real weeks each, a server setting).
- **Nor'easter and hurricane-with-flooding events are both in.** _Changed from the proposal, which had the hurricane as "maybe later."_
- **HUD shows only a general feel; a watch or thermometer gives exact time and temperature.** _Added by the developer._
- **Weather radio forecast questioned** ("who's broadcasting in an apocalypse?"); the forecast source is open.
- **Forecasts come from a barometer item and a safe-zone radio broadcast.** _Not chosen: automated airport/Central Park stations; no forecasts._ Answers the open item above.

## 2026-10-27: Servers: persistence, wipes & admin

- **Official servers wipe every 6 months to a year**; may change after release based on feedback. Why: progress shouldn't feel like it was for nothing. _Rejected: Claude's pick of one wipe per in-game year (every 1–2 months); never wiping._ Answers the open question "permanent world or scheduled wipes?"
- **A wipe clears bases, items, vehicles, bank, storage units, levels and recipes; it keeps appearance, clan name and tag, stats and achievements.**
- **One server per character** (no shared hive); restarts every 6–12 hours, not counted as combat logging; continuous saving with seconds-to-a-minute crash rollback.
- **Unused world vehicles relocate:** each has a radius (a few blocks) and a timer; if no player enters the radius in time, it respawns elsewhere. _Added by the developer._
- **Storage units are a service in the safe-zone building, not a room you can live in.** _Clarified by the developer._
- Official and community servers (community servers can change settings, including the wipe interval); mod support later; one documented server settings file; admin tools (kick/ban, spectate, logs, item spawner).

## 2026-10-27: Character creation

- **Adopted as proposed** (GDD §21): appearance from presets plus a few sliders (kept through wipes), handedness, a name visible only to clanmates, a choice of starting outfit style.
- **Occupations** (NYC jobs) give a couple of free recipes or skills and one small starting item, never combat bonuses, and are re-picked each new life. What each gives will be refined later.
- **No separate traits system: the occupation's skill is the character's "trait."** _Refined by the developer._
- **Scars parked in "Maybe later."**

## 2026-10-27: Farming, fishing and the overgrown city

- **Farming adopted as proposed** (GDD §22): in diggable ground or in crafted planters (rooftops), about 8 crops tied to the food groups, seeds from loot and harvests, plant-water-harvest with status icons, real-time growth while offline, **compost** from rotten food, seasons with winter frost, greenhouses and endgame grow lights, crop theft and trampling, a small mood bonus, chickens, and crops counting toward the piece cap.
- **Fishing: yes.** Details to design.
- **Setting: an overgrown, beaten-down NYC where wild animals have come back**, including animals from the north. _Added by the developer._ Implies the outbreak was years ago (a lore question).
- **Hunting: under consideration**, tied to the returning wildlife.

## 2026-10-27: Wildlife and hunting

- **Hunting: yes**, with the proposed animals (GDD §22). Prey: deer, wild turkeys, geese and ducks, rabbits, pigeons and rats. Dangers: feral dog packs, coyotes, black bears and bobcats from the north. Bows are the hunter's weapon; tracking via snow footprints and blood trails.
- **No zombie animals.**
- **Seals in the harbor and a beaver in the Bronx River as rare sightings.** _The developer's call: keep them._

## 2026-10-27: Lore foundations

- **Origin: it came from outside, plus a mystery or twist (B + C).** The whole world has fallen, with pockets of survivors elsewhere; most people inside don't know what's happening outside. Direction: researchers came to NYC to study it, the city was walled off and held well, then it spread inside the walls because of the research. _Rejected as the main origin: a lab accident that started in the city (A); Claude's pick was C leaning A._
- **Deep lore, no cutscenes**: clues in the world and **random** radio broadcasts (Zomboid-style, adapted to starting years after day 0).
- **Build the deep lore before development gets far**, because it has a big impact on the rest. The lore gets its own document: `docs/lore/LORE.md`. _Changed 2026-11-08: development starts first, and the lore gets revisited in full later in development (entry "Development starts; lore paused")._
- **Decide the origin before the timeline and the wall** (the developer's ordering), since both follow from it.

## 2026-10-27: The lore twist

- **Chosen layers of the truth** (details in `docs/lore/LORE.md`, kept out of the GDD on purpose): the wall was never meant to keep the outbreak out, and the people inside were unknowing study subjects; the breach inside the walls wasn't an accident; the safe-zone group's founders came out of the research program; the special zombies are the original test subjects.
- _Not chosen:_ "the research wasn't for a cure" and "the outside world isn't what the radio suggests." Claude's pick was layers 1, 4 and 5; the developer added layer 3.
- **The study was genuinely to find a mass-producible cure. The existing cure is extremely hard to produce from its known materials** (why the antiviral is rare). **The researchers had good intentions; something made them flip.** _Added by the developer._ What flipped them is open.
- **The flip, as a chain:** the world went dark → they ran out of test subjects (infected from nearby towns already used up; expeditions outside the locked-down city too risky) → a small controlled release inside the walls, which got away. The release site was chosen for practical reasons (population, ease of sealing off), never by who lives there. _Changed from Claude's "many infected hosts" version of step 2._ The developer finds the chain a bit predictable; ways to subvert it are open.
- **The turn: the release worked.** A scalable cure method was found, but it needs living infected hosts (B1). A researcher who saw the price **split the method apart and partially destroyed it** (B4, _modified by the developer from "split and hidden across the city"_). The researcher died or turned (possibly a Patient); the founders still want the method. Players move through three layers: lab accident → "it got away" → "it worked." _Not chosen: the method held as leverage (B2), a lost courier (B3), sabotaged containment (A)._ _(The split-and-destroy part changed on 2026-10-27, new chat: the method was already in parts, the founders voted to cover it up, and one founder hid his part. See "The safe-zone group, part 1". Later the same day: the founders are gone, and no one wants the method at release; see "The Breach, the founders' fates, the Force's secret".)_
- **The process survived; multiple key formulas and some ingredients are missing.** _Changed from Claude's "the process survived, one key formula destroyed."_
- **Whether it can ever be rebuilt is left open on purpose.**
- **The deepest secrets must be hidden so well that finding them could take months to years after release, with nothing obvious in the game files** (players will datamine). _The developer's requirement._ Suggested technique: keep the deepest content server-side, neutral names, encrypted text, clue chains needing in-game actions, time-gated reveals. Where the surviving process is: TBD.
- **How residents were studied: the registry → health screenings and blood drives → quarantine wards** (e.g., North Brother Island). The founders' bank registry today mirrors the old registry. _Not chosen:_ "free immunizations" as the public face (the developer: not feeling it), trial compounds in rations. The water-supply false rumor is suggested, not confirmed.
- **The water-supply story is a rumor only (false).** _Confirmed._

## 2026-10-27: Special zombies

- **Two special types, both original test subjects, only at lore areas: the Patient and the Host** (GDD §8; backstory in the lore bible).
- **The Patient:** tougher, the only true runner, hospital gown and lootable wristband; **sometimes says a word or a sentence in English, then goes back to mumbling.** _Added by the developer._
- **The Host:** slow, very hard to kill, restraints and tubing; tied to the cure's price.
- **Both must look clearly different, e.g. mutated.** _Added by the developer._
- _Not chosen as specials:_ the Screamer and the Blind.

## 2026-10-27: The release as a staged breach

- **The release was a staged wall breach** at a small, deliberately lightly defended neighborhood on the border (NJ or the Bronx), letting in a small horde gathered in advance from test subjects and people taken for experiments. Only a few extra patrols beforehand, to avoid suspicion. **It went almost perfectly**: many in the neighborhood infected, with extra patrols sent afterward to contain it. _The developer's design._ _Not adopted: Claude's "they let it spread."_
- **The cure needs living infected** (people between infection and turning), as decided with B1.
- **The research group was effectively a small government** by then; needs a deep dive. _(Clarified below in "The Force is the city's government.")_
- What went wrong after "almost perfectly" (how the city fell) is open. Draft timeline v1 saved in the lore bible, under review.

## 2026-10-27: How the city fell, the Force, the delay compound, naming

- **Real NYC neighborhood names, fictional events.** _Rejected: Claude's suggestion of a fictional or unnamed neighborhood for the breach._ Exception: trademarked or branded names (sponsor-named stadiums, team-owned names, privately owned landmarks) get fictional versions; check each landmark.
- **A separate compound with a mysterious name (like The Boys' "Compound V") holds hosts in the infected state.** Related to the cure, not the same. **It's also a very rare or top-tier item that delays infection but doesn't cure.** _The developer's design. Rejected: Claude's idea that the antiviral itself sustains hosts._
- **How the city fell:** the harvest was enough to start mass-producing the cure but not to sustain it; right after the breach, a few infected were drawn by a noise along a route through buildings and slipped the cordon; some infected lucky victims who carried it into populated, lightly defended areas; **"the Force"** (working name), the research organization's own patrols, not real military _(clarified below: the Force is the city's government, with the research agency and the military under it)_, was spread too thin; daily life stopped. _The developer's design. Not adopted: Claude's options (cordon slip by people, an infected patrol, a host-facility breakout, the researcher opening the facility, repeated breaches)._ How the real military fits in is open. _(Changed 2026-10-27, new chat: the first mass-produced batch was never made; see "Who runs the Sanctuaries, the first batch, numbering".)_
- Next: daily life in the first years.

## 2026-10-27: Factions and daily life

- **The military built the wall.** **The research agency is a sub-branch of the federal government, like FEDRA** (The Last of Us). **The Force is its face**: technically a military sub-branch, but more "were" than "are". **After the outside fell (only small settlements left across the USA), they became effectively independent.** Answers "how does the real military fit in." _(Superseded in part by "The Force is the city's government" below: the agency and the Force are one organization.)_
- **Daily life in years 0–2 adopted as proposed** (registry and ID cards, curfews, ration credits that the current currency descends from, assigned work and urban farming, blackouts and solar, black markets and smuggling, schools and stadium food centers, screenings and disappearances, pirate radio). **Change: propaganda posters and broadcasts only start in late year 1 or year 2.** _The developer's timing._

## 2026-10-27: The Force is the city's government

- **The Force and the research agency are one organization.** **The Force is the overarching government of the city** (FEDRA-like, created by the federal government); **the research agency is part of it**; **it controls the military in the city**, which built the wall; the patrols are its enforcement. It became independent after the outside fell. _Clarifies and supersedes the "Factions and daily life" entry, which described the agency and the Force as separate, and the "How the city fell" entry, which called the patrols "groups from the research organization."_
- **The developer asked for this to be clear everywhere.** Updated: the lore bible ("The Force" section, the release, the fall, factions, the truth) and GDD §23.
- **Official name: F.O.R.C.E., an acronym** ("Federal Office for Response, Containment and E___"); "the Force" is the survivors' name for it. _Rejected for the E: "Enforcement."_ The E is TBD.
- **F.O.R.C.E. = Federal Office of Response and Containment of Epidemics.** **"Eradication" appears only in deep clues** (e.g., an internal "Eradication Protocol" document). _Not chosen: "Eradication" in the official name, which would give the twist away too early; "Emergencies"; "Evacuation."_ _"Office **of**" instead of "Office for", at the developer's request (it sounds more like a real US agency)._

## 2026-10-27: Names: SANCTUS, Hourglass, Sanctos Notes

- **Research program codename: Project SANCTUS.** The developer's condition: not already used in films or games. Web search found nothing titled exactly "Project Sanctus"; "Sanctus" alone is used by an unrelated horror game, a thriller novel and a horror film. A proper trademark check is still advised before marketing use.
- **Currency: Sanctos Notes** (final), named after the program as a hidden clue. _Not chosen: Boros, Quarants._
- **The infection-delaying compound: Hourglass (HG-7).**
- **The antiviral gets a name** (options pending).
- **Antiviral: Remisso** (reads as "remission"; Latin *remissio* = forgiveness). _Not chosen: Absolve, Salvus, Clementia, Spera, Lux, Agnus._ Generic name TBD; _rejected: "remissivir."_
- **Antiviral generic (label) name: remitrel.** _Rejected: "remirel", which is a real multiple-sclerosis drug (Zentiva)._ A web search found no existing drug named "remitrel."

## 2026-10-27 (new chat): The safe-zone group, part 1

- **The founders voted unanimously to cover it up**, though some wanted to make amends. _The developer's design._ Answers Claude's proposal of a split inside the founders. _Not adopted:_ two lasting factions (amends versus cover-up) inside the group.
- **The cure method was already in separate parts; one founder who voted for the cover-up hid his part instead of destroying it.** _The developer's design._ _Supersedes_ "a researcher who saw the price split the method apart and partially destroyed it" (entry "The lore twist"), and so the idea that this researcher died or turned. Open: which part he hid (Claude's reading: the process, so "the process survived; formulas and some ingredients are missing" still holds), where, what became of him, and whether the founders still want the method.
- **Guards: mostly ex-military (including soldiers contracted to the Force), ex-police and the like. Snipers: above average in the lore, mostly ex-military the group kept training; elite in gameplay** for anti-camping. _The developer's design._ GDD §18 updated.
- **The Patient's lines are collectible clues** (Claude's proposal; the developer: "i guess so").
- **Flashlights: leaning yes, zombies are drawn to them**, because zombies can see. Final once the infection itself is designed (the developer raised its type: a virus? a fungus?). _Not adopted: Claude's "no special pull."_ GDD §19 updated.
- **Rejected: players come out now because the safe-zone radio calls survivors in.** The developer wants a different reason, later. The other timeline points (8 years in total; wall soldiers ordered to let no one out) are still pending.
- **The Latin Mass phase names: "potentially"**, not decided.
- **"The Sanctuary" (Claude's proposed name for the safe-zone group) clashes in the genre:** a web search confirmed it's the Saviors' base in *The Walking Dead* and Fallout 4's starting settlement. Claude advises against it; the name is still open.
- **Awaiting confirmation (the developer's change, reverses earlier lore):** the spread was too fast for the Force to get the gathered hosts back to the labs, so **the first mass-produced batch was never made**, and **the Remisso that exists is what's left from testing**, which is why it's so rare. Earlier lore (entry "How the city fell, the Force, the delay compound, naming") said the harvest was enough to begin mass production. Not applied until confirmed; recorded in the lore bible.
- **Why the founders could name their money after SANCTUS: it's hidden in plain sight.** "Sanctos" reads as coming from "sanctuary" (which is where the name was first derived, in the trading topic), so survivors never suspect it carries the program's name. _The developer's call_, matching Claude's option A. _Not chosen:_ C (the program's printing plates came with them), D (survivors named it from a stamp). Option B (the amends-minded founders insisted on the name) stays open as an add-on. GDD §18 now says the name comes from "sanctuary". Fixes a gap: the "from sanctuary" origin had never reached the lore bible.

## 2026-10-27 (new chat): The safe-zone group is what's left of the Force

- **What's left of F.O.R.C.E. runs the safe zones; there's no separate safe-zone group.** _The developer's design._ Answers "what's left of the Force after the fall" in part. _Not chosen:_ "The Sanctuary" as the name of a separate group (Claude's proposal), which also clashed with *The Walking Dead*.
- **Each safe zone is "Sanctuary" plus a number: Sanctuary 1 to 6 or 7.** _The developer's design._ GDD §18 updated (names only; who runs them stays in the lore bible until it's decided whether survivors know).
- Name check (web search): no game found with zones called "Sanctuary 1" or "Sanctuary One". The word alone is used by *The Walking Dead*, Fallout 4 and, closest in theme, Mass Effect 3 (a refugee shelter secretly experimenting on refugees). Lower risk as numbered designations; recorded in the lore bible.
- **Outdated by this:** the surface-story draft "the safe-zone group is just survivors who got organized", and the timeline's "the founders regroup" and "answering the call" rows (the radio call was already rejected). Updated in the lore bible.
- Open (Claude's questions, in the lore bible's Pending proposals): do survivors know the Force runs the Sanctuaries (Claude's pick: openly, FEDRA-style)? Do the SANCTUS founders lead it? Numbered in the order they opened, with a gap for a fallen Sanctuary?

## 2026-10-27 (new chat): Who runs the Sanctuaries, the first batch, numbering

- **The Sanctuaries are run by former members from all of the Force's branches, not by the SANCTUS founders.** Mostly higher-ranking Force members (some don't know how deep it goes), leftover Force military who stayed with the groups in the safe zones to survive, and lower-ranking members who stayed for the same reason. _The developer's design._ _Not adopted:_ Claude's reading that the founders lead it.
- **The SANCTUS founders are gone**, including the one who hid his part of the method. What happened to them is open. _Changes_ "the founders know the method existed and still want it" (entry "The lore twist") and twist layer 3's wording ("its founders came out of the research program"); new layer-3 wording suggested by Claude, awaiting the developer's OK. "The founders' currency" and "the founders' bank registry" now read "the Sanctuaries'".
- **The military didn't collapse in the fall:** it failed to contain the spread with the soldiers and ammunition it had, until there was no turning back. _The developer's correction_ of Claude's suggestion that the military side broke down.
- **Confirmed: the first mass-produced batch was never made.** They contained the breached neighborhood and brought the infected hosts back, but by then it was already spreading fast inside the walls. The Remisso that exists is what's left from testing. _Supersedes_ "the harvest gave them enough hosts to begin mass-producing the cure, but not enough to sustain it" (entry "How the city fell, the Force, the delay compound, naming"). Timeline and "The turn" updated; the three layers players move through need new wording (Claude's suggestion pending).
- **Sanctuaries are numbered in the order they opened, and one has fallen** (a gap in the numbers; its ruins are a lore area). Claude's suggestions; the developer: "Yeah sure, and yes a fallen one would be cool." GDD §5 and §18 updated.
- **The breach (the "original fall") gets a name.** The developer asked for one; Claude's options are in the lore bible's Pending proposals.

## 2026-10-27 (new chat): The Breach, the founders' fates, the Force's secret

- **Names for the staged breach:** survivors call it **"the [neighborhood] Breach"**; the Force's paperwork calls it **"the [neighborhood] containment incident"**; internal codename **AGNUS DEI** ("Lamb of God"; deep clues only). The neighborhood is still TBD (NJ or the Bronx). _Claude's options, the developer's picks._ _Not chosen:_ "the Breach" alone, "the Hole in the Wall". Web search found no game, film or codename project called "Agnus Dei" with a related plot. "The fall" stays the name for the whole collapse. GDD §5 and §23 updated (survivor name only).
- **Most survivors don't know the Force runs the Sanctuaries;** the few who know are enough for believable rumors. _The developer's call._ _Not chosen:_ Claude's pick, running them openly (FEDRA-style). Twist layer 3 now reads: the Sanctuaries are what's left of the Force, it knows more than it says, and the people who knew everything are gone.
- **The founders' fates:** some are dead, some escaped the city (fate unknown), some are still hiding in the city. _The developer's design._
- **At release, no one in the remnant knows about the cure method or wants it;** that may change as players uncover the lore. _The developer's design._ So the bank registry isn't a list of hosts at release.
- **The three layers players move through:** "a lab accident let it loose" → the Force's hidden records: "a controlled release got away from us" → the truth: "it worked, and they buried it." _Claude's rewording; the developer: "Essentially."_ _Supersedes_ layer 3 "it didn't get away. It worked, and that's worse." Layer 1's wording ("lab accident" versus the survivors' name "the Breach") is flagged for the developer.
- **The military shrank:** many soldiers left after the breach led to rapid spreading; **no wall checkpoints are manned.** _Maybe:_ rare roaming patrols in the game (GDD §18 open items). _Not adopted:_ Claude's option that the wall's soldiers were pulled back to hold the Sanctuaries.
- **The method's 3 parts are the process, the key formulas and the ingredients.** _Conflict flagged, not applied:_ the developer wrote "both ingredients and process are lost", which would make the surviving part the formulas and reverse the earlier "the process survived". Awaiting the developer's answer.
- **Resolved: the part the founder hid is the process.** The formulas and some ingredients are lost, as decided before. The developer's "both ingredients and process are lost" was a slip for "formulas". _Not chosen:_ the formulas surviving instead.

## 2026-10-27 (new chat): Timeline v2, the Latin Mass pattern, the currency's meaning

- **8 years in total:** the game starts in year 8; the city fell in year 2, about 6 years before the game. _Claude's proposal from timeline draft v1; the developer: "yes"._ GDD §5 and §23 updated.
- **The wall's soldiers were ordered to let no one out** (twist layer 1 made physical). _Claude's proposal; the developer: "yes"._ Later, many of them left (entry above), so no checkpoints are manned today.
- **Timeline v2 written into the lore bible**, consolidating everything decided. Still draft, awaiting the developer: the wall in months 2–4 of year 0, the flood in years 2–3, Sanctuary 1 in years 3–5, the network in years 5–8, survivors' line "They abandoned us." Still open: why players come out in year 8, the timing of the cover-up vote and of the fallen Sanctuary, how the escaped founders got past the wall. _Context:_ the developer felt the timeline had already been gone over; the last chat built draft v1 and reworked the release and the fall, but these three points (8 years, the order, the radio reason) were never answered until now.
- **The Latin Mass naming pattern is adopted: "use it where we can."** SANCTUS (the program) and AGNUS DEI (the breach) use it; KYRIE, GLORIA, CREDO and BENEDICTUS are free for other internal names. _Claude's proposal; earlier "potentially"._
- **Not lore: the amends-minded founders insisting on the currency's name** (Claude's option B). The developer: "maybe it can be up to interpretation but nothing solid." Players may read it that way; nothing confirms it.

## 2026-11-08: Development starts; lore paused

- **Development of the game starts now.** The developer: "I want to get going on actually making the game."
- **The entire lore will be revisited later in development, not now.** The developer's call. _Changes_ "build the deep lore before development gets far" (entry "Lore foundations"); the lore bible's status, GDD §23 and the Systems checklist are updated. Open lore items and the lore bible's Pending proposals wait for that revisit.
- _Claude's note:_ early work (source control, the 300-player load test, core systems) doesn't depend on the lore; lore-heavy content (points of interest, safe zones, radio broadcasts) is best built after the revisit.

## 2026-11-08: Source control and engine version

- **Git + Git LFS, in two private GitHub repos:** [NYZ-DOCs](https://github.com/NNarwhall/NYZ-DOCs) for the docs, lore, decision log and transcripts (the developer only), and [NYZ](https://github.com/NNarwhall/NYZ) for the UE5 game (the repo volunteers would get). _Claude's recommendation; the developer created both repos._ Why two: the lore twist is spelled out in the lore bible, this log and the transcripts, and splitting one repo's history later is messy. _Not chosen:_ Perforce; one repo for everything. Answers the GDD open question "Source control: Git LFS or Perforce?" (GDD §4).
- **Unreal Engine 5.8**, built from source, because the Epic Launcher version can't build dedicated servers (GDD §3). _Claude's recommendation_ (the newest version installed); the developer is downloading the 5.8.4 source and updating the launcher copy to 5.8.4. The source build itself can wait until the load test needs it.

## 2026-11-08: Load test early, kept small

- **Milestone 1 is an early, small load test** built on the game's real foundation (player character and movement, the dedicated server setup, basic zombies), plus a bot script and a map of plain boxes. It is rerun as systems are added; a full test with the finished systems still comes later. _Claude's recommendation; the developer: "Early kept small."_ Why: if 300 players don't fit on one server, the fixes change how every system sends its data (GDD §3). Written into the new GDD §24 (Development plan).
- _Not chosen:_ testing only after most systems are built, so nothing is made just for the test (the developer's first understanding). The test-only parts are small, and the bot script is reused for every rerun.
- The test's details (pass bar, map size, bot behavior, zombies, networking, where it runs) are proposed in GDD §24 and await the developer's answer.
- **The load test runs at both 300 and 500 players.** The developer: "lets test both when we do the test wont hurt." 300 is the launch target, 500 the later goal; Claude's analysis put the map's comfortable maximum at about 500 (GDD §5). GDD §24 updated.
- **The load test details in GDD §24 are agreed** (pass bar, 25 × 25 km box map, bot behavior, zombies ramped up to find the count, Iris first, decide on failure with the numbers, hosting-cost estimate). The developer: "All yes i guesss, but i dont have money."
- **No budget for now** (new GDD §2 row). So the test runs on **free options only**: stage 1 on the developer's PC at several bot counts to see how the cost per player grows; stage 2 (the full 300 and 500) from free cloud trial credit or friends' PCs, decided when we get there. _Changes_ Claude's proposal of a few hours on paid rented cloud machines.

## 2026-11-08: Game project created

- **The UE 5.8 C++ project exists:** blank template, named NYZ, no starter content, raytracing off, at `C:\Game Dev Folder\NYZ\NYZ`, pushed to the NYZ repo with UE5 ignore and LFS rules. The docs repo ignores the folder. _Changes_ Claude's earlier suggestion of a `Game` folder: Unreal names the folder after the project, and renaming it adds steps for no gain.
- **Nothing carries over from older projects** (the developer): NYZv409 stays as a reference backup only.

## 2026-11-08: The load test uses bare versions

- **Each piece in the load test gets only what the test needs**, so it loads the server the way the real thing would. Its full design pass comes after the test, when it's built for real. Applies to every system in the test and its reruns. The developer: "Youre already going "all in" on a system before ever even testing, thats what i mean. This is the problem we will run into everytime with the test first mentality, if we are just testing the server limit, why are we going all out on movement." GDD §24 updated.
- **The test character uses Unreal's standard Character Movement** (the template's default), with walk, sprint and jump at rough speeds and the mannequin as the body. _Why:_ the test measures its server cost, so it's the one movement choice the test depends on. Mover, Unreal's newer system, is still experimental in 5.8 (checked in the engine's plugin files), and its readme says little work has gone into scaling.
- _Not chosen:_ a full movement design pass before the test (Claude's proposal). Claude's draft points, never discussed, kept for the later movement pass: walk/jog/sprint at 1.5/3.5/6 m/s with jog the default, crouch 1.2, prone 0.5, zombies 0.8/1.4/4 (decayed/weathered/fresh); stand, crouch and prone; stamina used by sprint, jump, climb, melee and swimming, with weight shrinking max stamina; one key for hop, vault (waist-high) and climb (up to about 2 m), plus ladders and fire escapes, with base walls taller than 2 m; falls safe under 3 m and deadly over about 12 m; swimming slow and stamina-limited to a few hundred meters, so rivers need bridges or boats; aiming always in first person, Alt free look; Q/E lean; footstep noise from gait × stance × footwear × surface.

## 2026-11-08: Load-test map built

- **The box map is one plain level, with no World Partition and no landscape.** _Claude's call_ (how to build the agreed point 2, GDD §24). _Why:_ the server loads the whole map either way (World Partition's default on servers), and the test measures players and zombies, not map streaming. One level with all 15,900 boxes drawn as copies of one mesh is a single 3 MB file that loads in about 0.1 s. _Not chosen:_ World Partition (many small files plus streaming the test doesn't measure; the real NYC map will use it); a landscape (heavy terrain data for flat ground).
- **Layout:** 25 × 25 km flat ground; boxes on a 200 m grid (50–150 m wide, 10–60 m tall); 5 dense hotspots of 64 boxes each with 10–15 m alleys, tagged "Hotspot" for the bot script; 500 player starts on street corners, one per bot in the 500 run. Built by `Tools/build_load_test_map.py` in the game repo with a fixed seed. Set as the default map for the game, the server and the editor's start. GDD §24 point 2 updated.
