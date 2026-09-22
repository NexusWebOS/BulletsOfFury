# Stage 6: City in the Sky / Rebel route (20 September 2026)

The user-supplied BOF2 Ghost, Rift Phantom, and Ouroboros view sheets are visual
references. The current three-quarter plates are cropped from those authored
reference sheets, with the Phantom's bright purple accents shifted to steel.
The source sheets have not been changed. SpriteCook is now connected. GPT-2.5
Flare produced view, somersault, underside and charge/dash art for all three
hulls. Their stable asset IDs are in `docs/qa/stage6_rebel_spritecook_0920.json`;
the playable loose frames live in `assets/game/bosses/rebel_squad_0920/frames`.
The playable frames are turned 180 degrees from SpriteCook's upward-facing
views so the noses point downscreen toward the player and the exhaust trails
behind them. The renderer never falls back to the old upward-facing plates.

Mike specified **SpriteCook GPT-2.5** for those missing frames. Use the
project's recorded `gpt-image-2.5-flare` SpriteCook model; do not substitute
another image generator, a mirrored single-view plate, or a scripted rotation.
The plugin became available in the next Codex session and these assets were
generated on 20 September. The previous connection blocker is resolved.

### SpriteCook production brief and asset provenance

Use each original BOF2 source sheet as the identity reference, beginning with
its top-down view. Make one **three-quarter top-down master** per hull, then
use that master's `edit_asset_id` for every follow-up pose so the silhouette,
wing geometry, engine count, canopy, markings, and palette stay consistent.
`reference_asset_id` alone produces a lookalike, not an identity-preserving edit.
The three sources are:

| Rebel | Source sheet | Final accents |
| --- | --- | --- |
| Ghost | `ship_support_relay_ghost_views_hq.png` | purple |
| Rift Phantom | `ship_experimental_rift_phantom_views_hq.png` | black/steel with restrained purple lights |
| Ouroboros | `ship_experimental_ouroboros_views_hq.png` | teal |

For **each** hull, request transparent, individually separable 16-bit pixel-art
frames: idle/front; bank-left and bank-right at 25° and 50°; barrel roll in
eight successive poses; somersault in eight successive poses, including a
distinct underside and recovered top view; four charge-up frames with
increasing engine light but unchanged hull; and four directional dash frames
with visible, attached thrust. Front, sides, underside, and back must be
genuinely drawn. Keep a fixed pivot and canvas size, with no text, shadows,
background, extra ships, or motion blur baked into the hull. Generate separate
shield, teleport, and thrust effects so attack telegraphs can animate without
redrawing or obscuring the ship. Do not mirror frames that expose asymmetric
markings or hidden faces.

Normalize every returned plate with the existing SpriteCook normalizer before
registration: compare ink bounds and pivot, quantize to the source palette
without dither, inspect transparency and opaque-color count, and render the
whole reel in game at its actual draw size. Keep the existing cropped plates
until the complete reels pass visual inspection.

## Implemented

- [x] Shared authored-jet maneuver controller: committed corner dash facing
  travel and side-entry ground-reticle bomb pass. Normal, Hard, and Furious
  speeds differ; the warnings use the existing ground-targeting system.
- [x] Juggernaut's charge stops at the top boundary or on a target and enters
  his existing somersault reel instead of continuing beyond the field.
- [x] Stage-6 carrier overflight, shadow and turbulence; two departing jets;
  radio warning; concealed interceptors acquire the player and reveal when
  they fire. The existing slow-motion Shoot interception remains live.
- [x] Stage-6 length extended from 56 to 75 seconds with additional late jet
  and bomber waves. Two randomized wingmen arrive in each of two windows,
  then the remaining eight pilots form up around the player. They shoot and
  use their authored roll/somersault reels to dodge. Wing-only supply icons
  briefly boost their shots and repair a hit; they withdraw with a radio line
  if overwhelmed. The player remains the ninth pilot.
- [x] Left/right split pauses stage progress until a direction is selected.
  Half the formation departs, the other half escorts the player. The left lane
  brings Nightwing fighters to the Warhive carrier. The right lane brings fast
  dashes to the Rebel Squad.
- [x] A false clear overlay and reverse scratch precede the boss ambush.
- [x] Rebel Squad: three separately targetable large hulls, each with its own
  energy shield. Purple Ghost fires rapid fans; teal Ouroboros uses ground
  reticles and missiles; black Phantom charges. The trio exchanges lanes with
  the authored Chaos Harrier warp effect. Shields break and briefly stun.
  Easy has half the Normal HP; Hard and Furious raise HP and attack cadence.

## Still to produce and tune

- [x] SpriteCook GPT-2.5 bank, side, dedicated underside, somersault,
  charge-up and dash frames for all three Rebel ships, cut into consistent
  pivot canvases and registered in the live boss renderer. The strongest
  somersault views are used; the generated 2x2 reels contain some repeated
  top-down geometry, so a future art polish pass may improve the flip illusion.
- [ ] Give wingmen their own full weapon/ability roster and a dedicated
  smoke/departure reel. The current ships fire, dodge, collect wing supply,
  and can withdraw.
- [ ] Give the split route a longer, hand-tuned squadron set-piece. The current
  branch-specific pre-boss waves are short.
- [ ] Confirm whether Mike's “Harrier boss” on the left branch means the
  existing Stage-6 Warhive/Nightwing fight or the Stage-5 Chaos Harrier. The
  playable left route currently retains the Stage-6 Warhive.
- [ ] Replace the false-clear playfield caption with a full authored clear-card
  interruption and record a production scratch/reverse cue if desired. The
  current scratch is synthesized and the caption is functional.
- [ ] Tune the Rebel Squad's shield budgets, collision lanes, music transition,
  and difficulty patterns with Mike after a full manual run.

## Verification

`node --check assets/game.js` passed. `_BUILD_SOURCE/test_fl.js` reached its
final summary with 76 failures (exit 1) after the SpriteCook art integration:
the only additional failure name versus the immediately preceding 75-failure
run is the known intermittent Stage-1 sand-tank assertion, which was present in
the earlier 76-failure local baseline. An intervening run showed a transient
Maverick-lance assertion failure; the repeat returned to the baseline set.
Real Chromium captures of the carrier/intercept, allied pair, nine-pilot
formation, false clear, and Rebel Squad were inspected. The focused Rebel probe
passed ten assertions covering damage routing, wing dodge, and supply, with no
page or console errors. The GPT-2.5 bank, charge and warp/somersault frames were
also inspected in real Chromium; captures and a short GIF are under ignored
`_shots/stage6_rebel_gpt25_*`.
