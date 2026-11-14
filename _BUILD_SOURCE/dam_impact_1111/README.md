# Stage1 helicopter dam impact and white-fade reveal — November11,2026

Mike corrected the Stage1 helicopter death: it must spin into the dam and explode, then use a white screen flash that fades back to the destroyed dam. H127 supersedes H126's Stage1 offscreen exit. Dracodia's copied-helicopter death remains under its previous director.

## Finished sequence

The existing accelerating spin/cook-off begins at the actual death position. A forward-only3.6s terrain approach brings the actual CoastlineDam plate into view. The helicopter reels toward a lower staging point, then flies into the central gate at source coordinate(340,286), measured from the approved680x4212 intact/destroyed plates. The camera settles before impact; current source-window geometry owns the aircraft's final world position. It never snaps or scrolls backwards, including when the dam is already in view.

The native shatter blast begins at6.65s. An authored full-screen white pulse rises over160ms, holds180ms, then fades back over1.18s. The damaged plate swaps at6.83s while every screen pixel is white. Camera framing remains fixed during the swap/reveal, so the broken gate replaces the intact gate at the same position. The normal background, player and debris emerge as white recedes. The existing post-helicopter raid still opens at8.6s. Native reward, Forge/Continue drops and raid ownership remain unchanged.

Reduced motion uses a slower420ms white buildup,160ms hold and1s reveal; its plate swap also happens at full white. Pause freezes the aircraft, map travel and white frame together. Retry clears the owner and flash. No fullscreen white remains after the transition.

## Source and integration

New late owners: assets/dam_impact_art_1111.js and assets/dam_impact_1111.js. Nine small pages under assets/game/shared/combat/dam_impact_1111/ contain33 fixed480x512 authored white/alpha levels, drawn with ordinary image blits. No runtime opacity, filter, additive blend or procedural full-screen effect was added. The editable white-flash.aseprite intensity bank retains all levels; five exported source states match exactly. Native motion selects those states for rise/hold/fall.

H126 received only a position-selection helper and optional dam-swap time. Its default path math is unchanged. H127 supplies the Stage1 path/camera/swap/flash behavior; all other forms delegate unchanged. game.js, HC79, H125, D124 and the native Stage1 repair/raid owner are byte-identical. Source archive: _BUILD_SOURCE/dam_impact_1111/. Source/raw dam measurements, guarded installer, pre-change backups, edited H126 candidate, exact flash frames, Aseprite source and QA are retained.

## Observed verification

37 scoped checks pass. Native Normal/Furious recordings confirm the aircraft hits the actual gate, scroll moves forward and holds for impact, the full framebuffer becomes RGB255 white, the map switches only at full white, fade/reveal completes, the destroyed dam appears and the native raid/reward continue. Easy/Hard, early/late map positions, reduced motion, pause and retry checks also pass. Dracodia's default trajectory matches its prior equation exactly. All flash pages and both terrain states preload before use. No browser/console/draw errors occurred.

Required syntax checks pass. The full suite still exits1 at the recorded missing difficultyHealthBaseline15 helper (combat_polish_0927b.js:151 / test_fl.js:4537), before its final summary. That unrelated failure remains unchanged.

## Review media

dam-crash-transition.mp4 shows Normal then Furious. dam-crash.gif shows the Furious sequence. Real-renderer checkpoints start near the boss encounter, with a stationary invulnerable presentation pilot and real native lethal damage. Death clocks are not edited during the recorded sequence. No commit, push or installer.
