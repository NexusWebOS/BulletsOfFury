from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil,numpy as np
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;D=W/'candidate/frames';D.mkdir(parents=True,exist_ok=True);O=W.parents[1]/'outputs/snake-assault';O.mkdir(parents=True,exist_ok=True)
master=Path('C:/Users/Mike/.codex/generated_images/01a1c263-6df7-7072-a76a-4b41ccbb8b8a/exec-33d99f3f-5b73-442b-b103-86cead6e8424.png');shutil.copy2(master,O/'generated-burrow-master.png');raw=Image.open(master).convert('RGBA');print('master',raw.size,raw.getchannel('A').getextrema(),flush=True);holes=[];records={}
def save(name,frames,pivot,cols=8):
 w,h=frames[0].size;atlas=Image.new('RGBA',(w*cols,h*((len(frames)+cols-1)//cols)))
 for i,im in enumerate(frames):assert im.size==(w,h);atlas.paste(im,(i%cols*w,i//cols*h))
 atlas.save(D/(name+'.png'),optimize=True);records[name]={'path':f'assets/game/shared/combat/snake_assault_1110/{name}.png','cell':[w,h],'pivot':pivot,'cols':cols,'frames':len(frames)}
for f in range(8):
 x=round(f%4*raw.width/4);y=round(f//4*raw.height/2);q=raw.crop((x,y,x+round(raw.width/4),y+round(raw.height/2))).resize((192,128),Image.Resampling.NEAREST);v=np.array(q);v[v[:,:,3]<96]=0;v[:,:,3]=np.where(v[:,:,3]>=96,255,0);holes.append(v)
samples=np.concatenate([v[v[:,:,3]>0,:3]for v in holes])[::2];p=Image.fromarray(samples.reshape(1,-1,3)).quantize(colors=32,method=Image.Quantize.MEDIANCUT);pal=p.getpalette();qpal=Image.new('P',(1,1));qpal.putpalette(pal);clean=[]
for v in holes:
 rgb=Image.fromarray(v[:,:,:3]).quantize(palette=qpal,dither=Image.Dither.NONE).convert('RGB');q=Image.fromarray(np.dstack([np.array(rgb),v[:,:,3]]));clean.append(q)
save('hole',clean,[96,64]);front=[]
for q in clean:
 v=np.array(q);v[:64]=0;front.append(Image.fromarray(v))
save('hole-front',front,[96,64])
arrow=Image.open(R/'assets/game/shared/ui/ui/warn_0916/escape_arrow.png').convert('RGBA').resize((46,31),Image.Resampling.NEAREST);base=Image.new('RGBA',(64,64));base.alpha_composite(arrow,(9,16));v=np.array(base);hsv=np.array(base.convert('HSV'));colored=(v[:,:,3]>0)&(hsv[:,:,1]>70)&(hsv[:,:,2]>65);frames=[]
for hue in [80,31,0]:
 for pulse in range(2):
  q=hsv.copy();q[:,:,0]=np.where(colored,hue,q[:,:,0]);q[:,:,1]=np.where(colored,220,q[:,:,1]);im=Image.fromarray(q,'HSV').convert('RGB');a=v[:,:,3].copy();a=(a.astype(np.uint16)*(255 if pulse==0 else 160)//255).astype('uint8');im.putalpha(Image.fromarray(a))
  for n in range(32):frames.append(im.rotate(-n*360/32,Image.Resampling.NEAREST))
save('arrows',frames,[32,32],16)
s=(R/'assets/sumpjaw_serpent_art_1104.js').read_text();T=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
for mode,n in [('dive',0),('riseL',14),('riseR',18)]:
 for state in ['body0','body1','body2','body3','hit']:
  b=T['banks'][state];p=next(p for p in b['pages']if p['start']<=n<p['start']+p['frames']);f=n-p['start'];source=Image.open(R/p['path']).convert('RGBA').crop((f%b['cols']*176,f//b['cols']*176,f%b['cols']*176+176,f//b['cols']*176+176));frames=[]
  for j in range(16):
   im=Image.new('RGBA',(176,176));im.paste(source,(0,round(j/15*176)));v=np.array(im);v[158:]=0;frames.append(Image.fromarray(v))
  save(mode+'-'+state,frames,[88,88])
(O/'art.json').write_text(json.dumps(records,indent=2));contact=Image.new('RGB',(768,384),'#19221c')
for f,q in enumerate(clean):contact.paste(q,(f%4*192,f//4*128),q)
for i,n in enumerate([0,5,10,15]):
 im=Image.open(D/'dive-body0.png').crop((n%8*176,n//8*176,n%8*176+176,n//8*176+176));contact.paste(im,(i*192,230),im)
contact.save(O/'art-contact.png');print(json.dumps({'banks':len(records),'frames':sum(a['frames']for a in records.values()),'master_sha256':hashlib.sha256(master.read_bytes()).hexdigest()}))
