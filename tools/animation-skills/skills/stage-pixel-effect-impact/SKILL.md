---
name: stage-pixel-effect-impact
description: Stage cleaned pixel effect animations with registered playback, impact timing, smoke holds and environment response; includes the creator Godot reference and authored-sprite adaptations.
---

# Stage pixel effect impact

Read [references/godot-reference.md](references/godot-reference.md) for the creator's exact scene behaviour and controls. `assets/godot` is an unmodified MIT reference project from Kasperzack Games at revision d25ce128ac5f2487e8187d0f1c6f4ac27dced599, not an already approved ColeForge implementation. Copy it into a workspace before experimenting. Its source and shaders use procedural drawing, runtime blend/dissolve and tint techniques; preserve the target project's rendering rules when adapting.

First prove the cleaned sheet alone. Read actual JSON durations, rects and local anchor; place world position minus anchor, respecting native fixed cells. 80 ms/frame is 12.5 fps, independent of simulation rate. Keep integer display scaling, nearest filtering and integer camera offsets. Empty/absent frame tags must be handled safely. A one-shot should finish, not automatically loop a white flash. Test overlapping instances and cleanup.

Layer impact responses one at a time and compare:

- Schedule flash, shake and debris against the selected impact frame. The video shows a 40% single flash and whole-pixel shake. Expose flash/shake reduction through the project's existing settings.
- Add authored rock flight drawings/positions with landing/bounce, a persistent authored scorch sprite, and ember frames. Do not substitute new code-drawn art in authored-only projects.
- Hold the fullest smoke drawing about 1.8 s and continue a deliberate drift/dissipation tail. For authored-only projects use drawn erosion/fade frames, not a dissolve shader or runtime alpha fade. The reference replaces part of its original smoke timeline; do not assume it plays all 16 frames unchanged.
- Time the fixed-location lit background variant to visible fire intensity. Bake transition variants offline if runtime blending is outside the project's contract. Preserve dark sky and distant areas.
- The linked fight also mentions 4–6 simulation frames of hit-stop at 60 Hz and two black/white impact frames. Those are separate fight-scene techniques, absent from the bundled explosion project; add only when useful to the current brief. Keep collision events and damage independent of visual repeats.

The reference uses a 320x180 viewport displayed at 1280x720, pixel snapping and Compatibility rendering. Run a copied project with the available Godot executable and verify actual import, play, trigger/retrigger, disabled flash, ground contact, smoke tail and light location. If Godot is unavailable, report source inspection separately from runtime verification.

Retain raw/generated/cleaned/integrated/played statuses distinctly. An AI prompt produces the main animation; code in the reference supplies the extra effects and presentation. Do not imply one prompt authored the entire fight.

Source: [creator kit](https://github.com/kasperzackgames/chatgpt-pixel-effects), MIT; LICENSE included. For assets use sibling `clean-pixel-effect-gifs`; for fixed background variants use `paint-pixel-background-relighting`.
