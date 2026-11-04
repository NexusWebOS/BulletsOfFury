# Galaga-inspired regular aircraft — November 3–4

Mike supplied [Galaga (1981) gameplay](https://www.youtube.com/watch?v=dvjapcHsqXY) as the flight reference. Visual samples at 00:15–00:44 and 02:03–02:14 show staggered curved chains, looping entrances, formation holds, peeling attack dives and returns. This pass adapts those movements to BOF's existing small, medium and large regular aircraft. It does not reproduce Galaga's entire encounter system.

## Live behavior

`assets/galaga_flight_1103.js` loads last, after the existing combat and story adapters. Eligible jets enter in spaced chains, bank around a curve on their side of the screen, briefly settle into formation, peel into an attack dive, rejoin, then depart. Dive targeting commits to a position rather than following the player continuously. Followers receive offsets and staggered release times. Larger aircraft turn more slowly and receive greater spacing.

| Profile | Base travel speed | Maximum route turn | Minimum launch interval | Formation hold after alignment |
| --- | ---: | ---: | ---: | ---: |
| Small | 200 units/s | 3.8 rad/s | 0.75s | 0.62s plus slot spacing |
| Medium | 160 units/s | 3.0 rad/s | 1.05s | 0.85s plus slot spacing |
| Large | 136 units/s | 2.4 rad/s | 1.45s | 1.05s plus slot spacing |

Difficulty adjusts route speed by 0.92 / 1 / 1.06. Native weapon cadence still belongs to the existing difficulty and attack systems. Queued aircraft do not fire from outside view. Long native tells, beams, locks, charges and rolls temporarily own motion; the route resumes from the aircraft's actual position afterward. Late-stage attacks begin after the entrance and within the existing weapon swivel range. Native recovery is preserved.

The new movement uses numerical paths and bounded heading changes, selecting the existing authored 16/32-direction cells. No image generation, runtime sprite rotation, source resampling, new glow graphics, weapon redesign, HP multiplier or damage rewrite was introduced. Gun/exhaust sockets, actual projectiles, native flashes, warnings, sounds, interception and death handlers retain their owners. Ordinary bullets remain unshootable.

Eligible regular aircraft are covered across Stages 1–9. Ground units, organic non-aircraft, bosses, minibosses, active encounter helpers, stealth/Dasher bomb runs, carrier launches and dedicated maneuver controllers remain with their existing owners. Stage 3's legacy aircraft without the required directional bank are excluded. The newer ice interceptor uses the flight layer. Normal still ends at Stage 5.

Two core conditions let the new owner bypass legacy edge pinning and entry clamping while active. Native encounter cancellation releases it. The legacy Furious displacement multiplier is suspended only while this motion owner is active, preventing a second movement application. Space bobbing continues visually but no longer determines the jet's flight heading.

## Review and verification

Review: `http://127.0.0.1:65042/review.html`. Three silent, real-wall-time native engine recordings show small, medium and large Stage 6 groups on Furious with an invulnerable observer and no player firing. These are representative observation fixtures, not natural campaign wave timing. Older wave films remain separate and have not been relabelled as new footage.

The native roster matrix checks visible arrivals, finite motion, native attack releases (including sustained beams and the authored depth-spin), formation/dive progression and finite departures across the applicable campaign difficulties. Additional fixtures cover mixed-size groups, 30/60/120Hz updates, real pause/resume, real damage/hit flash, encounter handoff, carrier-child release, exclusions, native turret sockets and bullet/missile interception. Final group-only tuning widened launch gaps and replaced a mid-flight stop with reduced forward throttle; the single-aircraft matrix does not exercise either group-only branch. Mixed fixtures and all three live films were repeated after that tuning. Counts, tested source hashes and complete observations are in `docs/qa/galaga_flight_1103.json`.

Mixed groups all depart without a persistent queue or formation stall. Brief overlapping crossings remain during dives; this is not a promise that sprites never overlap. The recordings retain rendering/first-use hitches and are not a 60FPS performance guarantee. They are silent canvas recordings, so they do not certify audio. Human dodgeability and full campaign balance still require playtesting.

`node --check` passes for the core and adapter. The required full `node _BUILD_SOURCE/test_fl.js` run still exits 1 before its final summary on the pre-existing `difficultyHealthBaseline15` ReferenceError in `assets/combat_polish_0927b.js:151`. Its fixture was not changed or stubbed. The focused native browser checks are separate evidence.

Reproduction tools: `_BUILD_SOURCE/galaga_flight_1103/`. Native films and images: `_shots/galaga_flight_1103/`. Source hashes and capture conditions accompany the QA receipt. Existing local work, including the concurrent story/projectile changes and earlier asset retirements, was preserved. No commit or push.
