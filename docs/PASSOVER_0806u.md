# PASSOVER — drop 0806u   (9,283 FILES -> 1,126)

Build: `BulletsOfFury_0806u`
Harness: **2,055 assertions / 186 sections / 0 failing**, twice, reaching the banner.

---

## 1. YOU WERE RIGHT AND I STOPPED SHORT

I built three atlases, deleted only those three families' frames, and left **9,113 individual
images** still being referenced one at a time. That was not the job.

    files under assets   9,283 -> 1,126
    keys served from a packed sheet          8,192
    sheets                                   43
    source frames deleted                    8,192   (205 MB)
    still loose files                        964     (masters, backdrops, audio, aliased art)

## 2. HOW IT IS WIRED — THE SHIP MECHANISM, NOT 0806a's

8,192 of the 9,598 registered keys resolve out of 43 packed sheets. The cell is extracted into
its own canvas and cached, **lazily** — a cell nobody draws costs nothing beyond its share of
the sheet.

That is deliberately the SHIP sheet's mechanism, already proven in your build, and not 0806a's
descriptor. **A canvas is a CanvasImageSource**, so it is safe in all twenty-six 2d contexts,
needs no prototype patch, and cannot throw the way 0806a did. The cell is rebuilt at its own
natural size, so every caller that scales by `naturalWidth` lands exactly where it did when the
key was a loose file.

⚠ **Order matters, and it is subtle.** `BOFX.img` still names the SHEET for every atlased key, so
anything asking "is this registered / is the file on disk" gets a true answer — the harness alone
does that in hundreds of places. But `_touch` checks `BOFX.cells` FIRST, because at runtime the
cell must win or a key would resolve to the whole 4096px sheet instead of its own frame.

**Verified before deleting anything: 8,192 / 8,192 cells resolve, 0 at the wrong size.**

## 3. WHAT IS DELIBERATELY NOT IN A SHEET — 964 FILES

Not everything should be packed, and each exclusion was measured:

    aliased art        750   two or more keys share one file; packing would silently fork them
    over 1024px         74   level masters and backdrops — a 4800px master cannot be a cell
    other namespaces     7   BOF/BOFA name the file directly, not through BOFX
    not png              9
    the 43 sheets + audio + data + the 3 scripts

## 4. SIX ASSERTIONS THAT MEASURED THE WRONG FILE

Every assertion that measured a key's SIZE was reading the sheet's dimensions once the key
pointed at one — `mbg2_mflash_0` came back as 2752x3655. They read `BOFX.cells` now, via one
`cellSize()` helper, which is where the frame's real width and height live.

The Decker Vol.3 check pinned a content HASH — meaningless once packed, since hashing the file
hashes the whole sheet. It pins the cell DIMENSIONS instead: the three generations shipped
different-sized boxes, so size still tells them apart.

## 5. STILL OPEN

* The nine stage fonts are **111.6 MB decoded** — 2688x1152 each for 47 glyphs. Biggest single
  number left, and the same "stored far larger than drawn" pattern that gave 7.9x on the box/pill
  sheet.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment · the ice-level freeze retest.
