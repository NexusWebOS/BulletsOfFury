# Jungle Overlord-X four-pass frenzy — 2026-09-15

## Result

The first below-half-health charge now becomes a bounded four-crossing helicopter pattern:

1. Pass one charges from top to bottom.
2. Pass two turns north, charges from bottom to top, and rains authored orange machine rounds downfield.
3. Pass three turns south and charges from top to bottom.
4. Pass four turns north, charges from bottom to top, and adds the denser final bullet rain.

Each pass selects the available lane band nearest the player's position, then removes that band from the sequence so all four sections of the playfield are used once. Every crossing receives the complete eight-beat warning and locks its lane before release. The helicopter rotates into its travel direction, goes fully off screen between legs, and hands back to its existing curved return after the fourth pass. Existing below-half-health rapid bursts, smoke, fire and frenzy movement remain active outside this set piece.

## Verification

- `node --check assets/game.js` and `node --check _BUILD_SOURCE/test_fl.js` pass; runtime LF and suite CRLF line endings are preserved.
- Focused suite section 314: **8/8** assertions pass for half-health trigger, exact four-pass order, alternating directions, distinct lanes, bullet-rain ownership and bounded return.
- Full suite: **4,050 passing / 57 failing**, exit 1. Every failure name matches the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium: **16/16**, zero page or console errors. Six native frames cover the top warning, first southbound charge, bottom warning, both northbound bullet-rain legs, and the third southbound charge.
- The probe counts 32 warning beeps, four unique lane bands, and machine-rain calls exclusively on passes two and four.
- Browser evidence: `docs/qa/overlord_four_pass_frenzy_0915.json`.
- Screenshots: `_shots/overlord_four_pass_frenzy_0915/overlord_pass_1_warning_top.png`, `overlord_pass_1_down.png`, `overlord_pass_2_warning_bottom.png`, `overlord_pass_2_up_bullet_rain.png`, `overlord_pass_3_down.png`, and `overlord_pass_4_up_bullet_rain.png`.

