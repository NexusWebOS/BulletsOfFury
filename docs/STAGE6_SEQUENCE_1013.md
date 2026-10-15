# Stage 6 sequence and solo miniboss repair — October 13, 2026

Mike reported ordinary enemies appearing during the Rebel introduction while
firing was disabled, and friendly pilots helping against the Stage 6 miniboss.

The core dialogue gate did not contain the later formation wrappers. VP12 could
advance and spawn while the older story code was holding the player's controls.
`stage6_sequence_1013.js`, loaded after the combat extensions, gives each locked
Stage 6 scene sole ownership of its update. It calls the existing native intro,
pre-choice radio or rescue controller, including their actual motion and sound.
It does not run the ordinary wave/formation controllers behind that scene.
VP12 also explicitly respects `h3Locked()` and the cinematic director.

Scene entry retires outgoing ordinary enemies, hazardous bullets, turret burst
queues and transient combat effects without kill rewards or chain explosions.
Pickups are hidden only during rendering and remain available afterward. The
scene's private, noncolliding weapon demonstrations still animate. The AV3 sound
cue clock continues; old sustained combat loops stop on entry. Native firing
becomes available again after the introduction finishes. The existing live
GANG callout continues to allow combat; it is not a locked cinematic.

Independent review caught one visual lifecycle omission in Cole's pre-choice
demonstration. The isolated update now advances the fusion reel clock, authored
impact effects, short muzzle flashes and weapon release reels without polling
gameplay input. Demonstration rounds clear as soon as the dialogue leaves that
beat, so no frozen shot or muzzle carries into the following caption.

During the Stage 6 miniboss warning/fight, friendly wing ships are suspended,
their existing tagged bullets are removed, their draw/arsenal paths are gated,
and the ally pressure multiplier is neutral. The surviving approach wing
returns from below after the native miniboss death completes. The boss and
Rebel encounters retain their separate ally rules.

## Verification

- `_BUILD_SOURCE/probe_stage6_sequence_1013.py`: 56/56 native Edge assertions
  across Easy, Normal, Hard and Furious. Actual Right + Confirm route input,
  natural Rebel intro completion, restored player firing, actual miniboss
  spawn/hit/death and returning wing. 10,298 individually observed intro frames:
  zero ordinary enemies, zero hazardous bullets, zero stage/formation timer drift.
- `_BUILD_SOURCE/probe_stage6_cinematics_1013.py`: 30/30 native Chrome/Firefox
  checks for final visible scene cleanup, preserved pickups, animated private
  weapon demonstrations, rescue/pre-choice scenes, continuing cue clocks and
  preservation of the live GANG callout. Six added checks per browser verify
  Cole's native demonstration, visual expiry and shot cleanup without resuming
  normal input or hostile combat. Zero page/console errors in both probes.
- Inspected actual game pixels in `_shots/stage6_sequence_1013`: solo Tempest,
  wing return, clean introduction, Rook's native demonstration, Decker rescue,
  pre-choice radio, and Cole's charge/release/next-caption frames. No replacement
  renderer or synthetic sprites used.
- Module JavaScript syntax check passes. The parent task owns the required
  combined `assets/game.js` syntax and full `_BUILD_SOURCE/test_fl.js` run.

Combined portable result: `docs/qa/stage6_sequence_1013.json`, 86/86 checks.
The 56 difficulty/solo-miniboss checks preceded the final visual-lifecycle-only
repair; the 30 cinematic checks verify that final revision.
The initial probes had sampling/setup errors: clock comparisons included up to
one second of resumed combat, and one fixture expected the retired locked GANG
scene. Those initial reports remain in the ignored screenshot directory. The
corrected probes watch the actual locked interval and current live callout.
Tests are controlled native observation fixtures, not a human playthrough or
an assertion about physical-controller response.

Local change only. No commit or push.
