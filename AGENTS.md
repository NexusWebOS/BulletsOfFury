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
  muzzle-anchored arrow boxes or duplicate floating hazard signs. Bullet-attached asterisks are retired globally (October31). Keep impact
  reticles and explicit SHOOT! objectives with
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

## October29 Herald chaos warning exceptions

- Mike explicitly removed tornado and skull FOV fields. Tornado charge uses one ground asterisk below Herald. Skull bombs are the explicit shootable-energy exception: accelerating one-by-one releases, eight growth variants, size-linked splash/ricochet chunks. Ricochet chunks stay unshootable.
- Lightning uses committed local filled circles/ground Retina/asterisk for two full seconds per strike; accelerating release cadence must never shorten the warning. Keep source red lightning/orbs, charge/throw/depth return and opposite-edge flight re-entry. Preserve native module damage/hit/death owners and HL51 actual bomb landing marks. See docs/HERALD_CHAOS_1029.md.

## October29 Herald skull spellcaster

- Mike replaced the bouncing pentagram with HS53's drawn rune seal: skull/eye glow, overhead asterisk, five line strokes, circle, spin, authored1015 pulse/size return, explosion, ruby penta balls and red-glass scatter. Keep actual orb world velocity/fuse/committed burst point together; native difficulty pressure must not send impacts offscreen.
- After both claws and both wings break, retain the skull/core magic book and native HP/death owners. No empty flight attacks in this phase. Glass rounds stay unshootable ordinary energy, with bounded lifetime/owner cleanup; the earlier explicitly shootable skull bombs are separate. See docs/HERALD_SPELLCASTER_1029.md.

## October29 Herald 20% depth desperation

- HD54 owns the final 20% native-HP transition: red protection, north retreat, five-second accelerating skull charge, generated 32-view depth turntable and red/black actual Falva rollers. Keep native damage clamping, growing collider/art sizes, protected Retina/solid exclusion, bounded ordinary-energy rounds, foreground damage windows and native defeat. Generic full-sized hull smoke is suppressed during protected background casting only. Prior HS53/HH52/HL51 owners remain. See docs/HERALD_DESPERATION_1029.md.

## October29 Dredger turret lock and roof mortar

- DF55 Stage7 tank hull remains protected and absent from bullet/Retina targets until both actual twin-barrel guns die. Preserve native total pools and gun alpha masks, alternating single-slug barrels, real white hits/expiry. Roof uses source-pixel emission/ooze, toxic mortars and committed actual ground Retinas; no circular roof FOV. Wall rush owns metal collision/rumble,2.95s distance-driven reverse tracks. Disarmed hull cycles only charge/ram/reverse/magma until native defeat. Keep bounded ordinary-energy projectiles and cleanup, without affecting the Warden boss. See docs/DREDGER_FINAL_1029.md.

## October29 Warden foreground guns and clear sewer

- WS56 keeps live Warden guns after head/body in draw and overlapping hit order, retaining native sockets, masks and flash expiry. Exposed core uses authored32-angle circling slams and back/forward hops with committed landing Retinas, toxic bursts and ground shadows. Native full HP and death/escape remain. Stage7 sluice pipe outlet events, drawing and damage are removed on every difficulty; do not restore them from older stage helpers. Structural floor/wall art stays. See docs/WARDEN_SPIN_CLEAR_SEWER_1029.md.

## October29 Event Horizon alien symbiote lasers

- EH57 owns Stage9 miniboss alien eye/spiral/360 beam/orb/radial attacks and50% aqua spinning dash phase. Keep normalized fixed-pivot32-angle whole hull, white hits and eye source masks together; include upcoming SG26 space float in live laser/dash contact calculations. Preserve native HP clamp/defeat and finite protected offscreen transitions. Ordinary alien energy stays unshootable. Shared360 disc/rotation warnings and400px dash lane must match side-beam danger. Do not restore EH25 projectile-only book over this owner. Main Stage9 boss/Dracodia remain separate. See docs/HORIZON_SYMBIOTE_1029.md.

## October29 Tidal Sovereign water arsenal and transferred Sentinels

