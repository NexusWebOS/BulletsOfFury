# PASSOVER — drop 0806t   (ATLAS AUDIT + DIRECTORY STRUCTURE)

Build: `BulletsOfFury_0806t`
Harness: **2,055 assertions / 186 sections / 0 failing**, reaching the banner.

---

## 1. ATLASES — 27 WIRED, 1,403 CELLS, 208.3 MB DECODED

**Built this session and wired (3):**

    nba_boxpill     45 cells    496x683      1.4 MB   stage 1-9 boxes + pills
    nia_icons       57 cells    668x656      1.8 MB   weapon + special icons
    nsa_ships      162 cells   3120x1805    22.5 MB   every ship frame, all 9 pilots

**Pre-existing and wired (24):**

    main.png       267 cells   1024x9383    38.4 MB   the legacy BOF.atlas
    stagefont1-9    47 each    2688x1152    12.4 MB each  = 111.6 MB across 9 sheets
    stage1-5 art  86-100 each  ~1024x1100    4.5-5.5 MB each = 24.1 MB across 5
    pbar_atlas_*     -          288x840      1.0 MB each = 9.0 MB across 9 pilots

**Built but NOT wired (9):** the per-stage enemy sheets `nes_0..8` — 459 cells, 12 MB on disk,
135 MB decoded if all were resident. They are on disk and de-registered, so they never load.
Reason in 0806s: the delivery mechanism is known (patch `CanvasRenderingContext2D.prototype`,
not one ctx) but I could not verify it headlessly, and this feature has already broken the game
once.

⚠ **Worth flagging from this audit: the nine stage fonts are 111.6 MB decoded** — more than half
of all wired atlas memory, for title cards shown for a couple of seconds each. Every one is
2688x1152 holding 47 glyphs. That is the same "stored far larger than drawn" pattern that gave
7.9x on the box/pill sheet, and it is the biggest single number in the table. Worth a look before
the enemy sheets.

## 2. DIRECTORY STRUCTURE

    BulletsOfFury/
      index.html            the game
      minimal.html
      assets/               9 folders · 9,283 files · 481 MB
        game.js  manifest.js  section_geom.js     <- the only three files index.html loads
        data/          3      live config
          anchors/     3      rig anchor dumps
          reports/    27      build artefacts
        player/      687      ships, thrusters, player projectiles + weapon FX, pilot art, icons
        enemy/     3,575      every enemy, miniboss, boss
          atlas/       9      the unwired per-stage sheets
        game/      4,863      stages, UI, effects, fonts, atlases
          music/      22
          sounds/     91
      docs/          41 + proofs/     every .md and every proof render
      _BUILD_SOURCE/ 57      gamecode.js, patches.js, assemble.py, test_fl.js, probes
      _superseded/    8      permanent stub, excluded at zip time
      tools/          1

## 3. CONDENSED THIS DROP

The project ROOT was carrying 26 loose `.md` files and 23 loose `proof_*.png` renders alongside
`index.html`. Verified first that nothing reads them — 11 mentions in code, **zero** of them a
`fetch` or `readFileSync`, all comments — then folded them into `docs/` and `docs/proofs/`.

    project root:  52 entries -> 7
    assets:        182 folders -> 9   (0806p/q/r)

The root is now the two HTML files and five directories.

## 4. STILL OPEN

* Stage-font atlas resolution — 111.6 MB, the biggest number in the table.
* Enemy sheets — need one browser confirmation (0806s §3).
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment · the ice-level freeze retest.
