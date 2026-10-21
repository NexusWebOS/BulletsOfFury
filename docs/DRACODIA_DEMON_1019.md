## October 19 follow-up — spinning ball, safe edges, wireframe downloads

Implemented Mike's follow-up in the GitHub Coding checkout. Shadow Ascension
rotates clockwise at 0.85 revolutions/second throughout charge, release and
approach. The lethal foreground inherits the incoming frame clock and angle.
No FOV/Retina warning was added. The final aim still freezes for 2/1.75/1.5/1.25s
on E/N/H/F. At commit, aim is constrained 120 world pixels inside each side
(radius64 +56 clearance; bounded to40% of viewport width). The projectile
continues smoothly from its actual pre-commit trajectory to this frozen aim.
All16 edge cases survive at base speed with zero invulnerability: left/right,
starting at center/already at edge, each difficulty. Central core remains lethal.

Every current identity has its own hollow PixelLab wireframe: infused host,
ghost, main Colossus, Hammer, helicopter, Harrier and volcano. Actual current
native rigs were exported and visually reviewed before generation. Seven
Pixen wireframe edits preserve their weapons and pose. PixelLab exact drawing
then animates a moving highlight across the authored lattice:16 frames/form,
112 frames total, seven1024x1024 fixed-cell PNG sheets,807,496 PNG bytes.
All cells256x256 with common128,128 pivot; no border pixels, stretching or
individual frame fitting. All source edits, recipes and native references remain
under _ART_SOURCES/dracodia_download_1019. No atlas outside this drop changed.

The transition peels solid armor into wireframe, compresses into code, opens the
next wireframe and reconstructs live armor under a moving scan. Phase2/3
arrivals, infused conversion, every copy morph and final reform use this owner.
The complete hologram is framed below the HUD and eases into the live rig;
this only translates drawing, leaving positions, module sockets and damage
owners authoritative. Live modules retain ordinary hit feedback. Seven sheets
preload only with Stage8. Teleport audio triggers on incoming mode entry,
never on redraw. Hammer's native protected attack states remain authoritative.

Verification:70/70 final native Edge checks,0 browser/asset/draw errors,exit0;
8,854 regressions,BUILD OK/0 errors,exit0; game.js and demon layer syntax pass.
The existing112/112 combat/audio checks also passed after the spin/edge change.
The first morph fixture incorrectly bypassed the full attack-book gate, then
assumed Hammer could never protect himself in fight mode; corrected to satisfy
the gate and assert the native protection owner. Production guard unchanged.

Owners: assets/dracodia_demon_1019.js, assets/dracodia_download_art_1019.js,
_BUILD_SOURCE/build_dracodia_download_1019.py and
_BUILD_SOURCE/probe_dracodia_download_1019.py. Final logs:
_shots/dracodia-download-shipping-native.log and shipping-suite.log.
Review: _shots/dracodia_download_1019/review.html; movies rotating-ball.webp,
form-downloads.webp and phase-downloads.webp. Cache wire-download-1019.
No commit/push requested for this follow-up; preserve unrelated dirty work.

## October 19 correction — homing, no FOV, giant foreground approach

Mike requested that this attack track the pilot until the last second or two,
show no FOV warning, and grow dramatically toward the screen. Implemented and
verified: 112/112 native Edge checks on E/N/H/F, no browser errors; 8,854 whole-game
checks, BUILD OK, 0 errors, exit 0. The focused final preview passed 6/6 checks and verifies that a
lethal eradication continues from the incoming ball size instead of shrinking it.
Evidence: _shots/dracodia_demon_1019-homing-native.log, homing-suite.log and
homing-final-preview.log. Updated movie: _shots/dracodia_demon_1019/homing_encounter.webp.
The earlier fixed-target description and 80-check checkpoint are superseded.

# Dracodia: demon in the machine — October 19, 2026

Mike requested distinct demonic-machine behavior for all three Stage 8 phases,
a depth-scaling overhead shadow ball, ghost feints/strikes, half-health downloads,
code shields, contextual pilot deaths and mechanical symbiote cinematics.

## Encounter behavior

- Phase 1: committed alternating arm lasers with authored muzzles, charged palm
  orbs, and a warned jumping grab. A lethal grab flings the actual selected hull
  toward the screen edge. Surviving shield absorption retains normal control.
- Phase 2: three/four ghost teleports followed by a levitating, committed down
  strike; existing Soul Bomb and void wells remain. A download ritual raises the
  arms, tilts the head back, illuminates eye pixels white and summons helpers.
- Phase 3 main body: opens with **Fear THIS!** and an overhead purple shadow ball.
  Dracodia retreats to 48% depth; the projectile approaches from 70 display
  pixels to a foreground canvas 4.8 times the larger playfield dimension. Its visible orb grows wider than the whole screen. It has no Retina target; it tracks its selected living pilot during charge and flight, then freezes its aim for the final escape window. Its damaging radius
  is 64 world pixels and is live only in the final 6% of approach plus 0.16s.
  The large corona is presentation. Late rolls/somersaults, lateral movement and
  shields remain valid. The whole expanded ten-attack main-body book completes
  before a copy morph; all four approved copy pools remain intact.

Easy/Normal/Hard/Furious shadow tells: 2.20/2.00/1.80/1.65 seconds. Travel:
4.40/4.00/3.65/3.40 seconds. The ball stops homing for the final 2.00/1.75/1.50/1.25 seconds respectively. Mike explicitly requested no FOV cone or impact reticle for this attack; the charging orb, approach and caption are its tell. Other attacks retain their FOV warnings. Ghost slam tells: 1.40/1.20/1.05/0.95 seconds
after the final feint. The shadow ball does not resume tracking after its final aim freeze.
Every attack clears on phase cancellation, with no pending timers or audio.

