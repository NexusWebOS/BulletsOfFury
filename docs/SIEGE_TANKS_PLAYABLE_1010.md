# Playable Level 1 siege minibosses — October 10

Mike approved all three modular preview tanks for password encounters.

| Password | Encounter |
| --- | --- |
| `sonic` | Sonic Siege Tank |
| `ordos` | Deviator Missile Tank |
| `hark` | Devastator Assault Tank |

Enter a password, then choose difficulty and pilot through the existing menus.
Each code starts its real Level 1 miniboss fight with the current jungle
terrain, miniboss music and HUD. The in-game pinned password catalog includes
each named encounter. Normal campaign Level 1 retains its existing Razorback.

## Combat

Sonic alternates pressure volleys, a charged pressure blast and sweeping
volleys. Its charged explosion preserves the approved raster footprint of
33% of the active playfield. A charge tell, the original targeting retina and
FOV warning announce the fixed target before release. The complete large bloom
stays inside the playable area.

Ordos staggers its emerald missile salvos, fans and lock volleys. Those missiles
can be shot down; intercepted explosions are harmless. Hark alternates heavy
plasma cannon streams and fans. Each tank scales timing and volley density
with difficulty, using the existing difficulty/threat/co-op HP budget. A short
recovery window separates attacks. Pressure and plasma shots follow the
existing non-interceptable energy-ordnance rule.

All eight modules remain separate: left/right tracks, hull, reactor,
left/right auxiliary pods, sensor and main weapon. Bullets, spread, laser
projectiles, held beams, missiles and area damage reduce actual encounter HP.
Retina locks follow individual live modules. Collision samples the decoded
authored PNG alpha, including gaps and destroyed pieces. Cached opaque lock
pixels avoid rescanning an entire module during every targeting getter.

Breaking the main weapon stops its attack book and leaves the auxiliary pods.
Breaking tracks reduces movement. Destroyed modules leave the lock list,
burn, drift and spin into authored explosions. Remaining pieces detach in
sequence on defeat. Modules never disappear through an opacity fade. Each
current animated silhouette flashes white on impact. The empty miniboss slot
and normal Level 1 progression resume after the final cookoff.

The fight reuses the reviewed pressure/charge/rocket cues and native impact,
module-break and explosion sounds.

## Ownership and rebuild

- `assets/siege_tanks_1010.js`: password routes, modular combat, precise hits,
  anchored tells, physical breakup and authored FX rendering.
- `assets/siege_tanks_art_1010.js`: generated shipping art registry/metrics.
- `assets/game/levels/stage_01/miniboss/siege_tanks_1010/`: 553 approved PNG
  cells in 58 banks and their manifest.
- `_BUILD_SOURCE/build_siege_tanks_1010.py --deploy`: reproduce normalized
  preview output and copy the approved cells into the production folder.
- `_ART_SOURCES/siege_tanks_1010/`: unmodified generated returns, prompts,
  registration corrections and provenance from the approved preview pass.

Production loads shipping PNGs, independently of the art-review page and source
folder. Each exported bank uses even frame dimensions, a fixed canvas/pivot
and one proportional scale under [the frame rules](FRAME_RESOLUTION_RULES.md).
No atlas cells were changed. The only monolith changes dispatch held-beam and
ship-contact collision to these modules; ordinary encounters use their prior
paths. `index.html` loads the owned extension after the current HUD runtime.

## Verification

The full regression suite and native Chromium password/difficulty probes are
recorded in [the portable QA report](qa/siege_passwords_1010.json).
The encounters were subsequently combined with GitHub commit `7539951`;
see [the merge record](MERGE_7539951_1010.md). The incoming ice/fire orb code
also damages these live modules, and the probes copy the current split HUD.

Native probes use `_BUILD_SOURCE/shoot.py` to load the actual production
entry point and draw through the game's own canvas. They check typed password
entry, real projectile/held-beam/missile damage, current-frame white hits,
live attack books, breakup, defeat, all four difficulties and ship damage.
Representative screenshots are under `_shots/siege_passwords_1010/`.

Protected observation fixtures prove attack scheduling and rendering; they do
not establish complete human clears or final difficulty balance. Separate
unprotected ship-shield checks verify that damage fields and physical contact
actually hurt the player and empty sprite gaps do not.

The original preview remains available at
`docs/previews/siege_tanks_1010/index.html`, with its independent art controls.
This integration is local; no commit or push was requested.
