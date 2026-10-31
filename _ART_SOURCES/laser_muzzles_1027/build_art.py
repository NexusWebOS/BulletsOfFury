from pathlib import Path
from PIL import Image
import json,hashlib,math
W=Path(__file__).resolve().parent;S=W/'source';O=W/'compiled';O.mkdir(exist_ok=True)
src=Image.open(S/'emitter.png').convert('RGBA');data=json.loads((S/'emitter.json').read_text());frames=[]
for q in data['frames']:
 r=q['frame'];assert(r['w'],r['h'])==(64,64);frames.append(src.crop((r['x'],r['y'],r['x']+64,r['y']+64)))
assert len(frames)==16
M={'source':'PixelLab VFX Workbench / ba5669e0-cf0d-4acf-9de2-9a14830f7824','sourcePivot':[16,32],'directionCount':64,'fps':24,'banks':{}}
for name,size,reference in [('small',42,12),('medium',54,20),('large',68,29)]:
 k=size/64;sheet=Image.new('RGBA',(4096,1024));edges=0
 for phase,im in enumerate(frames):
  scaled=im.resize((size,size),Image.Resampling.NEAREST);base=Image.new('RGBA',(64,64));base.alpha_composite(scaled,(32-round(16*k),32-round(32*k)))
  for direction in range(64):
   q=base.rotate(-direction*360/64,resample=Image.Resampling.NEAREST,center=(32,32));b=q.getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<64 and b[3]<64,(name,phase,direction,b)
   i=phase*64+direction;sheet.alpha_composite(q,(i%64*64,i//64*64))
 p=O/(name+'.png');sheet.save(p,optimize=True);M['banks'][name]={'key':'lm27_'+name,'path':'assets/game/shared/combat/laser_muzzles_1027/'+name+'.png','cw':64,'ch':64,'cols':64,'frames':16,'directions':64,'pivot':[32,32],'referenceBeamWidth':reference,'sourceScale':k,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(O/'manifest.json').write_text(json.dumps(M,indent=2));(W/'laser_muzzles_art_1027.js').write_text('"use strict";\nconst LM27_ART='+json.dumps(M,separators=(',',':'))+';\n')
contact=Image.new('RGBA',(64*8,64*2),(10,19,28,255))
for i,im in enumerate(frames):contact.alpha_composite(im,(i%8*64,i//8*64))
contact.resize((1024,256),Image.Resampling.NEAREST).save(W/'source-contact.png')
print('Built 3 fixed 64x64 banks, 16 phases x64 directions each; all alpha bounds clear of cell edges.')
