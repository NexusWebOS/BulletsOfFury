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
→ Level 5 → Level 6**. There is no mission picker at startup.

Current build: **`overdrive1013-yuri-motion-r1`**. Yuri has new large infantry art,
the fortress now leads to Gosfer, four new enemy tank families join the tank
stages, and Hotwire drives the new Silverado turret pursuit. See
[the October 13 guide, controls and passwords](../../docs/OVERDRIVE_ASSAULT_1013.md)
and [Yuri's animation viewer](art/assault_1013/review.html).

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
The Warrior rolls into the arena from above with a tracking camera that pulls
back. An authored Overdrive dossier slides in with a 360-degree turntable,
actual armor/HP/target data, attack profile and Mike's warning. D-pad rotates
and selects parts; A inspects, B returns to overview, Start continues after the
scan. The card slides out and camera/control return to normal. Boss music begins
then. See [the introduction and verification](../../docs/OVERDRIVE_BOSS_INTRO_1011.md).

## Missions

| Mission | Playable content |
| --- | --- |
| Level 2 — Iron Infiltration | Smooth Fury tank movement, independent turret aim, sideways strafe, destructible buildings, concrete cover, charged cannon recoil, tank homing missiles. **The Warrior** has an original helmet/torso, two arms and a chassis, lateral broadside movement, bullet/laser/missile volleys and a warned cover-breaking ram. No boss charge orbs. |
| Level 3 — Fortress / Dead Signal | Large Yuri in eight directions, independent aim, jump/roll/crouch/prone, destructible cover and physical wall peeking. Unlimited assault rifle with finite upgrade guns. Destroy three red relays and enter the AI data center to face **Gosfer**, an alien rifleman with laser volleys and reflex dodges. |
| Level 4 — Machinists: Rebel Siege | New coastal rail/factory battlefield and rocket, rail and siege tank roles. Wren/Foundry, Rolf/Vector and Chaz/Redline are hostile tanks. Select **Hotwire, Phoenix or Niel** as your teammate. The squad attacks both of you; your teammate follows, fires and regroups after being disabled. |
| Level 5 — Museum of Violence | Mercs × Demolition Man × Contra Hard Corps × MGS on foot. Push-scroll that never scrolls back; A+B / G Mega Crash (3 bombs); POW; a boardable exhibit Fury tank that ejects you alive. Smash-TV Hall of Arms that locks for three waves; 31 shootable exhibits (23 with fixed contents); five hostages (do not shoot them). Four A–D gun slots, death loses only the gun in hand. Three routes: stealth gallery (laser tripwires, cameras), prone-only duct, armour hall. CQC from behind, found bodies, alarm panels as the only reinforcement source. Boss THE EXHIBIT: three Hard Corps forms. See [docs/MUSEUM_STUDY_1009.md](../../docs/MUSEUM_STUDY_1009.md). |
| Level 6 — Night Run / Hull Zero | Hotwire drives a green Silverado through night hills. Freely aim its bed turret through a 150-second pursuit after jet searchlights expose it. Intercept rockets and destroy jets, gun trucks and running robots; red elites arrive late. 100-point HULL bar, whole-run restart on destruction, no boss/miniboss. |

Level 5 shares the new rifle/fallback rules and Yuri's new animation bank.
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
persist by controller ID. The default supports an M30 Windows X-input report;
setup supports alternative button mappings and D-pad axes. For a hat-only report,
select the controller's X-input / D-pad-as-left-stick mode. See the official
[8BitDo M30 manual](https://download.8bitdo.com/Manual/Controller/M30/M30_Manual.pdf).

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
