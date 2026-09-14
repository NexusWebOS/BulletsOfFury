# Furyship solid assembly and individual arrivals — September 14

Mike requested opaque parts, no invented perspective flipping, a faster vertical
approach, individual arrivals from below with sound, and removal of the travelling
top/bottom cloud treatment shown in his screenshot.

## Current behavior

- Vertical intro speed is **1,000 px/s**, up from 420, through sky, assembly,
  reveal and countdown. The same scroll accumulator keeps advancing throughout.
- The dense foreground cloud deck is a finite world-space section. It passes
  once; it does not wrap around the camera. The former travelling cross-screen
  top and bottom caps are removed. Four fixed-height side banks frame the clearing.
- Twelve parts start individually below the entire screen. The first launch
  occurs after entering the cloud section, from 3.1 seconds when art is ready;
  subsequent launches are spaced **0.54 seconds** apart. Each rises into its
  moving orbit over 1.1 seconds, with one `furyPartArrival` cue from the existing
  game sound engine. The charge waits until every part has arrived.
- Every component draw uses exactly one authored **top view at full opacity**.
  Rotation and orbital movement supply motion; no side-view blending, mirrored
  transform, perspective flip, or per-part fade is used. Independent rotation
  shares an evenly spaced orbital clock to avoid the former pileups.
- The aircraft sits below the passing cloud deck, visible through its gaps.
  Incoming hardware draws above the deck so its individual arrival is visible.
- The plane and parts remain opaque through convergence and fusion. The completed
  fighter replaces the kit underneath the fully opaque white transition. The
  existing requested full-screen white fade and smaller local energy ring remain.
  Flight roll/somersault reels are separate from this assembly and are unchanged.

No new bitmap art was generated. Existing authored cloud and kit frames are used;
the unused perspective frames remain stored. Normal gameplay scroll tuning after
the intro and the legacy SPCBOY intro were not changed by this pass.

## Verification

`node --check assets/game.js` passed. The full suite reached its final summary:
**3,849 passed / 61 failed, exit 1**. Failure names exactly match the established
61-failure baseline in `docs/qa/furyship_live_0914.json`. The random historical
sand-tank assertion failed on this run; no new failure was introduced. The test
file is unchanged, and runtime LF / test CRLF line endings are preserved.

Native Chromium via the existing `shoot.py`/`capture3` path passed **17 checks**.
It ran the complete launch from time zero, including the full HQ dialogue. Actual
component draws were audited for top-only keys, opacity 1 and positive transform
determinants. The game sound log contains all twelve arrival cues in order at the
specified spacing. Every part's initial cell is wholly below the screen. Clearing
cloud draws contain only the fixed side-bank positions. Constant scroll, fully
white pixels and the handoff to PLAY were verified. No page, console or loop errors.

The screenshot sequence was visually inspected, including partial arrival, full
orbit, charge, white and reveal. The **26-second H.264/AAC recording with game sound**:

`_shots/furyship_solid_0914/BulletsOfFury_Solid_Assembly_0914.mp4`

The final movie fully decodes with ffmpeg, exit 0. Sound is reconstructed from the
game's frame-stamped event log; a constant export gain controls peaks. Capture-only
invincibility prevents post-GO deaths from interrupting the demonstration.

Proof: `docs/qa/furyship_solid_assembly_0914.json`.
Runtime SHA-256:
`5150c9c4134da494bec2d2789b9e7fecfd4c022f8647302a470945f4072109b5`.
Sources and capture tools: `_BUILD_SOURCE/furyship_solid_0914/`. Do not reapply
older integrators over this build. No atlas or shipping-manifest edits, commits,
pushes or user-data deletion.

Tally remains **51 complete / 11 partial / 73 pending**. Assembly perspective
blending is now superseded by Mike's solid-rotation instruction. SPACE-12 still
tracks the separate flight-reel silhouette consistency and exact component fit.
