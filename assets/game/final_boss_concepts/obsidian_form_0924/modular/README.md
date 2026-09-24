# Final boss — modular first form and alien second form

Mike's 2026-09-24 direction: the blackened gray robot and symbiote fusion is the final boss's first form. Its arms must be separate from the body. The viewer-left claw becomes a circular beam cannon; the viewer-right claw retains its fingers but has a recessed rocket/charge launcher in its palm. After its machine shell breaks, the surviving symbiote and fragments form a more alien second form.

All five PNGs are 1254×1254 transparent RGBA concept art generated with built-in imagegen from the approved `../robot_merge/fusion_black.png` and `../obsidian_alien_face.png` references:

| File | Role |
| --- | --- |
| `form1_assembled.png` | Whole first-form design reference, with dormant weapons and clean shoulder seams. |
| `form1_body.png` | Face, armored body, fixed torso ports, shoulder sockets. No long arms. |
| `form1_beam_arm.png` | Separate viewer-left articulated arm and dormant circular beam emitter. |
| `form1_rocket_arm.png` | Separate viewer-right articulated arm and claw with hexagonal rocket/charge palm. |
| `form2_alien_remnant.png` | Larger organic survivor with the broken horn, armor shards, damaged emitter and launcher remnants embedded in tentacles. |

The prompt for the assembled form preserved the black alien-robot identity and two-arm silhouette, changed the viewer-left claw to a circular beam emitter and the viewer-right palm to a recessed hexagonal launcher, and demanded independent shoulder sockets. The isolation prompts selected only body, beam arm, or rocket arm from that master while making every other part transparent. The second-form prompt made the symbiote roughly three-quarters of the silhouette and limited surviving robot material to embedded fragments. No beam, rocket, muzzle flash, or other attack effect is baked into these plates.

`layout.json` records the body scale/position, shoulder pivots, draw order and weapon emitters. The body isolation came back slightly larger than the arm plates, so its layout transform is needed for their reviewed assembly. Open `preview.html` to switch forms, toggle the three first-form parts, and rotate each arm independently. Chromium review confirmed the assembly, independent arm movement and second form display with all images loaded and no page errors. This art pack is not yet registered as a gameplay encounter.
