# DROP 0813X — THE STAGE-2 FLOOR, AND THE SPAWN OFFSET THAT WAS MEASURED FROM A MOVING EDGE

Two reports from Mike, two fixes, both measured in pixels on this base.

---

# PART 1 — THE STAGE-2 BOSS ARENA OUTLIVED THE BOSS IT WAS BUILT FOR

> "During the final boss for the second level 'It's hot in here', the floor in the background
> disappears (probably falls behind the lava backdrop). This should not happen."

## 1. IT IS NOT BEHIND THE LAVA. IT IS NOT BEING DRAWN.

Mike's guess is one layer off, and the layer matters. `drawLevelMaster` builds the background in a
fixed order and has since 0801dp:

    base fill  ->  animated liquid bed  ->  the keyed master over it

The bed is drawn **underneath** the master, so anything keyed out of the terrain shows lava moving
below. Nothing can put the floor *behind* the lava — the lava is already behind the floor.

What actually happens is the master stops being drawn at all. `arenaLiquid` on stage 2 makes the
boss branch **return before the master blit**, leaving the bed that was always under there as the
only thing on screen. The floor does not fall anywhere; it leaves the frame.

## 2. THE FLAG WAS AUTHORED FOR A BOSS THAT IS NO LONGER IN THE GAME

0806f built this, and Mike's own words for *that* drop say who it was for:

> "we should be traveling past this mountain, flying over just lava that repeats, and **he appears
> and does his intro**."

That is the **MAGMA COLOSSUS**. He hauls himself up out of the lava — `genesisInit(b,'mbg2')`, four
hauls, limbs breaking a surface — so he needs an open liquid surface to break, and the mountain was
being drawn over it. Correct fix for that unit.

**0810q/0810s scrapped him.** Stage 2 fields the **INFERNO REAVER** now (`STAGES[1].boss`), a
gunship off the South-Facing Ships sheet that flies in and never touches the ground. The flag stayed
behind on the **stage**, so the terrain still vanishes for the whole fight and nothing replaces it.

⚠ **SAME SHAPE AS THE 0810m SPLIT LOGGED DIRECTLY ABOVE IT IN THE SOURCE** — one flag standing in
for a particular unit's requirement, left pointing at whatever unit arrives next. 0810m separated
`_bossRun` from `_realBossRun` because `arenaLiquid` was firing for the *miniboss*; the same block
was also firing for a *replacement boss* that never needed it, and that half went unseen because the
symptom is subtler: the miniboss case read as a teleport, this one only as an absence.

## 3. BOTH BEATS, NOT ONE OR THE OTHER

The first cut simply never dropped the master. That fixes the complaint and quietly throws away the
arrival Mike asked for in 0806f. His follow-up — *"anyway to have that floor render back in by
scrolling downward once the fight starts?"* — keeps both, and costs nothing:

    0.0 - 1.1s   open lava. The boss arrives over the corridor — 0806f's beat, untouched.
    1.1 - 2.7s   the terrain travels DOWN into frame, smoothstepped, entering at the top edge.
    2.7s on      the level, held exactly where _bossHold stopped the scroll.

**Downward is the level's own direction**, which is why it reads as the level catching up rather
than as a wipe. `srcY` DECREASES as a stage runs, so a master row travels DOWN the screen and new
terrain always enters at the TOP — the 0813c note at the windowed draw already spells this out.
Starting the plate one screen high and easing it to 0 delivers it the way the level would have.

`ARENA_FLOOR_HOLD` / `ARENA_FLOOR_IN` are the two dials, next to the clock at the top of the file.

⚠ **DELETING THE EARLY RETURN IS THE WRONG FIX.** The obvious edit drops stage 2 into `_loopDraw`,
which maps the master by `mapScroll % H` rather than by `scrollFrac` through `rangeSrc` — a
different mapping of the same plate. 0810m identified exactly that as the miniboss "teleport".
Swapping a floor that disappears for a floor that jumps is not a fix.

⚠ **THE PROPS HAD TO BE PUBLISHED THE SAME OFFSET.** 0813c fixed signs sliding against the ground by
giving the blit and the props ONE published mapping. An offset only the blit knew about would have
re-opened exactly that: `_masterSrcY` carries `srcY - _floorDy` now, and `drawLiquidFalls` takes the
same value.

⚠ **AND THE CLOCK IS ABOVE `spawnEnemy`.** Anything below its unclosed `if(base.art===undefined){`
is function-scoped and re-initialised on every spawn, so a clock declared there would restart the
slide every time a wave spawned.

## 4. MEASURED IN PIXELS — `_BUILD_SOURCE/probe_arenafloor_0813x.html`

Real game, real Chromium (headless Edge), driving `updatePlay`/`drawWorld` at a fixed `dt` so the
frame is a function of arena time and not of how fast the machine ran.

| arena t | `_masterSrcY` | what the frame contains |
|---|---|---|
| 1.0s | 0 (never set) | **periodic**, period 128px — the tiling lava bed, master not drawn |
| 1.5s | 4708 | terrain for the top **80px**, lava below |
| 1.9s | 4532 | terrain for the top **256px**, lava below |
| 2.3s | 4356 | terrain for the top **432px**, lava below |
| 3.5s | 4276 | no boundary — full terrain, settled |

