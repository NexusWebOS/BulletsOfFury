from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,shutil,subprocess,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/cockpit_talk_1114';OUT.mkdir(parents=True,exist_ok=True);ART=OUT/'art';ART.mkdir(exist_ok=True)
SCRIPTS=Path('C:/Users/Mdogg/.codex/plugins/cache/openai-curated-remote/game-studio/0.1.2/scripts')
sources=json.loads((ROOT/'docs/COCKPIT_TALK_ART_1114.json').read_text(encoding='utf-8'));banks={};minis={};stats=[];previews=[]
def reg(frame,reference):
 a=np.array(frame.convert('RGB'),dtype=np.int16);b=np.array(reference.convert('RGB'),dtype=np.int16)
 x0,x1,y0,y1=202,374,20,94;target=b[y0:y1,x0:x1];mask=target.max(axis=2)>40;best=(1e9,0,0)
 for dy in range(-5,6):
  for dx in range(-5,6):
   score=np.abs(a[y0-dy:y1-dy,x0-dx:x1-dx]-target).mean(axis=2)[mask].mean()
   if score<best[0]:best=(float(score),dx,dy)
 c=Image.new('RGBA',frame.size);c.alpha_composite(frame,(best[1],best[2]));return c,best[1:]
def feather(rect):
 mask=Image.new('L',(576,384));d=ImageDraw.Draw(mask)
 for n,v in [(0,64),(1,160),(2,255)]:d.rectangle((rect[0]+n,rect[1]+n,rect[2]-n,rect[3]-n),fill=v)
 return mask
mouth=(202,104,370,198);eyes=(194,52,382,118)
for item in sources['assets']:
 p=item['pilot'];raw=Image.open(ROOT/item['source']).convert('RGBA');W,H=raw.size;assert abs(W/H-3)<.03,(p,raw.size)
 dest=ART/p;dest.mkdir(exist_ok=True);shutil.copy2(ROOT/item['source'],dest/'source.png')
 frames=[raw.crop((round(i%4*W/4)+4,round(i//4*H/2)+4,round((i%4+1)*W/4)-4,round((i//4+1)*H/2)-4)) for i in range(8)]
 cw=max(f.width for f in frames);ch=max(f.height for f in frames);strip=Image.new('RGBA',(cw*8,ch))
 for i,f in enumerate(frames):strip.alpha_composite(f,(i*cw,0))
 work=OUT/p;work.mkdir(exist_ok=True);strip.save(work/'raw-horizontal.png')
 subprocess.run(['python',str(SCRIPTS/'normalize_sprite_strip.py'),'--input',str(work/'raw-horizontal.png'),'--out-dir',str(work/'normalized'),'--frames','8','--frame-size','576'],check=True)
 normalized=[Image.open(work/'normalized'/('%02d.png'%(i+1))).convert('RGBA').crop((0,192,576,576)) for i in range(8)]
 base=normalized[0];final=[base];offsets=[(0,0)];blink=p not in ['axel','maverick','juggernaut']
 for i in range(1,8):
  aligned,offset=reg(normalized[i],base);offsets.append(offset)
  if i==7 and not blink:final.append(base.copy());continue
  final.append(Image.composite(aligned,base,feather(eyes if i==7 else mouth)))
 finaldir=work/'frames';finaldir.mkdir(exist_ok=True);atlas=Image.new('RGBA',(576*4,384*2))
 for i,f in enumerate(final):
  f.save(finaldir/('%02d.png'%(i+1)));atlas.alpha_composite(f,(i%4*576,i//4*384))
  diff=ImageChops.difference(f,base).convert('RGB');outside=Image.new('L',(576,384),255);ImageDraw.Draw(outside).rectangle(eyes if i==7 else mouth,fill=0)
  assert ImageChops.multiply(diff.getchannel('R'),outside).getbbox() is None,(p,i,'outside motion')
 atlas.save(dest/'cockpit.webp',lossless=True)
 subprocess.run(['python',str(SCRIPTS/'render_sprite_preview_sheet.py'),'--frames-dir',str(finaldir),'--out',str(work/'preview.png'),'--columns','4'],check=True)
 a={'key':'cp15_'+p,'path':'assets/game/shared/cinematics/cockpit_talk_1114/'+p+'/cockpit.webp','w':576,'h':384,'cols':4,'frames':8,'blink':blink,'pivot':[288,192],'mouthROI':list(mouth),'eyeROI':list(eyes),'sha256':hashlib.sha256((dest/'cockpit.webp').read_bytes()).hexdigest()};banks[p]=a
 for n in [48,64,84,96]:
  mini=Image.new('RGBA',(n,n*8))
  for i,f in enumerate(final):
   q=f.crop((144,4,432,292)).resize((n,n),Image.Resampling.NEAREST);mini.alpha_composite(q,(0,i*n))
  file=dest/('radio-'+str(n)+'.webp');mini.save(file,lossless=True)
  minis[p+'-'+str(n)]={'key':'cp15_'+p+'_'+str(n),'path':'assets/game/shared/cinematics/cockpit_talk_1114/'+p+'/'+file.name,'w':n,'h':n,'cols':1,'frames':8,'size':n,'baselines':[n]*8,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
 unique=len({hashlib.sha256(f.tobytes()).hexdigest() for f in final});assert unique>=6,(p,unique)
 stats.append({'pilot':p,'sourceSize':[W,H],'uniqueFrames':unique,'alignment':offsets,'bodyAndCockpitLocked':True,'blink':blink})
 previews.append((p,final[1]))
data={'pilots':list(banks),'banks':banks,'minis':minis,'poses':['idle','A','E','O','U','FV','small','blink'],'generator':'built-in image_gen','normalization':'Shared-scale sprite-pipeline normalization, registered upper-face anchor, neutral cabin/body lock outside generated mouth/eye regions.'}
(OUT/'cockpit_talk_art_1114.js').write_text('"use strict";\nconst CP15_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8')
(OUT/'packing.json').write_text(json.dumps({'stats':stats,'data':data},indent=2),encoding='utf-8')
contact=Image.new('RGB',(1440,930),'#10151d');d=ImageDraw.Draw(contact)
for i,(p,im) in enumerate(previews):
 q=im.resize((456,304),Image.Resampling.NEAREST);x=i%3*480+12;y=i//3*310;contact.paste(q,(x,y));d.text((x+8,y+286),p.upper(),fill='#fff0cf')
contact.save(OUT/'all-pilots.jpg',quality=95)
print(json.dumps(stats,indent=2),flush=True)
