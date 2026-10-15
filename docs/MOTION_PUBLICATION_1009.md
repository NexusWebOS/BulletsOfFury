# October 9 motion publication and continuation

Mike requested publishing the completed Stage 1 animation pass and continued
boss motion work from `2026-10-09 00-30-03.mp4`. This batch is based on main
`d87ed6a8ab18d2e0e3b7cd235cf6651d2f681f90`.

## Included

- Current ten Stage 1 vehicles: eight-cell idle/flight reels and four-cell
  firing reels for the nine armed actors. Independent tank aim, boat weapon
  HP/launch/reload states and original jet banks/rolls remain live. Seven
  accepted source sheets produce 48 new moving-part/FX cells and 116 complete
  actor review cells. Static props and the unarmed landing craft keep their
  existing roles. See [Stage 1 ownership and QA](STAGE1_MOTION_1009.md).
- Eight accepted boss source reels, 64 frames: corrected two-arm Hammer death
  with seated head, directional counter after the bottom spike storm;
  Dracodia attached-head torso acting and alternating physical claws;
  Warden forelimb/rear-leg poses, gravel landing and converged gun stance;
  Stage 3/4 physical turret charge/recoil. Existing encounter HP, transformations,
  module ownership and original warning/sound families remain authoritative.
  See [timestamped video direction](feedback/BOSS_DIRECTION_1009.md).
- Reproducible builders, exact generation prompts, approved original RGBA
  sheets, measured pivots/tips, live reference plates, taxonomy entries,
  stage-loading integration and native Chromium probes. No shared atlas edits.

The older ZIP tank candidates and reference designs are retained locally and
are not published as playable replacements. The live roster was explicitly
requested. Separate Overdrive development, local guide staging and unrelated
scratch remain outside this commit.

## Verification

[Portable results](qa/motion_1009.json): 7,952 base assertions, exit 0 and final
zero-error banner; 18 boss motion checks, 22 counter-edge/dead-turret checks and
35 Stage 1 checks, all passing with zero browser errors. Existing Stage 3
combat regression also passes. All five game/registry JS syntax checks pass.
Native screenshots and eleven silent motion/gameplay clips were inspected.

The counter checks cover both directions at both camera edges on Easy, Normal,
Hard, Furious and Insanity. Stage 1 capture uses shoot.STEP's complete frame
loop so the terrain-owned wave clock advances; it includes forty seconds of
real naval, jet and tank firing. Focused boss clips retain actual updatePlay
projectile/encounter owners. Protected captures verify pixels and attack
geometry; they do not establish an unassisted full-fight balance sign-off.

To regenerate art and review on another checkout:

```powershell
python _BUILD_SOURCE/build_boss_motion_1009.py
python _BUILD_SOURCE/build_stage1_motion_1009.py
python _BUILD_SOURCE/probe_boss_motion_1009.py
python _BUILD_SOURCE/probe_boss_motion_edges_1009.py
python _BUILD_SOURCE/probe_stage1_motion_1009.py
python _BUILD_SOURCE/build_motion_review_1009.py
```

Probes require Pillow, NumPy, Playwright with Chromium, and imageio-ffmpeg.
`_shots/boss_motion_1009/review.html` and its captures are regenerated ignored
verification output. Raw recordings, capture dumps and the local preview server
are not committed. The owning builders register native cells and manifests
together. Game.js and test_fl.js remain unchanged, including their line endings.

## Remaining follow-up

- Longer unforced complete encounters on Hard/Furious, with normal player
  movement and damage, to tune pressure, recovery and overlapping patterns.
- Full Dracodia transformation cycling, persistent form HP and whole-campaign
  progression checks alongside the newly verified physical acting.
- The ZIP's shared explosion and Stage 2 volcanic in-between batches, plus
  optional damaged/critical-state Stage 1 reels, are not delivered by this pass.

Do not reinstate the rejected extra-arm/forked-limb source variants. Keep the
head seated through intact Hammer/Dracodia acting, use the existing attack
owners, and preserve independent live modules rather than replacing them with
the composite review reels.
