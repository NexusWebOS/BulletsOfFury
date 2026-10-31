from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import numpy as np,json,math,hashlib
from scipy.ndimage import distance_transform_edt
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=W/'compiled';O.mkdir(exist_ok=True);A={}
def js(name):
 s=(R/name).read_text(encoding='utf-8');return json.loads(s[s.index('{'):s.rindex('}')+1])
def register(name,frames,pivot=None,cols=8,**meta):
 cw,ch=frames[0].size;assert cw%2==0 and ch%2==0 and all(f.size==(cw,ch)for f in frames)
 pivot=pivot or[cw//2,ch//2]
 # One union crop for the whole bank, never a per-frame trim. Every pose keeps
 # exactly the same logical pivot; only transparent atlas padding is removed.
 if name not in ['dark','red_flash','rearL','rearR','rearL_hit','rearR_hit']and not name.startswith('clean_'):
  boxes=[f.getbbox()for f in frames if f.getbbox()]
  if boxes:
   l=max(0,(min(b[0]for b in boxes)-2)//2*2);t=max(0,(min(b[1]for b in boxes)-2)//2*2);r=min(cw,math.ceil((max(b[2]for b in boxes)+2)/2)*2);b=min(ch,math.ceil((max(b[3]for b in boxes)+2)/2)*2)
   frames=[f.crop((l,t,r,b))for f in frames];pivot=[pivot[0]-l,pivot[1]-t];cw,ch=r-l,b-t
 sheet=Image.new('RGBA',(cw*cols,ch*math.ceil(len(frames)/cols)))
 for i,f in enumerate(frames):sheet.alpha_composite(f,((i%cols)*cw,(i//cols)*ch))
 sheet.save(O/(name+'.png'),optimize=True);A[name]={'key':'er28_'+name,'path':'assets/game/shared/combat/encounter_revision_1027/'+name+'.png','cw':cw,'ch':ch,'cols':cols,'frames':len(frames),'pivot':pivot,**meta}
def white(im):
 out=Image.new('RGBA',im.size,(255,255,255,0));out.putalpha(im.getchannel('A'));return out
def red(im):
 p=np.array(im);v=p[:,:,:3].astype(float);mx=v.max(2);mn=v.min(2);mask=(mx-mn>22)&(mx>35)&(p[:,:,3]>0)&(v[:,:,0]<v[:,:,2]*1.15)
 y=v[:,:,0]*.2126+v[:,:,1]*.7152+v[:,:,2]*.0722;scale=np.minimum(255,y/(.2126+.7152*.18+.0722*.23));target=np.stack([scale,scale*.18,scale*.23],axis=2)
 p[:,:,:3]=np.where(mask[:,:,None],target,v).astype(np.uint8);return Image.fromarray(p)
def fit(im,w,h):
 k=min(w/im.width,h/im.height);return im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.Resampling.NEAREST)
def rotation(name,srcs,size,pivot=(.5,.5),angles=64,world=None):
 # Each source has one proportional world scale and one common mounting pivot.
 frames=[]
 for src in srcs:
  src=src.convert('RGBA');src=fit(src,*(world or src.size));c=Image.new('RGBA',(size,size));c.alpha_composite(src,(round(size/2-src.width*pivot[0]),round(size/2-src.height*pivot[1])))
  for i in range(angles):frames.append(c.rotate(-i*360/angles,resample=Image.Resampling.NEAREST))
 register(name,frames,angles=angles,cycles=len(srcs));register(name+'_hit',[white(f)for f in frames],angles=angles,cycles=len(srcs))
for name,size in [('death_ball',128),('pentagram',128),('tornado',384),('nuke',512),('head_rage',108),('head_grin',108),('lightning',512),('code_round',32)]:
 frames=[]
 for f in range(1,17):
  im=red(Image.open(W/'generated'/name/(str(f).zfill(2)+'.png')).convert('RGBA'))
  if name=='lightning':
   from PIL import ImageFilter
   im=im.resize((128,512),Image.Resampling.NEAREST);mask=im.getchannel('A');out=Image.new('RGBA',im.size)
   for color,alpha in [((125,0,23),mask.filter(ImageFilter.MaxFilter(11))),((255,18,36),mask.filter(ImageFilter.MaxFilter(7))),((255,230,213),mask.filter(ImageFilter.MaxFilter(3)))]:
    layer=Image.new('RGBA',im.size,(*color,0));layer.putalpha(alpha);out.alpha_composite(layer)
   cell=Image.new('RGBA',(512,512));cell.alpha_composite(out,(192,0));im=cell
  else:im=im.resize((size,size),Image.Resampling.NEAREST)
  if name=='pentagram':
   # Legible original bitmap code, baked into each phase rather than browser text.
   fontroot=W.parent/'BOF-Pixelmap-Fonts-1027/fonts'
   if not fontroot.exists():fontroot=R/'assets/game/shared/ui/pixelmap_fonts_1027'
   fm=json.loads((fontroot/'command_ember.json').read_text());fi=Image.open(fontroot/'command_ember.png').convert('RGBA')
   bits='01000110010101010101001001011001'
   for row in range(3):
    for col in range(5):
     if row*5+col>f:continue
     bit=bits[(row*5+col+f//4)%len(bits)];g=fm['glyphs'][str(ord(bit))];im.alpha_composite(fi.crop((g['x'],g['y'],g['x']+g['w'],g['y']+g['h'])),(47+col*7,45+row*12))
  if name=='nuke':
   u=(f-1)/15;scale=(.12+.88*min(1,u/.60))*(408/512);small=im.resize((round(size*scale/2)*2,)*2,Image.Resampling.NEAREST);im=Image.new('RGBA',(size,size));im.alpha_composite(small,((size-small.width)//2,(size-small.height)//2))
   if u>.70:
    a=np.array(im);a[:,:,3]=(a[:,:,3].astype(float)*max(0,(1-u)/.30)).astype(np.uint8);im=Image.fromarray(a)
  frames.append(im)
 register(name,frames,pivot=[54,88]if name.startswith('head')else None,cols=4)
 if name.startswith('head'):register(name+'_hit',[white(f)for f in frames],pivot=[54,88],cols=4)
# Actual Dredger/Warden gun pixels, barrel recoil and 64 fixed angular poses.
for name,src,w,h in [('tank_gun','tank_1',67,105),('warden_gun','warden_5',38,84)]:
 im=Image.open(W/'source'/(src+'.png')).convert('RGBA');rows=[]
 for f in range(4):
  cell=Image.new('RGBA',im.size);cell.alpha_composite(im,(0,[-0,4,2,0][f]));rows.append(cell)
 rotation(name,rows,160,world=(w,h))
pods=[Image.open(W/'source'/('arch_blaster_gun_'+str(f)+'.png'))for f in range(4)]
rotation('rook_pod',pods,88,pivot=(.5,.12),world=(64,38))
pf=js('assets/performance_finish_art_1020.js')['carrier_turret'];pi=Image.open(R/pf['path']).convert('RGBA');srcs=[]
for i in [0,5,9,14]:
 x,y,w,h=pf['cells'][i];srcs.append(pi.crop((x,y,x+w,y+h)))
rotation('carrier_turret',srcs,116,pivot=(.5,60/160),world=(38*1.45,47.5*1.45))
# Native four hull gun assemblies. Clean only the tiny original gun rectangles
# on the substrate, then mount their separated native pixel components above it.
metadata=json.loads((W/'source/metadata.json').read_text());hh=metadata['hh']
for key in ['whv_closed_w','whv_open_w']:
 im=Image.open(W/'source'/(key+'.png')).convert('RGBA');p=np.array(im);mask=np.zeros(p.shape[:2],dtype=bool)
 for a in hh['frames']:
  x,y,w,h=a['sourceRect'];mask[y:y+h,x:x+w]=True
 # Nearest authored neighboring substrate pixels; original images are preserved.
 _,indices=distance_transform_edt(mask,return_indices=True);p[mask]=p[indices[0][mask],indices[1][mask]];clean=Image.fromarray(p)
 register('clean_'+key,[clean],pivot=[im.width//2,im.height//2],cols=1)
for i,a in enumerate(hh['frames']):
 im=Image.open(R/a['path']).convert('RGBA');srcs=[]
 for dy in [0,2,1,0]:
  q=Image.new('RGBA',im.size);q.alpha_composite(im,(0,dy));srcs.append(q)
 rotation('hull_gun_'+str(i),srcs,80,world=(a['w']*.9*1.45,a['h']*.9*1.45))
# Flipped rear legs retain the exact source alpha and a measured flipped pivot.
for name in ['rearL','rearR']:
 rows=metadata['legs'][name]['frames'];frames=[ImageOps.flip(Image.open(W/'source'/(r['key']+'.png')).convert('RGBA'))for r in rows]
 register(name,frames,cols=4);register(name+'_hit',[white(f)for f in frames],cols=4)
 k=metadata['legs'][name]['worldScale'];rows=[fit(f,256*k,256*k)for f in frames];size=224;out=[];angle=-.60 if name=='rearL'else.60
 for im in rows:
  c=Image.new('RGBA',(size,size));c.alpha_composite(im,((size-im.width)//2,(size-im.height)//2));out.append(c.rotate(-math.degrees(angle),Image.Resampling.NEAREST))
 register(name+'_fixed',out,cols=4);register(name+'_fixed_hit',[white(f)for f in out],cols=4)
for name in ['frontL','frontR']:
 frames=[];row=metadata['legs'][name];k=row['worldScale'];size=224
 for f in row['frames']:
  im=fit(Image.open(W/'source'/(f['key']+'.png')).convert('RGBA'),256*k,256*k);c=Image.new('RGBA',(size,size));c.alpha_composite(im,((size-im.width)//2,(size-im.height)//2))
  for a in range(17):frames.append(c.rotate(-math.degrees(-.8+a*.1),Image.Resampling.NEAREST))
 register(name+'_swat',frames,angles=17,cycles=8);register(name+'_swat_hit',[white(f)for f in frames],angles=17,cycles=8)
# Source-derived 1015 emission: brighten only existing green liquid pixels.
for name,src,size in [('core','body_0',(168,198)),('canister','warden_6',(46,88))]:
 im=Image.open(W/'source'/(src+'.png')).convert('RGBA');im=fit(im,*size);cell=Image.new('RGBA',(size[0]+size[0]%2,size[1]+size[1]%2));cell.alpha_composite(im,((cell.width-im.width)//2,(cell.height-im.height)//2));p=np.array(cell);v=p[:,:,:3].astype(float)
 green=(v[:,:,1]>v[:,:,0]*1.22)&(v[:,:,1]>v[:,:,2]*1.12)&(v[:,:,1]>48)&(p[:,:,3]>0);frames=[]
 for i in range(16):
  strength=.5+.5*math.sin(i*math.tau/16);q=p.copy();light=np.minimum(255,v*(1+.55*strength)+np.array([8,38,3])*strength);q[:,:,:3]=np.where(green[:,:,None],light,v).astype(np.uint8);frames.append(Image.fromarray(q))
 register(name,frames,cols=4);register(name+'_hit',[white(f)for f in frames],cols=4)
# Native toxic weapon pixels, proportionally sized around their existing pivot.
ea=js('assets/element_arsenal_art_1011.js')['banks']['toxic_round'];im=Image.open(R/ea['path']).convert('RGBA');rounds=[]
for r in ea['frames']:
 x,y,w,h=r;rounds.append(im.crop((x,y,x+w,y+h)))
rotation('toxic_slug',rounds,48,pivot=(.5,48/128),world=(32,32))
im=Image.open(R/'assets/game/levels/stage_07/stage/stage7_modular_0927/toxic_orb_8.png').convert('RGBA');w,h=im.width//4,im.height//2;frames=[]
for f in range(16):
 i=f%8;q=fit(im.crop((i%4*w,i//4*h,(i%4+1)*w,(i//4+1)*h)),32,32);c=Image.new('RGBA',(40,40));c.alpha_composite(q,((40-q.width)//2,(40-q.height)//2));frames.append(c)
register('toxic_orb',frames,cols=4)
# Special attack poses preserve the native Herald part silhouette and socket.
hd=js('assets/herald_art_1003f.js');im=Image.open(R/hd['path']).convert('RGBA')
for name,p in hd['parts'].items():
 if name=='head':continue
 x,y,w,h=p['rect'];q=im.crop((x,y,x+w,y+h));k=p['scale'];q=fit(q,w*k,h*k);size=384 if name.startswith('wing')else 288 if name.startswith('gun')else 256
 c=Image.new('RGBA',(size,size));c.alpha_composite(q,(round(size/2-p['pivot'][0]*k),round(size/2-p['pivot'][1]*k)))
 angles=[-.9+i*.06 for i in range(31)]if name.startswith(('wing','gun'))else[0];frames=[c.rotate(-math.degrees(a),Image.Resampling.NEAREST)for a in angles]
 register('herald_'+name,frames,cols=4,angleMin=angles[0],angleStep=.06,cycles=1);register('herald_'+name+'_hit',[white(f)for f in frames],cols=4,angleMin=angles[0],angleStep=.06,cycles=1)
# Authored scenery-only darkness and red flashes, fixed tiles with baked alpha.
veils=[]
for i in range(16):veils.append(Image.new('RGBA',(64,64),(0,0,0,round(i/15*170))))
register('dark',veils,cols=4)
register('red_flash',[Image.new('RGBA',(64,64),(170,0,8,a))for a in [0,20,45,75,45,20,0,0,0,15,35,60,35,15,0,0]],cols=4)
(O/'manifest.json').write_text(json.dumps(A,indent=2));(W/'encounter_revision_art_1027.js').write_text('"use strict";\nconst ER28_ART='+json.dumps(A,separators=(',',':'))+';\n')
print('Built',len(A),'authored banks',flush=True)
