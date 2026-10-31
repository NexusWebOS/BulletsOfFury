# Overdrive Yuri28 — upward cross-step with side aim, 2026-10-15

Build `overdrive1015-yuri28-r1`. Yuri now has dedicated top-down motion when
moving upward while facing/aiming left or right. Legs advance north/away from
camera while hips and upper body twist to hold the rifle horizontally sideways.
The actual movement/firing state selects movement or braced side-fire clips.

16-frame movement loop,12-frame clean firing loop in each facing, plus2setup
stills:58exported PNGs.28selected generated action drawings, with mirrored right
facing, give56motion PNGs. Mirroring is declared rather than counted as new
generated drawing. Fire source repeats its first pose at frame13, so the last
four repeated phases are excluded for a clean12-frame wrap. First input/reference
frame is excluded from both motion loops. All raw17-frame clips remain in source.

192x224 common cells, root96,160; one proportional88/185 scale across clips and
one fixed translation per facing based on selected reference root127,216
(mirrored65,216). No per-frame fitting, recoloring of the body, image rotation,
warping, tween-generated body frames or skeleton cutouts. Binary alpha and
nearest sampling retain pixel edges. This matches the existing roughly88px Yuri
body unit and preserves whole hands, boots and rifle. Each frame has a measured
upper-body barrel tip; existing footVisualSocket/footSocket, attached muzzle
effects and actual projectile pipeline use that point.

The runtime wrapper applies to modern on-foot Yuri only, with real upward
movement dominant over horizontal movement, standing stance and horizontal side
aim. It uses the existing distance-based gait phase, so movement and firing share
phase. Blocked/stopped feet do not continue stepping. Ordinary horizontal travel,
prone/crawl, transitions, rolls, jumps, death, cover and stationary poses keep
their current owners. Stage7 fixed-depth combat/traversal retains its own player
pose renderer; this new upward motion is for top-down movement. Controls, speed,
weapon cadence/damage, HUD27 font/gun box, music and0.75room exposure remain.

Initial attempts were rejected for walking toward the gun, torso turning and
unwanted baked effects. A corrected rear-hip setup was generated, then two new
loops. Rejected raw candidates and both edited setups remain under source for
provenance; only selected loops are registered. No detached firing particles
are baked into the selected clips; actual game effects remain socket-attached.

The identity references came from public raw.githubusercontent.com/NexusWebOS/
BulletsOfFury/main/expansion/topdown/art/yuri_motion_1013/frames/od_ym_*_walk_0.png.
Each was fetched and verified byte-identical to the local original before a
192x224crop was uploaded to PixelLab. `source/public_references.json` records
URLs, hashes and crops. This provides public provenance for the reference
transfer; no unpublished local game artwork was uploaded. Source endpoints,
job IDs and prompts retained; temporary upload endpoint removed after transfer.
32included generations used across candidates/setups/final clips;1690remained.

Owner `_research/build_yuri28.py`, runtime `js/yuri28.js`, asset registration in
`index.html`. Source paths are retained at `art/yuri28/source`; rebuild is local
and does not call PixelLab. Viewer `art/yuri28/preview.html` supports pause,
stepping, half speed, onion and existing-Yuri size reference. The separate
setup images are available for future transitions; moving clips are wired now.

## Verification

30/30 native Chromium checks, zero page/console/shader/asset errors. All58images
draw real nonempty native pixels. Synthetic raw M30 inputs: D-pad up plus physical
B shoots right / Y shoots left; both select the correct upward firing bank and
advance through multiple drawings. Releasing fire keeps the side aim through
the existing aim hold and selects movement. Actual bullet origin and live muzzle
socket match. Collisions stop feet; horizontal run, prone/crawl, roll and pause
retain expected behavior. Actual hit timer, white hit pixels and expiry verified.
Stage7 retains its player/HUD/exposure. All820previous PNG hashes match.
Screenshots, contacts and onion overlays inspected. Base suite completed BUILDOK
/0ERRORS/exit0; syntax checks passed. These are isolated native input fixtures,
not a physical controller or full campaign playthrough.

Evidence `docs/qa/overdrive_yuri28_1015.json`, `docs/qa/yuri28_views`.
Probe `_research/probe_yuri28.py`. Local preview8781. No assets/game.js edit,
commit or push. Preserve all other work.
