# Fury HQ Windows installer and launcher - November 6, 2026

Bullets of Fury now has a dedicated Windows x64 executable, a custom per-user installer/uninstaller, and a 90s arcade Fury HQ launcher. The complete existing game and its high-quality assets are retained.

## Deliverables

- Installer: `BulletsOfFury-Setup-2026-11-06.exe` (3,835,068,966 bytes / 3.84 GB).
- Ready-to-run folder: `Releases/BulletsOfFury-Windows-2026-11-06/`; start **Bullets of Fury.exe** and choose **Launch Game**.
- Preview: `Releases/BOF-Fury-HQ-Launcher-Preview.mp4`.
- Original generated artwork, exports, bitmap fonts, motion keys and cue files: the build's `art/` directory. Prompt set and provenance: `ARTWORK.md`.
- All 18,775 payload files are verified during install; 3,843,175,520 payload bytes. Includes all 18,674 game asset files and all 91 extension files from the official mouse/keyboard snapshot.
- Installer SHA256: `c2378bbc6f3b5191ecf05f0a15151f16d7e795a35013e81ce3428b5560535195`.
- Desktop executable SHA256: `bdea011ead60360f2b149eafce678780e2086ccf93347ebab33ab03bdcc85a98`.
- Unchanged game.js SHA256: `0903eec65a966a55980baef7a2eddf59ab4a3f18a8e77868ccb52fa90d231c91`.

## Behavior

The launcher uses new generated hangar, armored door, briefing-console and hexagonal emblem art, the existing BOF logo, and the game's original sounds. Two rigid logo-bearing door panels follow96 explicit eased position keys, with cached opaque image blits and a stopwatch-driven scheduler. Cinematic and quick door timing are selectable.

Mike's typography correction is applied to both launcher and installer: every normal label uses the original **BOF Pixelmap Fury Strike** atlas and glyph metrics. Headings, menu rows, two-column controls, status lines and footer text are centered within explicit bounds. Long text wraps or selects a smaller native font bank (8-32px); glyphs are not stretched. The progress percentage has its own space beyond the segmented bar. All 4,760 text-fit observations during the final install passed; the launcher tour also passed58 fitted labels and was visually inspected at125% Windows scaling.

Launch Game opens a dedicated fullscreen WebView2 window without browser chrome or a local web server. F11 and Alt+Enter switch display modes. Closing the game returns to the launcher. Normal launch has no GOD mode or review bot. Requested controls remain: right-click Retina, Space missiles, hold physical Mouse4 or double right-tap-and-hold Multi-Retina.

Setup verifies each payload file's SHA256, installs through a temporary owned staging folder, and cancels without leaving a partial game. It never overwrites an existing unrelated destination. Normal installs register a per-user Installed Apps entry even if shortcuts are disabled; optional desktop/Start shortcuts use the generated icon. Uninstall is available from Launcher Options and removes only owned files, preserves extra files and separate saves, checks for other BOF windows, rejects linked install paths, and does not recursively delete arbitrary user directories.

Saves live in the local ColeForge/BulletsOfFury application-data profile under the stable `https://bof.coleforge.local` origin. Old browser-port saves are a separate profile and are not automatically imported. The ready-to-run companion intentionally creates no Apps entry or shortcuts; its START-HERE.txt explains this.

## Verification and limits

- Full clean installation of the final centered-font installer completed. Every payload file passed the native installer's hash verification; the installed executable and game core hashes match the release receipt.
- 21 native game/control/stage observations passed: fullscreen at1920x1200, window-mode toggles, normal vulnerability, requested bindings, actual native Retina locks, missile and Multi-Retina volleys, release cleanup, and Stages2/5/6/7/8/9 loading/rendering without missing local assets or page errors. Stage1 supplied the live combat/input fixture.
- 4 additional native restart/exit checks passed: persistent saves/bindings, game Exit returns to the graphical launcher, direct EXE restart preserves the same save origin, and process exit is clean.
- Final ready-to-run EXE smoke passed with SS2 quality, correct local origin, GOD=false, correct mouse bindings and clean exit.
- 15 ownership/path/frame/cancellation checks passed, including traversal/absolute-path rejection and cancelled extraction cleanup. Four uninstall checks passed, including keeping tester-added files and separate saves. A further final temporary uninstall completed and removed its empty owned folder.
- Five PCM exports contain non-silent audio. Windows cue calls completed without errors. Preview visuals are live native-window footage; its exact BOF PCM cues are synchronized from the app event log, not a microphone/system-audio recording. Physical speaker loudness was not certified.
- C# compilation passed without warnings. The application is an unsigned tester build; no signing certificate was used. The included offline WebView2 installer had a valid Microsoft signature. This machine already had the runtime, so the missing-runtime installation branch and other Windows machines were not exercised.
- UI capture observed about 40.1 paint frames/s on this build machine; the requested movement track contains96 keys. This is not a constant60FPS guarantee. The matched uncaptured SS2 Razorback sample measured 30.51FPS in the native host versus 26.32FPS in Edge at matching960x1024 backing canvases and1536x960 CSS viewports. Separate warmed native samples reached47-51FPS. These are one-machine observations under build/test load, not a full-game performance audit.
- The older full JavaScript regression harness remains blocked by the pre-existing missing `difficultyHealthBaseline15` helper in combat_polish_0927b.js:151. Game code/assets are byte-identical to the tested official snapshot; this desktop pass does not claim a full campaign completion or a full-suite pass.
- Real desktop shortcuts/Installed Apps registration were deliberately skipped in QA; that code was compiled/reviewed rather than altering the working desktop. Physical controller hardware and every pilot were not re-tested.

## Platform references

The host loads local game resources through Microsoft's documented [virtual-host folder mapping](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/working-with-local-content). Its bundled runtime/dependency approach follows Microsoft's [WebView2 distribution documentation](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution). SDK version and package hash are retained in vendor/dependency.json; Microsoft license text is included with the installed application.

Source and evidence are retained in `_BUILD_SOURCE/desktop_windows_1106/` and `docs/qa/desktop_windows_1106/`. No commit or push was requested.
