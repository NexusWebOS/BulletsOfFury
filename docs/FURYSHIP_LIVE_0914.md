# Furyship live integration — September 14

The replacement is now used in the game. Level flight uses an exact byte copy of
Mike's approved `furyship_somersault_13.png`. The generated component, roll,
somersault and effect families now run through the actual space rendering path.
This supersedes the candidate-only integration status in the preceding asset notes.

## What changed

- Six independent components orbit, show top/front/side/back views, scatter and
  converge on measured assembly sockets. Their final blend resolves into the
  complete frame-13 hull before the fusion glow begins.
- Twelve pitch poses and eight roll poses follow the existing somersault and roll
  actions. Both roll directions work. Exhaust anchors change with the pitch/roll;
  front-facing end-on poses hide the exhaust behind the hull.
- Authored fusion, transition and speed effects are installed. A travelling energy
  strip covers the sky/space join while both authored backgrounds keep scrolling.
  The transition curtain stays behind the HQ panel and model announcement.
- All nine existing pilot colors apply through luminance-preserving masks. Flight,
  Stage 9 retention and the space burning-spin death route use the new hull. Twin
  laser origins now match the frame-13 gun mouths at a 48-pixel ship size.
- `spcboy` selects the preserved original fighter; entering it again restores the
  replacement. Campaign snapshots save and restore that selection. Old ship art
  and its original weapon anchors remain available.
- The new asset family waits for every required image and palette mask to decode
  before taking over. Existing rendering remains available during loading. The
  simulation clock freezes the new animation while paused.

`furyEffect` exposes the authored effect reels for other engine callers. They are
currently used for the transformation and space evasions; unrelated encounters
have not been changed to use them automatically.

## Verification and video

- `node --check assets/game.js`: passed.
- Full `node _BUILD_SOURCE/test_fl.js`: **3,849 passed / 61 failed, exit 1**,
  final summary reached. All 61 failure names match
  `docs/qa/supply_audit_0914.json`; no new names. The ten new section-309 checks
  pass. Two older source/coordinate assertions were updated for the replacement,
  with the legacy behavior checked separately.
- Native Chromium via `shoot.py` and `capture3`: **26 passed / 0 failed**.
  Actual game drawing checks cover all nine palettes, every evasion pose, pause,
  legacy selection/save restoration, real death, Stage 9 and every assembly phase.
  Screenshots were inspected; no page, console or game-loop errors.
- **26-second native video**, transformation followed by Stage 5 miniboss flight:
  `_shots/furyship_live_0914/video/BulletsOfFury_Furyship_0914.mp4`.
  Captured game sound events are rendered with the existing audio exporter. A
  constant export gain prevents clipping; no replacement soundtrack was added.
  Final H.264/AAC movie fully decodes with ffmpeg, exit 0.

The recording skips already-completed HQ reading and the miniboss entrance, and
uses capture-only invincibility so the requested actions remain visible. Gameplay
sound settings and damage rules were not altered by the capture. This is visual
integration verification, not a complete Stage 5 balance run.

Machine-readable proof: `docs/qa/furyship_live_0914.json`.
Runtime SHA-256:
`3fc67f9238c635ee3367f574a2a57bd2a1094ffadcf52aae1b7e76de59a02e45`.
Runtime LF and test CRLF line endings are preserved.

## Open refinement and checklist

SPACE-13 (effects) and SPACE-14 (nine pilots plus legacy selection) are complete.
SPACE-12 stays partial: the generated somersault wingspan still varies from
98–112 opaque pixels, versus 90 in the approved base; some silhouettes differ.
The parts use blended authored perspective views and a final hull blend. Their
exact silhouette fit and smoother intermediate views remain polish work. These
limitations are visible rather than concealed by independent frame stretching.

Current tally: **135 entries — 51 complete / 11 partial / 73 pending**.
See `REQUEST_CHECKLIST_0914.md` and `WORK_ORDER_0914.md` for all 84 unfinished items.
The remaining Stage 5–9 encounter cleanup is still open.

## Ownership

- `_BUILD_SOURCE/furyship_0914/build.py` owns the asset pack, including the exact
  base copy and its supporting palette mask. Original source reel is untouched.
- `_BUILD_SOURCE/furyship_live_0914/runtime.js` and `integrate.py` record this
  guarded runtime change. Do not rerun this or earlier integrators over later work.
- `append_tests.py`, `probe.py`, `record.py`, `finish_audio.py` and `validate.py`
  reproduce this batch's checks and recording/export path.
- Loose XART registrations are installed together; no atlas was repacked and no
  generated shipping manifest was edited in this batch. Existing staged and other
  working-tree changes were preserved. Nothing was committed or pushed.


## Later cloud-flight revision

Mike revised the staging after reviewing this video. The current twelve-piece, sustained-speed cloud intro and full-white reveal are documented in [FURYSHIP_CLOUD_INTRO_0914.md](FURYSHIP_CLOUD_INTRO_0914.md).
