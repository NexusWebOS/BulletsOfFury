# Original move patterns

Starting drawing budgets below are proposals, not classic-game measurements. Design contact silhouette first. Timing may reuse a drawing.

| Family | Pose sequence | Drawings |
|---|---|---:|
| Jab | guard/load, drive, extension, retract, guard | 4–5 |
| Cross/finisher | hip load, turn, extension, follow-through, recoil, settle | 5–7 |
| Kick | load, chamber, pivot, extension, recoil, plant | 5–7 |
| Uppercut | low load, rising drive, extension, follow-through, descend, settle | 6–8 |
| Jump attack | takeoff, ascent, chamber, extension, descent, landing, stand | 6–8 plus flight holds |
| Run attack | last run contact, load, lunge, contact, follow-through, brake, recover | 6–8 |
| Knockdown | pain, recoil, launch, airborne, floor contact, ground, brace, rise, stand | 7–10; death branches before rise |
| Carry | squat/reach, load, raise, hold; walk under load; draw back, release, follow-through | 3–5 lift, 4–8 walk, 3–5 throw |

Example 280 ms light punch: `[40,40,70,60,70]`, active drawing 3, startup 1–2, recovery 4–5. One hit ID across any held contact. Tune in engine; do not call this a measured SoR2 jab.

Plan format for the checker: `body_unit`, `root:[x,y]`, `moves:[{id,frames:[{phase:"startup|active|recovery",duration_ms,hitboxes:[{id,rect:[x,y,w,h],damage}]}],cancel:{from_ms,to_ms,next:[moveIds]}}]`. Cancel is optional. Add actual paths, cell bounds, root deltas, hurtboxes, victim outcome and hand anchors in the project's own schema; do not replace its existing format to match this small example.

OpenBOR `delay` values in this module are centiseconds; simulation `game_speed=200` is a separate clock. Aseprite integer milliseconds must round-trip exactly. Verify hit, whiff, buffered input, late input, interruption, both facings/players and a killed target. Art plus boxes alone is not a complete combo system.
