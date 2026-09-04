# 0902f — CO-OP: the pill is open, both pilots pick, and two ships fly

Mike: *"lets continue with the co-op mode"*, then on the shape of it:

> "when you do the end stats screen, you do a split screen where we show their seperate stats.
> both players also get to pick their own pilot, and when they do we show a screen with both
> pilots they selected via avatar and P1 and P2 symbol above them both in a triangle of ours we
> have flipped vertically facing south"

And on the four questions that decide the data model: **separate lives each**, **separate
scores**, **both pilots chosen up front**, and P2 driving *"either keyboard via 2 player
controller settings, or controller of their own"*.

**Two ships now fly.** The split stats screen is NOT in this drop — see WHAT IS NOT DONE.

---

## ⚠ THIS WAS FIRST BUILT ON `main` AND `main` IS FOUR DAYS STALE. READ THIS BEFORE STARTING WORK.

The whole drop was written once against `Desktop\Github Coding\BulletsOfFury`, which is the
`main` worktree at `52207678` (Aug 29) — **18 commits and 512 KB of `game.js` behind** this
branch. Nothing was committed or pushed, and it was re-done here from scratch, but a full session
went into the wrong tree.

`git branch -a` was run at the start and the branch list was READ AS A LIST rather than as a
question. **`* main` does not mean "main is current."** The check that would have caught it costs
one line:

```
git rev-list --count main..origin/codex/reconciled-house-and-repairs
```

CLAUDE.md already carries a "THERE ARE TWO DIVERGENT TREES — READ THIS BEFORE MERGING ANYTHING"
section. It is about `laptop-0810a`, so it did not name this case, and being about a *different*
pair of trees is exactly why it did not fire. **The rule is the general one: confirm which branch
is live before the first edit, not before the push.**

There are four worktrees of this one repo. `git worktree list` prints all of them with their
branches, and that is the fastest way to see where the work actually is.

---

## THE PORT ITSELF WAS NOT A COPY, AND THREE THINGS WOULD HAVE BEEN WRONG IF IT HAD BEEN

- **Seven weapons here, not six.** `LASER MIST` joined `WEAPONS` and `run.wlevels` grew with it.
  A six-slot `run2.wlevels` copied from the older tree leaves P2's last weapon slot permanently
  `undefined`, which reads in play as *"the mist just does nothing for player two"* — a long way
  from where anyone would look. `run2`'s arrays are built from `WEAPONS.length`, so the next
  weapon added cannot reintroduce it.
- **VERSUS is gone** (0902d) and its row carries a "do not re-add" note. Only the CO-OP row was
  flipped; the table stays at three.
- The player-update block has call sites the old tree did not (the s7 Warden cinematic gate in
  the `firing` expression, extra `keybind.fire` reads for the mist and charge weapons). Two of
  the anchors were **ambiguous** — `if(Input.lf)mvx-=1` appears twice in the file and
  `keybind.fire.some(k=>Input.down(k))` six times — so the edits were scoped to the block's line
  range instead of replaced globally.

---

## ⚠ `player` IS `let` NOW, AND THAT ONE WORD IS THE STRATEGY

There are ~750 `player.` references. Renaming them to `players[i].` across nine stages — in a
file whose recorded failure modes include an unclosed `if` inside `spawnEnemy` that swallows
every declaration after it, a `pShoot` chain of early returns where one weapon claiming the
trigger silences another pilot, and `_selfPat` overwriting any pattern not listed in it — is a
change that cannot be reviewed and cannot be partially reverted.

So `player` stays what it has always been: **the ship currently being updated or drawn**. Solo, it
is P1 forever and nothing in the file can tell the difference. Co-op, `withSeat(2, …)` points it
at the second ship for one bounded section and puts it back in a `finally`.

**The rule that makes it safe:** the swap may only wrap code that is ABOUT ONE SHIP. Never enemy
AI, never the camera. `SEAT_RUN_FIELDS` is the reviewable list of what is per-player; everything
off it is shared, and `stage`/`distance`/the Gravity Mode group are off it deliberately.

⚠ The `finally` is the whole safety property. This build's own 0902a note records that draw
errors here are **swallowed**, so a throw inside a seat would not even be loud — it would leave
the seat pointing at P2 and every enemy, pickup and camera following the wrong ship for the rest
of the run. That reads as "the game went mad", not as an exception. A probe asserts the restore
survives a throw.

---

## ⚠ MY SEAT-AWARE INPUT BROKE NINE ASSERTIONS, AND THE FIXTURES WERE RIGHT

The first cut of `Input.hold(seat, action)` read the closure-local `down` and the `keys` map
directly. Same answer in normal play; **different answer under test.** Section 16 stubs
`Input.lf/rt/up/dn` with `defineProperty` and replaces `Input.down`/`Input.tap` wholesale, and a
reader that skips the public surface sees straight through every one of those stubs. The
bank/twist sequence, the twist hitbox, the charge-weapon tap and the tier-8 fusion lances all
failed.

Seat 1 now routes through the **same four getters the solo code always used**. This is not a test
accommodation: `Input.lf` **is** the definition of "seat 1 is holding left" — it has been since
the file was written, it honours the keybind table, and going around it means two definitions
that can drift.

---

## ⚠ THE TRIANGLE POINTS EAST. A VERTICAL FLIP IS VERY NEARLY A NO-OP ON IT.

`nsel_arrow` is the menu selection arrowhead — `nca_2` at `[715,1717,109,107]`, with `_r`/`_g`/
`_y` recolours beside it. It points **east** and is close to symmetric about its horizontal axis,
so `FLIP_TOP_BOTTOM` returns almost the same image pointing the same way. Both were rendered
before a line was written.

