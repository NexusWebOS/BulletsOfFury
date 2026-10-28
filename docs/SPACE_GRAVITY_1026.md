# Space float and Chronos foreground protection — October26

Chronos background strafe angular speed is another15% lower than the previous20% reduction. Period1.64706s; the paired3.29412s duration preserves two complete sweeps and the centre return. Other charge/fire durations remain unchanged.

assets/space_gravity_1026.js owns the shared foreground gate for every hammer actor, including body/module damage, ordinary collision, space weapons, Retina collection, retained lock validity and missile damage. Existing foreground armor/shield/phase protection remains in charge. Background scale below1 rejects damage and clears stale hammer-module selection.

Space stages5/9 apply a simulation-clock vertical displacement,3.5px for ordinary enemies and5px for bosses/minibosses (reduced by depth). The previous displacement is removed before native AI; the new displacement is applied once to physical hulls, draw anchors, newly emitted projectiles and projectile source anchors. Event Horizon eye/core and twin sentinel hulls move together. Owner-relative muzzle flashes follow once; live Chronos and Tidal beam collision sources use the same position. C43's previous ambient vertical float yields to this owner while preserving its authored transformation lift and horizontal sway. Rocks/props and ground stages retain their existing movement. No HP, damage, interception or attack timers are changed by the float.

Verification:15 focused native-browser checks,10 background-form damage fixtures,20s drift stress check with<1e-8px residual, real native Rage checkpoint recording, beam/muzzle alignment and full return. Full required regression suite retains the same5 pre-existing failures; see docs/qa/space-gravity-1026.json. Native checkpoint capture retains the previously documented optional recovery-art fallback for the missing STOP sheet; it does not replace shipped graphics.

Review: http://127.0.0.1:54427/index.html
Evidence: C:/Users/Mike/Documents/New project/BOF-Space-Gravity-1026
