# October 10 audio playthrough update

Mike's following HQ-map request is implemented in
[the live HQ cinematic update](HQ_LIVE_1010.md). Its new environment plates,
interactive radar and exact ship sprites supersede the static HQ presentation
described in this earlier pass; the original sources and QA remain preserved.

The complete 44:32.48 recording was processed locally into 307 timestamped
speech segments. Its sampled video frames are black. The direction log therefore
distinguishes spoken feedback from observations made in the current game.
The source SHA256 and recognition method are saved in
[`qa/audio_playthrough_1010.json`](qa/audio_playthrough_1010.json).

[Open the animated art review](previews/audio_1010/index.html) and
[read the 39 timestamped directions](feedback/PLAYTHROUGH_AUDIO_1010.md).
The playable build is the repository's normal `index.html`.

## Changes in this pass

- Bottom HUD: new complete chrome/amber housing, raised lives/missile tabs,
  larger weapon/status wells, radar beside the top scores, and full playfield
  width at four tested window sizes. Ordinary pilot/Fury flight holds its
  authored neutral frame; maneuvers retain their actual poses.
- Weapons: one committed ice orb, two MG/chaingun lanes at every tier, chaingun
  attachments in the actual loadout preview, normal spread fan trajectories,
  no missile launches or ammunition loss while charging, and 80% same-element
  absorption by ice bosses on every difficulty. Native Freezer time-slow missile
  launch and impact pass; that reported failure was not reproduced.
- Stages 2–4: larger shieldless kamikazes with readable Normal dives and faster
  circular approaches on Hard/Furious; firewall arrival sound; healthy twin
  turret miniboss favors widened charged lasers and returns to magma bombardment
  when damaged. Furnace forms before shielding, uses one HP rail, animated
  real chains and a new shield/shatter sequence. Cryospear fires genuine icy
  laser art from its hardpoints. Sovereign charges a southbound fusion shot,
  bursts into aimed lightning balls at mid-screen, and its independent helpers
  fire from both barrels with warnings.
- Space: slower cruise, moving/attacking frigates, gravity ships and stations,
  new fusion cannon art, and a complete generated Cole assembly. Assembly art
  matches the original aircraft's height through drift/charge/scatter; its
  docking snap follows the existing intended tuck. Other pilots retain their
  own ship and hardware. Decker owns the kit dialogue. A real undeclared-scroll
  error no longer aborts Stage 9 return: the timer, future waves, completed
  miniboss and backdrop position restore.
- Stage 6: HQ landing/attack/radar/scramble cinematic, actual red/green/blue
  stealth fighter plates facing south, faster Normal reinforcement waves and
  four allies alongside the player. Rebel demonstrations retain a live world
  while blocking movement and duplicate dialogue. Jace releases a full-sized
  agitated ball south, Rook's slugs travel south, Voss keeps 1250px/s through his
  return and uses new charge/snap art. Cloak energy ends with a completion sound.
- Stage X: protected titled five-ship arrival, actual Harrier attack participation
  on Normal, and carrier core must reach zero before its phase ends. Its once-only
  Air Superiority reward grants one life, 12 missiles, super-missile progress and
  a forge credit.
- Wind replaces the Stage 6 Prism reward. Nine actual craftable carriers use
  authored gust/tornado/impact art and separate icons. Legacy saves preserve
  their highest crafted levels and earned entitlements when migrated.
- Campaign: larger hovering map ship, side-UI readiness, physical directional
  neighbors, Stage 6↔X vertical navigation, and no Stage 7/8 wrap to Stage 1
  before Stage 8 is cleared. The escaping map ship is the rotating Harrier.
  The active cinematic director now lets Decker identify the alien sewer signal.
- Finale: safe straight portal handoff, a 32-frame void, a 16-frame portal-behind-
  drone consumption with attached head and arm-raise/shriek, stronger committed
  ordinary-enemy volleys, and real physical claw geometry. Early two boss fights
  sustain actual attacks. Defeated copied forms visibly rupture, change form and
  retain their zero HP pool. Four authored homecoming plates replace the short
  return sequence; final completion bypasses upgrades and the redundant cinematic.
