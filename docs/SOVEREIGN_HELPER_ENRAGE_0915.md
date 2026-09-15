# Sovereign generator-hit helper enrage — September 15, 2026

## Result

S4-12 is complete. On Hard and Furious, damaging a live Storm Sovereign shield generator now triggers a dedicated helper-enrage sequence:

- Each surviving helper switches to the existing engine's true red luminance-band palette and displays a glowing red asterisk.
- The pair moves to opposite screen edges and turns its whole authored turret plate toward the player.
- Each side fires six-round rapid streams with an offset lane, a staggered start, and repeated pause windows. The separation preserves a readable route between the streams.
- The Hard sequence lasts 5.6 seconds; Furious lasts 6.8 seconds.
- During this phase the Sovereign holds its shielded position and pauses its ordinary orb and final-chaingun routes, preventing unrelated attacks from obscuring the intended dodge gap.
- The helpers withdraw into their established formation cycle when the enrage ends. A generator triggers the sequence once per shield cycle; rearming resets generator eligibility.

Normal remains unchanged. The later limited vertical/backward tracking and spider-walk response remains tracked separately as S4-13.

## Verification

- `node --check assets/game.js` and the CRLF suite file pass.
- Focused suite section 326: **12/12** assertions pass for Normal isolation, real generator-hit triggering, one-shot eligibility, side stations, inward facing, both staggered lanes, gap windows, clean exit, Furious duration, and surviving-helper behavior.
- The repeat complete suite reaches its final summary with the exact established **57 failure names** and no new failures. The first pass omitted the known timing-sensitive Stage 1 sand-tank assertion and introduced no new name.
- Real Chromium through `_BUILD_SOURCE/sovereign_helper_enrage_0915/probe.py`: **19 passed / 0 failed**, with zero page or console errors.
- Pixel-reviewed gameplay frames prove the red helper plates, paired asterisks, side placement, inward turns, and visible stream gap without the former orb clutter.

Machine-readable Chromium evidence: [qa/sovereign_helper_enrage_0915.json](qa/sovereign_helper_enrage_0915.json).
