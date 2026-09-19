# Razorback early turret targeting — 2026-09-19

During the front-gun phase, point projectiles could damage and flash the central turret, but held laser collision and Retina targeting listed only the two machine guns. A player using lasers or lock-on weapons therefore could not exercise the approved early turret vulnerability.

The shared Razorback target-part list now includes left gun, right gun and central turret in the gun phase. Both the single tank and Hard duo use it for Retina targets; beam collision uses each part's own authored hit radius. Destroyed parts and transformation windows stay untargetable.

Chromium proof: `_shots/razorback_turret_0919/turret_hit.png` renders the authored white turret flash. The focused browser probe found a central beam hit on `turret`, three live targets on the single tank and six on the duo, turret HP 458 → 456, and no page or console errors. The first draw was blank because art was still decoding; the inspected capture waits for the hull and turret cells to load. Full-suite comparison is in `_shots/razorback_turret_0919/suite.log`.
