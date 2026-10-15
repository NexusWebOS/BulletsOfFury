# Pixel glow pass, part 1: the Stage 5 Chrome Hammer core (October 15)

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

Registered so far: `arch_orbital_sweep_0926` (his main strike/idle sheet), `arch_chaingun_break_enrage`,
`arch_leap_strike_0922`, `arch_spell_raise`, and the 16 `pt11_hammer_core_*` plates. That is 1.2 MB of
companions.

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
