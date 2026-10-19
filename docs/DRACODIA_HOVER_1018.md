# Dracodia hover, core missiles and charged arms — 18 October 2026

Mike requested lateral movement during standard main-form combat and code
bombs, missiles from the core, and visibly charged arm lasers or physical
swipes. `assets/dracodia_archive_1018.js` owns this extension after V19.
The main-form arm lasers are now explicitly approved; this supersedes the
older blanket description of Dracodia having no arm beams.

The main body continuously follows a smooth left/right hover, with a small
vertical float. Its movement respects the current viewport and full-size
body margins. The native capture measures 133 world pixels of lateral travel
in the 480-pixel field, with a maximum 0.92-pixel frame step during an
eight-second standard hover. Bomb volleys keep moving through the existing
53% background retreat and return. Native shoulder swipes retain their
planted stations, committed arcs and smooth return; hover resumes afterward.
The native controller still advances its clock, dialogue, damage flashes,
persistent effects and transitions exactly once per frame.

## Emitters and attacks

All new emission points use the current rendered module transform, including
background scale and arm rotation. The inspected 320×320 shipping coordinates
are core `(160,139)`, left palm `(75,198)` and right palm `(245,198)`. These
points remain opaque in all sixteen standard frames. There is no separately
estimated world-space muzzle or arm stretching.

- Code bombs and spiraling lightning now originate at the actual core.
- Missile volleys launch three shootable authored code warheads from that
  same core. They fly along their released headings. The shared interception
  system receives a proper missile classification; retaining the old energy
  orb classification silently removed shootability. Actual centered machine
  gun fire now intercepts them in Chromium.
- Arm lasers rotate the real limb about its shoulder, illuminate its own
  pixels and charge the palm with the existing authored electrical/muzzle
  graphics. Each arm commits a player position when its charge starts, shows
  its FOV/Retina warning and fires from its moving palm through that position.
  Moving the player cannot redirect an already committed laser.
- Each arm owns its warning, beam and destruction state. Destroying it stops
  its attack and removes its target immediately; the surviving arm continues.
  With both arms destroyed, the laser turn becomes a core-missile turn.
  Native owner/part hit flashes remain visible and expire normally.

| Timing | Normal | Hard | Furious |
| --- | ---: | ---: | ---: |
| Initial arm/core charge | 1.35 s | 1.16 s | 0.98 s |
| Subsequent arm charge | 1.05 s | 0.88 s | 0.74 s |
| Each arm beam | 0.68 s | 0.75 s | 0.82 s |
| Arm releases with both arms intact | 2 | 2 | 3 |
| Core volley interval | 0.90 s | 0.76 s | 0.64 s |

The natural main book is download, physical scythes, spiraling electricity,
code bombs, roar, core missiles and charged arm lasers. Exactly the existing
four copied forms follow: Hammer, helicopter, Harrier and volcano. Their
controllers, finite health pools, phase fades, deaths and final red-portal
campaign reward remain intact. Phase cleanup removes all new damage sources.
Existing authored art is reused without atlas or frame-bank changes.

## Verification and review

284 real Chromium checks passed with zero page, console, draw or asset errors:
52 hover/arm/core checks, 71 archive checks, 89 physical-swipe checks,
32 phase/ending checks and 40 delivered-review checks. Captures include charge,
beam release, moving hover and core volleys at all three difficulties.
Dedicated checks use the original native player damage/death function and
verify protection, warning timing, weapon interception and independent arm
breaks. These are controlled encounter checks, not a human balance pass.

Both JavaScript syntax checks pass. The full core suite exits 0 and reaches
`FALVA/LIZZIE BUILD OK, 0 ERRORS` (8,785 printed passing assertions; the incoming
record was 8,784). `assets/game.js`, `assets/stage8_identity_1018.js` and
`_BUILD_SOURCE/test_fl.js` retain their starting hashes; LF/CRLF rules hold.
Existing local work is preserved. No commit or push was requested.

Evidence: `docs/qa/dracodia_hover_1018.json` and
`_shots/dracodia_hover_1018/`. The review now includes standard hover,
charged arms, core missiles, the earlier archive attacks and the natural
book. The arm scene's **Break left weapon** button uses actual boss damage.
Campaign saves remain isolated and selected attacks repeat.

[Review charged arms](http://127.0.0.1:8794/docs/previews/dracodia_archive_1018/index.html?scene=armLasers&difficulty=furious&revision=dracodia-hover-1018)
· [Review moving bombs](http://127.0.0.1:8794/docs/previews/dracodia_archive_1018/index.html?scene=codeBombs&difficulty=furious&revision=dracodia-hover-1018)
