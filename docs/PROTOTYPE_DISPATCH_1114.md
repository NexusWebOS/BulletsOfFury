# Prototype pieces, single-panel satellite and original-aircraft departure

Mike revised the Stage 4-to-5 scene: the team discovers the Federation kit in separate pieces, the support pilot explains that it binds to the aircraft during ascent, the threat continues hacking Earth's networks, and one pilot volunteers to trace it. Silent visual inserts should be one giant comic frame with no empty dialogue box. The departure must use the selected pilot's unconverted aircraft.

The late owner is `assets/prototype_dispatch_1114.js`, following `cinematic_rework_1114.js`. It replaces only the active post-Stage-4 rows and the two silent visual inserts. The earlier Stage 3 water, escape, satellite discovery and six-panel workshop remain with CW16. The kit's actual binding, assembly timing, whiteout, conversion and gameplay handoff remain with the existing Stage 5 owner.

## Dialogue and roles

The selected pilot reports that the kit is in separate pieces and asks the actual technician about it. Decker explains the Federation binding technology; Cole responds when Decker is the selected flying pilot. The support line explicitly refers to Decker's engineering work in that case. The revised network-hacking, volunteer and “Awaiting your orders, sir!” lines use Mike's requested wording with spelling/punctuation cleanup. The earned Stage 4 upgrade event remains exactly once, including Maverick's route, without changing his weapon stats.

The Stage 5 ascent's existing dialogue clock and text are retained. Its speaker/portrait now follow the same support-role helper, so flying Decker receives the call from Cole. No native assembly clocks, part coordinates or kit readiness flags are rewritten.

## Presentation and aircraft

The satellite is one new 1280×720 illustration, displayed in a full 888×488 comic panel. It uses the approved satellite design and exactly two-eyed symbiote reference. The image fills the scene with the parasite gripping the satellite and alien data streaming toward Earth. It has no dialogue box, empty reaction panel, name label or caption. The next speaker cuts in without restoring the retired small insert.

The departure is also a full panel without a dialogue box. It draws `ship_<pilot>` and the native glow/thruster sockets directly through `pt11OpeningShip`. No converted `ship-space` illustration is used. The aircraft climbs smoothly with a fixed horizontal position over the existing scrolling ascent sky/cloud assets. Co-op uses the actual selected pair. Presentation does not set `run.gravityShipReady`; the kit attaches later through the native Stage 5 assembly.

All nine current normal aircraft were exported from the real Chromium XART renderer and inspected before use. Their identity references/hashes are retained under `_ART_SOURCES/prototype_dispatch_1114/aircraft-references`. No aircraft were generated. Built-in image generation produced only the new satellite illustration. Its exact prompt, source, reference paths and shipping path are in `docs/PROTOTYPE_DISPATCH_ART_1114.json`. SpriteCook was not used.

## Verification and preview

Forty-nine native Chromium checks pass: every pilot's kit/technician dialogue, earned upgrade, actual normal-aircraft bitmap draws, absence of premature conversion/caption, stable ascent, full satellite panel, clean transition out of that panel and Cole's actual native ascent call to flying Decker. Native screenshots were inspected for the satellite, Cole's departure and the role swap. No page, console or HTTP errors were observed.

Syntax checks pass. The full core suite reaches its final summary with 8,969 passing assertions, zero errors and exit 0. Failing names remain empty compared with the prior baseline. Core `assets/game.js` and `_BUILD_SOURCE/test_fl.js` were not edited.

The fresh complete Stage 4-to-5 recording includes the new scene and the native Stage 5 ascent/kit assembly through gameplay. It is a cinematic-checkpoint reel with no dialogue skipped; gameplay between scenes is omitted. It is not a campaign playthrough. Its chapter page is `http://127.0.0.1:8766/_shots/prototype_dispatch_1114/review.html`. Raw captures, media/decode/volume receipts and browser chapter tests are retained alongside the movie and in `docs/qa/prototype_dispatch_1114.json`.

The final recording is 95.62 seconds at 1824×1024/30 fps, H.264/AAC, with embedded chapters and fast-start metadata. It decodes without errors. Audio mean is −14.6 dB and peak −1.7 dB. Eleven browser playback checks pass, including all eight chapter jumps with actual decoded frames and byte-range seeking. The original aircraft is visible before conversion; the native assembly/countdown then finish with `run.gravityShipReady=true` at the gameplay handoff. Both native scene continuations occur exactly once.

Reproduction helpers are `_BUILD_SOURCE/prototype_dispatch_1114_probe.py`, `_BUILD_SOURCE/prototype_dispatch_1114_record.py`, `_BUILD_SOURCE/prototype_dispatch_1114_package.py` and `_BUILD_SOURCE/prototype_dispatch_1114_verify_movie.py`. The pack helper rebuilds staged art/manifest from the canonical source and prompt record. Capture uses the game server on 8765; chapter playback uses the existing byte-range-capable preview server on 8766.

Earlier recordings and assets are preserved. No commit or push was performed.
