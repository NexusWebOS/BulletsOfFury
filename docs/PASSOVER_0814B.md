# DROP 0814B — ITEM 10: THE RIGHT DIALOGUE BOX WAS BUILT INSIDE A FUNCTION NOTHING ELSE COULD REACH

> 10. Still using plain dialogue where the game has its own boxes. **Asked for twice.**

---

# 1. THE BOX EXISTS. IT WAS PRIVATE.

0811m built exactly the panel Mike is asking for — authored `dlg_window`, the BOF bitmap face, the
body **wrapped and SIZED to the frame**, the speaker's portrait mirrored in the left bay — and
built the whole of it **inside `storyDraw`**, as a hundred lines of local code. Nothing else in the
game could call it. So every other thing that speaks during play went on drawing its own:

| surface | what it drew |
|---|---|
| `thawDraw` (stage 3) | a `fillRect` + `strokeRect` box, canvas BOFmil at 11px, a hand-rolled `measureText` word wrap |
| `freezerL3Draw` (stage 3) | **no box at all** — floating text with a manual drop shadow |

Both are the "faux box" this project has a standing rule against. The 0811m note is *written
against that exact rule*, in a comment, while the two functions beside it kept doing it.

Measured, on the pre-drop tree, by `probe_dialogue_0814b.py`:

| surface | dlg_window | faux rects | canvas fillText | BOF face |
|---|---|---|---|---|
| thaw / SHIP | **0** | 16 | 32 | **0** |
| thaw / PILOT | **0** | 16 | 32 | **0** |
| freezer L3 | **0** | **0** | 16 | **0** |
| stage story *(0811m, control)* | 8 | 0 | 0 | 24 |

The `freezerL3` row is the finding in one line: **zero panels and zero rects** — there was no box
of any kind, not even a bad one. And the story row is the control that keeps the other three
honest: the probe is not simply failing everything.

`dlgBox(o)` is `storyDraw`'s body, lifted out unchanged. `storyDraw` now calls it and is nine
lines. Nothing about the panel changed; it moved.

⚠ **THIS IS NOT `drawCommWindow`, AND THE 0811m NOTE ALREADY SAYS WHY.** That helper opens with
`fillRect(0,0,VW,VH)` at 0.66 alpha — it is a MODAL, and the delivery rule is *"never hold the
player in a dialogue box during active combat"*. There are two legitimate dialogue renderers in
this game, a modal one and an in-play one. **There is no longer a third.**

⚠ **`freezerL3Draw` USED `setTransform(1,0,0,1,0,0)` TO ESCAPE THE CAMERA**, which also throws
away the 2x backing-store scale — so it rendered at half the size of every other glyph in the
game. `dlgBox` undoes the camera the way the rest of the file does, by translating `camX`.

---

# 2. THREE THINGS THE COUNTERS COULD NOT SEE, AND THE FRAME COULD

This is the part worth keeping. After the refactor the probe went **4/4 green** — authored panel,
authored face, zero faux rects, on every surface — and the saved frames were wrong three separate
ways. **CLAUDE.md rule 2, happening inside the probe written to enforce it.**

## 2a. THE THAW'S TEXT RAN OFF ITS RAIL

196x96 was sized for canvas BOFmil at 11px. The BOF bitmap face is far wider per glyph, and with
the portrait bay taking 58 of those 196 the body wrapped into a **96px column**: *"Then let's show
them what BURNING feels like."* came out as `THEN L / SHOW T / WHAT`.

→ the probe now re-measures **every line it saw drawn**, with `msgMeasure`, at the height it was
drawn at, against the panel rect taken from `drawPanel`'s own arguments. Not recomputed, not
inferred — the numbers the draw was handed.

## 2b. TWO PANELS STACKED ON STAGE 3

`thawStart` fires from `beginStage(3)` for everyone; `freezerL3Begin` fires on the same stage when
Freezer takes the flamethrower. **As Freezer, both run.** With small faux boxes in different
corners that was invisible; at the authored size they sat on top of each other.

The narration WAITS now rather than being cut — it is Mike's copy and both halves should be read.
→ the probe counts **distinct panel rects**. Two is a collision, not a dialogue.

## 2c. AND BOTTOM-RIGHT IS NOT AVAILABLE ANY MORE

Anchored right at the standard width, the panel ran **under the EQUIPPED box**, which is drawn
after it and on top: `SHOW TH`, `FEEL` — the tails hidden rather than missing.

