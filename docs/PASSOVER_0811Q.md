# Passover 0811q — the cutscene fits its boxes; "fullscreen" is a decision, not a fix

> Mike, 0811m: *"Cinematics - Needs to be wide/fullscreen, not gameplay size. then it will look
> right. Needs scaling and fitting inside boxes."*

Two asks in one line. **The second is objective and is done.** The first turns out not to be
fixable in code without a real cost, so it is costed and handed back rather than guessed at.

Proof: `docs/proofs/cutscene_0811q_before.png` / `_after.png`.

---

## 1. "Fitting inside boxes" — the text was laid out to the panel, not to its interior

In the before shot the dialogue runs **out over the right rail** and starts **on** the left one,
and the speaker's emblem and name sit on the top-left corner of the frame rather than inside it.

Every surface that puts text in `dlg_window` had picked its own inset by eye. Measured off the
plate — walking in from each edge until the bright machined rail gives way to the dark grid
interior and stays dark for 24px, because a single dark pixel is a rivet shadow, not the interior:

```
dlg_window is 1465x808   ->   interior  x 0.0389   w 0.9208   top 0.0817

drawCutscene assumed          x 0.0199   w 0.9603   (12/604, 580/604)
drawCommWindow assumes        x 0.055    w 0.89
```

The cutscene's column was **6% wider than the frame and started 2% left of it**. That is the
overflow, exactly.

⚠ **THE BOTTOM RAIL CANNOT BE MEASURED DOWN THE CENTRE.** The frame carries a dark star medallion
there, so a centre-column scan runs straight past the rail to the plate's edge and reports
`h 0.915`. The rails are symmetric, so the bottom is taken as the top. Do not "improve" this by
trusting a centre scan.

⚠ **`drawCommWindow` keeps its own looser numbers deliberately.** They are wider insets than these,
so its text sits *inside* its frame and nothing is broken. Changing a surface this drop has not
rendered, on the strength of a measurement taken for a different one, is how a fix becomes two bugs.

### And the size was fixed where it should have been solved

The body was hard-coded at `S(15)` with a comment asserting "three lines of room". Three lines was
true of the old, **too-wide** column; a correct column needs four for the bible's longest line, and
a fixed size cannot know that. It solves against the box now — the largest size whose wrapped block
fits the interior's height — so it cannot go stale when a line of dialogue is rewritten.

`stageFitH` and `stageFitBlock` already existed and were simply not used here. New:
**`stageWrapCount`**, which runs the same greedy wrap **without drawing**. `stageWrap` draws as it
goes and only reports its count afterwards, which is too late to choose a size — so a block could
be fitted to its box's width but never to its height. That was the missing piece.

---

## 2. ⚠ "WIDE/FULLSCREEN" IS NOT A BUG, AND IT COSTS SOMETHING TO GIVE HIM

Measured, so the decision can be one sentence:

```
every cutscene plate      640 x 480   aspect 1.333   (all ten, no exceptions)
the viewport              480 x 512   aspect 0.938
current fit               Math.min -> 480 x 360, centred, 76px bars top and bottom
```

**The design space is already correct for the art.** The letterbox is 4:3 plates in a near-square
playfield, which is the shape a vertical shmup has. Filling the screen means one of:

| option | what it costs |
|---|---|
| **cover** (`Math.max`) | crops **203 of 640 design px — 31.7% of the width**, ~101 each side. That eats both stairwells and would clip the left-hand portrait. Measured, not estimated. |
| **stretch** | fills, but distorts vertically by 42%. On hand-authored pixel art that is not an option. |
| **letterbox** (today) | 76px bars top and bottom. |
| **new plates** | Mike re-authors at the playfield's aspect (or wider). **The code already fits whatever aspect it is handed** — `drawCutscene` derives its scale from SW/SH, so a new plate size needs two numbers changed and nothing else. |

⚠ **The last row is almost certainly what he means** — *"then it will look right"* reads as him
picturing the art filling the screen, and only new plates do that without cutting a third of the
scene off. **It is an art job, not a code one, and it is his call.** Nothing is guessed at here.

---

## 3. Suite

**2,493 assertions / 220 sections / 4 standing failures.**

---

## 4. Still owed from Mike's 0811m list

- **Projectile variety / screen-filling patterns** — the last substantial item, and design as much
  as code. Five boss patterns and the quad-laser's lanes landed this for BOSSES in 0810s; the
  ordinary roster is still the stage-3 change only. Needs a brief on which stages get which shapes.
- **Cinematic aspect** — the decision above.
- **Boats**: fewer on screen since 0811n. If he wants more it is a wave-script change.
