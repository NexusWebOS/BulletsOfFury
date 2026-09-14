# Mike's overnight development requests — September 14, 2026

This ledger preserves Mike's requested design. A listed item is not complete
until its implementation and relevant native Chromium pixels are verified.
Work is authorized through the morning, without commits, pushes or deletion of
user/trailer data. Overnight heartbeat: `bullets-of-fury-overnight-development`,
every 30 minutes through 8:00 AM America/New_York on September 14.

## Current priority

**First batch verified:** straight jet guns, Stage-3 side beams/central pulse,
Furnace head aim commitment, Regent port warnings, bounded impacts, player flame
scaling and Backspace pause protection. Proof and limits:
docs/READABLE_ATTACKS_0914.md and docs/qa/encounter_cleanup_0914.json.
Shared laser-family warnings, the stronger dark-blue palette and full pause menu
are now verified; remaining non-laser warning migrations are still pending. Missile supplies are now verified in docs/MISSILE_SUPPLIES_0914.md
(12 new suite checks, Chromium11/0). Tier upgrades/caps remain pending art.
Pause controls and verified browser campaign autosave are now implemented;
proof and limits: docs/PAUSE_MENU_0914.md (11 new suite checks, Chromium14/0).
Bitmap buttons remain pending SpriteCook. Component targeting and directional
Retina Scan are now verified: docs/RETINA_TARGETS_0914.md and docs/RETINA_SCAN_0914.md.
Next pending: universal no-one-shot damage rules and requested encounter variants.
Stages 5–9 should then be reviewed in individual rounds with Mike; stage 5 is
the first round. Preserve earlier improvements that already work.

## Screenshot corrections

- Stage-1 jets must use their authored straight twin guns or rocket sequence,
  without a second generic spread/steering attack layered over it.
- Stage-3 boss lasers fire at visible cannon exits. Its central charge/FOV must
  not look like the same full-length laser emitted through its body. Use dark
  blue ordnance with a restrained light core, readable over snow.
- Verify the stage-4 mounted guns, their flashes, apparent orange beams and
  upper rocket racks against whole authored plates.
- Stage 5 needs readable attacks and impacts, not full-screen purple curtains,
  opaque stacked explosions, stray tracers and simultaneous competing patterns.

## Shared engine rules and encounter requests

- Green/yellow/red FOV charge stages and an alert above the attacker are shared
  rules for boss/miniboss dangerous attacks. Lock aim before release, with time
  to dodge; especially improve the stage-2 Furnace Tyrant head's accurate lasers.
- Add reusable horizontal gliding, including controlled following of the player.
- Player flamethrower: scale down 25%, retain the plane connection, and match
  Fire Orb's palette/art style. Boss flame weapons are separate: stage-2 boss
  flamethrower is 25% wider. Its flame shield must always use the actual flame
  shield, including its first frame.
- Stage-2 boss rollerball: slow → medium → fast → very fast spin, moving
  horizontally with increasing speed. All pilots retain barrel roll and
  somersault access. Improve graphics and patterns without losing the approved
  head-phase exception. Note the planned missile-sequence head fight.
- Stage-2 lava/magma fodder: tougher hulls, weak breakable shields. Shared shield
  break/stun mechanic can make enemies dizzy, levitate and spin, with bounded
  splash damage to neighboring enemies. Reuse existing stage-2/stage-6 and helper
  shield systems and authored shield/break effects.
- Stage-3 miniboss: return from above aligned to player X, follow horizontally
  until its laser phase, darken the screen, crackling lightning charge and laser
  sounds. Attack 25% wider, sweeping left/right across the viewport while leaving
  the intended diagonal/upward dodge route. Choose sweep direction from player side.

## Jungle chopper boss

- Remove erratic movement. Preserve and optimize its otherwise approved patterns.
- Use ElevenLabs or Mike's existing sound engine for proper chopper/rotor noise.
- At the dam, enter from below over the player, with whole-frame shadow behind
  and hull above the player; whip spin into position. Boss bar fades in and fills
  left-to-right with repeated existing chime. Fight and boss music begin after fill.
- At 50% health retain frenzy and add four passes: down, up, down, up, across
  distinct screen sections. Passes 2 and 4 charge while raining bullets.
