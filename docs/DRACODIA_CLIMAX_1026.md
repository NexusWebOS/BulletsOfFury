# Dracodia accelerating cinematic reveal - October26

Mike requested continuous faster loops, a complete-body reveal after the light
flashes, and additional dramatic strikes across the screen. This supersedes
the earlier preflash settling/material handoff in DRACODIA_DEPTH_1026.md.
[Current audible 36.18s transformation recording](http://127.0.0.1:53746/_shots/dracodia_climax_1026/video/take-f72285dd/dracodia-final-transformation.mp4). Earlier takes remain.

`assets/dracodia_depth_1026.js` keeps one integrated unwrapped phase from the
existing 20/24 revolutions/s carrier. Angular speed increases by 0.15 revolutions/s
each second, reaching about 2.57 revolutions/s at peak whiteout. Both banks index
that shared phase with modulo, retaining the 16 authored depth views and all
24 original carrier views. There is no late front-facing pause or deceleration.

Download percentage and visible material are separate. Visible material stays
at most 86% complete (111 of 128 scan bands); the remainder keeps the rotating
wire/carrier, including after the data reaches 100%. The actual native completed
body is never drawn before 25.6s. Only after the authored whiteout is fully opaque
does it replace the turning assembly at the same anchor and native scale. The
body becomes visible as the light clears after 25.9s and continues into native
speech at 28.5s.

Rear/front electric helices remain. Additional downward channels strike across
nine playfield lanes, away from the boss, with a quicker three-channel climax.
They reuse authored r25Bolt art and are non-damaging silent visual partners to
the existing 24 native lightning/audio beats. Native HP/form pools, portal,
protection, arena swap, speech, hit feedback and defeat/rewards remain unchanged.
This revision reuses the existing generated art and spends no generation credits.

## Boss Cinematics skill

The validated personal skill is installed at
`C:/Users/Mdogg/.codex/skills/boss-cinematics/SKILL.md` with display name
**Boss Cinematics** and invocation `$boss-cinematics`. It covers continuous
registered assembly, real depth loops and acceleration, concealed complete-body
reveals, layered surrounding electricity, distributed cinematic strikes and
native recorded visual/audio verification. A focused Bullets of Fury reference
records the actual owners, asset pivots, timings, build workflow and probe paths.
The staged source and installation hashes are under this revision's `_shots/`.

## Verification

- 30 native checks pass. Actual partial rendering makes zero native complete-body
  calls at 24.7s, 25.22s and 25.59s. All 16 poses remain in the late accelerated
  loop. Actual distant-strike pixels, both helix layers and nine lanes pass.
  Native health, protection, one arena/speech handoff, damaged pixels and flash
  expiry pass, with no browser/asset errors. Native screenshots inspected.
- 19 recording checks and 6 playback checks pass. The film fully decodes with
  -4.6dB sound at about 59.0 native frames/s. Decoded preflash,
  peak-flash and clearing-light frames were inspected; play/seek works in Chromium.
- Skill validation passes for the installed files. JavaScript/Python syntax and
  scoped whitespace pass. game.js and test_fl.js hashes are preserved.
- Required `node _BUILD_SOURCE/test_fl.js` exits 1 before assertions/final summary
  on existing missing `_BUILD_SOURCE/retired_art_archive_1022.cjs`; it is not green.

Run the existing probe, recorder and playback helper with `--climax`:
`probe_dracodia_download_reveal_1025.py`, `record_dracodia_transformation_1025.py`,
`check_dracodia_transformation_video_1025.py`, all under `_BUILD_SOURCE/`.
Evidence: `docs/qa/dracodia_climax_1026.json` and `_shots/dracodia_climax_1026/`.
The film is a transformation checkpoint using explicit native arm/core damage,
not a full fight. No commit or push.
