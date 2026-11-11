# NYZ Lore Bible

**Status: paused (2026-11-08).** Development of the game starts now, and the developer wants to **revisit the entire lore later in development**, not now. Until then, nothing here changes unless the developer brings it up; open items and Pending proposals below wait for that revisit. The developer's words: "I want to revist the entire lore at some point, so later in development but not rn".
_Earlier plan (2026-10-27), now changed:_ deep lore built before development gets far, because it shapes the map, the points of interest and several mechanics. _Claude's note:_ early work (source control, the 300-player load test, core systems) doesn't depend on the lore; lore-heavy content (points of interest, safe zones, radio broadcasts) is best built after the revisit.
Decisions here are also logged in `docs/DECISIONS.md`; the GDD (§23) holds a short summary that points here.
**The developer's lore messages, word for word:** [developer-words.md](developer-words.md). Where this bible paraphrases, that file is the source. Full conversation: `docs/transcripts/`.

---

## How the lore is told
- **Deep lore, never explained by cutscenes.** Told the way Project Zomboid does it: **clues in the world** and **radio broadcasts**.
- **Radio is different from Zomboid's:** Zomboid's broadcasts work because the game starts on day 0. NYZ starts years later, so broadcasts are **random**, from whoever is still transmitting. (See Radio below.)
- **Players who care can dig deep; players who don't are never forced to.**
- **Two layers:**
  - **The truth:** what really happened. Written down here, known to the developers, never told to players outright.
  - **What survivors believe:** the story most people inside the city tell. Partly wrong.

---

## Decided

### Where it came from (origin: B + C)
- **It came from outside.** NYC wasn't where it started.
- **The whole world is "cooked":** like the city, there are pockets of survivors and safe zones elsewhere, but for the most part the world has fallen.
- **Most survivors don't really know what it is, or what's going on outside the wall.**
- **The developer's direction (not final wording):** it started outside, and **researchers and scientists came to the city to study it.** NYC was walled off, and **for a while the city was locked down and holding its ground well.** Then **it spread inside the walls because of the experimenting and research.**
- **Plus a mystery (C):** the twist, below.

### The truth: the twist (chosen 2026-10-27)
**Never told to players outright.** These four layers are what clues gradually reveal:

