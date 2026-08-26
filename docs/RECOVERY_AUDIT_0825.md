# Bullets of Fury Branch-Recovery Audit — 2026-08-25

## Reconciliation status — completed locally

The two known repository lines have now been reconciled on
`codex/reconciled-house-and-repairs`. The branch was built from the complete house/Codex tip
`877c783`, then the repair commits were replayed and resolved feature by feature.

The reconciliation preserves:

- the complete pilot portrait runtime pack and sources;
- the corrected Stage 8 sky, modular scenery, transitions, music, and house graphical work;
- the Doomsday Carrier Mk II and newer house boss/projectile mounts;
- the generated Hellwing **HERALD OF DEATH** as the live Stage 8 miniboss;
- the generated combat-SFX bank and corrected weapon identity;
- the energy-shield system and source pack;
- the no-fade, authored 125%-of-unit death-animation contract.

Safety references were created before reconciliation:

- `safety/pre-merge-repairs-20260825` at `16f23df`;
- `safety/house-codex-877c783` at `877c783`.

The audit below is retained as the historical record that prevented either line from being
overwritten. The home-workspace follow-up still applies to work created after `877c783` that may
never have reached GitHub.

## Stop: do not overwrite either line

The GitHub repository contains two divergent development lines. Neither line is a complete substitute for the other, so do not use a hard reset, force push, directory replacement, or wholesale `assets/game.js` checkout.

Protected reference points:

- House/Codex remote line: `origin/codex/codex-edition` at `877c78358da0386946fa93e6b48667e7445eadc6`.
- Current repair line: `codex/bugfix-continuation` at `946c2d1` when this audit began.
- Common ancestor: `3bcee0d0efed7b95036f6f1e4f7cf84dcf14af50`.
- Divergence at audit time: 38 commits only on the house/Codex line and 9 commits only on the repair line.

The remote branch was refreshed with `git fetch --all --tags --prune` before this comparison. No merge, reset, checkout, push, or asset replacement was performed.

## Confirmed missing from the current repair line

### Complete runtime portraits

Commit `747424493156ba1d0ca63c8c3a0c06071521cfe3` (`Codex Edition: install pilot portraits and Level 6 combat fleet`) exists on the remote house/Codex line. It contains 108 runtime files under `assets/game/pilot_portraits/` and 127 full-pack source files. The current line has the smaller 36-PNG emotion-source subset but does not have the runtime portrait directory.

### Corrected Stage 8 sky/background pass

Commit `37dcce08c768e298f69f1ef347bb560e80ce7a69` (`Furious Death - stage 8 runs the modular sky with parallax scenery`) is remote-only. It adds `assets/game/nst8_sky_master.png`, Stage 8 modular/parallax runtime changes, tests, and `docs/proofs/l8_furious_death.png`. The master is absent from the current repair line.

### Prior graphical work

The remote-only sequence contains substantial graphical work that must be reviewed before any final build is declared complete, including:

- Stage 6/7/8 environment, portal, connector, and transition work;
- palette/halo cleanup across stage masters;
- cinematic approach and top-down transition art;
- weapon icons, effects, projectiles, damage overlays, and Level 6 fleet art;
- Spawn Carrier effects and other older miniboss material;
- the later portrait and user-asset installation.

This explains why the current game can look older even though GitHub was reported as updated: the update landed on `codex/codex-edition`, while later repair work continued from `main` and then diverged.

## Stage 8 miniboss rule

The remote line contains the older Spawn Carrier assets and effects. The current repair line deliberately replaces the live Stage 8 miniboss with the generated Hellwing-based **HERALD OF DEATH** in commit `8f5426d` and fixes its destruction behavior in `946c2d1`.

During recovery:

- keep the current Herald of Death identity and complete Hellwing hull;
- do not restore the retired Spawn Carrier as the live miniboss;
- review the remote-only Spawn Carrier/teleport/effect art selectively for reusable effects only;
- preserve the current no-fade, authored 125%-of-frame destruction contract.

## Music and sound status

Music changes from the home session are **not yet proven complete** on the current line and must remain on the recovery checklist.

What the repository proves:

- remote-only commit `550508835fa745b367a1469d973f7331f65627ae` wires four corrected sounds and adds `assets/game/sounds/lz_stack.wav`;
- remote-only commit `f49e77cc5faec12a02762723eead9df93e19c332` says it restores combat audio and modifies `assets/game.js`;
- the current line independently adds the larger generated combat-SFX set in `ab68b59` and later wiring fixes;
- only one audio file path is present on the remote tree but absent from the current tree (`lz_stack.wav`), but code routing can still be missing even when sound files exist;
- no audit result proves that all home-session music selections, timing, or routing were uploaded.

Therefore, do not replace the current sound folder or current audio routing wholesale. Reconcile the remote audio commits with the current generated-SFX implementation, then compare the home workspace for any never-pushed music files or code.

## Safe reconciliation procedure

1. Preserve both exact commit IDs above and begin reconciliation on a new branch.
2. Inventory all 38 remote-only commits by subsystem instead of merging the whole branch blindly.
3. Bring over non-conflicting binary assets first, retaining their original paths and manifests.
4. Reconcile `assets/game.js` and `_BUILD_SOURCE/test_fl.js` manually, feature by feature; both lines changed these files heavily.
5. Keep the current Herald, shield system, elemental rules, weapon-identity fix, and authored death transitions unless a deliberate replacement is approved.
6. Re-run the automated harness and visually playtest every recovered stage, portrait state, transition, miniboss, boss death, music cue, and continuous weapon.
7. Only after verification should the reconciled branch replace the playable build or be pushed as the new canonical line.

## Home-workspace follow-up

Ask the home-session GPT for:

- the exact branch name and final commit hash it pushed;
- whether it pushed to `codex/codex-edition` or another branch;
- a clean `git status`, `git log -5 --oneline --decorate`, and `git remote -v` from that machine;
- a list/archive of untracked portrait, Stage 8, miniboss, music, and graphical asset files;
- confirmation that Git LFS or partial-clone objects completed uploading.

The newest branch tip currently visible on GitHub is `877c783` from 2026-08-25 13:20 EDT. Anything completed at home after that point may never have reached this repository and cannot be declared recovered until the home machine is checked.
