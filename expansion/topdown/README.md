# Bullets of Fury: Overdrive — Ground Operations

Playable **standalone expansion prototype** at `expansion/topdown/index.html`.
The base-game flight campaign is a separate entry point. No base atlas edits.

From the repository root:

```powershell
python -m http.server 8778 --bind 127.0.0.1
```

Open [Ground Operations](http://127.0.0.1:8778/expansion/topdown/index.html).
Choose a mission with the D-pad / arrows, then Start. Left/right selects the
player pilot in the briefing; Level 4 up/down selects the companion. Start on
results advances Level 2 → Level 3 → Level 4. Each stage is also directly selectable.

## Missions

| Mission | Playable content |
| --- | --- |
| Level 2 — Iron Infiltration | Smooth Fury tank movement, independent turret aim, sideways strafe, destructible buildings, concrete cover, charged cannon recoil, tank homing missiles. **The Warrior** has an original helmet/torso, two arms and a chassis, lateral broadside movement, bullet/laser/missile volleys and a warned cover-breaking ram. No boss charge orbs. |
| Level 3 — Boots on the Ground | Authored Miami beach → palm park → fortress route. One damaging hit consumes a life. Six guns with finite magazines/reserves, manual reload, prone/crawl, vulnerable roll, committed grenade throw, stealth, tall-stack occlusion and fixed weapon-box drops. Defeat three sentries, then walk through the opened north gate. |
| Level 4 — Machinists: Rebel Siege | New coastal rail/factory battlefield and rocket, rail and siege tank roles. Wren/Foundry, Rolf/Vector and Chaz/Redline are hostile tanks. Select **Hotwire, Phoenix or Niel** as your teammate. The squad attacks both of you; your teammate follows, fires and regroups after being disabled. |

Machinist tracks, hulls, turrets and rear modules use the existing calibrated
layer canvases. Track phases follow travel distance. Breaking a part cancels its
owned attacks, launches that exact opaque rotating part, and gives a recovery
opening. Wren has a timed Bastion damage barrier, Rolf a three-lane laser volley,
and Chaz missiles plus a cover-breaking breach. Destroyed tracks immobilize a tank.

## Keyboard and mouse

Full keyboard/gamepad mapping is available with **F1** in the build.

| Action | Tank | On foot |
| --- | --- | --- |
| Move | WASD / arrows | WASD / arrows |
| Aim | Mouse, right stick, or Q/E | Mouse, right stick, or Q/E |
| Fire | Left mouse / J | Left mouse / J |
| Secondary | K cannon | K / R reload |
| C | Shift / L strafe with hull locked | Shift / F toggle prone |
| X | Hold right mouse / H / Space; release charged cannon | H / Space roll, without invulnerability |
| Y | U smoke | U grenade |
| Z | I / wheel swap weapon | I / wheel swap weapon |
| Start | Enter pause / confirm | Enter pause / confirm |
| B in menus | B / Escape back; controller B | B / Escape back; controller B |

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
```

Evidence lives in ignored `_shots/ground_1008/`. Protected fixtures isolate
combat, rendering and transitions; these results do not establish unassisted
clear rates or final difficulty balance. Existing generated action and track
phases retain some pose/detail drift. The Fusion weapon fires piercing pulses;
the supplied directional actions remain candidates for further animation polish.
No flight-campaign/save integration or publication is implied by this prototype.
