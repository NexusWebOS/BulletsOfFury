# New Yuri and readable typography — 0914

Mike requested the approved new Yuri likeness, matching compact dialogue portraits, uppercase 16-bit dialogue lettering, a new game face, and new fonts for stages 1–9.

## Delivered

- Routed legacy Yuri portrait requests before cache/atlas lookup to the seven existing approved `yuri_v2` expressions. New-Yuri idle is used while talking because this approved set has no mouth-animation frames; no retired face is substituted.
- Built 64×64 dialogue cells for all nine pilots from their existing authored portraits and avatar borders. Yuri uses the new mohawk/goatee likeness with his red border. Source mappings are retained in `assets/game/comm_portraits_0914/sources.json`.
- Authored Command Signal: a complete uppercase pixel alphabet with digits, punctuation and symbols. Dialogue uses white lettering, consistent sizing and centered stable typewriter layout. Default in-play panels now clear the bottom weapon/evasion HUD.
- Authored Command Alloy for shared game labels and nine coordinated biome font variants. These are new bitmap letterforms with width, slant, stencil and color treatments; they are not nine AI-generated alphabet sheets. The new TrueType Command Signal companion also replaces BOFmil on legacy canvas-text screens. Existing baked button labels remain authored button art.
- Fonts register sheets and maps together in `assets/game/fonts/command_0914/fonts.js`. No existing atlas, manifest or source artwork was replaced. Build sources are in `_BUILD_SOURCE/readable_type_0914/`; the TrueType builder uses fontTools 4.55.3.

## Verification

The native Chromium probe loads the real index, XART and game renderer. It checks all eleven faces and required glyph coverage, uppercase measurement, TrueType decoding, pixel equality between legacy Yuri keys and the approved expressions, seven distinct expressions, and compact portraits/layouts for all nine pilots. Page, console and game-loop errors are checked. Nine focused checks pass.

Visually inspected: real PLAY dialogue above the weapon HUD, long HQ launch text, modal comms, cinematic lettering, main menu, Yuri selection, seven expressions and all nine stage title samples. The four-second silent MP4 uses a scripted radio line and capture-only invincibility. Representative surfaces were verified; this is not an exhaustive replay of every campaign conversation.

The suite harness now loads the shipping font registrations; assertions that pinned replaced font names/donors and the former portrait accessor were updated to verify the new routes. Full-suite counts, inherited failure names, syntax result and runtime hash are recorded in `qa/readable_type_yuri_0914.json`. Runtime and test-file line endings remain LF and CRLF respectively.

Preview: `_shots/readable_type_0914/Yuri_Readable_Dialogue_0914.mp4`. Stage font contact sheet: `_shots/readable_type_0914/stage_fonts.png`.

## Campaign opening correction — 2026-09-20

Mike found an omitted route: the first Campaign flight's cockpit figure still asked for `pose_yuri_0`, a retired likeness on the cinematic atlas, even though the dialogue portraits and Pilot Select had already moved to the replacement Yuri. The intro now selects the approved `yuri_body_0` front-facing figure for Yuri, preloads it, and waits for it to decode. It never falls back to the retired pose. `cutPose()` also routes Yuri to the same current figure, preventing the archived cinematic pose/seated paths from showing the old likeness if used. Other pilots keep their existing scene poses.

`_BUILD_SOURCE/probe_yuri_campaign_intro_0920.py` rendered the real opening in Chromium for Yuri and Cole, checked the intro asset keys and `cutPose()` route, and captured `_shots/yuri_campaign_intro_0920/yuri_intro.png` and `cole_intro.png`. The Yuri screenshot was inspected: the cockpit now shows his approved mohawk, beard and red jacket. No page or console errors occurred. `node --check assets/game.js` and whitespace diff check passed. The full test suite still exits nonzero with exactly the same 76 failing assertion names as the recorded baseline.
