# Locked Cole and launcher captions - November 6, 2026

Completed Cole first, then the launcher captions, as requested.

## Locked Cole

The main card and both roster slots use actual Cole pilot and high-quality
ship silhouettes. Padlocks replace the question mark. Eighteen even-canvas,
two-frame authored Aseprite banks alternate opaque #606060 and #000000 at450ms
per frame. Both states have identical alpha and pivots; no runtime tint,
opacity animation, scaling or generated placeholder is used by the new blits.

The later black/gray background request applies to Cole while locked: outer
field #000000/#484848 and card #181818/#686868 use opposite contrast to the
silhouettes. Frame/arrow accents become neutral and the old white hover wash
is suppressed for this card. Existing color portraits remain in other slots.
Other selected pilots retain their own palette. Unlocked Cole returns to olive
and his original full-color pilot/jet/copy/stat/selection rendering.

Native isPilotLocked, COLE4U password, deployment refusal, session/save storage
owners and input routes remain authoritative. No debug unlock ships enabled.
Both the classic-card fallback and Pixelmap card delegate their locked branch
to the same renderer. All new frame dimensions are even, and source exports
retain the inspected live cole_body_0922 and ship_cole_pv2 identity.

Source/authoring: _BUILD_SOURCE/locked_pilot_1106/. Runtime metadata and PNGs:
assets/game/shared/ui/locked_pilot_1106/. Registry: locked_pilot_art_1106.js;
renderer: locked_pilot_1106.js. Original production atlases were not repacked.
Rebuild: export_sources.py once against the intended identity, then
build_assets.py (uses installed Aseprite). integrate.py/neutral_background.py
are one-time migration receipts, not idempotent build steps.

## Launcher captions

Under the wordmark: **2026 © COLEFORGE PRODUCTIONS.**
Bottom black panel: **THANK YOU FOR DEDICATED SUPPORT AND APPRECIATION!**

Both are centered, fit the original apertures and use BOF Pixelmap Fury Strike.
Copyright is a real authored glyph169 in all12 native banks, exported offline
by src/CopyrightGlyphs.cs. The unused final cell holds the new symbol; existing
letters remain intact. Old home/options captions and footer instructions are
removed. Controls and installer progress/destination keep their functional UI.

## Verification and scope

- 28 authored-asset/live-Chromium checks passed: exact opaque black/gray,
  identical masks, synchronized gray/black/gray, wide/native480/portrait fit,
  locked deployment refusal, actual password restoration, other pilots and
  no page errors/missing assets.
- Three editable Aseprite roundtrips preserved exact exported pixels, two
  frames and450ms duration. Official API references:
  https://www.aseprite.org/api/sprite/ and https://www.aseprite.org/api/image/.
- 6 actual packaged fullscreen-EXE checks passed, including the
  new artwork, real unlock, SS2/noGOD normal startup, retained interception
  contract and no runtime errors/missing files.
- Five native launcher-caption checks passed; all48 observed text fits
  passed. Copyright is433px within512px available; footer820px within904px.
- Updated installer verifies all18798 included files by CRC/size/SHA256.
  Full installation/uninstall was not repeated for this UI/asset-only revision;
  its unchanged installer logic passed in revision B. No full campaign replay.
- node --check passed for the changed scripts. Required full test_fl still
  exits1 at the pre-existing undefined difficultyHealthBaseline15 helper in
  combat_polish_0927b.js:151 (from test_fl.js:4537). No full-suite pass claim.

## Release

Revision: 2026.11.06c
Installer: C:\Users\Mike\Documents\New project\Releases\BulletsOfFury-Setup-2026-11-06.exe
Installer SHA256: eaa93fbbf197844f2ef6a60785e67ceb78868bede3bb7438494e7a974480b722
Core SHA256: de8d04acc4f903e66290abae59502194ce20f353c16c959e969ac3aa53fbf01d
Host SHA256: 88639db15130794ea44d366d6c25366a90595cd37e0f9902a606d4234c40e9b8

Existing ready game and BOF Launcher.exe in Releases/BulletsOfFury-Windows-2026-11-06
are updated, including all new runtime assets. The launcher preview was refreshed.
No commit or push was requested; existing unrelated work was preserved.
