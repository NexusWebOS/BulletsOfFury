from pathlib import Path
from PIL import Image
import json,math,sys,shutil,hashlib
import numpy as np
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_ART_SOURCES/hammer_jump_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Hammer-Jump-1022'
D=W/'shipping';D.mkdir(exist_ok=True);jobs={j['id']:j for j in json.loads((W/'jobs.json').read_text(encoding='utf-8-sig'))}
A={'banks':{},'sheets':{},'phases':{},'legacyGlow':{},'pending':[]};audit=[]
def frames(name):
 j=jobs.get(name,{});files=sorted((W/'returned'/name).glob('*.png'))
 if j.get('status')!='completed' or len(files)!=j.get('frames'):return []
 return [Image.open(files[i]).convert('RGBA') for i in j.get('selected',range(len(files)))]
def centre(im,kind,hint=None):
 a=np.asarray(im).astype(float);r,g,b,al=[a[:,:,i] for i in range(4)];yy,xx=np.indices(al.shape)
 m=(b>135)&(g>70)&(b>r*1.3) if kind=='blue' else (r>110)&(b>150)&(b>g*1.2)
 m&=(al>128)
 if hint is None:m&=((xx-128)**2+(yy-112)**2>28**2)
 groups,n=label(m);choices=[]
 for i in range(1,n+1):
  y,x=np.where(groups==i)
  if len(x)<4:continue
  c=[float(x.mean()),float(y.mean())];score=len(x)
  if hint:score/=1+math.hypot(c[0]-hint[0],c[1]-hint[1])/30
  choices.append((score,c))
 return max(choices,key=lambda q:q[0])[1] if choices else (hint or [128,200])
