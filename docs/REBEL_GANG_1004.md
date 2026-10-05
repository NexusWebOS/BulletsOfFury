# October 4 — Rebel weapons, Gang Mode and Decker's rescue

October 4 follow-up: [Personal arsenals, attached pilot bars and survivor radio](REBEL_ARSENAL_1004C.md) supersedes the original arsenal table and escape-pod scan fallback below. Active priority is Kaia → Nyx → Jace → Rook → Voss; only living Rebels speak. Kaia now has twin rockets, Jace the red/orange helix nova, Nyx sustained stealth, Rook .50-cal slugs, and Voss turbo plus retained Fusion.

Mike requested five personal weapons, a three-of-five half-health escalation, and a live team-cloak scene with Kaia's counter-scan and the Cole/Decker exchange. `assets/rebel_gang_1004.js` loads after `finale_structure_1003j.js` and owns the Rebel fight after the existing introduction. The earlier three-encounter Stage 8 finale is unchanged.

## Encounter

| Rebel | Personal ability | Gang Mode |
| --- | --- | --- |
| Voss | Whole-hull pink charge, original impact-imminent asterisk, committed pink Fusion beam | Alternates Fusion with two shootable missiles |
| Nyx | Cloaked ambush; reveals before releasing three aimed rounds | Remains cloaked between attacks; cloaking removes Retina acquisition |
| Rook | Two visible authored heavy machine-gun attachments, spinning barrels, muzzle flashes and alternating bursts | Faster movement and a longer, faster burst |
| Kaia | Authored Falva rollerball; two smaller satellites split while still inside the arena | Destructible Axel-style blue helper orb fires twin lasers |
| Jace | Cloak, committed tell, reveal and strafing fire | Turbo strafe and faster repositioning |

The five original hulls and roll frames remain whole. Hit flashes never remove wings. Original individual pilot names/HP bars remain; stealth hides its own readout until reveal. There are no rebel shields, armor HP refills or hidden module damage gates. A shared attack budget prevents five large specials from releasing together. Missiles remain shootable and committed rather than homing. Rollerballs and the helper have separate HP and Retina targets; ordinary bullets and sustained beams can destroy them without damaging the owner hull.

Gang Mode triggers once when at least three of the original five have HP <= 50% of maximum. Destroyed fighters count toward that threshold but never respawn. The colored charge lasts 3.1 seconds. The single-pilot Stage X duel receives its personal ability without triggering a five-pilot cinematic. Rebel music continues to use the existing Stage X routing.

## Decker scene

Twelve seconds of Gang combat lead to the rescue, or sooner if the whole squad's HP falls below 17%. Decker leads a centered bowling-pin formation using the actual player and live allies; absent allies arrive as temporary cinematic participants. Selecting Decker uses the real Decker player, not an extra copy. Borrowed allies peel away afterward.

Eight timed, unskippable portrait beats cover Decker's oath, shield wave, the rebels' confusion, Kaia's “Leave it to the ladies…” counter-scan, her geek remark, Cole's matchmaking line, and Decker's “Love isn't always at first sight…” response. If Kaia's fighter has already been destroyed, Nyx takes the scan; if both female fighters are down, Kaia transmits the scan remotely from her escape pod. No fighter is revived. The original multi-Retina art searches and converges on the team.

Flight animation, weather, background scrolling and the world update continue. Formation steering is scripted during this scene. Combat inputs, incoming damage, attacks and pause/skip are blocked while the lines play. Supply pickups are retained but do not obscure the scene. The camera stays steady, and cloaking covers the player's gun attachments too. The generated reveal removes cloak; a visible friendly shield remains for five seconds after control returns. An undestroyed helper keeps its HP across the scene; a destroyed helper stays gone.

## Art and sound

- `assets/game/rebel_gang_1004/decker_effects.png`: built-in imagegen, original 1536×1024 RGBA copied unchanged. Four rows of six 256px cells: shield wave, cloak swirl, cloak reveal, chrome overcharge. Runtime palette variants retain the authored luminance/alpha.
- Owning registration workflow: `_BUILD_SOURCE/import_rebel_gang_1004.py`; deployed `manifest.json` records cells and SHA-256. Prompt and source filename: `docs/rebel_gang_prompts_1004.json`. `ART_TAXONOMY.json` registers `rg4_`.
- Existing `rr_ship_*`/`rr_roll_*`, `nfrb_*`, `florb_*`, `arch_blaster_gun_*`, generated 1003i laser strips/muzzles, original impact-imminent asterisk, Retina and portrait assets are reused. Source cells were rendered using `XART.get` and the game's own canvas before use.
- Existing generated Fusion, charge, teleport, gravity, targeting, impact and laser cues accompany the new beats; heavy MG, missile, shield and lock cues use their existing buses. Sustained combat audio releases during dialogue.

## Verification and review

- `node --check assets/game.js` and `node --check assets/rebel_gang_1004.js`.
- Full `_BUILD_SOURCE/test_fl.js`: 7,022 passing assertions, final `FALVA/LIZZIE BUILD OK` summary, exit 0. The new roller-split assertion initially caught a split that occurred too low; release now splits after 0.95 seconds, inside the arena, and the corrected test passes.
- A full-suite repeat also returned exit 1 at the earlier Maverick hold test (`HOLDING leaks nothing for maverick ... got 4`), before this new layer loads. The fixture intended to exclude random damage but granted only 99 invulnerability **frames** for a 180-frame trial. Its isolation window is now 600 frames; the no-leaked-shots assertion is unchanged. This changes no shipped Maverick gameplay. The failed log is retained as `_shots/rebel_gang_1004/full-suite-before-fixture-fix.log`.
- `_BUILD_SOURCE/probe_rebel_gang_1004.py`: 24 native Chromium checks. Five real release paths, original asterisk draw, stealth acquisition, gunfire destroying the helper, exact HP boundary, no enemy shields/heal, automatic scene entry, protected combat inputs, all eight lines, scrolling, original scan plus generated FX, control return and expiry. Zero page/console errors.
- The same probe with `--review`: seven checks covering all four playable launch buttons, actual keyboard fire from the live player, and playing Decker without duplicating him in the formation. Zero page/console errors.
- Screenshots inspected at native canvas resolution: complete source art, Fusion charge/release, heavy guns, individual health readouts, Gang charge, formation wave, cloaked multi-scan, reveal and final banter.
- `_BUILD_SOURCE/build_rebel_review_1004.py` owns `_shots/rebel_gang_1004/review.html`. Includes Normal/Hard/Furious and Yuri/Decker/Cole/Falva selectors, full intro, direct fight, Gang preview and scene preview.

Automated checks establish behavior and visible rendering; they do not replace Mike's difficulty/play-feel review. All work remains local. No commits, pushes, merges, asset deletions or repository copies.