- TS58 starts Stage9 with the whole water Sovereign, no Sentinel prelim/fusion. Preserve its native water HP once after spawn, exact hull/white-hit alpha and actual turret/fan sockets. Source-derived flowing/filling/glowing water, arcing warned geysers/falling waves, four-edge water rollers emitting bounce bombs, three asterisk water walls, fan rain,50% protected middle/360 charge plus naturally merging buoyant bubble volumes, Slip N Slide arrows/trails/waves. Ordinary water energy stays unshootable, hazards finite and cancelled on threshold/death/reset. The former two Wardens now occupy Stage8 actual34.5s carrier beat as independent normal enemies; keep their source hulls, heavy HP normalization, native death and visible muzzle firing guard, without the old mutation rig flags. Do not restore the old twins or WT25 turn book over TS58. Dracodia remains separate. See docs/TIDAL_SOVEREIGN_1029.md.

## October29 actual Stage2 water triplets and fan spirals

- The water wave source is nwf_fire_0..7, the actual Stage2 WFX three-wave hazard. Never substitute nib_wall player-weapon art. Keep native .75/1.1/1.25 warning/crossing constants, one wave at a time, six authored approaching sizes, matching alpha collision and queued lane asterisks. Fan motion rotates the actual spiral disk within fixed metal rims in all hull states, not just a moving liquid texture. Rebuild from corrected TS58 author/inputs; see docs/TIDAL_WAVES_FANS_1029.md.


## October29 Tidal forward guns and fan-owned ordnance

- TS60 corrections live in TS58 owner: L/R barrels face south with five committed spread angles and matching ten-lane FOV; use directional water capsules/muzzle plumes, not rotating orb bullets. Both geyser turns launch north from circleL/circleR, paint jets in front of hull, and only create marked1.6s returning rain after the actual jet exits view (handoff at viewTopY()-4 before native-16 cull). Grenades are fan-launched arcing water balls with1.8s fuse/contact splash and water droplets, never lower-turret ricochet rollers. Half-health lamp bubbles remain distinct. Preserve exact Stage2 water triplets/fan rotation, native HP/hit/death and pending/grenade/burst cleanup. See docs/TIDAL_FORWARD_FANS_1029.md.


## October29 water-wall warning layering and audio

- Water-wall lane asterisks render after the whole hull and effects, below the gauge, and stay queued until their individual wall launches. Preserve ordered Stage2 timing and reveal beeps. Full walls use tidalWaterWave through its two lazy Snd voices; small geyser waves retain cfComboWater. Keep generated master/provenance and build_tidal_wave_audio_1029.py. See docs/TIDAL_WALL_WARNINGS_1029.md.

## October30 water-wall warning identity

- Mike means the actual Stage2 metal nwarn_yield/nwarn_alert signs for water-wall lane warnings. Use TS58 wall_warning: yellow queued, red next, painted above hull/effects. Do not substitute HH52 red impact stars. Preserve per-lane release ownership, ordered beeps and aqua wave sounds. Source masters/recipe/manifest are archived with the boss art. See docs/TIDAL_WARNING_SIGNS_1030.md.

## October30 Rough Riders intro, dialogue and score

- Rough Riders Stage6 music is the original Gasline LevelX.mp3, explicitly confirmed by Mike; keep a separate roughriders6 transport. Harrier uses Level6b; newer StageX remains separate. Preserve scoped recovery and steady camera. Intro uses one actual barrel roll per pilot at flight cells72–87, never pitch/somersault cells32–47. Rebuild through build_riders_roll_type_1030.py using canonical native roll strips, and validate actual alpha on every cell. Compact portrait body text uses command_dialogue masters with common baseline; register font sizes in numeric order and preserve existing reveal/audio/name owners. See docs/RIDERS_ROLL_TYPE_MUSIC_1030.md.

## October30 continuous Rough Riders flight and solid shield

- RR65 owns final Stage6 squad positions. Do not restore RR45 instant projection, nearest-free-slot teleport or repeated attack-anchor translation. Keep bounded physical cruise, swept reservations, nearest formation assignment and the finite4.8s current-clear-slot fallback. Both entry and combat stunts use actual barrel-roll cells72–87. Native turbo corridors/Retina/HP remain separate. Decker Golden Aegis uses authored gold_grid40-cell fixed480x64 art, not rocky tiles; preserve its charge/seed, reflection, sounds and duration. See docs/RIDERS_FLIGHT_GRID_1030.md.

## October30 allied overflight continuity

