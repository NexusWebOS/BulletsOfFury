# Overdrive — Yuri, Dead Signal and Night Run

Release build: `overdrive1013-yuri-motion-r1`, October 13, 2026.
Publication details: [GitHub release](GITHUB_RELEASE_1013.md).

## Yuri movement follow-up

Mike requested clearer crawl/walk frames and smoother movement after playing.
The follow-up supplies **316 newly authored frames in 24 banks**: walk,
run-and-fire and crawl in all eight directions, with 12–16 distinct drawings
per bank. Existing jump, roll, cover and utility actions remain available.

Animation advances by actual distance after collision, using a 96 px standing
stride and 48 px crawl stride. Walk/fire share the same phase; backpedaling
reverses it. A blocked wall stops the loop, with an 80 ms foot-settle on stopping.
The directional sprite has a small boundary dead band to prevent flicker;
weapon aiming remains continuous. Scripted boss-entry walking advances the
same cycle. Standing speed 165 px/s and crawl speed 63 px/s are unchanged.
Measured east crawl: 15 pose changes over one second (about 16 fps versus the
previous 3.8 fps). No movement acceleration or weapon balance was changed.

Owner: `expansion/topdown/_research/build_yuri_motion_1013.py`; sources and
exact built-in imagegen prompts: `expansion/topdown/art/yuri_motion_1013/source`.
Frames have 320x320 transparent canvases, shared pivot 160,256, common bank
scale, no cut limbs and a recorded crop/registration audit. The animation
viewer now supports variable frame counts, actual cadence, half speed and
an old/new comparison. New art is registered after the original assault pack.

Verification: 26/26 native movement/art/viewer checks and 38/38 existing assault
checks, zero browser/asset errors; all 316 new frames inspected in native ART.
Required base suite: 8,700 passes, zero errors, final banner and exit 0.
Syntax checks pass. Evidence: `docs/qa/overdrive_yuri_motion_1013.json`.
Verification was recorded locally before publication.

## Play

Run `PLAY_OVERDRIVE.bat` from the repository root for the fullscreen launcher.
The normal title, difficulty, pilot, options and password menus remain the entry
point. Campaign order is **2 → 3 → 4 → 5 → 6**.

To try the new stages immediately, enter either code through **Password**:

| Stage | Yuri / Normal / Hotwire password |
| --- | --- |
| Level 3 — Fortress / Dead Signal | `OD-237B-5JXM` |
| Level 6 — Night Run / Hull Zero | `OD-237E-5JXQ` |

[Animated Yuri viewer](../expansion/topdown/art/assault_1013/review.html) includes
eight direction choices, individual frames, pause/step and an onion-skin option.

## Yuri and cover combat

The initial Yuri bank contained 384 core frames: eight directions × eight
actions × six poses; the movement follow-up above supersedes its walk,
run-and-fire and crawl loops. The initial walk,
run-and-gun, jump, crouch, roll, prone fire, crawl and cover peek have changing
limb poses. Additional six-frame grenade and death sequences face south.
Yuri draws at approximately 65–74 pixels standing height in the 640×480 field.
The remaining pilots retain their previous infantry art.

Movement and aim are independent. Yuri has three armor points; jump and roll
consume a refilling stamina budget. Jump has physical sprite height. The
default assault rifle is unlimited; upgrade guns use a finite total ammunition
pool and automatically return to the rifle when empty. Reload is unnecessary.
These weapon rules also apply to the existing Museum mission.

Hold cover beside a barrier, box, barrel, server or wall. Holding fire plays a
peek/fire/return cycle; releasing fire immediately lowers the character. Low
cover absorbs incoming fire while hidden and leaves the player vulnerable
during the exposed firing interval. At a tall wall, the character physically
slides to its end to peek and returns to the protected anchor. Prone stays
latched until toggled. Retina can acquire the available firing lane from cover.
Concrete, wood, barrels and equipment have HP, authored broken states, collision
removal and the existing authored dust, debris, smoke and explosions.

| Action | Keyboard / mouse | Standard pad | Six-button pad |
| --- | --- | --- | --- |
| Move | WASD / arrows | Left stick / D-pad | D-pad |
| Aim/fire | Mouse + left button / J | Right stick + A | X north, Y west, A south, B east; adjacent pairs diagonal |
| Jump | R or K | B or Mode+A | Mode+A |
| Roll | H / Space / right mouse | X | C |
| Crouch / cover | Hold L / Shift | Hold L shoulder | Hold L shoulder |
| Prone / crawl | F, then movement | Mode+X | Mode+X |
| Grenade | U / middle mouse | Y | Z |
| Retina | I / N | R shoulder | R shoulder |
| Cycle upgrade | Tab / wheel | Mode+B | Mode+B |

Bindings are editable in the original Options renderer. B remains Back in
menus; A and Start confirm. Physical shoulder indices follow controller setup.

