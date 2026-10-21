# Instructor Cole / B.O.B. — October20

## User direction

Mike's two photos define Instructor Cole's likeness. Black blazer, black collared shirt, red tie; BOF square green-framed 16-bit portrait style. Four generated expressions: neutral, small/open talk, encouraging smile. Likeness remains subject to Mike's review. Tutorial only; pilot Cole elsewhere keeps his existing assets.

## Course and encounter

Stormglass remains a separate offshore tutorial stage with the accepted animated PixelLab water and four independent parallax layers. The 17 lessons use real controls and systems. B.O.B. is the Ballistics Orientation Bot: “Why haven't I retired yet?” His actual missile and cannon modules demonstrate ground and FOV warnings before graduation. Two escort waves precede his modular fight. Both pods must be disabled to expose the cryo reactor. Destroyed modules leave immediately; their unlaunched attacks cancel. All hits, including reactor armor absorption, visibly flash only the struck module. Shared muzzle, projectile, impact and audio owners remain authoritative.

| Module | HP | Type | Damage / targeting |
|---|---:|---|---|
| Missile pod |90|Neutral steel|Normal damage; destroy to stop ground missiles|
| Cannon pod |110|Neutral steel|Normal damage; destroy to stop FOV volleys|
| Cryo reactor |240|Ice|Both pods first; fire X1.5, ice X0.5, exposed core missiles X2|

Missile weakspot multiplier is a B.O.B. tutorial rule. Element multipliers come from the native engine, not the earlier obsolete “double damage” tutorial prose. The two labs demonstrate both matching resistance and opposing-element advantage with actual infused shots. Level-I equipment is borrowed and restored, including forge/variant banks, on completion or exit; no save/armory writes. The pilot-specific primary/secondary brief reads the existing HUD loadout owner for all nine pilots.

## Dossier

Existing Overdrive card frame copied locally into tutorial art, with Instructor Cole in its portrait slot. Full craft, missile pod, cannon pod and reactor each have32 genuinely generated PixelLab turntable poses that show front, side and rear. This is authored sprite inspection, not polygonal 3D. Up/down selects parts, left/right steps the rotating view, A/fire deploys after the scan, B/missile returns to whole unit, Start/pause opens normal pause/skip. Keyboard mappings remain in Help/Options. No combat progresses or ammo is consumed behind the dossier. The bottom prompts use the existing generated controller assets.

## Files and performance

- Runtime: `assets/instructor_bob_art_1020.js` then `assets/instructor_bob_1020.js`, after arena_download owner.
- Art: `assets/game/pilots/cole/portraits/instructor_1020/` and `assets/game/levels/tutorial/stormglass_1020/instructor_bob/`.
- Source: `_ART_SOURCES/instructor_bob_1020/`, including prompts/jobs, original photos and all returned frames. Photos are not runtime assets.
- Build/retrieval: `_BUILD_SOURCE/build_instructor_bob_1020.py`, `retrieve_bob_art_1020.py`, `prepare_bob_parts_1020.py`.
- QA: `_BUILD_SOURCE/probe_instructor_bob_1020.py`, `audit_instructor_bob_1020.py`; report and native captures in `_shots/instructor_bob_1020/`.

Live modules share256canvas/pivot128; inspection modules192/pivot96; whole craft256/pivot128. A single uniform627→628pad→256 transform handles each portrait. No per-frame fitting. Atlases retain even cells,2px gutters/extrusion, fixed canvases and source metadata, max1560px. Live alpha plates recompose the original exactly. All128 poses are nonblank and have transparent margins. Assets are warmed only for tutorial entry; normal campaign boot does not fetch the new art. No new animation loop, WebGL dependency or generated runtime pixel effects.

## Verification

Native Edge: 27/27, no page/console/asset errors. Entire17-lesson course completed through input; no foreign spawns/life loss, normal Stage1 handoff. Actual damage tested on Easy/Normal/Hard/Furious. Per-part native damaged pixels and restored pixels checked; launcher cancellation, source rectangles for all4 yaw banks, all9 lab guns, pause/skip, gear restoration and decoded mixer routing verified. Required full suite8940 passing/0errors/exit0 and syntax checks passed. Runtime addition 1,851,313bytes. Original protected hashes recorded in art-audit.json. Local changes only; no commit/push requested.


## October21 — Instructor card text fitting and black/red portrait frame

Mike requested safe scaling/centering for every B.O.B. dossier label and a black/red Instructor Cole portrait box. `ic20CardDraw` now maps explicit text apertures from the1200x832 authored template, bounds its overall proportional size to the available screen, and separates the part title from the rotating model. Ten independently centered/fit/clipped text blocks cover the title/subtitle, part name, six statistics and retirement line. The model has its own viewport. Tutorial objective/footer labels now fit their own bounds. Inset dialogue retains enough vertical room for the three longest four-line lessons; all17 lesson texts and runtime reactor feedback fit completely. Native logical selection and deploy controls remain.

The built-in image generator supplied the charcoal/black steel and red lamp treatment. The owning builder applies its palette only to the original green frame pixels in an explicit rim mask, preserving the exact portrait artwork, expressions, alpha and frame geometry. Four256-square `*-black-red.webp` exports; old green exports archived outside game assets in `_ART_SOURCES/instructor_bob_1020/palette_black_red_1020/previous-green-exports`. Two naturally greenish eye pixels are deliberately preserved. No original photos uploaded; no PixelLab charge. Source image, palette export audit and notes saved beside originals.

Native UI verification:41/41, four card selections at390x844,1366x768,1920x1080,768x1024; all10 text blocks centered and bounded, model/title and card/prompts clear, all lesson text fits, all4 portrait states decoded, actual selection/deploy controls. No browser errors. During testing, repaired the existing locked-pilot hover font guard (`typeof _pilotFace` before access); no other core changes. Required full regression8940/0/exit0 and syntax clean. Core game LF and test harness CRLF preserved. Cache instructor-bob-fit-black-red-1020. Updated review `_shots/instructor_fit_1020/review.html`; previous instructor review redirects here. No GitHub push requested.



## Superseded dossier — October21

The copied Overdrive card and its former layout are replaced by the approved Holoscan owner. The four actual turntables, module anatomy, HP, native targeting, audio and training rules remain. See HOLOSCAN_1021.md for current layout and verification.
