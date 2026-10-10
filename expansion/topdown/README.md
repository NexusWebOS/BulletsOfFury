# Bullets of Fury: Overdrive — Ground Operations

Playable **standalone expansion prototype** at `expansion/topdown/index.html`.
The base-game flight campaign is a separate entry point. No base atlas edits.

From the repository root:

```powershell
python -m http.server 8778 --bind 127.0.0.1
```

Open [Ground Operations](http://127.0.0.1:8778/expansion/topdown/index.html).
Boot opens the existing pilot-selection presentation with framed avatars and full-body
art, expanded to **two rows of six** including Hotwire, Phoenix and Niel. D-pad /
arrows select a pilot; Start confirms, then choose a mission. B returns to pilot
selection. Level 4 briefing up/down selects the companion. Start on
results advances Level 2 → Level 3 → Level 4. Each stage is also directly selectable.

## Missions

| Mission | Playable content |
| --- | --- |
| Level 2 — Iron Infiltration | Smooth Fury tank movement, independent turret aim, sideways strafe, destructible buildings, concrete cover, charged cannon recoil, tank homing missiles. **The Warrior** has an original helmet/torso, two arms and a chassis, lateral broadside movement, bullet/laser/missile volleys and a warned cover-breaking ram. No boss charge orbs. |
| Level 3 — Boots on the Ground *(hidden from the menu since 2026-10-09; kept intact)* | Authored Miami beach → palm park → fortress route. One damaging hit consumes a life. Six guns with finite magazines/reserves, manual reload, prone/crawl, vulnerable roll, committed grenade throw, stealth, tall-stack occlusion and fixed weapon-box drops. Defeat three sentries, then walk through the opened north gate. |
| Level 4 — Machinists: Rebel Siege | New coastal rail/factory battlefield and rocket, rail and siege tank roles. Wren/Foundry, Rolf/Vector and Chaz/Redline are hostile tanks. Select **Hotwire, Phoenix or Niel** as your teammate. The squad attacks both of you; your teammate follows, fires and regroups after being disabled. |
| Level 5 — Museum of Violence | Mercs × Demolition Man × Contra Hard Corps × MGS on foot. Push-scroll that never scrolls back; A+B / G Mega Crash (3 bombs); POW; a boardable exhibit Fury tank that ejects you alive. Smash-TV Hall of Arms that locks for three waves; 31 shootable exhibits (23 with fixed contents); five hostages (do not shoot them). Four A–D gun slots, death loses only the gun in hand. Three routes: stealth gallery (laser tripwires, cameras), prone-only duct, armour hall. CQC from behind, found bodies, alarm panels as the only reinforcement source. Boss THE EXHIBIT: three Hard Corps forms. See [docs/MUSEUM_STUDY_1009.md](../../docs/MUSEUM_STUDY_1009.md). |

Machinist tracks, hulls, turrets and rear modules use the existing calibrated
layer canvases. Track phases follow travel distance. Breaking a part cancels its
owned attacks, launches that exact opaque rotating part, and gives a recovery
opening. Wren has a timed Bastion damage barrier, Rolf a three-lane laser volley,
and Chaz missiles plus a cover-breaking breach. Destroyed tracks immobilize a tank.

## Controls — keyboard, mouse and six-button pads

Boss fights keep the normal **1:1 camera scale**, with the camera following the
player throughout. Weapon pickups equip immediately and replace the current gun;
there is no stored weapon inventory or manual swap button, including mouse wheel.

| Input | Tank | On foot |
| --- | --- | --- |
| WASD / arrows / D-pad | Drive | Move |
| Mouse / Q-E | Aim independently | Aim independently |
| Left mouse / J | Fire | Fire |
| Right mouse / H / Space | Hold charge, release cannon | Roll |
| K | Uncharged cannon | Reload |
| Shift / L | Hull lock / strafe | Toggle prone |
| U | Smoke | Grenade |
| I | Hold Retina scan | No weapon swap |
| Enter / Start | Pause / confirm | Pause / confirm |
| B / Escape in menus | Back | Back |

Six-button controller layout follows the physical two rows:

| Top row | X: fire north | Y: fire west | Z: Retina (tank) / grenade (foot) |
| --- | --- | --- | --- |
| Bottom row | A: fire south | B: fire east | C: hold/release cannon (tank) / roll (foot) |

The D-pad moves independently of fire direction. Hold two adjacent firing buttons
for diagonals. Opposing directions cancel. No analog stick is required.
Tank **Mode** holds the hull for strafe; **Mode + Z** throws smoke. On foot,
**Mode + A** reloads, **Mode + X** toggles prone, **Mode + Y** taps a wall.
In menus A/Start confirms and B/Mode goes back. F1 opens Help.

**F2 or Mode + Start** opens controller setup. Release all inputs, then follow the
prompts for four D-pad directions, A/B/C/X/Y/Z, Mode and Start. Button mappings
persist by controller ID. The default supports an M30 Windows X-input report;
setup supports alternative button mappings and D-pad axes. For a hat-only report,
select the controller's X-input / D-pad-as-left-stick mode. See the official
[8BitDo M30 manual](https://download.8bitdo.com/Manual/Controller/M30/M30_Manual.pdf).

### Retina

Hold I / controller Z to scan a visible hostile in the turret's forward cone.
Acquisition takes 0.45 seconds, requires clear line of sight, and is limited to
320 world pixels and the visible playfield. The marker follows the exact unit or
individual Warrior/Machinist module. While locked, tap/release the cannon (C on
controller, K or charge on keyboard/mouse) to launch a guided missile. Charging
still increases its damage. Start with six missiles; smoke supply boxes add three
up to twelve. An empty rack cannot launch a free missile. Releasing Retina clears
the lock; destroyed modules invalidate it. Missiles never retarget other enemies.

## Art ownership and rebuilding

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
