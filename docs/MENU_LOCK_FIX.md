# THE "MENU 0" LOCK — root cause and permanent fix (drop 0801n)

    verify 130 passed / 0 failed

Mike: *"the menu is still at 0 and I cant move the menu ... this is a nightmare and repeating
problem that appears only after we go for these two changes."* And he pointed at the chase and
the vertical-scroll transition, which is where the last one came from.

## Why it keeps coming back

    a real canvas THROWS on drawImage(null):
      "The provided value is not of type '(CSSImageValue or HTMLImageElement or ...)'"

    loop() catches it -> nothing crashes, nothing appears on screen

    BUT menu input is handled INSIDE the draw. handleTitleInput() is the LAST line of drawTitle.

    So a throw ANYWHERE above it renders the menu and never reaches the input.
    Result: a menu you can see, that will not move. Exactly "menu 0".

This has been patched twice already — once by making `XART.get` return a 1x1 blank, once by
guarding three `.parts` lookups. It keeps returning because **there are 377 drawImage call sites**
and any one of them reaching a null re-arms it. Patching them individually is precisely why this
is a repeating problem rather than a fixed one.

## Two fixes, both structural

**1. The guard goes on the CONTEXT, once.**

`ctx.drawImage` is wrapped at creation. A null, undefined or undecoded source now draws nothing
instead of throwing. All 377 sites are covered at once — including every site written after this,
and including whichever one the transition work was actually hitting. It logs the first offender
per key under `DBG.verbose`, so a genuinely missing asset is still visible; the goal is to stop it
killing the FRAME, not to hide that it happened.

**2. Menu input no longer depends on the draw surviving.**

The title state services its input FIRST, outside the draw's try block. Even if the draw dies
completely, the menu still moves and the player can always leave. Calling it twice in a frame is
harmless — `Input.tap` is edge-triggered and already consumed.

The drawImage guard removes the usual cause. This removes the *dependency*, so a future throw in
any menu draw cannot strand the player again.

## Proven, not asserted

The harness now reproduces the lock and shows it closed:

    ok  ctx.drawImage is wrapped at the context, so all 377 call sites are covered at once
    ok  drawImage(null) draws nothing instead of throwing
    ok  a null draw mid-frame no longer stops the frame reaching handleTitleInput
    ok  the loop still catches genuine errors
    ok  the title menu services input BEFORE the draw, outside its try block

## The harness could never have caught this

Its canvas stub returned quietly on a null source. A real canvas throws. That stub is now STRICT
and throws the same way, which is what let the reproduction above be written at all.

---

# ROUND 2 — what the screenshot actually showed (drop 0801p)

    state title   kd25 ku26 md7 mm58
    last shift    at 429,160
    menu 0        PHOTOGRAPH THIS

## The probe was never gated on DBG.probe

You asked twice to have your screen back, and it kept coming up. The condition is:

    if(typeof window!=='undefined' && window.__inp && typeof ctx!=='undefined'){

`window.__inp` is set unconditionally when input is initialised, so it is ALWAYS truthy. Setting
`DBG.probe = false` never did anything. Now gated properly, and asserted.

## What the readout tells us

    kd25 ku26   keys ARE arriving — 25 down, 26 up
    last shift  with no "!" suffix, which the probe appends when a key fails to register.
                So the last key was SHIFT and it registered correctly.
    md7 mm58    the mouse is working too

So input reaches the game. The failure is downstream of input, in whether the cursor code runs.

## The menu had a single point of failure

The real `handleTitleInput` lives in `patches.js`, not `gamecode.js` — and it read RAW KEYS only:

    Input.down('arrowdown') || Input.down('s')

`Input.menuDown()` / `menuUp()` already existed and respect the user's KEYBINDS plus gamepad
d-pad and stick, but the title never used them. One route, no fallback: if a raw key stops
registering for any reason, the cursor is dead and there is nothing else to try.

Both routes are wired now. Losing one cannot strand the player.

There is also a note already in that file from a previous round of this same bug:

    "{"down":[]} passed straight through and menuDown() returned false forever."

An empty keybind array is truthy, so a corrupted bind file silently disables that direction — which
is worth remembering as a separate way this can present.

## Standing now

    1. ctx.drawImage is guarded at the context — a null source cannot kill a frame (377 sites)
    2. title input runs BEFORE the draw, outside its try block
    3. the cursor has two independent input routes
    4. the probe actually turns off

If it still locks after this, the cause is none of the above and that is genuinely useful — the
three most likely mechanisms are now closed and instrumented.

---

# THE DIFF AGAINST THE WORKING BUILD (drop 0801q)

Mike: *"Compare the old build that worked to the new build to find out whats breaking it."* That
was the right call — it found something none of my reasoning had.

## Method

Booted BOTH builds headless in a sandbox with a REAL-behaving canvas (throws on drawImage(null),
like a browser). Then diffed function by function.

    drawTitle          IDENTICAL
    chooseTitle        IDENTICAL
    handleTitleInput   differs — my additive keybind route only
    loop               differs — my additive guards only
    both builds boot, schedule rAF, and expose every function

So the CODE was not the difference. That pointed at data, which is where it was.

## What was actually broken

    window.BOF   old build: 39 paths, 0 missing
                 new build: 29 paths, 26 MISSING

The levels reorganisation moved files that the `BOF` namespace still pointed at — `mapJungle`
above all, which is stage 1's background. `BOFX` was repaired at the time because I checked it;
`BOF` was never checked, because I had been treating it as legacy.

**And the stage font atlases were gone entirely:**

    assets/atlases/stagefont1.png .. stagefont8_v5.png     8 files
    assets/atlases/stage1.png .. stage5.png                5 files

Present in the working build, absent here. Restored from it.

Final state across every namespace: **6850 paths, 0 missing.** That is now asserted, walking
arrays and nested objects rather than just top-level values — the first version of that assertion
missed the list entries and reported a false pass.

## Why this mattered more than the code

A missing image is not a crash. `new Image().src = <404>` fires an error event, `naturalWidth`
stays 0, and every guarded draw simply skips. But anything that reached an UNGUARDED draw threw,
and — before the context guard went in — that killed the frame at that line. Which is the "menu
renders but will not move" symptom exactly.

So the three fixes stack, and all three were needed:

    1. ctx.drawImage guarded at the context   nothing can throw there again
    2. title input runs outside the draw      a broken draw cannot strand the player
    3. the missing files are back             there is nothing broken to draw
