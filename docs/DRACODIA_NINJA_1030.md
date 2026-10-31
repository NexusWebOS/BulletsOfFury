# Dracodia: physical robotic-ninja claws — October30

The final main body now fights with physical dive/landing and alternating jump-slash combos. The earlier confusing main-body bullet/energy book is replaced while claws survive. The first host and all four copied forms keep their own controllers.

The same approved anatomy supplies96 new authored poses across raised guard, depth retreat, approach, left swing and right swing. Shoulder-joint rotations, slight body bank/twist, depth and alpha-preserving white hit states are baked offline. Three2048px unrotated packed atlas pages plus three hit pages restore a common512px logical canvas and256px pivot with explicit even crops. Exact baked alpha owns each part's hit geometry and physical contact; Retina targets share those same live part anchors. Sources, hashes, reproducible builder and an editable Aseprite source strip are retained. The Aseprite file is the editable strip, not a claim of a manually authored animation timeline. No paid generation was used.

## Attack rules

- Guard0.55s, recede0.65s to38% depth, leap0.25s offscreen, then0.40s foreground plunge. The first ground Retina commits at combo entry. Foreground landing at1.85s has a25px impact hazard inside the64px warning.
- Each follow-up has a0.43s committed landing tell,0.44s authored twisting jump slash and0.16s landing. Normal has one follow-up; Hard/Furious have two. Orders alternate left/right and right/left; background side and landing heights vary on later combos.
-0.8s moving recovery, then0.75s Furious /1.05s other cooldown. No new radial bullets, broad energy storm or shadow-claw substitute. Once both claws are gone, the existing physical core-missile attack remains available.
- Background depth below85% and the offscreen leap are protected and absent from Retina targets. Foreground alpha remains hittable. A real surviving claw owns each side strike; severing it cancels that strike's pending warning/impact/contact. Later combos adapt to the remaining arm. Native hit flashes, HP, final-life guard, copy cursor, living morphs, main defeat and ending/reward owners remain.
- Pause freezes the attack. Cancellation/retry clears the committed warning and contact state. Landing/physical hits call native playerHit; GOD, normal death, roll/somersault/armor rules remain native. Charge, leap, slash, impact and common-warning cues use the shared audio mixer. No runtime sprite transforms, tint/composite generation or image-alpha animation were added.

## Evidence

55 main native checks across Normal/Hard/Furious and both orders;11 boundary checks cover pause/resume, real mid-swing limb destruction, cancellation, surviving-arm choice, no-GOD alpha-contact death, retry, copied-life download into the new main style, and exhausted final copied-hammer destruction. Zero page/console/draw errors. The separately verified RD76 return/last-life behavior retains its84 checks. Required full suite has exactly the same five existing failures, with no new failures. Core game.js remains unchanged.

Live full final-main-life checkpoint:5330HP with both limbs, preceding lives cleared before recording; invulnerable native GOD and input-only aiming. No recorder HP/phase/timer changes during capture. Native main-life defeat at65.15s;72.57s film includes the opening of final destruction. Both limbs remain unbroken in this particular film; the destroyed-claw path has separate native tests.58.18 nativeFPS; decoded audio mean−20.5dB / peak−4.4dB, native warning/charge/impact/slash cues recorded. No game/browser/asset errors. This is not a whole-game playthrough or non-GOD difficulty/balance claim.

Quick combo: http://127.0.0.1:51046/?dracodia=ninja-claws-1030#clip=stage8-dracodia-ninja-combo

Full native final-life fight: http://127.0.0.1:51046/?dracodia=ninja-claws-1030#clip=stage8-dracodia-ninja

Arena return/rebuild: http://127.0.0.1:51046/?dracodia=copy-return-1030#clip=stage8-copy-arena-return

Old clips remain archived. No commit or GitHub push was requested for this pass.
