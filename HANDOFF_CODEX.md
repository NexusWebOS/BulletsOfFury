# 2026-10-09 — GitHub publication: fullscreen and readable HUD

Mike authorized publishing the completed fullscreen/HUD improvements. Browser
and native fullscreen use the full available height at the original playfield
aspect; menus and mobile layouts have no hidden HUD reserve. Dense 2x bitmap
rendering retains letter detail. Scores use large comma-grouped number lines,
and the 34px non-playable footer fits large scores and equally legible special
counts/charge readouts. Solo/co-op reserve 104/208 logical pixels. The lock box
always shows the authored crosshair: silver when idle, red on a live lock.
Corrected side portrait paths, concept-label cleanup, actual HUD canvas clearing
and rounding/fallback exit behavior. PLAY_OVERDRIVE.bat is included.
Native HUD: 205/205; fullscreen Chromium/Firefox/WebKit: 51/51; footer pixel
bounds: 12/12, zero browser errors. Full base suite completed with exit 0 and
the final zero-error banner. Syntax checks passed; real captures inspected.
Reports: docs/FULLSCREEN_HUD_1008B.md and docs/PLAYER_HUD_1008.md.
Two former source-text layout assertions now execute the shipped fitter to
verify actual desktop/mobile/fullscreen width and visible/hidden HUD height.
Separate Overdrive development and Contra scratch are preserved locally.
Earlier LOCAL ONLY HUD entries below are historical verification checkpoints.

# 2026-10-08 — expanded non-playable score/special strip

Mike requested more black HUD space for scores and specials such as nukes.
Footer expanded from 20 to 34 logical pixels, with padded 7px labels and 12px
score/high-score/special values in three independent lanes. Housing remains
70px; total solo row is 104px, co-op 208px; dense backing 960x208 / 960x416.
Initial HTML reserves the same dimensions. Fixed floating-point budget rounding
that otherwise left a 1px gap at 1366x768. No combat or asset changes.
Native HUD 205/205; Chromium/Firefox/WebKit fullscreen 51/51; focused footer
pixel checks 12/12 (nukes, A-bombs, full charge, long scores, co-op); zero errors.
Inspected captures: `_shots/fullscreen_hud_1008/footer_status` and
`_shots/fullscreen_hud_1008/footer_expanded`. Local only, no commit/push.

# 2026-10-08 — clearer score readout

Mike found the small footer score hard to read. Score/high score now have
separate 12px number lines (formerly 7px), comma grouping and no leading-zero
padding. Pilot/score labels remain above the numbers; special status has its
own center lane. HUD row is now 90 logical pixels, reserved from initial HTML
layout; solo backing 960x180, co-op 960x360. Sidebar and leaderboard score
numbers are larger too. Fullscreen still fills the viewport height and keeps
the playfield aspect. Native HUD 205/205, fullscreen across three browsers
51/51, zero errors; syntax passes, final pixels inspected under
`_shots/fullscreen_hud_1008/score_final`. Local only, no commit/push.

# 2026-10-08 — fullscreen and HUD readability

Mike requested full-height browser/fullscreen and clearer new HUD lettering.
[Report](docs/FULLSCREEN_HUD_1008B.md): shared exact viewport-height budget,
2px divider, no hidden menu/mobile rail space, working F/native/fallback exit,
2× HUD backing (same logical layout), bitmap rounding on the dense grid,
concept-label fragment removal, opaque status backing and pilot-owned side
portrait paths. No art or combat changes; main loop clears the actual HUD
dimensions. Full base suite exit 0/final zero-error banner; native HUD 205/205;
Chromium/Firefox/WebKit fullscreen 51/51, zero browser/asset errors. Screenshots
inspected under `_shots/fullscreen_hud_1008` and `_shots/player_hud_1008`.
Installed in `C:/Users/Mike/Desktop/Github Coding/BulletsOfFury`; local only,
no commit/push. Preserve the local Overdrive launcher and Contra study scratch.

# 2026-10-08 — GitHub publication: live player HUD and encounter bars

Mike authorized publishing the completed HUD integration. Ten authored stage rows
now show live equipment, stocks, cooldowns, specials, loans, radar and lock state;
complete miniboss nameplates, co-op rows, independent Rebel bars and Dracodia's
actual HP pools/eight colored refills are verified. Source crop provenance,
reproducible builder, native probe and portable QA ship with the runtime.
See [integration report](docs/PLAYER_HUD_1008.md) and
[verification results](docs/qa/player_hud_1008.json): 7,952 regression assertions,
450 native Chromium checks, final success banners and zero errors. Captures use
protected rendering fixtures, not a new balance sign-off. Base game/test bytes and
line endings are unchanged. Earlier local HUD notes are verification checkpoints
for this publication. Unrelated expansion work and scratch remain local.

# 2026-10-08 — Live player HUD and complete encounter bars (LOCAL ONLY)

Mike requested installing the new HUD, boss bars and miniboss bars.
[Runtime, ownership and verification](docs/PLAYER_HUD_1008.md),
[portable checks](docs/qa/player_hud_1008.json). Ten compact authored stage rows
now replace the concept samples with live fonts, icons, stocks, cooldowns,
specials, timed loans, radar and lock warnings. Fixed 80-pixel solo / 160-pixel
co-op geometry reserves complete independent rows. Miniboss nameplates now sit
directly below the player assembly; the existing authored boss/shield/Harrier and
five Rebel housings remain live. Finale actual pools and eight colored coronation
refills are preserved. Stage textures and derived HUD caches retire on departure,
including Stage X under Stage 6 ownership. Original generated pixels/alpha,
source hashes and reproducible crop builder are retained; no atlas repack.
Required full suite: 7,952 passes, zero errors, exit 0 and final success banner.
Native player HUD: 205 checks; enemy HUD: 245 checks; zero page/console
errors. Captured native stage/pilot/weapon/co-op/finale views were inspected.
Controlled protected fixtures verify rendering, not unassisted clears or balance.
Base game and test harness remain byte-identical; index CRLF retained. Review:
`_shots/player_hud_1008/review.html`. Local only, no commit/push; existing unrelated
work preserved. Earlier player-HUD-concept notes below are historical checkpoints.

# 2026-10-08 — GitHub publication: organized assets, combat checks and enemy HUD

Mike authorized publishing the current game. This batch includes the completed
projectile/animation pass, per-pilot/per-level asset organization and memory lifecycle,
maneuver/safety and recovery adjustments, and the generated stage/pilot enemy HUD.
See [enemy HUD details](docs/ENEMY_HUD_1007C.md), [portable HUD checks](docs/qa/enemy_hud_1007c.json),
and the October 7 reports below. Nine HP palettes, optional thin cyan shields,
the Stage X Harrier turbine frame, and individual themed Rebel bars are installed.
Player HUD rows in the art gallery remain concepts. Existing balance limitations
remain documented; this publication is not a claim of human-perfect balance.
Latest full suite: 7,952 passes, zero errors, final success banner. Native HUD:
245 passes, zero page/console errors, including all four Rebel difficulties and both
routes. Source and runtime asset paths are published together. Captures, unused
asset archives and unrelated Contra study scratch remain local. Earlier LOCAL ONLY
notes are historical checkpoints for work included in this publication.

# 2026-10-07 — continued balance recovery

[Playable changes and qualified results](docs/BALANCE_RECOVERY_1007B.md), [attempt matrix](docs/qa/balance_recovery_1007b_matrix.md). Added the small final `assets/balance_recovery_1007b.js` layer after maneuver safety: Stage 2 flame vent/crossing/re-warning, miniboss/environment scheduling, fresh tell after a surviving Furnace arm's stun; genuine Stage 4 retreat/punish windows with solid live attachments; slow-pilot whirlwind reaction budget; longer rotating-cross gaps/tells; once-per-earned-milestone collectible recovery; Normal/Hard/Furious HP budgets for Stage 2/4/5 with finale donor exclusion. Death still resets equipment; no free lives or automatic pickups. Full suite 7,952 assertions, final banner, exit 0. Chromium/Firefox/WebKit 56 checks each (168 total), zero errors. Complete Easy finale verified in the installed build: actual stageclear, all nine persistent pools zero, 535.15 seconds, six deaths, no continue. Hard Stage 2 repeated its full clear in the final build; separate equipped screens cleared Hard 3/5/9 using real credits, including a naturally collected Continue Up in Stage 3. Slow-pilot boss results and unresolved Hard/Furious failures stay separate by profile and credit use; do not claim human survival percentages or an all-green balance sign-off. Optional helper pause during ram failed both Hard/Furious screens and remains UNINSTALLED in `_BUILD_SOURCE/sovereign_helper_candidate_1007b.js`. Do not overlay the complete recovery candidate onto the installed game (duplicate globals). Core game/ram/ground source files are byte-identical to the prior maneuver pass, line endings preserved, no new art binaries. Local only; no commit/push. Reproduce via the report; full native traces/captures remain under `_shots/maneuver_safety_1007`.

# 2026-10-07 — maneuverability and safety screening

[Report](docs/MANEUVER_SAFETY_1007.md) and [per-difficulty matrix](docs/qa/maneuver_safety_1007_matrix.md). Fixed 60 Hz combat updates remove low-refresh movement disadvantage; yellow tracked ground reticles commit their aim with measured escape time. Stage 4 damaged-weapon ram now displays during outer recovery, includes its live generators and allows time to clear its swept path. Native final checks: 180/180 ground escapes, 20/20 damaging controls; 24/24 ram escapes, 16/24 damaging stationary controls (eight edge controls already outside the unshielded path); three-browser clock audit 47/47 plus final 15/15. Full suite 7,840 assertions, final success banner, exit 0. The 164-case broad screen, 16 carrier/ace variants, 12 affected-build replays and separate loadout/tactics runs retain real damage and stocks. This is NOT an all-green balance sign-off: several early bosses/stages, Hard/Furious full-stage runs and the complete finale have no confirmed scripted clears. Form visits are not full-finale clears; human survival, learning and enjoyment remain unmeasured. Source encoding was repaired and original game bytes hash-verified apart from two intended loop edits. Review `_shots/maneuver_safety_1007/review.html`; portable evidence and human worksheet under docs/qa. Local only, no commit/push; earlier asset/layout/projectile work preserved.

# 2026-10-07 — owned asset layout and memory lifecycle

Assets now live in per-pilot portraits/body_frames/ship_frames/abilities and per-level stage/enemies/boss/miniboss/projectiles/effects folders. Start at `asset-library.html` and `docs/ASSET_LAYOUT_1007.md`. All 3,943 moved files and 400 lossless repacked cells verified. Native Chromium/Firefox/WebKit checks are recorded in `docs/qa/asset_layout_1007_results.json`. Canonical URL image sharing, boot deferral, scene-boundary retirement and low-spec/adaptive native rendering are active. Full regression: 7697 assertions, zero errors. Changes are local; no GitHub publication performed. Preserve the earlier projectile and balance work.

October 7 projectile/animation pass: [Native four-difficulty audit and enhancements](docs/PROJECTILE_ANIMATION_PASS_1007.md). Herald/Stage 7 charge-size columns now hold complete flight poses with internal pixel light and measured core/hull pivots; chaingun casings retain shape, Stage 4 lightning MG skips its transparent eighth cell. Correct zero-axis headings, simulation-owned visual clocks, continuous thrust phase, seconds-based authored debris and single fragment draw; cloud canvas dimensions and direct Ace launch offset fixed. 144 projectile kinds x 4 difficulties (4,608 frames), 25 dedicated variants (1,664 frames), 164 bounded live observations, 876 legal weapon loadouts, 120 final primary rechecks and 20 affected-scene replays. 53/53 report checks, 7,697 full-suite assertions, final banner/exit 0 and zero native browser errors. Invalid original Orb fixtures excluded; Maverick homing-lance fixed combat tier explicitly verified. No asset binaries, atlas repacks, damage or difficulty changes. Protected visual checks are not full human clears or sustained FPS benchmarks. Review _shots/projectiles_1007/review.html; portable evidence docs/qa/PROJECTILE_ANIMATION_1007.json and CSV. Local only, uncommitted/unpushed; earlier balance and unrelated work preserved.

October 7 balance measurement pass: [Four-difficulty screening and qualified findings](docs/BALANCE_PASS_1007.md). 838 measurements include 144 initialized HP checks, 120 surviving movement escapes plus 12 damaging stationary controls, all-nine-pilot weapon screens, 36 bounded stage slices, recovery/co-op/finale samples and fresh-browser Stage 5 confirmations. Rebels/ace/finale retain solo HP in co-op; Stage 5 Level III median clears are Easy 4.52s, Normal 6.99s, Hard 7.86s, Furious 9.03s. Base-weapon Normal/Hard/Furious fresh trials all lost first life. Original shared-context repeat exposed retained cooldowns; exploratory results remain labeled, final fresh-browser repeat matches. Nine invalid Orb fixtures excluded, actual MG selection verified for all pilots. 1,180 final measurement checks pass, zero recorded browser errors; cancelled local-server requests are documented. Human fairness/learning and full campaign/finale clears remain unproven. No gameplay edits or full-suite rerun; published runtime 2d5b72b retained. Reusable vectors/readme in _BUILD_SOURCE/balance_cases_1007; portable data and human sheet in docs/qa; local review _shots/balance_1007/review.html. Local only, uncommitted/unpushed; unrelated study scratch preserved.

October 7 GitHub publication batch: Mike authorized publishing the completed boss, art, engine and browser-startup work. Includes Stage 4 core repairs/revival, the unused-asset cleanup, all Contra-inspired encounter upgrades, authored effects and source/build/QA files. Latest runtime verification: 7,681 full-suite assertions and 563 encounter plus 32 startup native checks, zero reported browser errors. The approved Furyship source comparison now pins its pre-cleanup SHA-256 so validation does not require the local archive. UNUSED_ASSETS, captures and unrelated _STAGING/contra_study_1005 remain local. Publication recheck: full 7,681/0 with local archive/study paths hidden; the production-asset sweeps exclude only three retired editor sheets and the road-patrol fixture is deterministic. Evidence: docs/qa/github_publication_1007.json. Earlier LOCAL ONLY notes below are historical checkpoints; the combined ZIP predates this gameplay batch.

October 7 asset cleanup / portable refresh: [Separate unused archive and verified two-ZIP release](docs/ASSET_CLEANUP_1006.md). Runtime assets 2.32 GB→1.28 GB; 4,981 original files/1.04 GB preserved with hashes in ignored UNUSED_ASSETS/cleanup_2026-10-06. Three retired rig sheets moved; 72 superseded portrait cells removed, ten remaining dialogue panels pixel-identical, 6,915 other cells unchanged. Builders read archived donors; six unused music aliases removed. Extracted build caught and fixed obsolete prototype preloading. Full suite 7,485/0, final banner and exit 0; native 70 checks including complete nine-stage preloads, package 24 plus 77 Boss 4 checks, zero missing assets/errors/archive requests. ZIPs: game/audio 96.03 MB, art 375.05 MB, combined 471.08 MB; extract together and run BAT. QA docs/qa/asset_cleanup_1006.json. Protected fixtures are not full clears. LOCAL ONLY, uncommitted/unpushed; previous work preserved.

October 7 startup layout fix: [Stable shell and complete control reveal](docs/STARTUP_LAYOUT_1007.md). Reproduced a390.5px delayed-load jump; moved layout before runtime loading, deferred first game frame until all classic scripts register, unified canvas sizing and prewarmed hidden control hints. Native32/32 across cold/delayed/warm, narrow/wide, keyboard/fullscreen/resize; full7,681/0, zero errors. Local only; prior gameplay/assets retained.

October7 Contra-inspired upgrade: [encounters, chromium spell and engine](docs/HARDCORPS_UPGRADE_1007.md). Lost desert airbase, Sovereign/Stage5/6/Herald crosses, Rookhook, Nyx helix, blue-ace corridor, all final encounters/eight copies plus Code Hammer rift, opaque physical transformations and combat-body speech. Per-seat projectile/chaingun repairs and world-anchored final arena. Full7,681/0; native563/0, zero browser errors. Sources preserved; local changes only. Review _shots/hardcorps_upgrade_1007/review.html.

October 6 Boss 4 core revival: [Authored ship charge, four lightning feeds and socket reconstruction](docs/S4_CORE_REVIVAL_1006.md). Built-in imagegen generates three four-frame clips with unchanged archived RGBA, exact prompts, measured source rectangles/pivots and owning builder; no shared atlas repack. Existing1.08s threshold rearm preserved, cosmetic afterglow ends1.48s; cycle-owned cleanup, no new hazards/damage. Native 77 revival checks plus repeated101 core repair checks pass (178 total), zero browser errors, all twelve difficulty/threshold combinations captured. Full suite7,485 assertions, final banner, exit0;32 new checks. Review _shots/s4_core_revival_1006/review.html; QA docs/qa/s4_core_revival_1006.json; reload/use BOSS4. Protected fixtures are not full clears/balance proof, audio cue dispatch only. LOCAL ONLY, uncommitted/unpushed; prior work preserved.

October 6 Boss 4 repair: [Generator ownership, local middle-weapon flash and immediate render cleanup](docs/BOSS4_RENDER_1006.md). Fixed the October 2 core draw override that substituted the central lightning weapon for every generator/helper socket and used shared hull flash; removed its duplicate generic plate. Generators now draw only while active/visibly rearming and alive. Local centres retain owner geometry/flash after middle weapon destruction. Full suite 7,453 assertions, final banner, exit 0; 101 native checks pass with zero browser errors, ordinary projectile damage, native held beams, curved Retina missiles, all twelve threshold rearms and weaponless rams verified. Runtime/test hashes unchanged in the second audit; retained 7,453-assertion full-suite evidence. Protected fixtures are not fight clears/balance proof; deliberate threshold rearm remains. Review _shots/boss4_render_1006/review.html; QA docs/qa/boss4_render_1006.json; reload and use BOSS4. No art, shared game.js, HP, thresholds or reward changes. LOCAL ONLY, uncommitted/unpushed; earlier Herald/study work preserved.

October 6 Contra study / Herald integration: [Committed twin cannons, owner cleanup and generated break effects](docs/CONTRA_HERALD_1006.md). Complete 35-encounter visual atlas retained in _STAGING/contra_study_1005. Existing approved modular Herald now alternates fully warned cannon beats, clears a broken arm's released shots and pending warning, and grants longer recovery after both guns break. Unchanged generated joint/breach pixels registered with source, prompt, builder and taxonomy; no shared atlas repack. Full suite 7,445 assertions (baseline 7,407), final success banner, exit 0. All 41 native checks pass with zero browser errors; eight ordinary-movement fixtures use actual slowest-pilot speed, no invulnerability/specials, plus stationary positive damage control. Focused cannon cycles are not complete balance/campaign/co-op proofs; other capture fixtures protect the pilot. Native review _shots/contra_herald_1006/review.html, portable QA docs/qa/contra_herald_1006.json, play password MINI8. Four original lab bosses/eleven forms remain candidates. LOCAL ONLY, uncommitted and not pushed; earlier user work preserved.

October 6 GitHub publication batch: Mike requested uploading the completed local game work. Includes the Dracodia cinematic/reform/destruction/home-portal integration, approved Code Hammer and knight art/behavior, shared Cronos warning repairs, and Stage 8 motion/AI pass. Final gameplay verification: 7,407 assertions, final success banner, exit 0; latest 42 native checks plus prior cinematic/Hammer evidence retained, zero latest browser errors. Runtime/test hashes still match that verified build; fresh origin/main matched the starting HEAD. Authored source/deployed art, audio provenance, builders, probes and handoff/QA are included. Human balance review remains; protected fixtures are not unassisted clears. Earlier LOCAL ONLY notes below are historical verification checkpoints. Unrelated _STAGING/contra_study_1005, ignored captures and the existing stash are preserved locally.

October 6 Stage 8 motion/AI completion: [Full native Code Hammer motion and harder form patterns](docs/FINAL_FORM_AI_1006.md). Sixteen generated identity-consistent cells cover curl/ball, giant strikes, four whirlwind directions and weapon loss/throw; measured reactor/head pivots and source scale/rotation. All six campaign donor copies get distinct module-aware warned followups (Normal one, Hard two, Furious up to three); actual Furnace relay starvation fixed without overlaying beam phases. Knight distance/equipment selection, immediate disarm cancellation, newly warned Furious smite and three code bursts. Furious Hammer return swing, earlier host/ghost signatures and warned colossus claw echoes; nine saved pools, three outer fights and sole reward preserved. 7,407 assertions, final banner, exit 0; 42 native checks, zero errors; all six authored ordnance releases and co-op selection verified. Review _shots/finale_ai_1006/review.html; prompts/source/QA retained. Protected fixtures are not unassisted clears. LOCAL ONLY, not committed or pushed; earlier dirty work and unrelated staging preserved.

October 6 Hammer/knight completion: [Separate Code Hammer, sword/shield extension and shared Cronos warning repairs](docs/HAMMER_KNIGHT_1005.md). Forty-nine authored native alpha cells preserve the approved black/chrome/crimson robot identity. Ninth persistent copied-form pool, live source Hammer controller, side strikes, healing missile counter and eight-percent emergency; measured catch anchor and red detached throw. Knight shield smite, committed downward/rising combo, code fireballs and collapsing Armageddon with mandatory side retinas/inward arrows. Stage 5/HAMMER/HAMA columns stay fixed at the visible bottom; super blast FOV only; spikes retract with their collision. Actual HAMR8 password entry and pinned catalog verified. 7,363 full-suite assertions, final banner, exit 0; 17 native checks pass with zero browser errors; 49 rebuilt cells match SHA-256 exactly. Review _shots/hammer_knight_1005/review.html; portable QA docs/qa/hammer_knight_1005.json. Three outer fights and sole reunion reward preserved. Protected fixtures are not unassisted Furious clears; human balance/creative review remains. LOCAL ONLY, uncommitted and not pushed. Earlier work/stash preserved.

October 5 resumed Dracodia cinematic: [Protected reforms, complete villain speech and authored destruction/home portal](docs/DRACODIA_CINEMATIC_1005.md). Mike explicitly resumed the paused passover after the latest main download. Fifty-five native alpha cells, dedicated processed shriek, mouth-only speech for nine expressions, measured joints, exact reform/final lines, twin sun ruptures, opaque fragments and charred wreckage. New portal departure/arrival retains the original sole reunion reward. Copied HP/equipment and three outer fights preserved; co-op and fresh-stage cleanup verified. 7,310 full-suite assertions, exit 0; 29 native plus 19 playable-review checks pass with zero browser errors. Review _shots/dracodia_1005/review.html; portable QA docs/qa/dracodia_cinematic_1005.json. Human balance/creative review remains. LOCAL ONLY, uncommitted and not pushed. Earlier paused-publication notes below are historical.

October 5 paused publication: Mike explicitly requested pause and GitHub upload. [Resume passover: Dracodia requirements, archived generated art and unfinished integration](docs/PASSOVER_DRACODIA_1005.md). Finished password catalog, all-pilot portrait repair, alien arena/modular ghost and pellet/elite warnings are included. The Dracodia cinematic/runtime and four source sheets are preserved as an UNLOADED DRAFT; index.html and the suite do not load it. Portrait/effects/portal crops, scream registration, native animation fixes, arrival integration and complete cinematic QA remain. Fresh publication checks: 7,292 assertions, final success banner, exit 0; game and eight layer syntax checks pass; actual Furious FINAL3 review reaches fight with animated code/void and zero browser errors; screenshot inspected. Previous 44 arena checks and portrait/password evidence remain documented. Fresh origin/main fetch matched HEAD before publication; unrelated projects/user scratch remain untouched. Earlier local-only notes below record historical verification checkpoints. Gameplay implementation is paused at Mike's request.

