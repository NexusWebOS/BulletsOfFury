# Stage6 reactor, radio and Harrier repair — October18

Later correction: the main Harrier has no energy core, is enlarged, and keeps
the allied wing in combat. Only the Fortress miniboss retains its reactor.
See [the current Harrier and wing notes](STAGE6_HARRIER_WING_1018.md).
The solo-wing and main-reactor descriptions below record the earlier build.

Native reproduction confirmed that the Fortress miniboss's radio line existed
but remained at age0 while its allied-wing controller was parked. Its old
bottom-HUD frame and talking portrait drew, but the stopped typewriter clock
left the words blank. Destroying all six batteries
made the reactor logically targetable, but the whole closed hull stayed on top
of it. The newer modular Harrier never called the original bay-launch or
carrier-to-Nightwing sequence: its bay stayed shut, no fighters launched, and
reactor destruction immediately awarded stage clear.

`assets/stage6_reactor_1018.js` reconnects those mechanisms through the actual
runtime. No replacement art, new atlas cells, procedural sprites, commits or
uploads are involved.

- Stage6 combat radio renders in the approved side-HUD pilot well, including
  both co-op rows. Compact mode uses its score compartment. Caption clocks run
  independently while the allies are intentionally parked during the miniboss.
  Flight and attacks continue. The existing speaker/portrait/route owners stay
  in control; this does not add synthesized voice recordings.
- The Fortress reactor sits on its measured original cyan vent at source
  `(512,251)`. Six destroyed laser batteries start an0.85s sliding-hatch
  animation. The existing vent leaves move over an authored animated blue energy
  cylinder from `mr27_corefx`; one proportional scale and a stable centre are
  used. The core becomes targetable/damageable when the opening finishes.
  Primary shots, continuous beams, area hits and Retina share `sc13Core`.
- The Harrier keeps its eight independent modules: two fans, four laser
  batteries and two missile racks. Its separate bay opens over0.65s and
  launches the real `xelite_hivewing` actors through the original safe launch
  and peel controller. Normal retains four live escorts; Hard/Furious retain
  five. Bay leaves close again; the original south departure/scaled return
  continues. Replacements reuse vacant formation slots and preserve survivors'
  HP. The bay's open state does not expose the reactor while modules survive.
- Destroyed fans produce repeated authored fire bursts and rising smoke at
  local fan coordinates. They follow translation, depth scale and the falling
  carrier. A bounded spring drift and small vertical/lateral tremor model the
  pilot countering lost thrust. Art, muzzle positions, targets and hitboxes all
  share the translated whole hull. Fan opacity follows the carrier's death fade.
- All eight modules must be destroyed before the Harrier reactor's own0.85s
  protected opening. Its animated energy core then accepts normal gunfire and
  Retina missiles. Reactor destruction enters the original falling-carrier
  controller on the same boss object, with no early clear, reward or unlock.
  The existing giant blue Nightwing emerges after2.4s and takes over after4.4s;
  its native evasions, attacks, hit feedback, death and Stage6 reward path remain.
- Existing owner/part `markHit` feedback is retained. The miniboss now also
  marks each struck battery and its core, ages flash timers in simulation and
  renders the battery flash reliably. Native pixels and expiry were checked.

Small supporting edits are in `stage6_carrier_1013.js` and
`stage6_roster_1017.js`: flash paths, separate bay state and a draw-only archived
carrier source for the fall. Loader tags were updated. `assets/game.js` and
`_BUILD_SOURCE/test_fl.js` were not edited by this repair; LF and CRLF remain.
StageX's legacy Harrier and the alternate Rebel branch retain their controllers.

Validation: `node --check assets/game.js` and all changed runtime files passed.
The full required suite reached `FALVA/LIZZIE BUILD OK, 0 ERRORS`,8791 passing
assertions,0 failures, exit0, matching the prior baseline. Native Edge:

- `probe_stage6_repair_1018.py`:82/0 on Normal, Hard and Furious. Actual J
  gunfire damages batteries and exposed cores; five broken batteries / a
  remaining fan or rack block premature exposure. Bay motion, real elite
  gunfire, capped escorts, native departures/returns, attached smoke/fire,
  momentum and continuous carrier-to-ace-to-clear were checked.
- `probe_stage6_review_1018.py`:14/0. Full-FOV review controls, actual core hit
  pixels and expiry, replacement slots/survivor HP, non-pausing captions, co-op,
  compact HUD and StageX/Rebel controller compatibility were checked.
- Existing `probe_modular_1017.py --only 6s,6b --weapons mg,lock,laser`:
  six hit-routing cases passed,0 failures, exit0. Its old fixture wrote only
  `b.x` while the carrier followed the live camera, causing Retina to report an
  obsolete fan position. It now follows these actors' actual moving targets,
  isolates the base MG from the earned chaingun/Forge/pickups, isolates connected
  gamepads in automation, and returns nonzero for a missed piece or browser error.

No game page, console, draw or missing-asset errors occurred. Some local static
server requests were cancelled normally when browsers closed. These fixtures
verify Stage6 encounters and their branches, not another nine-level campaign or
a human balance/mix assessment. Earlier Stage6 completion records describe the
pre-repair build and did not establish the missing visual/ace sequence.

Review: `docs/previews/stage6_repair_1018/index.html` uses the actual game and
isolated save keys. Six scenes cover the miniboss, reactor openings, Harrier
bays, broken fan and blue-ace emergence. QA: `docs/qa/stage6_repair_1018.json`.
Logs and inspected before/after captures: `_shots/stage6_repair_1018/`.
