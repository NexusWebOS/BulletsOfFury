# Bullets of Fury: Overdrive — Ground Operations

Playable **standalone expansion prototype** at `expansion/topdown/index.html`.
The base-game flight campaign is a separate entry point. No base atlas edits.

From the repository root:

Run `PLAY_OVERDRIVE.bat` to start the local server and open Edge/Chrome in
fullscreen by default. The generated Fullscreen/Windowed button or Alt+Enter
toggles native fullscreen; Escape exits it. Direct browser launches request
fullscreen on Start. For a windowed preview, add `?fullscreen=0`.

```powershell
python -m http.server 8778 --bind 127.0.0.1
```

Open [Ground Operations](http://127.0.0.1:8778/expansion/topdown/index.html).
Start opens the BOF/Overdrive intro and the original-style title menu. New Game
then opens difficulty, the original pilot screen with **two rows of six pilots**,
and the first campaign briefing. Continue and the new Overdrive password menu
restore campaign progress. The campaign advances **Level 2 → Level 3 → Level 4
→ Level 5 → Level 6 → Level 7**. There is no mission picker at startup.

Current build: **`overdrive1015-yuri32-r1`**. New straight-up firing, flat
walk/run slide transitions and object-free cover/pop-out/return clips are in
`art/yuri32/preview.html`; notes: `docs/OVERDRIVE_YURI32_1015.md`. The latest pass adds smooth slide
turns, completed rolls and front-facing fire straight into the floor. Review:
`art/yuri31/preview.html`; notes: `docs/OVERDRIVE_YURI31_1015.md`. Yuri’s new movement and aiming
frames now match his established red jacket and mohawk. Level 3 now ends in the
elevator, drone chute and side-view self-destruct escape. **Level 4 is Prism
Bastion**, the rear-view cover shooter with eight core-gated rooms and the
Prism Heart / Helios boss. Machinists, Desert Breaker and Convoy follow as
levels 5, 6 and 7; saved-password slots remain compatible. Vehicles, infantry, bosses, camera and projectiles
now use a fixed simulation clock with interpolated display motion.

**Escape29:** One-hit Yuri/lives-only HUD for stages3/4, tougher Gosfer, wall
vaults, roll landings, crouch/crawl/peek cover, fast travelling base projectiles,
wall impact sound/shake, new aiming and slide art. Full notes and controls:
`docs/OVERDRIVE_ESCAPE29_1015.md`. Animation review: `art/escape29/preview.html`.
53native checks plus base suite pass. Existing enemy/art banks retained.
Older pass notes below use internal stage7, now visible level4. The newer
one-hit rules hide the player health strip in stages3/4.

**Yuri upward side aim:** New cross-step and side-fire motion for moving north
while aiming left/right:16movement and12firing frames per facing. Gun effects
follow measured barrel points; foot motion stops at walls. Review at
`art/yuri28/preview.html`; source and30native checks: `docs/OVERDRIVE_YURI28_1015.md`.

**HUD27 polish:** Health now fills continuously. A newly generated Overdrive
bitmap font draws the player HUD, with centered ammo/action rows and a dedicated
equipped-gun inset. Stage7 room scenery is25%darker while HUD/ordnance remain
readable. Source and37native checks: `docs/OVERDRIVE_HUD27_1015.md`.

**Genesis corner HUD:** Stages3/7 now show the pilot face, lives and generated
health gauge at top left; ammo and current action at top right; score and saved
high score in the top center. The bottom strip is removed. Details and native
verification: `docs/OVERDRIVE_CORNER26_1015.md`.

**PixelLab pass:** Stages3/7 now use new rifle/heavy infantry, with rocket and
laser classes in stage7, real16-frame walks and dedicated fire/crouch/fall
drawings. Separate gritty room/courtyard components and four matching HUD panels.
Review animations at `art/pixel25/preview.html`; provenance and QA:
`docs/OVERDRIVE_PIXEL25_1014.md`.

**Music:** BOF-BASE plays in levels 3 and 7. Rise of the Last Hope fades in
after Gosfer's entrance and returns after his dialogue/transformation; level 7
starts it at the room-8 reactor reveal and keeps it through Helios. Original WAVs
and verification: `docs/OVERDRIVE_MUSIC23_1014.md`.

**Level 7 cover:** Yuri stays visible on our side of the wall, with enemies
beyond it. Idle returns to cover; Fire peeks, Cover + Fire blindfires, and
Retina raises him for free aim. Room textures are brighter and remain crisp.
Details: `docs/OVERDRIVE_COVER24_1014.md`.

**Prone: F or Mode + X.** Move while prone to crawl. At cover, fire to peek;
hold Retina + fire for protected blindfire (Genesis: Mode + Z). Straight
concrete bunkers cannot be destroyed. Gosfer has a visible filling health bar.
All six level passwords are pinned in the Password menu.

**Controller settings:** Choose **M30 2.4G**, **Genesis6** or **Standard** in
Options → Controller Preset. Bind individual controls or use Learn All Buttons,
release between inputs, then Apply. Genesis learning omits shoulders; M30 includes
L/R. Real M30 diagrams retain X/Y/Z above A/B/C. Fast keyboard taps and controller
presses now bind without also navigating the menu. Cancel restores the old setup.

**Level 7:** Eight rooms, each with a required door core and mounted corner turrets.
A fires, Y throws grenades, X toggles crouch, C/Mode takes cover and Z+D-pad free
aims. B+left/right twists and fires sideways. Elites launch finite-ammo shotgun,
laser and minigun upgrades. Clear each room to blast the rear wall, hop over cover,
walk as the corridor scrolls past, enter black and fade into fresh cover.
Room8's spinning-laser Master Prism Core fractures/shatters its glass, flashes
white and releases the fully animated Helios. Gosfer and Helios each get64 new
frames; the new art pack adds191 unique PNGs. Combat camera scale stays fixed.

See [the M30/eight-room/boss rebuild and verified evidence](../../docs/OVERDRIVE_BASTION18_1014.md).

See [the current combat overhaul guide](../../docs/OVERDRIVE_COMBAT_1013.md),
[cover and animation details](../../docs/OVERDRIVE_COVER_MOTION_1013.md),
[desert and pursuit details](../../docs/OVERDRIVE_DESERT_1013.md), and
[frame timing and menus](../../docs/OVERDRIVE_FRONTEND_PACING_1013.md).

The dated notes below retain the earlier implementation history.

Yuri's movement revision adds 316 authored walk, run-and-fire and crawl frames
across eight directions. Distance drives the animation, firing preserves the
step phase, and blocked movement settles the feet. The viewer compares the old
and new loops at actual game speed. Native checks: 26 movement/art plus 38
existing assault checks pass; base regression: 8,700 passes, zero errors.

Insanity unlocks after completing the Overdrive campaign and stays unlocked.
Options reuses the original BOF panel, four volume strips, key caps, scrolling,
controller settings and Apply/Cancel controls, wired to Overdrive bindings.
Help includes six-button tank, standard-pad tank and on-foot controls. B is Back;
Backspace only deletes text. The original “Bullets of Fury!” call now plays
first, followed by Mike's Overdrive recording with reverb, echo and matched
loudness. Title music waits for the final echo tail. Both calls use the saved
Voice/Master mix and can be skipped with Start or B. The original WAV is preserved.
See [the current menu/controls/art guide](../../docs/OVERDRIVE_MENU_1011.md).

Iron Infiltration uses the closer **640 × 480** gameplay field in fullscreen.
The Warrior rolls into the arena from above with the normal 1:1 tracking camera. An authored Overdrive dossier slides in with a 360-degree turntable,
actual armor/HP/target data, attack profile and Mike's warning. D-pad rotates
and selects parts; A inspects, B returns to overview, Start continues after the
scan. The card slides out and camera/control return to normal. Boss music begins
then. See [the introduction and verification](../../docs/OVERDRIVE_BOSS_INTRO_1011.md).

## Missions

| Mission | Playable content |
| --- | --- |
| Level 2 — Iron Infiltration | Smooth Fury tank movement, independent turret aim, sideways strafe, destructible buildings, concrete cover, charged cannon recoil, tank homing missiles. **The Warrior** has an original helmet/torso, two arms and a chassis, lateral broadside movement, bullet/laser/missile volleys and a warned cover-breaking ram. No boss charge orbs. |
| Level 3 — Fortress / Dead Signal | Large Yuri with smooth sidesteps, rear knockback, prone/crawl, indestructible straight cover, anchored pop-out and back-to-wall blindfire. Troops enter from the north. Three relay objectives lead to **Gosfer**, with a filling health bar and art-aligned hitboxes. |
| Level 4 — Machinists: Rebel Siege | New coastal rail/factory battlefield and rocket, rail and siege tank roles. Wren/Foundry, Rolf/Vector and Chaz/Redline are hostile tanks. Select **Hotwire, Phoenix or Niel** as your teammate. The squad attacks both of you; your teammate follows, fires and regroups after being disabled. |
| Level 5 — Desert Breaker | Open desert, four mixed armor/air waves, acceleration and continuous steering, telegraphed committed rams, Retina locks, guided missiles and supplies. Replaces Museum of Violence in the active campaign. |
| Level 6 — Night Run / Hull Zero | Hotwire drives a green Silverado through night hills. Freely aim its bed turret through a 150-second pursuit after jet searchlights expose it. Intercept rockets and destroy jets, gun trucks and running robots; red elites arrive late. 100-point HULL bar, whole-run restart on destruction, no boss/miniboss. |
| Level 7 — Prism Bastion | Rear-view cover shooter: sidestep, duck, stand, Retina free aim, grenades, minigunners, rifle/laser/rocket troops, corner turrets and animated cores. Prism Heart transforms through a white flash into Helios, with an orange-then-fire-red two-layer gauge, running attacks, volleys, lightning and a warned geyser slam. |

Levels 2 and 4 now include **Jackal, Lancer, Manticore and Bastion** armor.

Machinist tracks, hulls, turrets and rear modules use the existing calibrated
layer canvases. Track phases follow travel distance. Breaking a part cancels its
owned attacks, launches that exact opaque rotating part, and gives a recovery
opening. Wren has a timed Bastion damage barrier, Rolf a three-lane laser volley,
and Chaz missiles plus a cover-breaking breach. Destroyed tracks immobilize a tank.

## Controls — keyboard, mouse, six-button and standard pads

October 12: original BOF Retina tap/cycle, travelling seeker and pilot-colored
locks return. L + D-pad aims while cruising; A fires along that aim. A and Start
confirm menus and dossier Continue. The Warrior is 15% smaller, with matching
mounts/collisions/breakoffs, and framed text fits its boxes. **187 native checks
pass; base suite 8,700/0, exit 0.** See
[Retina and shoulder correction](../../docs/OVERDRIVE_RETINA_1012.md).
That published build was `overdrive1012-retina-r1`. The October 13 build adds
**38 assault + 20 route + 40 existing Retina/controller checks = 98/98**, with
zero browser errors. The required base suite passes **8,700/0, exit 0**.

October 11 input correction: saved D-pad bindings now override defaults, mouse
aim works while a keyboard/controller drives, and holding Retina after the boss
introduction cannot block other fire inputs. All eight firing directions are
verified. See [input corrections and QA](../../docs/OVERDRIVE_INPUT_1011.md).
Reload the `overdrive1011-input-r1` build to use the correction.

### October 11 — approved chip sound pass

The standalone expansion now imports Mike's **81 approved ColeForge chip cues**.
Tank engines, treads and turret movement have action-owned loops. Cannon, shell
impact, missiles, Warrior volleys, Bastion shields, infantry, alarms, concrete,
buildings, crates, pickups and menu actions use their contextual sounds. Loops
stop on action/scene exit, death and focus loss. The supplied Warrior music
retains its fight.

The wider approved bank is registered for later expansion systems. A
pitch-preserving firewall timing hook is ready; there is no travelling firewall
attack in this ground prototype yet. See the
[sound mappings and verification](../../docs/OVERDRIVE_CHIP_AUDIO_1011.md).
Current correction: **55/55 restored frontend + 44/44 sound = 99/99 native checks**,
zero browser errors. The required base suite reaches its final summary with **8,700 passes,
zero errors, exit 0**. Older results remain in their dated QA records. Local
changes are uncommitted and unpushed.

Boss fights keep the normal **1:1 camera scale**, with the camera following the
player throughout. The Warrior camera also frames its large authored modules
while keeping the player's escape route visible. Tank weapon pickups equip
immediately and replace the current gun. On foot, the rifle remains available
and up to three upgrade guns can be cycled with Tab / wheel / Mode+B.

| Input | Tank | On foot |
| --- | --- | --- |
| WASD / arrows / D-pad | Drive | Move |
| Mouse / Q-E | Aim independently | Aim independently |
| Left mouse / J | Fire | Fire |
| Right mouse / H / Space | Hold charge, release cannon | Roll |
| K | Uncharged cannon | Jump |
| Shift / L | Hull lock / strafe | Hold crouch / cover |
| R | Hold speed boost | Jump |
| F | Cruise / free turret aim | Toggle prone |
| Controller L / R shoulder | Hold cruise + D-pad aim / tap-cycle Retina | Hold cover / tap-cycle Retina |
| U | Smoke | Grenade |
| I | Tap-cycle Retina; hold to maintain | Tap-cycle Retina |
| Tab / wheel | No weapon swap | Cycle rifle / upgrade guns |
| Enter / Start | Pause / confirm | Pause / confirm |
| B / Escape in menus | Back | Back |

Six-button controller layout follows the physical two rows:

| Top row | X: fire north | Y: fire west | Z: Retina (tank) / grenade (foot) |
| --- | --- | --- | --- |
| Bottom row | A: fire south | B: fire east | C: hold/release cannon (tank) / roll (foot) |

The D-pad moves independently of fire direction. Hold two adjacent firing buttons
for diagonals. Opposing directions cancel. No analog stick is required.
Tank **Mode** holds the hull for strafe; **Mode + Z** throws smoke. On foot,
**Mode + A** jumps, **Mode + X** toggles prone, **Mode + Y** taps a wall.
In menus A/Start confirms and B/Mode goes back. F1 opens Help.

Tank **Mode + C** holds the speed boost. While holding that combination, the
four directional firing buttons still aim and fire independently. Normal C
still charges/releases the cannon. The boost reaches 2.05 times normal speed,
lasts 2.25 seconds from a full meter, and refills in 3.4 seconds. It costs no
energy when stationary. Release after exhausting the meter to boost again.
Charge, hedge slowdown, collisions and physical recoil still apply.

**F2 or Mode + Start** opens controller setup. Release all inputs, then follow the
prompts for four D-pad directions, A/B/C/X/Y/Z, Mode, Start and L/R shoulders.
The standard-pad preset learns four face buttons, Mode, Start, L/R and boost. Button mappings
persist by controller ID. The M30 2.4g Genesis receiver now auto-detects its
raw button layout separately from standardized/XInput reports. Physical A
fires in Prism Bastion; Y throws grenades, X ducks, and Z controls free aim.
Untouched generic presets upgrade automatically; learned bindings remain yours.
If using a different receiver, Learn All Buttons records its actual layout.

Night Run now uses D-pad steering, independent face-button directional fire,
L + D-pad free aim, and R / Z Retina. Hotwire maintains forward road speed.
The gun and projectile origin stay attached to the turning truck bed.

Raw receiver mapping reference:
[Libretro M30 2.4g Windows profile](https://github.com/libretro/retroarch-joypad-autoconfig/blob/master/dinput/8Bitdo_M30_24G.cfg).

### Retina

On foot, R shoulder / I locks without requiring missiles. The selected rifle or
upgrade gun shoots the acquired target. Cover locks use its available peek lane.
The following missile behavior applies to tanks:

Tap I / controller Z or R shoulder to acquire a visible hostile; tap again to
cycle targets. The original BOF seeker travels and shrinks over 0.45 seconds.
Locks last five seconds after release; holding Retina maintains them. Targets
must stay in the visible playfield with no solid cover blocking the route.
The marker follows the exact unit or Warrior/Machinist module. While locked,
tap/release the cannon (C on controller, K or charge on keyboard/mouse) to launch
a guided missile, or hold Retina + A to fire it with the primary gun. Charging
increases its damage. Start with six missiles; smoke supplies add three, up to
twelve. Empty racks cannot launch free missiles. Destroyed modules invalidate
their locks. Launched missiles never retarget other enemies.

## Art ownership and rebuilding

### October 13 — infantry, fortress and night pursuit

`_research/build_assault_1013.py` owns 518 even-sized exports and their loose
manifests. Original generated sources, exact prompts, crop/scale audit and
Yuri identity references are preserved in `art/assault_1013/`. See the
[implementation guide](../../docs/OVERDRIVE_ASSAULT_1013.md) for all current
controls, art ownership, test fixtures and gameplay reference videos.

### October 11 — new Warrior, menus, supplied music and tank boost (historical)

The active navy/silver HK-inspired Warrior uses `art/warrior_mk2_1011/`:
640 × 512 hull/damage/wreck canvases and 512 × 512 torso/arm canvases. All have
registered physical pivots; matching chassis states share one scale. The
chassis canvas draws at 332.8 world pixels and the assembled front spans about
437.6 pixels. The arena becomes 480 × 480 at the same 1:1 world zoom, keeping the
warrior helmet, large chassis, player and HUD visible together. Bullet/laser/
missile volleys, lateral lower-body turning, the cover-breaking ram and exact
rotating module breakoffs remain. The old olive bank is preserved.

Mike's supplied `BOF-O-BOSS1.wav` is retained in `audio/source/`; its 122.76-second
stereo MP3 loops for this fight. Title and pilot selection restore the original
Title/PilotSelect tracks. Engine cue gain is reduced from .22 to .08, with a
separate Options slider. The other ground encounter music remains in use.

Forty-two newly generated menu frames include twelve slim buttons, five
difficulty plates featuring Hotwire/Phoenix/Niel, extra settings plates, two
controller diagrams, sixteen Overdrive badges and four general-game badges.
Original faces, aircraft, full bodies, font and pad prompts are reused.

```powershell
python expansion/topdown/_research/build_menu_art_1011.py
python expansion/topdown/_research/export_original_pilot_1011.py
python expansion/topdown/_research/build_boss_audio_1011.py
python expansion/topdown/_research/build_original_options_1011.py
python expansion/topdown/_research/build_startup_audio_1011.py
python expansion/topdown/_research/probe_restored_frontend_1011.py
python expansion/topdown/_research/probe_warrior_1011.py
```

Current [implementation and verification](../../docs/OVERDRIVE_MENU_1011.md).
Older [Warrior measurements](../../docs/OVERDRIVE_WARRIOR_1011.md) and masters
remain available. The new loose manifests belong to `build_menu_art_1011.py`.

- `art/ground_1008/source/`: generated Warrior, compound/plaza terrain, buildings,
  concrete debris/dust, charge states, tank missiles and colored laser masters.
- `art/ground_1008/prompts.json`: original generation prompts and provenance.
- `art/campaign_1008/`: generated rebel terrain, gate-free Miami terrain edit,
  normalized pilot bodies, Niel tank paint, and registered references to the
  existing `ground`, `onfoot`, and `windstorm_machinists` packs.
- `art/campaign_1008/generation-prompts.json`: full terrain generation/edit prompts.

```powershell
python expansion/topdown/_research/build_ground_1008.py
python expansion/topdown/_research/build_campaign_1008.py
python expansion/topdown/_research/build_museum_1009.py      # Level 5 plate + exhibits
python expansion/topdown/_research/check_museum_1009.py      # Level 5 collision overlay
```

These builders own loose expansion exports and their manifests. They preserve
source PNGs, recorded pivots and alpha; neither repacks the game's atlas.

## Verified October 8, 2026

- All expansion JS passes `node --check`.
- Native Chromium Warrior probe: **23/23**.
- Native Chromium campaign probe: **29/29**.
- Both probes report zero page/console/asset errors, and their screenshots were inspected.
- Base gate: `node --check assets/game.js`; full `_BUILD_SOURCE/test_fl.js`
  completed with **7,952 passing assertions, zero errors, exit 0** and the final
  `FALVA/LIZZIE BUILD OK` summary.

Run native probes from the repository root:

```powershell
python expansion/topdown/_research/probe_ground_1008.py
python expansion/topdown/_research/probe_campaign_1008.py
python expansion/topdown/_research/probe_museum_1009.py      # Level 5: 28 checks
```

Evidence lives in ignored `_shots/ground_1008/`. Protected fixtures isolate
combat, rendering and transitions; these results do not establish unassisted
clear rates or final difficulty balance. Existing generated action and track
phases retain some pose/detail drift. The Fusion weapon fires piercing pulses;
the supplied directional actions remain candidates for further animation polish.
No flight-campaign/save integration or publication is implied by this prototype.

## October 8 control revision

Native Chromium checks: 29/29 pilot/controls/Retina, 23/23 tank/Warrior and 29/29
infantry/Machinists. Screenshots and detailed results are in the ignored
`_shots/ground_controls_1008/` and `_shots/ground_1008/` folders. Controller checks
use synthetic browser Gamepad reports; a physical M30 was not connected.

The required base-game suite currently exits 1 with two HUD-fit assertions:
“the rails are given room in windowed mode and none in fullscreen” and “the fit
accounts for the HUD and the divider.” Expansion checks pass; this revision does
not edit the base runtime or its HUD. These failures are recorded separately from
the earlier publication's green verification.

Run the focused probe with:

```powershell
python expansion/topdown/_research/probe_controls_1008.py
```

## October 8 infantry repair

Miami pool collision now follows the L-shaped water and the central planter,
leaving the surrounding paved route walkable. Foot movement resolves crate and
world collision together. The fortress gate still requires its sentries defeated.

All twelve pilots have materialized west-running frames and matching armor
palettes for prone, roll, grenade and death actions. Derived exports retain the
source alpha and authored pivots. The body aims with its baked-in weapon, and
bullets originate from that pose's transformed muzzle; loose pickup weapon icons
are no longer drawn over the pilot. Roll actions preserve the starting stance.
Combined infantry vision cones are capped at 30 percent opacity.

Native Chromium repair probe: **17/17**; campaign **29/29**, controls **29/29**,
tank **23/23**, for **98/98** expansion checks. The route probe walks with real
keyboard inputs from the beach through the pool area to the fortress exit;
incidental enemies are disabled for this collision test. It also presses prone,
crawls west and stands while moving for every pilot, checks both roll recoveries,
and verifies one rendered gun and matching shot origins. All 432 recolored action
frames preserve source alpha. Browser/console/asset errors: zero. Screenshots
were inspected in `_shots/infantry_repair_1008/`; portable results are in
`_research/infantry_1008_verification.json`. The base suite retains the two HUD-fit
failures documented above. This does not establish unassisted mission balance.

```powershell
python expansion/topdown/_research/probe_infantry_1008.py
```

## Pinned level passwords — October 13

The Password menu displays selectable shortcuts for every playable stage.
Click a pinned row or select it with D-pad and A/Start to load its password and
choose a pilot before the matching briefing. Codes use Yuri / Normal / Hotwire;
the pilot can be changed on the following screen. D-pad left/right moves between
the pins and manual keypad. Manual typing, checksums and the Insanity unlock
gate remain supported.

| Level | Stage | Password |
| --- | --- | --- |
| 2 | Iron Infiltration | `OD-237A-5JXL` |
| 3 | Fortress / Dead Signal | `OD-237B-5JXM` |
| 4 | Machinists / Rebel Siege | `OD-237C-5JXN` |
| 5 | Desert Breaker | `OD-237D-5JXP` |
| 6 | Night Run / Hull Zero | `OD-237E-5JXQ` |
| 7 | Prism Bastion | `OD-237F-5JXR` |

Native menu probe: 26/26 passing checks, zero browser/console/asset errors,
including actual pointer launches into all five briefings, synthetic controller
navigation, manual text entry and both desktop/narrow screenshots inspected.
Results: `docs/qa/overdrive_password_pins_1013.json`. Reproduce with
`python expansion/topdown/_research/probe_password_pins_1013.py`.
Previous local password build: `overdrive1013-password-pins-r1`. Superseded by the combat overhaul above.


## 2026-10-14 — Gritty base and ground animation pass

Current local build: `overdrive1014-bastion19-r1`. See [pass notes](../../docs/OVERDRIVE_BASTION19_1014.md) for the new room/reactor/boss/player art, buffered prone controls, authored motion and verified routes.


October14 Gosfer encounter pass: build overdrive1014-gosfer20-r1. Three linked barriers, portrait dialogue/fear/transformation, fast duel,5s rolls/roll-to-prone, graphical HUD and new whole-body motion. See docs/OVERDRIVE_GOSFER20_1014.md.


## October 14 — Grid21 Three.js base

Separate gritty component assets and real corridor geometry with existing 2D sprite flats.
See [pass notes](../../docs/OVERDRIVE_GRID21_1014.md) and [verification](../../docs/qa/overdrive_grid21_1014.json).


## October 14 — Lighting22 cover and projectiles

Dynamic corridor lighting and shadows, solid walls in front of Yuri, brighter
projectile heads/trails and larger top-down on-foot ordnance.
See [pass notes](../../docs/OVERDRIVE_LIGHTING22_1014.md) and [verification](../../docs/qa/overdrive_lighting22_1014.json).