- RR66 keeps the Stage6 allied formation escape visible over the Rough Riders: 1.8s native physical northbound travel, authored depth100→16 with original pilot/flame identity, matched ground shadows, and hidden hold only after the actual top edge is cleared. Keep shadows below enemies and hulls above even Voss foreground; protect dialogue. Preserve native return, wing HP and incoming warnings. Never substitute a vanished wing at the enemy row or runtime sprite scaling. Rebuild through build_riders_allied_overflight_1030.py. See docs/RIDERS_ALLIED_OVERFLIGHT_1030.md.

## October30 Nightwing wind charge readability

- NW32 Stage6 Nightwing uses authored336px front/rear vortex cells (12.5% reduction) from nightwing_teal_charge_1030. Wind charge adds the exterior teal-green1015 contour through the existing six-step ladder; preserve actual white hit feedback and the blue cockpit. The glow must remain visible around a hit, end with its attack, and never alter collision/HP. Rebuild from build_nightwing_teal_charge_1030.py; do not point the runtime back at the larger384px source. See docs/NIGHTWING_TEAL_CHARGE_1030.md.

## October30 Nightwing directional side passes

- NW32 wraps the native25% desperation flight with actual64-heading frame selection from its analytical tangent, including five-wave vertical displacement. Do not use stale cruise vx or south-facing whole/clean frames during side crossings. Hull, alpha hit, white flash, shadow and exhaust share the directional pose; release it at the native inverted somersault. Preserve movement, warning, health and wind owners. See docs/NIGHTWING_SIDE_FACING_1030.md.

## October30 Herald paired red claw lasers

- target17 Herald waves fire both living claws together. HL67 uses authored red BPFX laser packets and larger64px proper laser flashes, seven pixels into current claw tips. Preserve native warning/aim/cadence/hitbox and one shared launcher cue; let a committed warning/fire finish before native flight/spell selection. Broken claws lose rounds/flashes. Keep unshootable laser rules, native HP/hits/death and final desperation. Rebuild/evidence: docs/HERALD_CLAW_LASERS_1030.md.

## October30 Herald bottom landing Retina arrivals

- Latest user request supersedes HL51 four-height bands: every bomber drop owns a VH-36 impact and authored64x32 green/yellow/red Retina with8-step pixel fade. Its short position sweep locks within0.18s/first quarter of flight, then never drags the target. Draw after hull/effects; cancel on impact/claw/death/exit. Only original heavy bombs emit native radial volleys; ordinary drops retain direct danger and small impact without new radial/splash damage. Preserve cap, red dual claw lasers and native HP/final phase. See docs/HERALD_LANDING_RETINAS_1030.md.

## October30 Herald tornado lifecycle and lightning

- HH52 storm uses HH69 authored8-frame materialize/departure banks, actual metal yellow/red warning, accelerating visual summon channels, and actual lightning_ball projectiles. No storm FOV/plain impact star. Complete fade-in before contact danger; fade-out is harmless recovery. Every real alternating volley flashes only its emitting funnel through three alpha-preserving internal-lightning1015 levels over0.20s. Preserve native timing/collision/pressure/cancellation and prior red claws/Retinas/final phase. Sources and evidence: docs/HERALD_STORM_1030.md.

## October30 Herald gothic/counter/spiral contract

- HG70 depth orbs are a named weapon-interaction exception: missiles return foreground depth orbs to Herald for native1.25% maxHP damage; lasers shatter them into dangerous, unshootable red glass; ordinary gunfire passes through. Background boss remains protected except the tightly scoped reflected hit. No generic enemy-bullet interception change.
- Preserve actual reference skull gothic banks, continuous cast/raised/lower module poses, exact96-frame spiral alpha masks/sockets,48-flight/80-glass/128-owner caps and finite owner/death/stage cleanup. Sphere bursts must use skull-free glass banks; only skull bombs use full skull destruction. All graphic rotation/scale/glow remains offline authored. See docs/HERALD_GOTHIC_1030.md.

## October30 Dracodia possession / whole shoulders

- RD71 replaces the first-host intro: use actual toxic-rim portal bank recolored purple/red, not the rejected rectangular amethyst gate. Keep the UFO above/behind the drone, committed1.35s FOV, real data-bomb release/impact, code only after impact, authored rear/front/fade frames, moving bright red eye, overhead arm lift, shared-mixer robotic scream variants and white-covered host reveal. No new runtime sprite transforms/compositing.
- First-host arm destruction includes the whole shoulder and claw. Preserve pose-specific disjoint RD71 layers, exact hit alpha/opaque targets, native33.3/33.3/33.4 budget/core gate and five alpha-anchored native explosions with one sound. Do not restore broad strip masks or rectangular detached tiles. Late rebirth/copies/HP/death remain with native owners. Sources/evidence: docs/DRACODIA_POSSESSION_1030.md.

