# Passover 0811m — Mike's bug list: the icon chain, the dialogue window, the arcade banner

Five of the nine items on Mike's 0811m list. Four are not attempted and are listed in §6 with what
is known about each, rather than half-built.

Suite: **2,491 assertions / 220 sections / 4 failures** — the four standing ones. See §5, two
assertions in this suite are order-dependent and need reading carefully.

---

## 1. ⚠ THE PICKUP ICON CHAIN HAD FOUR ELEMENT TABLES IN IT (items 1 and 2)

> "On Level 3 - Fireorb icon does not appear and displays as ice orb instead when opened from a
> powerbox" / "On Level 2 - Icebreath icon does not appear and shows as flamethrower icon"

**Both reports are one bug, and it is the three-art-stores trap for the FOURTH time.**

The world pickup branch asked `XART.rdy()` for a `micon_` key. `micon_*` lives in `BOFX.icons`.
That check is not the first-call race drop 0810f took it for — **it is permanently false**, so the
fallback ran for every weapon pickup on every frame of its life. Measured, all three stores side by
side:

```
micon_fireorb_3    -> BOFX.icons only
micon_icebreath_3  -> BOFX.icons only
ice_icon_3         -> XART
firewall_icon_3    -> XART
pw_iceorb_3        -> IN NO STORE AT ALL
```

Underneath that check sat three more element tables, each contradicting the one above it:

| where | what it did |
|---|---|
| `weaponIconKey` | **correct** — fixed in 0806d, returns `micon_fireorb_*` / `micon_icebreath_*` |
| fallback #1 | slot 4 substituted `firewall_icon_` with **no Freezer check** → ice breath drew the FLAMETHROWER. Mike's item 2, exactly |
| fallback #2 | 0810f correctly stopped slot 5 substituting on stage 3 — and it then fell through to… |
| the ASSETS map | …a third table hard-coding `5:'iceorb'`, `4:'firewall'` |

And the part neither report named: **slots 0, 1 and 2 have no legacy `*_icon_` family at all**, so
an MG, spread or missile pickup has never once drawn an icon in its life. It draws a plain coloured
capsule. That is the "does not appear" half of both of Mike's sentences, and it was never
slot-specific.

**Fixed by asking `iconBlit` first** — the one lookup that knows all three stores, built in 0810s
for the EQUIPPED box for this exact reason. `weaponIconKey`'s element rules are now the only
element rules in the path. `weaponLegacyName()` replaces the ASSETS map and returns **null** where
the legacy set has no art for the element the slot actually dispenses, so a pickup can look plain
for a frame but can never advertise the wrong weapon.

Verified by **observing the real draw**, not by asking the resolver — that is what made the two
previous fixes look complete:

```
L3 fireball  (slot 5, orbIsFire)   iconBlit micon_fireorb_3    <= DREW
L2 ice breath(slot 4, Freezer)     iconBlit micon_icebreath_3  <= DREW
L1 ice orb   (slot 5, control)     iconBlit micon_iceorb_3     <= DREW
```

No legacy key is queried at all any more. `_BUILD_SOURCE/probe_pickicon.py`.

⚠ **CLAUDE.md's own line "the world pickups already use iconDraw correctly" was wrong**, and it is
why this path was never re-checked after 0810r. Corrected there.

---

## 2. Decker's shotgun box had no draw branch (item 7)

> "Deckers Shotgun icon and powerup has not appeared for me yet, so I dont know if this is working
> or not."

It **is** wired — `dkPickKind()` rolls `dkshotbox` 50/50 for Decker and the collect switch has a
`case 'dkshotbox': dkGrant()`. Only the **draw** was missing. Its two siblings `sonicbox` and
`lzmgbox` have a branch; `dkshotbox` fell past them to the generic capsule with nothing on it. It
has been grantable and unrecognisable at the same time, which is exactly why he cannot tell.

