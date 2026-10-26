# Chronos glow pass: 16-bit pixel glow, auras and transformation effects (October 25, Claude)

Mike: *"the stage 5 boss chronus who turns super saiyan red/rage mode, we need that to be a glowing aura
around him, some shakes while he transforms, better transforming effects, and better effects in all his
forms including his chromium armor."*

Owner: `assets/chronos_glow_1025.js`, loaded right after `chronos_chromium_1025.js`. It wraps
`hammerBossDraw` for Chronos only (`c25Own(b)`), and reads the fight's state without writing any of it.
Timing, damage, collision, HP and phases are untouched. `CG.base` is the wrapped draw, which makes A/B easy.

## What "pixel glow" means here (the 1015 method)

Light comes off the art's own silhouette in hard one-pixel steps. There is no blur and no soft fade. Its
brightness walks the fixed ladder `0, .16, .32, .52, .74, .95` on `efxClock`, like a 16-bit palette cycle.

The rings are traced at runtime from the exact plate the fight draws this frame:
- the plate's alpha is dilated by offset-drawing it to its 8 neighbours;
- ring r is dilation r minus dilation r-1, filled with one flat colour through `source-in`.

So the glow follows every pose and cannot drift. **Nothing reads pixels back** (no `getImageData`), so it
also works from file://. Named plates are cached (LRU 48). The unnamed per-frame red rage canvases keep
their trace for 0.25 s on a WeakMap.

## Revision: HE glows, no aura sprites (same day)

Mike: *"I meant to make HIM glow, not put that giant glow/aura around him"*, and *"make the hammer core
and center core of his armor pixel animate/glow"*.

The SpriteCook aura loops are removed from the game. Their sources are kept in
`_ART_SOURCES/chronos_glow_1025/` and nothing loads them. All the light now comes off his own plate:

- **Rim.** 3 to 6 one-pixel shells just outside his outline. The inner shells always hold light, and a
  brighter step travels outward through them one shell at a time.
- **Lit.** His armour is lit from within: his silhouette in the form's colour, added, on the ladder.
- **Cores.** The chest core and the hammer core breathe and throw five hard light rings that pulse
  outward. Panel lamps join in.
  - The mask is an SVG colour matrix (`#cg25emit`, `2.0B + 0.8G - 2.2R - 0.55`, a hard step at .25),
    plus near-white pixels within 3 px of blue (`#cg25bright` AND a grown mask, by `destination-in`).
    That fills the white-hot core centres while silver highlights stay out.
  - The core light is added cyan, never white. White flattened the hammer face into a sticker, which is
    the 1015 warning again.
- **Plating sweep and chrome glint**, as before.

## Red swirling bolts in the rage charge (same day)

Mike: *"those electric lines should be palette swapped to red, and only form when hes charging up and
swirling around him for added effect."*

- During `_hf22Charge`, every stock `c25Bolt` call inside Chronos's draw is skipped (`CG.noBolts`).
  That covers C30's static "A" from his feet to over his head and C29's diagonal.
- In their place, the same `arch_hammer_lightning_0926` frames are palette-swapped to red with a
  `'color'` composite. The hue comes from the red and the luminosity from the art, so the white-hot
  cores stay white.
- They run as arcs on rings that orbit him and rise from his feet to over his head: 2 rings at the
  start, building to 4, and spinning faster as the charge builds.
- Each arc is split at the near/far side of its ellipse. The far half draws before his body and the near
  half after it, so the lightning wraps around him.
- Bolts in every other state (hammer recovery, chromium activation) keep their own colour; the probe
  checks this.

## The hammer throw and the SSJ length (same day)

Mike: *"he should have a frame of him throwing the hammer up, not making it just shoot up like that ...
can you make the transformation a little longer like a true ssj though?"*

- **Length.** The live rage charge is already 4.8 s: `chronos_commitment_1025.js` feeds the 1.8 s charge
  clock at `dt*1.8/4.8`. My first cut stretched it again and the probe measured about 10 s, so that
  stretch is removed and this layer only reads `CG_SSJ`. ⚠ The earlier review clips stepped the clock
  over 1.8 s, so they showed the charge 2.7x faster than the game plays it.
- **The throw.** The charge opens on the authored C27 `throw_empty` bank: frames 0-2 are the wind-up
  with the hammer cocked back over his shoulder, frame 3 is the release, and frames 4-8 are the
  empty-handed follow-through. Then the C29 rage bank plays from its first frame. The stock flight,
  which launched from an idle grip on frame 1, is skipped until the throw has left his hand.
