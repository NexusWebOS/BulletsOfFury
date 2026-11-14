from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil
W=Path(__file__).resolve().parent;ARCHIVED=W.parent.name=='_BUILD_SOURCE';R=W.parent.parent if ARCHIVED else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W/'export'if ARCHIVED else W.parents[1]/'outputs/helicopter-death';O.mkdir(parents=True,exist_ok=True);C=W/'candidate';D=C/'art';D.mkdir(parents=True,exist_ok=True);A={'version':'H126','banks':{},'pages':{},'sources':{},'chunks':{},'directions':64,'logical':{'dracodia':[512,512],'normal':[320,320],'furious':[320,320]},'scope':'Actual helicopter plates, offline yaw/rotor poses, actual-pixel shatter chunks and direct-master explosions.'}
class Pack:
 def __init__(self):self.im=Image.new('RGBA',(1024,1024));self.x=self.y=self.rh=self.n=0
 def flush(self):
  if not(self.y or self.rh):return
  key='h126_'+str(self.n);im=self.im.crop((0,0,1024,min(1024,(self.y+self.rh+1)//2*2)));im.save(D/(key+'.png'),optimize=True);A['pages'][key]={'path':'assets/game/shared/combat/helicopter_death_1111/'+key+'.png','size':list(im.size)};self.n+=1;self.x=self.y=self.rh=0;self.im=Image.new('RGBA',(1024,1024))
 def emit(self,name,im,pivot):
  b=im.getbbox()or(0,0,2,2);x=b[0]//2*2;y=b[1]//2*2;r=min(im.width,(b[2]+1)//2*2);bottom=min(im.height,(b[3]+1)//2*2);q=im.crop((x,y,r,bottom));w,h=q.size
  if self.x+w>1024:self.x=0;self.y+=self.rh+2;self.rh=0
  if self.y+h>1024:self.flush()
  self.im.paste(q,(self.x,self.y));A['banks'].setdefault(name,[]).append({'key':'h126_'+str(self.n),'rect':[self.x,self.y,w,h],'offset':[x-pivot[0],y-pivot[1]],'w':w,'h':h,'logical':list(im.size),'pivot':pivot});self.x+=w+2;self.rh=max(self.rh,h)
pack=Pack()
def read(p):
 p=Path(p);A['sources'][str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();return Image.open(p).convert('RGBA')
def meta(n):
 s=(R/'assets'/n).read_text(encoding='utf-8');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
HC=meta('dracodia_helicopter_art_1030.js');cache={}
def hc(name,f):
 a=HC['banks'][name][f];p=R/HC['pages'][a['key']]['path'];im=cache.get(p)
 if im is None:im=cache[p]=read(p)
 x,y,w,h=a['rect'];return im.crop((x,y,x+w,y+h)),a
def dracodia(mask,rotor):
 im=Image.new('RGBA',(512,512))
 for name,f,at in [('core_6',rotor,[256,256]),('pod_left',0,[256+HC['mounts'][6]['left'][0],256+HC['mounts'][6]['left'][1]]),('pod_right',0,[256+HC['mounts'][6]['right'][0],256+HC['mounts'][6]['right'][1]])]:
  if name=='pod_left'and mask&1 or name=='pod_right'and mask&2:continue
  q,a=hc(name,f);im.alpha_composite(q,(round(at[0]+a['offset'][0]),round(at[1]+a['offset'][1])))
 return im
families={}
for mask in range(4):
 frames=[]
 for d in range(64):
  im=dracodia(mask,d*5%16).rotate(-d*360/64,resample=Image.Resampling.NEAREST,center=(256,256));frames.append(im);pack.emit('spin-dracodia-'+str(mask),im,[256,256])
 families['dracodia-'+str(mask)]=(dracodia(mask,0),256)
for variant in ['normal','furious']:
 body=read(W/'sources'/('ovbody_critical'+('-furious'if variant=='furious'else'')+'.png'));frames=[]
 for d in range(64):
  rotor=read(W/'sources'/('ovrotor_'+str((d*5%16)*72//16).zfill(2)+'.png'));whole=body.copy();whole.alpha_composite(rotor);whole=whole.resize((196,196),Image.Resampling.NEAREST);im=Image.new('RGBA',(320,320));im.alpha_composite(whole,(62,62));im=im.rotate(-d*360/64,resample=Image.Resampling.NEAREST,center=(160,160));pack.emit('spin-'+variant,im,[160,160]);frames.append(im)
 families[variant]=(frames[0],160)
# Chunk banks preserve real fuselage/rotor/pod pixels, without generated filler.
for name,(im,pivot)in families.items():
 step=40 if name.startswith('dracodia') else 28;tiles=[]
 for y in range(0,im.height,step):
  for x in range(0,im.width,step):
   q=im.crop((x,y,min(x+step,im.width),min(y+step,im.height)));alpha=q.getchannel('A');mass=sum(v>48 for v in alpha.getdata())
   if mass>=35:tiles.append((mass,x,y,q))
 tiles=sorted(tiles,reverse=True)[:28];A['chunks'][name]=[]
 for i,(_,x,y,q)in enumerate(tiles):
  bank='chunk-'+name+'-'+str(i);cell=64;canvas=Image.new('RGBA',(cell,cell));canvas.paste(q,((cell-q.width)//2,(cell-q.height)//2));A['chunks'][name].append({'bank':bank,'origin':[x+q.width/2-pivot,y+q.height/2-pivot]})
  for f in range(8):pack.emit(bank,canvas.rotate(-f*45,resample=Image.Resampling.NEAREST,center=(32,32)),[32,32])
source=R/'_BUILD_SOURCE/helicopter_effects_1111/explosion-master.png';master=read(source);shutil.copy2(source,O/'explosion-master.png');cell=2*math.ceil(max(master.width,master.height)/4/2)
for size in [88,144,256,384]:
 for f in range(16):
  x=round(f%4*master.width/4);y=round(f//4*master.height/4);xx=round((f%4+1)*master.width/4);yy=round((f//4+1)*master.height/4);q=Image.new('RGBA',(cell,cell));q.paste(master.crop((x,y,xx,yy)),(0,0));q=q.resize((size,size),Image.Resampling.NEAREST)
  if f==15:q=Image.new('RGBA',(size,size))
  pack.emit('burst'+str(size),q,[size//2,size//2])
pack.flush();(O/'art.json').write_text(json.dumps(A,separators=(',',':')));(C/'helicopter_death_art_1111.js').write_text("'use strict';\nconst H126_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print(json.dumps({'banks':len(A['banks']),'frames':sum(map(len,A['banks'].values())),'pages':len(A['pages']),'chunks':{k:len(v)for k,v in A['chunks'].items()}}),flush=True)
