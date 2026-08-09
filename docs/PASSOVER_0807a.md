# PASSOVER — drop 0807a   (I TRIED TO DECIDE WHICH ART IS DEAD, AND CAUGHT MYSELF TWICE)

Build: `BulletsOfFury_0807a`
Harness: **2,068 assertions / 189 sections / 0 failing**. Nothing deleted.

---

## 1. YOU WERE RIGHT THAT I SHOULD JUDGE, NOT JUST HAND YOU A LIST

Observation alone cannot separate "art Mike isn't using" from "frame 7 of a rotation this run
didn't land on". But there is a second, much stronger signal I had not used: **can any code path
build this key at all?** If no fragment of a key's name appears anywhere in `game.js` — as a
literal or as a piece of a dynamic `'prefix'+n+'_'+i` builder — then nothing can ever ask for it.

Applied to the 3,175 never-touched families, that narrowed it to **868 families / 1,321 frames**
with no reachable code path. Names like `nqm_*` and `nqv_*` — 231 frames of what looks like the
quadlaser miniboss art that was superseded when minis moved to `nab_`.

## 2. ⚠ AND IT PRODUCED TWO FALSE POSITIVES THAT WOULD HAVE BROKEN THE GAME

**First attempt flagged `sfont1..9` as dead.** They are the stage title fonts, built at line
26989 as `'sfont'+st+'_'+safe`. My fragment loop only tested `sfont1`, never `sfont`, because the
family name has no underscore to split on. **That would have deleted every stage font.**

I fixed that, deleted 1,508 keys — **and the suite crashed on `sp_lizzie_0..3`**, built as
`'sp_'+pilot+'_'+i`. Missed because `sp_lizzie` reduces to the fragment `sp`, and I had set a
minimum fragment length of 3.

Both are the same bug: **an arbitrary threshold in a heuristic I was about to delete art with.**
Restored in full — 9,535 cells, 0 broken paths, suite back to 2,068.

## 3. WHAT I AM CONFIDENT OF, AND WHAT I AM NOT

**Confident:** the method is sound and the signal is real. A key nothing can construct is dead.

**Not confident:** that my implementation has found every dynamic builder. It missed two in a
single afternoon, and both were only caught because something else happened to depend on them —
`sfont` by my own reading of the code, `sp_lizzie` by an assertion. **A family with no such
guardian would have gone silently.**

So `docs/UNUSED_ART_CANDIDATES.txt` is now a **shortlist of 868 families / 1,321 frames** with
the caveat written at the top, ordered by size. `nqm_*` and `nqv_*` are the strongest candidates
and I would delete those first — but I want you to confirm the quadlaser miniboss really was
replaced rather than take my word for a heuristic that has already been wrong twice today.

## 4. THE HONEST SUMMARY OF THIS WHOLE THREAD

    files          9,283 -> 258
    folders          182 -> 9
    art keys       9,535 served from 78 sheets grouped by USE, not by prefix
    duplicates     994 redundant copies collapsed (213 MB)
    playable       verified: 20 screens, 8 stages, boss reached on every one, ZERO blanks

The one thing not done is the deletion, and it is not done because every automated route to it
has produced a false positive that would have shipped broken art.

## 5. STILL OPEN

* The deletion, once you confirm `nqm_`/`nqv_`.
* Helix contact burst POSITION · flame / ice fade-on-release · miniboss slow/shield ·
  stats-screen alignment · the ice-level freeze retest.
