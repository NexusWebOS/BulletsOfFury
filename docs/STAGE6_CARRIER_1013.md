# Stage 6 — Warhive Siege Carrier

The normal Stage 6 left route now ends with one overhead container-carrier fight.
It replaces the Warhive carrier / Nightwing Ace chase sequence. The right-route
rebel squad and Stage X Harrier still use their existing encounter owners.

The new whole-hull plate spans 129% of the viewport and occupies roughly the top
40% of the field. It crosses slowly, eases into reversals, and continues drifting
over the original Stage 6 weather and city. Six separately damageable laser
batteries are mounted to measured sockets on that plate.

## Combat

- **Battery cascade:** cannons charge and discharge in horizontal travel order.
- **Cross-deck gates:** outside and inside pairs take turns.
- **Alternating comb:** alternating three-cannon banks leave broad intervening lanes.
- **Missile recovery:** visible outward trajectories, followed by shootable missiles;
  this phase runs after all lasers have ended. The centre remains open.
- Destroying a battery immediately cancels its pending/current beam, leaves an
  opaque wreck, and removes that battery from every later pattern.
- Two destroyed batteries expose the central reactor. The player can finish it,
  or destroy more batteries to make permanent additional firing/dodging gaps.

| Difficulty | Charge | Beam on | Cascade stagger | Beam width | Hull speed |
|---|---:|---:|---:|---:|---:|
| Easy | 1.28 s | .42 s | .76 s | 32 px | 16 px/s |
| Normal | 1.12 s | .50 s | .66 s | 34 px | 19 px/s |
| Hard | 1.02 s | .56 s | .57 s | 36 px | 22 px/s |
| Furious | .94 s | .60 s | .50 s | 38 px | 24 px/s |

Insanity passwords use the Furious laser schedule. Lasers are vertical and never
track the player; their slow-moving origins remain attached to the visible guns.
The warning shows that same path. Warning/cooling frames cannot damage the player;
beam collision starts only when its visible core opens. At most three beams fire
simultaneously. Paired/comb banks recover before the next bank charges.

## Integration and damage

`assets/stage6_carrier_1013.js` loads after the existing encounter and air-motion
modules. It wraps the six Warhive entry points and stage loading, and does not edit
the monolithic game file. The original boss kind remains `warhive`, retaining
native music, score, boss rewards, achievements and stage completion.

Gun damage flashes only that gun. Core damage flashes the reactor region. The
hull and wrecks remain opaque until explosion takeover. Health pools reconcile
once against the final post-spawn HP, including co-op and encounter floor changes.

Continuous laser/flame damage samples the current weapon geometry instead of old
hit coordinates. Ordinary projectile collision uses its current intersection.
Retina targets carry an explicit one-hit component choice. For coordinate-less
area/special damage, the engine first determines whether the boss is in range;
the carrier then spends that one damage budget on the exposed reactor, or the
nearest surviving battery while the reactor is protected. Old hit coordinates
cannot select an unrelated component and splash cannot bypass the two-battery gate.

Death clears all owned warnings, beams, rockets and queues, calls native `bossDie`,
awards the native Stage 6 score, performs an anchored carrier cook-off, and reaches
the native flyover. No ace is created.

## Art and memory

Five PNGs plus manifests live in
`assets/game/levels/stage_06/boss/siege_carrier_1013/` (about 905 KiB of runtime images).

- One complete authored 1024 × 512 container hull; physical pivot 512,256.
- Four authored 128 × 160 cannon states in a 512 × 160 strip, common pivot 64,60:
  idle, energized charge, recoil/release, and destroyed.
- Built-in image generation used the game's existing skycarrier palette/style as
  a reference. It generated the whole aircraft and the four cannon states.
- Normalization uses one uniform proportional scale per bank, alpha padding and
  equal cells. No generated geometry, procedural aircraft, or per-frame stretching.
- Four new authored dark red beam frames in a 512 × 512 sheet, each 128 × 512, pivot 64,0. A common proportional scale and clipped vertical tiles preserve the authored shape.
- Four existing Furnace muzzle drawings are normalized with one shared crop into a 512 × 128 sheet. The authored small ignition, expanding ring, burst and cooling ring animate at each gun.
- Six front vent patches are cropped from the actual hull into a 240 × 12 strip (40 × 12 cells). Charge, firing and cooling follow their matching gun. Small cached palette variants avoid recoloring a full hull per frame. Destroyed batteries extinguish their lens.
- Smoke and explosion effects retain the existing authored game art.
- FX source/prompt and SHA-256 are in `_ART_SOURCES/stage6_carrier_1013/` and `fx_manifest.json`. Rebuild with `_BUILD_SOURCE/build_stage6_carrier_fx_1013.py --install`.
- Only Stage 6 queues these new textures. Existing stage-owned memory retirement
  releases them on transition; no whole-game preload or per-frame asset processing.

## Verification

Native Edge, Chrome and Firefox checks exercise all four difficulty schedules,
gun damage, current/queued beam cancellation, permanent wrecks, reactor unlocking,
continuous weapons with fresh/stale coordinates, native death scoring, stage exit,
route isolation and movement/fire through the real update loop.

Sixty-second schedule samples measured a largest open horizontal interval of at
least 102.99 / 100.99 / 98.99 / 96.99 px on Easy / Normal / Hard / Furious,
including the player collision margin. This is a geometry check, not a measured
human survival rate. Follow-up gamepad playtesting remains useful for feel.

The dark red effect revision passed **73 native checks in each of Edge, Chrome and Firefox** (219 total), with zero page/console/game-resource errors. Pixel checks prove four distinct predominantly dark-red beam drawings and a visible muzzle burst at every gun. Collision checks exercise the inside and outside of each difficulty’s expanded beam width. All six lights follow charge/fire/cool/off states. Full damage, co-op, route isolation, and native stage-exit tests were repeated.

Native screenshots and per-browser JSON are under `_shots/stage6_carrier_1013/fx-{browser}/`. The new full-game hero is `fx-chrome/native-stage6-hud.png`.
The combined tracked QA record is `docs/qa/stage6_carrier_1013.json`.
The previous encounter integration reached its final zero-error full-game summary. This effect revision passes game and module syntax checks; the parent integration task owns the new combined full-game regression result. No Git publication
is performed by this encounter change.

## Dark red weapon feedback revision

Mike requested broad dark reddish beams, visible muzzle flashes and animated front lights. The beam body is now 32/34/36/38 px for Easy/Normal/Hard/Furious, and its damage width uses the same opening/retract function as drawing. Bright edge fringe is non-damaging. The existing warning now reserves the expanded body width. Warmup, cadence, simultaneous-bank limit, missile separation and HP remain unchanged. Muzzle and lens animation use the simulation clock and stop while gameplay is paused; no wall-clock animation is added.
