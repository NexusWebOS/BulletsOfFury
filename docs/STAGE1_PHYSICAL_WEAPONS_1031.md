> The kamikaze movement/palette is now superseded by [rolling orbit pursuit](KAMIKAZE_ORBIT_1031.md). Other contracts below remain current.

# October31 physical weapons and camo-tank revision

This supersedes the preceding five-enemy pass where the specifications below
changed. Mike's follow-up makes the Light Jungle Tank a gray/black camo MG
variant restricted to Hard and Furious, with faster fire and more appearances.

## Current attack owners

`assets/stage1_followup_1031.js` (S1B) loads after S1A. Native health, death,
rewards, component damage, traffic, target locks and offensive/defensive
interception rules retain their existing owners.

| Enemy | Current behavior |
|---|---|
| Patrol Boat | Its two existing side modules alternate three-round spreads; the main bow gun gives rapid nine-round bursts between them. Each has its own physical source mouth, short flash and authored FOV reaction window. A destroyed side module immediately cancels its warning and release. The main gun uses the live hull/core; side-module HP is retained. |
| River Corvette | Four straight rounds from the actual central bow cannon, replacing the broadside origins/fan. A compact attached flash follows the current bow, with native Heavy MG sound. |
| Strike Bomber | Visible crimson/silver source bomb, preserving source alpha, neutral metal and dark outlines. It drops through the lower screen until its actual exit. Native Retina, damage and impact/audio remain. |
| Heavy Jungle Tank | Physical paired missiles retain native locks and flashes. Configured reload becomes3.3s Normal,1.85s Hard,1.05s Furious. Native motion/braking may extend an interval; measured samples were3.43/2.52/1.05s. |
| Jungle APC | Five paired MG releases per burst from the visible twin rails, with two short flashes and one native Heavy MG cue per pair. Native turret aiming, tracks and traffic remain. |
| Light Jungle Tank | Gray/black camo armor and matching gray/black slugs, eight paired releases per burst and faster rounds/fire than the APC. It cannot spawn on Easy, Normal or Insanity; only Hard/Furious. |
| Delta Strike Fighter | Current actual AF21 Strike hull, source heading/drift frames and animated thrusters, with limited turn rate, constant forward speed and a clean exit. Chosen curve/corner routes steer the actual flight. The normal Delta shares this correction. |
| Rocket Buggy | Actual red/white material from its loaded MT18 rack becomes the launched rocket, with authored animated exhaust. MT18 keeps both independent launcher HP pools, warning/fire/reload animations, native release sockets, motion and damage. |
| Missile Ground Turret | Two missiles simultaneously from the two visible tubes, after native target Retina/beeps. |
| MG Ground Turret | Six paired releases per burst from the two rotary mouths, with attached flashes and Heavy MG audio. |

The generic nine-second aircraft exit push now defers to every native moving
ground-vehicle owner, including tanks/APCs/rocket trucks in other stages. Their
terrain-relative movement and traffic reservations own the chassis throughout
its life.

The MG/missile emplacement controller and source-heading rendering are shared
throughout the campaign. The existing sonic/laser emplacement owners are
unchanged. Head and base both show the native white damage flash; source palette
returns after expiry. Native non-shootable ordinary rounds and shootable physical
missiles keep their rules before their first simulation update.

## Camo reinforcement and aircraft contracts

Hard adds five camo wave slots at32/44/56/68/77s; Furious adds eight at
28/35/42/49/56/63/70/77s, in addition to the now difficulty-gated native Light
Tank waves. These are queued ground waves, not an independent overlap-prone
spawn loop. They require the native coastline gate and a legal arrival row;
`ground_traffic_1018.js` reserves the actual hull and maintains clearance. A sea
arrival waits; no ground unit is converted into a boat or placed on water.
Boss/miniboss/end interlocks remain native.

S1A flight initializes native Hard/Furious aircraft HP, speed and fire modifiers
exactly once before controlling a new turning sortie. It does not drop the elite
health multiplier when replacing the former slide. Existing rush/pair/kamikaze
controllers remain separate. The kamikaze uses its original committed vector and
one shared `jetDash` cue when it locks that vector; it gains no gun volley.

