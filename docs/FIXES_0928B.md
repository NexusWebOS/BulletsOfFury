# 0928b — wind bed, Hammer heal counter, Chromium activation, chaingun from Stage 6

Mike: *"When playing level 6, if I die or quit, the wind noise should stop. Stage 5 boss on furious ...
shooting the missile into his hammer didnt cause the animation and effect to stop the healing and bring
him to his stun state. Also, the chromium armor activate sequence was horrible and needs to be re-done.
We never get to switch machine-gun to chaingun, nor does my machine-gun default to chaingun anymore after
level 5 ... anchored chaingun attachments ... spin the barrels ... chaingun borrows the same elements from
machine gun upgrades, just make the bullets go faster and appear like .50 cals and stronger with their
own impact fx. Do not worry about generating or changing any graphics in this pass."*

No art was generated or edited. Suite section 376 (`test_fixes_0928b.cjs`, 21 assertions);
probes `probe_hammer_counter_0928.py`, `probe_chromium_activation_0928.py`, `probe_chaingun_0928.py`
(17/0), `measure_chaingun_mounts_0928.py`.

## 1. The Stage 6 wind

`amb_storm` (`reviewed_stage6_wind_loop.mp3`) is its own `<audio>` element started by `beginStage` and
stopped only by the next `ambStart` — so a game over, a quit to the title or a return to the map left it
blowing forever, and it ignored the volume sliders and mute. `ambTick()` in the main loop owns it now:
alive only while a Stage-6 run is on screen (play, pause, stage card, launch), back on when play resumes
after a continue, scaled by SFX × master, silent when muted, ducked while paused. Measured in Chromium:
plays in the stage, stops at game over, returns on continue, stops at the title.

## 2. The Hammer's heal counter (all difficulties)

Two faults, and both had to go for a missile to land:

* **The raised hammer sits inside the top of the body's 72 px hit circle** (measured: hammer y 107,
  body centre 256 on the heal pose). Anything fired upward entered the body circle first, so during the
  heal no round and no missile could reach the hammer from below. While the heal charges, rounds in the
  column under the hammer now pass the body and the hammer (±40 px) is the hit.
* **`retinaMissileDamage` cleared the module on an unguided impact**, so a missile whose impact target
  was the boss always landed on the body. It re-resolves the module at the missile's own impact point.

Then: any player missile into the hammer breaks the heal outright on every difficulty (ordinary rounds
still drain the core); on Furious the barrier wall lets missiles through while he heals and the break
plays the base burst + shake. Measured: unguided and Retina-locked, Normal / Hard / Furious — 6/6 break
to the stun, three consecutive runs.

## 3. The Chromium armor activation (Furious)

Before: 3.4 s of a separate sheet (a silver robot with a silver hammer that is not the boss) stepped at
four frames, then a pop to the real boss; the HP bar emptied and refilled; the caption sat in the HUD.
Now 2.1 s on the real boss: a brace ring, then the engine's own chromium treatment (`h.empowered` +
`empowerLevel`, the pixel-stepped core-out mask) spreads the armor from his chest reactor in silver,
sparks run over the plating, the grey armor gauge fills as it spreads, and it locks with a chrome ring,
a flash and shake. The HP bar never moves; the caption sits under him and lingers a second.
`fr27_chromium_actions` row 0 is no longer drawn.

## 4. The chaingun from Stage 6

Before: the Stage-5 unlock put the chaingun in your hands once; every death, stage start and space
exit resets to the machine gun, so it was gone at the first death and never came back.

* From Stage 6 on (once unlocked), **the MG slot is the chaingun**: one shared level (MG crates raise
  it), the MG's forged element and field infusions ride it, and a death drops you to it. Stage 5 and
  earlier keep the MG; Cole keeps his MG tiers 6–8 (the fusion-cannon line).
* **Rounds** leave two wing pods instead of the nose: alternating at L1–2, both at L3–4, both plus a
  centre round at L5; 15–17.5 px/frame (was 10.5–12.3), ×1.3 damage; drawn as the Hammer's own tracer
  (`arch_blaster_fx_4/5`) in brass (red-hot near overheat) with a stepped additive pass. Infused rounds
  keep the element's bullet art.
* **Impacts**: the Hammer's blaster starburst (`arch_blaster_fx_0–3`) in amber, on enemies, minibosses
  and bosses.
* **Pods**: the Hammer's gatling (`arch_blaster_gun_*`, 0–3 barrels turning, 4–5 red-hot) turned to point
  forward, on each pilot's measured wing row (`CHAINGUN_MOUNTS`), barrels spinning with the rev meter,
  a flash at each barrel, hidden through rolls, somersaults and the death spin. The nose flash is gone
  for these rounds. **`CHAINGUN_POD_KEY` is the one line to change when Mike's pod art arrives.**

A 0927 assertion pinned the chaingun's single nose flash; it now asserts the pods own the flash (the
0927 rule — one nose flash per volley, not one per lane — still holds for weapons 0–2).

## Mike's calls

* The switch is automatic (the Stage-5 unlock converts you; Stage 6+ is the chaingun). A manual MG ↔
  chaingun toggle would need a new binding and screen — say if you want one.
* Cole's MG tier 6+ exemption.
* The 5 s overheat lock-out is unchanged, and now applies to the default gun from Stage 6.
