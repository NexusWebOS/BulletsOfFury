# Pixel glow pass: the Stage 5 Chrome Hammer core, then every unit actually drawn on levels 1-9 (October 15-16)

Mike: *"pixel glow should occur instead of overlayed graphics like our stage 5 boss's middle core. I know the
game needs this enhancement in alot of places."*

## What was wrong

The Stage 5 boss (the Chrome Hammer Archmage, which `spawnBoss` swaps in for `xenoregent` on stage 5) had two
kinds of core light:

1. **A pasted sticker in the charge phase.** In `core_orbit`, `hammerBossDraw` blitted effect cell 6 from
   `arch_effects` (a white burst with sparks) straight over his chest at `b.y-9`. It has its own silhouette
   and its own pixel grid, and it hides the authored chest ring entirely (`_shots/pixel_glow_1015/core_orbit_old_new.png`,
   the 1st, 3rd and 5th tiles).
2. **A flat painted disc everywhere else.** Every body plate carries a bright authored core ring that never
   changes, so the core read as a decal rather than a light.

## What pixel glow is here

The light comes from the art's own lit pixels: the core ring, the panel lights, the hammer's energy. It spills
past them in hard steps of one to four pixels. There is no blur, no extra silhouette, and no smooth fade.
Brightness walks a fixed six-step ladder (`PXG_STEPS`: 0, .16, .32, .52, .74, .95) on the game clock, like a
16-bit palette cycle.

- **Baker** `_BUILD_SOURCE/pixel_glow_1015.py`. For each registered sheet or loose plate it writes two
  companions with the same size and layout into `assets/game/shared/combat/pixel_glow_1015/`:
  - `_glow`: every emissive pixel at about half its own colour (it is *added* light), plus three hard rings.
  - `_core`: only each pose's chest core, plus four rings.

  "Emissive" means bright and saturated within the sheet's light hue band, or near-white. The core is the lit
  cluster nearest a torso guess (pose ink centre, 30% down from its top). It is not the largest cluster: on
  several poses the largest is the hammer head. The enrage reel paints its ring in the same pale steel as the
  armour highlights, so colour cannot find it there; that reel searches a torso window instead (`core_window`).
  `--check` writes a contact sheet. Nothing is read from pixels at runtime, because file:// taints the canvas.
- **Runtime** `assets/pixel_glow_1015.js`, loaded after `stage34_assault_1014.js`. It adds one hook on
  `ctx.drawImage`: when a registered sheet lands while a driver is live, its companions are redrawn under
  `'lighter'` with the **same source and destination rectangles**, so the light cannot drift off its panels
  and no draw site had to change. Images are matched three ways:
  - a sheet by its unique pixel size;
  - a loose plate by the key `XART.get` was asked for (tagged on return);
  - a tinted per-frame canvas by a tag set in `hammerArchFrame`, which also carries the tint, so a blue-charge
    or red-rage pose gets an `xartPalette` recolour of its own light. A white hit-flash pose gets none.

  Outside a driver window the art draws exactly as before.
- **The Hammer driver** `pxgHammerDrive`:
  - Idle: the core breathes slowly on the low steps.
  - Charging (`core_orbit`, `mega_charge`, `spell`, `enrage`, ...): the core climbs to the top step and beats
    faster, and the panel lights follow.
  - A hit pushes both to the top step.
  - Death fades the light out with the body.

  The `core_orbit` chest paste is suppressed. The converging motes around him still draw.

**Superseded by part 1b below**: the hand-picked Hammer sheets (`arch_chaingun_break_enrage`, `arch_spell_raise`,
`arch_leap_strike_0922`) are gone. They were forms the fight never draws.

## Verified

`python _BUILD_SOURCE/probe_pixel_glow_1015.py`: **20/20** in real Chromium on the live index.html, zero
page/console errors.

- All 40 companions decode. No glow is drawn before the boss appears, or for a registered sheet drawn
  outside a driver window.
- In three live states (warn, leap, hammer) the same frame was rendered with the glow on and off. The glow
  brightened 3,300 to 5,600 px, never darkened any, and every changed pixel sits on the boss.
- The core climbs the ladder through `core_orbit` (.32 to .95), and the old chest paste is suppressed.

The before/after renders were inspected by eye. Two of them changed the design:

- The first bake pushed the core toward white and flooded the ring into a flat disc, which is the exact
  sticker look being removed. The companion now adds partial light.
- The first rage frame glowed red on a blue-tinted body. The tint now carries through.

Full suite: **8,700 passes, 0 errors**, final `FALVA/LIZZIE BUILD OK` banner, exit 0. The suite loads `game.js` plus a fixed set of layers and not this one, so it guards against side effects and the probe is the proof.

Captures are in `_shots/pixel_glow_1015/` (ignored). This is a visual pass on protected fixtures, not a
balance change. Damage, timing and collision are untouched.


## Part 1b: only the units and frames the game actually draws, levels 1-9 (October 16)

Mike: *"I dont know why your using these frames with the chaingun on his back or forms we havent used. but only
do this for enemies and frames were actually using please. Do a pass for levels 1-9."*

