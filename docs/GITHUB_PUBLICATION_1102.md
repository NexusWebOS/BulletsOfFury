# November2 complete GitHub publication

Mike authorized uploading the complete current Bullets of Fury work. The source
branches are `main` and `codex/build-2026-10-26`. The review hub uses `gh-pages`.
The release is `bof-complete-update-2026-11-02`.

Included: Stage1–9 enemy refits, ordnance/contact effects, carrier waves, Current
Breaker and its guard, shared difficulty/elemental follow-ups, cast/storyboards,
Furious encounters, audio quality, sources/builders/probes and documentation.
Separate local game projects and local assistant settings remain untouched.

The complete playable runtime is packaged as three standard ZIPs: core,
Stages1–5, and Stages6–9/X. Extract all three into the same directory. The shared
`BulletsOfFury-2026-11-02` folder contains `START-BOF.cmd`; Python3 serves the
game locally. Package CRCs and SHA256 checks accompany the release.

Large preview media is uploaded as release assets with stable route-derived
names and content hashes. Public Pages files point to these assets; they retain
the existing field manual, prior releases and review routes. The new hub features
57 Normal/Hard/Furious boss films,313 regular-wave chapters, the current enemy
guide, four replacement concepts, cast and dialogue storyboards. Local-only
release proxies are converted back to public GitHub URLs. No captured media is
forced into Git history.

Owner: `_BUILD_SOURCE/github_publish_1102.py`. Preparation/source-scan/upload/
package/publication evidence is under ignored `_shots/github_upload_1102/`.
Source publication uses an explicit reviewed path list; Pages uses a separate
Git index and a fast-forward commit without switching the working checkout.
Media hard links and D: package staging avoid full repository copies.

Before publication the native boss collection passed57 playback,20 collection,
11 UI,29+6 storm and complete audio-source/action checks. Razorwake's capture
still averages about41fps. The full core suite exits1 before assertions/summary
on the pre-existing missing `UNUSED_ASSETS/retired_art_1022/manifest.json`; no
bypass or fake archive is introduced. Exact public commit IDs and integrity
results are stored in the final publication receipt.
