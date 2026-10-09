# Boss motion direction — October 9, 2026

Mike requested downloading the latest GitHub update, then carefully reviewing
his spoken boss feedback and physical demonstrations in
`C:/Users/Mdogg/Videos/2026-10-09 00-30-03.mp4`.

The recording lasts 5:50.73. It is a face-camera direction session: Mike acts
out the intended motion. The review covers all spoken segments and the visual
timeline, with closer 2 FPS frame sequences for eight demonstrations. Local
speech recognition supplies timestamps; nonverbal attacks are interpreted from
the images rather than invented from missing transcript words.

These are recorded design directions. The initial review installed no boss
graphics. The October 9 implementation checkpoint below now records the authored
pose integration and its verification separately from the starting baseline.

## Download and verified starting point

- Inspected and fast-forwarded main from `d7441c84` to
  `d87ed6a8ab18d2e0e3b7cd235cf6651d2f681f90`.
- Incoming changes improve fullscreen fitting, dense HUD lettering, score and
  special readability, idle/live lock crosshairs, portrait paths and HUD clearing.
  The Overdrive launcher is included. They do not implement this recording's
  new boss direction.
- Existing staged and unstaged guide edits were preserved as separate layers.
  A guide-only restore conflict was resolved by retaining the complete incoming
  prefix plus both original local layers. Recovery snapshots and the temporary
  stash remain available; other local/untracked projects were not changed.
- `node --check` passes for game.js, player_hud_1008.js and
  widescreen_hud_0918.js. Full suite: 7,952 passing assertions, exit 0, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner.
- Existing real Chromium footer probe: 12/12, zero page/console/asset errors.
  Native HUD pixels inspected. These checks verify the download, not a full
  campaign clear or the pending boss changes.

## 00:00–00:40 — Stage 5 Hammer death

Mike dislikes the current handling of the head and body. Generate actual death
poses of the same boss, then use them in the in-engine death sequence.

The demonstration at approximately 00:21–00:29 shows the torso leaning back,
both arms lifting/opening, the head looking left and right while the body holds
the distressed posture, then a startled upward/front expression. The sequence
needs acting and a readable buildup before the body ruptures.

The final rupture releases many pieces, smoke, fire and electrical fire. Keep
the head present and correctly seated through the intact poses. The explosion
must follow the performance; detached/rotated existing parts alone do not
deliver the requested acting. Preserve the previously approved ordering of
in-engine death before cinematic cutaways and the return-to-Earth segment.

Acceptance: capture the complete death at normal speed, including intact
anticipation, head turns, final expression, rupture and continuing debris/FX.

## 00:41–01:58 — Stage 8 Dracodia physical attacks

Mike likes the current full Dracodia appearance but wants a more aggressive
scream, with his arms participating visibly. Preserve that approved identity.

The giant hands have an attack purpose. Hover over the player, shift into a
position, visibly prepare an arm and warn the intended strike. The demonstration
at 01:30–01:34 shows a large arm drawn back/up, torso turned into anticipation,
then a fast downward/across-body swipe with follow-through. An ordinary volley
following that warning does not convey the attack being demonstrated.

Below 50% of this form's own HP, add the more vigorous combinations demonstrated
around 01:49–01:54: alternating raised-arm strikes, body rotation/lean into each
blow and repeated aggressive follow-through. This threshold refers to the active
Dracodia form, not the sum of every saved transformation pool.

Implementation interpretation: the physical hand sweep should be the primary
hazard, with a warned path and collision matching the visible limb. Projectiles
may support existing patterns but should not replace the indicated hand attack.
Keep an escape/recovery opportunity after the committed swing.

Acceptance: record full-health and below-50% sequences; show that the visible
windup, warning, attacking hand, swept damage and recovery agree. Preserve
separate persistent form HP and the existing encounter structure.

## 01:59–02:44 — Stage 7 sewer spider claws and leaps

Generate poses that let the spider raise its claws and execute crisscross
attacks. The demonstration at 02:17–02:24 includes crouching/preparing, drawing
one limb high, turning through an across-body slash and lifting both arms wide.
The following demonstration adds a two-leg leap and forceful landing.

Landings should visibly throw up gravel/ground fragments and impact effects.
Use authored effect assets. The legs should compress for takeoff, tuck/extend
in flight and absorb the landing rather than simply moving a stationary plate.

Existing `assets/stage7_modular_0927.js` already has swipeL/swipeR/swipeX and jump
modes. Its pose function mostly pivots existing front limbs; the request is to
improve the actual acting and motion, not to add another identically named mode.
Reuse its ownership and independent destroyed-part handling.