- **The hammer in his hand** is C35's own detached flight art. `c35Tool` picks one of eight drawn views
  by angle and never rotates, and it places the HEAD at the given point. View 1 (head up-left, handle
  down-right) is the wind-up and view 2 (upright) is the release. It draws BEHIND his body, so the
  raised fist closes over the handle.

Traps found on the way:
- **The `throw_empty` bank's tip and grip fields are synthetic.** They are always exactly 126 apart and
  nowhere near his hands. The fist is measured off the plate's pixels instead (`CG_FIST`: the ink
  centroid of the top 30 rows, in native cell px). The bank's frames are also in WORLD cell units, so the
  first release point, which multiplied them by `worldScale` again, launched the hammer from the wrong place.
- **`c30ChargeDraw`'s expanding aura blits its stencil at the plate's NATIVE size.** That is correct for
  the C29 rage plates, which draw 1:1, and wrong for the world-scaled C27 throw plate: the aura trailed
  off up-left of him as a ghost outline. While the charge draws, a C27 key is now given a stencil
  rescaled to the plate's drawn size (`sourceW/H` are scaled too, so `c27TraceAura` stays correct).
- **The rim was tracing that ghost.** "The first plate of 200 px or more" also caught faint aura copies,
  so the trigger now also requires the blit to be opaque `source-over` (`globalAlpha >= .95`). The halo
  copies draw at 0.02-0.6 alpha or additive, and the body draws at 1.

## Pixel-glowing cores (Oct 25-26)

Mike: *"now make frames of his hammer core and core center glowing"*, then, with crops of both: *"these should
be pixel glowing"*.

`cgCoreGlow` is now the 1015 pixel glow, in an 8-frame swell (0 1 2 3 4 3 2 1) at 9 fps (12 in rage,
18 while charging):
- **The bottom of the swell:** the core dims a palette step toward deep blue (`E.dim`, source-over at a
  ladder alpha).
- **The climb:** the core's OWN lit pixels (`E.self`, the plate cut out by the emissive mask) are added back,
  so the hammer face's lightning and the reactor's rings brighten in their own colours. At the top, the
  near-white heart (`E.heart`) flashes.
- **The spill:** hard one-pixel rings (`E.rings`, cyan family) light outward one per step, the newest the
  brightest.

There is no blur, no flat repaint and no overlay art. Measured mean brightness of the chest core across one
swell: 61 -> 115. The first two cuts (a source-over palette repaint and added sparks) were rejected: the
repaint smeared the hammer face's lightning and the sparks were overlay.

⚠⚠ **NOTHING AFTER THE BODY HAD EVER LANDED ON HIM FOR MOST POSES.** `b20Image` draws the plate inside
`translate(b.x,b.y)`, and `cgOver` ran after that draw had restored the transform, using the plate's LOCAL
`dx,dy`. So the lit armour, the plating sweep, the chrome glint and the core glow all drew off-screen,
around the canvas origin. The probe's "the layer changes the picture" still passed on the rim alone. Found
because the chest core measured byte-identical across eight frames. `CG.body.m` now records the plate's own
transform, and `cgOver` draws through it.

**In every animation (Oct 26).** Mike: *"this should also be part of his idle or attack animations"*.
`probe_core_states_1026.py` runs about 140 s of the live fight and logs, per hammer state, whether the core glow
landed. It landed on every frame of all 31 states drawn: idle, unfold, all hammer attacks, the depth combo,
the giant dive/drop, the spin and whirlwind, the nova, the ball, the catch and the chromium activation.
- **The detached hammer** (throws, recalls, the boomerang) is C35's separate flight sprite, not part of the body
  plate. `c35Tool` is now wrapped: its blit is caught and glowed under the same transform. It glowed 1,334 times
  in the run.
- **The whole-armour light was turned down** for regular, chrome and activation. Before the transform fix it never
  landed on these poses, so nobody had seen it. Once it landed, chrome read as pale blue instead of silver.
  Rage, which Mike approved, is unchanged.
- Contact sheet: `_shots/chronos_glow_1025/core_states/sheet.png`.

⚠ The charge is now **7.2 s**: the other session changed `chronos_commitment_1025.js` to `dt*1.8/7.2`, and
`CG_SSJ` follows it (read-only).

