from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil,math,numpy as np
from scipy.ndimage import label,distance_transform_edt
W=Path(__file__).resolve().parent;ARCHIVED=W.parent.name=='_BUILD_SOURCE';R=W.parent.parent if ARCHIVED else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');D=W/'candidate/art';D.mkdir(parents=True,exist_ok=True);O=W/'export' if ARCHIVED else W.parents[1]/'outputs/dracodia-energy';O.mkdir(parents=True,exist_ok=True)
def meta(n):
 s=(R/'assets'/n).read_text(encoding='utf-8');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
N=meta('dracodia_brain_art_1023.js');P=meta('phoenix_turbo_core_art_1030.js');E=meta('neural_optics_art_1030.js');A={'banks':{},'pages':{},'eyes':{},'phoenix':{},'source_hashes':{},'version':'D124'};cache={}
class Pack:
 def __init__(self):self.im=Image.new('RGBA',(1024,1024));self.x=self.y=self.rh=self.n=0
 def flush(self):
  if not(self.y or self.rh):return
  key='d124_'+str(self.n);im=self.im.crop((0,0,1024,min(1024,(self.y+self.rh+1)//2*2)));im.save(D/(key+'.png'),optimize=True);A['pages'][key]={'path':'assets/game/levels/stage_08/effects/dracodia_energy_1110/'+key+'.png','size':list(im.size)};self.n+=1;self.x=self.y=self.rh=0;self.im=Image.new('RGBA',(1024,1024))
 def emit(self,name,im,pivot,collision=False):
  bbox=im.getbbox()or(0,0,2,2);x=bbox[0]//2*2;y=bbox[1]//2*2;right=min(im.width,(bbox[2]+1)//2*2);bottom=min(im.height,(bbox[3]+1)//2*2);q=im.crop((x,y,right,bottom));w,h=q.size;assert w%2==h%2==0
  if self.x+w>1024:self.x=0;self.y+=self.rh+2;self.rh=0
  if self.y+h>1024:self.flush()
  self.im.paste(q,(self.x,self.y));a={'key':'d124_'+str(self.n),'rect':[self.x,self.y,w,h],'offset':[x-pivot[0],y-pivot[1]],'w':w,'h':h,'logical':list(im.size),'pivot':pivot};A['banks'].setdefault(name,[]).append(a);self.x+=w+2;self.rh=max(self.rh,h)
  if collision:a['spans']=spans((np.array(q)[:,:,3]>128)&(np.array(q)[:,:,:3].max(2)>155))
  return a
def spans(mask):return[np.flatnonzero(np.diff(np.pad(row.astype(np.int8),(1,1)))).astype(int).tolist()for row in mask]
pack=Pack()
def read(p):
 p=Path(p);A['source_hashes'][str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();return Image.open(p).convert('RGBA')
def actor(bank,f):
 a=N['banks'][bank][f];s=N['sheets'][a['sheet']];im=read(R/s['path']);x,y,w,h=a['cell'];return im.crop((x,y,x+w,y+h)),a
def phactor(phase,f):
 a=P['banks']['body_'+phase+'_0'][f];im=read(R/P['pages'][a['key']]['path']);x,y,w,h=a['rect'];q=Image.new('RGBA',(512,512));q.paste(im.crop((x,y,x+w,y+h)),(256+a['offset'][0],256+a['offset'][1]));return q,P['poses'][a['pose']]
# Moving source beam material fills all lens pixels, including the dark pupil.
flows=[]
for f in range(8):
 a=E['banks']['beam_5'][f*2];im=read(R/E['pages'][a['key']]['path']);x,y,w,h=a['rect'];q=np.array(im.crop((x,y+45,x+w,y+45+w)));valid=q[:,:,3]>48;_,idx=distance_transform_edt(~valid,return_indices=True);q[:,:,:3]=q[idx[0],idx[1],:3];flows.append(q[:,:,:3])
def collar(source,centres,maxr,root,level,f,hit):
 v=np.array(source);Y,X=np.indices(v.shape[:2]);out=np.zeros_like(v);block=np.zeros(v.shape[:2],bool);details=[];flow=flows[f]
 for cx,cy in centres:
  region=(abs(X-cx)<maxr+1)&(abs(Y-cy)<maxr+1);warm=region&(v[:,:,3]>48)&(v[:,:,0]>125)&(v[:,:,0]>v[:,:,1]*1.035)&(v[:,:,0]>v[:,:,2]*1.06)
  yy,xx=np.nonzero(warm);radius=min(maxr,max(8,((xx.max()-xx.min()+1)+(yy.max()-yy.min()+1))/4))if len(xx)else maxr
  lens=((X-cx)**2+(Y-cy)**2<=radius**2)&(v[:,:,3]>48);rim=((X-cx)**2+(Y-cy)**2<=(radius+4.5)**2)&~lens&(v[:,:,3]>48);block|=rim;out[rim]=v[rim]
  if hit:out[rim,:3]=255
  tex=flow[(Y-cy+f*3)%len(flow),(X-cx+flow.shape[1]//2)%flow.shape[1]].copy();strength=[.42,.64,.83,1][level];tex=(tex.astype(float)*strength+np.array([180,35,0])*(1-strength)).clip(0,255).astype('uint8');out[lens,:3]=tex[lens];out[lens,3]=255;details.append({'center':[cx-root[0],cy-root[1]],'radius':radius,'pixels':int(lens.sum()),'opaque':bool(np.all(out[lens,3]==255))})
 return Image.fromarray(out),block,details
for bank in ['brain','charge','focus']:
 for f in range(len(N['banks'][bank])):
  im,a=actor(bank,f);key='eye-'+bank+'-'+str(f);block=None
  for level in range(4):
   for hit in [False,True]:
    name=key+'-'+str(level)+('-hit'if hit else'')
    for phase in range(8):
     q,mask,d=collar(im,a['eyes'],17.5,[192,192],level,phase,hit);q=q.crop((124,194,252,274));pack.emit(name,q,[68,-2])
    block=mask
  A['eyes'][a['key']]={'bank':key,'block':spans(block[194:274,124:252]),'blockOffset':[-68,2],'details':d}
for phase in ['recover','wind','strike']:
 for f in range(len(P['banks']['body_'+phase+'_0'])):
  im,pose=phactor(phase,f);cx=256+pose['core'][0];cy=256+pose['core'][1];key='core-'+phase+'-'+str(f)
  for level in range(4):
   for hit in [False,True]:
    name=key+'-'+str(level)+('-hit'if hit else'')
    for k in range(8):
     q,mask,d=collar(im,[[cx,cy]],11.5,[cx,cy],level,k,hit);pack.emit(name,q.crop((cx-32,cy-32,cx+32,cy+32)),[32,32])
  A['phoenix'][phase+'_'+str(f)]={'bank':key,'block':spans(mask[cy-32:cy+32,cx-32:cx+32]),'blockOffset':[-32,-32],'details':d}
def generated(path,name,size):
 raw=read(path);shutil.copy2(path,O/(name+'-master.png'));cw=2*math.ceil(raw.width/4/2);ch=2*math.ceil(raw.height/2/2);frames=[]
 for f in range(8):
  x=round(f%4*raw.width/4);y=round(f//4*raw.height/2);xx=round((f%4+1)*raw.width/4);yy=round((f//4+1)*raw.height/2);q=Image.new('RGBA',(cw,ch));q.paste(raw.crop((x,y,xx,yy)),(0,0));v=np.array(q);valid=(v[:,:,3]>=110);labs,n=label(valid);counts=np.bincount(labs.ravel());keep=np.zeros_like(valid)
  for i in range(1,n+1):
   if counts[i]>=12:keep|=labs==i
  v[:,:,3]=np.where(keep,255,0);v[v[:,:,3]==0]=0;frames.append(Image.fromarray(v).resize(size,Image.Resampling.NEAREST))
 sample=np.concatenate([np.array(q)[np.array(q)[:,:,3]>0,:3]for q in frames])[::3];p=Image.fromarray(sample.reshape(1,-1,3)).quantize(colors=32,method=Image.Quantize.MEDIANCUT);pal=Image.new('P',(1,1));pal.putpalette(p.getpalette());out=[]
 for q in frames:rgb=q.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGB');rgb.putalpha(q.getchannel('A'));out.append(rgb)
 return out
base=Path('C:/Users/Mike/.codex/generated_images/01a1c263-6df7-7072-a76a-4b41ccbb8b8a')
def master(name,original):return W/(name+'-master.png')if(W/(name+'-master.png')).exists()else base/original
wind=generated(master('phoenix-vortex','exec-3b6e93ee-e531-430d-ab67-306754a47e63.png'),'phoenix-vortex',(288,288))
for level,size in enumerate([164,188,212,236,264]):
 for f in range(8):
  # Each production size comes directly from the generated master extraction.
  raw=Image.open(O/'phoenix-vortex-master.png').convert('RGBA');cw=2*math.ceil(raw.width/4/2);x=round(f%4*raw.width/4);y=round(f//4*raw.height/2);src=Image.new('RGBA',(cw,cw));src.paste(raw.crop((x,y,round((f%4+1)*raw.width/4),round((f//4+1)*raw.height/2))),(0,0));q=src.resize((size,size),Image.Resampling.NEAREST);cell=Image.new('RGBA',(288,288));cell.alpha_composite(q,((288-size)//2,(288-size)//2));v=np.array(cell);v[v[:,:,3]<110]=0;v[:,:,3]=np.where(v[:,:,3]>=110,255,0)
  if level==4:
   fade=v.copy();Y,X=np.indices((288,288));fade[((X//2)*7+(Y//2)*11)%8<=f,3]=0;pack.emit('wind-out',Image.fromarray(fade),[144,144])
  for front in [False,True]:
   a=v.copy();a[:178 if front else 0]=0
   if not front:a[178:]=0
   pack.emit('wind-'+str(level)+('-front'if front else'-rear'),Image.fromarray(a),[144,144])
shield=generated(master('brain-shield','exec-3045bde0-bbf3-4e6f-b85f-8c18cb1455a8.png'),'brain-shield',(352,352));Y,X=np.indices((352,352));angle=(np.arctan2(Y-176,X-176)+math.pi)/(2*math.pi)
for mode in ['deploy','loop','break']:
 for f in range(8):
  v=np.array(shield[f]).copy()
  if mode=='deploy':v[angle>(f+1)/8,3]=0
  if mode=='break':
   rank=((X//3)*7+(Y//3)*11)%8;v[rank<=f,3]=0
  for front in [False,True]:
   q=v.copy()
   if front:q[:176]=0
   else:q[176:]=0
   pack.emit('shield-'+mode+('-front'if front else'-rear'),Image.fromarray(q),[176,176])
bolt=generated(master('purple-lightning','exec-b8859837-8925-49f1-9d06-7c7e9af469a8.png'),'purple-lightning',(192,512))
for f,q in enumerate(bolt):
 v=np.array(q);v[(v[:,:,2]>v[:,:,0]*1.8)&(v[:,:,0]<70),3]=0
 # Register the impact point from the brightest lower horizontal burst.
 mass=(v[:,:,3]>0).sum(1);lo=400;iy=lo+int(np.argmax(mass[lo:500]));xs=np.flatnonzero(v[max(0,iy-2):iy+3,:,3].max(0));cx=int(round(xs.mean())) if len(xs) else 96;im=Image.new('RGBA',(192,512));im.paste(Image.fromarray(v),(96-cx,496-iy));pack.emit('bolt',im,[96,496],True)
# Existing authored circular ground Retina, doubled uniformly for the large bolt.
H=meta('herald_desperation_art_1029.js');print('herald metadata keys',list(H.keys()),flush=True)
# Read the native shared24-cell ground marker directly from its runtime registry.
s=(R/'assets/herald_desperation_1029.js').read_text(encoding='utf-8')if(R/'assets/herald_desperation_1029.js').exists()else''
import re
match=re.search(r"const HL51_ART=(\{.*?\});",s)
if not match:
 for file in(R/'assets').glob('*.js'):
  if 'art'in file.name:continue
  t=file.read_text(encoding='utf-8');m=re.search(r"const HL51_ART=(\{.*?\});",t)
  if m:match=m;break
assert match,'Native ground marker registry';path=re.search(r"path\s*:\s*['\"]([^'\"]+)",match[1]).group(1);marker=read(R/path)
for i in range(24):
 q=marker.crop((i%8*64,i//8*32,i%8*64+64,i//8*32+32)).resize((128,64),Image.Resampling.NEAREST);pack.emit('mark',q,[64,32])
pack.flush();(O/'art.json').write_text(json.dumps(A,separators=(',',':')));(W/'candidate/dracodia_energy_art_1110.js').write_text("'use strict';\nconst D124_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print(json.dumps({'banks':len(A['banks']),'frames':sum(len(x)for x in A['banks'].values()),'pages':len(A['pages'])}),flush=True)
