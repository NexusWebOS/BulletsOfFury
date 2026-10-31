# Herald chaos revision — October 29, 2026

Herald now uses a GPT-authored red tornado loop, accelerating shootable skull bombs and a committed ground-lightning storm. The old broad tornado/skull fields and pre-cast lightning columns are replaced by the requested cues.

## Live behavior

- Tornadoes: one ground asterisk below Herald during charge; two 16-frame red chaotic funnels during the storm. No tornado FOV lanes. Contact stays within the visible funnel height; native radial fire and the128-round budget remain. Darkening remains in the scenery pass.
- Skulls: source-authored red body charge and raised claws. Normal/Hard/Furious release12/15/18 skulls, one at a time; intervals decrease from1.05s to0.105s (NG+ accelerates release cadence once). Eight fixed size variants grow with downward travel. Ordinary player bullets can intercept these explicitly shootable bombs before their first rules update.
- Splash: radius22–57px and6–13 energy chunks depend on the skull's actual growth level at destruction. Source-derived impact and chunk variants grow with that level. Chunks rebound off viewport edges, remain ordinary unshootable energy and expire after2.6s or their fourth boundary impact. Native player damage and dodge invulnerability remain authoritative.
- Lightning: red source-pixel armor illumination, claws together with a visible red lightning ball, claws/energy thrown upward, northward departure and authored shrinking frames. Herald returns south in the background, weaves and casts committed impacts. Each point gets a filled local FOV circle, ground Retina and asterisk for two full seconds. Release cadence accelerates toward the player's sampled east/west motion; each existing warning stays fixed. Actual bolts use the current red lightning art; orbs reuse the Stage6 red1015 lightning source. Geyser lightning, charge, scream and impact sounds use the shared mixer/gates.
- Flight return: bomber/swoop passes wrap outside the camera, re-enter opposite the exited edge, use authored rotational poses and return to their native rest. Modular joints, masks, hit flashes, HP, breakup, defeat and rewards remain native.
- Earlier HL51 bomb landing retinas remain tied to each released bomb's actual upper/middle/lower/bottom impact point.

## Authored assets and rebuild

Owner: `assets/herald_chaos_1029.js`, loaded after `herald_bomb_landing_1029.js`. Registration: `assets/herald_chaos_art_1029.js`, taxonomy prefix`hh52_`.

Sources/exports: `assets/game/levels/stage_08/miniboss/herald_chaos_1029/`. This includes the selected GPT source, editable Aseprite animations, `author.lua`, input metadata and hashed manifest. All 110 banks use fixed even cells and common pivots; all module source extents fit the final canvases. The initial generated sheet with cropped rims and initial clipped pose exports were rejected. Final decoded bank footprint is 190.8MiB.

Rebuild: `python _BUILD_SOURCE/build_herald_chaos_1029.py --aseprite <Aseprite executable>`. Full generation prompts and the built-in tool provenance are archived in [GENERATION.md](../assets/game/levels/stage_08/miniboss/herald_chaos_1029/GENERATION.md). No PixelLab generation credits used for this pass. New rendering selects authored fixed cells with ordinary source-over blits; existing older strike/debris rendering owners remain outside this scoped migration.

## Verification

28 focused native checks and19 distinct film/playback checks pass. Focused fixtures cover actual player-bullet interception, splash collision, ricochet bounce/expiry, fixed two-second warnings, removed FOVs, native white hit pixels and expiry, opposite-edge returns and stage cleanup. All110 art banks pass even/cell checks and all six source module extent checks pass.

The final movie is139.93s, completed through native defeat, with58.95 nativefps and no page, console, asset or audio exceptions. Input-only invulnerable Cole bot, native4264 Furious health pool and native attack clocks; no enemy HP/phase/timer writes during filming. The bot briefly shoots the growing skulls before its general weapon hold ends. The film contains7 skull detonations at multiple growth levels,15 warned lightning strikes and native opposite-edge returns. Maximum live Herald ordnance observed:60/128. Decoded audio mean-21.0dB / peak-4.1dB. 39 aborted requests were recorded for audio-pool URLs; no failed asset HTTP responses or decoded playback exceptions. The GOD bot verifies operation and visuals; it does not establish human difficulty balance.

Required syntax checks pass. The full regression suite reaches its final summary and exits1 with the same five recorded baseline failures:

- and the flash is held long enough for a single hit to register
- dialogue ends with the opening jump warning
- opening jump lands and returns before chromium activation
- unchosen right route persists as the opposite Stage X fight
- Stage X right branch launches a full encounter

No `game.js` or `test_fl.js` edits, commit or GitHub upload for this pass.

## Review

- Full fight: http://127.0.0.1:51046/?herald=chaos-verified-1029#clip=stage8-miniboss
- Tornado chapter: http://127.0.0.1:51046/?herald=chaos-verified-1029&card=tornado#clip=stage8-herald-tornado
- Skull chapter: http://127.0.0.1:51046/?herald=chaos-verified-1029&card=skulls#clip=stage8-herald-skulls
- Lightning chapter: http://127.0.0.1:51046/?herald=chaos-verified-1029&card=lightning#clip=stage8-herald-lightning

The local gallery uses the new uniquely named movie and preserves earlier media. Original downloaded movies remain. QA: `docs/qa/herald_chaos_1029.json`.
