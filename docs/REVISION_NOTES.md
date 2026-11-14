# Everybody Home — November 11 cinematic revision

## Guided panel reading and comic motion

CM3 begins each sequence in black, reveals the first speaker's panel with the dialogue, then reveals the reply panel and pans toward it. Unread panels stay black. Previously read panels dim while the active speaker remains clear. Contiguous conversations keep a stable left-to-right page layout; the first speaker takes the left panel. On the next strip, the old artwork scrolls out and the new strip scrolls in. Captions remain stationary so the words are readable while the page moves.

Seven authored zoom sizes move from the native view into a20% closer speaker view. All nine pilots, their individual backgrounds and the inked frames use matching raster zoom exports. Visible body baselines stay attached to the ink borders at every size. Nine stored black-to-clear fade frames control reveals; there is no runtime sprite scaling, global-alpha animation, filter or shader. Runtime camera motion only translates and clips images. The27 editable Aseprite banks contain545 frames; all roundtrip to their prepared source frames without pixel differences.

Dialogue reveal, mouth timing and instrument/weapon cues begin after the panel's reveal lead-in. The added lead-in is0.42s for a new strip and0.26s for replies. Continuous missile/action phases retain their timing and avoid repeated blackouts. The original gameplay, native rewards, stage callbacks, saves and skip controls retain their owners.

## Portrait panel correction

All nine visible bodies now meet the bottom of their comic panels. The renderer uses the measured visible silhouette baseline (250px in the256px portrait cell), with a2px overlap behind the ink border. Cole's actual central torso ends2px higher than the furthest silhouette pixel, so the overlap also closes his center gap. The same placement applies to straight, angled and small reaction panels; the original seven mouth poses and portrait pixels are preserved.

Nine new backgrounds give each pilot a distinct16-bit comic composition in their aircraft colors. Cole has green action rays, Axel blue chevrons, Freezer cyan ice shards, Yuri red slashes, Maverick teal speed arcs, Falva magenta rings, Lizzie gold sunbursts, Decker gold circuit paths, and Juggernaut bronze impact slabs. Each was authored to16 colors in an editable Aseprite document. Background cells are512×340; the generated1536×1024 source sheet is cropped at native pixels with row origins0/342/684. No runtime rescaling, tinting or effects are used. Framed384×288 talking GIFs use the same visible-body anchoring and backgrounds.

The older action-scene portrait helper uses the same treatment. It selects explicit96/180/256px talking banks for short, medium and tall panels, aligns each bank by its measured body baseline, and fills taller panels using the authored background. All size variants are exported directly from the128px source. Credits retain their existing layout.

The generated source sheet, editable masters, production exports and prompt/provenance notes are retained in this package. The110 focused native-renderer checks cover all nine pilots across the three new portrait-panel layouts and three older panel sizes, actual draw order, bottom placement, background coverage and missing/error checks. Every framed GIF also keeps all non-mouth pixels stable across its full animation. This correction changes presentation only.

The dialogue now follows what the crew wants, what they learn and what they do next. Cole checks on people, Decker explains the practical meaning of evidence, and the team gets room for fear, relief and small jokes. The readable story and full shooting script are in `BULLETS_OF_FURY_STORY_AND_SCRIPT.md`.

The intro, all eight post-mission bridges, the Stage4/7/9 arrivals, optional Stage5→9 warp, true ending and final transmission use the new presentation. The conference, recovered gun, prototype demonstration and Cole/Decker hug remain, with rewritten dialogue and faster inserts. The normal/easy completion pause remains distinct from the hard/furious city deployment. The two Stage6 outcomes identify the actual surviving threat. Maverick's guns are never promised elemental or chaingun upgrades.

Four illustrated paper pages replace the thin industrial dividers: straight panels, a lightning-shaped diagonal split, a wide establishing panel and an unequal picture/reaction pair. Portraits are large and still while listening. Names use their aircraft colors, including teal for Maverick. Brief flights use the actual flat in-game aircraft. The generated six-frame hangar/landing ship banks no longer appear in these story scenes, and native connector landings use the actual aircraft marker.

All nine talking GIFs were generated anew from their current native headset portraits. Seven mouth poses were authored into editable Aseprite documents. Cleanup restores every pixel outside the mouth from the original portrait and preserves its exact alpha silhouette. The GIF exports also keep all non-mouth pixels and alpha identical across their complete timelines. Only the current speaker animates; speech ends on a closed mouth. These are timed text performances, without voice acting or recorded-speech lip sync.

The comic page master was generated for this revision and reduced to a shared16-color palette in Aseprite. Native portraits remain128×128; the cinematic256×256 variants are explicitly baked at2× with nearest-neighbor pixels. Small victory icons have separate fixed exports. Every delivered cell has even dimensions. The runtime only positions, clips and blits these authored cells; it adds no portrait transforms, glows or opacity animation.

The earlier13:25 movie was reviewed through its full caption record, samples every12 seconds across the whole timeline, and denser hangar samples. Examples: the unexplained “request” at0:12, the missing setup at0:24, and the long hangar shot around1:15. This was a sampled visual/caption review, not a claimed continuous audio audition. The old movie is retained in the previous output folder as an archive.

Native Chronos final words/missile destruction, optional pursuit destruction, Dracodia's death, combat rewards, Forge progression, route unlocks, difficulty completion, saves and stage callbacks retain their owners. The new movie labels gaps where gameplay occurs and puts alternate outcomes after the main ending. No generated voices, installer, commit or push are included.

The focused story, portrait and continuation checks pass. The full project suite still exits1 at its existing missing `difficultyHealthBaseline15` helper in `assets/combat_polish_0927b.js:151` (`_BUILD_SOURCE/test_fl.js:4537`). Core gameplay and the suite are not edited by this revision.

## Maverick mouth and non-strip dialogue frames

Maverick’s bright teal tooth pixels are now warm ivory with a natural dark mouth interior. The jacket and glasses retain their teal palette. The seven poses, talking GIF, framed GIF, C16 portraits and all seven CM3 zoom sizes are rebuilt from the repaired editable source.

Four generated, authored frame styles cover crew radio, command briefing, hostile transmissions and narration. Crew accents follow all nine pilots. Wide and compact versions use fixed raster tiles; portraits meet the lower ink border. Existing text timing, fitting, paging, camera transforms and callbacks are retained. The CM3 comic pages retain their presentation.

The final non-strip frames use square-corner rectangular brushed steel plates, rivets and dark inset name/text apertures. The paper/comic frame concepts are superseded. Four metal treatments and all nine crew color variants are installed as CX4 revision2.