⚠ **`chronos_transform_1025.js` (another session, loaded after this layer) now owns the whole draw
during the rage charge.** It has its own throw that sends the hammer south and its own lightning, so this
layer's swirl, red bolts and Super Saiyan burst no longer run there. The probe's two checks on them fail
for that reason, and they still fail with this layer's new code switched off. Everything outside the
charge is still this layer's.

## The red rage forming, rebuilt (Oct 26)

Mike, on the other session's sequential-lightning transformation (`chronos_transform_1025.js`, "C43"):
*"please fix our lightning effects and red rage forming. Its very janky atm"*. Measured off its draw:
- Every strike was one 64x256 `c42_bolt` cell stretched to the full screen height. That scaled its width up
  too, and it landed in a random lane beside him rather than on him.
- Black to red was a hard one-frame swap at u .92.
- The rim/core glow and the red swirl did not run during the charge at all.

`assets/chronos_rageform_1026.js` (loaded last, after `chronos_kame_1025.js`) now owns only the charge's
DRAW. C43 keeps the clock, the protection, the float and the throw pose.
- **0-.30, the throw:** C43's pose, the held hammer and the southward flight. The throw-to-rage size change
  is eased (the rage bank is authored about 21% smaller, `C45_SCALE0`).
- **.30-.92, sequential strikes:** red lightning (the tiled `cgBolt`, never a stretched cell) from the top
  of the screen onto HIM. Targets are his head, shoulders and fists in turn, taken from the pose's own
  ink bounds. The strikes accelerate, and each one gives a 2-frame half-strength silhouette flash, sparks
  where it lands (`fxBurst`, `chunks:0`, no grey debris) and a shake step. The red pose burns in over
  the black one, a ladder step every 4 strikes.
