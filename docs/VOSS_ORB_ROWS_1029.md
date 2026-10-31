# Voss: parallel spinning twin-cannon orbs — October29

The two cannon sockets previously aimed separately at the same target point, so each row narrowed as it approached the player. Voss now fires true straight-down columns at one shared velocity: vx0, vy240. Each orb keeps the horizontal coordinate of its original cannon socket. The native side-reflection condition cannot turn a vertical orb inward. Travel is240world pixels/second instead of180 (+33.3%). The five native rows, .30s row cadence, source weapon audio, charge duration, cannon modules, collision radius13, energy HP/counters, owner-loss cleanup and full turbo sequence remain with their existing owners. The native two green/yellow/red warning lanes now show the same parallel direction as the actual shots. A destroyed cannon emits no orb.

An inspected native florb_0 source is authored offline in Aseprite into32 circular spin frames with a baked stepped1015 red light pulse. It spins around each orb's fixed center; projectile centers keep their row spacing. Fixed48x48 cells, pivot24/24,24fps;32 matching white hit cells preserve actual damage feedback. No new runtime alpha, additive blend, tint, glow, rotation or scale. Editable source, original reference, recipe and hash manifest are beside the atlas. No external generation or credits used.

The late owner assets/voss_orb_rows_1029.js is scoped to Stage6's five-ship Rough Riders fight. Rook's existing machine gun, other pilots, StageX's Voss, all ship artwork and the confirmed Stage6 boss music/steady camera retain their existing behavior.

34 native checks and4 source/art checks pass. All four difficulties retain ten orbs in five simultaneous pairs, source socket separation, exact velocities after the player moves, native turbo progression and appropriate broken-cannon behavior. Real native damage selects the aligned white hit bank. StageX and Rook are excluded; no game errors.

Fresh172.81s complete native Furious GOD/input-bot fight reaches actual squad defeat at59.00nativefps. No enemy HP/phase/attack timing writes. The recording contains Voss's actual new volley; measured paired spacing and initial velocity remain constant. All five fighters and allies remain native. 20 film/player checks pass. Sound mean-18.9dB / peak-2.2dB. The full card and related chapters now use the fresh movie; the Voss chapter starts immediately before the first corrected volley. Earlier movies are retained.

Preview: http://127.0.0.1:51046/?riders=orb-rows-1029#clip=rough-riders-voss

Syntax passes. Required full suite reaches summary with the same five baseline failures (exit1): single-hit flash duration, opening-jump warning dialogue, opening jump return before Chromium, opposite StageX route persistence, StageX right full encounter. assets/game.js and _BUILD_SOURCE/test_fl.js untouched. No commit or GitHub upload.

Evidence and raw film: C:/Users/Mike/Documents/New project/BOF-Orb-Rows-1029/.