Every figure is the smoothstep to the pixel (`p=0.25 → 80`, `0.5 → 256`, `0.75 → 432`), it is
**monotonic**, and it settles on 4276 — the held level position — so the ground that slides back in
is the ground the player was fighting over, not a jump elsewhere.

⚠ **THE PERIODIC PROFILE IS THE PART THAT PROVES THE HOLD.** A single mean cannot tell "lava bed"
from "terrain"; both are mid-brown on this stage and the two screenshots are hard to tell apart by
eye. The bed TILES, so it repeats every 128px and the master does not.

⚠ **MY EDGE DETECTOR WAS THE WRONG INSTRUMENT** and reported the same `edgeY` for every sample — the
largest row-to-row step in the frame is the HUD, not the terrain edge. The ROW PROFILE found it. A
single-number summary picks the loudest edge in the frame, not the one under test.

⚠ **THE BACKING STORE IS 2x** (`SS=2`, canvas 960x1024), so the probe's row indices are buffer rows,
half of them screen px. Read as screen rows every boundary doubles and still looks monotonic.

---

# PART 2 — THE SPAWN OFFSET WAS STATIC. THE THING IT WAS MEASURED FROM WAS NOT.

> "Some enemies look like they're teleporting into the map ... could the spawn offset be changing
> because the player is going left and right causing the screen to scroll? If this is the problem
> can we give the offset a static value?"

**Mike's hypothesis was right, and the mechanism is one step to the side of how he put it.**

## 5. THE OFFSET NEVER CHANGED. THE RUNWAY DID.

`offLeftX()` / `offRightX()` returned a **constant** — `-28` and `worldWidth()+28`. But they are
WORLD coordinates, and `drawWorld` renders under `translate(-camX)` with `camX` easing to follow the
player across `0 .. WORLD_W-VW`. So the number is fixed and the *edge it is measured from* slides.
What the player experiences is the **runway**: the gap between the spawn point and the visible edge.

Measured on stage 1, `_BUILD_SOURCE/probe_spawnoffset_0813x.html`, one unit per side, w=95:

| player | camX | left runway | right runway |
|---|---|---|---|
| HARD LEFT | 0 | **6px** | 326px |
| CENTRE | 160 | 166px | 166px |
| HARD RIGHT | 320 | 326px | **6px** |

**6px against 326px — a 54x swing from nothing but the player's x**, and it is always the side the
player is standing on that collapses. At 6px the unit is not entering; it is already at the edge
with no approach to be seen making.

⚠ **EVERY STAGE IS AFFECTED, NOT JUST 1/5/6.** Measured all eight: **worldW 800, camX 0..320, every
one.** The "wide stages are 1, 5 and 6" line in CLAUDE.md predates the stacked art pack (which made
every master 800) and is **stale** — it was true when written and quietly stopped being true, which
is why this was only ever chased on stage 1.

⚠ **THIS IS WHY EVERY POP-IN PROBE PASSED IT.** The camera window is a strict subset of the world,
so a unit outside the WORLD is always outside the CAMERA — nothing ever spawned on screen, and
`probe_popin`'s "is the box inside the play area" was correctly NO at 6px and at 326px alike. The
fault is the SIZE of the runway, not its sign, and only a screen-space measurement can see it.

## 6. STATIC — BUT AGAINST THE CAMERA, WHICH IS THE ONLY PLACE "STATIC" MEANS ANYTHING

`camLeftX()` / `camRightX()` give the camera window in world coords; the helpers anchor to those,
and `ENTRY_CLEAR` (64) is the guaranteed screen runway and the one number to tune.

| | camX 0 | camX 160 | camX 320 |
|---|---|---|---|
| left runway | 64 | 64 | 64 |
| right runway | 64 | 64 | 64 |

Verified at w=95 and w=29 — the guarantee is per-sprite, so a small unit and a large one both get
64px of screen to cross.

⚠ **THE FIRST CUT MEASURED −19px AND WAS WORSE THAN THE BUG.** Moving the helpers to the camera
while leaving the clamp's trigger on the WORLD edge: `offRightX()` becomes `camRight+28` = 508,
which is *inside* an 800 world, so a world-edge trigger never fired — and 28px of centre offset does
not clear a 95px sprite, so 19px of hull sat on screen at spawn. That is 0812k's "a side entry has
to clear the SPRITE, not just the world edge" arriving by a new route. **A half-migrated coordinate
system is worse than either whole one.**

⚠ **THE TRIGGER NEEDS BOTH HALVES.** Fire when the CENTRE is beyond the visible edge (the unit
declaring itself an entry rather than a placement) AND only while it lacks `ENTRY_CLEAR` of runway.
Drop the first and a mid-screen placement gets shoved; drop the second and a wave that authored a
long approach has it shortened.

⚠ **AND `inPlace` HAD TO BE MADE EXEMPT.** The old world-edge trigger could never reach a splitter's
halves or a surfacing maw because their x is in-world. A visible-edge trigger can, so the 0811o
declaration has to be honoured explicitly now. Regression-guarded: mid-screen (240), off-camera
in-world (700) and `inPlace` at the visible edge (500) all come back **moved=0**.

