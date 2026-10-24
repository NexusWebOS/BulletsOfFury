# Bullets of Fury â€” Codex project guide

Read `HANDOFF_CODEX.md`, then the opening rules and latest relevant drop notes in
`CLAUDE.md`. Read `docs/CODEX_TAKEOVER_0913.md` for the measured takeover baseline.
Older README branch names, passovers, and test counts are historical; verify the
current Git state and runtime before relying on them.

## Working on this build

- Mike owns creative and design decisions. Continue his requested work using the
  existing authored assets and encounter specifications.
- Preserve existing staged, unstaged, and untracked work. Commit or push only when
  Mike asks. Inspect incoming GitHub changes before integrating them.
- Have one writer at a time for `assets/game.js`. Preserve its LF line endings and
  the CRLF line endings in `_BUILD_SOURCE/test_fl.js`.
- Available disk space is limited. Avoid full repository copies and worktrees.
  Keep temporary verification output under the ignored `_shots/` directory.
- Do not delete user data or trailer scratch files without explicit authorization.
  Do not expose secrets or SpriteCook signed URLs.

## Creative constraints

- Frame widths and heights must be even integers. Choose the resolution first;
  keep a uniform canvas, stable pivot and one proportional scale per bank.
  Use shared transparent padding for odd crops. Follow
  `docs/FRAME_RESOLUTION_RULES.md` for generation headers and export checks.

- Use the existing generated pad_* graphics for D-pad, action-button and Start prompts
  on game screens. B is the logical Back action; Backspace only deletes text. Show
  physical keyboard assignments in Help/Options, not competing navigation prompts.

- Use authored art; do not add placeholder or procedural sprites. Render candidate
  art before trusting its name. Consult `assets/data/ART_TAXONOMY.json`.
- For every newly generated ship-bearing cinematic, export and inspect the
  current actual in-game aircraft or Furyship and supply it as an identity
  reference. Preserve its design and palette; prefer the actual sprite for live
  movement. Follow `docs/CINEMATIC_SHIP_REFERENCES_1010.md`.
- Maverick's homing lasers are not upgradeable. Keep their combat stats fixed
  and exclude them from Forge/elemental upgrades, including Wind. His separate
  Laser Beam and charged Helix Beam special retain their own progression.
- Preserve authored stage biomes. Palette changes must retain luminance, outlines,
  and the authored colors of ordnance.
- Bosses remain whole authored plates. The approved Furnace Tyrant head phase
  and Mike's October18 PixelLab Stage8 phase1â€“3 modular redesign are named
  exceptions. Stage8 phase3 has its main body plus exactly Hammerboss, helicopter,
  Neural Archon brain and volcano forms (October23 user replacement of Harrier). Approved miniboss aperture mechanics and the two
  independent Tempest ships are separate encounter designs.
- Player death remains hit, anchored burning spin through 540â€“900 degrees, crash,
  then shock ring and explosions. Space deaths use the spaceship.
- Read `docs/ATLAS_REPACK_0903.md` before editing an atlas. Register sheet and cell
  changes together; generated manifests require their owning build workflow.

## Combat warnings and audio

- Ordinary enemy bullets, including boat spread fire, cannot be intercepted by
  player weapons. Use `enemyOrdnanceCanIntercept` for offensive cancellation,
  including Chromium and rollers; `_weaponProof` alone is insufficient before
  a new round receives its first update. Preserve physical missile interception
  and separate authored defensive clears.


- Bosses and minibosses use authored green/yellow/red FOV warnings. Do not add
  muzzle-anchored arrow boxes or duplicate floating hazard signs. Keep impact
  reticles, projectile collision alerts and explicit SHOOT! objectives with
  their existing owners; preload all FOV colours before combat.
- Added or updated enemy attacks need an approved sound assignment through the
  shared mixer and retrigger gates. Preserve intentional silent volley partners,
  cancel pending audio with the launcher, and use enemy gun cues independently
  of the player's current weapon. Verify decoded playback for new cue routes.

## Hit feedback

- Every added or updated enemy, boss, helper and modular piece must visibly flash
  when hit, through the existing markHit and owner/part flash paths. Never zero
  or suppress flash timers to preserve a palette; retain the authored palette
  between hits and verify actual damaged pixels and expiry in the native renderer.

## Ground traffic clearance

- Tanks and moving ground vehicles must never overlap or stack. Reserve their
  full visible authored hulls at spawn and maintain clearance during movement,
  including queued entry rows and highway reinforcements. Use the shared
  `ground_traffic_1018.js` owner; do not bypass it with per-wave spacing hacks.
  Keep crowded tanks upstream on valid terrain while their native attacks
  continue. Props and fixed missile pads are separate ground fixtures.

## Verification

For gameplay edits, run `node --check assets/game.js` and
`node _BUILD_SOURCE/test_fl.js`. Confirm the suite reaches its final summary and
compare failing assertion names with the recorded baseline; a nonzero suite exit
must be reported even when failures predate the change.

Verify visible behavior in real Chromium using `_BUILD_SOURCE/shoot.py` and the
relevant existing probe. Inspect screenshots and both page and console errors.
State assertions alone do not verify pixels. Check local art through `XART.get`
keys and the game context's own `drawImage`; cached canvases have no reliable
`.src` or object identity. Poll lazy asset readiness and yield between frame batches.


## October21 art/combat contracts

