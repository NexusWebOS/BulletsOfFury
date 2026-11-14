from pathlib import Path
from PIL import Image
import json,hashlib,sys,numpy as np
from scipy.ndimage import label,distance_transform_edt
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';D=C/'frames';D.mkdir(parents=True,exist_ok=True);O=W.parents[1]/'outputs/cannon-fit';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,'C:/Users/Mike/.codex/skills/clean-pixel-effect-gifs/scripts');import pixelcore as px
master=R/'_ART_SOURCES/stage67_flow_1110/generated-wind-master.png';sheet=Image.open(master).convert('RGBA');raw=[];samples=[];caps=[]
for f in range(8):
 x=round(f%4*sheet.width/4);y=round(f//4*sheet.height/2);v=np.array(sheet.crop((x,y,x+280,y+701)));lab,n=label(v[:,:,3]>=96);sizes=np.bincount(lab.ravel());sizes[0]=0;keep=lab==sizes.argmax();v[:,:,3]=np.where(keep,v[:,:,3],0);v[v[:,:,3]==0]=0;raw.append(v);samples.append(v[keep,:3])
 q=np.array(sheet.crop((x+64,y+120,x+232,y+194)));valid=q[:,:,3]>=96;_,idx=distance_transform_edt(~valid,return_indices=True);q[:,:,:3]=q[idx[0],idx[1],:3];q[:,:,3]=255;caps.append(Image.fromarray(q).resize((84,37),Image.Resampling.NEAREST))
sample=np.concatenate(samples)[::8].reshape(1,-1,3);pal=Image.fromarray(sample).quantize(colors=32,method=Image.Quantize.MEDIANCUT);pal=np.array(pal.getpalette(),dtype=np.uint8).reshape(-1,3)[:32];clean=[]
for v in raw:
 q=np.dstack([px.map_to_palette(v[:,:,:3],pal),v[:,:,3]]);q[q[:,:,3]==0]=0;clean.append(Image.fromarray(q).resize((182,456),Image.Resampling.NEAREST))
def meta(n):
 s=(R/'assets'/n).read_text();return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
T=meta('thunderhead_reactor_art_1105.js');M=meta('thunderhead_modular_art_1104.js');cache={}
def source(meta,name,f):
 b=meta['banks'][name];c=b['cells'][f];key=c[0]
 if key not in cache:cache[key]=Image.open(R/meta['pages'][key]['path']).convert('RGBA')
 if 'cw'in b:return cache[key].crop((c[1],c[2],c[1]+b['cw'],c[2]+b['ch']))
 out=Image.new('RGBA',(b['w'],b['h']));out.paste(cache[key].crop((c[1],c[2],c[1]+c[3],c[2]+c[4])),(c[5],c[6]));return out
Y,X=np.mgrid[:832,:256];metrics=[];sockets=[]
for pod in range(2):
 # The two perspective mouths are offset in opposite directions in their
 # source plates. Their inner faces are 83x37, rather than the old105x45 cap.
 cx=123 if pod==0 else 133;cy=238;opening=((X-cx)/41.5)**2+((Y-cy)/18.5)**2<=1;sockets.append({'pod':pod,'center':[cx,cy],'radii':[41.5,18.5]})
 mask=Image.fromarray((opening*255).astype('uint8'));mask.save(O/f'opening{pod}-mask.png')
 for mode in ['body','hit']:
  atlas=Image.new('RGBA',(2048,3328))
  for f in range(28):
   level=min(3,f//2)if f<6 else max(0,3-(f-22)//2)if f>=22 else 3;plate=source(T,f'pod{pod}_d0_0',level*8+f%8);body=Image.new('RGBA',(256,832));energy=Image.new('RGBA',body.size);im=clean[(f-6)%8].copy()
   if f>=22:im.putalpha(im.getchannel('A').point(lambda a:round(a*max(0,(27-f)/6))))
   energy.alpha_composite(im,(cx-91,196));e=np.array(energy);keep=Y>=260
   if f<6:keep&=Y<238+round(456*(f+1)/6)
   e[:,:,3]=np.where(keep,e[:,:,3],0);e[e[:,:,3]==0]=0;body.alpha_composite(Image.fromarray(e))
   # The entire original cannon rim stays in the foreground of the discharge.
   if mode=='hit':body.alpha_composite(source(M,f'pod{pod}_hit',0),(32,2))
   else:body.alpha_composite(plate,(30,0))
   rgb=np.array(caps[(f-6)%8]);sx=np.clip(X-(cx-42),0,83);sy=np.clip(Y-220,0,36);v=np.zeros((832,256,4),dtype=np.uint8);v[:,:,:3]=rgb[sy,sx,:3];v[:,:,3]=np.where(opening,255,0)
   if mode=='hit':v[:,:,:3]=(v[:,:,:3].astype(np.uint16)*45//100+140).clip(0,255).astype('uint8')
   v[v[:,:,3]==0]=0;body.alpha_composite(Image.fromarray(v));atlas.paste(body,(f%8*256,f//8*832));metrics.append({'pod':pod,'mode':mode,'frame':f,'filled_pixels':int((v[:,:,3][opening]==255).sum()),'opening_pixels':int(opening.sum()),'no_fan_visible':bool(np.all(v[:,:,3][opening]==255))})
  atlas.save(D/f'cannon{pod}-{mode}.png',optimize=True)
p=R/'assets/thunderhead_reactor_1105.js';live=p.read_bytes();before=(C/'before.js').read_bytes()if(C/'before.js').exists()else live;assert live==before or live==(C/'thunderhead_reactor_1105.js').read_bytes(),'Concurrent source changes'
if not(C/'before.js').exists():(C/'before.js').write_bytes(before)
code=before.decode();assert code.count('assets/game/shared/combat/cannon_cover_1110/')==4;code=code.replace('assets/game/shared/combat/cannon_cover_1110/','assets/game/shared/combat/cannon_fit_1110/');(C/'thunderhead_reactor_1105.js').write_text(code,encoding='utf-8',newline='\n')
m={'expected_source_hash':hashlib.sha256(live).hexdigest(),'source_master_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'cell':[256,832],'pivot':[128,146],'sockets':sockets,'frames':28,'firing_coverage':metrics,'scope':'Source-fitted per-cannon openings; complete original metal rim in foreground. Opaque energy through final recovery pose. Four texture paths only.'};(O/'manifest.json').write_text(json.dumps(m,indent=2));assert all(q['no_fan_visible']for q in metrics)
contact=Image.new('RGB',(512,320),'#10192b')
for pod in range(2):
 im=Image.open(D/f'cannon{pod}-body.png');f=10;q=im.crop((f%8*256,f//8*832,f%8*256+256,f//8*832+320));contact.paste(q,(pod*256,0),q)
contact.save(O/'chamber-detail.png');print(json.dumps({'fully_covered_poses':len(metrics),'sockets':sockets}))
