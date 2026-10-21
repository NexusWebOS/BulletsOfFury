from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import numpy as np,json,math,hashlib,zipfile,io
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';D=R/'assets/game/shared/final_effects_1021';D.mkdir(parents=True,exist_ok=True)
art={'sheets':{},'banks':{},'audit':[]}
def read(name):return [Image.open(p).convert('RGBA') for p in sorted((S/'raw'/name).glob('*.png'))]
def cleanfx(im,interior=False):
 a=np.array(im);rgb=a[:,:,:3].astype(float);mn=rgb.min(2);mx=rgb.max(2);gray=(mx-mn<28)&(mx>70)&(mx<195)
 a[gray,3]=0
 if interior:
  yy,xx=np.indices(a.shape[:2]);inner=(xx-128)**2+(yy-128)**2<86**2;a[inner,3]=(a[inner,3].astype(float)*.22).astype('uint8')
 return Image.fromarray(a)
def recolor(im,color):
 # Authored luminance and white specular peaks stay intact. Hue is an offline
 # palette operation, never a canvas allocation during a projectile draw.
 a=np.array(im);rgb=a[:,:,:3].astype(float)/255;v=rgb.max(2);lo=rgb.min(2);sat=np.divide(v-lo,np.maximum(v,.001));c=np.array(color,dtype=float)/255
 value=c[None,None,:]*v[:,:,None];white=np.clip((v-.78)/.22,0,1)*(1-sat*.55);out=value*(1-white[:,:,None])+v[:,:,None]*white[:,:,None]
 a[:,:,:3]=np.clip(out*255,0,255).astype('uint8');return Image.fromarray(a)
def tip(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);m=(a[:,:,3]>120)&(rgb[:,:,0]>110)&(rgb[:,:,2]>150)&(rgb[:,:,0]>rgb[:,:,1]*1.16)&((xx-128)**2+(yy-112)**2>40**2)
 z=np.pad(m.astype(float),((6,6),(6,6))).cumsum(0).cumsum(1);v=z[12:,12:]-z[:-12,12:]-z[12:,:-12]+z[:-12,:-12];y,x=np.unravel_index(v.argmax(),v.shape);return[int(x),int(y)]
def emit(name,ims,folder=D,pivot=(128,128),fps=18,tips=False):
 if not ims:return
 w,h=ims[0].size;assert w%2==0 and h%2==0 and all(im.size==(w,h) for im in ims)
 cols=min(8,len(ims));rows=math.ceil(len(ims)/cols);sheet=Image.new('RGBA',(cols*w,rows*h));bank=[];sheetid='fv21_'+name;key='nca_'+sheetid
 for i,im in enumerate(ims):
  bb=im.getbbox();bb=bb or (pivot[0],pivot[1],pivot[0],pivot[1]);x=i%cols*w;y=i//cols*h;sheet.alpha_composite(im,(x,y));a={'key':f'fv21_{name}_{i}','w':w,'h':h,'pivot':list(pivot),'bounds':list(bb),'cell':[x,y,w,h],'sheet':sheetid}
  if tips:a['tip']=tip(im)
  bank.append(a)
 folder.mkdir(parents=True,exist_ok=True);p=folder/(name+'.webp');sheet.save(p,lossless=True,method=6)
 for a in bank:a['path']=p.relative_to(R).as_posix()
 art['sheets'][sheetid]={'key':key,'path':p.relative_to(R).as_posix(),'w':sheet.width,'h':sheet.height}
 art['banks'][name]={'frames':bank,'fps':fps,'pivot':list(pivot),'w':w,'h':h};art['audit'].append({'bank':name,'frames':len(ims),'cell':[w,h],'pivot':pivot,'clipped':[i for i,a in enumerate(bank) if a['bounds'][0]<=0 or a['bounds'][1]<=0 or a['bounds'][2]>=w or a['bounds'][3]>=h]})
# The first large-figure slam has consistent armor scale. Reject its four
# oversized baked blast frames and bridge the two approved physical endpoints.
hammer=R/'assets/game/levels/stage_08/boss/hammer_final_1021'
for n in ['idle','spin','side','gun','unarmed','dance','fire','punch','fists','break','tool']:
 ims=read('corrupt_'+n)
 if n=='break':ims=ims[:13]+ims[14:]
 if n=='gun':
  emit('hammer_gun_left',[ImageOps.mirror(im) for im in ims],hammer,(128,112));
 emit('hammer_'+n,ims,hammer,(128,112),tips=n not in ['gun','unarmed','fire','punch','fists'])
