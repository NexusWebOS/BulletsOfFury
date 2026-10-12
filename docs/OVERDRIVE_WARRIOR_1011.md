# October 11, 2026 — Warrior scale, supplied boss music and tank boost

> Current runtime: [the later menu/Warrior revision](OVERDRIVE_MENU_1011.md)
> uses the navy/silver `warrior_mk2_1011` bank and restored startup menus.
> [The current introduction](OVERDRIVE_BOSS_INTRO_1011.md) uses the requested
> closer 640 × 480 field, cinematic entrance and rotating dossier. The measurements below describe the earlier olive-bank pass;
> its source assets and QA record are preserved.

Mike supplied `BOF-O-BOSS1.wav` and asked for a larger regenerated tank boss
at the current zoom, an epic fight, and the ability to accelerate the player
tank. This extends the existing standalone `expansion/topdown/` game.

## Play and controls

Serve the repository and open `expansion/topdown/index.html`, select a pilot,
then Level 2. **Hold R** to boost the tank. On the six-button controller,
**hold Mode + C**. Normal C still charges/releases the cannon. While boosting,
directional fire and turret aim remain independent; Mode also locks the hull
for sideways movement. Smoke remains Mode + Z. Help includes the new input.

Boost accelerates smoothly to 2.05 times the normal speed, lasts 2.25 seconds
from a full meter, and refills in 3.4 seconds. Release after exhaustion to use
it again. Standing still spends no energy. Existing authored dust trails both
tracks; armor, hedge slowdown, collision, cannon charge and recoil still apply.
Boost grants no invulnerability. Death clears it; respawn/restart refills it.
The same player-tank owner supports the other ground tank missions and the
boardable museum tank. On-foot R still reloads.

## Warrior and arena

- Six regenerated 512 × 512 module canvases, original olive/steel/orange/red
  identity and no hammerhead. Built-in imagegen used the current Warrior master
  as its identity reference. The original October 8 bank stays available.
- Fixed module pivots and one proportional scale per bank; the hull, damaged
  hull and wreck share a canvas and mounting point. The left arm's measured
  crop excludes a fragment from the adjacent generated cell and restores its
  transparent gutter without moving the arm. Source pixels remain archived.
- Hull canvas renders at 286.72 world pixels. The front assembly's measured
  visible width is 436.62 pixels, with no change to the 480 × 360 playfield or
  the 1:1 camera zoom. The chassis turns sideways beneath its fighting upper
  body; the helmet and arms detach at their actual mounted angle/pivot/scale.
- The old 1:1 entry camera followed the player at y650 while the boss remained
  at y305, outside the viewport. The Warrior now approaches its y500 combat
  position and the camera frames the duel while prioritizing the player's
  escape route. The arena radar yields its area to the large boss. Volley
  labels occupy the upper-right HUD area instead of overlapping its face.
- Bullet, visor laser and homing-missile volleys remain. The ram keeps its
  committed warning and breaks concrete cover with its larger hull radius.
  No boss charging orb. Separate health: hull220, helmet120, each arm85.
  Hull armor still encourages breaking the helmet and arms.

## Music and source ownership

`expansion/topdown/audio/source/BOF-O-BOSS1.wav` is a byte-for-byte copy of
Mike's Desktop file. `audio/BOF-O-BOSS1.mp3` is the shipping 256 kbps stereo
encode: 122.76 seconds, no mix, gain, trim or fade changes. The new `warrior`
music key starts it when the entry finishes, loops it, then stops it for death
and the existing stage-clear track. Other ground boss music keys are retained.
`audio/boss1.json` records source/runtime hashes and conversion details.

Art sources, exact prompt, crops, anchors, scales and registration:
`expansion/topdown/art/warrior_1011/`. Owning builders:

```powershell
python expansion/topdown/_research/build_warrior_1011.py
python expansion/topdown/_research/build_boss_audio_1011.py
```

Only loose expansion exports and their manifests are updated. No base atlas
or base-flight gameplay file is edited by this pass. Existing user work is
preserved. No commit or push was requested for these new changes.

## Verification and limits

- Syntax: `node --check assets/game.js` and all edited expansion JS pass.
- Final `probe_warrior_1011.py`: **22/22 native Chromium checks**, zero page,
  console or missing-file errors. Actual media playback and end looping pass;
  independent boost/aim/fire, exhaustion/refill, release/blur, thin-wall
  collision, frame sizes, camera, modules, death/results and restart pass.
- Measured one-second travel: normal153.45 versus boost309.96 world pixels.
  A live Warrior ram was evaded by real boost input with collision and damage
  enabled. Controller checks use synthetic M30-shaped Gamepad reports.
- During this pass, existing ground probe **23/23** and controls probe
  **29/29** passed. No browser errors. Front/rotated boss, missile volley,
  ram escape, boost trails, breakaway arm, results and Help captures inspected.
- Required full base suite reached its final summary: **8,683 assertions
  passed, nine failed, exit1**. Its current failures concern HUD rails,
  pilot-card naming/spacing, story layout and Help font size. This differs
  from the most recent recorded green base result. The base harness does not
  load the standalone Overdrive runtime; these files were already part of
  separate local work and were not edited by this pass. Failures are recorded
  by name in `docs/qa/overdrive_warrior_1011.json`; no green base-suite claim.

Reproduce the focused check:

```powershell
python expansion/topdown/_research/probe_warrior_1011.py
```

Captures/logs: ignored `_shots/warrior_1011/`. Portable native results and source
hashes: `docs/qa/overdrive_warrior_1011.json`. Most fixtures are protected to
inspect the encounter and pixels; they do not establish a natural campaign
clear or final difficulty balance. The single real-damage ram escape is
reported separately. Source-sheet arm pose differences remain authored art,
not a newly generated moving-track animation bank.