- **.92-1, the final strike:** a wide strike straight down his centre, full red, the burst (once,
  `h._c45Burst`, so `cgDrive`'s landing burst does not double it).
- **Throughout:** the red swirl and his rim/core pixel glow, through the new `cgWithGlow(b, M, fn)`
  helper that any layer taking over his draw can use. `cgDrive`'s shock rings are suppressed during the
  charge (`CG.noRings`), because the strikes replace them, as C43 intended.

The probe's burst and lightning checks now test this design: 18/18.

**The throw, final (Oct 26).** Mike: *"why is he glowing when he throws the hammer? And thats the wrong
hammer style ... the hammer should anchor with his arm so he actually throws it when he swings his arm down.
then when hes done, then you can start the charge up animation"*. He also pointed at his idle hammer, the big
square head on a long dark handle: *"the hammer should look like that"*. He rejected both detached sprites:
- the long-handled flight sprite held in his fist;
- `hf22_blue_tool`, the short-handled hammer.

`throw_empty` (the C27 bank) has no hammer in it and no in-between frames, so no hammer pinned onto it could
read as a throw. The game already ships the right animation: **`arch_hammer_throw_0926`**
(`HAMMER_THROW_REEL`). It has eight authored frames with his own hammer in both hands, drawn as part of the
frame, chest-core pivot and measured head point:
- 1: the idle grip
- 2: crouch
- 3: wind-up
- 4: swung back overhead
- 5: swung over
- 6: arm thrown out, hand empty
- 7: empty stand

`chronos_rageform_1026.js` plays it over u 0-.30, frames 1-2-3-4-5-6-7. The hammer leaves at u .145, between
frames 5 and 6, from frame 5's measured head, as C35's flight sprite (the same 0926 art family). It is drawn
at the reel's pixel scale, `.57/.72`, spins up out of the top of the screen and shrinks.
- **No glow during the throw:** no rim, no lit, no cores, no swirl and no drive. The charge-up starts after the
  throw.
- **Scale:** the reel draws at .57, which matches his idle plate (the stock scale). He settles to .43 while he
  stands empty-handed, so the hand-off to the smaller rage bank does not pop.
- **No dip:** the reel's overhead swing stays on screen, so `C45_DIP` is 0.
- **Loading:** the reel is warmed with stage 5's load, so the first frame is never the fallback pose.

**The full rage forming, five beats (Oct 26).** Mike: *"We still need him to recoup, pose to get ready to charge,
then begin to shake and slowly charge up and do this animation. the lightning should also strike around him
and blow up."* `C45_BEAT` splits the 7.2 s charge:

| beat | u | what plays |
|---|---|---|
| THROW | 0-.17 | `arch_hammer_throw_0926` frames 1-6, hammer released at .135, spins up out of the top |
| STOP | .17-.30 | Hammer Time raised-palm STOP (ht27 boss 12-15) with the hammer masked out of his hand (`_BUILD_SOURCE/build_stop_empty_1026.py`, the mask shifted by each frame's pivot); "ENOUGH! / I'LL SHOW YOU REAL POWER!" typed above him in the stage font |
| READY | .30-.38 | rage 0-2: plants himself and sinks into the power stance |
| CHARGE | .38-.92 | rage 2-6 slowly. Body jitter 1-5 px in hard steps, new every frame. Red burns in a ladder step at a time. 26 accelerating strikes: early ones hit the ground on a shrinking golden-angle ring around his feet and `explode()` there; later ones alternate onto him; the last few are all on him. |
| RELEASE | .92-1 | final strike down his centre, full red, the burst, rage 7-12 (roars arms-out) |

Through CHARGE and RELEASE, "SUPER SAIYAN / RAGE MODE ACTIVATED!" sits above him, flickering red and white in hard steps, then solid red once it lands. Mike: *"dont animate him into kneeling after throwing his arm out, use his hand STOP frame from the hamma fight"*. The kneeling recoup is gone. His feet are lined up across the handoffs: the throw reel drops 38 px as it shrinks, so its feet land at `b.y + 150`, where the STOP and C29 poses stand.

Nothing glows before CHARGE. The charge's whole-body red light (`lit`) was cut to .05-.17: the red pose itself
burns in now, and the old .12-.50 washed his armour to flat salmon.

**The SSJ aura and a visible release (Oct 26).** Mike, with a screenshot of him as a pure white silhouette at the
final strike: *"he should be more visible in this pose, its critical to the super saiyan way and more energy emits
off him like an energy aura"*.
- **The white-out** was the body hit-flash (`C.c45Flash` through `b20Image`) firing on the release, with the core
  glow stacked on top. The release no longer flashes his body. It fires two shock rings, sparks, a shake 18 and a
  lighter screen flash (.18).
- **The aura** (`c45Aura`) is his OWN current pose silhouette dilated 3/6/10 px, coloured gold/orange/red, drawn
  BEHIND him with normal blending. Each layer has a second copy stretched upward from his feet in stepping flame
  tongues (12 fps). It builds from 60% of the charge and blazes in the release.
- ⚠ The first cut used additive blending with three copies per layer, and the nine copies summed to a white blob
  bigger than him: the same failure in a new place. Normal blending, outer layer first.

**Longer release, smooth handoff (Oct 26).** Mike: *"you can flash him. I meant make him stay visible LONGER in that
pose, and make him fade glow into that new form he takes so its a smoother transition"*.
- `chargeEnd` moves .92 -> .80, so the release holds for 1.44 s, not .58 s. He roars into rage frame 9 (arms out)
  and HOLDS it.
- The white flash is back: full white, held, then fading out of him in ladder steps over about 1 s.
- After the charge, a wrapper keeps the aura burning off his settled form and fades it out over `C45_AFTER` (1.4 s).
  The held release pose dissolves into the settled form over 0.6 s, so there is no cut between the two red banks.

## The rage opener (kamehameha) and the orb, fixed (Oct 26)

Mike: *"as soon as he forms and finalizes it, make him fly up, fly into the background, begin moving left and right
fast while gravitating and make him do a kamehameha wave ... the screen darkens as he charges up, energy glows/his
aura glows, and it should be a loud laser blast sound. then make him fly back up north, return to the screen. And do
his new attacks. You may also include his orb laser beam attack ... but of course fix the animations"*.

`assets/chronos_kamehameha_1026.js` (C46, loaded after `chronos_rageform_1026.js`) wraps `c30Start`, so the first time
the rage loop starts it plays an opener on `h.c30` with its own phases. The phases use only art that already ships:

| phase | s | what |
|---|---|---|
| kame_up | 1.55 | `c35DepthFlight` north off the screen, back in at scale .42 |
| kame_strafe | 2.24 | two fast left-right swings (34% of the view), floating bob, dips at the turns |
| kame_charge | 2.6 | C30 cast 0-3 (hip gather); red rage energy ball at his hand (C30 wave head, as authored); screen darkens to .74; `c45Aura` blazing; lane locked at 1.75 s and warned; sounds `warpCharge`, then `hammerEradCharge` x2; shake builds |
| kame_thrust | .36 | C30 thrust |
| kame_fire | 1.6 | his red rage wave (`wave_smooth`, c41Draw red=true; Mike: *"he should be using the red one we had"*) down the locked lane, pixel hit test (`c41Hit`); `fusionBeam` + `expBig` + thunder, a second `fusionBeam` at .7 s; shake 12, flash .3 |
| kame_recover | .55 | the dark lifts |
| kame_return | 1.55 | `c35DepthFlight` back to scale 1, then `c30Retreat` into the normal loop |

- **No DBZ-style charge sound could be generated:** `_BUILD_SOURCE/.secrets.json` (the ElevenLabs key `sfx_gen.py`
  needs) is not on this machine. The charge layers the closest existing cues, and a real one drops in at `c46Sfx`.
- **The orb laser (C42) is back on.** `chronos_kame_1025` had forced `c42Active` to false. It is restored on alternate
  wave turns (cycle%6<3: orb, wave, orb...).
- **The orb's animation is fixed.** It used to hold the cast-5 arms-out frame for the whole turn with a 28 px crop as
  the orb. Now he gathers at his hip (cast 2-3) while a growing, crackling energy orb rides his hand, swings it forward
  (cast 4), and holds it out as the beam fires (cast 5/6).
- **The low-HP damage vents** (`encounterDamageOverlay`) are sized from his full-size box, so in the background they
  floated around his head as big grey clouds. They are scaled to his depth now, and are off during the opener.
- ⚠ **`xartPalette` returns null for every XART cell:** it reads `naturalWidth`, which a canvas does not have. Recolour
  with a `'color'` composite directly.

**Smoother laser poses (Oct 26).** Mike: *"better animation when shooting his lasers like not appearing to jerk his body
so much"*. The fixes live in `chronos_kamehameha_1026.js`:
- **Beams.** The red wave (C30), the orb (C42) and the kamehameha flipped cast 5/6 at 14 fps; they all hold cast 5 now.
- **Palm volleys.** Each C32 shot swung the whole 9-frame twist (0 <-> 8) in .13-.16 s. Now:
  - the twist is half as wide (frames 2/6);
  - each shot holds its pose for 40% of the gap as the recoil, then smoothsteps to the next shot's pose, arriving as it
    fires;
  - the warning stance is the centre (4), not the guard frame (10);
  - the dual shot holds frame 9 for its beat.

  Measured by `probe_palm_1026.py` over one volley: total pose travel goes 155 -> 79 frame steps, and jumps of 4+ frames
  go 6 -> 5. Routing the dual pose through the centre was tried and measured worse (12 jumps), so it was reverted.

## Forms

| Form | Rim | Lit | Cores |
|---|---|---|---|
| regular | cold blue, slow | faint blue | breathe slowly |
| `fr_activation` | cyan, faster as plating builds | strobing cyan, capped low | fast |
| chrome | cyan/white | cyan | normal |
| rage charge | red/gold, strobing faster in hard steps | red, brighter per step | fast |
| rage | 6 shells red/orange/gold (no dark reds: added over blue space they turn purple) | red | normal |

Shake escalates through both transformations. The bursts when a form lands are unchanged: rage gets
fxBurst, shake 22 and a flash; chrome gets fxBurst, shake 14 and a flash.

## Traps found on the way

- **The first big plate drawn in rage is a faint halo copy, not the body.** An aura that multiplied
  `globalAlpha` inherited the copy's low alpha and nearly vanished. Every draw here sets alpha absolutely.
- **A state jump in a probe fires the transformation burst**, and its shock ring then sits frozen over the
  chest in every later screenshot, which looks like a white disc bug. The probe pins `_cgPrev` and clears
  `particles` per state.

## Verified

`python _BUILD_SOURCE/probe_chronos_glow_1025.py` passes **18/18** in real Edge on the live `index.html`:
- the aura sheets decode;
- every form renders differently with the layer on vs off;
- shake builds through the rage charge;
- the rage and chrome bursts fire on the real state transitions;
- frame cost in rage stays within 4 ms of the layer-off draw (measured +0.3 ms before the core pass);
- there are no layer or browser errors.

Contact sheets: `_shots/chronos_glow_1025/forms_off_on.png` and `film_contact.png`. Silent clip of both
transformations: `_shots/chronos_glow_1025/chronos_glow_transformations.mp4` (`film_chronos_glow_1025.py`
drives the real state clocks).

`test_fl.js` does not load this layer, and it currently exits before assertions on the missing
`retired_art_archive_1022.cjs`, so it was not used as evidence. No commit or push.
