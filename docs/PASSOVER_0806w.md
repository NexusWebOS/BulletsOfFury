# PASSOVER — drop 0806w   (1,126 -> 247 FILES)

Build: `BulletsOfFury_0806w`
Harness: **2,061 assertions / 187 sections / 0 failing**, twice, reaching the banner.
**9,535 / 9,535 cells resolve, 0 at the wrong size.**

---

## 1. YOU WERE RIGHT AGAIN — AND THE BIGGEST NUMBER WAS MY FAULT

Breaking down the 1,126 exposed three things, one of them plainly a mistake:

    531  "no reason — MISSED"     three sheets came back UNPACKABLE in 0806u and I let their
                                  keys stay loose without saying so
    308  aliased                  excluded out of caution. Aliasing is TRIVIAL: point every key
                                  that shares a file at the same cell. There was never a problem.
     74  over 1024px              68 of them fit inside a 4096 sheet perfectly well

All three folded in: **903 more images packed into 24 more sheets, 0 unpackable.**

    files under assets   9,283 -> 1,126 -> 247
    keys served by a cell                9,535
    sheets                                  67
    images deleted this drop               903  (123 MB)

## 2. THE 247, AND WHY EACH GROUP IS WHAT IT IS

    113   audio          music + sfx. Not atlasable without an audio-sprite system.
     67   packed sheets  every piece of 2D art in the game
     34   data json      config, anchors, build reports
     29   loose images   too large for a 4096 sheet — the level masters (4800-5360px tall),
                         main.png, the boot image, the logo, the campaign map
      3   scripts        game.js, manifest.js, section_geom.js
      1   other

## 3. ⚠ ABOUT "UNDER 100" — I CANNOT GET THERE HONESTLY

**113 of the 247 are audio.** Music and sound effects cannot be packed into an image atlas.
Getting under 100 total means an audio-sprite system: concatenate every sfx into a handful of
long files and seek to offsets on playback. That is a real technique and it would work, but it
is a rewrite of the audio layer, not a packing pass, and it changes how every sound is triggered.

**Excluding audio, the art side is 134 files** — 67 sheets, 34 data, 29 oversized masters,
3 scripts, 1 other. The 29 masters are genuinely unpackable: a 4800px-tall level backdrop cannot
be a cell in a 4096px sheet.

So: **247 is the honest floor for this approach.** If you want audio sprited, say so and I will
scope it as its own job rather than pretend it falls out of atlasing.

## 4. STILL OPEN

* Audio sprites, if you want them — the only route below ~134.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment.
* The **ice-level freeze** retest, and a browser look at the 67 sheets.
