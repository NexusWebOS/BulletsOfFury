from pathlib import Path
from PIL import Image
import numpy as np
import json,math,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/riders_return_overflight_1030';S=R/'_ART_SOURCES/riders_return_overflight_1030';D.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
raw=(R/'assets/manifest.js').read_text(encoding='utf8');a=json.JSONDecoder().raw_decode(raw[raw.index('window.BOFX=')+len('window.BOFX='):])[0];atlas=Image.open(R/a['img']['florb_0']).convert('RGBA');sources=[]
for i in range(8):
 row=a['cells']['florb_'+str(i)];_,x,y,w,h=row;im=atlas.crop((x,y,x+w,y+h));im.save(S/f'florb_{i}.png');v=np.array(im);rgb=v[:,:,:3].astype(float);hi=rgb.max(2);sat=hi-rgb.min(2);mask=sat>24;teal=np.stack([hi*.18,hi*.94,hi*.83],2);v[:,:,:3][mask]=teal.astype('uint8')[mask];sources.append(Image.fromarray(v))
art={}
for role,count in [('orb',17*8),('shadow',17)]:
 sheet=Image.new('RGBA',(64*8,64*math.ceil(count/8)))
 for f in range(count):
  depth=f//8 if role=='orb' else f;size=14+depth*2;out=Image.new('RGBA',(64,64))
  if role=='orb':
   im=sources[f%8].resize((size,size),Image.Resampling.NEAREST);out.alpha_composite(im,((64-size)//2,(64-size)//2))
  else:
   im=sources[0].resize((size,max(4,round(size*.32))),Image.Resampling.NEAREST);alpha=im.getchannel('A').point(lambda v:v*90//255);q=Image.new('RGBA',im.size,(0,7,13));q.putalpha(alpha);out.alpha_composite(q,((64-q.width)//2,(64-q.height)//2))
  sheet.alpha_composite(out,(f%8*64,f//8*64))
 p=D/(role+'.webp');sheet.save(p,lossless=True);art[role]={'key':'rr75_'+role,'path':p.relative_to(R).as_posix(),'cw':64,'ch':64,'pivot':[32,32],'cols':8,'frames':count,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(R/'assets/riders_return_overflight_art_1030.js').write_text('const RR75_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8');(D/'manifest.json').write_text(json.dumps(art,indent=2));print('Authored17 depth levels,8 original teal orb frames, matched shadows.')
