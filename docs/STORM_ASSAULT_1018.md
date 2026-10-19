# Storm Sovereign assault — October 18, 2026

The final-quarter controller cleared its glow every frame, and the road renderer
still looked for legacy chase mode names. The phase now visibly overcharges the
whole authored hull before a committed south ram, an enlarged northbound overhead
return, and sustained pursuit. Existing damage, shield thresholds, module HP,
unshootable lightning and native defeat/reward paths remain authoritative.

- Overload tells: Normal2.15s, Hard1.95s, Furious1.75s, Easy2.40s. Ram0.82s,
  offscreen hold0.26s, overhead return1.85s, scale2.45 to1.0. The overhead hull
  remains outside the combat plane. Pre-pursuit burst protection still commits
  the attack; exposed pursuit damage multipliers remain2.0/2.1/2.2/2.3.
- The background road speed eases from480 toward710 during overload,1180 on the
  ram,1080 during the return and960 in pursuit. This changes the visual road
  offset only; it does not advance the stage plan or spawn waves.
- The approved chip library supplies engine revs, lightning crackle, discharge,
  charge/ram, gun, missile and bomb cues. The owned engine stops on death/stage
  exit and obeys the existing pause, mute, visibility and mix controls.
- Live comms explain the four generators, multi-Retina missile salvo, exposed
  core/weapon pods, incoming lightning wing and overload/chase. Choose Decker
  unless he is playing, then Cole; if both are playing, choose Axel. Portraits
  and bitmap text occupy the existing side-HUD pilot well. Compact mode uses
  its score compartment. Comms do not enter story state or pause play.
- The same two helper actors enter from the south after an0.85/1.07s warning,
  scaling2.25 to1 over1.55s. Entry has no body hazard, gunfire, materialization
  or Retina targets. Afterward they orbit, scatter to opposite sides, make
  crossing bombing passes and rejoin. Gun/missile clocks continue independently
  of flight choreography; HP and destroyed actors are not reset.
- Each crossing helper drops up to two lightning bombs. A site commits on drop,
  warns1.85/1.65/1.45/1.30s by rank, and deals circular radius30 damage only after
  the tell. Existing ground Retinas and near-danger beeps use the same geometry.
  The16-pose bomb loop is128x192/pivot64,96; the16-pose detonation is
  256x256/pivot128,128. One scale per bank, transparent padding, no stretching.
- The complete four outer generator plates now spin with their inner cores.
  Their station anchors remain fixed during hull charges. The original
  markHit/part flashes remain visible and expire. Airborne Retina targets are
  filtered rather than assigning to cached getter-only `dead` properties.

Owners: `assets/storm_assault_1018.js`, `assets/stage4_panic_1017.js`,
`assets/stage34_assault_1014.js`, `assets/storm_guard_1017.js` and the road-speed
read in `assets/game.js`. Generated pixels/manifest are owned together by
`_BUILD_SOURCE/build_storm_assault_1018.py`; provenance and measured registration
are under `_ART_SOURCES/storm_assault_1018`. No shared atlas changes.

Validation: required core suite8791 passed,0 failed, BUILD OK, exit0, matching
the recorded baseline; `node --check assets/game.js` passed. Native Edge checks:
50 assault/ordnance/phase/audio,113 existing Stage4 panic/spiral regressions,
14 review/art/co-op/layout checks; all passed, no page/console/draw/asset errors.
Native hit pixels and expiry were verified for helpers, generators and the
pursuit hull. All32 new poses rendered through XART and the native drawImage
path; contact/onion sheets and full-FOV captures were inspected. MP3 media
elements decoded and the owned rev loop started with positive gain. Browser
audio was muted for automation; this is not a human listening/mix assessment.
These are encounter fixtures, not a nine-level campaign completion claim.

Review: `docs/previews/storm_assault_1018/index.html`, four actual-game scenes,
Normal/Hard/Furious, Cole/Decker/co-op selection. Review storage is isolated;
invulnerability is confined to the review. QA: `docs/qa/storm_assault_1018.json`;
captures/logs: `_shots/storm_assault_1018`. No commit or push requested.