**Survey first.** `_BUILD_SOURCE/probe_glow_usage_1015.py STAGE DIFF` plays each stage in real Chromium. It runs
60 s of the stage's own waves, then its miniboss, then its boss, on Normal and on Furious. The player fires real
rounds under the target, so the fights advance through their damage states and phases. Every image drawn while
`drawEnemy`, `drawSubBoss` or `drawBoss` runs is recorded by the XART key it came from and the exact key-space
rectangle shown. That covers 18 runs, all nine bosses, with zero page errors.

The survey recorded 1,097 keys:
- **474 are effects** drawn in those windows (warning cones, alerts, gauges, explosions, debris, wakes, exhausts,
  shields, muzzles, projectiles, the Hammer's lightning and spiked ball). The `FX` pattern in the baker drops them
  by name; they are already light.
- **623 are unit art.** `export_glow_sources_1015.py` saves each one's exact pixels.
- After baking, **368 carry lights**: per stage 21 / 98 / 74 / 10 / 34 / 22 / 29 / 51 / 29.
- The other 255 get nothing: 244 have no lamp at all, and 11 are already mostly light (ice-crystal jets, water
  swirls, toxic canisters), where an extra wash would be a halo sticker.

On a sheet, light is only baked inside the rectangles the survey saw drawn. Unused frames on the same sheet stay
dark.

**Most units are drawn from derived canvases**, so the runtime follows them:
- crops cut into a module's own cache (`mr27Cell` for the Rime Wall, Iron Warden, Storm Sovereign and
  space carrier; `hammerArchFrame`);
- `xartPalette` recolours.

Every image XART hands out is tagged with its key, and an atlas cell is tagged with its own key rather than its
sheet's. Drawing a tagged image into another canvas tags that canvas with the key and source rectangle it came
from, through a `CanvasRenderingContext2D.prototype` wrap; offscreen contexts use the prototype, while the main
`ctx` has its own `drawImage`. A `'color'`/`'source-in'` fill over a tagged canvas records the tint. So a Storm
Sovereign part cut from `mr27_storm` and tinted blue lights the right part of the right frame, in blue. A white
hit-flash copy or a black camo pass takes no light.

**What counts as a light (baker).**
- Bright (v > .72) and saturated (s > .50), and at least .16 brighter than the mean of its surroundings.
- **Not the unit's own paint.** Hue bins holding more than 12% of its coloured pixels are armour, and a lamp in that
  hue must be far brighter. The first cut lit the tan desert buggies and the green camo tanks wholesale; the check
  sheet caught it.
- A white-hot pixel counts only as the centre of a coloured light, never as a glint on armour.
- Each cluster must be smaller than 2.5% of the frame, or it is a painted panel.

**Rings and storage scale with the draw size.**
- Each ring is one game pixel wide at the size the key is really drawn, measured by the survey.
- Each companion is stored pre-reduced to its draw size (`n`, box-reduced with premultiplied alpha). Full-size
  companions smooth-downscaled at runtime cost up to 7 ms a frame on the stage-2/7/8 boss sheets. Pre-reduced, the
  measured overhead is under 1 ms on every stage, and all companions total 3.0 MB.

**Drivers.**
- Ordinary units, minibosses and bosses: the lights hold a low step and breathe slowly, each unit on its own phase,
  so a formation never pulses in lockstep.
- A hit takes them to the top step, and a dying unit's light goes out with it.
- The Hammer keeps his own charge driver and chest-core companions.

**Verified.**
- `probe_pixel_glow_1015.py`: **23/23**. No unused Hammer form is registered, every stage 1-9 has registered art,
  ordinary stage-5 enemies glow, and every Hammer state brightens only (never darkens) and stays on the boss.
- `probe_glow_live_1015.py` renders the same live frame with the drivers on and off for stages 1-4 and 6-9:
  - Lights brighten 4,000-11,000 px a frame on stages that have units on screen. The stage 4 and stage 6 frames
    had no lit units on screen, so they drew no glow.
  - Darker pixels appear only where the stage animates on its own clock (stage 1's water band, stage 3). A second
    glow-off render shows the same differences.
- Per-stage contact sheets (source | source + glow, one tile per drawn frame) were inspected:
  `_shots/glow_usage_1015/check_stage1..9.png`.
- Full suite: see CLAUDE.md.

To refresh after art changes:
1. Run the survey for every stage, Normal and Furious.
2. `pixel_glow_1015.py --survey`
3. `export_glow_sources_1015.py`
4. `pixel_glow_1015.py --check`

## Next places for this pass (measured, not yet converted)

- **230** non-zero `ctx.shadowBlur` sites in game.js. Each is a Gaussian halo around a sprite, which is the
  same sticker class and also the measured frame cost (0916ab). The highest-value conversions are hull and
  core glows on bosses, not bullets.
- **23** `createRadialGradient` discs painted over art. The boss and miniboss ones:
  - `razorbackDraw` (19857): the Sonic Hammer charge disc on the muzzle.
  - `fztCharge` (21730): the Furnace Tyrant's charge disc.
  - `drawS7PortalSeal` (75259).
  - `drawShield` (41918).
- Other bosses with an authored core that could breathe the same way: the Furnace Tyrant reactor, the Stage 4
  Storm Sovereign core, Dracodia's core, the Xeno Regent.

To convert one: add a `SHEETS` row to the baker (hue band, grid or loose frames), run it, then give the owner a
driver by wrapping its draw the way `hammerBossDraw` is wrapped here.