- Before each fast but reactable pass, flash a red warning zone with eight
  synchronized beeps. Commit after beep eight. Player should be able to land shots.

## Missile supplies, tiers and pickups

- Spawn missile supplies during boss fights. Remove x2 boxes. Stages 1–7 use
  x5/x10/x20 only; stage 8 may use x50/x100. Stage-9 box quantities were not specified.
- Manual/retina missiles, separate from passive homing missiles: standard →
  Super → Ultra → Uber. Each tier is 25% stronger than the preceding tier and
  visibly larger. Hard ammo caps: Super 50, Ultra 35, Uber 20; do not permit box
  quantities or accumulated pickups to bypass the cap.
- SpriteCook Super/Ultra/Uber upgrade icons and tier boxes, including a distinct
  Super Missile Box for the stage-2 head-sequence plan.
- Upgrade acquisition replaces the equipped manual tier; death resets to standard.
  Ultra may spawn only after acquiring Super and surviving until the next spawn
  wave; Uber follows the same rule after Ultra. Define wave eligibility explicitly.
- Ordinary enemy destruction may RNG-drop one or two spinning authored missiles,
  with a scatter animation for two. Boss/miniboss destruction does not produce
  these loose drops.

## Pause, title and pilot UI

- Pause cannot exit via Backspace. Remove the basic instructional text.
- Pause engine rule: grayscale gameplay, quieter music, green flashing selector.
  Drop-in buttons with sounds: Return to Main Menu, Restart Level, Options,
  Quit/Exit Game, Help. Default to the top row using the title's cursor art.
- Options and Help reuse existing screens. Return to title ends the run through
  the complete GAME OVER voice/noise sequence, autosaves campaign, visibly confirms
  `Autosav0X.json`, then fades back to title. Do not bypass save completion.
- Intro silhouettes: all nine front-facing pilot portraits with their ship,
  scrolling Cole first through the rest of the roster.
- Pilot selection fills the game screen, readable typewriter text, left-to-right
  filling bars and normalized centered ship rotation frames.
- Replace legacy Yuri avatars everywhere. Regenerate Yuri's avatar box via
  SpriteCook to exactly match the roster style with red lights.
- SpriteCook improved Life Up, new Continue Up, menu/mode/achievement buttons
  where authored buttons are missing. Better stage fonts for all nine biomes,
  main menu/stage select/announcer font and readable dialogue font.

## Space Fighter replacement art and naming

- Find and render the newly generated SpriteCook spaceship concept. Generate
  separate parts matching the current assembly contract and consistent turning,
  somersault, roll, thrust, speed and transformation frames. Provide all nine
  pilot palettes, then replace the current ship only after art approval/verification.
- Retain the old ship as hidden unlockable password `spcboy`.
- Replace Gravity Mode wording with Space Fighter model names: Yuri Yamado,
  Maverick Moonraker, Lizzie Lavender, Falva Foxtrout, Cole Collisto,
  Juggernaut Janis, Axel Aristotle, Freezer Falcon. **Decker's model name is
  unspecified; preserve him and request Mike's naming decision when he returns.**

## Achievements, timers and modes

- Persistent achievements, once per account/profile, designed for later Steam
  mapping. Generated achievement button and bottom-center slide/fade notification.
- Nine `Campaign Clear - <Pilot>` achievements: campaign or arcade clear, 100 pts.
- Each stage on Normal or harder: 10 pts; each stage with no lost life on Normal
  or harder: 200 pts; no continue lost through the entire game: 1,000 pts and a
  generated trophy avatar; stage clear without firing a manual missile: 100 pts.
- Every weapon reaching level 5: its own 20-point achievement.
- Upper-right boss timer `00:00`. Stage-1 boss/miniboss defeat under two minutes:
  200 pts; under one minute: 500 pts. Clarify whether awards stack when Mike returns.
- New-game modes Campaign, Arcade, Co-op, Boss Rush, Time Attack. Boss Rush and
  Time Attack use Nexus II chain/lock art, gray buttons and denial alert until
  final-boss campaign clear. Final campaign currently cannot be completed; retain
  a real clear condition rather than silently unlocking them.
- Arcade mirrors encounters exactly, excluding cutscenes and campaign map.
  Continues Easy 7 / Normal 5 / Hard 3 / Furious 1; starting lives 7 / 5 / 3 / 3.
