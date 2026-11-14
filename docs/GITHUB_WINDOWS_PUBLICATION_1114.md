# Current Windows build publication — November14,2026

Release: https://github.com/NexusWebOS/BulletsOfFury/releases/tag/bof-windows-2026-11-14-revg

Download [BOF-Install-Helper-RevG.zip](https://github.com/NexusWebOS/BulletsOfFury/releases/download/bof-windows-2026-11-14-revg/BOF-Install-Helper-RevG.zip), extract it, and run Install-BulletsOfFury.cmd. The helper downloads17 byte-exact installer parts, verifies each SHA256, joins them in order, verifies the complete setup EXE and opens native Fury HQ setup. It preserves earlier releases and local saves. Allow16GB free during download/setup. Windows10/11 x64; all game graphics/audio, the unchanged byte-verified Fury HQ host and signed offline WebView2 runtime are included. No Python or separate browser is required to play.

This is the current development prerelease for playtesting. Mike's unassisted full experience/balance review remains pending. The older RevF stable release is retained.

## Source and complete payload

The full pending source/art update was committed as636ee1165cf697c7cdbfef6e8e1947dd93c49026. Tracked development-only reference fixtures and publication tooling followed in5eb79c862c16cbde66b29b810948d7baf6abbb5a. Both existing publication branches, main and codex/build-2026-10-26, were fast-forwarded together without rewriting history. All current Chronus/Draconus animation, rage, ship and modular-gun work, Stage5 bomber behavior/targeting, pilot/playtest work, authored editable sources, documents and regression fixes are included. The final receipt/documentation commit follows the tagged runtime snapshot without changing gameplay.

The complete installer is4,412,658,675 bytes with SHA256 `8dabf873fc7484158eebf56cb7bce8698ee189d2b43d61ba9551b7fd7e1bea7a`. Its payload contains21,040 owned files totaling4,511,531,539 unpacked bytes. All committed runtime inputs matched their Git blob IDs while being packaged; the exact legacy signed offline runtime bytes matched their known hash. All remote installer-part digests match the local streamed bytes. The embedded footer, complete deployment manifest, unique entry names and every entry size were read back from GitHub and verified. 733 critical/active-script files were fully read back, decompressed and SHA256-checked against the deployment manifest. The existing native installer verifies every extracted payload file's SHA256 again when installed.

## Checks and previews

- Full regression runner reaches its final summary with8,969 passing assertions, zero failures and exit0, using only the tracked reference fixtures rather than the optional local ignored archive.
- Actual native Windows host:14 self-tests passed. Its executable and embedded original launcher artwork are unchanged from the previous verified host.
- A clean build directory with byte-identical hard links avoids a second4GB copy. Its fresh title and Stages5/6/7/8 load/update/render checks pass with no page/update/draw errors. The directory's files are bound to the uploaded manifest and source identities; the uploaded payload itself is separately checked above.
- Current source also retains the previously verified60 native bomber/weapon checks,7 active-targeting checks,256 exact editable retina frames and restored16 native leech cells.
- All25 published assets have verified GitHub SHA256 digests. Anonymous retrieval verifies the helper ZIP and sample beginning/footer bytes from the public installer parts.

Three native checkpoint previews accompany the build: new beeping/rotating/flashing bomber target lock; two full bomber attack/flight cycles; Draconus's new rage/two-handed wave/center smash. Their invulnerable review labels remain visible. They are behavior previews, not unassisted full-stage clears. Previous full-stage films keep their original dates.

See qa/github_windows_publication_1114.json, qa/github_publication_1114/ and the release validation/checksum manifests for exact counts, source hashes and verification limits. Publication scripts are retained in _BUILD_SOURCE/github_upload_1114. They use the existing GitHub login only in memory; no credential or signed asset URL is published. Large temporary installer parts are removed locally only after their remote SHA256 is confirmed. No existing user data or prior GitHub release assets are deleted.
