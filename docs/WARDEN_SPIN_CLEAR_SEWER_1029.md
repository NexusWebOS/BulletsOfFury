# Warden front barrels, circling slams and clear sewer — October29

[Full Warden fight](http://127.0.0.1:51046/?warden=spin-no-pipes-1029#clip=stage7-boss) · [Spin slams](http://127.0.0.1:51046/?warden=spin-no-pipes-1029&chapter=spin#clip=stage7-warden-spin) · [Back-forward hops](http://127.0.0.1:51046/?warden=spin-no-pipes-1029&chapter=hops#clip=stage7-warden-hops)

Live gun poses are painted last, after the Warden face and body, in every ordinary pose. The same order determines overlapping hit-mask priority; no separate cosmetic barrels or detached muzzle origins are introduced. Existing aim, recoil, gun damage, foreground white flashes and FOV sockets remain with their native owners. The Warden's protected canisters, articulated claws/rear drive and original full6150HP Furious budget are retained.

## Exposed core book

After the four legs/arms and both toxic canisters are destroyed, the core adds two new attacks. Surviving guns still take their native machine-gun turn. With guns gone, the book is spin slams, back-forward hops, then the existing roof mortars.

The spinning attack has a .95s first landing warning, then five1.08s hops around a circular arrangement. Its visible core spins continuously through32 authored angles; each landing has its own committed ground Retina, real34px slam collision and8/11/14 ordinary toxic rounds on Normal/Hard/Furious. Landings use the shared body-drop and toxic sound routes, shake, an authored ooze splash and native player damage. The subsequent hop attack holds the forward facing while jumping backward, forward and home over three1.16s hops with128px lift. Both have a matching ground shadow and a .65s smooth return to native center before finite recovery; no snap back or stale landing warning.

New core/face, white-hit and shadow art is derived from the actual ER28 core and existing Warden mask in Aseprite. Five fixed even-cell banks cost32.62MiB decoded. All new spins, shadows and sizes are authored offline; runtime selects ordinary source-over frames. The spun alpha mask and actual physical gun poses remain the damage/collision sources. Native total HP, part pools, white hit pixels/expiry, death escape, score and progression stay authoritative; no HP refill or alternate defeat owner.

## Removed hazards

Stage7's sluice outlet events, draw path and hazard ticking are disabled throughout the level. This removes the beacon/pipe outlet graphic shown by Mike, its warning spray, drips and damage; saved active outlet events are cleared. This does not erase the sewer's authored structural wall/floor artwork or ordinary enemies. Native tests verify zero outlet draw calls and zero outlet damage on Easy/Normal/Hard/Furious, including stale saved live events.

## Verification and review

- 19 native gameplay/pixel checks, 5 art checks and18 film/playback checks pass.
- New full Warden film:133.09s at56.66native FPS. Its real6150HP Furious encounter naturally reaches spinning/hopping core attacks and native defeat. Sound mean-20.6dB, peak-4.3dB.
- Refreshed Dredger film:80.29s at58.09native FPS. Prior turret lock, twin slugs, wall impact/slow reverse and magma retain their native behavior. Both films keep pipe event count zero throughout.
- Real-RAF input-only invulnerable Cole bot, actual Laser5/missiles, no enemy HP/phase/timer writes during either recording. No engine/console/asset/audio exceptions. GOD recordings establish behavior and presentation, not human difficulty balance.
- Required syntax checks pass. The full suite reaches its final summary and exits1 with the same five baseline failures: hit-flash hold; opening dialogue jump warning; opening jump/chromium ordering; opposite StageX route persistence; StageX right-branch encounter. No game.js or test_fl.js edits.

Owner:`assets/warden_spin_1029.js`. Source assets, Lua, input metadata and hashed manifest:`assets/game/levels/stage_07/boss/warden_spin_1029/`. Rebuild:`_BUILD_SOURCE/build_warden_spin_1029.py --aseprite <path>`. QA:`docs/qa/warden_spin_1029.json`. Both full Stage7 gallery films are refreshed and older media preserved. No commit or push was requested.
