# Stormglass Academy — dedicated tutorial stage

Enter from a fresh Campaign, Arcade or Co-op pilot selection and choose **YES — FLY STORMGLASS ACADEMY**. The academy is offered again even if the older Stage1 tutorial was completed. The default changes to NO after graduating from this new course; YES always replays it.

## The course

A classified offshore academy with a newly generated, transparent architecture plate and its own visual cruise clock. It never borrows Stage1 terrain or its runway, campaign waves, bosses or stage clock. It remains a tutorial route rather than a campaign stage slot or password.

Fifteen lessons: movement beacons; gunfire; supply crate; barrel roll; somersault; manual missile; Retina lock; multi-lock missile queue; committed FOV lanes; ground strike reticles; actual pilot special pickup; elemental Forge briefing; the chosen pilot's primary and secondary loadout briefing; three graduation waves ending in the instructor drone; a rating and debrief.

The tutorial uses the real selected aircraft, weapons, pickups, hit flashes, muzzle effects, sounds, Retina and enemy destruction. Training targets have fixed HP and bullet speed on Easy, Normal, Hard and Furious. Hits remain visible and count toward the final rating but never consume a life. Targets give no score. Only the crate lessons admit supply drops. Colored warnings are FOV lanes, with no anchored arrow boxes. Targets are placed below the complete radio and objective strip.

## Real ocean animation and parallax

1. New PixelLab ocean:32 distinct224x224 frames at12fps, on one lossless lazy-loaded atlas;10px/s travel, camera factor0.24.
2. Six authored distant cloud poses at2.2fps,15px/s travel, camera factor0.36.
3. New transparent academy structures,28px/s travel, full camera response.
4. Six authored nearer cloud poses at2.2fps,39px/s travel, camera factor0.82.

All scenery layers draw beneath aircraft and projectiles. Water animation has its own time input and continues even when architecture travel is held fixed. Pause freezes course time. PixelLab water plays directly from one texture; no recoloring canvases or legacy-water fallback. Native clouds remain shared. The dedicated PixelLab water pack adds 375,493bytes; see STORMGLASS_WATER_PIXELLAB_1020.md for source and validation. The unused opaque first concept stays in the art-source archive, outside playable assets.

## Ownership and rebuild

- Runtime: `assets/stormglass_tutorial_1020.js`, after the approved Command UI owner.
- Terrain: `assets/game/levels/tutorial/stormglass_1020/architecture.webp`,680x1360 with genuine alpha.
- Source, exact prompts and audit: `_ART_SOURCES/stormglass_1020/`.
- Builder: `_BUILD_SOURCE/build_stormglass_1020.py`. One proportional nearest export; even canvas; no shared atlas edits.
- Native QA: `_BUILD_SOURCE/probe_stormglass_1020.py`.

The bounded tutorial asset list warms the two training hulls, shared weapons/pickups/effects, radio, FOV art, water and clouds. It avoids loading Stage1's full scenery and bosses for this route. Existing campaign warm/loading functions resume on exit. Sound preparation runs once rather than restarting pending downloads every frame.

Completion stores only tutorial completion/rating data and hands the original Campaign or Arcade start back to its native owner. Skipping has the same handoff without awarding completion. Co-op training is solo and restores both seats afterward. Main-menu exits clean up the tutorial and restore its borrowed mode.

## Validation

- Native Edge: 22/22 checks passed, no page/console/missing-asset errors.
- Input-only completion of all15 lessons, including the real two-target missile queue and all3 graduation waves.
- Actual hit-flash pixel change and restoration; fixed tutorial HP/speeds in all4 difficulties; pause, Campaign skip and co-op restoration.
- Visible ocean pixels change while academy scroll is held still. Native draw positions prove four different camera-parallax factors; travel speeds are independent. Machine-gun cue is decoded and requested through the shared mixer.
- Desktop and narrow screenshots, plus native animated preview in `_shots/stormglass_1020/review.html`.
- Core and tutorial JavaScript syntax checks pass. Full regression: 8,940 passing assertions, BUILD OK,0errors, exit0.

No GitHub publication was requested for this change.
