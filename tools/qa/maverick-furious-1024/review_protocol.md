# Maverick / Furious beta playthrough — review protocol

Requested route: full campaign as Maverick; Rebel Fighters at Stage 6; earned Harrier pursuit at Stage X; complete the final boss and ending. Include the optional rift stage if the run earns its entrance.

Tested source baseline: `a5760cb4ab856b2e48f2d3fabc70720a47a86b21` (October 24, 2026). Existing unrelated development files were left untouched. Shipping game files are not modified by the recorder.

## Recording integrity

- Microsoft Edge running the actual `index.html`, native requestAnimationFrame, combat clock, rendering and audio. 1280×720 capture at a requested 30 FPS; actual engine frame timing is measured separately.
- Native HP, modular parts, phases, projectiles, rewards, campaign progression and ending. No forced damage, kill commands, speed changes, granted equipment or unlimited ammunition.
- Review-only controller observes currently exposed targets and ammunition, reacts after 220 ms, and writes ordinary game Input keys. Menu navigation uses CDP keyboard input and earned native map actions. This is automated play, not evidence of physical controller operation or a human skill clear.
- Initial attempt without immunity. After a native player death, enable the existing DBGT God mode as Mike authorized. Record the activation time and all subsequent contact attempts. These are repeated overlap samples, not independent deaths a human necessarily would suffer.
- While invulnerable, favor the southern playfield, align horizontally with visible targets, use native Retina/manual missiles and charge, and collect reachable native pickups. Do not manufacture upgrades.
- Preserve naturally timed protected cinematics. Show results, unlocks and between-stage screens before continuing. The recorder may make an ordinary menu selection directly; it cannot unlock unearned stages.
- Stream the original WebM to disk. Encode a seekable H.264/AAC MP4 at normal speed. No synthetic combat, animation interpolation or secretly removed defeats.

## Review lenses

1. Progression correctness: stage entrance, actual victory, route choice, modular defeat, reward once, menu handoff, final ending.
2. Challenge: threat distribution at the south edge, warning-to-impact time, committed attacks, movement demand and long no-progress intervals. Immunity limits conclusions about fair human clear rate.
3. Combat and balance: damage reach, protected parts, ordinary weapons versus missile dependence, resource recovery, Maverick-specific progression and phase duration.
4. Art and motion: fixed pivots, armor/hammer identity, readable windup/recoil/recovery, emitter attachment, hit states, deaths, parallax seams and cinematic identities.
5. Readability: hostile bullets against backgrounds, overlapping FOV/reticles/effects, radio occlusion, bitmap text fitting and information hierarchy.
6. Bugs and performance: native page/console exceptions, failed assets, missing finite geometry, prolonged stalls, recorded frame-time distribution and capture overhead.
7. Audio: verify decoded audio at opening, regular combat, bosses and ending; report capture failures separately from game sound failures.

## Finding standard

Each confirmed finding includes timestamp, player-visible symptom, reproduction context, severity, likely owner and a measurable acceptance check. Design concerns and untested hypotheses are labeled separately. Priorities favor progression/damage correctness, then threat readability and pacing, then art continuity, then optional polish. No blanket art regeneration or paid generation is part of this review.

Skills applied: ColeForge workflow, portability, playtest/release, shmup design, boss design, enemy AI and art direction; Game Studio playtest; design-game-verification, design-game-balance and design-hud-readouts. Generic recipes remain subordinate to BOF's authored sprite and warning contracts.
