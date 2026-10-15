# Current Stage 1 vehicle animation — October 9

Mike requested the animation workflow in `passover_imagegen_1009.zip` for the
**current** Stage 1 roster, alongside continued implementation of the filmed
boss direction. Native reference exports showed that the ZIP's older NEF
tanks, jets and boats differ from the current modular tank/Fury Fleet art.
This implementation uses the current in-game designs. The two first ZIP-based
tank candidates are retained as unwired sources; they do not replace the live
modular tanks. The source actors face south, matching the actual game.

## Delivered roster

| Live actor | Idle/flight cells | Fire cells | Independent runtime motion |
| --- | ---: | ---: | --- |
| s1tankheavy | 8 | 4 | Treads/vents, separately aimed twin-barrel turret |
| s1tanklight | 8 | 4 | Same approved modular rig, faster tread cadence |
| s1tankapc | 8 | 4 | Same approved modular rig at the actor's own size |
| s1truckmissile | 8 | 4 | Wheeled buggy motion, roof-tube launch/recoil |
| s1boatpatrol | 8 | 4 | Moving wake, two existing aimed gun mounts |
| s1boatgun | 8 | 4 | Moving wake, independent ready/launch/reload racks |
| s1corvette | 8 | 4 | Wake, existing alternating broadside mounts |
| s1landingcraft | 8 | 0 | Wake, existing unarmed mine-deployment role |
| s1jetdelta | 8 | 4 | Tail exhaust, original bank/roll and ordnance |
| s1jetbomber | 8 | 4 | Tail exhaust, original bank/roll and ordnance |

The complete actor reels contain **116 composite cells** and are exported from
the actual game renderer to `_ART_SOURCES/stage1_motion_1009/returned_live/`.
They are review/delivery composites, not flattened replacements for the runtime
rig. The current `_b` tank/plane variants share the compatible moving parts;
their authored base palettes and jet bank/roll poses remain owned by Fury Fleet.

Seven accepted built-in imagegen source sheets provide **48 new loose cells**:
eight hull, four turret, eight buggy idle, four buggy fire, eight wake, eight
exhaust, four kinetic muzzle and four rocket muzzle. Existing boat hulls and
weapons and jet base sprites are retained. Static barrels, fuel tanks, crates
and mines remain static. Landing craft does not acquire a new gun.

## Ownership and registration

- Exact edit prompts, references and modes: `live-prompts.json` in the source
  directory. Unchanged generated originals: `returned/`.
- Current in-engine reference plates and modules: `live_reference/`.
- Builder: `_BUILD_SOURCE/build_stage1_motion_1009.py`. It normalizes cells with
  shared per-reel scale and measured pivots, crops neighboring cells and removes
  sparse near-transparent fringe. It does not paint or invent art.
- Generated registry: `assets/stage1_motion_art_1009.js`; loose PNG bank:
  `assets/game/shared/combat/stage1_motion_1009/`.
- Runtime: `assets/stage1_motion_1009.js`, loaded after the existing combat
  owners in index.html. Stage 1 queues every cell before play.

Runtime animation uses the existing actor clock and actual shot releases.
Tank aim stays independent of tread cycling. Boat destroyed-part ownership,
launch/reload states, existing hit colors and ordnance are preserved. The buggy
rocket now starts at its visible roof tube rather than its bumper. Generic
automatic muzzles are suppressed where the new physical fire reel owns them,
preventing duplicate effects. Rejected/AI-held shots do not trigger the new
recoil clock. Exhaust is omitted during existing authored roll poses so it
cannot hang from an unrotated socket.

## Verification

`_BUILD_SOURCE/probe_stage1_motion_1009.py` uses real Chromium and the actual
game context's drawImage. **35/35 pass**, zero page/console/asset errors:

- All 48 registered moving-part cells and eight muzzle aliases decode.
- All ten vehicles have eight visibly distinct idle/flight composites; all
  nine armed vehicles have four distinct fire composites.
- Every vehicle retains a visible white hit flash.
- Tank turret aim works both ways independently of the hull, boat mounts retain
  separate destructible HP, and a real buggy rocket originates at the roof tube.
- A 40-second full-loop ocean-to-land capture shows live naval, jet and tank
  controller releases and actual projectiles. It does not replace the firing
  director or force enemies to die. Ordinary wave capture does not guarantee
  every possible rare spawn or attack has occurred.

The harness initially advanced updatePlay while drawing terrain with dt=0,
freezing its draw-owned wave clock. It now uses the repository's shoot.STEP
full frame loop. That harness failure was corrected; no terrain/controller
workaround was installed in the game.

Native reels, normal/hit stills and the gameplay MP4 are under
`_shots/boss_motion_1009/`. The combined review page includes the continued
filmed boss work. Game.js and all new JS scripts pass syntax checking; the full
base suite reaches its zero-error final summary, exit 0. See the separate boss
direction document for its native motion and edge checks.

Long unforced campaign playtests remain useful for subjective balance. The
ZIP's Stage 2 and common-explosion batches, and extra damaged/critical-state
reels, are not claimed as delivered by this Stage 1 pass.