⚠ **There is no authored icon for it.** The manifest has `nsw_icon_cole` and `nsw_icon_lizzie` and
no Decker entry. Candidates were rendered before choosing, per rule 1 —
`docs/proofs/decker_shotbox_candidates_0811m.png`:

- `ndk_shot_0..3` are the blast seen head-on: a glowing orange emitter that **reads as a fireball
  pickup**, which is the last thing this box should be confused with.
- `ndk_shell_0` is a brass shotgun shell — an object, not an effect, unmistakably ammunition.

`ndk_shell_0` is in, and the branch tries `nsw_icon_decker` first so a real icon drops straight in
the moment Mike supplies one. **His call whether the shell is what he wants.**

---

## 3. The level-1 dialogue window (item 8)

> "they must remain in the bottom left corner and never scroll away, and need to use OUR dialogue
> window graphics, and our fonts. again, scale and fit the text inside the window."

Every part of that was wrong, and the two branches were wrong differently:

- the **safe** panel was a `fillRect` plus a `strokeRect` — a faux box, against this project's own
  standing rule, with `dlg_window` sitting unused two functions away;
- the **combat** branch — which is the one that plays on stage 1's opening, so it is the one Mike
  is describing — was a bare translucent strip with no panel at all, bottom-CENTRE, in canvas
  BOFmil;
- both measured with `ctx.measureText` against a font they were not drawing in.

Now one panel for both: **bottom left**, `dlg_window`, every glyph in the BOF face, body wrapped to
the panel's inner width. Proof: `docs/proofs/dialogwindow_0811m_{a,b}.png`.

⚠ **"Never scroll away" is about the CAMERA, not a timer.** `drawWorld` runs under
`translate(-camX)`; anything drawn inside it slides with the terrain. The panel undoes that
translate and draws in screen space. This is the same world-vs-screen fault the file already
records three times — the launch seam, the outbound routes, and the level-1 opening ship.

### The line-breaker the handoff has been owed for two drops

`stageText`/`msgText` had no measure and no wrap, which is why every authored-font surface used one
hand-counted line or fell back to canvas text. New, next to `msgText`:

- `msgMeasure(text,H)` — walks the **same** glyph selection `msgText` does, a1 with the a2 fallback,
  so a measurement can never disagree with the draw. Returns **0 when the sheet has not decoded**,
  and callers must read that as *unknown*, not *empty*.
- `msgWrap(text,maxW,H)` — greedy word wrap.
- `msgTextLeft(...)` — left-aligned; `msgText` only ever centred.
- `msgFitH(...)` — largest size that fits a width.

Measured: the BOF face is **missing no glyph** across A–Z, 0–9 and `! ? . , : ' -`.

⚠ **The first cut clipped overlong lines and it was wrong.** Rendered, it turned *"CIVILIAN
EVACUATION IS BLOCKED ON THREE SIDES."* into *"…ON THREE"* — the player loses the end of the
sentence. "Scale and fit" means fit. The body size now solves against the box: the largest height
whose wrap fits the rows available. One render caught it; no amount of reading would have.

---

## 4. The arcade pickup banner (item 9)

> "text that appears letter by letter and then flashes left to right in yellow/white color with an
> ! at the end and then slides and fades... Ex: - LVL 1 Machine Gun!"

Four beats in his order — **TYPE → SWEEP → HOLD → SLIDE OUT** — in the BOF face, screen space, on
every weapon, missile-level, special and loaned-weapon pickup. It replaces `floatText`, which drifts
a small tinted string up from the crate and reads as a damage number.
Proof: `docs/proofs/banner_0811m.png`, caught mid-sweep.

Three details that are load-bearing rather than styling:

- **the left edge is pinned from the FULL string.** Centring on what has been typed so far makes the
  whole line crawl sideways as it fills in.
- **it is drawn in screen space**, for the same reason as the dialogue panel.
- **the `!` is only appended if the face has the glyph** — an unmapped character renders as a blank
  advance, so a missing `!` would silently become a trailing gap, the same family as the pilot
  card's periods. It asks first. (It has one; the branch is insurance.)

