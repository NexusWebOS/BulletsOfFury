# Rough Riders missile warnings and allied breakaway — 2026-10-29

The Stage 6 five-ship Rough Riders formation volley now has a dedicated audible tell. Existing authored pilot-color Retina frames remain attached to the real victim and continue animating after launch. All targets are committed to living player/co-op seats for this barrage; allied NPCs evacuate instead of remaining missile targets. The player receives no automatic movement or evade.

| State | Warning | Allied NPCs |
| --- | --- | --- |
| Assemble | Warm the four dedicated sound pools | Fight normally |
| Tell, 2.1 seconds | Existing Retina animation; accelerating .32 to .10-second beeps | Boost north, clear the screen before launch |
| Launch | One existing LOCK-ON alert per formation sequence | Hold offscreen, stop firing and leave the target list |
| Missile approach | Dedicated beeps accelerate as real missiles close; already-launched missiles remain warned if their shooter falls | Remain offscreen |
| Riders' post-volley stunt | Incoming warnings continue for remaining real threats | Wait for Riders to settle |
| Formation complete | Warning ends when no live approaching missiles remain | Return from the south and resume native navigation/weapons |

All fifteen missiles, homing/commit motion, HP and physical player interception remain native. Allies retain their real ships, baked animated engine art, health and individual return lanes. No invulnerability or forced dodge is added to player seats. No projectile-damage, enemy HP, rewards, music-track or camera changes.

## Sound mapping

Shared mixer, settings, unlock and bounded-voice adapter own all playback. Each event has three dedicated voices so player Retina scans cannot steal these warnings. Sources are existing BOF assets; no generated audio or source alteration.

- riders49_seek: existing retinaLockBeep / nsp_console_beep; gain .95, native playback, .07s retrigger floor. Cadence .32 to .10s during the committed tell.
- riders49_locked: existing alertLockon recording; gain .95, .9s gate, once per sequence. Incoming beeps wait .5s after it starts.
- riders49_incoming: existing retinaLockBeep source; gain .95, .09s floor; .10 to .28s cadence for approaching missiles inside 330px with closest-approach time below 1.45s.
- riders49_boost: existing jetDash; gain .7, .5s gate, one launch cue for the allied group.

Warning activity ducks only music to 60% for a .45s rolling hold. No per-ship fivefold audio spam. Dedicated voices stop at pause or encounter exit; stage loads clear ally evade state. Stage X and other encounters keep prior owners.

Native fixture verification and full required regression run completed. The suite still reaches summary with exactly five baseline failures (exit 1): single-hit flash duration, opening-jump warning dialogue, opening jump return before Chromium, opposite Stage X route persistence, and Stage X right full encounter. assets/game.js and _BUILD_SOURCE/test_fl.js are unchanged. All 23 native checks pass. The friendly Golden Aegis barrier explicitly passes evacuating NPCs while retaining its normal player/enemy collision; this integrated case is covered by the fixture. The first full recording caught the shield trapping the allies and was preserved without publishing. Final 240.85s complete native Furious defeat averages 59.20fps. Every observed salvo and post-volley stunt has all four NPCs off-screen; they return only after the Riders settle. Actual decoded playback includes 77 seek beeps, 7 lock-confirmed alerts, 43 proximity beeps and 7 group boost cues. Audio mean -19.3dB / peak -3.3dB, no clipping or game/browser/audio errors. All 27 distinct film/player checks pass. The capture uses native GOD and player inputs only, with no enemy HP, phase or clock writes.

The new direct chapter shows an unobstructed volley, after the earlier gold shield and angry radio have cleared: http://127.0.0.1:51046/?riders=missile-warning-1029#clip=rough-riders-missile-barrage . Full fight and related local chapters use the fresh movie; earlier media is preserved. Decoded frames were inspected, with the red player Retina visible and allies absent throughout missile fire.

Evidence: C:/Users/Mike/Documents/New project/BOF-Riders-Missile-Warning-1029/. No commit or GitHub upload.
