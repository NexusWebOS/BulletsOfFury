# Targeted boss, finishing-effect and Cole performance pass — October 20

Completed local integration of two selected weapon banks across three older encounters, three distinct player terminal effects, and Cole-only reporting/alarm animation. Hammer, Phoenix and Dracodia form animation banks are unchanged. Other pilots remain unchanged pending Mike's review of Cole's likeness in motion.

## Audit and selection

Inspected 17 older native encounters for 36 simulated seconds each, with half-HP phases in the second half. Protected fixture/player; this is visual/behavior QA, not a human survival-rate measurement. Sources, contact sheets and actual blit keys: `_shots/performance_finish_1020/audit/report.json`. Initial observer was corrected to avoid double drawing before the final census.

- razorback: Retained: authored turret/tread motion and clear weapon cues.
- damkeeper: Retained: distinct assault/weapon choreography and existing recoil cues.
- magmaward: Retained: distinct magma windups, release and recovery.
- infernoreaver: Retained: authored modular/elemental phase motion.
- frostcruiser: Retained: recent rotating shoulder and reactor/laser animation.
- cryospear: Retained: recent cryogenic banks and physical weapon cues.
- olivewarden: Retained: recent claw/leg banks and rotary cannon.
- stormsovereign: Retained: recent core lightning and modular weapons.
- siegebomber: UPGRADED: both laser cannon sockets now charge, retract/recoil and recover on the current Hard Corps director.
- siegefortress17: UPGRADED: six carrier turret sockets gain a generated charge/recoil/recovery bank.
- warhive: UPGRADED: same turret bank at this carrier's original sockets, retaining its aiming/warnings.
- rebelsquad: Retained: existing individual fighter attack/roll/destruction banks.
- dualscoopdredger: Retained: authored scoop/launcher motion and clear warning beats.
- sludgeemperor: Retained: authored claw/weapon phase movement.
- heralddeath: Retained: current threat-specific windups/release effects; opaque modular hulls.
- voidhorizon: Retained: current sentinel phase cues; avoid unnecessary replacement art.
- tidalfusion: Retained: current tidal weapon/phase choreography.

## Weapon changes

The Eclipse bomber's two cannon sockets follow each actual `hc-lances`/`hc-strafe` line's delayed warning/release and current recovery state. The shared carrier turret bank serves the Stage 6 cargo miniboss and Warhive carrier. Source mounts, warning lines, beam collisions, damage, sound calls, durations and difficulty books remain with their original owners. Native white hit flashes and timer expiry are retained. Dead pieces use their original opaque wreck/removal path, and no new animated ghost survives.

The generated fire frames included unwanted baked beams; those frames are excluded, retaining clean physical recoil poses while the native beam and muzzle remain authoritative. Consequently the delivered 16-slot banks have 13 and 12 unique source poses, including deliberate idle-return/recovery reuse; these are not claimed as 16 unique motion drawings. Even fixed canvases: carrier160x192/pivot80,76; bomber104x240/pivot52,120. One common scale per bank. Carrier main-boss socket offset preserves its original q.y-22 placement; miniboss retains its own60px source socket.

## Player terminal effects

- Laser: cyan/white ablation sweep and motes consume the actual captured aircraft. Object-based carrier/Harrier laser damage sources and the real committed bomber lance are classified correctly.
- Ice: the original short freeze shell fractures into the new PixelLab shard bank plus 12 irregular Voronoi regions of the actual aircraft, replacing rectangular tile chunks. Some ships occupy11 of the12 regions. Alpha coverage is conserved once; native canvas premultiplication introduces at most one rendered color level of rounding.
- Dark: gray/white/purple inward collapse and actual aircraft fragments, used for evil chromium/void well/shadow impacts and the shadow-ball erasure. The existing giant approaching shadow ball and victim scale-up remain. The already separate legacy darkVoid cinematic retains its owner.

Gray matte contamination was removed only from the laser/ice effect art. Final blank effect frames are intentional. Each bank has16 fixed256-square cells/pivot128. The native death/life/respawn timing, iframe/shield protection and ordinary burn/spin death remain. Existing approved mixer cues `slice`, `expIce`, `shadowRelease` play once at transition. The newly verified reset cleanup releases contextual effect canvases on respawn for either seat.

## Cole performance and likeness gate

Four PixelLab banks:16 reporting eyelid/lip poses,16 horrified eyelid/lip poses,24 reporting hand/breath poses and24 alarm/flinch/breath poses. Original full-resolution hair, nose, outer jaw/beard silhouette and lower-body pixels remain authoritative; generated face animation is restricted to small eye/mouth windows. Body motion uses a shared shoulder-to-waist band with common boundary matching. Confirmed red matte debris beside the old source legs was cleaned. Reporting now reads the actual512x1024 full-body source; the old704-row crop hid the feet. The squad shot retains the closer704-row framing to match the eight unchanged pilot poses. The alarm uses an initial flinch followed by restrained breath/hand motion and occasional blinking, rather than repeatedly jumping in shock.

Mike explicitly approved sending existing Cole pixel artwork and selected BOF boss/effect references to PixelLab. No original photos were uploaded. Four Cole banks are ready for review; **do not batch-generate the other eight pilots until Mike accepts Cole's likeness in motion**. This review gate is Mike's requested sequence, not a new permission requirement.

## Asset/loading ownership

`build_performance_1020.py` owns all nine equal-cell lossless WebP atlases, cell/pivot registry and source export ledger.2px extrusion/gutters, no per-frame fitting. Game assets live under their owning Stage5/Stage6, shared player-FX and Cole body-frame folders. Effects lazy-warm with stages; selected weapons load only in Stage5/6; Cole performance loads with ending assets. No new animation loop or per-frame readback. Shard masks are built once per contextual death, then released at reset.

Runtime: `assets/performance_finish_1020.js` and generated art registry, loaded last; only existing file render edit is the narrow carrier turret hook in `stage6_roster_1017.js`. Core game, full test harness and Command UI files are byte-identical to the starting checkpoint. Sources/jobs/prompts/authorizations/receipts are preserved in `_ART_SOURCES/performance_finish_1020`.

## Final verification

75 focused native Edge checks pass, zero browser errors. Includes all four difficulties/three encounters, damaged pixels and expiry, cancelled launchers/no ghosts, all nine actual aircraft and all nine Furyship palettes, protected maneuvers, exactly one life per native respawn, co-op effect/memory isolation, pause clocks and decoded audible transition playback. Full suite:8,940 passing/0errors/exit0. Syntax clean.160 delivered animation slots across9 banks; total new runtime 1,033,324bytes. PixelLab charge$0.3528 plus2 daily generations; remaining display$0.58. No additional generation needed.

Review: `_shots/performance_finish_1020/review.html`. Native capture movies show the actual game rendering. The older audit fixtures, selected-bank frame sheets, source receipts and machine-readable reports are linked there. No GitHub push requested or performed.
