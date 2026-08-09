# PASSOVER — drop 0806p   (THE RESTRUCTURE, SHIPPED)

Build: `BulletsOfFury_0806p`
Harness: **2,055 assertions / 186 sections / 0 failing**, twice, reaching the banner.

Third attempt. This one ships.

---

## 1. THE TREE

    assets/
      player/   687 files    ships, thrusters, player projectiles and weapon FX, pilot art, icons
      enemy/  3,575 files    every enemy, miniboss and boss
      game/   4,975 files    stages, UI, effects, fonts, everything else
        music/    22
        sounds/   91

    182 folders -> 23        9,237 files relocated
    broken paths, ALL nine namespaces      0
    stray paths outside the three buckets  0

`game/` has exactly the two subfolders specified — music and sounds — and an assertion fails if
a third ever appears.

## 2. WHAT KILLED THE FIRST TWO ATTEMPTS

**manifest.js declares NINE namespaces**, not one:

    BOF   BOFA   BOFFI   BOFPI   BOFQL   BOFRS   BOFTK   BOFTM   BOFX

0806n rewrote `BOFX.img` and lost the 115-sound registry in `BOFA`. 0806o rewrote both and lost
`BOF`'s logo, boot image, mapJungle and the atlas path for every stage font and stage card.

**The fix is to stop enumerating namespaces.** Treat the manifest as TEXT, pull every
`"assets/..."` string, and repair by BASENAME against the moved tree. One pass fixed all nine —
including the seven I had never identified — because the flatten produces zero basename
collisions, which makes basename lookup unambiguous. 9,237 references repaired, 0 ambiguous.

The new assertion works the same way: it reads the manifest as text, so it cannot be fooled by a
namespace nobody remembered.

## 3. THE OTHER TWO TRAPS, BOTH NOW ASSERTED

**`find -empty -delete` ate protected folders.** `assets/levels/level9`, `assets/fonts/stages/9`
and `assets/music/stages/9` are on `PROTECTED_ASSETS.json` for the unbuilt stage 9. They are
empty RIGHT NOW — empty is not the same as unneeded. They are re-created after every cleanup with
a `.keep` marker, and an assertion checks for that marker specifically.

**21 assertions encoded the OLD folder tree** — `enemies/boss`, `enemies/tanks`, `fonts/stages/N`,
`music/stages/N`. Re-pointed, not deleted, and to a STRONGER invariant than they held: every path
in every namespace must resolve AND must live under one of the three buckets. A folder-exists
check never caught a file dropped in the wrong place; this does.

One of them, the sfx check, pinned three literal paths. It now matches on FILENAME — the sample
it resolves to is the real guarantee, and the folder is the restructure's business, not that
assertion's. It survives the next move too.

## 4. THE HONEST NOTE, REPEATED

This buys **zero** runtime speed. The manifest maps a key to a path and the browser opens it;
nothing in the frame loop touches the directory tree. It is a maintainability win — 182 folders
to 23 — and worth having for that alone.

The performance that actually moved this session was **2,891 MB -> 2,555 MB decoded**, and every
megabyte of it came from resolution caps and atlases, not from layout.

## 5. STILL OPEN

* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment.
* The **ice-level freeze** retest — still the one thing I cannot check myself.
