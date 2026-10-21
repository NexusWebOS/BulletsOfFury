from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import numpy as np,json,shutil
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/boss_redesign_1020';D=R/'assets/game/levels/stage_08/boss/hammer_redesign_1020';D5=R/'assets/game/levels/stage_05/boss/hammer_redesign_1020';M=R/'assets/game/shared/boss_redesign_1020';O=R/'_shots/boss_redesign_1020'
for p in [D,D5,M,O]:p.mkdir(parents=True,exist_ok=True)
jobs=json.loads((S/'jobs.json').read_text());art={'banks':{},'jobs':jobs,'pivot':[128,112],'registration':'Fixed256 canvases, chest pivot128,112. No per-frame fitting.'};audit=[]
def tip(im,blue):
 a=np.asarray(im);r,g,b,al=[a[:,:,i].astype(float) for i in range(4)];yy,xx=np.indices(al.shape)
 m=((b>r*1.25)&(b>90)&(g>65)) if blue else ((r>110)&(r>g*1.10)&(g>55))
 m=m&(al>120)&(((xx-128)**2+(yy-112)**2)>30**2)
 # Dense authored hammer-head pixels win over thin trails and isolated sparks.
 integ=np.pad(m.astype(float),((5,5),(5,5))).cumsum(0).cumsum(1);v=integ[10:,10:]-integ[:-10,10:]-integ[10:,:-10]+integ[:-10,:-10];y,x=np.unravel_index(v.argmax(),v.shape)
 return [int(x),int(y)] if v[y,x]>=6 else [75,162]
