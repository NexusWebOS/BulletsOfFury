# HAMA authored animation integration — 2026-09-29

Password **HAMA** → difficulty → pilot → Stage 5. The local checkout includes the incoming d4abcfd48 engine changes and instrumental, plus the previously generated hammer-only art pack. No back-mounted chaingun is used by this pack.

`assets/hama_frames_art_0929.js` registers 13 live atlases / 112 frames from `assets/game/hama_art_0928`. The source pack retains all 15 reels / 128 frames, including two unused silver moonwalks. `assets/hama_frames_0929.js` loads after the existing HAMA encounter. The generated registry is owned by `_BUILD_SOURCE/hama_art_0928/build_runtime.py`; it validates every live atlas rectangle against its image and retains the source pack unchanged. Rebuild with Python and `--root` pointing at the game checkout.

## Connected behavior

- Eight-frame backward moonwalks in both directions, retaining the regular black-steel/cyan body before and after the intro shield rises. Raising this dance shield does not transform his armor. The unused silver variants are neither registered nor preloaded.
- Twelve-view lasso/hop reels for boss and helpers. Side and back views are authored frames, not rotations of a front sprite.
- Two distinct hammer contact poses, at frames 2 and 7. Impact positions follow the drums in the art; the existing soundtrack cues, explosions, sound and shake retain their timing.
- Sixteen-frame hammer toss / helper grab / shoulder carry / release / beckon. Nearby and carried helpers are already in the body plate, so their independent sprites are hidden. The held target, warning origin and caption follow the carried helper's actual position.
- Eight-frame detached hammer spin and eight-frame thrown-helper tumble. The thrown robot keeps the existing target, damage and death behavior; its sprite no longer uses canvas rotation.
- Singing and chanting helmets replace compatible front helmets at the neck. Side/back helmets stay intact. The carried helper also uses the singing helmet on its front carry pose.
- Twelve-frame vocal leap, including recovery, through the engine's body pose hook. Existing ground reticles, attack lanes, collision and recovery mechanics remain owned by the combat engine.
- A replacement helper is recalled once at the authored summon pose. Combat draws helpers once, rather than drawing the troupe twice through nested renderers.
- The instrumental waits for the complete HAMA pack to decode before the shared entrance/music gate opens. The atlases load only when HAMA is selected.

The original HAMMER password retains its remix and render path. Campaign healing/armor logic, missile counters, chaingun loadouts and other incoming changes are preserved. The original encounter's measured media clock and cue sheet remain in `hama_0928.js` / `hama_art_0928.js`; this pass adds no verse transcription.

## Verification

`test_hama_frames_0929.cjs` is registered in the complete suite. It also re-runs the original HAMA behavior assertions after the new hooks are installed, covering throw/catch, double slams, lock windows, helper immunity, song selection and cleanup. New assertions cover art readiness, contact frames, attachment coordinates, replacement summon, duplicate suppression, authored flight views and original HAMMER isolation.

`probe_hama_frames_0929.py` uses real Chromium and the actual game loop. Its deterministic cue pass pins the media clock, checks all 13 live reels through the game context's own `drawImage`, saves screenshot and source-frame evidence, and checks page/console/draw errors. It also checks both moonwalk directions through the shield rise and rejects silver moonwalk draws. This is an integration probe, not a difficulty balance verdict. Real-time playback is checked separately without pinning the music clock.

Temporary screenshots, cue logs, video and frame evidence belong under `_shots/hama_frames_0929`, not the shipped asset manifest. Local changes are left uncommitted for Mike's next upload request.

Original integration results before the moonwalk correction: full suite **5,768 passes / 0 errors**; focused dependency/HAMA section **58 passes / 0 errors**; native Normal **48/0** and Furious **47/0**, with every authored frame rendered and no page, console or draw errors. The real-time 36-second canvas recording includes the actual instrumental audio track, three hammer launches, two completed catches and jump/boomerang combat. The game advanced 1,597 frames with maximum measured game/media clock difference under 80 ms. This earlier recording contains the superseded silver switch; the current screenshot/probe replaces it for appearance review. The recording uses an invulnerable observer pilot and captures the instrumental; it is not a player survival run or a mixed sound-effects capture.

Moonwalk correction verification: full suite **5,769 passes / 0 errors**, focused section **59/0**, native Chromium **47/0**. All 112 active frames rendered; both directions kept the regular body through the shield rise, with no silver draws or page/console/draw errors. Current screenshot: `_shots/hama_frames_0929/moonwalk_regular_body_shield_up.png`.
