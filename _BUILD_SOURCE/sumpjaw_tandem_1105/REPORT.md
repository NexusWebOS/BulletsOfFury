# Sumpjaw — coordinated jumping pair and one shared health bar

November 5, 2026. SJ120 extends the existing approved SJ98/SS116 serpents.

The two floating health bars are replaced by one top-screen gauge. Each snake
permanently owns half: the left half is snake 01, the right half snake 02.
Killing either empties precisely its share while the other keeps its own
remaining health. No refill or transferred health occurs.

Base Furious HP is **14,000 total**, **7,000 each**, compared with **12,466 HP**
for the actual Hard Stage 7 boss in the matched native fixture: about 12.3%
more health. Each snake retains two 1,750 HP toxic gills and a protected
3,500 HP intake heart. Both gills must break before its heart takes damage.
NG+ still scales the complete pair to 17,500 HP, with equal 8,750 HP shares.
Hard's original Dredger and Warden encounters are unchanged.

The shared attack director performs six consecutive left/right leaps,
alternating high and low paths. The lower arc crosses the pilot's ground row
while airborne. Shadows stay on the floor; the visible head and its actual
gill sockets remain hittable in the air. Landing reticles mark committed
landing points. The snakes fire straight down from their real mouths while
passing overhead, with a point-blank shot guard.

They then align in a separated horizontal row, charge their mouth cores,
and strafe together while firing rapid dual large-orb bursts. Each mouth
fires every 0.14 seconds during 0.86-second bursts with brief gaps. They
split-hop apart, jump offscreen north, cross in opposite directions at
different heights, and return. The remaining snake uses faster solo jumps
and 0.105-second firing bursts instead of waiting for a dead partner.

All little acid/spread pellet emissions are removed from this encounter.
The only new rounds are the existing 72px toxic-orb artwork, travelling
straight down at speed 5.2. Their actual collision radius is 24px. They are
ordinary unshootable enemy ordnance from birth, have a 3-second maximum life,
and are capped at 44. Native pool breaks, death and retry clear owned rounds.
High overflight does not have body contact; low landings use native player
protection and hit/death rules. Floor shadows never absorb weapons.

The whole-body and tail green outer hot frames are no longer drawn when
charging or firing. Instead, authored emission pixels animate only inside
the original toxic mouth core, with four levels, an eight-cell source-timed
loop, both jaw positions and all 32 headings. The source's held frames are
preserved. No emission alpha extends onto armor or outside the mouth mask.
A small mouth-local ooze flash accompanies each launch. Native white hit
flashes still appear on the body and trail, then expire to normal material.

Toxic launch, heavy-gun pulse, charge, jump, landing, module break and death
sounds use the shared mixer and retrigger gates. The full recording contains
597 toxic-spit, 328 enemy-heavy-gun and 81 landing cue plays, with decoded
game audio and no audio tap errors. These counts include the complete fight,
not a synthetic sound montage.

## Artwork and ownership

No external image generation or generation credits were used. Existing
approved source pixels were re-authored offline into **2,066 frames in four
banks**, on six compact pages: 1,472,019 compressed bytes / 9.20 MiB decoded.
Mouth cells are fixed 176×176, local flashes 48×48, the shared frame 400×28
and its clipped half-fill 190×4. All dimensions are even with fixed pivots.
The complete rectangular UI border/fill intentionally have full-bleed edges;
creature effect cells have transparent padding. Runtime draws only selected
authored frames, with ordinary source-over blits and health-fill clipping.

Owners: `assets/sumpjaw_tandem_1105.js` and its art registry, loaded after
TC119. Editable Aseprite sources, strips, manifests, runtime snapshots and
rebuild/verification helpers are in `_BUILD_SOURCE/sumpjaw_tandem_1105/`.
The original native pool, damage/Retina and once-only defeat owners remain.
`assets/game.js` is unchanged. No commit or push was requested in this pass.

## Verification and limits

- **26 focused native checks pass**: all attack families, real jumping
  paths/heights, aligned dual fire, only large downward orbs, no outer hot
  frames, actual mouth playback, visible-air targets, four gill gates,
  actual white hit pixels/expiry, one fixed 50/50 bar, solo behavior,
  unshootable bounded rounds, pause, retry, six pools and one native defeat.
- **6 compatibility checks pass** for Hard Stage 7, both current
  Stage 6 alternates, NG+ health/pool scaling and browser errors.
- **2,066/2,066 frames** pass Aseprite roundtrip and compact-atlas visible
  RGBA/alpha comparisons. All 2,048 emission frames match the exact rotated
  original mouth mask; every emission level animates with distinct frames.
- Uncaptured high-quality native playback measured **59.54 FPS observing**
  and **58.81 FPS with sustained player fire**, without page errors.
- Full fresh real-RAF fight: **57.34 average engine FPS** over
  **298.703 seconds**, with 60 seconds hold-fire before an input-only
  Cole GOD bot attacks. No enemy health, phase or timer writes occur after
  spawn. All gills/hearts are destroyed with native player weapons and
  missiles; native rewards/progression finish. 960×1024 native canvas,
  30 FPS media, audio peak **-2.1 dB**. Source stability, full decoding,
  audible playback and browser/asset checks pass.
- **14 preview checks pass** for actual video/audio, seeking,
  byte ranges, mobile fit and browser errors.
- Syntax and Windows-line-ending-aware whitespace checks pass. The required
  older `test_fl.js` suite still aborts before its final summary at the
  existing `difficultyHealthBaseline15 is not defined` dependency failure in
  `combat_polish_0927b.js:151`. Its fresh log is retained. This is not a
  full-suite pass.

The higher HP, faster cadence and paired choreography establish a stronger
encounter budget; they do not prove human difficulty. The GOD bot blocked
447 native hits during this recording. Human dodgeability/balance testing,
complete campaign testing and other machines remain unverified.

[Watch the revised full fight and attack chapters](http://127.0.0.1:65123/?sumpjaw=tandem-final-1105#sumpjaw)
