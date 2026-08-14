# Passover 0811r — speaker colour, typing sound, and the black edges that were already there

> Mike: *"see how the text is spiling out of the window, you need to frist off use the right colors
> via palette swap for the character whose speaking, load each word letter by letter like the pilot
> cards with sound, and give all my pilot unit frames black edges"*

---

## 0. ⚠ THE SPILL IN HIS SCREENSHOT IS THE PRE-0811q BUILD

His frame shows three lines ending **"CONNECTED TO"**, with the last word on the right rail. That is
`docs/proofs/cutscene_0811q_before.png` exactly. The committed build breaks after **"CONNECTED"**
and puts "TO IT IS BECOMING A WEAPON." on line three — `cutscene_0811q_after.png`.

Another chat's dev server is running in this folder, so the page in front of him is almost certainly
stale. **Nothing was re-fixed on the strength of that screenshot** — the measurement (interior
x 0.0389 / w 0.9208 against an assumed 0.0199 / 0.9603) stands, and re-fixing a fixed thing on a
stale render is how a codebase grows two overlapping fixes for one bug.

---

## 1. The speaker's own colour, as a palette swap

`PILOTS[].tint` — the colour each pilot's emblem, card and HUD already use (Cole `#7ad63a`, the
green on his emblem in the frame). Taken from that table so it cannot drift from the art. Applied
to the name **and** the body.

⚠ **THERE ARE TWO DISAGREEING TINT TABLES FOR THE SAME NINE PEOPLE.** `STORY_TINT` — used by the
in-game story panel rebuilt in 0811m — has `COLE:'#ff6b3a'`, orange, against `PILOTS`' green.
`PILOTS` is the one that matches what is drawn, so it wins here. `STORY_TINT` is **left alone**
rather than changed blind on a surface this drop has not rendered. Worth reconciling; worth
rendering both first.

⚠ **`stageWrap` HARD-CODED `null` FOR THE TINT** and had no parameter for one, so no caller could
colour a wrapped block however much `stageText` supported it — which is why the cutscene dialogue
was the only text in the game with no speaker colour. `tintC`/`tintA` are appended, optional;
existing nine-argument callers get `undefined`, which `stageText` already treats as "no tint".

⚠ **It is safe to pass a colour here only because 0809q exists.** `drawFrameTinted` uses `'color'`
(source hue/sat, destination luminosity, then `destination-in` to re-mask) precisely because a
`source-atop` flood repainted this face's opaque drop shadow the same colour as its face and turned
every **E into a B** for three drops. Verified by rendering: the letterforms survive the swap —
`docs/proofs/cutscene_0811r_tinted.png`.

---

## 2. Letter by letter, with sound

The letters already arrived one at a time. What the scene had was **silence** — eight authored
ensemble scenes whose only audio was the music cue 0811a added.

⚠ **MATCHED TO THE PILOT CARDS' FEEL, NOT COPIED FROM THEIR CODE.** `pcUpdate` does:

```js
C.typed += PC_TYPE_CPS*dt;
if((C.typed|0)%3===0 && ... && Math.random()<0.5) Audio.SFX.blip();
```

That test runs **every frame**, not on a character. At 42cps and 60fps one character sits on the
same integer for about a frame and a half, so the same letter can blip twice — the random coin is
what stops it sounding like a buzz rather than any cadence. Here the blip fires on the character
actually **advancing**, every third one, which gives the same sparse tick deterministically.

**The pilot-card version is left as it is.** It is not what he reported, its coin flip masks the
fault, and changing a screen he did not complain about is how a fix becomes a regression. Recorded,
not quietly altered.

---

## 3. ⚠ THE BLACK EDGES WERE ALREADY IN THE ART. SMOOTHING WAS DISSOLVING THEM.

Measured before touching anything — boundary pixels of the source cells:

```
ship_cole_pv2    97.5% dark   mean edge luminance 18.7   magenta 0
ship_falva_pv2   93.8%                            19.8            0
ship_yuri_pv2    97.5%                            14.9          0.2
ship_lizzie_pv2  93.7%                            26.9            0
ship_axel_pv2    92.9%                            19.2            0
ship_decker_pv2  92.8%                            19.8          0.7
```

**Every pilot hull already carries a black edge** — `docs/proofs/shipframes_0811r_before.png` shows
the outlines plainly. There was no missing art to add, and adding any would have been drawing over
work that was already done.

What there was: `drawPlayer` blits a **226x271 cell at h=60** — a 4.5x downscale — under the canvas
default set once at init, `imageSmoothingEnabled = true` with `imageSmoothingQuality = 'high'`.

⚠ **AND THE EFFECT IS NOT WHAT I FIRST WROTE.** I described it as averaging the rim to grey. Measured
at the real drawn size, both ways, the edge pixels stay about as dark either way — what changes is
their **alpha**:

```
              SMOOTHED (shipped)          NEAREST (fixed)
cole          soft-alpha rim  94.7%       soft-alpha rim  13.0%
falva                         89.0%                       19.1%
yuri                          89.4%                       11.3%
lizzie                        77.7%                       14.1%
```

Under smoothing **78–95% of the boundary is semi-transparent.** A black rim at 30% alpha over a
bright stage reads as a soft haze, not a line. The edge is in the file and not in the frame.

Nearest-neighbour is not a preference here, it is the contract this file states at a dozen other
draws (*"pack contract: nearest-neighbour"*) — `drawCutscene`, the mech pieces, the arcade plates
and the boss rigs all set it, and the player hull never did. Set around that one blit and restored
after, so nothing else inherits it.

⚠ **THE TRADE, STATED PLAINLY.** Nearest-neighbour at a 4.5x reduction samples rather than averages,
so the hull is crisper **and** harder — Lizzie's roundel detail thins out, and the whole ship reads
more aliased. Side by side in `docs/proofs/shipedge_0811r_smooth_vs_nearest.png`. Mike asked for
black edges and this is what delivers them, but if he prefers the softer hull it is **one line** —
delete the two `imageSmoothingEnabled` lines around the blit.

---

## 4. Suite

**2,493 assertions / 220 sections / 4 standing failures.**

## 5. Still owed

- **Projectile variety / screen-filling patterns** — the last substantial item; needs a brief on
  which stages get which shapes.
- **Cinematic aspect** — all ten plates are 640x480 against a 480x512 playfield; cover crops 31.7%
  of the width. New plates are the only clean answer and `drawCutscene` already fits any aspect.
- **Boats**: fewer on screen since 0811n.
- **`STORY_TINT` vs `PILOTS[].tint`** — two colour tables, nine people, disagreeing.
