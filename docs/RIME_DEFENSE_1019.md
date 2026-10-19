# Stage 3: Rime Wall's icy final defense

Mike requested ice bullets/lasers, permanent shoulder laser-mortar emitters,
an icy reactor charge, an ordinary-primary route to the disarmed core, and an
erratic final defense. He added PixelLab credits for the main boss and
miniboss's frost effects. Native browser inspection initially failed because
automatic approval review was at capacity; Mike chose "Continue code; test
afterward."

`assets/rime_defense_1019.js` loads after the existing encounter owners. Its
combat and damage changes own only Stage 3's `cryospear` / Rime Wall. The
Frost Cruiser retains its independently authored encounter and shares the
new ice-charge art and registered cold-bullet rendering.

The intact boss alternates rapid icy MG fire, twin ice cannon lasers, native
ice missiles, permanent shoulder mortars and the authored ice-ball volleys.
Lasers use the regular green/yellow/red FOV plates and stop independently
when their gun is destroyed. Their warning tracks only during its first
55%; release keeps the committed aim and matching gun pose.

The black shoulder apertures are measured on the whole authored hull. They
glow before launching pairs of laser mortars; the landing points commit at
launch and use circular ground Retinas. The projectiles rise from the actual
shoulder positions, leave upward and descend to the marked points. These
shoulders are permanent emitters, outside the destructible/Retina roster.
Owner death or a native module rupture cancels pending owned attacks.

After all four original weapons are destroyed, the boss changes to warned
rams and strafing shoulder-mortar salvos. Ordinary primaries can pass through
the retired nose conduit to the actual seated reactor. Its occupancy mask is
measured offline from the authored core cell. The whole hull remains solid
for player contact, including rams. Exposed core damage is 3x, other hull
damage is 1.5x; manual Retina uses the actual core position. Native HP,
hitBoss, markHit and defeat paths remain authoritative.

| Difficulty | Cannon warning | Mortar charge | First landing warning | Ram warning | Mortar pairs per turn |
|---|---:|---:|---:|---:|---:|
| Normal | 1.40 s | 1.65 s | 1.35 s | 1.25 s | 2 |
| Hard | 1.18 s | 1.40 s | 1.20 s | 1.08 s | 3 |
| Furious | 1.02 s | 1.20 s | 1.10 s | 0.96 s | 4 |

PixelLab provides 32 generated poses per bank: outer frost swirl, reactor
charge and shoulder mortar. The build owner is
`_BUILD_SOURCE/build_rime_effects_1019.py`. Source generations and prompts
stay under `_ART_SOURCES/rime_effects_1019/`. All banks have fixed even
canvases and pivots, source scale 1 and identical 16px padding; no per-pose
fitting, synthetic warp frames, tiling or shared atlas edits. Rejected
mechanical-gear, snowflake-icon and asteroid seeds are recorded separately.
The MG uses the existing authored 28x64 ice bullet, explicitly registered in
the new manifest instead of asking for an unregistered `rime_mg` bank.

Review: `docs/previews/rime_defense_1019/index.html` uses the native full
playfield and side HUD with isolated review saves. Its six scenes are full
encounter, cannon lasers, shoulder mortars, exposed critical core, ram and
Frost Cruiser charge. `frames.html` plays all banks with adjacent-frame
onions and fixed-pivot crosshairs.

Verification results are recorded in `docs/qa/rime_defense_1019.json`.
State checks and native pixel checks are reported separately. The targeted
native probe is `_BUILD_SOURCE/probe_rime_defense_1019.py`; it uses the actual
game context's drawImage and XART keys, real primary input, native frame
batches with yields, screenshot inspection and page/console/asset checks.
These controlled fixtures do not establish campaign completion.