- Hard enemy hulls and shields: +15% across Campaign and Arcade. Some Hard/Furious
  enemies duplicate as visibly distinct elite, shielded, skilled fighters. Furious
  is more capable; do not turn ordinary fodder rounds into homing spreads.
- Hard/Furious missile supplies and Life Up frequency +25%. Continue Up in all
  modes from specified no-death sections or Hard/Furious elite kills.

## External access and verification

At intake, this session exposes no SpriteCook or ElevenLabs callable tool.
Investigate existing local integrations without printing tokens or signed URLs.
Do not substitute ImageGen for Mike's specified SpriteCook work. Record required
art as pending if generation access remains unavailable; continue independent code.

Measured baseline before this batch: 3,724 passing assertions / 61 failures,
suite exit 1, final summary reached. Native probe: 42/0, but Mike's screenshots
demonstrate that those checks were insufficient for encounter readability.
Compare failing assertion names, inspect actual pixels and page/console errors,
and test natural attack timing as well as debug windows. New source/output:
`_BUILD_SOURCE/encounter_cleanup_0914/`, ignored `_shots/encounter_cleanup_0914/`.

## Completed batches

The current tally is maintained in the generated checklist linked below.

Use [REQUEST_CHECKLIST_0914.md](REQUEST_CHECKLIST_0914.md) as the current status index.
It consolidates all requests, links proof, and distinguishes partial work from completion.
The older batch entries below are historical snapshots; they are not the current tally.

## Mike's additional requests — September 14, targeting and Hard/Furious

These are newly authorized requests, not completed implementations. Prioritize
retina target eligibility after the shared-laser verification batch.

### Retina engine rules

- Stage-6 boss and any multi-part/helper encounter: tap Retina cycles electrical
  nodes and live helpers. Exclude the boss hull while its shield is active; allow
  hull targeting only after the field is down. Share target eligibility with
  weapon targeting.
- Retina upgrade: hold Retina and tap a direction to scan targets inside the
  player's FOV. Additional retina markers lock additional eligible targets.
  Firing manual missiles releases all selected targets one by one with a few
  milliseconds between launches, paying actual ammo per missile.
- Five-second firing window; expired markers flash and disappear using the
  existing single-lock lifecycle. Duplicate its system rather than inventing a
  disconnected lock behavior.
- By default no enemy should die to one hit, to avoid multi-lock abuse. Implement
  and verify this as a gameplay rule, including high-damage weapons, without
  silently changing damage accounting.

### Stage 1 miniboss

- Faster projectiles, sonic boom and movements.
- Hard: two simultaneously.
- Furious: one 50% larger, Furious palette, hyper tank mode; sonic waves become
  Furious waves, a giant chaotic monster tank challenge.

### Elemental engine rules and stage 2

- Hard stage-2 miniboss and boss: +25% HP, absorb 50% fire damage.
- Display Fire Dmg Absorbed! around targets on absorption; reusable engine rule.
  Ice enemies similarly absorb ice weapon damage.
- Fire deals 2× damage to ice; ice deals 2× damage to fire.
- Apply the shared elemental rules consistently across ordinary foes and
  boss/helper/shield paths where relevant.

### Stage 3 miniboss on Hard/Furious

- Black/royal dark-blue palette, 35% larger.
- Charge with player retina lock, release shootable spiral rockets alternating
  left/right/left/right. Survival uses somersault, barrel roll and shooting
  remaining rockets.
- Furious additionally requires late movement before its charge into the player.

### Stage 3 boss on Hard/Furious

- Hard: Juggernaut-style charge dash with authored charge effects, then circular
  return flight with fluid fast rotation. Always a boss-shaped shadow.
- Below 50% on Hard: double laser firing; shootable homing laser balls follow the
  player until leaving screen or losing lock to barrel roll/somersault.
- Shared HUD threat lock icon above Equipped: gray idle, red flashing when a
  missile locks the player. Flash/beep accelerates as distance closes and ends on
  evasion or hit.
- Furious: black/blue palette; retain all requested Hard patterns. Add a giant
  Iron-Man-style laser derived from stage-2 beam mechanics, with better authored
  fire-boss beam graphics and a stage-3 palette variant.
