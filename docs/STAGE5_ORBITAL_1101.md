# Stage5 orbital roles — November1

Live owner: `assets/stage5_amplify_1101.js`, loaded after S411. Art registration:
`assets/stage5_amplify_art_1101.js`. No changes to the current `assets/game.js`
or test source in this pass; existing user work remains. No commit or push.

Current local films: <http://127.0.0.1:8805/current/stage5-orbital-1101.html>.
Full guide: <http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage5-orbital-1101#enemy=stage5-s5frigate>.

## Behavior

| Enemy | Current behavior |
| --- | --- |
| Frigate | One measured south beam; same muzzle/direction/full alpha width for FOV and contact. Source alpha is18/64px across; actual26px beam width matches its warning. |
| Rammer | Normal/Hard/Furious entry115/185/240px/s, windup.64/.42/.30s, committed charge440/650/850px/s. Fixed authored heading cells and twin exhaust. |
| Skimmer | Finite curved flybys, both animated thrusters; fixed twin weapons release only while nose faces the pilot. |
| Gravity | Existing magma-orb animation recolored violet/white with luminance and alpha retained. Actual own-pixel1015 companion uses six native PXG_STEPS and1/2px hard spill. Hard/Furious fire full12-way rings; Normal has an opening. These explicit energy balls remain interceptable. |
| Minelayer | New swept-wing minelaying ship, rear-bay frames, fast finite sortie and stationary mines. Three-HP mines arm after.6s, proximity45px, explosion65px contact,8s lifetime. Real primary fire can destroy them; proximity uses native playerHit and explosion. |
| Satellite | Existing Retina/beep owner, twin actual racks,2/3/4 missiles with.16s ripple. Missiles retain native locks, homing, interception and dodge commitment. |
| Portal Mine | Whole-hull registered rotation cells throughout its attack.6 directions Normal,9 Hard/Furious. Ordinary rounds cannot be shot down. |
| Repair | Swift side entry following its nose, fast vertical turn, measured twin-tip warnings and falling beams; Normal/Hard/Furious native hull HP multiplier1/1.65/2.15. |
| Station | Two purple projectile spreads, then one charged beam. Medium once-only native absorbing shield38EHP. Shields, real hits and break feedback remain native. |
| Leech | No ranged shots. Sixteen claw spread/clamp/recovery poses, homing pounce and connected front-claw contact through native playerHit/dodge/death. |
| Voidreaver | Direct and adaptive factory gates reject both legacy IDs across all stages. Removed from difficulty rosters and two active encyclopedia entries; original sources/old films remain archived. |

The unchanged Interceptor and all unrelated stages retain their previous owners.
Old queued/EP13 alternate attacks are disabled only for these ten replacements.
Native whole hull budgets, shield absorption, visible damage flashes, anchored
burning-spin/crash/death, rewards and ordinary-bullet immunity remain owners.
Real defeat cancels pending missiles, beams and attached flashes. Already laid
mines remain independent hazards until destruction, contact or expiration.

## Art and rebuild

Run `python _BUILD_SOURCE/build_stage5_amplify_1101.py`, then
`python _BUILD_SOURCE/update_stage5_metadata_1101.py`.

Two built-in image_gen original PNGs and exact prompts are retained under
`_BUILD_SOURCE/stage5_amplify_1101/`. Minelayer uses generated rear-bay and bank
poses. Leech uses a complete claw reel registered around its red core. The
generator supplied a different layout for the Minelayer heading rows; the
exporter uses the complete bay/bank reels and source-derived registered
directional cells. No live sprite rotation substitutes for these banks.

Four approved complete aircraft banks are reused; four other whole native
orbital plates are extracted from the owning Stage5 atlas without editing it.
Source hashes, proportional scales, pivots, even160px body cells and inherited
64/128px projectile cells are recorded in the manifest. The violet ordnance
and1015 companion derive from actual Stage2 magma art. Original sources and
palettes remain intact. No PixelLab/SpriteCook credits or uploads were used.

## Verification and films

Evidence: ignored `_shots/stage5_amplify_1101/`.

- 85 native Normal/Hard/Furious behavior/hit-pixel/interception checks pass.
- 21 native damage, shield, beam/contact, actual player mine interception,
  mine detonation and defeat cleanup checks pass.
- 7 final checks pass: same-frame1015 pixel brightness, current beam screenshots,
  real Leech player damage and all-stage Voidreaver suppression.
- 23 asset dimension/hash and unchanged core-source capture checks pass.
- 10 current films seek/play/decode video and audio in real Chromium. All MP4s
  fully decode with ffmpeg; H264/AAC,1280x800,30fps delivery. Native simulation
  averages59.2–60fps; no page/console/asset/audio-tap errors.

The ten isolated Furious films use actual movement inputs and an explicitly
labelled invulnerable pilot. Enemy HP/phases/attack clocks are not written
during filming. They demonstrate attacks and animation, not human survival
certification or a full campaign playthrough. Gravity's final1015 companion
was re-recorded separately; the other nine clean takes were retained.

`node --check assets/game.js` and the new runtime pass. The required
`node _BUILD_SOURCE/test_fl.js` exits1 before assertions/final summary because
this machine lacks ignored `UNUSED_ASSETS/retired_art_1022/manifest.json`, the
same recorded baseline blocker. The full suite is not claimed green.

Record with `_BUILD_SOURCE/record_stage5_amplify_1101.py`. Publish using
`_BUILD_SOURCE/publish_stage5_amplify_1101.py --install` after verification.
The publisher replaces only ten Stage5 cards, removes the one active
Voidreaver video card, preserves all unrelated cards and adds a focused
ten-film page. Current full guide:163 cards; earlier media files retained.
