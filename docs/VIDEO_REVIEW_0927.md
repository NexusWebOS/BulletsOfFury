# September 27 recording review and overnight repairs

Source: Mike's `2026-09-27 02-54-46.mp4`, 9:08.50, 1280×720, 30 fps. This report describes the local working build, not a pushed release.

## What the recording shows

| Approximate time | Observed section | Response in this build |
|---|---|---|
| 0:00–1:58 | Stage 5 opening and retired miniboss | Replaced by the generated modular Eclipse Siege Bomber. Engines and cannons are independently targetable; bombs trail behind it and its charged forward beam threatens the allied wing. |
| 2:07–4:05 | Stage 9 Horizon and Tidal encounters | Committed warning lanes and distinct attack turns. Fixed a recovery-position jump after Horizon arrives, cleared disabled Sentinel warnings, and kept fusion/portal/hull positions in world coordinates. |
| 4:15–6:15 | Stage 5 Hammer fight | More HP, the ball attack retained before the low-health transition, faster Hard/Furious slam lasers. The red fields and warning signs now end separately as their own spikes erupt. |
| About 5:52 | Persistent red spike fields | Native frames now show warning-only lanes beside active spikes with no retained red field or sign on the active spike. |
| 6:20–7:15 | Weapon Forge | Elemental previews have sound; Maverick's equipped Fire Whip wins over his old lance selection. Added generated graphical Armory collection with unknown cells. |
| 7:20–end | Stage 6 Harrier | Fighters launch from the front bay toward north, grow from 18% to full size, then peel into their combat positions. |

Stage 4 and Stage 8 are not present in this recording. Their reported problems were checked separately in native Chromium.

## Additional fixes

- Stage 4 no longer zooms out to fit its boss. The game keeps its normal gameplay scale.
- Camera shake is limited to under two logical pixels. Stationary enemy-kill checks in all nine stages produced zero player-coordinate, camera-coordinate or zoom displacement. This does not prove every possible movement defect is eliminated.
- Stage 2/3 encounter controllers and Horizon no longer begin their first recovery move from stale offscreen spawn coordinates after arriving.
- Stage 8 has no automatic Furious elite-helper additions. Its large regular ships wait until visible before charging; simultaneous volley releases are spaced apart, and regular fleet pressure is capped by difficulty.
- The final boss's ghost walls stay at their cast location in world space. They no longer follow the camera and amplify their own push. Somersault animation remains smooth while horizontal confinement uses the ship's ground position.
- Map selection lights the chosen island silhouette only. The marker ship remains upright. Verified through actual menu input and the complete scene renderer.
- Shadow Orb's damage multiplier is .78 instead of 1.35, about 42% lower. Offensive specials own the trigger while active. Cole/Lizzie missile specials and defensive abilities keep their intended primary weapon behavior.
- Manual and automatic space missiles damage ordinary enemies, Hammer and the new bomber without Retina lock. Native input checks spent ammo and measured target damage.

## Sound pass

Fourteen finished MP3 effects combine generated ElevenLabs sources with ColeForge SFX-engine layers. They cover missile launches, cannon charge and discharge, heavy impact, beam release, toxic and ice attacks, alien calls, module breaks, stun and magnetic recovery. Forty-two cue aliases point to the new effects, with gain and repetition limits.

An additional bug was found during verification: the first sound-throttle implementation used `stageTimer`, which pauses during miniboss encounters. It is now driven by elapsed combat time. Repeated attack cues were rechecked on Stage 2, 3 and 9 minibosses while their stage timers stayed frozen at 30.

All 42 aliases decoded and played audibly in Chromium. Twenty-nine current videos capture real game audio, with measured SFX-only peaks at or below .893; music is muted in those clips to expose the effects. Source IDs and prompts are in `audio_sources_0927.json`; mastering is reproducible through `_BUILD_SOURCE/build_audio_0927.py`.

## Verification and limits

