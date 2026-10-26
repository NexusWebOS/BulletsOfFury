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

## October 25 Warden / first-host review

- Mike approved actual spider walking for Stage7: distance-driven diagonal support,
  planted toes, bent-knee recovery and stable steering using the existing authored
  modular anatomy. Keep the measured alpha masks and opaque Retina targets.
- Mike explicitly replaced first-host arm darkening with exploding breakaway arms
  and actual alpha-bearing shatter fragments. This exception is scoped to the
  infused first host; all four final copies retain their separate native owners.
- Preserve the33.3/33.3/33.4 protected-core budget, native portal entrance and24
  rebirth beats. Ball form travels continuously and drops warned code bombs;
  digital reconstruction completes before its whiteout/final-arena reveal.
- Current owner, rebuilds, source IDs and verification:
  `docs/STAGE78_REVIEW_1025.md` and `assets/stage78_review_1025.js`.

## October25 bullet hell sections

- assets/bullethell_1025.js owns the new Warden/Dracodia and nine campaign miniboss barrages. Preserve native HP/form pools, original attack-book progress, authored projectile art, part flashes, committed openings and finite recovery.
- New ordinary barrage rounds reject offensive interception before their first update, while retaining native defensive clears. Physical missiles keep their native rules. Broken wings/claws/guns cancel their warnings and rounds.
- Preserve the escort, archive-army and Warden shield-counter interlocks. First-body Dracodia raises the real claws before committing warnings and uses those same sockets for release. See docs/BULLETHELL_1025.md.

## October25 grounded Warden and Tidal water arsenal

- Warden gait counts actual chassis motion relative to retreating terrain. Never scroll the retreat floor without live walking legs; braced barrages and exhausted legs stop that scroll. Keep fixed gun trunnions and the same connected claws throughout swipe windup/strike/return.
- Tidal remains one whole authored hull with96 fixed320x256 liquid frames. Keep armor/alpha unchanged, exact circle/cannon sockets, visible native hit flash/expiry and the complete6500 Furious water pool from its first live frame.
- assets/warden_tidal_1025.js owns coordinated flood, geyser, circle-mortar, turret-mist, cutter/torpedo and maelstrom turns. Preserve committed escape windows, ordinary-energy interception rules, physical torpedoes, defensive clears, shared cues, targeter interlock, native convergence/portal/death/rewards and owner cleanup. See docs/WARDEN_TIDAL_1025.md.


## October25 barrage corrections

- Stage3 lighting dims scenery only; retain native projectile, FOV, aircraft and HUD brightness.
- Stage6 Siege Fortress battery guns have no added bullet hell. The exposed core may use it after the native all-six-batteries gate.
- Caustic Dredger barrages leave measured turret barrel mouths with attached muzzle flashes, or arc from the top liquid opening into warned outward splashes. Never restore the generic gap/bottom launch point.
- Herald uses visible round red chaos energy, warned Phoenix-style corner flights and bomber passes dropping from surviving claws with energy muzzle flashes. Preserve native module damage, hit feedback, cancellation and breakup. See docs/BARRAGE_READABILITY_1025.md.


## October25 Event Horizon assault

- assets/horizon_assault_1025.js owns the Stage9 miniboss fast spin, vertical flight and charged eye bomb. Keep the authored whole plates and common eye pivot; do not stretch the spin bank over the barrage duration.
- Keep the live core, eye, hull, warnings and release aligned during vertical passes. Settle upright for charge, preserve the committed reaction window, ordinary-energy interception rules, defensive clears, hit flash and native complete HP/defeat ownership. Native defeat cancels pending bombs. See docs/HORIZON_ASSAULT_1025.md.

- Herald bomber passes match corner-flight world speed; commit the whole drop carpet before the rapid paired-claw releases. Keep the visible red energy, muzzle flashes, escape opening and broken-claw cancellation. See docs/HERALD_SPEED_1025.md.

## October25 Dracodia rotating download

- Use the authored turning carrier to download the actual live final-form body through one measured chest anchor and native scale. Preserve continuous carrier/build/speech positions, completed pixels, all24 lightning beats and native HP/reveal/death ownership. Fusion uses combatEnergy0927; do not reintroduce a small fusion snapshot, teleport pop or teleport cue for this beat. See docs/DRACODIA_DOWNLOAD_REVEAL_1025.md.

## October26 Dracodia depth download

