# October 9 feedback pass

Mike played the local build and sent the list below. No new art was generated this pass ("hold off
on generations"). Everything is local; nothing was committed or pushed.

Owners: `assets/feedback_1009.js` (combat, HUD copy), `assets/campaign_follow_1009.js` (campaign
map), `index.html` (HUD rows and `fit()`), two authored-data edits in `assets/game.js` (the Stage 1
wave table and the stage-clear hover), and the merge of `origin/claude/sweet-mayer-oaj2q4` into the
local working tree.

Verification: `python _BUILD_SOURCE/probe_feedback_1009.py` (native Chromium, all scenarios) plus
the expansion probes listed below. Screenshots go to `_shots/feedback_1009/`.

## Overdrive expansion

| Request | What changed |
| --- | --- |
| Level 5 missing locally | Level 5 *Museum of Violence* lived only on the cloud branch `claude/sweet-mayer-oaj2q4`. Merged file by file into the local tree, so both sides survived: the local controller rewrite, Retina, pilot select and infantry work, plus the branch's museum, exhibit boss, POW/Mega Crash/four-slot rules, frame pacing and the boss-bar/finale-form layers. Level 5's extra inputs were added to the local input layer: Mega Crash (`G`, or pad Mode+C on foot), leave the vehicle (`O`, or pad Mode+B in a tank), and A–D weapon swap (Tab, mouse wheel, or pad Mode+B on foot). Swapping is limited to Level 5's four-slot mode, so Levels 2–4 still have no weapon swap. The working tree was snapshotted first as `stash@{0}` ("pre-level5-merge safety 1009"). |
| Hide Level 3, don't delete it | `TD.MISSIONS` entry 3 is `hidden:true`. It's removed from the title cards, the selector, and the clear → next chain. The mission, map and art are untouched and still covered by the campaign probe via a fixture. |

Probes: museum 28/28, campaign 29/29 (selector check now asserts Level 3 is skipped), ground 23/23.

## Main game

| Request | Cause found | Fix |
| --- | --- | --- |
| Campaign map should zoom in; HQ → Stage 1 practically on the stage; stay zoomed and follow after a clear | The camera parked on the whole-continent overview once boot finished, and the jet flew in from off the left edge. | The jet starts at Fury HQ until a stage is cleared. The camera follows it at a close zoom, leading toward its destination. After a clear the map opens already zoomed on the jet. The unlock cinematic waits for the jet to reach the new flag, so the ding and unfurl happen in view. Boot, Stage X/Rebel framing, bonus stage, rift return and the progression-bar view keep their own cameras. |
| Stage 1: no boats on land; the ones coming up the coast should be tanks | The land mask was built from whichever image was decoded first and cached forever. The 680×4212 plate is rarely ready on frame one, so boats were placed against the old 800×3616 map, beached on its "land", and slid down over the real jungle (357 on-land samples in one run). | The mask now rebuilds from the plate once it decodes. The two coast markers (map Y 3050 and 2910) are tank files now. Measured on-land boat samples: 357 → 0. |
| Two jets from the left/right edges, half circle down, off the bottom; somersaults, guns, missiles | — | `fb9SwoopPair()` is scheduled at map Y 3130 and 1700. One delta enters from each side, turns onto a southbound heading and dives off the bottom. Both fire machine-gun bursts down the nose. One of the pair loops a somersault; the other fires an unguided missile at the pilot's position. Uses the authored delta plate, rotated. |
| Jumpy enemies jerking around and appearing out of nowhere mid-level | Every single-frame jump over 7 px came from `enemySeparate`: 20 relaxation passes landing the whole correction in one frame, `sepClearAircraft` relocating stuck aircraft, and Stage 1 tanks snapping back to their lane every frame after being shoved. No unit was ever first drawn mid-screen. | Units on screen now have a per-frame separation budget (3.2 px per axis), so contacts glide apart. A shoved tank keeps its new lane. Jumps over 7 px in the same run: ~90 → 0. |
| Stage 1 miniboss: sonic projectiles must not be shootable | Player fire never destroyed an `rzbSonic` orb. It did shoot down the razor missiles the hull launches out of the same green charge glow (27 in a 40 s Furious fight). | Every Razorback round is weapon-proof: no interception, no lock-on target. Dodging is the counterplay. **If you want the missiles shootable again,** delete `rzbMissile=` in `feedback_1009.js`. |
| Furious charge-up red, not green | `rzbSprite` only swaps to the authored `rzbf_` red set for tint `'furious'`, but the charge draw passed `'#ff1838'`. The release flash also used the green sonic palette. | Furious draws `rzbf_sonic_charge` and a red release flash. |
| HUD at the bottom; score bar stays on top; boss bar under it | — | `#hud` is the off-screen drawing surface now, and `player_hud_1008.js` is unchanged. Each frame the 34 px score strip is copied to `#hud-top` above the playfield and the 70 px five-panel housing to `#hud-bot` below it. Boss and miniboss bars stay at the top of the playfield, directly under the score strip. `fit()` splits the same height budget between the two rows and keeps the control-hint strip clear of the bottom row. Visibility and the pause greyscale are mirrored to the new row. |
| Bomber jets that act like bombers | — | On Stage 1, `s1jetbomber` flies a committed straight lane: no guns, no Elite hunting, and no fallback rocket (jetTick's last branch fired for `_atk:'none'`, and its first-frame init zeroed the reload). It drops a stick of bombs, each a shared ground-targeting strike with a floor reticle. **New bomber art is still to be generated.** |
| Jet twisting animations | The evasive barrel roll plays `furyjet_<v>_roll_0..7`. On the black delta those cells jump between unrelated headings. | The Stage 1 evasion keeps its sideways break on the steady nose-south pose. **The roll/turn reels need regenerating** before they can come back. |
| Can still slide during the stage-clear pause | The fly-off hover was deliberately steerable. | `FLYOVER_HOVER_INPUT=false` in `game.js`. The ship holds while STAGE CLEAR types and the music starts, then climbs. |
| Stage 2 miniboss: cold damage doesn't crit or flash blue; bare body too tanky; give the body its own moves | Cold rounds did deal +50%, but `av3ReaverHit` cancels the hull flash and every module flashed a fixed white plate. The modules held 953/2016 HP, so ~1060 was left on the bare core, and its pixel hit test let 34/40 spread rounds through. | Module flashes take the weakness colour (blue for cold, red for fire). When the last module breaks the core is capped at 28% HP, gets a round hitbox (25/30 spread rounds land), and fights on its own: spinning three-arm fire spray, a warned spinning charge that caroms off the edges, and a leap that slams down where the pilot stood and releases a ring of fire. |
| Stage 4 barrels move | Three systems moved them: the catch-all exit push (+0.7 px/frame after 9 s), the entry sweep (up to 4.5 px/frame sideways), and the cached terrain step while the road stood still. | Barrels are pinned to the map spot and lane they were placed on. They're re-seated after movement and again just before drawing, they still block other units, and nothing can shove them. |

## Held for a generation pass
- New Stage 1 bomber art.
- Regenerated Stage 1 jet roll/turn reels (the black delta's are not usable), part of the smooth-animation pass.