- Faster cannon attacks; Simon-Says-style cannon FOV sequencing/feints.
  Furious only: no green charge phase. Yellow/red/yellow/red/red flash → fire.
  Remove overhead asterisks/alerts only on Furious.
- Preserve distinct authored attack/release geometry despite the intended feints.

### Stage 4 miniboss on Hard/Furious

- Hard: rapid mounted dual spread guns and center straight machine flurries.
  Circular flight/gliding/charge, shaking warn before ram or completed maneuver.
- Hard two palette-matched fighter helpers; Furious three.
  One shielded stationary turret-like rapid burst fighter, one aggressive
  player-like protector using player-style missiles, forward/back movement.
- Furious third helper: elite black camo, opaque black/white Maverick-like ball
  with blue glow. Ball grows while charging; release darkens/fades the screen.
  Ball shatters/disintegrates with authored dark chromium energy, producing dual
  spinning flame-style energy hazards.
- Dark chromium hit uses literal ship disintegration rather than explosion, with
  proper sound-engine cues. This is Mike's named exception to the normal death
  sequence; ordinary deaths retain the existing anchored spin/crash rule.

### Stage 4 boss on Hard/Furious

- Helpers +50% shield HP, faster straight→diagonal attacks. Move forward into a
  horizontal row in front of the field to obstruct electrical core access.
- A hit on an electrical neuron enrages helpers: red palette, overhead asterisk,
  hyper independent mode. Move to sides, scroll/follow player's position, face
  the needed side and fire rapid side-facing rows.
- If both survive, stagger firing so their bullets nearly form a navigable row,
  with space between streams. Avoid unavoidable overlap.
- Enraged side mode lasts about 5–7 seconds. Hugging either outer edge while
  between streams lets the player hit electrical nodes.
- Helpers respond to node hits with limited upward and backward spider-walk
  movement, requiring the player to adjust gradually as well.
- Furious: lightning balls more frequent and wider spread.
- Hard chain-lightning phase: double coverage/additional projectiles, wider
  spread. Furious: faster, broader patterns and an additional giant lightning
  attack. FOV yellow→red→one red flash, screen darkens, authored lightning forms
  around a five-second energy-core charge, then release.
- Giant strike has safe bottom-left/right corners. Authored Bullets of Fury arrows
  point left/right (one approved source duplicated/flipped), flash with sound on
  both sides and rapid FOV before impact to direct evacuation.
- Hard boss victories: separate achievements, 200 points each.
  Furious boss victories: separate achievements, 500 points each.

Verified shared laser-family FOV inheritance and dark-blue Stage-3 beams: suite 3759/61 exit 1, same baseline failures; Chromium 7/0. Remaining non-laser boss tells and Furious exceptions still pending. Pause video export exposed overlapping explosion audio clipping; correction queued with Retina work.

Verified Retina component eligibility: shielded hulls excluded; live nodes, open bays and helpers selectable; missile damage resolves selected piece. Shared seeking weapon targeting updated. Suite3771/60 exit1, no new baseline assertion names; nativeChromium12/0. Five-second directional multi-lock upgrade and no-one-shot rule remain pending. Combined pause/blue-laser video passed570-frame full decode with native unclipped audio; measured explosion mix corrected in the live sound engine. See docs/RETINA_TARGETS_0914.md.

Verified directional Retina Scan: four targets, hold Retina plus direction, five-second expiry, 50ms manual missile sequence, one ammo per valid launch, authored pickup from Stage-2-or-later missile crates. Pause freezes timers; death/stage change clear active locks; campaign saves retain equipment. Native13/0, new section30516/0, full3787/60 exit1 with no new failure names. Fourteen-second native preview fully decoded. Crate undefined-text bug and scanner cue stacking corrected. See docs/RETINA_SCAN_0914.md for scope, design choices and remaining work. Universal no-one-shot rule is still pending, not implied complete by multi-lock delivery.


## 0914 Arcade rules and consolidated checklist

Arcade lives 7/5/3/3 and continues 7/5/3/1 (Easy/Normal/Hard/Furious) are verified. The continue bank is run-wide, including Stage 9, with mode-correct difficulty descriptions and remaining-credit text. Campaign save loading refreshes its own difficulty. Full Arcade narrative/encounter parity remains partial. Proof: docs/ARCADE_RULES_0914.md and docs/qa/arcade_rules_0914.json; native 22/0, full suite 3804/60 exit 1, no new failure names.