def emit(name,images,blue=False,tips=True,pivot=[128,112]):
 bank=[];folder=(D5 if name.startswith('blue_') else D)/name;folder.mkdir(exist_ok=True)
 for i,im in enumerate(images):
  assert im.size==(256,256);q=im.getbbox();assert q and q[0]>0 and q[1]>0 and q[2]<256 and q[3]<256,(name,i,q)
  p=folder/f'{i:02}.png';im.save(p,optimize=True);a=dict(key=f'hb20_{name}_{i}',path=p.relative_to(R).as_posix(),w=256,h=256,pivot=pivot,bounds=list(q))
  if tips:a['tip']=tip(im,blue)
  bank.append(a);audit.append(dict(bank=name,frame=i,bounds=q,tip=a.get('tip')))
 art['banks'][name]=bank
 if len(images)>1:
  cols=8;cw=192;ch=212;sheet=Image.new('RGB',(cols*cw,((len(images)+cols-1)//cols)*ch),'#10131d');dr=ImageDraw.Draw(sheet)
  for i,(im,a) in enumerate(zip(images,bank)):
   x=i%cols*cw;y=i//cols*ch;small=im.resize((192,192),Image.Resampling.NEAREST);sheet.paste(small,(x,y),small);dr.text((x+5,y+194),f'{name} {i}',fill='white')
   if a.get('tip'):tx,ty=a['tip'];tx=x+tx*.75;ty=y+ty*.75;dr.ellipse((tx-4,ty-4,tx+4,ty+4),outline='#20ff80',width=1)
  sheet.save(O/(name+'-contact.png'))
for name,row in jobs.items():
 if not name.startswith(('blue_','corrupt_')) or name in ['corrupt_master','corrupt_tool','corrupt_ball','corrupt_gun_seed']:continue
 files=sorted((S/name).glob('*.png'))
 if len(files)!=row['count']:continue
 ims=[Image.open(p).convert('RGBA') for p in files]
 if name=='blue_throw':
  # Once the released weapon leaves the source cell, it belongs to the native
  # flying weapon object. Never ship a cropped off-cell hammer in the body reel.
  for i in range(12,len(ims)):ims[i]=Image.open(S/'blue_empty/00.png').convert('RGBA')
 if name=='blue_gun':
  # PixelLab's recoil clip drew a stray spark over the helmet. Keep the exact
  # approved fixed head/shoulders and use only the authored moving held gun below.
  seed=ims[0].copy()
  for im in ims:
   im.paste(seed.crop((0,0,256,104)),(0,0))
 if name=='corrupt_gun':
  # Keep recoil in the held barrel; reject hallucinated forehead/leg sparks.
  seed=ims[0].copy();mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon([(132,123),(239,168),(239,215),(156,182)],fill=255)
  ims=[Image.composite(im,seed,mask) for im in ims]
 emit(name,ims,name.startswith('blue_'),name not in ['blue_gun','blue_empty','corrupt_unarmed','corrupt_gun','corrupt_fire','corrupt_punch','corrupt_fists'])
 if name=='blue_side':emit('blue_side_left',[ImageOps.mirror(im) for im in ims],True)
 if name=='corrupt_gun':emit('corrupt_gun_left',[ImageOps.mirror(im) for im in ims],False,False)
for name,file,pivot in [('blue_idle',S/'refs/hammer.png',[128,112]),('corrupt_idle',S/'corrupt-reference.png',[128,112]),('corrupt_tool',S/'corrupt_tool/00.png',[128,112])]:
 if file.exists():emit(name,[Image.open(file).convert('RGBA')],name.startswith('blue'),True,pivot)
# refs live in the approved source folder for reproducibility.
ball=S/'corrupt_ball/00.png'
if ball.exists():
 im=Image.open(ball).convert('RGBA');c=Image.new('RGBA',(256,256));c.alpha_composite(im,(0,-10));emit('corrupt_ball',[c.rotate(-i*360/24,Image.Resampling.NEAREST,center=(128,128)) for i in range(24)],False,False,[128,128])
# The measured counter uses sixteen authored poses at a common 512px canvas.
# Its release frames8..11 progress to the actual side-swing release, not a trail.
for side,source in [('right','blue_side'),('left','blue_side_left')]:
 if source not in art['banks']:continue
 bank=[];cache={};order=[0,1,2,3,3,3,3,3,3,4,4,5,6,7,8,0]
 for i,f in enumerate(order):
  if f not in cache:
   a=art['banks'][source][f];im=Image.open(R/a['path']).resize((512,512),Image.Resampling.NEAREST);p=D5/f'counter_{side}_{f:02}.png';im.save(p,optimize=True);cache[f]=dict(key=f'hb20_counter_{side}_{f}',path=p.relative_to(R).as_posix(),w=512,h=512,pivot=[256,224],bounds=[v*2 for v in a['bounds']],tip=[v*2 for v in a['tip']])
  bank.append(cache[f])
 art['banks']['counter_'+side]=bank
(M/'manifest.json').write_text(json.dumps(art,indent=2)+'\n')
for target,prefixes in [(D5,('blue_','counter_')),(D,('corrupt_',))]:(target/'manifest.json').write_text(json.dumps({'banks':{k:v for k,v in art['banks'].items() if k.startswith(prefixes)},'registry':'assets/hammer_redesign_art_1020.js','source':'_ART_SOURCES/boss_redesign_1020/jobs.json'},indent=2)+'\n')
(O/'hammer-alpha-audit.json').write_text(json.dumps(audit,indent=2)+'\n');(R/'assets/hammer_redesign_art_1020.js').write_text('"use strict";\nconst HB20_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
# Archive only this builder's earlier misplaced duplicate exports, after the
# correctly owned Stage5 files exist. No unique source art is deleted.
archive=S/'retired_exports/stage08_blue_duplicates'
for p in [*(D.glob('blue_*')),*(D.glob('counter_*.png'))]:
 assert p.resolve().is_relative_to(D.resolve()) and archive.resolve().is_relative_to(S.resolve())
 archive.mkdir(parents=True,exist_ok=True);dest=archive/p.name
 if dest.exists():raise RuntimeError('Refusing to replace archived export '+str(dest))
 shutil.move(str(p),str(dest))
print(json.dumps({'banks':{k:len(v) for k,v in art['banks'].items()},'frames':len(audit),'layout':'Stage5 blue/counters; Stage8 corrupted; shared family registry'}))
