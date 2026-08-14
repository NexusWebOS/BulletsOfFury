# Passover 0811n — dialogue portraits, and why "boats on water" failed three times

Mike, going to bed: *"continue working and fixing the game. use their portraits for the stage 1 and
onward texts when the portraits appear"*.

The portrait ask, plus the boats-on-water item that has now been attempted in four drops. The
second one turned out to have a cause nobody had looked for, and it is the useful part of this
passover.

---

## 1. Speaker portraits in the stage dialogue window

The panel rebuilt in 0811m now carries the speaker's portrait in its left bay.
Proof: `docs/proofs/dialogwindow_0811m_b.png`.

⚠ **NOT `drawCommWindow`.** That helper already does frame + portrait + typed text and was the
obvious thing to reuse — but it opens with `fillRect(0,0,VW,VH)` at 0.66 alpha. It is a **modal**,
and this file's own delivery rule is *"never hold the player in a dialogue box during active
combat"*, which is why the combat path was a bare strip to begin with. Reusing it would have traded
one of Mike's complaints for a worse one.

⚠ **The portrait is MIRRORED.** Every portrait in the pack is authored facing SCREEN-LEFT — the note
on `drawCutscene` records it and Axel's drawn pistol is the giveaway. A portrait in a panel's LEFT
bay facing left is facing away from its own words. `drawCutscene` mirrors its left slot for exactly
this reason; this is the same slot. Confirmed by rendering: Axel faces into his line.

`pilotPortrait()` already falls back `port_<pilot>_<emo>` → `port_<pilot>_idle` → `face_<pilot>`, so
this needed no new art and no new fallback chain.

---

## 2. ⚠ THE BOATS DO NOT FIT IN THE RIVER

This is the fourth attempt at *"boats only exsit on the water section"*, and the first three each
died with a different-looking explanation:

| attempt | diagnosis at the time |
|---|---|
| every frame | correct (0 on land) but 70 candidate scans per unit per frame changed what section 202 reaches, twice |
| at spawn | free, and moved 0 of 955 — boats spawn above the screen, so the mask row is one they never sit on |
| at arrival (`y>0`, this drop) | ran on 777 of 779 sample-frames and **every one was still on land** |

**None of those was the cause.** Measured this drop, on the rows stage 1's boats actually occupy:

```
widest contiguous water on the row   32px
hull footprint pickWaterX demanded   47px
```

**The boat does not fit.** `pickWaterX` required the whole footprint on water, so it returned null
at every x, on every row, forever — which is indistinguishable from *"there is no water here"*, and
is exactly why this kept being re-diagnosed as a timing problem. Three drops of work on **when** to
call it, when the answer was always going to be null whenever it was called.

`pickLandX` asks for the full footprint and is right to: a tank track hanging over a cliff looks
wrong. A hull overhanging its banks in a narrow channel reads as being **in** the river — that is
how every game of this kind draws it. So the test is now the **keel**, not the beam: `NAVAL_KEEL`
(0.28 of hull width either side) must be over water.

### Two more things the measurement separated out, both of which had been hiding in one number

⚠ **A ONE-SHOT SOLVE CANNOT HOLD, whatever the footprint.** A naval unit CANCELS the map scroll to
hold station on screen — so it does not ride the river, **the river slides out from under it**. The
handoff's premise ("a boat that starts in water and rides a river stays in water, so one solve is
enough") is false for a station-holding unit. The check is per-frame now and cheap — three mask
reads on the keel — with a full search only on arrival and before giving up.

⚠ **TWO THIRDS OF "779 BOATS ON LAND" WAS CORRECT BEHAVIOUR.** Drop 0809n made a boat stop steering
and withdraw off the bottom once the coastline has passed under it; past that point being over
jungle is deliberate. The flat count included those. Split out:

```
779 naval sample-frames  =  527 beached (correct)  +  252 live, all on land
   of the 252:  172 had NO WATER ANYWHERE on the row (a WAVE fact — no placement rule can fix it)
                 80 had water available (a real placement failure)
```

The 172 are handed to `_beached`, which is the behaviour already authored for exactly that case,
rather than a wave-script edit.

### Result

```
                     before        after
live samples on land   252 / 252     2 / 5
boats ever placed        0           314 sample-frames carried the solve
```

⚠ **AND ONE THING IS NOT SETTLED.** The live naval population fell sharply — total naval
sample-frames 779 → 635, beached 527 → 630 — because boats that used to sit on land now either
move to water or withdraw. Withdrawing is the authored behaviour for "past the water" and is better
than sitting on jungle, but **it means fewer boats on screen than before, and that is a gameplay
change Mike has not seen.** It is recorded rather than tuned. If he wants more boats in the water
section the fix is in the wave scripts (spawn them earlier, while the ocean is still under them),
not here.

---

## 3. Probe changes

`probe_stack.py` now reports, for naval units: distinct boats, live vs **beached** samples, how many
live-on-land rows had no water at all versus water available, and **the widest contiguous channel
against the hull footprint**. That last line is the one that ended this; it prints
`*** THE HULL DOES NOT FIT ***` when the geometry makes the search unsatisfiable.

⚠ It also seeds `Math.random` (0811l) and reports scope before any number. `pickWaterX` is in the
scope line now, because it is declared next to `pickLandX` at the top of the file and a
function-scoped copy would measure exactly like a broken one.

---

## 4. Still owed from Mike's 0811m list

Unchanged from `PASSOVER_0811M.md` §6: **cinematic fullscreen**, **projectile wobble** (needs him to
say which projectile — pellets, missiles and the volley layer are three systems), **projectile
variety / screen-filling patterns** (the largest item, and design work as much as code), and the
**pop-in** half of "enemies from thin air" (handoff §2.3 — still blocked on finding which ground rig
picks up `_tracked`/`ground` outside its spawn case).