## Source art and rebuilds

- `_BUILD_SOURCE/build_stage1_amplify_1031.py` owns nine banks/1089 fixed
  directional frames, including the added actual AF21 Strike hull and updated
  crimson/silver bomb. The two Delta families each have measured tail/gun
  sockets, three source poses and32 baked headings. Animated exhaust replaces
  their frozen blue flame pixels in the derived hulls.
- `_BUILD_SOURCE/build_stage1_followup_1031.py` owns six banks/456 frames:
  gray hull/turret, gray slugs,64-heading native MG/missile heads and32-heading
  four-frame rack rockets. The rack crop excludes olive mounting material;
  red/white rocket paint, neutral metal and outlines are preserved. Exhaust is
  reused authored S1M motion art with a warm palette.
- Manifests are under `enemies/amplify_1031/manifest.json` and
  `enemies/physical_1031/manifest.json` in Stage1 assets. They register source
  paths/crops, hashes, fixed even cells/pivots and proportional scale. Existing
  source atlases are read without repacking or editing them.

No new paid art is used. Revised bodies, headings and projectile art use source
cell selection rather than runtime rotation of a static sprite. The APC retains
the existing S1M twin-rail rig; the new Light Tank palette distinguishes its rapid
fire role. The original live MT18 whole chassis and modular launchers remain its
native rig.

## Verification and accepted previews

`probe_stage1_followup_1031.py`:69 native Chromium checks pass across Normal,
Hard and Furious. They include every revised attack, paired physical origins,
Patrol weapon alternation, straight Corvette rounds, Strike headings/exit and
native difficulty HP, measured Heavy cadence, camo difficulty/frequency gates,
native damaged pixels and30-frame flash expiry, and immediate interception rules.

`probe_stage1_followup_edges_1031.py`:14 checks cover both chosen corner routes,
destroyed Patrol-module cancellation, the shared MG/missile owners in Stages4/6/7,
two real reinforcement placements through native traffic, waiting at sea, and ground-vehicle ownership of the age-based exit rule.
There are no page/console/render errors in these runs.

`record_stage1_followup_1031.py` uses real native RAF, an invulnerable input-only
observer and shared-mixer audio. Enemy HP, attack clocks and movement states are
not edited during footage. Native initialization is allowed to apply its own
difficulty values. The final ordinary fighter fixtures initialize that native
controller before recording and report the resulting complete HP. Unrelated
waves are suppressed by the isolated fixture; external gamepad input and stray
taps are excluded. These are animation/attack samples, not balance runs.

Twelve new H264/AAC30fps faststart clips fully decode; all contain actual decoded
native sound. The guide retains all163 cards. This pass updates twelve cards,
preserving the existing current Gunboat and paired Delta film and the remaining
roster. The original complete compilation stays labeled as an archive.28
Chromium guide checks verify current sources, seeking, playback and decoded audio,
preserved other151 cards and no page/asset errors.

The camo sample shows96 rounds versus36 from the APC in similar12.3–12.5s
samples. The Heavy sample shows five Furious paired salvos. The bomber shows nine
visible drops through its exit. The kamikaze remains a ram with one decoded
jet-dash sound rather than an artificial gun attack.

Current local guide:
`http://127.0.0.1:8805/enemy-showcase-1031.html?revision=stage1-physical-1031#enemy=stage1-s1boatpatrol`

Ignored evidence is under `_shots/stage1_followup_1031/`: source contact sheets,
native screenshots/traces,69 primary/14 edge receipts, the twelve accepted film
folders and telemetry, full decode/publish receipt and28 playback checks.
`publish_stage1_followup_local_1031.py --install` updates the local server's
existing whitelist with only these scoped files. Later fixes to spawn eligibility
and the coast gate do not alter the isolated Furious recordings.

Syntax/whitespace checks pass. Required `node _BUILD_SOURCE/test_fl.js` still
exits1 before assertions or its final summary because this checkout lacks
`UNUSED_ASSETS/retired_art_1022/manifest.json`; it is not a passing full suite.
No commit, push or GitHub publication is included in this pass.
