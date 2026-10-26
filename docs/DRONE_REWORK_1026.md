# Drone entrance rebuild â€” October26

Mike replaced the former void/player entry and creature-overlay conversion with
an authored gate entrance and synthetic-code fusion.

`assets/drone_rework_1026.js` owns the first-host introduction only. The native
current scenery now warps in wrapped scanline strips while palette cycling and
stepping down to black (0â€“3.4s). The living arena fades up (3.4â€“5.4s), then the
existing PixelLab `amethyst_gate` animates open/loop/closed (5.4â€“10s). Its mechanical
frame stays fixed while the purple interior moves. The actual V18 drone emerges
from 7.2â€“9s; the pilot remains in place.

The approved final-form violet/red-magenta synthetic DNA spirals behind and in
front of the drone and downloads code inside its actual alpha. From 9â€“14.75s,
rumble/jitter, shared-mixer charge/crackle and six stepped 1015 glow levels build.
`_BUILD_SOURCE/build_drone_rework_1026.py` derives the magenta emission from the
actual drone's bright/green pixels, with hard 1â€“3px rings on the same 256Ã—256
canvas and 128,128 pivot. The original drone remains unchanged. Source and output
hashes, builder ownership and taxonomy are registered; no new generated assets
or shared-atlas changes.

The authored whiteout frames rise from 14.3s, cover the full playfield including
the pilot, and remain opaque as the whole first-host body takes over at 14.75s.
The light clears through 16.7s; native combat resumes at 16.8s. No preflash host,
old dragon/symbiote overlay, black-void portal, player teleport or phase/timer skip.
The native clocks, initial protection, part budgets, later skeletal rebirth,
lightning, speech, combat, hit flashes and death/rewards keep their original owners.
Existing `arena-teleported` history naming is retained only for compatibility;
its new style explicitly reports background warp without a ship teleport.

Validation: 22 entrance checks and 48 existing final-transformation regression
checks pass in native Chromium, including actual rendered code/glow/whiteout,
protected health, native arm damage and flash expiry. Native screenshots were
inspected. Syntax checks pass. Required `node _BUILD_SOURCE/test_fl.js` exits 1
before assertions/final summary because `_BUILD_SOURCE/retired_art_archive_1022.cjs`
is absent (recorded existing blocker); it is not a passing suite.

Recording helpers: `_BUILD_SOURCE/record_drone_host_1026.py --rework` and
`_BUILD_SOURCE/check_drone_host_video_1026.py --rework`. Recording observes native
animation/audio from time zero through opening phase1, without damage fixtures,
phase writes or timer jumps. Evidence and latest film are listed in
`docs/qa/drone_rework_1026.json`. Older review films remain preserved.

Current film: `_shots/drone_rework_1026/video/take-3b2096b2/drone-to-dracodia-phase1.mp4`. All13 recording and11 playback checks pass;
23.07s at 59.44 native fps, decoded audio peak -6.2dB, no browser/asset errors.
Decoded warp, charge and reveal frames were inspected. Boss Cinematics reference
is updated with this sequence; no commits or pushes.
