# Stage 6–8 pressure pass — October 22

Four new PixelLab models: TEMPEST DASHER, MIASMA SLIMEWING, FERROPHAGE SCOUT,
PLAGUE RELAY. Twenty hull banks, three original Herald module motion banks,
six effect banks. 201 shipping cells in 29 lossless WebP sheets (337630 bytes).
Fixed even canvases, common per-bank scale, authored alpha, stable pivots and
measured weapon sockets. Hull bands reconstruct each complete cell exactly.

Stage 6: three bounded alternating-side crossing waves; difficulty-scaled
warnings and committed lanes, shootable low-HP craft, native evasion immunity,
visible far-edge suicide explosions without kill rewards. Free-combat flybys
cycle bombs, machine-gun rain and charge runs. Ally radio uses the existing
wing, and no wave is queued during story, radio hold, boss or miniboss.

Stage 7: airborne and former magic-mutator slots use one toxic jet/drone family.
Ground barge, pipe, walker and tank retain native placements and mechanics.
Mobile fan, paired needle, lattice-gap and committed hook attacks; capped
sorties, visible recovery, native shot ownership, collision and kill handling.
Original sewer entrance remains in the scrolling master, held during arrival
and released during gameplay. Existing Warden reverse chase is unchanged.

Herald: original skull/core, separate wings and gun/claw modules retained.
New PixelLab wing flap and head motion, targeted talon dive, diagonal swoop,
bone/crimson soul feathers and separately warned double swoops below35%HP.
Native eclipse attacks interleave with the predator book. Recovery/return is
harmless. Shared part transforms drive art, targets and swept contact. Module
breaks cancel pending feather lanes; native flash and breakup clocks retained.

Selection: each craft master selected from four candidates, common.875 scale
on128-square canvas. Selected raw refs and all receipts retained. Dasher recoil
pitch was rejected for its attack: unarmed turbo uses the approved rigid idle
accelerator pulse plus separate wake. Raw rejected bank remains archived.
Two toxic needle/wave effects are luminance/alpha-preserving hue derivatives
of previously approved PixelLab water effects; no extra generation charge.
No stock explosion reel replaced. PixelLab balance9.99->8.61 (~$1.38 used).

Build: _BUILD_SOURCE/build_pressure_1022.py --install
Native QA: _BUILD_SOURCE/probe_pressure_1022.py
Full engine: node --check assets/game.js; node _BUILD_SOURCE/test_fl.js
Core8943 passed, final BUILD OK banner and0errors. Native report/screens/clips
are copied to docs/qa/pressure_1022 and docs/previews/pressure_1022.
These are encounter fixtures, not claims of whole-campaign playthrough wins.
No commit or push performed. Existing unrelated local work preserved.
