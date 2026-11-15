---
name: coleforge-beat-em-up-attack-combo-frames
description: Plan, generate, normalize and integrate consistent whole-character 16-bit beat-em-up attacks, combos, jump and running attacks, hitstun, knockdowns, recovery, death and object lifting/throwing. Use with approved identity and the ColeForge walk/run workflow; includes gameplay and sprite-sheet study of Streets of Rage 2, Comix Zone, Final Fight and SNES Maximum Carnage.
---

# ColeForge-Beat Em Up Attack & Combo Frames

## Standing sprite clarity rule

When this work creates, exports, integrates or reviews sprites or raster game art/animation, apply [the ColeForge sprite clarity standard](../coleforge-sprite-clarity/SKILL.md). Blurry or muddy finished frames are not acceptable; use direct master exports and verify the actual animation at its intended game/display size.


Build combat around **complete poses, deliberate holds, visible reach and corresponding victim reactions**. Use `coleforge-walk-run-frames` for identity, body units, registration, palettes and Aseprite export. Read `coleforge-portability` for authored-pixel runtime rules. Never assemble people from body tiles or stamp an unchanged head over combat poses.

## Study before generating

Read [the evidence and version limits](references/classic-reference-study.md). Inspect relevant local sheets and gameplay before a new move family. Record version, character, interval, drawn poses and holds separately. A sheet is a collection of drawings, not a playback clock; a 60 FPS upload is not 60 unique poses. Sheets may include prototypes, unused/custom poses and shared drawings. Do not infer canonical game frame counts from a row alone.

Use references for mechanics, silhouette, spacing and cadence. Draw the project's own character, outfit, props and setting. Preserve the approved face, age, physique and clothing. Natural head turns and partial occlusion are allowed; unexplained costume or facial redesign is not.

## Specify each move

Write intent, facing/camera, native cell/root/body unit, ordered complete poses, duration per pose, startup/active/recovery phases, contact point, root movement/flight gap, hurtbox, active hitbox, hit ID, damage, hitstun/knockback/knockdown, cancel window and allowed successors. See [move patterns](references/move-patterns.md).

Prove a small slice first: jab → cross → finisher, kick, jump attack, running attack, high/low pain, fall/ground/rise/death and lift/carry/throw when needed. Test paired attacker/victim before expanding the roster. Pattern budgets are **design proposals**, not extracted classic-game timings.

## Draw complete combat poses

Use the approved GPT look and proven motion/reference with explicit roles. A coherent sheet of one move with generous fixed cells is acceptable when it preserves identity. Every cell contains a whole figure. Retain raw output, exact prompt and references.

- Punch: load through hips/shoulders, drive the fist to clear full extension, retract. A jab can have minimal anticipation; avoid slow windup on every light hit.
- Kick: chamber knee, pivot supporting foot/hips, extend at the declared height, recoil and plant. Do not lengthen the leg to manufacture reach.
- Uppercut: load low, rotate upward, extend along an ascending path, settle. Taller bounds come from actual arm/body movement with consistent anatomy.
- Jump attack: distinguish takeoff, ascent, airborne extension, descent and landing. Keep world position separate from the drawn pose and support genuine air/landing states.
- Running attack: transition from momentum into a committed lunge/shoulder/kick, then brake and recover. Do not rename a standing attack.
- Keep head, torso and limb dimensions stable. Wider extension bounds and taller airborne bounds are valid. Never fit each pose separately to its alpha box.
- Preserve support-foot/root registration for planted poses and explicit root deltas for lunges. Keep authored flight space. Do not hide bad anatomy with scaling.

Use contact holds and sharp phase changes deliberately. Smoothness does not require equal durations, excessive in-betweens, interpolation, tweened paper limbs or runtime deformation.

## Couple offense to reactions

At contact interrupt vulnerable ordinary movement with the matching pain pose. Contact must agree with the visible fist/foot/weapon. Register one damage event per hit ID; a held drawing must not drain health every tick. Multi-hit moves need deliberate rearming and separate IDs.

Separate high/low pain, hitstun, launch/fall, floor contact, grounded hold, rise and terminal death. Recovery visibly passes through bracing/kneeling/standing. Light hits need not knock down; finishers should read stronger. Killed actors cannot resume AI or rise. Release encounter waits even while visual corpse/debris cleanup continues. Clean up invulnerability, velocity and input state on transitions.

Use explicit combo buffer/cancel windows and successors. Verify mashing cannot restart a contact forever, intended links fit victim hitstun, whiffs recover and dropped input returns to idle. Avoid incidental body shake, perpetual hitstop and unbounded juggles.

## Enemy spacing and UI

Separate locomotion, approach, lane alignment, telegraph, commitment, recovery and retreat. Limited attacking slots, stable flank positions and hysteresis are useful **Elementalist choices inferred from visible spacing**, not claims about the originals' AI source. Avoid all enemies targeting the identical point or circling continuously at touching distance. Give archetypes distinct ranges/reactions while preserving identity.

Group portrait, name, lives and HP tightly for both players using authored bitmap bars/fonts/borders. Where supported show the current target identity/health. Check the actual viewport so HUD does not cover heads/telegraphs. Do not ship reference-game HUD graphics or logos.

## Modular objects and layers

Read [objects and layers](references/objects-and-layers.md). Objects stay separate from complete fighter drawings. Carry poses provide hand anchors, not body-part assembly. Use intact/dented/airborne/break/debris/cleanup states appropriate to the material. One input picks up; one release pose throws once. Hit/death/disconnect/transition releases ownership safely. Both players work independently.

Separate sky, distant skyline, facade/floor, animated objects and foreground. Runtime uses offsets, clipping, frame selection and blits. Glow, flutter, steam, rotation, debris and flashing use authored frames. No arbitrary runtime sprite scaling, rotation, tint/additive glow, alpha fades, shaders or procedural art replacement.

## Export and verify

Preserve fixed native cells, origins, shared model palette, transparent index and integer durations. Added OpenBOR character actions use the existing model palette; separate prop models may have their own. Export editable Aseprite sources with tags and root/hand slices. Ensure full asset rebuild retains the work.

Run `scripts/check_combat_plan.py`, then onion-review and play paired sequences at 1x/2x. Structural checks cannot approve visual quality. Test real input → action → contact → reaction → recovery, interruptions, both facings, both local players, object loss, throw collision, material destruction, cleanup and encounter progression. Preserve backups and installed hashes. Report generated, integrated and verified work distinctly.

For Elementalist's tested command names, palette requirements, handle guards and native obstacle cleanup, read [OpenBOR integration lessons](references/openbor-integration-lessons.md).
## Standing retro reference direction

For Mike's 16-bit and retro work, apply the [standing retro art direction](../coleforge-art-direction/references/retro-art-direction.md) automatically alongside this skill. Choose a coherent source family and inspect/use actual images in generation. Preserve this skill's specific source requirements, current character identity, complete authored poses and project camera. The selected arcade styles now supplement the standing sheet libraries without needing to be named again; exact palettes, proportions and timings still come from the current brief/assets.

## Selected full-recording brawler studies

Use `coleforge-brawler-studies` for the new whole-recording survey of Final Fight arcade, SOR2/3 Genesis, Genesis Maximum Carnage and Comix Zone. This supplements the earlier short/SNES study. Use `coleforge-brawler-hitboxes` for real Elementalist frame delays, cancels and native lane/strike checks, and `coleforge-brawler-grapples` for coupled grabs/slams/body throws. Extra drawings do not require extra startup: allocate holds deliberately.