- Existing Hammer 1010 death/chromium work remains. Earth stays a fixed size
  against the existing space backdrop while the current Furyship approaches it.

## New artwork and ownership

Thirteen accepted native `image_gen` sources produce **193 loose cells plus
one HUD housing**: ice16, fusion16, Wind16 and nine icons, fire shield32,
chains16, void32, drone consumption16, Voss turbo16, Cole assembly16, HQ4 and
homecoming4. This pass does not replace the separate final-boss combat rig.

Each clip keeps an even canvas, physical pivot and common proportional scale.
Builders cut/pad/translate at source scale1; individual cells are not resized
to fit their visible bounds. Wind's four distinct effect clips have their own
ignition/center pivots. The fusion source has unequal row spacing; measured
blank gutters and real nozzle centers are used to remove adjacent-row bleed
and keep its muzzle stationary. Original RGBA, exact prompts, measured registrations and
hashes are retained in
[`generation_manifest.json`](../_ART_SOURCES/audio_1010/generation_manifest.json).
The manifest distinguishes the accepted sources from intermediate generation
prompts. No shared atlas changed. SpriteCook upload did not occur; built-in
image generation supplied the accepted transparency edits.

`_BUILD_SOURCE/build_audio_*_1010.py` owns exports and art registries together.
`assets/audio_*_art_1010.js` registers the pixels; `assets/audio_*_1010.js`
owns the late runtime integrations. Existing shared controllers, warnings,
ordnance, targeting and destruction remain in use. In particular,
`audio_encounters_1010.js` owns Sovereign/Reaver changes,
`audio_fleet_1010.js` owns the active fleet/Harrier changes,
`audio_wind_1010.js` owns migration and carrier effects, and
`audio_alien_1010.js` owns final encounter participation and copied-form breakup.

## Verification

`node --check assets/game.js` and the runtime syntax checks pass. The complete
`node _BUILD_SOURCE/test_fl.js` run reaches its final success summary:
**8,170 passing assertions, zero failures, exit0**, compared with 8,132/0
before the audio work. Final failing-name lists are empty.

Real Chromium gameplay probes use `_BUILD_SOURCE/shoot.py`, lazy asset polling,
the game's actual `XART.get`/`drawImage` route and yielded frame batches.
Five probes total **52 passing checks, zero failures**, including wide/narrow
HUD layout, actual projectile release/impact, attack-cycle participation,
module ownership, Wind recipes, dialogue clocks, Stage X health gates and the
final exit. Page, console and asset error lists are empty. Representative
screenshots were inspected, including the earlier off-screen/undersized
presentation fixtures; the final fixtures place actors on their real stage
and register assembly scale against the aircraft, not the outer sheet.
The preview has a separate browser check recorded in the durable QA file.

These are controlled fixtures with invulnerability and selected encounter
states. They do not constitute campaign victories or a finished human balance
verdict. All temporary captures, intermediate failing logs and the full working
transcript stay under `_shots/playthrough_audio_1010` and `_shots/audio_1010`.

## Remaining identification and human checks

- The exact unnamed weak/modular enemy at 15:50–17:44 and particular final-boss
  forms/poses at 40:38–42:53 need names or visible references. Stage 5 space
  enemies are a campaign-order inference; the existing space miniboss is already
  modular and its pursuit attacks were verified, but this is not evidence that
  it is the unit Mike meant to remake.
- White map artifacts and the specific completion-stretch effect cannot be
  located in black video. Current native completion flight keeps the real ship's
  scale and moves north; the result panel matches its actual authored aspect.
  No bespoke replacement completion reel has been claimed.
- Play Normal through the revised Stage 2/4 fights, Stage 6 choices and all three
  final encounters, then compare Hard/Furious for fairness and attack readability.
  Full audio mixing and hardware/gamepad behavior still need a human pass.

Working tree is updated locally on `7539951`. Existing user work remains.
No commit or push was requested for this audio pass.
