# Whole-character hammer attack correction — November 10, 2026

Mike rejected the body-and-weapon assembly. Stage5 Chronos and Stage8's copied Chronos now select complete GPT-generated character-and-held-hammer drawings for their overhead windup, downstroke, compression, recovery and left/right sweeps. Matching generated empty-handed release/guard/receive poses keep the body unit consistent during actual thrown flight. Regular, chromium and copied red/rage materials share the new complete drawings.

The blue cylindrical T-hammer and purple six-spiked T-hammer were supplied as identity references, never pasted onto the new actors. Both hands, arms, torso and held weapon are drawn together. Whole-source registration, complete-pose mirroring and offline whole-frame material derivatives are the only normalization steps. No head stamping or separately transformed held weapon is used.

## Production ownership

- `assets/rigid_hammer_art_1110.js` now registers the new whole-frame banks; its historical filename does not indicate held-weapon assembly.
- `assets/boss_animation_1109.js` handles measured640×640 cells, whole alpha masks, end-face impact landmarks, landed root positions and the original difficulty contact sequence.
- `assets/whole_hammer_1110.js` keeps ordinary held weapons inside the actor's silhouette, removes the copied held hammer's separate target, and activates separate weapon rendering/deflection only after real release. Chronos's pre-existing charging counter aperture is retained within the whole actor.
- Released weapons retain their existing approved canonical spin art, missile-only reversal and native flight timing. Their release and catch positions now match the new full drawings. Native HP, white real-hit flashes, depth vulnerability, audio, deaths/rewards and campaign progression remain with their original owners. The explicitly approved modular chaingun is retained.
- Normal: one down strike. Hard: two down strikes. Furious: two down strikes then left/right sweeps. One initial jump, planted follow-ups.

## Source and export evidence

Built-in GPT image generation; exact prompts, source IDs and approved references are saved in `_ART_SOURCES/whole_hammer_1110/source-index.json`. Rejected axial-club and clipped-fingertip outputs were excluded from production and the accepted-source archive.

56 distinct complete source drawings feed six held-attack and two empty-handed16-cell timelines:128 timeline cells, including intentional holds and complete-pose mirrors.40 lossless material textures. Even640×640 cells; common320,320 pivot and474px boot baseline. All held banks and Chronos empty hands use one0.63 source scale; the more padded Dracodia empty-hand source uses one0.75 scale. No per-pose auto-fit/upscaling.

All eight editable Aseprite files contain exactly one whole-figure layer and16 frames. Their exported pixels match the regular production sheets exactly. All56 used source crops and128 normalized cells were checked for clipping; no edge crossings remain. See `docs/qa/whole_hammer_sources_1110.json` and `whole_hammer_bounds_1110.json`.

## Native verification

38/38 native Chromium combat checks passed with no page/renderer errors: Normal/Hard/Furious contacts, planted roots, real white-hit pixels and new pose selection for both regular/chromium actors and the copied red material.

Both extra whole-actor/released-weapon contracts passed. Held Chronos has no independent hammer target/interceptor; copied Chronos exposes only the core actor and draws no separate held tool. The visible hammer belongs to the complete actor alpha mask. After release, separate targeting and rendering become active and the body switches to its matching generated empty-handed bank. Measured release errors are below0.000001px; native catch destination error is0px for Chronos and below0.001px for the copied form. No native HP or progression shortcuts were installed.

The previews use actual live RAF/native engine drawing and the game's audio mixer with a labelled invulnerable observer who holds fire. They trigger native Furious attack checkpoints to demonstrate regular, chromium and released-flight chapters; they are not full-fight/win recordings. Sound was decoded and recorded; both native mixes had nonzero peaks around0.70. These observations do not establish a whole-campaign performance result.

- [Chronos native preview](../_shots/whole_hammer_1110/chronos-hammer.mp4)
- [Dracodia native preview](../_shots/whole_hammer_1110/dracodia-hammer.mp4)
- [Chronos animated excerpt](../_shots/whole_hammer_1110/chronos-hammer.gif)
- [Dracodia animated excerpt](../_shots/whole_hammer_1110/dracodia-hammer.gif)

Syntax checks passed. The full suite was run and exited1 on the existing `ReferenceError: difficultyHealthBaseline15 is not defined` at `assets/combat_polish_0927b.js:151` / `_BUILD_SOURCE/test_fl.js:4537`. It did not reach its final summary. Full log: `docs/qa/whole_hammer_full_suite_1110.txt`; this is not a full-suite-green result.

Core `assets/game.js` remains SHA256 `b46bb789b6344f31d0ecba126169447d491152670c09decc6da624bc4b5d2215`. Other cinematic work and script order were preserved. No installer, ZIP, commit or push was requested or performed.

## Rebuild handoff

Accepted raw sources/prompts, references, single-layer Aseprite projects and the source normalizer live in `_ART_SOURCES/whole_hammer_1110/`. Runtime installer snapshots and native verification/recording fixtures live in `_BUILD_SOURCE/whole_hammer_1110/`. Those fixtures are not included by the game's index.

This correction supersedes the held-attack portions of `rigid_hammer_1110` and `hammer_face_1110`. Never run those older body/prop assembly builders over these banks. Preserve their canonical detached spin art. The current installer checks for concurrent boss-animation owner changes before writing.
