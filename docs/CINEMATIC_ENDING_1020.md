> SUPERSEDED by Mike's invasion/resurrection ending. Current direction: [CINEMATIC_INVASION_1020.md](CINEMATIC_INVASION_1020.md). Earlier epilogues/no-uplink plot remains historical.

# Cinematics and proper ending — October20,2026

Main Bullets of Fury. Mike requested that cinematics match Dracodia's demonic
machine identity, use the actual pilots and aircraft, and resolve the game.
No changes to combat health/damage, stage order, awards or campaign unlocks.
No new pilot or aircraft likenesses were generated.

## Current sequence

| Native ending time | Scene |
| --- | --- |
|0–3s|Selected original front-view aircraft emerges from the existing void portal.|
|3–9.4s|Original rear-view aircraft descends toward Earth and approaches Fury HQ.|
|9.4–26.4s|Physical touchdown, disembarkation, walk through the HQ doorway and fade.|
|26.4–31.6s|New dawn command gallery. Dracodia's destroyed core and terminated invasion signal are confirmed.|
|31.6–37.6s|A distinct resolution for each of the nine actual pilots.|
|37.6–42.8s|The actual squad assembles; the player gets an explicit victory before the sequel hook.|
|42.8–49.8s|Pilot cast credits and thanks.|
|49.8–53.3s|Post-credits: damaged orbital relay, severed uplink, tiny existing mechanical parasite.|
|53.3–56.3s|Federation reports a different, unidentified deep-space contact.|
|56.3–59.6s|Existing approved sequel silhouette. It is not presented as Dracodia returning.|
|59.6s onward|Resolved final card, selected victory portrait, score and native Start-to-title input.|

The standard campaign branch keeps its original homecoming-to-card route;
Arcade retains its native short score card. The complete ending still requires
the earned `_trueFinaleCleared` flag. The native Dracodia defeat, escape portal,
reunion, single reward and stage-clear flow remain the authority.

Co-op shows both original selected aircraft throughout the homecoming. The
second pilot disembarks one second behind the first, follows a converging
physical route to the actual doorway, and appears on the final card. The final
score displays both players' score sum without changing either stored score.

## Story/identity consistency

- Dracodia's monologue now describes a will from the dark inhabiting machines
  and code. Its full-body performance uses the actual combat Colossus core and
  limbs, anchored at their existing joints. The speech portrait is cropped from
  that same combat core, inside the existing authored bezel.
- Actual native A reveals/advances a line; Start finishes the speech through
  its original combat handoff. HP, protection release and reward ownership are
  preserved. Existing authored pad prompts display these controls.
- Non-live mission dialogue uses actual pilot body/portrait assets instead of
  unrelated generated cockpit busts. Interactive HQ radar, live Rebel dialogue,
  Cronos and the director's branch/callback logic retain their existing owners.
  The approved Cole/Decker lab hug artwork is preserved as an intentional
  upper-body action shot, keeping its original dialogue physically consistent.
- The orbital reveal shows the actual demonic machine model. Existing October19
  mechanical emergence/contact plates and parasite banks remain the identity
  references; the obsolete organic takeover no longer appears in the ending.
- Narrow caption headings and body text fit separate bounded areas. The squad
  stands in two grounded rows on narrow displays and a line on wide displays.
- Scene fades and seek-aware cue latches avoid flashes and missed-cue replay.
  No new voice recordings were fabricated. Existing music and mixer cues remain.

## Art, loading and ownership

Two built-in image_gen environment-only plates: the dawn debrief gallery and
the severed orbital relay. No people or aircraft were baked into either plate.
The1672x941 original pixels are preserved, with a single bottom row of padding
to even1672x942 exports. Lossless WebP payload:4,901,736bytes. No stretching,
per-frame fitting, atlas edits or runtime bitmap generation of characters.

- Runtime: `assets/cinematic_ending_1020.js`.
- Registry: `assets/cinematic_ending_art_1020.js`.
- Shipping plates/manifest: `assets/game/shared/cinematics/cinematic_finish_1020/`.
- Rebuild: `_BUILD_SOURCE/build_cinematic_finish_1020.py`.
- Raw masters, exact prompts and direction: `_ART_SOURCES/cinematic_finish_1020/`.
- Thirty-seven real XART/drawImage identity exports: that folder's `references/`.

The old ending assets remain preserved for archival previews. The current
ending key list and stage-loading path exclude83 retired organic-infection
textures:66,086,208 decoded bytes, about63.03MiB. The scoped preload guard is
restored with `finally`; it does not alter archived previews outside loading.
Portrait caches are bounded by the16 actual combat frames; body trim bounds are
cached once per pilot. No offscreen surface is allocated per cinematic frame.

## Native review and verification

Play/seek/select pilot/co-op/ending branch in the actual game renderer:
`docs/previews/cinematic_finish_1020/index.html`.
Recorded movie: `_shots/cinematic_finish_1020/ending-native.webm`.
The66.071-second native canvas movie is silent; the interactive preview plays
the original music and sound cues. Its container is remuxed without re-encoding
the frames so duration and seeking work normally.

Final native reports:

-80/80 pilot identities, epilogues, layouts, branches, all nine post-stage director callbacks,
  cue crossing/seek silence and retired-load dependency checks.
-32/32 co-op ships/walk/score, actual keyboard scene/speech controls, all four
  difficulty death-to-portal transitions, full-engine armor expiry, original
  reunion/one reward/earned ending entry and three decoded mixer cues.
-8/8 playable review controls, narrow layout and complete real-time recording.
-11/11 saved-film finite duration, nine decoded scene frames and browser errors.
-Total131 focused checks, zero browser/draw/missing-asset errors. A final8/8 UI
  smoke test additionally checks pause, resized paused rendering, the alternate
  co-op pair and the seekable video on the final cache revision.

The required whole-game suite reaches BUILD OK/0 errors with8,938 checks and
exit0. Syntax checks cover game.js and both new runtime files. No game.js or
test_fl.js edits were made by this pass; prior LF/CRLF and unrelated dirty work
are preserved. No commit or push was requested for this pass.

Fixture notes: initial resize capture could be cleared by a queued resize
between drawing and encoding; final snapshots repaint/encode atomically.
An isolated boss-only tick leaves global debris frozen; final normal-difficulty
death evidence advances the actual whole engine and verifies armor expiry.
Raw MediaRecorder WebM has streaming duration; the final saved container has
finite duration. These were verification/capture repairs, not invented gameplay
fixes. This is cinematic and encounter-flow verification, not a full new
campaign playthrough or a cross-browser FPS guarantee.
