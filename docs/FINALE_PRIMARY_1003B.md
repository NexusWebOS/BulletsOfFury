# October 3: late-stage chainguns and the eight-life finale

Mike's latest rule supersedes the old Cole exception: all nine pilots default
to anchored chainguns after Stage 5, regardless of password, campaign or save.
Machine guns are an explicit Loadout choice. Remaining sewer toxic pods use
selected mutants. Stage 8 now has the alien host followed by an alien version
of every Stage 1–7 boss, with independent lives and reset components.

## Build and preservation

- Working checkout remains `main` at `938d1079`, with the previously inspected
  Claude `d69cffa4` integration and local authored work preserved. No commit or
  push was made for this pass.
- `assets/game.js` remains LF; `_BUILD_SOURCE/test_fl.js` remains CRLF.
- New runtime layers load after Monster Mutator and before widescreen HUD:
  `primary_1003b.js`, `finale_art_1003b.js`, `finale_1003b.js`.
- Local play: `http://127.0.0.1:8794/index.html?build=d69cffa4-finale-1003b`.
- Native review: `_shots/finale_1003b/review.html`. The generated review includes
  actual game screenshots and a short host/knight motion recording.

## Primary weapon behavior

Stage 6–8 entry grants the run's chaingun progression flag even on a clean-profile
password start or an older save missing that flag. The bay changes from MG to
chaingun, the primary has at least tier 1, and the existing shared MG/chaingun
upgrade and Forge path remains in use. The existing authored per-pilot mounts,
barrels, projectiles, fire cadence and wing sockets are retained.

The Loadout weapon form selector exposes the other primary. It updates the bay,
held primary and crate pool, and saves optional `primary1003b: mg|chain` without
changing the save version. An old Stage 6–8 save without this field migrates to
chaingun. Deliberate MG choice survives save/load, respawn and stage advancement.
Unrelated held weapons are preserved. Space mode keeps its existing systems.
Both the opposite-primary icon and its preview use the selected weapon.

Stage 7 `s7canister` now dispatches Hexpyre and `s7mine` dispatches Imp Harrow.
Existing wave times/counts and the seven selected designs remain the source of
the roster. No unselected candidate was introduced.

## Finale

| Life | Identity | Inherited and upgraded attacks |
| --- | --- | --- |
| 1 | Orbital Host | Independently destructible arms, lunging talon sweeps, gravity well, paired code beams |
| 2 | Hive Helicopter | Sweeping MG streams, ground bomb Retinas, shootable guided missiles, gravity |
| 3 | Alien Furnace | Complete visible arms, shootable magma spread, eruption zones, charged beams, orbital ordnance |
| 4 | Cryo Hive | Rapid ice gun streams, twin charged lasers, orbiting ice and gravity |
| 5 | Storm Organism | Retina-targetable missiles, central charged lightning, committed ram, code beams |
| 6 | Null Knight | Full code-wall guard, jumping downcut/horizontal follow-up, alternate double-jump combo, teleport/reset |
| 7 | Void Harrier | Turbine pull, missile batteries, dual carrier laser lanes and gravity |
| 8 | Last Warden | Chaingun sweep, gravity stomp, charged scissors and code lanes |

All difficulties encounter these identities; HP, warning/recovery windows and
projectile speed scale. Furious has eight colored authored health housings,
filled sequentially during takeover. Their independent pools total 11,716 HP
(1,136 / 1,278 / 1,420 / 1,420 / 1,420 / 1,704 / 1,563 / 1,775).
The eight-row display also communicates progression on lower difficulties.
The authored fills are palette variants retaining their original luminance.

Only the explicitly requested host uses detached arm components. The five new
boss reels are whole authored plates; damage in a previous life cannot remove
their arms. Each life resets its own modules and clears owned hazards/locks.
The first seven defeats lead to a 1.65-second transformation plus a 1.1-second
reveal, with no rewards. The eighth uses the established final fall, portal,
sewer reunion and single stage-clear reward.

Gravity uses bounded continuous displacement, and ordinary hulls remain upright.
Targets commit during tells. Lasers reuse the alien/code FOV geometry for their
actual collisions. MG sweeps warn their firing region. Player evasion abilities
remain available; the knight has a longer final recovery and a two-second reset.
Projectile/effect counts are bounded. New MG attacks use the registered heavy
machine-gun audio; charging, impacts, beams and transitions invoke native cues.

## Authored art

Built-in image generation created five transparent 2x2, four-state reels:
Furnace, Cryo, Storm, Harrier and Warden. The Furnace reel deliberately includes
two complete articulated arms and claws in every frame. Sources remain in
`_ART_SOURCES/finale_1003b/`; generated sheets are copied unchanged by
`python _BUILD_SOURCE/build_finale_1003b.py`. The owning importer emits the asset
registration and equal-cell metadata together. Exact image-generation prompts and reference paths are recorded in
`_ART_SOURCES/finale_1003b/prompts.json`. Source SHA-256 hashes are in
`assets/game/finale_1003b/manifest.json`. No existing shared atlas was repacked.
Existing host components, helicopter/rotor, knight poses, FOV, code wall,
teleport, transformation and radial shield-shatter reels remain in use.

## Verification and limits

- `node --check assets/game.js`, `assets/primary_1003b.js`, and
  `assets/finale_1003b.js`: exit 0.
- `node _BUILD_SOURCE/test_fl.js`: **6,818 passing assertions**, exit 0, final
  `FALVA/LIZZIE BUILD OK, 0 ERRORS` banner reached. Previous baseline: 6,554.
- `_BUILD_SOURCE/probe_finale_1003b.py`: **99 native Chromium checks**, exit 0,
  zero page/console errors. Includes every pilot's real password entry, real
  chaingun projectiles, actual Loadout mouse handler, save/advance preference,
  all eight authored identities, every attack/recovery, native player-shot
  damage on every form, independent arm destruction, and full eight-life
  progression through the one final reward.
- Existing `_BUILD_SOURCE/probe_mutator_1003.py`: **76 native checks**, exit 0,
  no page/console errors; its expected Stage 7 roster count now includes the two
  replaced pod slots.
- `_BUILD_SOURCE/record_finale_1003b.py`: real canvas host/knight motion capture,
  zero page/console errors. Media stays in ignored `_shots/`.
- Pixel captures were inspected. The first stacked gauge obscured tall heads;
  housing spacing and resting silhouettes were adjusted and recaptured.
- Initial suite run exited 1 on a mismatched form-table identifier; fixed.
  Initial native run found an idle-position snap affecting collision and an art
  instrumentation miss. Idle movement now approaches its target continuously.
  Native draw instrumentation now starts before the rotation cache binds the
  game context's drawImage; it records logical XART keys, not canvas `.src`.
  Follow-up native and full-suite runs pass. A first sandboxed Chromium launch
  received WinError 5; the authorized native launch succeeds.

Portable native evidence: `docs/qa/finale_1003b.json`. These are controlled
fixtures, not a human campaign win or a claim of final difficulty balance.
