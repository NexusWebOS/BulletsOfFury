# Passover 0811o — "enemies appearing out of thin air", closed on all eight stages

> Mike, repeatedly, for drops: *"I still have enemies appearing out of thin air for level 1 ...
> We've gone over this one like 20x."*

```
                        before          after
stage 1  popped in        4               0
stage 2                   6               0
stage 3                   0               0
stage 4                   4               0
stage 5                   4               0
stage 6                   4               0
stage 7                   1               0
stage 8                   0               0
```

Two causes, one of which also closes a second long-standing open item. And the probe that had been
measuring this was wrong twice over, which is why it survived so long.

---

## 1. ⚠ THE PROBE WAS ASKING THE WRONG QUESTION, TWICE

**It only looked at the top edge.** `probe_popin` flagged a unit whose `y - h/2 > 0` and never
looked at x. Stage 1's corner-route jets are authored at `x = -28` / `x = VW+28` with `y = 96/150` —
deliberately off the SIDE at an entry altitude, which is how a corner route is supposed to start
(0801kn, and the clamp that broke it in 0809a). All four were reported as pop-ins. They were not.
Acting on that number would have broken the routes.

**And it read the wrong moment.** It measured `e.x` at `spawnEnemy`'s RETURN. `l6Crosser` and its
siblings correct x on the very next line — *"spawnEnemy clamps x into the field — place truly
offscreen"* — so stage 5's `octo` and stage 6's `fang` both read as `x = 480` and were flagged as
materialising in open sky, when a line later they are at `worldWidth()+50`. **That is the
probe_seam.py lesson exactly: a probe that reads the wrong moment asserts a bug that is not there.**

The test is now: a unit pops in when **no part of its box is off ANY edge on its first DRAWN
frame** — there is no edge it could be entering from. Units are queued at spawn and measured after
the next `loop()`.

Both wrong versions produced non-zero numbers that looked like progress. **Four of the eight
"bugs" this probe reported at the start of this session did not exist.**

---

## 2. `VW` IS THE VIEWPORT. THE WORLD IS 800.

Waves author a right-side entry as `VW+28`. VW is the viewport (480); stage 1's world is its
master's width, **800**. So `VW+28 = 508` is not off the right edge — it is a third of the way in
from it, and a `cornerRL` jet written to fly in from the right materialised in open sky. Left
entries used `-28` and were always correct, which is why this only ever affected one side.

`offRightX(pad)` / `offLeftX(pad)` say what was meant. On any stage whose world **is** the viewport
width they return exactly what `VW+n` did, so this is a no-op there rather than a behaviour change.

---

## 3. ⚠ THE CATCH-ALL EDGE PIN WAS TELEPORTING EVERY SIDE ENTRY ON SCREEN

This is the bigger one, and it is in the enemy update loop:

```js
const _edgeM = Math.max(14, e.w*0.66);
if(!_racerDrifting){
  if(e.x<_edgeM){ e.x=_edgeM; ... } else if(e.x>_wW-_edgeM){ e.x=_wW-_edgeM; ... }
}
```

Any unit outside `[w*0.66, W-w*0.66]` is snapped to that margin **on its very first tick** — so a
wave that authors an entry from off the side never gets one. The unit is placed at x=-28, ticked
once, and is on screen before it is ever drawn. The signature is unmistakable because the margin is
a function of the unit's own width:

```
s1jetdelta_b (w 95)   spawned -28   ->  drawn at  63     (95 * 2/3)
skim         (w 44)   spawned -30   ->  drawn at  29     (44 * 2/3)
talon        (w 60)   spawned   0   ->  drawn at  40     (60 * 2/3)
fang         (w 44)   spawned 480   ->  drawn at 771     (800 - 29)
```

⚠ **AND THE EXEMPTION LIST IS HAND-WRITTEN**, which is the `_selfPat` trap this file already has a
standing rule about. `ai` crossers, racer phases, `topgun`, `sideswirl` and `jetflyby` were listed.
Routed jets (`s1jet`), volcanic skimmers (`volc`) and plain `straight` crossers were not. Drop 0809a
fixed exactly this inside `jetTick` and could not reach here.

**The predicate is geometry now, not a list:** a unit is pinned only once it has been fully inside
the field at least once (`_inField`). Until then it is arriving, and the pin has no business
touching it. Leaving is still handled by the branches below it, and an entering unit falls through
to the soft `±w` clamp, which is exactly right for an entrance.

### ⚠ THIS IS ALSO "SOMETHING OUTSIDE jetTick DISPLACES THEM"

CLAUDE.md has carried that as open alongside *"observed jet speed varies 96–138 even on
`straight`"*. A 91px teleport on frame one is precisely that. **The two open items were one bug.**
The speed figure should be re-measured now; `probe_stack`'s seeded harness is the place to do it.

---

## 4. `inPlace` — a declaration, so the zero means something

Two units are AUTHORED to appear where they are: a splitter's two halves emerge from the wreck
(`ash`, at the parent's x±24), and a sewer `maw` **surfaces** mid-screen. Those are beats, not
pop-ins, and a check that flags them invites someone to "fix" the design — which is how this
session nearly "fixed" the corner routes.

They carry `{inPlace:1}` at their spawn sites now, so the intent lives in the game rather than in a
list maintained inside a probe. Anything without it is expected to enter from an edge.

---

## 5. Suite

**2,491 assertions / 220 sections / 4 standing failures**, plus the known-flaky *"every volley fired
is 5-8 rounds"* — which failed on 2 of 6 runs today **with no code change between them**. It is
attributed (0811m: seeded, separation off and on, identical `volleys=8` and 60.8px drift) and
belongs with §202 and `curveL` in the order-dependent family. Read the COUNT.

⚠ The drivable-band assertions the handoff warned about are green. **They were never the obstacle** —
the mirror-the-y approach they blocked was chasing the wrong cause entirely. No y transform was
needed on any unit: every real pop-in was horizontal.

---

## 6. Still owed from Mike's 0811m list

- **Cinematics wide/fullscreen** — not started; structural, and any resize moves the frame-for-frame
  handoffs `probe_arrival`/`probe_exit` measure.
- **Projectiles "appear wobbly"** — needs Mike to say which; pellets, missiles and the volley layer
  are three separate systems.
- **Projectile variety / screen-filling patterns** — the largest item, design as much as code.
- **Boats**: fewer are on screen since 0811n (they move to water or withdraw rather than sitting on
  jungle). Mike has not seen that yet; if he wants more, it is a wave-script change.
