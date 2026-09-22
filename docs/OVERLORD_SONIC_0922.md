# Cole sonic boost and Furious Overlord — September 22

- [x] Cole's sonic damage increases by exactly 50% at every charge level, including boss damage. Full charge: **22 → 33**; half charge: **14 → 21**. Piercing and range remain intact. Other pilots' forged sonic emissions retain their damage.
- [x] Furious Stage 1 helicopter uses jungle/neon-green armour on both intact and critical plates. The cached pixel palette preserves luminance and neutral metal/outline pixels; rotor and missile art retain their authored colours. The previous red damage overlay no longer overrides this Furious palette.
- [x] Completing the helicopter's circling/rain-sweep sequence leads into a green-glowing sonic windup. The shared alert changes green → yellow → flashing red. Heading commits before release.
- [x] Three fast pressure fronts fire **horizontal → vertical → horizontal**, 0.66 seconds apart, all travelling along the committed facing direction. They use Cole's authored sonic-wave art; the vertical front rotates instead of flipping. Oriented collision leaves the outer edges/corners open.
- [x] A subsequent shudder and pod-flash windup locks Retina onto the player with six spaced beeps. Three volleys of four sonic-infused missiles launch, 0.72 seconds apart. The helicopter resumes its orbit and gun pattern as the volleys continue. Missiles are shootable and use the existing lock-breaking/evasion system.
- [x] Added encounter is Furious-only. Hard and lower retain their existing attack sequence.

## Verification

`_BUILD_SOURCE/probe_overlord_sonic_0922.py` runs real Chromium with empty temporary storage. Passed checks: damage at three charge levels, horizontal/vertical/horizontal order, six windup beeps, all three volleys from moving positions, native projectile interception, oriented collision edge/corner clearance, Hard exclusion, and the natural enraged bullet-rain sequence reaching the new combo.

Native barrel roll and somersault both survived an incoming pressure front; the unprotected control case was hit. Screenshots inspected for intact/critical palette, warning colours, wave orientation and moving missile volleys. Page/console errors: **0**. Evidence: `_shots/overlord_sonic_0922/`.

Syntax checks pass. Updated the existing full-charge assertion to the requested 33 damage, preserving CRLF test line endings. Full suite reaches its final summary and exits **1 with the same 76 failing assertion names as baseline**; no new failures. Gameplay source remains LF. This is encounter verification, not a claim that every campaign balance issue is resolved.

Existing authored art and sound cues reused; no generation credits spent. Nothing committed or pushed.
