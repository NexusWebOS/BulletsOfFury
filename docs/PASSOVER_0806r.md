# PASSOVER — drop 0806r   (DATA FOLDER, AND THE TREE DOWN TO 9)

Build: `BulletsOfFury_0806r`
Harness: **2,055 assertions / 186 sections / 0 failing**, twice, reaching the banner.

---

## 1. THE TREE

    assets/
      game.js  manifest.js  section_geom.js      <- the three loaded scripts, nothing else
      data/            3 files                    live config the game reads
        anchors/       3                          rig anchor dumps
        reports/      27                          build artefacts
      player/        687
      enemy/       3,575
      game/        4,865   music/ 22   sounds/ 91

    182 -> 23 -> 14 -> 9 folders

The root of `assets/` now holds only the three files `index.html` actually loads. Every `.json`
in the project — all 33 — is under `data/`, subfoldered as allowed.

## 2. FOUR REFERENCE SITES, ALL FOUND BEFORE MOVING

The lesson from the two failed restructures is to locate every reader FIRST. For the data move
there were four, and only one of them lives in the manifest:

    assets/game.js          fetch('assets/ui_layout.json')    -> data/
    _BUILD_SOURCE/gamecode.js   the same fetch, in the source
    test_fl.js              ROOT+'/assets/PROTECTED_ASSETS.json'
    test_fl.js              the _KEEP allow-list regex

All four updated in the same pass. **0 broken manifest paths** afterwards.

⚠ `_thruster_map.json` has now lived in FOUR locations. Its reader resolves a list rather than
pinning a path, which is why it survived this move without a code change — the fourth entry was
added to the list. That pattern is worth copying anywhere a build artefact is read by literal
path.

## 3. SIX FOLDERS THAT EXISTED TO GUARD NOTHING

`assets/levels/level9`, `assets/fonts/stages/9` and `assets/music/stages/9` — plus their parent
chains — were the entire remainder after the data move.

I wrote the assertion protecting them ONE DROP AGO, after `find -empty -delete` ate them in
0806n. Right instinct, wrong target: the three-bucket move had already relocated the stage-9 art
into the buckets, leaving those folders as empty shells whose only purpose was to satisfy my own
check. **Six directories guarding nothing.**

`PROTECTED_ASSETS.json` now records where that art actually lives, with a note explaining the
change, and the assertion checks the **fifteen protected KEYS** instead. That is strictly
stronger — a folder can exist and be empty; a key that resolves means the file is really there —
and it survives the next restructure, which a hardcoded path never will. All 15 verified.

## 4. WHERE THE CONDENSING STANDS

    folders          182 -> 9
    disk            435 MB -> 470 MB on disk / 414 MB registered
    decoded RGBA  2,891 MB -> 2,555 MB
    atlases                12 sheets, 1,443 cells

**The remaining condensing win is not folders, it is the enemy art.** 0805y measured it at
1,322 MB decoded for a set a session touches 12% of. Per-stage sheets were built and measured at
33.6 MB peak (0806a) and reverted in 0806b because the delivery mechanism threw in the browser.
Redoing that with explicit source-rect blits is the biggest remaining item by an order of
magnitude.

## 5. STILL OPEN

* Per-stage enemy atlases via source-rect blits.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment.
* The **ice-level freeze** retest.
