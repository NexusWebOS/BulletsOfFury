"""Register PixelLab Furnace poses on one physical skull / eye mounting point.

Only transparent padding and integer translation are applied to head pixels.
All generated poses retain one common scale; the three actual lamp clusters
measure roll and physical center. The native renderer uses these same eyes.
"""
from pathlib import Path
from itertools import permutations
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/furnace_pixellab_1017'
OUT=ROOT/'assets/game/shared/combat/furnace_pixellab_1017'
QA=ROOT/'_shots/furnace_pixellab_1017/export'
OUT.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)

def components(im):
 a=np.asarray(im);mask=(a[:,:,0]>225)&(a[:,:,1]>150)&(a[:,:,2]<210)&(a[:,:,3]>150)
 h,w=mask.shape;result=[]
 for y,x in zip(*np.where(mask)):
  if not mask[y,x]:continue
  mask[y,x]=False;stack=[(x,y)];points=[]
  while stack:
   xx,yy=stack.pop();points.append((xx,yy))
   for nx,ny in ((xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)):
    if 0<=nx<w and 0<=ny<h and mask[ny,nx]:mask[ny,nx]=False;stack.append((nx,ny))
  if len(points)>5:result.append((len(points),np.array(points).mean(0)))
 return sorted(result,key=lambda q:-q[0])[:14]

REFERENCE=np.array([[92.51,133.46],[158.20,133.50],[125.88,94.14]])-128
P=REFERENCE-REFERENCE.mean(0)
def wrap(a):return (a+math.pi)%(2*math.pi)-math.pi
def upright(im):
 a=np.asarray(im);y,x=np.indices(a.shape[:2]);lamps=[]
 for cx,cy in REFERENCE+128:
  mask=((x-cx)**2+(y-cy)**2<13**2)&(a[:,:,0]>230)&(a[:,:,1]>180)&(a[:,:,3]>200)
  yy,xx=np.where(mask);assert len(xx)>8,'Upright eye/lens lost'
  lamps.append([float(xx.mean()),float(yy.mean())])
 Q=np.array(lamps);center=(Q-REFERENCE).mean(0)
 error=float(np.sqrt(np.mean(np.sum((REFERENCE+center-Q)**2,axis=1))))
 return dict(score=error,error=error,angle=0,center=center.tolist(),eyes=Q[:2].tolist(),lamps=lamps,
  eyeSpan=float(np.linalg.norm(Q[1]-Q[0])),components=[],method='fixed lamp windows, includes white cores')
def register(im,expected):
 cs=components(im);best=None
 for combo in permutations(range(len(cs)),3):
  Q=np.array([cs[i][1] for i in combo]);q=Q-Q.mean(0)
  angle=math.atan2(float(np.sum(P[:,0]*q[:,1]-P[:,1]*q[:,0])),float(np.sum(P*q)))
  c,s=math.cos(angle),math.sin(angle);R=np.array([[c,s],[-s,c]])
  center=Q.mean(0)-REFERENCE.mean(0)@R
  fit=REFERENCE@R+center;error=float(np.sqrt(np.mean(np.sum((fit-Q)**2,axis=1))))
  score=error+abs(wrap(angle-expected))*7
  if best is None or score<best['score']:
   best={'score':score,'error':error,'angle':angle%(2*math.pi),'center':center.tolist(),'eyes':Q[:2].tolist(),'lamps':Q.tolist(),
    'eyeSpan':float(np.linalg.norm(Q[1]-Q[0])),'components':[int(cs[i][0]) for i in combo]}
 assert best is not None,'No visible eye lamps'
 return best

def read(name,keep_input=False):
 paths=sorted((SRC/'returned'/name).glob('frame_*.png'));assert paths,name
 images=[Image.open(p).convert('RGBA') for p in paths]
 if not keep_input and len(images) in [9,17,41]:images=images[1:];paths=paths[1:]
 assert len({im.size for im in images})==1,(name,'nonuniform source canvas')
 return list(zip(paths,images))

def save(key,im,pivot,**extra):
 assert im.width%2==im.height%2==0
 path=OUT/(key+'.png');im.save(path,optimize=True)
 return dict(key=key,path=path.relative_to(ROOT).as_posix(),w=im.width,h=im.height,pivot=list(pivot),**extra)

def glow(im,lamps):
 a=np.asarray(im).copy();y,x=np.indices(a.shape[:2]);roi=np.zeros(a.shape[:2],bool)
 for lx,ly in lamps:roi|=(x-lx)**2+(y-ly)**2<16**2
 m=roi&(a[:,:,0]>175)&(a[:,:,1]>65)&(a[:,:,3]>100)
 alpha=np.where(m,a[:,:,3],0).astype('uint8');core=Image.fromarray(alpha)
 result=Image.new('RGBA',im.size)
 # Hard stepped spill is derived only from each pose's own eye/lens pixels.
 for size,strength in [(7,.08),(5,.11),(3,.18),(1,.35)]:
  ring=core.filter(ImageFilter.MaxFilter(size))
  # Spill carries the local fire hue even outside an opaque lens pixel.
  tint=Image.new('RGBA',im.size,(255,139,22,0));tint.putalpha(ring.point(lambda v:round(v*strength)));result=Image.alpha_composite(result,tint)
 return result

