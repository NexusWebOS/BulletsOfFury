# Recorded Levels 4–6 review — 18 October 2026

Follow-up correction: the main Harrier energy core described in this recording
has since been removed at Mike's request. The carrier is larger and allies
remain in combat; see [the current Stage 6 notes](STAGE6_HARRIER_WING_1018.md).

Reviewed `2026-10-18 19-34-17.mp4` (17:47.83) using timestamped frame sheets,
full-resolution incident frames and native Chromium reproductions. The file
starts with Yuri's selection and the Stage 4 boss, then contains Stage 5 and
Stage 6's Harrier branch. It does not show Stage 4's highway/miniboss or the
alternate Rebel branch. Automatic audio analysis produced no reliable spoken
transcript; no guessed dialogue is attributed to Mike.

## Fixed findings

| Time | Finding | Cause and correction |
| --- | --- | --- |
| 00:10; recurring in the Stage 4 fight | Radar reports only the boss while its two independent helper jets are visibly fighting. | The radar only enumerated `enemies` and the boss. These jets live in `boss._s4war.coreTurrets`. Landed, live helpers now receive their own contacts. Harmless scaling entries and destroyed helpers are excluded; identity deduplication prevents double counts. The reproduced scene now shows three hostile contacts. |
| 12:31 | The Fortress reactor opens, but firing at it produces an opaque white rectangular slab around the core. | The old reactor hit effect still tinted a rectangular section of the original closed hull. The newer sliding-aperture renderer then drew its own core flash over it. The aperture owner now supplies the flash on the actual energy-core silhouette. The hull stays intact and the blue energy remains readable. |
| 15:20 | The Harrier's exposed reactor has the same white-box problem. | Its legacy hatch-area hull flash also remained active after the new aperture took over. It now delegates to the actual core's existing hit-flash path. Owner/part timers, `markHit`, core damage and expiry remain native. |
| Around 16:20–16:50, during edge passes | A fighter can remain partly visible while its radar contact disappears. | Radar previously culled by the actor's centre. It now checks visible hull bounds and clamps the contact to the radar edge until the hull fully leaves view. Nightwing uses its actual render dimensions rather than its smaller collision box. A fully visible ace already tracked correctly; this was an edge-culling issue. |

The core change does not zero or suppress any hit timer. The actual core
brightens with a capped white overlay, retaining blue energy under continuous
fire. In the native incident reproduction, hitting the core changed 1,056
surrounding-hull pixels on the Fortress and 915 on the Harrier. Those unwanted
rectangular changes are removed, while actual core pixels still flash and
their timers expire normally.

The earlier core tests checked damage, a visible pixel change and flash expiry.
The unwanted white rectangle satisfied those assertions. The new checks also
require the surrounding hull to remain unchanged and blue core pixels to remain
visible during the flash. Earlier radar tests covered regular enemies, but did
not include these embedded helper actors or partially visible hulls.

## Observed and verified behavior

| Recording window | Result |
| --- | --- |
| 00:03–03:05: Storm Sovereign | Shield rounds, helpers, the south departure/large return and north-facing last pursuit occur; the fight completes. The recording contains the earlier lightning artwork. The separate PixelLab lightning/depth pass already replaced it in the current build; see `LIGHTNING_DEPTH_1018.md`. |
| About 03:10: Stage 4 rewards | Both Lightning Orb and Thunder Storm are shown as unlocked. The later HUD displays Thunder Storm Mk II. The earlier missing-upgrade report is not reproduced by this recording. |
| About 04:15–04:30: Stage 5 miniboss | The Siege Bomber encounter appears and completes before the Hammer fight. |
| About 04:55–08:25: Chrome Hammer | The fight advances through armor, chromium attacks and repeated restoration windows. At 07:20 the displayed manual-missile counter is 1/5. Ordinary primary fire and automatic space volleys do not interrupt this counter. Native checks confirm 3/4/5 distinct manual impacts on Normal/Hard/Furious; repeat routing of one missile counts once. No health or counter rebalance was made. |
| About 08:25–09:40: Hammer finish and Earth approach | The defeated pose, core finish, scattering/explosions and Earth approach complete. Earth grows at its destination while the ship approaches; the scene hands off to the next stage. |
| About 12:05–12:45: Fortress | Six batteries are destroyed and its core opens. The core takes damage and the encounter finishes. The reproduced defect was the flash rectangle, not failure to expose or damage the reactor. |
| About 13:05–14:10: team conversation | Flight and primary projectiles continue while new waves wait. Native reproduction confirms steering, old enemy-projectile motion and sky scrolling, with the original pending wave plan preserved. The dialogue advances once per frame. The large authored conversation panel is retained. |
| About 14:45–17:05: Harrier and Nightwing | The modular carrier opens its reactor, falls and releases the giant blue fighter. The ace then fights and Stage 6 clears after its defeat. Native regression checks verify real bay launches, attached fan smoke/explosions, protected openings and the continuous carrier-to-ace lifecycle. |

## Validation

- 51 focused native Chromium checks pass: reactor pixels/damage/expiry and
  ace radar on Normal/Hard/Furious, Stage 4 helper radar, live radio flight,
  and the Hammer's distinct manual-missile counter.
- 82 existing Stage 6 encounter checks and 14 delivered-review/co-op/compact-HUD
  checks pass. Total: 147 native checks, zero failures and zero game page,
  console, draw or missing-asset errors.
- `node --check` passes for `assets/game.js` and all four changed runtime files.
- The full `node _BUILD_SOURCE/test_fl.js` exits 0 with 8,785 printed passing
  assertions, zero errors and the final `FALVA/LIZZIE BUILD OK` banner.
- `game.js`, `test_fl.js`, the Hammer counter/ending and the PixelLab lightning
  renderer match this pass's starting hashes. LF/CRLF are preserved.

The first focused probe stopped on a test-harness lazy-load timeout after its
Stage 6 checks: the child RAF was intentionally trapped, but the new Stage 5
readiness wait used RAF polling. Explicit polling and the stage's real preload
queue fixed that harness issue; the complete final run passes. No production
change was made for the timeout. Normal static-server request cancellations at
browser shutdown are separate from the game error collectors.

Evidence, source metadata, full incident frames and native before/after images
are under `_shots/review_levels456_1018/`. Durable results and source hashes are
in `docs/qa/playthrough_review_1018.json`. These are recorded observations and
targeted native regressions, not a new uninterrupted campaign playthrough on
every difficulty or a claim to have reviewed the unrecorded route.

## Runtime owners and review

The changes are in `assets/siege_console_1012.js`,
`assets/stage6_carrier_1013.js`, `assets/stage6_roster_1017.js` and
`assets/stage6_reactor_1018.js`. Entry-script revisions use
`playthrough-fixes-1018` so the browser reloads the repaired renderers.

- Stage 4 radar: `docs/previews/storm_assault_1018/index.html?scene=helpers&difficulty=furious&revision=playthrough-fixes-1018`
- Fortress core: `docs/previews/stage6_repair_1018/index.html?scene=minicore&revision=playthrough-fixes-1018`
- Harrier core: `docs/previews/stage6_repair_1018/index.html?scene=reactor&revision=playthrough-fixes-1018`

Reviews use the native encounter at the regular field of view, with isolated
saves. No new art generation, commit or upload was performed for this repair.