1. **The wall was never meant to keep the outbreak out.** NYC was chosen as the research site *because* it could be sealed. **The people inside were never told they were part of the study.**
2. **The breach inside the walls wasn't an accident.**
3. **The safe-zone group knows more than it says.** **Its founders came out of the research program** (the Force's research agency).
   - **Updated 2026-10-27 (new chat):** the safe zones are run by **what's left of the Force**, not by the founders, and **most survivors don't know it** (a few do, enough for rumors). **The SANCTUS founders who covered it up are gone.** Some higher-ranking members of the remnant know part of what the Force did; others _"dont even know how deep it goes"_ (the developer). See "The safe-zone group".
   - So layer 3 now reads: **the Sanctuaries are what's left of the Force, and it knows more than it says; the people who knew everything are gone.** (Claude's summary of the developer's answers.)
4. **The special zombies are the original test subjects.**

_Not chosen:_ "the research wasn't for a cure" (so, as far as the lore goes, the cure research was real; the antiviral is its result) and "the outside world isn't what the radio suggests."

**The research and its people (added by the developer, 2026-10-27):**
- **The study's purpose was real: finding a cure that could be mass-produced.**
- **A cure already exists (the antiviral), but it's extremely difficult to produce from its known materials.** That's why it's so rare in the game (GDD §8, §12).
  - **Decided (the developer, 2026-10-27, new chat):** the Remisso in the world today is **only what's left from testing**, because the first mass-produced batch was never made (see "How the city fell"). The developer: _"Only remenants of testing remains, which is why theyre so rare."_
- **The researchers genuinely had good intentions.** They weren't villains from the start.
- **Something made them flip**, leading to the deliberate breach.

**What flipped them: a chain (chosen 2026-10-27)**
1. **The world went dark.** Contact, funding and orders from outside stopped. They believed they were humanity's last chance, with supplies running out.
2. **They ran out of test subjects.** The research needed infected subjects, which **came from expeditions outside the wall**. They had **already used up the infected from nearby towns**, and with the city locked down so tightly, **further expeditions outside were too risky.**
3. **So they planned a small, controlled release inside the walls**, sure they could contain it. It got away.
- **Where the release happened** was chosen for **practical reasons** (population, how easy it was to seal off), **never by who lives there.**
- _The developer's concern: this chain is a bit predictable._ Answered by the turn below.

**The release: a staged breach (the developer's design, 2026-10-27)**
- **Names (decided 2026-10-27, new chat).** The developer: _"Lets do "The (Neighborhood) Breach" for survivors, containment incident good for FORCE Paperwork , good code name)"_
  - **Survivors call it "the [neighborhood] Breach."** The neighborhood is still TBD (NJ or the Bronx).
  - **The Force's paperwork calls it "the [neighborhood] containment incident."**
  - **Internal codename: AGNUS DEI** ("Lamb of God", the part of the Mass about the sacrifice that takes away the world's sins): a neighborhood offered up for everyone else. Deep clues only. It follows the Latin Mass naming pattern (adopted; see SANCTUS below).
  - "The fall" stays the name for the city's whole collapse.
  - _Not chosen:_ "the Breach" on its own, "the Hole in the Wall".
  - _Name check (2026-10-27, web search):_ no game, film or codename project called "Agnus Dei" with a related plot. A 2026 audiobook titled *Agnus Dei* (Podium Entertainment) is about a boy's apparent miracle, unrelated. It's also a common religious term.
- They needed **a large group of living infected**, and the nearby towns had few subjects left.
- **The plan:** stage a **breach in the wall** at a **small neighborhood on the border** (candidates: somewhere in NJ or the Bronx), letting in **a small horde they had gathered in advance**: test subjects and other people they had taken for experiments.
- The area was **deliberately left lightly defended.** To avoid raising suspicion beforehand, they **didn't add much security there, only a few more patrols.**
- **It went almost perfectly:** many people in that small neighborhood were infected. **Extra patrols were sent in afterward** to keep it from spreading.
- **This was the Force's plan, run by its research agency** (see "The Force" below). Needs its own deep dive (see Factions).
- **The cure needs LIVING infected** (decided with B1): people kept in the window between infection and turning. So the newly infected neighborhood was the harvest.
- **Holding hosts in the window: a separate compound** with a mysterious name (like "Compound V" in *The Boys*). It **holds people in the infected state** before turning. **Related to the cure, but not the same thing.** _The developer's design._ _Not adopted: Claude's idea that the antiviral itself sustains hosts._
  - **It also exists as a very rare or top-tier item** that **delays infection for survivors but doesn't cure them** (GDD §8).
  - **Name: Hourglass** (lab code **HG-7**). Decided 2026-10-27. Why: it buys time, which is exactly what it does for players, and still sounds mysterious. _Not chosen: Halcyon, Limbo, Tether._

**How the city fell (the developer's design, 2026-10-27)**
- **The first mass-produced batch was never made (decided by the developer, 2026-10-27, new chat).** They **contained the breached neighborhood** and **brought the infected hosts back**, but by then **it was already spreading fast inside the walls** (from the few that slipped the cordon, below). The Remisso that exists is **what's left from testing**, which is why it's so rare.
  - The developer: _"The operation went wrong, the spread was not instant instant, but it was not slow enough for them to take the infected that they were able to gather back, so the first mass produced batch was never made. Only remenants of testing remains, which is why theyre so rare."_ Then, confirming: _"No, first batch wasnever made, like i said, they ended up containing the original fall (Which we shoould name that even), but by the time they got the infected back, it was already rapidly spreading within the walls"_
  - _Superseded:_ "the harvest gave them enough hosts to begin mass-producing the cure, but not enough to sustain it" (the developer's earlier version, same day). _Also corrected:_ Claude's first cleanup said they couldn't get the hosts back to the labs; they did, but too late.
  - **The breach itself (the "original fall") is named:** the [neighborhood] Breach (see "The release" above).
- **Right after the breach, a few infected were drawn by a noise** that led them along a route, through some buildings, and **they slipped past the cordon.**
- They spread out. **A few died before infecting anyone; some found lucky victims**, and those victims carried it into **more populated but lightly defended areas.**
- **The Force's patrols** (see "The Force" below) were **spread too thin** to manage it.
  - **The military didn't collapse** (the developer, 2026-10-27): _"the military didnt just entirely collapse during the fall, they just failed to contain the situation to a point there was no turning back with their army size and munitions."_ With the soldiers and ammunition it had, it couldn't contain the spread, until there was no turning back. Much of it survived (see "The safe-zone group"). _Not adopted:_ Claude's suggestion that the military side broke down in the fall.
  - **But it shrank** (the developer, 2026-10-27): _"no active checkpoints, the military is way smaller than when the breach was around as many left after the breach led to rapid spreading. Maybe rare roaming patrols ingame."_ **Many soldiers left** once the breach turned into rapid spreading, so **today's military is far smaller** than at the time of the breach. **No wall checkpoints are manned.** _Maybe:_ **rare roaming patrols** in the game (GDD §18). _Not adopted:_ Claude's option that the wall's soldiers were pulled back to hold the Sanctuaries.
- It reached the point where **daily life stopped.**

### The Force: the city's government (decided 2026-10-27; applies everywhere in the lore)
- **Name: F.O.R.C.E. = Federal Office of Response and Containment of Epidemics** (decided 2026-10-27). "The Force" is what survivors call it. Harmless on the surface: nothing gives the twist away early.
  - **"Eradication" appears only in deep clues:** e.g., an internal document titled **"Eradication Protocol"** inside the research program. Players who find it get the chill deep into the mystery, not on the first poster. (In public health "eradication" means wiping out a disease, which makes the document read as innocent until you know the truth.)
  - _Not chosen:_ "Enforcement", and "Eradication" as the official E.
- **The Force** is **the overarching government of the walled city**, created as a sub-branch of the real federal government, like **FEDRA** in *The Last of Us*.
- **Everything is under it.** It is **one organization**, not separate groups:
  - **The research agency is part of the Force.** It ran the study, the screenings, the quarantine wards, the staged breach and the cure program.
  - **The Force controls the military** in the city. **The military built the wall** under it. _(The developer first wrote "the military was there to setup the fall"; they confirmed on 2026-10-27 that they meant "wall".)_
  - **The patrols and enforcement are the Force's.** Technically a branch of the military, but more "were" than "are".
- **After the outside fell** (only small settlements left across the USA), **the Force became effectively independent**, answering to no one.
- **After the city fell, what's left of the Force runs the safe zones**, named Sanctuary 1 to 7: former members from all of its branches, not the founders (decided 2026-10-27; see "The safe-zone group").
- When this document says "the program", "the researchers" or "the patrols", it means **parts of the Force**.
- **The antiviral's name: Remisso** (decided 2026-10-27, the developer's spelling). Everyone reads it as "remission" (a disease going away); in Latin, *remissio* means **forgiveness**. Surface reading versus truth, like "Eradication". **Generic (label) name: remitrel.** _Rejected: "remissivir"; "remirel" (already a real multiple-sclerosis drug, Zentiva). A web search (2026-10-27) found no drug named "remitrel"._
- **The research program's codename: Project SANCTUS** (Latin, "holy"). Decided 2026-10-27.
  - **The Sanctuaries' currency, "Sanctos Notes", is named after it:** a clue hiding in plain sight. Only players who find the program's name ever connect the two (twist layer 3). Keep the program name out of anything shallow.
  - **Two readings of "Sanctos" (decided 2026-10-27, new chat):**
    - **What survivors believe:** it comes from **"sanctuary"**, the safe zones' own money. This is where the name first came from: Claude proposed "Sanctos: from sanctuary" in the trading topic (transcript, 2026-10-27), before SANCTUS existed.
    - **The truth:** whoever named it chose a name that reads as "sanctuary" because it also carries the program's name. _(Who named it is open now that the founders are gone: the founders before they left, or higher-ups who knew.)_ That's why they could use it without drawing attention. The developer (2026-10-27): _"Well isnt sanctuary where we derived Sanctos from to begin with? Kinda a hidden in plain sight"_
    - _Up to interpretation, nothing solid (decided 2026-10-27):_ Claude's option B, that the founders who wanted to make amends insisted on the name as a confession nobody can read, is **not lore**. The developer: _"No, maybe it can be up to interpretation but nothing solid."_ Players may read it that way; nothing in the game confirms it.
    - _Also true:_ "sanctos" is a real Latin word form, "the holy ones" (noted by Claude in the trading topic). Obscure enough that nobody reads it as a real word; a third layer for Latin-minded lore hunters.
  - **The Latin Mass naming pattern (adopted 2026-10-27, new chat; Claude's proposal).** The developer: _"Okay so we use it where we can."_ The program's internal names come from the parts of the Latin Mass wherever they fit: **Kyrie, Gloria, Credo, Sanctus, Benedictus, Agnus Dei.** In use: **SANCTUS** (the program) and **AGNUS DEI** (the breach). Still free: KYRIE, GLORIA, CREDO, BENEDICTUS (e.g., phases of the program in deep documents). Lore hunters who spot the pattern can work out the program's structure.
  - _Name check (2026-10-27, web search):_ no game, film or book found titled exactly "Project Sanctus". "Sanctus" alone is used elsewhere: a horror game by Madmind Studio, Simon Toyne's thriller novel *Sanctus*, a horror film *Sanctus House* (2026). None is a cure or virus program. Worth a proper trademark check before marketing uses the name.

**Daily life inside the wall, years 0–2 (adopted 2026-10-27)**
- **Year 0, the sealing:** panic, then adjustment. The gates close; refugees at the wall are turned away (an early hint the wall works both ways). The **registry** begins: an ID card needed for food, work and checkpoints. Curfews and checkpoints between boroughs.
- **Year 1, the new normal:**
  - **Ration cards and ration credits.** The dollar fades; the authority prints **credit notes**. _Tie:_ the Sanctuaries' currency today descends from these.
  - **Assigned work:** building the wall, utilities, **urban farming** (why rooftop and community gardens are everywhere, GDD §22).
  - **Rolling blackouts; solar panels go up** (why solar is on rooftops and bike-share docks, GDD §16).
  - **Black markets:** bodegas as fronts, smuggling through the wall. _Tie:_ the customs warehouse full of seized smuggled guns at the ports (GDD §12) dates from this era.
  - **Schools stay open** with lockdown drills; **stadiums become food distribution centers.**
  - **Mandatory health screenings;** people start disappearing to the quarantine wards, and whispers spread.
  - **Pirate radio** appears: rumors and resistance (the origin of today's unreliable stations).
- **Late year 1 to year 2, the cracks:**
  - **Propaganda starts here, not earlier** (the developer's timing): official posters and broadcasts like "The wall keeps us safe" and "Report symptoms".
  - The radio from outside goes silent; rations shrink; more "exposure removals"; neighbors inform on neighbors.
  - Then the breach, and the fall.
- **Clues players find:** ID cards, ration cards, old credit notes, propaganda posters (late-era only), school notices, black-market ledgers, official radio recordings, removal notices.

**Real names, fictional events (decided 2026-10-27)**
- The breached neighborhood, and others in the story, use **real NYC neighborhood names**. **All events are fictional.**
- Exception: names that are trademarked or branded (see GDD §5 naming rule).

**How the residents were studied without knowing (chosen 2026-10-27)**
1. **The registry:** everyone inside the wall had to register for an ID card "for safety". It tracked blood type, health and who could be useful. **The Sanctuaries' bank registry today (GDD §18) is the same idea continuing**, a clue that ties past to present. _Clues:_ old ID cards, registration posters, registry terminals.
2. **Health screenings and blood drives:** mandatory checkups at checkpoints collected blood and samples, raw material for the research, and picked out useful people. _Clues:_ screening wristbands, blood bank logs, "donor" lists.
3. **Quarantine wards:** residents flagged for "possible exposure" were taken to quarantine hospitals (e.g., **North Brother Island**) and never came back. They became subjects. _Clues:_ removal notices, lists of names, empty wards.
- _Not chosen:_ "free immunizations" as the public face (the developer wasn't feeling it); trial compounds in rations.
- **The water supply: a rumor only, and false.** A red herring that sends lore hunters chasing the rooftop water towers. _Confirmed 2026-10-27._

**The special zombies: the original test subjects (chosen 2026-10-27)**
Both appear **only at lore areas**, and each one is evidence in itself.
- **The Patient:** one of the people taken to the quarantine wards, from the first round of tests.
  - Tougher (takes more head damage to drop); **the only zombie that truly runs.**
  - Still wears a hospital gown and a **registry wristband** (a lootable clue).
  - **Can sometimes be heard saying a word or a sentence in English**, then going back to incoherent mumbling. _Added by the developer._ (The lines can carry clues; audio files get neutral names, see "Hiding the truth".)
  - **The lines are collectible clues** (Claude's proposal, adopted 2026-10-27; the developer: "i guess so"). Each Patient says something different (a name, a ward number, "they said it would help"), so players can collect them like audio logs.
- **The Host:** one of the people used for the **cure process**, kept in the window between infection and turning. They turned anyway.
  - Slow and very hard to kill; medical restraints and tubing still hang off it.
  - The most lore-heavy sight in the game: how players start to understand what the cure costs.
- **Both must look clearly different from regular zombies, e.g. mutated.** _Added by the developer._
- _Not chosen as specials:_ the Screamer (shrieks to pull in hordes) and the Blind (hunts purely by sound). Claude suggested they could become regular zombie behaviors later; not decided.

**The turn: it didn't get away. It worked. (chosen 2026-10-27: B1 + B4, modified)**
- **The release worked.** The researchers got their subjects and **found a way to mass-produce the cure.** **But the first batch was never made** (see "How the city fell").
- **The price (B1):** the scalable method needs **living infected hosts**, people kept alive in the window between infection and turning, which the cure is grown from. Mass production means farming people.
- **Already in separate parts; destroyed in the cover-up, except the part one founder hid (changed by the developer, 2026-10-27, new chat).** The developer: _"Some want to  make amends, but ultimately they unanimaously decide to cover it up. So we can go back on what we said before, and instead of splitting the 3 parts. they are already split parts. But oone of the founders that agreed to cover up ends up just hiding his part of the clue"_
  - Cleaned up: the method **was already divided into parts**, held separately, so nobody had to split it. The founders **unanimously chose to cover it up** (see "The safe-zone group"). **One founder who voted for the cover-up hid his part instead of destroying it.** What survives is incomplete.
  - _Superseded:_ "a researcher who saw the price split the method apart and destroyed part of it" (B4 as modified earlier on 2026-10-27). Why: the developer's call. The act moves from one researcher to the founders' shared decision, which one of them quietly breaks.
  - **What survived: the process** (the steps for growing the cure from living hosts). **The 3 parts are the process, the key formulas and the ingredients** (confirmed 2026-10-27).
  - **The part the founder hid is the process** (confirmed by the developer, 2026-10-27): _"The process survived, as before. The formulas and some ingredients are lost; "process" in my last message was a slip."_ Their earlier _"Yes, both ingredients and process are lost"_ was a slip for "formulas". _Not chosen:_ the formulas surviving instead.
  - **What's missing: multiple key formulas and some ingredients.** Anyone rebuilding it would have to rediscover them, possibly the same terrible way.
  - **Whether it can ever be rebuilt is left open on purpose.** Clues and broadcasts can hint that someone is getting closer.
  - **Where the founder hid his part:** TBD. It must be hidden extremely well (see "Hiding the truth" below).
- From Claude's pick, accepted with it:
  - _Superseded (2026-10-27, new chat):_ "the researcher who did it died or turned, possibly one of the Patients." There's no lone researcher any more. **The founder who hid his part is gone with the other founders**; which of their fates he met is open (see "The safe-zone group").
  - _Superseded (2026-10-27, new chat):_ "the founders know the method existed and still want it." **The founders are gone.** The bank registry (GDD §18) now belongs to what's left of the Force and tracks survivors. **Answered (the developer, 2026-10-27):** _"No, not at release, maybe if lore starts getting discovered."_ **At release, no one in the remnant knows about the method or is after it**, so the registry isn't a list of hosts. **That may change later, as players uncover the lore** (a story beat over a server's life or in an update).
- **Three layers players move through:**
  1. What survivors believe: "a lab accident let it loose."
  2. What the Force's hidden records say: "a controlled release got away from us." Players think they've solved it.
  3. The truth: **it worked, and they buried it.** They had found how to make the cure for everyone, it costs living people, and the founders chose to destroy it.
  - _Reworded 2026-10-27 (new chat): Claude's wording, the developer: "Essentially."_ _Superseded:_ layer 3 "it didn't get away. It worked, and that's worse" (since the first batch was never made, it partly did get away) and "the founders' hidden records" in layer 2.
  - _Small mismatch to settle:_ survivors call the event "the [neighborhood] Breach", so they know it came through the wall; layer 1 still says "a lab accident" (see Pending proposals).

**What survivors believe (the surface story), draft:** the world fell; NYC was walled off to protect it and became a place where scientists worked on a cure; it held for a while; then something went wrong in a lab and it got loose inside; the safe-zone group is just survivors who got organized. _(2026-10-27: most survivors do believe the Sanctuaries are survivors who got organized. In truth they're what's left of the Force; a few people know, enough for rumors. The "lab" part may change, see Pending proposals.)_

### The safe-zone group (in progress, started 2026-10-27)
**Who runs the safe zones: what's left of the Force** (the developer, 2026-10-27): _"FORCE, can be the ones running the safe zones, with each safezone being just Sanctuary x (1-6 or 7)"_ and _"Whats left of FORCE"_
- **There's no separate group.** The safe zones are run by **what's left of F.O.R.C.E.** In this document, "the safe-zone group" now means the Force's remnant.
- **Who's in it (the developer, 2026-10-27):** _"It is not necessarily founders running safezones, just people that use to part of FORCE, remember there multiple branches. The founders are gone, whats left is mostly higher ranking members from FORCE(some who dont even know how deep it goes), leftover FORCE military that all decided to stay with the groups in safezones for preservation, and even lower ranking members that stayed for the same reason."_
  - **Former members from all of the Force's branches**, not the founders:
    - **mostly higher-ranking Force members**, some of whom **don't know how deep it goes**;
    - **leftover Force military**, who all chose to stay with the groups in the safe zones **to survive**;
    - **lower-ranking members** who stayed for the same reason.
  - _Not adopted:_ Claude's reading that the SANCTUS founders lead it.
- **Each safe zone is "Sanctuary" plus a number:** Sanctuary 1 to Sanctuary 6 or 7 (GDD §18).
  - **Numbered in the order they opened**, so Sanctuary 1 is the oldest. **One number is missing: a Sanctuary that fell**, now a lore area the Force never talks about. Claude's suggestions, adopted 2026-10-27 (the developer: "Yeah sure, and yes a fallen one would be cool").
  - _To confirm:_ with 6–7 active zones plus the fallen one, the numbers run to 7 or 8.
- **How it fits what's decided:** "Sanctos" now reads even more naturally as coming from "Sanctuary"; the Force printed the ration credit notes in year 1, so it printing Sanctos Notes now follows; the bank registry is the same organization's registry, continued; the guards include soldiers who had been contracted to the Force.
- _Not chosen:_ "The Sanctuary" as the name of a separate group (Claude's proposal). The developer made the group the Force itself; the name also clashed with *The Walking Dead*.
- **Name check, "Sanctuary" plus a number (2026-10-27, web search):** no game found with safe zones called "Sanctuary 1" or "Sanctuary One". The word alone is still used by *The Walking Dead* (the Saviors' base), Fallout 4 (Sanctuary Hills) and, closest in theme, **Mass Effect 3's "Sanctuary"**: a refugee shelter on Horizon secretly run by Cerberus to experiment on the refugees. Numbered official designations read differently from one named compound, so the risk is lower, but players who know Mass Effect 3 may guess the twist from it.
- **Most survivors don't know the Force runs the Sanctuaries** (the developer, 2026-10-27): _"For the most part no, but those who know know. Not a lot of people but enough for rumor spreads to be plausible."_ A few people know, enough that rumors about it are believable. The numbered names, the registry and Force-issue gear on the guards can feed those rumors. _Not chosen:_ Claude's pick, running them openly (FEDRA-style).

**The founders** came out of Project SANCTUS (twist layer 3). **They are gone** (the developer, 2026-10-27: _"The founders are gone"_). **What happened to them** (the developer, 2026-10-27): _"Some dead, some escaped the city and we dont know their fate, some in hiding in the city still."_ **Some are dead; some escaped the city, fate unknown; some are still hiding in the city.** Still open: which fate the founder who hid his part met; how the ones who escaped got out; whether they had any hand in the first Sanctuary.
- **The cover-up (the developer, 2026-10-27):** _"Some want to  make amends, but ultimately they unanimaously decide to cover it up."_ Some founders wanted to make amends, **but in the end they all voted to cover it up.** This answers Claude's proposal of a split inside the founders. _Not adopted:_ two lasting factions (amends versus cover-up) inside the group, because the vote was unanimous.
- **One founder broke it quietly:** he voted for the cover-up, then **hid his part of the method instead of destroying it** (see "The turn").

**Guards and snipers (the developer, 2026-10-27):** _"guards are mostly just ex military, military that was contracted for FORCE, or ex police etc, with the snipers not neccesarrily being elite, just above average but also mostly ex military that they continued to train. For sake of anti camping gameplay theyre elite."_
- **Guards:** mostly ex-military, including **soldiers who had been contracted to the Force**, ex-police and the like.
- **Snipers, in the lore:** **above average, not elite**; mostly ex-military **whom the group kept training.**
- **Snipers, in gameplay:** **elite aim**, for the anti-camping rule (GDD §18). The game makes them better than the lore does, for the sake of fair play around the gates.

**What survivors believe:** mostly that the Sanctuaries are **survivors who got organized**; a rumor says they're the Force (decided 2026-10-27).

### Hiding the truth (decided 2026-10-27)
- **The deepest secrets (where the founder hid his part of the method, the full truth) must be so well hidden that finding them could take players months to years after release.**
- **Nothing obvious in the game files.** Players will datamine the files; asset and file names must give nothing away.
- _Technical notes (suggested, for the deeper design pass):_
  - **The best hiding place is not shipping it at all:** keep the deepest content **on the server** and only send it to a client when it's unlocked in game. Dataminers can't find what isn't on their disk.
  - Neutral or meaningless names for anything lore-related that does ship; text stored encrypted, not as plain strings.
  - **Clue chains that need in-game actions:** e.g., a radio frequency only active at certain in-game times, coordinates from a numbers station, an item that only reveals something at a specific place.
  - **Time-gated reveals:** new clues unlock over a server's life and over updates, so even full datamining at launch can't reveal everything.

---

## What the lore has to explain (mechanics already decided in the GDD)
Every rule below needs an in-world reason, or at least shouldn't contradict the lore.

| Mechanic | GDD |
|---|---|
| Only people infected at death turn; destroying the head stops it | §8, §10 |
| Bites infect often, scratches rarely; clothing can block it | §8 |
| Fresh zombies move faster than decayed ones | §8 |
| 1–2 special zombie types, extremely rare, harder to kill, found at lore areas | §8 |
| A rare antiviral cures infection (hospitals, labs) | §8, §12 |
| Zombies hunt mainly by sound, see worse at night, don't swim | §8, §16, §19 |
| No zombie animals; wildlife has returned to the city | §22 |
| The city is **overgrown**, so the outbreak was **years** ago. _Under revision 2026-11-11: likely 1–3 years, so lighter overgrowth (see Timeline v2)_ | §5 |
| The map border is a **wall along major highways**; bridges are open | §5, §16 |
| An organized safe-zone group: NPC guards, elite snipers, a bank, its own currency (Sanctos Notes, final), radio broadcasts. _It's what's left of the Force (most survivors don't know); the zones are Sanctuary 1–7_ | §18, §19 |
| Smuggled guns in a customs warehouse at the ports | §12 |
| A hurricane has flooded low areas | §19 |
| Players are fresh survivors with basic gear; each death is a new life | §10 |
| Whether flashlights draw zombies (leaning yes, since zombies can see; final once the infection itself is designed) | §19 |

---

## Pending proposals
Claude's proposals still waiting for the developer's answer, with every option, so nothing is lost if a chat ends. Remove an entry once it's answered (and record the answer in the right section).

Current topic: **the safe-zone group**, now decided to be **what's left of the Force** (former members from all its branches) running Sanctuary 1–7, **mostly without survivors knowing** (2026-10-27, new chat; see "The safe-zone group" above).

_Answered 2026-10-27 (new chat) and moved out:_ the split inside the founders (became the unanimous cover-up), the Patient's lines (adopted), flashlights (leaning yes, see "What the lore has to explain"; Claude's "no special pull" not adopted), the radio call as the reason players come out now (rejected), "The Sanctuary" as a separate group's name (not chosen: the Force runs the zones), who leads the Force's remnant (former members of all branches, not the founders), the Sanctuaries' numbering (adopted, with a fallen one), "the first batch was never made" (confirmed), whether survivors know the Force runs the Sanctuaries (mostly not; Claude's "openly" not chosen), the breach's names (the [neighborhood] Breach / containment incident / AGNUS DEI), the founders' fates, whether anyone wants the method (not at release), the reworded three layers ("Essentially"), the wall soldiers (many left; Claude's "pulled back" not adopted), which part of the method survived (the process; "process are lost" was a slip), Claude's option B for the currency name (up to interpretation, nothing solid), the Latin Mass pattern (adopted: "use it where we can"), 8 years in total and the wall's order to let no one out (both yes). _Keep in mind:_ avoid *The Walking Dead*'s Terminus slogan, "Sanctuary for all", as a motto.

Waiting for the developer:
1. **Layer 1 wording** (Claude, 2026-10-27). Survivors call the event "the [neighborhood] Breach", so they know it came through the wall, but layer 1 still says "a lab accident let it loose". Options:
   - **A. "The wall failed at [neighborhood]":** survivors think the breach was an accident (an old stretch of wall, too few patrols). Twist layer 2, "the breach wasn't an accident", then overturns it directly.
   - **B. Keep "a lab accident":** infected escaped from a lab and got out through the wall at [neighborhood]. Harder to explain why a lab breakout would come through the outer wall.
   - **C. Both:** the official line is A (a wall failure, the "containment incident"); a rumor says something got out of a lab.
   - Claude's pick: **A + C's rumor.**
2. **Timeline v2's draft parts** (Claude, 2026-10-27): the wall going up in months 2–4 of year 0; the flood in years 2–3; Sanctuary 1 opening in years 3–5 and the network growing in years 5–8; survivors' line for the fall, "They abandoned us." See "Timeline v2" below. _May change with item 3._
3. **1–3 years counted from what?** (Claude, 2026-11-11, after the developer's "not likely to be 8 years in, closer to 1-2, maybe 3"). Options:
   - **A. 1–3 years since the outbreak:** the whole story (the wall, the lockdown, the breach, the fall) fits in the first year or so, and the game starts 1–3 years after it all began. The lockdown's daily life (registry, ration credits, assigned work, propaganda from late year 1) gets squeezed into months.
   - **B. 1–3 years since the fall:** the city still holds for about two years as now, falls, and the game starts 1–3 years later (3–5 years after the outbreak in all). Daily life inside the wall keeps its time; the overgrowth and the Sanctuaries have 1–3 years.
   - Claude's pick: **B**, since the lockdown years carry much of the clue material (ID cards, ration credits, propaganda, removal notices).

---

## Open: to build next

### 1. Fill in the twist
The four layers are chosen (see "The truth" above). Questions they raise:
- **Decided:** the flip and the turn (see "The turn" above). **Still open:** which part of the method the founder hid (**the process**, confirmed 2026-10-27) and where; whether the destroyed parts can ever be rebuilt (and so whether players could ever complete it, e.g. as a long-term server event); who the founder who hid his part was (he's gone with the other founders; which of their fates he met is open).
- _Superseded options:_ **how to make the flip less predictable**, i.e. a turn on top of "they released it and it got away". Options in the 2026-10-27 discussion: the containment was sabotaged (a second deliberate act); the release *worked* and the scalable cure was found, then hidden or lost; the infected brought in from nearby towns weren't what the researchers thought; three layers of truth that each feel like the final answer.
  - **Option B fleshed out (the developer's leaning, 2026-10-27), not chosen yet.** The release worked and the scalable cure method was found. Why it isn't saving the world:
    - **B1, the price:** the scalable method needs **living infected hosts**, people kept in the window between infection and turning. Mass production means farming people.
    - **B2, the power:** whoever holds the method controls who survives, inside the wall and out. The founders hid it as leverage.
    - **B3, the lost courier:** it was being carried out of the city when the city fell, and never made it (a crashed helicopter on a roof, a boat sunk in the harbor, a subway tunnel).
    - **B4, split apart:** the researcher who realized the price split the method into pieces and hid them across the city, unable to destroy the only hope. Pieces can be found; assembling them could be a long-term server event, or never fully pay off.
    - Claude's pick: **B1 + B4.** The researcher who split it may have died or turned (possibly one of the Patients). The founders know it exists and are still searching; their bank registry (§18 of the GDD) helps them track survivors and possible hosts.
- _Earlier:_ **Who caused the breach, and what made well-meaning researchers flip?** (Ties layers 2 and 3: were the safe-zone founders part of it?) Options discussed 2026-10-27, before the "good intentions" detail: leaders on purpose because the study needed a live outbreak; insiders exposing it, gone wrong; a military fail-safe; destroying evidence before an oversight team arrived; cover for the leaders' escape; a company needing a cure trial at scale; one true believer; sabotage gone wrong; orders from outside; a cult. Flip options (what turned good researchers, 2026-10-27):
  1. **The impossible ingredient:** the scalable cure needs something only obtainable from many infected people, so saving billions outside means sacrificing one city.
  2. **The strain had to evolve:** the cure only works on a later form of the strain, which only appears after spreading through a large population.
  3. **The world went dark:** contact, funding and orders from outside stopped; believing they were humanity's last chance, they took the shortcut.
  4. **Someone they loved:** the lead researcher's child was infected; the slow route would never save them.
  5. **Hubris, "we can contain it":** they ran out of subjects and planned a small controlled release they were sure they could contain. It got away.
  6. **Ordered to, under threat:** what's left of the outside authority threatened to cut supplies or worse.
  7. **A rushed cure:** they knowingly released an unproven cure because people were dying, and it backfired.
  8. **Infiltrated:** backers with another agenda quietly took over; the good researchers realized too late.
  Claude's pick: **3 + 1 + 5** (pressure, then the math, then the hubris).
- **What do the safe-zone founders want now?** _Superseded (2026-10-27): the founders voted for a unanimous cover-up, and they are gone; the safe zones are run by what's left of the Force._ The remnant mostly wants to survive (the developer: "for preservation"). Open: what the higher-ups who know want. _Answered (2026-10-27): no one is after the method at release; that may change as lore gets discovered._

### 2. Timeline v2 (2026-10-27, new chat)
**Decided:** **8 years in total.** The game starts in **year 8**; the city fell in **year 2**, about **6 years** before (long enough for the overgrowth and the returning animals). **The wall's soldiers were ordered to let no one out** (twist layer 1 made physical). The developer confirmed both on 2026-10-27 ("4. yes").
- **Under revision (the developer, 2026-11-11, while planning the streets' look):** _"With the lore rework, it is not likely to be 8 years in, closer to 1-2, maybe 3."_ Proposed by the developer; not final until the lore revisit. **Open: 1–3 years counted from what** (see Pending proposals, item 3). Until then the 8-year table below stands as written, marked as under revision.
- _What changes with a shorter time (Claude, 2026-11-11):_ the overgrowth is lighter (weeds and grass in every crack, wild lots and parks, vines starting on low walls, saplings in tree pits and cracks; not trees through the asphalt or towers covered in vines); returning wild animals still work but fewer (coyotes, deer, foxes and turkeys already live in and around NYC); canned food, fuel and batteries are mostly still good, so cars still run (fits GDD §16); the Sanctuary network (years 3–8 in the table) has less time to grow; the "decayed" zombie tier (GDD §8) needs the fall to be at least a year or two back.

Built from everything decided. Parts marked _draft_ are still Claude's from v1 and need the developer's OK.

| When | Phase | The truth | What survivors believe |
|---|---|---|---|
| Year 0 | The outbreak | It starts outside NYC and spreads across the world within months. | Same |
| Year 0, months 2–4 _(months: draft)_ | The wall | The federal government creates **F.O.R.C.E.** to govern the city. Its military builds the wall along major highways, with checkpoints at the bridges and tunnels. NYC was picked *because* it could be sealed. **Project SANCTUS** (the Force's research agency) moves in. The **registry** begins; refugees at the wall are turned away. **The wall's soldiers are ordered to let no one out.** | "The wall keeps us safe; scientists came to find a cure." |
| Years 0–1 | The lockdown | The city holds well: ration credits, assigned work, urban farming, blackouts and solar, black markets. Screenings and blood drives; people flagged for "exposure" go to the quarantine wards (North Brother Island) and become subjects (the Patients). Expeditions bring infected in from nearby towns. Remisso exists, but only in tiny test batches. | "It's tough, but we're holding." |
| Late year 1 | The silence | The world goes dark: contact, funding and orders stop. The Force becomes independent. Rations shrink; propaganda posters start. | "The radio stopped." |
| Years 1–2 | The decision | The nearby towns are used up and expeditions are too risky. The program needs a large group of living infected, so it plans a **staged breach** (codename **AGNUS DEI**) at a small border neighborhood (NJ or the Bronx, TBD) picked for practical reasons: a horde gathered in advance, only a few extra patrols. | Nothing |
| Early year 2 | The release: **the [neighborhood] Breach** | It goes almost perfectly: much of the neighborhood is infected, then contained. The harvest gives them their subjects and the scalable method, which needs living hosts (held with Hourglass). But a few infected, drawn by a noise, slip the cordon. By the time the hosts are brought back, it's spreading fast inside the walls. **The first mass-produced batch is never made.** | "The [neighborhood] Breach" (layer 1's wording is pending). Force paperwork: "the [neighborhood] containment incident." |
| Year 2 | The fall | It spreads into populated, lightly defended areas. The military fails to contain it with the soldiers and ammunition it has, until there's no turning back; **many soldiers leave.** Daily life stops. The program collapses. The founders vote to cover it up and destroy the method's parts, but one hides his (the process). Then the founders scatter: some die, some escape the city, some hide in it. | "They abandoned us." _(draft)_ |
| Years 2–3 _(draft)_ | The flood | A hurricane floods Red Hook, Lower Manhattan and the Rockaways. | Same |
| Years 3–5 _(draft)_ | The hiding | Survivors hide in sealed apartments, subway shelters and basements. What's left of the Force (higher-ranking members, leftover military, lower ranks) regroups to survive and opens **Sanctuary 1**. Sanctos Notes and the bank registry start. | "Some survivors got organized." A rumor says it's the Force. |
| Years 5–8 _(draft)_ | The network | More Sanctuaries open, numbered in order, up to 6–7 active. One of them falls. | "There's a place that's safe." |
| Year 8 | Game start | Players come out of hiding. No wall checkpoints are manned. | |

**Still open in the timeline:** why players come out in year 8 (the radio call was rejected); when the founders' cover-up vote happened (during or after the fall); when and how the fallen Sanctuary fell; how the founders who escaped got past a wall ordered to let no one out.

**What changed from draft v1** (Claude's first version, same day): the release is the developer's staged breach (_not adopted:_ Claude's "they stopped containing it and let it spread"); "a researcher splits the method" became the founders' cover-up; the first batch is never made; the safe zones are the Force's remnant, not "survivors who got organized"; the wall's soldiers left rather than being "lost" (_not adopted:_ Claude's "pulled back to hold the Sanctuaries"); _rejected:_ players come out because the safe zones' radio started calling survivors in.

### 3. Radio
Random broadcasts from whoever is still transmitting. Candidate stations:
- **The safe-zone group's station:** weather warnings (§19), rules, news. Official, and maybe not fully honest.
- **Automated loops** still running on solar or backup power: years-old evacuation orders, research-facility recordings. Eerie, and full of clues.
- **Numbers stations:** coded broadcasts for players who like puzzles.
- **Survivor and pirate stations:** other groups, unreliable narrators.
- **Faint signals from outside the wall:** other safe zones elsewhere in the world, hinting at how bad it is out there.
- **Lore across a wipe cycle:** wipes are 6–12 months apart (§20), long enough for new broadcasts and clues to unlock over a server's life, so the story unfolds in seasons.

### 4. Factions
- **Decided:** **the Force** is the city's government (FEDRA-like); **the research agency is part of it**; **it controls the military**, which built the wall; its patrols are its enforcement; it became independent after the outside fell (see "The Force" above).
- Still open: the Force's internal structure (including the research agency's own name; its program is Project SANCTUS); the safe-zone group's origin and real goals; what else is left of the Force and its military after the fall (_decided 2026-10-27: what's left of it, former members from all its branches, runs the safe zones, Sanctuary 1–7; the military didn't collapse, it failed to contain the spread_; open: e.g., who holds the military sites); _maybe_ rare roaming military patrols in the game (the developer, 2026-10-27); other groups.
- Questions Claude raised for the safe-zone topic (2026-10-27, new chat): **who the guards and snipers are** (answered, see "The safe-zone group"); **why the traders never sell Remisso** (answered by its rarity: only test remnants exist, confirmed); **why founders hiding their past would name the currency after their secret program** (answered: it reads as "sanctuary", hidden in plain sight; see SANCTUS above).

### 5. The infection itself
- What it is, how it works, why only infected people turn, why animals don't, why fresh zombies are faster, what the antiviral does.
- **What type of infection?** The developer (2026-10-27): _"what type of infection is it, a virus? something like a fungus, etc."_ Not discussed yet.
- **Flashlights depend on it.** The developer's leaning: they will probably draw zombies, since zombies can see (GDD §19).

### 6. Lore areas
Candidates from the discussion (also points of interest): **North Brother Island** (a real old quarantine hospital), a **research lab** (e.g., Roosevelt Island), **Fort Hamilton** (a real Army base in Brooklyn) as the quarantine headquarters, **the antiviral lab**, **the fallen Sanctuary** (decided 2026-10-27), **the breached neighborhood** (NJ or the Bronx, TBD). To be redone once the truth is decided.

### 7. Special zombies
Decided: the Patient and the Host (see "The special zombies" above).