art={};audit={}
for bank,count in [('spin',30),('charge',17)]:
 entries=[entry for quarter in range(4) for entry in read('head-turn-'+str(quarter))
  if (entry[0].parent.name,entry[0].name) not in [('head-turn-1','frame_006.png'),('head-turn-2','frame_006.png')]] if bank=='spin' else read('head-charge',keep_input=True)
 assert len(entries)==count,(bank,len(entries))
 frames=[];records=[];contact=Image.new('RGBA',(320*8,344*math.ceil(count/8)),(11,17,24,255));d=ImageDraw.Draw(contact)
 for i,(source,im) in enumerate(entries):
  expected=(int(source.parent.name[-1])+int(source.stem[-3:])/8)*math.pi/2 if bank=='spin' else 0
  reg=register(im,expected) if bank=='spin' else upright(im);dx,dy=[round(160-v) for v in reg['center']]
  padded=Image.new('RGBA',(320,320));padded.paste(im,(dx,dy))
  eyes=[[round(x+dx,3),round(y+dy,3)] for x,y in reg['eyes']];lamps=[[x+dx,y+dy] for x,y in reg['lamps']]
  key=f'f17_{bank}_{i:02d}';a=save(key,padded,(160,160),eyes=eyes,angle=reg['angle'] if bank=='spin' else 0)
  g=save(key+'_glow',glow(padded,lamps),(160,160));a.update(glowKey=g['key'],glowPath=g['path']);frames.append(a)
  records.append(dict(source=source.relative_to(SRC).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),translation=[dx,dy],**reg))
  ox=(i%8)*320;oy=(i//8)*344;contact.alpha_composite(padded,(ox,oy));d.text((ox+8,oy+320),f'{i:02d}  {reg["angle"]*180/math.pi:.1f} deg / err {reg["error"]:.2f}',fill='#ced8e8')
  for x,y in eyes:d.ellipse((ox+x-3,oy+y-3,ox+x+3,oy+y+3),outline='#53f9a7')
 # Keep source time order in the audit, but choose the nearest measured roll
 # at runtime rather than assuming equal angular progress from the model.
 art[bank]={'frames':frames};audit[bank]=records;contact.convert('RGB').save(QA/(bank+'-contact.png'))
 onion=Image.new('RGBA',(320,320));onionAligned=Image.new('RGBA',(320,320))
 for a in frames:
  plate=Image.open(ROOT/a['path']).convert('RGBA');plate.putalpha(plate.getchannel('A').point(lambda v:round(v*.10)))
  onion=Image.alpha_composite(onion,plate)
  aligned=plate.rotate(math.degrees(a['angle']),resample=Image.Resampling.NEAREST,center=(160,160))
  onionAligned=Image.alpha_composite(onionAligned,aligned)
 onion.save(QA/(bank+'-onion.png'));onionAligned.save(QA/(bank+'-registered-onion.png'))
 assert max(q['error'] for q in records)<4,(bank,'lamp registration exceeded4px')
 assert min(q['eyeSpan'] for q in records)>60 and max(q['eyeSpan'] for q in records)<72,(bank,'head proportions drifted')
 if bank=='spin':
  angles=sorted(q['angle'] for q in records);gaps=[(b-a)%(2*math.pi) for a,b in zip(angles,angles[1:]+[angles[0]])]
  assert max(gaps)<math.pi/6,('rotation lacks continuous angular coverage',max(gaps)*180/math.pi)

laser=[];roots=[];tips=[];records=[]
for i,(source,im) in enumerate(read('eye-laser')):
 assert im.size==(64,256),im.size
 # The source model added a small grey ornament below the real ignition flare.
 # A common fixed crop removes it from every frame; no beam pixels are fitted.
 # Shared module rectangles keep root, body and tip at one proportional
 # scale. Only the straight body repeats; its last instance is clipped,
 # never stretched. The unwanted grey ornament remains outside all crops.
 laser.append(save(f'f17_laser_{i:02d}',im.crop((0,96,64,192)),(30,96)))
 roots.append(save(f'f17_laser_root_{i:02d}',im.crop((0,188,64,220)),(30,26)))
 tips.append(save(f'f17_laser_tip_{i:02d}',im.crop((0,0,64,40)),(30,7)))
 records.append({'source':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'bodyRect':[0,96,64,192],'rootRect':[0,188,64,220],'tipRect':[0,0,64,40]})
assert len(laser)==16
art['laser']={'frames':laser};art['laser_root']={'frames':roots};art['laser_tip']={'frames':tips};audit['laser']=records
audit['rejected']={'head-spin':'Yawed, hid both eyes for part of the turn.','head-turn-1/frame_006.png':'Sudden dark exposure.','head-turn-2/frame_006.png':'Lost glowing eye lenses.'}
(ROOT/'assets/furnace_head_art_1017.js').write_text('"use strict";\nconst F17_ART='+json.dumps(art,separators=(',',':'))+';\n',newline='\n')
(SRC/'export_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print('EXPORTED',sum(len(v['frames']) for v in art.values()),'primary frames; fixed head320x320; proportional laser modules64x96/32/40; source scale1')
