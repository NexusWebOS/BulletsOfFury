# Contra-inspired combat pass — 13 October 2026

Implemented in the main Bullets of Fury checkout. This pass concentrates on ordinary enemies in Stages 5, 7, 8 and 9, plus the Stage 6 left-route carrier encounter.

## Footage studied

These are selected visual sequences and frame inspections, not a claim to have watched every minute of all three games. Exact source observations and proposed BOF translations are separated in `contra_iii_iv_observations.json`.

| Source | Direct observation | BOF application |
| --- | --- | --- |
| [Contra III, 6:01–6:21](https://www.youtube.com/watch?v=5tg771rvU2M&t=360s) | A huge overhead ship reveals separated underside cannons. One cannon forms a blue-white orb while another has an attached electrical column. | A wide moving Stage 6 cargo hull with independent, sequential laser batteries. |
| [Contra III, 6:11](https://www.youtube.com/watch?v=5tg771rvU2M&t=371s) | Frame steps at about 371.16, 371.36 and 371.56 show muzzle orb, descending orb, then electrical column and ground impact. | Distinct charge, release and recovery states. BOF timings are tuned independently for ship movement. |
| [Contra 4, City at 27:26–28:21](https://www.youtube.com/watch?v=yWCf8UmWq74&t=1646s) | Rear infantry and elevated sentries appear around a durable frontal tank and hovering escort. | Give a wave one major attack to read while retaining its lighter ordinary threats. Avoid continually layering every heavy pattern. |
| [Contra 4, robot around 3:39](https://www.youtube.com/watch?v=xWh--t4pivo&t=219s) | A detached rocket fist crosses the lower field; arm damage changes the boss silhouette. | Destructible attack sources with lasting combat consequences and visible wreck states. |
| [Hard Corps, mechanical forms around 15:11–17:40](https://www.youtube.com/watch?v=iooQeqdyB8E&t=911s) | Segmented mechanical arms and end pieces reorient around a moving central body as the player changes position along the sloped platform. | Keep the attack attached to its visible source; show a distinct state change rather than hiding it in undifferentiated effects. |
| [Hard Corps, Big Magnum around 30:31–30:50](https://www.youtube.com/watch?v=iooQeqdyB8E&t=1831s) | A huge body occupies the right side. A horizontal barrel changes height, with large separated rounds visible in a horizontal lane; the player stays in the lower platform area and repositions. | Strong emitter silhouettes, committed firing lanes and space to reposition between releases. |
| [User's Contra IV reel](https://www.facebook.com/reel/1034071451914065) | Sampled cable/platform scenes place blue heavy enemies above and alongside the player. | Distribute threats spatially and preserve an obvious dominant attack. |

Red pellet fans seen in the Contra 4 boss compilation and reel were **not** accepted as confirmed enemy fire: the player may be using Spread. The deliberate-gap ring and missile fan are BOF design choices requested by the user, not an asserted transcription of those uncertain frames.

## Playable changes

- **Stage 6 Warhive Siege Carrier:** a newly authored cargo fortress fills the top of the playfield and slowly reverses its horizontal drift. Six individual batteries fire a cascade, paired gates and alternating comb sequence. Each gun has charge, active, cooling and broken states.
- **Target choice matters:** destroying a gun cancels its queued and active beam. Destroying two exposes the reactor. The remaining guns keep fighting; their wrecks remain visible. Defeating the reactor completes this encounter without spawning the former ace chase.
- **Later ordinary enemies:** selected existing families now use lateral beam passes, charged fixed-direction lasers, pellet rings with an open wedge, or committed missile volleys. Their ordinary controllers resume after recovery. The director permits one new complex attack owner at a time and limits each unit to two special cycles.
- **Difficulty:** Easy has longer warnings and recovery with fewer shots; Furious has shorter warnings and denser volleys. Escape gaps, damage-free warnings and recovery periods remain part of every setting.
- **Effects:** compact animated charge orbs, animated beam cores, existing stage-matched projectile art, visible missile launch paths, per-gun hit flashes and solid broken battery art. The revised carrier uses five authored PNGs totaling 926,447 bytes (905 KiB), including broad crimson beams, muzzle bursts, and animated front vents; the ordinary-enemy pass reuses existing effects.

The Stage 6 rebel route and Stage X Harrier retain their existing encounter owners. The companion `AIR_MOTION_1013.md` describes the completed airborne rotation/roll art pass.

## Verification and limits

Native browser checks cover attack release/recovery, actual scheduled-wave activation, co-op damage ownership, interrupted emitters, carrier module removal, reactor damage, boss defeat and route isolation. Detailed machine-readable results are in the corresponding `docs/qa` reports. Visual examples are in the local review gallery.

Final results:

- Full `test_fl.js` regression suite: **0 errors** after the final integration fixes; main game and both new modules pass syntax checks.
- Ordinary enemies: **16 difficulty fixtures**, **19 stage/type ownership checks**, **8 scheduled-wave scenarios**, and **24 base-speed escape fixtures**. Co-op survival and real shield-break interruption checks also passed. Browser coverage includes Edge, Chrome and Firefox; the complete four-difficulty matrix was exercised in Edge, with Furious escape cases repeated in Chrome and Firefox.
- Carrier: **73 native checks each in Edge, Chrome, and Firefox (219 total)**, with zero game-resource or page errors. The updated checks include red beam pixels, four distinct beam frames, six muzzle sources, front light states, and inside/outside collision edges. All four difficulty profiles, queued/live beam removal, reactor unlock, beam/flame targeting, bomb routing, co-op health, victory progression and route isolation were exercised.
- Read the detailed [enemy report](ENEMY_PATTERNS_1013.md), [carrier report](STAGE6_CARRIER_1013.md), and [source observations](qa/contra_iii_iv_observations.json) for methods and scope.

Automated movement and collision fixtures demonstrate escape paths in their tested conditions. They do not establish a universal human survival percentage or a guaranteed frame rate on every laptop. Full-wave player feedback remains useful for tuning the frequency and intensity of these new attacks.
