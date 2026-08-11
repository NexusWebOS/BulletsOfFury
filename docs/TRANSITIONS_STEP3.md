# STEP 3 — 2 -> 3 · LAVA -> ICE

    verify_0730a: 242 passed / 17 failed   (all 17 pre-existing — see §5)
    test_fl:      2093 passed / 190 sections / 2 failed  (both are a missing folder, §5)
    Route runs 478 frames, five beats, hands off to stage 3.

---

## 1. THE TABLE WAS KEYED BY THE WRONG END, AND STEP 3 IS WHERE IT WOULD HAVE BITTEN

Step 3 in your order is the 2 -> 3 join. `TRANS[2]` said:

    2: {via:['water','lava'], note:'water into lava, arriving at the volcano'}

**Stage 2 IS the volcano.** A route leaving it cannot begin over water and cannot arrive at the
place it started. That entry describes the 1 -> 2 journey — jungle, water, volcano.

`transVia()` reads `TRANS[fromStage]`, but entries 2..8 were written as the join ARRIVING at that
stage. Checked against the real biomes in `_levelCfg` — 1 jungle, 2 volcano, 3 ice, 4 crash-town,
5 orbital, 6 sky, 7 sewer, 8 toxic — every single entry shifts by one, consistently:

    old TRANS[3]  'lava into the ice mountains'     is the 2 -> 3 join   <- the one you asked for
    old TRANS[4]  'ice up into the sky, then town'  is the 3 -> 4 join
    old TRANS[5]  'THE BOSS CHASE'                  is the 4 -> 5 join

That last one confirms it from outside the table: the roadmap has always called it *"the 4>5 boss
chase is the big one"*. And stage 5 is orbital, so 5 -> 6 has to descend space -> sky, which is
what sat on key 6.

Entry 1 was already source-keyed — it got corrected when 1 -> 2 was actually built in 0801a, while
the rest were left as authored. That is why 1 -> 2 was described **twice** and 8 -> 9 not at all.

**It was inert.** `via` is read in exactly one functional place, `outboundIsWaterRoute`, which is
hard-gated to `o.from===1`. Nothing else has ever consulted it. It becomes a live bug the moment a
second join is built off the table — which is precisely what this step does. Fixed before building
on it rather than after.

`TRANS[N]` now means **the join leaving stage N**. Seven assertions pin it to the biomes, including
the exact old bug as a guard: *TRANS[2] contains no water, because stage 2 is the volcano.*

8 -> 9 is left with an empty `via` and a note saying it has never been described. Not invented.

## 2. THE ROUTE — VOLCANO OUT, ICE IN

Same shape as 1 -> 2: the player is **held** at the position they had when the boss died and the
world changes underneath. Your water spec — *"follow the player. do not fly them off in the
distance"* — is treated as a standing rule for end transitions, not a one-off, so the generic climb
beat is skipped here too. **Asserted: 0 position changes across all 478 frames.**

Five beats, one more than the water route, because `via` names two terrain changes and not one:

    PAST     2.2s   nst2_master keeps scrolling and accelerating, the caldera passing BEHIND
    LAVA     1.6s   tflat_lava washes down from the top and takes the ground over
    FREEZE   1.8s   tflat_ice washes down OVER the lava
    CRUISE   1.3s   a beat of open ice, so it reads as a journey rather than a wipe
    FADE     1.0s   to black, into the stage-end stats

Both washes descend from the **top**, for the reason the water one does: in a vertical scroller
everything you approach enters from the top and travels down past you. Ice rising from the bottom
would read as the glacier coming up to meet the player. Asserted, so it cannot flip.

The ice can never lead the lava — frost only rises once the lava has fully landed, so there is no
frame where ice sits over bare volcano. Asserted.

## 3. THE SEAM IS STEAM, NOT FOAM

The water route draws a pale foam line where its two surfaces meet. Lava meeting ice does not foam
— it flashes off as vapour and skins over. So the boundary here is a still-glowing crust line with
steam lifting off it, and the steam drifts UP against the scroll, because that contrary motion is
what reads as vapour rather than more scenery.

Same structural job as the foam line (the takeover is never a hard rectangle), correct material.

Asserted by **colour**, not by word: the water route's `190,225,245` gradient must not appear here.
My first cut asserted the source contained no `'foam'`, which the explanatory comment trips over —
a test of the prose rather than the pixels.

## 4. ⚠ THE RIVAL RACE SITS ON THIS EXACT JOIN, AND IT WINS

