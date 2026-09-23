# Weapon previews, single combinations and Axel Megashield — 2026-09-23

Each weapon/element recipe is now one permanent combination. Repeating a recipe
returns `owned` without spending another combine; the Armory no longer sells
combination levels. Legacy forged levels normalize to one while existing purchase
receipts remain intact. Base weapon pickups still have their existing progression.

Forge, Armory and Loadout simulations show level one, independently of the equipped
level, overheat, active special or spaceship mode. They run the real weapon firing
and rendering functions. Orb breakup, laser mist splits, elemental bursts, particles
and impact art stay in preview-owned pools instead of leaking into the next stage.
The narrow preview camera keeps the weapon visible. Fire + Laser equips Firewhip;
its live sweeping attack uses authored fire laser art and now produces fire impact
bursts. Existing authored elemental orb, shard, lance, laser and mist art is reused.

Axel's special grants five shield charges. Remaining charges survive the 15-second
special timer and campaign save/load. The bubble reflects hostile moving rounds
and stationary projectile contacts toward an enemy, retaining their projectile art.
Reflected rounds damage enemies and bosses, with swept checks to avoid tunneling.
Continuous beam volumes remain damage hazards rather than reflectable rounds.
An impact spends one charge with a 350 ms grace window for simultaneous volleys.
The last charge removes the bubble. Co-op charges and damage attribution belong
to the reflecting pilot.

Eight shield animation frames were generated using SpriteCook GPT 2.5
(`gpt-image-2.5-sunburst`, 14 credits). They have a common anchor and scale, render
at 50% opacity and use brighter frames for deflection. Source, prompt, asset ID and
hashes are in `assets/game/axel_mega_shield_0923/`; the reproducible normalization
script is `_BUILD_SOURCE/build_mega_shield_0923.py`.

Verification:

- `node --check assets/game.js` passes.
- `_BUILD_SOURCE/probe_forge_megashield_0923.py` passes in real Chromium: all 90
  bare/element weapon previews fire level-one rounds without changing live run,
  pilot, special, impact, explosion or smoke state; one-time recipe migration;
  actual Forge menu with a level-eight equipped weapon; persistent five-charge
  shield, save/load, fast return damage, final-charge depletion and co-op ownership.
- Browser page and console errors: zero. Forge, preview gallery and shield
  screenshots were inspected under `_shots/forge_megashield_0923/`.
- Old tests expecting combination tier upgrades were replaced with checks for
  duplicate rejection, level-one migration and preserved historical receipts.
- Final full suite completes with 4,889 passing assertions and 81 failures
  (exit 1). Failure names match `_shots/muzzle_variants_verified_suite_0923.log`;
  there are no new failure names. Final log:
  `_shots/forge_megashield_suite_final_surface_0923.log`.

No commit or push requested or performed.
