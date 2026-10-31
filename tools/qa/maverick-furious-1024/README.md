# Maverick / Furious review recorder (October 24, 2026)

Review tools only. Not loaded by the shipping index.html. See docs/BETA_TEST_MAVERICK_FURIOUS_1024.md for the result, interventions and limits.

Requires Python 3.12, Playwright, an installed Microsoft Edge, Pillow and imageio-ffmpeg; Node is useful for syntax checks. Set BOF_GAME_ROOT to your own game checkout. Run from a NEW output folder: record_campaign.py appends native WebM chunks and telemetry, so do not reuse an existing capture slug/output file. Native audio is captured, not replaced. Online score submission is disabled in the review context.

The bot starts Maverick on Furious without God mode, enables the game's native God mode after its first death, favors the southern playfield and uses normal inputs/pickups/ammo. It does not grant weapons, edit enemy HP, force kills or accelerate the game. This is not a human clear.

## Provenance and reproduction limits

- campaign_bot.js is the compiled seed adapter retained for the campaign. capture_base.js and build_recorder.py make its base available without a private workspace dependency; rebuilding uses the current controller/audio source and is not a byte-identical historical capture.
- live-control-history/ contains the ordered snippets actually applied during the continuous run, with wall-clock application timestamps and SHA-256. These include read-only observers, audio capture repairs, controller refinements and the explicitly disclosed earned-map navigation. They are not silently applied by a fresh run. The archived source plus event log documents the performed run; it is not a seeded deterministic replay.
- record_campaign.py includes the corrected protected-cinematic menu filter. Earlier Enter/Skip mistakes and the old ending-stop condition affected the historical movie and are disclosed in the report. The current campaign_controller.js now uses the effective INV20.end endpoint; rebuild before a future capture. The archived campaign_bot.js deliberately retains the historical compiled seed.
- replay_scenes.py records complete native post-1/post-3 scenes separately. replay_ending.py calls the official native C22 ending viewer, copying only the already-recorded final score for presentation. Neither supplement establishes a new combat victory.
- postflight.py checks decoding/asset retries and a short non-matched native performance sample; --gate-only tests the native gate on a diagnostic part object without touching live boss health. Its synthetic call timing illustrates refresh behavior, not every real attacker's causal contribution.
- media_tools.py encodes normal-speed H.264/AAC and extracts evidence frames without interpolation. Video frame rate and native RAF/simulation are distinct.

Never add these files to a production script manifest or use review God mode to certify human balance. No paid art generations are required by these tools.
