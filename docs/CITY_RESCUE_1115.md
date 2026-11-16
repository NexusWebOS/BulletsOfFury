> Superseded cinematic presentation: Juggernaut now always owns the album request, and the airborne technician uses the current cockpit art throughout Stage7 arrival. See [CITY_STYLE_1115.md](CITY_STYLE_1115.md) for the corrected full reel.

> Later November15: the album cover is now named **Bulletalica**, using a new built-in imagegen lettering edit. Cutscene timing, dialogue and gameplay are unchanged. The four recordings below retain the earlier lettering; current native-image verification is recorded in docs/qa/bulletalica_1115.json.

# Stage6 city rescue and Storm exhaust - November15

Original BOF source: D:/BOF-Downloads/2026-11-14/RevG-source. CITY16 implements Mike's newest corrections. It supersedes the earlier FATE15 optional next destination, old menu presentation and eleven-beat post6 ending. Actual native encounters, prior HQ/kit/Chronos/pilots, outcomes, passwords and awards stay under their current owners.

## Presentation

Stage6 uses new generated rural American farmland, country roads, homes, barns, forests and creek scenery under the native scrolling/cloud/weather layers. StageX retains its real urban scenery. Cole's Stage6 Callisto/private-weapon demonstration and its reactions are removed; prior squad talk stays. The earlier Stage3 workshop scene is a separate approved scene and is preserved.

The new Hard/Furious pursuit screens have generated artwork AND lettering, faithful current Harrier/Storm Cannon and all five Rebels. Existing logical controller/keyboard input and route briefing callbacks still launch the actual encounters. Native pad graphics sit in the reserved footer. No viewport or gameplay-resolution change.

All four current Storm engine rims now have correctly measured sockets172,93 /236,66 /340,66 /404,93 in its576 model. Sixteen unique generated exhaust phases are registered to a fixed mouth, cleaned to a common32-colour palette, then baked at16 headings and16 native depths. They render behind the real hull with its native clock. Northwest/west flyovers are re-exported with this same exhaust; body-only shadows exclude flame. No new runtime exhaust rotation, stretching, canvas glow or filters. Source/GIF details: _ART_SOURCES/city_rescue_1115/README.md. The source generation was a sixteen-cell sheet; the packed native/GIF animations were exported from its actual cells.

## Route and dialogue

Eight post6 beats remain. Cole directs the team: "Route us for the city. If anyone is still alive, we have to save them! Is there anything else on the radar? We have to find out what is causing this!" After the tech reports the underground contact he says: "Underground? After we save those people, we have to check it out." The response is: "As you wish. Alright team, let's do this!" The tech still swaps Decker/Cole according to the existing selected-pilot rule. Current CP15 talking cockpit frames and native letter sounds remain.

The map camera moves a little closer to the city fight/crash without altering gameplay framing. Existing Furious outcomes remain:

| Main Stage6 victory | Mandatory city encounter | Preserved map event |
| --- | --- | --- |
| Hard Harrier | Rebels | Fury/remaining Rebels reach city |
| Hard Rebels | Harrier | Fury/Harrier reach city |
| Furious Storm Cannon | Rebels | Harrier reaches city, is shot down; Crossed Fate |
| Furious Rebels | Actual Furious Harrier | Storm escapes west; Road Not Taken |

The exact existing STRM messages and once-only200FP awards remain. STRM opens Stage6's difficulty picker; BASE4 remains Stage4. The bottom map briefing now explicitly says STAGE X - CITY RESCUE and asks the team to save the people before heading to the riverbank.

Stage7 is locked until StageX is defeated and its new debrief finishes. This applies to map unlocks, deployment, direct Stage7 entry, native autosave and reload. Existing campaigns with an already earned Stage7 completion are not regressed. Earlier completed-city saves can migrate their native done receipt into the new debrief; fabricated/unverified new city results cannot unlock7.

## City victory, rewards, debrief and chibi flight

