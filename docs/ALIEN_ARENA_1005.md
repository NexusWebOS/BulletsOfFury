# October 5 — alien arena and combat readability

Mike requested a darker central void, animated green Matrix elements, better
mutation/phase introductions, a modular ghost, stronger alien attacks and clearer
Stage 6 pellets/elite warnings. This pass remains local and uncommitted.

## Authored arena

The third encounter engulfs the screen in a growing black symbiote iris, then
reveals an opaque alien cathedral with an almost-black central combat corridor.
A restrained rotating void stays active in the middle. Twelve generated code
frames animate alternating emerald columns in eight perimeter banks. Independent
near/far rib movement supplies parallax. These layers persist through every
copied form and disappear when leaving Stage 8. Simulation owns the clock;
draw calls cannot accelerate it while paused.

Five preserved imagegen sources deploy 35 loose cells. Original pixels/alpha are
unchanged; the builder slices equal cells and trims only transparent padding on
ghost modules. Source prompts, hashes and native dimensions are recorded in
`_ART_SOURCES/alien_arena_1005/manifest.json`. The builder owns the registry in
`assets/alien_arena_art_1005.js`. No shared atlas or game.js edit.

## Finale behavior

- The entity gathers behind the original drone and consumes it before the
  mutated host emerges. Copied-form transitions use the new symbiote iris and
  loose rotating authored fragments.
- The ghost has eight HP modules rendered as nine authored shapes, including
  one complete head attached to the torso's shared HP. Arms articulate and move
  their claws; the eye satellite orbits. Native muzzle, shot, contact and Retina
  geometry all follow surviving modules. White hit flashes preserve silhouettes.
  Destroyed arms take their attached claws with them; plates break off into
  opaque burning/spinning debris, including the final collapse.
- Mutated drone adds crossed cannon lanes and a committed warned charge. Ghost
  adds pincer/cross swipes, a void relocation and cannon rail. Hard/Furious unlock
  an expanded cannon/orb attack below half health; breaking those modules disarms
  their emitters.
- Dracula combines actual articulated claw sweeps/crushes with faster claw
  salvos, paired void batteries leaving gaps, bounded gravitational drift and a
  committed Hard/Furious body dive. After its attack cycle it selects a remaining
  copied form; exact host/form health and destroyed modules persist.
- Copied bosses retain their actual campaign controllers. Hard/Furious add
  warned elemental/module volleys instead of an extra generic radial curtain;
  the knight retains its existing Hammer-derived sword/shield/Dark Code book.
  Furious allows forty seconds with a copied controller before returning to
  Dracula, without allocating or healing another life.

The supplied Contra Hard Corps video was sampled directly in the browser,
including folding/charging machinery and rapid alien battery bursts. This is
behavioral inspiration using Fury's authored art and existing controllers;
the entire 55-minute video was not watched.

## Stage 6

Approaching pellets receive a glow and the original authored flashing impact
asterisk. Prediction uses trajectory and time to collision, excludes safe/receding
rounds, and limits warnings to four closest rounds per living player. Rebel heavy
rounds and carrier ordnance share the warning. Collision/shootability is unchanged.

The actual Harrier elite presents FOV from its twin gun ports before four
staggered twin tracer bursts. Movement continues during the warning; dash/roll
interrupts it. Missile volleys defer until gun recovery and are bounded by
difficulty. The actual blue frames and white-hit path remain in place.

## Verification

Final results are recorded in `docs/qa/alien_arena_1005.json`. Native Chromium
checks use the game's own XART loader, context and simulation. The review at
`_shots/alien_arena_1005/review.html` contains screenshots, focused silent GIFs
and playable password routes on Furious. Protected recordings expose complete
attack cycles; they are not unassisted campaign clears or final balance proof.

`node --check assets/game.js` and both new runtime syntax checks passed.
`node _BUILD_SOURCE/test_fl.js` reached its final summary: **7,292 assertions,
zero errors, exit 0**, compared with 7,274 before this pass. **44 native/pixel
checks pass**, with no page or console errors. The sampled central corridor is
100% below RGB 25; 27,957 green pixels visibly change between simulation
timestamps. All four recording contact sheets were inspected for real movement,
complete heads, surviving modules and visible ordnance.

The first native check caught an overly bright center and a fixture camera
transform mismatch. Both were corrected, followed by an extended native run.
The playable review also launches the real Furious FINAL3 password route and
renders both animated layers. Its first harness attempt timed out after freezing
animation frames; switching readiness polling to timers fixed the harness.
No automatic Git publication is part of this pass.
