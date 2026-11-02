# Stage6 solid aircraft â€” November1

Mike replaced Stage6 whole-hull animation with one canonical frame per aircraft.
Live owner: `assets/stage6_airframe_1101.js`; registry:
`assets/stage6_airframe_art_1101.js`. It loads after the Stage4/5 refits and
scopes changes to regular Stage6 sky actors. No core/test edits, commit or push.

Current review: <http://127.0.0.1:8805/current/stage6-solid-hulls-1101.html>.
Full guide: <http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage6-solid-hulls-1101#enemy=stage6-flyby-charge>.

## Current art and behavior

- Six new canonical plates: black/neon-blue fighter, navy/white fighter,
  teal/gray twin-gun-pod strike fighter, blue/teal heavy wind jet, navy/white four-engine
  bomber and black/blue four-engine bomber.
- The existing Zephyr, Gale, Stratus and Tempest helper designs are retained,
  frozen to their actual idle0 source pixels. Native wind/helper attack books,
  shields, health and cues remain; no generated attack/roll body reel is used.
- Each body uses one proportional scale, fixed192px cells and one stable
  fuselage pivot. Direction cells are exported from that same canonical plate;
  live rendering never rotates or squashes the static hull. Whole-body recoil,
  morphing attack frames and alternating designs are removed from this path.
- Six-step native1015 light follows the source's actual blue/teal emissive
  pixels, with1/2px hard spill. It is independent from the fixed hull geometry.
  White damage flashes retain priority and expire on the native clock.
- Separate animated exhaust leaves each measured nozzle: two for fighters,
  four for heavy/bomber plates. Gun barrels and exhaust anchors are measured
  on the chosen source PNGs and checked against all32 exported alpha frames.
- Compact blue/teal muzzle reports replace oversized centre flares. The old
  unkeyed `t_muz0/1` nose overlay is suppressed only while a revised sky actor
  draws. No muzzle/engine effects are painted into the hull source.
- Legacy eShoot/eMG direct rounds and eShootT rounds share the new weapon
  mouths. New fixed-gun aircraft fire along their displayed facing direction;
  physical missiles preserve native Retina/interception/steering grants.
  Ordinary rounds remain unshootable and use readable compact teal ammunition.
- Native steering, volleys, cues, shields, whole-hull HP and deaths remain.
  Collision dimensions follow the revised regular jet footprint. Preserved
  wind/helper actors keep native dimensions/pools.
- Stage6 ground-turret construction is rejected before actor creation. All
  three guide cards and Stage6-only encyclopedia entries are removed; shared
  turret entries retain their other stages. The campaign placement factory
  already guards a null result, so its queued callbacks remain safe.
- Plain opening stealth-bomber actors are excluded. The opening cinematic,
  allied wing, bosses/minibosses, Rough Riders, StageX and other levels retain
  their existing owners. Native Tempest helper departure may self-destruct;
  this is not a hidden HP write in the recorder.

## Sources and rebuild

Run `python _BUILD_SOURCE/build_stage6_airframe_1101.py`, followed by
`python _BUILD_SOURCE/update_stage6_airframe_metadata_1101.py`.

Six selected built-in image_gen PNGs are retained under
`_BUILD_SOURCE/stage6_airframe_1101/`, with style reference, generation notes,
hashes, source pivots and measured sockets. Four preserved sources come from
the existing complete R46 wind/helper banks, taking only idle0. The exporter
writes10 canonical models and23 fixed body/glow/effect banks together. No
original atlas or original wind source is modified. No PixelLab/SpriteCook
credits or uploads were used. Generated animation strips were not requested.

## Verification and films

Evidence: ignored `_shots/stage6_airframe_1101/`.

- 66 native Furious sortie/damage checks pass across27 cases: same actual
  canonical frame through native flight/attack, finite coordinates, real
  exhausts, native hit pixels/expiry, no ground turrets and preserved entrance.
- 15 focused native checks pass: real gun/muzzle releases, live ordinary-round
  immunity and teal rendering, actual1015 pixel brightness, Normal/Hard launch
  and health samples, native burning/crash/death and gun cancellation.
- 5 final teal gun-pod checks pass: fixed hull/native HP, actual MG mouths and
  unshootable rounds, four hollow barrel anchors, native hit pixels/expiry and
  no browser errors.
- 33 final source geometry/hash/actual-alpha weapon-nozzle checks pass.
- 27 production-code/selected-art integrity checks pass. Retained registry
  snapshots prove the26 untouched takes still match their actual model/effect
  banks; the corrected teal gun-pod model has a fresh take with current hashes.
- 27 published clips seek/play/decode video and audio in real Chromium.
  All H264/AAC files also fully decode with ffmpeg. No page/console/asset or
  mixer-tap errors. Delivery1280x800 at30fps; native simulation59.1â€“60.1fps.

The isolated Furious films use movement inputs and a labelled invulnerable
observer; they do not alter enemy HP, phases or attack clocks. One interrupted
take was replaced while26 clean takes were retained. Recording hides external
hardware gamepads from the fixture so they cannot pause or steer the sample.
A final visual review replaced the teal candidate’s pointed missile-shaped pods
with actual paired machine-gun barrels to match its native attack, then
re-recorded only that model. The movies demonstrate native attacks/art, not
campaign difficulty completion.

The native strike API queues a warned flight and returns null. The recorder
therefore observes its actual `fb2FlightSpawn` owner with the authored mode,
rather than constructing an incomplete `s6strike` shell without its flight
state. Bomb/stream/charge and Tempest helper fixtures keep their native owners.

`node --check assets/game.js` and the new runtime pass. The required full
`node _BUILD_SOURCE/test_fl.js` still exits1 before assertions/final summary
on missing ignored `UNUSED_ASSETS/retired_art_1022/manifest.json`, the recorded
baseline blocker. Full-suite success is not claimed.

Record: `_BUILD_SOURCE/record_stage6_airframe_1101.py`. Publish after review:
`_BUILD_SOURCE/publish_stage6_airframe_1101.py --install`. Current guide160
cards:27 refreshed Stage6 clips, three ground-turret cards removed, every
unrelated card retained byte-for-byte. Original films/files remain archived.
