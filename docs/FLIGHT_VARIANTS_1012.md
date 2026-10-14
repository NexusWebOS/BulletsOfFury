# Filmed flight-pattern trial — October12,2026

Mike supplied 9c972f81-8de3-49aa-b78a-86911b86b22f.mp4 (4.73sec) and db93af2a-33ea-459b-9a83-f14bbafa6d6c.mp4 (161.53sec). Frames reviewed across both; spoken explanation decoded locally with Whisper base.en (audio not sent to a service). Transcript and actual current in-game aircraft references archived under _ART_SOURCES/flight_variants_1012.

## Installed trial

Stages1,4,6,8 gain seven scheduled formation types: orbit, corner, barrel/banking, south, spiral, kamikaze, mixed. Difficulty sizes3/5/7/9 (Easy/Normal/Hard/Furious); cadence24/20/17/14seconds. Native registered enemies retain ordinary projectile collision, damage, rewards and destruction. One formation at a time; starts only below ten existing enemies and85enemy rounds. Boss, miniboss, warning, dialogue, opening, firewall and player-death gates suppress new formations. Timers pause while controls/gameplay are blocked; boss transitions retire current formation aircraft. Existing stage waves and biomes retained.

Group target is captured at creation. Charge lanes commit to that point, then travel along the same line; they do not chase continuous movement. Easy kamikaze wind-up1.79sec and dash2.4sec; Furious1.25/1.6sec. Corner entry starts1.8×size then settles to normal in1.4sec, with engine shadows. Bombs drop vertically using existing authored lz_bomb art. Destruction immediately cancels that aircraft’s release. Live aircraft stay opaque; only effects dissipate.

Generated assets use actual stage aircraft references. First multi-aircraft sheet rejected for missing columns. Four separate16pose source grids retained; curated eight-direction runtime banks normalized to96×96, fixed48,48pivot, one common proportional scale per bank and transparent margin.64runtime cells across heading/banking banks; no canvas/CSS hull rotations. The banking reel currently uses selected right-facing authored bank/edge/underside poses; reverse-direction passes use the heading bank. This is a trial, not a claim of a fully continuous16heading or bidirectional360degree barrel animation. Original sprites and generation sources preserved. Runtime PNGs live in each stage’s enemies/flight_variants_1012 folder and preload only for the active stage.

## Verification and limits

Full base suite reaches FALVA/LIZZIE BUILD OK,0ERRORS. Syntax and whitespace pass. Edge native28pattern fixtures (seven types×fourstages) pass with finite positions, actual releases, difficulty formation counts and transition cleanup. The original visual fixture raised enemy HP only in the test to expose entire paths. Its shipping20/36/60/90 HP overrides have been replaced by the October13 balance below. Camera/intro fixtures are controlled; they are not unassisted play. Generated PNGs verified uniform, even and unclipped. Screenshot review caught and fixed outward corner curls, clustered orbit origins and overly compressed follower delays.

Four independent24second post-opening Furious trials use ordinary lateral inputs, held L5Spread, speed5,shield5 and three starting lives, no player invulnerability. Final samples remain playable with one life and shield0 in each stage. Formations and releases occur in all four. These short samples include original wave pressure and pickup randomness; they do not isolate a numeric before/after difficulty gain or certify survival odds/full-stage fairness. Stage6opening was bypassed for the post-opening trial, explicitly; intact opening blocks formations normally.

Review: _shots/flight_variants_1012/review.html. Detailed results: docs/qa/flight_variants_1012.json. Local only; no GitHub push.

## October13 small-enemy balance

Mike reported excessive health on these small and depth-entry aircraft. Corner scale-in formations now take exactly the hull HP of their authored reference family, calculated through the live roster and EHP: Jungle s1jetdelta, Airbase s4interceptor, Storm s6dart, Void s8interceptor. The Airbase value includes the same1.12 modular hull multiplier applied by encounters_0930.js. This retains stage, difficulty, player-loadout pressure and cooperative scaling without attaching the reference aircraft's competing movement or weapon controllers.

The other six small formation types use half that family health, rounded upward, with absolute caps6/8/10/12 for Easy/Normal/Hard/Furious. Their native two-damage hit checks require2–6 hits; the game's existing first-impact survival rule remains. No hidden shield or separate armour pool is added. The inherited generic drone cannon is removed: it was invisible under the authored aircraft render and fired outside the formation's own warned schedule, including during destruction.

Measured fresh solo fixtures (Easy / Normal / Hard / Furious):

| Stage | Regular family and matching corner HP | Small formation HP | Actual two-damage hits to kill small craft |
|---|---|---|---|
|1 Jungle|4 /6 /6 /11|2 /3 /3 /6|2 /2 /2 /3|
|4 Airbase|7.84 /10.08 /12.32 /14.56|4 /6 /7 /8|2 /3 /4 /4|
|6 Storm|7 /12 /15 /19|4 /6 /8 /10|2 /3 /4 /5|
|8 Void|13 /18 /21 /29|6 /8 /10 /12|3 /4 /5 /6|

The values above are measured under the probe's solo loadout. Regular/corner health still follows the engine's live pressure and co-op adjustments; small health remains bounded by the stated caps.

Missile first release is1.90/1.75/1.60/1.50seconds instead of2.30; repeat-volley gaps are.48/.42/.36/.30seconds instead of.70. Banked bomb releases begin at1.10seconds instead of1.50. Formation slot delay is.08seconds. Full1.15second missile tells and.75second bomb tells remain visible. Existing volley counts, shot speeds, fleet counts, flight paths and kamikaze charge times are unchanged. Both gameplay and warning rendering read one shared timing function.

Validation owner: _BUILD_SOURCE/probe_formation_balance_1013.py. It runs the real native Edge engine:112 formation/difficulty/stage fixtures,16 exact regular-versus-corner HP comparisons with native damage/death checks, hidden-cannon absence, destruction cancelling release, transition cleanup and authored heading/roll rendering. Output: docs/qa/formation_balance_1013.json; screenshots in _shots/formation_balance_1013. These are controlled encounter fixtures, not unassisted full-stage survival claims. Root's full regression result is recorded with the combined balance pass.
