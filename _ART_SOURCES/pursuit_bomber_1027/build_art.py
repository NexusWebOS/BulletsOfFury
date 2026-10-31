from pathlib import Path
from PIL import Image,ImageDraw
import json,math,subprocess,os,shutil
W=Path(__file__).resolve().parent;R=W.parents[1];D=W/'compiled';D.mkdir(exist_ok=True)
src=Image.open(R/'assets/game/shared/combat/polish_0927b/bomber.png').convert('RGBA');ordnance=Image.open(R/'assets/game/levels/stage_04/projectiles/projectiles_0927/stage4_ordnance.png').convert('RGBA');M={}
def pack(name,frames,cw,ch,cols=8,**extra):
 sheet=Image.new('RGBA',(cw*cols,ch*math.ceil(len(frames)/cols)))
 for i,f in enumerate(frames):sheet.alpha_composite(f,(i%cols*cw,i//cols*ch))
 sheet.save(D/(name+'.png'));M[name]={'key':'pb28_'+name,'path':'assets/game/levels/stage_06/miniboss/pursuit_1027/'+name+'.png','cw':cw,'ch':ch,'cols':cols,'frames':len(frames),'pivot':[cw//2,ch//2],**extra}
plate=src.crop((351,615,588,1150)).resize((36,81),Image.Resampling.NEAREST);bay=src.crop((790,685,1112,1114)).resize((32,43),Image.Resampling.NEAREST);frames=[]
# Fixed measured launch pods: original metal silhouette plus original twin bomb rack.
for i in range(16):
 c=Image.new('RGBA',(48,104));c.alpha_composite(plate,(6,11));c.alpha_composite(bay,(8,50));g=ImageDraw.Draw(c);op=(0 if i<2 else min(1,(i-2)/5)if i<8 else min(1,max(0,1-(i-10)/5)));width=round(14*(1-op));door=plate.crop((2,27,16,64))
 if width:
  c.alpha_composite(door.crop((0,0,width,37)),(10,53));c.alpha_composite(door.transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,0,width,37)),(38-width,53))
 frames.append(c)
pack('bay',frames,48,104,8)
hit=[]
for f in frames:
 q=Image.new('RGBA',f.size,(255,255,255,0));q.putalpha(f.getchannel('A'));hit.append(q)
pack('bay_hit',hit,48,104,8)
for name,row,h,cell in [('missile',3,42,64),('fragment',0,14,32)]:
 frames=[]
 for f in range(4):
  q=ordnance.crop((f*256,row*320,f*256+256,row*320+320));q=q.resize((round(256*h/320),h),Image.Resampling.NEAREST)
  base=Image.new('RGBA',(cell,cell));base.alpha_composite(q,((cell-q.width)//2,(cell-q.height)//2))
  for d in range(64):frames.append(base.rotate(-d*360/64,Image.Resampling.NEAREST))
 pack(name,frames,cell,cell,8,directions=64,cycles=4,zeroHeading='down')
frames=[]
for f in range(16):
 q=ordnance.crop((f%4*256,4*320,f%4*256+256,5*320));q=q.resize((29,36),Image.Resampling.NEAREST);base=Image.new('RGBA',(64,64));base.alpha_composite(q,((64-q.width)//2,(64-q.height)//2));frames.append(base.rotate(math.sin(f/16*math.tau)*6,Image.Resampling.NEAREST))
pack('bomb',frames,64,64,4)
(D/'manifest.json').write_text(json.dumps(M,indent=2),encoding='utf-8');(R/'assets/pursuit_bomber_art_1027.js').write_text('"use strict";\nconst PB28_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8')
ase=os.environ.get('ASEPRITE_EXE')or shutil.which('aseprite')
if ase:subprocess.run([str(ase),'--batch',str(D/'bay.png'),'--save-as',str(W/'bomb-bays.aseprite')],check=True,capture_output=True)
for a in M.values():
 target=R/a['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(D/(target.stem+'.png'),target)
shutil.copy2(D/'manifest.json',W/'manifest.json')
print('Authored bomb racks, bombs and64-direction missile/fragment banks from existing BOF artwork.')

