# Stage5 to6 full cinematic recording — November14

Mike requested a full recording to review the existing sequence. No game, artwork, input, story, timing, combat or test files were changed.

Recorded fresh real Chromium checkpoints with **Cole / Hard**. Hard follows the Stage6 continuation branch. The native shared game audio bus is recorded directly; every cinematic and dialogue beat runs at its existing native pace, without injected Next/Skip input.

The complete reel is **140.99s**,1824x1024,H264/AAC. It contains Chronos's last words, native core lock/committed missile, chromium ignition and physical armor breakup; orbital/Earth aftermath and monochrome hold; every team return-radio line and Earth descent; the full post5 HQ homecoming, chaingun inspection, earned upgrade and emergency scramble; a direct native launch into Stage6 card/fly-in and all five stealth-ambush radio cues, ending at its first interactive interception.

The reel joins two cinematic checkpoints. HQ through Stage6 is one continuous native capture. Combat preceding the boss defeat, optional result/equipment menus between scenes and ordinary Stage6 combat after the interception prompt are omitted. A fresh isolated Chromium profile was used; this is **not a campaign victory** or an unassisted playthrough. Boss defeat was initialized at the native death checkpoint using the existing lab fixture and native bossDie; no finale phase or dialogue timer was jumped. Native achievement banners may appear in that isolated preview profile.

Validation: all native recorded phase/beat coverage checks pass; no game page/console/HTTP errors. The recorder initially waited for an unused map callback after HQ, but the native story launches Stage6 directly. The excess ordinary gameplay/idle tail was removed after the first interactive SHOOT prompt; no cinematic was removed. Raw footage is retained. The capture endpoint in the repro now follows the actual native Stage6 handoff. Full MP4 decode has zero errors, audible/unclipped native audio ([Parsed_volumedetect_0 @ 000002a57a1b6e00] mean_volume: -14.5 dB; [Parsed_volumedetect_0 @ 000002a57a1b6e00] max_volume: -1.2 dB). All12 browser checks pass, including chapter playback, geometry/duration,206 byte-range seeking and no preview errors. Game.js/test_fl.js/index hashes match before/after. Screenshot samples and decoded representative frames were inspected. No implementation edits required a new core suite run; the existing8969/0 verified baseline remains unchanged.

Video: `_shots/stage56_cinematics_1114/stage5-to-6-full-cinematics.mp4`
Preview: http://127.0.0.1:8766/_shots/stage56_cinematics_1114/review.html
Receipts: `docs/qa/stage56_cinematics_1114.json`
Repro: `_BUILD_SOURCE/stage56_cinematics_1114_record.py`, `_BUILD_SOURCE/stage56_cinematics_1114_package.py`, `_BUILD_SOURCE/stage56_cinematics_1114_verify_movie.py`.

Prior recordings are preserved. No commit or push.