- Aircraft refits use complete idle/attack/drift/roll/somersault banks before activation. Keep fixed even cells/common fuselage pivots, one proportional scale, registered weapon sockets and disjoint reusable modules. Native emitters own muzzle flashes/projectiles. Preserve metallic highlights and dark outlines in palette variants.
- Re-authored weapon silhouettes require new measured muzzle/head/target anchors. Verify actual native damaged pixels, target overlap and hit-flash expiry; a selected animation key is insufficient evidence.
- Composite encounters retain the entire displayed live health budget. A destroyed core stops exposing a live Retina target; surviving modules keep fighting. Defeat/rewards/cookoff/progression occur once at full exhaustion.
- Rebel formation/personal attacks keep complete FOV lanes, committed reaction windows, shootable homing missiles and heavy-attack interlocks. Cloak reveal must work through regular Retina, Multi-Retina and missiles. Depth attacks return visibly and restore scale/heading.
- Shield variants remain transparent enough to read the hull and honor native energy/deploy/break/hit timers. Portal-only art keeps the native pass-through window and upright travel orientation.
- Supplementary explosions attach to the current native death owner, remain bounded and never replace hit/burning-spin/crash/shock-ring rules or fade modular wrecks.
- Coastal scrolling is monotonic; adjacent district rows match. Water and other animated parallax layers use independent clocks. Stage cards freeze unsafe live combat until their protected entrance finishes.

## Menu windows and Chrome Heart (October21)

- Menu confirmation/training prompts use the avatar-free S/M/L/XL `MW21` family, its measured text apertures and proportional corner-preserving renderer. Cinematic pilot dialogue stays separate. Never stretch a cinematic portrait plate into a tall menu window.
- Mike selected concept02, Holoscan / Exploded View, on October21. Its live owner is `assets/holoscan_dossier_1021.js`: actual authored turntables, shared BOB20_SPEC stats, readable responsive text and native tutorial input/clocks. Preserve the selected cyan/black material, fixed frame pivots and all four part views. Do not reintroduce the Overdrive card or concept-only weapon/size statistics.
- BARBIE is a protected account unlock after a real Falva/Lizzie final win (including co-op), never a debug victory. Chrome Heart stays scoped to its secret arena, with native dodge/death/audio ownership, absorbing shields, real hit flashes and its own post-fight result. See `docs/MENU_HEART_1021.md`.

## HQ / Forge / Re-Spec (October23)

- Decker Re-Spec resets the entire current-run elemental build for300 Furious Points. Preserve stage/base weapon unlocks and score; restore exactly two upgrade points per distinct completed stage. Stage6 before clear=10, after6=12, after7=14. Never refill on menu visits or retries.
- Preserve the completion ledger, remaining points and NG+ import suppression in saves. Payment must roll back if profile or campaign storage fails. Profile normalization must retain respec spend records. Confirmation defaults to Cancel.
- HQ/Forge landmarks and menu/button states belong to hf23_ and their authored builder. See docs/HQ_FORGE_RESPEC_1023.md; preserve native keyboard/mouse/controller routes.

## Hammer tactical transition and shared SHOOT header (October23)

- Every boss SHOOT! objective/header uses Stage6's authored nwarn_shoot graphic through bossShootGraphic. Preload boss_shoot_prompt; never replace it with plain text, a Retina ring or a custom warning box.
- Stage5 chaingun handoff: strike the exclusive chaingun icon box (never a chest), throw the canonical glowing hammer upward until offscreen, eject the actual gun, catch with articulated arms, then enter tactical gunfire. Native Chromium activation must retain the acquired gun and return to chain_warn, never respawn a held hammer.
- Preserve dark armor outlines/seams, fixed body unit/pivots, visible white hit flash, matched red rage weapon variants, native emitter/FOV socket agreement and existing attack/death owners. See docs/HAMMER_TACTICAL_1023.md.

## Chronos modular chaingun (October23)

- Canonical visible name is CHRONOS. Preserve legacy cronos asset/function IDs.
- Mike explicitly approved one separate chaingun module for Stage5 Chronos:
  whole authored body + independent rotary gun + foreground grip, not new limbs.
  Eight source-preserving rotor poses rev before firing and coast during rest.
- Preserve the native gun HP/Retina target and actual alpha hit mask/muzzle.
  Gun break stops its rounds/target; Chronos continues his native arsenal.
- Alternate straight-down rakes and centered fan volleys (Normal5/Hard7/Furious9).
  Keep warning reaction windows, dodge gaps and all3 authored FOV colors loaded.
  Rounds remain ordinary unshootable bullets; one audible native launcher per fan.
- The pickup/throw/catch owns its complete transition. Retain acquired gun through
  Chromium. Salvage radio waits during portrait dialogue instead of covering it.
- Sources/selection and rebuild ownership: docs/CHRONOS_MODULAR_1023.md.

## Furious recording regressions (October23)

- Announce Chromium activation only after a real activation; a declined opening-jump attempt queues no dialogue.
- Destroyed chainguns retain native chain_cool so Furious final recovery/rage checks run, never a stationary broken-gun fan.


## October 24 encounter rules

- Chronos speech is a live combat overlay: preserve movement, projectiles, new input taps and vulnerability. His non-missile spike-ball response is the explicit authored **red** hit-feedback exception.
- Siege-tank sonic waves are never offensive interception targets. Dracodia first-body arms each own 33.3% HP; the 33.4% core stays protected until both arms are destroyed.
- Read `docs/ENCOUNTER_REVIEW_1023.md` before rebuilding these encounters. Preserve the portal entrance and symbiote rebirth into the final arena.
