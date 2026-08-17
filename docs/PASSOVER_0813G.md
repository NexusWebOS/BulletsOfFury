# PASSOVER 0813G — MAGMA VENT takes stage 2's miniboss slot

Mike: *"remove siege ember find a different mini boss for stage 2 out of unused enemies and
minibosses we have"* → he picked **lavamaw** off the sweep.

## What landed

`SUBBOSS[2]` is now `lavamaw` — **MAGMA VENT**, 196x194, hp 234, `pat:'ember'`.

New `SHIPBOSS.lavamaw` entry with `mini:true`, plus a `case 'lavamaw':` on the miniboss build path so
it goes through the same construction as the nsb_ family. Verified in a browser: it spawns, draws its
real art, and carries a miniboss health bar (`docs/proofs/stage2_mini_lavamaw.png`).

`pat:'ember'` — the wall-with-a-walking-gap — because a vent that erupts upward suits that far better
than a ship's missile fan.

## ⚠ The size reading was BACKWARDS, and it nearly killed the pick

The VOLC roster lists `lavamaw:{... w:40, h:38, art:'maw'}`, which reads like a pebble and looked
disqualifying for a miniboss — right after Mike spent a whole drop objecting to upscaled art.

**The art is `nvl_maw_0..5` at 223x220** — a six-frame caldera that fills with magma, floods, then
erupts and shatters. The stage was drawing a miniboss-sized plate shrunk to 40px. At 196x194 the vent
runs *under* its authored size, so it is scaled DOWN. Nothing is upscaled.

Another instance of the standing rule: the table said one thing, the pixels said another.

## ⚠ "I broke the enemy" — no, 0801ip did, on purpose

`spawnEnemy('lavamaw')` returns nothing, which looked like a name collision introduced by putting
`lavamaw` in SHIPBOSS. It is neither new nor a fault: `lavamaw` sits in `_DELETE` (game.js:6255) from
drop 0801ip — Mike's *"delete the ones with no waves, were not using them."* That note also says
**"Their ART stays in the tree — only the ability to spawn goes."**

So the plates were deliberately preserved when the unit was retired, which is exactly why this
candidate works. Check whether a behaviour predates your change before claiming you caused it.

## Assertions

Two pinned siege ember as stage 2's miniboss and failed on the change. **Read before fixing** — they
were recording a design decision Mike has now overruled, not defending a bug. Rewritten to track his
choice, and strengthened rather than merely repointed:

- `SUBBOSS[2].kind==='lavamaw'`
- `SHIPBOSS.lavamaw.mini===true` — a real entry, not an unknown kind hitting the generic 130x120
  fallback (which is what any unrecognised string produces — see below)
- `key==='nvl_maw_0'`
- `w>150 && w<=223` — sized under its authored width, so it can never drift into being upscaled

## ⚠ `spawnSubBoss__inner` VALIDATES NOTHING

It accepts any string and builds a generic 130x120 sub-boss with no art. A candidate-rendering pass
therefore reported eight different units at identical dimensions, all drawing a **red placeholder
rectangle**, and it looked like a roster of real options. If every unit in a sweep has the same w/h,
that is the fallback, not a finding.

## Suite

**2,639 assertions / 234 sections / 5 failures** — the same long-standing five.

## Still open on the reshuffle

- **stage 3** needs a miniboss (thorn rime out). Nothing ice-themed is spare; `glacierrail` is the
  natural fit but Mike scrapped it and thorn rime was its replacement.
- **stage 4** needs one (blacksteel moving to 6).
- **blacksteel → 6** and **olivecarrier → 7** land once 3 and 4 are filled.
- `quadlaser` (QUAD-LASER GUNSHIP, 196x196, 22 keys, full BOFQL layout) is the only other CONFIRMED
  real miniboss with art — displaced from stage 1 when jungle cruiser took that slot.