- assets/dracodia_depth_1026.js supersedes flat rolling during the protected download: upright front/profile/back poses, one shared chest pivot/scale, native final-body handoff. Keep the skeletal carrier in unbuilt bands, separate rear/front electric helices and overhead downward strikes, all 24 native beats/audio and native health/reveal/death owners. Rebuild the source-derived 512-cell art through _BUILD_SOURCE/build_dracodia_depth_1026.py. See docs/DRACODIA_DEPTH_1026.md.

## October26 Dracodia accelerating flash reveal

- Mike's latest revision supersedes preflash settling: keep depth rotation accelerating and cyclic through peak whiteout, retain incomplete carrier/wire scan bands until full cover, and show the complete native body only as the flash clears. Preserve rear/front surrounding electricity, additional downward strikes across the playfield, all 24 native audible beats and native gameplay owners. Boss Cinematics is the personal reusable skill; current implementation/evidence: docs/DRACODIA_CLIMAX_1026.md.

## October26 independent Dracodia lightning

- Only the surrounding ending lightning spirals. Downward channels remain fixed per strike, independent of boss yaw; their separate cadence accelerates through the climax with release intervals. Preserve nine distant lanes, native audible beats and the flash-covered final-body reveal. Current notes: docs/DRACODIA_STRIKES_1026.md.

## October26 engine-wide rotation and bullet rules

- All players, enemies, projectiles, bullet hell, bosses, minibosses and final bosses use actual authored directional/rotation frames, never HTML/CSS or canvas rotation of a static sprite as a substitute. Keep common pivots and proportional scale. Apply this to new and revised rendering; existing owners require explicit migration and pixel verification.
- Ordinary enemy bullets, including boat spread fire, are never offensive interception targets, even before their first update. Magma/ice balls and physical missiles retain their explicit rules; authored defensive clears remain separate.

## October26 Dracodia loop/fade/speech/body polish

- RD27 preserves cyclic interpolated carrier/material/wire frames and 24-step 25%-100% skeleton visibility before lightning. Strike beats increase shared-mixer gain; only the closing speech line owns the roar/arm lift. Keep full-width first-host body pixels after arms break and the same authored recovery body during its fall, with 90 registered opaque arm targets across 45 poses. Use the stage78 owning builder; preserve native budgets, hit feedback and cinematic progression. Current evidence: docs/DRACODIA_POLISH_1026.md.

## October26 Dracodia living DNA-code formation

- The initial skeletal rise has its own living green DNA-code formation from 6.2 to 15.8s: authored code/liquid lobes, rear/front helix, binary cross-links and code inside the actual carrier mask. It wraps the stepped skeletal fade, then converges into download before lightning. This material spiral is separate from the blue ending electricity. Preserve native dialogue, protection and all later fixes. Current owner/evidence: docs/DRACODIA_DNA_1026.md; source manifest owner build_dracodia_dna_1026.py.

## October26 DNA final-form palette

- RD28 DNA uses Dracodia violet/red-magenta energy and pale highlights through two local palette sheets. Preserve native luminance, alpha, outlines and original green sources; regenerate through build_dracodia_dna_1026.py. The current drone-to-phase1 film records the unchanged native conversion for review. See docs/DRACODIA_PALETTE_DRONE_1026.md.

## October26 first-host entrance replacement

- Mike explicitly replaced the former void/player entry and dragon overlay with
  scenery scanline warp/palette darkening, living-arena fade, authored PixelLab
  amethyst gate and actual V18 drone emergence. The pilot stays in place.
- assets/drone_rework_1026.js owns the protected native intro. Final-form magenta
  synthetic code wraps and downloads the drone with rising rumble and 1015
  own-pixel glow; reveal the complete first host only under full whiteout,
  then clear to native phase1. Preserve all later cinematic/combat/HP owners.
  Source-derived glow builder, proof and recording: docs/DRONE_REWORK_1026.md.


## October26 Dracodia copied forms and protected final life

- assets/dracodia_forms_1026.js protects the final base HP and arms until Hammer, helicopter, Neural Archon and Phoenix/volcano pools are all exhausted. Preserve early hit/shield feedback, native pools and one final defeat owner. The infused drone host keeps its separate arm/core destruction.
- Use actual source pixels, continuous anchors, magenta DNA and flash-covered assembly for copy changes. Keep cyclic fixed-pivot loops and measured sockets together; the authored whole-body scythe pose owns its visible contact and recovery. Donor muzzle callbacks expire with their original form.
- Preserve the advancing native attack book, archive/helper interlocks, ordinary-energy interception rules, defensive clears, physical missiles, native cues and hit flash expiry. Full-fight evidence must use native inputs without enemy HP/phase/timer writes. See docs/DRACODIA_FORMS_1026.md.
