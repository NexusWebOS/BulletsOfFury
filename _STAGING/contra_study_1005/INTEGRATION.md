# Use this package in Bullets of Fury

October 6 production follow-through: the existing Stage 8 Herald now implements committed, staggered twin cannon releases, owner-specific disarm cleanup and longer disarmed recovery. Two generated signature clips (joint/breach) are registered and reviewed in the native game. The full game suite passes 7,445 assertions; 41 native checks pass with zero errors. See the repository’s `docs/CONTRA_HERALD_1006.md` and `docs/qa/contra_herald_1006.json`. The four original lab bosses / eleven forms remain candidates; this does not implement all 35 reference bosses.

October 6 update: **BOSS_FIGHT_ATLAS.md** now contains the close replay of all 35 numbered encounters. **ENCOUNTER_KIT.md** is the newer world-pixel runtime contract for four original bosses/eleven forms with actual independent part HP, shared socket geometry, core vulnerability and phase cleanup. The older normalized six-pattern API below remains useful as a smaller recipe library; its limitations do not describe the newer boss implementation.

Best initial experiment: apply **committed cannon** to an existing cannon hardpoint, followed by **staggered crossfire** on an existing two-arm boss. These make the reference's weight and evasive choreography visible with little new art. Walking gates and form changes are a larger encounter-design change and should follow after ordinary-movement testing.

## Existing project systems inspected

Read `AGENTS.md`, current handoff notes, `assets/data/ART_TAXONOMY.json` and relevant parts of `assets/game.js` in the active Desktop repository. The taxonomy warns that filenames have misidentified assets, so reuse decisions below use registered roles. The `cole_fusion_1004l/weapons.png` source was also visually inspected: it contains long yellow/purple weapons, helix mass, hollow aura, burst/shatter, fragments and muzzle imagery.

| Transfer | Existing BOF family / entry point | Concrete change to make when integrating |
| --- | --- | --- |
| Visible lock, committed cannon | Original `combatWarningDraw` / `groundTargetReticleDraw`; `av3Beam` and `av3_` beam/muzzle registry | Resolve the live hardpoint transform once, track during the first tell segment, freeze the attack vector for the last tell segment, and fire from that same transform. |
| Paired arms and disarm | `hd1003_` Herald independent cannon arms; `av3_` Stage 2 modular miniboss | Alternate arm release slots. Destroyed arm cancels its warning and future emissions. Keep the other arm's scheduled tell intact; killing both creates a longer punish window. |
| Moving gap / shield overload | `cwd_` code-wall rows, impacts, overload/shatter and reconstruction | Reuse existing authored wall strips with a deliberate gap. Shift the NEXT gate during its tell; never move a committed gap unexpectedly after release. |
| Heavy recovery and eruption | Existing hammer windup/leap/impact/recovery poses, `arch_chromium_spike_0926`, original ground warnings | Reuse marked eruptions as a short relay of committed targets, preserving the visible-shaft collision rule and edge-inclusive world layout. |
| Distinctive player weapon contrast | `cf1004_` yellow lasers, purple Fusion helix, aura and impact/shatter | Retain those identities. Keep boss tells and hostile rims legible under the large player beam. |
| Cloak/phase punctuation | `rg4_` shield wave, cloak swirl/reveal, charge; `aa5_` alien arena/iris/ghost components | Reuse authored phase effects. Insert an attack cleanup boundary and a short readable emergence pose before the new phase fires. |

## Library API and adapter contract

`patterns.js` exports `Encounter`, `recipes`, `presets`, `hit` and `segmentDistance` through CommonJS or `window.BOFPatterns`. It is a standalone candidate library; production geometry, pilot speed, damage and registry calls are intentionally supplied by the game adapter.

```js
const encounter = new BOFPatterns.Encounter('cannon', 'Normal', cycleNumber);
// Seconds, not the game's frame-scaled dt. Maintain one local encounter clock.
const events = encounter.advance(localSeconds, targetAtTime);
const geometry = encounter.sample(localSeconds, normalizedPlayerPosition);
// events contain lock / beam / curtain / ring / fan / hazard / fx / recovery / complete.
// Render geometry with authored effects. Apply actual BOF collision in the same geometry.
// On owner death, disarm, phase change or encounter exit:
encounter.cancel('phase-change');
```

`targetAtTime(eventTime)` must return the target position at that simulation time, not whichever render frame happened to catch the event. The lab interpolates between simulation steps; a production adapter should use the game's update clock/history. All scheduled events crossed by `advance()` are processed in order; it does not lose volleys on a long frame. Aim snapshots are immutable after `lock`.

Coordinates are 0–1 relative to the arena. Source dimensions and pivots are independent of normalized collision shapes. Map x/y through the actual playable world, not the browser/window size or UI gutters. A normalized circle will become an ellipse if x/y use different pixel scales. Production should convert to pixel/world units before collision; choose bullet radii and velocity in those units. The lab's schematic scaling and `hit()` are for pattern trials, not a replacement for BOF's shared collision system. In particular, moving-beam swept volumes and attack-end transitions need production collision verification; the lab checks current/previous endpoints and uses 120 Hz simulation.

The cannon aims along a ray from its emitter through the locked target. Gate bullets preserve the announced gap. The radial pattern excludes a 1.24-radian sector centered on its locked target direction. Pincer fans alternate left/right sources with separate targets. The eruption pattern marks the captured position before activation; it does not silently retarget underneath a moving player.