Only the native terminal defeat callback of the actual StageX Harrier/Rebels can verify the new result. The Harrier keeps its carrier-to-Nightwing handoff and all death phases; Rebels require all five real pools, Nyx reveal and full wrecks. Native bonus, Super Missile/air-superiority rewards, Signature MKII, lives/ammo/upgrades and settlement execute once. CITY16 replaces S113's obsolete post-result staged-battle insert by invoking that insert's actual settlement callback; it does not create a parallel reward path. Repeated results cannot replay rewards.

A native autosave is written at6 while the verified city debrief remains unseen. Reload resumes the scene with its result/rewards intact. Six current cockpit conversations then play:

1. Cole: "Wa-hoo! Another win for us team!"
2. Decker: "I think that's enough distractions for one day. Shall we embark to the riverbank now?"
3. Selected pilot: "Is it going to smell bad?"
4. Cole: "Very funny, [pilot]." Decker replies when playing Cole, avoiding a self-conversation.
5. An actual paired ally: "Is this a good time to put on one of my favorite albums?"
6. Cole: "Only if it's sad but true."

The pairing is Axel/Freezer, Cole/Decker or Falva/Lizzie if that partner is among the actual allies; otherwise Juggernaut. The final five-second full comic image always shows the current Juggernaut smiling and holding an original nearly-black Bullets of Fury album with embossed jet/ammunition art and generated title. No dialogue box covers that image.

The selected native map chibi flies from the city to the Stage7 flag over3.2s. Input waits during this movement, then Stage7 is available for manual selection. The game does not auto-start the sewer. Native map reward briefings remain. Completion/travel receipts are persisted through Rival24's optional story field; native suspend/autosave remain owners. Native skip also finishes once and returns to the map.

## Verification and limits

- presentation: 48/48 passed.
- nativeLifecycle: 37/37 passed.
- pointerRoutes: 19/19 passed.
- artReproduction: 4451/4451 passed.
- moviesBrowser: 50/50 passed.
- fullSuite: 8969/8969 passed.

Final failing-name comparison is empty against the earlier full suite. Core game.js LF and test_fl.js CRLF bytes are unchanged. Focused Chromium checks inspect real pixels and page/console/HTTP errors, all clear. All nine pilot dialogue/pairing scripts are checked. Both actual city opponents are exhausted through native damage/Retina/missile/death owners before the full result/debrief/save/chibi path. Source reconstruction checks every generated page, fixed pivot/crop, even cell, source alpha/palette, tile seam and all16 GIF phases without rewriting shipping art.

Four real Chromium H264/AAC1824x1024/30fps films with native game audio, full FFmpeg decode, decoded browser audio and byte-range chapter seeking:

- split.mp4 - 82.2s: Rural split - Harrier leads, Storm Cannon follows.
- storm.mp4 - 62.47s: Storm Cannon defeated - city rescue required.
- rebels.mp4 - 57.84s: Rebel Fighters defeated - city Harrier required.
- city.mp4 - 32.7s: City rescued - regroup, Black Album, riverbank.

Review: http://127.0.0.1:8766/_shots/city_rescue_1115/review.html

These are explicitly prepared cinematic/encounter checkpoints with scripted damage through native combat owners, not unassisted campaign wins or difficulty-balance validation. Real Chromium pointer input is tested; physical8BitDo hardware is not tested in this pass. Existing Normal/Easy Stage5 completion remains. The prior prepared Stage7 player-visibility concern remains outside this pass; the new film ends at the map's manual Stage7 offer. No commit, push, installer or release.

Runtime: assets/city_rescue_1115.js after FATE15; registry: assets/city_rescue_art_1115.js. Sources/prompts/native identity references: _ART_SOURCES/city_rescue_1115. Rebuild and native probes/recording/package/playback scripts: _BUILD_SOURCE/city_rescue_1115_*.py. Durable receipt: docs/qa/city_rescue_1115.json; temporary evidence/films: _shots/city_rescue_1115. The menu lettering, rural master, thruster sheet and Juggernaut album were created with the built-in image tool, not SpriteCook; exact prompt set is retained at _ART_SOURCES/city_rescue_1115/prompts.json.
