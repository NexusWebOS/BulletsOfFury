"""Whole448x448 plates; fixed pixel pivot224,252, world scale512/342.
PixelLab animates one intact actor. Bake the SAME native hammer bitmap at the
tracked fist before export; no body sections and no held-tool geometry changes.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,distance_transform_edt,binary_dilation
import numpy as np,json,math,hashlib,sys
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/chronos_motion_1025';O=R/'assets/game/shared/combat/chronos_motion_1025';O.mkdir(exist_ok=True);S=R/'_shots/chronos_motion_1025';S.mkdir(exist_ok=True)
spec=json.loads((D/'motion-spec.json').read_text());seeds=json.loads((D/'seed-manifest.json').read_text());partial='--partial' in sys.argv
raw={};tracking=[]
def marker(a,expected):
 rgb=a[:,:,:3].astype(float);m=(rgb[:,:,0]>85)&(rgb[:,:,2]>85)&(rgb[:,:,0]>rgb[:,:,1]*1.8)&(rgb[:,:,2]>rgb[:,:,1]*1.8)&(a[:,:,3]>50);labs,n=label(m);c=[]
 for j in range(1,n+1):
  yy,xx=np.where(labs==j)
  if len(xx)>=3:c.append((sum((v-w)**2 for v,w in zip([xx.mean(),yy.mean()],expected)),[float(xx.mean()),float(yy.mean())],labs==j))
 if not c:return expected,None
 _,point,mask=min(c,key=lambda q:q[0]);return point,mask
def core(a):
 rgb=a[:,:,:3].astype(float);m=(rgb[:,:,1]>155)&(rgb[:,:,2]>180)&(rgb[:,:,0]<205)&(a[:,:,3]>50);labs,n=label(m);c=[]
 for j in range(1,n+1):
  yy,xx=np.where(labs==j);cx=float(xx.mean());cy=float(yy.mean())
  if len(xx)>=8 and xx.max()-xx.min()<35 and yy.max()-yy.min()<35 and abs(cx-128)<55 and abs(cy-116)<55:c.append(((cx-128)**2+(cy-116)**2,[cx,cy]))
 return min(c,key=lambda q:q[0])[1] if c else [128,116]
for q in spec:
 fs=sorted((D/'frames'/q['name']).glob('*.png'))
 if len(fs)!=q['frames']+1:
  if partial:continue
  raise RuntimeError('Incomplete PixelLab bank: '+q['name'])
 points=[];ims=[]
 for i,p in enumerate(fs):
  im=Image.open(p).convert('RGBA');assert im.size==(256,256);a=np.array(im);first=seeds.get(q['first'],seeds.get('motion_'+q['name'].split('_')[-1]+'_7'))['hand'];last=seeds.get(q['last'],None)
  if last:last=last['hand']
  else:last=[255-seeds['motion_'+q['name'].split('_')[-1]+'_7']['hand'][0],seeds['motion_'+q['name'].split('_')[-1]+'_7']['hand'][1]]
  u=i/(len(fs)-1);expected=[first[j]*(1-u)+last[j]*u for j in [0,1]];hand,mask=marker(a,expected)
  if mask is not None:
   _,indices=distance_transform_edt(mask,return_indices=True);a[mask]=a[indices[0][mask],indices[1][mask]]
  # PixelLab's fixed source canvas is the registration authority. Following a
  # bright cyan region can accidentally select a knee during a torso twist and
  # jerk the entire actor sideways. Preserve the authored motion and track only
  # the explicit fist marker; occluded markers interpolate the pinned sockets.
  if q['name'].startswith('palm_'):
   # PixelLab occasionally adds a floor matte beneath an otherwise clean
   # floating actor. Preserve both pinned boot silhouettes and discard this
   # non-actor scenery outside their shared padded lower-leg envelope.
   ends=[np.array(Image.open(D/'seeds'/(q[k]+'.png')).convert('RGBA'))[:,:,3]>30 for k in ['first','last']]
   lower=binary_dilation(ends[0]|ends[1],iterations=2);a[180:,:,3]=np.where(lower[180:],a[180:,:,3],0)
  shift=[0,0];aligned=Image.fromarray(a)
  # Track the registration dot, never a guessed weapon crop. Missing dots are
  # flagged for inspection rather than hidden behind a successful bank name.
  tracking.append({'bank':q['name'],'frame':i,'marker':mask is not None,'hand':hand,'reactorShift':shift});ims.append(aligned);points.append(hand)
 raw[q['name']]=(ims,points)
tool=Image.open(D/'refs/hammer-canonical.png').convert('RGBA');tool=tool.resize((342,342),Image.Resampling.NEAREST);wide=Image.new('RGBA',(512,512));wide.alpha_composite(tool,(85,85));tool=wide;GRIP=(256,85+382*342/512);HEAD=(256,256);WORLD=512/342
art={'frame':[448,448],'pixelPivot':[224,252],'worldScale':WORLD,'worldSize':[448*WORLD,448*WORLD],'banks':{},'sheets':{},'weapon':{'source':'_ART_SOURCES/chronos_motion_1025/refs/hammer-canonical.png','sha256':hashlib.sha256((D/'refs/hammer-canonical.png').read_bytes()).hexdigest(),'sourceGrip':[256,382],'sourceHead':[256,256],'scale':1,'authoringScale':342/512,'note':'Same source bitmap, one fixed scale and rigid rotation in every whole exported plate.'}}
contacts=[]
def bake(body,hand,theta,empty=False):
 base=Image.new('RGBA',(448,448));base.alpha_composite(body,(96,111));grip=[hand[0]+96,hand[1]+111];c=math.cos(theta);s=math.sin(theta);off=[-s*(HEAD[1]-GRIP[1]),c*(HEAD[1]-GRIP[1])];tip=[grip[0]+off[0],grip[1]+off[1]]
 if not empty:
  turned=tool.rotate(-theta*180/math.pi,resample=Image.Resampling.NEAREST,center=GRIP);at=(round(grip[0]-GRIP[0]),round(grip[1]-GRIP[1]));base.alpha_composite(turned,at)
  # A small authored hand aperture occludes the shaft at its actual grip.
  patch=Image.new('RGBA',(448,448));patch.alpha_composite(body,(96,111));mask=Image.new('L',(448,448));ImageDraw.Draw(mask).ellipse((grip[0]-10,grip[1]-10,grip[0]+10,grip[1]+10),fill=255);mask=np.minimum(np.array(mask),np.array(patch.getchannel('A')));patch.putalpha(Image.fromarray(mask));base.alpha_composite(patch)
 headbox=[tip[0]-34,tip[1]-34,tip[0]+34,tip[1]+34]
 return base,{'tip':[v*WORLD for v in tip],'grip':[v*WORLD for v in grip],'headBounds':[v*WORLD for v in headbox],'bounds':[v*WORLD for v in (base.getbbox() or (0,0,0,0))],'angle':theta,'empty':empty}
def angle(name,u):
 if name.startswith('strike'):return -.4+(math.pi-.2+.4)*u
 if name.startswith('windup'):return -math.pi/2-.12+(-.4+math.pi/2+.12)*u
 if name.startswith('retract'):return math.pi-.2+(-math.pi/2-.12+math.pi*2-math.pi+.2)*u
 if name.startswith('left'):return -math.pi/2-.12+(-math.pi*.75+math.pi/2+.12)*u
 if name.startswith('right'):return -math.pi/2-.12+(math.pi*.75+math.pi/2+.12)*u
 return -math.pi/2-.12
def export(name,frames):
 sheet=Image.new('RGBA',(448*4,448*math.ceil(len(frames)/4)));meta=[]
 for i,(im,m) in enumerate(frames):sheet.alpha_composite(im,(i%4*448,i//4*448));meta.append(m)
 for suffix in ['', '_hit']:
  out=sheet
  if suffix:out=Image.new('RGBA',sheet.size,'white');out.putalpha(sheet.getchannel('A'))
  path=O/(name+suffix+'.webp');out.save(path,lossless=True);art['sheets'][name+suffix]={'key':'nca_c27_'+name+suffix,'path':path.relative_to(R).as_posix()}
 art['banks'][name]={'sheet':'c27_'+name,'count':len(frames),'cols':4,'cell':[448,448],'frames':meta}
 contacts.extend([frames[0][0],frames[len(frames)//2][0],frames[-1][0]])
for name,(ims,hands)in raw.items():
 if name.startswith('shield_'):continue
 export(name,[bake(im,hands[i],angle(name,i/(len(ims)-1))) for i,im in enumerate(ims)])
for mat in ['regular','chrome']:
 if all(n+'_'+mat in raw for n in ['left','right']):
  fs=[]
  for i in range(32):
   u=i/32;side='left' if u<.5 else 'right';v=u*2 if u<.5 else (u-.5)*2;v=v*2 if v<.5 else 2-v*2;ims,hands=raw[side+'_'+mat];f=round(v*(len(ims)-1));fs.append(bake(ims[f],hands[f],-math.pi/2-.12+u*math.pi*2))
  export('spin_'+mat,fs)
 if 'strike_'+mat in raw:
  ims,hands=raw['strike_'+mat];export('throw_empty_'+mat,[bake(im,hands[i],0,True) for i,im in enumerate(ims)])
manifest=O/'manifest.json';manifest.write_text(json.dumps(art,indent=2)+'\n',encoding='utf8');(R/'assets/chronos_motion_art_1025.js').write_text('"use strict";\nconst C27_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(D/'tracking.json').write_text(json.dumps(tracking,indent=2)+'\n',encoding='utf8')
sheet=Image.new('RGBA',(448*6,448*math.ceil(len(contacts)/6)),(17,25,36,255))
for i,im in enumerate(contacts):sheet.alpha_composite(im,(i%6*448,i//6*448))
sheet.save(S/'baked-contact.png');print(json.dumps({'banks':len(art['banks']),'frames':sum(a['count'] for a in art['banks'].values()),'missingMarkers':sum(not q['marker'] for q in tracking),'trackingFrames':len(tracking),'partial':partial}),flush=True)

# Keep the approved rage palettes registered when rebuilding the source banks.
import runpy
runpy.run_path(str(R/'_BUILD_SOURCE/build_chronos_red_1025.py'))

# Last, preserve the corrected physical turns and overhead chromium animation.
runpy.run_path(str(R/'_BUILD_SOURCE/build_chronos_final_1025.py'))
