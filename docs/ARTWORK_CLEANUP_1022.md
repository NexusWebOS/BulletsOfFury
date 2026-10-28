# Verified artwork cleanup — October 22, 2026

Applied Mike's verified artwork cleanup to the official game. Removed135 retired runtime files and19 superseded physical atlas cells. Three shared atlases were rebuilt; the retired Cole-only pose atlas was removed. Runtime savings:19,219,725bytes (19.22MB). Six legacy Cole pose names remain aliases to his current body artwork.

All retired originals remain hash-verified under `UNUSED_ASSETS/retired_art_1022/`, with pre-cleanup manifest, atlas and test-harness snapshots in `_snapshots/`. `installation.json` records installed hashes and removed paths. Exclude `UNUSED_ASSETS/` and `_BUILD_SOURCE/` from shipping. The development-only `retired_art_archive_1022.cjs` resolver lets existing integrity checks inspect exact archived reference pixels; it is not loaded by the game.

Gameplay code, attack clocks, controllers, collision, animation timing and official audio files were not edited. Recent approved artwork and conditional loading fallbacks remain.

Installed verification: syntax checks pass; full official core suite8943 assertions,0errors, exit0 and final BUILD OK. All9 native Chromium stage starts and60 manual frames per stage pass with0page/console errors and0missing assets;109 aliases match staged browser pixel hashes. All220 retained cells in rebuilt atlases are pixel-identical. This is a stage-start smoke test, not a complete campaign playthrough. The test server backlog was increased and asset loads allowed to settle after an initial local connection failure.

Rollback: use the exact originals and `_snapshots/` from the archive, checking the installation hashes before replacing any later edits. Preserve later user changes; do not blindly restore whole files. No commit or push.
