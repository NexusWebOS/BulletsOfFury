# October27: NG+ and final encounter review

`assets/ngplus_1027.js` owns this pass. Ordinary campaigns and password fights retain their original rules.

## New Game +

- Existing earned campaign receipt remains the gate: real final clear, stages1–7 recorded, then Stage8 finale. Debug encounters cannot mint the receipt.
- Dark recipes for all nine Forge weapon families are free NG+ rewards. Existing pause/loadout selection applies them; late weapon gates open in NG+, while pilot-specific families and Gravity Mode retain native restrictions. Purchased recipes continue to import normally.
- Free dark/profile imports do not count as spent run upgrade points. An unused free arsenal alone cannot offer a paid Re-Spec. Re-Spec can clear an equipped build; dark options stay available as an NG+ reward.
- Player damage +12%, excluding Maverick homing lances. Ordinary hostile health and boss/miniboss health +25%. Dracodia source copy pools and future module HP inherit one multiplier; first-host33.3/33.3/33.4 budget stays native (integer part rounding retained).
- Boss/miniboss actual decreasing attack cooldowns and idle/recovery clocks advance15% faster. Global simulation time, warning/charge clocks, movement, hostile bullet speed, protected cinematics and death clocks are not multiplied. This is a cooldown/recovery increase, not a blanket speed-up of the whole encounter.
- NG+ ordinary enemies have a stable biome element, with selected fire/ice/lightning/dark counter-elements. Generic small rounds use the existing elemental artwork baked to16 frames x32 directions, fixed72px cells and36px pivots. Physical missiles and special boss projectiles keep their original owners; ordinary bullets remain unshootable.

## Stage X

The existing reward already unlocks Signature MKII for all nine pilots, Super Missiles,12 missiles, one life and one bonus Forge combination. Both routes are verified. This pass gates the supply call on native defeat and retains the extra Forge point through save/load and Re-Spec; campaign receipt and one-award guards remain.

## Verification and footage

Reproducible native check: `_BUILD_SOURCE/probe_ngplus_1027.py`. Rebuild directional plates: `_BUILD_SOURCE/build_ngplus_1027.py`. Actual source hashes, source frames and geometry are in the new manifest. Syntax and native Chromium checks pass. The full required suite reaches its summary with the same five prior assertion failures; see QA JSON for names.

Fresh Furious footage covers Harrier/Nightwing, Rebels, Siege Bomber, Dredger, Warden, Herald and the full Dracodia fight. Phase1, full Phase2, formation, base final life and all four alternate forms have separate videos. Each form video joins all visits from one native continuous fight, with its cuts disclosed in the gallery. The complete source fight is included. Cole uses native GOD and an input-only bot; enemy HP, attack decisions and phase progression are native. A separate65-second NG+ opening-wave preview verifies dark player weapons and multiple enemy elements in actual play.

An initial Dracodia take had a58.9-second observation/capture stall and was retained outside the final gallery. The final take warms the forms before recording and runs without overlapping test/encoding work. Both are preserved; final gallery and delivery manifest identify the selected take. These recordings prove native encounter completion, not human difficulty fairness. Full human survival balance and future NG+ extras remain design review work.

Local artifacts: `C:/Users/Mike/Documents/New project/BOF-Final-Pass-1027/`. No commit or GitHub push in this pass.

Final evidence:46 native NG+ checks,93 combined gameplay/video assertions and all16 Chromium play/seek/audio checks pass. All nine directional banks have even fixed cells and no edge clipping. The selected final Dracodia film is1013.23s (16:53),1280x800/30fps, with37.54 average native renderer frames/s and a0.988s maximum observation gap. Zero page/console/HTTP asset errors in the final take; recorded request cancellations are native audio voice aborts. Every exported audio peak remains below0dB; final full film peak is-0.5dB.

Review gallery: http://127.0.0.1:54814/index.html. The earlier stalled take and its chapters are retained but excluded from this gallery. Native GOD footage is useful for form/attack review; it is not a human survival or fairness sign-off. The long final encounter should be reviewed as a pacing decision before calling the game release-ready.
