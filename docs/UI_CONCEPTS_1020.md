> UPDATE: Mike selected A/Command Armor for both HUD and dialogue. Production implementation and all pilot/expansion templates are complete; see [UI_PRODUCTION_1020.md](UI_PRODUCTION_1020.md). Older pending-selection text below is historical.

# Dialogue / HUD concept choices and Dracodia portrait — October 20

Mike rejected the current cinematic dialogue windows and requested generated
choices, a clearer HUD with the listed information grouped on opposite sides,
and a proper Dracodia dialogue portrait.

All seven images were generated with the built-in **image_gen** tool. No
PixelLab credits were used for this concept pass. Actual current Cole portrait,
ship, gameplay screen and Dracodia head/body were exported through the native
XART/drawImage route as identity references. Generation prompts and source paths:
[`prompts.json`](../_ART_SOURCES/ui_concepts_1020/prompts.json).

Review: http://127.0.0.1:8794/docs/previews/ui_concepts_1020/index.html

| Choice | Dialogue window | HUD |
|---|---|---|
|A · Command Armor|Sculpted gunmetal radio panel, left portrait and pilot-colour tab.|Industrial cockpit rails with strong section separation.|
|B · Cartridge Classic|Indigo/silver cartridge-style panel with right portrait.|Quiet continuous instrument rails, high-contrast type and simple dividers.|
|C · Fury Broadcast|Angular matte-black comms ribbon with ivory edges and raised left portrait.|Black/amber side wings, cream numerals, compact icon-led gauges.|

Dialogue and HUD choices are independent. The review saves a preference in its
own browser origin; it does not install the chosen HUD/window. Existing game
HUD and dialogue frames remain unchanged pending Mike's selection.

Every HUD concept shows roll and somersault readiness, lives/ship icon,
missiles/icon, primary special and secondary warheads on the LEFT. The RIGHT
has pilot portrait, score, high score, equipped weapon/level, speed and armor.
Solid fills, visible numbers, clear centre playfield. Sample counters are design
illustrations; final implementation will use the actual selected pilot/loadout.
These are visual concepts, not gameplay changes or final extracted UI kits.

Saved original-pixel images (odd dialogue source height is padded one bottom row):

- [Dialogue A](../_ART_SOURCES/ui_concepts_1020/art/dialogue-a.png)
- [Dialogue B](../_ART_SOURCES/ui_concepts_1020/art/dialogue-b.png)
- [Dialogue C](../_ART_SOURCES/ui_concepts_1020/art/dialogue-c.png)
- [HUD A](../_ART_SOURCES/ui_concepts_1020/art/hud-a.png)
- [HUD B](../_ART_SOURCES/ui_concepts_1020/art/hud-b.png)
- [HUD C](../_ART_SOURCES/ui_concepts_1020/art/hud-c.png)
- [Dracodia portrait](../_ART_SOURCES/ui_concepts_1020/art/dracodia-portrait.png)

The Dracodia portrait is separately installed in live dialogue. It retains his
actual five-pronged crown, silver mechanical face, red-orange eyes, black/violet
armor and red circuitry. One dedicated square illustrated portrait, not the
previous magnified body crop. It is a single expression, not an invented bank
of animated expressions. `dr5_face_*` aliases now resolve to this image while
native dialogue timing/input/speaker selection remains intact. It preloads for
Stage8 and through dr5Warm; old portrait owner is the decode fallback.

Runtime: `assets/dracodia_dialogue_portrait_1020.js`, loaded after the cinematic
invasion layer. Image: `assets/game/levels/stage_08/cinematics/dracodia_portrait_1020/portrait.webp`.
The 1254×1254 master is losslessly exported, with no pixel changes. Concept
boards stay outside runtime assets/preloads. Sources and manifest:
`_ART_SOURCES/ui_concepts_1020`. Native review/dialogue proof:
`_shots/ui_concepts_1020/report.json` and screenshots beside it.

No game.js/test_fl.js edits, combat changes, Overdrive changes, commit or push.
