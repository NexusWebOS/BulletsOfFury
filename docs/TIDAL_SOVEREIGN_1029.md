> Current weapon behavior and recording: TIDAL_FORWARD_FANS_1029.md. Forward spreads, northbound fan geysers/marked return and exploding fan grenades supersede the old roller behavior.

> Wave/fan correction: see TIDAL_WAVES_FANS_1029.md. The latest gallery film uses actual Stage2 nwf_fire triplets and source-rotated fans; the older measurements below describe the initial pass.

# Tidal Sovereign water arsenal and Stage8 Warp Sentinels — October29

[Full water-boss fight](http://127.0.0.1:51046/?tidal=water-arsenal-1029#clip=stage9-boss) · [Geysers](http://127.0.0.1:51046/?tidal=water-arsenal-1029&chapter=geysers#clip=stage9-tidal-mortars) · [Half-health bubble storm](http://127.0.0.1:51046/?tidal=water-arsenal-1029&chapter=bubbles#clip=stage9-tidal-bubbles) · [Slip N Slide](http://127.0.0.1:51046/?tidal=water-arsenal-1029&chapter=slide#clip=stage9-tidal-slide)

## Roster and entry

Stage9 now begins directly with the whole Tidal Sovereign, arriving in1.6s. There is no preliminary Sentinel fight or merge. The established water pool is initialized once, after which the original native HP/hit/flash/death/reward owners remain. Restoring that pool after the outer spawn wrappers prevents the old twin spawn adjustment from being applied on top of the water phase. The full Furious film uses6500HP; no later refill occurs.

Both former Warp Sentinels move into Stage8. Its actual34.5s carrier wave callback now produces Alpha and Beta, retaining the real Sentinel hull with royal-blue/violet energy distinction and authored16-phase emission/white-hit art. They use ordinary enemy score, damage, death, loot and Retina bookkeeping, with the same heavy-enemy Normal/Furious and party normalization used by the existing roster. They arrive in separate lanes, hover/weave, commit five-shot fans and a gapped radial turn, and stop charging when their muzzles leave view. Old mutation markers are removed so the previous Furnace Maw mapper cannot replace their appearance, target modules or controller. Native hit/death tests cover both; the generic first-hit one-HP floor is retained.

## Water attack book

The existing hull/armor/sockets remain. Each native damage state now has16 flowing/turning liquid phases at four fill/emission levels, exact original hull alpha and a source-derived outer energy outline. Turret/fan flashes follow actual local sockets, including the shared physical space float.

- **Water bullets:** a committed twin-turret fan at205px/s, charged from the actual barrel openings.
- **Water mortars:** four arcing bombs with1.5s committed ground Retinas. Each impact becomes a generated16-frame geyser with splash damage, then a falling water wave. Impacts do not use a misleading full-height FOV.
- **Water rollers:** source-pixel fill, stone asterisk and turret FOV, then two rotating water spheres at255px/s. They bounce from all four playfield edges; each bounce launches a visible arcing water bomb from the contact point with its own ground warning/geyser. Five bounces/lifetime bound each orb.
- **Tidal walls:** violent water charging and exactly three stone asterisks, followed by staggered three-lane water walls derived from the actual authored lava-wall bank. Water cues fire on release.
- **Fan rain:** the two upper swirl fans emit glowing water muzzle flashes and animated upward water jets. They leave the top; descending water jets then arrive at green/yellow/red ground Retinas with warning beeps and two-second lead time, ending in geyser/splash/falling-wave impacts.
- **Slip N Slide:** a committed water trail and water arrows warn the rushing hull lane, then the whole craft charges off the southern edge while shedding forward water waves. Actual hull-alpha contact, finite offscreen wait and smooth north return replace generic homing motion. It remains vulnerable while visible and protected only offscreen.

At50%HP an oversized hit is clamped to the native threshold. The boss fills/shakes, moves to the middle, holds a protected three-second water-energy transition and opens a filled360 warning circle plus overhead asterisk. The bubble turn then charges2.5s, flashes the inner cores and launches five paired inward-moving water bubbles. Buoyancy and drag make them rise/fall; overlapping bubbles merge by conserved volume, selecting larger authored sprites/colliders, up to the explicit mass limit. The actual full recording includes natural merges without fixture writes. This attack rejoins a finite second-half book of rollers, rain, slide, tidal walls, mortars and bullets.

Ground marks, actual arcing world positions and impact collision share one committed target. Water projectiles are ordinary energy and cannot be shot down; physical missile interception and independent defensive clears retain their original routes. Owned rounds are capped at110 with11s lifetime, ground marks at12, waves at14, roller bounces at5. Each turn has finite recovery/cleanup, and half-health/death/stage changes cancel owned hazards. Geyser splash and dash collision respect native player defenses.

## Art and evidence

PixelLab supplied the geyser and two selected sphere designs; its fixed-base geyser animation supplies16 live phases from17 returned masters. Existing native ocean/lava-wall/Sentinel art supplies the other changes.20 banks use85.08MiB decoded, with fixed even cells and shared pivots; all rotations, palette changes, charge glow, alpha phases and size variants are authored offline in Aseprite. No added renderer transforms, additive blending or runtime tinting. Total new generation charges:$0.16 plus1 generation.

- 35 native gameplay checks, 41 art checks and19 film/player checks pass. Actual white hit pixels/expiry, non-GOD splash shield consumption, native threshold protection, both Sentinel deaths and the real scheduled Stage8 wave callback are verified.
- Real RAF Furious Cole GOD-observer film:146.97s, native defeat at139.56s,58.96native FPS. Input-only movement/fire/Retina/missiles; no enemy HP/phase/timer writes in the recording. Initial setup requests Laser5/40 missiles, then native space loadout reports Laser1. This observes behavior/presentation and is not a human difficulty certification.
- Every opening attack, the half-health fill/bubble book, natural volume merges, bounce bombs, fan rain, water cues and native defeat appear. Peak32owned rounds and6ground marks. Decoded audio mean-20.4dB, peak-2.7dB. No browser/engine/asset/audio/bot errors. Decoded geyser/slide/bubble frames inspected; six seekable chapters added without deleting earlier movies.
- Syntax passes. Required full suite completes and exits1 with the same five baseline failures: single-hit flash hold, opening jump dialogue, jump/chromium order, opposite StageX route persistence, StageX right-branch encounter. game.js and test_fl.js unchanged by this pass.

Owner: assets/tidal_sovereign_1029.js, after EH57. Art/masters/Lua/manifest: assets/game/levels/stage_09/boss/tidal_sovereign_1029/. Rebuild: _BUILD_SOURCE/build_tidal_sovereign_1029.py --aseprite <path>. Native probe/recorder/art audit helpers are archived in _BUILD_SOURCE; evidence in docs/qa/tidal_sovereign_1029.json. Dracodia is not revised in this pass. No commit/push requested or performed.
