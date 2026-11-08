# NYZ design session, 2026-10-27

Readable transcript: the developer's messages and Claude's replies only. The full export (tool calls, screenshots, metadata) is in the matching .zip.

---

### Developer (2026-10-27 10:29)

Hello, I want to use you to help me make a multilayer zombie survival game, that will kind of be a blend of Dayz, and zomboid, with some mechanics from survival games like ark and rust. I want to go into details with you VERY VERY thoroughly and keep those details noted somewhere that they wont get lost later into development. Before we begin, i want to layout the main details of the game, good?

### Claude (2026-10-27 10:30)

Yes, go ahead. The `NYZ` folder is empty right now, so we're starting from scratch.

**How I'll keep the details from getting lost:**

- **`docs/GDD.md`**: the main design document, organized by system (zombies, loot, crafting, base building, PvP, and so on). Everything we agree on goes in here.
- **`docs/DECISIONS.md`**: a dated log of every decision, especially the ones we change later. It records what we chose, what we rejected and why, so we don't argue the same point twice months from now.
- **`CLAUDE.md`** at the project root: it tells every future session to read the GDD before doing anything. The design then carries over between conversations instead of depending on my memory of this one.

I'll update these files as we talk, not in one batch at the end.

**When you lay it out**, these are the things that shape everything else. Cover them if you have answers, or tell me they're undecided:

- **Engine**: Unreal, Unity, Godot, or not chosen yet
- **Team**: just you, or others
- **Multiplayer scale**: a few friends, or 50–100+ players per server
- **Camera**: first person like DayZ, isometric like Zomboid, or both
- **Platform**: PC only, or consoles too

I'm reading "multilayer" as multiplayer; tell me if you meant something else.

Go ahead with the main details, in any order and as rough as you like. I'll organize them into the doc and ask follow-up questions where something is unclear or two ideas conflict.

I haven't created any files yet. I'll make the doc as soon as you send the first round of details.

### Developer (2026-10-27 10:31)

UE5, as of now just me, would like to bring on others if it helps but not paid, just maybe some friends or other people that see the vision and are dedicated to it

### Developer (2026-10-27 10:31)

[Request interrupted by user]

### Developer (2026-10-27 10:32)

UE5, as of now just me, would like to bring on others if it helps but not paid, just maybe some friends or other people that see the vision and are dedicated to it. Multiplayer, 100+ players per server. First person and third person like dayz. PC mainly, consoles would be awesome down the line

### Claude (2026-10-27 10:33)

I've saved all five fundamentals. Here's what's in the project now:

- [docs/GDD.md](docs/GDD.md): the design doc. It has the fundamentals, what they mean technically, team notes, a checklist of systems still to design, and open questions.
- [docs/DECISIONS.md](docs/DECISIONS.md): the dated decision log, with today's entry.
- [CLAUDE.md](CLAUDE.md): tells every future session to read the GDD first and keep both files updated.

**Three things your answers raise. They're in the doc, but you should know them now:**

1. **100+ players is the biggest technical risk in the project.** Unreal's default networking doesn't handle that many players well out of the box. Add a lot of zombies, each running AI on the server, and you have the hardest problem in the game. Most projects like this fail here. We should build a rough test with 100 players and lots of zombies early and prove it holds up, before any polished gameplay.
2. **Set up source control before writing any code.** Right now nothing is backed up or versioned. UE5 projects have large binary files, so the realistic options are Git with Git LFS, or Perforce. Perforce is the Unreal industry standard and has a free tier for small teams.
3. **Volunteers need a written agreement up front.** It should say who owns what they make and what they get if the game earns money. Unpaid projects that skip this often end in ownership fights once the game gets traction.

**Next,** tell me the core of the game: what you're taking from DayZ, from Zomboid, and from Ark/Rust. Also, is "NYZ" a working title, and what does it stand for?

I didn't save anything to my own memory, because the CLAUDE.md file already makes future sessions read the doc. Nothing is under version control yet, so these files exist only on this machine.

### Developer (2026-10-27 10:35)

for 1, how would we tes 100 players without 100 people? for 2. is that neccessary? Does ue5 not have something that can do that?

### Claude (2026-10-27 10:36)

**1. Testing 100 players without 100 people**

You use bots. You launch many copies of the game as headless clients, meaning no graphics and no sound, only networking and game logic. Each copy connects to your dedicated server the way a real player would, and a simple bot script drives it around.

