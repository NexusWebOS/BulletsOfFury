"""Source-owned Furious Razorwake/Thunderhead art. Fixed cells, actual roll views,
prebaked heading cells, disjoint gun pieces and source-pixel water/wind emission.
The selected October31 concept identities stay in PROMPTS.md and source PNGs.
"""
from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,math,hashlib,sys
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/furious_encounters_1102'
D=R/'assets/game/levels/stage_06/boss/furious_1102';D.mkdir(parents=True,exist_ok=True)
O=R/'_shots/furious_encounters_1102';O.mkdir(exist_ok=True)
M=dict(owner='_BUILD_SOURCE/build_furious_encounters_1102.py',banks={},models={},sources={})
def clean(im,threshold=35):
 a=np.array(im.convert('RGBA'));a[a[:,:,3]<threshold]=0;return Image.fromarray(a)
def bank(name,frames,dirs=1):
 w,h=frames[0].size;assert not w%2 and not h%2 and all(f.size==(w,h)for f in frames)
 cols=min(16,8192//w);rows=math.ceil(len(frames)/cols);assert rows*h<=16384
 out=Image.new('RGBA',(cols*w,rows*h))
 for i,f in enumerate(frames):out.alpha_composite(f,(i%cols*w,i//cols*h))
 p=D/(name+'.webp');out.save(p,lossless=True,method=4)
 B=dict(key='fb112_'+name,path=p.relative_to(R).as_posix(),cell=w,cols=cols,frames=len(frames)//dirs,dirs=dirs,sha256=hashlib.sha256(p.read_bytes()).hexdigest());M['banks'][name]=B;return B
def heading(frames,dirs=32):
 return[f.rotate(-360*d/dirs,resample=Image.Resampling.BICUBIC,center=(f.width/2,f.height/2))for f in frames for d in range(dirs)]
def white(f):
 x=Image.new('RGBA',f.size,'white');x.putalpha(f.getchannel('A'));return x
def charred(f):
 a=np.array(f);lum=a[:,:,:3].max(2).astype(float);a[:,:,:3]=np.stack([lum*.16,lum*.19,lum*.21],axis=2).astype('uint8');return Image.fromarray(a)
def flow(f,phase):
 a=np.array(f);rgb=a[:,:,:3].astype(float);lum=rgb.max(2);y,x=np.mgrid[:f.height,:f.width]
 energy=(rgb[:,:,1]>rgb[:,:,0]*1.12)&(rgb[:,:,2]>rgb[:,:,0]*1.1)&(a[:,:,3]>35)
 pulse=(.35+.65*(np.sin(y*.13+x*.07-phase*math.pi/2)*.5+.5))*energy
 out=np.zeros_like(a);out[:,:,:3]=[81,224,255];out[:,:,3]=(np.minimum(220,lum*pulse*.85)).astype('uint8')
 return Image.fromarray(out)
def normalized(im,canvas=512,scale=1,anchor=None):
 c=Image.new('RGBA',(canvas,canvas));anchor=anchor or(im.width/2,im.height/2);w=round(im.width*scale);h=round(im.height*scale)
 c.alpha_composite(im.resize((w,h),Image.Resampling.NEAREST),(round(canvas/2-anchor[0]*scale),round(canvas/2-anchor[1]*scale)));return c
def metadata(data):
 for p in data['models']['razor']['guns']:p['recoilOffset']=-4*1.05
 for p in data['models']['thunder']['guns']:p['recoilOffset']=-7*.58
 B=data['banks']['razor_body'];a=np.array(Image.open(R/B['path']).convert('RGBA').crop((0,0,B['cell'],B['cell'])));rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>80)&(rgb[:,:,1]>rgb[:,:,0]*1.1)&(rgb[:,:,2]>rgb[:,:,0]*1.05);yy,xx=np.where(mask)
 ports=[]
 for x,y in[(128,217),(385,217)]:
  j=np.argmin((xx-x)**2+(yy-y)**2);ports.append([int(xx[j]),int(yy[j])])
 data['models']['razor']['shear']=ports
 return data
def write(data):
 (D/'manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');(R/'assets/furious_encounters_art_1102.js').write_text('"use strict";\nconst FB112_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
 t=R/'assets/data/ART_TAXONOMY.json';taxonomy=json.loads(t.read_text(encoding='utf-8'));before={k:v for k,v in taxonomy.items()if k!='fb112_'};taxonomy['fb112_']=dict(role='furious_stage6_razorwake_and_thunderhead_whole_hulls_registered_weapons_and_storm_fx',owner='_BUILD_SOURCE/build_furious_encounters_1102.py',manifest=(D/'manifest.json').relative_to(R).as_posix(),note='Furious left route only; native right-hand Rough Riders and Stage X retained. Whole true-depth roll plates; disjoint rotary guns and pressure projectors, solid charred wrecks, source-pixel emission, measured ports and muzzle recoil. Generated tornado/hurricane/electric burst banks. Stage2-5 concepts are uninstalled proposals.')
 assert{k:v for k,v in taxonomy.items()if k!='fb112_'}==before;t.write_text(json.dumps(taxonomy,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if '--metadata-only'in sys.argv:
 write(metadata(json.loads((D/'manifest.json').read_text(encoding='utf-8'))));print('Registered measured shear/recoil sockets and taxonomy; all banks retained');sys.exit()

raw=clean(Image.open(S/'razorwake_source.png'));cells=[]
for i in range(8):
 x0=round(i%4*raw.width/4);x1=round((i%4+1)*raw.width/4);y0=round(i//4*raw.height/2);y1=round((i//4+1)*raw.height/2)
 cells.append(raw.crop((x0,y0,x1,y1)))
k=1.05;unit=normalized(cells[0],512,k,anchor=(222,222))
# The two actual rotary pods are disjoint crops. Their roots and mouths stay
# registered to their source coordinates; no renderer rotates a static plate.
boxes=[(115,202,170,295),(273,202,328,295)];mounts=[(143,216),(300,216)];bores=[(143,285),(300,285)]
rollboxes=[boxes,boxes,boxes,boxes,[(142,164,207,282),(240,144,296,256)],[(194,174,247,301),(196,174,249,301)],[(151,145,208,259),(244,171,302,289)],[(115,202,170,295),(273,202,328,295)]]
body=[]
for f,rects in zip(cells,rollboxes):
 z=f.copy()
 for rect in rects:z.paste((0,0,0,0),rect)
 body.append(normalized(z,512,k,anchor=(222,222)))
body=body+[body[6].transpose(Image.Transpose.FLIP_LEFT_RIGHT),body[5].transpose(Image.Transpose.FLIP_LEFT_RIGHT),body[4].transpose(Image.Transpose.FLIP_LEFT_RIGHT)]
bank('razor_body',heading(body[:4]),32);bank('razor_hit',heading([white(f)for f in body[:4]]),32)
bank('razor_flow',heading([flow(body[0],i)for i in range(4)]),32)
# Depth rolls use the whole generated craft. Burned gun states preserve alpha.
whole=cells+[cells[6].transpose(Image.Transpose.FLIP_LEFT_RIGHT),cells[5].transpose(Image.Transpose.FLIP_LEFT_RIGHT),cells[4].transpose(Image.Transpose.FLIP_LEFT_RIGHT)]
rolls=[0,4,5,6,7,8,9,10];roll=[];cleanroll=[]
for state in range(4):
 for pose in rolls:
  f=whole[pose].copy();a=np.array(f);yy,xx=np.mgrid[:f.height,:f.width]
  rects=rollboxes[pose]if pose<8 else[(f.width-r[2],r[1],f.width-r[0],r[3])for r in rollboxes[{8:6,9:5,10:4}[pose]][::-1]]
  for part,rect in enumerate(rects):
   if not state&(1<<part):continue
   x0,y0,x1,y1=rect;cx=(x0+x1)/2;cy=(y0+y1)/2;r=((xx-cx)/((x1-x0)*.6))**2+((yy-cy)/((y1-y0)*.6))**2;mask=np.clip((1.25-r)*3,0,1)[:,:,None]
   rgb=a[:,:,:3].astype(float);lum=rgb.max(2);burn=np.stack([lum*.16,lum*.19,lum*.21],axis=2);a[:,:,:3]=(rgb*(1-mask)+burn*mask).astype('uint8')
  f=normalized(Image.fromarray(a),512,k,anchor=(222,222)).resize((384,384),Image.Resampling.NEAREST);roll.append(f)
  if state==0:cleanroll.append(f)
bank('razor_roll',heading(roll,16),16);bank('razor_roll_hit',heading([white(f)for f in cleanroll],16),16)
gunpoints=[]
for i,(box,mount,bore)in enumerate(zip(boxes,mounts,bores)):
 piece=cells[0].crop(box);local=(mount[0]-box[0],mount[1]-box[1]);parts=[]
 for recoil in [0,-4]:parts.append(normalized(piece,192,k,anchor=(local[0],local[1]-recoil)))
 bank('razor_gun'+str(i),heading(parts),32);bank('razor_gun'+str(i)+'_hit',heading([white(f)for f in parts]),32);bank('razor_gun'+str(i)+'_wreck',heading([charred(f)for f in parts]),32)
 gunpoints.append(dict(mount=[256+(mount[0]-222)*k,256+(mount[1]-222)*k],bore=[(bore[0]-mount[0])*k,(bore[1]-mount[1])*k],size=192))
M['models']['razor']=dict(cell=512,world=250,engines=[[256+(x-222)*k,256+(67-222)*k]for x in[198,246]],guns=gunpoints,core=[256,273],coreBox=[94,115],bodyBox=[360,370],clips=dict(idle=0,brake=2,roll=[0,4,5,6,7,8,9,10]))

raw=clean(Image.open(S/'thunderhead_source.png'));factor=.58
unit=normalized(raw,768,factor,anchor=(627,627));hull=unit.copy();guns=[]
for i,(box,mount,bore)in enumerate([((345,388,474,609),(410,454),(410,590)),((781,388,910,609),(844,454),(844,590)),((341,736,498,1000),(420,807),(420,976)),((752,736,910,1000),(834,807),(834,976))]):
 piece=raw.crop(box);a=(mount[0]-box[0],mount[1]-box[1]);parts=[normalized(piece,256,factor,anchor=(a[0],a[1]-recoil))for recoil in[0,-7]]
 bank('thunder_gun'+str(i),heading(parts),32);bank('thunder_gun'+str(i)+'_hit',heading([white(f)for f in parts]),32);bank('thunder_gun'+str(i)+'_wreck',heading([charred(f)for f in parts]),32)
 # Erase only the source module's registered rectangle from the main plate.
 p0=(round(384+(box[0]-627)*factor),round(384+(box[1]-627)*factor));p1=(round(384+(box[2]-627)*factor),round(384+(box[3]-627)*factor));hull.paste((0,0,0,0),(*p0,*p1))
 guns.append(dict(mount=[384+(mount[0]-627)*factor,384+(mount[1]-627)*factor],bore=[0,(bore[1]-mount[1])*factor],size=256))
pressures=[]
for i,box in enumerate([(42,344,278,895),(976,344,1212,895)]):
 # Pressure towers remain actual pieces, with opening/recoil source-preserving
 # shutter masks. Their base hull pixels are never stretched or regenerated.
 piece=raw.crop(box);centre=((box[0]+box[2])/2,(box[1]+box[3])/2);parts=[]
 for phase in range(5):
  f=normalized(piece,384,factor)
  if phase:
   a=np.array(f);yy,xx=np.mgrid[:384,:384];energy=(a[:,:,1]>a[:,:,0]*1.13)&(a[:,:,2]>a[:,:,0]*1.1)&(a[:,:,3]>35)
   a[:,:,:3][energy]=np.minimum(255,a[:,:,:3][energy].astype(float)*(1+phase*.14)).astype('uint8');f=Image.fromarray(a)
  parts.append(f)
 bank('thunder_pressure'+str(i),parts);bank('thunder_pressure'+str(i)+'_hit',[white(f)for f in parts]);bank('thunder_pressure'+str(i)+'_wreck',[charred(f)for f in parts])
 p0=(round(384+(box[0]-627)*factor),round(384+(box[1]-627)*factor));p1=(round(384+(box[2]-627)*factor),round(384+(box[3]-627)*factor));hull.paste((0,0,0,0),(*p0,*p1))
 pressures.append(dict(mount=[384+(centre[0]-627)*factor,384+(centre[1]-627)*factor],bore=[0,(839-centre[1])*factor],size=384))
bank('thunder_body',[hull]);bank('thunder_hit',[white(hull)]);bank('thunder_flow',[flow(hull,i)for i in range(4)])
M['models']['thunder']=dict(cell=768,world=560,guns=guns,pressures=pressures,engines=[[384+(x-627)*factor,384+(235-627)*factor]for x in[360,505,750,887]],core=[384,420],coreBox=[110,180],bodyBox=[720,520])

raw=clean(Image.open(S/'storm_source.png'),24);fx=[]
for i in range(16):
 box=(round(i%4*raw.width/4),round(i//4*raw.height/4),round((i%4+1)*raw.width/4),round((i//4+1)*raw.height/4))
 cell=raw.crop(box);fx.append(normalized(cell,256,.76))
bank('tornado',fx[:8]);bank('hurricane',fx[8:12]);bank('storm_burst',fx[12:]);bank('exhaust',heading(fx[:4]),32)
# Source-pixel exhaust/muzzle partners come from the existing Stage6 ship art.
for name,path,cols,count in [('wind_round','assets/game/levels/stage_06/boss/nightwing_wind_1028/wind_bullet_gusts_1028.png',16,512),('wind_muzzle','assets/game/levels/stage_06/boss/nightwing_wind_1028/wind_muzzle_gusts_1028.png',16,256)]:
 im=Image.open(R/path).convert('RGBA');cw=64;bank(name,[im.crop((i%cols*cw,i//cols*cw,i%cols*cw+cw,i//cols*cw+cw))for i in range(count)])
for p in S.glob('*_source.png'):M['sources'][p.name]=dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),tool='built-in image_gen',prompt=(S/'PROMPTS.md').relative_to(R).as_posix())
write(metadata(M))
preview=Image.new('RGBA',(1536,768),'#06121d');preview.alpha_composite(unit,(0,0));preview.alpha_composite(body[0],(768,0));preview.alpha_composite(fx[3],(768,512));preview.alpha_composite(fx[9],(1024,512));preview.alpha_composite(fx[13],(1280,512));preview.convert('RGB').save(O/'art-contact.jpg',quality=95)
print('Built',len(M['banks']),'banks; disjoint hull/modules and measured sockets')
