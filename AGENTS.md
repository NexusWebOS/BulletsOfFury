# Bullets of Fury — Codex project guide

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
  and Mike's October18 PixelLab Stage8 phase1–3 modular redesign are named
  exceptions. Stage8 phase3 has its main body plus exactly Hammerboss, helicopter,
  Harrier and volcano forms. Approved miniboss aperture mechanics and the two
  independent Tempest ships are separate encounter designs.
- Player death remains hit, anchored burning spin through 540–900 degrees, crash,
  then shock ring and explosions. Space deaths use the spaceship.
- Read `docs/ATLAS_REPACK_0903.md` before editing an atlas. Register sheet and cell
  changes together; generated manifests require their owning build workflow.

## Combat warnings and audio

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