## October30 Dracodia physical claws / inset missiles / optic beams

- RD72 owns the armed first host's six-attack book: inset-tube purple missiles, actual extending swipe/grab/lift/fatal throw and rapid eye fan/sweep/360 beam. Retire the generic target17 first-host claw sidecar; never emit missiles/code from the claw tips. Same-frame body/eye/tube/Retina/arm collision anchors are required.
- Capture is initially nonfatal and spends no armor; it owns contact, locks only that seat's inputs, releases on actual arm destruction/cancel/stage change and invokes the native fatal-throw/death/life/respawn path only at release. Keep debug GOD functional and never fake death/HP/progression. Preserve RD71 whole-shoulder breakup, native arm/core gate and exposed-core roll/later forms.
- Keep fixed even directional/closure/warning/optic banks and source-authored alpha; no runtime sprite transforms or glow shortcuts. game.js edits are limited to the captured-seat input guard and scoped fatal playerHit bypass. Sources, native footage and verification: docs/DRACODIA_DEMON_1030.md.

## October30 Dracodia exposed-core ricochet

- RD73 supersedes the slow r25Route after both first-host arms are destroyed. Keep continuous reflected viewport motion, all24 authored source frames and measured full-silhouette/HUD margins; no waypoint teleport or stationary reset between barrages. Preserve native core HP, hit masks and later progression.
- Normal/Hard/Furious use255/290/330px/s and0.52/0.36/0.24s bomb attempts, with4/5/6 live D20 bombs. Keep committed landing points, original warning/flight/arming/damage/interception and death cleanup. Barrage9.6s, moving recovery0.7s. Do not restore the old four-bomb/112px spacing throttle. See docs/DRACODIA_RICOCHET_1030.md.

## October30 Dracodia corrupted Chronos and teal returns

- RD74 owns only Dracodia copied form8. Keep the new generated whole-body motion, immutable HC23 hammer bitmap/unit,1/2/4 difficulty combo, real throw/recall, dark chromium and icon-box gun handoff,7.2s crimson code rage and hand-origin wave. No round shield or old fire-fist fallback. Preserve native active HP and other-form progression; Stage5 remains unchanged. Speech uses the shared compact portrait plate after escaping the level camera. See docs/DRACODIA_CHRONOS_1030.md.
- The clarified flyover concerns teal Golden Aegis return balls. RR75 retains one native12HP hit and continues the same object over the Rider toward the far edge with authored depth/shadow frames. Never restore disappearance at impact, repeated damage, or runtime sprite scaling. Kaia ricochets and allied navigation remain separate. See docs/RIDERS_RETURN_OVERFLIGHT_1030.md.

## October30 Dracodia defeated-copy return

- RD76 owns only defeated copied-form returns with a surviving main life. Keep the covered arena transfer and fixed authored main-body scan, native HP pools/defeated lives and living morph owners. Repair missing main limbs only while other copied lives remain; the last life preserves broken limbs and uses original final destruction/reward. Never heal a life pool to repair anatomy. Preserve pause/retry cleanup and one return commit. See docs/DRACODIA_RETURN_1030.md.

## October30 Dracodia main-body ninja contract

- RD77 owns only the armed final main body: actual authored claw/depth/turn poses, committed ground-Retina dive and alternating jump slashes. Do not restore the confusing main-body barrage or generic target17 claw laser sidecar. Preserve exact same-frame part alpha, foreground damage/background protection, severed-claw warning/contact/impact cancellation and native HP/copy cursor/ending. Armless core missiles remain native. RD76 still repairs anatomy only on earlier defeated-copy returns; the final life preserves damage. See docs/DRACODIA_NINJA_1030.md.

## October30 Dracodia Luminaire contract

- RD78 inserts chest-origin Luminaire after two main-body claw decisions. Keep original generated orb art,48-frame rounded FOV/rising lower flood, held full red warning,0.9s active and harmless recovery. Use the native680x512 world field, never camera-following or triangular FOV. Upper-side pockets above halfway remain clear/visible; exact final warning spans own damage. Charge/body contact is harmless, foreground boss HP remains native. Preserve native arm breakup, voice cleanup, copy/arena-return/final-life rules and ending. No runtime sprite transforms or image-alpha animation. See docs/DRACODIA_LUMINAIRE_1030.md.

