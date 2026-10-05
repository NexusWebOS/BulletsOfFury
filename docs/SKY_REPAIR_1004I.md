# Stage X arena, blue giant fighter and fragile bombers — October 4

Mike reported that XHARR / XREBEL displayed Stage VI's arena, the giant fighter
alternated between blue and dark frames without white damage flashes, and the
bombing passes took too many hits.

The authored Stage X mountain/water arena was gated only by the retired single
duel system's `Rival24.active`. Both new passwords and campaign rematches use
`run._gp4StageX` instead. The background and transition renderers now recognize
either encounter owner, while ordinary stage entry clears the rematch flag.
XHARR / XREBEL keep their correct Harrier / five-Rebel encounters and music;
HARR6 / REBEL6 retain the original Stage VI arena.

The later September 30 giant-fighter renderer bypassed the earlier blue-frame
aliases. Its idle module branch ignored `b.flash`, and module hits used a white
hue composite rather than solid white. The current, larger airframe now uses
twenty authored blue poses and six matching module plates. Equal-luminance
palette normalization changes gray armor to blue, retaining outlines,
highlights, measured chrome engine masks, saturated engine/ordnance colors,
frame bounds and exact alpha. Separate white PNGs use the original alpha.
The renderer honors both whole-body and local module flashes, including rolls,
underside views and damage states. Module flash expiry now belongs to simulation
so a roll cannot hold an old module flash until the ship returns to idle.

Stage VI planned bombing passes, opening bomb runs and green bomber lanes have
six HP across Easy, Normal, Hard, Furious and Insanity. Their warnings, speed,
missile locks, bombs and guns remain authored. These fragile targets bypass the
generic protected-first-impact latch, allowing a lethal missile/heavy round to
destroy a bomber immediately. Ordinary unarmed gates and bosses retain their
existing durability and damage rules.

The owning builder `_BUILD_SOURCE/build_sky_repair_1004i.py` creates fourteen
PNGs, the manifest, runtime registration `assets/sky_repair_art_1004i.js` and
the `sky4i_` taxonomy entry. Its sources remain in
`assets/game/encounters_0930/`; SHA-256 hashes and measured luminance rounding
error are recorded in `assets/game/sky_repair_1004i/manifest.json`.
No AI regeneration, packed atlas edit, source deletion or new visual design
was needed. The existing authored fighter is preserved.

Native Chromium verifies real keyboard password entry, both campaign rematch
arenas, all twenty blue/white render poses, actual body/left-wing/right-wing
collision damage, six-basic-round kills for five bomber roles on five
difficulties, immediate lethal missile kills, and retained gun attacks.
The six playable review buttons are also exercised. 75 checks pass with zero
page/console errors. Screenshots of both Stage X
encounters and the native pose/hit contact sheet were inspected. The existing
Furious stealth-flight regression additionally verifies original lane warnings,
Retina missiles, atom bombs, guns and all entry directions.

`node --check assets/game.js`, modified gameplay/background scripts and generated
art registration pass. The full test_fl suite reaches BUILD OK with 7,177
assertions and exit 0. The original Stage X source-string test was replaced by
an ownership check; it now tests the rematch flag and a non-Stage-VI guard.
The test harness retains CRLF and game.js retains LF. Initial restricted
Playwright launch encountered Windows pipe error 5; the allowed local Chromium
launch completed. No implementation test failures remained.

The first legacy flight probe let the full mission's fake-out squad trigger
Cole's protected dialogue during its sixth case, correctly suppressing the
orange gun attack. Its isolated-flight fixture now clears that squad and story
before running. The initial failure log is retained separately; the corrected
fixture passes. Production dialogue protection was preserved.

This is controlled encounter/pixel verification, not a complete campaign clear
or a claim that final difficulty feel has been human-tested. Changes are local
and uncommitted; all prior work is preserved.

Playable review: `_shots/sky_repair_1004i/review.html`.
Portable evidence: `docs/qa/sky_repair_1004i.json`.
