# Dracodia helicopter — October30

HC79 owns only Dracodia's copied helicopter form1 in encounter2. The approved helicopter artwork retains its red/black/chromium identity. Its common proportional size is348 instead of410 (15.1% smaller), with a higher174px hover station that keeps the rotor clear of the top HUD. The body banks through13 authored headings. Its sixteen source rotor frames now advance at48fps instead of12fps. Independent left/right weapon pods have64 authored aim directions and three recoil poses; native core/left/right HP pools, actual component destruction, Retina targets, final-life protection, returning/copy cursor and native final destruction are preserved. Stage1's helicopter and the other copied forms stay under their previous owners.

## Attack decisions and counters

| Attack | Tell / commitment | Release / counter |
| --- | --- | --- |
| Twin machine guns | 1.45s Normal,1.30s Hard,1.15s Furious. Pods aim during the first70% then commit; the helicopter holds its firing station. | Two bounded1.25s tracer bursts at145/120/100ms cadence. An offset corridor at least96px wide remains between the committed lanes at the player's starting depth. Move into the gap or out of the lanes; the guns do not chase input during the burst. |
| Modular missiles |1.25s native player Retina warning; one actual lock per live pod. Turrets turn toward the observed player position. |2/3/4 missiles per pod on Normal/Hard/Furious,170ms apart. Visible actual launch sockets, recoil and appropriate flash. Physical homing missiles remain shootable. Broken pods cancel queued launches and vanish from hits/Retina targets. |
| Red pressure fronts |1.65s authored green/yellow/red warning plus the existing metal asterisk. |2/3/4 broad264px red sonic fronts. Safe flanks are reachable; ordinary gunfire and pressure waves cannot be shot down. |
| Committed charge |1.5s lane warning. |Straight charge exits the southern edge, then returns from north and settles at the hover station; no offscreen body target. |

The book cycles guns, missiles, sonic fronts, guns, charge and missiles with moving recovery/hover. After both weapon pods are destroyed, it skips gun/missile entries and alternates the remaining sonic/charge attacks. The scoped director replaces the older copied-form overlapping gun/sweep emissions. No changes to the original Stage1 Overlord-X director. Both weapon modules keep their native24% individual HP budget and shared copied-life damage; no new body immunity gate or extra HP was added. The living visit still downloads home after42s at a recovery boundary when other pools remain. Native death clears ordnance and follows the existing return/rebuild or final-destruction path.

## Digital jungle and authored artwork

The new original digital jungle was made with the built-in image generator, then normalized offline to680x1024. Dark emerald/teal canopy, roots, violet code faults and cyan circuit seams replace the former brown clearing/road. Opaque ground moves at12px/s; a separate stored-alpha near canopy moves at28px/s. Both remain world anchored as the normal camera moves. An exported wire palette supports the existing arena download transition.

Raw generated art, exact prompt, source hashes, an editable background Aseprite document, an editable helicopter inspection-strip Aseprite document and reproducible builder are retained under `_ART_SOURCES/dracodia_helicopter_1030/`. These documents are source images/inspection strips, not a manually authored animation timeline. Original16-pose PixelLab source files stay unchanged. The bank builder exports1244 frames across17 small1024px normal/hit texture pages, using even tight crops that restore fixed512px body /192px pod logical canvases and stable pivots. Pressure fronts, muzzle frames and the original six-stage tracer get authored directions/animation. Missile bodies and launch flashes reuse the approved RD72 authored directions. Source-alpha rows own hits; the same current pod frame owns its Retina position, recoil, gun and missile sockets. No runtime sprite rotation/scaling, generated glow, tint, animated image alpha or additive composite was introduced in the revised body/weapons/jungle path. The existing covered code-fusion snapshot and shared native engine impact/trail owners remain.

Rebuild: `_BUILD_SOURCE/build_dracodia_helicopter_1030.py`. Recorded checkpoint: `_BUILD_SOURCE/record_dracodia_helicopter_1030.py`. Native probes are alongside them. Machine-gun, missile, rotor, pressure-front and shared Retina warning sounds use the existing mixer. Ordinary energy/tracers cannot be intercepted; physical missiles can.

## Observed verification

58 focused native checks pass. Both left/right gun counters and broad-wave flanks are reached with ordinary inputs and survive with GOD off on Normal, Hard and Furious. Standing in an actual tracer lane causes native death. Checks cover correct difficulty missile counts, independent player locks and actual warning beeps, missile interception ownership, real component destruction/callback cancellation, exact aimed source alpha, same-frame cache/movement invalidation, pause, retry, committed charge, live morph snapshots, protected main-life return, dead-copy reconstruction and final-death anatomy. The previous860 frames/sockets remain pixel-identical after repaging; all1244 current exports have even geometry. No native draw/browser/asset errors in the final film.

The full native Furious copied-life checkpoint retains3690HP with intact modules. Other life bars are cleared before capture so the full selected life can be shown without the42s living visit return. An invulnerable input-only observer demonstrates22s before firing, reacts to the visible gun/wave patterns and then defeats the copy through normal weapons. No recorder HP/phase/clock writes occur during footage. It is not a whole-game run or a claim of a non-GOD full-fight win. Separate fixtures exercise the real protected main-body return. The film contains all four attack types, native copy defeat and the opening of final destruction. Defeat at114.23s; total121.42s. Measured native combat59.31FPS / overall59.21FPS. Decoded audio mean-21.7dB / peak-6.4dB, with actual launch, pressure-front and lock-beep playback. Smaller active texture pages corrected the initial capture slowdown while retaining identical artwork. Prior recordings remain archived.

The required full suite exits1 with its same five pre-existing failures and no new failures. `assets/game.js` remains byte-identical. No commit/push requested.

[Full updated helicopter fight](http://127.0.0.1:51046/?dracodia=helicopter-digital-jungle-1030#clip=s8-helicopter)

[Missile pods / red-wave preview](http://127.0.0.1:51046/?dracodia=helicopter-digital-jungle-1030#clip=stage8-helicopter-weapons)

[Original jungle artwork](../_ART_SOURCES/dracodia_helicopter_1030/digital-jungle-generated.png) · [Exact prompt](../_ART_SOURCES/dracodia_helicopter_1030/PROMPT.md)