## October30 copied helicopter contract

- HC79 owns encounter2/form1 only:348px common body size,48fps source rotor,13 authored body banks,64-direction destructible left/right weapon pods with recoil and frame-owned gun/missile sockets. Keep committed dodgeable twin-gun lanes, native per-pod player Retina locks, rapid finite missile bursts, red non-interceptible sonic fronts and original Stage1 behavior. Preserve680px world-anchored12/28px-s digital-jungle parallax, wire download palette, native copied HP/return/final-life guards. Render current authored pages with fixed blits, including the six-phase directional tracer; do not restore legacy mixed/rotated helicopter plates or procedural projectile glow. See docs/DRACODIA_HELICOPTER_1030.md.

## October30 Neural Archon optics contract

- NB80 owns only the brain eyeExpansion. Keep32px eye-aperture launch,0.16s outward startup,42px maximum continuous warm red/orange/yellow/ivory core and pose-exact emitting eye overlays over the native hit flash. Body, warning, beam origins and damage must share the current source pose, without separate live interpolation or the old purple generic muzzle/hairline source. Native tell/HP/geysers/cloud/shield/copy-return/final-death owners stay intact. Render166 authored frames with fixed blits. See docs/NEURAL_OPTICS_1030.md.

## October30 Neural Archon night-storm contract

- NB81 owns brain codeGeysers presentation/committed target selection: single metal ground warning and authored1015 caster pulse, no per-eruption rectangular plates; varied seeded positions with an open escape flank, native plume-alpha damage/count/cadence, longer caster tell. Keep clean night clouds only in sky arena, fixed world3/9px parallax and actual scenery dim/recovery. Preserve NB80 eye optics, native brain HP/cloud/return and every other arena/form owner.54 glow poses and3 cloud plates use fixed blits; editable source, generated reference edit/prompt and checks are in docs/NEURAL_NIGHT_STORM_1030.md.

## October30 Phoenix turbo/core contract

- PH82 owns only the Phoenix cannon station: straight non-interceptible twin-pod bullet pairs alternate four measured muzzles; all lasers originate at the measured orange chest core with authored1015 charge, committed FOV and one13-direction beam. Keep native cannon HP/dependency/breaks, white hit feedback, later swoons, copied-life return and other form owners. Bounded visible-fire evasion must not teleport or read future input. Dark lava uses8 palette phases,48px animated viewport-edge walls and independent8/18px parallax.467 authored fixed-blit frames, editable sources and remaining legacy-swoon rendering scope are documented in docs/PHOENIX_TURBO_CORE_1030.md.

## October30 Order of the Phoenix contract

- PH83 supersedes the native cannon-destroyed Phoenix corner stage only. Keep four unique shuffled corner origins/no immediate cross-cycle repeat, continuous committed world paths and direction-matched authored poses, real depth turns/rolls,4.2s accelerating fire-wind1015 charge,8-12 whole-body coded-fire perspective copies, charge-down/offscreen exit/foreground recovery. The caster remains world-centred and its250px wind fits both camera extremes. Echo targets commit; actual solid source spans hurt only in foreground. Preserve native pod/HP gate, hit flash, destroyed-claw contact cancellation, copy return/final anatomy and PH82 cannon station. Complete the combo before applying timed donor return; never heal. All702 frames use fixed blits and editable Aseprite sources. The PH82 atlas row-flush repair retains complete original frames. See docs/ORDER_OF_THE_PHOENIX_1030.md.

## October30 Dracodia terminal/reunion contract

- RD84 owns final death only after every life pool is exhausted. Preserve24 accelerating actual formation-lightning beats, increasing idle/raised scream alternation/white1015 source material, original-pack electric explosions, all9 stage/coastalX downloads and56-piece exact source-body shatter. Use the existing BLUE METAL-FRAMED blue_rift lifecycle, not an energy-only ring. The newly generated above-ground riverfront has native current aircraft (all other8 pilots), animated water and far/near parallax; no generated ship designs. Keep pause/reset/reduced motion, fixed authored blits, source-conserving fragments and the sole native reunion reward/Stage Clear/debug-return guards. Do not restart on repeated final-death notifications or alter normal copied-life breaks/HP. See docs/DRACODIA_TERMINAL_1030.md.


