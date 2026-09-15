# Jungle Overlord-X dam flyover — 2026-09-15

## Result

The Stage-1 boss now enters the dam fight as an aircraft instead of appearing at the top of the arena:

1. Jungle Overlord-X starts below the screen on the player's horizontal lane and climbs through the playfield in 1.18 seconds.
2. Its complete authored hull and spinning rotor cast a matching whole-frame shadow while the helicopter passes above the player.
3. The boss settles at its combat position and performs a fast 0.48-second full whip spin with the existing rotor/wind audio.
4. It returns level before the authored boss-gauge fade and eight-chime fill begin.

The boss gauge remains hidden during both the flyover and whip. The helicopter remains invulnerable and its combat AI stays disabled until the existing gauge introduction completes.

## Verification

- `node --check assets/game.js` passes; both focused contract tests exit cleanly.
- Focused suite section 312: 9/9 assertions pass for below-screen spawn, complete shadow, player crossing, centering, whip phase, full rotation and gauge handoff.
- Full suite: **4,032 passing / 57 failing**, exit 1. Every failure name matches the established baseline, including the intermittent Stage-1 sand-tank timing assertion on this run.
- Real Chromium flyover probe: **13/13**, zero page or console errors. Five native frames cover the climb, player overflight, whip start, mid-spin and settled pose.
- The dependent boss-gauge Chromium probe also passes **15/15** after the timing change, with zero page or console errors.
- Browser evidence: `docs/qa/overlord_flyover_intro_0915.json` and `docs/qa/overlord_gauge_intro_0915.json`.
- Screenshots: `_shots/overlord_flyover_intro_0915/overlord_rising_from_bottom.png`, `overlord_shadow_over_player.png`, `overlord_whip_start.png`, `overlord_whip_spin.png`, and `overlord_whip_settled.png`.

