# Stage7 toxic modular refit — November1

Live owner: assets/stage7_amplify_1101.js. Art registry:
assets/stage7_amplify_art_1101.js. Rebuild:
`python _BUILD_SOURCE/build_stage7_amplify_1101.py`.

The pipe is now a segmented mechanical crawler using the actual terrain mask
and shared GT18 hull reservations, with distance-driven legs and terrain-relative
travel. The existing toxic tank fires paired machine-gun slugs from measured
barrel mouths; inherited modular-tank missile locks are removed. Stage7 ground
MG heads retain twin firing mouths, laser shots are toxic-green1015 energy, and
the liked sonic head fires toxic-green waves. Turret fixtures remain anchored to
their actual scenery rows.

Brood Sentinel has a generated main body, two independently posed scythe arms,
eight registered mouth frames and eight robot-fly wingbeat frames. Claw motion
owns actual contact and commits the target during the warning. Mouth releases
are projectile actors, never helper enemies. The legacy escort spawn owner is
removed only from this Stage7 refit. The real once-only medium energy shield
absorbs damage, visibly hits/deploys/breaks, and renders along source body/module
pixels rather than a round bubble. Barge uses the same shield contract and four
independent rotating/recoiling deck weapons over a new toxic industrial hull.

Heavy Relay has separate swiveling rotary pods with eight source-derived rotor
poses, an accelerating burst interval, facing flight, chase/roll/finite departure,
and measured firing sockets through the generated underside roll poses. Slime
Jet has a distinct camouflaged hull and modular chainguns. Black/green Toxic
Missile Jet has independent pods and native audible Retina acquisition with
physical shootable homing missiles. Crescent Escort is a distinct crescent
aircraft; its independent20s campaign beat replaces a duplicate sampler. The28s
retired-Hunter beat fields the new missile jet.

Blacksteel Hunter (`ll18raptor`) direct and campaign spawns are retired, including
the Stage8 legacy field-veteran call. Its nsb_rap original art and source metadata
remain available for a **BOF expansion only**. This does not alter the separately
owned Stage6 Blacksteel boss. Warden, Dredger, portal/rescue and other stages'
Brood/Crescent owners are unchanged.

91 fixed even art banks register source/module pivots, one source-unit scale,
32 direction cells,16-direction genuine roll poses and native ordnance variants.
No runtime static-sprite rotation substitutes for the new cells. Newly enlarged
288px module cells retain the complete barrel/claw extent. All parts share the
owning native hull pool and flash; they do not invent hidden extra health pools.
Native markHit, shield energy, Retina, interception, contact/death, rewards and
shared mixer remain authoritative. Slugs/energy/robot-fly rounds are unshootable
from birth; physical missiles keep interception. Heavy transitions cancel pending
locks and flashes when their launcher leaves or dies.

Verification scripts and receipts:

- `_BUILD_SOURCE/probe_stage7_amplify_1101.py`:108 native difficulty, attack,
  actual damaged-pixel/expiry, shield and retirement checks.
- `_BUILD_SOURCE/probe_stage7_edges_1101.py`:384 real directed gun-mouth pixel
  overlaps,32 roll socket overlaps, three crowded ground-clearance checks,
  shared cue routes and expansion-art preservation.
- `_BUILD_SOURCE/record_stage7_amplify_1101.py`: fresh input-driven films with
  real mixer capture; no enemy HP/phase/attack-clock writes.
- `_BUILD_SOURCE/verify_stage7_preview_1101.py`:19 actual decoded-video,
  responsive-player, campaign-slot, physical-lock and launcher-cleanup checks.

Final:135 focused checks pass. Eleven current H264/AAC films total168.67s;
decoded sample peaks are0.233–0.304 with audible nonzero PCM in every cut.
Current review: http://127.0.0.1:8805/current/stage7-toxic-refit-1101.html .
The main enemy guide has163 cards;152 unrelated cards and all their films are
unchanged, including the existing sewer drone. Both retired field-Hunter cards
are removed. Original films remain in their previous archive routes.

Mandatory syntax checks pass. The full `_BUILD_SOURCE/test_fl.js` exits1 before
assertions/final summary because this machine is missing ignored
`UNUSED_ASSETS/retired_art_1022/manifest.json`; it is not a green full-suite run.
No commit or push.