def chrome(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);m=(a[:,:,3]>0)&(hi-lo<28)&(hi>27)&(hi<235);lum=rgb@np.array([.2126,.7152,.0722]);shine=np.minimum(245,130+lum*.85)
 for c,f in enumerate([.96,1,1.04]):a[:,:,c][m]=np.clip(shine[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)

def authored_unit(im,scale,origin,target):
 # Match the explicitly measured shoulder/chest unit of separately authored
 # reference poses. This is an offline source-unit conversion, never a fit
 # to the silhouette bounds (which change during the swing).
 out=Image.new('RGBA',(256,256));size=round(256*scale)
 out.alpha_composite(im.resize((size,size),Image.Resampling.NEAREST),
  (round(target[0]-origin[0]*scale),round(target[1]-origin[1]*scale)))
 return out
def emit(name,ims,kind,pivot=[128,112],tips=None,glows=None,factor=None):
 if not ims:A['pending'].append(name);return []
 factor=factor or (1.75 if kind=='blue' else 1.453125);side=512 if kind=='blue' else 464
 rw=round(256*factor);off=(side-rw)//2;rows=[];columns=4;sheet=Image.new('RGBA',(side*columns,side*math.ceil(len(ims)/columns)));white=sheet.copy()
 for i,im in enumerate(ims):
  assert im.size==(256,256);box=im.getbbox();assert box and min(box[:2])>0 and max(box[2:])<256,(name,i,box)
  cell=Image.new('RGBA',(side,side));cell.alpha_composite(im.resize((rw,rw),Image.Resampling.NEAREST),(off,off));bounds=cell.getbbox();x=i%columns*side;y=i//columns*side;sheet.alpha_composite(cell,(x,y))
  w=Image.new('RGBA',cell.size,'white');w.putalpha(cell.getchannel('A'));white.alpha_composite(w,(x,y))
  convert=lambda p:[round(p[0]*factor+off),round(p[1]*factor+off)]
  head=glows[i] if glows else centre(im,kind);tip=tips[i] if tips else head
  row={'key':f'ha21_hj22_{name}_{i}','white':f'ha21_hj22_{name}_hit_{i}','sheet':'hj22_'+name,'cell':[x,y,side,side],'w':side,'h':side,'pivot':convert(pivot),'bounds':list(bounds),'tip':convert(tip),'glow':convert(head),'_hj22':True,'bank':name,'frame':i,'kind':kind,'sourceScale':factor}
  rows.append(row);audit.append({'bank':name,'frame':i,'bounds':list(bounds),'pivot':row['pivot'],'tip':row['tip'],'glow':row['glow']})
 for suffix,img in [('',sheet),('_hit',white)]:
  p=D/(name+suffix+'.webp');img.save(p,lossless=True,exact=True,method=6);A['sheets']['hj22_'+name+suffix]={'key':'nca_hj22_'+name+suffix,'path':'assets/game/shared/combat/hammer_jump_1022/'+p.name,'w':img.width,'h':img.height}
 A['banks'][name]=rows;return rows
for kind in ['blue','corrupt']:
 wind=frames(kind+'_wind');strike=frames(kind+'_strike');front=frames(kind+'_front');low=frames(kind+'_low')
 final=frames('blue_impact') if kind=='blue' else [Image.open(W/'references/corrupt_impact.png').convert('RGBA')]
 if not all([wind,strike,front,low,final]):A['pending'].append(kind+'_jump');continue
 # Explicit authored in-betweens fill the wide over-crown-to-waist gap. No
 # silhouette fitting, software tweening or generated smear replaces a pose.
 if kind=='blue':
  # The new close reference keys have a 100px shoulder unit versus the
  # original 64px unit. Keep their detail and convert the entire key source
  # at .64 around the measured chest landmark, not individual frame bounds.
  front=[authored_unit(im,.64,[128,88],[128,112]) for im in front]
  final=[authored_unit(im,.64,[128,88],[128,112]) for im in final]
  low=[authored_unit(im,.64,[128,88],[128,112]) for im in low]
  descent=strike[1:3]+front+strike[3:5]+final
 else:
  upper=[authored_unit(im,.85,[128,104],[128,112]) for im in frames('corrupt_front_fix')]
  if not upper:A['pending'].append('corrupt_inbetweens');continue
  descent=strike[1:3]+upper+strike[3:5]+final
 bank=wind+descent;M={'windEnd':len(wind)-1,'strikeEnd':len(bank)-1,'recoverStart':len(bank)};bank+=(low if kind=='blue' else [strike[3]])+[wind[1],wind[0]]
 rows=emit(kind+'_jump',bank,kind);A['phases'][kind]=M
 if rows:
  contact=jobs.get(kind+'_impact',{}).get('contact',[134,237] if kind=='corrupt' else [132,233]);s=rows[M['strikeEnd']]['sourceScale'];off=(rows[0]['w']-round(256*s))//2
  if kind=='blue':contact=[round(contact[0]*.64+46),round(contact[1]*.64+56)]
  rows[M['strikeEnd']]['tip']=[round(contact[0]*s+off),round(contact[1]*s+off)]
  rows[M['strikeEnd']]['glow']=[round(contact[0]*s+off),round((contact[1]-24)*s+off)]
 if kind=='blue' and rows:
  silver=emit('blue_jump_armor',[chrome(im) for im in bank],'blue')
  for a,b in zip(silver,rows):a['tip']=b['tip'];a['glow']=b['glow']
for kind in ['blue','corrupt']:
 ims=frames(kind+'_glow_loop')
 if not ims:A['pending'].append(kind+'_glow_loop');continue
 sheet=Image.new('RGBA',(128*len(ims),128));rows=[]
 for i,im in enumerate(ims):
  assert im.size==(64,64) and im.getbbox();im=im.resize((128,128),Image.Resampling.NEAREST);sheet.alpha_composite(im,(128*i,0));rows.append({'key':f'hj22_{kind}_glow_{i}','sheet':'hj22_'+kind+'_glow','cell':[128*i,0,128,128],'w':128,'h':128,'pivot':[64,64],'kind':kind})
 p=D/(kind+'_glow.webp');sheet.save(p,lossless=True,exact=True,method=6);A['banks'][kind+'_glow']=rows;A['sheets']['hj22_'+kind+'_glow']={'key':'nca_hj22_'+kind+'_glow','path':'assets/game/shared/combat/hammer_jump_1022/'+p.name,'w':sheet.width,'h':128}
# New follow-up tells use existing authored warning art converted OFFLINE to
# fixed units. Do not inherit the old live rotation/scale/pulse helpers.
fov_cells=json.loads((R/'assets/data/ui_bossmode_fx_cells.json').read_text());fov_source=Image.open(R/'assets/game/shared/ui/ui_bossmode_fx.png').convert('RGBA');reticle=Image.open(R/'assets/game/levels/stage_05/boss/stage5_hammer/reticle.png').convert('RGBA')
for name,w,h in [('warning_cone',320,384),('warning_reticle',124,2*round(reticle.height/reticle.width*124/2))]:
 sheet=Image.new('RGBA',(w*3,h));rows=[]
 for i,col in enumerate(['green','yellow','red']):
  if name=='warning_cone':
   _,x,y,cw,ch=fov_cells['bmfx_fov_'+col+'_tall'];im=fov_source.crop((x,y,x+cw,y+ch)).resize((w,h),Image.Resampling.NEAREST);pivot=[160,334]
  else:
   im=reticle.copy();pivot=[w//2,h//2]
   if col!='green':
    a=np.array(im);lum=a[:,:,:3]@np.array([.21,.72,.07]);co=[1.4,1.25,.15] if col=='yellow' else [1.55,.23,.22]
    for c in range(3):a[:,:,c]=np.clip(lum*co[c],0,255).astype('uint8')
    im=Image.fromarray(a)
   im=im.resize((w,h),Image.Resampling.NEAREST)
  sheet.alpha_composite(im,(i*w,0));rows.append({'key':f'hj22_{name}_{col}','sheet':'hj22_'+name,'cell':[i*w,0,w,h],'w':w,'h':h,'pivot':pivot})
 p=D/(name+'.webp');sheet.save(p,lossless=True,exact=True,method=6);A['banks'][name]=rows;A['sheets']['hj22_'+name]={'key':'nca_hj22_'+name,'path':'assets/game/shared/combat/hammer_jump_1022/'+p.name,'w':sheet.width,'h':h}
# Reuse Mike's actual twelve-frame Hama double; half-size conversion is one
# declared source unit for the ENTIRE bank, not independent per-frame fitting.
s=(R/'assets/hama_frames_art_0929.js').read_text(encoding='utf-8');H=json.loads(s[s.index('{'):s.rfind('}')+1])['families']['double_hammer_slam'];source=Image.open(R/H['path']).convert('RGBA');ims=[]
for r in H['frames']:
 x,y,w,h=r;im=source.crop((x,y,x+w,y+h)).resize((224,240),Image.Resampling.NEAREST);cell=Image.new('RGBA',(256,256));cell.alpha_composite(im,(16,8));ims.append(cell)
# Preserve the original double reference in the source archive. Both native
# combos use its two-contact cadence with their current jump artwork; do not
# ship a second lower-detail body which would pop in halfway through a combo.
# Offline measured light sockets for old armed banks. These are positions only;
# the runtime draws the same pre-authored corona pixels without blend/rotation.
old=json.loads((R/'assets/game/shared/combat/hammer_acting_1021/manifest.json').read_text(encoding='utf-8'));h22=json.loads((R/'assets/hammer_correction_art_1022.js').read_text(encoding='utf-8').split('const H22_ART=')[1].rstrip(';\n'));cache={}
for registry in [old,h22]:
 for name,rows in registry['banks'].items():
  if not name.startswith(('blue_','corrupt_')) or any(k in name for k in ['empty','unarmed','gun','uzi','ball','ship','fists','punch','fire','beam','stun','rage']):continue
  kind='blue' if name.startswith('blue') else 'corrupt'
  for row in rows:
   if row['key'] in A['legacyGlow']:continue
   path=registry['sheets'][row['sheet']]['path']
   if path not in cache:cache[path]=Image.open(R/path).convert('RGBA')
   src=cache[path];x,y,w,h=row['cell'];im=src.crop((x,y,x+w,y+h));hint=row.get('tip',[w/2,h*.7]);A['legacyGlow'][row['key']]=centre(im,kind,hint)
for q in audit:
 row=A['banks'][q['bank']][q['frame']];q['tip']=row['tip'];q['glow']=row['glow']
(W/'hammer_jump_art_1022.js').write_text('"use strict";\nconst HJ22_ART='+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8');(W/'frame-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8');print(json.dumps({'banks':len(A['banks']),'pending':A['pending'],'cells':len(audit),'glowSockets':len(A['legacyGlow'])}),flush=True)
manifest={'owner':'_BUILD_SOURCE/build_hammer_jump_1022.py','source':'_ART_SOURCES/hammer_jump_1022','banks':{k:len(v) for k,v in A['banks'].items()},'phases':A['phases'],'rendering':'Fixed prebaked logical units, authored white flash and corona frames; position-only jump motion.','sheets':[]}
for sid,s in A['sheets'].items():
 p=D/Path(s['path']).name;manifest['sheets'].append(dict(s,id=sid,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(W/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if '--install' in sys.argv:
 assert not A['pending'],'All authored motion and glow banks must complete before install.'
 target=R/'assets/game/shared/combat/hammer_jump_1022';target.mkdir(parents=True,exist_ok=True)
 for p in D.glob('*.webp'):
  if 'hj22_'+p.stem in A['sheets']:shutil.copy2(p,target/p.name)
 for name in ['hammer_jump_art_1022.js','hammer_jump_1022.js']:shutil.copy2(W/name,R/'assets'/name)
 shutil.copy2(W/'manifest.json',target/'manifest.json')
 p=R/'index.html';data=p.read_bytes();tag=b'<script src="assets/hammer_jump_art_1022.js?v=jump-1022-1"></script>\n<script src="assets/hammer_jump_1022.js?v=jump-1022-1"></script>\n'
 if b'hammer_jump_1022.js' not in data:p.write_bytes(data.replace(b'</body>',tag+b'</body>'))
 else:p.write_bytes(data.replace(b'jump-1022-1',b'jump-1022-2'))
 print('Installed complete authored jumping Hammer pass.')
