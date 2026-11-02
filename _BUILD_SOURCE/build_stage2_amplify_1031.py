"""Stage2 authored volcanic refit. Fixed even cells, shared pivots/scales.
Generated whole motion sheets remain source evidence. No production atlas edits.
Heading interpolation and FX orientations are exported, never rotated live.
"""
from pathlib import Path
import json, math, hashlib, shutil,sys
from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from scipy.ndimage import label,find_objects

R=Path(__file__).resolve().parents[1]
O=R/'assets/game/levels/stage_02/enemies/amplify_1031';O.mkdir(parents=True,exist_ok=True)
S=R/'_BUILD_SOURCE/stage2_amplify_1031';S.mkdir(exist_ok=True)
Q=R/'_shots/stage2_amplify_1031';Q.mkdir(exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
FILES={'interceptor':'exec-b56e1f38-b469-4a20-98f0-1ab5db8af5ba.png','skimmer':'exec-cc2050c4-df04-4e28-a041-27e86c12b076.png','wasp':'exec-993f5a00-4057-4890-bfa2-5db538a7fc20.png','thunder':'exec-230026a1-fddb-4277-9556-f7ecd3c71774.png','crucible':'exec-dc6d18d6-3809-4c10-9cc5-f0a43e9d9513.png','minelayer':'exec-6ae83672-ea54-40f9-ab14-a23472ce08a7.png','carrier':'exec-6b1f0cf0-813f-4a91-ab1d-935096fab5b1.png','snake':'exec-81f7f6f7-7834-4b8f-8009-3eaf4cc3f583.png','disc':'exec-3f50f0c0-3dcf-4cac-a4e2-bda1a0bc89e7.png','elite':'exec-b288c5e9-02c7-49d0-bd3c-c50c4000c903.png','ordnance':'exec-1a53cb88-a6fa-4ffd-ad4d-090e5ca4c3e8.png','maw':'exec-5d029b59-cd8f-4ab0-8c4d-ec2d9476d48f.png','pod':'exec-58a806c9-2d7b-40b6-ae10-a73a5019677c.png'}
META={'owner':'_BUILD_SOURCE/build_stage2_amplify_1031.py','tool':'built-in image_gen; existing approved PixelLab BF22 banks for Ash/Basalt','models':{},'banks':{},'sources':{}}
ORIGINS={}
OLD=json.loads((O/'manifest.json').read_text(encoding='utf-8'))if (O/'manifest.json').is_file()else{}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(p,n):return json.JSONDecoder().raw_decode((R/p).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
def clean(im):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]<18,0,np.minimum(255,a[:,:,3].astype('int16')*255//252)).astype('uint8');return Image.fromarray(a)
def read(n,rows):
 p=S/(n+'_source.png')
 if not p.exists():shutil.copyfile(G/FILES[n],p)
 im=clean(Image.open(p));sw,sh=im.width/4,im.height/rows
 w,h=math.ceil(sw/2)*2,math.ceil(sh/2)*2
 META['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'sourceCell':[w,h],'frames':4*rows}
 if n!='ordnance':
  ar=np.array(im);labels,count=label(ar[:,:,3]>80);parts=[]
  for i,s in enumerate(find_objects(labels),1):
   if s is not None:
    size=np.count_nonzero(labels[s]==i)
    if size>500:parts.append((size,s))
  parts=sorted(parts,reverse=True,key=lambda x:x[0])[:4*rows]
  if len(parts)==4*rows:
   parts=sorted(parts,key=lambda t:(t[1][0].start+t[1][0].stop)/2);ordered=[]
   for row in range(rows):ordered.extend(sorted(parts[row*4:row*4+4],key=lambda t:t[1][1].start))
   side=math.ceil((max(max(s[0].stop-s[0].start,s[1].stop-s[1].start)for _,s in ordered)+12)/2)*2;out=[];rects=[]
   for _,s in ordered:
    x,y=max(0,s[1].start-3),max(0,s[0].start-3);xx,yy=min(im.width,s[1].stop+3),min(im.height,s[0].stop+3);tile=im.crop((x,y,xx,yy));pad=Image.new('RGBA',(side,side));pad.alpha_composite(tile,((side-tile.width)//2,(side-tile.height)//2));out.append(pad);rects.append([x,y,xx-x,yy-y])
   x,y,ww,hh=rects[0];ORIGINS[n]=[side,side/2-(x+ww/2),side/2-(y+hh/2)];META['sources'][n]['componentRects']=rects;META['sources'][n]['sourceCell']=[side,side]
   return out
 out=[]
 for i in range(4*rows):
  x,y=round(i%4*sw),round(i//4*sh);xx,yy=round((i%4+1)*sw),round((i//4+1)*sh)
  tile=im.crop((x,y,xx,yy));pad=Image.new('RGBA',(w,h));pad.alpha_composite(tile,((w-tile.width)//2,(h-tile.height)//2));out.append(pad)
 return out
def padframes(frames,cell=160,span=142):
 # A shared scale across the entire bank, including roll and somersault.
 scale=span/max(max(im.getbbox()[2]-im.getbbox()[0],im.getbbox()[3]-im.getbbox()[1])for im in frames if im.getbbox())
 out=[]
 for im in frames:
  t=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);p=Image.new('RGBA',(cell,cell));p.alpha_composite(t,((cell-t.width)//2,(cell-t.height)//2));out.append(p)
 return out,scale
def bank(n,frames,cell=160,dirs=1,headings=False):
 if '--basalt-only'in sys.argv and not n.startswith('basalt_')and n in OLD.get('banks',{}):
  META['banks'][n]=OLD['banks'][n];return META['banks'][n]
 dirrows=2 if dirs*cell>16000 else 1
 rows=1 if headings else len(frames)*dirrows;cols=len(frames)if headings else dirs//dirrows
 out=Image.new('RGBA',(cell*cols,cell*rows))
 for i,im in enumerate(frames):
  assert im.size==(cell,cell)
  if headings:out.alpha_composite(im,(i*cell,0));continue
  pad=Image.new('RGBA',(cell*3,cell*3));pad.alpha_composite(im,(cell,cell))
  for d in range(dirs):out.alpha_composite(pad.rotate(-d*360/dirs,Image.Resampling.NEAREST,center=(cell*1.5,cell*1.5)).crop((cell,cell,cell*2,cell*2)),((d%cols)*cell,(i*dirrows+d//cols)*cell))
 p=O/(n+'.webp');buf=BytesIO();out.save(buf,format='WEBP',lossless=True,method=4);p.write_bytes(buf.getvalue())
 a=dict(key='v31_'+n,path=p.relative_to(R).as_posix(),cell=cell,pivot=[cell//2]*2,dirs=cols if headings else dirs,cols=cols,dirRows=1 if headings else dirrows,frames=1 if headings else len(frames),sha256=sha(p));META['banks'][n]=a;return a
def point(x,y,scale,src=256,c=160):return [round(c/2+(x-src/2)*scale,2),round(c/2+(y-src/2)*scale,2)]
SOCKETS={'interceptor':([[43,145],[110,187],[145,187],[211,145]],[[110,29],[155,29]]),'skimmer':([[110,220],[153,220]],[[88,38],[174,38]]),'wasp':([[103,190],[151,190]],[[97,57],[175,57]]),'thunder':([[104,210],[158,210]],[[110,25],[163,25]]),'crucible':([[113,196],[164,196]],[[99,33],[164,33]]),'minelayer':([[128,176]],[[48,66],[203,66]]),'carrier':([[123,187]],[[39,77],[219,77]]),'elite':([[109,200],[143,200]],[[106,27],[152,27]])}
for n in ['interceptor','skimmer','wasp','thunder','crucible','minelayer','carrier','elite']:
 raw=read(n,6);frames,scale=padframes(raw)
 # Correct generated diagonals that disagree with their requested direction.
 # Preserve four actually drawn cardinal views; bake8 subheadings per view.
 cardinal=[0,6,4,10]if n in ['wasp','minelayer']else[0,10,4,6];heading=[]
 for d in range(32):
  view=round(d/8)%4;delta=(d-round(d/8)*8)*360/32;t=frames[cardinal[view]]
  pad=Image.new('RGBA',(480,480));pad.alpha_composite(t,(160,160));heading.append(pad.rotate(-delta,Image.Resampling.NEAREST,center=(240,240)).crop((160,160,320,320)))
 M={'span':142,'banks':{'heading':bank(n+'_heading',heading,headings=True),'idle':bank(n+'_idle',[frames[0]]),'attack':bank(n+'_attack',[frames[1],*frames[20:24]],dirs=32),'drift':bank(n+'_drift',[frames[2],frames[3]],dirs=32),'roll':bank(n+'_roll',frames[12:16],dirs=32),'somer':bank(n+'_somer',frames[16:20],dirs=32),'charge':bank(n+'_charge',frames[20:24],dirs=32)},'source':META['sources'][n]}
 ss,dx,dy=ORIGINS.get(n,[256,0,0]);M['guns']=[point(x+dx,y+dy,scale,ss)for x,y in SOCKETS[n][0]];M['tails']=[point(x+dx,y+dy,scale,ss)for x,y in SOCKETS[n][1]];M['sourceScale']=scale
 META['models'][n]=M
 # Each source frame rendered over a neutral contact sheet, no source alpha lost.
 contact=Image.new('RGB',(160*4,184*6),(8,20,28));draw=ImageDraw.Draw(contact)
 for i,t in enumerate(frames):contact.paste(t,(i%4*160,i//4*184+20),t);draw.text((i%4*160+4,i//4*184+3),str(i),fill='white')
 contact.save(Q/(n+'-contact.jpg'),quality=90)

BF=data('assets/biome_fleet_art_1022.js','BF22_ART')
for n,model in [('ash','magma_dart'),('basalt','magma_forge')]:
 M=BF['models'][model];banks={}
 for kind,B in M['banks'].items():
  im=Image.open(R/B['path']).convert('RGBA');fs=[]
  for x,y,w,h in B['cells']:
   t=im.crop((x,y,x+w,y+h))
   if n=='basalt':
    ar=np.array(t);rgb=ar[:,:,:3].astype(float);lum=np.sum(rgb*[.2126,.7152,.0722],axis=2);hot=(rgb[:,:,0]>rgb[:,:,1]*1.4)&(rgb[:,:,0]>100)&(rgb[:,:,1]>40);mask=(ar[:,:,3]>0)&~hot&(lum>34)&(lum<226)
    target=(np.stack([lum*.83,lum*.89,lum*.96],axis=2)/(.2126*.83+.7152*.89+.0722*.96)).clip(0,255);ar[:,:,:3][mask]=target[mask].astype('uint8');t=Image.fromarray(ar)
   fs.append(t)
  banks[kind]=bank(n+'_'+kind,fs,128,8)
 # The full authored idle/attack/drift/roll/somer sequence stays available.
 banks['heading']=bank(n+'_heading',[fs[0]],128,32)
 # Heading must derive from the idle seed, not last-loop somersault.
 B=M['banks']['idle'];im=Image.open(R/B['path']).convert('RGBA');x,y,w,h=B['cells'][0];t=im.crop((x,y,x+w,y+h))
 if n=='basalt':
  ar=np.array(t);rgb=ar[:,:,:3].astype(float);lum=np.sum(rgb*[.2126,.7152,.0722],axis=2);hot=(rgb[:,:,0]>rgb[:,:,1]*1.4)&(rgb[:,:,0]>100);mask=(ar[:,:,3]>0)&~hot&(lum>34)&(lum<226);ar[:,:,:3][mask]=(np.stack([lum*.83,lum*.89,lum*.96],axis=2)/(.2126*.83+.7152*.89+.0722*.96)).clip(0,255)[mask].astype('uint8');t=Image.fromarray(ar)
 banks['heading']=bank(n+'_heading',[t],128,32)
 META['models'][n]={'span':M['span'],'banks':banks,'guns':[[45,104],[86,104]]if n=='ash'else[[39,96],[89,96]],'tails':[[49,34],[80,34]],'source':M['banks']}

for n in ['maw','pod','snake']:
 fs,scale=padframes(read(n,4),192,166);META['models'][n]={'span':166,'banks':{'sequence':bank(n+'_sequence',fs,192)},'guns':[[96,62]]if n=='maw'else[[96,96]],'tails':[]}

# Build the nine-spike disk from its actual generated core and one complete
# source spike. Explicit nine-piece authored assembly corrects generator's7.
fs=read('disc',4);src=fs[0];c=src.width;core=src.crop((round(c*.27),round(c*.27),round(c*.73),round(c*.73))).resize((88,88),Image.Resampling.NEAREST)
blade=src.crop((round(c*.39),0,round(c*.54),round(c*.38)));blade=blade.resize((28,71),Image.Resampling.NEAREST)
ds=[];mounts=[]
for i in range(32):
 t=Image.new('RGBA',(192,192));t.alpha_composite(core,(52,52));angles=[]
 for k in range(9):
  a=(k/9+i/32)*360;p=Image.new('RGBA',(384,384));p.alpha_composite(blade,(192-14,192-90));p=p.rotate(-a,Image.Resampling.NEAREST,center=(192,192));t.alpha_composite(p.crop((96,96,288,288)));angles.append([round(96+math.sin(math.radians(a))*82,3),round(96-math.cos(math.radians(a))*82,3),round(math.radians(a)-math.pi/2,6)])
 ds.append(t);mounts.append(angles)
META['models']['disc']={'span':180,'banks':{'spin':bank('disc_spin',ds,192)},'spikes':mounts,'source':META['sources']['disc']}

raw=read('ordnance',8)
for row,n in enumerate(['slug','thunder_slug','thunder_missile','orb','mine','laser','muzzle','thruster']):
 fs=raw[row*4:row*4+4];c=128
 if n=='laser':
  # Crop the actual central beam texture; export oriented segments, no stretch.
  fs=[im.crop((round(im.width*.38),0,round(im.width*.62),im.height))for im in fs]
 pfs,sc=padframes(fs,c,110)
 if n=='thunder_missile':pfs=[t.transpose(Image.Transpose.ROTATE_180)for t in pfs]
 if n=='laser':bank(n,[t.resize((64,64),Image.Resampling.NEAREST)for t in pfs],64,288)
 else:bank(n,pfs,c,32 if n not in ['orb','mine']else 1)
 if n=='thunder_missile':
  fire=[]
  for t in pfs:
   a=np.array(t);rgb=a[:,:,:3];mask=(rgb[:,:,2]>rgb[:,:,0]*1.3)&(rgb[:,:,2]>100);a[:,:,:3][mask]=a[:,:,:3][mask][:,[2,0,1]];fire.append(Image.fromarray(a))
  bank('fire_missile',fire,128,32)
# A source-derived flamethrower has no thruster nozzle pasted into its plume.
flames=[im.crop((round(im.width*.20),0,round(im.width*.80),round(im.height*.72))).transpose(Image.Transpose.ROTATE_180)for im in raw[28:32]]
pf,_=padframes(flames,256,220);bank('flamethrower',pf,256,32)

# Bake current actual turret heads into directional cells for fire aiming.
for weapon in ['laser','mg','missile']:
 p=R/('assets/game/shared/combat/enemy_overhaul_0925/sprites/ground_head_'+weapon+'.png');im=Image.open(p).convert('RGBA');fs,sc=padframes([im],192,166);bank('turret_'+weapon,fs,192,64)

(O/'manifest.json').write_text(json.dumps(META,indent=2)+'\n',encoding='utf-8')
(R/'assets/stage2_amplify_art_1031.js').write_text('"use strict";\nconst V31_ART='+json.dumps(META,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Exported',len(META['models']),'models,',len(META['banks']),'fixed banks; generator sources retained')
