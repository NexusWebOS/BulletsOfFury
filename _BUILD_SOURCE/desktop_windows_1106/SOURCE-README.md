# Fury HQ Windows desktop host

FuryDesktop.cs is the native Windows x64 launcher, installer, uninstaller and fullscreen WebView2 game host. ExportArt.cs exports the generated artwork and existing BOF logo. All production art, native font banks, motion keys and cue exports are retained in art/.

Build inputs: Windows .NET Framework C# compiler, Python for build orchestration, FFmpeg for the existing cue exports, the Microsoft.Web.WebView2 SDK listed in vendor/dependency.json, and the Microsoft-signed offline x64 runtime installer. SDK assemblies/loader and runtime installer are build dependencies, not checked into this source snapshot. Obtain them from the official URLs in the dependency record and report.

Set BOF_GAME_SOURCE to the production game repository. Set BOF_OFFICIAL_RECEIPT to the official mouse/keyboard snapshot package.json and BOF_OFFICIAL_ZIP if its ZIP moved. Run build_host.py, then build_installer.py. The source assets are already exported; rerun ExportArt.cs only when authoring those exports again. seal_installer.py refreshes the host inside an existing payload without recopying every unchanged game asset.

QA scripts are retained as the exact local probes used for this Windows pass; adjust their staging paths when running them in another checkout. Never use the --qa-* switches or debug ports in normal shortcuts. Normal play has no invulnerable bot. No game-engine rewrite or art-quality reduction is part of this desktop host.

The user-facing controls, centered text geometry, and Fury Strike font selection are in RenderScene/Fit/CenterWrap. Fitting selects native bitmap banks, not resampled system fonts. The 96-key door track contains positions for two rigid authored panels. The renderer uses cached opaque bitmap blits and literal font pixels.

The temporary bof-deploy.zip packaging cache was removed after final verification to recover disk space. build_installer.py recreates it from the official ZIP and host inputs. The released setup EXE contains the complete payload.


NOVEMBER6 REVISION B
Game EXE defaults to direct fullscreen play. BOF Launcher.exe is a companion
copy of the same host and selects the graphical HQ by its filename (or --launcher).
--setup / embedded installer payload and --uninstall still take priority.

Rebuild host with build_host.py after ExportArt.cs if art changes. The current
release refresh is refresh_release_1106.py: carries unchanged compressed art
from the existing complete installer, overlays current core/index/rules/pilot
background changes, rewrites the ownership manifest, verifies every member's
CRC/size/SHA256, then atomically replaces the installer. It requires the existing
release and ready-game folder. build_installer.py is the initial bootstrap from
the archived official snapshot; follow it with the current refresh for revision B.
update_game_1106.py is a one-time source migration preserved for audit, not an
idempotent build step. Native checks: verify_1106b.py and release_verify_1106b.py.

Framework4.6.2 target, app longPathAware and explicit validated Win32 namespace
on extraction writes support deep staging folders without changing Windows
registry settings. Payload.Open accepts either a raw ZIP or a trailer-sealed EXE.
Reference: https://learn.microsoft.com/en-us/dotnet/framework/migration-guide/retargeting/4.6.x

NOVEMBER6 REVISION F / PUBLISHED NOVEMBER8
The current complete Windows release is2026.11.06f. With the existing verified
installer and ready-game folder, use refresh_release_1106f.py, then
zip_release_1106f.py. These preserve original compressed assets and verify every
payload file. Earlier B/D/E refreshers are retained as historical tools.
Revision F includes the original Stage5 sky/starfield and64px assembly cells;
D's audio/loading/map/flame repairs and C's locked-pilot/launcher presentation
are retained. The graphical host itself remains the verified native binary.

Install-BulletsOfFury.cmd/.ps1 are the public two-part release installer helper.
It verifies individual SHA256 hashes and the reconstructed EXE before opening
setup, or validates already-downloaded parts using -VerifyOnly. It downloads
only from the fixed NexusWebOS/BulletsOfFury release and embeds no credential.
The small fixture helper tests and complete-game source checks are documented
in docs/GITHUB_WINDOWS_PUBLICATION_1108.md and the linked QA reports.
