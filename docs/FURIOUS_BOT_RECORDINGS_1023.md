# Furious live fight recordings — October23

30 complete native-engine encounters on Furious, 72.2 minutes of footage.
Review `_shots/furious_bot_1023/index.html`. Every selected video passed full
audio/video decoding. All have real game sound and the current Siege Console HUD.

Coverage: nine current minibosses, nine main bosses, Stage6 rebels, both StageX
routes, three arsenal elites, B.O.B., Chrome Heart, Rime Wall/Blacksteel alternate
encounters and both HAMMER/HAMA music fights. ALT8 is the same current Herald
encounter and shares its recording. Retired, unreachable archive bosses were
not resurrected. Dracodia includes all three encounters and native main/Hammer/
helicopter/volcano/Neural Archon forms, copy deaths, final disintegration and exit.

The reusable test-only bot is under `_BUILD_SOURCE/furious_bot_1023/`. It is not
loaded by the shipping game. It uses delayed observations, normal input and
movement, firing/charged-trigger releases, Retina/Multi-Retina missiles and
native double-tap evasions. Only player damage is blocked. Enemy health, attack
rules, phase gates and native death ownership remain authoritative. No forced
damage, phase jumps, pose fixtures, offline animation or accelerated stepping
was used in selected footage. Initial loadout is disclosed in every run report.

## Bugs discovered and fixed

- Chromium announcement was queued even when the opening-jump gate declined
  armor activation. It now speaks only after an actual activation.
- A destroyed modular chaingun could re-enter a stationary fan with no firing
  callback able to finish it. Broken guns now use the native cooling beat,
  retaining the Furious final recovery/rage checkpoint. A fresh complete Chronos
  recording verifies the shipping code without mid-fight changes.

Both owning runtime archives and browser cache versions agree. Required syntax
checks and the full core suite passed (BUILD OK, zero errors, actual exit0).
Four native regression checks passed. An intentionally failed capture endpoint
also verified the buffered local-download fallback without engine exceptions.

## Evidence and limits

See `review-report.json`, `coverage.json`, `video-verification.json` and per-fight
JSON alongside the videos. The bot is invulnerable and is not a balance benchmark.
Native rendering rate varies; heavy Stage4 averaged about21fps. The recorder
targets30fps and does not interpolate or speed up the game.

Harrier's full video and native completion poll were saved, but one cyclic
contact-source object prevented its detailed event array from serializing.
Its report explicitly identifies the recovered summary and missing detail.
The logger now records source names. Optional network failures in some original
console lists are retained; no missing HTTP art or unhandled engine error was
found in the selected recordings. Diagnostic/failed captures remain outside
the delivered gallery. No online score submission, persistent campaign unlock
or account victory was granted.

No commit or push was requested or performed.
