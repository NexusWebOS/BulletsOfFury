# Dracodia forms and final life â€” October 26

Mike requested a full Furious recording, animation/attack upgrades for the remaining forms, and a base body whose arms and life cannot be destroyed until all other forms have died.

## Runtime ownership

`assets/dracodia_forms_1026.js` loads last in `index.html`. It supplements the existing V18/V19, HC22, NB23, PH21/BI24, D20/DR21 and cinematic owners. It does not replace their health budgets, native attack books, warnings, defeat routing or rewards. No `game.js`, atlas, original art, or test-suite implementation changes are required.

The final encounter retains five native pools: base 5330, Hammer 4920, helicopter 3690, Neural Archon 4510 and Phoenix/volcano 4100 on Furious. The base's health and arm modules are protected while any of the four copy pools remains above zero. Early base hits produce native white hit feedback, a shared-mixer shield cue and a brief synthetic-code ward response. Protected pieces expose no Retina attack target. Direct part-break, base-break and finale routes are guarded too. No damage is silently healed back afterward.

After all four copies die, the full base life opens and its arms can break into real source-alpha fragments. The native final death and reward sequence remains the sole completion owner. The original infused drone host remains separate: its 33.3/33.3/33.4 arm/core damage sequence is unchanged.

## Animation and attack changes

- Base, helicopter and brain loops blend cyclic authored frames at fixed pivots. Phoenix windup, flight and recovery interpolate the original whole-body bank and the corresponding measured cannon sockets.
- Form changes disassemble the actual outgoing pixels, rotate the approved skeletal carrier inside magenta synthetic DNA, and assemble the actual incoming form in scan bands. A full playfield white flash covers completion before the new form becomes fully visible. The handoff follows one continuous position and retains original health. Each change takes 3.9 seconds; existing protected cinematic modes own it.
- Base visits advance a persistent native attack-book cursor instead of restarting the same opening attacks. Three completed attacks precede a safe form change; archive helpers, storms and barrage interlocks still have to clear.
- The old base ghost-hop moves continuously between committed points, with code trails and the approved fusion-energy cue. It keeps native warning and slam recovery ownership.
- The base scythe attack uses the authored 24-pose whole-body strike animation. Its warning commits the target, its lunge returns smoothly, and collision samples the actual visible non-core part mask during the active interval. Furious tell/active/recovery are 1.08/.78/.80 seconds.
- Original emissive body pixels brighten in stepped charge states. Hammer energy, helicopter barrel effects, Neural Archon eye charge/beam muzzles, and Phoenix cannon/talon effects follow their live owners and measured sockets.
- Final-form symbiote shots use authored energy-ball art and attached muzzle flashes. These ordinary energy rounds reject offensive interception from creation, retain defensive clears, and cancel when their owner/form/module is lost. Physical missiles preserve their own rules.
- Helicopter muzzle callbacks expire with their original form/proxy. This fixes an old callback reaching retired Harrier socket code after switching to the Neural Archon.

## Verification

Native fixtures in `_BUILD_SOURCE/probe_dracodia_forms_1026.py` select forms and apply native damage only for isolated checks. The full film uses `_BUILD_SOURCE/record_dracodia_full_1026.py`, real RAF, native boss-mode entry and input-only aiming; it does not write enemy health, phases or timers. Native GOD keeps the observer alive and is labeled in the film.

Current focused probe: 21/21 passing, including visible hit pixels/expiry, protected health/modules, all four copy deaths, final-life unlock, arm shatter, complete native finale, continuous fusion anchors, flash concealment, authored scythe frames/recovery, energy interception and zero page/update/draw errors. Native screenshots are under `_shots/dracodia_forms_1026/probe/`.

The entrance regression passes 22/22 and the full final-download regression passes 48/48, totaling 91 native checks. The complete 16:58.481 Furious film passes 28 health-ledger, decode, audio and Chromium playback/seek checks. It averages 59.61 native FPS, has a decoded audio peak of -0.3 dB, and has no game/browser/bot/asset errors. Every copied pool reaches zero before the base opens; the base then dies through its native finale and portal ending. Evidence: `docs/qa/dracodia_forms_1026.json`.

Film: `_shots/dracodia_forms_1026/full/stage8/stage8-furious.mp4`. Chapter controls: `docs/previews/dracodia_forms_1026/index.html`. The recording uses an invulnerable input observer, visibly labeled, with native enemy health, timers and progression.

`node --check assets/game.js` and the new runtime syntax check pass. The required `node _BUILD_SOURCE/test_fl.js` still exits 1 before any assertion/final summary: `_BUILD_SOURCE/retired_art_archive_1022.cjs` is missing. This is the same recorded prerequisite failure as the preceding cinematic passes; do not represent the full suite as passing.

No commit or push. Preserve other chats' staged, unstaged and untracked work.