Each library instance represents one encounter owner. `cancel()` clears that instance's active hazards and pending releases. For a production modular boss, route each arm's releases through its actual part owner and suppress only that part when destroyed. Do not run two independently looping instances without coordinating their safe routes. The built-in pincer demonstrates scheduling, not a finished two-part health model.

Recovery in the lab is a label/opportunity; it does not simulate a weak point, player DPS or boss HP. Match the actual authored exposed-core/recovery pose and damage rules in BOF. Whether a weak point is newly vulnerable is an encounter decision, not something inferred from every bright Contra hit flash.

## Proposed tuning, not measured Contra timing

| Preset | Tell | Bullet travel speed (arena units/sec) | Walking gap width | Recovery after active geometry |
| --- | --- | --- | --- | --- |
| Easy | 1.35 s | 0.27 | 0.34 | 1.70 s |
| Normal | 1.15 s | 0.32 | 0.30 | 1.40 s |
| Furious | 0.95 s | 0.37 | 0.27 | 1.15 s |

Lab movement is 0.48 arena units/sec with a 0.012 collision radius. It has a generous 0.8-second feedback cooldown and no roll, somersault, dash or other invulnerability. BOF's actual pilot speeds, hitboxes and frame-scaled movement differ. These numbers establish reviewable candidates, not a certified safe path for every production pilot/start position.

Production acceptance: validate from both extreme edges and worst starting position; verify the slowest pilot can reach an opening within warning plus projectile travel time; allow room for body collision and scrolling; retain one opening during support fire; check solo/co-op targeting; verify native aspect ratios; cancel stale locks on phase/part destruction; inspect charge, impact and recovery midreel; then run the required BOF syntax/full regression suite and native Chromium encounter captures. Never conceal a failing escape route with extra invulnerability.

## Effects to generate or reuse

| Priority | Effect / event | Asset decision | Specification |
| --- | --- | --- | --- |
| 1 | Reactor pressure discharge / cannon release or part break | **Generated in this package** | Cyan/white hollow electrical ring, navy rim, 12 frames, 20 fps, centered on the source. Render once over 0.6 s, then stop. Cosmetic only: the ring's bright pixels are not its damage mask. |
| 1 | Muzzle charge → flash → beam → recoil | Reuse `av3_` / round muzzle / existing casting poses | Charge begins before lock; strongest flash at release; beam from shared nozzle transform; recoil immediately after. Existing authored colors retain ownership. |
| 1 | Structural death cascade | Reuse current explosion and part/debris art | 3–5 breakpoints along the body, staggered roughly 0.08–0.14 s. Remove dangerous emitters first. Detached pieces follow existing debris rules. Screen flash is brief and never obscures surviving hostile threats. |
| 2 | Articulated conduit arcing between two live joints | New four-frame socket discharge/break clip generated in `boss_signature_fx.png`; fixed-endpoint strip still needed | The socket clip is a local accent. A stable bridge still requires a separately authored anchored strip; curved shapes need segmented attachment support. Cosmetic unless separately warned with matching collision. |
| 2 | Weight/contact: foot slam, hull landing, arm stop | Reuse actual biome splash/impact art after inspection; generate missing variants | Low horizontal pressure/debris burst, four buildup/impact frames plus four dissipating frames. Ground anchor stays fixed; warm dust for metal/concrete, blue splash for water, organic flecks for alien terrain. Never repaint an approved asset family to match Contra. |
| 2 | Organism emergence / peel-back rupture | Reuse registered alien/finale transformation art; generate only a missing pose transition | Twelve fixed-pivot frames showing outer tissue separate from a darker readable core. Use the boss's approved anatomy/palette. Separate body, tissue fragments and damaging emitters so old-phase geometry can be cleared. |
| 3 | Committed charge afterimage | Prefer existing authored pose/flight reels and rendering support | 2–3 brief trailing silhouettes sampled from actual poses; preserve direction and avoid full-body spinning as an animation substitute. Clear trails before new attacks; trails are cosmetic. |

The pressure PNG is preserved exactly as generated. Measured size is 1448×1086, a 4×3 grid of 362×362 cells (the requested 1024×768 was not honored). Significant alpha stays inside each cell, but the largest ring is only 1 px from a cell edge; it did not meet the requested 12 px padding. Use exact source rectangles and nearest-neighbor sampling, and keep this as a candidate reel until native-size BOF review confirms no bleed or an imagegen padding repair is made. Do not assume requested dimensions or auto-pack it into the shared atlas. Center is 181,181; small contour/pivot variation should be reviewed against the chosen hardpoint.

## Run and verify

Open `index.html` in a browser for local file use, or serve this directory with `python -m http.server 8766 --bind 127.0.0.1` and open `http://127.0.0.1:8766/`. No npm install or external dependencies are required. JSON manifests are supporting data; the lab renders the measured reel cells directly.

```powershell
node --check patterns.js
node --check lab.js
node patterns.test.cjs
```

The tests exercise all 18 recipe/preset combinations, event equivalence at 30/60/144 Hz and skipped frames, immutable locks, owner/phase cleanup, gate clearance, radial escape-sector clearance, swept projectile crossing, tells/recovery and explicit input validation. Passing these proves the standalone recipe mechanics covered by those checks; it does not prove production encounter balance.
