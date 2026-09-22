# Enemy burn effects — 2026-09-22

Replaced the floating single flame on burning enemies with an eight-frame,
transparent fire envelope wrapping the hull. The open center keeps the enemy
visible. Size follows its footprint, with bounded scale; animation uses a stable
per-enemy phase, and fades only as the burn expires. Dying enemies use their own
existing death effects.

Normal burns use the same `#ff6924` luminance-preserving palette mapping as the
player flamethrower. The generated source references both the current flame and
magma orb. Forged flamethrower burns retain the originating infusion palette and
matching ember colors even after changing weapons. Subsequent ordinary fire
resets that palette. Existing fire infusion, spread, geyser and column ignition
routes share the burn applicator. Damage tick rate and damage remain unchanged;
reignition extends an existing burn. Decker/flamethrower set-piece exclusions
remain intact. Stage-2 vents keep their existing art.

## Assets and reproducibility

- `assets/game/fx_burn_0922/source.png`: original generated master, eight cells.
- `burn_0.png` through `burn_7.png`: 128×128 frames with original transparency.
- `assets/game/fx_burn_0922/provenance.json`: full prompt and reference paths;
  generated through built-in image_gen.
- `_BUILD_SOURCE/build_enemy_burn_0922.py`: repeatable cell packaging, common
  anchors, nearest-neighbor scaling. No atlas changes.

## Verification

`_BUILD_SOURCE/probe_enemy_burn_0922.py` uses real Chromium and the game canvas:
actual flame collision, palette retention/reset, burn damage, set-piece exclusion,
expiry, all eight frames and four palette variants beside the weapon art.
Screenshots and results: `_shots/burn_0922/`.

The infusion suite's old source-string check now exercises actual fire infusion
ignition, including the stored palette.

Syntax and Chromium checks passed; no page or console errors. The full suite
completed with exit 1 and the same 75 existing failure names as the preceding
portrait/rebel pass, with no new failures.