- Syntax checks pass for every changed runtime module.
- `_shots/overnight_0927/suite-30.log`: full suite reached its final success banner, **5,351 passing assertions, zero failures**, exit 0. Incoming recorded baseline was 5,221/0. New behavior tests cover framing, missiles, specials, Hammer, Harrier, fleet spacing, entry recovery, fusion placement, wall confinement and repeated attack audio.
- A native encounter inspection covered all 17 configured boss/miniboss encounters across Normal, Hard and Furious: 51 cases. Stage 8 has no separate miniboss. All entered once, retained finite positions/projectiles, emitted sound cues, and produced no page/console errors. These opening-health inspections do not cover every later form.
- Additional current recordings cover Hammer ball/Chromium, Stage 4, Harrier, bomber, Stage 8 fleet/cannons/final forms, Horizon and Tidal fusion. These use damage immunity and selected starting phases. They are inspection evidence, not campaign wins.
- Two 27-case campaign input-bot sweeps exercised all nine stages on all three difficulties without damage immunity or forced kills. The improved bot uses normal roll/somersault cooldowns. It cleared Stage 9 on Normal and Hard but lost its lives in the other cases. It poorly understands ground warnings, body strikes and encounter-specific targeting. These results are **not a claim that all nine stages are balanced**.
- No native page/console errors were reported by these probes. Full human difficulty progression and controller-hardware feel remain review items.

Review: `http://127.0.0.1:8794/_shots/overnight_0927/review.html`.

## Remaining overnight priorities

1. Further finite-life encounters with ground-warning avoidance and appropriate module targeting, particularly Stage 5's new bomber and Stage 6's field/miniboss pressure. Do not tune the game solely to compensate for a weak test bot.
2. Check later-health audio/attack coverage for Stage 2, Stage 3 Furious forms and Stage 7's leg/shield/core sequence. Existing native fixtures cover their visuals but the final audio routing was added afterward.
3. Compare representative mid-level loadouts and boss time-to-kill across difficulties. Stage progression should gain complexity without hidden frame, movement or unavoidable-damage penalties.
4. Keep the final report explicit about completed changes and balance limits. No commit or push without Mike's instruction.


## 05:15 follow-up

Current suite is **5,316/0**, `_shots/overnight_0927/suite-12.log`. The review now has13 current audio clips. Stage6 allies now target live miniboss modules and recharge on a combat clock while wave progression is paused. Tempest warnings use shared authored graphics, with a longer committed tell on Normal and controlled engine/beam audio. Stage7 has a newly generated body without a duplicate faceplate, a visibly raised mask over the real emitter, matching sweep/gun warning origins and green toxic muzzle flashes.

Additional later-phase native inspection:17cases, zero errors/reentries. Saved controller bindings survive actual page reload/disconnect/reconnect for simulated raw buttons2/5. The two-ally native test counted14 missiles during a frozen stage timer. These do not establish physical controller compatibility.

V5 finite-life probes reached the Stage5 boss and Stage8 boss on all three difficulties; the latter's first death was in the boss fight. They still exhausted lives. Stage6 remains difficult for the bot at the Tempest duel. The stage probes initialize arcade mode with selected equipment; the phrase campaign probe above refers to campaign-stage scripts, not uninterrupted campaign play. Current encounter-by-encounter recommendations: `qa/BOSS_DIFFICULTY_REVIEW_0927.md`.


### 05:50 follow-up

The Stage 4 damage-window probe revealed a second problem beyond framing: generators were partly hidden by the gauges/HUD and the carrier field intercepted ordinary shots aimed at the upper pair. Their spacing now clears both; native shots destroyed every generator. The large helper hulls retain their authored size with world-bound clamping.

Horizon also discarded its scaled HP on the first combat tick; it now preserves the pool and has enough durability to show its entire attack book. Its gauge uses the campaign miniboss frame. Stage 6 chatter moved into the reserved HUD bay and pauses for specials; Tempest's previously unmarked return from offscreen now has a committed warning.

See docs/qa/BOSS_DIFFICULTY_REVIEW_0927.md for the 33-case damage-window table and limitations. No uninterrupted campaign clear or physical controller verification is claimed.