## 0914 easiest-to-hardest queue — first two entries verified
Mike asked for the full list in chat and work ordered easiest to hardest. Current queue is docs/WORK_ORDER_0914.md, generated from workOrder/difficulty fields in docs/REQUEST_CHECKLIST_0914.json. Tally: 135 entries, 46 complete / 11 partial / 78 pending (89 unfinished). Follow ascending ready work; respect dependencies and skip unavailable external assets. This replaces the earlier foundation-first ordering.
Completed SPACE-15: eight supplied Space Fighter model announcements; Decker currently displays SPACE FIGHTER DECKER pending Mike's requested naming response (SPACE-16). Completed MODE-06: Hard/Furious Life Up chance +25% on both midpoint and ordinary death routes, without stealing ammo/shield outcomes. Midpoint pickups use visible camera bounds. New ship and Life Up replacement art remain pending.
Proof docs/EASY_QUEUE_0914.md and docs/qa/easy_queue_0914.json. Native Chromium25/0, no page/console/loop errors; section30715/0; full suite3818/61 exit1, final summary reached, no new failure names. Historical random sand-tank assertion failed this time. Runtime SHA256 e2e95dfbd9e0d65bfe55ac40d4989f3be1aba6d3ad4f33c9c89efe5f57674533. Sources _BUILD_SOURCE/easy_queue_0914; LF/CRLF preserved. No commits/pushes, new atlas art, data deletion or background automation.
Next ready item: MSL-09 remaining missile-supply frequency audit, then SPACE-11 source-ship inspection, S4-02 screenshot review and S2-05 actual flame shield from the opening frame. Decker naming is independently pending; do not invent a model.


## 0914 Draven and complete missile supply frequency
Mike named Decker's Space Fighter Draven and asked to continue. SPACE-16 and MSL-09 are now complete. Read docs/SUPPLY_AUDIT_0914.md and docs/qa/supply_audit_0914.json. Hard/Furious boss opening/repeat times 5.6/14.4s; fodder loose chance 12.5%; legacy single-ammo chance 7.75%; scheduled/scripted boxes receive one 25% bonus roll with a two-second, existing-box-clear queue. No recursive bonus or double bonus on the boss clock. Forced scripted x10 stays guaranteed.
Native27/0, real crate shooting/collection and real player death, zero page/console/loop errors. Full suite3839/61 exit1, final summary, section30821/0, no new failure names; historical random sand-tank assertion failed. One section307 fixture now allows the extra ammo interval above its life boundary. Current runtime SHA256 41a0790603c5e4d8320839e1083b19a6e123e9075fce334a744825dea888d7d5. Sources _BUILD_SOURCE/supply_audit_0914; LF/CRLF preserved. No commits/pushes/atlas edits/user-data deletion.
Tally 135: 48 complete / 10 partial / 77 pending. Follow docs/WORK_ORDER_0914.md. Next SPACE-11: distinct new SpriteCook ship concept not yet identified; current ledger contains Warden/map assets and the known active ship traces to _ART_SOURCES/gravity_mode_v2. Do not select the already-shipped ship or GPT component master as the new concept without evidence. Then S4-02 screenshot review and S2-05 actual flame shield opening.


## 0914 - Frost Cruiser nose laser correction

Mike clarified the wing pods are missile turrets and the nose must shoot Falva-style black/blue lasers. Read docs/FROST_NOSE_LASER_0914.md and docs/qa/frost_nose_laser_0914.json. Nose now launches fixed-frame fllaser_0 bolts at 24x112 and 0.34s cadence, with cached black/blue palette, four-step pixel lighting, laser muzzle/audio, nose-tail launch anchoring, committed aim and oriented shaft collision. Wing missiles and shared Jungle Cruiser nose remain unchanged. Full-tail culling and lazy-ready release guard verified. Native15/15, zero browser errors; nine-second silent native preview under _shots/frost_nose_laser_0914. Syntax passed; full suite 3852/58, exit1, no new names. No source-art/atlas/test-harness/music changes or commit/push. Checklist S3-14 added complete: 139 entries, 62 complete / 10 partial / 67 pending (77 unfinished). The charged sweeping beam and new difficulty attacks remain pending; next queue item UI-09.
