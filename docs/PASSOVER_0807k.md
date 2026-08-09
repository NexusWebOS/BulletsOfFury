# PASSOVER — drop 0807k   (SMOKE RINGS ON HEAVY DEATHS, AND THE CLOUD LAYER)

Build: `BulletsOfFury_0807k`
Harness: **2,147 assertions / 197 sections / 0 failing**, twice, reaching the banner.

---

## 1. THE SMOKE RING

Mike: *"the smoke ring can be an additional ring graphic we use when tanks and the mini boss blows
up that expands out while animating and slowly rises in the air like real smoke and then fades
out."*

Three motions at once, which is what makes it read as smoke rather than as a sprite playing: the
reel animates through its eight frames, the ring **expands** to 2.15x as it goes, and it **rises**
about 33px in the first second. The fade is last and only on the tail — it holds at full opacity
through the first 55% and thins from there, so it dissipates instead of blinking off.

Measured: tank 1 ring, miniboss 1 ring, **jet 0, turret 0**. The ring marks a heavy death, so a
routine kill does not get one. Expires on its own and is cleared by a stage change.

⚠ **The fade is a deliberate exception to the no-fade-outs rule from 0806j.** That rule is about
UNITS — enemies, minibosses and bosses must not dissolve, they have death art for that. Smoke that
does not fade is not smoke. Written into the assertion so nobody "fixes" it later.

## 2. THE CLOUD

Mike: *"the other fog one is a cloud, a nice cloud you can actually use on levels 1 and 4. on
stage 3 and 6, palette swap to a more gray color."*

It shipped named `ground_fog_creep` and it is a cloud bank — 4518 colours, wide and low, and it
LOOPS, so it drifts continuously rather than playing once. Folded into the existing cloud layer
that already handles parallax, wrapping and drift:

    stages 1 and 4    its own blue
    stages 3 and 6    desaturated through xartTint — a palette swap, not a new asset
                      and not a canvas filter

## 3. ⚠ I COULD NOT FIND THE TWO CUT FRAMES

*"dont use these frames - those 2 got cut off."*

I tested for it two ways and both came back clean:

* **No frame touches its canvas edge.** All eight measure 0 ink on every border.
* **Every frame tapers.** A sliced cloud ends abruptly — its lowest row stays near full width.
  These run 13-23% of their widest row at the bottom, which is a natural taper on all eight.

So nothing is cut by any test I can run, and I would rather not guess and drop the wrong two.
`NSD_CLOUD_SKIP` is in place and empty; add the numbers and they are excluded everywhere at once.

`proof_0807k_cloud_frames.png` has all eight numbered, with the grey swap previewed underneath —
just say which two.

## 4. STILL OPEN FROM THE PLAYTHROUGH

Eight: stats screen · dialogue box art · liftoff music · L2 miniboss routing into lava · the tank
on the mountain · the runway plate · retiring the beach water · L2/L3 boss assembly spacing.
