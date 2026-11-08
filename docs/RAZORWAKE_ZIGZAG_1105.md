# Razorwake — accelerating diagonal zigzags

November 5, 2026. Mike's request refers to the Razorwake review tab.

The sixteen straight up/down throttle lanes are replaced by diagonal
on/offscreen zigzags. Each pass enters beyond one corner and exits beyond
the opposite edge. Alternating lateral directions and reversing the order
after eight keeps the path changing while north/south directions alternate.
Entry/exit centers have 210px clearance, outside the complete visible hull.
Bezier turns stay beyond the edge, using existing authored rotational poses
and actual path tangents. No new ship design, runtime artwork transforms or
generation credits are involved.

Every successive pass travels faster. Committed runs shorten from
**0.90 to 0.36 simulation seconds**, with offscreen turns shortening from
0.26 to 0.16 seconds. The measured trajectory speed increases from
1439.6 to 3598.9 logical pixels/second:
**2.50× faster on the final pass**. Small route offsets do
not reverse the actual speed escalation in the tested viewport. Existing
32-heading hull, gun, thruster and shadow frames follow the diagonal vector.

Each committed diagonal retains a green/yellow/red warning lane and the
actual warning sign, with 0.80–0.70 seconds of reaction time. Dash cues and
throttled exhaust remain anchored. High-speed body contact now sweeps the
existing oriented collision ellipse through the previous/current hull
positions, preventing a crossed pilot from being skipped between frames.
Native invulnerability, roll/somersault, shield/GOD and once-per-pass
contact protection remain in force. A pilot outside the swept lane is safe.

This is a motion/collision revision only. Native 1,785 HP, two 536-HP guns,
713-HP protected core, spinning/recoiling gun fire, module breakaway,
hit flashes, Helix orb/capture death and once-only defeat remain unchanged.
Core game.js and all art pixels are unchanged. The runtime stays in
assets/razorwake_tempest_1105.js with a refreshed script URL in index.html.

## Verification

- All **33 existing native encounter checks pass**, including
  the four attack families, gates, real hit pixels/expiry, protected core,
  native death, retry, pause, bounded unshootable rounds and defeat.
- **6 trajectory checks pass** for sixteen diagonal crossings,
  both lateral/vertical directions, increasing actual speed, 2.5× escalation,
  heading/vector agreement and offscreen endpoints.
- **4 native collision checks pass** for swept crossing hits,
  safe out-of-lane positions, native protection and browser errors.
- Uncaptured high-quality native playback through the attack cycle measured
  **59.20 FPS**, including diagnostic instrumentation.
- Final full native fight: **51.11 average engine FPS** over
  **158.523 seconds**. The input-only Cole GOD bot holds position/fire
  during the first60 seconds, then tracks visible targets and holds its
  position when they leave view. No enemy HP/phase/timer writes after spawn.
  Full native gun/core destruction and defeat, decoded sound, no browser or
  asset errors, source stability, peak -1.9dB. Native 960×1024 canvas,
  30FPS media. The earlier H264 capture path stalled; a25s VP8 benchmark
  reached56.60FPS. The final take uses VP8 capture and exports H264 for review.
  No gameplay or animation slowdown was added to accommodate recording.
- **14 video-page checks pass**, including audio, seeking,
  exact ranges, mobile fit and other existing review movies.
- Syntax and line-ending-aware whitespace checks pass. The required older
  test_fl.js suite still exits1 before its summary at the pre-existing
  difficultyHealthBaseline15 missing-helper error in combat_polish_0927b.js:151.
  Its current log is retained; this is not a full-suite pass.

Human dodgeability and full campaign balance remain unverified. Sources,
receipts and performance limits are retained in
_BUILD_SOURCE/razorwake_zigzag_1105/ and docs/qa/razorwake_zigzag_1105/.
No commit or push was requested.

[Watch the revised flight and full fight](http://127.0.0.1:65123/?razorwake=accelerating-zigzag-1105#razorwake)
