"""Source-authored Stage3 aircraft/eye and palette-only ice ordnance export.
Hull directions are actual distinct source poses, never rotated idle plates.
Only oriented effect/turret textures are baked offline into registered cells.
"""
from pathlib import Path
from io import BytesIO
import json,math,hashlib,shutil,base64
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects,binary_erosion
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/stage3_amplify_1031';S.mkdir(exist_ok=True)
Q=R/'_shots/stage3_amplify_1031';Q.mkdir(exist_ok=True)
O=R/'assets/game/levels/stage_03/enemies/amplify_1031';O.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
FILES={'shard':'exec-2b275f7e-27da-4774-a2d4-f4a5c6769b25.png','eye':'exec-63a5a2a2-7f86-4c0f-bba6-32cda881ad4d.png','mine':'exec-0dbf28b5-9914-4a9b-a348-3a32eae712e7.png','interceptor':'exec-56aced13-90b3-4673-b318-47e27a56f19a.png'}
M={'owner':'_BUILD_SOURCE/build_stage3_amplify_1031.py','tool':'built-in image_gen / source-preserving palette export','models':{},'banks':{},'sources':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sheet(n,fs,dirs=1):
 c=fs[0].width;assert all(i.size==(c,c)for i in fs)and c%2==0
 out=Image.new('RGBA',(c*dirs,c*len(fs)))
 for f,im in enumerate(fs):
  for d in range(dirs):out.alpha_composite(im.rotate(-360*d/dirs,Image.Resampling.NEAREST),(c*d,c*f))
 p=O/(n+'.webp');bio=BytesIO();out.save(bio,format='WEBP',lossless=True,method=4);p.write_bytes(bio.getvalue())
 B={'key':'i31_'+n,'path':p.relative_to(R).as_posix(),'cell':c,'pivot':[c//2,c//2],'dirs':dirs,'cols':dirs,'frames':len(fs),'sha256':sha(p)};M['banks'][n]=B;return B
def heading(n,fs):
 B=sheet(n,fs);im=Image.open(R/B['path']);out=Image.new('RGBA',(160*len(fs),160))
 for i in range(len(fs)):out.alpha_composite(im.crop((0,i*160,160,(i+1)*160)),(i*160,0))
 out.save(R/B['path'],format='WEBP',lossless=True,method=4);B.update(dirs=len(fs),cols=len(fs),frames=1,sha256=sha(R/B['path']));return B
def normalize(fs,c=160,span=140):
 k=span/max(max(t.getbbox()[2]-t.getbbox()[0],t.getbbox()[3]-t.getbbox()[1])for t in fs);out=[]
 for t in fs:
  t=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);p=Image.new('RGBA',(c,c));p.alpha_composite(t,((c-t.width)//2,(c-t.height)//2));out.append(p)
 return out
def generated(n,rows):
 p=S/(n+'_source.png')
 if not p.exists():shutil.copyfile(G/FILES[n],p)
 ar=np.array(Image.open(p).convert('RGBA'));ar[:,:,3]=np.where(ar[:,:,3]<24,0,np.minimum(255,ar[:,:,3].astype('int16')*255//252));im=Image.fromarray(ar)
 lab,_=label(ar[:,:,3]>90);parts=[]
 for j,s in enumerate(find_objects(lab),1):
  if s is not None:
   count=np.count_nonzero(lab[s]==j)
   if count>700:parts.append((count,s))
 if n=='eye':
  fs=[];rect=[]
  for y in [4,260,516,772]:
   for x in [110,430,765,1103]:
    t=im.crop((x,y,x+318,y+252));pad=Image.new('RGBA',(320,320));pad.alpha_composite(t,(1,34));fs.append(pad);rect.append([x,y,318,252])
  M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'rects':rect,'commonSourceCanvas':[320,320]}
  return normalize(fs)
 parts=sorted(parts,reverse=True,key=lambda v:v[0])[:rows*4];assert len(parts)==rows*4,(n,len(parts))
 parts.sort(key=lambda v:(v[1][0].start+v[1][0].stop)/2);ordered=[]
 for row in range(rows):ordered+=sorted(parts[row*4:row*4+4],key=lambda v:v[1][1].start)
 side=math.ceil((max(max(s[0].stop-s[0].start,s[1].stop-s[1].start)for _,s in ordered)+12)/2)*2;fs=[];rect=[]
 for _,s in ordered:
  x,y=max(0,s[1].start-3),max(0,s[0].start-3);xx,yy=min(im.width,s[1].stop+3),min(im.height,s[0].stop+3);t=im.crop((x,y,xx,yy));padded=Image.new('RGBA',(side,side));padded.alpha_composite(t,((side-t.width)//2,(side-t.height)//2));fs.append(padded);rect.append([x,y,xx-x,yy-y])
 M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'rects':rect,'commonSourceCanvas':[side,side]}
 fs=normalize(fs);contact=Image.new('RGB',(640,184*rows),(8,22,36));d=ImageDraw.Draw(contact)
 for j,t in enumerate(fs):contact.paste(t,(j%4*160,j//4*184+20),t);d.text((j%4*160+4,j//4*184+3),str(j),fill='white')
 contact.save(Q/(n+'-contact.jpg'),quality=92);return fs
for n in ['shard','mine','interceptor']:
 fs=generated(n,6)
 ids=[0,9,10,7,4,5,6,11]
 # Shard never flips. Its complete restricted bank remains south-facing.
 if n=='shard':ids=[0,2,2,0,0,0,3,3]
 banks={'heading':heading(n+'_heading',[fs[i]for i in ids]),'idle':sheet(n+'_idle',[fs[0]]),'attack':sheet(n+'_attack',fs[20:24]),'drift':sheet(n+'_drift',fs[2:4]),'roll':sheet(n+'_roll',fs[12:16]),'somer':sheet(n+'_somer',fs[16:20]),'charge':sheet(n+'_charge',fs[20:24])}
 M['models'][n]={'span':140,'banks':banks,'guns':[[56,71],[104,71]]if n=='interceptor'else[[65,124],[94,124]],'tails':[[62,21],[99,21]],'source':M['sources'][n]}
M['models']['interceptor']['gunPoses']=[[[54,63],[105,63]],[[60,58],[105,80]],[[78,58],[91,86]],[[57,86],[95,61]],[[54,91],[105,91]],[[60,60],[90,101]],[[80,62],[80,103]],[[60,67],[91,85]]]
fs=generated('eye',4);M['models']['eye']={'span':140,'banks':{'sequence':sheet('eye_sequence',fs)},'guns':[[80,14],[146,80],[80,146],[14,80]],'tails':[]}
# Retain the actual four-frame Glacier Carrier, preserving its silhouette.
fs=[Image.open(S/f'ndr_glaciercarrier_idle_{i}.png').convert('RGBA')for i in range(4)];fs=normalize(fs)
M['models']['carrier']={'span':140,'banks':{'idle':sheet('carrier_idle',fs),'attack':sheet('carrier_attack',fs)},'guns':[[57,134],[105,134]],'tails':[]}
for n in ['overhaul_ground_base_3','rzb_sonic_wave']:
 p=S/(n+'.png')
 if not p.exists():shutil.copyfile(Q/(n+'.png'),p)
# Preserve alpha, neutral metal and luminance; colored warm/green energy -> ice blue.
def ice(im):
 a=np.array(im.convert('RGBA'));rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);l=(rgb*[.2126,.7152,.0722]).sum(2);mask=(hi-lo>28)&(a[:,:,3]>0)
 ramp=np.stack([l*.42,l*1.12,l*1.55],2);ramp/=np.sum(np.array([.42,1.12,1.55])*[.2126,.7152,.0722]);a[:,:,:3][mask]=np.minimum(255,ramp)[mask].astype('uint8');return Image.fromarray(a)
v=json.load(open(R/'assets/game/levels/stage_02/enemies/amplify_1031/manifest.json'))
for n in ['slug','mine','muzzle','thruster','laser']:
 B=v['banks'][n];im=ice(Image.open(R/B['path']));p=O/('ice_'+n+'.webp');im.save(p,format='WEBP',lossless=True,method=4);M['banks'][n]={**B,'key':'i31_'+n,'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
for weapon in ['laser','sonic']:
 im=Image.open(R/f'assets/game/shared/combat/enemy_overhaul_0925/sprites/ground_head_{weapon}.png').convert('RGBA');sheet('turret_'+weapon,normalize([im],160,140),64)
im=ice(Image.open(S/'rzb_sonic_wave.png'));sheet('sonic',normalize([im],128,110),32)
# Ice island top surface, explicitly exclude transparent water and dark cliffs.
p=R/'assets/game/levels/stage_03/stage/nst3_master_v2.png';ar=np.array(Image.open(p).convert('RGBA'));rgb=ar[:,:,:3].astype(float)
c=8;gh=math.ceil(ar.shape[0]/c);gw=math.ceil(ar.shape[1]/c);bits=np.zeros((gh,gw),dtype=np.uint8)
for y in range(gh):
 for x in range(gw):
  t=ar[y*c:min((y+1)*c,ar.shape[0]),x*c:min((x+1)*c,ar.shape[1])].mean((0,1));bits[y,x]=t[3]>245 and t[0]>62 and t[1]>90 and t[2]>140 and t[2]>t[0]
bits=binary_erosion(bits,iterations=1).astype('uint8')
M['islands']={'cell':c,'gw':gw,'gh':gh,'bits':base64.b64encode(np.packbits(bits.flatten())).decode(),'source':p.relative_to(R).as_posix(),'sha256':sha(p),'acceptedCells':int(bits.sum())}
preview=Image.fromarray((bits*255).astype('uint8')).resize((340,2040));preview.save(Q/'island-mask.png')
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8')
(R/'assets/stage3_amplify_art_1031.js').write_text('"use strict";\nconst I31_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Exported',len(M['models']),'models',len(M['banks']),'banks;',M['islands']['acceptedCells'],'island cells')