### ⚠ THREE INSTRUMENTS IN A ROW SAID THIS WAS BROKEN, AND ALL THREE WERE WRONG

Worth keeping, because each failure mode is general:

1. **A source grep** of `updatePlay`/`drawWorld` for the call → "declared but never fired". The
   calls sit one level down, in `updateEffects` and `_drawEffectsInner`. **A source test cannot see
   a call chain.**
2. **A before/after frame diff** → ~963,000 changed pixels with the banner up, and ~969,000 after
   it expired. The stage scrolls; every pixel moves regardless. **A diff that large measures
   nothing.**
3. **A same-state double draw** (draw the identical tick with and without) → differed across the
   whole canvas, because the renderer reads `performance.now()` directly for clouds, water frames,
   scanline phase and muzzle timers. **Same-state isolation is not available in this renderer.**

The screenshot settled it in one look. That is rule 2 in its most literal form, and the probe now
says so in place of a number it cannot honestly produce.

---

## 5. ⚠ TWO SUITE ASSERTIONS ARE ORDER-DEPENDENT, AND ONE IS NEWLY IDENTIFIED

Run A of the suite showed 6 failures, run B showed 4, with **no code change between them**:

```
run A   4 standing  +  "every volley fired is 5-8 rounds (5, 4)"  +  "curveL bleeds LEFT (-48)"
run B   4 standing
```

`curveL` joins the flaky family the handoff already lists (§202, and the volley one). Attributed
rather than assumed — section 212's own fixture, seeded, separation off and on, three seeds:

```
seed 20260811  sep off  curveL dx=-177      seed 7  off -177      seed 99  off -177
seed 20260811  sep ON   curveL dx=-177      seed 7  ON  -177      seed 99  ON  -177
```

**-177 every time, against a threshold of -60.** The in-suite -48 is not reproducible in isolation
and is not separation. All three of these assertions run long play simulations and inherit globals
from earlier sections. They should be lifted into standalone probes; until then, **re-run before
blaming a change**, and read the assertion COUNT.

That run also re-confirms 0811l's banking channel: **`straight lean = 0/0` with separation ON**, in
all six arms.

---

## 6. NOT ATTEMPTED — what is known

- **Cinematics need to be wide/fullscreen** (item 3). Not started. This is structural: the
  cinematics draw at gameplay dimensions and Mike wants them letterboxed/scaled with content fitted
  inside boxes. It touches `drawLaunch`, `drawOpening`, `drawOutbound`, `drawCutscene` and the
  arcade intro plates. Worth doing as its own drop with `probe_arrival`/`probe_exit` re-run after,
  because those two measure frame-for-frame handoffs that any resize will move.
- **Enemies appearing out of thin air** (item 4, second half). The stacking half landed in 0811l
  (settled burial 50.3% → 20.0% on stage 1). The **pop-in** is handoff §2.3 and still open: the
  mirror formula is known and works, but a blanket lift breaks *"crawling tank NEVER leaves the
  drivable band"*, and excluding `ground/_tracked/_crawler/_sx` did not clear it — **finding which
  ground rig gets those flags outside its spawn case is the remaining work.**
- **Projectiles "appear wobbly"** (item 5). Not investigated. Needs Mike to say which projectile —
  there are enemy pellets (`mfx_`), missiles, and the volley layer, and "wobbly" could be a
  sub-pixel rounding issue in the draw or an authored spin.
- **Projectile variety / screen-filling patterns** (item 6). Not started, and it is the largest item
  on the list. Five boss patterns and the quad-laser's four lanes landed this for BOSSES in 0810s;
  **the ordinary enemy roster is still the stage-3 change only.** This is design work as much as
  code and deserves a brief from Mike on which stages get which shapes.

## 7. New tools

| tool | proves |
|---|---|
| `probe_pickicon.py` | which STORE holds each candidate key, and which key the real draw path chose |
| `probe_0811m.py` | scope, the BOF face's glyph coverage, wrap output, and the banner render |
