"""Keep the working live map review and open on the floating Stage X island."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_stagex_1004g';O.mkdir(exist_ok=True)
s=(R/'_shots/campaign_markers_1004f/review.html').read_text(encoding='utf-8')
s=s.replace('campaign-markers-1004f','campaign-stagex-1004g').replace('Chrome campaign flags.','Floating Stage X island.')
s=s.replace('Stage X stays planted in the central city. Fury HQ is the building itself, with raised lettering built into its frontage. Extra map labels are removed. The ship points down on 4 → 5 and up on 7 → 8 and 8 → 1.','Stage X now hovers over the central landscape on its own deep rocky island. The city, X flag and encounter ships share its floating position. Click the island to inspect it; an earned route opens its Harrier or Rebel fight.')
s=s.replace('openStageSelect(1,{boot:true});sselUnlockCine=null;','openStageSelect(1,{});sselBoot=0;MAP4E.xPreview=true;sselUnlockCine=null;')
s=s.replace('live-overview-screen.png','overview.png').replace('hq-native-screen.png','floating-stage-x.png').replace('Fury headquarters in the game renderer','Floating Stage X city in the game renderer').replace('The lettering belongs to the authored headquarters building.','Stage X lifts above the terrain with its own rocky underside and moving shadow.')
s=s.replace('w.Storage.prototype.setItem=function(){};w.Storage.prototype.removeItem=function(){};','w.map4hPreviewStorage();')
(O/'review.html').write_text(s,encoding='utf-8');print(O/'review.html')
