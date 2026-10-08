"""Live review of the permanent X marker, physical HQ frontage and travel."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1]
# Preserve the previous review builder/output. Use its working live-engine UI.
runpy.run_path(str(R/'_BUILD_SOURCE/review_campaign_landscape_1004e.py'))
s=(R/'_shots/campaign_landscape_1004e/review.html').read_text()
s=s.replace('campaign-landscape-1004e','campaign-markers-1004f')
s=s.replace('One campaign world.','Chrome campaign flags.')
s=s.replace('A connected continent beneath the stage regions: jungle rivers, lava foothills, glacier ridges, desert roads, storm highlands and toxic canals. The central city, Fury HQ and cosmic bonus rift retain the original navigation markers. Blue water and drifting clouds surround the coast.','Stage X stays planted in the central city. Fury HQ is the building itself, with raised lettering built into its frontage. Extra map labels are removed. The ship points down on 4 → 5 and up on 7 → 8 and 8 → 1.')
s=s.replace('<button data-stage="x">Stage X city</button>','<button data-stage="xl">Stage X locked</button><button data-stage="xh">Stage X Harrier</button><button data-stage="x">Stage X Rebels</button><button data-stage="hq">Fury HQ close-up</button>')
s=s.replace('w.Storage.prototype.setItem=function(){};','w.__reviewMapCamera=w.cmap2CameraTick;w.Storage.prototype.setItem=function(){};')
s=s.replace('if(!ready)return;const w=frame.contentWindow,stage=button.dataset.stage;','if(!ready)return;const w=frame.contentWindow,stage=button.dataset.stage;w.cmap2CameraTick=w.__reviewMapCamera;w.eval("MAP4E.xPreview=false;");')
s=s.replace("if(stage==='x')w.eval('campaign.stageX1004={route:\"right\",done:false};CF4.flight=4;CF4.focus=true;sselCursor=7;MAP4E.focus=true;');", "if(stage==='x'||stage==='xh')w.eval('campaign.stageX1004={route:\"'+(stage==='xh'?'left':'right')+'\",done:false};CF4.flight=4;CF4.focus=true;sselCursor=7;MAP4E.focus=true;');\n else if(stage==='xl')w.eval('MAP4E.xPreview=true;');\n else if(stage==='hq')w.eval('cmap2CameraTick=function(){cmap2.cam={...cmap2World(\"hq\"),z:.55};};');")
s=s.replace('live-focused-volcano-screen.png','hq-native-screen.png').replace('Volcanic region camera focus','Fury headquarters in the game renderer').replace('Stage regions lift on selection; the landscape remains connected below.','The lettering belongs to the authored headquarters building.')
s=s.replace('<div class="grid">','<figure style="margin-top:24px"><img src="../../assets/game/shared/campaign/campaign_landscape_1004f/flags_preview.png" alt="Generated I through IX campaign flags in the approved X flag style"><figcaption>I–IX and X share the chrome frame, mast and base, with stage colors preserved.</figcaption></figure><div class="grid">')
s=s.replace('w.Storage.prototype.setItem=function(){};w.Storage.prototype.removeItem=function(){};','w.map4hPreviewStorage();')
O=R/'_shots/campaign_markers_1004f';O.mkdir(exist_ok=True);(O/'review.html').write_text(s,encoding='utf-8');print(O/'review.html')
