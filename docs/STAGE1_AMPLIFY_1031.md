> Current revision: see [Stage1 physical weapons](STAGE1_PHYSICAL_WEAPONS_1031.md). The following records the preceding pass.

# October31 Stage1 enemy animation and physical firing pass

Mike selected five regular enemies from the local enemy guide. The current owner
is `assets/stage1_amplify_1031.js`, loaded after the existing encounter/refit
owners. It preserves their native HP, damage/death/reward and combat rules.

## Result

- **Gunboat:** the existing two destructible weapon modules now carry the
  authored small machine-gun turrets. They alternate solid gold rounds straight
  south, with short attached flashes and native Heavy MG audio. Ordinary rounds
  cannot be shot down, including before their first update.
- **River Corvette:** the native alternating broadside keeps its actual hull
  sockets. A short, compact source-frame muzzle reel replaces the oversized
  later flash override and follows the current barrel position.
- **Delta Fighter:** the actual current AF21 hull/drift pixels have fixed source
  heading cells, measured twin gun sockets, two separately animated exhaust
  reels and attached muzzle frames. Ordinary sorties approach, turn into a
  committed gun pass, then peel out with limited turn rate and consistent forward
  speed. The paired native flyby remains intact and uses the same revised art.
  Shared lateral dodges steer the flight rather than sliding the hull sideways.
- **Strike Bomber:** visible gold authored bombs alternate from its wing/bay
  sockets throughout the pass, including the lower screen. The former eight-drop
  and 68%-height stops are removed. The aircraft exits fully; native ground
  Retina, fall/impact timing, damage and audio remain the attack owners.
- **Heavy Jungle Tank:** its existing twin-barrel turret fires exactly two
  physical Jungle missiles after the native targeting/lock-beep window, from
  measured barrel mouths with attached rocket flashes. It brakes to fire and
  retains native tracks, terrain legality and ground-traffic clearance. It can
  engage targets outside the former120px centre column.

The two small core changes are the native naval MG's straight round replacing
its spread, and recognizing the explicit Delta/flyby route in the generic
aircraft edge clamp. The late owner also prevents the generic age-based movement
push from fighting these explicit routes. Revised actors start with a real birth
clock rather than a random initial age that could spend their entrance window.

## Art ownership

Rebuild with `python _BUILD_SOURCE/build_stage1_amplify_1031.py`.

Output: `assets/game/levels/stage_01/enemies/amplify_1031/manifest.json`, eight
sheets and `assets/stage1_amplify_art_1031.js`. There are993 fixed directional
frames, all in even square cells with centred pivots and one proportional scale
per bank. Sources, crops, emitter pivots, removed static exhaust rectangles,
socket coordinates and SHA256 hashes are registered in the manifest. No shared
atlas was repacked and no new paid art was generated.

Sources are the current AF21 Delta idle/drift plates, S1M exhaust/muzzle and
actual twin-barrel turret, native gold MG cells, native `lz_bomb`, and the Jungle
missile frames. The two frozen blue Delta exhaust patches are removed only in
the derived hull bank and replaced by the animated source reels. Directions are
baked into asset cells; the revised native Delta renderer does not rotate an
idle sprite canvas. The tank turret and revised rounds also select baked cells.

## Native verification

`_BUILD_SOURCE/probe_stage1_amplify_1031.py` runs real Chromium through
`shoot.py`, native spawning, simulation and drawing.38 focused checks pass in
Normal and Furious: attacks, straight slugs, physical sockets/flashes, multiple
Delta headings/constant forward speed/full exit, late bombing, locked paired
missiles beyond the old column, source-bank preloading and interception rules.
Actual damaged pixels flash white, then recover after30 native frames with an
expired flash timer. The Delta renderer reports zero runtime canvas rotations.
No page/console/render errors were observed.

Required syntax checks pass. `node _BUILD_SOURCE/test_fl.js` exits1 **before
assertions or its final summary** because this checkout lacks
`UNUSED_ASSETS/retired_art_1022/manifest.json`. This is a blocked full-suite run,
not a passing suite or an assertion-baseline comparison.

## Current local previews

`_BUILD_SOURCE/record_stage1_amplify_1031.py` records actual native RAF sorties,
shared-mixer sound and input-only observer movement/fire. Aircraft/tank HP,
attack clocks and movement states are not edited during the footage. The
observer is invulnerable; these are isolated animation/attack demonstrations,
not campaign difficulty measurements. The fixture disables unrelated campaign
reinforcements and external gamepad polling. It clears stray input taps before
capture and verifies the source hashes remain unchanged while recording.

Six current cards replace only their local guide media:

| Card | Length | Native attack events |
|---|---:|---:|
| Gunboat |12.33s|7 straight rounds|
| River Corvette |12.63s|10 rounds|
| Delta Fighter / Flyby |5.25s|24 rounds across the pair|
| Delta Fighter / Gun Run |5.74s|8 rounds|
| Strike Bomber |7.07s|9 bomb drops and full exit|
| Heavy Jungle Tank |16.12s|2 paired salvos /4 missiles|

MP4s have constant30fps H264 video, AAC audio and faststart. Native simulation
rates are58.7–60fps. All six streams fully decode and contain actual shared-mixer
playback, including MG, bomb/impact and lock/missile cues. No pause/player death,
unrelated actors or browser errors occur in the accepted footage.

The publish helper `_BUILD_SOURCE/publish_stage1_amplify_local_1031.py` validates
recording telemetry, fully decodes each MP4, derives posters and registers only
the six scoped media paths plus the copied guide HTML/manifest in the local
server's existing whitelist. All163 cards remain; the other157 original clips
and the original full compilation are retained. The page labels that compilation
as an archive. No GitHub publication, commit or push is part of this pass.

Local guide:
`http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage1-amplify-1031#enemy=stage1-s1boatgun`

Current ignored evidence: `_shots/stage1_amplify_1031/` contains source contact
sheets, native screenshots,38-check receipt, native traces, six accepted films
and telemetry, full-suite error, decode/publish receipt and Chromium guide
playback checks. The old invalid capture attempts were overwritten before these
cards were installed; the original downloaded review library is unchanged.