October 5 alien arena and combat readability: [Deep black animated arena, modular ghost and warned pellet/elite attacks](docs/ALIEN_ARENA_1005.md). Five imagegen sources deploy 35 native loose cells; dark central swirling void, animated green code banks, independent ribs and full-view symbiote engulfment persist through all copies. Ghost keeps its complete head, actual articulated modules, white hits and opaque breakup; stronger host/ghost/Dracula patterns, real copied campaign controllers and forty-second Furious visits preserve exact HP. Stage 6 approaching-round asterisks and warned staggered elite gun rain. 7,292 full-suite assertions, exit 0; 44 native/pixel/review checks, zero browser errors. Four protected silent recording contacts inspected; not campaign clears or final balance proof. Review _shots/alien_arena_1005/review.html; QA docs/qa/alien_arena_1005.json. Local only, no commit/push.

October 5 all-pilot portrait repair: [Complete fixed frames and mouth-only speech for all nine Fury pilots](docs/PILOT_PORTRAITS_1005.md). Every menu/comm expression retains one complete authored bezel and stable size; speaking keeps heads/shoulders fixed, mirrored comm facing and idle return. Cole shouting repair retained, Lizzie emotion rails protected, Falva aspect preserved; legacy/Yuri avatar aliases covered. 7,274 full-suite assertions, exit 0; 236 native Chromium checks, zero browser errors. All nine native contacts inspected; speech animations/review _shots/pilot_portraits_1005/review.html; portable QA docs/qa/pilot_portraits_1005.json. Local only; no commit/push.

October 5 Cole dialogue portrait repair: [Fixed complete bezel and mouth-only animation](docs/COLE_PORTRAITS_1005.md). Normal speech keeps the supplied head/shoulders; all expressions keep four complete rails. Stage 6 shouting keeps one head/body anchor. Menu/comm facing preserved through XART, original art retained. 7,274 full-suite assertions, exit 0; 46 native Chromium pixel/dialogue checks, zero browser errors. Native pose contact and dialogue captures inspected; animation/review _shots/cole_portraits_1005/review.html; portable QA docs/qa/cole_portraits_1005.json. Local only, no commit/push; preserve prior work.

October 5 pinned passwords: [Permanent in-game catalog](docs/PASSWORD_CATALOG_1005.md). Password menu exposes all 59 current/new codes on nine pages, including bosses, minibosses, finale phases/copies, Stage X routes, unlocks and Cole previews. Existing authored panels, fonts and pad prompts; D-pad/mouse browse, A fills entry, B returns without submitting. Repaired duplicate raw keyboard edits. 7,274 full-suite assertions, exit 0; 89 native Chromium checks pass, zero browser errors; all nine page captures inspected. Review _shots/password_catalog_1005/review.html; portable QA docs/qa/password_catalog_1005.json. Local only; no commit/push.

October 5 GitHub publication: Mike requested publication of the combat integrity and overnight finale/Rebel upgrades. Fresh fetch found no incoming commits on origin/main. The verified batch includes runtime, authored source/deployed art, encounter passwords, builders, probes and portable QA. Latest full suite: 7,274 assertions, exit 0; 185 overnight native checks and eight recording checks pass with zero final browser errors. Scratch recordings/reviews remain ignored and unrelated projects, trailer scratch and original HAMA vocal FLACs remain preserved outside this commit. Earlier local-only notes below describe their verification checkpoints.

October 5 overnight upgrade: [Independent finale encounters, intact knight, live Rebels and laser collision](docs/OVERNIGHT_1005.md). Stronger mutated-drone and ghost attack books; spectral/black-symbiote introductions with 24 loose rotational views. Eight persistent boosted pools, real campaign donors, whole knight in eight head-complete poses, independently targetable sword/shield, Hammer combos, shield smite/Dark Code, exact-zero code shatter and Flash/Time Bomb pills. Sustained beams and Cole VI/VII/Fusion damage actual Rebel hulls; homing selects visible fighters. Gang defense stays live; Voss remains fast, Jace/Rook fire south. Genuine red/green stealth bombers, brighter authored late rounds, musical Hammer gun/spell upgrades, HAMA instrumental. Fixed real ace/carrier epsilon-width beam renderer stall. 32 new boss/copy/phase passwords; reference docs/PASSWORD_ENCOUNTERS_1005.md. 7,274 full-suite assertions, exit 0; 185 native checks plus eight recording checks pass, zero final browser errors. Eight focused silent gameplay clips (not full campaign completion), all knight poses and timeline contacts inspected. Review _shots/overnight_1005/review.html; QA docs/qa/overnight_1005.json. Local only, no commit/push; preserve unrelated work.

October 5 combat integrity: [Fusion collision, independent co-op weapons and cloak hits](docs/COMBAT_INTEGRITY_1005.md). Fusion impacts moved out of the weapon pool; P2 ricochets/shards retain attribution. Cole tier/unlock and primary choice are per-seat, chords suppress only their own ship, fresh runs clear tiers and loads validate saved values. Blind Fusion hits cloaked Nyx without exposing missile locks or double-hitting on reveal; phased hulls ignore splash. Multiple Rebel slots and centered single-contact duels verified. 7,240 full-suite assertions, exit 0; 19 new native/review checks and 25 existing Cole/Rebel checks pass, zero browser errors. Review _shots/combat_integrity_1005/review.html; QA docs/qa/combat_integrity_1005.json. Local only, no commit/push; preserve unrelated work.

October 4 Cole/Rebel update: [Selectable lasers, Fusion overload and stolen-tech introduction](docs/COLE_REBEL_1004L.md). Fire/A + Multi-retina/Y cycles earned VI yellow, VII black/homing, VIII Fusion with live equip updates. Generated authored lasers/charge/muzzle/shatter/fragments and rotating crystal-diamond cloak. Fusion rises through 300%, pink danger above 200%, red/white RELEASE at 300%, normal shield-proof overload death at 315%; swept module collision, splash and bounded damaging ricochets/shards. Protected Jace full-ball/gasp, Rook harmless slug rain, Voss fast angled turbo demonstration; lower four-allied wing. Authored main HUD restored above play. 7,223 full-suite assertions, exit 0; 25 native/review checks, zero browser errors. Review _shots/cole_rebel_1004l/review.html; QA docs/qa/cole_rebel_1004l.json. Mike authorized publishing this Cole/Rebel pass on October 4; prior unrelated local work remains preserved.

October 4 GitHub publishing batch: Mike requested publication of the accumulated campaign, Stage X, Rebel arsenal, modular finale, combat/audio/art and music-organization updates, including the final 2-pixel Spread Fire muzzle adjustment. Fresh fetch found no incoming commits on origin/main; Claude d69cffa4 was already inspected/imported in the October 3 working-tree integration. Latest full suite reaches its final summary with 7,200 passing assertions and exit 0; 49 current native Stage 3 checks pass with zero page/console errors, with earlier review/encounter evidence retained. Original HAMA voice FLACs, unrelated projects and local scratch remain excluded. Earlier local-only notes below are historical checkpoints.

October 4 Stage 3 recording pass: [Frost Cruiser / Rime Wall combat and projectile interception](docs/STAGE3_COMBAT_1004K.md). Reused Voss charge, modular gun geometry, original FOV/beam controllers and authored elemental FX. Gun pellets/ground shots cannot be shot down; real fire/ice balls and missiles can. Rime orbital guns, paired rocket volleys, laser commitment; miniboss warned charge. Spread flashes follow all nine authored noses. HP and Furious forms preserved. Playable review _shots/stage3_combat_1004k/review.html; final QA docs/qa/stage3_combat_1004k.json. 7,200 full-suite assertions, exit 0; 53 native/review checks passed, zero browser errors. Initial mock-canvas exception fixed. Local only; preserve all earlier work.

October 4 Stage X water/city regeneration: [Terrain-only coast over animated water](docs/STAGEX_COAST_1004J.md). Built-in imagegen military ports and coastal city around the snowy mountain; final edit removes painted lagoon water, waterfalls and foam. Native alpha exposes the four existing authored blue-water frames, at six FPS with independent drift; camera/world alignment retained. XHARR/XREBEL share it; Stage VI remains sky. Original art retained, no atlas edits. 7,177 full-suite assertions, exit 0; 15 new native checks plus 75 existing sky/encounter checks pass, zero final browser errors. Review _shots/stagex_coast_1004j/review.html; QA docs/qa/stagex_coast_1004j.json. Local only; preserve prior work.

October 4 sky encounter corrections: [Stage X arena, blue ace and arcade bombers](docs/SKY_REPAIR_1004I.md). XHARR/XREBEL and campaign rematches use the authored mountain/water arena; HARR6/REBEL6 retain Stage VI. Current larger giant fighter has twenty blue poses, six matching module plates and exact-alpha white hits; simulation owns part flash expiry. Bombing passes have six HP on every difficulty and can die to one lethal missile. 7,177 full-suite assertions, exit 0; 75 native Chromium checks and existing Furious stealth-flight regression pass, zero browser errors. Review _shots/sky_repair_1004i/review.html; QA docs/qa/sky_repair_1004i.json. Local only; preserve all earlier work.

October 4 campaign controls and save slots: [Navigation, menu ownership and persistent saves](docs/CAMPAIGN_CONTROLS_1004H.md). Left I→VIII→VII→VI works; III→IV points down; Up VI→X / Down X→VI moves the actual ship. Start opens Save/Load/Exit before Stage X reads input; slots own Up/Down and B returns to the menu. Manual writes verify bytes, retain selected map stage/bonus/X focus and survive reload. Generated blank chrome cartridges with authored font/ships; campaign hub and autosave verified. Review demo slots persist separately from live saves. 7,160 full-suite assertions, exit 0; 98 native Chromium checks, zero browser errors. Review _shots/campaign_controls_1004h/review.html; QA docs/qa/campaign_controls_1004h.json. Local only; preserve all earlier work.

October 4 floating Stage X correction: [Central floating city island](docs/CAMPAIGN_STAGEX_1004G.md). Generated deep rock underside, permanent elevation, ground shadow and hover/bob. City, X flag, whole-island pointer and both encounter orbits share one pose. Camera exposes the complete skyline; locked briefing no longer resets its letters. Locked viewing grants no fight; earned Harrier and five-Rebel launches preserved. 7,146 full-suite assertions, exit 0; 19 native/review checks, zero browser errors. Review _shots/campaign_stagex_1004g/review.html; QA docs/qa/campaign_stagex_1004g.json. Local only; preserve all earlier work.

October 4 campaign flags and routes: [Roman flags, permanent Stage X and physical Fury HQ](docs/CAMPAIGN_MARKERS_1004F.md). Generated I–IX in the approved X chrome style with stage colors, normalized mast-base anchors, locks, rank/selected/unlock states. X stays in the central city; both earned rematches and all five Rebel/Harrier orbit art preserved. HQ lettering is built into the regenerated building; extra map labels/old plaque removed. Fixed invisible HQ NaN bobbing. All nine pilot hulls support down 4→5 and up 7→8 / 8→1 with correctly placed trails and stable arrival headings. 7,143 full-suite assertions, exit 0; 69 native/review checks, zero browser errors. Review _shots/campaign_markers_1004f/review.html; QA docs/qa/campaign_markers_1004f.json. Local only; preserve all earlier work.

October 4 connected campaign landscape: [Large regions over one authored continent](docs/CAMPAIGN_LANDSCAPE_1004E.md). Mike approved the island scheme and requested terrain underneath. New connected eight-biome continent, eight large stage regions, central city/Stage X, HQ coast with original HQ icon, cosmic Stage 9 portal and satellite islets. Original blue ocean, clouds, flags, locks, typed briefing and progression preserved. Arrival overview then region focus; hovered/selected landmarks lift above anchored terrain. Horizontal D-pad path reaches every stage; Stage X/bonus cinematics share updated positions and camera framing. 7,130 full-suite assertions, exit 0; 23 final native Chromium checks and 12 live review checks, zero browser errors. Earlier incorrect hook name caught and fixed in Chromium. Review _shots/campaign_landscape_1004e/review.html; QA docs/qa/campaign_landscape_1004e.json. Local only; preserve prior work.

October 4 password shortcuts: [All thirteen stage and encounter codes](docs/PASSWORD_ROUTES_1004D.md). Added HARR6 / REBEL6 for direct Stage 6 fights; XHARR / XREBEL remain Stage X rematches. Skip normal opening and waves, retain encounter introductions and four allies; normal TURB still starts the full mission. Shortcut state clears on consumption and ordinary passwords; campaign X resets the Stage 6 flag. 7,118 full-suite assertions, exit 0; 36 native Chromium checks, zero page/console errors. QA docs/qa/password_routes_1004d.json; screenshots _shots/password_routes_1004d. Local only; preserve all prior work.

October 4 Rebel arsenal update: [Personal ability boxes, attached HP and survivor counter-scan](docs/REBEL_ARSENAL_1004C.md). All five baseline guns; Voss warned turbo rams + retained pink Fusion, Rook .50-cal slugs, Jace actual red/orange helix nova with eight mini balls, Nyx tracing cloak/hidden HP and broken missile locks, Kaia anchored alternating teal/black rockets. Generated five boxes/icons and 24 FX cells, true authored palette swaps; enemy ability boxes are collectible and shootable. Friendly five-ship ability badges restored through the icon atlas. Living scan priority Kaia -> Nyx -> Jace -> Rook -> Voss with Rook/Voss correction. 7,089 full-suite assertions, exit 0; 32 native and 25 playable review checks, zero browser errors. Review _shots/rebel_arsenal_1004c/review.html; practice blocks campaign writes. Local only; preserve all prior work.

October 4 hit-frame/palette repair: [Stage 6–8 white flashes and authored stealth paint](docs/FLASH_PALETTE_1004.md). Restored red/green Stage 6 bomber fighters from the approved blue source sheets in place of a recolored Harrier boss hull; verified unchanged metal, outlines, ordnance and alpha. Repaired white frames in the shared Stage 8 fleet atlas and late boss/modular render paths. 47 Chromium pixel and damage checks plus the Stage 6 stealth-flight probe pass with zero page errors; the full suite has 7,053 assertions, exit 0. Review `_shots/flash_palette_1004/review.html`. Local and uncommitted; preserve prior work.

October 4 follow-up: [Stage 6 / 8 teams, routes, portal and final combat](docs/CAMPAIGN_FOCUS_1004B.md). Removed the second ally split; five-versus-five roster, stronger staggered Rebel specials and living-pilot-only bars. The unchosen encounter travels to central Stage X and persists. Live Warden exit hands off directly to Stage 8 while retaining earned results. Stage 6 Prism, Stage 8 Dark Matter. Rotated the three finale tracks; new finalform.wav converted to MP3 for Dracula and all mimics. Independent Dracula hands/pull; twelve generated knight pose components with measured joints, actual Hammer timing and visible thrown sword/gun/spell/ground hazards. 7,053 full-suite assertions, exit 0; 37 native Chromium checks, zero errors. First suite run had two obsolete element expectations, corrected. Review `_shots/campaign_focus_1004b/review.html`; practice blocks save writes. Latest 15:15 recording sampled across its entire timeline. Local only, no commit/push; preserve all earlier work.

October 4 recording repairs: [61:29 timeline audit and repair evidence](docs/GAMEPLAY_AUDIT_1004.md). Finite Stage 4 shield, Forge Up/global-unlock fixes, stronger orbs and Stage 3/4 attacks, guaranteed Hammer 8%→38% reserve, in-engine modular death and distant Earth homecoming. Five-versus-five Rebels keep all HP readouts and whole-hull burning deaths with large shocked portraits fading white. Approved red/green stealth bombers and consistent blue ace art; Stage 6 map return. Stage 8 donor forms now execute real campaign controllers with persistent HP/modules and stronger alien attacks. Generated connected biome islands/central city, hover lift and arrival zoom. Passwords: `RIFT9`, `XHARR`, `XREBEL`; both X routes play LevelX. 7,038 full-suite assertions, exit 0; six native Chromium probe reports with zero errors. Initial four obsolete Forge expectations corrected and documented. Review `_shots/gameplay_audit_1004/review.html`; QA `docs/qa/gameplay_repair_1004.json`. Video sampled every two seconds across its entire timeline; not a full audio review or human campaign clear. Local only, no commit/push; preserve prior work.

