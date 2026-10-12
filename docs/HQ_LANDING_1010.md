# Fury HQ homecoming — October 10

> Superseded aircraft direction: the current ending uses each pilot's original
> static front/rear ship images from portal exit through landing. See
> [Original static pilot ships](STATIC_PILOT_SHIPS_1010.md) for the
> active art, clocks and final QA. This document describes the earlier Furyship
> art pass; its selected-pilot walking, fixed HQ doors and camera remain active.

The campaign ending now brings the selected pilot home in the current Furyship,
lands it level on its gear, shuts down the engines, opens the canopy and deploys
the ladder. The pilot climbs down, walks around the parked aircraft and enters
the opening Fury HQ doors. The five small parked aircraft are removed from the
sunset shot. The ship remains stationary after touchdown.

[Play the actual ending and choose any pilot](http://127.0.0.1:8794/docs/previews/hq_landing_1010/index.html).
The preview has playback with the original engine sound cues, pause and timeline
controls. It stops before the following story stinger. The gameplay ending
continues normally into that stinger and final card.

## Art and ownership

Generated with the built-in `image_gen` tool. The actual current Furyship and
each pilot's accepted game body were exported through native `XART.get` and the
game's own canvas renderer as identity references. Costume and ship colors are
specific to Cole, Axel, Freezer, Yuri, Maverick, Falva, Lizzie, Decker and
Juggernaut. There is one pilot on the landing pad, selected from the active run.
The spacecraft seen returning toward Earth is also the current selected
Furyship; it is not a baked green aircraft in the backdrop.

328 registered native-alpha PNG frames:

| Art | Frames | Export canvas |
| --- | ---: | --- |
| Each pilot's landing / gear / shutdown / hatch | 16 per pilot | 288 × 288 |
| Each pilot's climb out | 8 per pilot | 288 × 288 |
| Each pilot's walking loop | 8 per pilot | 288 × 288 |
| Coastal approach / frontal HQ | 2 | 840 × 472 |
| Portal / Earth | 2 | 840 × 472 |
| Ground shadow | 4 | 452 × 230 |
| Sliding HQ door | 16 | 384 × 384 |
| Neutral downwash dust | 16 | 384 × 384 |

Source import uses crop, transparent padding and integer translation at scale1.
Engine mouths anchor the aircraft, torso roots anchor the bodies and the shadow's
rear axle anchors the landing-wheel contact. Each bank has one even canvas and
one physical pivot. The renderer uses uniform proportional scaling; it never
fits each frame to its individual silhouette or stretches one axis. No atlas
was edited. Original and rejected source art remain available.

The raw generators used uneven vertical row gutters. The importer measures
those gutters before cutting cells, so pilot heads stay complete. An extra
walking body in Axel's original bottom row and a ladder attached to Juggernaut's
body were caught in the final sheet review. Both were corrected with built-in
image edits, and only the corrected row is shipped. Body imports now reject
visible pixels crossing a column edge.

Files:

- Shipping frames: `assets/game/shared/cinematics/hq_landing_1010/`.
- [Frame registration](../assets/hq_landing_art_1010.js) and
  [ending renderer](../assets/hq_landing_1010.js).
- [Owning build](../_BUILD_SOURCE/build_hq_landing_1010.py) and
  [native identity export](../_BUILD_SOURCE/export_hq_landing_refs_1010.py).
- [Exact initial prompt set](../_ART_SOURCES/hq_landing_1010/final_prompts.json),
  [correction prompts](../_ART_SOURCES/hq_landing_1010/correction_prompts.json),
  [source/frame manifest](../_ART_SOURCES/hq_landing_1010/generation_manifest.json)
  and [generation IDs](../_ART_SOURCES/hq_landing_1010/accepted_generation_ids.json).
- Supplied sunset references and actual pilot identity exports:
  `_ART_SOURCES/hq_landing_1010/references/`.

## Timing

| Ending clock | Action |
| --- | --- |
| 0–3s | Exit the alien portal |
| 3–6s | Return toward Earth |
| 6–9.4s | Coastal runway approach |
| 9.4–13.6s | Gear, descent, touchdown, shutdown and open canopy |
| 13.6–16.6s | Pilot climbs out |
| 16.6–24s | Walk around the ship and into the opening HQ door |
| 24–26.4s | Pilot is inside; doors close |
| 26.4s onward | Original survivor continuation / final card |

Original thruster, part-arrival, landing lock, hatch, door and confirmation
sounds are scheduled once at their physical events. Extra redraws do not replay
them. Ordinary campaign completions finish the homecoming before their card;
Arcade keeps its direct score/end card. The bounded art-loading fallback uses
only the new cleared scene, so retired parked aircraft cannot reappear.

## Verification

Full regression: **8,243 passed, 0 failed**, final success summary and exit0,
against the incoming measured 8,174/0 baseline. Syntax checks pass. `game.js`
remains LF and `test_fl.js` remains CRLF. Existing staging remains preserved.

Real Chromium ending checks: **18/0**; preview controls: **8/0**. The previous
daytime HQ/live-radar probe still passes **25/0**. All nine selected pilots,
landing/door/entry timing, fixed parked position, old-aircraft fallback,
ordinary/true/Arcade continuation and narrow layout were checked. Pilot pixels
were compared with the same frame rendered without the actor: the actor stays
visible around the aircraft and through the doorway. Native screenshots were
inspected, including the corrected Axel and Juggernaut clips.

A 26.28s native canvas recording reaches all seven homecoming phases, with no
page, console or asset errors. Its frame sequence was inspected. Temporary
MP4/WebM, screenshots and logs are in `_shots/hq_landing_1010/`; the recording
is silent and the interactive preview plays the real sound cues.

[Portable QA evidence](qa/hq_landing_1010.json). This pass verifies the ending's
art, animation and controls. It does not constitute a campaign balance or
hardware/gamepad verdict. Local changes only; no commit or push.


## October 10 door registration follow-up

Mike spotted the door architecture shifting between opening frames. Onion
comparisons confirmed about 14 pixels of horizontal drift across source rows
and smaller vertical offsets. The owning importer now registers the doorway
and uses one authored open plate for its stationary lintel, pillars, threshold
and corridor. The two authored closed panels slide symmetrically inside that
fixed aperture. All 16 poses remain distinct, on even 384x384 cells with the
same pivot. This is native pixel cropping/translation/compositing, without
repainting or resampling. Source frames 0 and 15 provide the panels and frame;
the raw generated sheet remains untouched.

Only the 16 door PNGs changed. All 312 other registered cells and two retained
unregistered background PNGs are byte-identical to the pre-fix files. Sheet
registration and its manifest were rebuilt together through their owner. The
landing renderer, pilot graphics, dialogue and timing were unchanged.

Verification: full suite **8,256/0**, final success summary, exit 0; real Chromium
**21/0**, zero page/console/asset errors. Native `XART`/game-context `drawImage`
comparisons show **zero changed fixed pixels** in every frame, continuous panel
reveal, and all 16 opening/closing poses in the actual timeline. Onion/contact
sheets and native doorway/entry screenshots were inspected. All nine pilots,
sounds, continuation and narrow layout still pass. Syntax checks pass; existing
LF/CRLF runtime files and staged changes remain preserved. No commit or push.

[Portable door QA evidence](qa/hq_door_1010.json). Onion sheets, animation and
native screenshots are in `_shots/hq_door_1010/`.


## October 10 camera and transition follow-up

The homecoming camera now eases forward during touchdown, moves with the pilot
along the cockpit/ladder/walk route, and settles on a 3x doorway close-up. All
scene layers share one proportional camera transform. The authored world roots
and door registration remain fixed; the camera alone pans and zooms. Continuous
monotone cubic interpolation prevents cue jumps and overshoot. Focus is bounded
to the authored scene so the camera cannot expose uncovered edges. Captions
remain in their original screen layout outside the camera.

The pilot enters at 24s and the door closes by 25.65s. A 0.70s fade starts at
25.70s, reaches black at 26.40s, and the next scene fades in over 0.65s. True
endings retain the survivor continuation. Ordinary campaign endings fade into
their final card; Arcade keeps its direct score/card. Ending clocks and sounds
are unchanged. The preview now has Doorway and Next scene controls and continues
to 30.8s so the transition can be reviewed.

Verification: **8,256/0** regression checks, final success banner, exit 0;
**32/0** native Chromium checks and **9/0** preview-control checks, zero page,
console or asset errors. Native camera/pilot pixels, clipping, fixed captions,
continuous interpolation, a fully black cut on both sides, restored drawing
state, all nine pilots and narrow layouts were checked. A **28.40s** recording
of the actual engine clock reaches the next scene with zero errors. Its timed
frame film and representative native screenshots were inspected. The recording
is silent; the interactive preview plays the real cues. Temporary media and
logs are in `_shots/hq_camera_1010/`.

No sprite files, source sheets, registry, `game.js` or `test_fl.js` changed in
this camera pass. Existing work and staged notes remain preserved. Local only;
no commit or push. [Portable camera QA evidence](qa/hq_camera_1010.json).

## October 10 survivor animation follow-up

The continuation now has regenerated wide and close satellite-dish art,
32 crawling poses, 16 charge poses, 16 takeoff poses and 16 electrical contact
effects. Core registration prevents pose jitter. The preview includes Symbiote,
Charge and Launch controls and continues through Fury Command at 34.5s; use
`?scene=survivor` to open on its close-up. The prior homecoming camera, doorway
registration and all nine pilots remain intact. Active ending window resizes
also retain the correct native proportions.

Verification: **8,269/0** regression assertions, **17/0** native survivor checks
and **12/0** preview checks, zero browser errors. The actual engine transition
recording and complete native animation reels were inspected. See
[survivor art, timing and provenance](SURVIVOR_1010.md) and
[portable QA](qa/survivor_1010.json). Local only; no commit or push.
