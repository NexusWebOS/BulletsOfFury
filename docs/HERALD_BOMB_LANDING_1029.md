# Herald explosive bomb landing retinas — 2026-10-29

The Stage8 miniboss's bomber passes no longer paint a pre-drop carpet of ground reticles and vertical FOV columns. Bomb-burst ray FOVs are also removed. The ordinary horizontal bomber entry/swoop flight warning and other Herald attack warnings keep their existing owners.

A reticle appears only after an explosive bomb physically leaves a living claw. The drop commits once to a world-space landing point, cycling upper/middle/lower-middle/bottom bands at18/46/70/90% of the visible playfield. That same point drives the released velocity vector, marker and native timed burst. Player/camera motion does not retarget an airborne bomb. Its final impact is clamped to the committed point. Regular nonexplosive chaos shots remain free-flying rounds.

The native .68s fuse, two claw emitters, rapid drop interval, two Furious passes, burst angle/gap logic, 128-projectile cap, sound routes, ordinary unshootable chaos rules, part hit flashes, modular HP and defeat remain. At a full bullet budget the visual landing explosion still appears at its reticle while extra scatter rounds are suppressed, retaining the cap. Dead owners/claws and stage exit remove their bombs and markers through the native cleanup.

19 focused native checks pass. These cover absence of premature marks and vertical/radial carpet FOVs, one reticle per released explosive, all four native landing depths, real fuse/velocity endpoints and exact impacts, bounded projectile counts, fixed targets under camera/player movement, an actual explosion under full budget, claw/stage cancellation, real damaged white claw pixels and flash expiry. Native screenshots inspected.

Syntax checks pass. Required full suite reaches summary with the same five baseline failures, exit1: single-hit flash duration, opening-jump warning dialogue, opening jump return before Chromium, opposite StageX route persistence and StageX right full encounter. assets/game.js and _BUILD_SOURCE/test_fl.js unchanged.

Fresh76.68s complete native Furious defeat averages58.30fps. The actual attack book releases12 explosive bombs and all12 observed impacts match their own landing retinas, covering all four bands. No phantom live-bomb markers occur during pre-drop tells. All13 film/player checks pass, including actual decoded launch/impact/flight sound and both full-film/short-chapter playback. Audio mean-21.0dB / peak-3.7dB; no game/browser/asset/audio errors. Native and decoded frames were inspected. Recording uses native GOD and player inputs, with no enemy HP/phase/clock writes.

Full Stage8 miniboss and a focused4.662–12.311s bomber chapter now use the new movie; prior media is retained. Direct preview: http://127.0.0.1:51046/?herald=actual-landings-1029#clip=stage8-herald-bomb-landings . Evidence: C:/Users/Mike/Documents/New project/BOF-Herald-Bomb-Landing-1029/. No commit or GitHub upload.
