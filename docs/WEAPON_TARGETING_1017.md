# Highway pressure, stationary generators and modular weapon locks — October 17

Mike requested more Stage 4 highway tanks on Hard/Furious, generators that stay
behind during the Sovereign's charge, and visible targeting attacks for the
Stage 1–3 minibosses and later modular encounters.

## Behavior

- Hard adds a native modular desert tank every 3.8 seconds during ordinary
  Stage 4 waves; Furious uses 2.6 seconds and Insanity 2.2 seconds. The added
  live-tank caps are five/seven/seven. Normal/Easy retain their existing plan.
  Placement requires the authored paved-road boundary at the center and both
  sides of the tank. Original waves and native tank guns/racks still operate.
  Reinforcements pause during boss/miniboss encounters and resume afterward.
- The Sovereign captures its four generator positions before charging or
  overflying. Their stations remain fixed while the moving hull's lightning
  tethers extend, and the detached art retains its ordinary scale. They rejoin
  normal positioning when the hull returns. Generators remain real shootable
  objectives; their existing shield reconstruction and damage routing remain.
  Player body contact now tests the hull and its mounted weapons separately
  from the shot-target router, so detached objectives cannot cause ram damage.
- The shared warning follows a selected living player, orbits the reticle, then
  commits its aim for the final 0.40 seconds with the native lock beeps. The
  warning uses the normal playfield FOV and existing authored reticle art.
- The Razorback launches a large animated sonic missile. It can turn for 1.35
  seconds at a bounded angular speed, then retains its heading. It can be shot
  down and uses the existing sonic impact animation/audio. Existing pressure
  waves keep their original interception rules. Hard's two tanks retain their
  individual identities and alternate the new launch.
- Magmaward fires sustained fire bullets from its surviving left/right turrets.
  Frostcruiser fires ice machine bullets and shootable ice missiles from its
  surviving guns/racks. The burst lasts 2.4 seconds, followed by recovery and a
  fresh warning. Those rounds retain their release heading. Their original
  encounter attacks, module HP and authored bodies remain in place. Gun bullets
  retain ordinary gun interception rules through the shared elemental adapter.
- Stage 7's Dredger and Sludge Emperor, Stage 8's Herald and ranged finale rigs,
  and Stage 9's Void Horizon/twin Sentinels/merged Tidal Sovereign use the same
  warning followed by a bounded supplemental salvo. Positions come from each
  encounter's current living emitters, including transformed finale rigs.
  The Null Knight keeps its native melee targeting. Hidden arrivals,
  transformations and destroyed weapons cancel the added channel.

Owner: `assets/targeting_1017.js`. Its one `assets/game.js` hook separates boss
body contact from projectile targeting. `index.html` loads the owner after the
Warden/Stage 3–4 encounter modules. Both loader cache keys are `targeting-1017`.
The pass reuses authored projectile/reticle/muzzle/effect banks; it adds no atlas,
palette, source-art or sprite-frame changes. The Warden helper entry fix remains.

## Verification

Final focused results: 96/96 in the working build and 96/96 in the exact
publishing candidate, with no page, console or missing-resource errors. The
existing Sovereign completion/Hammer regression passes 53/53 and Warden entry
safety passes 43/43. The required working-build suite reaches its final
`BUILD OK` summary with 8,742 passing assertions, zero failures and exit 0.
Both runtime syntax checks pass. Representative captures were inspected.

Run syntax checks and the required complete suite:

```powershell
node --check assets/game.js
node --check assets/targeting_1017.js
node _BUILD_SOURCE/test_fl.js
python _BUILD_SOURCE/probe_targeting_1017.py
python _BUILD_SOURCE/probe_boss_repairs_1016.py
```

The native probe exercises real Chromium, actual `updatePlay`, the native
damage/interception routes and the game's renderer. It measures highway
placement/scrolling, stationary shootable generators, unshielded player contact,
tracking/committed aim, finite missile guidance, real shoot-down feedback,
destroyed emitters, later rigs, actual damaged pixels and flash expiry. Reverting
only the body-contact hook reproduces the generator death in its control; the
moving hull still causes real damage with the repair enabled.

The optional `--candidate <directory>` mode serves explicitly prepared publishing
files over the same native game, allowing separate uncommitted changes to remain
in the workspace. Candidate runtime hashes and both native results are recorded
in `docs/qa/weapon_targeting_1017.json`. Captures/logs are under the ignored
`_shots/targeting_1017/` directory. Evidence covers controlled encounter fixtures;
it does not represent a full human campaign balance playthrough.
