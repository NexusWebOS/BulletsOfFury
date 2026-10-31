# Overdrive levels 3–5 correction pass — 2026-10-17

Runtime/cache stamp: `overdrive1017-playtest40-r1`. No commit or push.

## Corrected behavior

- Level 3: directional enemy action time zero remains frame zero rather than falling back to unit age. North weapon draws advance through their authored frames. Retreating units show walking feet while their reload waits for cover. A search at the last known position no longer freezes an active attack/recovery controller. The generated flamethrower firing bank previously existed only for north; new PixelLab east/south clips and a complete-bank west mirror fill the remaining directions.
- Yuri: single shots can finish the full standing/prone firing clip. The firing clock starts before the muzzle is sampled. Mouse fire is calculated from the visible muzzle to the reticle. Enemy rounds interpolate from their muzzle height to Yuri's body height. The roster uses one warning owner instead of duplicate generic and attack cones.
- Level 4: gun and laser turrets share a 0.9-second green/yellow/red windup, lock their aim before firing, release travelling projectiles, and request their own approved gun/laser cues through the shared mixer. Destroyed turrets cannot release queued shots. Enemy infantry finish committed volleys. Warning progress uses the actual windup duration.
- Base projectiles: the distant authored bullet was four pixels wide and scaled to 0.8 screen pixels. It now starts at a readable size, traverses its complete approaching-camera animation without looping back to the distant frame, and retains a dark edge and short authored trail. Ground and pursuit rounds also have larger readable heads/trails and correct diagonal orientation.
- Level 5: a runner's muzzle previously overlapped the truck damage box, making bullets disappear into immediate hits. Runners occupy a separate foreground road lane and remain visible beside the Mustang. Runner/drone fire uses frame-specific measured hardware sockets. Their whole firing clips play before recovery; movement stops when they take aim. Yuri's on-foot and turret shots finish their generated clips, and his on-foot facing follows the aim reticle. Jump and prone body-roll selection remain available.
- Prone controls: default **F** toggles prone/stand, movement crawls, and **Space/V/H** rolls while staying prone. Pause points to the movement controls in Help; Help displays the current configured prone key. Help/Options retain rebinding.

## Art and sound

Two new PixelLab animation jobs: `ac219aa7-777c-4b6c-a995-0c25da1c5925` (east) and `75b27bc1-7ded-4d10-848b-6380964eb4aa` (south), nine delivered frames each, two generations charged. Palette is locked to each approved idle reference; frame size/origin is unchanged, with no per-frame fitting. Previous/next onion sheets were inspected. West is an exact complete-bank mirror. Receipts and references are under `expansion/topdown/art/combat39/source/` and the host source workspace retains originals and normalization/build scripts.

Combat package now contains 434 playback banks / 4114 frames / 27 stills. Night package remains 53 banks / 280 frames. Aliases and mirrors count as playback banks, not additional generations. Night builder now measures hardware-tip metadata independently of muzzle-flash pixels.

Gun turret cue: `gd_soldierRifle`; laser turret cue: `enemyHeavyLaser`; windup cue: existing `blip`. All use shared mixer/retrigger limits. The 12 existing combat cue files were fully decoded again and contain non-silent PCM. Browser playback has not been heard or verified.

## Verification and limits

- `node expansion/topdown/_research/verify_playtest40.cjs`: **99/99**, exit 0. Uses production modules, registered keyboard event handlers and native Canvas/PNG rendering. Includes all ten roster roles in all four firing directions, repeated complete volleys, seven authored-cover scenarios, single-shot Yuri animation coverage, mouse/muzzle agreement, actual F/Space input handling, both turret warning cycles and cue requests, visible projectile pixels, crate pickup/boarding, repeated runner/drone fire, turret aim geometry, and gate ram/fade/clear.
- `node expansion/topdown/_research/verify_combat39.cjs`: **54/54**, exit 0. Includes all four turret/core waves, Gosfer reinforcements, hit-flash pixels/restoration, fixed roots/even canvases, missile interception and exact 1%/5% truck damage.
- Changed runtime JavaScript and `assets/game.js` pass syntax checks. The required `_BUILD_SOURCE/test_fl.js` suite reaches **BUILD OK / 0 ERRORS**, exit 0. Evidence: `_shots/playtest40/required-suite.log`; final rerun saved separately as `required-suite-final.log`.
- Evidence: `_shots/playtest40/verification.json`, `level3-prone-roll.png`, `prone-controls.png`, `level4-turret-fire.png`, `level5-pursuit.png`. The report is also copied to `docs/qa/overdrive_playtest40.json`.
- **Live browser playthrough and audible playback remain outstanding.** The browser tool reported local browser use disabled before and after the user changed settings. No alternate browser mechanism bypassed that restriction. Screenshots and assertions above come from native rendered fixtures, including deliberately protected combat setups; they do not establish an ordinary-input complete playthrough or difficulty balance.

Owning source workspace: `C:/Users/Mike/Documents/Codex/2026-10-15/fo/work/overdrive39`. Rebuild assets with `build_assets.py` / `build_night.py`; new flame files are registered in `extra-clips.json`. Preserve existing unrelated local changes and the user's music work.
