# Herald faster bomber passes — October25

[Fresh Furious clip](previews/barrage_revision_1025/index.html#herald-bomber).
The bomber chapter now shows the faster revision in a new continuous 52-second
native film. Existing recordings are preserved.

The bomber used a separate 4.6-second flight and a sequential 0.62-second warning
plus wait before each release. It now travels at the exact world speed of the
diagonal corner swoop. The shorter horizontal route takes 0.97s on
Furious, 4.74 times the previous speed.

Both living claws rapidly release animated red energy, with attached energy
muzzle flashes. Furious waves are 70ms apart while the sockets cross the screen.
Measured complete passes release 11 and 11 projectiles, versus 3
per pass in the previous film. Selected drops burst into radial chaos; direct
rounds form the falling carpet. All releases use the actual current claw mouths.

The complete carpet is committed during the existing 1.05-second pass warning.
Native green/yellow/red fields show its lanes before takeoff; the carpet and
radial bursts retain an escape opening. Broken claws immediately cancel their
scheduled releases and active rounds. Native HP, hit/Retina, visible white
damage, wing animation, breakup and finite returns remain authoritative.
Projectile budget stays at 128; the focused Furious observation peaks at
43. Launch audio uses the existing shared cue with a 130ms
retrigger gate and silent paired partners. No new artwork was needed.

Film checkpoints: warning 0:17.1, fast pass 0:18.6,
red burst 0:19.2, native return 0:23.5.
The gallery supports slow motion and frame stepping. The invulnerable observation
bot withholds fire; this verifies presentation, not human difficulty.

## Verification

- 41 native Chromium checks pass across Normal, Hard and
  Furious: measured corner-speed agreement, at least eight drops per pass,
  committed warnings/opening, exact birth sockets, unshootable energy from birth,
  bounded rounds, unchanged observation HP, actual white damaged pixels and
  expiry, broken-claw cancellation and decoded audio routes.
- 34 review-browser checks pass for all eight chapters,
  playback/seeking, audio enabled, frame stepping, slow motion and byte ranges.
  The new Herald film fully decodes with -9.0dB audio; actual
  playback includes all four charge/flight/launch/burst cues. No page, console or
  asset errors.
- JavaScript syntax checks pass. Required test_fl.js exits 1 before assertions or
  its final summary because the existing retired_art_archive_1022.cjs helper is
  missing. This is not a full-suite pass.

Evidence: docs/qa/herald_speed_1025.json, _shots/herald_speed_1025/, and
_shots/barrage_revision_1025/video/herald-220000/. Reproduce using
_BUILD_SOURCE/probe_herald_speed_1025.py, record_barrage_revision_1025.py --cases
herald, publish_barrage_revision_1025.py and check_barrage_revision_1025.py.
This pass did not edit game.js/test_fl.js, commit or push.
