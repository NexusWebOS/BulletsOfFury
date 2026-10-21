# Retina palette consistency — October 20

Mike reported wrong regular and Multi-Retina colors, particularly Lizzie, Decker
and Axel. Restored the explicitly authored targeting palette from the existing
Retina specification (docs/PASSOVER_0806a.md, section34):

| Pilot | Targeting color | Hex |
|---|---|---|
| Axel | Blue | #2f6fff |
| Decker | Yellow | #ffe11a |
| Lizzie | Gold | #ffc21a |
| Cole | Neon green | #39ff5a |
| Yuri | Red | #e02020 |
| Falva | Pink | #ff4fa3 |
| Freezer | Purple | #9a4fe0 |
| Juggernaut | Orange | #ff8a1a |
| Maverick | Forest green | #1f7a3a |

The personal targeting palette is separate from hull/HUD/dialogue colors. The
October10 dialogue adapter had overwritten Decker's yellow targeting with orange
and Lizzie's gold with a lighter yellow. It now extends only Rebel scanner colors;
Decker's orange dialogue and the existing Rebel identities remain unchanged.

All boss/miniboss Retina graphics are now palette-swapped to the selected pilot's
Retina color; previously several main pilots fell through to old pre-colored
nbret plates (including Axel's wrong hue). Ordinary seeking/locked frames use
luminance-preserving color compositing rather than multiplying a residual source
hue. Target halos and fallback brackets use the same Retina palette instead of
the different ship/HUD color. Composites remain cached, without runtime pixel reads
or new artwork. Existing frame clocks, geometry, lock validity, timers, missiles,
damage and Multi-Retina's per-seat controller are unchanged.

Owners: assets/game.js (retinaColor, retinaTinted, drawRetina, drawBossRetina) and
assets/part2_combat_1010.js (palette extension and boss renderer). Both script URLs
use retina-colors-1020. No atlases changed.

Verification: native Edge53/53, zero page/console/draw/missing-asset errors;1,152
rendered combinations covering9 pilots ×4 difficulties ×regular/multi ×ordinary/
boss ×seek/lock ×4 frames. Neutral backgrounds isolate the visible Retina hue
from terrain blending. Co-op proves Axel and Decker retain distinct colors and
restore seat state; real two-target acquisition/launch spends two missiles on
each difficulty. All native pilot screenshots visually reviewed. Full regression
reaches FALVA/LIZZIE BUILD OK,0ERRORS; game.js syntax passes. No full campaign
rebalance or performance benchmark is claimed. Probe:_BUILD_SOURCE/
probe_retina_colors_1020.py; report:docs/qa/retina_colors_1020.json; native gallery:
_shots/retina_colors_1020/review.html. Local only; no commit/push requested.

The first full regression run exited1 on one obsolete assertion requiring the old
Lizzie shade. The fixture now asserts Axel blue, Decker yellow and Lizzie gold,
plus separate Rebel/dialogue identities and protection against the Decker
overwrite. The complete rerun reaches its successful final summary. The original
nonzero log is preserved; _BUILD_SOURCE/test_fl.js itself is unchanged.
