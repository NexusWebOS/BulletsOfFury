# October 1 playable build

The current local playable package is `C:/Users/Mike/Documents/New project/release_1001/BulletsOfFury-playable-2026-10-01.zip`. It is 487,046,094 bytes, below the 500,000,000-byte target; SHA-256 `5bc9d12aa6948bbb9ddddafe1bb9863e98e0d7d8386591389c4d68215695100f`. The archive contains 3,218 entries and passed a full ZIP CRC read. The ZIP is a local deliverable and is not committed to GitHub.

The source tree and generated runtime assets are committed separately. To rebuild, run `_BUILD_SOURCE/collect_release_0927.py` in the source checkout to collect the current browser registry, set `BOF_RELEASE_DIR` to a fresh local output folder, then run `_BUILD_SOURCE/build_playable_1001.py`. The package converts registered PNG art to WebP at original dimensions; projectile art, icons and fonts remain lossless.

Verification: the full gameplay suite reached `FALVA/LIZZIE BUILD OK, 0 ERRORS` with 6,121 passing assertions. Focused campaign, repair, realm and cinema tests exited successfully. Native Chromium loaded the packaged map, its binary-row East Coast wall and nine-slot Theater Progression row, then entered Stage 8's portal approach with all 31 realm art keys registered. No page/console errors or HTTP 404s occurred in this packaged smoke test. This smoke test does not claim a complete nine-stage playthrough of the ZIP.
