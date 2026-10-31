# Dracodia articulated claws and double jumping strike — October31

Mike requested the windup/jump/alternating strike rhythm of Nick Bruiser at30–33s in https://youtu.be/Tvof46gpSbY?t=28, translated into Dracodia's physical claws. The actual reference interval was inspected at eight samples per second. Its low preparation, tucked ascent and distinct alternating strikes inform the timing; no reference-game pixels or audio are used in BOF.

## Authored anatomy

236 poses retain the approved Dracodia skull, chrome-violet armor, red cables and crescent blades. Fixed shoulder plates plus separately posed upper arms, forearms and claw assemblies provide the reach; shoulder/elbow/wrist rotations, small torso banks and perspective sizes are baked offline. The source part pixels come from the existing approved `colossus_scythe` bank, with source hashes retained. Small detached fragments created by segmentation are excluded during authoring. No new paid generation was used; Mike explicitly allowed authored rotations for these arms.

All poses restore one768x640 logical canvas and chest pivot(384,320), with one410px body unit. Six normal2048px pages and six exact-alpha white-hit pages hold708 disjoint modular part entries with even crops. Metadata restores the full canvas, current opaque Retina anchor, source-alpha spans, live claw spans, break points and all articulated joint positions. Four actual swept-claw footprints each have authored green/yellow/red warning plates. Runtime rendering selects source rectangles and positions them without sprite rotation, rescaling, glow, alpha animation or compositing.

The actual layered `extended-claws.aseprite` has left/core/right layers,236 frames, eight pose tags, a chest-root slice and nominal Furious phase timings. Normal/Hard use their explicit longer warning durations. Editable source: `_ART_SOURCES/dracodia_extended_claws_1031/extended-claws.aseprite`. Owning rebuild: `_BUILD_SOURCE/build_dracodia_extended_claws_1031.py`. Frame/alpha/socket manifest: `assets/game/levels/stage_08/boss/extended_claws_1031/manifest.json`. The source-preserving offline builder requires Pillow, NumPy and the installed Aseprite; it performs no API requests.

## Native attack book

RD88 replaces the prior RD77 physical combo only. The surviving-armed final main body coils, rakes from one edge toward the center, retracts and rakes from the opposite side, retreats into the background, leaves north, jumps back into the foreground and delivers two alternating claw strikes before recovering. The next combo reverses the side order; a single surviving arm supplies both legal strikes. The first host, all four copies, native life pools, main-life/copy transitions, arena returns and terminal destruction keep their existing owners.

| Phase | Furious timing | Counter |
|---|---:|---|
| Coiled guard/positioning |0.50s|Read the first flank|
| Each side rake |0.95s tell,0.30s strike,0.32s retract|Leave the actual swept blade field|
| Retreat, distant hold, northward leap, approach |0.65/0.30/0.25/0.38s|Read the fixed ground landing mark|
| First jumping strike |0.55s tell,0.28s strike,0.16s retract|Move clear of its committed footprint|
| Second jumping strike |0.62s tell,0.28s strike,0.16s retract|Evade the opposite claw|
| Moving recovery |0.85s, then0.85s native cooldown|Attack or reposition outside the returning hull|

Normal and Hard side tells are1.15s and1.05s; second-jump tells are0.72s. Both jump strikes appear on every difficulty as requested. Body/landing targets commit before the attack; no future player input is read. Actual alpha of the visible claw, including traversed pose frames, owns contact. The non-attacking hull does not become an invisible slash. Native playerHit owns death, armor, roll/somersault protection and GOD behavior. Ground impacts are presentation; they add no hidden radial damage or bullets.

Depth below85% and the offscreen jump are protected and excluded from Retina. Foreground native damage, white hit feedback and part HP remain. A real claw break removes its whole displayed module, target, warning and contact immediately. Both claws gone restore the original exposed-core missiles. The existing third-decision Luminaire schedule remains. Pause and retry clear/freeze the correct state; native death/rewards are not replaced.

Sweep FOV appears under the body; ground Retinas and the existing metal warning sign render above it. Warning audio, charge, slice, jump and ground-contact cues use the shared mixer/retrigger gates. No music replacement or ordinary-projectile interception change was introduced.

## Verification and limits

82 native checks cover both orders and all three difficulty settings, native3380/4290/5330HP, immutable target marks, current opaque anchors, background protection, both rakes and both jump strikes, real non-GOD alpha-contact death, hit timers, actual claw destruction/cancellation, surviving-arm selection, exposed core, pause/resume, Luminaire, copy ownership and retry. Six additional input-driven runs survive the whole combo by flying to an upper flank without GOD, armor, roll or somersault. The simple straight-north route was rejected because remaining in the returning hull is unsafe; the verified route also clears its recovery.

Source checks verify every exported crop against its full-cell source, hit alpha equality, even geometry, actual opaque targets, fixed roots, complete warning colors, layered source and absence of prohibited runtime transforms. Core SHA256 remains `024a0933c5729b6afa2a6e88864574636293bdb535d9f4e5eb91d36bb98509de`.

Required core syntax check passes. The completed full suite retains exit1 and the same five pre-existing assertions: held hit flash; opening-jump closing dialogue; jump return before Chromium; opposite unchosen StageX route; StageX right-branch full encounter. No new core edits or test-baseline changes were made. The exact output and check names are in the archived proof folder.

The fresh native recording is a full-health final-main-life checkpoint with preceding lives cleared before filming, not a whole-game playthrough. Its first22s withhold player fire to expose the animation. Thereafter an invulnerable input-only pilot uses the normal weapons. No recorder health, phase or clock edits occur during capture. Recorded duration, native performance, decoded audio and preview verification are in `DRACODIA_EXTENDED_CLAWS_1031_MEDIA.json`.

Current local review: http://127.0.0.1:51046/?dracodia=extended-claws-1031#clip=stage8-dracodia-ninja-combo

No Git commit or push was requested or performed. Old source banks and recordings remain available; only the current main-body combo preview is superseded.

## Final media results

The full final-main-life recording lasts109.683s, with native5330HP defeated at102.607s. Native game rate averages54.33frames/s. Decoded recorded audio mean−21.8dB, peak−6.1dB; real playback includes13 charge,32 slice,8 jump and15 ground-contact cues. No browser/game/asset/audio-tap errors. Three gallery entries load and play1280x800 footage; the prior combo URL now resolves to the new movie. The first22s are unobstructed by player fire.

99 focused native/input/source checks pass, plus three preview playback checks. The full regression suite retains only the five recorded baseline failures. No non-GOD whole-fight balance claim is made; the six no-GOD checks establish a movement escape through both combo orders on each difficulty. Old clips remain archived.
