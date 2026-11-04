# November 3 — all-pilot gameplay ship quality

Ordinary launches now use the existing 960x1024 backing for the fixed 480x512 logical playfield. The previous default first reduced the approved aircraft to a60px canvas and the Furyship to48px, then enlarged that low-detail result with the whole game. The high-quality path samples those same sources at120/96 backing pixels respectively, preserving substantially more cockpit, armor, outline and engine detail before display sizing. Nearest-neighbor sampling stays enabled.

No sprite redesign, atlas reduction, artificial sharpening, new runtime effect, ship-size change, weapon-stat change or hitbox change. The9 aircraft sources and all pilot palettes of the authored Furyship keep their original animation/frame/socket owners. This change affects the whole backing surface, so menus, transitions and stage5/9 space flight receive the same consistent resolution. It is a rendering-policy correction, not a claim that low-resolution source artwork has been re-authored.

No-query, high, auto and default launches select2x. Slow frames no longer silently switch the game to native backing. Explicit `?quality=performance` or `?quality=low` remains available for slower hardware. `renderPerformanceTick` remains a compatible no-op loop hook. The core script version in index.html is refreshed; other scripts, including concurrent story work, are retained.

## Native verification

-389 focused checks pass;414 native renderer samples across all9 pilots, aircraft/space, banking,8 roll frames and8 aircraft/12 space somersault frames, plus paired1x/2x neutral crops. All registered banks decode; visible pixels are measured from the actual drawPlayer path. Pose contact sheets and actual Stage5/9 full-frame renders were inspected.
-Six fresh launch URLs verify960x1024 high backing versus explicit480x512 performance backing, with smoothing disabled.600 simulated slow-frame notices retain high quality. Logical aircraft height60 and Furyship size48 remain unchanged.
-No browser page/console errors in the focused run. Native syntax check passes.
-Required `node _BUILD_SOURCE/test_fl.js` still exits1 before its final summary on the recorded pre-existing `difficultyHealthBaseline15` setup error in combat_polish_0927b.js151. The test fixture was not edited.

## Performance limits

Sequential12s native observation scenes compare1x and2x backing in Stages1/7/5/9. Stage1 remains59.4/59.6FPS and Stage9 remains59.0/59.7FPS in this environment. Stage7 still has loading hitches (35.9/39.0FPS in this cold-transition sample). A space scene after these retained stage assets measures31.1/18.3FPS, so this is not a blanket claim of smooth long-session performance. An isolated fresh Stage5 A/B measures58.0/58.5FPS, draw mean2.22/5.90ms with residual first-use spikes. The sharper path has real render cost; retained-asset/loading pressure remains a separate performance issue. Keep the explicit performance option rather than automatically degrading ships. No playback speeds, enemy budgets or simulation rates were altered.

Reproduction: `_BUILD_SOURCE/pilot_quality_1103/`. Measured samples, source receipt and policy assertions: `docs/qa/pilot_quality_1103.json`. Actual PNG comparisons and pose sheets: `_shots/pilot_quality_1103/`. The source art is unchanged. Prior local changes are preserved; no commit or push.
