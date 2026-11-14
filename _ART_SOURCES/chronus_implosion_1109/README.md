# Chronus death — aura and chromium implosion

The current native Stage 5 ending was captured as a before GIF, then its fire/terminal visual progression was revised with the saved prompt-pixel-effect-animations workflow. New image-generation sheets supply a sustained hollow fire aura and a white/silver/blue chromium-flame expansion followed by inward collapse. The original boss plate remains unchanged.

The new animation was captured from the actual Chromium game renderer using the current game's final-defeat checkpoint, native core shot, impact, two-second ignition and ending owner. This is a defeat-checkpoint capture, not a whole-fight playthrough. Temporary previews overlaid only the changed native functions and loaded the real authored PNG frames; no Python mock of the game scene was used.

Timing: native pulse/lock/missile and one core impact remain; the body-hugging aura loops during the native two-second engulf phase, then a 16-pose chromium flame effect surges outward and collapses into the measured core. The terminal hold is shortened to 2.35 seconds. Outward follow-up fireworks and moving armor fragments are superseded for this ending by Mike's requested implosion. The existing after/cutaway, Earth approach, dialogue and reward owners remain.

Source file: assets/hammer_finale_1017.js. New assets: assets/game/levels/stage_05/boss/chronus_implosion_1109/. All 32 frames have even fixed canvases and fixed pivots. Aura: 320x320, pivot160,160. Implosion: authored larger640x640 size bank, pivot320,320. Both use one38-colour shared palette and binary transparency. The larger bank is a direct nearest-neighbour derivative of the native generation crops, not additional generated detail. The build preserves raw lossless sheets and does not shrink/enlarge an intermediate sprite. Runtime uses integer source-over blits without a new rotation, tint, shader or alpha fade.

Generation used built-in imagegen with the actual defeated-boss plate and the captured old fire/explosion as references. Exact prompts, source master sheets, native strips, effect previews, frame manifest and native capture records are included. Cleanup reused the saved skill's pixelcore key/despill/shared-palette steps at native size, without downscaling these larger effect sources. The implosion reference was revised once for padding. Every contraction pose is authored in the sheet; runtime does not scale a single picture inward.

Verified in the native preview: pulse→lock→missile→engulf→burst→after; exactly one core-impact event and one chromium-implosion; no captured page errors. The source plate/core coordinates remain fixed. Opaque-pixel area falls from25,819 at peak to1,531 in the compact inward knot, then179 at the final blue ember and zero in the final two cells. The aura has sixteen distinct sustained frames. Visual checkpoints cover the aura, massive peak and inward tail.

The prior source file is retained with the candidate build for rollback. No commit, push, installer or external publishing is part of this change.

Cleanup code credit: Kasperzack Games, MIT, https://github.com/kasperzackgames/chatgpt-pixel-effects at d25ce128ac5f2487e8187d0f1c6f4ac27dced599. Reference art belongs to Mike's BOF project; that code license does not relicense the reference art.
