from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
from scipy.ndimage import distance_transform_edt
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;D=W/'candidate/frames';D.mkdir(parents=True,exist_ok=True);O=W.parents[1]/'outputs/cannon-chambers';O.mkdir(parents=True,exist_ok=True)
master=R/'_ART_SOURCES/stage67_flow_1110/generated-wind-master.png';raw=Image.open(master).convert('RGBA');yy,xx=np.mgrid[:832,:256];opening=((xx-128)/52.5)**2+((yy-239.28)/22.5)**2<=1;metrics=[]
# Use the original generated energy pixels, at one common proportional scale.
# Nearest valid energy colour fills alpha gaps before the complete oval is authored.
textures=[]
for f in range(8):
 x=round(f%4*raw.width/4);y=round(f//4*raw.height/2);q=np.array(raw.crop((x+64,y+120,x+232,y+192)));valid=q[:,:,3]>=96;_,idx=distance_transform_edt(~valid,return_indices=True);q[:,:,:3]=q[idx[0],idx[1],:3];q[:,:,3]=255;textures.append(Image.fromarray(q).resize((105,45),Image.Resampling.NEAREST))
for pod in range(2):
 for mode in ['body','hit']:
  name=f'cannon{pod}-{mode}';source=R/f'assets/game/shared/combat/stage67_flow_1110/{name}.png';atlas=Image.open(source).convert('RGBA');out=atlas.copy()
  for f in range(28):
   cell=atlas.crop((f%8*256,f//8*832,f%8*256+256,f//8*832+832));layer=Image.new('RGBA',(256,832));layer.paste(textures[(f-6)%8],(76,217));v=np.array(layer)
   # Common52.5x22.5 ellipse reaches the chamber's full inner wall on both sides.
   # Include the fractional bottom/right pixels from the same source texture.
   rgb=np.array(textures[(f-6)%8]);sx=np.clip(xx-76,0,104);sy=np.clip(yy-217,0,44);v[:,:,:3]=rgb[sy,sx,:3];v[:,:,3]=np.where(opening,255,0)
   if f>=22:v[:,:,3]=(v[:,:,3].astype(float)*max(0,(27-f)/6)).astype('uint8')
   v[v[:,:,3]==0]=0;cell.alpha_composite(Image.fromarray(v));out.paste(cell,(f%8*256,f//8*832))
   if 6<=f<22:metrics.append({'pod':pod,'mode':mode,'frame':f,'filled_pixels':int((v[:,:,3][opening]==255).sum()),'opening_pixels':int(opening.sum()),'no_fan_visible':bool(np.all(v[:,:,3][opening]==255))})
  out.save(D/(name+'.png'),optimize=True)
runtime=R/'assets/thunderhead_reactor_1105.js';live=runtime.read_bytes();b=W/'candidate/before.js';before=b.read_bytes()if b.exists()else live
assert live==before or live==(W/'candidate/thunderhead_reactor_1105.js').read_bytes(),'Concurrent source changes'
if not b.exists():b.write_bytes(before)
code=before.decode();old='assets/game/shared/combat/stage67_flow_1110/';assert code.count(old)==4;code=code.replace(old,'assets/game/shared/combat/cannon_chambers_1110/');(W/'candidate/thunderhead_reactor_1105.js').write_text(code,encoding='utf-8',newline='\n')
m={'expected_source_hash':hashlib.sha256(live).hexdigest(),'source_master_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'cell':[256,832],'pivot':[128,146],'opening':{'center':[128,239.28],'radii':[52.5,22.5]},'frames':28,'firing_coverage':metrics,'scope':'Only baked chamber-face coverage and four texture paths; native weapon and movement logic unchanged'};(O/'manifest.json').write_text(json.dumps(m,indent=2));assert all(q['no_fan_visible']for q in metrics)
contact=Image.new('RGB',(512,340),'#10192b')
for pod in range(2):
 im=Image.open(D/f'cannon{pod}-body.png');f=10;im=im.crop((f%8*256,f//8*832,f%8*256+256,f//8*832+340));contact.paste(im,(pod*256,0),im)
contact.save(O/'chamber-detail.png');print(json.dumps({'fully_filled_firing_poses':len(metrics),'opening_pixels':int(opening.sum()),'runtime_changes':'four texture paths only'}))
