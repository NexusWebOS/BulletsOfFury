# Black Event Horizon alien symbiote pass — October29

[Full Furious fight](http://127.0.0.1:51046/?horizon=symbiote-1029#clip=stage9-miniboss) · [Eye sweep](http://127.0.0.1:51046/?horizon=symbiote-1029&chapter=sweep#clip=stage9-horizon-eye-sweep) · [Aqua spinning dash](http://127.0.0.1:51046/?horizon=symbiote-1029&chapter=dash#clip=stage9-horizon-dash)

Stage9's miniboss now moves and attacks as an alien spacecraft. This pass does not revise the Stage9 main boss or Dracodia; the current void/space arena is retained.

## Attack book

The centered optical eye, whole ship, damage mask and lasers share the same physical pivot, including the shared space-hover displacement.32 normalized authored views let the hull rotate while hovering and recovering through bounded lateral/vertical motion. The eye's source pixels brighten during charge; a shared filled green/yellow/red360 warning disc and rotation symbol precede spinning attacks. Locked straight beams/orbs use their actual committed shot lane.

The opening book is two spiraling laser arms, a locked straight beam, a complete360-degree eye sweep, three charged symbiote plasma orbs and a spinning radial laser volley. Spirals use contiguous segment collision along the authored energy tiles. Beam collision goes through native playerHit and respects roll, somersault, shield and invulnerability. Ordinary laser/orb rounds cannot be shot down and retain defensive-clear ownership. Shots have a120-owner budget and five-second lifetime; the real recording peaks at60.

At50% of the actual native HP pool, incoming damage is clamped to the threshold and a2.4s protected transformation starts. Aqua source-pixel hull emission, a white eye and three hull-attached smoke emitters appear. The second book alternates warned spinning dash passes with the laser/orb attacks. It retreats beyond an edge, commits the player's current route, holds a1.15s edge warning, then crosses to the other side in1.05s while rotating and firing lasers forward and to both sides. A400px warning lane covers the complete spinning side-beam danger; an edge asterisk marks the entry. Horizontal and vertical passes alternate, followed by offscreen recovery and a smooth north return. Native Retina/damage targets disappear only during protected transitions/offscreen travel; visible dash/return windows remain vulnerable.

## Art and ownership

PixelLab supplied source-referenced hull motion, a symbiote laser master and an alien orb. The provider motion did not complete a uniform full turn: measured eye centers/headings,16 selected first-half views and authored opposite views build32 consistent angles without per-frame fitting. One scale per bank, fixed even cells, shared transparent padding, stable optical pivot, authored normal/aqua/hit/eye/beam/dash/orb/smoke banks. All rotations, glow, alpha and sizing are baked offline in Aseprite; runtime uses source-over fixed-cell blits. Dark armor highlights were lifted for readability; eye glow is isolated from blue fin reflections.11 banks use131.0MiB decoded. The generated credits charged total$0.2192. Job details/selected masters and exact normalization inputs are archived beside the art.

Owner: assets/horizon_symbiote_1029.js, loaded last after WS56. Existing native10965HP Furious pool, core/whole-hull damage, white hit pixels/expiry, native defeat, score and progression remain. There is no health refill or independent death controller. The shared space-hover upcoming offset is included in laser source and dash contact calculations; it is not a detached eye overlay. Stage exit/death cancels owned live beams and shots.

## Verification

- 26 native gameplay/pixel checks, 11 art checks and 16 film/player checks pass. A non-GOD laser collision consumes the actual native player shield. Actual white damage pixels and timer expiry are verified.
- Full native Furious film:164.77s, native defeat at158.64s,58.89native FPS. Real RAF, input-only invulnerable Cole observer; no enemy HP, phase or timer writes. Starts with Laser5/40 missiles; the native space loadout subsequently reports Laser1. GOD footage verifies behavior/presentation, not human difficulty balance.
- All five opening attacks, half-health transition, multiple dash releases/finite returns, matching eye/body positions, bounded ordnance and native defeat occur in the recording. Six seekable chapters added to the existing gallery; older media preserved. Decoded charge/beam/orb/dash sound cues are present; audio mean-19.4dB, peak-3.5dB. No browser, engine, asset, audio or bot errors. Decoded spiral, aqua and dash frames inspected.
- Syntax checks pass. Required full suite reaches its final summary and exits1 with the same five baseline failures: flash hold, opening jump dialogue, jump/chromium order, opposite StageX route persistence, StageX right-branch encounter. game.js and test_fl.js are unchanged by this pass.

Rebuild: _BUILD_SOURCE/build_horizon_symbiote_1029.py --aseprite <path>. Native fixture: _BUILD_SOURCE/probe_horizon_symbiote_1029.py. Native recorder: _BUILD_SOURCE/record_horizon_symbiote_1029.py. Archived evidence: docs/qa/horizon_symbiote_1029.json. No commit or push requested/performed.
