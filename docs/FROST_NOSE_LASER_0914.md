# Frost Cruiser nose laser correction - 0914

Mike identified the wing pods as missile turrets and requested Falva-style black/blue laser bolts from the nose. S3-14 records this correction separately from the pending charged laser sweep and difficulty-pattern work.

Frost Cruiser's nose now launches a 24 x 112 laser bolt every 0.34 seconds during the lateral firing pass. Its rear end starts at the physical C mount, including the Hard/Furious hull scale. Aim is committed at release; the bolt does not home, accelerate like a missile or become shootable ordnance. The paired missiles remain on L/R wing turrets. The shared Jungle Cruiser keeps its existing machine-gun nose attack.

The art is Falva's actual helper-ball laser (`fllaser_0`, inspected through XART), held on one source cell. A cached luminance-based palette maps its shading to black, dark blue and a blue-lit core while preserving source alpha. Four stepped lighting levels and a clipped six-pixel band animate at 12 ticks/second using projectile age. The silhouette, footprint and opacity remain stable; there is no blur or frame cycling. Existing laser muzzle art and laser sound are triggered once per nose shot. The new kind is registered in PROJ, and its dedicated renderer takes precedence over generic arsenal art.

The laser's hit test rotates with its shaft, inset from the glowing edges. Offscreen cleanup allows the entire tail to leave before removing it. A source-readiness guard defers shots rather than releasing an invisible hazard. Existing source images, music, atlases and test harness are unchanged.

## Verification

Fifteen native Chromium checks passed through `_BUILD_SOURCE/frost_nose_laser_0914/probe.py`: nose rear anchor, dimensions, stable non-homing flight, both missile mounts, sound dispatch, Jungle Cruiser exclusion, exact alpha preservation, blue palette, actual changing rendered pixels at fixed dimensions, real director cadence, shaft-hit and adjacent-safe-lane callbacks, diagonal collision, full-tail cleanup, and the Hard hull variant. No page, console or game-loop errors.

Falva's source strip, four lighting phases, normal and Hard firing scenes and wing missiles were visually inspected. `_shots/frost_nose_laser_0914/Frost_Cruiser_Nose_Lasers_0914.mp4` is a nine-second silent native recording, decoded after capture. The fixture uses debug fights, controlled entry phases and player-hit interception; it verifies this weapon correction, not every phase's difficulty balance. Laser sound calls are verified, but the silent preview does not demonstrate the audible mix.

Final syntax and full-suite results are recorded in `qa/frost_nose_laser_0914.json`. No commit or push.

Syntax passed. Full suite reached its final summary: 3,852 passing assertions / 58 inherited failures, exit 1. No new failing assertion names against the last recorded baseline.
