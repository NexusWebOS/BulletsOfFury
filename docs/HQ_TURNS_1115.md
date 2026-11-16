# November15: frame-by-frame banked HQ turns and faster departures

Original BOF at `D:/BOF-Downloads/2026-11-14/RevG-source`. Mike requested frame-by-frame turning and quicker fly-outs after the HQ animation reel. The existing authored per-pilot banking poses and native nozzle/exhaust animation supply the art. No new aircraft design or image generation.

Each actual pilot aircraft now plays a20-cell banking/heading/exhaust sequence on fixed256x256 cells, pivot128,128 and one physical104px hull scale. The native source art is exported through Chromium; per-pilot bank handedness is respected. Wings visibly bank and return to level. Runtime departures select a source cell and draw it proportionally, with no continuous rotation of a static hull or per-frame raster generation. Guard emergence/aiming likewise uses discrete15Hz bank poses and smooth target changes. Original9 aircraft plus Lizzie's actual B42 alternate are preserved:10 pages/200 cells. All source exports, geometry and registry metadata remain under `_ART_SOURCES/hq_turns_1115`; runtime pages under `assets/game/shared/cinematics/hq_turns_1115`.

Individual exit time2.6→1.3 seconds, exactly2x speed at corresponding path progress. First-wave spacing2.8→1.5 seconds keeps a0.2s gap; the seven-plane launch beat21.7→12.6 seconds. Southwest/southeast alternation and proportional scale-up remain. Decker leaves at defense time8.8; Axel now follows at10.3, also individually. The five-second quiet interval, six takedowns, shared mixer cues, dialogue and native Stage6 handoff remain. Earth hold, doors, pilot walk/cheer/radar banks and native Chronos destruction/rewards remain unchanged. game.js/tests and global gameplay flight controls are untouched.

Verification:42/42 native turn checks, including200 exact/unclipped source cells, all20 actual atlas selections for each of9 pilots, zero runtime rotation calls during those departures,1.3s timings and actual B42 selection.26/26 native lifecycle checks preserve all11 HQ beats, single-file9-ship alternating order, six kills,5s empty base, frozen Earth/starfield, original metal portraits/audio and native settlement. No page/console/HTTP errors. Full suite8,969 passed/0 failures,exit0, unchanged empty failing-name list. Syntax passes; game.js LF and tests CRLF retained. All10 pages/registry reproduce byte-for-byte from saved source cells.

Focused native recording53.90s, H264/AAC1824x1024 at30fps with game audio; zero full-decode errors. Eight chapter playbacks, video geometry/duration,Range206, browser errors and all9 GIF decodes pass12/12. Audio: [Parsed_volumedetect_0 @ 00000250820c6dc0] mean_volume: -13.9 dB; [Parsed_volumedetect_0 @ 00000250820c6dc0] max_volume: -0.2 dB. Prepared Cole/Hard checkpoint from the HQ squad launch, through the five-second pause, base attack/counterattack and both fast guard exits into Stage6's first interactive interception. Earlier homecoming omitted; no cinematic dialogue skipped inside the checkpoint. This is not a full campaign win or balance test.

Video: `_shots/hq_turns_1115/hq-turns-fast.mp4`.
Review: http://127.0.0.1:8766/_shots/hq_turns_1115/review.html
Owner: `assets/hq_return_attack_1114.js`; art registry `assets/hq_turn_art_1115.js`.
Evidence: `docs/qa/hq_turns_1115.json` and `_shots/hq_turns_1115`.
Repack from saved cells: `_BUILD_SOURCE/hq_turns_1115_pack_saved.py`.
Re-export from current native art: run `_BUILD_SOURCE/hq_turns_1115_export_refs.py`, then `_BUILD_SOURCE/hq_turns_1115_build.py`, then `_BUILD_SOURCE/hq_turns_1115_variant.py`. Outputs go into the ignored review install directory for comparison.
Native probe, lifecycle, record, package and movie-verification scripts share that prefix. Prior owner/index/captures are preserved. No commit, push, installer or release.
