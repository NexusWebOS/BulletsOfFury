# Furious Stage 7, 8 and 9 review — October 25

Elapsed MP4 time in the original Oct25 recordings; not the BOSS HUD clock.

All three continuous native Furious recordings inspected in chronological 2-second frame samples, targeted sub-second sequences, and source-owner audit. Cole invulnerability/input aiming enabled: footage does not prove dodge difficulty or player lethality.

Reference inspected: [Raiden II, 02:52](https://youtu.be/1oj6zi1ZfNw?t=172). Its useful motion cues are planted feet, bent-knee recovery, alternating support and a stable body heading. Preserve the Warden's own authored armor and anatomy.

## Stage 7

| MP4 time | Priority / area | Observation and disposition |
|---|---|---|
| 00:33–00:36 | P1 · Gait | Legs swing as rigid plates; toes slide with the chassis instead of planting, pushing, lifting and stepping. **Implemented: four eight-pose leg banks, alternating diagonal support and planted world-space toes; native alpha targets verified.** |
| 00:36–00:43 | P2 · Body rotation | Swipes and gun bracing tilt the entire top-down actor; the feet do not establish a new support stance. This reads as rocking a card. **Implemented: bounded continuous steering; body, native melee tips, guns, projectiles and warnings share one transform.** |
| 00:42–05:08 | P2 · Attack repetition | 21 jump states occupy 79.3 seconds. Dedicated chase/crawl states total only 8.5 seconds, so the spider spends little of this recording visibly walking. **Implemented: walking between groups and fewer automatic swipe-to-jump continuations; native HP and warning windows retained.** |
| 02:14–04:56 | P2 · Damaged stance | After the first front leg breaks at 02:14.7, the chassis leans while the surviving legs keep the same sliding gait. Front pair ends at 03:39.5; rear pair ends at 04:56.3. **Implemented: surviving legs retain the planted gait; destroyed parts remain absent from rendering and native targets.** |
| 05:08–05:51 | P1 · Hit readability | Sustained hits refresh the core white overlay almost continuously, hiding the faceplate and attack detail. HP is still decreasing. **Implemented: visible white hit pulses with authored color returning between sustained-hit pulses; native timers and expiry retained.** |

## Stage 8

| MP4 time | Priority / area | Observation and disposition |
|---|---|---|
| 00:07–02:18 | P2 · Living arena | The organic background reads as a still picture. Existing very slow drift and faint code layers do not make its veins feel alive. **Implemented: moving organic tissue bands, brightness pulses and native code layers on an independent clock.** |
| 00:14–00:16 | P1 · Eye beam | The thin red beam does not fill the red eye aperture. The final socket override uses boss center rather than the visible eye in the current pose. **Implemented: measured eye sockets in all 45 poses and an eight-frame red/white flare covering the eye, rooted to the native animated laser.** |
| 00:17–00:21 | P1 · Claw warnings and shots | Claw FOV starts at a previous pose while shots use the moving raised claws. No distinct claw muzzle flash links each release to the arm. Repeats throughout the first host. **Implemented: raised claw pose, exact shared FOV/muzzle sockets, visible native muzzle flashes and alternating shootable physical rockets/ordinary projectiles.** |
| 01:10–01:44 | P1 · Arm destruction | Destroyed right arm stays attached and darkened at 01:10.3; left arm at 01:44.2. Neither breaks off or shatters. **Implemented per Mike's new approval: arms explode, break away and shatter into actual authored alpha fragments. Native part HP and protected core retained.** |
| 01:44–02:18 | P1 · Ball traversal | Ball movement stops during every horizontal beam tell/fire. Its route clock advances only while moving, leaving much of its four-point route unfinished before recovery. First active movement also jumps to the path start. **Implemented: continuous full-field paths, smooth start, one permanent fold and no stopped horizontal beam cycles.** |
| 01:44–02:18 | P2 · Code bomb pressure | Bombs only appear after every second stopped laser cycle. This yields sparse aimed bombs instead of the requested trail left by a moving ball. **Implemented: regularly dropped native shootable code bombs, four-active cap, 112-unit target spacing and native 1.8-second Furious reaction time.** |
| 00:14–02:17 | P1 · Host hit flash | Whole humanoid/ball becomes a solid white silhouette under repeated shots, masking pose, dead-arm state and attack details. **Implemented: damaged arm/core pixels flash separately; ball pulses retain detail between hits. Native timers are preserved.** |
| 02:18–02:22 | P2 · Falling host explosion | The falling explosion works, but the body produces no recognizable armor fragments moving away from it. **Implemented: preserve the loved falling explosion and supplement it with opaque authored armor fragments; final native destruction also gets fragments.** |
| 02:32–02:44 | P1 · Download transformation | The rebirth resolves into a fully solid held pose before the reveal. There is no visible accumulating data reconstruction or completion beat. **Implemented: actual fusion plate reconstructs in digital scan bands while spinning, shows increasing download completion and settles upright at 100% before native whiteout/reveal.** |
| 02:35–02:44 | P1 · Lightning identity | The alleged lightning is a curved blue pinwheel/ring, including the same shapes in Mike's screenshots. It does not read as branching electrical bolts. **Implemented: inspected authored branching blue bolts replace the rejected wheel in rebirth; exactly 24 accelerating native beats remain.** |
| 03:16–04:16 | P2 · Final form hit readability | White whole-body hit plates also hide the final main form during attack tells. Copied Hammer, helicopter, brain and Volcano forms exhibit the same problem later. **Partly improved: final main plate and Volcano now use readable hit pulses. Hammer, helicopter and brain native hit/effect composition remains a documented follow-up.** |
| 03:23–03:35 | P2 · Effect congestion | Portal, duplicate silhouettes, download helpers, FOV and large pickup labels overlap the main actor. 03:29–03:33 is a clear example. **Visual/readability follow-up; authored final-form attack composition retained in this pass.** |
| 07:50–08:58 | P1 · Volcano visibility | Repeated corner passes leave the Volcano mostly beyond the screen edge while large diagonal FOV fields remain visible. Examples: 07:51, 08:07–08:15, 08:27–08:29 and 08:49–08:59. **Confirmed visually; separate later-form choreography issue, outside Mike's first-host/rebirth redesign.** |
| 09:31–09:33 | P2 · Hammer copy aura | The Hammer copy's red rage aura forms a hard rectangular-looking field around the body at 09:31. It obscures the silhouette. **Confirmed visually; Stage8 copy retains its independent native owner; Stage5 fixes do not automatically apply here.** |

## Stage 9

| MP4 time | Priority / area | Observation and disposition |
|---|---|---|
| 00:03–01:25 | P2 · Twin progress readability | No health display during the entire twins fight. The first disabled sentinel dims but remains present; progress is difficult to judge amid the nebula and supply drops. **Intentional source contract: health appears only after fusion, disabled twins wait at 1 HP. Readability proposal, not a stuck/immortal-boss bug.** |
| 00:27–00:43 | P2 · Projectile contrast | Purple sentinel rounds compete with bright purple nebula branches and glowing supply drops; several shot lanes are hard to read at normal size. **Visual/readability finding; a human dodge test is still needed before making a balance claim.** |
| 01:25–01:27 | P3 · Fusion presentation | Fusion succeeds and both sentinels converge, but supply crates remain in front of the reveal. The center crate competes with the new hull. **Confirmed visually; presentation polish proposal, native fusion logic works.** |
| 01:33–02:15 | P2 · Final-form staging | Tidal Sovereign spends most of its approximately 50-second fight near upper center; volleys change more than body choreography. Pickup labels repeatedly cover the attack field. **Visual/design finding; no evidence of a stalled state machine.** |
| 00:03–01:25 | P3 · Rotated hit overlay | Twin base hull is rotated by w.spin, but its blue hit overlay is drawn axis-aligned in the draw owner. This can create offset edges. **Implemented: native blue overlay now shares hull rotation, fusion scale and disabled opacity; hidden twin HP and fusion rules remain intact.** |

## Interpretation and scope

The protected opening dialogue, portal entrance, symbiote rebirth, final-arena monologue, disabled Stage9 sentinel, hidden twin health and debug boss-mode exit are authored behavior. Do not report them as broken combat. The late bot's occasional missed targeting and weapon pickups are recording conditions. No browser/console or asset failures occurred in the three captures.

Mike explicitly authorized analysis and implementation in this pass. The requested Warden gait and Dracodia first-host/background/ball/rebirth revisions are the implementation scope. Later copied-form choreography and Stage9 presentation proposals remain documented follow-ups.

Original recordings are preserved under `_shots/furious_789_1025/`; the local review includes clickable findings. Implementation and native verification are tracked in `docs/STAGE78_REVIEW_1025.md`.
