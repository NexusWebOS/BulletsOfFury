# Current Breaker liquid arsenal — November 2

Mike requested internal1015 water light, a rapidly spinning approaching orb,
alternating hand-grenade animation, warned vertical flight with side waves,
nine-direction marble grenades, hand-shoved tides and a background spinning
roller attack. This pass installs the controller in the actual Stage9 game.

## Gameplay

- The orb approaches on a small circular weave with32 baked rotation cells and
  moving emissive water pixels inside its actual mask. The existing29-cell
  liquid transformation gains source-matched internal/edge1015 light.
- A scenery-only darkening precedes the sustained grenade barrage. Water gathers
  in the throwing palm; the16-cell bank alternates charge, windup, release and
  recovery between hands. Grenades retain physical interception, committed ground
  reticles, native water splash damage and finite flight time.
- The existing overhead flight bank owns launch, actual directional turning,
  northbound departure, south-edge northbound pass and north-edge southbound pass.
  Water waves leave registered hands toward both sides. Forecast rows use the same
  fixed60Hz release ticks and sockets as the actual attack. Wave collision sizes
  grow with the visible wave, and side-wave hitboxes follow their rotated shape.
- The orb rolls around the field, pulses and emits nine radial grenades per
  release, then reforms. Both palms gather water and visibly shove three paired
  tidal releases on the actual open-palm frames12/13. Held water leaves with each
  shove and rebuilds for the next one. The casting stance settles at world centre
  so camera movement cannot clip the body. The prior wave art gains32 baked
  optical-flow frames.
- Current flies north and shrinks into the background, settles frontally, charges
  and turns through32 source-derived yaw cells using actual generated
  front/profile/back views. Growing16-frame Falva-derived water rollers approach
  the pilot. Physical missiles send them back into depth for22 native damage;
  primary weapons burst them into harmless splash art. An intact roller kills
  through the native player-hit path. Maverick's spaceVolley remains a regular
  weapon response and is never classified as a physical missile here.
- A short background recovery lets counter shots finish before he flies back to
  the foreground, recovers into the humanoid and retreats through the native
  regular-enemy ending. Native death cancels owned warnings, hazards and counters.

The Normal210 / Hard242 / Furious278 budget and shared difficulty policy remain.
Enemy damage, actual white/element hit flashes, expiry, shared audio/retrigger
gates, party ownership and native death/reward paths remain the owners. Flight
body contact stays disabled; the emitted attacks own their contact volumes.

## Stage9 progression

The12.05 scheduled wave is tagged and retried if its spawn is refused. Both queued
and living Current Breaker gate native encounter entry. During the expanded
window, progression holds at the authored miniboss threshold18.9 while actor,
projectile, input and audio clocks continue. Once Current is killed or completes
his finite arsenal/retreat, the normal miniboss warning resumes first. This avoids
skipping the later regular waves or letting the overdue boss warning replace the
miniboss warning. A64-second actor-age failsafe still guarantees a finite exit.

`probe_current_campaign_1102.py` runs the real Furious wave book with no player
fire or enemy HP/phase writes. Under that crowded case Current enters around35s,
completes at native278 HP and hands off to the miniboss while stageTimer remains
18.9 and wave17/38 leaves the later waves queued. This is a progression stress
case; a firing player can clear the dispatch pressure earlier.

## Art and implementation owners

- `assets/current_breaker_1102.js`: Current-only controller, sockets, actual alpha
  contact, forecast warnings, counterable rollers and scoped progression hold.
- `assets/current_breaker_art_1102.js` and
  `assets/game/levels/stage_09/enemies/current_breaker_1102/manifest.json`:
  ten registered even-cell banks. All bodies keep384px cells and a common chest
  pivot;192px proportional glow cells sample the existing1015 rings baker.
- `_BUILD_SOURCE/build_current_breaker_1102.py`: source-preserving exports,
  measured/snapped hands, spatial own-water emission, opaque yaw interpolation,
  smooth wave frames and water-palette Falva rollers. OpenCV is isolated under
  `_shots/current_breaker_1102/deps`; install with
  `python -m pip install --target _shots/current_breaker_1102/deps --no-deps opencv-python-headless`.
- Selected project-owned sources:
  `_BUILD_SOURCE/current_breaker_1102/actions_source.png` and `yaw_source.png`.
  Built-in ImageGen used the approved prior humanoid and pose bank as identity
  references. Exact prompts/output IDs and normalization notes are in
  `_BUILD_SOURCE/current_breaker_1102/prompts.md`.
- `assets/game.js` only gains guarded encounter-entry checks. Its LF and
  test_fl.js's CRLF are preserved. Current's scripts load after the existing
  Stage9 FOV and shared difficulty owners. Concurrent S9F improvements remain.

No runtime canvas/CSS rotation substitutes for the authored body/yaw/flight
banks. No HTML opacity fades drive the transformation. Scenery darkening and
own-pixel additive1015 light remain separate from hull pixels and hit flashes.
The other18 Stage9 model sources and the rest of the roster art are preserved.

## Verification and preview

22 focused native Chromium checks pass, covering the complete untouched-HP attack
book, alternating palms, nine-way counts, overhead views, tide releases,
background scaling/yaw, exact warning rows, shared health, actual native missile
and primary launches, both counter responses, lethal intact contact, damaged
pixels/flash expiry, emitter overlap, owner death cleanup and encounter gates.
The actual casting alpha stays on screen while native pilot movement pans the
camera across its full200px range.
The separate real-schedule campaign handoff check passes.

The fresh native-input film is47.76 seconds at59.07 native render fps, with labelled invulnerable pilot
assistance and no enemy HP/phase/attack-timer writes. It demonstrates physical
missile returns, native owner damage and harmless primary-weapon splashes.
The final take includes three missile returns and four harmless primary splashes;
H.264/AAC fully decodes with audible unclipped sound (peak0.283, RMS0.0732).
Other waves and unrelated pickups are held only in this labelled focused film.
Existing water/charge/dash/missile-hit cues use the shared mixer and retrigger
gates. Full video/audio decode and browser chapter receipts live under
`_shots/current_breaker_1102/publication/`.
All14 real-Chromium chapter, desktop/mobile and existing-guide checks pass.

Review: http://127.0.0.1:8805/current/current-breaker-1102.html

Publish/verification owners: `record_current_breaker_1102.py`,
`publish_current_breaker_1102.py`, `verify_current_breaker_1102.py` under
`_BUILD_SOURCE/`. Only Current's individual film is replaced in the19-enemy
Stage9 page and154-card full guide. The previously recorded all-wave films
remain their earlier build's baseline.

Syntax checks pass. Required `node _BUILD_SOURCE/test_fl.js` still exits1 before
assertions/final summary on the existing missing ignored
`UNUSED_ASSETS/retired_art_1022/manifest.json`. No commit or push.
