# Animations we have

Every clip here comes from Epic's free Game Animation Sample (GDD §25). There are about 800. This page says what exists, how to read the names, which ones the game uses today, and what is missing. Written 2026-11-12.

## How to watch one

In the editor's Content Browser open `Content > Characters > UEFN_Mannequin > Animations`, pick a folder, and double-click a clip. It opens with a play bar. Hovering over a clip also plays a small preview.

When you tell Claude what you want, the clip's name (or "the one in folder X that does Y") is enough.

## How to read the names

| Part of the name | Meaning |
|---|---|
| `Walk`, `Run`, `Sprint`, `Crouch` | The pace. **Our jog plays the `Run` clips; our walk plays `Walk`; our sprint plays `Sprint`.** |
| `F`, `B` | Moving forwards, backwards |
| `FL`, `FR`, `BL`, `BR` | Diagonals |
| `LL`, `LR`, `RL`, `RR` | Sideways: the first letter is the direction of travel, the second which way the hips are turned |
| `Lfoot`, `Rfoot` | Which foot leads when the clip starts |
| `045`, `090`, `135`, `180` | Degrees of a turn |
| `Loop` | Steady movement, repeats |
| `Start`, `Stop` | Setting off, coming to a halt |
| `Pivot` | Reversing direction without stopping |
| `Turn` | Turning while moving (or on the spot, in `Idle`) |
| `Reface_Start` | Setting off in a direction the body isn't facing |
| `Transition_A_to_B` | Changing pace, for example `Run_to_Sprint` |
| `Box`, `Diamond`, `Hourglass`, `Prism`, `Shuffle`, `Arc` | Changing direction while strafing; the word is the shape of the path the actor walked |
| `Light`, `Heavy` | A soft or a hard landing |
| `1_0`, `2_5` | The obstacle height the clip was made for, in metres (the game stretches it to the real height) |
| `V2` | A second version of a vault; here these are the sideways rollovers |

The clips were made at the sample's speeds: walk 2 m/s, run 5 m/s, sprint 7 m/s. Ours are 1.6, 3.5 and 6 m/s, and the game slows the clips to fit.

## Two kinds of clip

- **Moving around (walk, run, sprint, crouch, idle, jump):** the game picks these by itself, many times a second, from whatever best matches what the body is doing. Nobody chooses one by name. What Claude can do is take clips out of a set or put clips in (this is how the sprint losing its lean was fixed).
- **Getting over things (the `Traversal` folder):** Claude picks these with a short table in the code, by the obstacle's height and depth, your speed, and which foot is in front. This table is easy to change.

## Getting over things: every clip

Folder `Traversal`. Each exists as a left-foot and a right-foot version unless noted.

| Clip | What the body does | Used today? |
|---|---|---|
| `Hurdle_1_0_run` | Running jump over a fence, no hands | Yes: fences up to 75 cm at a jog or sprint |
| `Hurdle_1_0_walk` | Hands on top, step over | Yes: fences up to 1.5 m when walking, standing, or taller than 75 cm |
| `Hurdle_1_0_run_V2`, `_walk_V2`, `_stand_V2` | Rolls the body sideways over the fence | **No. Rejected 2026-11-11 ("rollover parkour type vault")** |
| `Vault_1_0_stand`, `_walk` (one foot each) | Both hands on top, over a low wall, then a long fall | Yes: thin walls up to 1.1 m with a drop behind |
| `Vault_1_0_run` (one foot) | One hand planted (the right), left arm up, legs over, then a long fall | Yes: the same at a run. Also the other ending of a climb over a thin tall wall, when `Climb Over One Handed` is switched on in the NYZ Movement settings (off by default) |
| `Mantle_1_0_stand`, `_walk` | Hands on a ledge, step up onto it | Yes: onto things up to 1.5 m |
| `Mantle_1_0_run` | Leaps straight onto the ledge | Yes: only up to 75 cm at a run |
| `Climb_Start_2_5_stand`, `_walk`, `_run` | Jump, grab a high ledge, pull up, stand | Yes: onto things from 1.5 m to 2.6 m, and the jump and grab of climbing over a thin tall wall |
| `Catch_Cliff_high_stand` (one) | In the air: grab a high ledge, pull up | Yes: Space held in the air, ledge more than 1 m above the feet |
| `Catch_Mantle_low_stand`, `_med_stand` (one each) | In the air: grab a ledge at foot or waist height, get onto it | Yes: Space held in the air, lower ledges |
| `Catch_Hurdle_low_stand`, `_med_stand`, `_high_stand` (one each) | In the air: grab a thin fence, go over | Yes: Space held in the air at a fence |
| `Catch_Vault_low`, `_med`, `_high` (one each) | In the air: grab, pull up, go over, long fall | Yes, since 2026-11-12: the pull up and over of a thin wall taller than chest height with ground behind it (the developer's pick), after the climb's grab from the ground or by itself from a jump. Never over a drop |

That is the whole folder: 34 clips.

## Moving around: what each folder holds

| Folder | Clips | What's in it |
|---|---|---|
| `Idle` | 20 | Standing still (`Stand_Idle_Loop`), five fidgets (`Stand_Idle_Break_v01` to `v06`), the same crouched, and turning on the spot by 45, 90, 135 and 180 degrees |
| `Walk` | 206 | Loops in ten directions, starts, stops, pivots, turns, direction changes, and changes of pace from run and sprint |
| `Run` | 208 | The same set at a run (our jog), plus two gentle curves (`Run_Arc_Small_L`, `_R`) |
| `Sprint` | 35 | Forwards and forward diagonals only: loops (`Sprint_Loop_F`, `_FL`, `_FR`), starts, stops, 90 and 180 degree turns, and changes of pace from walk and run |
| `Crouch` | 205 | The walk set, crouched, plus standing up and crouching down (`Transition_Stand_to_Crouch`, `_Crouch_to_Stand`) |
| `Jump` | 59 | Take-offs by pace and direction (forwards, backwards, left, right), the fall (`Jump_Loop_Fall`), light and heavy landings by pace, and stepping off an edge (`Jump_F_Off_Walk`, `_Run`) |
| `Poses` | 6 | The body leaning into a turn at a run |
| `AimOffset` | 17 | The upper body looking up, down, left and right. Not used yet |

## What does not exist

No clip in the sample does any of these. Each needs another free source (for example Mixamo), a bought pack, or a rough stand-in made by Claude (GDD §25).

- Lowering down the far side of a tall wall by the hands. Climbing over one is two clips joined (the climb's grab, then the catch-vault), and the far side is always a drop.
- Ladders and fire escapes.
- Hanging from a ledge and moving sideways along it.
- Lying prone and crawling (prone plays the crouch clips for now).
- Swimming.
- Rolling or stumbling out of a long fall.
- Leaning around a corner (planned as code-driven, not a clip).
- Anything holding a weapon or an item, melee swings, eating, drinking, bandaging.
- Limping or other injured movement.
- Any zombie movement.
