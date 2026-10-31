> Current weapon behavior and recording: TIDAL_FORWARD_FANS_1029.md. Forward spreads, northbound fan geysers/marked return and exploding fan grenades supersede the old roller behavior.

# Correct Stage2 water triplets and visible fan swirl — October29

[Corrected water-wave chapter](http://127.0.0.1:51046/?tidal=stage2-waves-fans-1029&chapter=waves#clip=stage9-tidal-walls) · [Fan rotation](http://127.0.0.1:51046/?tidal=stage2-waves-fans-1029&chapter=fans#clip=stage9-tidal-fans) · [Full fight](http://127.0.0.1:51046/?tidal=stage2-waves-fans-1029#clip=stage9-boss)

Mike rejected the vertical water strip from the previous pass. It came from the wrong source: the player's nib_wall weapon graphic. This correction uses the actual Stage2 WFX hazard, nwf_fire_0 through nwf_fire_7 from fx_weather_1. Original Stage2 assets/code are read only.

The eight frames retain their silhouettes and use the same vertical flip as Stage2, with an authored navy/royal-blue/cyan/white water palette. Six approaching widths190/242/294/346/398/452 are baked into48 fixed480-square cells; the runtime selects frames without transforms/tints/compositing. The small falling-wave derivative also uses this source; the vertical strip is no longer rendered. Wave collision samples the same authored alpha frame at the player hitbox, rather than a tall rectangular placeholder.

The actual Stage2 constants control the attack: .75s sequential warning steps,1.1s final warning hold, then waves descending from y=-140 at(VH+300)/1.25px/s. The next wave waits for the previous one to leave at VH+180. Three lanes use .22/.50/.78 of the visible area. Queued asterisks stay until their own wave launches. Defeat/half-health may cancel a remaining wave normally.

Each fan now rotates the actual spiral source pixels inside its measured15px-radius disk. Left/right rotate oppositely through16 authored phases per second; the metal rim remains fixed, including damaged/critical hulls and all four water charge levels. The previous moving texture alone did not establish a visible spiral turn. White hit art/alpha, muzzle sockets, all other water attacks, native pools/defeat and transferred Stage8 Sentinels remain.

40 native checks, 34 art/provenance checks and24 film/player checks pass. New art checks explicitly match the eight Stage2 sources, six flipped source silhouettes and distinct16-frame fan turns with unchanged metal rims. No new paid generation. Updated whole-bank decode cost:124.52MiB.

Fresh native Furious Cole GOD-observer film:147.37s,57.32native FPS, native defeat at140.19s. No enemy HP/phase/timer writes. Maximum one large wave throughout, full opening triplet, full sixteen-phase fan animation, ordinary water combat and native defeat. Final damage may interrupt the last triplet. Audio mean-20.5dB, peak-3.1dB; no engine/browser/asset/audio/bot errors. Root Stage9 film and six attack chapters refreshed, new fan chapter added, earlier movies preserved. This is behavior/visual evidence, not a human balance certification.

Syntax checks pass. Required full suite completes and exits1 with the same five existing failures: hit-flash hold, opening jump dialogue, jump/chromium order, opposite StageX route persistence, StageX right-branch encounter. game.js/test_fl.js unchanged. No commit/push requested.

Owner remains assets/tidal_sovereign_1029.js and its source author.lua/inputs/manifest in assets/game/levels/stage_09/boss/tidal_sovereign_1029/. Existing _BUILD_SOURCE/build_tidal_sovereign_1029.py rebuilds the corrected archived sources. New probe/record/art-audit helpers use tidal_waves_fans_1029; evidence in docs/qa/tidal_waves_fans_1029.json. This supersedes the wave/fan presentation in docs/TIDAL_SOVEREIGN_1029.md.
