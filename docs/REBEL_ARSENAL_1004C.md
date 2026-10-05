# October 4 — Rebel pilot arsenals and survivor radio

Mike requested attached pilot HP bars, living-pilot counter-scan dialogue and five distinct personal arsenals. `assets/rebel_arsenal_1004c.js` loads after `campaign_focus_1004b.js` and extends the existing live Rebel encounter. Existing complete hulls, burning deaths, shocked portrait cinematics, Stage X music, five-versus-five roster and protected scrolling dialogue are retained.

## Combat

All five Rebels fire baseline machine-gun rounds between specials. Each pilot now receives a generated personal ability box, flies to collect it, then announces the attack through the original warning system. Boxes have six HP, white hit flashes, actual projectile/beam/Fire Whip collision and Retina targets. Destroying a box delays its owner's next special by four seconds. Enemy boxes never unlock player weapons or combos. Active specials display their corresponding generated box; individual HP readouts carry matching hex icons. The four allies and actual player display their own existing authored ability icons/active boxes through the game's atlas-aware `iconDraw` path.

| Rebel | Arsenal | Response |
| --- | --- | --- |
| Voss | Fast physical turbo dash, then three passes (four in Gang Mode) from alternating offscreen sides; retains pink Fusion every third cycle | One-second committed horizontal warning rows before subsequent rams; original asterisk and generated pink wake |
| Rook | Attached twin .50-cal slug chainguns: alternating 14-shot bursts, 20 in Gang Mode; occasional physical charge ram | Original directional warning; authored heavy rounds, animated barrel attachments and muzzle flashes |
| Jace | Actual Maverick helix sphere and charge aura palette-swapped to red/orange; destructible 14-HP ball detonates after 1.35 seconds into eight distinct miniature energy balls | Shoot the orb before its nova; no laser-strand volley; occasional warned ram |
| Nyx | Five-second stealth ambush (longer in Gang Mode), faint hull/swirl tracing and irregular aimed gunfire | HP readout and new/existing missile locks disappear while cloaked; blind gunfire remains effective and briefly flashes her white |
| Kaia | Two anchored generated black/teal rocket pods; four rockets, six in Gang Mode, alternating sides every 0.42 seconds | Alternates freefire and original-Retina locks. Locked missiles steer briefly, then commit within 115px or after 0.9 seconds; all rockets remain shootable |

Baseline fire targets the actual five friendly participants; physical rams use real player/ally hit paths. The existing special concurrency budget and original green/yellow/red FOV warnings remain. Turbo rows clip those authored FOV pixels to a readable 62px band. Gang Mode retains the original half-HP threshold, colored overcharge and destructible helper support. No Rebel shields or HP refills were added.

HP bars use each pilot's live world position and measured ship height. Offscreen, defeated and cloaked pilots have no bar. There is no fixed five-bar row at the top of the screen.

## Survivor scene

Counter-scan priority is **Kaia → Nyx → Jace → Rook → Voss**, with living hull/HP checks. The scene's confusion lines also use surviving Rebels. Dead pilots are never assigned a radio line and never return from an escape pod to scan.

- Kaia/Nyx retain the ladies/geek exchange and Cole/Decker's romantic banter.
- Jace says “Leave it to the new recruit to show them how it's done.”
- Rook boasts about the big boss; a living Voss adds “Remember who the actual big boss is here, big guy.” This variant has nine timed portrait beats.
- Voss alone says “Jeez, do I gotta teach you guys how to do everything around here? Lock on and use the radar hack!”
- Male scan variants use technology banter for Cole/Decker rather than the romantic reply. No surviving Rebel means no new rescue scene.

The actual player/four allies form up. Flight, weather and scrolling continue while firing, damage and skip remain protected. Existing original multi-Retina and generated Decker wave/swirl/reveal effects are reused.

## Asset ownership

Two built-in imagegen outputs are preserved in `_ART_SOURCES/rebel_arsenal_1004c/` and deployed in `assets/game/rebel_arsenal_1004c/`. Their original 1536×1024 RGBA bytes and genuine alpha are retained. The UI output's actual five-column/two-row layout is measured, not assumed from its prompt. The FX sheet has six frames each for turbo wake, nova, rocket pod and missile. Ten UI cells and 24 effect cells are registered together in `manifest.json` and `rebel_arsenal_art_1004c.js`, with source filenames, sheet hashes, prompt-set link and alpha information.

`_BUILD_SOURCE/export_rebel_arsenal_1004c.py` resolves the original Maverick art via `XART.get` and the game context's own `drawImage`. `_BUILD_SOURCE/build_rebel_arsenal_1004c.py` owns the twelve palette swaps and sheet metadata. Swaps retain source alpha byte-for-byte, preserve neutral outlines/highlights and map colored pixels to a red/orange ramp at their original Rec709 luminance. Maximum quantization error is below 0.004. These are palette swaps, not color overlays. Generation specifications and provenance are in `docs/rebel_arsenal_prompts_1004c.json`; `ART_TAXONOMY.json` registers `ra4_`.

## Verification

- `node --check assets/game.js`, new runtime and generated registration pass.
- Full `node _BUILD_SOURCE/test_fl.js`: **7,089 passing assertions**, final `FALVA/LIZZIE BUILD OK, 0 ERRORS`, exit 0. New tests cover each weapon, eight-way nova, shootable personal crates, collection-to-charge, HP anchors, cloaked existing locks and all survivor variants. Game JS remains LF; test harness remains CRLF.
- `_BUILD_SOURCE/probe_rebel_arsenal_1004c.py`: **32 native Chromium checks**, zero page/console errors. Actual canvas blits prove source UI/FX/palette art, complete ships, original warnings, sequential rockets, native gunfire interception, five friendly badges, moving HP readouts, Nyx hit silhouette and the complete nine-line Rook/Voss rescue. Natural encounter scheduling collects all five personal boxes and releases all five arsenals.
- Same probe with `--review`: **25 checks**, zero page/console errors. All nine fight/special shortcuts, four allies beside the player, real keyboard firing, five survivor selectors and actual Decker without a duplicate pass.
- Native screenshots inspected: generated/resolved source art, five-versus-five badges, Jace charge/nova, turbo dash/row, Kaia pods/missiles/box, Nyx tracing/white hit and Rook counter-scan portrait.
- Initial visual testing caught the friendly icon lookup incorrectly treating atlas cells as loose images; fixed with the existing `iconDraw` path. Two probe fixture errors were corrected: a rocket hit test initially put the shot inside its owner's hull, and a direct scene-event call omitted its scene argument. The final tests use actual midair interception and complete native scene timing.

The owning review builder is `_BUILD_SOURCE/build_rebel_arsenal_review_1004c.py`; output `_shots/rebel_arsenal_1004c/review.html`. Practice supports all nine friendly pilots, four difficulty levels, full intro/fight/Gang Mode, each individual arsenal and every counter-scan survivor. It blocks campaign storage writes. QA evidence is `docs/qa/rebel_arsenal_1004c.json`.

This verifies the implemented behavior and visible pixels, not a human campaign clear or final difficulty tuning. All work remains local and uncommitted; prior staged/unstaged/untracked work is preserved.
