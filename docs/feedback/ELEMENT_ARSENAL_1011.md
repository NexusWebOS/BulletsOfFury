# Nine player weapon families — October 11, 2026

Mike requested a complete family of Fire, Sonic, Lightning, Water, Ice,
Chromium, Toxic, Dark Matter and Wind weapons and projectiles.

The pass is implemented locally. Open
`docs/previews/element_arsenal_1011/index.html` through the game server for the
interactive review. It uses the actual game's Forge preview and authored icons,
with all 81 combinations, weapon pickup levels I/III/V, 16-frame ammunition
scrubbing, onion skin and native collision screenshots.

## Family behavior

| Family | Reward | Main job |
| --- | --- | --- |
| Fire | Stage 2 | Burning damage, magma blasts |
| Sonic | Stage 1 | Pressure damage and ordinary-enemy knockback |
| Lightning | Stage 4 | Arcs between nearby targets |
| Water | Stage 9 | Soak, slow and lightning synergy |
| Ice | Stage 3 | Freeze buildup, piercing shards and shatter |
| Chromium | Stage 5 | Interceptable-shot reflection and beam immobilization |
| Toxic | Stage 7 | Poison and lingering plague-orb clouds |
| Dark Matter | Stage 8 | Formation pull, void beam and singularity orb |
| Wind | Stage 6 | Bounded push and slow, pressure and tornado projectiles |

Each has nine named Forge combinations: machine gun, spread, missiles, laser,
spray, orb, laser mist, chaingun and Yuri's sphere. Base weapon pickups still
have their normal progression. Each elemental combination remains a single
permanent recipe; the retired paid elemental tiers are not reintroduced.
Existing reward gates and saved ownership are preserved. Space weapons remain
their separate system. Maverick's homing lances remain Level I and uninfused;
his separately selected beam supports Forge combinations.

## Art

The later recording pass replaces the gold Sonic round art with sixteen
drawn pressure-wave poses and gives Blast Furnace sixteen distinct flame
poses with 22% more reach and contact matching its opaque silhouette.
Those two banks are owned by `build_playthrough_art_1011.py` and the late
`playthrough_1011.js` runtime. See `PLAYTHROUGH_1011.md` for the comparison,
provenance and fresh 81-combination verification. Other banks below remain.

Built-in image generation produced sixteen accepted source banks: sixteen
round drawings and sixteen missile drawings for each of the eight non-Wind
families, totaling 256 distinct exported poses. Wind keeps its existing nine
16-pose banks (144 drawings). The new rounds also paint spread, heavy slugs,
Yuri discharge bolts and matching non-fire/non-ice orb fragments.

The existing authored elemental beam, spray, orb and impact reels remain in
use; these are not claimed as newly generated 16-frame banks. Approved Fire
Whip, Thermoshock and pilot specials keep their owners. Toxic/water/metal/void
sprays and Yuri spheres now select their actual elemental plates. Old opaque
rectangular infusion auras are removed from these authored projectiles.

Accepted source images, exact prompts and registration records are in
`_ART_SOURCES/element_arsenal_1011/`. The first combined Fire layout and clipped
Sonic round layout were rejected; only their corrected banks ship.

Owning builder: `_BUILD_SOURCE/build_element_arsenal_1011.py`. It emits sixteen
512 × 512 RGBA atlases, each with sixteen equal 128 × 128 cells. Nose/casing
registration, a fixed physical pivot and one proportional scale per bank keep
the animated energy from moving the bullet body. Export bounds have clear
padding, all frame rectangles have even coordinates/dimensions, and all sixteen
frame pixel hashes in every bank differ. No synthetic pose interpolation.
The builder writes both the shipping manifest and
`assets/element_arsenal_art_1011.js` together.

## Gameplay repairs

- Stamp an element, element level and pilot on the shot at launch. A shot in
  flight keeps that identity after changing weapons or switching co-op seats.
- Both mist split generations, Yuri discharges, orb fragments and Chromium
  destruction splinters inherit their source's ownership and element.
- Automatic missiles consult their own missile recipe; a fire primary cannot
  turn unmodified secondary missiles into fire missiles.
- Each pilot owns a separate held beam/spray. Refreshes and muzzle anchors use
  the correct seat. Removing a held weapon's element clears its old damage type.
- Forged sprays apply their actual element instead of secretly burning targets.
- Sonic damage, elemental on-hit strength and dark-beam pull read the live
  projectile instead of the currently selected weapon. Mounted encounter bodies
  are excluded from Sonic/void positional pull.
- Orb blasts, clouds and reflected rounds preserve damage attribution to their
  originating pilot. Existing encounter collision/part routing is retained.

The late runtime owner is `assets/element_arsenal_1011.js`, after the Wind owner.
Core fixes are in `assets/game.js`, `assets/orbs_1010.js` and the existing
`assets/audio_wind_1010.js` wind-strength rider. Runtime state is `PA11`, avoiding
the previous enemy verification lab's `EA11` name.

## Verification

Authoritative current results are in `docs/qa/element_arsenal_1011.json`.

- Native Chromium collision matrix: all 81 combinations hit actual authored
  targets and carry the expected damage element. Eight non-fire sprays never
  add a fire burn. Weapon-switch, automatic missile, unforge, Maverick and co-op
  cases pass (32 checks total).
- Native Forge captures: 81 final views, real `XART.get` keys and game-context
  `drawImage`; no page, console or asset errors.
- Review page: all 81 element/weapon selectors, frame scrub/onion skin and
  mobile overflow checks pass (83 checks), no page/console/asset errors.
- Full regression suite and syntax results are recorded in the QA report.

The first native fixture accidentally tested Yuri's exclusive weapon as Cole
and left a Forge beam selected for Maverick. Those fixture setup errors were
corrected; no gameplay gating was loosened to satisfy them. These tests isolate
weapon behavior with protected, stationary targets. They are not human campaign
clears or a comparative weapon balance benchmark.

Local changes only. No commit or push was requested for this pass.
