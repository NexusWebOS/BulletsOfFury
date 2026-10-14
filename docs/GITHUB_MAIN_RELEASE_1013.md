# BOF main-game release — October 13, 2026

Mike requested publishing the completed main-game work to GitHub. This snapshot
contains the Stage 4 core/ordnance repairs, Stage 6 scene isolation and solo
miniboss, Rebel audio recovery and Voss turbo return, stage-specific mini-aircraft
palettes, fragile/faster formations, airborne headings/rolls, later-stage enemy
patterns, crimson carrier weapons, Hammer/Spread/firewall improvements, browser
performance changes, the animated enemy atlas and offline Field Manual extension.
Required authored art, sound, source/provenance, launchers and probes are included.

The separate in-progress Overdrive gameplay/art changes remain local. Only its
three query-gated atlas integration additions are included here; the atlas uses
the existing published Overdrive roster and APIs.

GitHub was fetched and reviewed at eb182add8; no incoming commits were present.
The final gameplay suite completed 8,700 passing checks, zero errors and exit 0.
Latest targeted verification: 332 native encounter checks plus 12 palette sheets,
zero browser errors; all four difficulties with focused Chrome/Firefox checks.
Sources, scope and limitations: docs/STAGE_REPAIRS_1013.md and linked QA reports.
Earlier combat, atlas, animation and performance tests remain in their reports.

Dependency audit verified main/atlas/extension local references and new runtime
art/audio paths, with no missing shipping resources. No new file exceeds GitHub's
size limit. Screenshots, caches and the old Contra prototype scratch stay local.
The exact shipping snapshot is recorded by this commit, not the concurrent
working tree. No manual laptop-speaker or complete human campaign claim is made.

Publication snapshot check: an HTTP fixture exposed only Git-index files and
served all 18 unstaged tracked paths from the index. The complete native Overdrive
atlas probe passed 139/139 checks with zero browser errors; the main game and
atlas also booted correctly. Actual startup/atlas pixels were inspected. Portable
summary: docs/qa/github_main_release_1013.json.
