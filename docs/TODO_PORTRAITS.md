# Emotion Portraits — Recovered and Complete

The missing house-build portrait work has been reconciled with the repair line. The approved
runtime pack is present under `assets/game/pilot_portraits/`, its code-owned mappings remain in
`assets/game.js`, and the original source/reference material remains preserved under
`_ART_SOURCES/`.

## Verified coverage

- Pilots: all nine Fury pilots
- Emotion states: idle, smile/happy, anger, laugh, sad, victory, and crash
- Dialogue talk poses: closed, small, medium, wide, and O
- Runtime naming: `port_cf_<pilot>_<pose>`

The 35 legacy emotion PNGs were also compared with their packed atlas cells and were
pixel-for-pixel identical. No portrait task remains open in this reconciled repository.

The historical divergence and protected recovery references remain documented in
`docs/RECOVERY_AUDIT_0825.md`.