slam=read('corrupt_slam');bridge=read('hammer_slam_bridge');
if slam and bridge:emit('hammer_slam',slam[:3]+bridge+slam[7:],hammer,(128,112),tips=True)
charge=read('hammer_charge_lift')
if charge:emit('hammer_charge',charge+charge[-2:0:-1],hammer,(128,112),tips=True)
ball=read('corrupt_ball')
if ball:
 im=ball[6];emit('hammer_ball',[im.rotate(-i*15,Image.Resampling.NEAREST,center=(128,112)) for i in range(24)],hammer,(128,112))
portal=read('portal_loop_safe')
if len(portal)==32:
 emit('portal',portal,R/'assets/game/levels/stage_05/effects/portal_only_1021',fps=16)
 emit('portal_blue',[recolor(im,[56,142,255]) for im in portal],R/'assets/game/levels/stage_05/effects/portal_only_1021',fps=16)
boss4=read('boss4_drift')
if len(boss4)==16:emit('boss4_drift',boss4,R/'assets/game/levels/stage_04/boss/drift_1021',fps=16/1.72)
wall=read('shield_wall_loop')
if len(wall)==16:emit('shield_wall',[im.crop((0,64,256,192)) for im in wall],R/'assets/game/levels/stage_05/boss/shield_wall_1021',pivot=(128,64),fps=16)
orb=read('nyx_orb_loop')
if len(orb)==24:
 keep=[0,1,2,6,7,8,9,10,11,12,13,14,16,17,22,23];orb=[orb[i] for i in keep]
 emit('nyx_orb',orb,R/'assets/game/levels/stage_06/boss/nyx/effects_1021',pivot=(64,64),fps=16)
 emit('wind_round',[recolor(im,[44,219,186]) for im in orb],R/'assets/game/levels/stage_06/boss/kaia/effects_1021',pivot=(64,64),fps=16)
hexes=read('shield_hex_loop');void=read('shield_void_loop')
hexes=[cleanfx(im,True) for im in hexes]
variants={'shield_hex':[70,225,255],'shield_volt':[70,135,255],'shield_fire':[255,91,36],'shield_toxic':[100,244,56],'shield_ice':[138,222,255],'shield_code':[195,70,255]}
for n,color in variants.items():emit(n,[recolor(im,color) for im in hexes],fps=18)
# Keep only the front-facing segment; reject the unrequested3D disk turn.
if void:
 yy,xx=np.indices((256,256));rim=np.clip((124-np.hypot(xx-128,yy-128))/5,0,1)
 selected=[]
 for i in [0,1,2,3,2,1]:
  a=np.array(void[i]);a[:,:,3]=(a[:,:,3].astype(float)*rim).astype('uint8');selected.append(Image.fromarray(a))
 emit('shield_void',selected,fps=10)
for name in ['explosion_star_burst','explosion_chain_burst']:
 ims=[cleanfx(im) for im in read(name)];last=max((i for i,im in enumerate(ims) if im.getbbox() and np.array(im)[:,:,3].sum()>4000),default=-1)
 emit(name,ims[:last+2],fps=30)
for pack,name in [('ColeForge_Explosions_FX_Vol1','fuel_tank_rupture'),('ColeForge_Explosions_FX_Vol1','implosion_collapse'),('ColeForge_Explosions_32bit','standard_eexplosions_04_smoke_core_blast')]:
 with zipfile.ZipFile(Path(r'C:\Users\Mike\Desktop\ColeForge-Packs')/(pack+'.zip')) as z:
  root=pack+'/Animations/'+name;meta=json.loads(z.read(root+'/animation.json'));files=sorted(p for p in z.namelist() if p.startswith(root+'/frames/') and p.endswith('.png'));ims=[Image.open(io.BytesIO(z.read(p))).convert('RGBA') for p in files]
  emit('pack_'+name,ims,pivot=(meta['pivot']['x'],meta['pivot']['y']),fps=1000/max(1,sum(meta['timing_ms'])/len(meta['timing_ms'])))
(D/'manifest.json').write_text(json.dumps(art,indent=2));(R/'assets/final_effects_art_1021.js').write_text('"use strict";\nconst FV21_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');(S/'export-audit.json').write_text(json.dumps(art['audit'],indent=2));print(json.dumps(art['audit']))
