# Passover 0809q — the tint that ate the E, and the Fury HQ cutscenes

## 1. `ENTER` rendered as `BNTBR`, and it was never the font

This had been on the open list for three drops as "every `E` in that face resolves to the `B`
glyph". It was not a glyph problem at all.

Three things were checked and all three were innocent:

- **the map** — `A→g00, B→g01, C→g02, D→g03, E→g04, F→g05`, sequential and correct
- **the atlas** — cropping `bof_font1.png` at E's rect and B's rect gives a difference bbox, and
  rendering the row shows a clean `A B C D E F G H`
- **the slices** — `sfont1_*` rects match the true column runs of the sheet exactly, contiguous
  with no drift (A ends 322 / B starts 324, D ends 740 / E starts 742, and so on)

The cause was `drawFrameTinted`. Every glyph in this face is a bright letter drawn over its **own
opaque dark drop shadow**, and the tint was a flat `source-atop` flood — which repaints that
shadow the same colour as the letter. The gaps between an `E`'s three arms *are* shadow. Fill them
with face colour and the E becomes a solid block, which is a `B`.

Proved with a controlled render of `NEXT BEEF` at 11/13/15/17/20px through both blit paths:

| path | result |
|---|---|
| untinted | `NEXT BEEF` — clean at every size, including 11px |
| tinted, `source-atop` @ 0.9 | `NBXT BBBF` — wrong at **every** size, including 20px |

Size was never a factor. I initially took it for a nearest-neighbour minification problem and
added filtered downscaling; that hypothesis was wrong and the change has been reverted, so the
pixel-crisp look is unchanged.

The fix is `globalCompositeOperation='color'` — source hue and saturation, **destination
luminosity** — then `destination-in` to re-mask, because the blend spreads past the glyph's alpha.
The shadow stays dark, the face takes the colour, and `tintA` still blends toward the untinted
original so every existing call means what it meant.

`multiply` was tried first and also preserves the shadow, but it can only darken: it cannot lift
the gold face to the pale chrome the hint row asks for, so that row came out warm. `'color'` is
the palette swap the standing rule actually describes.

**This was global.** Every tinted string in the game had it.

## 2. Commas were rendering as a raised middot

Same area, different cause, and this one *was* geometry. `glyphBox` bottom-aligns every glyph in
the cap box — correct for a period, which is all head. A comma is a period-sized head plus a
**descending tail**, so bottom-aligning the whole cell rests the tail on the baseline and lifts
the head to mid-height.

`glyphBox` now takes the character and drops `,` and `;` by their own height minus the period's,
which derives the amount from the art instead of a tuned constant. All five call sites pass it.

## 3. Fury HQ cutscenes

`CF_FuryHQCutscenes-Vol.1` shipped 224 files and a bible and none of it was reachable.
`drawCutscene()` could already compose a scene — background, up to three bottom-aligned portraits,
the `dlg_window` frame, emblem, name, body — and **nothing called it**. What was missing was a
state.

Added:

- `HQ_SCENES` — all eight ensemble scenes from `FuryHQ-Cutscene-Bible.md`, verbatim, 70 lines.
  Curly quotes stripped (this face has no double-quote glyph). Poses map to the pack's six sheets.
- `GS.CUTSCENE` + `drawCutsceneState(dt)` — types at 42 chars/sec; first tap completes the line,
  the next advances; `menuBack` skips the scene; holds on black while the art loads rather than
  treating a not-yet-ready background as missing.
- `hqTrigger(when, stage, next)` — fires the scene for a boundary and calls `next` when it ends.

Staging is two slots, and a speaker keeps its side: whoever talks takes the slot the *previous*
speaker is not in. The listener stays on screen dimmed, which reads as a conversation instead of a
slideshow of single portraits.

Wired at the two campaign boundaries: the hub's deploy path (`pre`) and campaign stage clear
(`post`), keyed on the stage that just finished because the bible's triggers read "After Stage 1".

Verified contract:

```
fired: true          state: cutscene       scene: HQ_ALL_00 (11 lines)
duringScene: null    <- the stage is held back while the scene plays
beganAfterScene: 1   <- the continuation enters the stage when it ends
replayFired: false   <- once per run
noSceneStage2: false, stage2Continued: 2   <- unscened stages pass straight through
arcadeFired: false,  arcadeContinued: 1    <- arcade untouched
```

Dialogue sits at `S(15)` — sized purely for fit, since the bible's longest line is 118 characters
and needs three lines inside the 112-unit frame.

## 4. Suite

**2,390 assertions / 215 sections / 5 failures.** All five are pre-existing at HEAD — confirmed by
stashing the change and re-running: boss limb pool, preload count, the two `_superseded` ones, and
the naval flash families.

⚠ **Section 202 is flaky.** It simulates 200 seconds of play to reach the stage-1 miniboss, and
its result depends on state left by earlier sections. It failed on one run and passed on a re-run
of the identical file; lifted into a standalone probe it reaches the miniboss every time
(`stageTimer 56.9, waveIdx 16, no throw`). Re-run before blaming a change for it.

## 5. Harness note

`shoot.py --warm N` is a **single synchronous burst** that never yields, so lazily-loaded art never
arrives however high N goes — 1400 warm frames showed a black screen where 200 warm plus
`--seconds 2 --fps 3` showed the scene. Each screenshot is a separate `evaluate`, and that boundary
is what lets the network run. Use `--seconds/--fps` whenever the shot needs art the state loads on
entry.
