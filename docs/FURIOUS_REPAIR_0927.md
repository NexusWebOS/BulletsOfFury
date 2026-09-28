# Furious full-game review — implemented repair pass

This list records Mike's 2026-09-27 playtest request. Items are complete only after runtime verification.

- [x] Single Retina holds one target; separate rebindable Y multi-lock acquires visible enemies/objects sequentially.
- [x] Remove enemy pop-ins; readable difficulty-scaled arrival speeds and varied entry routes.
- [x] Diagnose and fix Stage 4 movement/scroll jumps under combat.
- [x] Stage 4 miniboss switches destroyed gun routines to rockets; scale rocket speed and helper activity by difficulty.
- [x] Stage 5 Furious Chromium armor overlay, activation sequence and generated animation/effects.
- [x] Stage 5 restoration checkpoints, reflecting stun barrier, critical hammer twirl/restoration counterplay and fast red rage jumps; apply to Hammer password too.
- [x] Hammer password supports ordinary continues.
- [x] Stage 6 readable moving dialogue, paused/dimmed left/right decision and banking route transition.
- [x] Stage 6 rebel story and HotWire/Phoenix tie-in; cinematic parley before combat, five individual overhead bars, fair modular fighter abilities.
- [x] Campaign route persistence: surviving rebels unlock central-core Stage X encounters; defeated rebels do not.
- [x] Generate Stage X card and looping terrain.
- [x] Enemy shields fit each hull; remove oversized spherical bubbles.
- [x] Stage 7 enemy balancing and removal of barricade projectile.
- [x] Stage 7 boss self-destruct escape, dialogue, pursuit explosions and toxic portal ending.
- [x] Stage 8 portal arrival and isolated-pilot dialogue; new alien code/symbiote terrain, enemies, attacks and first boss form.
- [x] Stage 3 larger readable ice balls and distinct boss/miniboss attack families.
- [x] Stage 2 faster magma cannon, fix laser-eye collision between retinas.
- [x] Native visual/gameplay verification; mandatory suite; sync Desktop checkout and playable release.

Previously completed repairs remain in `REPAIR_0927_RELEASE.md`. No GitHub push is included without a new upload instruction.


## Verification and limits — September 28

- Mandatory full regression: `==== FALVA/LIZZIE BUILD OK, 0 ERRORS ====` in `_shots/furious_0927/suite-final.log`.
- Stage 4 root cause was an extra Canvas restore in the modular-jet renderer. Native 45-second combat probe covered eight kills and all three affected jet types: no stack-depth imbalance or screen jumps.
- Native controls probe: C preserved its original target with zero multi-lock marks; Y acquired four separate targets and launched four missiles using four rounds.
- Native Stage 5 probe covered armor absorption, restoration thresholds, critical hammer interruption/rage and HAMMER death -> continue -> same fight with three lives.
- Stage 6 route pause preserved player position, scroll and timer for 120 updates. Native screenshots cover route choice, parley and individual modular fighters. Stage X deployed one rival, then recorded only that rival defeated while leaving four encounters available.
- Stage 7 escape reached stage stats and set the Stage 8 portal-entry flag. Native Stage 8 arrival retained the fixed player destination; the new first boss form emitted its binary volley without browser errors.
- Eight generated asset sheets/plates are in `assets/game/furious_review_0927/`. `generation.json` records the exact final prompts, built-in image generation method and original output paths.
- Release: 497,260,554 bytes (497.3 decimal MB); ZIP CRC passed for all 3,024 entries. Release scripts match source after PNG/WebP URL conversion. Native packaged-build smoke test initialized all nine stages and decoded all eight new assets: no browser errors or failed HTTP responses.

These are focused automated/native-rendered checks, not a complete manual nine-stage Furious replay. Enemy arrival is guarded against late sprite loading and starts beyond the camera edge; the difficulty speed changes and new attack balance still need that sustained human playtest. Stage 8 work intentionally covers its new enemy family and first boss form, as requested. Audio event wiring was checked, but loudness and mix were not evaluated on the user's speakers. Expansion remains separate. No GitHub upload was performed in this pass.

Source, new assets, tests and this report are synchronized to `C:/Users/Mike/Desktop/Github Coding/BulletsOfFury`; checksum evidence is saved in `_shots/furious_0927/local-sync.json` in the repair workspace. Earlier Desktop versions are backed up under `local_backup_furious_0928` beside the repair workspace.
