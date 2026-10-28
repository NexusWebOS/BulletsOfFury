# The Rough Riders — crew identity and Stage 6 entrance

The five former Rebel Fighters are officially **The Rough Riders**. Voss, Nyx, Rook, Kaia and Jace keep their existing portrait identities, aircraft, weapons, health and combat controllers. Current campaign/route/radio labels and the native squad name use the new crew identity; historical provenance and internal encounter IDs remain intact.

## Generated art

The group portrait places each pilot in front of their matching aircraft at a coastal airbase, with a stamped crew wordmark. Actual current native portrait and whole-aircraft exports, including Rook's guns, supplied the image references. Four transparent branding marks are included: chrome/crimson wordmark, five-jet RR patch, Private Airspace sign and Five-Ship Crew stamp.

PixelLab generated **Rough Riders Ignition** (font job5432da36-c300-4705-afba-6fa29392a1eb). It has80 glyphs, original TTF and padded proportional bitmap exports in chrome, crimson and signal/teal. Common baseline and complete R/5 silhouettes checked; fixed32px cells leave safety margins. Native entrance header uses the chrome font. Other game typography is unchanged.

Sources, reference exports, manifests and reproducible builder: `_ART_SOURCES/rough_riders_1028/`. Five editable72-frame Aseprite files and the font Aseprite are retained. Runtime assets: `assets/game/levels/stage_06/boss/rough_riders_1028/`; registries/owner: `assets/rough_riders_art_1028.js`, `assets/rough_riders_1028.js`.

## Live entrance

1. Player and allies catch the five aircraft flying north, in the same direction.
2. The crew spools its anchored thrusters and boosts fully off the north edge.
3. All five return from the top, each making two16-frame somersault passes on crossing airshow paths. Whole ships render in depth order.
4. They settle into a spread bowling formation before dialogue begins.
5. Scrolling eases from the native740px/s cruise to approximately41px/s, with independently animated scenery and clouds. Player, allies and crew gently drift.
6. After the original motive/tech dialogue and new crew callout, normal scrolling eases back over1.6s and the existing full combat controllers resume.

This choreography is scoped to the full five-pilot Stage6 encounter. StageX and individual fights retain their prior entrances. Intro is protected: hostile targeting/collision/damage cannot touch the stunt pilots, stage/wave progression clocks stay frozen, and allies remain present. Each aircraft uses72 fixed192px authored cells:32 headings,16 native matching pitch frames and three eight-frame cruise/boost banks. Existing PixelLab plume pixels are recolored and anchored offline; no new runtime image transforms. Combat/FOV/physical missiles/flashes/cloak/health/defeat/reward owners remain native.

## Verification and review

-26 native/art checks pass across Easy, Normal, Hard and Furious. Native damage and hit-flash expiry remain active after handoff. Clear cell borders, even sizes, texture limits, complete font masks and actual scroll movement checked.
-Fresh59.64s **live Furious GOD observation** video reaches the natural end of dialogue and seven seconds of combat. No enemy HP, phase or timer writes. Actual allies attack after release. This is an entrance/handoff preview, not a boss clear.
-9 film checks pass, including all phases, protected full health, allies, scrolling, source hashes and decoded audio. Recorded audio mean−16.7dB/peak−2.7dB.3485 sampled native frames, approximately58.4fps. No game/console/HTTP asset errors or audio tap errors;21 cancelled media fetches are recorded separately as ERR_ABORTED.
-14 review playback checks pass: all images load, both1280×800 videos decode moving frames/audio, three seek positions each, range206 support, no browser errors.
-Syntax checks pass. `node _BUILD_SOURCE/test_fl.js` reaches its final summary, **exit1 with the same five baseline failures**: single-hit flash duration; dialogue opening jump warning; opening jump return before Chromium; opposite StageX route persistence; StageX right full encounter. No new failures.
-All20 PNG banks and the registry rebuild byte-identically. No game.js/test_fl.js edits in this task. Existing repository changes preserved. No commit or push.

Review: http://127.0.0.1:58112/index.html

Evidence: `docs/qa/rough_riders_1028.json`; portable `_BUILD_SOURCE/probe_rough_riders_1028.py`, `_BUILD_SOURCE/export_rough_riders_refs_1028.py`, `_BUILD_SOURCE/record_rough_riders_1028.py`. Local films/art download/viewer: `C:/Users/Mike/Documents/New project/BOF-Rough-Riders-1028/`.