Acceptance: real-renderer captures of claw raise, each cross-slash, takeoff,
flight and landing; ensure destroyed claws cannot attack and impact damage
matches the visible landing footprint.

## 02:47–03:48 — Stage 4 shielded boss and turret behavior

The boss is underwhelming while shielded. Make the surviving turrets actively
target the player and communicate a complete attack sequence:

1. Acquire the player with the original Retina graphics.
2. Build the FOV warning and its escalating pulse/beep rhythm.
3. Charge at the physical turret, then visibly recoil as the stream releases.
4. Follow through and recover before starting the next aimed attack.

Mike explicitly uses Retina as a tell here without necessarily firing missiles.
Do not turn every lock marker into a missile launch. His demonstration rotates
the firing pose and pumps the hands back on each burst: the turret should look
like machinery with kickback, not merely a source of rapidly spawned dots.

Add charge light/lightning that swirls around the turret, seated muzzle effects
and matching audio. Carry this approach to other applicable turrets in the game.
Keep the established Stage 4 shield, module and core-revival mechanics intact.

Relevant current owners include shipBossMount/mr27 module geometry,
`assets/hardcorps_bosses_1007.js`, and the Stage 4 repair/revival layers. Measure
physical pivots and muzzles before attaching the new motion or effects.

Acceptance: capture a complete shield-on cycle with the lock, warning, charge,
recoil and actual attack; confirm a destroyed turret cancels its pending attack.

## 03:50–04:15 — Stage 3 boss and smaller miniboss variant

The Stage 3 boss should benefit from the same expressive turret charge/recoil
behavior. The miniboss can use a reduced version, approximately half the
presentation/complexity; Mike does not prescribe an exact numeric HP or damage
multiplier in this recording.

The two miniboss turrets should behave as separate weapons, with individual
motion and the option of coordinated fire. Preserve the earlier projectile rule:
only magma/ice balls and missiles are shootable, with their elemental impact
effects and sounds; ordinary pellets remain enemy hazards.

Acceptance: inspect both emitters firing separately and together, plus individual
disarm/cancellation and the original shootable-projectile behavior.

## 04:16–04:58 — Stage 7 turret stance and combined battery

Mike likes the existing turret shooting motion but wants the body to angle into
a distinct firing stance first. His demonstration turns to the side, settles,
brings both hands/guns together, then alternates/pumps them while describing a
heavy bullet-hell barrage.

Reposition/angle the spider, visibly converge the turrets, charge, then release
the coordinated barrage. The final arm thrusts around 04:49–04:56 suggest a
strong physical finishing motion; its exact attack name and numerical timing
are not specified. Preserve the demonstrated rhythm instead of silently
substituting a random extra projectile fan.

Acceptance: the stance, gun convergence and charge remain readable before the
barrage; barrels, projectile origins, warnings and hit paths stay aligned while
the boss leans. Allow the player an earned gap after the commitment.

## 05:05–05:50 — Hammer bottom spike zone and upper counter

Move the ground Retina/spike presentation to the lowest part of the screen.
Spikes rise upward from that bottom band and threaten a player who stays
anywhere inside the affected zone, rather than appearing as isolated warnings
near the middle of the screen.

If the player moves above the spike range, Hammer occupies that upper space,
slides toward the player and counters with his hammer. The demonstration at
05:39–05:44 shows a clear shoulder-level backswing followed by a horizontal
smash, then the opposite-side windup and smash. Generate those directional
poses rather than pretending an unchanged plate is performing the swing.

Current code distinction: hammerStormFloorY already anchors the spike bases near
the bottom, while hammerStormTarget follows player.y and stormBounds extends
high into the playfield. Inspect these separate warning/target/damage owners
before changing the base Y again; the complaint is about the complete attack's
presentation and coverage, not just its spike spawn coordinate.

Acceptance: record warnings at the actual bottom band, visible upward growth,
damage inside the active zone, a player escaping it upward and the warned
sliding hammer counter. Verify both camera edges and every difficulty. Preserve
the existing Chromium recovery, break/stun and reward behavior.

## Art and integration checklist for the next pass

- Render existing reels before choosing a donor. Retain each boss's approved
  palette, silhouette, complete head and identity.
- Death acting, claws and directional hammer strikes need authored pose frames.
  A static image rotated more aggressively is not equivalent to Mike's demo.