## Final overnight review additions, 07:45

- Fixed a real death/respawn jump: the engine previously reused the falling wreck position. It now remembers the actual lethal-hit position, respawns there and clears stale movement/flip state. Real death-to-respawn runs on all nine stages spend one life and return exactly to the hit anchor. This is separate from the stationary-kill checks.
- Stage8 full natural damage progression now reaches all four forms on Normal/Hard/Furious. Diagnostic durations were274.63/333.07/384.58s with SpaceLaserIII/autoMissilesII, aiming input and immunity except authored grabs. These are not survival results or human clear times. Visible phantom/knight positions now own their collision and Retina targets. All four echoes can be locked; fake hits enrage, real hits damage; submerged phantom has no invisible central hitbox.
- Rival Fight now has five moving missile targets rather than a formation-center target. Its two selected allies obey the ordinary5s roll/7s flip cooldowns. Save, restart, stage exit and fresh-campaign cleanup are checked. Rendering no longer advances allied AI or recharge.
- Generated48 animation frames replace Stage3/4 flat ordnance. Six families per stage, four frames each. Both direct frame inspections and the full bullet renderer use the new XART keys, preserving physics/hitboxes. Enemy-specific authored ordnance stays with its owning encounter renderer.
- Furnace's detached head no longer carries an empty shield gauge after permanently losing that shield. Its core rearm remains intact.
- Review now29 clips,14 solo SFX auditions and9 stage links, all decoded in native Chromium without page/console errors. Includes the Furnace core/head, Stage7 weakened shield and both final gun/laser branches, Stage9 paired Sentinels/fusion, Rival Fight and every configured encounter.16m24s nominal footage; selected starting phases and damage immunity are clearly labeled.

Actual keyboard samples remain small and paused between observations. Normal Warden:29.28simseconds, one front leg destroyed, two deaths to toxic volleys, no clear. Normal Tempest retry:19.80simseconds, real roll/flip with recharging bars, three deaths, no clear. These reinforce the need for a human balance pass, particularly Tempest and the consequences of losing weapon tiers. Physical8BitDo mapping was not available to test; synthetic reload/reconnect checks pass.

No commit/push. The build is ready for review, not certified as balanced across all nine stages. The overnight automation expires at08:00NewYork on September27.


## 08:00 handoff — September 27 overnight cutoff

The final game change was hiding the permanently obsolete Furnace head shield gauge; suite30 afterward passes5351/0 with the final banner and exit0. All13 changed runtime modules pass syntax. No commit or push. The runtime is LF and testsCRLF.

Current review contains29 real Chromium recordings with captured SFX (16m24s nominal),14 sound auditions and two new projectile frame galleries. Every media file and image loads, all9 stage links resolve, and native page/console errors are empty. Review: http://127.0.0.1:8794/_shots/overnight_0927/review.html.

Final actual-keyboard Horizon Normal sample (`manual-horizon-normal/report.json`):31 actions,53.1 simulated seconds with pauses between observations, ordinary collision/lives, selected Cole/SpaceLaserIII/autoMissilesII equipment. No forced kill or damage immunity after the initial2frame grace. BossHP6327→0 by51.1s; two lives lost, including a death during the defeat sequence. Play resumed alive with2 lives at53.1s. Eight manual missiles spent without Retina lock; primary/auto missiles also active, so the total HP loss is not a manual-missile-only damage measurement. All four attacks observed. No page/console errors. This is a paused encounter clear, not a real-time campaign win.

Remaining priorities: Normal Tempest combined attack pressure; Hammer counter/recovery survival with ordinary acquired gear; Warden full module order and post-death weapon-tier recovery; human final-form decisions; uninterrupted1–9 Normal/Hard/Furious progression and actual8BitDo hardware. The review also records remaining legacy art/audio/cinematic auditing. Nothing here certifies every prior creative request complete or all difficulties balanced.

All temporary output is under `_shots/`. Keep existing user work intact. Scheduled work ends at08:00NewYork; further implementation requires Mike's next instruction.
