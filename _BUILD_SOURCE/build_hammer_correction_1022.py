from pathlib import Path
from PIL import Image,ImageOps
import json,math,sys,shutil,hashlib
import numpy as np
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_ART_SOURCES/hammer_correction_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Hammer-Correction-1022';D=W/'shipping';D.mkdir(exist_ok=True)
old=json.loads((R/'assets/game/shared/combat/hammer_acting_1021/manifest.json').read_text(encoding='utf-8'));art={'banks':{},'sheets':{},'pending':[]};audit=[];jobs={j['id']:j for j in json.loads((W/'jobs.json').read_text(encoding='utf-8'))}
endface_jobs=json.loads((W/'endface-jobs.json').read_text(encoding='utf-8')) if (W/'endface-jobs.json').exists() else []
vertical_jobs=json.loads((W/'vertical-jobs.json').read_text(encoding='utf-8')) if (W/'vertical-jobs.json').exists() else []
vertical=bool(vertical_jobs)
if vertical:endface_jobs=vertical_jobs
jobs.update({j['id']:j for j in endface_jobs})
active_jobs=[j for j in endface_jobs if j.get('status')!='failed']
endface=len(active_jobs)>=6 and all(j['status']=='completed' and len(list((W/'returned'/j['id']).glob('*.png')))==j['frames'] for j in active_jobs)
if vertical:endface=endface and {'blue_vertical_direct','corrupt_vertical_direct'}.issubset({j['id'] for j in active_jobs})
def oldframe(name,i):
 a=old['banks'][name][i];im=Image.open(R/old['sheets'][a['sheet']]['path']).convert('RGBA');x,y,w,h=a['cell'];return im.crop((x,y,x+w,y+h))
def tip(im,blue=False):
 a=np.asarray(im).astype(float);r,g,b,al=[a[:,:,i] for i in range(4)];yy,xx=np.indices(al.shape);px=im.width/2;py=112+(im.height-256)/2
 m=(b>100)&(g>65)&(b>r*1.3) if blue else (b>70)&(r>60)&(b>g*1.25)&(r>g*1.18)
 m&=(al>120)&((xx-px)**2+(yy-py)**2>45**2);groups,n=label(m);choices=[]
 for i in range(1,n+1):
  y,x=np.where(groups==i)
  if len(x)<4:continue
  dist=math.hypot(float(x.mean()-px),float(y.mean()-py));choices.append((len(x)+dist*.25,[round(float(x.mean())),round(float(y.mean()))]))
 return max(choices,key=lambda q:q[0])[1] if choices else [round(px),im.height-65]
