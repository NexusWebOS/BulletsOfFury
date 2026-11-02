# Stage3 ice roster / October31

Mike requested larger regenerated Shard Dart and Cryoeye, actual turning
interceptors with only two physical guns, ice Carrier ammunition, island-mounted
laser/sonic fixtures, blue pressure waves and a distinct mine-dropping ice jet.

## Current ownership

`assets/stage3_amplify_1031.js` (I31) loads after the Stage1/2 owners. Its scoped
spawn wrapper retains the native difficulty-scaled HP and death/reward owners,
removes the obsolete suicide/drone controllers only from the six revised types,
and routes their native `s3IceTick` updates. Unrelated enemies and bosses remain
with their existing owners. Stage1/2 art, combat and videos are preserved.

- Shard Dart uses a larger silver/blue regenerated dagger hull and restrained
  upright banking frames. No barrel roll, inverted frame or upward flip enters
  its live movement. Twin downward ice rounds leave its forward guns.
- Interceptor and Ice Interceptor follow curved, bounded-turn flight with actual
  eight-view source hulls, two measured cannon mouths, short attached flashes,
  animated blue exhaust and visible blue-white rounds. No live canvas rotation
  substitutes for their directional art. The source metadata records all eight
  two-mouth registrations.
- Glacier Carrier retains its actual four authored idle frames and emits paired
  ice bullets from the visible lower barrels.
- Cryoeye has four actual cannon apertures, a sixteen-frame charge/recoil/recover
  bank, four committed green/yellow/red lanes and simultaneous N/E/S/W beams.
  The beam is the actual Stage2 laser texture, palette-exported blue-white. Its
  fixed cross is released after a1.1s warning, held0.8s, then recovers. Native
  lethal damage clears the active beams and pending lanes.
- Laser/sonic ground fixtures reserve their full visible footprint against a
  mask measured from the real Stage3 ice master. Texture-averaged eight-pixel
  cells exclude transparent water/dark cliffs; edge erosion plus25 footprint
  samples keeps the complete base on island tops. The fixtures keep their world
  terrain anchors as the background scrolls. No per-wave placement hacks.
- Sonic uses the original pressure-wave shape with a blue palette. Its old early
  red-pressure renderer is bypassed only for I31 ordnance, before the final
  projectile owner. The native pixel test checks the actual `drawBullets` path.
- Ice Mine Bomber has its own magazine/bay aircraft, actual turning frames,
  a finite mine-laying pass and turbo escape. The mines are stationary pulsing
  native projectiles that player weapons can destroy; this is not a suicide
  Glacier Carrier. Ordinary ice bullets/laser shots and sonic waves reject
  offensive interception from birth; physical missiles elsewhere are unchanged.

Native white hit flashes and expiry are preserved on every revised hull and
fixture. The new hulls use the existing native rectangular combat footprints;
this pass does not claim an alpha-precise enemy collision-system migration.

## Art / exact rebuild

Four complete generated source sheets are retained in
`_BUILD_SOURCE/stage3_amplify_1031/`, along with actual Carrier source frames and
the original sonic/base reference images. `PROMPTS.md` records the final prompts.
Generation used the built-in `image_gen` tool with local identity references;
no SpriteCook/PixelLab credit spend or signed URLs.

`python _BUILD_SOURCE/build_stage3_amplify_1031.py` exports five model banks,
32 registered sheets and1805 cells under
`assets/game/levels/stage_03/enemies/amplify_1031/`. Every cell is a fixed even
square with one shared proportional scale/common pivot per model. Generated
source rectangles remain in the manifest. The eye's joined source rows use
explicit measured rectangles. Hull headings select distinct drawn poses;
oriented effect/turret textures are exported offline into registered cells.

The owning manifest and `assets/stage3_amplify_art_1031.js` are written together.
No production atlas was repacked. `ART_TAXONOMY.json` records `i31_`. The scoped
catalogue migration in `tools/enemy_atlas_1013/apply_stage3_amplify_1031.py` keeps
397 entries and updates only the six types plus the two Stage3 fixtures. The
atlas builder applies this migration after the Stage2 migration. Its adapter
shows I31 phases/four active beams, hides obsolete pattern buttons and clears
unrelated level-entry radio only in its isolated preview setup.

## Sound assignments

| Attack | Existing shared cue |
|---|---|
| Twin ice guns / Carrier | `enemyMachineGunHeavy` once per pair |
| Cryoeye / laser-turret windup | `bossWeaponCharge` and native warning ticks |
| Cryoeye / laser release | `enemyHeavyLaser` |
| Sonic charge / release | `razorbackCharge` / `razorbackPressure` through `stageRevisionCue` |
| Mine drop / boost | `bombDrop` / `turbo` (decoded `jetDash`) |

There are no new out-of-band audio timers. Silent volley partners stay silent.
The laser turret's duplicate MG cue was removed; its final movie decodes only
the laser release. Capture receipts record actual decoded mixer cue activity,
peaks and browser errors, rather than asserting that a sound method exists.

## Verification and local review

- `node --check assets/game.js`, I31 and the atlas adapter pass.
-40 focused native smoke checks pass: actual attacks/turning/upright poses,
  unchanged native HP, damaged pixels and flash expiry for all eight types.
-26 cleanup/source checks pass: native lethal damage and beam cancellation,
  actual blue projectile pixels, eight views without canvas rotation, complete
  island placement at five scroll positions and real player interception of a
  separated mine. The geometry test initially read the Stage2 manifest; it was
  corrected to Stage3 and only that file check was rerun. No gameplay bypass.
-3 interactive atlas checks pass: new Cryoeye from its first actor, four live
  beams/current phase and no obsolete pattern buttons or browser errors.
-14 final gallery checks pass: preserved non-Stage3 links, all13 refreshed ice
  cards, all eight clips playing/seeking with decoded audio, and no browser or
  asset errors. The full owning art rebuild is byte-identical across every
  runtime bank, manifest and registry. Total focused checks:84/84.
- The mandatory `node _BUILD_SOURCE/test_fl.js` exits1 before assertions/final
  summary: this machine lacks
  `UNUSED_ASSETS/retired_art_1022/manifest.json`. No archive was fabricated and
  no full-suite pass is claimed. `game.js` retains LF; `test_fl.js` retains CRLF.

Eight clean native Furious recordings use normal movement input and an explicitly
invulnerable observer, with no enemy HP/phase/timer edits during capture. These
are isolated animation/attack demonstrations, not campaign balance certification.
The preview setup clears unrelated Stage3 entry dialogue. Files, source hashes,
native frame rates and mixer receipts are under `_shots/stage3_amplify_1031/`.
Movies are H264/AAC, constant30fps, fast-start seekable and fully decoded before
publication; browser playback also checks seeking and decoded audio.

The local full guide remains164/164 cards. All13 Stage3 cards point to the eight
current native films; every non-Stage3 card/video is preserved exactly from the
Stage1/2 current manifest. Original full reels remain explicitly archived.

- Full guide: `http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage3-ice-1031#enemy=stage3-cryoeye`
- Focused films: `http://127.0.0.1:8805/current/stage3-amplify-1031.html`

The scoped local publisher updates only the review server's route overrides,
leaving archived media intact. No commit, push or GitHub publication in this pass.
