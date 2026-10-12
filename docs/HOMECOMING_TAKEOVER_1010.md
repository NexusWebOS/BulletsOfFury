# Nine pilot jets and satellite infection — October 10

The ending now shows the selected pilot's original static aircraft throughout
the return portal, Earth descent, coastal approach and HQ landing. Mike
rejected the generated Cole likeness and allowed static ship images; all
nine pilots now use their existing front/rear ship-sheet images. See
[the current correction](STATIC_PILOT_SHIPS_1010.md). The surviving
symbiote stays on the satellite, spreads across its hardware and corrupts the
screen with animated green binary and system code.

## Watch the actual engine

Open [the cinematic preview](previews/hq_landing_1010/index.html).
Choose Cole, Axel, Freezer, Yuri, Maverick, Falva, Lizzie, Decker or Juggernaut.
Play runs the real ending renderer. The portal, Earth, landing, disembark,
walk, infection, corruption and code buttons seek to their actual scene times.
The timeline includes the complete satellite takeover and Fury Command.
The preview's Recorded sequence link plays the actual 43.5-second engine
capture, including its original sound cues. Background music is disabled only
in that verification recording so the mechanical and code sounds can be heard.

The return gate uses all 32 opening, swirling and closing poses of the
Dracodia portal already used in gameplay. The aircraft exits on the central
axis; the following rear view travels straight down toward Earth and shrinks
into the planet. No flight shot rotates an angled spacecraft sprite.

Each aircraft uses its original straight front/rear image. Translation and
proportional scaling animate the return and touchdown without changing the
ship's shape. Existing selected-pilot exit/walk animations, registered HQ
doors and continuous camera push remain in the same scene. The previous
16 front, 16 rear and 16 landing poses per pilot are archived candidates;
they are no longer warmed or drawn by the live ending.

## Physical satellite takeover

The 16.4-second satellite scene starts after the pilot enters HQ. The survivor
crawls across the damaged dish, attaches to its equipment and grows through
32 new infection poses. Six smaller roots attach in succession to fixed panel
seams and hardware sockets. A generated, aligned infected-dish plate reveals
black roots, corrupted green circuitry and failing warning lights.

Green `10001001000` streams and system-code lines type in, multiply and scroll
across the entire cinematic. These use the game's authored bitmap font with
a cached palette transformation, preserving its glyph shapes and dark bevels.
The existing electrical charge, crackle, transmission and code-beep sounds
play at their live scene cues. Seeking does not replay missed sound events.

The true ending now reaches Fury Command at 42.8 seconds, with the following
space/stinger/card clocks moved by the same nine seconds. The ordinary
campaign ending retains its sequel skip; Arcade retains its direct score card.

## Art ownership and provenance

The previous generated pack used built-in **image_gen**, with transparent backgrounds for the
sprite reels. These are source-reference generations; the infected dish is an
aligned reference edit. Original generated files remain in place.

- [Exact flight, environment and infection prompts](../_ART_SOURCES/homecoming_1010/prompts.json)
- [Exact nine landing prompts](../_ART_SOURCES/homecoming_1010/landing_prompts.json)
- [Native aircraft and gameplay portal references](../_ART_SOURCES/homecoming_1010/references/native-manifest.json)
- [Original accepted and archived generations](../_ART_SOURCES/homecoming_1010/accepted_generations.json)
- [Individual landing generations](../_ART_SOURCES/homecoming_1010/landing_generations.json)
- [Source crops, registrations and shipping hashes](../_ART_SOURCES/homecoming_1010/generation_manifest.json)

The preserved pack has 467 loose PNGs: 432 archived aircraft cells, 32 active infection cells and three
environment plates. Flight/infection banks have fixed 384 × 384 canvases with
pivot 192,192. Landing banks have fixed 448 × 448 canvases with pivot 224,224,
allowing the complete open canopy, gear and boarding step to remain visible.
Native RGBA pixels are cropped at measured clear gutters and translated by
integer amounts to the flight nose, rigid landing wing tips or infection-root
fixtures. The landing fixture excludes rising canopies, gear and exhaust.
No frame is
individually rescaled, rotated, interpolated or painted. Every bank uses one
proportional runtime scale and fixed physical pivot. Plates receive only even
transparent padding; their original content rectangle is preserved.

`_BUILD_SOURCE/build_homecoming_1010.py` owns the loose cells,
`assets/homecoming_art_1010.js`, metrics and generation manifest together.
`assets/homecoming_1010.js` owns pilot flight and the actual portal.
`assets/survivor_1010.js` owns infection, hardware corruption and screen code.
`assets/hq_landing_1010.js` owns the landing, pilot route and camera.
Older spaceship/landing/launch art and the rejected generated jet reels
remain archived. The active static pilot views come directly from the
original ship manifest and are not rebuilt by this art pack.

## Verification

The results below record the original generated-art pass. For the latest
static-ship correction and native pixel comparisons, see
[current verification](qa/static_pilot_ships_1010.json).

All four JavaScript syntax checks passed. The complete required suite reached
its final `FALVA/LIZZIE BUILD OK, 0 ERRORS` summary: **8,335 assertions, exit 0**.
Native asset/scene checks passed 24/24, the existing camera/doorway probe passed
32/32 and preview controls/audio passed 14/14. There were zero page, console or
asset errors. Native wing fixtures remain within two pixels of their common
physical pivot across all 144 landing cells; every complete sprite was compared
against its actual game composite. The final recording has one decoded stereo
audio track, with audible cues in approach, landing, doorway, infection,
corruption and transmission windows.

[Portable QA](qa/homecoming_takeover_1010.json) records the final required
suite and native Chromium results. The native probe exports every new sprite
through `XART.get` and the game's own `drawImage`, compares visible pixels to
the registered source, checks complete silhouettes and unique poses, then
renders every pilot's portal, Earth, approach, landing, exit and walking shots.
Continuous frame stepping checks every real portal pose, every infection
pose, sound cues and screen-wide binary growth. The preview probe checks
visible pilot selection, playback, seeking, pause, next scene and narrow layout.
Screenshots, native contact sheets and recordings stay under the ignored
`_shots/homecoming_takeover_1010/` directory.

Existing staged, unstaged and untracked work is preserved. This drop is local;
no commit or push was requested for this change.
