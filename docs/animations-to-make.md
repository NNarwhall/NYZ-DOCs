# Animations to make

The one list of every animation NYZ needs, so that when animation work starts it can be worked through top to bottom and the finished clips handed to Claude to swap in. Started 2026-11-13 from the whole GDD as it stood that day.

**This list grows.** Whenever a system's design adds something a character, zombie, animal or NPC does, its animations are added here in the same turn (a rule in `CLAUDE.md`). Guns, food and other item-by-item detail get filled in when those lists are final.

What we have today (Epic's free sample, about 800 clips) is in [animation-list.md](animation-list.md).

## The plan (the developer, 2026-11-13)

> "I am either gonna have a friend come in later, and hand do the animations (he has no experience, so less likely), or im gonna use Higgsfield + Claude to make animations. But later down the line, so for now, what i need you to do it write down every possible animation that needs to be made for our game, adding to it later for guns food, etc other stuff that needs animations. Then, when its time to revist the animations, i have one list, that i just roll through making them with higgsfield, and can then just give all to you to replace ours"

- **Who makes them, later:** a friend by hand (less likely), or Higgsfield with Claude.
- **Until then:** Epic's sample clips stay in, with stand-ins made in code where the sample has nothing.
- **Claude's advice for when it starts:** before working through the whole list, prove the route on three clips of different kinds: one loop (jog forwards), one that touches the world (a vault, where the hands must meet a ledge), and one item use (bandaging an arm). If those three come out usable on our skeleton, the rest is production.

## How to read a row

| Column | Meaning |
|---|---|
| **ID** | The clip's permanent name for hand-over. Variants add a suffix: `MOV-004-FL` is the walk loop, forward-left. |
| **What the body does** | The brief, in plain words. Good enough to describe to a person or a tool. |
| **Loop** | **L** repeats seamlessly. **1** plays once. **1→L→1** is a start, a repeating middle and an end (three clips). |
| **Moves** | **In place**: the feet stay on the spot, the game moves the body. **Travels**: the clip itself carries the body (over a wall, up a ladder), and the distance or height it covers must be the one given. |
| **Variants** | Every version needed. *8 dir* = forwards, back, left, right and the four diagonals, the body always facing forwards. *L/R* = a left and a right version. |
| **When** | **Now**: already in the game on a sample clip, to be replaced. **M2**: needed for milestone 2, the core survival loop. **Sys**: when its system is built. **Opt**: nice to have, or not in the design yet. |
| **Have** | **E** a sample clip is in use. **e** the sample has one we don't use. **J** a stand-in made by joining clips or in code. **–** nothing. |

## Rules every clip follows

- **Start and end in a base pose** of the stance it belongs to (below), so any clip can follow any other. A loop's last frame matches its first.
- **One skeleton.** Today that is the sample's mannequin; the game will have two base bodies (GDD §21) that share clips.
- **The same clips serve first and third person.** The first-person camera sits on the full body (GDD §25 point 8), so there is no separate set of floating arms. Anything the hands do must look right from the character's own eyes.
- **Handedness (GDD §7):** clips are right-handed. Left-hand versions exist only where the design needs them: one-handed pistols, one-handed melee and throwing.
- **Speeds are fixed by the design:** walk 1.6 m/s, jog 3.5, sprint 6, crouch 1 and 2.2, prone 0.6, swim 1.2, limp up to 2, both legs destroyed 0.8. **Zombies (GDD §8):** chasing Fresh 4.5, Weathered 2.0, Decayed 1.2, crawler 0.4; wandering about half.
- **For Claude to add after hand-over, not part of the clip:** the moments hands or feet touch something (so the game can line them up with the real ledge), footstep and sound markers, and the point a move can be interrupted.

**Base poses:** standing idle, crouched idle, prone idle, hanging from a ledge, on a ladder, treading water, seated (chair height), seated in a vehicle, kneeling on one knee, lying on the back.

---

## 1. Player: moving around (GDD §25, §7)

### 1.1 Standing

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MOV-001 | Stand idle | Relaxed, breathing, small weight shifts | L | In place | 1 | Now | E |
| MOV-002 | Idle fidgets | Looks around, rolls shoulders, shifts feet | 1 | In place | 4–5 | Now | E |
| MOV-003 | Turn on the spot | Steps round to face a new way | 1 | In place | 45, 90, 135, 180 × L/R | Now | E |
| MOV-004 | Walk | Quiet, careful walk | L | In place | 8 dir | Now | E |
| MOV-005 | Jog | The normal pace | L | In place | 8 dir | Now | E |
| MOV-006 | Sprint | Flat-out run, leaning forwards. Forwards only | L | In place | F, FL, FR | Now | E |
| MOV-007 | Starts | Setting off from standing | 1 | In place | Walk and jog × 8 dir; sprint F | Now | E |
| MOV-008 | Stops | Coming to a halt | 1 | In place | Walk and jog × 8 dir; sprint F | Now | E |
| MOV-009 | Reversals | Changing to the opposite direction without stopping | 1 | In place | Jog: F↔B, L↔R | Opt | E |
| MOV-010 | Changes of pace | Walk to jog, jog to sprint, sprint to jog, and back | 1 | In place | 6 | Opt | E |
| MOV-011 | Limp | One leg hurt or broken, up to 2 m/s | L | In place | Left leg, right leg × F, B, L, R | M2 | – |
| MOV-012 | Both legs destroyed | Dragging, barely upright walk, 0.8 m/s | L | In place | F, B, L, R | M2 | – |
| MOV-013 | Trudge | Wading through snow | L | In place | Walk, jog | Sys | – |
| MOV-014 | Wade | Walking through knee-deep water | L | In place | Walk, jog | Sys | – |

### 1.2 Crouched

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MOV-020 | Crouch idle | Low, balanced, ready | L | In place | 1, plus 2–3 fidgets | Now | E |
| MOV-021 | Crouch down, stand up | | 1 | In place | 2 | Now | E |
| MOV-022 | Crouch walk, slow | Sneaking, 1 m/s | L | In place | 8 dir | Now | E |
| MOV-023 | Crouch walk, quick | 2.2 m/s | L | In place | 8 dir | Now | E |
| MOV-024 | Crouch turn on the spot | | 1 | In place | 90, 180 × L/R | Now | E |

### 1.3 Prone

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MOV-030 | Prone idle | Lying on the front, head up | L | In place | 1 | M2 | – |
| MOV-031 | Down to prone, up from prone | | 1 | In place | From and to crouch; from and to standing | M2 | – |
| MOV-032 | Crawl | On elbows and knees, 0.6 m/s | L | In place | F, B, L, R | M2 | – |
| MOV-033 | Prone turn | Pivoting on the belly | L | In place | L/R | M2 | – |

### 1.4 Leaning and looking (poses, blended by code)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MOV-040 | Lean | Upper body tilted out to one side | Pose | In place | L/R × standing, crouched | M2 | – |
| MOV-041 | Look and aim directions | Head and upper body turned up, down, left, right, as far as 120 degrees each side | Pose | In place | About 15 poses per stance | M2 | e |

### 1.5 Jumping and falling

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MOV-050 | Jump take-off | A small hop, about 75 cm | 1 | In place | Standing, walk, jog, sprint (F); B, L, R | Now | E |
| MOV-051 | Fall | In the air, short | L | In place | 1 | Now | E |
| MOV-052 | Long fall | Arms and legs working, from height | L | In place | 1 | M2 | – |
| MOV-053 | Land | Soft and hard, by pace | 1 | In place | Light, heavy × standing, walk, jog, sprint; backwards | Now | E |
| MOV-054 | Step off an edge | Walking or running off a drop | 1 | In place | Walk, jog, sprint | Now | E |
| MOV-055 | Bad landing | 4.5–5 m: lands hard, stumbles, a hand to the leg | 1 | In place | 1 | M2 | – |
| MOV-056 | Leg-breaking landing | Collapses on landing, gets up favouring one leg | 1 | In place | L/R | M2 | – |
| MOV-057 | Land in water | Splash, go under briefly, surface | 1 | In place | 1 | Sys | – |

### 1.6 Getting over things

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| VLT-001 | Running hurdle | Clears a fence up to 75 cm without touching it | 1 | Travels: over 0.75 m | L/R foot | Now | E |
| VLT-002 | Hands-on step-over | Hands on top of a fence, steps over, lands on the far side | 1 | Travels: over 0.75–1.5 m | Standing, walking, running × L/R foot | Now | E |
| VLT-003 | Vault with a drop behind | Hands on a low wall, over, and down a drop | 1 | Travels: over 1.1 m, then falling | Standing, walking, running | Now | E |
| VLT-004 | Climb onto, low | Hands on a ledge up to 1.5 m, step or pull up onto it | 1 | Travels: up 0.5–1.5 m | Standing, walking, running × L/R foot | Now | E |
| VLT-005 | Climb onto, high | Jump, grab a ledge up to 2.6 m, pull up, stand | 1 | Travels: up 1.5–2.6 m | Standing, walking, running × L/R foot | Now | E |
| VLT-006 | Climb over a tall wall | Jump, grab the top of a thin wall, pull up, a leg over, drop down the far side, in one motion | 1 | Travels: over 1.5–2.6 m | Standing, running | Now | J |
| **VLT-007** | **Side vault over a tall wall** | **From the push-up on top of the wall: the right hand stays planted on the right, the legs swing up to the left and over, carrying the momentum, and the body drops on the far side. No spin.** The developer's description, 2026-11-13. Every one-handed vault in the sample turns a full circle, so this has to be made | 1 | Travels: over 1.5–2.6 m | Right hand planted, left hand planted | Now | – |
| VLT-008 | Lower down the far side | From the top of a tall wall or a roof edge: turn, lower to a hang, drop | 1 | Travels: down to a hang | 1 | Sys | – |
| VLT-009 | Mid-air catch, onto | While jumping or falling: grab a ledge and get onto it | 1 | Travels | Ledge at shin, waist and head height | Now | E |
| VLT-010 | Mid-air catch, over a fence | While jumping: grab a thin fence and go over | 1 | Travels | Low, middle, high | Now | E |
| VLT-011 | Mid-air catch, over a tall wall | While jumping: grab the top of a thin tall wall, up and over | 1 | Travels | Low, high | Now | E |
| VLT-012 | Through a window | Climbs through an open window frame | 1 | Travels | Sill at knee and waist height | Sys | – |

### 1.7 Ledges (the light parkour: hold on and move sideways)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| LDG-001 | Catch a ledge | From a jump or a fall, both hands catch an edge and the body swings in to a hang | 1 | Travels | From a jump, from a fall | Sys | – |
| LDG-002 | Hang | Hanging by both hands, feet against the wall or free | L | In place | Feet on the wall, feet free | Sys | – |
| LDG-003 | Shimmy | Moving sideways hand over hand | L | Travels sideways | L/R | Sys | – |
| LDG-004 | Round a corner | Carrying on round an outside or inside corner | 1 | Travels | Outside, inside × L/R | Opt | – |
| LDG-005 | Pull up | From the hang, up onto the ledge | 1 | Travels: up | 1 | Sys | – |
| LDG-006 | Let go | Dropping from the hang | 1 | In place | 1 | Sys | – |
| LDG-007 | Climb down to a hang | Standing on a ledge: turn, kneel, lower over the edge | 1 | Travels: down | 1 | Sys | – |

### 1.8 Ladders and fire escapes

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| LAD-001 | Get on at the bottom | Steps up onto the first rungs | 1 | Travels | 1 | Sys | – |
| LAD-002 | Climb up | | L | Travels: up | 1 | Sys | – |
| LAD-003 | Climb down | | L | Travels: down | 1 | Sys | – |
| LAD-004 | Hold on | Stopped on the ladder | L | In place | 1 | Sys | – |
| LAD-005 | Get off at the top | Steps from the ladder onto the roof or landing | 1 | Travels | 1 | Sys | – |
| LAD-006 | Get on from the top | Turns round and steps down onto the ladder | 1 | Travels | 1 | Sys | – |
| LAD-007 | Get off at the bottom | Steps down and away | 1 | Travels | 1 | Sys | – |
| LAD-008 | Pull down a fire-escape ladder | Reaches or jumps up, grabs the bottom rung, pulls the ladder down | 1 | In place | 1 | Sys | – |
| LAD-009 | Slide down | Hands and feet outside the rails | L | Travels: down | 1 | Opt | – |

### 1.9 Swimming (on the surface only; no diving, no drowning)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| SWM-001 | Tread water | Staying in one place | L | In place | 1 | Sys | – |
| SWM-002 | Swim | Steady stroke, 1.2 m/s | L | In place | F, B, L, R | Sys | – |
| SWM-003 | Swim hard | Fast stroke, using stamina | L | In place | F | Sys | – |
| SWM-004 | Swim exhausted | Barely moving, head low, slower than normal swimming | L | In place | F | Sys | – |
| SWM-005 | Into and out of the water | Wading until it's deep enough to swim, and back | 1 | In place | In, out | Sys | – |
| SWM-006 | Climb out | Over a low dock edge, a bank, or the side of a boat | 1 | Travels | Low edge, boat side | Sys | – |

### 1.10 Pushing and carrying

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| CRY-001 | Shopping cart | Both hands on the bar: stand, push at a walk, turn | L | In place | Idle, walk, turn L/R | Sys | – |
| CRY-002 | Rolling suitcase | One hand behind, pulling: stand, walk | L | In place | Idle, walk | Sys | – |
| CRY-003 | Heavy two-handed carry | Lifts a generator, crate or bag of soil, walks, sets it down | 1→L→1 | In place | 1 | Sys | – |
| CRY-004 | Sack on the shoulder | | 1→L→1 | In place | 1 | Opt | – |

### 1.11 How the body shows its condition

Mostly short clips or poses layered over normal movement.

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| STA-001 | Out of breath | Stamina gone: heaving, hands on knees | L | In place | Standing, moving | M2 | – |
| STA-002 | Cold | Shivering, arms wrapped round the body | L | In place | Standing, walking | M2 | – |
| STA-003 | Hot | Wipes the brow, pulls at the collar | 1 | In place | 1 | Sys | – |
| STA-004 | Soaked | Shakes water off, wrings out a sleeve | 1 | In place | 1 | Opt | – |
| STA-005 | Sick | Coughing, hunched, a hand to the stomach | 1 | In place | Cough, retch | M2 | – |
| STA-006 | Hurt arm | The arm held against the body | Pose | In place | L/R × standing, moving | M2 | – |
| STA-007 | Hurt torso | A hand pressed to the side, bent over | Pose | In place | Standing, moving | M2 | – |
| STA-008 | Dazed | After a head hit: swaying, a hand to the head | L | In place | 1 | M2 | – |
| STA-009 | Infected, far gone | Feverish, unsteady | L | In place | Standing, walking | Sys | – |
| STA-010 | Stressed, bored | Shaky hands; looking around, scuffing a foot | 1 | In place | 2 | Opt | – |

---

## 2. Player: hands, items and inventory (GDD §11, §12, §6)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| INV-001 | Pick up | Takes something from the ground, a table, a high shelf | 1 | In place | Ground, table, shelf × one hand, two hands | M2 | – |
| INV-002 | Put down, drop | | 1 | In place | Place carefully, drop | M2 | – |
| INV-003 | Quick reach | Takes something from, or returns it to, a trouser pocket, jacket pocket, belt, chest rig or holster | 1 | In place | 5 places × take, put back | M2 | – |
| INV-004 | Dig through the pack | Stops, swings the bag round to the front, rummages, swings it back. The middle repeats for as long as the item is deep | 1→L→1 | In place | Standing, crouched | M2 | – |
| INV-005 | Toss into the pack | One quick throw-in over the shoulder or into the open bag | 1 | In place | 1 | M2 | – |
| INV-006 | Pack on and off | Puts on or takes off a backpack; slings a duffel or messenger bag | 1 | In place | Backpack, shoulder bag | M2 | – |
| INV-007 | Weapon to and from a sling | Swings a long weapon onto the back or shoulder and off again | 1 | In place | Body sling, bag sling, belt | M2 | – |
| INV-008 | Strap onto the pack | Ties a bulky item to the outside of the bag | 1 | In place | 1 | Sys | – |
| INV-009 | Change clothes | Pulls on or takes off a piece of clothing | 1 | In place | Top, trousers, footwear, headgear, vest or rig, gloves | M2 | – |
| INV-010 | Open and search | Opens a container, looks through it, closes it | 1→L→1 | In place | Cupboard, drawer, fridge, locker, lidded crate, cardboard box, car boot, shipping-container doors; at low, middle and high height | M2 | – |
| INV-011 | Search a body | Kneels and goes through the pockets | 1→L→1 | In place | 1 | M2 | – |
| INV-012 | Search for hidden pockets | A slower, careful search: seams, boots, waistband | L | In place | 1 | Sys | – |
| INV-013 | Flashlight | Holds a torch while standing and moving; switches a headlamp on | Pose, 1 | In place | Hand torch, headlamp | M2 | – |
| INV-014 | Check an instrument | Looks at a watch on the wrist; reads a thermometer or barometer in the hand | 1 | In place | Watch, hand-held | Sys | – |
| INV-015 | Map | Unfolds a map, studies it, marks it, folds it away | 1→L→1 | In place | 1 | Sys | – |
| INV-016 | Read | A sheet of paper, a book or a magazine | 1→L→1 | In place | Standing, sitting | Sys | – |
| INV-017 | Write in the journal | Takes out the journal and a pen, writes, puts it away | 1→L→1 | In place | 1 | M2 | – |
| INV-018 | Radio | Lifts a walkie-talkie to the mouth, talks, lowers it | 1→L→1 | In place | 1 | Sys | – |
| INV-019 | Money | Counts out notes and hands them over | 1 | In place | 1 | Sys | – |
| INV-020 | Spray a tag | Shakes a spray can and paints a wall | 1→L→1 | In place | 1 | Sys | – |

---

## 3. Player: surviving (GDD §7, §8, §10, §14)

### 3.1 Eating, drinking and other things you take

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| SRV-001 | Eat from the hand | Bites of a bar, sandwich or fruit | L | In place | Standing, sitting | M2 | – |
| SRV-002 | Eat from a can | Opens it (ring pull, knife, or opener) and eats with a spoon or fingers | 1→L→1 | In place | 3 ways of opening | M2 | – |
| SRV-003 | Eat a cooked meal | From a bowl or plate | L | In place | Standing, sitting | Sys | – |
| SRV-004 | Drink | From a bottle or canteen, a can, a mug | 1→L→1 | In place | 3 | M2 | – |
| SRV-005 | Drink from the hands | Kneels at water and drinks from cupped hands | 1→L→1 | In place | 1 | Sys | – |
| SRV-006 | Fill a bottle | At a tap or rain collector; kneeling at a river | 1→L→1 | In place | Standing, kneeling | M2 | – |
| SRV-007 | Purify water | Drops a tablet in and shakes the bottle | 1 | In place | 1 | Sys | – |
| SRV-008 | Smoke | Lights a cigarette, drags on it, flicks it away | 1→L→1 | In place | 1 | Sys | – |
| SRV-009 | Drink alcohol | From a bottle or flask | L | In place | 1 | Sys | – |
| SRV-010 | Take pills | Shakes some out and swallows them | 1 | In place | 1 | M2 | – |
| SRV-011 | Inject | A syringe into the arm or thigh (the antiviral, the delaying compound) | 1 | In place | Self, another person | Sys | – |

### 3.2 Treating injuries (per body part, GDD §7)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MED-001 | Bandage yourself | Wraps a bandage or rag round the part | 1→L→1 | In place | Head, torso, left arm, right arm, left leg, right leg | M2 | – |
| MED-002 | Bandage someone else | Kneeling or standing beside them | 1→L→1 | In place | Head or torso, an arm, a leg | Sys | – |
| MED-003 | Splint | Straps a splint to an arm (one-handed) or a leg (sitting) | 1→L→1 | In place | Arm, leg × self, another | M2 | – |
| MED-004 | Disinfect | Pours onto the wound, winces | 1 | In place | Upper body, arm, leg | Sys | – |
| MED-005 | Surgery kit | A long, careful job on a destroyed limb | 1→L→1 | In place | Arm, leg × self, another | Sys | – |
| MED-006 | Make a bandage | Tears a shirt into strips | 1 | In place | 1 | M2 | – |
| MED-007 | Being treated | Sitting or lying still, flinching | L | In place | Sitting, lying | Sys | – |

### 3.3 Fire, warmth and cooking

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| SRV-020 | Light a fire | Kneels, strikes a match or lighter, blows on it; adds fuel | 1 | In place | Light, feed | Sys | – |
| SRV-021 | Warm up | Hands held out to the fire | L | In place | Standing, crouched, sitting | Sys | – |
| SRV-022 | Boil water | Sets a pot on the fire, waits, lifts it off | 1 | In place | On, off | Sys | – |
| SRV-023 | Cook | Chops, stirs, serves at a cooking station | L | In place | Chop, stir | Sys | – |

### 3.4 Rest, comfort and leaving

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| SRV-030 | Sit | Sits down, sits, stands up | 1→L→1 | In place | On the ground, a chair, a couch, a bed edge | Sys | – |
| SRV-031 | Lie down and get up | In a bed or sleeping bag. Getting up is also how you appear when you respawn there | 1→L→1 | In place | Bed, sleeping bag | M2 | – |
| SRV-032 | Play an instrument | Sitting, playing a guitar | L | In place | 1 | Opt | – |
| SRV-033 | Play cards | Sitting at a table or on the ground: deals, plays a card | L | In place | 1 | Opt | – |
| SRV-034 | Listen to the radio | Sitting by it, relaxed | L | In place | 1 | Opt | – |
| SRV-040 | Log out | Sits down and waits out the 30 seconds; gets back up if cancelled | 1→L→1 | In place | 1 | M2 | – |

---

## 4. Player: melee and throwing (GDD §13, §7)

Five weapon classes, each needing the same set. **Classes:** bare hands; one-handed blunt (pipe, hammer, wrench); one-handed blade (kitchen knife, machete); two-handed swing (bat, crowbar, fire axe); sledgehammer (slower and heavier than the rest).

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MEL-001 | Hold | Carrying the weapon ready: standing, crouched, and while walking, jogging, sprinting | Pose, L | In place | 5 classes × standing, crouched, moving | M2 | – |
| MEL-002 | Draw and put away | From and to the belt, the back or a sling | 1 | In place | 5 classes | M2 | – |
| MEL-003 | Light attacks | Two or three quick swings that chain | 1 | In place | 5 classes × 2–3 swings | M2 | – |
| MEL-004 | Heavy attack | A wind-up and a full swing | 1 | In place | 5 classes | M2 | – |
| MEL-005 | Strike downwards | At something on the ground (a crawler, a knocked-down zombie) | 1 | In place | 5 classes | M2 | – |
| MEL-006 | Off-hand versions | The one-handed classes swung with the other hand, slower and clumsier (a broken main arm) | 1 | In place | 2 classes: hold, light, heavy | Sys | – |
| MEL-007 | Bounce off | The weapon stops dead on something hard | 1 | In place | 5 classes | Opt | – |
| MEL-010 | Shove | Both hands, or the weapon held across the body, push a zombie back | 1 | In place | Empty hands, holding a weapon | M2 | – |
| MEL-011 | Stomp | A heel down on a zombie's head on the ground | 1 | In place | 1 | M2 | – |
| MEL-012 | Tired swings | The same attacks with no stamina: slow, heavy | 1 | In place | 5 classes | Opt | – |
| THR-001 | Throw overhand | A rock, bottle or grenade | 1 | In place | Main hand, off hand (shorter, less accurate) | Sys | – |
| THR-002 | Toss underhand | A short, quiet lob | 1 | In place | 1 | Sys | – |
| THR-003 | Grenade | Pulls the pin, then throws | 1 | In place | 1 | Sys | – |
| THR-004 | Molotov | Lights the rag, then throws | 1 | In place | 1 | Sys | – |

---

## 5. Player: guns and bows (GDD §13, [gun roster](weapons/gun-roster.md))

The roster has 56 guns on **19 platforms**; every gun on a platform shares its clips. **This section gets a row per platform action when the roster is signed off.** Until then, this is the set every platform needs, then what each platform adds.

### 5.1 The set every platform needs

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| GUN-001 | Hold | Low ready: standing, crouched, prone, and walking, jogging, sprinting | Pose, L | In place | Per platform | Sys | – |
| GUN-002 | Aim | Raises to the eye, holds, lowers; the aim-direction poses | 1, Pose | In place | Per platform × standing, crouched, prone | Sys | – |
| GUN-003 | Fire | Recoil for one shot; for automatic fire | 1, L | In place | Per platform | Sys | – |
| GUN-004 | Empty click | Pulls the trigger on nothing | 1 | In place | Per platform | Sys | – |
| GUN-005 | Reload, rounds left | Swaps a part-used magazine from the chest rig | 1 | In place | Per platform | Sys | – |
| GUN-006 | Reload, empty | Swaps the magazine and readies the gun | 1 | In place | Per platform | Sys | – |
| GUN-007 | Clear a jam | Works the action to clear it | 1 | In place | Per platform | Sys | – |
| GUN-008 | Fire-mode switch | Thumbs the selector | 1 | In place | Platforms that have one | Sys | – |
| GUN-009 | Draw and put away | From and to a holster or sling | 1 | In place | Per platform | Sys | – |
| GUN-010 | Refill a magazine | Thumbs loose rounds into a magazine, as one action | 1→L→1 | In place | Pistol magazine, rifle magazine | Sys | – |
| GUN-011 | Fit and remove a part | Sight, muzzle device, under-barrel piece, stock, ghillie wrap | 1 | In place | Pistol, long gun | Sys | – |
| GUN-012 | Weapon light | Thumbs the light on and off | 1 | In place | 1 | Sys | – |
| GUN-013 | One arm only | A two-handed gun with a broken arm: fired from the hip, swaying badly | Pose, 1 | In place | Long guns | Sys | – |
| GUN-014 | Bipod | Sets a gun down on its bipod, prone or on cover, and lifts it | 1 | In place | Machine gun, anti-materiel | Sys | – |
| GUN-015 | Shoot from a vehicle | Leaning out of a window or door | Pose | In place | Pistol, long gun | Sys | – |

**Pistols need three versions of GUN-001 to GUN-009:** two hands; main hand alone; off hand alone (noticeably clumsier, slower reload). GDD §7.

### 5.2 What each platform adds

| Platform | What is different about handling it |
|---|---|
| Striker pistol, hammer pistol, heavy pistol, street pistol | Magazine in the grip. The hammer pistol also thumbs its hammer |
| Revolver | Swings the cylinder out, tips the empties out, loads loose rounds or a speedloader |
| Single-action revolver | Opens the loading gate, pushes out and loads one round at a time; cocks the hammer for every shot |
| SMG | Compact; magazine forward of or inside the grip, by model |
| Pump shotgun | Pumps after every shot; loads shells one at a time |
| Break-action (and the sawn-off) | Breaks open, empties fall out, drops in one or two shells, snaps shut |
| Semi-auto shotgun | Loads shells one at a time, then releases the bolt |
| Rimfire rifle | Small magazine or tube |
| Lever-action | Works the lever after every shot; loads one round at a time through the side gate |
| Bolt-action | Works the bolt after every shot; loads a magazine or single rounds |
| AR family (including the 9 mm), AR-10 | Magazine and bolt release; charging handle at the rear |
| Battle rifle | Heavier; rocks the magazine in |
| AK family (including the shotgun) | Rocks the magazine in; charging handle on the right |
| Machine gun | Opens the top cover, lays in a belt, closes it |
| Anti-materiel rifle | Very heavy; large magazine; fired from the bipod |
| Flare gun | Breaks open, one flare in, fired level or into the sky |
| Starter pistol | Blanks, loaded like a small revolver |
| Nail gun | A strip of nails pushed in |
| Pipe shotgun (crafted) | Pulls apart, one shell in, slams together to fire |
| Recurve and compound bow | Arrow from the quiver, nock, draw, hold (the arms begin to shake), loose, or let down without shooting; also while moving and crouched |
| Crossbow | Foot in the stirrup, hauls the string back, lays a bolt, aims, shoots |

---

## 6. Player: getting hurt, giving up, dying (GDD §7, §8, §10, §17)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| HRT-001 | Flinch | A light hit; a zombie's swipe also slows a moving player to a walk for 0.4 s (GDD §8 Attacks) | 1 | In place | From the front, back, left, right; standing, while moving | M2 | – |
| HRT-002 | Stagger | A heavy hit knocks the body off balance | 1 | In place | 4 directions | M2 | – |
| HRT-003 | Knocked down and getting up | | 1 | In place | Onto the back, onto the front | M2 | – |
| HRT-004 | Shot | By where it lands | 1 | In place | Head, torso, arm, leg | Sys | – |
| HRT-005 | Grabbed by a zombie | It has hold of you: a struggle, then either shoving it off or being bitten | 1→L→1 | In place | From the front, from behind; ends: break free, bitten | M2 | – |
| HRT-006 | Crawler at the ankle | Stumbles, kicks it off | 1 | In place | 1 | M2 | – |
| HRT-007 | Pulled off a bike | Dragged sideways off a bicycle or motorcycle to the ground | 1 | In place | 1 | Sys | – |
| HRT-008 | On fire | Flails, drops and rolls, beats the flames out | L, 1 | In place | 1 | Sys | – |
| HRT-009 | Thrown by a blast | | 1 | In place | Forwards, backwards | Sys | – |
| HRT-010 | Attacked by an animal | A dog hanging off an arm; knocked flat by a bear | 1 | In place | Dog, bear | Sys | – |
| HRT-011 | Knocked out | Collapses, lies out cold, comes round and gets up | 1→L→1 | In place | Falling forwards, backwards | M2 | – |
| RST-001 | Hands up | Raises them, holds, walks with them up, kneels, lowers them | 1→L→1 | In place | Standing, walking, kneeling | Sys | – |
| RST-002 | Being tied | Holds still while the hands are bound | 1 | In place | Standing, kneeling, lying | Sys | – |
| RST-003 | Restrained | Hands bound: standing, walking, kneeling | L | In place | 3 | Sys | – |
| RST-004 | Escort | One player leads a restrained player by the arm | L | In place | The one leading, the one led | Sys | – |
| RST-005 | Search someone | Pats down a standing player; goes through a knocked-out one (INV-011) | 1→L→1 | In place | The searcher, the searched | Sys | – |
| RST-006 | Tie someone | Zip ties, handcuffs or rope onto another player | 1 | In place | 3 kinds | Sys | – |
| RST-007 | Cut someone free | A knife through ties or rope; bolt cutters through cuffs | 1 | In place | 2 | Sys | – |
| RST-008 | Struggle free | Working at the bonds, then breaking them | L, 1 | In place | 1 | Sys | – |
| DTH-001 | Die | Falls dead | 1 | In place | Forwards, backwards, to the side; from crouched and prone | M2 | – |
| DTH-002 | Head shot | Drops at once | 1 | In place | 1 | M2 | – |
| DTH-003 | Bleed out | Sinks to the knees, then over | 1 | In place | 1 | M2 | – |
| DTH-004 | Die of the infection | Collapses and lies still | 1 | In place | 1 | Sys | – |
| DTH-005 | Die in a seat, in water | Slumps at the wheel; goes limp and floats | 1 | In place | 2 | Sys | – |

_To decide when death is built:_ whether deaths are clips or the body simply going limp (physics). Clips are listed in case.

---

## 7. Player: building, crafting, raiding (GDD §9, §14)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| BLD-001 | Place a piece | Holds the outline of a building piece and sets it | 1 | In place | 1 | Sys | – |
| BLD-002 | Hammer | Nailing | L | In place | Low, chest height, overhead | Sys | – |
| BLD-003 | Saw | Cutting wood on a bench or the ground | L | In place | 2 | Sys | – |
| BLD-004 | Lay bricks | Mortar, brick, tap it down | L | In place | 1 | Sys | – |
| BLD-005 | Weld | Mask down, weld, mask up | 1→L→1 | In place | Low, chest height | Sys | – |
| BLD-006 | Board up | Holds a plank across a door or window and nails it | 1 | In place | Door, window | Sys | – |
| BLD-007 | Plant the claim | Sets the claim item into the floor | 1 | In place | 1 | Sys | – |
| BLD-008 | Put down furniture | Unrolls a sleeping bag; sets down a bed, bench or storage box | 1 | In place | Sleeping bag, large item | Sys | – |
| BLD-009 | Code lock | Fits a lock to a door; types a code on it | 1 | In place | Fit, type | Sys | – |
| BLD-010 | Take a piece down | Prises a piece off with a crowbar or hammer claw | L | In place | 1 | Sys | – |
| BLD-011 | Generator | Pulls the starter cord; pours fuel in | 1 | In place | Start, refuel | Sys | – |
| BLD-012 | Doors, gates, hatches | Opens and closes: pushes, pulls, slides, lifts | 1 | In place | Push door, pull door, sliding gate, roll-up shutter, floor hatch | M2 | – |
| CRF-001 | Craft by hand | Puts something together in the hands | L | In place | Standing, crouched, walking | M2 | – |
| CRF-002 | Work at a station | Workbench; gunsmith bench; reloading press (pulls a lever); sewing station | L | In place | 4 | Sys | – |
| CRF-003 | Take things apart | Furniture (saw, crowbar); a car (wrench); electronics (screwdriver) | L | In place | 3 | Sys | – |
| CRF-004 | Chop a tree | Swings an axe into a trunk | L | In place | 1 | Sys | – |
| CRF-005 | Repair | Cleans a gun with a rod and cloth; sews a bag or clothes; works on a tool | L | In place | 3 | Sys | – |
| CRF-006 | Hacksaw | Saws through a barrel or a lock | L | In place | 1 | Sys | – |
| RAD-001 | Crowbar | Levers a door or boards open | L | In place | 1 | Sys | – |
| RAD-002 | Sledgehammer a wall | Full swings into a wall or door | L | In place | 1 | Sys | – |
| RAD-003 | Power tool | Leans on a grinder or drill cutting through metal | L | In place | 1 | Sys | – |
| RAD-004 | Explosive charge | Sets a charge against a wall and arms it | 1 | In place | 1 | Sys | – |
| RAD-005 | Bolt cutters | Cuts a padlock or chain; snips through a fence; a container seal; a bike dock | 1, L | In place | Padlock, fence | Sys | – |
| RAD-006 | Force a door | Kicks it in; shoulders it; takes an axe to it | 1 | In place | 3 | Sys | – |
| RAD-007 | Break a window | Smashes it with a tool or an elbow, clears the glass | 1 | In place | 2 | Sys | – |

---

## 8. Player: farming, fishing, hunting, burying (GDD §22, §6)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| FRM-001 | Dig | Shovels earth | L | In place | 1 | Sys | – |
| FRM-002 | Bury and dig up | Sets something in the hole and covers it; uncovers and lifts it out | 1 | In place | 2 | Sys | – |
| FRM-003 | Plant | Kneels and presses seeds in | 1 | In place | 1 | Sys | – |
| FRM-004 | Water | Tips a watering can along a row | L | In place | 1 | Sys | – |
| FRM-005 | Harvest | Pulls from the ground; picks from a plant | 1 | In place | Low, waist height | Sys | – |
| FRM-006 | Fill a planter | Carries a bag of soil and pours it in | 1 | In place | 1 | Sys | – |
| FRM-007 | Chickens | Scatters feed; collects eggs; catches and carries a chicken | 1 | In place | 3 | Sys | – |
| FSH-001 | Fish | Baits the hook, casts, waits, strikes, reels in, lands the fish | 1→L→1 | In place | Standing, sitting | Sys | – |
| HNT-001 | Butcher | Kneels over an animal and skins and cuts it up | L | In place | Large animal, small animal or bird, fish | Sys | – |
| HNT-002 | Read tracks | Kneels and studies prints or blood on the ground | 1 | In place | 1 | Sys | – |
| HNT-003 | Trap | Sets one; checks one | 1 | In place | 2 | Sys | – |

---

## 9. Player: vehicles, boats, helicopters (GDD §16)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| VEH-001 | Get in and out of a car | Opens the door, sits, closes it; and the reverse | 1 | Travels | Driver, passenger × car, tall vehicle (van, truck, Humvee), rear doors (van, ambulance) | Sys | – |
| VEH-002 | Drive | Hands on the wheel, steering either way | Pose, L | In place | Car, tall vehicle | Sys | – |
| VEH-003 | Ride as a passenger | Sitting, braced | L | In place | Front, back | Sys | – |
| VEH-004 | Look back | Twists round to reverse | Pose | In place | 1 | Opt | – |
| VEH-005 | Crash | Thrown against the belt or the wheel | 1 | In place | 1 | Sys | – |
| VEH-006 | Bicycle | Gets on, pedals slow and fast, coasts, leans into a turn, gets off | 1→L→1 | In place | Bicycle, e-bike (little pedalling) | Sys | – |
| VEH-007 | E-scooter | Steps on, pushes off, rides standing, steps off | 1→L→1 | In place | 1 | Sys | – |
| VEH-008 | Motorcycle | Swings a leg over, starts it, rides, leans, gets off | 1→L→1 | In place | Motorcycle, dirt bike | Sys | – |
| VEH-009 | Boot and bonnet | Opens and closes them | 1 | In place | 2 | Sys | – |
| VEH-010 | Work on a car | Under the bonnet; kneeling at a wheel changing a tyre; swapping a battery | L | In place | 3 | Sys | – |
| VEH-011 | Fuel | Pours from a can into the tank; siphons out with a hose | 1→L→1 | In place | 2 | Sys | – |
| VEH-012 | Start without a key | Works under the dashboard (old cars); holds a device to the car (modern ones) | L | In place | 2 | Sys | – |
| VEH-013 | Fit armour or a lock | Bolts or welds a plate on; fits a steering-wheel lock | L | In place | 2 | Sys | – |
| VEH-014 | Free a share bike | Cuts the dock lock and pulls the bike out | 1 | In place | 1 | Sys | – |
| BOT-001 | Paddle | Gets into a kayak or canoe, paddles each side, gets out | 1→L→1 | In place | 1 | Sys | – |
| BOT-002 | Row | Sits and pulls two oars | L | In place | 1 | Sys | – |
| BOT-003 | Outboard | Pulls the starter cord, sits steering by the tiller | 1, L | In place | 1 | Sys | – |
| BOT-004 | At the helm | Standing or sitting at a wheel and throttle | L | In place | Standing, sitting | Sys | – |
| BOT-005 | Jet ski | Gets on, rides, leans | 1→L→1 | In place | 1 | Sys | – |
| BOT-006 | Aboard | Steps on from a dock; climbs in from the water; sits or stands holding on | 1, L | Travels | 3 | Sys | – |
| BOT-007 | Mooring | Ties up and casts off | 1 | In place | 2 | Opt | – |
| HEL-001 | Get in and out | Pilot and passengers | 1 | Travels | Pilot, passenger | Sys | – |
| HEL-002 | Fly | Hands on the two controls, feet on the pedals | Pose, L | In place | 1 | Sys | – |
| HEL-003 | Start up | Flips switches overhead and in front | 1 | In place | 1 | Sys | – |
| HEL-004 | Ride | Sitting in the back, holding on | L | In place | 1 | Sys | – |
| HEL-005 | Repair | Works at an open panel | L | In place | 1 | Sys | – |

---

## 10. Zombies (GDD §8, §9, §10, §16)

Four ordinary tiers that differ in how they move, a crawler, and two special kinds. What a zombie was (police, firefighter, dockworker) changes its clothes, not its clips.

**Stand-ins until these are made (GDD §8, decided 2026-11-13):** first the sample's mannequin tinted by tier, playing the sample's walk and idle slowed down; next Mixamo's free zombie set (about 20 files the developer downloads), which covers most of the M2 rows here. The server never plays zombie animations.

### 10.1 Every ordinary zombie

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| ZMB-001 | Stand | Swaying, head lolling | L | In place | 3–4, so a crowd doesn't move as one | M2 | J |
| ZMB-002 | Wander | Slow, aimless, at about half its chasing speed | L | In place | Per tier: Fresh about 2.2 m/s, Weathered 1.0, Decayed 0.6; 2 each | M2 | J |
| ZMB-003 | Notice | The head snaps round to a sound; turns to face it | 1 | In place | Left, right, behind | M2 | – |
| ZMB-004 | Chase: Fresh | Between a walk and a run, driven, arms reaching; 4.5 m/s | L | In place | 2 | M2 | J |
| ZMB-005 | Chase: Weathered | A brisk walking pace, stiff; 2.0 m/s | L | In place | 2 | M2 | J |
| ZMB-006 | Chase: Decayed | A dragging shamble; 1.2 m/s | L | In place | 2 | M2 | J |
| ZMB-007 | Turn on the spot | Lurching round | 1 | In place | 90, 180 × L/R | M2 | – |
| ZMB-008 | Grab | Lunges and takes hold of a person, then holds on for about 1.5 s (the bite, ZMB-009, or shoved off, ZMB-011, follows) | 1→L | In place | Front, from behind | M2 | – |
| ZMB-009 | Bite | Bites what it is holding | 1 | In place | Standing; on someone on the ground | M2 | – |
| ZMB-010 | Swipe | A clear 0.5 s wind-up a player can read and step away from, then a clawing scratch reaching about 1.5 m; one every 1.5 s | 1 | In place | Left arm, right arm | M2 | – |
| ZMB-011 | Shoved off | Thrown back off its victim | 1 | In place | 1 | M2 | – |
| ZMB-012 | Beat on something | Fists and claws on a door, wall or barricade; a city door gives after about 30 s of one zombie | L | In place | 2–3 | M2 | – |
| ZMB-013 | Break through | The last heave as a door or boards give, or a fist through a closed window | 1 | Travels | Door, boards, window glass | M2 | – |
| ZMB-014 | Over a low fence | Hauls itself over, slowly (about 2 s) | 1 | Travels: over up to 1.1 m | Makes it; falls on the far side; in through a ground-floor window opening | M2 | – |
| ZMB-015 | Reach up | Clawing upward at someone on a ledge, ladder or car roof it can't climb; reaches about 1.5 m; in a crowd, the others pressing in | L | In place | 1 | M2 | – |
| ZMB-016 | At a vehicle | Beats on a car; reaches in through a window; drags a rider off a bike | L, 1 | In place | 3 | Sys | – |
| ZMB-017 | Hit, still standing | Rocked by a hit to the body | 1 | In place | Front, back, left, right | M2 | – |
| ZMB-018 | Pushed back | Stumbles backwards from a shove; either keeps its feet or goes down | 1 | In place | Stays up, falls | M2 | – |
| ZMB-019 | Knocked down and up again | | 1 | In place | Onto the back, onto the front | M2 | – |
| ZMB-020 | Legs gone | Drops as the legs are destroyed and keeps coming on its arms | 1 | In place | 1 | M2 | – |
| ZMB-021 | Killed | A hit to the head: drops | 1 | In place | Standing, moving, on the ground | M2 | – |
| ZMB-022 | Feed | Crouched over a body | L | In place | 1 | Sys | – |
| ZMB-023 | Trip | Falls over something low and gets up | 1 | In place | 1 | Opt | – |
| ZMB-024 | Burn | Keeps walking on fire, then falls | L, 1 | In place | 1 | Sys | – |
| ZMB-025 | At the water's edge | Stops at deep water, reaching out | L | In place | 1 | Sys | – |
| ZMB-026 | Rise | A dead body turns: twitches, then gets up as a Fresh zombie | 1 | In place | From the back, from the front | Sys | – |
| ZMB-027 | Spot | Catches sight of something: stops, head pushed forward, stares for about a second (the moment a player can still duck) | 1 | In place | Ends two ways: loses interest; a moan and a lurch into the chase | M2 | – |
| ZMB-028 | Search | Where it last saw someone: stops, turns, head sweeping and sniffing, a few steps, again (about 30 s) | L | In place | 2 | M2 | – |

### 10.2 Crawlers

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| ZMB-030 | Lie | Still, or twitching | L | In place | 2 | M2 | – |
| ZMB-031 | Crawl | Dragging itself by the arms; 0.4 m/s chasing, about 0.2 wandering | L | In place | 2 | M2 | – |
| ZMB-032 | Grab an ankle | Reaches and takes hold; bites | 1 | In place | 1 | M2 | – |
| ZMB-033 | Hit, killed | | 1 | In place | 2 | M2 | – |

### 10.3 The two special kinds

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| ZMB-040 | The Patient: stand, wander | In a hospital gown; more alert than the others | L | In place | 2 | Sys | – |
| ZMB-041 | The Patient: run | The only one that truly runs, at full speed | L | In place | 1 | Sys | – |
| ZMB-042 | The Patient: attack | A running lunge; grab; bite | 1 | In place | 3 | Sys | – |
| ZMB-043 | The Patient: speak | Stops, says a word or a sentence, goes back to mumbling | 1 | In place | 2–3 | Sys | – |
| ZMB-044 | The Patient: hit, killed | Takes more to the head than the others | 1 | In place | 3 | Sys | – |
| ZMB-045 | The Host: stand, walk | Slow and heavy, restraints and tubing hanging off it | L | In place | 2 | Sys | – |
| ZMB-046 | The Host: attack | A heavy swing; a crushing grab | 1 | In place | 2 | Sys | – |
| ZMB-047 | The Host: hit, killed | Barely reacts to hits; goes down slowly | 1 | In place | 3 | Sys | – |

---

## 11. Animals (GDD §22)

Each animal needs: standing, moving at each of its paces, turning, being hit, dying. The table gives what is particular to each.

| ID | Animal | Paces | Also |
|---|---|---|---|
| ANM-001 | Deer | Walk, trot, bounding run | Grazing; head up, alert; bolting |
| ANM-002 | Wild turkey | Walk, run | Pecking; a short flapping flight |
| ANM-003 | Goose, duck | Walk, swim, fly | Take-off and landing on land and water; feeding |
| ANM-004 | Rabbit | Hop, run | Sitting up, alert |
| ANM-005 | Pigeon | Walk, fly | Pecking; take-off, landing |
| ANM-006 | Rat | Scurry | Sniffing |
| ANM-007 | Feral dog | Walk, trot, run | Growling, barking; circling as a pack; lunge and bite; hanging on to an arm |
| ANM-008 | Coyote | Walk, trot, run | As the dog, plus howling |
| ANM-009 | Black bear | Walk, run | Standing up on the hind legs; roar; swipe; mauling someone on the ground |
| ANM-010 | Bobcat | Stalk, run | Crouch; pounce; claw and bite |
| ANM-011 | Chicken | Walk, flapping run | Pecking; sitting in a coop; being carried |
| ANM-012 | Seal | Shuffle, swim | Lying on a pier; slipping into the water |
| ANM-013 | Beaver | Walk, swim | Gnawing |
| ANM-014 | Fish | – | Flapping on the line and on the ground |

All animals also need **running from zombies** (their run, already listed). When: with wildlife (Sys).

---

## 12. Other people in the world (GDD §18)

Traders and guards can use the player's clips for moving and shooting. These are what only they need.

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| NPC-001 | Trader | Stands behind a counter; greets; hands something over; takes money; shrugs; points | L, 1 | In place | 5–6 | Sys | – |
| NPC-002 | Talk | Talking with the hands, so traders and guards aren't statues | L | In place | 3 | Sys | – |
| NPC-003 | Guard | Stands watch with a rifle; paces a beat; raises a hand to stop someone; waves them in | L, 1 | In place | 4 | Sys | – |
| NPC-004 | Overwatch sniper | Lies or kneels behind a rifle scanning; settles on a target; fires a warning shot | L, 1 | In place | 3 | Sys | – |
| NPC-005 | Clerk | At the bank or storage desk: types, slides a card back | L | In place | 2 | Sys | – |
| NPC-006 | Mechanic | Works at a bench or a vehicle | L | In place | 1 | Sys | – |
| NPC-007 | Use a card and keypad | The player's side of the bank: card in, type a PIN | 1 | In place | 1 | Sys | – |
| NPC-008 | Vending machine | The player buys from one: taps, takes the item | 1 | In place | 1 | Sys | – |

---

## 13. Menus and character creation (GDD §21)

| ID | Clip | What the body does | Loop | Moves | Variants | When | Have |
|---|---|---|---|---|---|---|---|
| MNU-001 | On show | Standing for the character screen; turns to show an outfit | L, 1 | In place | 2 | Sys | – |
| MNU-002 | Gestures | Wave, point, nod, shake the head, beckon, thumbs up, finger to the lips | 1 | In place | 7 | Opt | – |

_Gestures other than hands-up are not in the design yet; listed because players of this kind of game expect them._

---

## 14. Still to be added

These lists aren't final, so their clips can't be listed one by one yet. Each gets its rows when the list is settled.

- **Guns, platform by platform** (section 5): after the roster's final sign-off.
- **Food and drink, item by item:** only where an item is handled differently from SRV-001 to SRV-004.
- **Melee weapons, item by item:** only where one needs more than its class's set (the nail bat and spiked pipe use their class's).
- **Special zombies' unique moments** and anything the lore adds (the lore is to be revisited; GDD §23).
- **Traps, tracking and fishing tackle** (GDD §22 open items).
- **Helicopter types, boat types** (GDD §16 open items): only where getting in or the seat differs.
- **Anything new a system's design pass adds.**

## Rough size

308 numbered rows, plus the 21 gun and bow platforms in section 5.2. By when they're needed: 27 are in the game now on sample clips, 83 are for milestone 2, 168 come with their systems, 16 are optional, and 14 are the animals.

Each row is several clips once its variants are made. Claude's rough estimate, not a count: 1,400 to 1,600 clips in all, with movement about 350, guns about 400 once every platform has its set, and zombies about 115. The sample we use today is about 800 clips, nearly all of them movement.

Fewer are needed to start: the rows marked **Now** and **M2** are 110 of the 308.