## 7. WHAT PART 2 DOES NOT COVER

⚠ **A UNIT THAT DOES NOT MOVE HORIZONTALLY GAINS NOTHING FROM A LONGER RUNWAY.** Tracing a bare
`s1jetDelta` spawned at `offLeftX()`, the leading edge sat at −6px for all 24 frames — it descends
and never crosses. Waves pass route options this trace did not, so it is a probe limitation rather
than a finding, **but it means the fix helps side-ENTERING units and does nothing for a unit whose
route is vertical.** If pop-ins persist, that is the next thread to pull.

⚠ **THE EDGE PIN AT `_edgeM = w*0.66` IS UNTOUCHED AND IS A SEPARATE SUSPECT** (0811o/0811t). It did
not fire in any trace here because the traced unit never moved into `_inField`. The two look
identical from a single frame and are told apart by a per-frame trace: a smooth ramp is the runway,
a discontinuity is the pin.

⚠ **DETERMINISM TRADE, AND IT IS MIKE'S TO OVERRULE.** Spawn x is now camera-dependent, so a wave no
longer replays at identical WORLD coordinates — it replays identically in SCREEN terms instead,
which is what the player perceives and what the complaint was about. The determinism rule
(`_volSeed` from spawn position, never `Math.random`) is about reproducibility, and that is intact:
same player position, same spawn, every time. Nothing was made random.

---

# 8. ⚠ HOW THIS DROP WAS BUILT, AND A NEAR-MISS WORTH KEEPING

**This work was originally written against an 0813g zip while trunk was already at 0813w** — sixteen
drops ahead. The six edited files were nearly handed over for a direct copy, which would have erased
`0813h` through `0813w` wholesale. It is the "two divergent trees" warning in CLAUDE.md happening
again, and the tell was cheap: `git ls-remote` showed a branch, and one `git log -1` showed a commit
from the same afternoon.

⚠ **CHECK THE REMOTE'S HEAD BEFORE WRITING A LINE, NOT BEFORE PUSHING.** The cost of checking is one
command; the cost of not checking is discovering it after the work is shaped against the wrong base.

⚠ **AND THE DROP LETTERS COLLIDED.** The first pass labelled itself 0813h/i/j — all three already
existed on trunk as entirely different changes. Renumbered to 0813x, which is free. A drop letter is
not a private namespace.

⚠ **THE FIXES RE-APPLIED CLEANLY BECAUSE ALL FIVE ANCHORS WERE BYTE-IDENTICAL ON 0813w** — verified
before editing, not assumed. Both bugs were still live on trunk (`if(cfg.arenaLiquid && frames)
return true;`, `offRightX` → `worldWidth()+28`, the `w/2 + 6` clamp) and none of the new identifiers
(`_arenaFloorT`, `ENTRY_CLEAR`, `camLeftX`) existed there, so nothing was duplicated or superseded.

## 9. ⚠ VERIFICATION: NO `node` ON THAT MACHINE — HEADLESS EDGE INSTEAD

`node`, a real `python` and a driveable Chrome were all absent, so `node --check`, `test_fl.js` and
`shoot.py` could not run. **Headless Edge does both jobs** and was used for both.

    msedge.exe --headless=new --disable-gpu --allow-file-access-from-files
      --user-data-dir=%TEMP%\edge-probe --virtual-time-budget=40000 --dump-dom <file:// url>

⚠ **`& msedge --dump-dom` RETURNS NOTHING through PowerShell** — redirect via `Start-Process
-RedirectStandardOutput -Wait -NoNewWindow`, or every run reads empty and looks like headless being
unavailable.
⚠ **`--allow-file-access-from-files` IS LOAD-BEARING TWICE** — the XHR that reads a source file for
the parse check, AND `getImageData` on a canvas that is otherwise taint-blocked on `file://`.
⚠ **`node --check` STAND-IN: `new Function(src)`** — parses without executing, so runtime errors
from a missing manifest/canvas do not drown the syntax signal. **Make it fail first**: feed it
known-broken source and require a `SyntaxError` before believing any OK.
⚠ **A PROBE HTML CAN LIVE IN `_BUILD_SOURCE`** with `<base href="../">` — every relative asset URL,
including the ones XART fetches lazily, then resolves against the project root.

**`assets/game.js` and `_BUILD_SOURCE/test_fl.js` both PARSE OK on this base.**

⚠ **THE SUITE WAS NOT RUN.** `test_fl.js` is a node script and there is no node on that machine. It
is untouched by this drop, so nothing in it should have moved — but that is an argument, not a run.
**Run it before trusting the count**, and expect the 0806f-era §180 assertions
(`if(cfg.arenaLiquid && frames) return true;` matched verbatim as source text) to FAIL: they pin the
exact line Part 1 replaces. Read them before fixing them — they are protecting 0806f's behaviour,
which is being NARROWED, not removed, and they ask the TABLE whether the stage declares the flag
when the thing that changed is which BOSS the stage fields.