At stage clear the dispatch is an else-if chain:

    else if(RACE_AFTER[run.stage] && rollRivalEncounter()){ startRivalSequence(); }
    else if(run.mode==='arcade'){ outboundStart(run.stage); ... }

The race branch comes **first**. `RACE_AFTER` is `{2:'a', 4:'b', 6:'c'}`, `rollRivalEncounter` is
documented *"guaranteed encounter after stages 2, 4 and 6"*, and when the race finishes it calls
`beginStage(3)` **directly** rather than handing back. The two are mutually exclusive and the race
takes it.

**This route is reachable today only because `RIVAL_ENABLED = false`.** The day that flag goes
true, the 2 -> 3 transition silently stops playing and nothing anywhere says why.

I have not re-wired it — whether the route plays before the race, after it, or not at all when a
rival shows up is your call, not mine. What I did add is a **tripwire assertion on the flag**, so
that day announces itself instead of the transition just disappearing.

Also worth knowing: the outbound is on the **arcade** branch. Campaign mode hands to the
stage-select instead, so this has to be tested in arcade. Asserted too.

## 5. THE HARNESSES WERE ABORTING, NOT FINISHING

Both suites had the same anti-pattern in an unrelated section — assert a folder exists, then read
it unconditionally:

    ok(fs.existsSync(bk), '...the original lv3 sprite is backed up...');
    ok(!fs.readFileSync(bk).equals(buf), '...');     // <- ENOENT, and the run DIES here

`verify_0730a` died at assertion 82 of 259. `test_fl` died before section 150. Every section after
those points simply never ran, and the output gave no hint that anything had been skipped — the
suite just reported a smaller number.

Guarded both. Not part of this brief, but it was hiding the evidence for it:

    verify_0730a   79 passed / 3 failed  (aborting)  ->  242 passed / 17 failed  (complete)
    test_fl      1713 passed / 0 failed  (aborting)  -> 2093 passed / 2 failed   (complete)

**None of the newly-visible failures are new.** Ran the pristine 0807c tree with only the crash
guard applied: 219 passed / 17 failed, and the seventeen failure lines are byte-identical to the
current ones. This drop adds 23 assertions and zero failures.

The 17 in `verify_0730a` are art/backup checks — `_chroma_backup` and the emblem/pilot-card
placement work. The 2 in `test_fl` are both *"removals are quarantined in `_superseded/`"*, and
that folder — 126MB of quarantine plus eight ledgers — is simply not in this shipped tree. On the
machine 0807c was built on it exists, which is exactly the **2,095 / 191 / 0 failing** the 0807c
passover reported. The counts reconcile.

## 6. WHAT I CHANGED

    assets/game.js               TRANS re-keyed · route added · 2->3 enabled per-join
    _BUILD_SOURCE/gamecode.js    same region back-ported, byte-identical
    _BUILD_SOURCE/verify_0730a.js  23 new assertions · crash guard
    _BUILD_SOURCE/test_fl.js       section 133 re-labelled · crash guard

`assets/game.js` is the authoritative artifact — the 0805a stale-source guard exists because it was
once nine drops ahead of `gamecode.js`. I edited it directly and back-ported the identical region
rather than letting them drift again. Originals are in `_BUILD_SOURCE/_pre0810a_backup/`.

Per-join enablement is unchanged in spirit — `DBG.transitions` still gates 3 -> 4 onward:

    1 -> 2  water         built 0801a
    2 -> 3  lava -> ice   built 0810a

## 7. TEST IT

    COLE2   drops you at the stage-2 boss on its last sliver — kill it and the route plays
            (arcade mode; campaign goes to the stage-select instead)

## 8. STILL OPEN

* **The rival/outbound collision in §4** — your design call.
* **`_levelCfg()` ignores its argument.** It switches on `run.stage`. `outboundDrawWater` calls it
  as `_levelCfg(1)`, which reads like "give me stage 1's config" and does not do that; it is right
  only because `run.stage` is still 1 there. Mine does not lean on it, but the next person building
  a route off that template will not know. Thirty-odd call sites, so I left the signature alone.
* Step 4 in your order is **3 -> 4 · ICE -> SKY -> TOWN**, `TRANS[3]` after the re-key. It wants
  the scale-DOWN into the town, which no route has needed yet.
* The **dam swap** from STEP 2 is still blocked on art — `ASSETS.mapJungleDam` points at a file
  that does not exist, and no 800x3616 destroyed variant exists in the tree.
