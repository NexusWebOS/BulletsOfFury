# PASSOVER — drop 0806q   (ANSWERING BOTH QUESTIONS, AND FINISHING THE FOLDERS)

Build: `BulletsOfFury_0806q`
Harness: **2,055 assertions / 186 sections / 0 failing**, twice, reaching the banner.

---

## 1. HOW MANY ATLASES — 12 SHEETS, 1,443 CELLS

Three I built this session:

    nba_boxpill    45 cells   496x683     1.4 MB    stage 1-9 boxes + pills   (0805l)
    nia_icons      57 cells   668x656     1.8 MB    weapon + special icons    (0805p)
    nsa_ships     162 cells  3120x1805   22.5 MB    every ship frame          (0805q)

Nine that predate this session:

    main.png              267 frames   the legacy BOF.atlas
    stagefont1-9_v3        423 frames  across 9 sheets
    stage1-5.png           449 frames  across 5 sheets
    pbar_atlas_<pilot>     9 sheets, one per pilot

⚠ **Note the ships sheet is 22.5 MB against boxpill's 1.4 MB.** That is the line where atlasing
stops paying: 0805y measured the enemy/boss art at **1,322 MB** for a set a session touches 12%
of, and an atlas must decode ENTIRELY. Per-stage enemy sheets were built and measured (33.6 MB
peak, 459 cells) but reverted in 0806b because the delivery mechanism threw in the browser —
they are still the right next atlas, via source-rect blits rather than descriptors.

## 2. WHY 23 FOLDERS — AND IT IS 14 NOW

You were right to push. 23 broke down as 5 intended + `assets/` itself + **17 leftovers**, and
the leftovers were two different things:

**32 unreferenced build files.** `anchors.json`, `_keys.json`, `_bossparts_report.json` and
friends — build metadata that no manifest names. My move relocated files the manifest *referenced*,
so anything unreferenced simply stayed where it was and kept `enemies/`, `fx/`, `fx/_json`,
`fx/master` and `fx/pack0704` alive. All 32 are now folded into the bucket they describe.

**Three protected `.keep` markers.** `assets/levels/level9`, `assets/fonts/stages/9` and
`assets/music/stages/9` are on `PROTECTED_ASSETS.json` for the unbuilt stage 9. Each one drags
its parent chain along, so 3 markers cost 6 folders. **They are the entire remainder.**

    182 -> 23 -> 14

    assets/                    6 config + js files that must stay put
    assets/player/           687
    assets/enemy/          3,575
    assets/game/           4,894   (+ music 22, sounds 91)
    assets/fonts/stages/9        protected marker
    assets/levels/level9         protected marker
    assets/music/stages/9        protected marker

**14 is the floor without changing PROTECTED_ASSETS.json.** Those three paths are the spec; if
you want them re-pointed into the buckets — say `assets/game/stage9/` — that is your call to
make, not mine, and it drops the tree to 6.

## 3. ⚠ THE SUITE CRASHED AND READ AS A PASS AGAIN

After relocating the 32 files the run reported **1,348 ok / 0 fails**, which looks fine until you
notice it should be 2,055. It had thrown on a literal path — `assets/fx/_json/_thruster_map.json`
— and never reached the end.

The resolver that opens it already handled TWO locations, because this file has moved before. It
now handles three, and resolves rather than pins: a build artifact that moves should not take the
harness down with it. **Counting the assertions is the only thing that catches this** — the exit
banner and the failure count both looked healthy.

## 4. STILL OPEN

* Per-stage enemy atlases, via source-rect blits (0806b §1).
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment.
* The **ice-level freeze** retest.