October 4 Rebel expansion: [Five personal weapons, Gang Mode and Decker's experimental team cloak](docs/REBEL_GANG_1004.md). Voss pink Fusion + asterisk, Kaia upgraded Falva roller, Rook heavy guns, Nyx/Jace stealth. Three of five at half HP trigger colored charge and missile/turbo/helper upgrades. Live, protected eight-beat rescue scene, original multi-Retina counter-scan, generated wave/swirl/reveal, complete hulls and no rebel shields. 7,022 full-suite assertions and 31 native Chromium checks pass; zero browser errors. Review `_shots/rebel_gang_1004/review.html`; source `assets/rebel_gang_1004.js`; QA `docs/qa/rebel_gang_1004.json`. Local only; preserve all prior work.

October 3 finale correction: [Three outer encounters, Dracula-only transformations, whole rebels and live protected dialogue](docs/FINALE_STRUCTURE_1003J.md). Normal drone arrival/mutation → mutated-drone fight → ghost fight → Dracula with eight persistent modular lives. One gauge fills eight times only on Dracula; actual active HP/color and broken weapons persist. Source-specific attacks, initialized HP budgets and single final reward verified. Rebel ships stay whole under damage, all shields removed; Stage 6 dialogue keeps flight/scrolling live while remaining timed and protected. 6,993 full-suite passes and 106 native checks; zero browser errors. Review `_shots/finale_structure_1003j/review.html`, evidence `docs/qa/finale_structure_1003j.json`. Local only; preserve all prior dirty work.

October 3 combat feedback: [Modular Stage 2 Reaver, generated boss beams/muzzles and full sound pass](docs/COMBAT_REAVER_AUDIO_1003I.md). Six articulated/destructible Reaver parts share live shot/Retina/hardpoint geometry. Six beam colors with three frames each and matching muzzles cover boss/miniboss laser renderers, including deployed Warhive taper. Twenty generated/mastered sound families cover missing attacks, impacts, targeting, teleports, code breakage, Stage 2 firewalls, Fusion and Cole VI/VII; silent Cyclone/Turbine paths fixed. 6,967 assertions and 260 native Chromium checks pass, including actual mixer playback of every new cue and all eight finale forms; zero browser errors. Review `_shots/combat_1003i/review.html`, portable evidence `docs/qa/combat_1003i.json`. Local only; no commit/push. Preserve prior dirty work.

October 3 Stage 6 and Hammer homecoming: [Protected dialogue, rebel portraits/music and orbital victory](docs/STAGE6_HAMMER_HOMECOMING_1003H.md). Approved stealth palettes cover all Stage 6 bombers; Cole/rebel introductions are timed and block combat. Complete rebel frames and five generated portrait boxes; every rebel fight uses Stage X music. Actual Hammer portrait and 25% less Furious chromium armor. Generated current-Furyship ending includes complete destruction, a static six-second fade to monochrome, crew welcome and shrinking Earth descent. 6,958 assertions, 34 native checks, 13 Stage X checks and Hammer arrival regression pass; zero browser errors. Review `_shots/feedback_1003h/review.html`; portable evidence `docs/qa/feedback_1003h.json`. Local only; preserve prior dirty work.

October 3 music organization: [Assigned independent miniboss tracks and final boss form 2; consolidated named music](docs/MUSIC_ORGANIZATION_1003.md). All 51 files live in assets/game/music with LevelN/LevelNmb/LevelNb naming and preserved hashes. Native warning gates, form transitions and audio decoding pass. Catalog/README retain original names. Local only.

October 3 music naming: active Stage 2/3 miniboss tracks renamed to miniboss2_magma_ward.mp3 and miniboss3_frost_cruiser.mp3; removed misleading unused2/unused_fire/unused_fire2 aliases. Audio bytes unchanged. Eleven numbered unused tracks remain archived.

October 3 campaign UI: [Blank typed mission panels, relocated Theater Progression and stable Lizzie portraits](docs/MAP_BRIEFING_LIZZIE_1003G.md). Progression now sits above the briefing on the game canvas. Generated blank frame, centered authored fonts and per-selection typewriter include Stage 9/Stage X. Lizzie keeps original character pixels in a complete fixed generated bezel; only the mouth changes while talking. Narrow layout preserves aspect and one prompt row. 6,952 full-suite assertions, 25 native checks and existing campaign regression pass, zero browser errors in completed passes. Review `_shots/map_briefing_1003g/review.html`. Local only; preserve prior dirty work.

October 3 Herald and enemy warnings: [Restored modular Herald and original warnings for every Level 7/8 mutant and alien](docs/HERALD_WARNINGS_1003F.md). Mike explicitly restored Herald of Death and authorized higher-quality modular regeneration. Six generated components, destructible wings/cannons, skull weak point, matching shot/Retina/contact geometry, original warnings, native death and normal stage resume. Fixed missing emitter ownership and original warning preloading for all affected enemies. 6,952 full-suite assertions and 65 native Chromium checks pass; zero browser errors. Review with engine replay and playable miniboss: `_shots/herald_1003f/review.html`. Local only; preserve prior dirty work.

October 3 Stage X music and original warnings: [Gasline and restored warning/Retina visuals](docs/GASLINE_ORIGINAL_WARNINGS_1003E.md). Complete 88.36-second stereo Gasline converted to 256 kbps MP3 and registered as the dedicated Stage X looping score; normal Stage 6 music remains separate. Stage 8 now uses original boss FOV/alert art, ground Retinas and ordinary-enemy lane bands. 6,917 assertions and 13 native Chromium checks pass, including actual deployed music playback and audible waveform capture. Review `_shots/original_warnings_1003e/review.html`. Local only; preserve earlier dirty work.

October 3 code wall correction: [chrome rows, red shield and reconstruction scan](docs/CODEWALL_1003D.md). Generated horizontal blue/chrome rows alternate left/right and keep moving under separate impact flashes. New binary-chip shatter replaces crystal bursts; knight projects a red kite barrier from his modular shield. Shared growth/rotation geometry handles bullets and Retina, including pre-acquired locks. Vertical reconstruction replaces spherical form transitions. 6,917 assertions + 147 native Chromium checks pass, zero browser errors. Actual-engine review `_shots/codewall_1003d/review.html`. Local only; preserve earlier dirty work.

October 3 modular finale correction: [all forms modular, head-only knight and one refilling gauge](docs/FINALE_MODULAR_1003C.md). Mike explicitly superseded the Stage 8 whole-plate restriction. All eight forms now use independent authored components, live weapon muzzle/hit/Retina geometry, recoil and breakage; knight has separate corrected head, arms, sword/shield and generated power-up FX. One boss housing fills eight successive times and then follows active-form HP/color. 6,893 full-suite assertions and 122 native Chromium checks pass, zero browser errors; actual engine replay in `_shots/finale_modular_1003c/review.html`. Local only; preserve earlier dirty work.

October 3 late-stage primary and eight-life finale: [chainguns and alien boss progression](docs/FINALE_PRIMARY_1003B.md). All nine pilots default to anchored chainguns from Stage 6, including password/old-save entry; explicit MG choice survives saves. Remaining Stage 7 canisters/mines now use selected mutants. Eight independent Stage 8 identities with stacked colored HP, new whole Furnace/Cryo/Storm/Harrier/Warden reels, host arm modules, gravity/orbits, committed laser warnings and chained knight jumps/slashes. Native finale 99 checks and existing mutant regression 76 pass with no browser errors; host/knight video in `_shots/finale_1003b/review.html`. Local, no new commit/push; preserve the earlier integrated work. See linked notes for full-suite evidence and initial fixes.

October 3 GitHub + Monster Mutator integration: [downloaded build and selected enemies](docs/GITHUB_MUTATOR_1003.md). Fetched Claude branch `d69cffa4`; imported its inspected delta while preserving local work (HEAD remains `938d1079`, no commit/push). Independently added October 2 layers coexist under distinct names. Seven selected final enemy revisions now replace existing Stage 7/8 slots; Rifle Locust, Hexpyre and Hellhugger have animated/destructible modules. Full Hammer arrival keeps the trap taunt and completes the opening jump before Chromium activation. 6,554 assertions pass; native roster 76, Stage 8 42, HAMA 14 plus stealth/Fusion/full-arrival probes pass with no browser errors. Initial failed runs and fixes are documented. Not campaign clears or final balance. Review: `_shots/mutator_gameplay_1003/review.html`.

October 3 Rifle Locust revision: ID 06 now has neon-red hull/pods, pink organic connections and charcoal rifles/laser markings. Built-in image generation produced the assembled revision and a six-component sheet. Source images, exact prompts and SHA-256 hashes are in `_ART_SOURCES/monster_mutator_1003/revision2/manifest.json`; measured sockets/pivots are in `rigs.json`. Gallery now contains three modular art studies. Rifle Locust keeps its hull upright while rifles aim/recoil independently and pods articulate. Native Chromium verified loaded art, moving/separated modules, gallery controls, mobile fit and zero page/console errors; screenshots inspected. No campaign wiring, runtime edits, commit or push.

October 3 selected Monster Mutator revisions: Mike selected IDs 01,03,04,06,07,08,11. Final current art and exact prompts are in `_ART_SOURCES/monster_mutator_1003/revision2/manifest.json`; preserved superseded edits have active=false. Latest steering: 01 has a new four-sensor/vertical-maw face; 04 has no hanging triangles and yellow eyes/cannon interiors; 08 has no raised shoulder fins. Hexpyre and Hellhugger have generated separate component sheets and measured `rigs.json`, verified in the art-only browser animation preview. Hellhugger demonstrates fragile three-hit core and fast claw lunge, not final campaign balance. Review: `_shots/monster_mutator_v2_1003/review.html`. No campaign wiring, runtime edits, commit or push in this art pass.

October 3 Monster Mutator selection set: 15 generated drone/monster fusion candidates are preserved in `_ART_SOURCES/monster_mutator_1003/`, with source pairings, exact prompts, hashes and a portable `roster.html` picker. Local review: `_shots/monster_mutator_1003/review.html`. Mike explicitly wants to PICK candidates before implementation. None from this set are wired into gameplay; proposed attacks are concepts only. Gallery images, saved shortlist, filtering, zoom and mobile layout verified in Chromium with zero page/console errors.

October 3 local Stage 8 pass: [Code knight, alien roster and shield shatter](docs/STAGE8_CODE_KNIGHT_1003.md). Generated sword/shield/jump/follow-up poses, full-body binary wall, code teleport/transformation, three upright orbital aliens, committed FOV/Retina lasers, and all-direction impact/shatter fragments. 6,392 assertions and 42 real Chromium checks pass, zero browser errors. Controlled fixtures are not campaign wins or final balance certification. Source art/prompts and portable evidence preserved; no game.js edit, commit or push.

October 2 GitHub upload prepared: campaign feedback and approved hooks-only HAMA audio accompany the downloaded d19c9666 build. Original voice recordings stay local and are excluded from this upload; remote publication awaits confirmation. Verification: 6,287 passing assertions, 118 campaign-feedback Chromium checks, zero browser errors; earlier HAMA playback checks are documented separately. Prior local/uncommitted labels below are historical checkpoints.

October 2 local campaign feedback: [Campaign repairs and straight enemy hulls](docs/FEEDBACK_1002.md). Generated Frost Cruiser/fire jet/Hammer parts, corrected Freezer and dam pacing, Level 2 ordnance/crates, Level 3 loadout/attacks, Level 4 lightning/helper/ram behavior, regular Hammer moves and unique death, and straight-facing Level 7/8 enemies with committed attacks. 6,287 assertions and 118 real Chromium checks pass; no page/console errors. Controlled fixtures are not campaign wins or verified final balance. Optional new modular sewer roster remains a follow-up. Local and uncommitted.

October 2 downloaded build: [GitHub build integration](docs/GITHUB_DOWNLOAD_1002.md). Local main is now `d19c9666`, downloaded from `claude/epic-clarke-rtfnuk`; local hooks-only HAMA work preserved. 6,247 assertions pass, plus Chromium HAMA and Stage 2/9 launch checks. No new commit or push.

Latest local audio pass: [HAMA — hooks and OH chants only](docs/HAMA_VOCALS_1001.md). Mike requested only the recorded hook and OH chants; removed all verses, spoken lines and their captions. Deep robotic processing retained. Revision 3 is active; original takes preserved. 6,203 assertions and 14 Chromium checks pass. Local and uncommitted.

October 1 GitHub upload: the dialogue/elemental feedback and encounter-feedback passes below are included in this publishing batch. Validation: 6,188 passing assertions, zero errors, plus the recorded native browser/audio checks. Earlier local/uncommitted labels below describe historical checkpoints. Temporary videos remain in ignored `_shots/`; portable evidence and reproduction probes are included.

Latest local encounter pass: [October 1 encounter feedback](docs/ENCOUNTER_FEEDBACK_1001.md). Stage 8 health/audio/warnings/performance, Stage 3 cold ordnance and paired turret beams, solo Stage 4 miniboss/new tanks, shorter aggressive Stage 5/6 bombers, Hammer rage recovery, northbound Fury departures, Furious Warden pressure, and generated Spreadfire animation reels. Full suite: 6,188 passes, zero failures; native combat/audio/render checks and three fixture videos. Local and uncommitted. Fixtures are not campaign clears or verified final balance.

Latest local bugfix: [October 1 dialogue and elemental feedback](docs/FEEDBACK_1001.md). Centered dialogue portraits and fitted text, regenerated eight-frame data wall, blue/red opposing-element critical flashes and +50% damage. Full suite: 6,129 passes, zero failures; focused Chromium and 33 cinematic checks pass. Local and uncommitted.

Latest local campaign work: [Expanded campaign world](docs/CAMPAIGN_WORLD_0930.md). Fury HQ north of Stage 1, central battleground, wider island spacing, northern portal/coast, eastern ruins, offshore islands, locked East Coast USA sector with four fixed-position cyan binary-row poses over a ragged transparent ocean edge, and fixed horizontal map ships. Latest native map/animation checks pass; prior full-suite baseline is 6,121 assertions with zero errors. Included in the October 1 publishing batch.

Latest local Stage 8 work: [Three-form finale and portable rotations](docs/REALM_ROTATION_PASS_0930.md). Generated destructible code walls/shields, three encounter lives, portal reunion, corrected steering and portable rotation pages. Full suite and native combat checks pass. Local and uncommitted; preserve prior work.

Latest local internal polish: [September 30 cinematic polish](docs/CINEMATIC_POLISH_0930.md). Portal leap, uniform storm lighting, Harrier beam rendering/collision, dam capture bookmark, and native checks are complete locally. No trailer reshoot or push yet. Preserve the earlier uncommitted work below.

Latest local cinematic work: [September 30 cinematic director pass](docs/CINEMATIC_PASS_0930.md). New mission bridges, nine pilot upgrade conversations, Cronos, Harrier/Rebel/Stage X dialogue, art and scene review are local and uncommitted. Preserve the repair pass below as well.

Current local work: [September 30 repair/art pass](docs/REPAIR_PASS_0930.md). The pass is uncommitted and includes corrected Fusion icons, armor/weapon wiring, encounter assets, and focused verification. Preserve it before pulling or merging.

# Current passover — September 28, 2026

**Opus: start with [docs/PASSOVER_OPUS_0928.md](docs/PASSOVER_OPUS_0928.md).**
It covers the complete September 27–28 upload, verified baseline, engine ownership,
generated assets, release tooling, prioritized remaining adjustments and acceptance criteria.
Portable evidence is in [docs/qa/opus_passover_0928.json](docs/qa/opus_passover_0928.json).

The last full suite reached its final summary with **0 errors**. Stage 6 now uses
the Eclipse Siege Bomber miniboss and Warhive Harrier/Ace boss. Stage 8 form 0 is
the newly mutated alien vessel. The text below is preserved historical context;
its uncommitted status, incoming commit warnings and old failure counts are stale.

---

# Handoff to Codex — 2026-09-13 (from Claude)

Read `CLAUDE.md` in this folder first. Its tail has notes for every drop below.

## Status
- **Nothing is committed or pushed.** All of the work below is local in the working tree.
- **origin/main is ahead** by two Tempest-staging commits from another session, labelled 0912u and 0912v. My local drops also use the labels 0912u–0912z, so the labels clash.
  - Before committing: `git fetch`, rebase or merge, and relabel the local drops.
  - Commit only when Mike asks.
- **Test suite** (`node _BUILD_SOURCE/test_fl.js`, a CRLF file): 3,626 checks pass and 61 fail. All 61 failures already existed before these drops; don't chase them as regressions.
  - To spot a new failure, compare the list of failing check names against the previous run, with the numbers in them masked.
- **C: drive has about 5 GB free.** Don't make worktrees or full copies of the repo.

## How to verify changes
- The suite has missed real bugs before. Check anything visible with `_BUILD_SOURCE/shoot.py`, which runs the game in real Chromium; the probe scripts are listed below.
- `assets/game.js` is about 64.7k lines with LF endings. Have only one writer editing it at a time.

## Changes in the working tree
| Drop | What changed | Probe |
|---|---|---|
| 0912x | Stage-3 boss laser warning: FOV cones (`L23_FOV`, `l23FovDraw`) go green, then yellow, then red; alert frames use `bmfx_alert_<col>_danger` | `probe_fov_telegraph_0912x.py` |
| 0912y | Every hit now flashes the enemy through `markHit(t,f)`, which runs before shields and part routing: enemies, `hitBoss`, `hitSubBoss` and the Furnace Tyrant (`fztFlashSprite`, plus a nearest-part fallback in `furnaceHit`). The sealed quad-laser is exempt and keeps its shield pulse. Six enemy draw functions gained hit tints | `probe_hitflash_0912y.py` |
| 0912z | Juggernaut's two wrecking balls: the chains are anchored under the hull (`WB_CHAIN0=14`, `wreckPos`/`wreckSync`) and cleared on special end, death and the attract demo. His charge dash is easier to see: launch ring, afterimages, bigger wake, landing ring, sound | `probe_wreckdash_0912z.py` |
| 0913a | The spaceship is used in every space scene (`spaceShipActive()`, `gravityModeRetain`) with per-pilot palettes. The transformation is fixed (no shrink or black frame; doesn't replay after returning from stage 9). Also a spaceship death spin and somersault frames. The weapons atlas gained 16 cells | `probe_spaceship_0913a.py` |
| 0913b | Tempest Leviathan is now stage 6's miniboss (`SUBBOSS[6]`), with the Blacksteel Raptor as the alternate (`ALTBOSS[6]`). Art is in `assets/game/bosses/tempest/`; the patch was applied by `patch_tempest_0913b.py` | `probe_tempest_0913b.py` |

New suite sections are §289–§293.

## Open decisions for Mike
1. Once the spaceship is earned, re-entering stage 5 from the map skips the transformation. Should it play every time?
2. Tempest Leviathan:
   - Hitting a laser port flashes the whole hull. On the quad-laser, only the hit turret lights.
   - Its frenzy lasers draw over the MINI BOSS bar.
   - Its needles are the fastest enemy round at 7.49 px/frame.
   - A ram from the right edge can park half hidden behind the EQUIPPED box.
   - The pursuer can't clear a player hugging the bottom edge.
3. Razorback pellet collision and exposed-gun laser hits resolved by Codex on
   2026-09-13; see `docs/BUGFIX_0913.md`.
4. Older open items:
   - End-card copy resolved by Mike on 2026-09-13; see the Codex update below.
   - Cole's silent middle nuke resolved by Codex on 2026-09-13; see `docs/BUGFIX_0913.md`.
   - Stage-5 laser cannon loudness.

## Trailer
- **Outputs:** v7 is on the Desktop as `BulletsOfFury_Trailer.mp4`. Older versions are kept as `_v2`–`_v6`, and Mike has seen v7.
- **Pipeline scripts:** `capture3.py`, `edit3.py`, `mix3.py`, `render_v7.sh`. They live in Claude's temp scratchpad, `%LOCALAPPDATA%\Temp\claude\...\scratchpad\trailer\`, which uses about 20 GB.
  - Ask Mike before deleting anything there.
  - That folder can vanish, so don't depend on it.
- **Mike's trailer rules:**
  - One file, with the game's own sounds, and sound is never silent.
  - Only live in-game footage.
  - Pilots get equal screen time, with no repeated shots and no pilot twice in a row.
  - No boss name cards.
  - No stage-6 bosses, except the Tempest Leviathan duel.
  - Full-size view; zoom only on intense moments.

## Rules
- Don't echo SpriteCook signed URLs.
- Don't delete user data.
- A PostToolUse `validate_antipatterns.py` hook error comes from a broken plugin and can be ignored.

## Codex update — 2026-09-13: trailer end-card resolved

- Mike approved replacing the closing credit with **BUILT WITH THE ASSISTANCE OF AI & HUMAN TOOLS.**
- Updated `edit3.py` and `edl3.json` in `_BUILD_SOURCE/trailer_v7/` and rendered trailer v8.
- Output: `C:/Users/Mdogg/Desktop/BulletsOfFury_Trailer_v8.mp4`; v7 remains at its original Desktop path.
- Verified 9,900 frames at 1920×1080 / 60 fps, duration 2:45, full decode with zero duplicate or dropped frames.
  The full AAC soundtrack and the first 9,566 video frames match v7 by SHA-256.
- The updated encoded end-card was inspected. The 44px credit fits on one line with safe margins.
- Validation: `docs/qa/trailer_endcard_0913_validation.json`. Reusable range renderer:
  `_BUILD_SOURCE/trailer_v7/render_endcard_0913.py`.

## Codex update — 2026-09-13: Stage 6 Tempest duo integrated

- Mike approved the black/gray duo integration and the MINI BOSS laser visibility fix.
- `SUBBOSS[6]` now selects `tempestbrothers`; Blacksteel remains stored in `ALTBOSS[6]`.
  Other stage assignments were preserved. The original solo Tempest remains spawnable.
- Reviewed source is pinned to GitHub main `f936f106d85d935aaf518fbac5ab34756bc26724`.
  Native adapter/source notes: `docs/TEMPEST_BROTHERS_0913.md`.
- Independent ship/aperture damage, combined gauge, coordinated pincer/ram timing,
  offscreen gray holds, survivor AI and one ordinary final slot release are wired into BOF.
  Gray's return/counterattack and visible regroup now also defer black's ram warning.
- Forward lasers stop below the gauge; duo drawing clips below its band and the gauge draws last.
- Real in-game recording with game SFX: `_shots/tempest_duo_0913/BulletsOfFury_Stage6_TempestBrothers.mp4`.
  58 seconds, 960×1024, 30 fps. The demonstration uses an invincible pilot and accelerated native
  damage gates; gameplay code contains neither capture behavior.
- Validation: syntax checks passed; full suite **3,647 passed / 60 failed**, exit 1,
  with **zero new failure names** against the takeover baseline. All 20 new native duo checks pass.
  Real Chromium **16 passed / 0 failed**, with zero page or console errors.
- Results: `docs/qa/tempest_brothers_0913.json`; complete log:
  `_shots/tempest_duo_0913/test_fl_final.log`. Nothing committed or pushed.

## Codex update — 2026-09-13: Mike's revised fighter flight

- After viewing the duo, Mike requested south-facing jets, rapid turns/slides,
  red-to-green flashes and charged thrusts toward the pilot with sounds. This
  supersedes the earlier fixed nose-up/one-axis direction for the active duo.
- Both authored hulls now bank, slide twice, aim red, lock green, thrust along a
  fixed committed vector, brake and turn back to the upper arena. Only one
  brother owns a pass at a time. Independent damage, disabled apertures,
  phase/death cancellation, survivor behavior and campaign slot release remain.
- Hull art, hardpoints, hit geometry, gunfire and laser lanes rotate together.
  The existing authored engine flames follow each tail. Charge, ready, turn,
  booster, engine-loop and braking cues use the game's own sound samples.
- Source and notes: `_BUILD_SOURCE/tempest_source_0913/fighter.js`, `adapter.js`
  and `docs/TEMPEST_FIGHTER_0913.md`. The source builder embeds them in the actual
  `assets/game.js` runtime; stored solo Tempest remains original.
- Video: `_shots/tempest_fighter_0913/BulletsOfFury_Tempest_FighterPasses.mp4`.
  Thirty seconds, 960×1024 at 30 fps, 900 fully decoded frames with game SFX.
  The recording uses real movement/fire input and an invincible demo pilot;
  health gates are not accelerated. Capture behavior is confined to the probe.
- Syntax checks passed. All 12 new fighter tests pass; real Chromium passed
  **10 / 0**, with zero page or console errors. Two full suite runs each finish
  **3,658 passed / 61 failed**, exit 1. Sixty failure names match the takeover
  baseline. The additional Stage 1 sand-wave sampling failure also exists in the
  earlier duo log from before fighter flight; no unexplained failure names remain.
- Results and comparison evidence: `docs/qa/tempest_fighter_0913.json`.
  Complete logs: `_shots/tempest_fighter_0913/test_fl_final.log` and
  `test_fl_confirm.log`. Silent video/WAV intermediates removed; final recordings
  and user data retained. Nothing committed or pushed.

## Codex update — 2026-09-13: complete thrust exit and physical return

- Mike requested that each jet turn into its thrust direction, fly offscreen,
  and then fly back onscreen. The charge now waits for nose alignment before
  ignition; thrust stays aligned and continues until the entire rotated hull
  and exhaust clear a camera edge. The old onscreen timer brake is removed.
- The jet turns fully offscreen, then flies back at 560 world pixels/second
  facing the inbound path. It reaches its visible upper-arena position before
  releasing its pass. No teleport or early timed return completion. Existing
  damage, phase/death cancellation, duo coordination and red/green cues remain.
- Notes: `docs/TEMPEST_RETURN_0913.md`. Source remains `fighter.js` in
  `_BUILD_SOURCE/tempest_source_0913/`, embedded in `assets/game.js`.
- Video: `_shots/tempest_return_0913/BulletsOfFury_Tempest_ExitAndReturn.mp4`.
  Thirty seconds, 960×1024 at 30 fps, 900 fully decoded frames with game sounds.
  Both brothers complete two exits and two returns. Real movement input,
  invincible demo pilot, unchanged health gates. Prior videos remain intact.
- Syntax checks passed. All eight new section-296 tests pass. Full suite:
  **3,666 passed / 61 failed**, exit 1, zero new failure names against the prior
  fighter baseline. Real Chromium **14 passed / 0 failed**, zero page/console
  errors, zero thrust/return heading mismatches or position jumps.
- Validation: `docs/qa/tempest_return_0913.json`. Run the actual-game probe with
  `python _BUILD_SOURCE/probe_tempest_fighter_0913.py --return-pass`.
  Nothing committed or pushed.

## Codex update — 2026-09-13: collision, laser reach and nuclear audio fixes

- Mike asked Codex to continue improving and bugfixing the game. Three reproduced
  bug groups were fixed; notes and reproduction details: `docs/BUGFIX_0913.md`.
- Razorback ordinary shots now use exposed-part collision, so sealed armor,
  destroyed guns and invulnerable transitions do not swallow pellets.
- Held lasers now intersect finite beam widths/endpoints with exposed Razorback
  guns and rotated Tempest geometry. The duo's combined center no longer blocks
  a reachable target, and targets beyond the endpoint remain unhittable.
  Tempest laser damage routes to the nearest intersected brother/live aperture.
- Cole's 1.8-second nuclear sound gate rejected the middle impact in a three-nuke
  sequence. The gate is now 120ms, with the same sample, volume, filters and pool.
  Actual before/after sound acceptance: true/false/true -> true/true/true.
  The three-cue game-mixer render has peak 0.3684, no clipping or errors.
- Readable sources: `_BUILD_SOURCE/bugfix_0913/beam.js`, `tests.js`, and the existing
  Tempest adapter/fighter sources. The actual self-contained runtime is `assets/game.js`.
  Rebuild with the Tempest integration script followed by `bugfix_0913/integrate.py`.
- Syntax checks passed. All 14 new section-297 tests pass. Full suite:
  **3,680 passed / 61 failed**, exit 1, zero new failure names against the prior
  return-pass baseline. Targeted Chromium **11 / 0**; original live Razorback
  attack/progression probe **19 / 0**; zero page or console errors.
- Validation: `docs/qa/game_bugfix_0913.json`. Actual before/after screenshots,
  archived before-runtime and sound proof are under `_shots/game_bugfix_0913/`.
  Existing dirty work and previous recordings preserved. Nothing committed or pushed.

## Codex update — 2026-09-13: four weapon graphics and sound

- Mike requested improvements to Cole Sonic Boom, Juggernaut charge dash and wrecking balls, and Laser Mist. Details: docs/WEAPON_FEEDBACK_0913.md.
- Authored compression fronts and wakes scale with sonic charge. Juggernaut has aft exhausts, clear ram plates, a solid dash hull and independent mechanical audio. Two opposite flails keep their original contact rules and ship anchors, with full steel art, visual recoil, stationary contact flashes and gated metal cues. Laser Mist has three blue launch flashes, readable lance echoes, split pulses and one sound per split beat per wave. Sixteen authored WAV mixes are registered through seventeen explicitly tamed runtime sound routes.
- Fixed duplicated generic ram explosions and dead-pilot charge ownership. Laser Mist now honors exposed miniboss geometry; sealed Razorback armor no longer consumes lances with fake wet impacts, while live rotated guns take damage.
- Syntax passes. All 23 new section-298 assertions pass. Full suite: 3,703 passed / 61 failed, exit 1, no new failing assertion names against game_bugfix_0913. Focused Chromium 27/0, original wreck/dash probe 23/0, zero page/console errors. Runtime LF and suite CRLF preserved.
- Video: _shots/weapon_feedback_0913/video/BulletsOfFury_Weapon_Feedback_0913.mp4. Forty seconds / 1,200 fully decoded frames / 960x1024 at 30fps, frame-aligned game sounds, protected demo pilot, unchanged target health gates. Cole 0–10s, dash 10–20s, flails 20–28s, mist 28–40s. All four mixer renders stay below clipping with zero cut voices.
- Sources and probes: _BUILD_SOURCE/weapon_feedback_0913/. They reproduce the runtime byte-for-byte. Proof and complete baseline failure names: docs/qa/weapon_feedback_0913.json. Prior dirty work, videos and trailer scratch preserved. Nothing committed or pushed.

## Codex update — 2026-09-14: stage 1–5 encounter corrections

- Mike clarified that surviving stage-1 fodder should burn at half health, and
  space Volley Missiles should be the passive homing upgrade in its space style.
  All requested stage 1–5 corrections are implemented. Details:
  `docs/STAGE_1_5_CORRECTIONS_0914.md`.
- Stage 1 uses clean plates plus animated half-health fire/smoke; Razorback and
  Overlord have dedicated weapon and rotor sounds. Stage 2 uses reviewed stable
  projectile flight poses. Stage 3 boats are stored with their assets/controllers
  preserved; ice-drone shots are larger, and every Rime Wall laser originates at
  an actual cannon with authored FOV warning and center charge.
- Olive Warden has mounted spread guns, centered dual straight guns, mounted
  rocket salvos and anchored flashes/sounds. Sovereign helpers fit outside its
  shield above the generator columns. A held laser pierces both nodes per column.
  Its unpowered dive clears the screen, flies overhead with a frame-shaped shadow
  and returns through the opposite edge without an invisible ground-plane hit.
- Stage 5 extends the scrolling sky to five seconds, uses the finished authored
  spaceship, keeps three passive homing volleys independent, reduces cannon gain
  to 0.30 and raises Shadow Orb damage 35%. Regent stays centered with charged
  escort fire and warnings for each new grid opening. Dense combat effects use
  0.40 encounter gain; voices and player volume preferences remain intact.
- Syntax passes. Full suite: **3,724 passed / 61 failed, exit 1**, final summary
  reached; all 61 failure names match `docs/qa/weapon_feedback_0913.json` after
  normalizing dynamic numeric observations. All 21 section-299 assertions pass.
  Real Chromium **42 / 0**, zero page, console or controlled-loop errors.
  Actual held input, authored source pixels and screenshots were checked.
- Preview: `_shots/stage_1_5_0914/video/BulletsOfFury_Stages_1_to_5_0914.mp4`,
  **76 seconds / 2,280 decoded frames / 960×1024 at 30 fps**, native game sounds,
  protected demo pilot and selected debug attack windows. Sovereign's demo has
  1-HP nodes after its 75/50% gates; runtime health gates are unchanged. All ten
  sound-effect renders stay below clipping; rapid-fire voice-pool reuse is
  retained. Music is not included. The recorder pins the buffer-source overload
  to fix inherited noise scheduling, without export-only normalization.
- Proof and current measured baseline: `docs/qa/stage_1_5_0914.json`. Sources:
  `_BUILD_SOURCE/stage_1_5_0914/`; exact archived dirty baselines and verification
  output remain under ignored `_shots/stage_1_5_0914/`. `integrate.py --dry-run`
  reconstructs the comparison byte-for-byte; mutation refuses subsequent edits.
  Do not run older integration workflows over this newer runtime. Runtime LF
  and suite CRLF preserved. No atlas changes, GitHub integration, commit or push.
  Prior staged/unstaged/untracked work and user/trailer recordings are preserved.

## Codex update — 2026-09-14: readable attacks and overnight work

Mike authorized autonomous work until morning. Full scope:
docs/OVERNIGHT_REQUESTS_0914.md. Thread heartbeat every 30 minutes through 8 AM
EDT September 14; quiet unless meaningful verified progress or required access.

Verified batch: docs/READABLE_ATTACKS_0914.md. Stage-1 jets lose their second
generic volley; Stage-3 blue side beams and finite central pulse; Furnace head
aim/pose commitment; Regent mounted-port warnings; six ordinary space impact
decorations; player flame shrinks 25%, boss flame widens 25%; Backspace pause
protection. Shared warning/gliding helpers ready. Full encounter migration,
dark-blue refinement, pause menu and new progression remain pending.

Syntax passes. Full suite **3,734 / 60, exit 1**, no new failing assertion names
against stage_1_5_0914; one prior randomized sand-tank assertion passed this run.
Section 300 9/0; Chromium 47/0, zero errors.
Proof: docs/qa/encounter_cleanup_0914.json.
Video: _shots/encounter_cleanup_0914/video/BulletsOfFury_Readable_Attacks_0914.mp4,
37 seconds/1,110 decoded frames, native sounds, protected debug pilot, no music.
Sources: _BUILD_SOURCE/encounter_cleanup_0914/. Do not run older integration
workflows over this runtime. LF/CRLF preserved. Nothing committed/pushed.

SpriteCook's Claude plugin exists but no authenticated callable SpriteCook MCP
is exposed to this task; ElevenLabs is likewise unavailable. Specified art is
pending. Do not extract OAuth credentials or substitute ImageGen for Mike's
specified SpriteCook work. Existing authored assets remain usable.

## Codex update — 2026-09-14: missile supplies

Verified details: docs/MISSILE_SUPPLIES_0914.md. Boss/miniboss supply clock
7-second first allowance/18-second restock, one shared live ammo box, Hard/Furious
25% faster restocking. Stages 1–7 x5/x10/x20; stage 8 x50/x100. Stage 9 retains
small x5/x10 pending Mike's quantities. x5 grants five (formerly three); x2
migrates to x5. Fodder-only one/two spinning projectile pickups, bounded scatter,
one roll per death, native one-round collect. Bosses/minibosses/props excluded.
Tier upgrades/caps remain pending SpriteCook art.

Syntax pass; full suite **3,745 / 61, exit 1**, final summary reached, names
match stage_1_5_0914. Section301 12/0; Chromium11/0, zero errors.
Proof: docs/qa/missile_supplies_0914.json. Sources:
_BUILD_SOURCE/missile_supplies_0914/. Prior runtime archived under ignored
_shots/missile_supplies_0914/. Do not run older integrators over this runtime.
LF/CRLF preserved, nothing committed/pushed.

## Codex update — 2026-09-14: green pause menu

Verified details: docs/PAUSE_MENU_0914.md. Drop-in Resume/Return to Main Menu/
Restart/Options/Help/Quit rows, authored green cursor/fonts and existing chrome
helpers. Grayscale playfield via one reusable offscreen composite. Music ducks
to 28% without altering the preference. Real Options/Help return to frozen combat;
Backspace cannot abandon the stage. Restart resets the same level.

Campaign Return/quit: verify rotating Autosav01/02/03.json localStorage records
(separate from manual slots), native anchored death spin/crash, game-over cues/
over voice, fade and title/exited state. SAVED only after identical readback.
Continue recovers latest campaign record after session loss; controls reset
preserves autosaves. These are browser JSON records, not Windows files.

Syntax pass. Full suite **3,756 / 61, exit 1**, final summary reached, all names
match stage_1_5_0914. Section302 11/0; Chromium14/0, zero errors.
Proof: docs/qa/pause_menu_0914.json. Sources: _BUILD_SOURCE/pause_menu_0914/.
Runtime SHA256 2fd799df3f07d58042ee5093e1e2ea935c772d12da6ee44f426a1541867f4bdd.
LF/CRLF preserved. No commits/push or user-data deletion. Bitmap button production
and remaining overnight scope stay pending in docs/OVERNIGHT_REQUESTS_0914.md.

## 0914 shared laser warnings
Shared laser families now inherit the same three-second authored green/yellow/red FOV. Stage-3 cannons use dark-blue bodies and a narrow light core. Full suite 3759 pass / 61 baseline failures, exit 1; Chromium 7/0, no errors. Proof: docs/qa/shared_laser_warnings_0914.json. Combined pause/laser video is pending a clipping correction for overlapping death explosions. Retina target eligibility is next.

## 0914 Retina component target pass
Read docs/RETINA_TARGETS_0914.md and docs/qa/retina_targets_0914.json. Runtime SHA256 95b659ac2bd4327f292e4197fdb56bf8aa6449baa7ca3632ea471373c8123e53; suite 3771/60 exit 1, no new failure names, historical random sand-tank check passed. Chromium12/0. Component targets and manual missile damage verified. Native pause/blue-laser video now fully decoded with unclipped audio: _shots/shared_laser_warnings_0914/video/BulletsOfFury_Pause_and_Blue_Lasers_0914.mp4. Current source: _BUILD_SOURCE/retina_targets_0914. Do not run old integrators over this newer runtime. Next: directional multi-lock upgrade and five-second sequential missile firing; universal no-one-shot rule, Hard/Furious variants and achievements remain pending. Preserve all dirty work; no commits/pushes/deletions authorized.

## 0914 directional Retina Scan verified
Read docs/RETINA_SCAN_0914.md and docs/qa/retina_scan_0914.json. Four-target directional scan, five-second expiry, 50ms sequential manual missiles, exact ammo, invalid-target skips, pause/death cleanup and campaign equipment persistence. Native13/0; section30516/0; full suite3787/60 exit1, no new assertion names (historical random sand-tank check passed). Runtime SHA256 3e8159683cba3b65b344244e50de5ee300e0f7371e2119eb5b30bd9511a14212. Current source _BUILD_SOURCE/retina_scan_0914; older integrators must not overwrite this runtime. Native14sec preview _shots/retina_scan_0914/video/BulletsOfFury_Retina_MultiLock_0914.mp4, 420 frames decoded, 60% in-game SFX, no export normalization. Universal no-one-shot rule and remaining Hard/Furious/achievement/missile-tier work are still pending. Mike explicitly resumed development after the overnight schedule ended with "continue on lad!". No new recurring automation was created.


## 0914 Arcade credit rules and request tally
Mike asked to continue unfinished work and maintain a tally. Read docs/REQUEST_CHECKLIST_0914.md: 135 entries, 44 complete / 11 partial / 80 pending. Its editable source is docs/REQUEST_CHECKLIST_0914.json; regenerate with python _BUILD_SOURCE/update_request_checklist.py. Do not count partial encounter passes as finished designs.
Arcade stocks now match Easy/Normal/Hard/Furious lives 7/5/3/3, continues 7/5/3/1, including a run-wide bank in Stage 9. Campaign/co-op tuning stays separate; campaign loads refresh DIFF. Native difficulty and credit prompts verified with real Enter input; the Stage-9 retreat cannot refund Arcade credits. Proof and limits: docs/ARCADE_RULES_0914.md and docs/qa/arcade_rules_0914.json.
Full suite 3804/60, exit 1, final summary reached, no new failing assertion names; section306 17/0. Native Chromium 22/0 with no page/console/loop errors. Runtime SHA256 41ee9c77220592dc818374cd5a1fba54d870ac22036c113c38284d48c9b15835. Runtime LF and test CRLF preserved. Current patch sources _BUILD_SOURCE/arcade_rules_0914; do not apply older integrators over this build. No commits, pushes or user-data deletion.
Next shared foundations remain universal no-one-shot damage and elemental/shield behavior; encounter variants, production assets and achievements remain on the checklist. The overnight schedule expired; this was Mike's resumed interactive request, not a new background automation.


## 0914 easiest-to-hardest queue — first two entries verified
Mike asked for the full list in chat and work ordered easiest to hardest. Current queue is docs/WORK_ORDER_0914.md, generated from workOrder/difficulty fields in docs/REQUEST_CHECKLIST_0914.json. Tally: 135 entries, 46 complete / 11 partial / 78 pending (89 unfinished). Follow ascending ready work; respect dependencies and skip unavailable external assets. This replaces the earlier foundation-first ordering.
Completed SPACE-15: eight supplied Space Fighter model announcements; Decker currently displays SPACE FIGHTER DECKER pending Mike's requested naming response (SPACE-16). Completed MODE-06: Hard/Furious Life Up chance +25% on both midpoint and ordinary death routes, without stealing ammo/shield outcomes. Midpoint pickups use visible camera bounds. New ship and Life Up replacement art remain pending.
Proof docs/EASY_QUEUE_0914.md and docs/qa/easy_queue_0914.json. Native Chromium25/0, no page/console/loop errors; section30715/0; full suite3818/61 exit1, final summary reached, no new failure names. Historical random sand-tank assertion failed this time. Runtime SHA256 e2e95dfbd9e0d65bfe55ac40d4989f3be1aba6d3ad4f33c9c89efe5f57674533. Sources _BUILD_SOURCE/easy_queue_0914; LF/CRLF preserved. No commits/pushes, new atlas art, data deletion or background automation.
Next ready item: MSL-09 remaining missile-supply frequency audit, then SPACE-11 source-ship inspection, S4-02 screenshot review and S2-05 actual flame shield from the opening frame. Decker naming is independently pending; do not invent a model.


## 0914 Draven and complete missile supply frequency
Mike named Decker's Space Fighter Draven and asked to continue. SPACE-16 and MSL-09 are now complete. Read docs/SUPPLY_AUDIT_0914.md and docs/qa/supply_audit_0914.json. Hard/Furious boss opening/repeat times 5.6/14.4s; fodder loose chance 12.5%; legacy single-ammo chance 7.75%; scheduled/scripted boxes receive one 25% bonus roll with a two-second, existing-box-clear queue. No recursive bonus or double bonus on the boss clock. Forced scripted x10 stays guaranteed.
Native27/0, real crate shooting/collection and real player death, zero page/console/loop errors. Full suite3839/61 exit1, final summary, section30821/0, no new failure names; historical random sand-tank assertion failed. One section307 fixture now allows the extra ammo interval above its life boundary. Current runtime SHA256 41a0790603c5e4d8320839e1083b19a6e123e9075fce334a744825dea888d7d5. Sources _BUILD_SOURCE/supply_audit_0914; LF/CRLF preserved. No commits/pushes/atlas edits/user-data deletion.
Tally 135: 48 complete / 10 partial / 77 pending. Follow docs/WORK_ORDER_0914.md. Next SPACE-11: distinct new SpriteCook ship concept not yet identified; current ledger contains Warden/map assets and the known active ship traces to _ART_SOURCES/gravity_mode_v2. Do not select the already-shipped ship or GPT component master as the new concept without evidence. Then S4-02 screenshot review and S2-05 actual flame shield opening.


## Codex update — September 14: Furyship source selected

Mike approved `assets/game/gravity_mode/furyship_somersault_13.png` as the top-down replacement reference. Actual PNG and the existing sixteen-frame reel were inspected. SPACE-11 is complete; new parts, perspective frames, transformation and speed effects remain pending. See `docs/FURYSHIP_REFERENCE_0914.md`. SpriteCook is unavailable; tool-choice clarification is pending. No runtime or atlas change in this pass.


## Codex update — September 14: Furyship generated candidates

Mike approved built-in image generation for the ship. Eight master sheets and 70 normalized transparent candidate frames are saved with prompts/build metadata. Native Chromium rendered 71 assets including the approved reference with zero browser errors. Interactive preview also checked. See `docs/FURYSHIP_ASSETS_0914.md`. Exact assembly fit, intermediate animation/palettes and gameplay integration remain; SPACE-12/13 are partial. Runtime unchanged, no gameplay-suite rerun.


## Codex update — September 14: somersault and nine palettes

Added 12 generated somersault candidate frames (82 total frames) and 50 blue/cyan masks. Verified all 450 pilot/frame palette combinations and preserved all unmasked pixels. Native render: 83 assets including reference, no browser errors. See `docs/FURYSHIP_SOMERSAULT_0914.md`. Runtime integration/assembly fit and some frame-width drift remain. SPACE-14 is now partial; runtime unchanged, no gameplay-suite rerun.


## Codex update — September 14: Furyship installed in the game

Read docs/FURYSHIP_LIVE_0914.md and docs/qa/furyship_live_0914.json. The approved frame-13 hull, six-part assembly, 12 somersault poses, both eight-frame rolls, transition/speed effects and all nine palettes now run in the game. SPCBOY selects the preserved original fighter; campaign snapshots save/restore the selection. New cannon anchors and space death/Stage 9 rendering verified. Sources _BUILD_SOURCE/furyship_live_0914; no atlas repack or shipping-manifest changes in this batch.

Native Chromium 26/0, no page/console/loop errors. Full suite 3,849 passed / 61 failed, exit 1, final summary reached; failure names exactly match docs/qa/supply_audit_0914.json. Section309 10/0; two older replacement-sensitive assertions updated with separate legacy checks. Runtime SHA256 3fc67f9238c635ee3367f574a2a57bd2a1094ffadcf52aae1b7e76de59a02e45. LF/CRLF preserved.

Video: _shots/furyship_live_0914/video/BulletsOfFury_Furyship_0914.mp4 (26 seconds, actual game sound events, export gain prevents clipping, full decode passed). Capture skips completed HQ dialogue/entrance and uses fixture-only invincibility; this is not a full balance run. SPACE-13/14 complete; SPACE-12 partial for wingspan/silhouette drift and smoother component turns/fit. Tally 135: 51 complete / 11 partial / 73 pending, 84 unfinished. Preserve docs/WORK_ORDER_0914.md; the larger encounter requests are still open. No commits/pushes/deletion/background automation.


## Codex update — September 14: cloud-flight intro revision

Mike rejected the small six-piece assembly and slow sweep. Read docs/FURYSHIP_CLOUD_INTRO_0914.md and docs/qa/furyship_cloud_intro_0914.json. The new Stage-5 intro now stays at 420px/s through sky, clouds, clearing, assembly, white fade and countdown. Twelve independent pieces use the existing authored kit; full-size loose cells draw at 194.7px around a 118px cinematic hull. The local energy ring is smaller. Space replaces sky only under opaque white, which also covers HQ and scanlines. Latest request explicitly supersedes the old no-fade rule for this intro. Retained new fighters skip rebuilding and stay 48px; other stages/legacy route unchanged.

Native full launch from t=0 including all HQ dialogue: 11/0; separate retained/animated-exhaust probe passed; zero page/console/loop errors. Full suite 3,850/60 exit1, final summary, no new failure names. Historical random sand-tank assertion passed; no fix claimed. Test file unchanged. Runtime SHA256 3d55604968cc2af62926ed8ef7ed296a03cf051c57d87686ad6434d9405e2978. LF/CRLF preserved. Video _shots/furyship_cloud_0914/BulletsOfFury_Cloud_Transformation_0914.mp4 (26 seconds, game sound effects, fully decoded). Sources _BUILD_SOURCE/furyship_cloud_0914; do not reapply prior integrators over this build.

Tally still 135: 51 complete / 11 partial / 73 pending. SPACE-12 retains art consistency/fit/perspective refinement; SPACE-13 evidence updated for the revised staging. No commit/push/atlas edits/user-data deletion/background automation.


## Codex update — September 14: solid parts, individual arrivals and faster sky

Mike rejected part fades, perspective flips and travelling top/bottom clouds. Read docs/FURYSHIP_SOLID_ASSEMBLY_0914.md and docs/qa/furyship_solid_assembly_0914.json. Parts now use opaque top plates only, rotated in evenly spaced orbits. Twelve individual bottom entrances begin in the cloud section, 0.54s apart, each with the new game-engine furyPartArrival sound. Incoming kit draws above clouds, plane beneath the holes. Entire kit stays opaque until the full white transition hides the completed-hull substitution. No per-part fade or mirrored transform. Side banks hold fixed positions; the central cloud deck passes once and does not wrap. Intro speed 1,000px/s, no braking. Flight roll/somersault frames unchanged.

Native full-launch checks 17/0, actual draw opacity/key/transform and twelve sound-cue timing audit passed; zero page/console/loop errors. Video _shots/furyship_solid_0914/BulletsOfFury_Solid_Assembly_0914.mp4 (26 seconds, game sound, full decode passed). Full suite 3,849/61 exit1, final summary, exact failure names from furyship_live_0914 baseline. Historical random sand-tank assertion failed. Test file unchanged; LF/CRLF preserved. Runtime SHA256 5150c9c4134da494bec2d2789b9e7fecfd4c022f8647302a470945f4072109b5. Sources _BUILD_SOURCE/furyship_solid_0914. Do not reapply old integrators over this build.

Checklist remains 51 complete / 11 partial / 73 pending. SPACE-12's assembly perspective blending is superseded by the opaque top-view rotation requirement; flight silhouette consistency and exact fit remain. No new bitmap/atlas/manifest changes, commit, push, user-data deletion or automation.


## 0914 - Solid space hazards and shared dialogue frame

See docs/DIALOGUE_HAZARDS_0914.md and docs/qa/dialogue_hazards_0914.json. Generated pilot-tinted rectangular dialogue plate, centered stable typewriter text, no decorative asteroid/comet ghosts, physical shootable hazards and real contact checks. Native 12/12, no browser errors. Full suite 3852 pass / 58 inherited failures, exit 1, no new failing assertion names. Preserve all working changes; no commit or push. Checklist updated.


## 0914 - Static projectile cells and pixel glow

Read docs/PROJECTILE_PIXEL_GLOW_0914.md and docs/qa/projectile_glow_0914.json. Stage-5 CFX rows now hold column 1; Stage-2 saws already held that column. Shared fixed-frame shots get stepped pixel lighting without blur or growing sprites. Spin/trajectory/collision unchanged. Native 19/19, zero browser errors. Full suite 3853/57, exit1, no new failure names. No atlas/test changes or commit/push.


## 0914 - New Yuri and readable typography

Read docs/READABLE_TYPE_YURI_0914.md and docs/qa/readable_type_yuri_0914.json. Legacy Yuri portrait routes now use the approved seven new expressions; talking holds the approved idle pose. All nine pilots have compact dialogue portraits. Added uppercase Command Signal dialogue/TrueType, Command Alloy game labels and nine biome stage font variants. In-play panels clear the bottom HUD. Native 9/9, zero browser errors. Full suite 3852 pass / 58 inherited failures, exit 1; no new failure names against recorded baselines. Font/portrait source assets retained, no existing atlases changed. Harness loads current font registrations and updated obsolete font/portrait expectations. Checklist: 57 complete, 11 partial, 70 pending (81 unfinished). No commit or push.


## 0914 - Pilot name flair

See docs/PILOT_NAME_FLAIR_0914.md and docs/qa/pilot_name_flair_0914.json. Shared bitmap nameplates now have pilot-colored edges, white highlights, dark keylines and a slow three-second halo in dialogue, cinematic dialogue, comms and pilot selection. Authored portraits/body lettering preserved. Native 11/11, no browser errors. Full suite 3853 pass / 57 inherited failures, exit 1; no new failing names. One obsolete source-call assertion now checks pilotNameDraw. No atlas changes, commit or push. Tally remains 57 complete / 11 partial / 70 pending.


## 0914 - Stage-4 visual audit and Furnace flame shield

Read docs/ENCOUNTER_VISUAL_0914.md and docs/qa/encounter_visual_0914.json. S4-02 closed by native visual review: the apparent orange beams are road markings; Warden emits short machine rounds at its mapped mounts and upper racks are part of the whole authored plate. S2-05 fixed: actual Magma Ward flame shield now draws throughout Furnace assembly; the intro-only overload-wave substitute is removed. Lazy cells hold a decoded flame frame; break, core rearm and vulnerable head lifecycle verified. Native 16/16, no browser errors; two silent gameplay clips under _shots/encounter_visual_0914. Syntax passed; full suite 3853 pass / 57 inherited failures, exit 1, no new names. No atlas/test edits or commit/push. Tally 59 complete / 10 partial / 69 pending (79 unfinished). Next ready item is S1-04 Razorback baseline speeds, then S3-07 Hard/Furious size/palette.


## 0914 - Razorback baseline speed

See docs/RAZORBACK_SPEED_0914.md and docs/qa/razorback_speed_0914.json. S1-04 done: travel +30%, turn +20%, shots and rocket acceleration/cap +20%, Sonic Hammer/Nova expansion +25%. Warning/attack timing, HP and authored art unchanged. Native 12/12, zero browser errors; standing-hit versus post-release keyboard escape verified. Syntax passed; suite 3852/58, exit 1, no new failure names against recorded baselines. No test/atlas edits or commit/push. Tally 60 complete / 10 partial / 68 pending (78 unfinished). Next S3-07: Hard/Furious miniboss royal-dark-blue/black palette and +35% size.


## 0914 - Frost Cruiser Hard/Furious hull variant

Read docs/FROST_CRUISER_VARIANT_0914.md and docs/qa/frost_cruiser_variant_0914.json. S3-07 complete: the actual stage-3 miniboss is Frost Cruiser, not alternate Cryo Spear. Hard/Furious hull dimensions increase 168 to 226.8 (+35%) and use cached black/royal-dark-blue armor, preserving alpha, linework and protected emitters. Actual mounts, ordnance origins, collision bounds and damage/enrage rendering verified; Easy/Normal and other encounters excluded. Native 12/12, zero browser errors. Syntax passed; full suite 3851/59, exit 1: 58 recorded failures plus one intermittent road-tank heading failure reproduced identically against the pre-change backup (nine controlled cases). No newly introduced failure found. Silent seven-second native preview under _shots/cryo_variant_0914. No source-art, atlas or test-harness edits; no commit/push. Tally 61 complete / 10 partial / 67 pending (77 unfinished). Next UI-09: pilot-select letter reveal and stat-bar fill, followed by UI-08 fullscreen presentation.


## 0914 - Three new boss music tracks stored

Mike supplied minderaser (Boss 1), Hazardous-Death (Boss 2), and Lie Down or Stay Down (Boss 3). Original WAV copies are in assets/game/music/newboss/; see docs/NEW_BOSS_MUSIC_0914.md and the folder inventory.json. SHA-256 verified against Desktop originals. Stored only: no existing music replaced, no runtime registration or encounter music assignments changed. Boss numbers are inventory labels pending future direction.


## 0914 - Frost Cruiser nose laser correction

Mike clarified the wing pods are missile turrets and the nose must shoot Falva-style black/blue lasers. Read docs/FROST_NOSE_LASER_0914.md and docs/qa/frost_nose_laser_0914.json. Nose now launches fixed-frame fllaser_0 bolts at 24x112 and 0.34s cadence, with cached black/blue palette, four-step pixel lighting, laser muzzle/audio, nose-tail launch anchoring, committed aim and oriented shaft collision. Wing missiles and shared Jungle Cruiser nose remain unchanged. Full-tail culling and lazy-ready release guard verified. Native15/15, zero browser errors; nine-second silent native preview under _shots/frost_nose_laser_0914. Syntax passed; full suite 3852/58, exit1, no new names. No source-art/atlas/test-harness/music changes or commit/push. Checklist S3-14 added complete: 139 entries, 62 complete / 10 partial / 67 pending (77 unfinished). The charged sweeping beam and new difficulty attacks remain pending; next queue item UI-09.


## 0914 - GitHub integration and publication

Mike authorized committing and pushing the complete current build. Local build commit 45174735 collects game changes, art, new boss music storage and verification notes. Integrated origin/main through f936f106, preserving the Stage-6 duo and both stored ALTBOSS6/ALTBOSS8 encounters; Stage 8 now has no miniboss as requested in the incoming commit. Both sets of development notes are retained. Post-merge syntax passed, native15/15 with no browser errors; suite 3850/58, exit1, no new names. Read docs/GITHUB_BUILD_0914.md and docs/qa/github_build_0914.json. Unrelated nested projects and ignored scratch remain local.


## 0914 - Pilot text and stat reveal (UI-09)

Read docs/PILOT_REVEAL_0914.md and docs/qa/pilot_reveal_0914.json. The composed drawPilot screen now consumes the existing pcard reveal state for names, subtitle, biography, special and stat labels, then fills each bar from its left edge. Layout uses full strings; styled names keep one cached plate. Screen re-entry resets the reveal; Enter skips without same-press confirmation. Nine-pilot VM checks pass. Native controlled-time screenshots cover partial text, intermediate bars, skip and roster layouts; ordinary intro path not completed, and a review tab crashed during a large synchronous render batch before recovery with bounded steps. Full suite 3850/58, exit 1, no new failure names. UI-09 complete; tally 63 complete / 10 partial / 66 pending (76 unfinished). Next UI-08 fullscreen pilot screen, then ACH-09 boss fight timer. No commit/push.

## 2026-09-14 — generated input prompts / B is Back

Implemented Mike's consistent generated D-pad/action/Start prompts and logical B navigation; Backspace is deletion only. See docs/CONTROL_HINTS_0914.md and docs/qa/control_hints_0914.json. Final focused checks 25/0; full suite 3851/57, exit 1, no new failure names. Campaign-hub native proof is limited by the pre-existing missing CAMPHUB_ITEMS definition. AGENTS.md preserves the convention. Existing UI-08 and later work remain queued; nothing committed or pushed.

## 0914 — Pilot fullscreen desktop pass (UI-08 partial)

Read docs/PILOT_FULLSCREEN_0914.md and docs/qa/pilot_fullscreen_0914.json. Pilot now owns a proportional browser-sized buffer; card/roster expand and pointer mapping follows. Desktop Axel/Lizzie five-stat layouts and B return verified. Portrait bounds and backing pixels are valid, but resize screenshots remain black; fresh default tabs recover. Keep UI-08 partial and first in queue until this is resolved. Viewport override reset. Syntax passes, reveal9/0, controls25/0, full suite3851/57 exit1 with no new names. No commit/push.

## 0914 — UI-08 complete and ACH-09 boss timer

Pilot resize verified in a real game iframe at 390x844 and 1100x620, both directions; earlier native viewport capture gap closed. Read docs/PILOT_FULLSCREEN_0914.md follow-up. Added upper-right unit-owned boss/miniboss timer: excludes initial entry/pause, includes respawns/later transforms, freezes on defeat. Read docs/BOSS_TIMER_0914.md and QA. Focused12/0, full3851/57 exit1 with no new names; native timer review no errors. 66 complete / 10 partial / 64 pending; 74 unfinished. Next ENG-03 shared gliding/follow integration, then S3-05 miniboss movement and S1-07 chopper movement. No commit/push.

## 0914 — Shared glide and two encounter movement fixes

ENG-03, S3-05 and S1-07 complete. Read docs/MOVEMENT_BATCH_0914.md and docs/qa/movement_batch_0914.json. Frost tracks sampled player X, returns vertically on a committed lane and follows 1.15s before beam charge. Chopper orbit phase latches once; pursuit and orbit-entry speeds are bounded. Weapon patterns retained. Focused23/0, suite3850/58 exit1, no new names; native both encounters no errors. 69 complete / 9 partial / 62 pending, 71 unfinished. Next S1-08 rotor audio, UI-10 ship frame alignment, UI-07 title silhouettes. No commit/push.


## 2026-09-14 Overlord rotor audio
Dedicated original helicopter rotor WAV replaces the servo placeholder. Native loop/release verified; syntax passes; full suite 3850 passed / 58 known failures, exit 1, no new names. See docs/ROTOR_AUDIO_0914.md. Checklist: 70 complete, 8 partial, 62 pending; UI-10 ship-frame alignment next. No commit or push.


## 2026-09-14 Pilot ship alignment
UI-10 complete: menu-only alpha-bound centers and shared reel scale. Native 72 stock frames, nine onion pairs, Axel/Decker menu verified. See docs/SHIP_ALIGNMENT_0914.md. Syntax passed; suite 3850/58 known failures, exit 1, no new names. 71 complete / 8 partial / 61 pending, 69 unfinished. UI-07 next. No commit or push.


## 2026-09-15 Opener pilot pairs
UI-07 complete: nine frontal bodies beside ships, Cole-first 12s sweep. Corrected Lizzie to current ship. Native nine pairs and Enter-to-title verified; full suite 3850/58 known failures, exit 1, no new names. See docs/OPENER_LINEUP_0915.md. 72 complete / 8 partial / 60 pending; 68 unfinished. No commit/push.


## 2026-09-15 Generated pause-button art
UI-06 complete, six rows share generated plate with preserved endcaps and bitmap labels. Native selection/resume verified; suite 3851/57 known failures, exit 1, no new names. See docs/PAUSE_ART_0915.md. SpriteCook spent 16, balance 118. 73 complete / 8 partial / 59 pending, 67 unfinished. MODE-08 Life/Continue Up art next. No commit/push.


## 2026-09-15 Stage 4 death / Stage 5 transformer
Read docs/BOSS_BATCH_0915.md and docs/BOSS_DESIGNS_0915.md. New Easy/Normal Stage 5 chrome hammer transformer, authored SpriteCook reels, distinct manual missile knockback, 15-second ball and warned hammer leaps. Stage 4 cinematic cookoff and regenerated reflected-edge highway loop. Stage 2 identity question unanswered; do not replace its boss or generate the wrong head. Full natural-play balance remains SPACE-06. QA in docs/qa/boss_designs_0915.json. Preserve all dirty work; no commit/push.
Final 0915 boss QA: syntax pass; focused 20/0; full suite 3850 pass / 58 recorded failures, exit 1, no new names. Checklist 148 total: 79 complete / 8 partial / 61 pending (69 unfinished). SpriteCook balance 22.

## 2026-09-15 Overnight gameplay continuation

Chrome Hammer now has its one-hand vertical boomerang, Hard/Furious difficulty aces are injected across all nine stages, and Olive Warden Hard/Furious has both its warned assault cycle and difficulty-only two/three-escort formations. Read docs/CHROME_HAMMER_BOOMERANG_0915.md, docs/DIFFICULTY_ELITE_ACES_0915.md, docs/OLIVE_WARDEN_HARD_ASSAULT_0915.md and docs/OLIVE_WARDEN_ESCORTS_0915.md. Final focused sections 304e and 321-323 pass. Latest full suite has only the established 57 named failures; latest native proofs are 50-frame/zero-error hammer capture, 28/28 Warden assault, 42/42 nine-stage aces and 15/15 Warden escorts. Checklist 149: 114 complete / 9 partial / 26 pending, 35 unfinished. Mike explicitly authorized committing and pushing the completed overnight batch to GitHub.

## Codex update — 2026-09-15: Continue Up rewards

- MODE-07 is complete: deathless miniboss/boss encounters and Hard/Furious authored aces drop a physical Continue Up exactly once.
- Either co-op seat dying blocks the deathless reward. The collected credit extends the shared finite bank, survives campaign save/load, and is shown on the Continue screen.
- Current art is a clearly marked composition of the authored Life Up; MODE-08 still owns the dedicated SpriteCook pickup art.
- Verification: focused 18/18, Chromium 18/18 with zero errors, full suite exact 57-name recorded baseline. Evidence: docs/CONTINUE_UP_REWARDS_0915.md.

## Codex update — 2026-09-15: Sovereign helper blockade

- S4-11 is complete: Hard/Furious Sovereign helpers get 50% more shield capacity, faster attack handling and a timed forward blocking row that follows the player before returning to its generator stations.
- Normal remains unchanged. S4-12 and S4-13 still own the generator-hit enrage and side-stream follow-up.
- Verification: focused 14/14, Chromium 17/17 with zero errors, and the exact established 57-name full-suite baseline. Evidence: docs/SOVEREIGN_HELPER_BLOCKADE_0915.md.

## Codex update — 2026-09-15: Sovereign helper enrage

- S4-12 is complete: real Hard/Furious generator damage sends surviving helpers red to opposite edges with glowing asterisks, inward hull aim, and staggered six-round streams separated by recurring dodge gaps.
- The dedicated phase lasts 5.6s on Hard and 6.8s on Furious; unrelated boss orb/final-gun pressure pauses so the intended route remains visible. Normal is unchanged, and S4-13 still owns the later spider-walk tracking response.
- Verification: focused 12/12, Chromium 19/19 with zero errors, repeat full suite exact 57-name baseline. Evidence: docs/SOVEREIGN_HELPER_ENRAGE_0915.md.

## Codex update — 2026-09-15: Sovereign helper spider walk

- S4-13 is complete: generator damage during the red side phase makes both helpers walk upward and back within explicit 58px Hard / 72px Furious limits, while preserving the edge route, separated streams, and pause windows.
- Different nodes are recognized, repeated damage cannot pin the motion at its start, and a new response can begin after the pair returns. Normal is unchanged.
- Verification: focused 9/9, Chromium 13/13 with zero errors, full suite no new failure names. Evidence: docs/SOVEREIGN_HELPER_SPIDER_WALK_0915.md.

## Codex update — 2026-09-15: Sovereign chain lightning

- S4-14 is complete: Hard doubles and widens both chain-lightning side volleys for nine total bolts; Furious accelerates and widens the cycle and adds three distinct shootable balls from alternating authored racks. Normal preserves its original 5-bolt/1-ball pattern.
- Verification: focused 10/10, Chromium 13/13 with zero errors, full suite exact 57-name baseline. Evidence: docs/SOVEREIGN_CHAIN_LIGHTNING_0915.md.

## Codex update — 2026-09-15: Sovereign giant lightning strike

- S4-15 is complete: Furious Sovereign follows chain lightning with an exact five-second yellow/red warning, darkened authored core charge, red release flash, and seven-column central lightning field. Both 17% camera-edge lanes remain safe and helper/final-gun fire pauses for readability.
- Normal/Hard routing is unchanged. Focused 13/13, Chromium 15/15 with zero errors, full suite exact 57-name baseline. Evidence: docs/SOVEREIGN_GIANT_LIGHTNING_0915.md. Tally: 120 complete / 9 partial / 20 pending.

## Codex update — 2026-09-15: Hard Razorback duo

- S1-05 is complete: Hard Stage 1 fields two full Razorbacks at once with independent destructible components, offset attack books, owned ordnance/locks, camera-safe movement and a combined gauge that requires both kills.
- Normal and Furious remain single for their distinct designs. Focused 14/14, Chromium 17/17 with zero errors, full suite exact 57-name baseline. Evidence: docs/RAZORBACK_DUO_0915.md. Tally: 121 complete / 9 partial / 19 pending; S1-06 is the next ready encounter.

## Codex update — 2026-09-15: Furious Razorback hyper tank

- S1-06 is complete: Furious Stage 1 fields one exact 150%-scale crimson Razorback with matching hardpoints/collision, faster movement/turn/attack clocks and expanded sonic, resonance-nova and Razor Rack pressure.
- Normal remains the original single tank and Hard remains the independent two-tank fight. Focused 14/14, Chromium 17/17 with zero errors, full suite exact 57-name baseline. Evidence: docs/RAZORBACK_FURIOUS_0915.md. Tally: 122 complete / 9 partial / 18 pending; S2-08 is the next unfinished queue item.

## Codex update — 2026-09-15: Sovereign shared ram warning

- ENG-02 advances: the live unpowered Sovereign ram now owns the shared green/yellow/red field and matching overhead alert, commits after 0.40 seconds and releases at one second without changing its dive/flyover/return.
- The shared warning renderer accepts an encounter alert anchor; Stage 4 uses it below the dual gauges. Focused 8/8 and Chromium 14/14 with zero errors; the full suite has 56 established names and no new failures. Evidence: docs/SOVEREIGN_SHARED_RAM_WARNING_0915.md. The tally remains 122 complete / 9 partial / 18 pending.

## Codex update — 2026-09-15: Razorback shared ram warning

- ENG-02 advances: every live Razorback body ram now owns the shared green/yellow/red field and matching overhead alert. Tracking ends when yellow begins, so late dodges cannot move the committed lane.
- Normal, both Hard actors and Furious retain their existing movement envelopes. Focused 9/9, Chromium 15/15 with zero errors, full suite exact 57-name baseline. Evidence: docs/RAZORBACK_SHARED_RAM_WARNING_0915.md. Tally remains 122 complete / 9 partial / 18 pending.

## Codex update — 2026-09-15: Chrome Hammer shared leap warning

- ENG-02 advances: the Chrome Hammer leap/slam now owns the shared green/yellow/red path field and matching overhead alert while preserving the original committed landing reticle. Late player movement cannot steer the attack.
- The completed one-hand boomerang timing and behavior are unchanged. Focused 7/7, Chromium 16/16 with zero errors, full suite 56-name subset of the 57-name baseline and no new failure names. Evidence: docs/HAMMER_SHARED_LEAP_WARNING_0915.md. Tally remains 122 complete / 9 partial / 18 pending.

## Codex update — 2026-09-15: Toxic Portal Warden rail warning

- ENG-02 advances: the Stage-7 Toxic Portal Warden rail fan now commits its aim and safe-side gap at charge start. Five shared green/yellow/red fields show every released spear lane; one matching overhead alert renders in front of the giant hull.
- Focused 7/7 and corrected Chromium 15/15 pass with zero errors; the confirmation suite has the exact 57-name baseline. Evidence: docs/STAGE7_WARDEN_SHARED_RAIL_WARNING_0915.md. Tally remains 122 complete / 9 partial / 18 pending.

## Codex update — 2026-09-15: Toxic Portal Warden minefield warning

- ENG-02 advances: the Stage-7 Toxic Portal Warden now commits its safe minefield column when the charge begins. Six shared green/yellow/red fields preview every mined column while leaving the seventh lane open; one matching alert renders in front of the giant hull.
- Moving after the warning begins cannot relocate the gap, and all six mine anchors match their previews. Focused 7/7 and Chromium 16/16 pass with zero errors; the confirmation suite has the exact 57-name baseline. Evidence: docs/STAGE7_WARDEN_SHARED_MINE_WARNING_0915.md. Tally remains 122 complete / 9 partial / 18 pending.

## Codex update — 2026-09-15: Toxic Portal Warden cannon-burst warning

- ENG-02 advances: the Stage-7 Toxic Portal Warden now commits the aim for its ten-round toxic cannon burst when its 0.48-second charge begins. Five shared green/yellow/red fields preview the five lanes used twice by the alternating physical cannons; one matching alert renders in front of the hull.
- The opening and post-stun direct burst entries now arm the same warning. The original ten-round cadence and shell behavior are unchanged. Focused 7/7 and Chromium 16/16 pass with zero errors; the complete suite has the exact 57-name baseline. Evidence: docs/STAGE7_WARDEN_SHARED_BURST_WARNING_0915.md. Tally remains 122 complete / 9 partial / 18 pending.

## Codex update — 2026-09-15: Stage-8 Vile Annihilation warning

- ENG-02 advances: Furious Death now previews its committed Annihilation cross through four shared green/yellow/red fields converging from the exact release sources onto the retained square target. One overhead alert renders in front of the authored final form.
- Late movement cannot move the cross, and the first eight rounds follow the four previewed paths. Focused 7/7 and corrected Chromium 16/16 pass with zero errors; the complete suite has a 56-name subset of the established 57-name baseline. Evidence: docs/STAGE8_VILE_SHARED_ANNIHILATION_WARNING_0915.md. Tally remains 122 complete / 9 partial / 18 pending.

## Codex update — 2026-09-15: Stage-9 Horizon/Sentinel volley warnings

- ENG-02 advances: Event Horizon and both Warp Sentinels now warn for 0.62 seconds before their eight-lane radial or committed five-lane aimed volleys. Focused 9/9, Chromium 14/14 zero errors, full suite exact 57-name baseline. Evidence: docs/STAGE9_HORIZON_SHARED_VOLLEY_WARNING_0915.md.

## Codex update — 2026-09-15: dedicated Life Up and Continue Up art

- MODE-08 is complete: SpriteCook produced a matched pair of rugged gunmetal pickup plates, with red/orange `1UP` and blue/cyan `C` faces baked into separate transparent assets. The live renderer draws each at a proportional 48–50 px height and retains the shipped Life Up only as a cold-load fallback.
- Focused 7/7 and native Chromium decode/render checks pass with zero errors. The full suite has the exact established 57 failure names. Evidence: docs/MODE_UP_ART_0915.md. Tally: 123 complete / 9 partial / 17 pending.

## Codex update — 2026-09-15: Super, Ultra and Uber missile-tier art

- MSL-08 is complete: SpriteCook produced three separate S/U/X upgrade badges and three matching armored tier boxes, including the distinct Super Missile Box. Six dedicated runtime keys preserve aspect and rising tier scale without changing quantity-box art.
- Focused 15/15 and native Chromium six-asset decode/render checks pass with zero errors. The full suite retains the exact 57-name baseline. Evidence: docs/MISSILE_TIER_ART_0915.md. Tally: 124 complete / 9 partial / 16 pending; MSL-06/MSL-07 can now be wired in ordinary play.

## Codex update — 2026-09-15: ordinary-play missile-tier boxes

- MSL-06 and MSL-07 are complete: authored waves offer Super from wave two, then Ultra and Uber only after their required survived wave. Offers retry if missed, suppress duplicates and bind to the correct co-op seat; collection reuses the existing grant/cap path and death still resets to Standard.
- Focused 12/12 and native Chromium progression proof pass with zero errors. The full suite retains the exact 57-name baseline. Evidence: docs/MISSILE_UPGRADE_SPAWNS_0915.md. Tally: 126 complete / 7 partial / 16 pending.

## Codex update — 2026-09-15: winged Life Up

- Life Up now uses a cache-safe 1520x882 transparent edit with broad symmetrical gunmetal/red jet wings and orange vents. The central `1UP` badge and Continue Up remain unchanged. Focused 7/7 and native Chromium gameplay-scale proof pass with zero errors. Evidence: docs/LIFE_UP_WINGS_0915.md. Tally remains 126 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-9 Tidal Cascade row warnings

- ENG-02 advances: all four Tidal Sovereign cascade rows now commit their two-column opening before a 0.62-second shared green/yellow/red warning. Six fields match the six released columns exactly; the opening moves one column only after release and cannot chase late movement.
- Fields render behind the authored Sovereign and the matching alert renders above it. Focused 9/9, Chromium 19/19 with zero errors, full suite exact 57-name baseline after rebasing the incoming GitHub batches. Evidence: docs/STAGE9_TIDAL_CASCADE_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Thunderhead row warnings

- ENG-02 advances: all four live Doomsday Carrier Mk II Thunderhead rows now own a 0.66-second shared green/yellow/red warning. Six fields match the twelve released projectiles while two adjacent columns remain open; the opening moves one column only after release.
- Fields render behind the giant carrier and its storm nodes; the matching alert remains visible above them and below the boss gauge. Focused 12/12, Chromium 19/19 with zero errors, full suite 4,359 passes with the established 56-name baseline after rebasing onto `02f38a6b`; that incoming build removed the intermittent Stage-1 sand-tank failure and Thunderhead added no new names. Evidence: docs/STAGE6_THUNDERHEAD_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: active Archmage boomerang repair

- The current Chrome Hammer Archmage again shows the committed green/yellow/red lane and floor reticle during its authored one-hand twirl. The alert no longer overlaps the CHAINGUN module label.
- The detached authored hammer descends vertically, turns below the screen, returns at the capped medium magnetic speed and catches in the raised hand. One solid weapon plus three faint motion echoes replaces the accidental row of opaque hammer clones.
- Focused 12/12 mechanics and 6/6 active-render checks; Chromium 19/19 with zero errors; full suite 4,364 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture. Evidence: docs/ARCHMAGE_BOOMERANG_VISUAL_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-7 DUAL SCOOP DREDGER minefield warning

- ENG-02 advances: the live Stage-7 miniboss now commits one of six columns as safe, previews the five dangerous mine trajectories through a 0.86-second shared green/yellow/red warning, and releases the original five slow mines only after red. The old attack required a nonexistent third Dredger phase; it now runs every fourth attack in the real damaged phase.
- The opening cannot chase late player movement. Fields remain below the authored hull and the matching alert remains above it. Focused 10/10, Chromium 16/16 with zero errors, and full suite 4,375 passes with the exact established 56-name failure baseline. Evidence: docs/STAGE7_DREDGER_MINE_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-8 BLACK COCOON crescent-wall warning

- ENG-02 advances: the opening Stage-8 form now commits its original wide center corridor and previews all eleven dangerous crescent columns through a 0.72-second shared green/yellow/red warning. Later boss-clock changes and player movement cannot shift the promised opening.
- The original eleven purple crescents, speed, muzzle and 1.35-second cadence remain intact. Focused 10/10, Chromium 16/16 with zero errors, and full suite 4,384 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture. Evidence: docs/STAGE8_VILE_CRESCENT_WALL_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-8 Vile aimed-fan warnings

- ENG-02 advances: RAVENOUS ASCENDANT commits its five needle paths before a 0.62-second shared green/yellow/red warning, and FURIOUS DEATH commits its seven gunship paths before a 0.58-second warning. Late player movement cannot redirect either fan.
- The original projectiles, speeds, alternating physical hardpoints, muzzles and total cooldowns remain intact. The second form's even-step homing pair keeps the Retina rule and now begins its lock with the warned fan's release. Focused 10/10, Chromium 23/23 with zero errors, and full suite 4,395 passes with the exact established 56 failures. Evidence: docs/STAGE8_VILE_AIMED_FAN_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-8 ABYSSAL LEVIATHAN solar-wheel warning

- ENG-02 advances: the third Vile form now commits its nine original solar-wheel paths before a 0.62-second shared green/yellow/red warning. Late player movement cannot rotate the promised lanes.
- The 0.19-radian wheel step, equal spacing, authored solar rounds, speed 2.45, center hardpoint, muzzle and 0.95-second total cadence remain intact. Focused 8/8, Chromium 16/16 with zero errors, and full suite 4,402 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture. Evidence: docs/STAGE8_VILE_SOLAR_WHEEL_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-8 FURIOUS DEATH straight-missile warning

- ENG-02 advances: the final Vile form commits its four original vertical missile columns before a 0.58-second shared green/yellow/red warning. Player movement cannot shift the promised lanes.
- The missile budget, four hull offsets, armored-gunship muzzles and 0.78-second cadence remain intact. Missiles stay shootable and straight with no Retina/homing grant after Stage 1. Focused 9/9, Chromium 16/16 with zero errors, and full suite 4,412 passes with the exact established 56 failures. Evidence: docs/STAGE8_VILE_MISSILE_SALVO_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier twin-cyclone warning

- ENG-02 advances: the Doomsday Carrier Mk II now commits all six paths from its two rotary batteries before a 0.62-second shared green/yellow/red warning. The warning follows the physical hardpoints while the aim angles remain locked against late movement.
- The mirrored three-lane geometry, authored `s6cyclone` rounds, base speed 4.1, muzzle reels and 1.35/1.12-second phase cadences remain intact. Focused 10/10 and Chromium 16/16 pass with zero errors. The full suite reaches 4,421 passes and the established 56 failures plus the intermittent Stage-1 sand-tank fixture, with no new name. Evidence: docs/STAGE6_CARRIER_CYCLONE_FAN_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier storm-node warning

- ENG-02 advances: both shield-down phases now commit the alternating storm-node pair and its six- or ten-lane fan before a 0.62-second shared green/yellow/red warning. The fields follow each live node while aim and pair parity remain locked against late movement.
- Destroying a warned node disarms only its lanes. Phase transitions cancel stale Carrier fan warnings, and the original offsets, speeds, total cadences and central prism-lance beat remain intact. Focused 11/11 and Chromium 16/16 pass with zero errors. The full suite reaches 4,432 passes and the established 56 failures plus the intermittent Stage-1 sand-tank fixture, with no new name. Evidence: docs/STAGE6_CARRIER_NODE_FAN_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier prism-crossfire warning

- ENG-02 advances: Phase 5 now commits the four authored upper-barrel paths before a 0.62-second shared green/yellow/red warning. The origins follow the moving hull while the alternating outward/inward angles remain locked.
- The original `s6prism` rounds, speed 4.3, muzzle reels, cannon sound and 1.25-second total cadence remain intact. Phase transitions cancel stale crossfire warnings. Focused 12/12 and Chromium 16/16 pass with zero errors. The full suite reaches 4,443 passes with the established 56 failures plus the previously documented intermittent Stage-1 sand-tank and road-tank fixtures; no new name. Evidence: docs/STAGE6_CARRIER_PRISM_CROSSFIRE_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier gravity-mine warning

- ENG-02 advances: Phase 5 now commits the paired gravity-mine paths before a 0.72-second shared green/yellow/red warning. The origins follow the moving left and right mounts while the two crossing angles remain locked.
- The original `s6gravity` art, base speed 1.35, acceleration 0.16, maximum speed 2.15, scale 1.05, muzzles, sound route and 1.72-second total cadence remain intact. Phase transitions cancel a pending mine warning. Focused 11/11 and Chromium 16/16 pass with zero errors. The full suite reaches 4,455 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture; no new name. Evidence: docs/STAGE6_CARRIER_GRAVITY_MINE_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier Last Run slide repair

- The Carrier's sixth-phase sine traverse now runs before warning, cannon/beam and cooldown returns, so the complete authored hull and its live effects move on every gameplay frame instead of stepping only on attack beats.
- The original 0.85 motion rate, bounded amplitude and attack cadence remain intact; earlier phases are unchanged. Focused 7/7 and Chromium 12/12 pass with zero errors. The full suite reaches 4,463 passes with the exact established 56-name baseline. Evidence: docs/STAGE6_CARRIER_LAST_RUN_SLIDE_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier omega-bomb warning

- ENG-02 advances: both Last Run omega variants now commit the center corridor before a 0.66-second shared green/yellow/red warning. The origin follows the continuously sliding center cannon while the downward angle stays locked.
- The original base speeds 1.1/1.25, acceleration 1.05, maximum speed 5.2, scale 1.15, muzzle, sound route and 1.45/1.20-second total cadences remain intact. Phase transitions cancel a pending omega warning. Focused 11/11 and Chromium 16/16 pass with zero errors. The full suite reaches 4,473 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture; no new name. Evidence: docs/STAGE6_CARRIER_OMEGA_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier mirrored cluster-fan warning

- ENG-02 advances: the Last Run cluster fan now commits its six original mirrored paths before a 0.62-second shared green/yellow/red warning. Origins follow the continuously sliding side mounts while the angles stay locked and the middle escape wedge remains open.
- The three paths per side, authored `s6cluster` bomblets, speed 3.35, twin muzzles, single release cue and 1.18-second total cadence remain intact. Phase transitions cancel a pending cluster warning. Focused 11/11 and Chromium 16/16 pass with zero errors. The full suite reaches 4,484 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture; no new name. Evidence: docs/STAGE6_CARRIER_CLUSTER_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-6 Doomsday Carrier chrome-flak warning

- ENG-02 advances: the Last Run chrome-flak pair now commits both shell paths before a 0.62-second shared green/yellow/red warning. Origins follow the continuously sliding lower-inner hardpoints while the angles stay locked.
- The previously unreachable outer `-18°/+18°` pair now alternates with the inner `+10°/-10°` pair. Authored shells and burst reel, speed 3.75, 0.64-second fuse, five fragments per shell, twin muzzles and 1.08-second total cadence remain intact. Focused 13/13 and Chromium 19/19 pass with zero errors. The full suite reaches 4,497 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture; no new name. Evidence: docs/STAGE6_CARRIER_FLAK_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-7 Toxic Portal Warden cripple-rail warning

- ENG-02 advances: the crippled Warden now commits a complete rail group before a 0.58-second shared green/yellow/red warning. Four fields preview its three alternating straight singles and paired offset finisher. The fields follow the crawling hardpoints while their angles stay locked against late movement.
- The original three `5.25`-speed singles, dual `4.65`-speed finisher, `-0.07/+0.07` offsets, authored rail spears, muzzles and sound remain intact. A new group samples the player only after the previous group completes, and phase transitions cancel pending warnings. Focused 13/13 and Chromium 18/18 pass with zero errors. The full suite reaches 4,510 passes with the established 56 failures plus the intermittent Stage-1 sand-tank fixture; no new name. Evidence: docs/STAGE7_WARDEN_CRIPPLE_RAIL_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-5 Archmage spiked-ball warning

- ENG-02 advances: the Chrome Hammer Archmage now commits its spiked-ball launch direction and exact first wall impact before a 1.25-second shared green/yellow/red corridor. Player and camera movement cannot shift the promise after the curl begins.
- The first reflection uses the committed bounds, then the original dynamic reflections resume. Authored ball art, `150/165` base velocity, 15-second duration, missile knockback and weapon-triggered rage remain intact. Focused 10/10 and Chromium 18/18 pass with zero errors. The full suite reaches 4,521 passes with the exact established 56-name baseline and no new name. Evidence: docs/ARCHMAGE_SPIKED_BALL_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-5 Archmage core recovery

- Easy/Normal no longer freezes after the Archmage chaingun breaks. A 2.15-second authored blue core conversion returns the boss to its anchor and releases into the dual-Uzi/mega-wave loop.
- Both obsolete module targets retire at the final break, so invisible hammer hits cannot resurrect the destroyed chaingun phase. The fused mega-wave now shows the shared green/yellow/red corridor for its exact damage width before release.
- Focused section 358 passes 10/10; Chromium passes 22/22 with zero errors; full suite reaches 4,530 passes and the established 56 failures plus the intermittent Stage-1 sand-tank fixture. Evidence: docs/ARCHMAGE_CORE_RECOVERY_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-16: Stage-2 Inferno Reaver role and shared shotgun warning

- The shieldless Stage-2 miniboss again runs its intended Inferno Reaver controller. The stable `magmaward` slot no longer dispatches into the retired Magma Ward shield/fire controller; its five-station laser pass and rolling-flamethrower finale now advance and render on the live identity. The Furnace Tyrant retains its real boss shield.
- ENG-02 advances: the nine-round shotgun commits seven center lanes plus two wing escorts before a 0.6888-second shared green/yellow/red warning. Late movement cannot redirect the fan; warning origins stay on the live hardpoints and release uses the authored Inferno shotgun family.
- Focused section 359 passes 16/16; Chromium passes 18/18 with zero errors; full suite reaches 4,547 passes / 56 failures, repairing the former Magma Ward opening-fan baseline name. The remaining failures are the reduced 55-name established set plus the intermittent Stage-1 sand-tank fixture. Evidence: docs/STAGE2_REAVER_SHARED_WARNING_0916.md. Tally remains 128 complete / 7 partial / 16 pending.

## Codex update — 2026-09-18: Furious Razorback and global boss-element Forge repair

- The Furious Razorback is now the current authored tank at 150% scale with a reproducible green-panel-to-neon-red palette set; gray armor, black outlines, lights and ordnance remain authored. Furious sonic pressure draws five directional or eleven nova decibel lobes with collision-safe openings.
- Boss kills award one deterministic stage element rather than a random weapon pair. The element applies to all nine forgeable weapons, survives save/load and is available in Stage 5 space. Each stage retains two upgrades and two re-specs; every crafted form persists when another form or bare weapon is equipped.
- Loadout selection now exposes Ice Breath, Fire Orb, Ice Orb, Thermoshock and forged elemental forms as their requirements are earned. A new Forge/loadout plate shows Fury Points and embeds RE-SPEC; a separate four-row Weapon Found plate announces actual weapon systems.
- Fire Orb draws a dedicated Magma Orb plate without additive washout. Combat audio validation covers ordinary projectile families, boss-specific families, Razorback charge/release and Magma Orb launch through real-sample routes.
- Verification: syntax pass; full suite 4,921 pass / exact incoming 57-name failure baseline; real Chromium 9/9 with zero page or console errors. Evidence: docs/WEAPON_FORGE_REPAIR_0918.md and docs/qa/weapon_forge_repair_0918.json. Checklist: 156 entries, 133 complete / 7 partial / 16 pending.

## Codex update — 2026-09-20: Furnace, gate, Archmage and late-stage openings

- The Furnace core beam has new pixel art, and its shield gauge preserves the source aspect ratios of both frame and fill. Stage-5 gates now move with their background rather than on a separate scroll clock.
- The Chrome Hammer Archmage now has missile-triggered arms-up/kneel/magnetic-recovery stun poses and a heavier leap. Stage 6 opens with two black fighters, separate Retina locks and a shootable slow-motion missile check. The Stage-7 Warden hyper rotation gains a toxic chaingun burst and a leg-strike leap. Do not touch the Stage-8 boss; Mike reserved that encounter for a separate design session.
- Focused Chromium checks passed for all new flows, including successful Stage-6 Retina interception and the life-loss path. The full legacy suite reached its summary at 75 then 76 failures; the final 76 matches the recorded baseline exactly, with no new failing assertion names. The one changing name is the existing intermittent Stage-1 sand-tank spawn fixture. Current evidence and remaining scope: docs/OVERNIGHT_PASS_0920.md. The generated checklist and work order are rebuilt from `docs/REQUEST_CHECKLIST_0914.json`; the old rendered tally was stale.

## Codex update — 2026-09-20: combat audio, decals and stage exit

- A 20-cue ColeForge offline sound bank now gives the nine forged elements, Thermoshock, fire hazards, shield destruction, three boss attacks and three enemy projectile families new short sounds with retrigger gates. The project's ElevenLabs script remains available, but its ignored credentials file is absent; ElevenLabs finishing and listening review of the full boss/miniboss roster remain open.
- All nine primary weapon slots now have authored impact decals, while uninfused fire, ice and lightning hits use the existing eight-frame elemental burst art. Stage-2 and Stage-4 boss tracks have louder copies; the originals remain. The pilot can steer through boss death and the fly-off hover, then loses control as the climb starts.
- `node --check` passed; the full suite ended with the exact 76-name failing baseline and no new name. The Chromium probe verified playback, visible decals, music volume and exit controls with no page or console errors. Evidence: docs/AUDIO_DECALS_EXIT_0920.md and `_shots/qa_0920_audio/`. Tally: 186 entries, 148 complete / 10 partial / 28 pending.

## Codex update — 2026-09-20: Stage-5 Chaos Harrier miniboss

- Kept Mike's approved teleport rift and three-warps-then-stationary fight. Corrected horizontally shifted source frames so plasma, wing emitters, flashes and the nose beam remain anchored through their animation. Each warp now leads to a distinct weapon beat: plasma glide, paired straight-lane bay missiles, then twin lasers. Lower spawn/warp anchors keep the full hull below the MINI BOSS gauge.
- Chromium captured the final encounter in `_shots/chaos_harrier_final_full_0920/capture.gif`; the focused live probe traversed every attack with no page or console errors. Syntax passes. The full suite remains at 76 failures; a rerun matched the baseline names exactly, while other runs exchanged two unrelated intermittent fixtures. Details: docs/CHAOS_HARRIER_REPAIR_0920.md. Checklist: 187 entries, 149 complete / 10 partial / 28 pending. No commit or push.

## Codex update — 2026-09-20: Stage-7 Warden machine round

- The hyper chaingun no longer shrinks the Warden's large pressure shell. A dedicated static machine round comes from the authored small-slug cell of the existing Stage-7 toxic projectile atlas, preserving its gold casing and bright green tip. Only the 20-round chain attack uses it; the other Warden projectile families are unchanged.
- Syntax passes; real Chromium shows the rounds firing from both cannon mouths with no page or console errors. The complete suite again exits nonzero with the exact recorded 76 failing names and no additions. Evidence: docs/STAGE7_MACHINE_ROUND_0920.md and `_shots/stage7_chain_0920/`. Checklist: 188 entries, 150 complete / 10 partial / 28 pending. Stage-7 natural-play balance remains open; do not touch Mike's reserved Stage-8 boss. No commit or push.

## Codex update — 2026-09-20: Furious ice beams and Forge reward audit

- The Stage-3 Furious Rime Wall now releases a dark-blue, pale-core giant beam from the cannon selected by its Simon-Says FOV warning. The warning and collision width are both 62 world pixels. The Furious Frost Cruiser miniboss uses the same authored-source palette variant for its nose sweep; other difficulties retain their original art. See docs/FROST_FURIOUS_BEAM_0920.md and `_shots/frost_furious_beams_0920/` for native-browser frames.
- A real Chromium Stage-1 boss reward fixture confirmed one Kinetic element, two Forge combines, third-combine denial, re-spec and Loadout form restoration, audible UI cue routes, then Stage-2 death persistence. It begins at the boss's last hit; full later-stage natural play and campaign save/load remain. See docs/FORGE_REWARD_AUDIT_0920.md.
- `node --check` passed and the browser probe recorded no page or console errors. The full suite exited nonzero on both runs: the first had 77 failures including the intermittent Stage-1 three-drone lance fixture, the repeat matched the recorded 76-name baseline exactly. Checklist: 188 entries, 151 complete / 11 partial / 26 pending. Stage-3 Furious hull palette and Hard-pattern parity remain. No commit or push.

## Codex update — 2026-09-20: Stage-clear separation

- Moved the Fury Point conversion below the score separator rail and kept it above the sign-off. The existing achievement queue holds its notices throughout Stage Clear so they do not cover the password or Continue prompt, then resumes after the debrief.
- Chromium rendered the authored debrief at wide, square and portrait browser sizes. All showed separate conversion, sign-off, Continue and footer areas with no page or console errors. Syntax passes. The complete suite still exits nonzero at 75 failures, a subset of the recorded 76-name baseline; the absent name is the intermittent Stage-1 sand-tank fixture. Evidence: docs/STAGECLEAR_SEPARATION_0920.md. Checklist: 188 entries, 152 complete / 11 partial / 25 pending. No commit or push.

## Codex update — 2026-09-20: Loadout catalog paging

- The arsenal now displays one weapon's six larger authored form badges per page. D-pad left/right changes weapon and up/down traverses Base and both element pages. The selected row and badge glow, and a separate strip identifies the form and its owned, Armory cost, recipe or boss-locked state before equipping.
- The focused Chromium probe navigated both pages, checked a locked weapon and equipped an owned form with no page or console errors. Screenshots were visually reviewed. Syntax and whitespace checks pass. The full suite exits nonzero with 75 failing assertions, all within the recorded 76-name baseline; the intermittent Stage-1 sand-tank fixture was absent. Evidence: docs/LOADOUT_CATALOG_0920.md and `_shots/loadout_pages_0920/`. Checklist: 188 entries, 154 complete / 11 partial / 23 pending. No commit or push.

## Codex update — 2026-09-20: Pilot Select checklist re-audit

- Fresh Chromium frames confirmed Yuri's identity and biography type before the first stat, each stat fills separately, and the completed card shows the special icon. The GOOD LUCK slide retains only pilot and ship. No page or console errors. The 0919 implementation already prewarms all nine art families and was previously rendered across the roster; only two outdated checklist statuses were corrected, with no game-code changes. Evidence: docs/PILOT_REVEAL_REAUDIT_0920.md and `_shots/pilot_reveal_0920/`. Checklist: 188 entries, 156 complete / 11 partial / 21 pending. No commit or push.

## Codex update — 2026-09-20: stats and tread checklist reconciliation

- The Stats screen's BULLETS FIRED value and fill already use the shot count, with WEAPON ACCURACY separately using hits/shots; the 0919 Chromium check measured every label/value inside its authored bay at portrait, standard and ultrawide sizes. The Razorback already uses the recorded tread loop and its pair controller keeps audio owned by the moving tank. Both 0919 proofs were present, so two stale pending statuses were marked complete without further game-code changes. Evidence: docs/STATS_FIT_0919.md and docs/RAZORBACK_TREAD_RECORDING_0919.md. Checklist: 188 entries, 158 complete / 11 partial / 19 pending. No commit or push.

## Codex update — 2026-09-20: save audit and checklist corrections

- An isolated Chromium campaign-slot probe saved Kinetic and Fire discoveries, selected/saved forms, the Ice Breath variant and Forge state, then reloaded and applied that slot. It also exercised the Stage-2 to Stage-3 autosave and reload; Stage-3 start reapplied Kinetic. No browser errors. The later boss rewards and full natural-play Forge path remain open. Evidence: docs/FORGE_REWARD_AUDIT_0920.md and `_shots/forge_campaign_save_0920/`.
- Existing 0919 proofs closed stale entries for respawn safety and the Hard Razorback duo, while the 0916 synchronized Stage-4 giant-strike escape arrows and achievement menu/unlock card also had stale pending flags. The unlock card uses Mike's later-approved lower-left placement. Evidence: docs/RESPAWN_SAFETY_0919.md, docs/RAZORBACK_HANDOFF_0919.md, docs/ESCAPE_ARROWS_0916.md and docs/AWARDS_0916.md. No new gameplay change for these status corrections.

## Codex update — 2026-09-20: incoming lock warning and working-file recovery

- The authored Retina plate now draws gray above the in-game EQUIPPED panel and flashes red during an incoming lock. Warning beeps tighten with missile distance, and the next beep advances immediately when a missile closes in. Chromium inspected idle and active frames and measured 0.444-second and 0.100-second gaps at 400px and 90px; no page/console errors. Evidence: docs/LOCK_WARNING_0920.md and `_shots/lock_hud_0920/`.
- A large-file patch operation unexpectedly damaged a middle span of `assets/game.js`. A copy of the damaged bytes is in `_shots/recovery_0920/game_corrupted.js`. The committed span was restored, the smaller working changes reapplied, and the Warden escort, Stage-6 chase, fly-off input and sound mappings were restored at their intended sites. `node --check` passes; the full suite exits 1 at 75 failures, all a subset of the earlier 76-failure baseline. The Stage-5 Chaos Harrier Chromium attack-cycle probe passes again. Review `docs/LOCK_WARNING_0920.md` before another edit to this giant file; use exact byte-level replacements, not `apply_patch` on `assets/game.js`.
- Checklist: 188 total, 163 complete / 11 partial / 14 pending. No commit or push.

## Codex update — 2026-09-20: Chaos Harrier field isolation and recovery verification

- Stage-5 scheduled and adaptive waves now stay queued from the Chaos Harrier warning through its defeat, then resume. Existing hazards remain physical and pickups remain available. Chromium verified the due wave did not dispatch during the fight, resumed afterward, and the full teleport/weapon cycle still reached every state without browser errors. Evidence: docs/CHAOS_HARRIER_REPAIR_0920.md and `_shots/recovery_0920/harrier_waves.log`.
- The working-file recovery was extended to restore the Archmage's authored missile-stun poses and heavy leap, background-anchored Stage-5 gates, and weapon impact decals. Focused Chromium probes passed for those systems, both Stage-6 opener outcomes, and audio/decals/stage exit. The full `test_fl.js` suite reached its summary and exited 1 with the exact recorded 76 failing names and no new failures. `node --check` and `git diff --check` passed. Details: docs/LOCK_WARNING_0920.md. No commit or push.
- The Harrier's stationary sequence now truly plays nose beam, paired wing lasers, nose beam; the old post-increment produced side/beam/beam. New Stage-5 asteroid/comet spawns pause during the warning/fight while existing rocks remain physical. Supply crates use side lanes clear of the hull. The 32-frame real-game recording is `_shots/chaos_harrier_repaired_0920/capture.gif`. Full-cycle and field-flow Chromium probes passed with no browser errors, and the final complete suite still exits 1 with the exact 76-name known baseline. No commit or push.
- Stage-7 through Stage-9 real boss defeat routes were also probed: one Toxic, Prism, and Water element respectively. Stage 7 begins a staged defeat and keeps the boss object alive on its first frame. ENG-23 remains partial until natural-play Forge combinations are checked. Evidence: docs/FORGE_REWARD_AUDIT_0920.md.

## Codex update — 2026-09-20: Forge form isolation

- A native Chromium pickup probe reproduced a Forge leak: a level-I Kinetic Spread inherited the level-V aura from the previous Machine Gun, and a bare flamethrower kept that aura. `forgeApply()` now records the forged slot, reapplies that slot's exact level, and clears its aura on a bare pickup while preserving an independent field infusion.
- The focused probe passed afterward and exercised all 81 weapon/element pairings. The boss reward/Forge UI/death flow and campaign save/autosave round-trips passed again without browser errors. Evidence: docs/FORGE_REWARD_AUDIT_0920.md and `_shots/recovery_0920/forge_switch_matrix.log`. ENG-23 remains partial for later natural-play combination review. No commit or push.

## Codex update — 2026-09-20: Campaign Stage-1 flight bridge

- After clearing Stage 1 in Campaign, the selected pilot and Cole (or Axel when Cole is selected) now fly a short top-down radio scene over the authored jungle terrain. It uses the existing comm portraits and framed 16-bit dialogue panel. Arcade remains direct, and the older HQ ensemble scenes stay archived. The scene is only the first transition; PRE-11 is partial.
- Chromium verified Yuri and Cole variants plus the real `scLeaveStage` to flight to map unlock route, with no page or console errors. Screenshots and details: docs/CAMPAIGN_BRIDGE_0920.md and `_shots/campaign_bridge_0920/`. `node --check` and whitespace diff check passed. The full suite reached its summary with 76 failing assertion names, exactly matching the recorded baseline; it still exits nonzero. No commit or push.

## Codex update — 2026-09-20: natural Stage-5 miniboss entrance

- A normal Stage-5 progression probe found the Chaos Harrier appearing under nine surviving fleet enemies, shield domes, portal effects and bullets. Its warning now clears ordinary fleet units and hostile rounds so the teleport encounter has a readable arena; physical asteroids/comets and pickups remain. The repeated Chromium run reached the miniboss naturally at 28.57 seconds with zero ordinary enemies and two physical rocks still present. The before/after screenshots and probe are under `_shots/stage5_natural_mini_0920/`; details are in docs/CHAOS_HARRIER_REPAIR_0920.md.
- `node --check` and whitespace diff check passed. The complete assertion suite exits 1 with exactly the same 76 failing assertion names as the baseline. No commit or push.

## Codex update — 2026-09-20: current Yuri in the Campaign opening

- The opening cockpit still used `pose_yuri_0`, an older likeness despite the new Yuri already being used elsewhere. It now loads the approved `yuri_body_0` front-facing figure and never falls back to the retired pose. `cutPose()` redirects Yuri's old cinematic/seated routes to the same current figure; other pilots are unchanged.
- Real Chromium rendered and visually checked Yuri and Cole openings; no page or console errors. Evidence: docs/READABLE_TYPE_YURI_0914.md and `_shots/yuri_campaign_intro_0920/`. Syntax and whitespace checks passed. The full suite exits 1 with the same 76 failing assertion names as the baseline. No commit or push.

## Codex update — 2026-09-20: current cinematic ships, distant escorts and pickup UI

- All cinematic ship views and the opening silhouette now resolve to the current nine-pilot gameplay atlas. The old cutouts are removed from runtime registration; source files remain archived. Chromium rendered the Stage-1 bridge with the current Cole, Axel and Yuri airframes.
- Hard/Furious Olive Warden escorts now receive ordinary and special-weapon hits at their own positions, including when they fly outside the miniboss's central bounding box. A real browser shot from the lower field took 60 HP from the distant left helper.
- Stage passwords lead to difficulty, then pilot, then the chosen Arcade stage. Back from difficulty returns to password. Pickup banners and floating labels use the authored graphical game font, with no plain canvas-font loading flash.
- Chromium probes passed with no page or console errors. Evidence: `docs/LATEST_REPAIRS_0920.md`, `_shots/campaign_bridge_0920/`, `_shots/latest_repairs_0920/`. The full suite retains its established nonzero baseline; see `_shots/test_fl_latest_0920_final.log`. No commit or push.

## Codex update — 2026-09-20: Pandemonium and dialogue portraits

- Stage 3's main boss now plays Mike's `pandemonium.wav` via the encoded `boss3_pandemonium.mp3`. The former boss track is preserved under the `unused2` music key; the Stage 3 miniboss uses the Stage 3 field music.
- Shared dialogue portraits, including Cole's Campaign radio scene, are centered in the panel's left portrait bay with the name and message clear of the frame. Real Chromium screenshots and music-key routing pass without browser errors.
- Full details and baseline comparison: `docs/STAGE3_PANDEMONIUM_PORTRAITS_0920.md`. The suite retains exactly the same 76 known failure names and exits nonzero. No commit or push.

## Codex update — 2026-09-20: right-facing portraits and B/Back

- The shared dialogue renderer now mirrors all nine pilot comm portraits to face the message and enlarges each square to fit its left bay. Cole and Yuri were visually inspected in real Chromium.
- Campaign setup no longer consumes B/Back without acting: hub → mode select, difficulty → hub, pilot → difficulty. Arcade and Co-op setup return from difficulty to mode select and pilot to difficulty. The Campaign map returns from its button bar to the map and then to the hub; slot-picker cancel remains intact.
- Chromium navigation and render proof: `docs/DIALOGUE_BACK_0920.md`, `_shots/dialogue_back_0920/`. The repeat full suite has the same 76 failing names as baseline and exits nonzero. No commit or push.

## 2026-09-22 repair pass

See [REPAIR_0922.md](docs/REPAIR_0922.md) for the latest request checklist, exact repairs, remaining work and verification limits. The old status/test totals above are historical. Current full-suite result: 76 pre-existing failures, identical assertion names to the 0920 cinematic baseline; no new failures. Nothing committed or pushed. ElevenLabs generated two batches but browser export is blocked; do not regenerate them or claim they are installed. IDs are in the repair note.

Large-file tooling warning: apply_patch on assets/game.js truncated unrelated sections again on 0922. Recovery artifacts are under _shots/repair_0922; use backed-up, count-asserted text replacements for this file and run node --check immediately. Do not use whole-file patch rewriting on this multi-megabyte source.

## 2026-09-22: independent Stage 6 wingmen

See docs/STAGE6_WINGMEN_0922.md. Allies now own their movement/targets, use the player hull scale and native damaging shots, avoid incoming projectiles and ground strikes, and withdraw when hurt. Added side bombing runs with fixed landing warnings, rotating descending bombs and difficulty-scaled racks. Corrected south-facing jet orientation. Chromium passes with zero page/console errors; full suite exits 1 with the same 76 failing names as baseline. Nothing committed or pushed.

## 2026-09-22: Cole sonic and Furious helicopter

See docs/OVERLORD_SONIC_0922.md. Cole sonic damage +50% (full 22 to 33). Furious Overlord gets green armour, a warned horizontal/vertical/horizontal pressure combo after rain/reentry, then a six-beep pod windup and three sonic missile volleys while resuming flight. Chromium validates native rain-to-combo progression, interception and roll/somersault survival. Full suite: same 76 known failure names, exit 1; no new failures. No commit/push.


## September 22: Level 4 target sizes and projectile protection
See `docs/STAGE4_TARGETS_0922.md` and `_BUILD_SOURCE/probe_stage4_targets_0922.py`. Warden +25%, escorts +50%, warship helpers 2x with matching collision geometry. Warship rounds resist player weapon interception. Existing work preserved; nothing committed or pushed.


## September 22: faster tally and post-loadout supplies
See `docs/SUPPLIES_TALLY_0922.md` and `_BUILD_SOURCE/probe_supplies_0922.py`. Results finish within 0.8 seconds. Fury Supplies offers 250-FP lives and 750-FP continues, persistent spending, stock guards, Back and optional skip. Shared debrief mouse mapping now uses its actual widescreen width. No commit/push.


## September 22: Cole overhaul, nine portrait packs and Roaming Rebels art
See `docs/PORTRAITS_REBELS_0922.md` and its HTML visual catalog. Current likenesses route through menus/dialogue/legacy aliases; Cole body comes from Mike's supplied PNG, and his ZIP is retained. Generated five-member Rebel roster (leader included) and five south-facing alpha ship masters, registered for art/editor use; existing Stage 6 encounters unchanged. Native Chromium: 236 assets, all pilot aliases, dialogue and Cole intro verified, no browser errors. Full suite exits 1 with the same 75 failure names, no new ones. No commit/push.

## Codex update — 2026-09-22: enemy burn effects

- Generated and integrated eight hull-wrapping burn frames matching the flamethrower/orb heat palette; forged flames retain their source color.
- Native Chromium collision, palettes, animation, expiry and readability verified; zero browser errors. Syntax passed; full suite exit 1, same 75 baseline failure names.
- Source, prompt, implementation and verification: docs/ENEMY_BURN_0922.md. Nothing committed or pushed.

## Codex update — 2026-09-22: Level 4 electrical-core anchoring

- Four shield-generator cores now follow fixed boss-relative offsets; camera/background scrolling no longer moves them independently. Independent chaingun helper patterns preserved.
- Chromium scroll/movement/rearm/hitbox checks passed with no browser errors. Syntax passed; full suite exit 1, 4,905 pass / same 75 baseline failures.
- Details: docs/STAGE4_CORE_ANCHORS_0922.md. Nothing committed or pushed.


## September 26: Stage 5–9 HUD, controller, weapon and combat repairs

See docs/GAMEPLAY_REPAIRS_0926.md for the exact implementation, generated asset prompts and remaining limits. Saved raw pad bindings now survive boot; radar/LOCK join the bottom rail and active specials overlay it; Firewhip is selectable after Fire discovery with one combine credit. Level-1 previews, hammer/cannon retina targets and missile counter context repaired. New Stage 5 turntable/orbital/beam sheets and late-stage projectile frames installed. Full suite: 4,957 pass / zero fail, exit 0; 15 Chromium boss opening checks, 90 preview cases and targeted collision/HUD/controller tests passed. The controller check uses a synthetic pad; full unassisted campaign balance runs remain open. All prior work preserved; nothing committed or pushed.

## September 26: correct the hammer identity and repeated-strike recovery

Mike rejected the double-headed weapon in the first generated strike/whirlwind sheets. Active reels now use the canonical single cylindrical blue head: twelve strike/recovery poses and eight whirlwind poses. Every repeat has a lowered idle hold, then wind-up and jump; orbital recovery returns into view above the HUD. Head damage/Retina targets follow the drawn pose. See docs/HAMMER_CONSISTENCY_0926.md and docs/hammer_consistency_art_0926.json. Real Chromium repeat checks passed on Normal/Hard/Furious, no clipped strike frames or page/console errors, three focused recordings saved. Latest full suite: 4,957 pass, zero fail, exit 0; an earlier run exited 1 on two intermittent jet-dodge assertions (both logs preserved). Game LF/test CRLF retained. No commit or push.

## September 26: whirlwind disarm and second-half arsenal

See docs/HAMMER_OVERDRIVE_0926.md. Whirlwind now crosses the full arena 2/3/4 times on Normal/Hard/Furious with acceleration and reversal warnings. Spaced hits disarm it (4/6/8 normal impacts, missiles count double), throwing the authored hammer loose and giving a five-second double-damage stun with generated static; recoil keeps the boss in view. Below 50%, deterministic warned cannon rakes/cooling, committed columns and chromium beam replace the old cannon loop. Broken-cannon core gets warned directional twin-gun rakes and beam/column rotation. New blue-reactor casting reel and reticles above the HUD. Final full suite 4,957 pass/0 fail, exit 0; native Chromium verifies all difficulties, real bullet disarm and original strike/orbital regressions, no page/console errors. Four focused videos at _shots/hammer_overdrive_0926/review.html. No commit/push.


## September 26: replace akimbo with the charged hammer

See docs/HAMMER_STORM_0926.md and docs/hammer_storm_art_0926.json. Cannon destruction now restores the approved hammer/armor, raises it into a lightning charge, and runs committed slams whose ground Retina markers split into 3/4/5 chromium eruptions. Generated 52 frames across six sheets: charge, catch/throw, overhead twirl, detached hammer, lightning and chromium spikes. Ordinary shots, space shots and Retina missiles can send the flying hammer back; magnetic recall/catch leads into faster behind-head twirl and a randomly mirrored inward spiral. The retaliation is counterable without an endless counter loop. Earlier whirlwind/stun and intact-cannon arsenal retained. No akimbo continuation.

Real Chromium: all three difficulties and all nine counter routes pass, spike warning/damage/safe areas verified, zero clipped pose edges, zero page/console errors. Three real-canvas clips at _shots/hammer_storm_0926/review.html; controlled invulnerable/muted fixtures, asteroid stream suppressed only for preview. Original strike/orbital regression passes. Syntax and whitespace checks pass; game LF/test CRLF preserved. Earlier full suites passed 4,981/0; final runs each exited 1 at 4,980/1 on alternating pre-existing random road-tank/drone-column assertions. Exact names, evidence and logs are in the report; all hammer assertions passed. No commit/push.

## September 26: bottom-row chromium sweep and remove throw warnings

Mike requested removing hammer-throw warnings and replacing staggered short spikes with a sequential bottom row. See docs/HAMMER_BOTTOM_ROW_0926.md and docs/hammer_bottom_row_art_0926.json. Ordinary/retaliation wind-ups retain their art and spin sound but no FOV, Retina, alert or warning clock. Generated 16-frame tall chromium sheet, preserved source alpha; 3/4/5 columns glow and rise in order with alternating sweep direction. Peak shaft is 384 logical pixels (75% of the 512-pixel game height); collision grows/retracts with the visible shaft, leaving safe gaps/residue. Rightmost hazard remains visible over the overlapping LOCK/radar footprint.

Final full suite: 4,997 pass / 0 fail, exit 0 and final banner. Initial run's single stale boomerang-warning requirement was corrected to the requested behavior. Native Chromium Normal/Hard/Furious loops and all nine counter routes pass, zero throw warnings, zero clipped opaque sprite edges, zero page/console errors. Three refreshed clips: _shots/hammer_bottom_row_0926/review.html; earlier storm preview links forward. Game LF and test CRLF retained. No commit/push.


## September 26: randomized eight-spike field with a red escape window

See docs/HAMMER_RANDOM_SPIKES_0926.md. All difficulties now get eight evenly spaced bottom Retina positions, with a newly shuffled committed order per slam (no repeated identical order). Each lane runs green/yellow/red for three seconds, including a full second of red before eruption; its authored red zone covers the complete future shaft with a small margin. Normal/Hard/Furious gaps are .50/.42/.34 seconds. The generated 75%-height spikes, visible damage, safe residue and warning-free throws remain. Existing shared warning art reused; no new generation needed.

Final full suite: 5,012 pass / 0 fail, exit 0 and final banner. Chromium: all difficulties and nine counters pass; actual sidestep avoids damage, staying hits at 1.15 seconds after red, 3,233 damage points all covered by rendered warning pixels, zero page/console errors. Initial escape fixture overlapped the boss body; corrected fixture below the body passes, with both logs retained. Three clips and updated preview at _shots/hammer_random_spikes_0926/review.html. Game LF and test CRLF retained. No commit/push.


## September 26: restore full-size Retinas and cover off-screen map edges

See docs/HAMMER_WORLD_ROW_0926.md. Stage 5 is 680px wide versus the 480px camera. Retinas restored to 96px (five widths per view); row now spans the entire world, including edge-centered spikes. Current world positions: 4, 100, 196, 292, 388, 484, 580, 676. Eight positions TOTAL across the world, not eight shrunken markers in one view. Camera movement cannot relocate or drop the row. Random order, green/yellow/red and full-second red warning, tall generated shafts and warning-free throws remain.

Final full suite: 5,021 pass / 0 fail, exit 0 and final banner; no failing names versus the 5,012/0 baseline. Chromium passes both-edge movement/damage on all difficulties, identical geometry across three camera views, all prior phase/counter/escape tests, zero page/console errors. First camera assertion failed because the fixture omitted the render-loop camera update; corrected fixture passes, logs retained. New scrolling video and screenshots: _shots/hammer_world_row_0926/review.html. Game LF/test CRLF retained. No commit/push.


## September 26: round columns and shared asterisk countdown

See docs/HAMMER_ROUND_ZONES_0926.md. Mike rejected the narrowing red cone: warnings now keep the full 96px Retina diameter with rounded caps, reusing the authored plate through runtime slicing. Shared green/yellow/red impact-imminent asterisks sit at the column crowns below the boss gauge, follow the Retina countdown, and clear at eruption. World-wide row, random order, warning duration, spike animation/collision and hammer counters retained.

Final full suite: 5,033 pass / 0 fail, exit 0 and final banner; no failing names versus 5,021/0. Native Chromium checks constant 96px width, round corners, all 3,233 damaging points covered, actual asterisk colors, both scrolling edges, three difficulties and nine counters. Zero page/console errors. First probe found one lower-boundary pixel outside the round foot; four extra pixels of bottom margin fixed it, verified on rerun. Updated recording/screenshots: _shots/hammer_round_zones_0926/review.html. Game LF/test harness CRLF preserved. No commit/push.


## September 26: framed signs, fast eruptions and committed recovery

See docs/HAMMER_SIGN_RECOVERY_0926.md. Replaced bare asterisks with the existing metal-framed bmfx_badge warning signs. Hard/Furious spike rises are 1.8x/2.8x faster (full height at .211/.136 seconds vs .38 Normal); eruption spacing is .30/.20 seconds vs .50 Normal. Full-second red warnings, round full-width zones, complete world row and authored collapse remain. Five authored recovery poses now lead into an eased return to a fixed world-space upper-arena home, independent of camera scrolling.

Final full suite: 5,048 pass / 0 fail, exit 0 and final banner, versus 5,033/0 baseline. Initial run exited 1 at 5,047/1 on the exact-release sign assertion; comparing the shared absolute Retina timestamp fixes the floating-point boundary. Both logs retained. Chromium verifies three difficulty timings, both-side recovery under scrolling, all prior counter/escape/row checks, zero page/console errors. Three 24-second comparison clips and inspected screenshots: _shots/hammer_sign_recovery_0926/review.html. Game LF/test harness CRLF preserved. No new assets or commit/push.


## September 26: interruptible Chromium empowerment and healing

See docs/HAMMER_CHROMIUM_RECOVERY_0926.md. After cannon destruction, the raised single-headed hammer shakes and pulses while a pixel-stepped Chromium glow climbs the boss. Armor, held hammer and gauge share cyan/silver/green palettes. He restores 25% maximum HP over six seconds, previewed by a pulsing RECOVERY segment. Direct shots, space shots and Retina missiles can break the raised core: the engine explosion gets a scoped Chromium tint, all healing from that charge is revoked, and the boss enters four seconds of double-damage stun. A 2.4-second visible hammer rebuild and armor sweep restore empowerment without retrying the heal. Damage flashes remain visible over empowered palettes.

Final full suite: 5,083 pass / 0 fail, exit 0 and final banner, versus 5,048/0 baseline. All full-suite runs this pass passed. Native Chromium verifies all nine interruption routes, three complete heals, actual pulse/segment/hit-flash pixels, target jitter and stun/rebuild transitions. Existing world-row, spike, counter and eased-return regressions pass; zero page/console errors. Two inspected 20-second focused recordings: _shots/hammer_chromium_recovery_0926/review.html. The interruption clip uses native Retina damage in a controlled invulnerable fixture; it is not an unassisted campaign run. Durable reports under docs/qa/hammer_chromium*. Game LF/test CRLF retained. No new raster generation or atlas changes; no commit/push.


## September 26: shake the complete hammer handle and hilt

Mike spotted that the original shake stopped partway down the handle. The raised hammer head, shaft, hilt and gripping hands now move together through the lowest visible handle pixels. A short upper-body flex joins the movement to the anchored torso; the charging glow covers the complete shaft. No new art or atlas edits. Healing, core interruption and reconstruction retain their behavior.

Full suite: 5,083 pass / 0 fail, exit 0 and final banner, unchanged from baseline. Native Chromium: 24 head/shaft/hilt/torso pixel comparisons across three raised poses and both shake directions all match 100%; existing nine damage-route and three complete-heal checks pass. No page/console errors. Inspected nine-second gameplay recording and enlarged crop at _shots/hammer_full_handle_0926/review.html. Details: docs/HAMMER_CHROMIUM_RECOVERY_0926.md; durable QA: docs/qa/hammer_full_handle_0926.json and hammer_full_handle_regression_0926.json. Game LF/test CRLF retained; no commit/push.


## September 26: lightning charges hammer, chest core spreads Chromium outward

Mike replaced the bottom-up empowerment with a chest-origin pulse. Lightning follows the shaking hammer tip and charges the weapon first. After 0.35 seconds, a bright reactor pulse and pixel-stepped expanding wave reveal the armor outward through the arms and legs. Rebuilding uses the same outward mask. Full-handle shake, healing timing and core counter remain. See docs/HAMMER_CHROMIUM_RECOVERY_0926.md; new recording/screenshots: _shots/hammer_core_wave_0926/review.html.

Syntax passed. Both full suites reached their final summaries at 5,082 pass / 1 fail, exit 1: 'a second lance may destroy the wounded 3-drone column'. Immediate baseline was 5,083/0; this exact intermittent failure is recorded in HAMMER_STORM_0926.md. No other failures; hammer checks passed. Native Chromium verifies initial hammer-only charge then core/arms/boots reveal, three difficulty timings, all nine core damage routes and completed/cancelled healing, hit flashes and gauge pixels, zero page/console errors. Reports: docs/qa/hammer_core_wave_0926.json and hammer_core_wave_regression_0926.json. Inspected real-canvas video/contact sheet; no new raster generation or atlas changes. Game LF/test CRLF retained; no commit/push.


## September 26: red recovery bar without text

Mike requested the pending recovery bar in red, without text. The segment and its pulse glow now stay #ff3030; the RECOVERY label is removed. Actual HP and armor keep their Chromium palette. Inspected native Chromium screenshot and refreshed video at _shots/hammer_core_wave_0926/review.html?v=red-recovery; no page/console errors. Syntax and final full suite passed: 5,083 assertions / 0 failures, exit 0 and final banner. Prior baseline was 5,082/1; the known intermittent drone assertion passed this run. Log: _shots/test_fl_red_recovery_0926.log. Game LF/test CRLF retained; no commit/push.


## September 26: Stage 2–4 encounter revamp and nuclear ordering

See docs/STAGE2_4_ENCOUNTERS_0926.md and docs/qa/stage2_4_encounters_0926.json. Stage 2 miniboss has a separate black/charred Furious book; Stage 3 keeps the original Frost Cruiser and Rime Wall hulls with neutral fight -> nuclear missile/engine explosions/whiteout -> Fire/Ice forms on Furious. Opposite element is 2x, same/neutral is 1x. Stage 4 bosses and helpers now take coordinated attack turns. The new assets/encounters_0926.js owns these live encounter directors; editor scenes retain their existing path. Full suite: 5,142 pass, zero fail, final banner and exit 0; no failing names against the 5,083/0 baseline. All 15 native Chromium cases, damage checks and five focused videos completed without page/console errors. Videos are invulnerable inspection fixtures, not campaign balance proof. Game LF/test CRLF preserved. Earlier work retained; nothing committed or pushed.


## September 26–27: Stage 5 music and shared weapon muzzle feedback

See docs/WEAPON_MUZZLES_0926.md and docs/qa/weapon_muzzles_0926.json. Stage 5 miniboss now uses the former boss track (Deadly Night); the main boss uses Mike's Hammerman Cometh, encoded for browser playback with the source WAV preserved. New assets/weapon_muzzles_0926.js attaches authored, weapon-specific muzzle reels to actual player/enemy releases, includes Maverick/Falva nose charges, ice breath and chain lightning, and replaces the flat player chaingun triangle and Stage 4 turret arrow flashes. Reaver, Warden, Sovereign and Stage 4 helper shots/flashes now use corrected visible barrel or launch-pod mounts. Shared flashes draw above boss hulls and support cached canvas art.

Final syntax checks pass. Full suite reaches the final banner: 5,159 pass / 0 fail, exit 0, against 5,142/0 baseline. Early passes found two stale source checks and two asymmetric hardpoint checks; source expectations and actual mirrored geometry were repaired. Native Chromium checks 55 valid pilot/weapon combinations, eight special/missile routes, all 11 reel families, moving-emitter lifetime behavior, three boss firing points and both actual audio decodes. Zero page/console errors. Five focused native recordings and inspected stills: _shots/muzzles_0926/review.html. Fixtures are for visual inspection, not campaign difficulty proof. Game LF/test CRLF retained. Existing work preserved; no commit or push.


## September 27: Stage 7/9 directors, field reactions, Stage 6 clarity

See docs/LATE_GAME_COMBAT_0927.md and docs/qa/late_game_combat_0927.json. New assets/combat_ai_0927.js and assets/late_encounters_0927.js own shared ordinary-enemy reactions/release gates, independent ally evasions (player timing: roll 5s, somersault 7s after completion), Stage 6 traffic/fire coordination and Rival turns, plus new Dredger/Warden/Horizon/Sentinel/Sovereign attack books. Preserved Warden story/core/cripple/escape and Sentinel fusion. Fixed missing drone sine amplitudes, cached-canvas Stage 9 projectile dimensions, new energy ordnance smoke and mine snapping. Existing authored art reused; no atlas edits.

Final syntax and full suite pass: 5,190 assertions / 0 failures, exit 0 and final banner (baseline 5,159/0). Native Chromium: 12 encounter/difficulty cases, nine-stage field rendering with 75 managed types, real ground/space missile damage and turret anchoring, predictive dodges, mine motion, Warden results transition, and projectile pixels. No page/console errors. Stage 6 peak hostile bullets in the controlled eight-ally window fell 35→26 / 42→34 / 61→48 (Normal/Hard/Furious). Five inspected native clips at _shots/late_game_0927/review.html are invulnerable inspection fixtures, not full campaign balance proof. Full mortal controller testing remains a tuning step. Game LF/test CRLF retained. Nothing committed or pushed.


## Codex update — 2026-09-27: modular Stage 7 tank/Warden and menus

- Mike explicitly authorized modular replacement of the Stage 7 tank and Warden.
  `assets/stage7_modular_0927.js` now owns these encounters; Stage 9 remains in
  `late_encounters_0927.js`. Seven generated sheets are registered as `s7m_*`.
- Six Warden modules, protected canisters, front/rear destruction gates, delayed
  exposed shield bar/counter-volley, survivor-gun and raised-mask laser endings;
  reversing terrain pursuit, swipes, committed jump/slam and three toxic orb waves.
  Tank chassis is constrained to the solid central ground corridor.
- Upright portal sits at the final traversable floor, 610px before the decorative
  void in the master. The Stage 7 spawn now requires actual terrain progress.
- Password horizontal navigation remains on its row; full-size cover/title and
  readable Fury Fighters opener. New generated-art prompts and paths are saved.
- Verification: syntax passed; full suite **5,221 passed / 0 failed**, exit 0
  (incoming 5,190/0; no failing-name regressions). Six native difficulty cases,
  native bullets/beams/Retina missiles, keyboard navigation, screenshots and three
  review videos. No page/console errors. LF/CRLF preserved.
- Full notes: `docs/STAGE7_MODULAR_0927.md`; evidence:
  `docs/qa/stage7_modular_0927.json`; preview:
  `http://127.0.0.1:8794/_shots/toxic_modular_0927/review.html`.
- Recordings are invulnerable inspection fixtures; named modules are forced to
  break in the progression clip. Do not present them as campaign balance clears.
  Existing work preserved; nothing committed or pushed.


## September 27: Reaperman is the Stage 7 boss theme

Mike supplied reaperman.wav. Both boss7 music aliases now select the encoded
Reaperman track; the previous theme is preserved byte-for-byte as
assets/game/music/unused13 - stage7b.mp3. Original WAV copied intact into
originals_0927; Desktop source untouched. Field music remains Over The Horizon.
Native Chromium decoded and played both new/archived themes with zero errors.
Syntax and full suite passed: 5,221 assertions, zero failures, exit 0 and final
banner; unchanged from 5,221/0 baseline. No gameplay code changes. Details:
docs/STAGE7_MUSIC_0927.md and docs/qa/stage7_music_0927.json. Nothing committed/pushed.


## September 27 overnight gameplay/audio pass, 04:40 checkpoint

See docs/OVERNIGHT_0927.md latest checkpoint and docs/VIDEO_REVIEW_0927.md.
Full suite: 5,309 passed, zero failed (suite-8.log), all runtime syntax checks pass.
Ten real Chromium clips with captured audio, 14 mastered SFX, 42 audible aliases,
51 encounter inspections and 27 improved finite-life campaign probes. Full human
balance is NOT approved; finite-life bot remains weak against ground warnings.
Review: http://127.0.0.1:8794/_shots/overnight_0927/review.html.
Current scheduled work continues until Sep27 08:00 NY. Nothing committed/pushed.


## September 27 overnight pass, 05:15 checkpoint

Current suite:5,316/0 (suite-12.log). Stage6 ally targeting/recharge and Tempest
warning clarity repaired. Stage7 generated body removes doubled faceplate;
mask/laser/muzzle warnings aligned. Native later-phase coverage17cases;
13 current audio clips. Saved gamepad reload/reconnect works with simulated
raw buttons2/5; physical pad untested. Review and detailed remaining work in
docs/OVERNIGHT_0927.md and docs/qa/BOSS_DIFFICULTY_REVIEW_0927.md.
Finite-life stage-script probes are arcade setups, not full campaign wins.
Scheduled work continues to08:00 NY; no commit/push.


## September27 overnight, 05:55 checkpoint

Suite5327/0, final banner/exit0 (`suite-16.log`). Fixed Stage4 generator access/HUD
placement and helper bounds; Horizon first-tick HP reset/durability/shared gauge;
Tempest return warnings; compact Stage6 HUD radio with special priority.
33 immunity damage-window samples are NOT player clears. 14current audio clips
and native screenshots in the overnight review. See docs/OVERNIGHT_0927.md
and docs/qa/BOSS_DIFFICULTY_REVIEW_0927.md for metrics and remaining work.
Next: Stage8 natural full-form progression and normal-life balance until08:00 NY.
No pending tools or writes; no commit/push.


## September 27 06:40 New York checkpoint — current verified state

Full suite `suite-22.log`: **5,347 passed, zero failed, final banner, exit0**. This follows the incoming5327/0 checkpoint. Suite19 aborted because a much earlier legacy fixture left playerHit stubbed; the new respawn regression now temporarily restores the real source function, then restores the prior binding. Suites20–22 pass. No commit/push. game.js remains LF; test_fl remains CRLF. Latest arrow-color synchronization is after suite22 and will be included in the next full run.

- Stage8 full-form natural damage routing: `probe_finale_progression_0927.py`, finale-progression/report.json. Ordinary aiming/fire, SpaceLaserIII/autoMissilesII, immunity except authored grabs,99reserve lives. All four forms defeated N274.63/H333.07/F384.58seconds, no deaths/errors/nonfinite projectiles. These are diagnostic durations, not campaign wins or human balance. Initial Furious sample timed out at360s; extended bound480s. A sound-wrapper fixture duplicates counts on later runs; do not use its raw cue counts as measurements.
- Final boss collision/Retina/shield pose now follows visible forms. Submerged phantom and clone formation center expose no invisible hitbox/lock; all four clones expose independent generic echo targets. Fake hits enrage that fake, real hits damage the boss. Knight/phantom/box use their own timed collision windows, without extra generic hull damage during a warning. Phantom and knight use local shared ground retinas/signs. Native finale-targets probe10checks/errors0; screenshots viewed. Refreshed cannon/finalform clips with sound; finalform peak.609.
- Actual-keyboard Hammer sample:22.18simseconds, ordinary collision, pauses between observations. Dodged a leap, countered into stun, then lost two lives to blast/another leap. Found real respawn bug: reset(true) reused the falling wreck's coordinates. playerHit now remembers the actual lethal-hit point; respawn restores it, clears stale velocity/somersault input, keeps the authored burning fall and120frame grace. Native real death->spin->respawn in all9stages returns exactly to hit position and spends one life. Warmed before/after space screenshots inspected. No claim that every possible movement bug is gone.
- Optional Rival Fight: five individual moving Retina/missile targets replace the formation-center target. No target while entering/warping/dead. Two chosen allies now use the shared navigation/evasion controller with normal5s roll/7s somersault recharge, correct poses and muzzle audio. AI tick moved from drawWorld to updatePlay, so rendering cannot advance cooldowns or fire. Native menu->Axel+Decker selection->card and30s fixture verifies both evasions/recharge, individual target damage and update-only progress. Generated controller prompts replace raw key text. Native first audio clip peak.830/errors0; label was found camera-relative and corrected. Refreshed clip pending.
- Furious Stage2 actual keyboard sample:13.45simseconds, ordinary damage, pauses; three lethal mistakes, no clear. It exposed paired cannon warnings/releases left at an old hull location. Incoming lanes now follow their owner's actual launcher while retaining committed firing direction; applies to bomber and ordinary missile jets too. Native moving-launchers probe checks both Magma mounts,5rounds per mount and bomber release; screenshots viewed. Arrow colors now use the same thirds as the shared green/yellow/red FOV.

Evidence: `_shots/overnight_0927/{finale-progression,finale-targets,respawn,rival-route,moving-launchers,manual-hammer-normal,manual-ward-furious}`. Current review recordings are being expanded to include every configured encounter across all9stages; fixtures remain explicitly labeled as inspection, not wins. Continue until08:00. Physical8BitDo and uninterrupted human campaign/difficulty progression remain unverified.


## September 27 07:15 New York checkpoint — current verified state

Full suite `suite-28.log`: **5,351 passing, zero failed, final banner, exit0**. No commit/push. This supersedes suite22 at06:40. game.js LF/test_fl CRLF preserved.

- Optional Rival Fight now clears temporary arena/allies on normal stage entry/title, restarts with the same five rivals and two chosen allies, saves its campaign return point rather than the arena's neutral stage number, and clears prior crew progression on a fresh campaign. Native menu/route/save/restart/cleanup checks all pass. Harness initially loaded Rival24 too late: suites23/25 had one cleanup failure,24 also had a lance failure. Loading the module with the initial runtime boot resolves the lifecycle harness mismatch; suites26–28 green.
- Reproduced intermittent legacy lance-column failure:6/150 attempts. The supposedly fixed targets randomly initiated airPatternTick lane curves before bullet collision; resetting them afterward was too late. Pin original target slots and a stationary route, keep all real bullet/hit/damage logic. Strengthened first-hit assertion to require all3 targets alive at1HP.150 repeats now pass; no gameplay lance or AI change.
- Generated six Stage4 ammunition families here (no SpriteCook), four frames each. New owning build measures uneven row gutters, preserves genuine RGBA and shared pixel scale, pads to256x320 cells. Replaces procedural Stage4 shells/rockets plus boss/mini MG and rocket art; no collision/damage/movement changes. Native24-frame renderer audit and actual Olive fight screenshots checked. Taxonomy/provenance registered. Stage3 still uses flat polygon ordnance; new generation is pending, not integrated yet.
- Review now25 real Chromium recordings with actual sound, covering all17 configured encounters plus late phases, Rival route and fleet. Three Stage4 captures refreshed after projectile change. All clips finite/zoom1/no page or console errors; movement max3.51px in these fixtures. Music gain explicitly0 during captures (helicopter intro previously restarted it). Largest current SFX-only peak .890 (Rival). Native review page decodes25videos+14solo sound auditions and all images,9working stage links; screenshots inspected.

Evidence: `_shots/overnight_0927/review.html`, `review_check.json`, `ordnance/report.json`, `rival-route/report.json`, `lance-stable-path.log`. These are selected-phase/immunity recordings, not campaign wins. Physical8BitDo hardware and full human difficulty progression remain unverified. Stage3 ammunition generation pending. Continue authorized work until08:00, then stop and report remaining work honestly.


## Latest verified state — September 27, 07:45 New York

This is the current result; earlier checkpoint blocks below are history. Scheduled work remains authorized only until08:00. Nothing committed or pushed.

- Full suite `suite-30.log`: **5,351 passing assertions, zero failures, final FALVA/LIZZIE success banner, exit0**. Syntax passes. Runtime `assets/game.js` remains LF; `test_fl.js` remains CRLF. Incoming September27 baseline was5,221/0; the intermediate failures and their repairs are recorded below.
- Review: [29 recordings and14 sound auditions](http://127.0.0.1:8794/_shots/overnight_0927/review.html),16m24s total nominal footage. Every configured encounter appears, across all9stages, with added Furnace core/head, paired Sentinels and Warden shield. Music muted for effect inspection. All43media files decoded;9stage links work; no native page/console errors. SFX-only peak maximum.893; normal input movement maximum3.51logicalpx/frame in these fixtures; zoom1 throughout. These selected-phase/immunity clips are **not campaign victories**.
- Generated and integrated24frames each for Stage3 ice and Stage4 military ammunition. Six families per stage, using measured row gutters and genuineRGBA. Game-owned XART/drawImage inspection confirmed all48frames and every actual drawBullets route; hitbox dimensions remain unchanged. Stage4 boss machine-gun/rocket routes use the new art too. Stage3/4 recordings refreshed. Sources/build/provenance/taxonomy retained; no SpriteCook.
- Furnace detached head now loses its permanently obsolete empty shield gauge. Core/arms and rearming shield gauges remain. Final head recording visually checked after this change.
- Normal Portal Warden actual keyboard sample:29.28simseconds, pauses between observations, ordinary damage/lives and MGIII/autoMissileII. Destroyed one front leg and observed its balance pose, avoided a committed chaingun and the jump center, then lost two lives to toxic volleys. No clear or balance claim.
- Normal Tempest actual keyboard retry:19.80simseconds including double-tap input frames,17actions, ordinary collision/lives. Real somersault and barrel roll registered and their7s/5s recharge advanced normally. Three deaths, one life remaining, no clear. Holding Retina intentionally blocks lateral double-tap rolls in the existing control design; release it to roll. This remains a high-priority human balance review. No difficulty change was made solely to rescue an input bot.

Current durable evidence: `docs/qa/overnight_0927.json`, `docs/VIDEO_REVIEW_0927.md`, `docs/qa/BOSS_DIFFICULTY_REVIEW_0927.md`. Native outputs live under `_shots/overnight_0927/` including `ice-ordnance`, `ordnance`, `manual-warden-normal`, `manual-tempest-normal-retry`, `late-review` and `review_check.json`.

Still unverified: uninterrupted human campaign clears across all difficulties, physical8BitDo hardware, and a strict stage-by-stage difficulty ranking. Tempest overlapping pressure, Hammer counter timing after cooldown use, Warden post-death firepower, and final-form fake/real target judgment need player review. This pass does not certify every legacy projectile graphic or every possible boss sound as finished.


## 08:00 handoff — September 27 overnight cutoff

The final game change was hiding the permanently obsolete Furnace head shield gauge; suite30 afterward passes5351/0 with the final banner and exit0. All13 changed runtime modules pass syntax. No commit or push. The runtime is LF and testsCRLF.

Current review contains29 real Chromium recordings with captured SFX (16m24s nominal),14 sound auditions and two new projectile frame galleries. Every media file and image loads, all9 stage links resolve, and native page/console errors are empty. Review: http://127.0.0.1:8794/_shots/overnight_0927/review.html.

Final actual-keyboard Horizon Normal sample (`manual-horizon-normal/report.json`):31 actions,53.1 simulated seconds with pauses between observations, ordinary collision/lives, selected Cole/SpaceLaserIII/autoMissilesII equipment. No forced kill or damage immunity after the initial2frame grace. BossHP6327→0 by51.1s; two lives lost, including a death during the defeat sequence. Play resumed alive with2 lives at53.1s. Eight manual missiles spent without Retina lock; primary/auto missiles also active, so the total HP loss is not a manual-missile-only damage measurement. All four attacks observed. No page/console errors. This is a paused encounter clear, not a real-time campaign win.

Remaining priorities: Normal Tempest combined attack pressure; Hammer counter/recovery survival with ordinary acquired gear; Warden full module order and post-death weapon-tier recovery; human final-form decisions; uninterrupted1–9 Normal/Hard/Furious progression and actual8BitDo hardware. The review also records remaining legacy art/audio/cinematic auditing. Nothing here certifies every prior creative request complete or all difficulties balanced.

All temporary output is under `_shots/`. Keep existing user work intact. Scheduled work ends at08:00NewYork; further implementation requires Mike's next instruction.


## September 27 afternoon — corrected modular roster

Mike corrected the new modular boss to Stage 3, requested the Stage 4 boss/black-brown warship/helpers too, moved the Earth bomber request to Stage 6, and authorized space Tempest remakes for Stage 5. Implemented in assets/modular_roster_0927.js plus measured generated art metadata. See docs/MODULAR_ROSTER_0927.md for exact assignments, Easy handicap, Furious final-form/true-ending gate and remaining balance limits. Built-in image generation only.

Final full suite: 5,432 passing assertions, zero failures, final success banner, exit0; incoming 5,351/0. Native checks: 20 encounter fixtures, six silent 26-second inspection clips (immunity/staged damage, not wins), 36 bounded ordinary-damage automated stage samples with all four difficulties. No native page/console errors. Final compact Stage4 helper geometry was rerun and re-recorded. Some bots failed on Easy stages1–2/7–8; Stage6 often outlasted the sample. Human campaign progression and final balancing remain unverified.

Review: http://127.0.0.1:8794/_shots/modular_roster_0927/review.html. Durable QA: docs/qa/modular_roster_0927.json. Runtime LF and tests CRLF preserved. No commit/push. Previous overnight automation remains paused.


## September 27 director pass — muzzle effects, destruction, Furious Tempest and thrusters

Mike's latest requested pass is implemented locally. See docs/DIRECTOR_UPGRADE_0927.md and docs/qa/director_upgrade_0927.json. No commit/push; the prior overnight automation remains paused.

- Generated here: four transparent sheets, sixteen distinct muzzle/exhaust families, six frames each. Measured ignition-root anchors and shared routing for player/enemy/boss emitters; explicit special, held-beam, Razorback, Furnace, Hammer and Harrier paths corrected. Harrier missile/plasma/laser routes verified individually; Maverick helix tap no longer selects toxic art. No SpriteCook.
- Modular part breaks use 12/18 staggered authored-engine explosions, following the moving hardpoint, idempotent per part, bounded at144 simultaneous queued blasts and cleared on stage change. Native large-part check drains18 blasts and rejects duplicate hits.
- Furious Stage5 space Tempest: Crimson Eclipse black armor/red energy, faster movement/charge/recovery, paired warned missiles and a five-lane bomb pattern with an escape lane. Hard retains Silver Eclipse. Engine destruction slows it and broken charging cannons interrupt attacks. Stage6 Earth bomber is unaffected by this Furious aggression.
- All nine pilots animate the exhaust already painted into their ships using six heat-pulse frames. Native pixel audit: six distinct frames per pilot, zero changes outside flame mask, zero alpha changes. Idle/bank/perspective supported; quick rolls retain authored poses.
- Final full suite5479/0, final success banner, exit0; incoming5432/0. Eight runtime modules pass syntax. game.js LF, test_fl/test_director CRLF. No baseline failing assertion names and no final failures.
- Review has7 real Chromium clips,145nominal seconds, actual SFX except two silent galleries. All decode; all posters/links work; native page/console errors0. Normal/Hard/Furious Tempest 35simsec each, finite projectiles/zoom1. Native special routes and Harrier mounts checked separately. These are controlled fixtures and staged module damage, not campaign victories or final balance proof.
- Special audition uses65% SFX plus0.4 capture-only gain (final sampled peak.831). Unattenuated overlapping specials measured peaks1.112/1.776; full-volume special mixing remains a follow-up. Other current clips peak below1. Capture gain does not modify game mixing.

Review: http://127.0.0.1:8794/_shots/director_0927/review.html. Sources/prompts/build scripts and metadata retained. Temporary evidence stays in _shots/director_0927. Prior human campaign, difficulty and hardware follow-ups remain open.


## September 27 — single muzzles, lance colors, ice breath and acceleration

Mike’s follow-up is implemented locally. See docs/PILOT_FEEDBACK_0927.md and docs/qa/pilot_feedback_0927.json. One centered ground emitter per volley; no stacked flashes at the real space cannon hardpoints. Fixed-strength homing lances now recolor across the five acquired laser tiers, with one matching muzzle flash. Generated twelve-frame Freezer ice breath here; measured nozzle roots and original RGBA retained. All nine pilots’ existing exhaust extends and brightens with real acceleration input, then eases back; space plume roots stay fixed too.

Final full suite:5492/0, final success banner, exit0, versus5479/0 incoming. Five intermediate new lance-flash failures exposed delayed-volley suppression and are fixed, with native firing confirmation. Four runtime syntax checks pass; game.jsLF and testsCRLF preserved. Native screenshots and actual draw routes inspected; three review clips/36nominal seconds with SFX decode, page/console errors0. Empty fixtures, not campaign wins.

Review: http://127.0.0.1:8794/_shots/pilot_feedback_0927/review.html. Generated source/prompt and owning build retained. No commit/push. The prior overnight automation remains paused; prior human balance/hardware/audio-mixing follow-ups remain open.


## September 27 — HAMMER password dance encounter

Mike supplied mchammer.wav and corrected the breakdown start to 0:16. Implemented a separate HAMMER password route through difficulty/pilot into a dancing Hammer space fight. Current break is16–24seconds: four backup dancers, generated deflective shield, uninterrupted music, frozen combat/actions and blocked in-game pause, then restored control/special and a short opening. Ordinary campaign Hammer stays separate. Generated here:16 boss poses,8 backup poses,8 shield frames; canonical single-headed hammer, stable anchors, no SpriteCook. Supplied track imported as hammer_time_mike_0927.mp3, original untouched. No separately generated singing audio; mouth motion follows the supplied track envelope.

Runtime: assets/hammer_time_0927.js plus generated metadata; no game.js edits in this pass. Owning build and prompt sources retained. Full suite5513/0, exit0/final summary versus5492/0 incoming. Intermediate fixture/Windows encoding errors were corrected; final failing-name list empty. Syntax and LF/CRLF checks pass. Native four-difficulty36simsec fixtures reach ball pattern, warnings/projectiles finite, zoom1. Actual victory frame-loop fixture returns to title and cleans music/lock.36nominal-second real Chromium recording with supplied music:16.013–23.988s lock,499 frames, zero position/ammo/shot/pause violations; zero page/console errors. Invulnerability recording aid, not a completed gameplay win or final balance proof.

See docs/HAMMER_TIME_0927.md and docs/qa/hammer_time_0927.json. Review: http://127.0.0.1:8794/_shots/hammer_time_0927/review.html. Mike should test balance, gamepad behavior and the chosen eight-second break endpoint. No commit/push. Prior overnight automation remains paused.


## September 27 — HAMMER flat wall, locked entrance and fighting helpers

Latest follow-up implemented locally. One generated flat horizontal forcefield, one draw at50% opacity, spans the whole world including scrolling edges. Entrance now locks all gameplay and pause through descent, canonical hammer raise/slam, engine explosion/shock ring, and four staggered robot arrivals. All difficulties receive the dancers; only Hard/Furious/Insanity helpers fight (warned aimed bursts/fans, muzzle/audio/hit/death feedback, Retina/space/missile targeting). One helper attack at a time during quiet boss beats. Insanity now takes the secret encounter's Furious Hammer logic. The0:16–0:24 dance break remains. Fixed protection after unlock to actual engine frame units (60 entrance/48 break). Normal campaign unchanged.

Full suite5538/0 versus5513/0 incoming, final success banner/exit0; one intermediate grace-period failure fixed. Syntax and LF/CRLF checks pass. Native five-difficulty encounter fixtures, entry freeze/summon order, armed-helper targeting/damage, one wall draw at.5 opacity, victory cleanup pass; page/console errors0. New36nominal-second Hard recording with supplied music: entry release5.749s,4helpers,12missiles unchanged; break16.003–23.991s,500locked frames, no action/pause leakage. Audio peak.457 at capture-only gain.4. Controlled fixtures/immunity recording, not gameplay victories or final balance proof.

Details: docs/HAMMER_TIME_WALL_0927.md, docs/qa/hammer_time_wall_0927.json. Generated wall provenance/owning build retained. Review: http://127.0.0.1:8794/_shots/hammer_time_wall_0927/review.html. No commit/push; prior automation stays paused.


## September 27 — HAMMER ship entrance and continuous opening lock

Mike corrected the ship/music choreography. Implemented in assets/hammer_time_0927.js: playback begins with the actual authored Hammer ship entrance after art/audio readiness; ship transforms, canonical hammer slams at6.15s, four helpers arrive from6.4s, one half-transparent wall rises7–16s. Helpers hold poses until dancing starts16s. No playable gap: all actions and pause remain locked from the entrance through24s. This replaces the old5.75s entrance unlock in the prior note. Existing approved art/music reused; normal campaign unchanged.

Full suite5545/0 versus5538/0 incoming, final success banner/exit0, failing-name sets empty. Runtime syntax and LF/CRLF pass. Native five-difficulty fixtures, actual ship draw, wall alpha/draw, action/damage blocking, helper targeting and victory cleanup pass. First native exit check was contaminated by held physical gamepad inputs selecting Armory after title; final keyboard fixtures isolate desktop hardware, no runtime workaround. New36.07s real Chromium Hard clip with music/SFX: dance16.011–23.999, first control24.011;500breakframes, no movement/shots/ammo/pause leakage throughout opening,4helpers/12missiles at release. Peak.528 at capture gain.4. Screenshot and review/video checks pass with zero page/console errors. Controlled fixtures/immunity recording, not campaign wins or final balance.

See docs/HAMMER_TIME_SHIP_0927.md and docs/qa/hammer_time_ship_0927.json. Review: http://127.0.0.1:8794/_shots/hammer_time_ship_0927/review.html. No commit/push; overnight automation remains paused. Prior balance/hardware follow-ups remain.