## Fortress / Dead Signal

The 800×2400 authored fortress leads into an AI data center. Destroy three red
security relays to unlock the encounter, then advance north. Relay destruction
drops an armor repair. Checkpoints save route progress between deaths.

The north blast doors open amid concrete explosions and introduce **Gosfer**:
an original alien soldier with a 40-watt laser rifle and 260 HP. He strafes,
fires aimed and spread volleys and reflexively dodges nearby shots. Dodges have
a 2.1-second cooldown, leaving a real damage window. His whole authored plate
uses four views with walk, fire, dodge and hurt poses. Defeat ends this encounter
with a retreat line, preserving his role as the expansion antagonist.

## Additional armor

| Enemy | Role |
| --- | --- |
| Jackal | Fast, light burst-fire scout |
| Lancer | Long-range rail attacker |
| Manticore | Missile carrier |
| Bastion | Slow, heavy quad-track tank |

Both existing tank stages mix these four new families into their encounters.
Each has authored idle, tread, firing and wreck artwork.

## Night Run / Hull Zero

Hotwire drives a green Silverado through dark hills while the selected pilot
mans the bed turret. Yuri has a newly drawn turret crew plate; other pilots use
their existing authored crew artwork. A 7.5-second searchlight opening precedes
**150 seconds of pursuit**. Jets launch interceptable rockets; flanking gun
trucks and running robot infantry attack the hull. Strong red robots enter
after 115 seconds. There is no boss or miniboss.

The turret rotates freely; its machine gun is unlimited. The truck has 100 hull
points. Destruction plays a wreck/explosion sequence and restarts the complete
run after three seconds. Surviving the timer ends with extraction and the normal
results/save flow. Pause freezes progression. Detection is recorded, so pursuit
does not incorrectly award an undetected clear.

## Art ownership

`expansion/topdown/_research/build_assault_1013.py` owns the **518 exports**,
86 banks and loose manifests under `art/assault_1013/`. Originals and exact
generation prompts are retained in `source/`. Yuri's actual shipped body and
portrait were supplied as identity references. Source sheets with odd measured
cells are isolated without repainting and padded onto even shared canvases.
Connected-component extraction preserves crossing limbs and excludes fragments
from adjacent cells. Each bank uses a common proportional scale and registered
anchor; metadata records source, bounds and scale. No existing atlas was edited.

Yuri uses 256×256 canvases, Gosfer 320×320, props/armor/vehicles 384×384,
fortress ground 800×2400, and the looping night road 800×1600. The separate
lateral-prone and utility sheets are scaled consistently to the main Yuri bank.

## Gameplay study

Opened and visually inspected [Mercs](https://www.youtube.com/watch?v=-tgkTCk-MFo&t=200s),
[Demolition Man's Museum level](https://www.youtube.com/watch?v=H7hg8JXUMB4&t=275s),
and Contra's [Base 1](https://www.youtube.com/watch?v=2mWZlNOzdv8&t=84s) and
[Base 2](https://www.youtube.com/watch?v=2mWZlNOzdv8&t=254s).
The design takes independent movement/fire and large readable actors from the
first two, and fortified shooting lanes and destructible control targets from
Contra. Shock Troopers supplied the user's character-detail target. Assets were
newly generated from BOF identity references; no game footage was extracted.

## Verification

- 27 expansion JavaScript modules and `assets/game.js`: syntax checks pass.
- Required base suite: **8,700 passes, zero errors, final summary, exit 0**.
- New native Chromium assault probe: **38/38**, zero browser/asset errors.
- Native keyboard/mouse fortress route: **20/20**. Guards were removed to isolate
  navigation; traversal uses actual inputs and relays take ordinary rifle fire.
- Existing native controller/Retina/Warrior probe: **40/40**.
- All 384 core Yuri frames inspected through the game's own ART renderer.
  Gameplay, cover, boss entrance/fight and pursuit screenshots also inspected.
- Gosfer defeated with actual Retina-aimed rifle shots in a protected fixture.
- Normal-hull 150-second pursuit bot: **23 hull remaining, 63 kills, 28 rocket
  interceptions, zero restarts**, targeting every 250 ms.

Controller tests inject Gamepad API reports; a physical controller was not
available to press. Protected fixtures and the aiming bot establish mechanics
and feasibility, not a human difficulty assessment.

Reproduce with:

```powershell
node --check assets/game.js
node _BUILD_SOURCE/test_fl.js
python expansion/topdown/_research/build_assault_1013.py
python expansion/topdown/_research/probe_assault_1013.py
python expansion/topdown/_research/probe_assault_route_1013.py
python expansion/topdown/_research/probe_retina_1012.py
```

Full captures remain in ignored `_shots/overdrive_assault_1013/`. Curated evidence
is in `docs/qa/overdrive_assault_1013.json` and `docs/previews/overdrive_assault_1013/`.