⚠ **THE OVERRUN CHECK SAID 0 AND WAS RIGHT.** Occlusion is not overrun. The two look identical in
a table of numbers and completely different in a picture, and only the picture could tell me which
one I was looking at.

0806d put this panel bottom-right so it stayed clear of the ship, and that was correct **for a
196px box on 2026-08-06**. `nequipbox` did not exist then — **0812p** found it registered and drawn
by nothing and put it in that corner. The corner is spoken for. Bottom-LEFT is where every other
in-play dialogue box already lives, so all of them share it and the queue stops them stacking.
→ the probe now intersects each panel rect with the EQUIPPED corner's rect.

## 2d. AND THE LAST ROW SAT ON THE BOTTOM RAIL

The draw tested a row's **TOP** against the limit and then drew its full height below it. A
horizontal-only check cannot see that either.

⚠ **AND FIXING IT MEANT FIXING THE SOLVER IN THE SAME BREATH.** The size solver asked how many row
TOPS fit while the drawer required the row's FOOT to clear — so the solver would have believed in a
row the drawer then refused, and the tail would have vanished **silently**. That is 0811m's
truncation bug arriving by a new route. `rowsFit(h)` is one definition, used by both.

Verified: the thaw's line now **shrinks to two rows and keeps every word** rather than dropping
one — *"THEN LET'S SHOW THEM / WHAT BURNING FEELS LIKE."* — which is 0811m's "fit, do not
truncate" rule doing its job through the new geometry.

---

# 3. VERIFICATION

    suite      2,660 ok / 5 failures  — unchanged from 0814a, the five long-standing ones
    pixels     probe_dialogue_0814b.py   4/4 surfaces clean, real Chromium

| surface | dlg_window | faux rects | ctx.fillText | BOF face | panels | overrun | hidden |
|---|---|---|---|---|---|---|---|
| thaw / SHIP | 8 | 0 | 0 | 24 | 1 | 0 | 0 |
| thaw / PILOT | 8 | 0 | 0 | 24 | 1 | 0 | 0 |
| freezer L3 | 8 | 0 | 0 | 24 | 1 | 0 | 0 |
| stage story | 8 | 0 | 0 | 24 | 1 | 0 | 0 |

`docs/proofs/dialogue_0814b_before_after.png` — the faux boxes against the authored panel, same
stage, same beat.

⚠ **THE PROBE WAS RUN AGAINST THE PRE-DROP TREE AND FAILED 3 OF 4**, in a `git worktree` at HEAD.
A probe that has only ever been green is not evidence. The one it passed is the control.

⚠ **AND ONE PROBE FAILURE WAS THE QUEUE WORKING.** After 2b, the freezerL3 case measured **zero
panels** and read as a regression — because the probe never let the thaw finish, so the narration
was correctly deferring. The case drives the real sequence now: thaw to completion, then Freezer
speaks. **A fix that adds ordering will break every test that assumed there was none.**

---

# 4. FOUND, NOT FIXED — THE APOSTROPHE RENDERS AS A COMMA

Visible in the proof frame: *"THEN LET,S SHOW THEM"*. It is in Mike's dialogue, so it matters, and
it is **not** the box — it survives this drop untouched.

What is known, measured rather than guessed:

- the glyph resolves. `sfont1_p39` / `sfont3_p39` are registered (55x92 cells in `nca_75`), so
  this is not the "stage fonts lack punctuation" case `fontGlyph` already handles.
- `glyphBox` bottom-aligns **every** glyph in the cap box (`dy = H - gh`). An apostrophe is a
  TOP-hanging mark; bottom-aligning it puts it on the baseline, which is exactly where a comma
  sits. **0809q added `FONT_DESC` for glyphs that hang BELOW the baseline and there is no
  counterpart for glyphs that hang ABOVE it** — the fix would be that counterpart.

⚠ **BUT DO NOT WRITE IT FROM THAT ARGUMENT.** Rendered as a contact sheet, `sfont*_p39` and
`sfont*_p44` are both chunky carved slabs and **I could not tell from the plates which way up
either is meant to sit** — this face is stone blocks, not a text face. Rule 1: a `FONT_ASC` table
written from reasoning could just as easily lift a mark that was already correct.

**The way to settle it is one render:** draw `'` and `,` through `msgTextLeft` at dialogue size,
side by side with a `.`, with and without a `dy = 0` override, and look. That is ten minutes and it
is the next thing to pull on this thread.