def chrome(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);m=(a[:,:,3]>0)&(hi-lo<28)&(hi>27)&(hi<235);lum=rgb@np.array([.2126,.7152,.0722]);shine=np.minimum(245,130+lum*.85)
 for c,f in enumerate([.96,1,1.04]):a[:,:,c][m]=np.clip(shine[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def emit(name,frames,blue=False,piv=None,tips=None):
 w,h=frames[0].size;columns=min(5,len(frames));sheet=Image.new('RGBA',(w*columns,h*math.ceil(len(frames)/columns)));rows=[]
 for i,im in enumerate(frames):
  assert im.size==(w,h);bounds=im.getbbox();assert bounds,(name,i)
  assert bounds[0]>0 and bounds[1]>0 and bounds[2]<w and bounds[3]<h,(name,i,bounds)
  cell=[i%columns*w,i//columns*h,w,h];sheet.alpha_composite(im,cell[:2]);pivot=piv or [w//2,112+(h-256)//2];point=tips[i] if tips else tip(im,blue)
  rows.append({'key':f'ha21_h22_{name}_{i}','sheet':'h22_'+name,'cell':cell,'w':w,'h':h,'pivot':pivot,'bounds':list(bounds),'tip':point,'_h22':True,'frame':i,'bank':name})
  audit.append({'bank':name,'frame':i,'bounds':bounds,'pivot':pivot,'tip':point})
 p=D/(name+'.webp');sheet.save(p,lossless=True,exact=True,method=6);art['sheets']['h22_'+name]={'key':'nca_h22_'+name,'path':'assets/game/shared/combat/hammer_correction_1022/'+p.name,'w':sheet.width,'h':sheet.height};art['banks'][name]=rows;return rows
def frames(name):
 files=sorted((W/'returned'/name).glob('*.png'))
 if len(files)!=jobs.get(name,{}).get('frames',-1):return[]
 return[Image.open(p).convert('RGBA') for p in files]

def strikeframes(kind,part):
 name=kind+('_vertical_' if vertical else '_endface_')+part
 if vertical and kind=='blue' and part=='down':name='blue_vertical_direct'
 if vertical and kind=='corrupt' and part=='down':name='corrupt_vertical_direct'
 clip=frames(name)
 return [clip[i] for i in jobs[name].get('selected',range(len(clip)))]
down=frames('blue_down');side=frames('blue_side');bridge=frames('blue_down_bridge');recover=frames('blue_recover')
if len(down)==9 and len(bridge)==9 and len(recover)==9:
 # Insert the actual descending positions without replacing the source windup
 # or impact. The native storm slam's7/16..12/16 window spans this new interval.
 # Reject the bridge's overshoot/return tail. Only monotonically descending
 # physical head positions enter the actual strike. Recovery omits its extra
 # above-head flourish and returns directly to the approved neutral stance.
 descent=down[:3]+bridge[1:3]+[down[3],bridge[3],down[4],down[7]]
 if endface:
  clip=strikeframes('blue','down');recovery=strikeframes('blue','recover')
  # Reject generated5/6: the cylinder collapses into a disc. Recovery2 adds
  # an unsolicited overhead flourish. Neither enters the live bank.
  descent=clip[1:] if vertical else [clip[i] for i in [1,2,3,4,7,8]]
  windup=[oldframe('blue_slam',i) for i in range(9)]+([clip[0]] if vertical else [])
  bank=windup+descent;art['blueSlam']={'windEnd':len(windup)-1,'strikeEnd':len(bank)-1,'recoverStart':len(bank)}
  # Lift back through the real waist/chest poses; discard the recovery job's
  # flattened disc and extra overhead flourish. Only its neutral endpoint ships.
  bank+=([clip[3],clip[2],recovery[-1]] if vertical else [recovery[i] for i in [1,3,4]])
 else:
  bank=[oldframe('blue_slam',i) for i in range(9)]+descent;art['blueSlam']={'windEnd':9,'strikeEnd':len(bank)-1,'recoverStart':len(bank)};bank+=[recover[i] for i in [1,2,3,7,8]]
 emit('blue_slam',bank,True);emit('blue_slam_armor',[chrome(im) for im in bank],True)
else:art['pending'].append('blue_down')
if len(side)==9:
 bank=[oldframe('blue_side',i) for i in range(6)]+side[1:]+[oldframe('blue_side',i) for i in range(12,17)];emit('blue_side',bank,True);emit('blue_side_armor',[chrome(im) for im in bank],True)
 # Native counter impact stays frame11, but its physical hammer now traverses
 # the full horizontal arc instead of skipping straight to an effects smear.
 order=[0,1,2,3,4,5,6,7,9,10,12,13,14,15,17,18]
 for direction,flip in [('right',False),('left',True)]:
  ims=[]
  for i in order:
   im=bank[i]
   if flip:im=ImageOps.mirror(im)
   ims.append(im)
  points=[[round(v*2.5) for v in tip(im,True)] for im in ims];large=[im.resize((640,640),Image.Resampling.NEAREST) for im in ims]
  rows=emit('blue_counter_'+direction,large,True,piv=[320,280],tips=points);emit('blue_counter_'+direction+'_armor',[chrome(im) for im in large],True,piv=[320,280],tips=points)
else:art['pending'].append('blue_side')
required=['idle','slam','side','charge','throw','spin','ball','shield','gun','unarmed','break','punch','fists','fire','dance','tool']
for name in required:
 ims=frames('corrupt_'+name)
 if name=='slam':
  raiseclip=frames('corrupt_raise_fixed');downclip=frames('corrupt_down_fixed');recoverclip=frames('corrupt_recover_fixed')
  ims=raiseclip+downclip[1:]+recoverclip[1:] if len(raiseclip)==5 and len(downclip)==9 and len(recoverclip)==5 else []
  art['corruptSlam']={'windEnd':4,'strikeEnd':12,'recoverStart':13}
  if endface:
   wind=raiseclip+(frames('corrupt_vertical_overhead') if vertical else [])
   motion=strikeframes('corrupt','down')
   if vertical and motion[-1].tobytes()!=frames('corrupt_vertical_key')[0].tobytes():motion+=[frames('corrupt_vertical_key')[0]]
   ims=wind+motion[1:];art['corruptSlam']={'windEnd':len(wind)-1,'strikeEnd':len(ims)-1,'recoverStart':len(ims)};ims+=strikeframes('corrupt','recover')[1:]
 if name=='ball':ims=frames('corrupt_ball_fixed')
 if name=='throw':
  follow=frames('corrupt_throw_fixed');ims=ims[:6]+follow[1:] if len(follow)==9 else []
 if name=='gun':
  clip=frames('corrupt_gun_fixed');ims=[clip[i] for i in [0,1,8]] if len(clip)==9 else []
 if name=='punch':
  clip=frames('corrupt_punch_fixed');ims=[clip[i] for i in [0,3,4]] if len(clip)==5 else []
 if name=='fire':ims=frames('corrupt_fire_key')
 if name=='fists':ims=ims[2:]
 if not ims:art['pending'].append('corrupt_'+name);continue
 # One shared32px pad on all frames; no per-frame resizing or silhouette fit.
 padded=[]
 for im in ims:
  assert im.size==(256,256),(name,im.size)
  box=im.getbbox();assert box and min(box[:2])>0 and max(box[2:])<256,(name,'source clipped',box)
  p=Image.new('RGBA',(320,320));p.alpha_composite(im,(32,32));padded.append(p)
 rows=emit('corrupt_'+name,padded)
 if name=='punch':
  # The authored extension is on image-left. The second native strike mirrors
  # the same physical motion; both fists have explicit source-space landmarks.
  for i,a in enumerate(rows):
   u=i/max(1,len(rows)-1);a['handR']=[round(115-23*u),round(177+4*u)];a['handL']=[205,167]
  left=emit('corrupt_punch_left',[ImageOps.mirror(im) for im in padded])
  for i,a in enumerate(left):
   source=rows[i];a['handR']=[320-source['handR'][0],source['handR'][1]];a['handL']=[320-source['handL'][0],source['handL'][1]]
 if name=='tool':
  for a in rows:a['_h22Tool']=True
 if name=='gun':
  # First frames draw the weapon; only the ready/recoil tail loops in combat.
  art['banks']['corrupt_gun_fire']=rows
  for a in rows:a['muzzle']=[262,218];a['gunAngle']=.43
  left=emit('corrupt_gun_left',[ImageOps.mirror(im) for im in padded])
  for a in left:a['muzzle']=[58,218];a['gunAngle']=math.pi-.43
# Physical head centres override colour detection where violet armour or a
# cyan motion spark is brighter than the weapon. Never anchor a hit to a trail.
for name in ([] if endface else ['corrupt_slam']):
 points={4:[160,62],5:[160,75],6:[160,158],7:[160,250],8:[160,262],9:[160,262],10:[160,262],11:[160,262],12:[160,262],13:[157,263]}
 for i,p in points.items():art['banks'][name][i]['tip']=p
for name in ([] if endface else ['blue_slam','blue_slam_armor']):
 for i,p in {13:[128,110],14:[128,174],15:[128,202],16:[128,211],17:[128,214]}.items():art['banks'][name][i]['tip']=p
if endface:
 art['endfaceImpact']=True
 art['straightDownImpact']=vertical
 if vertical:
  for name in ['blue_slam','blue_slam_armor']:
   for i,p in enumerate(jobs['blue_vertical_direct']['contacts']):art['banks'][name][9+i]['tip']=p
  # The selected central descent crosses the torso; colour detection there
  # would mistake violet leg armour for the hammer. Use its actual end cap.
  for i,p in {5:[128,78],6:[128,80],7:[128,110],8:[134,237]}.items():art['banks']['corrupt_slam'][i]['tip']=[v+32 for v in p]
 for name in ['blue_slam','blue_slam_armor','corrupt_slam']:
  m=art['corruptSlam' if name=='corrupt_slam' else 'blueSlam'];pad=32 if name=='corrupt_slam' else 0
  impact=next(j for j in endface_jobs if j['id']==('corrupt' if pad else 'blue')+('_vertical_key' if vertical else '_endface_key'))
  art['banks'][name][m['strikeEnd']]['tip']=[v+pad for v in impact['contact']]
  if vertical:art['banks'][name][m['strikeEnd']]['strikeAxisX']=impact['body_axis']+pad
for row in audit:row['tip']=art['banks'][row['bank']][row['frame']]['tip']
(W/'hammer_correction_art_1022.js').write_text('"use strict";\nconst H22_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');(W/'frame-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print(json.dumps({'banks':len(art['banks']),'cells':len(audit),'pending':art['pending'],'bytes':sum(p.stat().st_size for p in D.glob('*.webp'))}))
if '--install' in sys.argv:
 assert not endface_jobs or endface,'New end-face slams must finish together before installation.'
 assert not art['pending'],'Incomplete actor bank cannot replace a complete one.'
 target=R/'assets/game/shared/combat/hammer_correction_1022';target.mkdir(parents=True,exist_ok=True)
 for p in D.glob('*.webp'):shutil.copy2(p,target/p.name)
 for name in ['hammer_correction_art_1022.js','hammer_correction_1022.js','helicopter_identity_1022.js']:shutil.copy2(W/name,R/'assets'/name)
 index=R/'index.html';data=index.read_bytes();tag=b'<script src="assets/hammer_correction_art_1022.js?v=hammer-correction-1022-1"></script>\n<script src="assets/hammer_correction_1022.js?v=hammer-correction-1022-1"></script>\n'
 if b'hammer_correction_art_1022.js' not in data:index.write_bytes(data.replace(b'</body>',tag+b'</body>'))
 if endface:
  data=index.read_bytes().replace(b'hammer-correction-1022-1',b'hammer-endface-1022-2');index.write_bytes(data)
 if vertical:index.write_bytes(index.read_bytes().replace(b'hammer-endface-1022-2',b'hammer-vertical-1022-3'))
 print('Installed complete Hammer corrections only.')
