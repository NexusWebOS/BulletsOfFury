# October 10 — fixed animation anchors and modular Stage I candidates

Mike's current requests: repair the drifting enemy/pilot sheets; extend the
approved Hammer explosions to 16–32 authored frames; make small Stage 2/3 flyers
shieldless kamikazes; add large fire and ice jets; turn the mountain geysers
sideways from the upper edges; and generate a modular Neo Geo preview of the
current Stage I miniboss, Furious miniboss and boss without replacing them.

## Shipped changes

- The 24 existing enemy/ship motion banks register their fixed chassis on every
  reel. The earlier seven-pixel search was silently saturating on source drift
  as large as 33 pixels. Masked translation now covers the real displacement,
  preserves common scale and fails rather than accepting a saturated match.
  Furyship also receives a final native-pixel cockpit correction after scaling.
  All nine pilots retain the original nozzle rigs, native dimensions and bank
  poses. Their eight-frame loops remain eight frames; this is an anchor repair.
- Hammer's electrical corona, violet/orange plasma blasts and fire/smoke rings
  each have **32 different authored frames**, 96 cells total. The accepted source
  sheets have clear cell borders. The sequence retains dialogue, white portrait,
  reactor lock, finishing missile, successive electric pops, the existing whole
  two-arm/head acting plate, rupture, cutaways and return home. Its engine-death
  draw/tick owns the new effects and excludes the legacy flat grey smoke discs
  and overlaid star-burst emitters.
- Stage 2 small air units `ash`, `skim`, `disc`, `eye`, `lance` and Stage 3 air
  units `s3mine`, `s3interceptor` lose their shields and autonomous gun volleys.
  They enter, warn for 0.6 seconds with the original Retina, snapshot a target,
  then accelerate into one committed dive. Contact uses native player damage
  and native enemy destruction, with no suicide score/pickup reward. Ground
  vehicles, props, bosses and minibosses keep their existing roles.
- Each stage adds a new **large south-facing jet with 16 authored frames**.
  The fire jet fires thermal needles; the ice jet fires shards. A 0.7-second
  lock tell precedes three twin-gun bursts, followed by a recovery interval.
  Three timed waves join the ordinary stage plan and skip active boss slots.
  Ordinary hitboxes, locks, HP routing, impacts, sound dispatch and white flashes
  apply. The jets have separate shipping assets in `arcade_jets_1010`.
- Mountain vents launch from the upper left/right edges. The original authored
  fire column rotates 90 degrees inward. Damage follows that horizontal lane,
  and release still works at the geyser cap. Stage 2 queues the column before
  play. Player/weapon geysers retain their vertical volumes.

## Stage I preview only

Open `docs/previews/neo_geo_stage1_1010/index.html` through the game server.
The page embeds an isolated copy of the actual renderer and native stage art,
player and health bars. It offers green Razorback, red Furious Razorback and
Overlord, current-art comparison, speed/pause controls and module break buttons.

Each candidate hull has **16 unique cells**. Twelve separate module banks have
four unique cells each for recoil/fire, missile doors, turbines and rotor art.
Weapon sockets remain empty in the hull plates; weapons are attached separately.
The helicopter rotor rotates independently around its hub. Break controls detach
only that component, spin it away, then consume it in the 32-frame explosion reel.
There is no alpha fade of the broken module.

These three candidate assemblies are **not imported by the shipping game** and
do not alter the current encounter art, pool values, patterns or module targeting.
The new enemy jets and Hammer effects are wired into gameplay. Other boss/roster
families still need their own later 16–32-frame art passes; this update does not
claim that every sprite in the game has that many frames.

## Ownership and verification

- `_BUILD_SOURCE/build_arcade_finish_1010.py` owns the 96 effect cells and registry.
- `_BUILD_SOURCE/build_arcade_candidates_1010.py` owns the 128 candidate/jet cells,
  shipping jet registry and preview-only registry together.
- `_BUILD_SOURCE/build_smooth_motion_1009.py` owns the repaired prior motion banks.
- Exact imagegen prompts, accepted/rejected returns, reference exports, cell
  registrations and SHA256 provenance remain in the two `arcade_*_1010` source
  folders. No atlas is repacked and no procedural sprites are painted.

`node --check assets/game.js` and all changed runtime scripts pass.
`node _BUILD_SOURCE/test_fl.js` reaches its final BUILD OK summary: **7,952 passing
assertions, 0 errors, exit 0**. The native farewell regression passes **16/16**.
The new Chromium probe passes **63/63**, including actual XART pixels for all
24 fixed cores, 32 unique renders per effect, jet frames/white flashes, locked
shieldless dives, contact destruction, horizontal damage and native preview
module separation and fixed mounts across all 16 candidate hull frames. Page,
console and asset errors: **0**.

`_BUILD_SOURCE/record_arcade_1010.py` streams real canvas frames to 30 FPS clips
under ignored `_shots/arcade_finish_1010`. Combat clips are staged demonstrations
with an invulnerable test pilot and cancelled intro overlays; they do not measure
Furious balance. Farewell and all three candidate clips were visually inspected.
`docs/qa/arcade_motion_1010.json` records the checks; temporary screenshots and
videos stay out of Git. Existing staged/unstaged guide edits and unrelated scratch
files are preserved.

The app tools expose no setting for changing chat submissions to queued mode;
the work continued with the user's live instructions instead.
