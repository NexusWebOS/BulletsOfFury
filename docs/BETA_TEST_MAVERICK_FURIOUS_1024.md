# Bullets of Fury — Maverick / Furious Beta test

**October 24, 2026 · Runtime baseline `a5760cb4ab856b2e48f2d3fabc70720a47a86b21`**

**Result: native campaign victory, Rebel Fighters defeated, Stage X Harrier defeated, optional Stage 9 cleared, and Dracodia's complete combat sequence defeated.** Maverick and Furious remained selected throughout the recorded host samples. Final score: **1,672,640**; final life stock: **7**. Recorded ranks: **1 B · 2 A · 3 A · 4 A · 5 C · 6 A · 7 B · 8 B · 9 B**.

This is an automated completion and presentation test, **not a human Furious skill clear**. The bot died at **00:03:15.11**; the existing God mode was then enabled as authorized. It favored the southern playfield and aligned with visible targets, occasionally moving for native pickups. Enemy health, part health, damage, ammunition, rewards and speed were not edited. This delivery publishes the videos and Beta report; recorder tools and raw diagnostics remain local. It does **not** claim the recommendations below are already fixed.

## Watch the evidence

- [Download/watch the continuous campaign movie](https://github.com/NexusWebOS/BulletsOfFury/releases/download/beta-test-maverick-furious-2026-10-24/Maverick-Furious-Beta-Playthrough.mp4) — **59:51.79**, 1280×720, H.264/AAC, normal speed, approximately 1.34 GB.
- [Complete post-Stage 1 and post-Stage 3 story replays](https://github.com/NexusWebOS/BulletsOfFury/releases/download/beta-test-maverick-furious-2026-10-24/Maverick-Story-Replays.mp4) — **2:11.40**, explicitly separate from the campaign take. Stage 3 starts at **01:12.61** in this supplement.
- [Complete post-Stage 2 story replay](https://github.com/NexusWebOS/BulletsOfFury/releases/download/beta-test-maverick-furious-2026-10-24/Maverick-Post-2-Story-Replay.mp4) — **0:40.13**, the additional early scene affected by the same recorder Skip, kept separate from the main movie.
- [Complete Maverick ending replay](https://github.com/NexusWebOS/BulletsOfFury/releases/download/beta-test-maverick-furious-2026-10-24/Maverick-Complete-Ending-Replay.mp4) — **2:33.60**, the native expanded ending through its final card, recorded separately using the game's cinematic viewer.
- [Release and chapter list](https://github.com/NexusWebOS/BulletsOfFury/releases/tag/beta-test-maverick-furious-2026-10-24).

**Recording exceptions are visible and retained.** Early menu automation accidentally sent START/Skip during part of post-1, post-2 and post-3; later protected scenes were left to run naturally. Complete replays are supplied instead of secretly splicing them into the take. After the Rebel Fighters, the game launched Stage 7 while the earned Harrier route remained pending. At **00:45:41.31**, the review adapter invoked the existing campaign map action, then launched the already-earned Stage X route. The first Stage 7 visit was abandoned; Stage 7 was subsequently replayed and cleared in full. No clear/unlock was granted by this intervention.

The main recorder also stopped using the **old 59.6-second ending-card constant**. The newer invasion ending lasts 145 seconds before its card, so the continuous movie stops during that expanded ending, after the actual campaign victory. The complete native ending is therefore a clearly labeled supplement, not a claimed continuation of the original capture. Its score display uses the final score from the completed run. This is a recorder defect, not an ending failure in the game.

## Route and encounter coverage

Times refer to the main movie; telemetry and movie start differ by less than a second. Encounter windows include native entrance/recovery where present, not damage-only speedrun times.

| Chapter | Time | Coverage / result |
|---|---:|---|
| Opening | 00:00:00 | Naturally timed opening; first PLAY approximately 03:10 |
| Stage 1 | 00:03:10 | Razorback 03:52–04:44; Dam Keeper 05:32–06:19; clear |
| Stage 2 | 00:08:06 | Magma Ward 08:31–09:19; Inferno Reaver 09:49–10:35; clear |
| Stage 3 | 00:12:11 | Frost Cruiser 12:37–13:02; Cryospear 13:32–14:08; clear |
| Stage 4 | 00:15:37 | Olive Warden 16:03–16:33; Storm Sovereign 17:12–18:49; clear |
| Stage 5, first leg | 00:20:48 | Siege Bomber 21:19–21:43; earned portal route to Stage 9 |
| Optional Stage 9 | 00:22:31 | Void Horizon 22:52–24:10; Tidal Fusion → Sovereign 24:46–25:41; clear |
| Stage 5, return | 00:26:22 | Chronos 26:32–31:13; native destruction sequence and rewards |
| Post-5 HQ scene | 00:33:06 | Forge/chaingun story, alarm and deployment |
| Stage 6 | 00:34:24 | Siege Fortress 36:31–36:54; Rebel Fighters 39:14–41:18; clear |
| Stage 7, first visit | 00:42:53 | Dredger defeated; Sludge Emperor started; visit abandoned for earned Harrier route |
| Stage X | 00:45:50 | Coastal entrance/city; carrier → death → Harrier ace → flyover; clear and reward |
| Stage 7, full return | 00:47:56 | Dredger 48:28–48:56; Sludge Emperor 49:56 onward; native exit to Stage 8 |
| Stage 8 | 00:51:19 | Herald of Death 51:51–52:15; first Dracodia body 52:48; rebirth 53:50 |
| Dracodia final encounter | 00:54:50 | Main form; corrupted Hammer 55:32; helicopter 56:19; brain 56:43; volcano 57:02; brain returns 57:56 |
| Final destruction / victory | 00:58:11 | Native destruction, portal/reunion, results at 58:37, ending begins 58:45 |

Native Stage X completion data was `done: true`, `signatureMk2: true`, `rewarded: true`. Native final completion was `state: victory`, `_trueFinaleCleared: true`. All four final copy identities above were verified from actual phase events and artwork; the standalone Harrier remains separate from Dracodia's brain replacement.

## Confirmed findings and recommended fixes

### BETA-01 — P1: earned Stage X route loses its normal handoff

**Evidence:** Stage 6 rewards at 41:28 onward, followed by Stage 7 approach at 42:12. The pending route remains `{route: 'left', done: false}`. The pause menu has no direct campaign-map return. Intervention is logged at **45:41** and the earned route launches at **45:50**.

**Player impact:** a player following the story can pass the desired optional pursuit without seeing its choice at the correct moment. This is a campaign-flow defect; it did not prevent the main campaign from proceeding.

**Change:** give one owner responsibility for the post-6 callback. Present the earned pursuit/map choice before automatic Stage 7 launch, preserving saved route and reward state. Inspect the cinematic director, campaign focus/leave-stage wrappers and `cf4LaunchX` handoff together.

**Acceptance:** beat either Stage 6 branch through normal UI; the opposite earned pursuit is offered before Stage 7, can be declined, survives save/reload, and grants its reward once. Test both pursuit directions and a completed-route revisit without review adapters.

### BETA-02 — P1: sustained hit flashes conceal the upgraded actors

**Evidence:** Harrier at **45:56–46:44**, Dracodia first body at **53:00–53:44**, main final actor at **54:55–55:15**. Several consecutive visual samples show almost solid-white silhouettes. See the hit-flash evidence in the main movie. A read-only observer installed late in the run sampled the owner `flash` timer active on **546/601 Herald frames (90.8%)** and **6,256/8,729 Dracodia frames (71.7%)**. These percentages cover the observer's remaining encounter windows, not every pixel or the entire game.

**Supported mechanism, requiring the final targeted regression test:** `gameplay_repair_1004.js` gates some owner hits at 0.14 seconds while the default flash lasts 0.16 seconds. A native-function probe on a flagged diagnostic part confirmed that hits 0.15 seconds apart refresh the flash with 0.01 seconds still remaining. Sustained rapid fire can therefore refresh before normal palette returns. This probe did not edit a live enemy. Other writers and part flashes must also be checked; it does not isolate every real attacker's causal contribution.

**Change:** keep the required visible hit response for every owner/part, but guarantee readable normal-palette recovery between flashes under continuous player and ally fire. If needed, use authored white-lit hit cells that preserve armor seams and weapon silhouette. Do not zero hit flashes or commission replacement art merely because the current art is hidden.

**Acceptance:** compare native-speed fire-off and sustained-fire captures for Harrier, Herald, Chronos and every Dracodia copy, with and without allies. Every damage event still has visible feedback; recurring normal-palette windows expose the face, hammer, muzzle, windup and recovery. Verify individually targeted parts too.

### BETA-03 — P2: two Stage X entrance-card owners render together

**Evidence:** **45:50**, legacy `STAGE X / FRACTURED …` behind the new `SEABREAK CITY / COASTAL FRONT` card. See duplicate-card evidence in the main movie. The new coastal city and scrolling environment are present.

**Change:** retain the selected coastal-city card in `coastal_city_1021.js`; retire the old card invocation for this route. Trace both draw owners before editing their assets.

**Acceptance:** one title card, one entrance cue, centered text with safe margins at narrow and wide aspect ratios, then a seamless coastal-to-city scroll. Check both Stage X route variants.

### BETA-04 — P2: live Chronos dialogue hides useful combat information

**Evidence:** **26:58**, large upper/central dialogue overlaps the boss/charge area while gameplay continues; the portrait is tiny/noisy inside its aperture. See dialogue evidence in the main movie.

**Important diagnosis:** the current source portrait is a readable framed head/bust. During the encounter, `XART.get('fb1002_hammer_portrait')` resolves to the 1254×1254 `feedback_1003h/hammer_portrait.png` alias, while `_src` still names the older file. This is a layout/resolved-binding investigation, not evidence that the artist supplied a full-body portrait. Initial lazy loads can return a 1×1 canvas; inspecting the requested filename alone is insufficient.

**Change:** use a compact live-combat radio aperture and correct crop/aspect for the resolved portrait. Keep the full cinematic window for protected story scenes. Inspect `command_ui_1020.js`, `cinematic_director_0930.js` and `feedback_1003h.js` together. Preserve the user's requirement that Chronos speech never pauses combat.

**Acceptance:** activation, throw and charge announcements remain readable, portrait recognizable, and player/boss/warning lanes visible. Text fits and centers within its border at the representative phone-sized layout and 1280×720. Player movement, hostile fire and the boss clock continue during each announcement.

### BETA-05 — P2: armor depletion looks like stalled body damage

**Evidence:** Chronos body maximum **11,220**, separate initial Chromium armor **8,415**. Main body HP stays flat for much of **26:25–28:00** while armor is depleted. Later diagnostics show armor zero/inactive and ordinary body damage. The fight eventually clears; this was not a damage softlock.

**Change:** distinguish ARMOR, BODY and missile-counter objectives in the approved HUD, with a clear transition when armor breaks. Keep the authored SHOOT graphic. Do not reduce HP simply to conceal an unclear bar.

**Acceptance:** a fresh player can tell whether bullets are damaging armor, a part, or the body, and why a missile-only target matters. The same distinction remains clear during recharge/healing; actual values agree with the displayed bars.

### BETA-06 — P2: repeated white FX hide turret motion

**Evidence:** Frost Cruiser **12:38–12:58**, Olive Warden **16:15–16:21**. Large repeated muzzle/impact clouds and owner flashes conceal gun silhouettes. See turret/FX evidence in the main movie.

**Change:** isolate muzzle flash, hit flash, impact, shield and recoil owners in a native review view. Tune authored FX footprint/hold time and layering so turret rotation and emitter attachment remain visible. These samples do not establish that the rotational banks themselves are defective.

**Acceptance:** two complete salvos show a stable attached muzzle, readable rotation and recoil/recovery at normal speed under player fire. Retain every required attack/hit cue; buy replacement banks only if a specific missing/broken pose remains visible after the masking issue is fixed.

## Balance, pacing and style concerns — follow-up tests, not proven defects

| Concern | Evidence / interpretation | Recommended experiment |
|---|---|---|
| Early power curve | Ordinary pickups reached weapon V by Stage 2. God mode preserved resources and avoids the normal death economy. Ice Orb is a base weapon, so its appearance here is not an unlock leak. | Matched pilot/weapon-level runs with and without a death; compare time-to-kill, pickup frequency and meaningful weapon choices before changing caps. |
| Late miniboss hierarchy | Dredger and Herald clear in roughly 22–28 seconds in this high-gear, immune run; Herald is meant to be the hardest miniboss. | Equalize entry gear, test human dodge pressure and safe windows, then tune committed attack combinations/recovery rather than adding blind HP. |
| Southern-edge strategy | The bot favors the bottom and still clears. There are 4,437 contact-attempt callbacks after/around immunity; repeated overlaps are not independent deaths or proof of unavoidable damage. | No-God tests with reaction delay and low/expected gear; measure lane coverage, warning-to-contact time, escape options and resource cost. Preserve roll/somersault counterplay. |
| Long exposition gates | Opening approximately 2:42; Stage 6 wave clock parks at 57.55 during roughly 100 seconds of live radio around 37:00–38:40. Movement/background continue, so this is not an engine-pause failure. | Shorten repeat-run recap and distribute Stage 6 exposition between threat beats. Retain first-run story and existing Skip; do not dump lethal patterns beneath a reading task. |
| Threat contrast | Amber Stage 1 bullets over tan jungle at 04:21; large Stage 2 beam/flame layers around 10:20–10:41. | Native-scale moving review of hostile silhouettes and warning/escape geometry. Adjust authored contrast/spacing only after viewing full salvos; one still cannot prove invisibility. |
| Mixer headroom | Some decoded combat/ending samples peak at 0 dBFS. | Listen and meter native music/SFX buses separately with repeatable salvos. A captured 0 dB peak alone does not prove the game's mixer is clipping. |

Keep BOF's metal frame language, military bitmap type, strong pilot colors and readable stage palettes. Stage 9's water enemies intentionally remain in the void arena, per the chosen direction. Cole's likeness/animation remains pending the user's approval; this test does not approve it or authorize copying an unapproved face to the other pilots.

## What worked in this run

- Siege Bomber's **four modules were all zero before portal departure**: at 21:39 one remained at 32.67 HP; at 21:41 all four and owner HP were zero. Stage 9 did not bypass a living miniboss.
- Storm Sovereign was actually reachable and defeated in about **96 seconds of live sampled encounter coverage**, rather than the previously reported four-minute stall. This verifies one mixed-arsenal path, not every weapon/part combination.
- Chronos's shielded hammer charge is visible at **27:34–27:40** and **28:35–28:39**. The authored SHOOT header, throw, depth combo, chaingun pickup/use, red armor/aura and red-energy hammer, stun and destruction all appear. White hit states must not be mistaken for permanent broken chrome edging. Individual contact-face continuity still needs focused frame review.
- The Stage X coastal entrance and city scroll, native carrier/ace sequence, and reward work once reached.
- The Stage 7 full return exits through the native transition into Stage 8. Dracodia's entry, first body, symbiote rebirth, main form, corrupted Hammer, helicopter, Neural Archon brain and volcano all occur, followed by native destruction, portal/reunion and victory.
- No page JavaScript exceptions or recorder write failure were logged during the campaign. No HTTP status of 400 or higher was logged.

## Performance, loading and completion metadata

The recorded engine averaged **53.2 RAF frames/s** over the entire take, including menus: median **16.7 ms**, p95 **33.3 ms**, p99 **50.1 ms**, maximum **966.6 ms**. Capture, screenshots, local serving and audio routing add overhead. The MP4 is variable frame rate, approximately **20.63 captured frames/s on average**, despite a requested 30 FPS. Do not confuse this with native simulation rate, or infer missing animation frames solely from the encoded movie.

A separate **35.5-second unrecorded Stage 4 entrance/early-play probe** measured p95 **17.0 ms**, p99 **17.4 ms**, maximum **583.4 ms**, with no page exceptions. It used different gear and no matched boss workload; it suggests capture overhead matters but does not certify late-boss performance. Profile matched native scenes without capture before assigning a game-side optimization defect.

There were **two console transport timeouts**, for `modular_roster_0927/rime.png` and Chronos `blue_throw/09.png`. Both files exist, returned **HTTP 200** and decoded successfully in a fresh browser retry. There were also **69 aborted requests**, predominantly native audio-pool/scene activity; these are not 69 established missing sounds. The local Python server and its request behavior are part of this test environment. Add a resolved-asset/preload retry audit, but do not label the art missing based on this run.

The separate completion-proof object retained pilot `axel` and omitted Stage 7 while all host samples identified Maverick, all campaign ranks 1–9 exist, and native true victory was reached. The proof wrapper initializes before native `startRun` assigns the selected pilot; Stage 7's direct exit uses a different append path. Treat this as **BETA-07 / P2 completion-metadata consistency**, with setup sensitivity: reproduce through normal pilot selection and both direct/map exits before claiming the production UI is affected. Normalize proof pilot/stage records at their actual commit points; do not use this stale field to mislabel the video or invalidate the recorded native victory.

## Recommended change strategy

1. **Repair campaign ownership first.** Fix BETA-01 route handoff and BETA-03 duplicate card. Add route/save/reward-once checks. These are concrete progression/presentation fixes requiring no paid art.
2. **Expose the existing artwork.** Address hit-flash recovery, live dialogue aperture/portrait binding, armor/objective bars and turret FX masking. Re-record identical sustained-fire excerpts before/after; keep native hit feedback and non-pausing Chronos speech.
3. **Measure a matched combat baseline.** Replay Storm Sovereign, Chronos, Harrier, Herald and all Dracodia copies with identical gear, allies and inputs, both recorded and unrecorded. Track frame-time spikes, active actors/bullets, sound voices and asset waits. Fix proven owners, then repeat once.
4. **Tune difficulty with human evidence.** Test expected gear plus a low-gear boundary on Furious without immunity. Compare bottom-hug, mobile and missile-conserving strategies. Tune warning/commit/recovery and safe-lane pressure before HP. Validate regular bullets and sonic waves remain non-interceptable while designated missiles/hammer targets retain their special rules.
5. **Buy only targeted art gaps.** Use resolved assets, canonical hammer references, fixed frame cells/pivots and emitter anchors. Review windup → active/contact → recoil → recovery under fire, not only on a clean sprite sheet. Generate only the exact failed bank, then integrate and film it again. Preserve Dracodia's four approved copy identities and standalone Harrier.
6. **Tighten cinematic delivery.** Shorten repeat-run exposition, verify stage callbacks and the newer ending timeline, distinguish cast silhouettes/palettes, and keep subtitle/portrait geometry inside approved frames. Cole likeness stays a user review gate.
7. **Run a release regression pass.** Normal UI campaign route/save/reload; part gates with bullet-only and missile weapons; every Chronos difficulty combo; each copy transition/death; narrow/desktop text; physical controller; audio listening; clean asset loading. Publish a new gameplay build only after these pass.

## Method and limits

Microsoft Edge ran the actual game `index.html`, native requestAnimationFrame, simulation, artwork and audio. Review input read visible/exposed target markers and wrote ordinary native Input keys with a reaction delay; menu confirmations used browser keyboard input. The controller was refined during the run to preserve fire during combat-live speech, prefer boss/module markers over edge missile markers, and use the native missile cadence during the healing counter. These changes, the God activation, route intervention and audio-capture refinements are retained in the local event log/source history. They alter the reviewer, not enemy stats or completion conditions.

The original WebM was streamed to disk and encoded at normal speed without animation interpolation, deleted defeats or synthetic combat. Audio came from native media/WebAudio; the capture adapter was refined for repeated pool playback and unity-gain compatibility. Decoded audio is nonempty at opening, combat, late bosses and ending; this is not a comprehensive listening/mix certification. All four complete MP4s decoded to completion with exit 0 and no codec-error messages. The null-output verification produced timestamp-order warnings (main 6, post-1/post-3 story 0, ending 139; post-2 checked separately); small audio timestamp corrections also occurred during encoding. Edge playback and seeking at early, middle and late positions succeeded for every movie, without media errors. The capture is variable rate, so these checks do not establish frame-perfect synchronization with the original simulation.

Analysis combined continuous native telemetry, systematic transition/interval screenshots, and selected native-time video excerpts. It is **not a claim that every frame of every attack was manually inspected**. No paid PixelLab generations were spent for this review. No shipping runtime/art files were changed.

Not covered as a certification: physical gamepad operation, mobile touch hardware, every pilot, the alternate Stage 6 branch/Stage X direction, Barbie fight, all Forge/respec recipes and previews, all save migrations, every per-weapon modular target gate, human Furious fairness, console builds, or Cole likeness approval. Those remain explicit follow-up coverage rather than silently marked complete.

Applied review skills: ColeForge workflow, portability, playtest/release, shmup design, boss design, enemy AI, combat feel and art direction; Game Studio playtest; game verification, balance, HUD readouts, performance and player UX. BOF's authored-frame/bitmap UI rules take precedence over generic effects recipes.
