"""Review live controls with persistent, isolated demo save slots."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_controls_1004h';O.mkdir(exist_ok=True)
runpy.run_path(str(R/'_BUILD_SOURCE/review_campaign_markers_1004f.py'))
runpy.run_path(str(R/'_BUILD_SOURCE/review_campaign_stagex_1004g.py'))
s=(R/'_shots/campaign_stagex_1004g/review.html').read_text(encoding='utf-8')
s=s.replace('campaign-stagex-1004g','campaign-controls-1004h').replace('Floating Stage X island.','Campaign controls and save slots.')
s=s.replace('Stage X now hovers over the central landscape on its own deep rocky island. The city, X flag and encounter ships share its floating position. Click the island to inspect it; an earned route opens its Harrier or Rebel fight.','Start opens the top menu. The D-pad navigates missions; Up from VI selects X and Down returns to VI. Save/load panels use generated chrome cartridges, with pilot ships and saved campaign details. Demo slots on this page persist separately from your real campaign saves.')
s=s.replace('<div class="buttons">','<p><a style="color:#9ee9ff" href="../../index.html?build=campaign-controls-1004h" target="_blank">Open the game with your real campaign saves</a></p><div class="buttons"><button data-stage="save">Save slots</button><button data-stage="load">Load slots</button>')
s=s.replace('sselBoot=0;MAP4E.xPreview=true;','sselBoot=0;MAP4E.xPreview=false;')
s=s.replace('run.pilot="lizzie";','run.pilot="lizzie";pilotIndex=PILOTS.findIndex(p=>p.key==="lizzie");')
s=s.replace("if(stage==='x'||stage==='xh')", "if(stage==='save'||stage==='load')w.eval('cmap2.focus=\"bar\";cmap2.bar='+(stage==='save'?0:1)+';cmap2BarActivate(cmap2.bar);');\n else if(stage==='x'||stage==='xh')")
s=s.replace('src="overview.png"','src="../campaign_stagex_1004g/overview.png"').replace('src="floating-stage-x.png"','src="save-slots.png"').replace('Floating Stage X city in the game renderer','Generated save cartridges in the actual game').replace('Stage X lifts above the terrain with its own rocky underside and moving shadow.','Saved slots show their ship, stage, difficulty, score and time. Saving is verified by reading back the stored data.')
s=s.replace('Preview changes do not write campaign saves.','Demo slots persist separately; the linked game uses your real saves.')
(O/'review.html').write_text(s,encoding='utf-8');print(O/'review.html')
