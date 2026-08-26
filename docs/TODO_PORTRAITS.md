# Emotion Portraits — Recovery Required

Do not mark the portrait task complete on `codex/bugfix-continuation` yet.

## What is preserved locally

- `_ART_SOURCES/BOF_EmotionPortraits_0825/` contains 36 source PNGs plus `SOURCE.md`.
- These are source/reference portraits, not the complete live portrait installation.

## What is missing from the current runtime tree

- `assets/game/pilot_portraits/` is absent from `codex/bugfix-continuation`.
- The live game therefore does not have the 108 runtime portrait files installed by the house/Codex branch.
- The prior text saying the portraits were "preserved in this branch" was misleading: the source subset is here, but the complete runtime pack is not.

## Where the missing portrait work exists

GitHub branch `origin/codex/codex-edition`, commit `747424493156ba1d0ca63c8c3a0c06071521cfe3`, contains:

- 108 files under `assets/game/pilot_portraits/`;
- 127 files under `_ART_SOURCES/CF_PilotPortraits-Vol1_0825/`;
- the manifest/runtime wiring in `assets/game.js`;
- the updated portrait verification tests.

Recover this work by content-aware reconciliation with the current repairs. Do not replace `assets/game.js` wholesale and do not reset either branch to the other.

See `docs/RECOVERY_AUDIT_0825.md` for the protected branch tips and the complete recovery warning.
