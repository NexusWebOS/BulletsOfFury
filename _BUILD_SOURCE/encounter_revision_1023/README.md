# Encounter correction sources

Read `docs/ENCOUNTER_REVIEW_1023.md` in the repository for the player-requested behavior and verification limits.

The approved raw frames, identity references, generated manifests and PixelLab job provenance are stored here. No original personal photographs or upload credentials are included.

Rebuild order: `build_turrets.py`, `build_revision_art.py`, `install_latest.py`. Runtime outputs are copied to `assets/game/shared/combat/encounter_revision_1023/`; the installer is idempotent and keeps one correctly ordered script tag per owner. Set `BOF_GAME_ROOT` to use another checkout.

`record_final.py` uses the existing `_BUILD_SOURCE/furious_bot_1023/` controller and job list. Set `BOF_CAPTURE_DIR` to an ignored `_shots/` folder before recording. Full real-time takes are separate from the deterministic component/animation fixtures. Video source files remain in the local review workspace to avoid adding large movies to the repository.
