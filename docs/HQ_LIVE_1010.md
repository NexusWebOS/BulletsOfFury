# Live Fury HQ cinematic — October 10

Mike requested an animated, interactive command-room map with beeps, moving
contacts and a filling radar, and actual ship references for every cinematic
generated from now on. The Stage 5 homecoming/HQ attack bridge now uses the
live scene in the normal game. The campaign's active cinematic director owns
its dialogue and continuation.

[Play the live cinematic review](previews/hq_live_1010/index.html). Choose a
pilot, play the four-shot sequence with sound, or open landing, attack, radar
and scramble separately. The review embeds the real game renderer and input.

## What changed

- Two-second acquisition fills the radar field, then a 24-frame held sweep
  keeps running. Three screens scan independently; the two lower instruments
  play the existing authored four-frame signal waveform.
- Fourteen actual stealth-fighter tracks and five actual pilot tracks move
  over the island geography. The sweep discovers contacts in sequence and
  plays original contact beeps. A separate alien interference source appears
  as the sweep reaches it.
- D-pad directions or pointer select a contact. A starts a 1.5-second scan,
  updates its progress and marks the contact identified with the original
  confirmation cue. Selecting and scanning does not skip dialogue.
- The map runs for 15 seconds in the campaign, with dialogue typing while
  instruments operate. B returns from inspection to the ordinary dialogue,
  where A reveals/continues as usual; Start retains scene skip. The separate
  review holds individual shots so they can be inspected.
- Arrival uses the selected pilot's exact game sprite and lands on the runway.
  HQ attackers use the existing red/green stealth palette plates. Scramble
  launches five unique actual pilot ships. These are moving sprites over new
  environment plates, not baked substitute aircraft.
- Narrow displays preserve equal pixel scale on both axes. The entire radar
  housing fits above dialogue, text fits inside its box and pointer coordinates
  use the actual cinematic viewport. Other cinematic surfaces retain their
  existing viewport behavior.

Sounds run from the cinematic update clock, not drawing. Repainting the map
does not duplicate beeps. The existing sound bank supplies charge/acquisition,
contact, focus, confirmation, alien targeting and launch cues. Sound follows
the user's music/SFX settings and browser audio activation.

## Art and identity ownership

Built-in image generation produced four clean HQ environment plates and a
32-cell radar bank (eight acquisition cells plus 24 held-sweep cells). The
backgrounds remove baked aircraft, trails, contacts and alien marks so the
runtime can animate and inspect them independently. Both prompts include the
actual nine-ship reference export. Original sources, exact prompts, references,
measured crops, pivots and shipping hashes are in
[`_ART_SOURCES/hq_live_1010`](../_ART_SOURCES/hq_live_1010).

`_BUILD_SOURCE/build_hq_live_1010.py` owns all 36 exports and their registry
together. Backgrounds use fixed 840 × 472 cells; radar cells use fixed
256 × 256 canvases and a stable physical origin. Import only crops, pads and
translates at scale 1; the generated alpha and aspect remain intact. Runtime
sector clipping reveals the authored acquisition field progressively. No atlas
was edited, and the actual aircraft pixels remain unchanged.

Runtime: `assets/hq_live_1010.js`; registry: `assets/hq_live_art_1010.js`.
`assets/cinematic_director_0930.js` supports the interactive beat and its reading
duration. The shared existing narrative beats also point to the new plates.
The permanent creative rule is in
[CINEMATIC_SHIP_REFERENCES_1010.md](CINEMATIC_SHIP_REFERENCES_1010.md) and AGENTS.md.

## Verification

- Required syntax checks pass. Full suite reaches its final success summary:
  **8,174 passed, zero failures, exit 0**, compared with the current 8,170/0
  audio-pass baseline. Four additional assertions validate shipping HQ pixels,
  unique frames, even dimensions and fixed pivots.
- Native Chromium: **25 passing checks, zero failures**. Verified real movement,
  scan/reveal/confirmation, input, sound calls, reading duration, continuation,
  nine actual landing ships, five-ship scramble, and narrow proportions and
  pointer hit testing.
- Actual review page: **nine passing checks, zero failures**. Playback, sound
  activation button, pilot selection, embedded keyboard focus and narrow review
  layout pass. Page, console and asset errors are empty in both probes.
- Native screenshots were inspected at acquisition, held scan, selected scan,
  alien discovery, landing, attack, scramble and narrow layout. The first probe
  checked the signal before its sweep had arrived; its timing fixture now
  waits for acquisition. Pixel review also caught the legacy narrow cinematic
  stretch and dialogue overflow; both are corrected in the HQ surface.

Portable evidence:
[`qa/hq_live_1010.json`](qa/hq_live_1010.json). Temporary captures/logs remain in
`_shots/hq_live_1010`. This verifies cinematic presentation and controls, not
campaign balance or a human verdict on the final audio mix. Existing work and
staging remain preserved. Local changes only; no commit or push.
