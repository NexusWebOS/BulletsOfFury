# Passover 0811u — the suite is deterministic now, and one red became honest

Three assertions in `test_fl.js` reported differently run to run **with no code change between
them**. Measured across roughly nine runs in one session, the suite came back with **4, 5 and 6
failures**, and the rotating offenders were always the same three:

```
202   "miniboss shield aura"        a 200-second play simulation
208   "every volley fired is 5-8"   14 seconds of live stage with one boat in it
212   "curveL bleeds LEFT"          7 seconds of live stage per route
```

⚠ **THIS IS WORSE THAN AN OCCASIONAL RED.** Rule 3 in CLAUDE.md is *"0 failures can mean a crash —
ALWAYS CHECK THE COUNT"*, and a suite whose failure count moves on its own teaches everyone to stop
reading it. Two separate investigations this session had to attribute a red before they could trust
it: 212's `curveL` measured **-48 in-suite and -177 in isolation**, across three seeds and both arms
of an A/B.

---

## 1. The cause was never the assertions

All three run the **live stage plan**, which picks waves, spawn offsets and fire cadences from
`Math.random` — so each of them measures a slightly different battle every time. That is the same
*"comparing two runs measures wave randomness rather than your change"* trap the probes already seed
against; the suite simply never did.

`seedWaves(n)` installs a fixed LCG for the duration of a fixture, `unseedWaves()` puts the real one
back. Nothing outside those three fixtures changes behaviour.

**Result — three consecutive full runs, no code change between them:**

```
run 1   ok 2500   fail 5   sections 221
run 2   ok 2500   fail 5   sections 221
run 3   ok 2500   fail 5   sections 221
```

Identical. Before this, those same three runs would have disagreed.

---

## 2. ⚠ AND IT SETTLED ON 5, NOT 4 — WHICH IS THE POINT, NOT A REGRESSION

Seeded, *"every volley fired is 5-8 rounds"* fails **every** run with the **same numbers, (6, 3)**.

That is not a new defect. It is the same one that has been failing intermittently for weeks, now
visible on every run instead of one in three. **A consistently red test you can attribute beats a
flaky one you learn to ignore**, so the standing-failure count going 4 → 5 is the fix working, not
a regression.

⚠ **AND ITS RED IS NOT YET ATTRIBUTABLE TO THE GAME.** The obvious reading of a trailing 3-round
group is the 14-second window closing mid-burst — a fixture artefact, not a short volley. Testing
that meant running the same fixture at 14/17/20/26 seconds standalone, and **it fired zero rounds at
every length**, with the fixture's own setup lines copied verbatim.

**That is the real finding.** The fixture only produces volleys at all because of state left by the
~200 sections that run before it. Its result is therefore meaningless in isolation, and no threshold
should be touched on the strength of it — which is exactly why the seeding note in the file says
**"it seeds, it does not tune"**.

Lifting it into a standalone probe is the remaining work, and it is a real piece of work: it means
establishing which accumulated globals the boat needs before it will fire. Recorded rather than
started, and **not** worked around by widening the range until it goes green.

---

## 3. What this changes for anyone reading a suite run

- The count is **2,505 assertions / 221 sections / 5 failures**, and it should be that every time.
  A different number now means something actually changed.
- Four are the long-standing ones (preload count, the two `_superseded`, the naval flash families).
- The fifth is the volley fixture, red by design until it is lifted out.
- `curveL bleeds LEFT` and the miniboss aura are green and stable.

## 4. Still owed — all needing Mike

- **Cinematic aspect** — ten plates at 640x480 against a 480x512 playfield; cover crops 31.7%.
- **Boats** — fewer on screen since 0811n.
- **`STORY_TINT` vs `PILOTS[].tint`** — two colour tables, nine pilots, disagreeing.
- **0811s's stage assignments** — which stage gets which of the four new bullet shapes.
