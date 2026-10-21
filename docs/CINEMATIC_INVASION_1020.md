# PixelLab cinematic invasion ending — October 20, 2026

Mike replaced the earlier resolved-victory/epilogue treatment with a specific
invasion cliffhanger. This is the current direction. Main BOF only; local only.

The return gate uses the existing **blue PixelLab** portal lifecycle directly,
without the Stage8 world-portal colour routing. The original pilot aircraft
remain exact native sprites. Only the 3–6s Earth descent uses their rear view;
from the 6s approach onward they arrive and park nose-first. Both co-op aircraft
and both original exit/walk animations remain owned by homecoming/HQ landing.

| Time | Beat |
|---|---|
|0–26.4s|Blue portal, Earth descent, corrected approach/landing, pilots physically enter HQ.|
|26.4–34s|Returning pilot or pilots run in and report Dracodia defeated.|
|34–39s|All nine pilots reunite and briefly celebrate.|
|39–44s|Red base alarm; urgent Space Federation transmission.|
|44–57s|Three-part message: digital black holes, alien drones hacking defenses, invasion of Earth's skies.|
|57–62s|All nine react in horror; Decker recognizes the spreading signal.|
|62–72s|Pull out of HQ: actual enemy drones/carriers fill the skies.|
|72–82s|Pull out to the coast: twenty actual game warboats approach the base.|
|82–94s|Pull out to Earth: actual enemy fleets and four authored black void rifts.|
|94–105s|Pull out beyond Earth to the solar system.|
|105–112s|A severed clump of Dracodia's machinery/wiring/symbiote grows his head.|
|112–119s|Animated mechanical skull screams and advances toward the viewer; camera follows the face.|
|119–127s|The machine parasite opens a portal outside the solar system and flies through it.|
|127–135s|BULLETS OF FURY — WILL RETURN!|
|135–145s|Pilot credits, names in their canonical colours.|
|145s+|Actual pilot portraits, actual combined co-op score, native Start to title after five seconds.|

The base/coast/Earth/solar transitions shrink and dissolve the actual preceding
render into the next view. One temporary canvas per transition, released afterward;
no per-frame allocation. Seeking stays silent and does not fabricate transition
frames. The story is about 2m25s before its final score card.

PixelLab generated nine reference-based reporting poses and nine individual
horrified reactions, all fixed 256×384 canvases. Existing character faces,
outfits, palettes and ships are the identity references. Native gameplay bodies,
HUD portraits and the approved Cole/Decker hug remain intact. No pilot selection
or combat art was replaced. Cinematic pilot busts use the new poses.

The cinematic UI uses a PixelLab 512×128 metal dialogue frame, sliced into nine
regions with fixed corners and a dark interior backing. PixelLab-generated
letterforms supply the new Fury Signal bitmap face. Actual glyph ink was measured
because the model did not obey its requested grid. The clipped first font was
rejected; the second sheet's accepted letters and 0–3 remain unchanged, with
existing native punctuation and 4–9 supplementing its rejected bottom row.
Glyphs are repacked with padding and recorded source rectangles. Names use each
pilot's actual palette; white body copy stays readable. Cached alpha-mask colour
copies avoid the old luminance tint leaving white names white.

PixelLab created four separate environment plates: base exterior, coastal ocean,
Earth and solar system. Rejected first plates with generic vehicles/UI remain
archived; only clean environment plates ship. All visible aircraft and warboats
in those shots use inspected actual game images. The growth bank has 17 poses;
the scream uses six accepted poses, excluding three closing-mouth frames.
Both banks share a 288×288 export canvas, fixed cable-root pivot and 16px padding;
no individual frame fitting or resampling. Raw masters, job IDs, requests,
reference exports, glyph source rectangles and rejection notes are preserved in
`_ART_SOURCES/cinematic_invasion_1020`.

Runtime owners: `assets/cinematic_invasion_1020.js` and its art registry, loaded
after `cinematic_ending_1020.js`. Builder:
`_BUILD_SOURCE/build_cinematic_invasion_1020.py`. Retired debrief/relay and old
purple-return assets leave the current ending preload; their archive remains.
Standard campaign/Arcade branches and original earned true-ending/reward logic
stay native. No game.js, test_fl.js, Overdrive, combat stats or passwords changed.

Sound uses existing mixer recordings: alarm, radio, crackle, jet movement,
Dracodia shriek and portal. No new voiceover is claimed. Interactive review has
audio; the native canvas recording is silent.

Review: http://127.0.0.1:8794/docs/previews/cinematic_invasion_1020/index.html
The earlier `cinematic_finish_1020` review entry now opens this same current
treatment; its old page and movie are archived rather than erased.

Verification is recorded in `docs/qa/cinematic_invasion_1020.json`, with native
screenshots, complete recording, reports and logs under `_shots/cinematic_invasion_1020`.
The full regression suite reached its final BUILD OK, 0 ERRORS summary with
8,938 checks and exit0. All nine identities, coloured name pixels, actual front
aircraft, both-seat reporting, source enemy sprites, responsive layouts, font,
scene callbacks, no early ending exit and native final Start were checked in Edge.

No commit or push in this pass.
