# Regular FOV for all enemies — October 11, 2026

Mike rejected the small rectangular enemy warning bands and asked for the
game's regular FOV for all enemies. This supersedes the September 29 decision
to give ordinary enemies bands while bosses kept cones.

The shared warning path now paints the complete authored
`bmfx_fov_green_tall`, `bmfx_fov_yellow_tall` and `bmfx_fov_red_tall` plates.
The normal FOV painter owns the muzzle apex, curved far edge, progress colors,
pulse and rising highlight.

- Removed the ordinary-enemy rectangle substitution from
  `assets/stage67_review_0929.js`. Legacy Stage 6 approach-gate and Stage 7
  sluice calls also paint the full FOV while preserving their endpoints.
- Removed the cropped-strip rectangle route in
  `assets/engine_combat_1007.js`. Explicit short attack segments retain their
  committed length and aim when passed to the regular FOV renderer.
- Queued aimed enemies in `assets/enemy_behaviour_1011.js` use the regular
  warning strength. Radial explosions still use their existing source charge;
  no misleading aimed field is added to an un-aimed attack.
- Existing attack timing, damage, projectile routes, warning budgets, alert-only
  calls and overhead-sign rules are unchanged. No art or atlas changes.

Verification: `node --check assets/game.js` and syntax checks for all edited
runtime owners pass. The full suite completes with **8,670 assertions, zero
failures, exit 0**, matching the immediately preceding baseline. The two old
band/cone assertions now check Mike's superseding request.

Native Chromium through `shoot.py`: **35 checks pass**, including all three
colors on stages 1–9, full-plate draw calls rather than cropped strips, legacy
gate spans, explicit line spans and alert-only behavior. Natural Stage 6 fighter
and Stage 8 alien-orb AI produce all three FOV phases before firing. Two short
gameplay clips and inspected screenshots are in
`_shots/enemy_fov_1011/review.html`. No page, console or asset errors.

The nine biome captures isolate the warning renderer; the two videos use
natural AI with a protected observer. Detailed report:
`docs/qa/enemy_fov_1011.json`. Local changes only; no commit or push requested.
