# Accepted Elementalist process

Mike explicitly accepted the resulting movement on 2026-11-05 and asked to save this workflow as a critical ColeForge skill. This approval covers the whole-character walk/run method and the installed 18-character movement pass, not every future draft.

## Recoverable project evidence

Original project: `Elementalist` (locate its checkout on this PC). The historical working directory was `C:/Users/Mike/Desktop/Github Coding/Elementalist`; it is provenance, not a required installation path. Set `ASEPRITE_EXE` to the local editor executable or put `aseprite` on PATH before running the recovery pipeline.

- `openbor/source/fullframe-v4/`: raw coherent cycle drawings, exact `*-generation.json` prompts, quality references, normalized `native/<character>/{walk,run}.{png,json,aseprite}`, root recipes, unit measurements and integration checks.
- `openbor/tools/build_fullframe_locomotion.py`: tested authoring/integration pipeline. A recovery snapshot is bundled in `assets/elementalist-tools/`; it belongs in the project's `openbor/tools/` folder and requires that project's source inventory. It is not a generic script to run directly inside this skill.
- `openbor/tools/export_animation.lua`: complete-frame Aseprite construction, millisecond timing, fixed-cell cels and origin slice.
- `openbor/tools/test_locomotion.py`: real-engine coverage of all 36 clips and 288 frames.
- `openbor/tools/test_pursuit.py`, `data/scripts/locomotion.c`: actual enemy chase/run and short-range walking transition. The test forces a chase choice; production retains wandering.
- `MOVEMENT_REVIEW.html`, `movement-previews/`, `Movement-GIFs.zip`: accepted integrated movement previews.
- `openbor/source/fullframe-v4/installation.json`: verified installation and backup record.

The completed pass had 36 Aseprite pixel/timing round trips and 75 native assertions, including both player arrangements, post-defeat progression, all nine guided encounters and pursuit. Guided fixtures do not establish combat balance or online/controller quality.

## The motion inputs that worked

SpriteCook walk job `ad0b252f-8cf9-466e-9924-37c36d5cb8fa`, result asset `073ec761-a913-44ff-ae34-8552ce2294eb`: eight frames, 126-by-126 source cells, 125 ms each, source root (66,126).

SpriteCook run job `7331c0fd-db3f-4095-b690-81b6b4eca024`, result asset `c543c45e-0706-4b0e-97d4-e425fffa76ff`: eight frames, 116-by-116 cells, 125 ms each, source root (64,116). Frames 4 and 8 have 4 px and 2 px floor gaps.

These two owned cycles were reused for the remaining roster with **no new SpriteCook jobs**. Some earlier six-frame enemy ZIPs were inspected but retained matte or weak motion. Their mere existence was not evidence they should be used instead of the validated guide.

Motion plates use complete figures on 192-by-192 native canvases, uniformly enlarged 2x into 384-square guide cells. Target grid: 4 columns, 2 rows, nominal 1536-by-768. Actual GPT output was often 1774-by-887. Normalize the entire canvas uniformly before slicing.

## Look and scale

Each fighter's full GPT identity reference supplied face, outfit and anatomy. Tyler's richer newly generated walk served as rendering-quality guidance, not as another enemy's identity. Run generation included the same character's new walk to preserve materials and proportions between cycles.

Keep Tyler youthful, with visible eyes, messy black hair and his closed black shirt; the approved design reads as a young college entrant. Keep Damien's Black identity, backwards cap, denim jacket, goth shirt/jeans, chain, gloves and boots. All other identities remain defined by their own approved references.

Standing units measured from the current native idles were Tyler 128, Damien 130, Harker 126; most enemies 126; Viper/Shiv 110; Bat Punk 105. Do not replace this with the older generic 128-pixel convention. Fire Boss's previous walk was much larger than his idle; the new bank was calibrated to his actual standing unit.

The pipeline uniformly calibrated whole action sheets to a shared body unit and translated complete frames for root registration. Run projection used the measured guide ratio 116/126. These calibrations did not resize individual poses. The 192-square export cell with root (96,167) provided full stride/weapon margins.

## Failures to avoid repeating

- Assembled body-part kits and an offline cutout rig were rejected. `source/modular-v3` is abandoned; never revive those character-part banks for this task.
- Independent pose invention lost the proven gait and changed faces and proportions.
- A motion guide's coat tails leaked into Viper/Shiv's first run renderings. Targeted whole-cycle corrections removed the invented cloth.
- Generated alpha sometimes retained pale backgrounds well above alpha 128. Thresholding alone was insufficient; exterior-connected cleanup was required.
- A palette made only for new walk/run frames was unsuitable for OpenBOR's model-wide palette use. Native reindexing preserved colors across actions.
- Body-alpha bounds are not anatomical measurements: crouches, stride extension, flame tongues and hair can change bounds. Compare anatomy, not just min/max height.
- The native AI could hold RUN all the way into attack range. A small on-move transition restored walking within 140 px on the same lane, with hysteresis against the native 150 px run trigger. Do not assume the same thresholds fit another game's scale.
