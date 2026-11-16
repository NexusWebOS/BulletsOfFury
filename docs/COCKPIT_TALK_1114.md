> Rejected appearance set: Mike identified the1114 cockpit art as old and then confirmed row B of the source comparison. Current newly generated cockpit/album art is documented in [COCKPIT_CASTB_1115.md](COCKPIT_CASTB_1115.md). Earlier key-binding tests below did not establish the intended character versions.

# Talking cockpit pilots — November 14

Mike requested talking frames of Cole and every pilot seated inside their own ships, matching the newer dialogue illustration style. This pass belongs to the original BOF checkout at `D:/BOF-Downloads/2026-11-14/RevG-source`.

## Artwork

Nine approved cockpit identities were supplied as generation references: Cole, Axel, Freezer, Yuri, Maverick, Falva, Lizzie, Decker and Juggernaut. The newer Decker dialogue portrait supplied the ink/pixel shading reference. Cole retains the short swept brown hair, close beard, blue eyes and green flightsuit from Mike's approved cockpit likeness.

Each pilot has one generated complete 4×2 talking sheet. Production exports use fixed 576×384 cells and one common anchor. Slots are idle, A, E, O, U, F/V, small speaking mouth and blink. Opaque aviators on Axel, Maverick and Juggernaut hide their eyes, so their blink slot intentionally repeats idle. There are 72 slots and 69 distinct exported images. No SpriteCook assets were generated in this pass.

The sprite pipeline normalizes the complete strip at a shared scale, aligns its upper face, and retains the neutral cockpit/body outside the generated mouth/eyelid regions. Hands, harness, controls, hair and cabin remain fixed. Four square/tight first drafts were rejected and regenerated as landscape cockpit compositions before export. Raw accepted generation sheets, exact prompts, references and hashes are retained in `docs/COCKPIT_TALK_ART_1114.json` and `_ART_SOURCES/cockpit_talk_1114`.

There are 45 shipping WebP banks: nine full cockpit sheets plus four small radio sizes per pilot (48, 64, 84 and 96 pixels). All cells have even dimensions. Runtime WebP total is approximately 6.42 MB. WebP can discard hidden RGB under zero alpha; visible RGBA and all alpha remain stable outside the animated regions.

## Runtime

`assets/cockpit_talk_art_1114.js` registers art; `assets/cockpit_talk_1114.js` loads after the service data-link module. It uses the existing dialogue reveal count to select mouth shapes, then returns to idle when the sentence finishes or another pilot speaks. Visible eyes blink during idle. Existing letter sounds, dialogue speed, input, native continuation, rewards and gameplay cameras remain authoritative.

The new art is wired into:

- The Stage 1 jungle comic cockpit panel.
- The post-Stage-2 service data-link scene's selected pilot.
- Native comic radio panels marked cockpit-sky, cockpit-space or cockpit-tunnel.
- Existing direct cockpit scene plates.
- Small native radio windows in all three cockpit locations.

In-person HQ/workshop/hangar portraits retain their location-specific front portrait family. This preserves the remote Decker/Cole technician role instead of putting the person at base into a ship. The previous service terrain camera-bounds repair is retained.

`window.BOF_COCKPIT_TALK_1114` exposes the owner and diagnostic metadata. It does not own dialogue timers or campaign state. `assets/game.js` and `_BUILD_SOURCE/test_fl.js` were not edited.

## Verification and preview

`_shots/cockpit_talk_1114/review.html` contains a 25-second native montage of all nine pilots, a frame-bank preview, and Cole's complete native service data-link scene through its single map continuation.

- Syntax checks pass for the core and both added modules.
- Full core suite reaches its final summary, exit 0: 8,969 passing assertions and zero failing names, unchanged from the immediately preceding all-green baseline.
- 59 native Chromium cockpit/dialogue checks pass: all nine pilot assets, active speech, idle listeners, the jungle panel, generic radio framing, location bindings and letter-to-mouth selection.
- 28 additional native radio checks pass, including actual source-cell blits for every pilot in sky, space and tunnel windows.
- 129 asset/suite checks pass, including stable visible pixels outside mouth/eyes, exact even bank geometry and complete pose sets.
- Ten native clips retain audible dialogue effects. No page, console or HTTP errors were observed. Both final MP4 files decode without errors. Audio peaks are below clipping (service −2.1 dB; montage −2.3 dB).
- Rendered native screenshots and decoded video frames were inspected for face identity, complete hair, framing and steady cabin details.

These are cinematic and radio-window checkpoints, not campaign playthroughs or combat-balance certification. There is no recorded spoken voice track; mouth shapes follow the letter reveal and the existing dialogue letter sounds.

Durable structured evidence is in `docs/qa/cockpit_talk_1114.json`; raw probe/recording logs are under the preview directory. No commit or push was performed.

## Reproduction

The canonical source record is `docs/COCKPIT_TALK_ART_1114.json`. `_BUILD_SOURCE/pack_cockpit_talk_1114.py` rebuilds staged exports under `_shots/cockpit_talk_1114` using the bundled sprite-pipeline scripts. Review the staged atlas before installing its WebP files and generated manifest.

Native proof scripts are `_BUILD_SOURCE/cockpit_talk_1114_probe.py`, `_BUILD_SOURCE/cockpit_talk_1114_probe_radio.py`, `_BUILD_SOURCE/cockpit_talk_1114_record.py`, `_BUILD_SOURCE/cockpit_talk_1114_verify_assets.py` and `_BUILD_SOURCE/cockpit_talk_1114_encode.py`. The server must serve this checkout on port 8765. Chromium recordings trap duplicate rAF chains, drive the real game loop, capture the game canvas and shared audio mixer, and normalize output to 30 fps for clean MP4 timestamps. The frame gallery separately cycles exported art and is labelled accordingly.