## October31 straight Herald glass and inscribed storm

- Mike explicitly removed shard bounces. HH52 skull-bomb glass, HS53 spell glass and HG70 depth-orb glass fly outward once and leave view; never restore edge reflection or clamping. Preserve dangerous ordinary/unshootable glass, shootable skull bombs, missile depth returns, native damage and bounded owner cleanup. HR87 adds the existing line/circle-built seal, spin, pulse and burst before tornado release with a complete5.4s tell. Keep the existing metal warning, red lightning/orbs, lifecycle/contact and recovery. See docs/SEWER_PORTAL_HERALD_1031.md.

## October31 stone chamber and actual PixelLab gated return

- SC86 restores the original Stage7 master stone chamber after Warden defeat, continuous northward camera/source travel, live approach steering, green gate inside the measured aperture, and authored ship entry/close/flash. Hand off to the existing native campaign finish for one reward/ledger/direct Stage8 entry; never duplicate rewards or restore the generic connector portal. Dracodia ending/reunion blue gates use actual pixellab_void_1017 metal-rimmed frames, not portal_lifecycle_1011 energy-only art or the Stage8 color router. Fixed384px green/320px blue cells, source hashes and owning rebuild are in docs/SEWER_PORTAL_HERALD_1031.md.


## October31 Dracodia articulated rakes and double jumping strike

- RD88 replaces only RD77 physical main-body combos: source-preserving fixed pauldrons, shoulder/elbow/wrist articulation, edge-to-centre left/right rakes, coiled background retreat/north leap, two alternating jumping strikes and finite recovery.236 authored poses/708 even part entries share768x640 chest root and410px unit. Actual opaque part targets, source-alpha claw contact and traversed-frame sampling stay together; native warning fields use baked swept footprints. Retinas/metal sign render above the body.
- Preserve native3380/4290/5330HP, background protection, real part flashes/break cancellation, surviving-arm selection, exposed-core missiles, third-decision Luminaire, copied forms/returns and terminal ending. Never restore whole-arm-only pivots, disconnected shadow attacks, hidden landing damage, or runtime sprite transforms. Source/builder,99 focused checks and current full native final-main-life film: docs/DRACODIA_EXTENDED_CLAWS_1031.md.


## October31 boss balance and Normal fifth-stage finale

- BA99 owns final-spawn Event Horizon health:3200*DIFF.eHp, native co-op1.5 and NG+1.25 once. Nightwing's future ace life is3600*DIFF.eHp with the same native modifiers; carrier parts/hull are unchanged. Do not restore the stacked Horizon stage ramp. EH57 keeps continuous shared0.60rps hull/core/laser rotation, but fires warned rank-specific pulses with real off gaps and foreground recoveries. Its return is protected. Retain real gated white hit flashes, exact50% transition, actual core laser art/audio and unshootable ordinary rounds.
- TS58 Hard now uses3 forward lanes,3 mortars,4 rain impacts and6 lamp bubbles; Furious retains5/4/6/10. Preserve all three original water-wall alert timings and sounds on both ranks, fan origins, finite cleanup and protected Slip N Slide re-entry. Do not accelerate warnings via a blanket dt multiplier.
- NF100 ends Normal at the real Stage5 Chronos defeat, autosaving earned rewards immediately; existing results/Forge settle before the Earth/HQ return. Keep the native-size avatar-free Hard/Furious menu, accurate difficulty copy, difficulty-preserving fade to PILOT and fresh Stage1 run. Actual Normal completion must survive a fresh operation in its archive and reopen the choice when loaded. Save failures must be honest and block restart. Debug/preview runs never grant completion. Normal NG+ also stops at5; preserve pre-clear Stage9 bonus detour compatibility. Older Normal campaign6-8 saves route to this choice. Do not bump CAMP_SAVE_VER or auto-launch the Stage6 cinematic.
- Dracodia new difficulty designs and the pending Stage6/9 concept pairs remain approval-only. No new Dracodia attacks/art were activated. See docs/BOSS_BALANCE_NORMAL_FINALE_1031.md and docs/qa/boss_balance_normal_1031/. Targeted native checks45 passed; full suite retains the same five pre-existing flash/Chronos-opening/Stage-X failures. Core game.js SHA024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de stays unchanged.
