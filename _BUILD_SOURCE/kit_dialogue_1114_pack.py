from pathlib import Path
import json,hashlib,shutil
from PIL import Image
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');O=R/'_shots/kit_dialogue_1114';S=O/'install';(S/'assets').mkdir(parents=True,exist_ok=True)
source=R/'_ART_SOURCES/kit_dialogue_1114/satellite-source.png'
im=Image.open(source).convert('RGB');sheet=Image.new('RGB',(1672,944));frames=[]
for f in range(16):
 x=(f%4)*418;y=[0,235,470,706][f//4];c=im.crop((x,y,x+418,y+235));sheet.paste(c,(x,(f//4)*236));sheet.paste(c.crop((0,234,418,235)),(x,(f//4)*236+235));frames.append(c)
a=S/'assets/game/shared/cinematics/kit_dialogue_1114';a.mkdir(parents=True,exist_ok=True);sheet.save(a/'satellite-code.webp',lossless=True)
frames[0].save(O/'satellite-clean.png');frames[-1].save(O/'satellite-corrupted.png');frames[0].save(O/'satellite-code.gif',save_all=True,append_images=frames[1:]+frames[12:16]*3,duration=125,loop=0)
# Keep source, reference and prompt in project provenance, not only generated-images.
d=S/'_ART_SOURCES/kit_dialogue_1114';d.mkdir(parents=True,exist_ok=True);shutil.copy2(source,d/'satellite-source.png');shutil.copy2(O/'clean-satellite-reference.png',d/'clean-satellite-reference.png')
shutil.copy2(O/'kit_dialogue_1114.js',S/'assets/kit_dialogue_1114.js')
s=(R/'assets/audio_extra_1010.js').read_text(encoding='utf8');start=s.index('furyShipDrawPhase=function');end=s.index('victoryRestoration=function',start)
s=s[:start]+'''// November14: every pilot uses the same twelve physical orbiting kit pieces.
// The retired Cole-only baked strip hid the actual kit and skipped its entrances.
furyShipDrawPhase=function(){return AP10_EXTRA.phase.apply(this,arguments);};
'''+s[end:];(S/'assets/audio_extra_1010.js').write_text(s,encoding='utf8',newline='\n')
s=(R/'assets/ship_forming_1104.js').read_text(encoding='utf8');s=s.replace("const cole=pilot==='cole',ph=G.phase;","const cole=false,ph=G.phase; // Same hardware and effects for every pilot.")
(S/'assets/ship_forming_1104.js').write_text(s,encoding='utf8',newline='\r\n' if b'\r\n' in (R/'assets/ship_forming_1104.js').read_bytes() else '\n')
s=(R/'index.html').read_text(encoding='utf8');import re
for name in ['audio_extra_1010','ship_forming_1104']:
 s=re.sub(r'(assets/'+name+r'\.js)(?:\?[^\"\']*)?',r'\1?v=kit18',s)
s=s if 'assets/kit_dialogue_1114.js' in s else s.replace('</body>','<script src="assets/kit_dialogue_1114.js?v=1"></script>\n</body>');(S/'index.html').write_text(s,encoding='utf8',newline='\n')
print('STAGED',S,'sheet',sheet.size,'distinct',len(set(hashlib.sha256(c.tobytes()).hexdigest()for c in frames)))
