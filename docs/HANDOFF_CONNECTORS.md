# Handoff — the seamless entry connectors, boss HUD, and the 0810h bug list

**Read `CLAUDE.md` first, then this.** Suite at HEAD: **2,441 assertions / 218 sections / 5
failures**, all five pre-existing. Tree clean, 29 commits since `d67dbbf`.

---

## Mike's brief, verbatim, 0810i

> "check all stage transitions, stage 1's start is horrible, stage 6's is broken and horrible, and
> even all stages basically have you fly over a flat and then pull the flat away and hover you over
> the level into it. I wanted you to make connecting sections of these animated flats like another
> 800x2000 flat or something that directly connects to beginning of our levels so it's seamless.
> The miniboss on level 2, broken. The hud and fills, remove and make your own please for all
> bosses and mini bosses. Mini boss 1 doesnt flash white when you attack his body after shield is
> down. Level 2 boss cuts to the lava instead of a connecting section at the end of the level and
> another one to lead us to the cinematic that we can scroll infinitely and make it look and not
> break the game at all. this is extremly important"

---

## 1. THE ENTRY CONNECTOR — the main ask

### The mechanism is already built and proven. Do not reinvent it.

`openingDrawArrival` (drop 0810e) does exactly what he is describing, for stage 1 only:

- the ocean flat tiles beneath, scrolling
- the level's **own first frame** descends into place over it
- at the end of the beat `dy` is 0 and the frame is **byte-identical** to PLAY's first tick

Measured by `_BUILD_SOURCE/probe_arrival.py`: **0 differing pixels out of 393,600**.

It works because it calls `drawBG(0)` under a translate rather than reimplementing the master blit.
That is the load-bearing decision — PLAY's first frame is *whatever drawBG paints*, so calling the
same function makes "last cinematic frame IS first play frame" structurally true instead of a claim
to re-verify. **Any generalisation must keep that property.**

### What is still wrong, and it is what he is describing

Stages 2–9 do not use it. They run `GS.INTRO` → `GS.LAUNCH`, and `drawLaunch` is the
"fly over a flat, pull the flat away, hover into the level" he is complaining about:

```
SEG_B1=2000, SEG_B2=4200, SEG_B3=13000     runway | terrain | liquid | level(entrance)
```

`_drawLevelRegion` clips the real level into a window that opens as `dist` grows, so the level
*appears through a hole* that widens. That is the "pull the flat away" — the runway is a separate
plate that ends, and the level is revealed behind it rather than joined to it.

### The build

Per stage, an **800×2000 connector** made from that stage's animated flat, butted directly onto the
level's first frame:

| stage | flat | source |
|---|---|---|
| 1 | Water | `tflat_water` / `Animated_Liquids/Water` |
| 2 | Lava | `tflat_lava` / `Lava` |
| 3 | Ice | `tflat_ice` / `Ice` |
| 4 | concrete/road | `tflat_concrete`, `tflat_road` |
| 5, 8 | space — no flat | `TRANS_FLAT.space` is deliberately null; use `cfg.fill` |
| 6 | sky — no flat | `TRANS_FLAT.sky` is null. ⚠ `tflat_sky` is the ORBITAL starfield; using it as a daytime sky was a documented mistake, do not repeat it |
| 7 | Sludge / Sewage | `tflat_metal`, `Sludge` |
| 9 | Water | `Water` |

Source art: `_ART_SOURCES/ColeForge_BOF_Rebuilt_Stages_RC2_SALVAGED/.../Animated_Liquids` — five
families (Ice, Lava, Sewage, Sludge, Water), each a `1024x128` row = 8 frames of 128×128, with
per-family JSON. The in-game `tflat_*` keys already exist and `TRANS_FLAT` maps terrain→flat.

**Recommended shape**, because it reuses what is proven:

1. Lift `openingDrawArrival` into a stage-agnostic `entryConnectorDraw(stage, prog)`, taking the
   flat from a per-stage table and keeping the `drawBG(0)` + translate core untouched.
2. Give `drawLaunch` a terminal beat that hands to it, or replace the LAUNCH entry for stages 2–9
   with the OPENING path parameterised per stage. The second is cleaner and kills the whole
   "reveal through a widening hole" mechanism rather than dressing it.
