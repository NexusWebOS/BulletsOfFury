# PixelLab lightning with body depth — 18 October 2026

Mike rejected the crescent chain in Dracodia's spiral attack and requested real
animated lightning behind, over and around him, plus PixelLab lightning for the
Stage 4 Storm Sovereign. This pass replaces the electrical artwork in those
encounters through `assets/lightning_depth_1018.js`.

## Generated artwork

PixelLab supplied five text-generated seeds and four 32-frame animation clips.
There were no local reference uploads or credit purchases. One edge-clipped
tether seed and eight orb poses that flattened into simple circles are excluded;
their source files remain preserved. The selected orb cycle has 24 crackling
poses. Forked bolts, horizontal tethers and the surrounding electric wrap each
retain all 32 generated poses.

The owner workflow is `_BUILD_SOURCE/build_lightning_depth_1018.py`. It registers
152 shipping PNGs in `assets/lightning_art_1018.js` and `ART_TAXONOMY.json`:

| Bank | Poses | Shipping canvas | Pivot |
| --- | ---: | --- | --- |
| Forked bolt | 32 | 160 × 160 | 80, 80 |
| Crackling orb | 24 | 128 × 128 | 64, 64 |
| Generator tether | 32 | 288 × 160 | 144, 80 |
| Wrap behind body | 32 | 320 × 320 | 160, 160 |
| Wrap in front of body | 32 | 320 × 320 | 160, 160 |

Every bank uses even, uniform canvases, one shared pivot and proportional scale.
The builder adds transparent padding without fitting individual frames or
interpolating duplicate poses. The rear/front wrap plates partition the same
generated frame and reconstruct its visible pixels exactly. The runtime draws
the rear plate, actual authored boss, then the matching front plate with the
same frame, center and transform. Transparent RGB is cleared only where alpha
is already zero. Loop/onion sheets and seam measurements live in the source
registration and ignored native evidence directory.

Generation IDs, prompts, selected indices, billing observations and authorization
scope are under `_ART_SOURCES/lightning_depth_1018/`. Existing assets remain on
disk; the crescent bank is retired from this attack and its frame-review menu.

## Encounter integration

Dracodia's spiral charge and active storm use the synchronized wrap around his
moving main body. Outgoing spiral actors use actual animated, forked bolts that
follow their existing curved trajectories. His core and arm charge sockets use
the new crackling orb cycle. The original hover, physical shoulder swipes,
arm/core emitters, attack clocks, damage and owner/part flashes remain native.

Storm Sovereign uses the same generated wrap during electrical charging and
its existing panic/ram/rear phases. Its four generator connections use animated
tethers between the existing moving endpoints, and its real released lightning
balls use the crackling bank. Scoped overrides leave other bosses' beam and
projectile graphics intact. Stage 4's FOV warnings, sounds, attack cadence,
shield/core rules and unshootable lightning balls remain authoritative.

The first native run caught three failures: Stage 4's actual early ball renderer
still selected its older artwork before reaching the generic projectile hook.
The final integration owns that real `tb28BallDraw` route and the other existing
Stage 4 ordnance routes. The corrected native run draws the new bank in real
volleys at Normal, Hard and Furious.

## Native verification

219 Chromium checks pass: 48 focused art/depth/combat checks, 71 archive combat
checks, 50 Storm Sovereign regression checks and 50 delivered review controls.
The runs report zero page, console, drawing or missing-asset errors. The focused
probe renders every actual XART pose through the game's own context, compares
all 32 rear/front compositions, measures rear-body/front occlusion, exercises
actual damaged pixels and flash expiry, and verifies native player damage,
warning timing, cleanup and Stage 4 interception immunity.

The original `assets/game.js`, `_BUILD_SOURCE/test_fl.js`, Stage 8 identity and
Storm Sovereign controller hashes match this pass's starting baseline. Game.js
retains LF; test_fl.js retains CRLF. Full-suite results and source hashes are
recorded in `docs/qa/lightning_depth_1018.json`.

Two 52-frame GIFs capture actual native gameplay with the full playfield and
side HUDs. They are under `_shots/lightning_depth_1018/`, with contact sheets,
onion sheets, result JSON and test logs. These are controlled native encounter
tests; this pass does not claim a new full-campaign balance playthrough.

## Review

- Dracodia: `docs/previews/dracodia_archive_1018/index.html?scene=spiralLightning&difficulty=furious&revision=lightning-depth-1018`
- Stage 4: `docs/previews/storm_assault_1018/index.html?scene=charge&difficulty=furious&revision=lightning-depth-1018`
- Frame/onion controls: `docs/previews/dracodia_archive_1018/frames.html?bank=wrap`

Both encounter reviews repeat the selected native attack, keep the full game
field of view, and isolate review saves from the campaign. The production entry
loads the new manifest and renderer after the existing encounter extensions.
