# Debrief screen and HQ scenes — full-size renders (0905)

Mike: *"Upload the new debriefing scene/stat screen full size images to the github please."*

All six are straight captures out of `_BUILD_SOURCE/shoot.py` at native size — no crop, no scaling,
no compositing after the fact. They were re-rendered from the tree at `aa786703`, so they include
both this session's work and the main-PC session's stage-3 and cutscene pass. Re-encoded once,
losslessly, at `optimize=True` (10.31 MB → 6.70 MB, pixels verified identical).

## The stat screen — 960×1152

Mike's own `statpanel_cf` plate with every bay measured off the art, the six stats on their authored
fills, and SCORE / CLEAR TIME / RANK sharing the wide bar with dividers on the midpoints between the
three column centres.

| file | what it shows |
|---|---|
| `statscreen_stage3_ice.png` | stage 3 — the glacier-ice face, the brightest in the pack |
| `statscreen_stage2_lava.png` | stage 2 — blackened basalt, the DARKEST face, on the darkened fills |
| `statscreen_stage6_aviation.png` | stage 6 — aviation enamel |

Three stages rather than one on purpose: the debrief is lettered in the face of the stage you just
cleared, and those faces run from 71 to 235 in 75th-percentile glyph luminance — a 3.3× spread. One
screenshot proves the layout; three prove it survives the range. Stage 2 is the hard case, and it is
the one to look at if the type ever needs revisiting.

Also visible here: the label is the stage face and the VALUE is the pack's FINAL LEVEL face (ivory
and old gold, the one cut that belongs to no stage), the 1px black edge on the stat-bar lettering,
the synthesised `=` built from the face's own hyphen, and the `:` in the clear time built the same
way from its period.

## The HQ scenes — 1280×1152

The ensemble briefings, each in one of the seven authored interiors rather than all eight on the
same command deck. The cast is composed into these plates, so no portraits are drawn over them —
only the speaker's name survives, and it is the only cue to who is talking.

| file | scene | room |
|---|---|---|
| `hq_all_00_division_lounge.png` | Nine Chairs, Eight Names | full division lounge |
| `hq_all_01_command_table.png` | Trust Is a Weapon | command table |
| `hq_all_03_prototype_lab.png` | The Man Behind the Door | restricted prototype lab |

⚠ The room-to-scene mapping in `HQ_ROOM` is a reading of the scripts, not a decision Mike has made.
These three are the clearest cases — the opening assembly, the accusation scene at the table, and
Decker's vault reveal in the lab — and the table is one line each to re-order.
