# Dracodia volcano: articulated combat — October 19, 2026

Mike requested an attack-animated, thoroughly modular volcano copy. Implemented
in the real GitHub Coding checkout. The independent Stage2 Furnace boss and the
other Dracodia forms retain their existing controllers.

## Body and attack animation

The approved volcano master is separated losslessly into17 registered pieces:
torso, reactor, two exhaust chimneys, two shoulder plates, two upper arms,
two forearms, two thighs, two feet and head, plus the two flame plates within
that17-piece count. A shared48x48 bearing cutout from the actual knee supplies
material under moving joints; it is instanced at elbows, shoulders, knees,
hips and exhaust hinges. Every original source pixel reconstructs the approved
master exactly. All primary cells320x320, even dimensions and fixed physical
pivots. No stretching, per-frame fitting, invented geometry or opaque backdrop.

The visible cannon now follows its native aiming, charging and recoil values;
its recoil braces the legs. Shoulders, upper arms and forearms articulate at
separate joints. Reactor charging uses internal authored orange pixels, with
proportional pressure movement. Exhaust tilts with heat. Feet, knees and
chimneys fold inward for the rotor/rolling attacks. The existing48-pose detached
head remains the final phase of this copy. Module loss preserves the actual
remaining skeleton and weapons; no complete replacement plate is pasted over it.

All attacking nozzles share one physical pose with their FOV, ordinary shots,
muzzle flashes and damaging beams. The native copied controller used to update
its position before firing while the rendered host lagged, then clamp the host
after release. New current-frame socket rebasing happens before native collision,
including viewport-edge clearance. Destruction removes a live beam immediately.
Rake retains its committed arm arc and real alpha contact, with its authored
curved FOV; the old auxiliary anchored arrow is suppressed for this form.

Stage8 uses viewport-relative Furnace stations while inside its native donor
tick. The compact rolling lane and Furious square route keep the folding body
visible; the intentional Furious jump/slam still leaves and re-enters the screen.
Generic Stage2 station/route functions use their original values outside this
narrow synchronous scope.

## Ten real damage modules, same total HP

| Native group | Independently damageable modules | Shares of group HP |
|---|---|---|
| Left arm | Left shoulder armor; left weapon arm |30%;70%|
| Right arm | Right shoulder armor; right weapon arm |30%;70%|
| Body | Left vent; right vent; left leg; right leg; reactor |10%;10%;15%;15%;50%|
| Head | Detached head |100%|

Integer allocation preserves the exact original total HP on each difficulty.
The four native Furnace pools are sums of the ten real modules. Arms are exposed
first, body modules next, head last. Breaking a weapon stops its emitter while
remaining shoulder armor can still be targeted. Breaking a vent removes its
rotor flame. Losing the reactor removes ring/lance attacks; unavailable attacks
are skipped. Destroyed legs and weapons stay absent. Genuine authored module
pieces supply the native debris, with no generic unrelated wreck sprite.

Native markHit owns whole-boss/part flashes and expiry. Real ordinary primary
fire was verified against arm/body/head. Retina targets use real module positions
and HP. Saved child HP, maximum HP and destruction flags survive copy changes;
the entry health helper cannot resurrect a destroyed zero-HP reactor.

## Art and sound

Shipping art:34 PNGs,77,655bytes (about76KiB), loaded only with Stage8. This is17
original components, one reusable bearing and16 PixelLab vent-flame frames.
The AI flame candidate8f1541b6-2c1d-4e40-a981-83697e833c34 was REJECTED: it grew into
an unrelated large swinging fireball. Raw outputs remain in _ART_SOURCES.
Accepted exact PixelLab drawingcf13a431-9785-406f-ba81-426bca718532 preserves the
approved flame, base pivot and palette with a registered flicker loop. Both
bookends match the source; fixed128x128 cells and64,96 base pivot.

Existing recorded enemyBossCannon, furnaceFlameIgnite, furnaceLaserCharge,
furnaceLaserBurst and shieldBreakCombat routes were decoded and played through
the native mixer. No redraw-triggered sound or pending callback is introduced.

## Verification

-114/114 final focused native checks: E/N/H/F, all eight native attack families,
 real muzzle/FOV/damage roots, ten independent damage/flash/break paths, immediate
 beam cancellation, no lingering pieces, and morph persistence.
-16/16 full game-loop checks: live ordnance/effects footage, ordinary arm/body
 gunfire, five recorded sound routes, zero browser/asset/draw/update errors.
-28/28 existing detached-head checks:48 poses per N/H/F, real eye sockets,
 full head turns, alpha targeting, ordinary primary damage and flash expiry.
-70/70 wireframe/ball checks: all forms and phase arrivals, safe edge escapes
 on E/N/H/F, ball rotation, full hologram framing, one-shot entry audio.
-8,854 whole-game regressions, BUILD OK/0 errors, exit0. Both script syntax
 checks pass. Final suite _shots/dracodia-volcano-final-suite.log.

Focused logs: dracodia-volcano-final-native.log, dracodia-volcano-live.log,
dracodia-volcano-existing-head-final.log, dracodia-volcano-wireframe.log.
The original head probe expected an absent parent output folder; the folder was
created and its unchanged probe then passed. Initial focused fixture did not
advance the shared markHit clock; corrected to use GP4.clock. Final probes
verify actual pixels rather than treating timer assertions as image evidence.

Runtime owner: assets/dracodia_volcano_1019.js. Art registry:
assets/dracodia_volcano_art_1019.js. Builders:
_BUILD_SOURCE/build_dracodia_volcano_1019.py and
_BUILD_SOURCE/build_dracodia_volcano_review_1019.py. Probes:
_BUILD_SOURCE/probe_dracodia_volcano_1019.py and film_dracodia_volcano_1019.py.
Review: _shots/dracodia_volcano_1019/review.html, with nine selectable native
animations, original components, vent frames and actual primary-fire captures.
Cache: volcano-modular-final-1019. Local only; no commit/push requested.
Preserve all independent Claude/Overdrive and unrelated dirty files.