3. `probe_arrival.py` already measures the join. Point it at each stage; the bar is 0%.

⚠ **`drawLaunch` also owns the 3-2-1 and `playShipPose`.** The seam fix from 0810a lives there —
one pose read by both sides. Whatever replaces the entry must keep that, or the +160/+92/+14 jump
comes straight back.

---

## 2. STAGE 2's EXIT — connector out, then an infinite scroll

> "Level 2 boss cuts to the lava instead of a connecting section at the end of the level and
> another one to lead us to the cinematic that we can scroll infinitely"

Two pieces, and the second is the unusual one: a section that scrolls **infinitely** while the
cinematic plays, so the handoff is never waiting on terrain running out.

The outbound already has the pattern — `outboundDrawWater` / `outboundDrawLavaIce` /
`outboundDrawSkyTown` each tile a flat and wash one over another. Infinite scroll is what
`_loopDraw` in `drawLevelMaster` does (`sY` wraps modulo the image height). Combine: the connector
tiles seamlessly and never terminates, and the cinematic ends on its own clock rather than on the
plate.

⚠ The routes must keep the standing rule: **the player is HELD** and the world moves under them.
"follow the player. do not fly them off in the distance" is treated as a rule for every end
transition, and suite section 133b asserts 0 frames of player movement across 2→3 and 3→4.

---

## 3. BOSS + MINIBOSS HUD — remove and replace

> "The hud and fills, remove and make your own please for all bosses and mini bosses."

Current art: `nbb_*` (boss) and `nmb_*` (miniboss) fills — **168 registered keys, 8 fills per stage
for both**. Drawn by `drawHealthBarV2`.

⚠ **`drawHUDCustom` returns early and only `drawHUDCustomImg` draws the boss gauge.** Documented in
0801ej: "calling it directly emits 3 nbb_ blits, calling drawHUD() emits none". Mike reported "no
fills showing up" once already and that was the cause. Whatever replaces this must be reachable
from the path that actually runs, and the way to prove it is to COUNT BLITS, not to read the code —
`probe_enemies.py` shows the technique (wrap `ctx.drawImage` for the duration of a call).

The bosses were being wired in another chat. **As of this drop that chat has not committed since
`73b3009`, ~29 commits back, so boss code is effectively unowned — but check `git log` first.**

---

## 4. The two smaller ones

**Miniboss 1 does not flash white after its shield drops.** SUBBOSS[1] is the quadlaser. The
standing rule is that every enemy gets a white flash on hit. Check whether the body registers hits
at all once the shield is down, or whether it registers and the flash is not drawn — those are
different bugs and the second is the more likely, given the shield swallowed hits by design.

**Level 2 miniboss is broken.** SUBBOSS[2] is `obsidiandrill`, sectional and tracked. Not yet
diagnosed. `probe_enemies.py --stages 2` will say whether it spawns, whether it draws, and whether
it reaches the playfield, which separates three causes in one run.

---

## 5. Tools you have, and the traps they cover

| tool | proves |
|---|---|
| `probe_arrival.py` | the cinematic's last frame and PLAY's first are the same picture |
| `probe_seam.py` | ship/camera/terrain deltas across an intro→PLAY seam |
| `probe_enemies.py` | per-unit BLIT COUNT and SPAWN position — invisible vs vanished vs pop-in |
| `probe_weapons.py` | what `pShoot()` actually puts in `pBullets`, all nine pilots |
| `probe_palette.py` | a palette swap moves hue and holds luminance |

⚠ **A probe that recomputes the thing under test cannot find the bug.** `probe_seam.py` computed
the ship's x as `player.x - camX` and so asserted the fix it was meant to be testing — it called a
160px offset clean for two drops. Record what the game actually drew.

⚠ **`0 failures` can mean a crash.** When `arsenalMiniFor` was function-scoped, the suite reported
0 failures with the count down from 2,421 to 1,567. Read the COUNT.

⚠ **World coords drawn into screen space with no camera has now bitten FOUR times** — the launch
seam, the outbound routes, the opening's ship, and the stage-clear flyover. A source assertion
enforces it for the cinematics. Any new connector must draw through `translate(-camX)`.
