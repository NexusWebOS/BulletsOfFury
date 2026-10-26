# Stage1 paired jet entrance — October26

Owner: `assets/feedback_1009.js`, `fb9SwoopTick`.
Replaced the asymmetric reversing somersault path with mirrored cubic entrance/exit paths, a 0.48-second row, and tangent-aligned heading. Minimum center spacing is 184 game pixels. Native aimed twin machine-gun bursts begin in the row and continue during outward departure; the silent partner convention is retained.

Verification: `_BUILD_SOURCE/probe_jungle_pair_1026.py`; capture/report in `_shots/jungle_pair_1026/`. Syntax checks passed. Full `_BUILD_SOURCE/test_fl.js` exits 1 before its assertion summary because `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing (existing suite blocker).

Directional-frame correction: fb9SwoopDraw now selects the existing air13_s1_s1jetdelta_heading eight-direction bank with air13Pose/air13Blit. No canvas rotation or CSS transform is used for these hulls. Fixed common cell/pivot/scale; native hit tint retained. Probe also verifies distinct heading frames.
