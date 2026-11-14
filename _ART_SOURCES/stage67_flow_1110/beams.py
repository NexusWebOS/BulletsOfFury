from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys,shutil,numpy as np
from scipy.ndimage import label
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;C=W/'candidate';D=C/'frames';D.mkdir(parents=True,exist_ok=True);O=W.parents[1]/'outputs/stage67-flow';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,'C:/Users/Mike/.codex/skills/clean-pixel-effect-gifs/scripts');import pixelcore as px
raw=Path('C:/Users/Mike/.codex/generated_images/01a1c263-6df7-7072-a76a-4b41ccbb8b8a/exec-9b19d22a-b0e2-4e88-b096-aa39dad8a5ec.png');shutil.copy2(raw,O/'generated-wind-master.png');sheet=Image.open(raw).convert('RGBA');frames=[];samples=[]
for i in range(8):
 x=round(i%4*sheet.width/4);y=round(i//4*sheet.height/2);q=np.array(sheet.crop((x,y,x+280,y+701)));lab,n=label(q[:,:,3]>=96);sizes=np.bincount(lab.ravel());sizes[0]=0;keep=lab==sizes.argmax();q[:,:,3]=np.where(keep,q[:,:,3],0);q[q[:,:,3]==0]=0;frames.append(q);samples.append(q[keep,:3])
sample=np.concatenate(samples)[::8].reshape(1,-1,3);p=Image.fromarray(sample).quantize(colors=32,method=Image.Quantize.MEDIANCUT);pal=np.array(p.getpalette(),dtype=np.uint8).reshape(-1,3)[:32]
clean=[]
for v in frames:
 rgb=px.map_to_palette(v[:,:,:3],pal);q=np.dstack([rgb,v[:,:,3]]);q[q[:,:,3]==0]=0;clean.append(Image.fromarray(q).resize((182,456),Image.Resampling.NEAREST))
def meta(n):
 s=(R/'assets'/n).read_text();return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
T=meta('thunderhead_reactor_art_1105.js');M=meta('thunderhead_modular_art_1104.js');cache={}
def source(meta,name,f):
 b=meta['banks'][name];c=b['cells'][f];key=c[0]
 if key not in cache:cache[key]=Image.open(R/meta['pages'][key]['path']).convert('RGBA')
 if 'cw'in b:return cache[key].crop((c[1],c[2],c[1]+b['cw'],c[2]+b['ch']))
 out=Image.new('RGBA',(b['w'],b['h']));out.paste(cache[key].crop((c[1],c[2],c[1]+c[3],c[2]+c[4])),(c[5],c[6]));return out
records={};Y,X=np.mgrid[:832,:256];opening=((X-128)/42)**2+((Y-239.28)/16)**2<1
for pod in range(2):
 for hit in range(2):
  out=Image.new('RGBA',(256*8,832*4))
  for f in range(28):
   level=min(3,f//2) if f<6 else max(0,3-(f-22)//2) if f>=22 else 3;plate=source(T,f'pod{pod}_d0_0',level*8+(f%8));body=Image.new('RGBA',(256,832));body.alpha_composite(plate,(30,0));energy=Image.new('RGBA',body.size);im=clean[(f-6)%8].copy()
   if f>=22:im.putalpha(im.getchannel('A').point(lambda a:round(a*max(0,(27-f)/6))))
   energy.alpha_composite(im,(37,197));e=np.array(energy);keep=((Y>=225)&opening)|(Y>=255)
   if f<6:keep&=Y<239+round(456*(f+1)/6)
   e[:,:,3]=np.where(keep,e[:,:,3],0);e[e[:,:,3]==0]=0
   if hit:
    white=source(M,f'pod{pod}_hit',0);body=Image.new('RGBA',(256,832));body.alpha_composite(white,(32,2))
   body.alpha_composite(Image.fromarray(e))
   # The source metal ring is the foreground, never an independently placed fan sprite.
   p=np.array(plate);yy,xx=np.mgrid[:plate.height,:plate.width];ellipse=((xx-98)/44)**2+((yy-239.28)/18)**2;rgb=p[:,:,:3].astype(float);metal=((rgb.max(2)-rgb.min(2))<95)|(rgb[:,:,0]>rgb[:,:,2]*1.2);rim=(ellipse>=.83)&(ellipse<1.36)&(yy>=219)&(yy<265)&metal
   p[:,:,3]=np.where(rim,p[:,:,3],0)
   if hit:p[:,:,:3]=255
   body.alpha_composite(Image.fromarray(p),(30,0));out.paste(body,(f%8*256,f//8*832))
  name=f'cannon{pod}-'+('hit'if hit else'body');out.save(D/(name+'.png'),optimize=True);records[name]={'path':f'assets/game/shared/combat/stage67_flow_1110/{name}.png','cell':[256,832]}
p=R/'assets/thunderhead_reactor_1105.js';before=p.read_bytes();(C/'thunderhead_reactor_1105.js.before').write_bytes(before);s=before.decode();start=s.index('function sr110CannonBeams(b)');end=s.index('function tc119Beams',start)
helper='''// The cannon and its discharge are one authored plate sharing the native mount.
const CF121={art:@@ART@@,draws:0,sockets:[]};
Object.assign(SR110.art,CF121.art);for(const[k,a]of Object.entries(CF121.art))XART._src['sr110_'+k]=a.path;
function sr110CannonBeams(b){for(const B of tm115State(b).beams){if(B.part.hp<=0)continue;const f=B.recovery?22+Math.min(5,Math.floor(B.tail*24)):B.age<TM115.beamGrow?Math.min(5,Math.floor(B.age*24)):6+Math.floor((B.age-TM115.beamGrow)*24)%16,m=fb112PartPoint(b,B.part),k='cannon'+B.part.index+'-'+(B.part.flash>0?'hit':'body'),im=XART.get('sr110_'+k);if(!im)continue;ctx.drawImage(im,f%8*256,Math.floor(f/8)*832,256,832,Math.round(m.x-128),Math.round(m.y-146),256,832);CF121.draws++;SR110.beams++;const bore=fb112Bore(b,B.part);CF121.sockets.push({part:B.part.id,dx:bore.x-m.x,dy:bore.y-m.y,frame:f});if(CF121.sockets.length>20)CF121.sockets.shift();}}
'''.replace('@@ART@@',json.dumps(records,separators=(',',':')))
s=s[:start]+helper+s[end:]
needle="else{tc119Blit(turn?'pod'+p.index+'_turn_d'+di"
assert needle in s;s=s.replace(needle,"else{if(di===0&&!turn&&tm115State(b).beams.some(B=>B.part===p))continue;tc119Blit(turn?'pod'+p.index+'_turn_d'+di",1)
(C/'thunderhead_reactor_1105.js').write_text(s,encoding='utf-8',newline='\n')
manifest={'hashes':{'thunderhead_reactor_1105.js':hashlib.sha256(before).hexdigest(),'sumpjaw_tandem_1105.js':json.loads((W/'motion-manifest.json').read_text())['hash']},'records':records,'frames':28,'pivot':[128,146],'outlet':[128,239.28],'source_root':[140,65],'source_scale':.65,'palette':['#%02x%02x%02x'%tuple(c)for c in pal],'beam_source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'render':'complete cannon/discharge plates; no independent outlet/beam alignment'}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2));contact=Image.new('RGB',(768,832),'#10192b')
im=Image.open(D/'cannon0-body.png')
for j,f in enumerate([6,10,14]):contact.paste(im.crop((f%8*256,f//8*832,f%8*256+256,f//8*832+832)),(j*256,0),im.crop((f%8*256,f//8*832,f%8*256+256,f//8*832+832)))
contact.save(W/'cannon-contact.png');print(json.dumps({'sheets':4,'poses':112,'source':sheet.size}))