- **UE5 supports this out of the box.** Launch the client with `-nullrhi` (turns off rendering) and `-nosound`. Each copy then uses a fraction of what a normal client needs.
- **Scale:** a decent PC can run a few dozen copies. For 100+, rent two or three cloud machines for an hour, which costs a few dollars.
- **The bots don't need to be smart.** They need to produce realistic network traffic: moving, sprinting, looting, opening inventories, shooting zombies.
- **Measure with Unreal Insights,** UE5's built-in profiler, which has a networking view. The numbers that matter are server tick rate, bandwidth per player, and the server's CPU and memory.
- **Bad connections:** UE5 has console commands that add fake lag and packet loss, so you can see what players on weak Wi-Fi will experience.
- **Everyday testing:** the editor can launch 2–4 players in one click (the Play menu's Number of Players setting). Use that for testing features and the bot swarm for testing scale.

The question the test answers: does the server stay smooth with 100 bots and X zombies? If it doesn't, you want to find that out in month 2, not year 2.

**2. Source control: yes, it's necessary**

I'd treat it as non-negotiable, for three reasons:

- **Backup.** At the moment, a dead drive or a corrupted file means the game is gone.
- **Undo for the whole project.** If you break something over a weekend, you roll everything back to Friday's version.
- **Working with others.** Once a volunteer joins, two people editing the same files will overwrite each other's work. Blueprints and maps are binary files that can't be merged, so you also need file locking: "I'm editing this map, nobody else touch it."

**Does UE5 have it built in?** Only partly. The editor has a Revision Control panel where you can check in work, view history and lock files without leaving Unreal. But that panel only connects to an outside system like Perforce or Git, which you still have to set up. As far as I know, Epic's fully built-in version exists only in UEFN (the Fortnite editor), not in regular UE5.

**My recommendation: Git with Git LFS (Git's add-on for large files), in a private GitHub repo.**

- It's free and simple to set up, it gives you an off-site backup, and a volunteer only needs a GitHub account to join.
- You don't have to use the command line. Use a desktop app instead: GitHub Desktop, or Anchorpoint, which is built for game developers and handles large files and locking.
- The catch is that GitHub's free storage for large files is limited, and UE projects grow quickly once you add assets. Expect to pay a few dollars a month at some point. If the team grows past a handful of people, switch to Perforce.

It's best to set this up before you create the UE5 project, so the rules that skip Unreal's cache and temp files (often 10+ GB) are already in place. Want me to set up the repository in this folder now? You'd need a GitHub account.

I haven't checked whether Git is installed on this PC. I also didn't quote GitHub's exact free storage numbers, so check their current pricing before relying on the free tier.

### Developer (2026-10-27 10:38)

Will the git not be public?

### Claude (2026-10-27 10:38)

No, it only becomes public if you choose that. When you create a GitHub repository, you pick **Public** or **Private**. With **Private**:

- **Only you can see it**, plus anyone you invite by name.
- **It's free.** Free GitHub accounts get unlimited private repositories and can invite unlimited people.
- **Volunteers are invited one at a time** with their GitHub username, and you can remove anyone's access whenever you want.

The Git repository on your PC also stays entirely local until you push it to GitHub. Nothing goes online by itself.

You can turn a private repository public later, for example to open-source the game. Once something has been public, though, people may already have copied it. So start private and only change that on purpose.

Want me to set it up? I'd create the local repository here with the UE5 ignore and large-file rules. You'd then create the private GitHub repository and give me the link, so you choose the privacy setting yourself.

I haven't checked GitHub's current storage limits for large files on free accounts. That cap is what will start costing money as the project grows.

### Developer (2026-10-27 10:39)

No, lets finish the details of the game. remind of that after we have the game mapped out? good or no?

### Claude (2026-10-27 10:39)

Good plan. I added a reminder to [CLAUDE.md](CLAUDE.md), so I'll bring up source control once the game is mapped out. That works even if we're in a different session by then. I also wrote the bot load-testing method and the private Git plan into [docs/GDD.md](docs/GDD.md), so that answer doesn't get lost.

To get back to the game, tell me the core:

- **From DayZ**, what are you taking? For example: the open world, emergent PvP, the medical system, gear looted from the world.
- **From Project Zomboid**, what are you taking? For example: deep survival simulation, skills that improve with use, the zombie horde behavior, a slow and heavy feel.
- **From Ark and Rust**, which survival mechanics? For example: base building, raiding, crafting tiers, clans, wipes.
- **The name:** is "NYZ" a working title, and what does it stand for?

Rough notes are fine. I'll organize them in the doc and ask about any gaps.

The reminder only fires if a session reads CLAUDE.md. Claude Code loads that file automatically in this folder, so it should come up as long as you work from here.

### Developer (2026-10-27 10:43)

From DayZ. the open  world, the engaging PvP, gear looted from the world. From Zomboid, deep survival simulation but not as deep, i want the game to be more enjoyable to an average player where as zomboid you take a while to learn in, zombie horde behavior.
From ark, some type of leveling to skill system that can be lost but recovered on death, base building, clans crafting. Other features i recommend may be a blend of a few different types. NYZ is kind of a place holder, for New York Z

### Developer (2026-10-27 10:44)

but nyz is more the project name than the actual game name

### Claude (2026-10-27 10:45)

I've added all of this to the Vision section of [docs/GDD.md](docs/GDD.md) and logged it in [docs/DECISIONS.md](docs/DECISIONS.md). I also wrote one thing down as a design principle: **"easy to learn for an average player."** That will be the tiebreaker on almost every system later. Whenever we're torn between a deep version and a simple one, we check it against that principle.

Two questions before we go system by system:

**1. Skills lost on death: how do you get them back?** These are the main options:

- **A. Corpse recovery:** you lose a chunk of XP when you die, and it stays on your body. Get back to your body to reclaim it. It's tense, but other players can camp your body to block you.
- **B. Catch-up boost:** you lose some levels, but you earn XP much faster until you're back to your old level. It's forgiving and nobody can grief it.
- **C. Skill journal:** a craftable item that stores your progress. Your next character reads it to recover the skills. A popular Zomboid mod works this way. It also gives raiders a reason to hit bases, because the journals are stored there.
- **A mix** of these.

I'd pick **B**, possibly with **C** added on top. B fits your "average player" goal: dying hurts, but you're never stuck at zero for long. Also, how much should be lost: everything, half, a fixed amount?

**2. Setting: is the game set in New York?** If so, is it New York City, the wider state, or a fictional region based on New York? This choice has a big effect on scope. A dense city has thousands of buildings to enter, which is a huge amount of work for a solo developer and heavy on the server. DayZ is mostly countryside with towns for that reason. A middle option is the edge of a city plus suburbs and countryside.

After these, I suggest we do **survival stats** next: which needs and conditions stay in, given "less deep than Zomboid".

I didn't put my recommendations in the doc, only your decisions. Option B goes in only if you choose it.

### Developer (2026-10-27 10:51)

B and C, and they can be burryable so the chance of ever getting found by anyone else is low. Everything lost until you find the journal, from there player levels can be maybe 60-80% recovered, but all learned skills can be recovered. SO say you die at level 80 and come back at 55 or something, you can still craft something learnd at level 80, you juust cant learn anything else from that level or on from 55

### Developer (2026-10-27 10:53)

Yes New York City, with the wider state potentially coming in a DLC. The real thing, 1:1 scale of new york (size wise, not every building or sign or mailbox etc lining up) Yes its extremely hard for a solo dev, maybe impossible. But I have you, have seen your capabilaties and think i can work with that, and your skills will likely only improve. Also we can narrow down on what parts of nyc if you want, or that can comne later and we can do survival stats, up to you

### Claude (2026-10-27 10:55)

Both are recorded. [docs/GDD.md](docs/GDD.md) has two new sections: **§5 World & setting** and **§6 Character progression & death**. Both decisions are also in the decision log.

**The skill journal: six details to settle.** Each has my suggested default, so you can reply "defaults" or change only the ones you disagree with.

1. **Your example:** back at level 55, you keep everything you learned up to 80. Can you only learn new things a level-55 character could, with more opening up as you level? *Default: yes.*
2. **Snapshot or live?** *Default: snapshot.* The journal only knows what you'd done when you last wrote in it, and writing in it is a quick action. That makes "update your journal before a risky raid" a real decision.
3. **Other players:** *Default: only the owner can read it, but anyone who finds it can destroy it.* Nobody can steal your progress, but raids and lucky finds still matter.
4. **Catch-up boost before you find the journal?** *Default: yes, starting from level 1.* That way a lost journal doesn't feel hopeless, which fits your "average player" principle.
5. **How many journals?** *Default: one active journal. Writing a new one makes the old one blank.* Otherwise people bury ten copies and dying stops meaning anything.
6. **How it's made and buried:** *Default: we decide this when we design crafting and items.*

**NYC at 1:1 scale.** I wrote the numbers into §5 so they don't get lost:

- NYC has about 780 km² of land, roughly 3.5 times the size of DayZ's main map.
- It has around a million buildings, so we'll need a rule for which ones can be entered.
- 100 players spread across the whole city is about half as crowded as a DayZ server. We'll need hotspots, or a smaller launch area, to keep PvP encounters frequent.
- The realistic way to build it is to generate the city from real map data (streets, building footprints, heights) using Unreal's built-in procedural tools, then hand-detail the key locations. That's an approach I can help with a lot.

**On relying on me:** I can write the C++ and Blueprint logic with you, build the tools that generate NYC from map data, and keep this design consistent. Blender is also connected to this session, so I can work on models there. I can't operate the Unreal editor directly from here, and I can't judge how the game feels to play. Playtesting is yours.

**Next:** once you've answered the journal questions, we'll do **survival stats**. Which parts of NYC to include can wait until the gameplay systems show what the map needs.

The 780 km² and "about a million buildings" figures are from memory, not checked against a source today. They're close enough for planning but shouldn't be quoted anywhere official.

### Developer (2026-10-27 10:57)

after you reply to this go straight back to topic i dont want to get sidetracked just curious, but whats the limit on how much yu can put in the mds?

### Claude (2026-10-27 10:57)

**No real limit on the files themselves.** They're plain text, and a design doc would never get big enough for size to be a problem.

**The practical limit is how much I can hold in view at once.** I don't remember previous sessions. Each session I re-read the files, and everything I read takes up room in my working memory for that conversation. In practice:

- **CLAUDE.md** loads automatically every session, so it should stay short. It's a pointer and a set of rules, not the design.
- **GDD.md** I only read when needed. It can grow to hundreds of pages, but once it gets large I'd read it in pieces instead of all at once.
- **When it gets big**, the fix is to split it: one file per system (`docs/systems/zombies.md`, `docs/systems/crafting.md`, and so on), with the GDD as a short index linking to them. Then I only read the system we're working on. I'll do that split when the doc starts getting long, so nothing gets lost and nothing gets cut.

---

**Back to the skill journal.** Reply "defaults" or change any of these:

1. Back at level 55, you keep everything learned up to 80, and new learning is limited to level 55 until you level up. *Yes*
2. Journal is a **snapshot**: it only knows what you'd done when you last wrote in it. *Snapshot*
3. Only the owner can read it; anyone can destroy it. *Yes*
4. Catch-up boost applies from level 1, even before you find the journal. *Yes*
5. One active journal; writing a new one blanks the old one. *Yes*
6. How journals are made and buried: decided during crafting/items. *Later*

### Developer (2026-10-27 11:00)

1. Yes, maybe not those exact numbers but that system.
2. Yes, unless you think otherwise. Going foward, if i say yes it also means unless you think otherwise
3. Not sure yet, may have to swing back to this idea but probably yes.
4. Yes.
5. No, can have multiple.
6. With a shovel, on any ground that is diggable like dirt or soil

### Claude (2026-10-27 11:02)

Recorded in [GDD §6](docs/GDD.md) and the decision log. I also saved your rule that "yes" means "yes, unless I think otherwise", so future sessions will speak up when they disagree.

Two notes on your answers:

- **Multiple journals:** I'm fine with this. Each journal is a snapshot, so keeping ten copies up to date takes ten writing sessions. That limits the problem I was worried about.
- **Burying needs dirt:** most of NYC is concrete, so journals end up in parks, yards, empty lots and riverbanks. That makes Central Park and Prospect Park valuable hiding places. I like that, and it's in the doc.

---

## Survival stats

Here is my proposal, built around "easy to learn": a few stats you always see, conditions that only show up when you have them, and one obvious fix for each.

**Always shown (5)**

| Stat | Fix |
|---|---|
| Health | Heals slowly when you're fed, watered and not hurt |
| Food | Eat |
| Water | Drink |
| Stamina | Rest; used up by sprinting, melee and climbing |
| Body temperature | Clothing, shelter, fire; being wet makes you colder |

**Conditions (only show up when you have one)**

| Condition | Cause | Fix |
|---|---|---|
| Bleeding | Cuts, gunshots, bites | Bandage or rag |
| Broken leg | Falls, heavy hits | Splint; until then you limp and can't sprint |
| Wound infection | Wounds left untreated | Disinfectant or antibiotics |
| Sickness | Rotten food, dirty water | Medicine and rest |
| Cold | Too cold or wet for too long | Warm up, medicine |
| Zombie infection | Bites and scratches | **Decided when we design zombies** |

**Cut, because it's Zomboid-level depth:** sleep and fatigue, boredom, unhappiness, stress, panic, nutrients (protein, carbs, fat), body weight, and separate health for each body part.

**Two things for you to decide:**

1. **Being knocked out.** In DayZ a big hit or a bad fall can knock you unconscious, and other players can then tie you up or rob you. It creates a lot of PvP stories and needs no extra stat on screen. *My suggestion: yes.*
2. **Water is a real problem in NYC.** The rivers around the city are salt or brackish water, so you can't just drink from them. Fresh water comes from bottles, rain collection, reservoirs (like the one in Central Park) and taps for a while early on. Dirty water has to be boiled or purified. *My suggestion: yes, make this part of the game.* It's realistic and gives the city its own survival flavor.

Answer per row or per section, or say "yes" to all of it.

This is a proposal, not a decision, so nothing about survival stats is in the doc yet. I'll write it in once you answer.

### Developer (2026-10-27 11:24)

1.100% yes.
2.Yes good. 
As for the cuts, while they are zomboid level depth i was thinking we have some similar systems, but they dont run out nearly as quick as zomboid, so it doesnt get to the point where you're just in a state of 24/7 stress/ boredum, unhapiness, it should take way longer to get depressed or unhappy at that, OR have way more options to cure them etc. As for tired and fatigue, we can cut that entirely. I want stress, bored, and happiness, no panic but yes to nutrients, but they wont be as critical as they are in zomboid. If im not mistaken, dayz has or had some kind of calorie system. Main stats and conditions, all yes

### Claude (2026-10-27 11:26)

Recorded in [GDD §7](docs/GDD.md) and the decision log: the main stats, conditions, knock-outs, NYC water and the cuts.

On DayZ: you remember right. DayZ tracks food as calories and has a stomach that can overfill, so if you eat too much you throw up. It doesn't track separate nutrients the way Zomboid does.

I changed one thing, per your "unless you think otherwise" rule. I replaced **"taps work for a while early on"** with **rooftop water towers**, the wooden tanks on NYC roofs. On a persistent server "early on" doesn't mean anything, and the water towers are a recognizable NYC landmark that holds water. I also learned the **Bronx River** is fresh water, the only exception to "the rivers are salt." Both are in the doc, marked "confirm."

---

## Mood: my proposal

Mood only appears on screen when it starts getting bad, like the conditions do. A player who eats decent food and spends some time at their base or with friends should rarely see a mood warning. It should take hours of neglect, not minutes.

| Mood | Gets worse from | Gets better from | When it's bad |
|---|---|---|---|
| **Stress** | Fights, zombies close by, getting hurt, being hunted | Being at your base, being near clanmates, cigarettes, alcohol, time away from danger | Shakier aim; stamina recovers slower |
| **Boredom** | Long idle stretches, repeating the same task | Books and magazines, music (radio, instruments), cards and games, exploring new places, being around other players | Slower XP gain |
| **Happiness** | Bad food, being wet, cold or sick, long stress or boredom | Good cooked meals, coffee, alcohol, music, comfort items, a comfortable base | **Low:** slower healing. **High:** small XP bonus |

The main idea: **being near your clanmates reduces stress and boredom.** That ties mood to clans and gives players a reason to group up, which suits a multiplayer game better than Zomboid's solo design.

## Nutrients: my proposal

- **Food is counted in calories**, like DayZ.
- **Three food groups tracked in the background:** protein (meat, fish, beans), carbs (bread, rice, pasta, chips) and vitamins (fruit, vegetables).
- **No extra bars on screen.** There's one status instead:
  - **"Well fed"** for a balanced diet: slightly faster healing and stamina.
  - **"Poor diet"** when a group has been missing for a long time, like living on canned beans: slightly slower healing and lower maximum stamina.
- **A poor diet never kills you on its own.** You fix it by eating the missing food group.
- Each food's tooltip shows which groups it covers.
- **When your stomach is full, you just can't eat more.** No throwing up from overeating, because that's a trap new DayZ players fall into.

---

**To answer:**

1. Mood proposal: yes, or changes?
2. Nutrient proposal: yes, or changes?
3. Should body weight and separate health per body part both stay cut? You didn't mention them.
4. Water towers instead of "taps early on": OK?

The Bronx River detail is from memory and I haven't checked it against a source. It's harmless if wrong, but double-check before it ends up in any in-game text.

### Developer (2026-10-27 11:30)

1. Yes no changes right now.
2. Yes, with maybe a deeper menu to show what type of food is missing from the diet
3. No, I want seperate health per body part. Although its in depth, a good UI makes it easy for a new player to understand. Bodyweight can stay cut
4. yes

### Claude (2026-10-27 11:31)

All recorded in [GDD §7](docs/GDD.md) and the decision log. Body-part health is in, and I agree with your reasoning: the UI is what makes it easy or hard to learn.

## Body-part health: my proposal

**Parts (6):** head, torso, left arm, right arm, left leg, right leg. Zomboid has 17, which is too many to read at a glance. Hands go with the arms and feet go with the legs.

**How damage works** (similar to Escape from Tarkov):

- Each part has its own health, and your total health is all the parts added together.
- **If your head or torso reaches zero, you die.**
- **If an arm or leg reaches zero, it's "destroyed."** You get a heavy penalty, and any more damage to that limb spreads to the rest of your body. A **surgery kit** fixes it, but the limb comes back with lower maximum health until it fully heals over time.

**What each part does when it's hurt:**

| Part | When hurt | Worst case |
|---|---|---|
| Head | Blurry vision, ringing ears; head hits can knock you out | Death at zero |
| Torso | Stamina recovers slower | Death at zero |
| Arms | More aim sway, slower reloading and melee | **Broken arm:** can't aim properly until splinted |
| Legs | Slower movement | **Broken leg:** you limp and can't sprint until splinted |

That turns the "broken leg" condition into **broken limb**, covering arms and legs.

**Conditions belong to a body part.** For example, bleeding is on the left arm, so you bandage the left arm. A bite is on the right leg. That will matter again when we design zombie infection.

**UI, so new players aren't lost:**

- **HUD:** a small body outline appears when you're hurt. Each part is colored green, yellow, red, or black when destroyed.
- **Health screen:** click a part to see its injuries, then drag a bandage or splint onto it.
- **"Treat" button:** one click uses the best item you have on your most urgent injury. New players never have to learn the details, while experienced players can treat each part by hand.

**Armor per body part follows from this:** helmets protect the head, vests protect the torso, and so on. I'd design that when we get to items and loot.

**To answer:** yes, or changes? The main choices are 6 parts, head or torso at zero means death, destroyed limbs fixed with a surgery kit, and the one-click Treat button.

The Escape from Tarkov model is a reference, not a copy. Its numbers and exact rules aren't in the doc, only the general pattern.

### Developer (2026-10-27 11:39)

For the most part good, excpet maybe when you have a broken arm you cant aim properly with a rifle or two armed weapon, if a pistol, they can aim with the good arm. Maybe some system in character design where you pick left handed or right handed, and players dont know its relavence till theyre in that type of scenerio

### Claude (2026-10-27 11:40)

Good change. It's recorded in [GDD §7](docs/GDD.md) and the decision log. I also removed two stale lines from the GDD that pointed at questions we've already answered.

## Handedness: my proposal

**What it changes:**

| Situation | Effect |
|---|---|
| Broken **off-hand** arm, using a pistol | Your main hand does the work, so there's almost no penalty: a little extra sway |
| Broken **main-hand** arm, using a pistol | You shoot with your off hand: noticeably more sway and slower reloads |
| One-handed melee (knife, machete) | Same pattern as pistols |
| Throwing (grenades, bottles, rocks) | Off-hand throws are shorter and less accurate |

**One suggestion:** handedness changes gameplay only, not animations. Everyone holds rifles the same way in normal play. Two reasons:

1. **Cost:** a mirrored animation set for every weapon doubles the animation work, and mirrored guns look wrong (ejection port and bolt on the wrong side).
2. **It keeps your secret:** if left-handed characters visibly held guns differently, players would know handedness matters before it comes up.

The only extra animations needed are one-handed pistol animations for each hand, which the broken-arm rule requires anyway.

**First-time hint:** the first time handedness matters, a short message pops up, for example *"Your main arm is broken: aiming with your off hand."* Players still discover it in the moment, but they aren't left confused about why their aim got worse. That follows the "easy to learn" principle.

**One more question:** with a broken arm, can you still fire a rifle from the hip with a lot of sway but not aim down the sights? Or can't you shoot it at all? *My suggestion: hip fire only, no aiming down the sights.* You can still shoot in a desperate moment, just badly.

**To answer:** yes to the handedness proposal, or changes? And hip fire only for rifles?

Once these are settled, survival stats is done apart from zombie infection. I'd suggest **zombies** next, since infection, hordes and server performance all depend on them.

### Developer (2026-10-27 11:43)

Hipfire only. I do like the idea of it not being a secret, making aiming for offhand intentionally a vviable strategy. But yeah, i does cost a lot more and require more animation work. Put that as maybe, but just gameplay for now

### Claude (2026-10-27 11:44)

Recorded. I also added a **"Maybe later"** section ([GDD §9](docs/GDD.md)) for parked ideas like this one, so they don't get lost. The entry notes the conflict: if visible handedness is ever added, handedness stops being a secret.

Survival stats is now done except zombie infection, which brings us to zombies.

---

## Zombies: my proposal

**1. Types and speed: they come from how fresh the zombie is.**
- **Fresh zombies** (recently turned) **run**. **Decayed zombies** **shamble**. That gives a natural, in-world reason for a speed mix: mostly shamblers, with some runners.
- **Variants by what they were:** civilian, police, firefighter, military, hospital staff. What they wear decides their toughness and their loot. Military zombies have armor and drop military gear; police drop pistols and ammo. That's DayZ's approach.
- **No special zombies** (spitters, tanks and so on, like Left 4 Dead). They keep the game grounded.

**2. Senses: hearing matters most.**
- **Hearing:** gunshots carry far, car alarms and breaking glass less, footsteps only close by. Crouching and walking slowly keep you quiet.
- **Sight:** worse at night, in rain and in fog.

**3. Hordes, Zomboid-style.**
- Noise **pulls zombies together**, and groups **migrate across the city** over time.
- A loud gunfight can bring a horde down on everyone nearby, so noise becomes a weapon and a risk in PvP.
- Cleared areas **stay cleared for a while** and refill slowly as hordes wander in. Zombies don't pop back into existence, so clearing an area means something.
- NYC adds **bridges and tunnels** as natural chokepoints, and **subways** as dark, packed danger zones.

**4. Killing them, which ties into body-part health.**
- **Only head damage kills.**
- Body shots stagger them and can knock them down.
- **Destroyed legs turn them into crawlers.**

**5. Infection: curable, but the cure is rare.**
- **Bites** have a high chance of infecting you; **scratches** a low one. Clothing on the bitten body part can block it, so a leather jacket protects your arms.
- Infection is cured only by a **rare antiviral** found in hospitals and labs. That turns hospitals into **high-value PvP hotspots**, which helps the player-density problem at 1:1 scale.
- **If infection kills you, you turn into a zombie wearing your gear.** Your friends have to put you down.

**6. Zombies against bases.**
- Noise attracts them to bases, and **large hordes can break weak doors and walls**. Loud bases attract trouble.
- Zombies can climb **low fences** but **not ladders**, which gives players a reason to use ladders when designing bases.

**To answer:** yes, or changes per number.

Two things I'm deliberately leaving for later. **How many zombies per server** depends on the load test. **Day and night behavior** fits better with weather and day/night.

### Developer (2026-10-27 11:54)

I want a few different speeds, so recently turned ones should move faster, but maybe not run, something between a run and a walk. Varients by what they were yes. Special zombies, but extremeley extremely rare, and harder to kill. But not overkill, 1, 2 special types at most. They could also spawn at lore areas ingame(we will need to dive deeper into lore). 

2. Good, except if they hear when close and crouched can come from the type of footwear you have on, so boots or something will be clunkier and louder, and sneakers quiter etc. Yes to sight.
3. Yes to all
4. Yes
5. Yes
6. Yes, for the most part. Noise will attract to bases, The horde breaking walls and stuff will come from the tiers of base building materials. So Large hordes and small hordes easily take down a t1 wall, but a small horde wouldnt even damage a t4, it would take a large horde damaging it over time. We can go more in depth on this when we get to base building. By climb low fences, do you mean fences taller than the average person, or the fences that they can kind of just hobble over?

### Claude (2026-10-27 11:55)

All of it is in [GDD §8 Zombies](docs/GDD.md) and the decision log. I also added **Lore** to the systems checklist as its own deep dive, since special zombies depend on it.

**Your fence question:** I meant the low ones they can hobble over, waist-high or lower, like a garden fence or a low wall. They'd stumble over slowly and sometimes fall. **Fences taller than a person stop them completely.** The only way through is breaking them, and that follows your tier system: a horde flattens a tier 1 fence, but a small horde can't touch a tier 4 one. Is that what you want?

**Speed tiers: my proposal**

| Tier | Speed | Where they're found |
|---|---|---|
| **Fresh** | Between a walk and a run | Rare. Near recent deaths, and players who died of infection |
| **Weathered** | Normal walk | Most zombies |
| **Decayed** | Shamble | Common in old, settled areas |
| **Crawler** | Crawl | Any zombie with destroyed legs |

Because no regular zombie runs at full speed, **a sprinting player can always outrun zombies until their stamina runs out.** I think that's good for the "easy to learn" principle, because panicking players have a way out. Hordes stay dangerous because there are so many of them and they wear down your stamina. Special zombies could be the exception that can keep up with you. We can decide that with lore.

**Two footwear questions:**

1. **Should footwear also change how loud you are to other players?** *My suggestion: yes.* The same footstep sound feeds both zombie hearing and player audio. Sneakers then become a real PvP choice for sneaking up on people.
2. **Should boots protect more to balance being louder?** *My suggestion: yes.* Boots would block more bites to the legs and feet, keep you warmer and last longer, while sneakers are quiet but wear out and protect less. That makes footwear a real trade-off, not just "sneakers are better."

**To answer:** the fence rule, the speed tiers, and the two footwear questions.

I'd suggest **base building** next. It now connects to several decisions already made: zombie damage by tier, ladders, burying journals, and comfort items for mood.

### Developer (2026-10-27 11:56)

1. Yes
2. yes
3. So for the fence rule, yes the can.

### Claude (2026-10-27 11:57)

Recorded in [GDD §8](docs/GDD.md) and the decision log.

**One thing you didn't answer:** the four zombie speed tiers (Fresh, Weathered, Decayed, Crawler). Yes, or changes? Until then they're still listed as open.

---

## Base building: my proposal

**1. Two ways to build**
- **Fortify existing buildings.** Claim an apartment, a storefront, a brownstone or a rooftop, then barricade and upgrade its doors and windows. In NYC this is the natural way to build a base.
- **Build from scratch** with snap-together pieces (foundations, walls, floors, doors, stairs) in open spaces: parks, empty lots, rooftops.

**2. The original city buildings can't be destroyed.** Only what players add can be damaged, so raiders have to come through doors, windows and player-built walls. Destructible city buildings would be an enormous technical cost, both for the server and for 1:1 NYC. It also means an apartment on the fifth floor with one barricaded door is a strong base, which is a nice tactical choice for players.

**3. Four material tiers**

| Tier | Material | Zombies (already decided) |
|---|---|---|
| T1 | Wood, scrap planks | Any horde breaks it easily |
| T2 | Sheet metal, reinforced wood | Small hordes slowly; large hordes quickly |
| T3 | Brick, concrete blocks | Small hordes barely; large hordes over time |
| T4 | Steel, reinforced concrete | Small hordes can't damage it; large hordes wear it down over a long time |

**4. Building is loud.** Hammering and sawing attract zombies, so building has a risk. Building fast in a dangerous area means fighting while you build.

**5. Claiming and decay**
- A **claim item** placed in your base sets an area where only you and your clan can build.
- **Bases decay if nobody from the clan visits for X days.** Visiting resets the timer. This is simpler than Rust's upkeep system, where you have to pay materials to keep a base standing.
- **Each clan has a cap on how many pieces it can build.** Every piece is something the server has to keep track of, and with 100+ players, server load is a real concern.

**6. Raiding**
- Higher tiers need better tools or explosives to break: a sledgehammer and crowbar for T1, power tools for T2–T3, explosives for T4.
- **Raiding is loud too, so it attracts hordes.** Raiders have to deal with zombies arriving mid-raid.

**7. Raiding while the owners are offline is your call.** This is the biggest decision here:
- **A. No protection** (Rust): anything goes, which is brutal for casual players.
- **B. Raid hours:** bases can only be raided during set hours, chosen per server.
- **C. Offline protection:** bases take much less damage while the whole clan is offline. It only starts 15–30 minutes after the last member logs off, so you can't log out in the middle of a raid to save your base.

*My suggestion: C, with a server setting to switch to A or B.* Getting wiped while you sleep is the top reason casual players quit Rust, and it clashes with your "average player" principle.

**8. Locks:** code locks on doors, with clanmates getting access automatically.

**9. Where you can't build:** bridges, tunnels, subway entrances, player spawn areas, and loot hotspots like hospitals. Otherwise players could block chokepoints or camp the best loot.

**To answer:** yes, or changes per number. Number 7 especially.

I left out respawning at your base (beds or sleeping bags). It belongs with death and respawn, and we can do that next if you want.

### Developer (2026-10-27 12:07)

Zombie speed tiers are good.

1.I like the idea of fortifying existing ones, but doesnt thaat add a lot for us? in a decaying nyc, fortifying an abandaoned building would likely mean lots of just giant open spots from decay and or bombing, having to be filled in/ modeled. It is a good system, and i think a combination of both could work.

2. agreed.
3. Good
4. Yes but not insanely loud, maybe a block or two if the construction is outside or at the edge of a building(like a window or door), and a muffled 1 city block radious for inside a building fully

### Developer (2026-10-27 12:19)

<pasted_content id="6fbc">
Zombie speed tiers are good.

1.I like the idea of fortifying existing ones, but doesnt thaat add a lot for us? in a decaying nyc, fortifying an abandaoned building would likely mean lots of just giant open spots from decay and or bombing, having to be filled in/ modeled. It is a good system, and i think a combination of both could work.

2. agreed.
3. Good
4. Yes but not insanely loud, maybe a block or two if the construction is outside or at the edge of a building(like a window or door), and a muffled 1 city block radious for inside a building fully
</pasted_content id="6fbc">

5. Yes, except the cap shouldnt feel very limiting on players.
6. Raiding Yes, but i dont want raiding to be easy by any means, so finding the stuff required to do it shouldnt be easy.
7. C with a server setting.
8. Yes
9. IDK i kinad like the idea of chokepoints being blocked off or held by clans, but it would ruin it if every clan did it. So they can build there, with major inconviences (Bridges Tunnels, subway entrances, NOT PLAYER SPAWNS, Maybe not loot hotspots, or if yes to loothot spots, the loot wont respawn with the active buildings nearby so they cant abuse it

### Claude (2026-10-27 12:20)

All recorded in [GDD §9](docs/GDD.md), with the speed tiers in §8.

**On #1, fortifying is a lot of work, but it can be kept cheap.** The holes don't need custom modeling if we set up one rule early:

> The city's building kit and the player building pieces use the **same grid**.

We already plan to generate NYC from modular building pieces (§5). A hole from decay or bombing is then just a missing piece on that grid, and players patch it with the same walls and floors they use for building from scratch. That means one system and no custom models for each hole. Only some building types can be claimed (houses, brownstones, small shops, some apartments), which keeps it manageable.

This has to be decided **before any building models are made**, because changing the grid later means remaking all of them. *My suggestion: yes.*

**On #9, the chokepoint inconveniences. My proposal:**
- **Hordes travel through chokepoints.** Bridges and tunnels are natural migration routes, so a base there takes constant zombie pressure.
- **No claim item and no storage there.** It's an outpost you hold, not a home, so nothing valuable can be stored there.
- **Faster decay**, so holding it means showing up often.
- **A small piece cap there:** enough for a gate and walls, not a fortress.

Together these make holding a bridge possible, but it's a commitment most clans won't bother with.

**On loot hotspots, a warning about the "loot doesn't respawn" option.** As written, someone could place one wall next to a hospital and shut off its loot for the whole server. That's cheap griefing. A fix: only a **claimed base** blocks loot respawns, not loose pieces, and unclaimed pieces near hotspots decay within hours. If that's too fiddly, banning building at hotspots is the simpler choice. *My suggestion: ban it.* Hospitals stay contested ground, which is what keeps them PvP hotspots.

**On "a city block":** Manhattan blocks are about 80 m one way and about 250–280 m the other. *My suggestion: 1 block = 100 m for game purposes.* Building outside is then heard 100–200 m away, and fully inside 100 m away, muffled.

**To answer:** the same grid, the chokepoint list, the hotspot ban, and 1 block = 100 m.

**Next**, I'd suggest **death and respawn**, since bases raise the question of whether you can respawn at your base (beds or sleeping bags).

The Manhattan block measurements are from memory, not checked against a source.

### Developer (2026-10-27 12:25)

1. yes to a degree, like if i want to add model that i ended up finding later for fab or something, i should be able to add it to the grid somehow. 9. Yes to the hordes it makes sense, no the the no claim and storage, if they decide to build in a dangerous area, they should be ready to hold it down or pay the conseqeunces. Thats a lesson you learn quickly after 1 or two goes. Faster decay yes, no smaller piece cap yet, maye down the line. I guess we can ban major loot hotspots, but not smaller hospitals clinics, schools,etc, only major ones, and the loot not respawning will only be in the claimed base are not whole surrounding area

### Claude (2026-10-27 12:26)

All recorded in [GDD §9](docs/GDD.md). The smaller chokepoint piece cap went into **"Maybe later."** Making the no-respawn rule apply only inside the claim area also fixes the griefing problem I raised.

**On the grid "to a degree", my suggested method:** only the structural pieces have to follow the grid (walls, floors, door and window openings), because those are what players patch. Any model you find later, on Fab or elsewhere, can then go in one of two ways:
- **Fitted to the grid:** resize or pad it so its walls line up. That's a quick job per model in Unreal or Blender, and afterwards it supports patching like everything else.
- **Used as-is:** as a building that can't be claimed (a landmark, a unique building) or as decoration. Those never need to match the grid.

Any asset works; only claimable buildings need to line up.

**Still unanswered:** is 1 city block = 100 m for building noise?

---

## Death & respawn: my proposal

**1. Where fresh characters spawn**
- **You pick a borough, and you spawn at a random point inside it.** On a 1:1 NYC map, being able to spawn near your friends matters a lot.
- Spawn points are spread out and random, so there's nothing to camp. (No building at spawns is already decided.)

**2. Respawning at your base**
- **Sleeping bags:** cheap, with a long cooldown between respawns.
- **Beds:** expensive, with a short cooldown. They also count as comfort items for mood.
- **You can share them with clanmates.**

**3. What you lose:** everything you were carrying stays on your body. Your body stays in the world for a while (*suggested: 30 minutes*), and anyone can loot it, including you if you get back in time.

**4. Starting kit:** basic clothes, one bandage, a small snack and a flashlight. For NYC flavor, add a **MetroCard with $0.00 on it**, a joke item that could later tie into the lore.

**5. Progression on respawn:** you start at level 1 with the catch-up boost (already decided), until you find your journal.

**6. Logging out**
- **DayZ-style:** your character stays in the world for a short timer (*suggested: 15–30 seconds*) and then disappears. A longer timer applies if you were just in a fight, so you can't escape a fight by quitting.
- *Not Rust-style:* in Rust your character keeps sleeping in the world after you log off, where anyone can kill and loot it. That clashes with your choice of offline raid protection, because protecting the base but not the player inside it makes no sense.

**7. Spawn protection: none.** It's usually abused, and spread-out random spawns already make spawn camping hard.

**To answer:** yes, or changes per number, plus the 100 m city block.

The 30-minute body timer and the 15–30 second logout timer are starting points. The real numbers come from playtesting.

### Developer (2026-10-27 12:33)

For 1 city block being 100m depends on each block, cause they are not all the same irl. The street layout/terrain im aiming for 1:1 or damn near it, buildings not as important. So the units depends on the map development i  guess.

1. Yes, you pick a bourough, and neighborhood(Higher loot neighborhoods will just not be spawn points, so just a few select spawn neighborhoods. That makes finding friends quicker. Spawn points are spread out randomly throughout each neighborhood.
2. Yes, but cannot place sleeping bags within x distance of another claimed base. Beds yes. Share them yes.
3. Yes, but your body will turn depending on how you died. So you may have to track it down. They shouldnt turn instantly though. Yes anyone can loot it. 
4. yes, but no metrocard, they've been phased out years ago. 
5. yes.
6. Dayz style.
7. Extremely extremely minimal, like you shouldnt die when your loading into a server and still have a black screen but loaded on their end first. I think 30 second logout timer is good

### Claude (2026-10-27 12:34)

All recorded in [GDD §10 Death & respawn](docs/GDD.md). Building noise will be set in meters during map development, and the MetroCard is gone. I also updated the zombie section, so "Fresh" zombies now include players' bodies that turned.

## Which deaths turn your body: my proposal

**Rule:** your body turns **if you were infected when you died, whatever actually killed you.**

| How you died | Turns? |
|---|---|
| Died of zombie infection | Yes |
| Killed by zombies (bitten while dying) | Yes |
| Infected, but killed by a player, a fall, bleeding and so on | Yes |
| Not infected (player, fall, cold, starvation) | No |
| **Killed by a head hit** | **Never.** Destroying the head stops it, the same rule as for zombies |

- **Turning time:** a random 3–10 minutes. That's enough for clanmates to get to your body, but not enough to always be safe.
- **A tactic this creates:** if you kill an infected enemy with a headshot, their body won't turn and walk off with their gear.

Whether everyone carries the virus, as in The Walking Dead, is a lore question. The rule above assumes **only infected people turn**. If lore later says everyone carries it, we change one line.

---

## Next: skills and progression (Ark-style): my proposal

**1. XP comes from doing things:** killing zombies, crafting, building, healing, exploring new places, and surviving.

**2. Each level gives learning points.** You spend them to learn things: recipes, building pieces, and abilities such as faster bandaging. These are the "learned skills" the journal restores. They're grouped by category: **Building, Weapons & Repair, Medical, Cooking & Farming, Mechanics (vehicles), Survival** (traps, fishing, tracking).

**3. No raw stat points.** Ark lets you put points into health, stamina and carry weight. I'd leave that out: high-level players are stronger because they can craft and build more, not because they're tankier. That keeps PvP fair for new players and makes losing levels on death hurt less.

**4. You can't learn everything.** There are fewer total points than there are things to learn, so players specialize and clans split roles: medic, builder, mechanic. It's another reason to group up.

**5. Re-spending points:** possible with a rare item. *Suggested:* a "Life Lessons" book found in the world.

**6. Level cap:** a placeholder of 100, tuned later.

**To answer:** the turning rule and the 3–10 minutes, then yes or changes per number on skills.

The turning rule depends on lore we haven't written yet. If the lore changes, this is the decision to revisit.

### Developer (2026-10-27 12:39)

Turning time should be longer 30minutes to an hour, its gonna be a 1:1 manhattan map, we want players to actually have a chance of getting back in time in such a large map. Everything else good. Can fit the lore around this or make connection.

1.Yes

2. Yes but like two seperate categories. Like engrams vs individual stat point increases, but instead of stat increases it can be either skills or crafting recipes, and the other will link to the opposite (skills/crafting)
3. Agreed.
4. Agreed
5. Agreed, method of doing it though will be differnt.
6. agreed.

### Developer (2026-10-27 12:40)

I think the ARK style stat points could = to skills for this, and engrams is recipes

### Claude (2026-10-27 12:41)

That clears it up, and it's a clean mapping. It's recorded in [GDD §6](docs/GDD.md):

| Ark | NYZ | Spent on |
|---|---|---|
| Stat points | **Skill points** | Abilities (faster bandaging, etc.) |
| Engram points | **Recipe points** | Crafting recipes and building pieces |

The 30–60 minute turning time and the turning rules are in §10. Two follow-ups came out of your answer:

**1. The body timer no longer fits.** Bodies that *don't* turn were set to disappear after 30 minutes. That's now shorter than the turning time, so an infected body would stay in the world longer than a healthy one. By your own reasoning (a big map, players need time to get back), *I suggest raising it to 60 minutes.*

**2. You said "1:1 Manhattan map."** Until now the doc says NYC at 1:1 with **which parts are in still undecided**. Is the launch map **Manhattan**? If so, that answers one of the biggest open questions. It also affects player density in a good way: Manhattan is about 59 km², a quarter of DayZ's map size, so 100 players would actually run into each other. I haven't changed the doc until you confirm.

Once those are answered, I'd suggest **loot, items and inventory** next. Crafting, raiding materials, armor per body part and the journal all depend on it.

The 59 km² figure for Manhattan is from memory, not checked against a source.

### Developer (2026-10-27 12:47)

1. Raise to 2 hours, can be difficult to get back and even games like ark give you a lot of time. 
2. Sorry my fault, shouldve clarified. Something like this?

### Claude (2026-10-27 12:48)

No problem, the screenshot makes it clear. I saved it in the project as [docs/images/launch-map-area.webp](docs/images/launch-map-area.webp), so it won't get lost with the chat. I also recorded the area and the 2-hour body timer in the GDD and the decision log.

**What I read from your outline (782.59 km², 105.69 km perimeter):**
- **In:** Manhattan, the Bronx, Brooklyn and Queens.
- **Also in:** a strip of **New Jersey** along the Hudson (Fort Lee, Hoboken) and the western edge of **Nassau County** (Great Neck, Elmont, Valley Stream).
- **Out, it looks like:** **Staten Island.** It sits west of your southwest edge.
- **Lots of water:** the Hudson, the East River, Jamaica Bay and part of the harbor are inside the outline, so the actual land is noticeably less than 782 km².

Is that right? In particular, is leaving out Staten Island intentional (maybe for the state DLC), and are the NJ and Nassau slices intentional?

**Three things this raises:**

1. **Save the exact outline.** In Google Earth, export the shape as a **KML file** and put it at `docs/map/launch-area.kml`. A screenshot is fine for us to talk about, but when we generate the map from real data, I'll need the exact boundary.
2. **The map's land edges need a reason to exist.** Water handles most sides naturally. But in NJ, Nassau and the north Bronx, the map just stops on land. *My suggestion: a **military quarantine wall** along the land edges.* It's an in-world reason for the border, a lore hook (who built it, and is anyone still guarding it?), and a natural way to expand later: the DLC "opens the wall."
3. **Player density:** this is basically the full-NYC size I worried about earlier, so that open question still stands. The spawn neighborhoods and loot hotspots we've decided will help pull players together. We'll come back to it with loot.

**To answer:** confirm the boroughs, and yes or no to the quarantine wall. After that, **loot, items and inventory**.

My reading of the map is by eye from the screenshot, so the borough edges could be a little off. The KML export will settle it exactly.

### Developer (2026-10-27 12:49)

Should i include staten island? could be an interesting POI needing a boat or kayak to get to

### Claude (2026-10-27 12:49)

I'd leave Staten Island out of the launch map and add it later. Your idea, an island you need a boat to reach, is a good one. But your outline already has several islands that do that job for much less work.

**Why not Staten Island at launch:**
- **It's big:** about 150 km² of extra land, roughly 20% more map on top of an already huge one. Every square kilometer needs roads, buildings, loot and zombies.
- **In real life it isn't boat-only.** The Verrazzano Bridge connects it to Brooklyn, so you'd need a lore reason it's cut off (for example, the military blew up the bridge). That works, but it's extra work too.

**Islands already in or right at the edge of your outline:**

| Island | Why it's a good boat-only point of interest |
|---|---|
| **Rikers Island** | NYC's jail complex, the equivalent of DayZ's Prison Island. High-risk, high-reward loot |
| **North Brother Island** | An abandoned quarantine hospital; Typhoid Mary was kept there. **A good fit for lore and a special-zombie spawn** |
| **Roosevelt Island** | Has ruins of an old smallpox hospital, plus the tram to Manhattan |
| **Governors Island** | A former military base with a fort. Military loot |
| **Liberty and Ellis Island** | The Statue of Liberty. Right at the edge of your outline, worth checking whether they're inside |

Rikers, North Brother and Roosevelt are definitely inside your outline. Since boats will be needed for those anyway, **Staten Island becomes cheap to add later.** It could be the first big post-launch update, reached by boat or through a "repaired Verrazzano Bridge" event. That gives the game a major update without making the launch map bigger.

*My suggestion:* Staten Island out at launch, the small islands in as boat-only POIs, and Staten Island as the first expansion.

**Still open from before:** are the NJ strip and western Nassau slices intentional? And yes or no to the **quarantine wall** along the map's land edges?

The island facts (Rikers, North Brother, Governors) are from memory. I haven't checked which islands are exactly inside your outline beyond the obvious ones.

### Developer (2026-10-27 12:52)

Well thats the thing, nj was included but i dont want save that cause thats an estimate. Things like the border being a quarantine wall should make sense, along major highways or streets, not randoms streets, which would be the case with this saved image. Whats the best way about making our final layout for full map? Can you access google earth or something similar to draw the border?

### Developer (2026-10-27 12:53)

Nj was meant to be included, but maybe not everypart i include.,

### Claude (2026-10-27 12:54)

Updated. The GDD now treats your outline as a **rough sketch only**. The decided part is that the border is a **quarantine wall along major highways or streets**, and that some of NJ is in. I kept the screenshot, labeled as a rough sketch; tell me if you'd rather I delete it.

## The best way to make the final border: build it from map data, not by drawing

**Can I use Google Earth?** I have a built-in browser and could open it, but I'd be clicking points by hand, which is imprecise and doesn't snap to roads. That's the same problem your sketch has. There's a better way:

1. **You pick the border roads in plain words**, for example: "North: the Cross County Parkway. NJ: everything east of the Turnpike. East: the Cross Island Parkway."
2. **I pull those exact roads from OpenStreetMap**, the free world map data we'd also use to generate the city, and join them into one border that follows each road exactly.
3. **I save the border as a file** in `docs/map/` that opens in Google Earth, and make you a **preview map page** to zoom around, with the exact area in km².
4. **You give feedback**, like "move the north edge up to X," and I rebuild it. Every version is saved, so nothing gets lost.

Why this beats drawing: the wall lines up perfectly with real highways, the area numbers are exact, it can be redone any time, and it's the **same data pipeline we'll use to build the map itself**. So this is also a first small test of that pipeline.

**Possible wall roads to start from** (my suggestions, to be checked against the data):
- **NJ side:** the **New Jersey Turnpike (I-95)**, which would take in the Hudson waterfront: Fort Lee, Weehawken, Hoboken, Jersey City.
- **North (Bronx):** the **Cross County Parkway**, just over the city line in Westchester.
- **East (Queens):** the **Cross Island Parkway**, which keeps the map inside Queens. If you want part of Nassau like your sketch had, we'd pick a road further east.

The Staten Island question is still open: my suggestion was to leave it out at launch and add it as the first expansion, with the smaller islands as boat-only spots now.

I haven't checked these roads against the actual map data yet; I'm going from memory of where they run, so the first draft may move them.

### Developer (2026-10-27 13:01)

Yes, build a first border draft from OpenStreetMap highways with a preview map, using your suggested wall roads as a starting point.

### Developer (2026-10-27 13:03)

Yes, build a first border draft from OpenStreetMap highways with a preview map, using your suggested wall roads as a starting point. For staten island, include just a few square miles, not the whole thing. Thats a journer on the boat, and although there is still land access (for now i dont want the bridge destroyed), a boat from manhattan would be faster than the journed to the bridge on foot

### Claude (2026-10-27 13:07)

The OpenStreetMap servers are overloaded right now, so the road download is retrying in the background. While it runs, I'm writing the script that turns those roads into the border.

### Claude (2026-10-27 13:08)

The road download is still retrying in the background against busy OpenStreetMap servers. The border script is ready, and I'll pick this up as soon as the data arrives.

### Developer (2026-10-27 13:10)

any luck?

### Claude (2026-10-27 13:11)

Not yet. The download script had a certificate problem in Python, though curl reaches the servers fine. I'm switching the download to curl.

### Claude (2026-10-27 13:11)

The download is running again, now through curl, and retrying while the servers are busy. I'll build the border as soon as the road data comes in.

### Developer (2026-10-27 13:16)

we just gonna sit here until it potentially downloads or?

### Claude (2026-10-27 13:19)

Got the data. The main OpenStreetMap servers worked, and all seven wall roads came back with full geometry. Now I'm checking where each road starts and ends so I can cut the border pieces.

### Claude (2026-10-27 13:21)

Got the data I needed, apart from the south-east corner near JFK, where I'll have to choose a road by looking at the map. Now I'm building the border and a preview map.

### Claude (2026-10-27 13:22)

The first border draft is built (about 1,000 km² including water). I'm opening it in a preview map now to check its shape.

### Claude (2026-10-27 13:23)

The preview map works. Most of the border sits on real highways already. I'm fixing two problems: a loop where two parkways meet, and a water stretch that cuts across Jersey City.

### Claude (2026-10-27 13:24)

The north junction still loops back on itself because the two parkways' ramps overlap there. I'm pinning the exact meeting point instead of letting the script guess it.

### Claude (2026-10-27 13:26)

The first border draft is built, and it follows real highways. You can see it in the browser pane next to this chat. Click anywhere on that map to get the coordinates, so you can tell me exactly where to move something.

**What it follows, clockwise from Yonkers:**

| Side | Wall follows | Includes |
|---|---|---|
| North | Yonkers Avenue, **Cross County Parkway**, **Hutchinson River Parkway** | South Yonkers, Mount Vernon, Pelham |
| East | Water down to Little Neck Bay, then the **Cross Island Parkway** | All of Queens down to Elmont |
| South | Ocean and the Lower Bay | JFK, the Rockaways, Coney Island |
| Staten Island | **Staten Island Expressway** and **Clove Road** | North-east corner: St. George to Fort Wadsworth |
| New Jersey | Newark Bay, up the Hackensack River, then the **NJ Turnpike** to the GW Bridge | Bayonne, Jersey City, Hoboken, Weehawken, Union City, Secaucus, Fort Lee |
| West | Up the Hudson | |

**Total: about 1,000 km² (386 sq mi) including water.** A lot of that is water: the harbor, Jamaica Bay, a strip of ocean and the Hudson. It's bigger than your 782 km² sketch, mostly because of the NJ Turnpike and the Yonkers/Pelham slice.

**Still placeholders (orange dotted lines):**
- **The Queens–Nassau line south of the Cross Island Parkway to the ocean** is the big one, about 11 km. I couldn't find a clean major road there from the data. Pick a road on the map, or I can try a few candidates next.
- Three short ones: downtown Yonkers to the Hudson, across Pelham Bay Park, and Fort Wadsworth to the Verrazzano.

**Staten Island:** the corner that's in now measures about 8.6 sq mi including the water at its edges. That's more than "a few square miles," so the wall would need to move east of Clove Road to shrink it.

**Everything is saved in the project:**
- [docs/map/border-draft.kml](../../docs/map/border-draft.kml): opens in Google Earth.
- [docs/map/border-draft.geojson](../../docs/map/border-draft.geojson) and [docs/map/preview.html](../../docs/map/preview.html).
- [tools/map/build_border.py](build_border.py): the list of roads and water points at the top of this file *is* the border. Every change you ask for is an edit there plus a rerun.
- The GDD §5, the decision log and CLAUDE.md are updated. The Staten Island decision is included: a few square miles, the bridge intact, and a boat being faster than walking.

**To open the preview yourself later:** double-clicking the file won't load the map tiles, so serve it locally first. Run this in the `docs/map` folder:

```bash
python -m http.server 8765
```

Then open `http://127.0.0.1:8765/preview.html`.

**Limits and loose ends:**
- The water stretches are hand-placed points, so some of them clip the shoreline slightly (for example, the Hackensack River bend near Secaucus).
- I couldn't measure land-only area, because that needs coastline data I haven't fetched yet.
- A small local web server is still running in the background to serve the preview.
- Python's isolated environment is in this session's temporary folder, so a future session will need to reinstall `shapely` to rebuild the border.

### Developer (2026-10-27 13:27)

<task-notification>
<task-id>btof4p6fo</task-id>
<tool-use-id>toolu_01D3V3mMWhHjdPfEy64HBfvF</tool-use-id>
<output-file>C:\Users\Paul\AppData\Local\Temp\claude\C--Game-Dev-Folder-NYZ\99617619-32a2-4d63-97ec-fb0b9b699f5b\tasks\btof4p6fo.output</output-file>
<status>completed</status>
<summary>Background command "Download wall road geometry from OpenStreetMap using curl with retries" completed (exit code 0)</summary>
</task-notification>

### Claude (2026-10-27 13:27)

The earlier background download from the overloaded servers has finished, but nothing needs it, because the border was already built from the main OpenStreetMap servers. Nothing changes. The two open questions are still the Staten Island size and which road to use along the Queens–Nassau line.

### Developer (2026-10-27 13:28)

Ok now can start cutting areas out and fine tuning the border. First, Thats a lot more of new jersay than needed. Staten island is fine. Green is my proposed border where yours is red. Dont change yet, take notes and we will make all changes at once

### Developer (2026-10-27 13:28)

GWB***

### Claude (2026-10-27 13:29)

I haven't changed the border. Everything is collected in a change list, [docs/map/border-notes.md](../../docs/map/border-notes.md), to apply all at once later.

**Noted so far:**

1. **Cut New Jersey back to your green line.** I saved your drawing in the project ([docs/images/border-v1-nj-proposal.webp](../../docs/images/border-v1-nj-proposal.webp)).
   - **Stays in:** Fort Lee, Edgewater, Cliffside Park, Fairview, Guttenberg, West New York, Union City, Weehawken, Hoboken, Jersey City and Bayonne.
   - **Cut:** Secaucus, Ridgefield Park, Leonia, the Meadowlands and west North Bergen.
2. **The GWB stays crossable.** In v1 the wall ran right along the bridge. The new border meets the Hudson north of it, so the whole bridge and its Fort Lee end are inside the map.
3. **Staten Island stays as it is.** That's recorded as settled.

Still waiting from v1: the Queens–Nassau road south of the Cross Island Parkway, and three short placeholder stretches.

**Two questions about your drawing, to answer whenever suits you:**
- Was the green meant to follow a specific street? If so, which one? Reading the map, it's probably Grand Ave / Bergen Blvd in the north and Kennedy Blvd or Tonnelle Ave further south. If not, I'll find the nearest major road when I apply the changes and show you.
- What should the dashed stretch at the bottom, from Hoboken to the Pulaski Skyway, follow? A road, the rail line, or nothing specific?

Send the next area whenever you're ready.

### Developer (2026-10-27 13:32)

For your question, Tonelle avenue all the way down basically from Broad From Grand. Dotted means not really a road, so just fill in from there, main roads preferred but if not its fine. SO fill in from the solid green to the blue dotted that you made marking water wall

### Claude (2026-10-27 13:32)

Got it, and it's added to the [change list](../../docs/map/border-notes.md). The NJ wall goes **Grand Avenue, then Broad Avenue, then Tonnelle Avenue** most of the way down. From the end of Tonnelle, it connects to the water wall on the Hackensack, along a main road if one fits and a plain connector if not.

Nothing is applied yet. Send the next area whenever you're ready.

### Developer (2026-10-27 14:00)

this, might aswell include that last little part of the area. As for the Eastern end, We can take more of Queens out, main thing is to keep both the throggs neck and whitestone, and at least the main highways connecting them, along with JFK which could be along or near the border. And then the new green lines in the next image. They dont trace a road or path, you can pick generally based off that line, just keep Coop city and bay plaza in it. Tha can also basically bet at the border but included

### Claude (2026-10-27 14:01)

All three are added to the [change list](../../docs/map/border-notes.md), and both drawings are saved in `docs/images/`. Nothing is applied yet.

3. **Breezy Point:** the v1 ocean line cut through the west end of the Rockaways and left that tip outside. I'll move the line south so it's included.
4. **North Bronx:** the border moves down to roughly the city line, from the Hudson at Riverdale east to the Hutch. That drops Yonkers, Mount Vernon and Pelham, and Co-op City and Bay Plaza stay inside. I'll pick major roads that follow your green line.
5. **East Queens:** both the Throgs Neck and Whitestone bridges stay crossable, along with their highways, and JFK stays in.

**Two things to confirm for the east side:**

- **The route:** my plan is to run the wall down the **Clearview Expressway (I-295)** from the Throgs Neck Bridge to where it ends. From there it would follow a major road south to JFK's east edge, then go into Jamaica Bay. Everything east of that (Bayside's east side, Douglaston, Little Neck, Bellerose, Queens Village, Rosedale) would be cut. Does that match what you had in mind?
- **The Rockaways:** if the wall reaches the water at JFK, should the whole Rockaway peninsula still be in, all the way east to Far Rockaway? If it should, the wall has to cross onto the peninsula near the Nassau line. If not, it could cut the peninsula somewhere in the middle.

Send the next area or answers whenever you're ready.

### Developer (2026-10-27 14:01)

Ok can go ahead

### Developer (2026-10-27 14:04)

Yes those are good, and yes for the second question not really sure, but yeah include the peninsula still

### Claude (2026-10-27 14:06)

Nominatim, OpenStreetMap's search service, is throttling the requests. I'm adding retries with slower pacing.

### Claude (2026-10-27 14:09)

Got the road data for all three areas. Now I'm looking at each area on the map to choose exact points.

### Claude (2026-10-27 14:15)

Now I'm rebuilding the border as draft v2. The script will follow each road along its actual route instead of cutting single pieces, which avoids the junction glitches from v1.

### Claude (2026-10-27 14:18)

v2 now follows the roads properly. I'm fixing one gap in the map data along JFK's east edge, then checking each changed area on the map.

### Claude (2026-10-27 14:20)

Draft v2 is done, with all five changes applied together. It's open in the browser pane, and the map is now **about 910 km² (351 sq mi) including water**, down from 1,000 km².

**What changed:**

1. **New Jersey:** the wall now runs along your line: **Tonnelle Ave, Broad Ave, Grand Ave, then Fort Lee Road**. The no-road stretch at the bottom became the **Pulaski Skyway**, which is a main road from the Hackensack River to Tonnelle. Secaucus, Ridgefield Park and the Meadowlands are out.
2. **GWB:** the wall runs along the north side of the bridge approach and meets the Hudson north of the bridge, so the bridge is fully crossable.
3. **Breezy Point:** the ocean line now runs south of the whole tip.
4. **North Bronx:** the wall goes from the Hudson at Riverdale along **East 233rd St** to the **Hutch**. Yonkers, Mount Vernon and Pelham are out; **Co-op City and Bay Plaza are in**.
5. **East Queens:** the water comes down **east of the Throgs Neck Bridge** (Fort Totten stays in). The wall then follows the **Clearview Expressway, Francis Lewis Blvd and Springfield Blvd**, then **Rockaway Blvd along JFK's east edge**. From there it goes through Head of Bay and down **Beach 9th St** to the ocean. Both bridges, their highways, JFK and the whole Rockaway peninsula are in. Douglaston, Little Neck, Bellerose, Laurelton and Rosedale are out.

**New on the preview: green dash-dot lines are "connectors"**, land stretches with no road that you said were fine, such as Riverdale to 233rd St. Orange dots are the **two placeholders still needing a road**: one across Pelham Bay Park and one at Fort Wadsworth.

**Everything is recorded:**
- [docs/map/border-notes.md](../../docs/map/border-notes.md) now lists what was applied in v2, and what's still pending.
- GDD §5 describes v2 side by side.
- The decision log has a v2 entry.

**Limits and loose ends:**
- I checked each changed area by eye on the map, but not every block. A few water lines are hand-placed and may clip a shoreline slightly.
- One stretch of Rockaway Blvd along JFK was missing from the map data, so that piece is a straight line that roughly follows the road.

Send the next round of changes whenever you're ready, and I'll collect them the same way.

### Developer (2026-10-27 14:21)

Can you estimate the usable land space not including water, in less than 2-4 minutes? if not i dont want to do it

### Claude (2026-10-27 14:21)

Yes, quick estimate: **about 680 km² of land (about 260 sq mi), give or take 10%.** That's about 3 times the size of DayZ's Chernarus.

I worked it out from known land areas of each borough and town, minus the parts the border cuts out. I didn't measure it from the map:

| Area | Land in the map (km²) |
|---|---|
| Brooklyn (all) | ~180 |
| Queens (minus far-east Queens) | ~240 |
| Bronx (minus small slivers in Riverdale and Pelham Bay Park) | ~103 |
| New Jersey (Jersey City, Bayonne, Hoboken, the Palisades towns, etc.) | ~85 |
| Manhattan (all) | ~59 |
| Staten Island piece | ~15 |
| **Total** | **~680** |

That means about 230 of the 910 km² inside the border is water. Most of it is Jamaica Bay, the strip of ocean, the harbor and the Hudson.

I've added the estimate to the GDD's open questions. The borough and town areas are from memory, and the cut-out parts are eyeballed, so an exact number would need coastline data, which takes longer than a few minutes.

### Developer (2026-10-27 14:29)

Ok one thing, i understated it with 100+ players, 100 players would feel like a ghost town. How about 250-300 to start, and if budget down the line allows then bump up to 500

### Claude (2026-10-27 14:29)

Agreed, and the numbers back you up. It's updated everywhere the old "100+" appeared: GDD §2, §3 and §5, the open questions, CLAUDE.md and the decision log.

**Player density** (players per km² of land, using the ~680 km² estimate):

| Players | Per km² | Compared to a 60-player DayZ server |
|---|---|---|
| 100 | 0.15 | Half as crowded: a ghost town |
| 250 | 0.37 | 1.4× more crowded |
| 300 | 0.44 | 1.6× more crowded |
| 500 | 0.74 | 2.7× more crowded |

So 250–300 makes the map feel busier than DayZ. That's what "engaging PvP" needs.

**Two consequences:**

1. **This makes server load even more clearly the biggest technical risk.** Most Unreal multiplayer games ship with around 100 players per server, so 300 is well past that, and 500 more so. It's not impossible, but it means serious networking work. If one server can't handle it, the fallback is splitting the map across several servers, which is a big project of its own. The early bot load test now targets **300 bots**, and it'll tell us where we stand before we build much else.
2. **I made the player cap a server setting.** Servers can then run at 150 or 200 if the load test or hosting costs demand it, without changing the game.

Hosting cost also rises with player count, since bigger servers cost more per month. That isn't in the doc yet. It belongs in the business-model question whenever we get to it.

### Developer (2026-10-27 14:32)

Ok, whats next

### Claude (2026-10-27 14:32)

Next I'd suggest **loot, items and inventory.** Crafting, raiding tools, armor per body part, the journal and the antiviral all depend on it. Here's a proposal to react to, in the same format as before.

## Loot, items and inventory: my proposal

**1. Inventory: a grid inside each piece of clothing** (DayZ-style)
- Your jacket, pants, vest and backpack each have their own grid, and items take up space by size. A rifle won't fit in a jeans pocket.
- Weight is kept simple: carry too much and you get a single **"Heavy"** status that slows you and drains stamina faster. There's no weight number to manage.
- **Hotbar:** keys 1–0 for weapons and items you use often.

**2. Item condition: 4 levels with colors**
- Pristine → Worn → Damaged → Ruined. Condition affects how well an item works: a damaged rifle jams more, a worn jacket blocks fewer bites.
- Repair kits restore items, but not back to Pristine, so items still wear out over time.

**3. Loot depends on the building type** (DayZ-style)

| Place | Loot |
|---|---|
| Apartments, houses | Food, clothes, basic tools |
| Bodegas | Snacks, drinks, cigarettes, coffee (a mood item) |
| Pharmacies, clinics | Medicine, bandages |
| Hardware stores | Tools, building materials |
| Police stations | Pistols, ammo, police gear |
| Military zones, National Guard sites | Rifles, armor, explosives (rare) |
| Hospitals | Medical supplies, antiviral (rare) |

**4. NYC twist: guns are rare.** The city has very few gun stores, so guns mostly come from police and military sources. That makes melee matter early, makes guns valuable, and turns police stations and military sites into PvP hotspots.

**5. Loot tiers by area:** spawn neighborhoods get low-tier loot. Better loot sits in dangerous places: Manhattan's core, military sites, and the boat-only islands (Rikers, Governors Island).

**6. Loot respawning: server-wide item counts** (DayZ's central economy)
- The server tracks how many of each item exist in the world and respawns items when counts drop. Rare items stay rare.
- This fits the rule we already have that loot inside claimed bases doesn't respawn.

**7. Rarity: 4 tiers.** Common, uncommon, rare and very rare. Raid tools, explosives and the antiviral are very rare.

**8. Decay:** food rots, batteries run down, and items dropped on the ground despawn after a while. That keeps the server clean.

Weapons and attachments would be the topic after this, since they're big enough for their own section.

**Other topics still to design:** crafting, clans (size limits, ranks), PvP rules, vehicles and boats, weather and day/night, trading, server persistence and wipes, character creation, lore, and the map's points of interest.

**To answer:** yes or changes per number, or pick a different topic.

### Developer (2026-10-27 14:33)

Im going to briefly start a different chat for something then come back to this

### Claude (2026-10-27 14:33)

Sounds good. Everything we've decided is saved in the docs. The loot and inventory proposal is the one thing that exists only in this chat, so come back to **this conversation** to answer it and we'll carry on from there.

### Developer (2026-10-27 15:25)

Ok  the inventory system has been decided in a seperate chat, can review the mds to see it. Hotbar still stays in that system. 

2. Condition yes
3. Good, also for gun source they should still be found in apartments/houses, but very rarely. Idk the statistics exactly, but ghetto neighborhoods with high crime rates should realistically have more in the apartments than just like manhatan per say.
4. Connects to previous. 
5. Yes
6. Yes.
7. Maybe 1 more above very rare, which would be the raid tools, explosives, antiviral, etc. Different types/tiers of guns can differentiate rare from very rare. 
8. Yes

### Claude (2026-10-27 15:26)

I read the inventory section from your other chat (§11), and loot builds on it. Loot & items is now [GDD §12](docs/GDD.md), and the decision log is updated.

**Recorded:**
- **Hotbar (keys 1–0) stays.** It's the quick bar from §11, so it only pulls from quick reach.
- **Condition:** 4 color-coded levels. Repair kits never bring an item back to Pristine.
- **Guns:** they come mainly from police and military, plus **very rare finds in homes**. Those finds are more common in higher-crime neighborhoods than in places like Manhattan. The exact rates are still to be decided.
- **Rarity: 5 tiers.** The new top tier, working name **"Extremely rare"**, holds raid tools, explosives and the antiviral. Gun types split rare from very rare.
- **Loot tiers by area, a server-wide economy and decay**, all as proposed.

**One thing to know about the gun rule.** Basing gun rates on real crime data for real neighborhoods can come across as stereotyping the people who live there, and that tends to draw criticism once a game gets attention. The mechanic itself is fine. The safer way to do it is to keep the difference modest, never name or label neighborhoods in the game, and treat the rates as hidden tuning. That's recorded as a note in §12, and the call is yours.

I also fixed a small formatting slip in §11's open items, where two lines had run together, and added **Weapons & attachments** to the systems checklist.

### Developer (2026-10-27 15:47)

Yes, let's do weapons and attachments next. Give me your proposal.

### Claude (2026-10-27 15:48)

## Weapons and attachments: my proposal

**1. Five weapon families**

| Family | Examples | Where found (§12) | Rarity |
|---|---|---|---|
| **Melee** | Pipe, bat, crowbar, kitchen knife, machete, fire axe, sledgehammer | Everywhere | Common to uncommon |
| **Pistols, revolvers** | Police 9mm, revolvers | Police; homes (very rarely) | Rare |
| **Shotguns, hunting rifles** | Pump shotgun, bolt-action | Police, homes | Rare |
| **Military rifles** | Assault rifles, marksman rifles, sniper rifles | Military sites | Very rare |
| **Bows and crossbows** | Recurve bow, crossbow | Sporting goods, crafting | Uncommon to rare |

Plus **throwables:** bottles and rocks (to distract), molotovs (crafted), grenades (extremely rare, military).

**2. Fictional gun names.** The guns look like real models but have made-up names. Using real brand names risks trademark trouble, and many games avoid it the same way.

**3. Noise is a big deal, because gunshots attract hordes (§8)**
- From loudest to quietest: shotgun, rifle, pistol, suppressed, bow and melee.
- That makes **melee and bows the main tools against zombies**, and guns a choice with consequences.

**4. Melee: quiet, and the core of early survival**
- Light and heavy attacks, using stamina.
- **Shove** pushes zombies back, which matters against crowds (Zomboid has this).
- **Stomp** finishes zombies on the ground. Head hits are what kill (§8).
- One-handed versus two-handed melee follows the broken-arm and handedness rules (§7).

**5. Ammo and magazines: a few calibers**
- About 6 ammo types: 9mm, .38, 12 gauge, 5.56, 7.62 and arrows. That's far fewer than DayZ, to keep it easy to learn.
- **Magazines exist and tie into reach zones (§11).** Magazines on your chest rig mean a fast reload; magazines in your pack mean you stop and dig.
- **Refilling magazines is one action** that uses ammo from quick reach, not a bullet-by-bullet chore.

**6. Attachments: 5 slots**
- **Optic:** red dot, low zoom, sniper scope (rare).
- **Muzzle:** suppressor (very rare). It cuts the noise radius but doesn't make a gun silent. **There's also an improvised suppressor** (crafted, e.g. from a bottle or oil filter) that breaks after a few shots.
- **Underbarrel:** grip or flashlight, which matters at night.
- **Stock**
- **Magazine:** extended magazines.
- **Attachments fit by rail type** (pistol rail or rifle rail), not by specific gun, so players don't have to memorize what fits what.

**7. Handling**
- **Recoil and sway.** Sway gets worse with stress (§7), hurt arms (§7) and low stamina.
- **Jams:** the chance goes up with worse condition (§12). Clearing a jam is a quick action.
- **Bullet drop at long range, but no wind.** Rooftop shooting across avenues is a real NYC thing, so drop matters, but wind would be too fiddly.
- Damage hits body parts (§7), and **armor per body part** blocks it: a helmet protects the head, a vest the torso.

**8. Weapon skills stay non-combat**
- Skills (§6) cover handling, not damage: faster reloads, faster jam clearing, gun repair, crafting attachments.
- **No "more damage" or "less recoil" skills.** That keeps PvP fair for new players, in line with "no raw stat points" (§6).

**9. Crafting ties in**
- Recipes: bows, arrows, molotovs, improvised suppressors, upgraded melee (nail bat, spiked pipe).
- **A crafted pipe shotgun:** unreliable, loud and short-ranged. It gives players without loot a last-resort gun without making real guns any less rare.

**10. Condition and repair:** weapons wear down with use. Cleaning kits and repair kits restore them, but never back to Pristine (§12).

**To answer:** yes or changes per number. The main choices are fictional gun names (2), magazines (5), the non-combat skills rule (8) and the crafted pipe shotgun (9).

### Developer (2026-10-27 16:01)

save. taking break

### Claude (2026-10-27 16:01)

Saved. The weapons proposal is in [docs/pending/weapons-proposal.md](docs/pending/weapons-proposal.md), clearly marked **not decided**. The GDD's systems checklist points to it, so it'll be found even from a new chat. Everything you've decided so far is in the GDD and the decision log.

When you're back, answer the 10 numbered points with yes or changes. The main choices are 2, 5, 8 and 9.

The small local web server for the map preview is still running in the background, which is harmless. It stops when this session closes.

### Developer (2026-10-27 16:50)

1. Good
2. Good
3. Good
4. Good
5. I would like to have a vast options of guns to use from, even if they are rarer or hard to find. I want this to be a game that has vast gun custimization
6. Same as previous, I want vast custimization so maybe a spot for a ghillie wrap on rifles and stuff, and different types of rails that can fit more, so like a 2 sided rail vs just one 
7. Yes good.
8. Agreed
9. yes, with maybe crafting ammo as an endgame thing
10. Yes

### Claude (2026-10-27 16:51)

Recorded. Weapons & attachments is now [GDD §13](docs/GDD.md), the decision log is updated, and the pending proposal file is removed now that it's answered.

**Your changes:**
- **A vast gun selection and deep customization** are now listed as core features of NYZ.
- **A ghillie wrap slot** on rifles.
- **Rail types that fit more,** such as a two-sided rail versus a one-sided one, so more rail sides means more attachment slots.
- **Ammo crafting** as an endgame recipe, to be detailed with crafting.

**Two things this raises:**

1. **Calibers.** A vast gun roster can't run on the 6 ammo types I proposed. My suggestion is to have many guns share common real calibers, about **10–12 in total**. Each one gets a color-coded ammo box and a "fits:" tooltip, so new players can always tell what goes where.
2. **Cost.** Every gun needs a model, first- and third-person animations and sounds. For a solo developer, guns become the biggest art and animation job in the game. The practical approach, now written into §13, is to build the roster on **shared platforms**: an AR-style family, an AK-style family, a pistol family and so on. Guns on the same platform share animations and rails, so you get lots of variety from variants and parts without remaking animations for each gun. Weapon packs on Fab can fill gaps.

Still open in §13: the full list of swappable gun parts, which platforms the roster uses, and how the customization screen stays easy to learn. My suggestion for the screen is that it only shows parts that fit, lights up compatible slots, and offers ready-made presets.

After calibers, I'd suggest **crafting** next, since several systems now point to it: ammo, sewing bags, improvised suppressors and the journal.

### Developer (2026-10-27 16:52)

You know what, while we're here lets make a list

### Claude (2026-10-27 16:54)

Here's draft v1 of the roster, saved in [docs/weapons/gun-roster.md](docs/weapons/gun-roster.md) with full details for every gun (platform, caliber, rarity, where it's found). It's marked **not decided** until you've reviewed it.

**40 guns on 17 shared platforms, plus 3 oddities.** The "based on" names are only for our reference; every gun gets a made-up name in the game.

**Pistols (10):** Glock 17, Glock 19, Sig M17, Glock 18 (full-auto, very rare), Beretta M9, Sig P226, 1911 (.45), Hi-Point, Tec-9, .22 pocket pistol.

**Revolvers (3):** .38 snub-nose, .357, .44 Magnum (very rare).

**SMGs and carbines (4):** MP5, Uzi, MAC-10 (.45), AR-9 (9mm carbine). All very rare.

**Shotguns (7):** Remington 870 (police), Mossberg 500, Mossberg 590 (military), double-barrel, sawed-off (crafted from the double-barrel), pipe shotgun (crafted), Benelli M4 (semi-auto, very rare).

**Hunting and sporting rifles (4):** Ruger 10/22 (.22), Marlin .30-30 lever, .357 lever, Remington 700 bolt-action.

**Military and tactical rifles (10):** NY-legal civilian AR-15, M4A1, Mk18, M16A4, M110 (marksman rifle), M24 (sniper), M14, AKM, short AK, SKS.

**Heavy (2):** M249 machine gun, Barrett .50 cal. Both proposed for the top "extremely rare" tier.

**NYC oddities (3):**
- **Flare gun**, found at marinas: a light that also lures zombies.
- **Starter pistol**: makes pure noise, to pull a horde somewhere else.
- **Nail gun**, found on construction sites: short range and quieter than a real gun.

**12 calibers:** .22, 9mm, .38, .357, .44, .45, 12 gauge (buckshot and slug), .30-30, .308, 5.56, 7.62×39 and .50 BMG. Arrows, bolts, nails, flares and blanks come on top, as special ammo.

**This adds new loot spots to the map:**
- **Port container yards** (Red Hook in Brooklyn, Port Jersey in Bayonne) for smuggled guns: the AK family, Uzi and MAC-10.
- **Police special-unit sites** and **federal sites** for the SMGs and short rifles.
- **One or two gun shops** in the whole map, so each one is a hotspot.

**Questions:**
1. Cut or add any guns?
2. Should the machine gun and the .50 cal go in the top tier, alongside raid tools and explosives?
3. Real-life rule: **.357 guns also fire .38 rounds.** Keep that, or drop it to keep things simpler?
4. Are port container yards OK as the source of smuggled guns? They'd tie nicely into lore.

The 17 platforms are what keep this affordable. Guns on the same platform share their animations and rails, so 40 guns doesn't mean 40 sets of animations.

### Developer (2026-10-27 16:57)

Maybe a few more pistol types, 2-4. at least 3 more revolver types, 1-3 more smgs, 2 more shotguns, and 1 or 2 more military sniper rifles, and also add an ak47

### Developer (2026-10-27 16:58)

Yes those things can stay with top tier. 3. Sure. 4. Lets explore this more

### Claude (2026-10-27 16:59)

Roster v2 is saved in [docs/weapons/gun-roster.md](docs/weapons/gun-roster.md), and your answers are in the GDD and the decision log. I picked the specific models to fill your counts, so swap any of them freely.

- **Pistols (+4):** S&W M&P9, CZ 75, H&K USP .45, and a .44 Desert Eagle-style pistol (very rare).
- **Revolvers (+4):** S&W Model 10 (the old police revolver), Ruger GP100, Ruger Super Redhawk (.44), and a Colt Single Action Army-style cowboy revolver.
- **SMGs (+3):** Scorpion EVO, UMP .45, Vector.
- **Shotguns (+2):** an over-under sporting shotgun, and a Saiga-12, an AK-style shotgun that takes magazines.
- **Sniper rifles (+2):** M40 (Marines), and M2010 (Army). The M2010 adds one new caliber, **.300 Win Mag**.
- **AK-47** (classic), next to the AKM, the short AK and the SKS.

That makes **56 guns on 19 platforms, 13 calibers**. The machine gun and the .50 cal are now officially top tier, and **.357 guns take .38** is decided.

---

## Port container yards: exploring the idea

**Which ports are inside the map:**
- **Red Hook Container Terminal** (Brooklyn).
- **Port Jersey** (Bayonne).
- **South Brooklyn Marine Terminal** (Sunset Park).
- The **Brooklyn Navy Yard**, a former naval shipyard that could have a different flavor.

Port Newark, the biggest port, is just outside the border, on the far side of Newark Bay.

**Why there'd be smuggled guns there.** Pick one or combine them:
- **A. Seized by customs:** a customs holding warehouse at the port is full of weapons taken off ships. One building, heavy loot, and an obvious hotspot.
- **B. Hidden in containers:** a few random containers have weapons hidden among normal cargo. That makes it a treasure hunt across the whole yard.
- **C. The outbreak arrived by ship** (lore): the port is where it started. That gives special zombies and lore areas a natural home there.

**How players find the gun containers (pairs with B):**
- **Shipping manifests:** paper items found around the yard and in offices, each naming a container number with "suspicious cargo". Read one and the container is marked on your map. Clans would race each other to it, and rumors spread.

**How you open them:**
- Containers have padlocks or seals. **Bolt cutters** open them. Make bolt cutters a rare tool, not a top-tier raid tool, or the yards would be locked to almost everyone.
- Cutting is loud, which draws zombies (§8), and anyone nearby hears you.

**The yard as a place:**
- Stacked containers make a maze: tight lanes, climbable stacks, long sightlines down the rows. That's good for PvP.
- **Gantry cranes** you can climb serve as sniper perches and landmarks visible from far away.
- **Dockworker zombies** in hard hats and hi-vis vests drop tools, fitting the "variants by what they were" rule (§8).
- Reachable by water too, which ties into boats.
- Most containers hold ordinary cargo: clothes, electronics, canned food. Guns are the rare jackpot.

**Respawn:** opened containers stay open until the central economy (§12) resets them.

**Questions:**
1. Which source: A, B, C, or a mix? *My pick: B and C.* Manifests make the hunt fun, and the outbreak arriving by ship gives the lore a strong anchor. A works as one extra building inside the yard.
2. Should all four ports be in, or just the two big container ports (Red Hook and Port Jersey)?
3. Bolt cutters as a rare tool to open containers: yes?

### Developer (2026-10-27 17:03)

A mainly, sometimes B. If all four ports are in our borders then yes 3.Yes, can also make other uses for them

### Claude (2026-10-27 17:03)

All four ports are inside border v2. Recording now.

### Claude (2026-10-27 17:03)

Recorded in [GDD §12](docs/GDD.md), the roster file and the decision log.

**Port container yards:**
- **All four ports are in.** I checked each against the border: Red Hook, South Brooklyn Marine Terminal, Port Jersey (Bayonne) and the Brooklyn Navy Yard.
- **Smuggled guns:** mainly from a **customs holding warehouse** at the ports. Sometimes they're **hidden in containers**, which players find through shipping manifests.
- The outbreak arriving by ship isn't used for now, though the lore can still come back to the ports later.
- The yard itself is as proposed: a container maze, climbable cranes, dockworker zombies, and access by water.

**Bolt cutters:** a rare tool, not top tier, used to open containers. **Other uses are on the list to design.** My ideas so far are padlocks on gates and lockers, chain-link fences, the locks on bodega roll-down gates, chained doors, and freeing a tied-up player.

The gun roster is still waiting for your **final sign-off**. Say the word whenever you're happy with it.

Next I'd suggest **crafting**. Several decided systems are waiting on it: ammo crafting, sewing ripped bags, improvised suppressors, the pipe shotgun, how journals are made, and the bolt cutters' other uses.

### Developer (2026-10-27 17:04)

Yes, let's do crafting next. Give me your proposal.

### Claude (2026-10-27 17:05)

## Crafting: my proposal

**1. Three levels of crafting stations**

| Where | Examples | Needs |
|---|---|---|
| **By hand** (anywhere) | Bandages from rags, splints, molotovs, improvised suppressor, nail bat, sawed-off (with a hacksaw), writing the journal | Nothing, or a hand tool |
| **Workbench** (placed at your base) | Bows and arrows, pipe shotgun, building pieces (tiers 1–2), repair kits, base furniture | A built workbench |
| **Specialty stations** | **Gunsmith bench** (attachments, gun repair, endgame ammo), **cooking station** (meals), **welder** (tier 3–4 steel pieces), **sewing station** (bag repair, clothing) | Some need **power from a generator**. Generators are loud, which draws zombies (§8) |

**2. Basic recipes everyone knows; the rest is learned**
- **Known by everyone, free:** bandages, splints, campfire, torch, boiling water, simple cooking, writing in the journal. Nobody can get stuck unable to survive.
- **Everything else costs recipe points** (§6), so specializing and splitting roles within a clan matter.
- **The crafting menu shows every recipe.** Ones you haven't learned are greyed out, with "learn at level X". You can always see what's possible.

**3. Materials: a short list of about 12 urban materials**
- Wood, scrap metal, cloth or rags, nails, duct tape, pipe, plastic, glass bottles, electronics, chemicals, fuel, and mortar or cement.
- **You get them by taking things apart:** furniture gives wood, cars give scrap metal, clothes give rags. That takes tools: a saw, a crowbar, a wrench. Every NYC apartment becomes a materials source.
- Building materials match the base tiers (§9): wood for tier 1, sheet metal for tier 2, brick and concrete blocks for tier 3 (mortar from hardware stores and construction sites), steel for tier 4 (needs the welder and power).

**4. Crafting pulls from nearby storage**
- Crafting uses what's in your inventory **plus storage containers within a few meters**, so you never have to shuffle materials around at your base.

**5. Time, noise and queues**
- Crafting takes time, and you stand still to do it.
- **Loud work makes noise**, following the building-noise rules (§9): hammering, sawing, welding, the generator.
- Station crafts can be **queued** and keep going while you're nearby (Ark-style).

**6. Crafted item condition depends on your tools**
- A worn saw makes a worn bow. That's simple and needs no skill math.
- A **non-combat skill** (§6), "Craftsman", makes crafted items come out one condition level higher.

**7. Items already promised in the decided systems**

| Item | How |
|---|---|
| **Journal** (§6) | A notebook (common loot: bodegas, schools, offices) plus a pen. Writing is an action anyone can do |
| **Bag repair** (§11) | A sewing kit fixes ripped seams by hand; the sewing station does it better |
| **Improvised suppressor** (§13) | A bottle or oil filter plus duct tape, by hand |
| **Pipe shotgun** (§13) | Pipe, nails, a spring and duct tape, at the workbench |
| **Ammo crafting** (§13, endgame) | Gunsmith bench with a **reloading press**, using **spent brass casings** (pick them up after firing), primers (rare loot), gunpowder and lead from scrap |
| **Water** (§7) | Rain collectors; boiling over fire; purification |
| **Comfort items** (§7, mood) | Beds, couches, radios, made at the workbench |

**8. Clan crafting**
- Clanmates can use each other's stations. Recipes belong to each person, so the clan's medic makes the medicine.

**9. Farming gets its own section later**
- NYC rooftop gardens and community gardens fit the setting well, but farming is a big system. I'd design it as its own topic.

**To answer:** yes or changes per number. The main choices are generators powering stations (1), the free basic recipes (2), crafting from nearby storage (4) and tool-based condition (6).

### Developer (2026-10-27 17:23)

1.Good

2. Everything cost recipe points, simple thngs will be very low level and very low costl But actual crafting recipes, things like boiling water, which is not crafting really, should be known by all characters. Things like uses a shirt as a bandage wont require a skill or recipe, things like that
yes to third part.
3. Yes, potentialy more down the line. I like the dissasembling to gain material, but also trees for wood, since some areas do actually have a lot like parks. Scrap metal could also come from taking some other things apart, like a computer or something, where you get some scrap metal some electronics. Also found in industrial sides/constructions sites llike the brick and concrete, and welder and steel.
4. Yes but only at base for the meters, outside of base, only what's in your direct vicinity on the ground.
5. Crafting takes time, and for the most part you stand still, but if youre "crafting" something that can realisticlly be done while walking then no you dont stand still. Loud work makes noise, but small recipes dont/. Que  is good.
6. Yeah.
7. Yes for now
8. Yes
9. Yes

### Claude (2026-10-27 17:23)

Crafting is now [GDD §14](docs/GDD.md), with your changes:

- **Every real recipe costs recipe points**, and simple ones are very low level and low cost. **Everyday actions** like boiling water or using a shirt as a bandage need no recipe at all.
- **Material sources:** taking things apart (a computer gives scrap metal and electronics), **trees** in parks, and **industrial and construction sites** for brick, concrete, steel and welders.
- **Pulling from nearby storage only works at your base.** Anywhere else, crafting uses your inventory and whatever is on the ground right around you.
- **Crafts you could realistically do while walking, you can.** Small recipes make no noise.
- **Farming** is on the checklist as its own topic.

**Two calls I made, so you can correct them:**
- **Writing in the journal is an action, not a recipe.** Locking your death recovery behind recipe points would hurt new players, and writing isn't really making something.
- **Splints, campfires and torches** were free basics in my proposal. They're now **very cheap recipes**, since they're real crafting.

**That raises one open item:** a fresh level-1 character needs **a few recipe points at the start**. Otherwise they can't make a splint or a campfire until they level up. It's in §14's open items.

**Next topic options:**
- **Clans:** size limits, ranks, permissions. Many decided systems already refer to clans (base access, shared beds and stations, mood bonuses, splitting roles).
- **Vehicles and boats:** boats are needed for Staten Island and the island points of interest.
- Others: PvP rules, weather and day/night, trading, server persistence and wipes, character creation, lore, the map's points of interest, farming.

My pick is **clans**, since so much already depends on them.

### Developer (2026-10-27 17:25)

They can get 5-10 points starting, with all the basic things only costing 1 each

### Claude (2026-10-27 17:25)

Recorded in GDD §14 and the decision log. New characters start with **5–10 recipe points**, and basic recipes cost **1 point each**, so a fresh spawn can learn splints, a campfire and a torch right away. The exact number in that range is left for playtesting.

### Developer (2026-10-27 17:26)

Yes, let's do clans next. Give me your proposal.

### Claude (2026-10-27 17:26)

## Clans: my proposal

**1. Clan size cap: 8 members by default, adjustable per server**
- With 250–300 players per server, unlimited clans turn into "zergs": one 40-person clan that runs the whole server. That's the classic Rust and Ark problem.
- A cap of 8 is big enough to split roles (medic, builder, mechanic, shooters) but small enough that several clans compete.
- **No formal alliances at launch.** Alliances bring zergs back in another form. Clans can still team up informally, by agreeing in voice chat.

**2. Creating and joining**
- Anyone can create a clan from the menu for free, and invite players who are nearby.
- **Leaving a clan starts a 24-hour cooldown** before you can join another. That stops people hopping into a clan to get access and then raiding it from inside.

**3. Three fixed ranks, plus a few toggles**

| Rank | Can |
|---|---|
| **Leader** | Everything: invite, kick, promote, disband, place the claim item |
| **Officer** | Invite, build, demolish, change door codes, officer-only storage |
| **Member** | Build, use stations, beds and shared storage |

- The leader can switch a few permissions per rank, such as "members can demolish". There are no custom rank trees, to keep it easy to learn.

**4. What clanmates share** (most of this is already decided)
- Door access (§9), building rights in the claim area (§9), beds and sleeping bags (§10), and crafting stations (§14).
- **Storage locks per container:** a container can be open to the whole clan, or set to officers only.
- **Mood bonus from being near clanmates** (§7).

**5. Seeing each other**
- Clanmates see **each other's name tags up close** and **positions on the map**, plus shared map markers. Losing your friends on a 1:1 NYC map would be a constant frustration.

**6. Friendly fire: on** (DayZ-style), with a server setting to turn it off. Bullets don't check whose side you're on, and it keeps fights realistic.

**7. Talking**
- **Proximity voice chat**, DayZ-style: people near you hear you, including enemies.
- **Long-range voice needs a walkie-talkie,** an item that runs on batteries, which decay (§12). Radios become valuable loot.
- **Clan text chat works anywhere**, as a quality-of-life feature.

**8. Clan identity: graffiti tags**
- Each clan designs a **tag**, an emblem, which players **spray-paint on walls** with spray cans to mark bases and territory. It's very NYC, and you can read the map by whose tags are where.
- It's cosmetic only, with no game rules attached.

**9. Leaving or getting kicked**
- Access ends instantly: doors, storage, beds.
- Whatever that person put in clan storage stays with the clan.

**10. Solo players stay viable**
- Offline raid protection (§9) and small bases keep playing solo workable. Groups have an edge, but solo play isn't a punishment.

**To answer:** yes or changes per number. The main choices are the cap of 8 (1), no alliances (1), the 24-hour cooldown (2), map positions (5) and friendly fire (6).

### Developer (2026-10-27 17:31)

1. Lets cap it at 10, with this being a server setting. Agreed for now, no formal alliances but vocal ones are fine and dont violate any rules.
2. 12 hours should be good.
3. Ranks are good
4. IF we're gonna have ranks, the door access should be more in depth, with general shared codes for everyone, and codes for officer and above. Same for storage locks. Mood bonus good
5. Tags when in LOS but not if they're behind a wall or something. Postition on map shown,  not sure about mini map though. The LOS thing may be subject to change but no surely.
6. Yes
7. Yes 
8. Sure
9. Agreed
10. Agreed, with maybe increased offline protection for solos.

### Claude (2026-10-27 17:32)

Clans are now [GDD §15](docs/GDD.md), and the decision log is updated. I also updated the base locks in §9 to match.

**What's recorded:**
- **Cap of 10** (a server setting). **No in-game alliances, but alliances agreed by voice are fine.**
- **12-hour cooldown** after leaving a clan.
- **Doors and storage have rank levels:** either everyone in the clan, or officers and above.
- **Name tags only in line of sight,** not through walls (may change). Clanmates' positions show on the map, and the **minimap** is undecided.
- **Solo players:** stronger offline protection for solos is noted as a maybe.

**One thing to check is how codes work with ranks.** My reading is that clanmates get in automatically at their rank level, so they never type a code. Each level's shared code is then for letting **outsiders** in, such as an informal ally, without making them a member. The alternative is that everyone types the code for their level. That's more hands-on, but slower and more fiddly for an average player, so I'd go with automatic access. The question is in the box below.

**Next topic options:** vehicles and boats, PvP rules, weather and day/night, trading, server persistence and wipes, character creation, lore, the map's points of interest, farming.

### Developer (2026-10-27 17:33)

No, I meant that if you're a captain, when setting a code lock, you have the option to make it for everyone in the clan to freely open, or Officer and above

### Claude (2026-10-27 17:33)

Got it, that's simpler, and it's fixed in [GDD §15](docs/GDD.md) and the decision log. When an officer or the leader sets a code lock, they pick who opens it freely: **everyone in the clan**, or **officers and above**. Storage works the same way. The code itself still works for anyone who knows it, which is also how you'd let an outsider in.

You said "captain". In the doc that rank is called **Officer**. If you'd rather call it Captain, say so and I'll rename it.

Next topic options: vehicles and boats, PvP rules, weather and day/night, trading, server persistence and wipes, character creation, lore, the map's points of interest, farming.

### Developer (2026-10-27 17:34)

Vehicles and boats

### Claude (2026-10-27 17:34)

## Vehicles and boats: my proposal

**1. The streets are jammed, and everything else follows from that**
- Abandoned cars clog most streets, bridges and tunnels. Main avenues have a few passable lanes; side streets are often blocked.
- **Driving in NYC means planning a route**, not just flooring it. That keeps cars from dominating a city built for walking, and makes bikes valuable.
- **Heavy vehicles can push small wrecks aside.** Big jams stay put.

**2. Land vehicles**

| Vehicle | Why | Rarity |
|---|---|---|
| **Bicycle** | Quiet, no fuel, fits through jams | Common |
| **E-bike, e-scooter** | Faster than a bike, quiet, runs on a battery | Uncommon |
| **Motorcycle, dirt bike** | Fast, weaves through jams, **loud** | Rare |
| **Sedan, yellow taxi** | Basic car | Uncommon |
| **SUV, police cruiser** | Tougher, police ones have a light bar | Rare |
| **Van, box truck** | **Big storage**, slow, can push wrecks | Rare |
| **Ambulance** | Medical loot inside | Rare |
| **Military Humvee** | Armored, pushes wrecks | Very rare |

**3. Bike-share docks: an NYC touch**
- Bike-share stations (Citi Bike-style, with a made-up name) are all over the city, with bikes still locked in their docks.
- **Bolt cutters free them,** which is one of the "other uses" bolt cutters were waiting for (§12).

**4. Starting and owning a vehicle**
- **Keys** turn up in the vehicle, in nearby homes or on nearby zombies. Without keys, you can **hotwire** it: it takes time, and it's a Mechanics skill (§6).
- **Your vehicle locks to you and your clan** (§15). Stealing one means hotwiring it, which is slow and exposed.

**5. Parts: four, kept simple**
- **Battery, tires, engine (condition), fuel.** That's it. DayZ's spark plugs, radiators and headlights are too fiddly for "easy to learn".
- Repairs use repair kits and Mechanics recipes (§14).

**6. Fuel and charging**
- Gas stations, plus **siphoning from the thousands of wrecked cars** with a hose. The city is full of gas if you're willing to work for it.
- **E-bikes and scooters charge from a generator** (§14).

**7. Noise** (hearing is the zombies' main sense, §8)
- Engines are loud: motorcycles loudest, cars and trucks next, then e-bikes, then bicycles (near silent).
- **Car alarms:** bumping or hitting some parked cars sets off their alarm, which pulls zombies (Zomboid-style). Every parked car is a possible trap.

**8. Zombies and vehicles**
- Running zombies over **damages your vehicle**, so plowing through a horde has a real cost.
- **Hordes can surround and stop a car.**
- **Zombies can pull you off a bike or motorcycle.**

**9. Vehicle storage**
- Trunks and cargo areas use the **same cutaway packing as bags** (§11). Each vehicle has its own trunk outline. It reuses a system we're already building.

**10. Boats** (needed for Staten Island and the island spots, §5)

| Boat | Why | Rarity |
|---|---|---|
| **Kayak, canoe** | **Silent**, slow, little storage | Uncommon |
| **Rowboat** | Silent, more storage | Uncommon |
| **Inflatable with an outboard motor** | Faster, uses fuel, loud | Rare |
| **Speedboat, police harbor boat** | Fast, loud, big storage | Very rare |

- Found at **marinas, boathouses** and the ports (§12).
- **Zombies don't swim:** they won't follow you into deep water. Water is safe from zombies, but not from players.
- **Swimming is possible but costly:** you get soaked, which drops body temperature (§7) and ruins anything not in a dry bag (§11).
- _Maybe:_ strong currents in the East River at Hell Gate, as a real NYC hazard.

**11. Server limits** (300 players means server load matters)
- **A cap on vehicles per server and per clan.**
- **Abandoned vehicles despawn** after X days unless they're inside a claimed base, which acts as your garage.

**12. Parked for later: helicopters.** NYC has rooftop helipads, but helicopters are a huge amount of work, change PvP balance a lot, and are costly on the server.

**To answer:** yes or changes per number. The main choices are jammed streets (1), bike-share docks (3), only four parts (5), no swimming zombies (10) and the vehicle caps (11).

### Developer (2026-10-27 17:44)

1. Agreed 
2. Yes to all, except maybe a few different types of sedans and suvs not just one. Also where would the ebikes and scooters be getting their charge?

3. I guess, but this goes back to 2 with the e-bikes for those, although they do have regular ones in the docks as well.
4. Keys idea good, locking the vehicle to you automatically idk. If there is some kind of lock system that has to be made would be better, and the car can freely be started once hotwired by whoever. How hard would it be to make a key in an apocolypse? Also, I want this to take place in a modern setting, and a lot modern cars cant be hotwired physically, but through hacking/tech. That would be a good add, some kind of advance OBD2 scanner that can make keys for a car, and some kind of hacking device to start cars without a key.
5. I think the sparkplugs and radiators and headlights make good sense, it shouldnt be easy to get a car. Maybe just not as hard to find all the parts as dayz. 
6. Good, also answers my earlier question partially, but what about eletric public bikes? 
7. Yes
8. Yes
9. Great thinking
10. Add more boats, theres a few marinas in nyc that have 10-20+ft civillian boats. Just harder to repair. Rest agreed.
11. Yes
12. I want helis from the jump, but extremely rare to find, and even harder to repair.
13. Car custimization, I want extensive car custimization with tier levels similar to building. Engine upgrades, (mostly durabilaty stuff, some speed/power) and the main show armor.

### Claude (2026-10-27 17:46)

Everything is recorded in [GDD §16](docs/GDD.md) and the decision log. Bolt cutters now officially free bikes from the docks, which is one of their "other uses". Here are answers to your questions, plus my suggestions for the open details, all marked "to confirm" in the doc.

**Where do e-bikes and scooters get charged?**
- A **generator** at your base. It's loud, so it draws zombies.
- **Solar panels:** quiet but slow, and rare. That gives players a real choice between noise and speed.
- **Power banks** you carry, and charging from a **running car**.
- **Public e-bikes:** the ones in the docks still have some charge left when you find them. In the game, some docks could **still trickle-charge from their solar panels**, which would make them contested public charging spots.

**How hard is making a key in an apocalypse?** In your modern setting:
- **Older cars** can be hotwired physically, as a Mechanics skill.
- **Modern cars** use your tech idea. The **OBD2 key programmer** writes a new key onto a **blank key fob**, found at dealerships, locksmiths and auto shops. The **hacking device** (very rare) starts a car with no key at all.
- **Copying an existing key** for clanmates uses a **key-cutting machine** at a hardware store or locksmith, which needs power.
- **Locks you install:**
  - A cheap **steering-wheel lock**, which bolt cutters or a hacksaw can remove.
  - An **immobilizer with an alarm**, crafted from electronics. Tampering with it sets off the alarm and pulls zombies.

**Car armor (the main show).** My parts list:
- **Window grates:** stop zombies grabbing you, and some bullets.
- **Ram plows:** push bigger wrecks, which matters on jammed streets.
- **Wheel guards and door plates.**

The tiers go from scrap and plywood up to welded steel. Armor adds weight, so the vehicle is slower and burns more fuel. Counters are the .50 cal, explosives and molotovs. Clan graffiti tags could double as car paint.

**Civilian boats:** center-console fishing boats, bowriders, cabin cruisers, pontoon boats and jet skis.

**Helicopters: one problem to solve.** A helicopter can land on roofs nobody else can reach, so a clan could build an unraidable rooftop base. We need a rule. Either a claimed roof must also be reachable by stairs, or helicopters can't land on claimed roofs. My pick is the stairs rule: it keeps roof bases possible without making them untouchable.

Other helicopter notes:
- Spawn spots could be NYC's real heliports, hospital helipads, and the police aviation base at **Floyd Bennett Field**, which is inside the map.
- A helicopter should be the loudest thing in the game.
- Expect a cap of a few per server.

**To answer:** yes or changes for the charging sources, the keys and locks, the armor parts, the boat types and the helicopter roof rule.

### Developer (2026-10-27 18:04)

quite franlkly, there arent that many buildings with that much room to land a heli on that dont have a helipad. We can let bases be made on roofs that cant be accessed by foot. Realistically, if they die and lose the heli, theyre cooked, they can only respawn up there but not get back any other way. And back to my first sentance, most roofs will have clutter on them making them risky to try to land.

### Claude (2026-10-27 18:04)

Fair points, and that's recorded in GDD §16 and §9 and the decision log, along with your reasoning. Rooftop bases that can't be reached on foot are allowed:

- **Few roofs without a helipad have room to land**, and most are cluttered with AC units, water towers and antennas, so landing is risky.
- **Lose the helicopter and you're stuck.** You can only respawn up there, with no way down.

The analysis note I added says such a base can only be raided by another helicopter owner, or with explosives or a .50 cal from a neighboring roof. Since helicopters are extremely rare, these bases stay rare too.

Still waiting from §16 for a yes or changes:
- **E-bike charging:** generator, solar panels, power banks, charging from a car, docks that trickle-charge.
- **Keys and locks:** key programmer plus blank fobs, the hacking device, key copying, steering-wheel locks, immobilizers with alarms.
- **Car armor parts:** window grates, ram plows, wheel guards, door plates.
- **Boat types:** center-console, bowrider, cabin cruiser, pontoon, jet ski.

### Developer (2026-10-27 18:06)

Yes to all those, with plans on going more in depth later, which i kinda assume were gonna do when we start building each system

### Claude (2026-10-27 18:06)

Confirmed and recorded in GDD §16 and the decision log: e-bike charging, keys and locks, the car armor parts and the boat types.

You assumed right. What we're doing now is the **high-level design**, the agreed shape of each system. When we start building a system, it gets a **deeper design pass** first: exact numbers, edge cases, UI details. I've written that into CLAUDE.md as a working rule, so future sessions follow it too.

**Topics still to design at high level:**
- PvP rules
- Weather, day/night and seasons
- Trading and economy
- Server persistence, wipes and admin tools
- Character creation
- Lore
- The map's points of interest
- Farming

Once those are done, the game is mapped out. That's also when the source-control reminder kicks in, before the UE5 project is created.

### Developer (2026-10-27 18:08)

what next? pvp rules?

### Claude (2026-10-27 18:09)

## PvP rules: my proposal

**1. Full PvP everywhere, full loot** (DayZ and Rust style)
- Anyone can attack anyone, anywhere, and everything you carry can be looted (bodies, §10).
- **Server types:** PvP is the default. A **PvE server setting** turns player damage off. A hybrid **"PvP zones" setting** (PvP only in marked areas like military sites and the ports) is a third option.

**2. Safe zones: decided with trading**
- If we add trader hubs, they could be **neutral safe zones** where weapons are holstered and nobody can be hurt (like Rust's Outpost). That only makes sense alongside trading, so I'd decide it there.

**3. Surrender, restrain, rob** (builds on knock-outs, §7)
- **Hands-up gesture** to surrender, or to show you're friendly.
- **Zip ties, handcuffs or rope** restrain a knocked-out or surrendered player. You can then search them (hidden pockets take longer, §11), **escort them** (they walk where you lead), or let them go.
- **Freeing:** a knife cuts zip ties and rope; bolt cutters cut cuffs (another bolt-cutter use, §12).
- **Anti-griefing limit:** a restrained player can **struggle free after about 10–15 minutes**, so nobody can be held hostage forever.

**4. Combat logging**
- "In combat" means you dealt or took damage, or fired a gun, in the last few minutes.
- While in combat, **the logout timer goes from 30 seconds (§10) to about 2 minutes**, and your character stays in the world the whole time.

**5. No kill feed, no killer names**
- No kill feed, DayZ-style. **The death screen shows only how you died** (e.g., "gunshot to the head"), never who did it. Strangers stay anonymous, and only clanmates get name tags (§15).

**6. No karma or bandit system**
- No hero/bandit meter or bounties at launch. How players behave and what gets said in voice chat sorts out reputations. It's also simpler to learn.

**7. First person and third person**
- This answers an open question: **server setting** for "first person only" or "both". Official servers offer both kinds. Third person lets players peek over walls, so the first-person-only setting matters for fair PvP.

**8. Anti-cheat**
- Server-authoritative design (§3) plus **Easy Anti-Cheat**, which is free through Epic Online Services and made to work with Unreal.

**9. Raiding: already decided** (§9): tools and explosives are hard to find, offline protection by default, and raiding is loud.

**10. Fresh spawns:** apart from minimal loading protection (§10), there's no new-player shield. Low-loot spawn neighborhoods (§10, §12) mean fresh spawns aren't worth hunting.

**To answer:** yes or changes per number. The main choices are server types (1), the restraint timer (3), the 2-minute combat logout (4), no kill feed (5) and no karma system (6).

### Developer (2026-10-27 18:12)

1. Anyone anywhere anytime
2. Yes i want safe zones with trading npcs, and unable to hurt people in it
3. Yes
4. Yes, remove the option to quit to menu entirely (greyed out or not clickable) when in combat or came from combat within the last 5 minutes, unless it was a clanmate that caused the damage
5. Agreed
6. Agreed
7. Agreed
8. Agreed
9. Went over already
10. agred

### Claude (2026-10-27 18:12)

The main PvP section didn't go in, because the end of §16 doesn't match what I expected. Checking the current text.

### Claude (2026-10-27 18:13)

PvP rules are now [GDD §17](docs/GDD.md), and the decision log is updated. The first-person question from §3 is answered too: it's a server setting, and official servers offer both kinds.

**Recorded:**
- **Anyone, anywhere, anytime,** with full loot. I read that as **no PvE or "PvP zones" server types**, so those are marked as not adopted.
- **Safe zones with trading NPCs** where nobody can be hurt. Their details come with trading.
- **Restraining** works as proposed, including the 10–15 minute struggle-free limit.
- **"Quit to menu" is greyed out** while you're in combat and for 5 minutes after, unless a clanmate caused the damage.
- No kill feed, no karma system, Easy Anti-Cheat.

**Two details on the quit lock:**
1. **What counts as combat.** I'd count only damage dealt to or taken from other players. Otherwise every zombie fight would lock you in for 5 minutes, which gets annoying fast.
2. **Force-quitting.** Greying out the button doesn't stop someone pressing Alt-F4 or pulling the plug. My suggestion: if they do, their character stays in the world until the 5 minutes run out, so force-quitting can't save them either. The button in the box confirms that as well.

**Topics left at high level:** weather and day/night, trading and economy (including the safe zones), server persistence and wipes, character creation, lore, map points of interest, farming.

### Developer (2026-10-27 18:19)

Players only, and for force quitting yeah they just stay until the 5 minute combat timer runs out, and the regular leave timer too

### Claude (2026-10-27 18:19)

Recorded in GDD §17 and the decision log:

- **Only fights with other players** (not clanmates) trigger the quit lock. Zombie fights don't.
- **A force-quitting character stays in the world** until the 5-minute combat timer runs out, then for the regular 30-second leave timer on top.

The only open PvP item is the safe zones, which come with trading. That makes **trading, economy and safe zones** the natural next topic.

### Developer (2026-10-27 18:20)

Yes, let's do trading, the economy and the safe zones next. Give me your proposal.

### Claude (2026-10-27 18:21)

## Trading, the economy and safe zones: my proposal

**1. Currency: a physical item that's also useful** (like scrap in Rust)
- Cash is worthless after the outbreak, so traders deal in something people actually need. It's a real item you carry, so it can be looted when you die (full loot, §17).
- Options:
  - **A. Cigarettes.** A prison-economy feel, already bodega loot (§12), and a stress reliever (§7). Smoking them takes currency out of the world, which helps keep prices steady.
  - **B. Batteries.** Useful for flashlights, radios and e-bikes.
  - **C. Scrap metal,** like Rust. Already a crafting material (§14), so every trade is a choice between spending it and building with it.
- *My pick: A, cigarettes.* It's the most New York, and the built-in way it gets used up keeps the economy from inflating.

**2. Safe zones: 3–4 survivor holdouts at famous landmarks**

| Borough | Candidate | Lore hook |
|---|---|---|
| Manhattan | **Grand Central Terminal** | A survivor hub under the famous ceiling |
| The Bronx | **Yankee Stadium** | A former emergency shelter |
| Brooklyn | **Barclays Center** | A former aid station |
| Queens | **Citi Field** | A former evacuation point |

- Spread out so every part of the map has one within reach.
- **NPC guards and walls keep zombies out.**

**3. Safe zone rules**
- **No damage inside**, ever (decided, §17).
- **Anti-camping:** shooting someone near a safe zone marks you **hostile**, and the guards won't let you in for about 10 minutes (like Rust). That stops people camping the exits.
- **Several exits** per zone, so nobody can watch them all.
- **No storage inside.** A bank would undo the risk of full loot.
- **No building near safe zones** (a set radius).

**4. NPC traders, by type**
- **General** (food, clothes, basic tools), **medical**, **weapons and ammo**, **building supplies**, and **mechanic** (vehicle parts, bikes, maybe an old car at a steep price).
- Each safe zone has some of these, not all, so different zones are worth visiting.

**5. What traders won't sell**
- **The top tier never** (raid tools, explosives, the antiviral, the machine gun, the .50 cal). Those stay loot-only, so exploring stays worth it.
- **Very rare items in tiny stock at steep prices.**

**6. Prices move with supply** (tied to the central economy, §12)
- When players sell lots of something, its price drops. When a trader's stock runs low, the price rises.

**7. A reason to pick up junk: valuables**
- A new loot category: jewelry, watches, phones and laptops. Good for selling, little other use.
- **NYC point of interest: the Diamond District** on 47th Street, with high-value valuables and a hotspot to match.

**8. Player-to-player trading**
- **Inside safe zones:** a **secure trade window**. Both players put items in, both confirm, and nobody can be scammed.
- **Outside safe zones:** drop-and-pick-up, DayZ-style. It's risky, so trust matters.
- **Player shops:** a craftable **vending machine** at your base sells your items for currency while you're offline. It can be raided like any other base part.

**9. Trader services: spending that keeps the economy healthy**
- Repairs (but never to Pristine, §12), key copying (§16), and possibly paid information like map intel.

**To answer:** yes or changes per number. The main choices are the currency (1), which landmarks (2), the hostile timer (3), what traders won't sell (5) and vending machines (8).

### Developer (2026-10-27 18:27)

1. Not cigarretes, I want some other standard replacement for Usd, like how modded dayz servers use ruples or rubles, idk something like that 
2. No to those safezones, I want combat or bases in those locations. But yes to 1 in each borough, maybe a known location but famous like the ones you listed.
3. No damage inside ever, for anticamping, yes shooting someone near a safezone can mark you hostile, but also the safezone can have snipers posted up, the watch for players that are camping within a certain area within a certain distance of the safezone, and start with a warning shot and loudspeaker message, and only given 5 seconds to leave the area before the snipers actually target the camper. They should essentially have navy seal aim, they can miss but not often if youre in LOS. Yes several exits. Idk about no storage inside, some kind of banking system where you cant really save everything but can some some is fine, and you need a physical thing linked to your character or a clan account to be able to access it. It would be like a double verifcation thing though, so like a cc has a pin, it needs something like that too for safezones. and a limit on the bank storage. No build near.
4. Agreed fully
5. Agreed fully
6. Agreed

### Developer (2026-10-27 18:28)

1. Not cigarretes, I want some other standard replacement for Usd, like how modded dayz servers use ruples or rubles, idk something like that
2. No to those safezones, I want combat or bases in those locations. But yes to 1 in each borough, maybe a known location but famous like the ones you listed.
3. No damage inside ever, for anticamping, yes shooting someone near a safezone can mark you hostile, but also the safezone can have snipers posted up, the watch for players that are camping within a certain area within a certain distance of the safezone, and start with a warning shot and loudspeaker message, and only given 5 seconds to leave the area before the snipers actually target the camper. They should essentially have navy seal aim, they can miss but not often if youre in LOS. Yes several exits. Idk about no storage inside, some kind of banking system where you cant really save everything but can some some is fine, and you need a physical thing linked to your character or a clan account to be able to access it. It would be like a double verifcation thing though, so like a cc has a pin, it needs something like that too for safezones. and a limit on the bank storage. No build near.
4. Agreed fully
5. Agreed fully
6. Agreed
7. 7. agreed 
8. Agreed
9. agreed

### Claude (2026-10-27 18:29)

All recorded in [GDD §18](docs/GDD.md) and the decision log. I also started a **running points-of-interest list** in §5, which now includes Grand Central, Yankee Stadium, Barclays and Citi Field as combat and base locations.

The sniper overwatch is a strong idea. It solves exit-camping without any invisible walls, and it fits the setting.

**Four open items, each with my suggestion:**

**1. Currency name.** It should sound like an official emergency currency:
- **Scrip:** emergency notes printed by the safe-zone network. Short and easy to say.
- **Ration Notes**
- **Relief Dollars**
- **Marks**

*My pick: Scrip.*

**2. Safe zone locations: known, but not the big combat landmarks.**

| Borough | Suggestion | Why |
|---|---|---|
| Manhattan | **The Intrepid**, the aircraft carrier museum at Pier 86 | A carrier is a natural fortress, and the snipers sit on the flight deck |
| The Bronx | **Kingsbridge Armory** | A huge historic armory, easy to defend |
| Brooklyn | **Brooklyn Army Terminal** | A historic military terminal in Sunset Park |
| Queens | **The national tennis center** (Arthur Ashe Stadium) | It really was used as a field hospital during COVID, which gives it a ready-made backstory |

Also: do the **Staten Island piece** and the **New Jersey side** get one each? They aren't full boroughs in the map. My suggestion: Staten Island gets one at **St. George Ferry Terminal**, and NJ doesn't. NJ is close to Manhattan's zone by bridge or tunnel.

**3. What counts as camping for the snipers.** My suggestion: staying inside a ring around the zone (say **100–150 m**) for more than **about 60 seconds**. The timer runs faster if you're prone or aiming down sights. Just walking through or waiting briefly for a friend never triggers a warning.

**4. Bank details.**
- **Lost or stolen card:** the thief still needs the PIN, so it's useless to them. You can buy a **replacement card** at any safe zone for a fee, which cancels the old one.
- **One account across all safe zones,** so you can deposit in Brooklyn and withdraw in Queens.
- **Storage limit:** a small fixed space (a few pocket grids' worth), maybe upgradeable for currency.

**To answer:** yes or changes for each of the 4.

The Arthur Ashe field-hospital fact is from memory. I'm fairly confident it's right, but check it before it goes into any lore text.

### Developer (2026-10-27 18:37)

1. I name idea where youre not using already real made words, but not too sure on scrip
2. Okay maybe lets not do any famous or well know places. We could do some random warehouses, like ups or amazon facilities where theres giant open rooms for the main traders. As for only 4, with the map being as big as it is, we probably need 2 or 3 more so one in jersey wouldnt hurt. As for the other ones in the city, im fine with random tall buildings that have good space for a safezone, and good sniping positions.
3. Agreed, somone shoulnd get shot if theyre just waiting for someone with no ill intention.
4. Yes, but make the fee expensive so its worth not losing or forgetting at base when you go to a safezone. For the money equavalent yes, im thinking maybe we have a storage unit as one of them so solos who cant grind to make a base for as much time are able to store a few items, like maybe 50-100lbs worth of stuff for a fee. They can store items in the location, but cant retrieve items at other locations, just their money.

### Claude (2026-10-27 18:38)

All recorded in GDD §18 and the decision log:

- **Safe zones:** about 6–7 of them, including one in New Jersey. They're in big distribution-warehouse-style buildings (with made-up company names) for the main traders, and in random tall buildings with good sniping positions. No famous places.
- **Camping:** someone just passing through or waiting for a friend never gets shot.
- **Bank:** replacement cards are expensive, and money is shared across all safe zones.
- **Storage units:** about 50–100 lbs for a fee, mainly for solo players. Items only come out where you stored them.

**Currency name ideas,** all invented:
- **Zollars:** "Z" plus "dollars". It ties to the Z in NYZ and sounds like money right away.
- **Nykels:** "NY" plus "nickel". Very New York.
- **Quarants:** from "quarantine", fitting the emergency-currency backstory.
- **Vells:** a made-up word with no meaning attached, if you'd rather keep it neutral.

*My pick: Zollars.* It's obviously money, and it's obviously this game.

**Two small things still open:**
- **Storage unit fee:** a one-time payment, or **rent** (for example, every few days)? Rent keeps the economy healthy, because money keeps leaving the world, and it stops abandoned units piling up. My pick is rent.
- **Staten Island:** does the small piece get a safe zone too, as part of the 6–7?

**After this, topics left at high level:** weather and day/night, server persistence and wipes, character creation, lore, the full points-of-interest pass, farming.

### Developer (2026-10-27 18:40)

Rent, and yes small safezone. I like your currency idea names, give me more

### Claude (2026-10-27 18:40)

Recorded: storage units use **rent**, and the Staten Island piece gets a **small safe zone**.

More currency names, grouped by feel:

**Tied to NYC or NYZ**
- **Zollars:** Z + dollars
- **Zimes:** Z + dimes. "Got any zimes?"
- **Nykels:** NY + nickel
- **Boros:** from "borough". "Twenty boros" sounds like real slang.
- **Fivers:** the five boroughs, and it already sounds like money
- **Zennies:** Z + pennies

**Emergency or quarantine feel**
- **Quarants:** from quarantine
- **Relis:** from relief, as in "relief notes"
- **Sanctos:** from sanctuary, the safe zones' own money
- **Holdos:** from holdout

**Invented, sounds like money**
- **Vells**
- **Kreds**
- **Tavs**
- **Dravs**
- **Orrins**
- **Bexes**

**Bills can have a nickname too,** like "bucks" for dollars. For example, the official name could be **Zollars** and players could call them **"Zs"**, as in "that rifle's 400 Zs". That would fit how players naturally talk.

My favorites are **Zollars** ("Zs"), **Boros** and **Quarants**.

Before you lock one in, search the name online. Another game or brand might already use it, and I haven't checked any of these.

### Developer (2026-10-27 18:41)

I kinda like Sanctos Notes. Zollars sounds hella zesty cant lie to ya, Boros and Quarants are kind of cool, Keep them for consideraton

### Claude (2026-10-27 18:42)

Ha, fair, Zollars is out. The shortlist is saved in GDD §18:

- **Sanctos Notes** is the leading candidate.
- **Boros** and **Quarants** are still in the running.

One heads-up on Sanctos: "sanctos" happens to be an actual word form in Latin ("the holy ones"). That's obscure enough that nobody will think of it as a real word, and the sanctuary meaning fits the safe zones well. It isn't strictly a made-up word, though, so it's your call whether that matters. It also comes out naturally as **"Notes"** in casual talk, as in "that's 300 notes".

Trading and safe zones are done at high level. **Topics left:** weather and day/night, server persistence and wipes, character creation, lore, the points-of-interest pass and farming. I'd suggest **server persistence and wipes** next. It's a big decision that affects how bases, the economy and progression feel over time.

### Developer (2026-10-27 18:42)

Weather

### Claude (2026-10-27 18:43)

## Weather, day/night and seasons: my proposal

**1. Day/night cycle**
- **About 3 real hours for a full day,** with **about 45 minutes of night**. It's a server setting. Long enough that a play session feels like a day, short enough that everyone sees night regularly.
- **Real darkness:** the power is out, so there are no streetlights. Light comes from the moon (with phases), fires, generators and flashlights. A lit window at night gives a base away.

**2. Night is dangerous, in both directions**
- Zombies see worse at night (decided, §8). **But more of them roam the streets at night,** so moving in the dark is a gamble: harder to spot, more to run into.
- **Flashlights and weapon lights give you away** to players and zombies.
- **Night vision goggles:** military, very rare.

**3. Weather types, NYC-flavored**

| Weather | Effect |
|---|---|
| **Clear** | Normal |
| **Overcast** | Darker nights (no moon) |
| **Rain** | Soaks you (body temperature, §7), fills rain collectors (§14), **muffles noise** so sounds carry less far, and cuts sight a little |
| **Thunderstorm** | Like rain, and **thunder masks gunshots** for a moment, a chance to fire unheard |
| **Harbor fog** | Rolls in off the water; **heavy sight loss** for everyone, worst near the rivers and harbor |
| **Snow** (winter) | Cold, slows movement, and **leaves footprints** others can follow (ties to the Survival skill's tracking, §6) |
| **Heat wave** (summer) | You get thirsty much faster |

**4. Seasons: they cycle**
- Spring, summer, fall and winter rotate on a cycle, with **each season about 1–2 real weeks** (a server setting; a server can also lock one season).
- Seasons set the temperature range and the weather mix: summer brings heat waves and thunderstorms, winter brings snow and the cold.
- **Winter is the hard season:** clothing, shelter and fire matter much more, which is a natural boost for base building.
- Seasons tie into **farming** later (growing seasons).

**5. Big rare weather events**
- **Nor'easter / blizzard:** a rare winter storm. Heavy snow, very cold, almost no visibility. Everyone hunkers down, which makes it a good time to raid.
- _Maybe later:_ a **hurricane with flooding** in low areas (Red Hook, Lower Manhattan, the Rockaways, as during Sandy). It's a great NYC event, but water levels that change across the map are a big technical job.

**6. Weather forecast on the radio**
- A **weather radio** item picks up an automated emergency broadcast with a short forecast: "storm moving in tonight." It's useful for planning raids and trips, and it's a natural lore channel too.

**7. Easy to learn**
- The HUD shows the current weather and how cold or hot it feels. The effects follow the survival stats you already understand (§7), with no new stats.

**8. Server cost: low**
- The server only tracks the weather state. Rain, fog and snow visuals are drawn on each player's own PC.

**To answer:** yes or changes per number. The main choices are the cycle length (1), more zombies at night (2), the season cycle (4) and the hurricane maybe (5).

### Developer (2026-10-27 18:46)

1. 3 hrs day 1 hr night
2. Zombies see worse at night yes, attracted to flashlights, idk could make it way harder than im intending, but i guess that impacts lore. NVGs, yes, very rare
3. Yes to those, but add blizzard/heavysnowfall, it will be more rare than just snow
4. Yes
5. Lol you keep getting to it before I do. Yes, these are both great
6. Who is making a weather broadcast in an apoclypse? Better yet, are they still operating weather ballloons to find out???
7. Yes, but only a general feel. A watch or something else can show exact time and temp
8. Yes

### Claude (2026-10-27 18:47)

Recorded in [GDD §19](docs/GDD.md) and the decision log:

- **3 hours of day, 1 hour of night.**
- **Blizzard and heavy snowfall** added as a weather type, rarer than regular snow.
- **Both the nor'easter and hurricane flooding are in.** The hurricane gets a note: flooding that rises and drains across the map is a big technical job, so it's worth testing early what Unreal's water tools can handle.
- **The HUD only gives a general feel** of weather and temperature. A **watch** or a **thermometer** shows the exact time and temperature.
- **Whether zombies are drawn to flashlights** is undecided and tied to lore.

**On the weather broadcast:** you're right, nobody is launching weather balloons in an apocalypse. Realistic options:

- **A. A barometer item.** This is how people forecast for centuries before satellites: when air pressure drops fast, a storm is coming within hours. No broadcaster needed, just a found item, and it's actually how sailors did it.
- **B. Safe-zone radio.** The group running the safe zones is clearly organized (guards, snipers, a bank). They'd broadcast short-term warnings from someone reading a barometer and the sky. It's also a ready-made lore channel.
- **C. Automated stations.** Real automated weather stations at the airports and in Central Park report *current* conditions without anyone running them. On backup power they could keep reporting for a while, but only current conditions, not forecasts.
- **D. No forecasts at all.**

*My pick: A plus B.* The barometer is the realistic tool anyone can use, and the safe-zone broadcast adds flavor and lore. All four options are in §19's open items.

**Topics left at high level:** server persistence and wipes, character creation, lore, the points-of-interest pass and farming.

### Developer (2026-10-27 18:48)

A B

### Claude (2026-10-27 18:48)

Recorded in GDD §19 and the decision log. Forecasts come from:

- **A barometer:** a found item. Falling pressure means a storm is coming within hours.
- **Safe-zone radio:** the safe-zone group broadcasts short-term warnings, which also works as a lore channel.

Weather has one open item left: whether flashlights draw zombies, which we'll settle with lore.

**Topics left at high level:** server persistence and wipes, character creation, lore, the points-of-interest pass and farming.

### Developer (2026-10-27 18:48)

Server persistence next

### Claude (2026-10-27 18:48)

## Server persistence and wipes: my proposal

**1. The big choice: does the world ever reset?**
- **Never wipe** (DayZ): progress feels permanent. But big clans dig in for good, new players face fortresses, and the server fills with clutter.
- **Scheduled wipes** (Rust): everyone starts fresh and equal on a fixed date. But losing everything frustrates casual players.
- *My pick: scheduled wipes tied to the seasons.* **One wipe per in-game year:** spring, summer, fall and winter, then a fresh start in spring. At 1–2 real weeks per season, that's a **wipe every 1–2 months**. It gives each server a story arc: build up through summer, survive winter, the world resets with the thaw. That's lore-friendly too.

**2. What a wipe clears and what it keeps**

| Wiped | Kept |
|---|---|
| Bases, storage, buried stashes | Character appearance |
| Items, vehicles, helicopters | Clan name and graffiti tag design |
| Bank money and storage units | Stats and achievements (e.g., "survived 3 winters") |
| **Levels and recipes** | |

- *Why wipe levels too:* everyone restarts equal. The journal (§6) and the catch-up boost already make leveling back up quick, and levels are lost on death anyway.

**3. Characters belong to one server**
- Your character lives on one server. **No shared character across servers** (DayZ's "hive"), because that lets players loot an empty server and carry the gear into a busy one.
- You can play on several servers, with a separate character on each.

**4. Server restarts**
- **A restart every 6–12 hours** for performance. Warnings at 15, 5 and 1 minutes.
- **Restarts don't count as combat logging**, so the quit lock (§17) doesn't apply.
- **Everything persists through restarts:** bases, buried items, vehicles, bodies until their timers run out.

**5. Saving and crashes**
- The world saves continuously, with important changes saved immediately: building, trades, bank deposits. **After a crash, the rollback should be seconds or a minute at most**, so nobody loses a raid's worth of loot to a crash.

**6. Clutter control: already decided, listed together**
- Base decay when nobody visits (§9), abandoned vehicles despawn (§16), dropped items despawn (§12), bodies last 2 hours (§10), containers reset through the central economy (§12), storage units cost rent (§18).

**7. Official and community servers**
- **Official servers** run the default settings and the season wipe.
- **Community servers** can be rented and change the **server settings**, including the wipe interval or "never wipe".
- _Later:_ mod support. It's a big job in Unreal, so I'd keep it out of the launch plan.

**8. Server settings in one place**
- The design already has a lot of server settings: player cap, first-person only, clan cap, friendly fire, offline raid protection mode, day/night length, season length and season lock, and vehicle caps. When we build, they go into **one settings file** with documented defaults.

**9. Admin tools**
- For server operators: kick and ban, spectate, **logs** (kills, raids and trades, for settling disputes and catching cheaters), and an item spawner for community events.

**To answer:** yes or changes per number. The main choices are seasonal wipes (1), wiping levels too (2), one server per character (3) and community servers (7).

### Developer (2026-10-27 18:53)

Maybe every 6 months- a year, realistically this could change after release depending on player feedback. I dont want progress to be for nothing. 

2. Yes to all
3. Agreed.
4. Yes
5. Agreed
6. Agreed, also maybe instead of just abanadoned, if many vehicles are spawned in areas without players, each vehicle should have a radius and a timer, and if no player enters that radius (a few block, not very small one) within the set timer time, the car respawns elsewhere. Also storage units will literally just be the building for the SZ and bank, you cant physically live in it.
7. Agreed.
8. Agreed
9. Agreed

### Claude (2026-10-27 18:53)

Recorded in [GDD §20](docs/GDD.md) and the decision log. This also closes the old "permanent world or scheduled wipes?" open question.

- **Official servers wipe every 6 months to a year,** and that can change after release based on player feedback. With that much time between wipes, progress means something.
- **Your vehicle rule is in:** a vehicle the world spawned that nobody comes near (within a few blocks) before its timer runs out respawns somewhere else. I read it as applying only to untouched world vehicles. Vehicles players own still follow the abandoned-vehicle rule.
- **Storage units** are a service in the safe-zone building, not a room you can live in.
- Also recorded: characters stay on one server, restarts every 6–12 hours, crash rollback of seconds, community servers, one settings file, and admin tools.

**Left at high level:** character creation, lore, the points-of-interest pass and farming. After those, the game is mapped out, and the source-control reminder comes up.

### Developer (2026-10-27 18:53)

Yes, let's do character creation next. Give me your proposal.

### Claude (2026-10-27 18:54)

## Character creation: my proposal

**1. Appearance: presets plus a few sliders**
- **Body type** (two base bodies), **face presets** plus a few sliders, **skin tones, hair, facial hair, tattoos.**
- **Age:** young adult up to older adult. Purely cosmetic, with no stat effects.
- **Voice:** a few voice sets per body type, for grunts, pain sounds and the hands-up callout.
- Not a deep face-sculpting system. Those are expensive to build, and in first person nobody sees your face much anyway.
- **Appearance carries over through wipes** (decided, §20).

**2. Handedness:** left- or right-handed, and players aren't told why it matters (decided, §7).

**3. Occupation: an NYC job before the outbreak** (Project Zomboid-style, kept light)

Each occupation gives **a couple of free recipes or skills (worth about 2–3 points) plus one small starting item. Never combat bonuses**, to keep PvP fair (§6).

| Occupation | Free knowledge | Starting item |
|---|---|---|
| **Nurse** | Basic medical recipes | Extra bandages |
| **Mechanic** | Vehicle repair basics, hotwiring older cars (§16) | Screwdriver |
| **Construction worker** | Basic building pieces | Hammer |
| **Line cook** | Cooking recipes (better meals for mood, §7) | Kitchen knife |
| **Firefighter** | Fire safety, forcing doors | Fire axe? (maybe too strong) |
| **Bike messenger** | Bike repair, faster bike handling | Bike lock |
| **Cab driver** | Car handling, knows the streets | City map |
| **Subway worker** | Knows the tunnels (subway map) | Headlamp |
| **Dockworker** | Container yards (§12): opening seals faster | Work gloves |
| **Bodega owner** | Better prices at traders (§18) | A little currency |
| **Unemployed** | No knowledge, but **+2 extra recipe points** | — |

- **You pick your occupation again each time you start a new life** after dying. You start fresh anyway, so you can adapt.

**4. No traits system at launch**
- Project Zomboid's positive and negative traits (fast learner, smoker, and so on) add a lot of depth, but also a lot to learn. Occupations give enough identity. Traits go in "Maybe later".

**5. Name**
- A character name, visible only to clanmates (name tags, §15). Strangers stay anonymous (§17).

**6. Starting outfit: pick a style**
- The starting kit is basic clothes (§10). **You choose its look** from a few civilian outfits: hoodie and jeans, work clothes, office clothes, track suit. Cosmetic only, and a cheap way to make each spawn feel personal.

**7. Maybe later: scars**
- Serious wounds you survive leave visible scars until you die. A nice survival story told by your body, but not a launch priority.

**To answer:** yes or changes per number. The main choices are occupations (3), re-picking the occupation each life (3), no traits (4) and the outfit choice (6).

### Developer (2026-10-27 18:56)

1. Agreed
2. Agreed
3. agreed, can refine what each thing will give later. 
4. Agreed, maybe the "trait" can just tie to the skill itll give you instead"
5. Agreed
6. Agreed
7. Agreed

### Claude (2026-10-27 18:56)

Recorded in [GDD §21](docs/GDD.md) and the decision log.

- **Occupations replace a traits system.** Each job's free skill is that character's "trait". What each one gives will be refined later, including whether the firefighter's fire axe is too strong to start with.
- **Scars** are parked in "Maybe later".

**Three topics left at high level:**
- **Lore:** what happened, who runs the safe zones, special zombies and lore areas, and whether flashlights draw zombies.
- **Farming:** rooftop and community gardens, growing seasons.
- **The points-of-interest pass:** best done after lore, since lore decides a lot of what's where.

I'd do **lore** next. Several decisions are waiting on it: special zombies, lore areas, the flashlight question, the safe-zone group, and the outbreak's origin.

### Developer (2026-10-27 19:10)

Let's do farming next. Give me your proposal.

### Claude (2026-10-27 19:11)

## Farming: my proposal

**1. Where you can grow: NYC-style**
- **In the ground:** anywhere diggable (parks, backyards, empty lots, community gardens). It's the same ground rule as burying journals (§6).
- **Raised beds and planters:** crafted and filled with **bags of soil** (from hardware stores and garden centers). Put them on **rooftops**, balconies or inside your base. Rooftop farming becomes the city-style way to farm.
- **Community gardens** across the city start with some overgrown crops and good soil, which makes them small contested spots.

**2. What you grow: about 8 crops, tied to the food groups (§7)**

| Crop | Food group | Note |
|---|---|---|
| Tomatoes, peppers, leafy greens, squash | Vitamins | The easy fix for a poor diet |
| Potatoes, corn | Carbs | Filling, store well |
| Beans | Protein | **Dried beans from a bodega can be planted** |
| Herbs | (cooking) | Make cooked meals better for mood (§7) |

**3. Seeds**
- Found at garden centers, hardware stores and community gardens, plus **dried food from groceries** (beans, some seeds).
- **Harvesting gives seeds back**, so a farm keeps itself going once started.

**4. Growing: simple to learn**
- **Plant, water, harvest.** Each plant shows small icons: "needs water", "ready".
- **Water:** rain does it for you (§19). Otherwise a watering can, using water from collectors (§14).
- **Crops grow in real time, even while you're offline.** Growth times are in real hours, roughly a few hours to a day depending on the crop.
- _Optional:_ **compost** made from rotten food (§12 decay) speeds growth. It gives rotting food a use.

**5. Seasons matter** (§19)
- **Spring and summer:** fast growth. **Fall:** slower, harvest time. **Winter:** outdoor crops die from frost.
- **Greenhouses** (crafted) protect crops into the cold months.
- **Endgame: indoor grow lights** (hydroponics-style) grow food all year, **but need power** from a generator or solar (§14). A lit grow room at night also shows from outside (§19).

**6. Risks**
- **Crops outside your base can be stolen** by other players, and **zombies trample** fields they wander through.
- Rooftop and indoor farms are safer, at the cost of carrying soil and water up there.

**7. Mood bonus:** tending a garden **eases boredom and stress a little** (§7). It's a calm thing to do at base.

**8. Small livestock: chickens**
- **Backyard chickens** (a real thing in NYC's outer boroughs) can be found and kept in a crafted coop. They give **eggs (protein)**. They need feed and water, and they can be stolen or eaten by zombies.
- _Maybe later:_ rabbits.

**9. Server limits**
- Crops and coops count toward the clan's building piece cap (§9), so farms can't sprawl and slow the server down.

**Related, but not farming:** **fishing** in the rivers and harbor (the Survival skill category, §6), as a protein source. We can design that with the points-of-interest pass or now, whichever you prefer.

**To answer:** yes or changes per number. The main choices are rooftop planters (1), the crop list (2), real-time offline growth (4), winter frost and greenhouses (5) and chickens (8).

### Developer (2026-10-27 19:12)

1. Agreed
2. Agreed
3. Agreed
4. Agreed, compost a good idea
5. Agreed
6. Agreed
7. Agreed

### Developer (2026-10-27 19:13)

1. Agreed
2. Agreed
3. Agreed
4. Agreed, compost a good idea
5. Agreed
6. Agreed
7. Agreed
8. Agreed
9. Agreed
10. Maybe hunting? We still havent gone over setting too much in detail, but i want it to be an overgrown beat down version of nyc. To the point that some wild animals have started coming back from where the would, like stuff from the north making its way into the city. Fising also for sure

### Claude (2026-10-27 19:14)

Recorded in [GDD §22](docs/GDD.md) and the decision log, with compost in. The **overgrown, beaten-down NYC** is now written into the setting in §5, and I like it a lot. One thing it implies: overgrowth like that takes years, so the outbreak must have happened **years before the game starts**. That's a lore question for later.

## Wildlife and hunting: a quick proposal

Many of these animals already live in or near NYC today. In an overgrown city, it's believable they'd spread.

**Prey** (food and materials):

| Animal | Where | Gives |
|---|---|---|
| **Deer** | Parks, Bronx, Staten Island | Lots of meat, hide |
| **Wild turkeys** | Parks, Staten Island | Meat, feathers (arrows) |
| **Geese and ducks** | Parks, Jamaica Bay | Meat, feathers |
| **Rabbits** | Parks, overgrown lots | A little meat |
| **Pigeons and rats** | Everywhere | Desperation food |

**Dangers:**

| Animal | Why |
|---|---|
| **Feral dog packs** | Former pets gone wild. The most common animal threat, hunting in packs |
| **Coyotes** | Already in the Bronx and Queens today. Packs, mostly at night |
| **Black bears** | **Coming down from the north**, through NJ and the Bronx. Rare and very dangerous |
| **Bobcats** | From the north. Rare, ambush hunters |

**How hunting works:**
- **Meat** (protein, §7), **hides** for leather (a leather jacket blocks bites, §8), and **feathers and sinew** for arrows and bowstrings (§14).
- **Gunshots attract zombies,** so **bows are the hunter's weapon**. That gives the quiet weapons another purpose.
- **Tracking:** footprints in snow (§19) and blood trails, part of the Survival skill (§6).
- **Hunting grounds:** the big parks (Central, Prospect, Pelham Bay, Van Cortlandt, Forest Park), Jamaica Bay and the Staten Island piece.
- **Animals run from zombies.** No zombie animals, unless lore says otherwise.
- **Server cost:** animals use AI like zombies do, so they count toward the same AI limits (§3).

**Bonus NYC touches:** **seals in the harbor** (they really are there today) and a **beaver** in the Bronx River, as small world details.

**To answer:** hunting yes or no, and changes to the animal list.

### Developer (2026-10-27 19:16)

agreed, no animal zombies. Seals and beavers as a rare sighting would be fucking sick. Keep them, and yes to answer

### Claude (2026-10-27 19:16)

Agreed, rare seal and beaver sightings will be great moments. It's all in [GDD §22](docs/GDD.md) and the decision log:

- **Hunting is in.** Prey: deer, turkeys, geese and ducks, rabbits, and pigeons and rats when you're desperate. Dangers: feral dog packs, coyotes, and black bears and bobcats coming down from the north.
- **No zombie animals.** Animals run from zombies.
- **Bows are the hunter's weapon,** since gunshots draw zombies.
- **Seals in the harbor and a beaver in the Bronx River** as rare sightings.

**Only two topics left at high level:**
1. **Lore:** what happened and when (the overgrowth implies years ago), who runs the safe zones, the special zombies and lore areas, and whether flashlights draw zombies.
2. **The points-of-interest pass:** what's where on the map. Best done after lore.

After those, the whole game is mapped out at high level, and the source-control reminder comes up before any UE5 work starts.

### Developer (2026-10-27 19:16)

Yes, let's do lore next. Give me your proposal.

### Claude (2026-10-27 19:17)

## Lore: my proposal

**1. Timeline: the game starts about 7 years after the outbreak**
- Seven years is long enough for real overgrowth (trees through asphalt, vines up the towers, animals back), and short enough that canned food, guns and cars still mostly work.

| When | What happened |
|---|---|
| Year 0, week 1 | The outbreak hits NYC |
| Weeks 2–4 | **Quarantine:** bridges and tunnels closed, and the military throws up a **wall along the major highways** |
| Months 2–6 | The city falls. Evacuation fails; the military pulls out and leaves bases and caches behind |
| Year 1–2 | **A hurricane floods** the low areas, wrecking what was left |
| Year 3–5 | Survivors organize: **the safe-zone network** forms in old warehouses and towers |
| Year 7 | **The game starts** |

**2. The quarantine wall explains the map border**
- The military built the wall fast, so it **follows the major highways**, which is exactly our border rule (§5). The design and the lore match.
- The bridge checkpoints were overrun or abandoned, which is why the GWB and the other bridges are open (§16).

**3. Where the outbreak started: pick one**
- **A. A lab accident:** a research lab inside the city, on **Roosevelt Island** for example, which has real history as an island of old hospitals.
- **B. It came from outside:** NYC was one city among many. Nobody inside knows how bad the rest of the world is.
- **C. A mystery:** nobody knows for sure. Players piece it together from notes, radio scraps and lore areas.
- *My pick: C, with clues that point toward A.* It gives players something to discover, and we never have to explain everything.

**4. Who the players are**
- People who **survived the 7 years in hiding**: sealed apartments, subway shelters, basements. Now they're coming out. That explains fresh spawns with basic gear, and why every new life is another survivor.

**5. The safe-zone group: "The Sanctuary"**
- Ex-military and civilians who **organized the safe zones, enforce the peace with snipers, run the bank, and print the currency.** That's why the money is called **Sanctos Notes** (§18). They also run the radio broadcasts (§19).
- Neutral and trade-minded. What they really want can stay a mystery players dig into.

**6. The antiviral**
- A research team inside the quarantine zone made a cure **late in the collapse**, and only a few batches survived. That's why it's in hospitals and labs (§8) and why it's top-tier rare (§12).

**7. Special zombies (1–2) and lore areas**
- **The Screamer:** when it spots you, it **shrieks and pulls in every zombie nearby.** It fits our sound-driven hordes (§8). Rare, and you want it dead before it sees you.
- **The Patient:** an early-strain infected found **only at lore areas**. Tougher (it takes more head damage to drop), and **the only zombie that truly runs.** It can carry lore items or keys.
- **Lore areas** (also points of interest):

| Place | What it is |
|---|---|
| **North Brother Island** | The real old quarantine hospital, used as the first quarantine site |
| **Roosevelt Island lab** | The research lab from origin A |
| **Fort Hamilton** (Brooklyn) | A real Army base, used as the quarantine headquarters |
| **The antiviral lab** | Where the cure was made, at a hospital research center |

**8. How the lore is told: no cutscenes**
- Notes, other survivors' journals, radio scraps, graffiti and environmental details: DayZ-style. Players who care can dig in; players who don't are never forced to.

**9. Flashlights** (open from §19)
- *My suggestion: no special pull.* Zombies notice a light the way they notice you: up close, when they're facing you. Your worry was nights getting too hard, and this keeps them fair.

**To answer:** yes or changes per number. The main choices are the 7 years (1), the origin (3), the Sanctuary (5), the two special zombies (7) and flashlights (9).

### Developer (2026-10-27 19:23)

I feel like 1-2 should come after 3 no?

### Claude (2026-10-27 19:23)

You're right. The origin shapes everything after it: how fast it spread, why the city was walled off, and what's in the lore areas. Let's settle that first.

**3. Where the outbreak started:**
- **A. A lab accident in the city** (Roosevelt Island, for example). The timeline then starts with a local leak, the city gets walled off fast to contain it, and the outside world may be fine. That raises a lore question of its own: why has nobody come back?
- **B. It came from outside.** NYC was one city among many in a wider collapse. The wall was a failed attempt to save the city, or to keep it in. Nobody inside knows how bad the rest of the world is.
- **C. A mystery.** It stays officially unknown, and players piece it together from clues. The clues can lean toward A or B, or point both ways.

Here's how the choice ripples:
- **Timeline (1):** A means a short, sharp collapse that started here. B means NYC fell as part of something bigger.
- **The wall (2):** A means "contain it here". B means "seal the city off from the outside".
- **The lore areas (7):** A puts the lab at the center. B puts the quarantine headquarters and the ports at the center.

My pick is still **C, with clues leaning toward A**. Which way do you want to go?

### Developer (2026-10-27 19:30)

B + C. it came from outside, but not everyone really knows what it is or whats going on outside. In reality, the whole world is just like the city, some surviovrs and safezones, but for the most part the whole world is cooked. Maybe it started outside and a lot of researches and scientest came to the city to do testing and research, so they walled it off. Or maybe something like that, where it came from outside, but spread in the city due to experiementing/research. Up until it spread Inside the walls, it was well on lock and holding its ground well. With the c coming from some kind of mystery or plot twist about it. I want a DEEP DEEP lore, not explained by any cutscenes or anything, but the same way zomboid does it, clues in the world and radio broadcast, although in zomboid the broadcast works becasue it starts at day 0. Maybe random broadcast. IDK, i wanna build the deep lore before getting too involved in game development, since that has a big impact

### Claude (2026-10-27 19:31)

Agreed: lore first, and deep. It now has its own document, the **lore bible** at [docs/lore/LORE.md](docs/lore/LORE.md), because it'll get too big for the GDD. GDD §23 holds a short summary that links to it.

**What's in it so far:**
- **The decided origin:** it came from outside, and the whole world has fallen. Researchers came to NYC to study it, the city was walled off and held well, then it spread inside the walls because of the research. There's a mystery or twist on top, still to write.
- **Two layers:** *the truth*, which only we know, and *what survivors believe*, which is partly wrong. That split is what makes Project Zomboid-style clue hunting work.
- **A checklist of every game rule the lore has to explain.** For example: why only infected people turn, why animals don't, why fresh zombies are faster, why there's a cure, and who runs the safe zones and why they have elite snipers.
- **Your radio point is solved with random broadcasts** from whoever is still transmitting. Candidates: the safe-zone group's station, automated loops still repeating years-old evacuation orders, coded numbers stations, unreliable survivor stations, and faint signals from outside the wall. Because wipes are 6–12 months apart, **new broadcasts can unlock over a server's life**, so the story unfolds in seasons.

**Order to build it:** the truth and the twist first, since everything hangs on it. Then the timeline, the infection itself, factions, radio, lore areas and special zombies.

**Twist directions to react to** (pick, mix, or throw them out):
1. **The wall was never meant to keep it out.** NYC was picked as the research site *because* it could be sealed, and the people inside were never told they were part of the study.
2. **The research wasn't for a cure.** It was to control the infection, and the antiviral was a by-product.
3. **The breach inside the walls wasn't an accident.**
4. **The safe-zone group knows more than it says.** Its founders came out of the research program.
5. **The special zombies are the original test subjects.**
6. **The outside world isn't what the radio suggests.**

My favorite combination is **1 + 4 + 5**. The wall becomes sinister, the safe zones become suspicious, and the special zombies become evidence. Each layer is something players can discover through clues.

### Developer (2026-10-27 19:34)

1, 3, 4, 5.

### Claude (2026-10-27 19:35)

The twist is chosen. I kept the four layers **only in the lore bible**, not in the GDD. Volunteers who read the GDD later won't get the story spoiled, and the lore bible becomes the "need to know" document.

**The truth, as chosen:**
1. The wall was never meant to keep it out. The people of NYC were **unknowing study subjects**.
2. The breach inside the walls **wasn't an accident**.
3. The safe-zone group's **founders came out of the research program**.
4. The special zombies are **the original test subjects**.

Now the details. Four questions, each with options and my pick:

**Q1. Who caused the breach, and why?**
- **A.** The program's leaders, on purpose. The study needed a *live* outbreak inside a population, so the breach *was* the real experiment.
- **B.** A group inside the program opened it to escape, or to expose what was going on, and it went wrong.
- **C.** The military, as a fail-safe: sacrifice the city to end the study.
- *My pick: A.* The founders of the safe-zone group were in the room when it was decided. That ties layers 2 and 3 together: the people keeping you "safe" helped cause it.

**Q2. What was the study?**
- **A.** A **"free vaccination drive"** for residents, actually test doses given without real consent.
- **B.** Something added to the **water supply**. That makes the rooftop water towers quietly creepy for lore hunters.
- **C.** **Emergency food aid** with something in it.
- *My pick: A, with a hint of B as a rumor.* Vaccination records, clinic flyers and dose cards make great clues to find around the city.

**Q3. What do the safe-zone founders want now?**
- **A. Atonement:** they genuinely protect survivors out of guilt.
- **B. A cover-up:** they control the radio, and their snipers keep people away from certain places.
- **C. The study never stopped:** the safe zones are observation posts. That bank card "linked to your character" (§18) means **they register every survivor**.
- *My pick: B and C together, left ambiguous.* Some members may truly want A, which gives you factions within the group later.

**Q4. The test subjects as special zombies**
- **The Patient** (the tough one that runs) is an original test subject, found at the study sites.
- **The Screamer** (summons hordes) is a failed later dose.
- Both appear only at lore areas: the labs, North Brother Island, the quarantine headquarters.

**To answer:** pick per question, or mix. Once these are set, the timeline nearly writes itself.

### Developer (2026-10-27 19:37)

Give me more options for q1

### Claude (2026-10-27 19:37)

More options for **Q1: who caused the breach, and why?** All of these keep the chosen layers: the breach was on purpose, the founders came from the program, and the residents never knew.

**D. Destroying the evidence.** An outside oversight team was about to arrive and uncover the unconsented trials. The leadership released the infection to "burn" the evidence, and the cover-up became the catastrophe.
*Clues:* an inspection schedule, shredded documents, a memo saying "the commission arrives Tuesday".

**E. The escape plan.** Funding was collapsing along with the outside world, and the program was being shut down. The leaders released it as cover to slip out of the city by boat or helicopter while everyone panicked. The founders of the safe zones were the ones left behind, who knew exactly what happened.
*Clues:* an evacuation manifest with only staff names, an empty helipad log. It ties into the helicopters and ports.

**F. The cure trial at scale.** A company backing the program needed proof the antiviral worked on a *real* outbreak, not just in a lab. So they made one. That's why antiviral batches exist at all.
*Clues:* company memos and dosing charts, plus a quietly horrifying "phase 3: field conditions".

**G. One true believer.** The lead scientist was convinced the strain had to spread through a large population before a real cure could be found. "The ends justify the means." A single person, a single choice.
*Clues:* personal journals that grow more unhinged over time. That's a great thread to collect.

**H. Sabotage gone wrong.** Someone tried to destroy the lab to *end* the experiments and broke containment instead. It was deliberate, but not meant to do this.
*Clues:* a whistleblower's notes and a bomb-making shopping list. The founders hide that one of their own did it.

**I. Orders from outside.** With the world collapsing, whoever was still in charge outside wrote NYC off and ordered one last full-scale trial. The people inside carried it out.
*Clues:* an encrypted order, and a reply that says only "understood".

**J. A cult inside the program.** A group of researchers came to believe the infection was humanity's next step, and freed it.
*Clues:* strange symbols in the lab areas and graffiti that spreads across the city. This one leans darker and stranger.

**My favorites:**
- **D (destroying the evidence):** it connects directly to the founders' cover-up today. They're still hiding the same thing.
- **E (the escape plan):** it explains why the founders were left behind, and it pays off the helicopters and ports.
- **G (one true believer):** the best for collectible clues, a scientist's journals across the map.

**These combine well.** For example: **D and E together.** The commission was coming, so the leaders released it to destroy the evidence *and* to cover their own escape. The staff who were left behind became the safe-zone founders, and they're still hiding it. Or **G inside D**: one true believer pushed the leadership into it.

### Developer (2026-10-27 19:40)

To note, the study and expirements being run, on surface level were for finding a cure that could be mass produced. The problem with the current cure, is that it is extremely difficult to produce with its known materials. They genuinely had good intentions, myabe something could make them flip or something?

### Developer (2026-10-27 19:40)

now with that said, give me options

### Claude (2026-10-27 19:41)

That changes things in a good way. Good people who flip are far more interesting than villains. I've added your details to the lore bible: the goal was a cure that could be mass-produced, the existing cure is extremely hard to make, and the researchers meant well.

## What made them flip: options

**1. The impossible ingredient.** They found the scalable cure needs something that can only come from **many infected people**, like antibodies from survivors or the strain after it passes through thousands of hosts. Saving billions outside meant sacrificing one city. The math flipped them.
*Clue:* a whiteboard that reads "8.3 million vs 7 billion."

**2. The strain had to evolve.** The cure only works on a **later form** of the strain, and that form only appears after it spreads through a large population. They released it to force the change.
*Clue:* mutation charts with "target: generation 40."

**3. The world went dark.** Contact, funding and orders from outside stopped. Believing they were **humanity's last chance**, with supplies running out, they took the only shortcut left.
*Clue:* the last radio log, then silence.

**4. Someone they loved.** The lead researcher's child was infected, and the slow, careful route would never save them in time. One person's grief pulled the team over the line.
*Clue:* a child's drawings pinned up in a lab office.

**5. Hubris: "we can contain it."** They ran out of willing subjects and planned a **small, controlled release** inside the walls, certain they could contain it. It got away.
*Clue:* a containment plan with a confident timeline, and the outcome crossed out.

**6. Ordered to, under threat.** What's left of the authority outside threatened to cut supplies, or worse, unless they produced results fast. Good people complied.

**7. A rushed cure.** People were dying, so they knowingly released an **unproven cure** to the residents (the "vaccination drive" from Q2), and it backfired.

**8. Infiltrated.** Backers with a different agenda quietly took over the program. The good researchers only realized when it was too late, and some of them became the safe-zone founders, carrying the guilt.

## My pick: 3, then 1, then 5, as a chain

The **world went dark**, so the pressure was on. Then they found the **cure needs many infected hosts**, which is the math. Then they convinced themselves they could **contain a small release**, which is the hubris, and it got away. Good intentions all the way down, which makes it tragic rather than evil.

**It also ties into what's already decided:**
- **The safe-zone founders were part of that decision.** Today they hide it (the cover-up) **and still need infected hosts or samples to make the cure** (the study never stopped). Their bank registering every survivor (§18) suddenly looks sinister.
- **Traders never sell the antiviral** (§18). In the lore, the safe-zone group **hoards** what little they can make.
- **The Patients** (special zombies) are the original test subjects from before the release.

One caution if you pick option 5: don't have the "small release" target a specific real neighborhood chosen by who lives there. That would read as targeting a real community. A district picked for practical reasons, like being easy to seal off, avoids that.

All eight options are saved in the lore bible. Pick one, chain a few, or mix.

### Developer (2026-10-27 19:44)

3 then 1, maybe not many infected people but with the city as locked down as it was, it was too risky to go on expeditions bring them in from the outside, as they already extered zombies from nearby towns. Then 5. I just feel like thats kind of predictable, at least a bit. Yeah i would probably not go by who lives there, but the population, and other practical reasons.

### Claude (2026-10-27 19:45)

Saved in the lore bible. Your version of step 2 is better than mine: test subjects came from **expeditions outside the wall**, nearby towns had already been used up, and further trips were too risky. It's concrete, it's logistical, and it fits a locked-down city. The release site is recorded as chosen by population and practical reasons only.

You're right that "they released it and it got away" is a bit predictable on its own. The fix is to make that **the answer players find first, not the real one.** Ways to turn it:

**A. The containment was sabotaged.** The small release really was planned, and it really would have held, but someone **deliberately broke the containment**. That's a second deliberate act. Who did it? Maybe one of the founders, maybe a researcher who wanted the program exposed, maybe someone who wanted it to spread. The founders' own story ("it got away from us") is a lie, or they don't know either.

**B. It worked.** The release succeeded, and **they found the scalable cure**. Then it was hidden, lost or destroyed. Now the method is somewhere in the city, and it becomes the deepest thing lore hunters can chase. Why hide it? Maybe making it needs something unthinkable, or someone wanted to control who gets saved.

**C. The infected from the nearby towns weren't what they thought.** The subjects from the expeditions carried **a different form of the strain**. Maybe those towns were an *earlier* trial, so NYC wasn't the first test site, just the biggest. The release didn't "get away"; it was a different animal than they planned for.

**D. Three layers of truth,** each feeling like the final answer:
1. **What survivors believe:** "a lab accident let it loose."
2. **What the founders' hidden records say:** "a controlled release got away from us." Players think they've cracked it.
3. **The real truth:** one of A, B or C.

*My pick: D, with A as the real truth, plus B as a rumor in the deepest clues.* A gives you a human mystery (who broke the containment, and why), and it explains why the founders still cover it up. They may be hiding that one of their own did it. B gives the most dedicated players something to hunt forever, without ever having to pay it off fully.

Which way do you want to take it?

### Developer (2026-10-27 19:48)

I would need an explanation for A or B, but B kind of sounds like a good one

### Claude (2026-10-27 19:48)

## B fleshed out: the release worked

The small release did its job. The researchers got their subjects, and **they found a way to mass-produce the cure.** That's the breakthrough the whole program existed for.

So why is the world still dying? Four versions, and they can be combined:

**B1. The price.** The scalable method needs **living infected hosts**: people kept alive in the window between infection and turning, who the cure is grown from. Mass-producing it means **farming people.** The researchers had been good people who crossed one line out of desperation, and this was a line too far. Some of them couldn't live with it, so the method was buried.
*The question it leaves players with: would they use it?*

**B2. The power.** Whoever holds the method decides who survives, inside the wall and out. The faint signals from outside (§19's radio) suddenly mean something: the rest of the world would trade *anything* for it. The founders hid it as **leverage**.

**B3. The lost courier.** The method was being carried out of the city to the survivors outside when the city fell, and it **never made it**. It's in a crashed helicopter on a roof, a boat at the bottom of the harbor, or a subway tunnel. It's lost, not hidden, and the founders have searched for years.

**B4. Split apart.** The researcher who realized the price **split the method into pieces** and hid them across the city. They couldn't bring themselves to destroy humanity's only hope, but they wouldn't let anyone use it easily. The pieces are out there.

## My pick: B1 + B4

- The method works, **but it costs living people.** A researcher who saw that split it into pieces and hid them across the city.
- **That researcher died or turned.** Maybe they're **one of the Patients**, a test subject in a way: a special zombie still guarding a piece.
- **The founders know the method exists and are still searching.** Their bank registering every survivor tracks people, and possibly future hosts. Their snipers keep everyone out of places where pieces might be. Their cover-up isn't just about the past; it's about what they still want.

**For gameplay**, this gives lore hunters something real to chase:
- Pieces are found through clues, notes and lore areas.
- **Assembling them could be a long-term server event** within a 6–12 month wipe cycle (§20), with clans racing or cooperating, and the founders reacting.
- Or it **never fully pays off**: players find enough to understand, but never enough to finish. We can decide that later, since it doesn't block anything now.

It also flips the earlier "a bit predictable" chain. Players find "the release got away" and think they've solved it. Then they learn **it didn't get away. It worked, and that's worse.**

All four versions are saved in the lore bible. Pick one, combine them, or tell me what to change.

### Developer (2026-10-27 19:51)

Ok i like that B1 +B4. But instead of it being split apart and spread out, it was split apart, and partially destroyed.

### Claude (2026-10-27 19:52)

Locked in, and "partially destroyed" is stronger than just "hidden". **The cure can't simply be found anymore.** At best someone gets back what survived, and the destroyed part is gone for good, or would have to be **rediscovered**, possibly the same terrible way. That keeps the stakes forever. It's recorded in the lore bible with the three layers players move through:

1. **"A lab accident let it loose"**: what survivors believe.
2. **"A controlled release got away from us"**: what the founders' hidden records say.
3. **"It didn't get away. It worked, and that's worse."**: the truth.

**Three follow-ups, with my suggestions:**

**1. What survived?**
*Suggestion:* the **process** survived, meaning the steps for growing the cure from living hosts, but the **key formula** was destroyed. The horrible part is still known; the part that makes it work is gone. Anyone who tries to rebuild it would have to experiment on people again. That's exactly the line the founders are tempted to cross.

**2. Where is it?**
*Suggestion:* **the founders have the surviving process** and keep it locked away in their most guarded safe zone. Notes from the researcher who destroyed the formula are the deep clues players find, explaining *why* they did it. Players learn the truth without ever holding the cure.

**3. Can it ever be rebuilt?**
*Suggestion:* **left open on purpose.** The radio and clues can hint that the founders are getting closer, for example missing survivors and quiet experiments. That gives the lore a live, threatening thread across a wipe cycle without promising a payoff.

This also answers most of the earlier **Q3 (what the founders want now)**: they're covering up the past *and* trying to finish the cure. Some of them may disagree, which gives you factions within the group later.

**Still open after these:** **Q2** (how the residents were studied; my pick was a "free vaccination drive"), **Q4** (the special zombies as test subjects), then the timeline, radio stations, factions and lore areas.

### Developer (2026-10-27 19:56)

1. yes the process survived, but multiple key formulas and some ingrediants are missing.
2. Idk, i want it to be so hidden, and maybe not named anything obvious in the game files for when people inevatably explore them, but so hidden to the point that it could take months to years irl for anyone to find from the first sale of the game
3. Yes, that should be left open on purpose


Q2, Idk, let me get options again

### Claude (2026-10-27 19:57)

Recorded in the lore bible:
- **What survived:** the process.
- **What's missing:** several key formulas and some ingredients.
- **Can it be rebuilt?** Left open on purpose.

The hiding requirement is in too, under its own heading, **"Hiding the truth"**. Months to years to find, with nothing obvious in the game files. The most reliable way to beat dataminers is to **not ship the deepest secrets at all.** They live on the server and are only sent to a player who unlocks them in the game. Add clue chains that need in-game actions (a radio frequency that's only live at certain times, coordinates hidden in a numbers station) and reveals that unlock over time, and even full datamining on launch day finds nothing. Where the surviving process actually is can be decided later.

## Q2: how were the residents studied without knowing?

This now fits the chain: the subjects came from outside until that got too risky. Before that, the residents were the **other half of the study**, unknowingly.

**A. "Free immunizations."** The city ran free booster clinics "to keep everyone safe". The shots were candidate cures and vaccines.
*Clues:* dose cards, clinic flyers, appointment reminders.

**B. Health screenings and blood drives.** Mandatory checkups at checkpoints collected blood and samples, which were raw material for the research. Some residents' blood may have been what the cure was grown from.
*Clues:* screening wristbands, blood bank logs, "donor" lists.

**C. Rations and aid.** Food and water handed out by the authorities carried trial compounds, with doses tracked by ration card.
*Clues:* coded ration cards, distribution schedules.

**D. The water supply.** Something added to the city's water. It fits naturally as a **false rumor**, a red herring that sends lore hunters chasing water towers.

**E. Quarantine wards.** Residents flagged for "possible exposure" were taken to quarantine hospitals, such as **North Brother Island**, the real historic quarantine island, and never came back. They became subjects.
*Clues:* removal notices, lists of names, an empty ward.

**F. The registry.** Everyone inside the wall had to register for an ID card "for safety". It tracked blood type, health and who could be useful. **The founders' bank registry today (§18) is the same idea continuing.** That's a clue that ties the past to the present.
*Clues:* old ID cards, registration posters, a registry terminal.

## My pick: F, then B, then E, with A as the public excuse and D as the false rumor

- **The registry** tracked everyone, and **screenings** (advertised as free immunizations) took samples and picked out useful people.
- The picked people were sent to **quarantine wards** and became subjects.
- **The water-tower rumor** is wrong, a trap for lore hunters.
- And when players notice that **the bank card works just like the old registry ID**, that's a goosebumps moment.

Pick, combine, or change.

### Developer (2026-10-27 20:07)

F, then B, Then E, not really feeling A

### Claude (2026-10-27 20:07)

Recorded in the lore bible. The residents were tracked by **the registry**, sampled through **health screenings and blood drives**, and the useful ones were taken to **quarantine wards** and never came back. "Free immunizations" is dropped. One small leftover: should the **water-supply rumor** stay as a red herring for lore hunters? It's marked as suggested for now.

## Q4: the special zombies (1–2 types, all original test subjects)

The twist says the special zombies are the original test subjects, so each one should *be* evidence: you find one, and it tells you something.

**1. The Patient.** One of the people taken to the quarantine wards, from the first round of tests.
- **Tougher:** it takes more head damage to drop. **The only zombie that truly runs.**
- Still wears a hospital gown and a **registry wristband**, a clue you can loot.

**2. The Host.** One of the people used for the **cure process**, kept in the window between infection and turning (the "price", B1). They turned anyway.
- **Slow and very hard to kill.** Medical restraints and tubing still hang off it.
- It's the most lore-heavy option: seeing one is how players start to understand what the cure costs.

**3. The Screamer.** A failed later test subject.
- **When it spots you, it shrieks and pulls in every zombie nearby.** It fits the sound-driven hordes (§8).
- Not tough, but you want it dead before it sees you.

**4. The Blind.** Test subjects whose eyes were destroyed in the experiments.
- **Hunts purely by sound, with hearing far sharper than normal zombies.** Silence is your only defense: sneakers, crouching, packing your bag quietly (§11, §8).
- Ties directly into the stealth systems already designed.

**My pick: the Patient and the Host.**
- The Patient is the **combat** threat, the one that runs.
- The Host is the **story** threat, the one that makes you understand.
- Both stay **only at lore areas**: the quarantine wards, the labs, wherever the process was run.
- The Screamer or the Blind could become regular zombie behaviors later instead of specials, since they don't need lore to work.

Pick 1–2 (the GDD caps it at two), or change any of them.

### Developer (2026-10-27 20:11)

yes as a rumor only. Q4. 1 Yes, 2 yes, but they have to visually look pretty different, maybe mutated. Maybe 1 can be heard saying a sentance or word in english before going back to incoherrant mumbling.

### Claude (2026-10-27 20:12)

Recorded. The water story is a **rumor only** (and false), and both special zombies are locked in:

- **The Patient:** tougher, the only zombie that truly runs, wears a hospital gown and a lootable wristband. It **sometimes says a word or a sentence in English**, then slips back into mumbling. That's a great horror moment, and the lines can carry clues.
- **The Host:** slow and very hard to kill, with restraints and tubing hanging off it. Seeing one is how players start to grasp what the cure costs.
- **Both look clearly different from regular zombies,** for example visibly mutated.

The full backstory is in the lore bible. The GDD (§8) only has their gameplay, so the team doc doesn't spoil the twist.

One idea for the Patient's lines: if each Patient says something different, like a name, a ward number or "they said it would help", players can collect them like audio logs. That's one more clue channel. The audio files would get neutral names, per the "hiding the truth" rule.

**What's left in the lore:** the timeline (now easy to build from everything above), radio stations, factions, the infection itself, and the lore areas.

### Developer (2026-10-27 20:24)

Yes, let's build the timeline next. Give me your proposal.

### Claude (2026-10-27 20:25)

## Timeline: my proposal

Built from everything decided. **Game start = year 8.** The city fell 6 years before that, which is long enough for the overgrowth and the animals to come back.

| When | Phase | What happened | Surface story (what survivors believe) |
|---|---|---|---|
| **Year 0** | **The outbreak** | It starts somewhere outside and spreads across the world within months | Same |
| **Year 0, months 2–4** | **The wall** | NYC is sealed with a wall along the major highways and checkpoints at every bridge and tunnel. Researchers and labs move in. **The registry begins.** | "The wall keeps us safe. Scientists came to find a cure." |
| **Years 0–1** | **The lockdown** | The city holds well. Screenings and blood drives. Quarantine wards on North Brother Island. **Expeditions bring infected subjects in from nearby towns.** The first cure, the antiviral, is made, but it's **extremely hard to produce**, so there are only tiny batches. | "It's tough, but we're holding." |
| **Late year 1** | **The silence** | **The world goes dark.** Contact, funding and orders from outside stop. | "The radio stopped. Nobody knows why." |
| **Year 1–2** | **The decision** | The nearby towns are used up, and expeditions are too risky. The program plans a **controlled release** in a district picked for practical reasons. | Nothing. Nobody outside the program knows. |
| **Early year 2** | **The release** | It works. They get their subjects and find the **scalable cure method**, which needs **living hosts**. *(See question below.)* | "Something got out of a lab." |
| **Year 2** | **The fall** | The city falls over a few weeks. **A researcher splits the method and destroys part of it.** The program collapses. The soldiers on the wall were ordered to let **no one out**. | "The military abandoned us." |
| **Years 2–3** | **The flood** | A hurricane floods the low areas: Red Hook, Lower Manhattan, the Rockaways. | Same |
| **Years 3–5** | **The hiding** | Survivors hide in sealed buildings, basements and subway shelters. **The founders regroup** and open the first safe zone, print the currency and start the bank's registry. | "Some survivors got organized." |
| **Years 5–8** | **The network** | The safe zones grow to 6–7. **Their radio starts calling survivors in.** | "There's a place that's safe." |
| **Year 8** | **The game starts** | Players are the survivors coming out of hiding, answering the call. | |

## One question that matters

**How did the city fall, if the release worked?** My suggestion: once the program found that the cure needs **living hosts**, it **stopped trying to contain the release** and let it spread, because more infected meant more hosts. The city didn't fall by accident. It was allowed to fall. That's the darkest version of "it worked, and that's worse", and it's what the researcher couldn't live with, which is why they destroyed the formulas.

**Two details I'd like to keep:**
- **The wall kept people in.** The soldiers on the wall were ordered to stop anyone leaving. That's the moment twist 1 (the wall was never meant to keep it out) turns physical. The soldiers were later lost or deserted, which is why the checkpoints are open now.
- **Why players come out now, in year 8:** the safe zones' radio started calling survivors in. It sounds like hope. It's also how the founders find and register everyone (§18), which quietly ties the game's start into the twist.

**To answer:** yes or changes. The main choices are 8 years in total, "they let it spread", the wall keeping people in, and the radio call as the reason players come out now.

### Developer (2026-10-27 20:44)

For how did the city fall, back to early year 2, they need a large group of infected, but as stated nearby towns dont really have many subjects left. They came up with a precise plan, to let a a small town along the border somewhere, maybe in NJ or somewhere else like the bronx, where the stage some kind of wall breach that lets in a small horde (that was gathered by them in advance from test subjects and other people they took for experiments ) . It is intentionally a very undefended area,  and to avoid raising any suspisions beforehand, they didnt increase security in that area too much, only a few more patrols in the area. (we will need to dive deeper on this research group/atp small government.) It almos goes perfectly according to plan, infecting many of a small neighborhood, with extra patrols sent out after the fact to assist in keeping it from spreading out. If they need live or dead infected to mass produce the cure changes the next part so what do we have on that?

### Claude (2026-10-27 20:45)

Your staged breach is much stronger than my "they let it spread". It's a deliberate, cold, *competent* plan, which fits a group acting like a small government. It's recorded in the lore bible, and draft timeline v1 is saved there too as "under review".

**To your question: the cure needs living infected.** We decided that with B1, "the price": the scalable method grows the cure from people **in the window between being infected and turning**. Dead or turned infected are useless for it. So the newly infected neighborhood **was the harvest**, and the "extra patrols sent to contain it" were also **rounding people up**, probably "for treatment".

That raises one lore detail, and I have an idea for it. **How long is the window?** If people turn fast, the process can't run at scale. The idea: **the existing antiviral, the one that's so hard to make, is what keeps hosts suspended in the window.** The small cure is used to keep people alive just long enough to grow the big one. That makes the rare antiviral in hospitals even darker: it's what was left over from keeping hosts alive.

## What went wrong after "almost perfectly"? Options

**A. Someone slipped the cordon.** A family, a delivery driver, a kid who knew a hole in the fence. A handful of infected got out before the patrols closed in, and by the time it surfaced elsewhere, it was in three boroughs.

**B. A patrol was infected.** One of the soldiers sent to contain it was bitten and hid it. The military itself became the carrier, spreading it through checkpoints and barracks, the places meant to stop it.

**C. The hosts broke out.** The rounded-up infected were held in a facility **inside** the city. Something failed there (power, staff, the window collapsing) and the hosts turned all at once, in the heart of the city. Those escaped hosts become **the Hosts** (special zombies).

**D. The person who tried to stop it caused it.** The researcher who destroyed the formulas **also opened the host facility**, meaning to free the people or end the program. Instead they released the infected into the city. Good intentions, again, causing the catastrophe. It mirrors the whole story.

**E. They got greedy.** One neighborhood wasn't enough hosts, so they staged a second breach. And a third. The plan that worked once stopped working.

**My pick: C, possibly with D underneath it.** C explains the Hosts directly. D, as the deepest truth, means the founders' records blame "a facility failure" while the real story is that one of their own opened the doors. That's another reason for the cover-up, and the same irony that runs through the whole lore: good people doing terrible things, and terrible outcomes from good people.

**One note on the neighborhood:** since the map is real NYC, I'd give the breached neighborhood a **fictional name**, or keep it unnamed, rather than make a real community the one that was sacrificed. The streets can still be real.

### Developer (2026-10-27 21:10)

Nope, real neighborhood names, just all fictional events. Unless they are copyrighted or something.

No, they can have something else with a mysterious name like how the boys uses compound V that holds them in the infected state, that is related but not the same as the cure. Maybe it can be found aswell as a very rare or top tier item that delays the infection for survivors but doesnt cure them. 

AS for how it went wrong, they had enough to begin mass producing for the cure but not to sustain it. But im thinking a few infected get drawn immedietly after the breach to a noise, that brings them along a route, maybe through some buildings that they managed to slip by. From there, they spread out, a few dying before getting any one, but some getting some lucky victims, and those lucky victims spreading out to more populated but not highly defended areas. From there, the Force (What ill call them for now, the patrols are not actually military, but groups from the research org) patrols are spread to thinly to effectively manage the situation, and it gets to the point where there is no more daily life. Speaking of daily life, I wanna talk what that looked like through the first few years).

### Claude (2026-10-27 21:11)

All recorded in the lore bible and the decision log. Your version of the fall is better than any of my options. It's small and realistic: a noise, a route through a few buildings, a lucky victim. **One unlucky chain of events, not a dramatic failure.** It also fits the "noise draws zombies" mechanic, which is a nice in-world echo.

**Recorded:**
- **Real neighborhood names, fictional events.** Neighborhood and street names are public place names, so that's fine. **One catch, now written into GDD §5 as a naming rule:** some *landmarks* are brands. **Citi Field and Barclays Center** are sponsor names, **Yankee Stadium** belongs to the team, and some famous buildings have trademarked names and designs. Those get fictional versions. I've flagged the four combat landmarks in the points-of-interest list.
- **The compound** (mysterious name to come) holds hosts in the infected state. It's related to the cure, but not the cure. It's in GDD §8 as a very rare item that **delays infection without curing it**, so it buys you time to find the antiviral.
- **"The Force"** is the research organization's own patrols, not the military.

**One open question this raises:** the GDD has **military and National Guard sites** as loot locations, and the wall was "military" in earlier talk. Was the real military there early on, building the wall before the organization took over? Or did the Force do everything? We can settle that with factions.

## Daily life in the walled city, years 0–2: my proposal

**Year 0: the sealing**
- Panic, then adjustment. The gates close, and refugees at the wall get turned away. That's an early hint the wall works both ways.
- **The registry** begins: everyone gets an **ID card**, needed for food, work and getting through checkpoints.
- **Curfew** and **checkpoints between boroughs**.

**Year 1: the new normal**
- **Ration cards and ration credits.** The dollar fades, and the authority prints **credit notes**. *Lore tie:* **the founders' currency today (Sanctos Notes) descends from these.**
- **Assigned work:** building the wall, utilities, and **urban farming**. That's why **rooftop gardens and community gardens** are already everywhere in the game (§22).
- **Rolling blackouts** and solar panels going up. That explains the solar on rooftops and the bike-share docks (§16).
- **Official radio and posters:** "The wall keeps us safe", "Report symptoms". Players will find these everywhere as clues.
- **Black markets:** bodegas as fronts and smuggling through the wall. *Lore tie:* the **customs warehouse full of seized smuggled guns** at the ports (§12) is from this era.
- **Schools stay open,** with lockdown drills. Stadiums become **food distribution centers**.
- **Mandatory health screenings** (decided). People start **disappearing to the quarantine wards**, and whispers spread.
- **Pirate radio** appears, with rumors and resistance. That's the origin of the unreliable stations players hear today.

**Year 2: the cracks**
- **The radio from outside goes silent.** Rations shrink, and tension rises.
- More "exposure removals". Neighbors start informing on neighbors.
- Then **the breach** and **the fall**.

**Clues this gives players:** ID cards, ration cards, old credit notes, lockdown posters, school notices, black-market ledgers, official radio recordings, and removal notices.

**To answer:** yes or changes, and anything you want to add. You clearly have ideas about daily life.

### Developer (2026-10-27 21:21)

The military was there to setup the fall, and the researh agency should come from some sub branch of the real government, kind of like TLOU's Fedra. The Force is like the face for the government, but after the outside falls, only small settlements remain throughout the USA, so they're kinda independetlly owned. So yes, the military put up the wall, and the patrols and stuff are technically a sub branch of the military, but more like were not are.  As for those first two years thats good for the most part. lets hold the propagand posters and stuff until  year 2 or at least late 1. Not that it changes gameplay but just lore

### Claude (2026-10-27 21:22)

Recorded in the lore bible and the decision log. I read "set up the fall" as **"set up the wall"**, since your next line says the military put the wall up. Tell me if you meant something else.

**Factions so far:**
- **The military** built the wall.
- **The research agency** is a sub-branch of the federal government, like FEDRA in The Last of Us.
- **The Force** is its face. It's technically a military sub-branch, but more "were" than "are".
- **After the outside fell,** with only small settlements left across the USA, both became **independent, answering to no one.**

That also explains why military and National Guard sites exist as loot spots. They're what's left of the military's role in building and running the wall.

**Daily life in years 0–2** is in as proposed. **Propaganda only starts in late year 1 or year 2**, so players who notice when posters appeared get one more subtle clue about when things turned.

**Lore still to build:**
1. **Names:** the agency, the Force's real name, the infection-delaying compound, and the currency (Sanctos Notes is leading).
2. **The safe-zone group:** how the founders went from program insiders to running the safe zones.
3. **Finishing the timeline:** 8 years in total, whether the wall's soldiers kept people *in*, and the radio call as the reason players come out now.
4. **The infection itself:** what it is, why animals are immune, why fresh zombies are faster.
5. **Radio stations**, then **lore areas** (which feeds the points-of-interest pass).

I'd do **names** next, since four things are waiting on them, and a quick round of options for each would unblock a lot.

### Developer (2026-10-27 21:24)

For factions, the Force and Research agency are one thing, like the research agency is part of the force. The force is the over archer "government" of the city, so they control the military. Make sure you clarify that EVERYWHERE for lore sake. Then we do those next 5

### Claude (2026-10-27 21:25)

Done. The Force is now the same everywhere in the docs. **It's one organization: the city's government.** The research agency is part of it, and it controls the military, which built the wall. The lore bible has a dedicated **"The Force"** section that says this outright, along with a line saying that "the program", "the researchers" and "the patrols" always mean parts of the Force. I fixed the release, the fall, the factions and the twist sections, and updated GDD §23. In the decision log, older entries that described them as separate are marked as clarified, with a new entry explaining the change.

Now the first of the next five: **names.**

## 1. The Force's official name

You called them "the Force" as a working name. What if that's what **survivors call them**, and it comes from the official acronym, the way FEDRA does?

- **F.O.R.C.E.: Federal Office for Response, Containment and Enforcement.** Your working name becomes the real one, and it sounds exactly like a government agency.
- **Metropolitan Containment Authority (MCA),** nicknamed "the Authority".
- **Federal Continuity Command (FCC),** nicknamed "Command".
- **Office of Civil Preservation (OCP),** nicknamed "the Office".

*My pick: F.O.R.C.E.* It keeps the name you already use, and players who find an old letterhead with the full name get a small "oh" moment.

## 2. The research program's codename

The research agency inside the Force runs a codenamed program.

- **Project SANCTUS** (Latin for "holy"). **The founders' currency today is "Sanctos Notes".** The safe-zone group named its money after the program it came from, a clue hiding in plain sight. Only players who find the program's name ever connect the two.
- **Project Meridian**
- **Project Lantern**
- **Project Tidewater**

*My pick: SANCTUS.* It locks in Sanctos Notes as the currency and turns it into evidence for twist layer 3, that the founders came out of the program.

## 3. The compound that holds the infected state (delays infection)

- **Hourglass** (lab code HG-7). It buys time, which is exactly what it does for players.
- **Halcyon:** sounds calm, hides what it's for.
- **Limbo:** holds you between alive and turned.
- **Tether:** holds you back from turning.

*My pick: Hourglass.* Players understand at a glance what it does, and it still sounds mysterious. "Got any Hourglass?" sounds right.

## 4. The currency

**Sanctos Notes**, if you take SANCTUS above. Otherwise, Boros and Quarants are still in the running.

## Optional: does the antiviral get a name?

Right now it's just "the antiviral". A name would make it feel like a real thing, for example **"Remedy"**, or a lab code. It's fine to leave it plain too.

**To answer:** pick per item, or ask for more options.

### Developer (2026-10-27 21:28)

1. I Like, Force as a acronym. I like the FORC, not a big fan of enforcement, different e?

### Claude (2026-10-27 21:28)

F.O.R.C.E. as an acronym is now recorded. Options for the E:

- **Federal Office for Response and Containment of Epidemics.** The most fitting: it names exactly what they were created for, and it sounds like a real agency.
- **Federal Office for Response and Containment of Emergencies.** More general, FEMA-like. It sounds harmless, which suits an organization that hid what it was doing.
- **Federal Office for Response, Containment and Evacuation.** Darkly ironic: they never evacuated anyone, and players who know the truth will notice.
- **Federal Office for Response, Containment and Eradication.** Cold and clinical, hinting at what they were willing to do.

My pick is **Epidemics**. It reads like a real government office, and "Response and Containment of Epidemics" makes the acronym flow naturally. **Evacuation** is my second choice, for the irony.

### Developer (2026-10-27 21:36)

I also thought of Eradication, and it kind of makes sense but i thought that might be too much

### Claude (2026-10-27 21:36)

I don't think Eradication is too much, for one reason: **in public health it's a positive word.** Smallpox was "eradicated". To residents, "Containment and Eradication" would read as "we'll wipe out the disease". Only players who learn the truth would read it as "wipe out *people*". That kind of double meaning is what good lore is made of.

The real risk is that it **gives away too much at first glance.** Some players will see "Eradication" on a poster and assume they're the villains right away, before the slow reveal does its work.

Three ways to go:

1. **Eradication as the official name.** Bold, the double meaning is there from day one, and players argue about whether it's sinister or just public-health speak.
2. **Epidemics as the official name.** Harmless on the surface. Nothing gives the twist away early.
3. **The compromise:** the official name uses **Epidemics**, and **"Eradication" turns up in deep clues instead**, for example an internal document titled "Eradication Protocol" inside the research program. Players who find it get the chill at the right moment, deep into the mystery rather than on the first poster.

My pick is **3**. You keep the word you like, and it hits harder when it's found than when it's printed on every checkpoint. If you prefer option 1, the public-health reading makes it defensible.

### Developer (2026-10-27 21:57)

3 is good

### Claude (2026-10-27 21:57)

Locked in. **F.O.R.C.E. stands for the Federal Office for Response and Containment of Epidemics.** "Eradication" is reserved for a deep clue, an internal **"Eradication Protocol"** document that players find far into the mystery. It's recorded in the lore bible, GDD §23 and the decision log.

**Names still open, with my picks:**

1. **The research program's codename:** **Project SANCTUS.** That makes the founders' currency, **Sanctos Notes**, a clue hiding in plain sight. Other options: Meridian, Lantern, Tidewater.
2. **The compound that delays infection:** **Hourglass** (lab code HG-7). Other options: Halcyon, Limbo, Tether.
3. **The currency:** Sanctos Notes if you go with SANCTUS. Otherwise Boros or Quarants.
4. **The antiviral:** leave it plain, or give it a name like "Remedy".

### Developer (2026-10-27 21:58)

maybe of instead of For?

### Claude (2026-10-27 21:58)

Good call. **"Office of"** sounds more like a real US agency, like the Office of Management and Budget. It's now **the Federal Office of Response and Containment of Epidemics** everywhere: the lore bible, GDD §23 and the decision log. Prepositions don't count in acronyms, so it's still **F.O.R.C.E.**

Still to name, with my picks:
1. **Program codename:** Project SANCTUS, which makes "Sanctos Notes" a hidden clue.
2. **The infection-delaying compound:** Hourglass (HG-7).
3. **Currency:** Sanctos Notes, if you go with SANCTUS.
4. **The antiviral:** leave it plain, or give it a name.

### Developer (2026-10-27 22:00)

1. Project Sanctus is nice, as long as it hasnt been used in any movies or games for anything.
2. Hourglass good
3. Currency is good
4. Antiviral should have a name, shoot ideas

### Claude (2026-10-27 22:00)

Name check done. Recording the decisions now.

### Claude (2026-10-27 22:01)

All three are locked in across the lore bible, the GDD and the decision log:
- **Project SANCTUS** (the program codename)
- **Hourglass, HG-7** (the compound that delays infection)
- **Sanctos Notes** (the currency, now final)

**Name check on SANCTUS:** I searched and found **nothing titled exactly "Project Sanctus"** in games, films or books. "Sanctus" on its own is used by a few unrelated things: an adult horror game by Madmind Studio, Simon Toyne's 2011 thriller novel, and a 2026 horror film called *Sanctus House*. None involves a cure or a virus, and an in-world codename is unlikely to clash. Before the name goes on marketing or the store page, a proper trademark search is still worth doing. That's noted in the docs.

## Antiviral names

A real drug has a **generic name** on the label and a **short name** people actually use. I'd do the same:

| Short name | Generic name (on the vial) | Feel |
|---|---|---|
| **Absolve** | absolvirine | "Absolution": a theme of guilt, fitting researchers who crossed lines. Subtly religious, like SANCTUS, so the program's naming style becomes a quiet pattern clue |
| **Remedy** | remedivir | Plain and hopeful. What a government would call it |
| **Kairo** | kairovir | From the Greek *kairos*, "the right moment". Clinical and modern |
| **Mercy** | mercivane | Emotional. What survivors would call it on the street |
| **Revena** | revenavir | From "revive". Pharma-brand feel |

One I'd **avoid**: anything close to "Sanctus" (like "Sanctivir"). It would openly link the cure to the currency and give away that the safe zones came from the program far too easily.

*My pick: **Absolve**, with "absolvirine" on the label.* It sounds like a real drug, it fits the guilt running through the whole lore, and attentive players may notice the religious naming pattern it shares with SANCTUS.

Sources:
- [Madmind Studio "Sanctus" trailer (Downright Creepy)](https://downrightcreepy.com/madmind-studio-sanctus-trailer/)
- [Sanctus Steam page announcement (Game*Spark)](https://www.gamespark.jp/article/2022/12/13/125310.html)
- [Simon Toyne, *Sanctus* (Publishers Weekly)](https://publishersweekly.com/9780062038302)
- [*Sanctus House* (2026)](https://bingebase.com/movies/sanctus-house-2026)
- [Project: Sanctity (itch.io)](https://ghosthatgames.itch.io/project-sanctity)

### Developer (2026-10-27 22:02)

Maybe something else latin to fit that theme

### Claude (2026-10-27 22:03)

Latin options for the antiviral. Short name first, with the generic name for the label:

| Short name | Generic | Latin meaning | Why it fits |
|---|---|---|---|
| **Remissa** | remissivir | *remissio* = forgiveness | **Double meaning:** "remission" is what doctors call a disease going away, and in Latin it means forgiveness. Medical on the surface, guilt underneath |
| **Salvus** | salvirine | "saved, unharmed" | Sounds like "salvation". Hopeful, official-sounding |
| **Clementia** | clemvir | mercy | Soft and humane. What a government would want on the vial |
| **Spera** | speravir | from *spes*, hope | Simple and hopeful |
| **Lux** | luxavir | light | Short and punchy. "Got any Lux?" |
| **Agnus** | agnuvir | from *Agnus Dei*, "Lamb of God, who takes away the sins of the world" | "Takes away" the infection. See the bonus idea below |

I'd **avoid anything starting with "Pax-"**, since Paxlovid is a real antiviral.

**Bonus deep-lore idea:** *Sanctus* and *Agnus Dei* are both **parts of the Latin Mass**: Kyrie, Gloria, Credo, Sanctus, Benedictus, Agnus Dei. If the program named all its projects after parts of the Mass, deep clues could mention **"Phase KYRIE"** or **"Phase GLORIA"** in documents. Lore hunters who spot the pattern can work out the program's structure, and it fits the "hidden in plain sight" rule.

*My pick: **Remissa**.* Everyone reads it as "remission", so it's instantly a cure. Only those who dig learn it means *forgiveness*. That's the same trick as "Eradication", the surface reading versus the truth. If you'd rather lean into the Mass pattern, **Agnus** is the one that ties into it.

### Developer (2026-10-27 22:04)

I like the Remisso, but not so much remissivir

### Claude (2026-10-27 22:04)

**Remisso** is recorded as the antiviral's name in the lore bible, GDD §8 and the decision log. You wrote "Remisso" rather than my "Remissa", and I kept your spelling. I think it reads better, more like a product name.

For the generic name on the vial, which is optional, other endings:

| Generic | Ending means | Note |
|---|---|---|
| **remizumab** | *-mab* = an antibody drug | **A hidden lore clue:** real antibody drugs are made from living cells, and Remisso is grown from living hosts. Anyone who knows drug naming gets a quiet chill |
| **remissane** | neutral | Soft, clean, sounds like a modern drug |
| **remitrel** | neutral | Short, clinical |
| **remissine** | *-ine*, old-style drug name | Classic pharmacy feel |

*My pick: **remizumab**.* It sounds completely real, and for players who know how drugs are named, the "-mab" hints at where it comes from. It's one more clue hiding in plain sight.

You can also **skip the generic name** and print just "Remisso" on the vial. Game players won't miss it.

I haven't checked whether "remizumab" is a real drug name. The "remi-" prefix is common in medicine (Remicade, for example), so search it before it goes into the game.

### Developer (2026-10-27 22:05)

Remirel sounds good

### Developer (2026-10-27 22:06)

remitrel

### Claude (2026-10-27 22:06)

Good thing you switched. I checked both: **"Remirel" is already a real drug**, a multiple sclerosis injection made by Zentiva, so it's out. **"Remitrel" turned up no existing drug,** so it's clear.

**Recorded:** the antiviral is **Remisso**, with **remitrel** on the label. It's in the lore bible and the decision log.

**All the names are now set:**
- **F.O.R.C.E.:** the Federal Office of Response and Containment of Epidemics
- **Project SANCTUS:** the research program
- **Hourglass (HG-7):** delays infection
- **Remisso (remitrel):** the cure
- **Sanctos Notes:** the currency

**Next of the five lore topics:** the safe-zone group (how the founders went from SANCTUS insiders to running the safe zones). After that: finishing the timeline, the infection itself, then radio stations.

Sources:
- [Remirel (glatiramer acetate), Czech product information](https://neurologiepropraxi.cz/view/e2024/eNEU_06_24/files/assets/common/downloads/page0075.pdf)
- [Remurel listing (oladoctor)](https://oladoctor.com/en/medicines/poland/remurel-roztwor-20-mg-ml)
- [Reminyl XL (medicines.ie)](https://www.medicines.ie/medicines/reminyl-xl-8mg-16mg-and-24-mg-prolonged-release-capsules-33553)
- [Remirta ORO (leki.pl)](https://leki.pl/?p=154755)

### Developer (2026-10-27 22:08)

Give me a prompt to give to you to ensure the Lore is saved in extreme detail, nothing should be lost in translation between chats at all, especially lore

### Claude (2026-10-27 22:09)

I did better than a prompt: the rules are now **built into CLAUDE.md**, which every new chat in this project loads automatically. You don't have to remember to paste anything. Those rules make any future session:

- **Read the whole lore bible** (and the recent decision log) before talking lore, not a summary of it.
- **Record every lore detail the same turn, in full**, keeping **your own wording** for key ideas, plus the date and who proposed it.
- **Record what was rejected and why.**
- **Save my unanswered proposals** in a new **"Pending proposals"** section of the lore bible, so options survive even if a chat ends mid-question.
- Keep **the truth** and **what survivors believe** clearly separated, and **keep the twist out of the GDD**.
- When something changes, **update every place it appears**, as we just did with the Force.
- **Check names against real games, films, books and drugs** before locking them.
- End each lore turn with one line saying what was recorded and where.

Still, here's a prompt for the start of any new lore chat, as a backup:

```text
We're continuing NYZ lore. Before anything else: read CLAUDE.md, read docs/lore/LORE.md in full (including "Pending proposals"), and read the latest lore entries in docs/DECISIONS.md. Follow the lore rules in CLAUDE.md exactly. Record everything I say about lore in the same turn, in full detail, keeping my own wording for key ideas, and record anything you propose that I haven't answered under "Pending proposals". End each turn by telling me what you recorded and where. Then tell me where we left off.
```

**The strongest safety net is also saving the raw conversation itself.** The docs hold every decision, but a full transcript in the project captures the reasoning and back-and-forth word for word. That's the question in the box below.

### Developer (2026-10-27 22:09)

Yes, export this chat's full transcript into the project as a backup, under docs/transcripts.

### Claude (2026-10-27 22:10)

I've backed this chat up in [docs/transcripts](docs/transcripts) as two files:

- **[2026-10-27-design-session.zip](docs/transcripts/2026-10-27-design-session.zip) (20 MB):** the full export. It has everything, including tool calls, the map screenshots and session data. Nothing was uploaded anywhere; it's a local copy.
- **[2026-10-27-design-session.md](docs/transcripts/2026-10-27-design-session.md) (about 230 KB):** a readable version with just the conversation, your 111 messages and my replies in order. I spot-checked it from your first message through to the Remirel/remitrel check.

I also added a small script, [tools/transcript_to_md.py](tools/transcript_to_md.py), that turns any future export into the readable version. CLAUDE.md now tells future sessions to:
- **search the transcripts** when a question is about *why* something was decided or exactly what you said;
- **offer a fresh export** at the end of any session with substantial design or lore work.

**Two things to know:**
- **The backup is a snapshot up to now.** Anything we discuss after this needs another export. I'll offer one at the end of future big sessions.
- **The 20 MB zip matters for source control later.** When we set up Git, zip files should go through Git LFS, the large-file add-on. I'll handle that when we get to the source-control reminder.

### Developer (2026-10-27 22:11)

Does the lore bible include every detail of the lore?

### Claude (2026-10-27 22:11)

I checked the lore bible against the conversation. It has every decision, but it was missing some things. Here's what I found, and I'm adding it now.

### Claude (2026-10-27 22:13)

Now it does. I went through the conversation against the lore bible. **Every lore decision was already in it**, but some things were missing, and I've added them:

**1. Suggestions you never answered.** They existed only in chat, so they're now under **"Pending proposals"** in the lore bible:
- "The Sanctuary" as the safe-zone group's name and role.
- A split inside the founders: some want to atone, others want the cover-up and the cure.
- The Patient's spoken lines as collectible audio clues.
- The Latin Mass naming pattern ("Phase KYRIE", "Phase GLORIA"), which SANCTUS already fits.
- Flashlights having no special pull on zombies.
- Three timeline points: 8 years in total, the wall's soldiers ordered to let no one out, and the radio call as the reason players come out now.

**2. Your own words.** The bible paraphrases you. A new file, [docs/lore/developer-words.md](docs/lore/developer-words.md), now holds **all 27 of your lore messages word for word**, typos kept. Each one has a note on what it was answering. I also added three earlier messages that touch the lore: the overgrown city and the animals returning, the modern setting, and "who's broadcasting weather in an apocalypse?" Where the bible and your words differ, your words are the source.

**3. Small gaps:**
- A note that you first wrote "the military was there to setup the fall". I read it as "set up the wall", since your next sentence said the military put up the wall.
- Why Hourglass was chosen, and the alternatives that weren't.

**From now on:** CLAUDE.md tells every session to add your lore messages to that file word for word, and to put any unanswered suggestion under "Pending proposals" the same turn. Nothing exists only in chat anymore.

The word-for-word file only covers this chat up to now. Later chats add to it as they go.

### Developer (2026-10-27 22:14)

I meant wall, you were correct on that. And i thought i did say Hourglass was good?

### Claude (2026-10-27 22:15)

**Wall:** thanks, the lore bible now says you confirmed it, instead of "read as wall, not corrected".

**Hourglass:** you did say "Hourglass good", and it was already recorded as **decided**, in the lore bible, GDD §8 and the decision log. My wording was confusing. The "gap" I filled wasn't the decision itself. It was the reason it won (it buys time, which is exactly what it does) and the names that weren't picked (Halcyon, Limbo, Tether), since the new rules say to keep both.

Your message is also saved word for word in developer-words.md.

### Developer (2026-10-27 22:16)

Ok, so can i start a new chat for context usage purposaes? Will every single important decision and detail be translated to the new chat

### Claude (2026-10-27 22:16)

Yes, start a new chat. Everything important is in files, not in this chat's memory.

**What a new chat picks up automatically:**
- **CLAUDE.md** loads by itself in any chat opened in this project folder. It tells the new chat to read the GDD first, follow the lore rules, and remind you about source control when the design is done.
- **My memory note** (that your "yes" means "yes, unless I think otherwise") also loads by itself.

**What the new chat reads from the files:**

| File | What's in it |
|---|---|
| `docs/GDD.md` | All 23 sections of the design, with open questions and "Maybe later" |
| `docs/DECISIONS.md` | Every decision with date, reason and what was rejected |
| `docs/lore/LORE.md` | The full lore, including the twist and pending proposals |
| `docs/lore/developer-words.md` | All your lore messages, word for word |
| `docs/weapons/gun-roster.md`, `docs/map/` | The gun list, the border and its change notes |
| `docs/transcripts/` | This whole conversation, for "why did we decide X?" |

**What doesn't carry over:**
- The feel of the conversation, meaning my memory of *how* we got somewhere. The decision log and transcripts cover the reasoning, so a new chat can look it up instead of remembering it.
- **The last few messages** (the lore-bible check, "wall", Hourglass) came after the transcript export. Their content is already in the docs, so nothing is lost, but the transcript doesn't include them yet. Re-exporting takes seconds if you want it complete.

**Paste this to start the new chat:**

```text
Continuing NYZ design from a previous chat. Follow CLAUDE.md. Read docs/GDD.md, the latest entries in docs/DECISIONS.md, docs/lore/LORE.md (including "Pending proposals") and docs/lore/developer-words.md. Then tell me where we left off. The next topic was the safe-zone group in the lore.
```

**One thing worth knowing:** the GDD is now about 1,300 lines, and the new chat reads all of it at the start, which uses a fair chunk of context. When it gets bigger, splitting it into one file per system would let each chat read only what it needs. That's not urgent yet, but worth doing before development starts.

### Developer (2026-10-27 22:17)

Re export