- Define the actual pose and attack sequence first, then place warning geometry,
  muzzle/charge effects, sound and collision at the measured parts.
- Reuse existing attack/state owners and remove superseded behavior at that
  owner; do not stack a second uncontrolled attack director over it.
- Native capture must show anticipation, commitment, impact and recovery. State
  assertions alone cannot confirm the animation or its readability.
- Numerical balance values remain an implementation/tuning decision. The video
  specifies one explicit threshold: Dracodia becomes more vigorous below 50% HP.

Local review evidence: `_shots/boss_feedback_1009/` contains the timestamped
transcript, six whole-recording overview sheets, eight denser gesture sheets,
download verification logs and preserved guide snapshots. The original MP4
remains untouched. No new commit or push was made during this review.

## October 9 — authored motion checkpoint (local, uncommitted)

Built-in image generation produced eight accepted transparent source reels,
64 frames in total. The first Hammer death reel had duplicate arms and was
rejected following Mike's correction. The replacement has exactly two arms and
two legs in each intact pose; its head remains seated until the rupture.
An incorrectly branched spider forelimb reel was likewise replaced.

Sources and exact prompts: `_ART_SOURCES/boss_motion_1009/`. The owning builder
is `_BUILD_SOURCE/build_boss_motion_1009.py`; it writes the loose native cells
and `assets/boss_motion_art_1009.js` together. No shared atlas was modified.
`assets/boss_motion_1009.js` is the encounter integration, loaded by index.html.

- Hammer: eight authored death states before the existing cutaways; eight
  directional counter poses. The storm's targets, warning volume and spike
  ground now agree on a bottom band. Native checking caught a later helper
  still reserving room for the former lower HUD; this override was corrected.
- Dracodia: isolated left/right arm poses retain the approved identity. Eight
  additional torso/head acting frames progress from inhale to open-jaw shriek,
  left/right scream and recovery, with the head attached in every frame.
  Physical alternating swipes replace the corresponding generic projectile
  substitutions. Below half of the active form's HP, Hard/Furious adds four
  individually warned swings. Existing Court/Void spells, transformations and
  persistent HP remain owned by the existing encounter.
- Warden: generated forelimb raise/slash and rear-leg crouch/tuck/landing cells
  feed the existing module rig. Broken claws cancel their pending attacks.
  Its new converged-gun stance charges, alternates existing owned rounds,
  recovers and finishes physically. Landing uses an authored gravel reel.
- Stage 3/4: authored ice/gold electrical charge frames augment the existing
  turret directors, physical muzzles and recoil. The miniboss presentation is
  smaller; projectile shootability and Sovereign's revival rules are preserved.

All relevant new reels are registered with each stage's loading queue before
play, including direct boss/password entry. Existing original sound families
remain in use; this pass does not synthesize new voices.

Verification: game.js and all four new runtime/registry scripts pass syntax checking. Full base
suite reaches its final zero-error banner, exit 0. Native Chromium probe
`_BUILD_SOURCE/probe_boss_motion_1009.py`: 18/18, no page/console/asset errors.
Nine normal-speed clips plus actual engine screenshots are under
`_shots/boss_motion_1009/`; inspected pixels include the intact death head,
horizontal counter, raised symbiote claw, Warden limbs/barrage and physical
turret charges. Clips step the full updatePlay owner so projectiles move.
Additional native counter probe: 22/22, both strike directions at both camera
edges on Easy, Normal, Hard, Furious and Insanity, plus destroyed-turret checks.
The existing Stage 3 combat regression also passes, including real shots into
orbital turrets, missile release, laser commitment, miniboss charges and all
nine pilot spread-flash anchors. These focused checks are not a claim of full
campaign-clear or subjective difficulty balance. Longer unforced complete
encounter playtests and cross-pattern difficulty tuning remain follow-up work.

Mike additionally requested Stage 1 idle/fire animation work from
`passover_imagegen_1009.zip`, for the current roster. The supplied older NEF
references differ from the live modular tank/Fury Fleet renderers; the native
reference audit is complete and the current designs are used. The first
two ZIP-based heavy-tank candidates remain source candidates and are not wired
over the current modular tank. Static props remain static. Stage 2 and shared
explosion batches in the ZIP are guidance, not yet added to this pass's scope.
The current ten vehicles now have eight-cell idle/flight composites and the
nine armed vehicles four-cell fire composites; independent runtime moving
parts, gun aim and destructible modules remain intact. Details and separate
Stage 1 native verification are recorded in `docs/STAGE1_MOTION_1009.md`.
