# Fury HQ, The Forge and full-build Re-Spec — October23

PixelLab-generated HQ and Forge map icons replace the old HQ landmark and temporary Upgrade Center island. Both use fixed256px exports and stable map anchors. The actual selected aircraft travels to The Forge. North from Stage1 or Start > Forge / Loadout opens Decker's Workshop. Forge and Loadout return here.

Re-Spec now resets ALL current-run element forms, equipped forge elements and element-dependent variants/infusion. It retains completed stages, discovered boss elements, earned base weapons, weapon pickup levels and profile recipes. NG+ recipe auto-import is suppressed after a reset for this run, so basic forms remain basic until selected/upgraded again. The next fresh run restores normal NG+ import.

The fee is300 Furious Points, selected as a default matching the base Forge recipe price. Confirmation defaults to Cancel. Insufficient funds, a basic build, held input or failed profile/campaign storage do not consume a fee. The profile supplies ledger explicitly recognizes respec transactions on reload. Score is never deducted.

Two upgrade points per DISTINCT completed stage, cumulative. Re-Spec restores the earned total, rather than adding it again. Before Stage6 clears:10; clear6:12; clear7:14. New stage selection, retries and repeated Forge visits do not award points. A saved completion ledger and remaining points round-trip with campaign saves. Old saves migrate from actual rank records, or their unlocked progress if ranks are absent. Saving at the Forge retains the campaign destination rather than Stage1's navigation flag.

Art: four PixelLab jobs and14 registered fixed assets, retained raw sources and hashes in _ART_SOURCES/hq_forge_1023/manifest.json. Builder:_BUILD_SOURCE/build_hq_forge_1023.py. Runtime:assets/hq_forge_1023.js and art registry:assets/hq_forge_art_1023.js. Claude's two upstream map/start routing modules were selectively imported from a59a2e0704476aa3bf794bd5c11ff5da0d2192a1; unrelated incoming debug/station/combat changes were not imported. Start/menu artwork uses fixed authored states, no runtime tint/glow/fade for these new screens.

Native QA:_BUILD_SOURCE/probe_hq_forge_1023.py;36/36 checks, zero console/page errors. Actual keyboard, mouse and gamepad poller; reset/save-failure rollbacks, cumulative budgets, legacy/NG+ saves, reassign/equip, all three service entry routes and390/1100/1920px layouts. Review:_shots/hq_forge_1023/index.html. Required core regression result is recorded at the top of HANDOFF_CODEX.md after completion.
