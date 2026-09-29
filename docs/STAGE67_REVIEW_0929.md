# Stage 6 / 7 review (0929)

Mike's list, item by item: what was wrong (measured in real Chromium first, `_shots/survey_0929/`),
what changed, and the proof. All code is `assets/stage67_review_0929.js`, loaded after
`mission_repair_0929.js`; derived art is built by `_BUILD_SOURCE/warhive_modular_0929.py`.

Proof: `python _BUILD_SOURCE/probe_s67_0929.py` — **39 ok / 0 fail**, 0 page or console errors
(sections carrier, ace, escape, warden, triangles, bombers, supply, warhive). Frames in
`_shots/probe_s67_0929/`. Suite section 379 (`_BUILD_SOURCE/test_stage67_review_0929.cjs`).

## Stage 6

| Ask | Was | Now |
|---|---|---|
| Boss modular, fans spin, beams make sense | one plate; a 44px fan disc spinning inside a 63px *painted* static fan; the beam came straight out of the fan hub | hull plate with both fan wells **cut open** (r 27.5 plate px, measured: blades to r 27, rim lip r 28–36); the authored fan spins **under** the rim with a motion-blur copy; a **beam cannon module** (the Furnace's authored coil cannon, recoloured to the carrier's gunmetal with cyan coils) **deploys** out from under each nacelle on Hard/Furious. The beam and the cannon volleys leave its **muzzle**; while it charges, its fan **spins up** (≈3x) and glows cyan, the coils pulse, a charge orb grows at the muzzle. The beam is the Tempest's authored blue beam (`tlv_beam`). |
| Fewer escort jets | 6 (8 on Hard/Furious) per launch | 3 / 4 / 5 / 5 (Easy / Normal / Hard / Furious) |
| Ace: larger, modular, own blue jet, a little easier | 92px single plate | 138px (1.5x, hit and lock box with it); fuselage + both wings as separate modules (cut at the roots, reassemble byte-exact): wings foreshorten into a bank and sweep back on the dash, a hit flashes the module it hit, each wing smokes on its own. Same moves, longer cooldowns: dodge-roll .6/.8 → .45/.6, bursts 3 → 2, missiles 2/4/6 → 2/3/4 every 7–9.5 s, Hard dash 10–12.5 s apart. |
| Bombers and boss don't flash (engine header rule) | `furyFleetDraw` had no flash branch; the carrier hull had no hull flash at all | bombers flash (the cell cut from the hit-tinted sheet); hull hits flash the hull, thruster hits the fan, door hits the door |
| Bombers too small / bomb run underwhelming / Lizzie's atomic sounds | 72px jets, a 24px spinning pip, a 90px explosion + `expBig` | bomb-run jets at **128px** (native cell size; the lane gates 100px, still inside their rows); Lizzie's `lz_bomb` falls from the bomber onto the reticle; `atomicLaunch` on release and `atomicDetonate` on impact; a mushroom from her own `lz_nuke` reel, shock rings, cook-offs walking out along the base, a short white pop. The damage circle is still the reticle's. |
| No special-ability boxes; abilities at random | supply crates (each pilot's `special_` icon) fell for everyone at 18/45/57 s and each could only be opened by its owner's rounds | no boxes. Each due supply becomes a grant at a random moment in the next few seconds, and between drops a random fighting wingman is powered up on its own clock (7–12 s). The player's own supply is delivered the same way. |

## Stage 7

| Ask | Was | Now |
|---|---|---|
| Hazard doesn't make sense | the warning was `sluice_warning_lane.png`, an orange/black striped **boom** with a lamp at each end — a solid barrier appearing across the floor — then a jet of goo that **stopped in mid-air** | the outlet itself warns (lamp flare, grate rattle, the authored drip then burst frames); the floor shows exactly where the spray lands in the shared green → yellow → red lane; the jet ends in the authored toxic **splash** (`s7m spew`) that pools and drains. Timing, reach and hit band unchanged. |
| No triangles on enemies | `drawS4/S6/S7DamageOverlay` painted a `lineTo` flame triangle and canvas-circle smoke on damaged hulls (a second, procedural damage system over the authored one); ordinary enemies still drew the FOV **cone** off the gun | the three overlays draw nothing (the authored `nsd_*` / `nxp_upward` damage reels remain); ordinary enemies get a straight lane band in the same phases; bosses and minibosses keep cones and alert frames |
| Furious Warden more aggressive | — | three new modes, Furious only, every other pick: **chaingun** (barrels extend and swing in a scissor sweep ±0.72 rad, ~22 green `mg` rounds/s); **stomp** (three hops onto committed ground reticles, splash + shock ring + acid ring each landing, then fast claw swats); **toxic mortar** (faceplate opens, the core visibly charges 1.6 s, four big lobbed toxic rounds land as drifting gas clouds — the cloud bank palette-swapped toxic — that hang ~6 s and cloud the screen; the clouds do no damage) |
| Ending underwhelming, can't see the portal entry, fly fast, fire not close, nothing scrolling with us | 180 px/s; the wreck drew as a near-white silhouette; explosions were fixed on screen while the terrain slid (they rode along) and the front climbed toward the ship; the ship reached the portal under explosions and a radio box, then was hidden | 2.2 s self-destruct beat with the wreck in its own colours → the level itself scrolls at up to **880 px/s** (analytic distance, frame-rate independent). The wreck and **every** effect the escape spawns (explosions, particles, smoke, shock rings, atlas flashes, bursts) move with the terrain by the same delta, so the reactor blows **behind** the ship below the bottom edge and the fire falls away. The flight decelerates onto the portal arriving on the ground ahead; the ship holds, then flies into it shrinking to 18% under a slight zoom, with nothing over it; the portal seals; only then does the blast roll over the spot. Radio lines sit either side of the entry. |
| Better entrance | a painted **3/4-view** gate still (purple, different perspective and palette), the ship shrinking into it, fade to **black**, hard cut | the engine's own top-down entry connector over the stage's sludge, butt-joined to the level's first frame (as every other stage), with the light closing in from the edges as the ship goes underground and "ENTERING UNDERGROUND. EXTERIOR SIGNAL LOST." typed at the top; no black cut |

## Traps worth keeping

- ⚠ **`xartPalette` caches its canvas**, so after the first frame a probe wrapping `XART.get` sees no key for
  a palette-swapped draw. Trap `xartPalette` itself.
- ⚠ **The Bash tool mangles heredocs** containing some JS (twice this drop). Write parts with the Write tool.
- ⚠ **A done sluice stops advancing its clock** (`stage7SluiceTick` skips `done` events) — an effect keyed off
  `e.t` after `done` freezes on screen. The splash runs on its own `efxClock` stamp.
- ⚠ **`bossActive` stays true through the Stage-7 escape**, so the boss supply clock keeps dropping boxes;
  they are collected every tick of the run or they sit on the portal.
- ⚠ **SpriteCook had 1 credit** — the cannon module is derived from authored Furnace art instead of generated.
