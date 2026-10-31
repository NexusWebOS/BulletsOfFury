# Caustic Dredger final combat pass — October29

[Full native fight](http://127.0.0.1:51046/?dredger=final-retinas-1029#clip=stage7-miniboss) · [Exposed hull cycle](http://127.0.0.1:51046/?dredger=final-retinas-1029&chapter=hull#clip=stage7-dredger-hull)

The two actual twin-barrel turrets protect the entire hull. Both physical bullet hit tests and Retina omit the hull while either gun lives. Bullets pass through sealed body pixels to the real gun masks. Direct/splash core callbacks also reject damage. Native gun pools and core accounting remain intact: Furious2028HP = two429HP guns +1170HP core. No refill, alternate defeat or pooled-health bypass.

## Attack behavior

| State | Behavior |
|---|---|
|Armed guns|1.15s aimed warning, then each gun fires one toxic slug at a time, alternating its two measured barrel sockets. Gun starts are staggered28ms. Release cadence85/70/55ms on Normal/Hard/Furious, with native heading/recoil, muzzle and gun audio.|
|Roof mortars|The top opening has authored1015 green emission and a16-frame anchored ooze fountain on every release. Three volleys use actual toxic orbs, with3/4/5 committed landing points across rows and columns. Ground Retinas appear with launch; no circular roof FOV. The marks stay fixed until impact.|
|Wall ram|A1.25s source-pixel charge precedes a committed .55s rush to the lower edge. Contact has its own native metal impact, .6s rumble/hold and visible impact effect. The tank reverses over2.95s with distance-driven tracks running backwards, then vents its roof.|
|After both guns break|Hull becomes vulnerable. The tank cycles only charge/ram/impact/slow reverse/magma roof bursts, with short native recovery. No turret or neutral attack returns. Magma is an authored orange variant of the same orb family, not the small spark atlas.|

Toxic landings scatter five real energy rounds; magma scatters eight. Damage and ordinary-energy protection use native player/ordnance paths. Roof flights cap at24 and native owned projectiles at128; scatters expire after2.7s. Death/reset ownership clears pending flights, effects and rounds. Native part breaks, actual white hit flashes/expiry, displayed total, defeat escape, score and progression are retained. Stage7's large Warden boss and other encounters are outside this owner.

## Art and source

`assets/dredger_final_1029.js` loads last after prior encounter owners. `assets/dredger_final_art_1029.js` registers nine fixed even-cell banks, 22.16MiB decoded. All new glow, palettes, sizes and padding are authored offline in Aseprite and displayed with plain source-over frame blits. The existing native barrel/muzzle and impact emitters retain their ownership. Editable files, Lua, input metadata, hashes and source notes are under `assets/game/levels/stage_07/miniboss/dredger_final_1029/`. No paid generation was needed.

Rebuild with `_BUILD_SOURCE/build_dredger_final_1029.py --aseprite <path>`. Art references: DC40 actual chassis/top/treads, ER28 toxic orb, original Stage7 modular spew16, and Stage5's actual green ground Retina with authored yellow/red variants. No filled-circle landing marks remain.

## Verification

- 30 native combat/pixel checks, 9 art checks and 17 film/playback checks pass.
- Native real-RAF Furious film: 81.54s at 58.27FPS, input-only invulnerable Cole bot, Laser5 and real missiles. No enemy HP/phase/timer writes in recording. Native defeat completes.
- Decoded metal wall collisions:6. Sound mean-20.3dB, peak-3.5dB. No game/console/asset/audio exceptions. Maximum sampled native rounds:93/128, mortar flights:18/24. 18 routine aborted pooled-audio requests are logged separately.
- Syntax checks pass. The full suite reaches its final summary and exits1 with the same five existing failures: hit-flash hold; opening dialogue jump warning; opening jump/chromium order; opposite StageX route persistence; StageX right-branch full encounter. No game.js or test_fl.js edits.

The local Stage6–9 gallery has the new full fight and focused gun/roof/ram/exposed-hull chapters; older films remain. No commit or GitHub push was requested.