What makes it face **south** is a quarter turn: `ctx.rotate(+PI/2)`, clockwise in canvas space
because y grows downward. P1 takes the blue arrow, P2 the red — recolours already in the atlas,
**no new art**.

The vector fallback is not decoration: `XART.rdy(k)` is false on its FIRST call, so the first
frame of the muster has no arrow.

## ⚠ `pcard_` AND `card_` ARE NOT AVATARS, AND THE FIRST CUT RENDERED WRONG

`card_` is the full 820x631 roster sheet with stat bars and profile strip; `pcard_` is a portrait
panel carrying a second, **empty** sub-panel. Contain-fitting either into a seat box gives a small
pilot floating in furniture — which is what the first render showed. The avatars are
`port_<pilot>_smile`, the seven-expression sheet the story doc already names as the portrait
source: a framed bust in the pilot's own colour at ~0.7 aspect.

---

## ⚠ WHY P2's DEFAULT KEYS ARE TFGH, AND WHY THE NUMPAD CANNOT BE

The usual split is P1 on WASD, P2 on the arrows. **Not available here**: `KEYBIND_DEFAULT` binds
w/a/s/d **and** the four arrows to the same four actions, so handing the arrows to P2 takes half
of P1's movement from every existing player the first time they open co-op. TFGH + V/B/N is the
largest free cluster left.

The numpad is a trap: `keyName` prefers `e.key`, and for a numpad key that is the **digit** with
NumLock on and **`ArrowUp`/`ArrowDown`** with it off. It would work on one machine, collide with
P1's arrows on the next, and change behaviour when someone pressed NumLock mid-game. **A key
whose identity depends on a toggle cannot be a default.** A probe asserts the two seats share no
bind at all, which is the property that survives someone editing either table.

## ⚠ THE FIRST PAD MUST NOT MOVE

`pollGamepad` took the first pad **present**, whatever slot. Mapping slot 0 to P1 and slot 1 to P2
would break existing solo players: browsers do not compact the gamepad array, so a pad that
reconnects lands in slot 1 with slot 0 null, and that player's controller silently becomes player
two's. It stays first-present for P1, second-present for P2. `padInto(pad, prefix, setk)` is
written once and called twice.

---

## WHAT LANDED

Seat foundation (`let player`, cloned `player2`, `withSeat`/`seatIn`/`seatOut`/`seatList`/
`seatShip`/`seatRun`, `SEAT_RUN_FIELDS`) · `run2` + `PILOTMOD2` · CO-OP pill open, `coopOn`
separate from `run.mode` · `GS.COOPROSTER` + the muster + `coopMarker` · the roster screen run
twice on one cursor, with the handover at the end of P1's comm and back rewinding one seat ·
`KEYBIND2_DEFAULT`/`keybind2`/`keybindFor` saved under `bof_keys2` · parameterised
`keybindValidate` · `padInto` + `pad2_` · `Input.hold`/`tapSeat` · `rebindWho` + the PLAYER 2
CONTROLS block · per-seat movement/fire/bomb/roll, enemy-bullet and ram collision, powerup
pickup, and draw · separate lives via `player.out`.

⚠ **`optSnapshot`/`optCancel` had to learn both seats** — the snapshot carried only `keybind`, so
CANCEL would have discarded P1's edits and silently KEPT P2's. A cancel that half-applies is
worse than no cancel. And **the action alone no longer identifies an options row**: `'fire'`
appears twice, so `rebindAction===r.act` lit both buttons and the click armed whichever drew last.

---

## VERIFIED

**Pixels** — two ships flying a live stage 1 with their own pilot hulls and thrusters; the muster;
the PLAYER 2 CONTROLS block; the solo pilot screen unchanged.

**Behaviour** — a 30-assertion probe in the live game: both tables complete and **disjoint**, seat
routing correct in both directions, P2 firing from pad 2 and P1 not, the swap symmetric,
**the seat restored after a throw**, separate lives, seven-slot weapon arrays, and a solo run
clearing the second seat so there is no ghost ship. Run in a deliberately-broken variant first and
it **failed loudly** — a probe that has only ever been green is not evidence.

**Suite** — baseline at `73d75ece` captured BY NAME before any edit: **3,178 ok / 66 fail**. After:
**3,179 ok / 65 fail**, **zero new failures by name**. Totals identical at 3,244 both sides, which
is the COUNT check rule 3 asks for.

⚠ **A FALSE ALARM WORTH KEEPING.** The first co-op screenshot looked empty and nearly went out as
"co-op does not draw". It was the probe: `invuln` was set to a huge number and the i-frame blink is
`floor(invuln/4)%2`, so both ships shared a hidden phase; then movement keys were held through 200
warm frames, driving P1 into the left clamp and P2 off camera. Instrumenting the actual draw
showed **60 `drawPlayer` calls and 7 blits per seat**. Measure the draw before believing an empty
frame.

---

## WHAT IS NOT DONE

1. **Enemies target P1 only.** Enemy AI runs outside any seat window, so `player` there is always
   seat 1. P2 takes contact and stray-round damage and is playable, but the wing is asymmetric.
   `playerTarget()` exists for those sites to move onto; the audit is its own drop.
2. **Two-score HUD** — separate scores are tracked, nothing shows P2's.
3. **The split stats screen** Mike asked for. `SC_ROWS` and `stageStats` are single-player and
   `stageStats2` does not exist.
4. **Pilot specials are still one global `special`**, so the two seats share it.
5. **Campaign co-op** — out of scope by construction; needs two save slots and both pilots in the
   story tokens.

## OPEN FOR MIKE

- The muster is titled **"CO-OP WING"** — placeholder, not a decision.
- Friendly fire has no answer yet in BOF1 because P2's rounds are not seat-tagged.
- Co-op currently runs the **arcade** structure. Campaign co-op is a separate ask.
