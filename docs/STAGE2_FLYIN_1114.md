# Stage 2 moving lava fly-in — November 14

The LS112 material connector ignored joinY and moved the lava at only 12 pixels/second on its effects clock. The native launch accelerates to 1,750 pixels/second, so the surface appeared stationary underneath the arrival.

assets/layered_stages_1102.js now accepts an optional travel argument in ls112Bed. Only the Stage 2 launch connector supplies it: joinY - VH + efxClock * 12. Both sides of the join use the same tile phase because the incoming level is already translated by joinY - VH. Animated lava frames continue independently. Other material beds retain their original movement; launch speed, camera, ship movement, countdown, gameplay, difficulty and combat ownership are unchanged. The script cache revision was updated in index.html.

Native Chromium checks the actual launch through PLAY, measures more than 1,000 pixels of travel, confirms the connector follows the native join on every sampled frame, and verifies different rendered pixels when only the join moves while the effects clock is held fixed. Screenshots and the 18.81-second audio-enabled real-time card-to-launch-to-gameplay recording were inspected. No page, console or asset errors. This is a launch checkpoint, not a full-stage playthrough. Syntax passes; full suite exits 0 with 8,969 passing assertions, zero failures and its success banner. No new failure names.

Evidence: _shots/stage2_flyin_1114/review.html and docs/qa/stage2_flyin_1114.json. Reproduce using _BUILD_SOURCE/probe_stage2_flyin_1114.py or record_stage2_flyin_1114.py against the running D: build on port 8765. No new art, commit or push.
