# BOF encounter revision and Pixelmap font experiment â€” October 27, 2026

The encounter changes address the Stage 6â€“8 review. The font pack is a separate review experiment; production typography is unchanged.

## Stage 6

- Direct boss entry seals the spent opening, arrival, supply and route-choice timers. It keeps boss-specific conversation and live wing AI. Normal stage arrivals still occur at 14, 41 and 52 seconds.
- Four allies are present during the Rebel introduction. The native Rebel attack, damage and defeat owners remain intact.
- Rook's two chaingun pods now use authored directional/recoil cells. Pod placement and bullet origins share his actual heading.
- Harrier laser turrets and separated hull gun modules use baked direction banks and native source pixels. The laser's collision origin now agrees with its visible muzzle. Native carrier-to-Nightwing progression is retained.
- Carrier helper jets weave through the upper part of the field in crossing patterns. They show a committed warning before a four-shot burst.

## Stage 7

- Dredger and Warden turrets use source-matched rotation and recoil banks. Both barrels fire rapid toxic slugs; these ordinary bullets cannot be shot down.
- Dorsal mortars launch from the top, arc to spread ground targets, and scatter toxic rounds on impact. The Dredger retains seeded, spacing-aware rush decisions and native Furious overdrive.
- Warden movement stays in the central lane. Rear legs are vertically flipped around measured mounts; front limbs retain their committed swats.
- The live diagnostic exposed an inaccessible rear-leg pose. Reversing the flipped hinges spreads the feet outward. Protected-body routing also lets ordinary fire reach the visible canisters. A native laser-only fixture damaged both rear legs and both canisters while leaving the core intact; no missiles or direct damage calls were used during that check.
- Core and canister liquid use 16 source-derived emission phases. The lifted face exposes the emitting core.
- Canisters divide the existing shield budget rather than adding health. The core cannot take damage while either canister lives. The target list exposes the canisters after the limbs, then the core after both canisters break.
- The final exposed state hops continuously, lands in the middle lane and scatters toxic rounds at impacts. High airborne contact is disabled; the visible airborne body remains targetable.

## Herald of Death

- Repeated side passes are the main pattern, with native corner swoops retained between special attacks.
- New authored special poses spread the arms or bring the claws together. PixelLab supplied 16-frame eye/jaw reactions, skull energy, red tornado, nuke impact, red lightning and code plasma sequences. The coded pentagram includes original bitmap binary glyphs baked offline.
- A charged tornado storm darkens the scenery. A skull nuke forms between the claws, then expands to 85% of the visible field width; its circular damage follows the blast and leaves the edges safe.
- Rage raises and accelerates the wings, animates the screaming head, flashes red and fires six lightning volleys. The coded sigil bounces and emits radial code volleys on wall impacts.
- New energy ordnance is unshootable, bounded and canceled when its owner dies or the stage changes. Native modular health, hit response, breakup, defeat and rewards remain owners.

## Verification and limits

- Actual Chromium/native renderer checks passed for encounter entry, allies, rapid dual guns, dorsal mortars, central lane movement, canister targeting and core protection, final impact scatter, Herald special releases and projectile interception.
- Additional checks passed for normal Stage 6 timed arrivals, one-time NG+ 25% health scaling, a single 15% firing-rate increase, local hit-flash expiry and continuous hop motion.
- All 59 new banks use fixed even cells and common pivots. Component banks have no clipped frames. One shared crop per bank reduced decoded memory from 494.3 MiB to about 223 MiB without moving frames; stage-specific loading selects the relevant banks.
- Existing drawing owners elsewhere still contain runtime transforms. This is a scoped authored-frame migration, not a claim that the entire renderer complies with the current portability rules.
- The required suite still reports the same five baseline failures: hit-flash hold length; opening jump warning dialogue; opening jump before chromium activation; unchosen Stage X route persistence; Stage X right-route launch. No new suite failures were introduced.
- The Rebel and final Dredger captures logged three generic `ERR_CONNECTION_REFUSED` console messages without URLs. These remain unattributed; there were no page exceptions, draw errors or HTTP asset-error responses. The fights completed, and the final video/audio/seek checks passed.
- GOD-bot footage demonstrates visuals, native damage flow and successful clears. It does not establish human difficulty or fairness by itself. The new red flashing sequence also needs human comfort review.

## Font experiment

Fury Strike, Afterburn, Sovereign and Command each have eight baked palettes and all 95 printable ASCII characters. The pack contains PNG atlases, JSON metrics, AngelCode .fnt files, editable Aseprite atlases, original glyph masters and a small host-independent atlas adapter. These are original glyph contours, not traced game-font sheets. The review gallery tests centered labels, wrapping, mixed case, numbers and integer pixel sizes. All 96 family/palette/size combinations passed the browser checks.

No commit or GitHub upload was performed for this pass.

## Final live footage

All five listed final fights reached their native defeat, with no bot deaths, game exceptions or draw errors. MP4 seek points, Chromium playback, audible unclipped audio and byte-range loading passed. Generic connection-refused messages from two captures are disclosed above. Earlier Warden diagnostic takes and the first Herald take are excluded. The source health/damage owners were not edited during any final take.

- Stage 6 / Harrier and Nightwing: 165.9s, `revised-stage6-harrier/stage6-furious.mp4`.
- Stage 6 / Rebel Fighters: 186.5s, `revised-stage6-rebels/stage6-furious.mp4`.
- Stage 7 / Caustic Dredger: 59.5s, `final-stage7-dredger/stage7-furious.mp4`.
- Stage 7 / Toxic Warden: 135.1s, `stage7-warden-final/stage7-furious.mp4`.
- Stage 8 / Herald of Death: 145.4s, `final-stage8-herald/stage8-furious.mp4`.

Local review: http://127.0.0.1:49919/index.html

Font comparison: http://127.0.0.1:59944/index.html
