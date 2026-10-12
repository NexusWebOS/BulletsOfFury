# Overdrive road and Warrior sizing — October 11, 2026

> Historical checkpoint: Mike rejected this 800 × 600 view as too distant.
> [The current 640 × 480 build and introduction](OVERDRIVE_BOSS_INTRO_1011.md)
> supersede it. This record and its original measurements remain preserved.

Mike reported that the arena shrank and the large boss was cut off. This corrects
presentation and framing in the standalone `expansion/topdown/index.html` build.
Current changes are local and uncommitted.

## Reproduced fault

In a 1469 × 796 browser, the road displayed at 960 × 720. At boss entry the
logical field changed from 480 × 360 to 480 × 480; integer display rounding
dropped its CSS scale from 2 to 1, yielding a 480 × 480 arena. The Warrior's
sideways arms and a tank across the compound could not fit in that narrow field.

Native before captures and measurements are preserved under
`_shots/overdrive_sizing_1011/before_*` and `before.json`.

## Correction

- Iron Infiltration uses a fixed **800 × 600**, 4:3 field from initial deployment
  through The Warrior. Entry no longer changes the viewport or tank/HUD scale.
- Canvas CSS fitting uses all available height or width proportionally, retaining
  nearest-neighbor rendering and a whole-number backing scale. There is no
  integer threshold that suddenly halves the image.
- World zoom remains 1. Authored tank art, Warrior module scales, damage pivots,
  collision radii, muzzle mounts and detached-piece scales are retained.
- Warrior lateral limits measure the rotated authored bounds of all surviving
  modules, leaving an 18-pixel gutter. Broadside goals respect those extents;
  arm/helmet aim and sideways chassis rotation stay registered.
- The camera frames the duel with space for the tank and bottom HUD. The briefing
  and results keep their existing 480 × 360 compositions centered over the wider
  field. Other missions keep their existing 480 × 360 layouts.
- The original Options panel remains 480 × 512. Pilot/title/pause remain
  640 × 512. Their display fits proportionally with unchanged panel geometry,
  four volume strips, binding capture, button effects and navigation.
- Script cache stamp and the default fullscreen launch helper use
  `overdrive1011-sizing`. Refresh an existing browser tab to load this correction.

At 1469 × 796 the road and arena both display at **1056 × 792**, compared with
the former 960 × 720 → 480 × 480 jump. At 1920 × 1080 both use the same
approximately 1435 × 1076 presentation. Aspect ratio is preserved.

## Verification

| Check | Result |
| --- | --- |
| Required base syntax + full regression suite | 8,700 passing assertions, zero failures, final summary, exit 0 |
| New native sizing probe | 53/53, zero page/console/asset errors |
| Existing Warrior probe | 22/22, zero page/console/asset errors |
| Original frontend/controller probe | 55/55, zero page/console/asset/decode/playback errors |

**130 native checks pass.** Both supplied window sizes (1612 × 878 and
1469 × 796), 1920 × 1080, 1100 × 850 and a 520 × 650 narrow pane were checked.
Real keyboard driving crosses the arena trigger. Front and both sideways poses
show the whole boss and tank. All 100 sampled frames through live broadside,
laser, missile and ram phases kept both visible. Native fullscreen and mouse
world-coordinate aim pass. Existing boost/aim/fire, ram escape, module breakoffs,
music looping, death/results, menu sliders and binding capture pass.

Inspected native screenshots include approach, front/left/right Warrior poses,
fullscreen volleys/concrete wreckage, narrow Options and briefing, plus the
existing Warrior result and regenerated frontend/controller views. Frame
assertions are backed by actual art-key draw calls through the game's context.

```powershell
python expansion/topdown/_research/probe_sizing_1011.py
python expansion/topdown/_research/probe_warrior_1011.py
python expansion/topdown/_research/probe_restored_frontend_1011.py
node --check assets/game.js
node _BUILD_SOURCE/test_fl.js
```

Portable evidence: `docs/qa/overdrive_sizing_1011.json`. Captures and full logs:
ignored `_shots/overdrive_sizing_1011/`. Protected fixtures establish display and
encounter behavior; they do not establish unassisted campaign difficulty balance.
Controller reports are synthetic. No physical-pad claim or Git publication.
