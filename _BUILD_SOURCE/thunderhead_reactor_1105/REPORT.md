# Thunderhead — connected cannons, coordinated batteries and reactor depth launch

November 5, 2026. TC119 extends the approved TM115/THS114 Thunderhead.

The existing wind beams now attach to the physical cannon fan/outlet through
an animated coupling. A separate source-derived lower metal lip overlaps the
beam throat, making the energy read as emerging from the cannon. Coupling
recovery uses authored frames, and destroying the cannon cancels its beam.

Four actual independently targetable machine-gun batteries acquire living
allied aircraft. Three select different allies while a rotating lead battery
selects the player in three of every four firing cycles. The fourth cycle
uses allies for all four. Assignment follows real native ship objects rather
than dummy coordinates. Guns reserve targets through a 0.92-second Retina/FOV
windup, commit after 0.62 seconds, then fire alternating-barrel wind slugs for
0.95 seconds. They rotate through 32 authored headings, recoil, show anchored
muzzle flashes and play independent heavy-gun cues. Target loss stops fire;
unavailable allies are not replaced by imaginary targets. Destroyed batteries
stop acquiring, warning and firing. Slugs remain unshootable from birth.

The glass chamber now contains the actual approved cyclone texture, rotating
and travelling north across its two glass sections. Its metal collar, central
brace, seams and silhouette remain intact. Chamber playback/emission
accelerates during charge. Storm clouds and rain remain over the city, while
16 authored shade steps darken it. Energy/wind rumble is routed through the
shared mixer. Every actual ground lightning impact gets the existing loud
Chronos/Dracodia strike cue. The live metal warning replaces the disabled
legacy symbol function.

The giant cyclone's attack is now a complete flight sequence: turn north,
leave above view, return south at background depth, charge the chamber,
launch from the distant core and kick backward, recover, turn north, exit,
then return south to the foreground. Sixteen authored ship depth sizes keep
the entire modular assembly, guns, outlets and exhaust registered. A ground
Retina shows the cyclone's committed foreground point for its final
0.85-second release warning. The projectile grows through sixteen authored
sizes while spinning and travelling into the foreground, then exits. Its
contact respects native player protection and is bounded to one hit per
seat. The distant form cannot be targeted or damaged.

Destroyed modules leave their mounts as complete coloured parts. The native
unitDeathFX owner supplies the engine's explosion family/coverage rules.
The detached part moves and turns, then explodes into four finite physical
shards. Receivers and anchored smoke remain on the hull, without full dark
weapon-shaped wreck plates. Cannon destruction also interrupts its beam.

Native health remains **6,348 HP**: four 762-HP batteries, two 889-HP cannon
pods and a protected 1,522-HP core. All six modules gate that core. Native
damage, white hit feedback, Retina, rewards and once-only defeat remain the
authority. Hard, Stage X, Rough Riders and Razorwake keep their routes.

## Artwork and source

No external generation was used or charged. This pass re-authors the
approved TM115, THS114 and RW118 pixels. There are **3,127 frames in 158
banks**, packed into 189 compact pages (229.5 MiB decoded). The unused
intermediate north/turn/charge banks are excluded. All rotation, depth,
emission, fades, coupling recovery and debris are authored offline. The
renderer uses ordinary source-over blits and selected fixed frames.

Editable Aseprite sources, strips, manifests and the reproducible builder
are retained under `_BUILD_SOURCE/thunderhead_reactor_1105/`. Its runtime
owners are `assets/thunderhead_reactor_1105.js` and its art registry, loaded
after RW118. `assets/game.js` is unchanged.

## Verification and practical limits

- **31 native checks pass**, including actual beam pixels and anchors,
  75% player assignment with distinct allies, live gun fire, all six pools,
  real white hit pixels and expiry, warning, chamber/flight clocks, depth
  protection, perspective launch/growth, lightning cues, bounded unshootable
  bullets, breakaway/shards, beam interruption, pause, retry and native defeat.
- **3,127/3,127 frames** pass actual Aseprite re-export and packed visible
  RGBA/alpha comparison. All cells are even and fixed per bank. All 64 source
  gun/recoil masks match their actual alpha. Sprite edges are unclipped;
  the background shade tiles intentionally have full-bleed edges.
- Full-quality real-RAF diagnostics measured **55.31 FPS while observing**
  and **58.72 FPS with sustained player fire**, with no page errors. These
  are measured desktop results rather than a locked-60 guarantee.
- Final full native fight: **56.75 engine FPS over 140.885 seconds**,
  70 seconds player hold-fire, then an input-only Cole GOD bot. Native allied
  AI and weapons stay active throughout. Native 6,348 HP, module pools,
  attack clocks, sounds and defeat remain in force; no enemy HP/phase/timer
  writes occur after spawn. Capture is the 960×1024 high-quality native
  canvas at 30 FPS media. Audio peak: **-1.8 dB**. Source stability,
  video/audio decoding, audible playback and browser/asset checks pass.
- **14 preview checks pass**, including video, audio, seeking, exact
  byte-range delivery and mobile fit.
- Syntax and Windows-line-ending-aware whitespace checks pass. The required
  older `test_fl.js` suite still has its existing
  `difficultyHealthBaseline15 is not defined` dependency failure. The log is
  retained; this is not a full-suite pass.

These are scoped native fixtures and a GOD-bot encounter film. Human
dodgeability, campaign completion and a complete hardware matrix have not
been established by this pass.

Review: http://127.0.0.1:65122/?thunderhead=reactor-final-1105#thunderhead

Movie: `_shots/boss_comparison_1102/thunderhead-reactor-final-1105/stage6-boss/stage6-furious.mp4`.
Evidence: `docs/qa/thunderhead_reactor_1105/`.

No commit or push was requested.