Phase 2 shields use violet/chromium/white; phase 3 uses reactor red-magenta and
chromium/white. Both have a genuinely transparent aperture, finite absorption,
native shield mini bars, absorb/break sounds and native owner/part hit flashes.
They emit no reflected shots. Download shields are 3.5% of current maximum HP;
dedicated Aegis shields are 4.5%. Retained archive attacks now use FOV warnings
without floating anchored warning boxes.

Downloads cap at 1/2/2/3 active helpers on E/N/H/F. Every summoned regular unit
and miniboss has half its source health; at most one archive miniboss is added.
They receive a 2-second materialization and 0.6-second settle before starting
their normal warned attack cycle. Dracodia retreats behind their render layer.
New INFERNAL WIRE JET and DAEMON SENTINEL use PixelLab idle/data assembly banks,
physical alpha masks, separately damageable side modules and native hit flashes.
Their body-contact footprint follows actual visible art. The archive roster
still includes hard jets and historical minibosses with native attacks.

## Pilot death ownership

The existing playerHit function still owns shields, invulnerability, special
protection, lives, stripped powerups and respawn. Only a genuine lethal hit
selects a contextual presentation. Neutral deaths keep the native burning spin.

- Shadow/Soul Bomb: the actual aircraft enlarges inside a growing energy sphere
  and is progressively erased by the white plasma effect.
- Laser: the actual hull is erased through the energy rupture.
- Ice: a blue-white frozen hull/cocoon fractures into nine physical moving hull
  pieces; the cocoon clears instead of remaining on screen.
- Fire: anchored burning 720-degree spin, then the shared explosion.
- Grab: a spinning hull is thrown to the screen edge.

The common hostile-projectile contact passes its existing kind/element flags to
the presentation selector. Unknown sources retain the original death. Both
co-op seats keep separate death state; a later neutral death clears old custom
state. Hulls are captured once from the real pilot or space hull, never generated
substitute aircraft. Drawing does not advance the effect clock.

## Art and sources

PixelLab generated all combat banks. Reviewed/repaired frames use exact PixelLab
workbench operations: shield aperture, phase-3 palette and wireframe interiors.
No placeholders or runtime-generated character art were added. 135 final PNGs,
2,310,706 bytes; two 960x540 GPT cinematic plates, 579,444 bytes. Total new
shipping bitmap payload is approximately 2.76 MiB. Every bank uses one common
proportional scale/pivot, even canvases, shared padding and zero opaque source
border pixels. One clipped fade spark and late burst blips were excluded.
Rejected draft portals and sources remain archived, outside runtime registration.

The mechanical cable-serpent replaces the organic symbiote effect in the drone
infusion, organic attack ordnance and surviving-fragment cuts. GPT imagegen
remade the orbital emergence and satellite contact with the approved Dracodia
master as identity reference. Actual runtime story keys, including the newer
pt11 mystery plates, now resolve to those scenes. No aircraft were generated.

Owners:

- `assets/dracodia_demon_1019.js` — encounter, seats, shields and contextual death.
- `_BUILD_SOURCE/build_dracodia_demon_1019.py` — normalized banks/manifest/review.
- `_BUILD_SOURCE/build_dracodia_cinematics_1019.py` — cinematic exports.
- `_ART_SOURCES/dracodia_demon_1019/jobs.json` — PixelLab IDs and curation.
- `_ART_SOURCES/dracodia_demon_1019/generation_requests.json` — generation prompts.
- `assets/game/levels/stage_08/effects/dracodia_demon_1019/` — boss effects.
- `assets/game/levels/stage_08/enemies/dracodia_legion_1019/` — exclusive helpers.
- `assets/game/shared/player_fx/context_deaths_1019/` — shared pilot death art.
- `assets/game/shared/cinematics/dracodia_demon_1019/` — GPT orbital plates.

The small shared death banks load with campaign stages; other banks load only
with Stage 8. Cached textures, bounded helpers/voices and finite attack state
avoid unbounded allocations or spawn storms. This is not a measured cross-browser
FPS guarantee or a human win-rate estimate.

## Verification

The required whole-game suite completed with **8,854 passing checks, BUILD OK,
0 errors, exit 0**. Both game scripts pass syntax checks. game.js remains LF and
test_fl.js retains CRLF. Final native totals: 80/80 encounter checks plus 5/5 caption, infusion, scene and visible dodge checks, all passing with zero browser errors. Native Edge reports and actual screenshots/animation:
`_shots/dracodia_demon_1019/`. Latest shipping tests are recorded in
`_shots/dracodia_demon_1019-native-complete.log`; the final caption/infusion/scene
check is `_shots/dracodia_demon_1019-caption.log`. Earlier successful checkpoints
were 62 and 78 checks; keep their logs as history rather than final evidence.

Native checks exercise all four difficulties, committed-target dodges, lethal
hits, shields, defensive iframes, owner cancellation, phase 2/3 teleport chains,
half-health helper caps, actual owner/module damaged pixels and flash expiry,
co-op death independence, all nine aircraft, source-specific deaths, ordinary
death recovery, FOV-only warnings, effect blits and decoded native cue playback.
The ten cue routes were verified as playing at positive volume through the
shared mixer. Native canvas captures and all-frame sheets were visually reviewed.

No voices were fabricated; Fear THIS! is a live in-game caption ready for Mike's
future voice recording. No commit/push was requested. Preserve unrelated dirty
work, including the independent Claude helper and Overdrive.
