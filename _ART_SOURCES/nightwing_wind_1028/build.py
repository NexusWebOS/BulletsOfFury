from pathlib import Path
from PIL import Image,ImageDraw
from locked_motion import locked_motion,belly
from gust_assets import gust_banks,contact
import numpy as np,math,json,colorsys,os,subprocess,hashlib
W=Path(__file__).resolve().parent;R=Path(os.environ.get('BOF_REPO',str(W.parents[1])));D=R/'assets/game/levels/stage_06/boss/nightwing_wind_1028';D.mkdir(parents=True,exist_ok=True)
M={'banks':{},'aliases':{},'sockets':{},'sources':{},'pixellab':{'ring':'4eba8168-3c04-4858-a4a0-e843f2b5f243','charge':'b12506e1-7690-400b-92a0-462a2e2f4851','bullet':'2009ff50-011a-4117-98a8-4d4030ac9fda'}}
def readjs(p):
 s=(R/p).read_text(encoding='utf-8');return json.loads(s[s.index('{'):s.rindex('}')+1])
old=readjs('assets/nightwing_entrance_art_1027.js');nf=readjs('assets/nightwing_flight_art_1027.js')
native=Image.open(R/'assets/game/levels/stage_06/boss/sky_repair_1004i/ace.png').convert('RGBA')
def pad(q,size=272):
 c=Image.new('RGBA',(size,size));c.alpha_composite(q,((size-q.width)//2,(size-q.height)//2));return c
def n(i):return pad(native.crop((i*176,0,(i+1)*176,184)).resize((184,192),Image.Resampling.NEAREST))
def recolor(q,cockpit=(136,169)):
 a=np.array(q);rgb=a[:,:,:3].astype(float)/255;hi=rgb.max(2);lo=rgb.min(2);mask=(a[:,:,3]>0)&(hi-lo>.07)&(rgb[:,:,2]>rgb[:,:,0]*1.35)&(rgb[:,:,2]>rgb[:,:,1]*.98)
 # Palette edit only, retaining authored value/shading and alpha. Cockpit
 # keeps its own deep royal-blue glass ramp rather than inheriting the hull.
 diff=hi-lo;teal=np.stack([lo,hi,hi-diff*.18],axis=2);a[:,:,:3][mask]=np.rint(teal[mask]*255).astype(np.uint8)
 cx,cy=cockpit;yy,xx=np.indices(hi.shape);glass=(a[:,:,3]>0)&(abs(xx-cx)<=10)&(abs(yy-cy)<=20)&(rgb[:,:,2]>rgb[:,:,0]*1.5)&(rgb[:,:,1]>rgb[:,:,0]*1.4);diff=np.maximum(diff,hi*.48);blue=np.stack([hi-diff,hi-diff*.75,hi],axis=2);a[:,:,:3][glass]=np.rint(blue[glass]*255).astype(np.uint8)
 return Image.fromarray(a)
def point(x,y,a,s=1):return[(x*math.cos(a)-y*math.sin(a))*s,(x*math.sin(a)+y*math.cos(a))*s]
def rotate(q,a,s=1,size=272):
 if s!=1:q=q.resize((round(q.width*s),round(q.height*s)),Image.Resampling.NEAREST)
 return pad(q.rotate(-a*180/math.pi,Image.Resampling.NEAREST,expand=True),size)
def meta(eng=[[-12.5,-64],[12.5,-64]],angle=0,scale=1):return{'engines':eng,'angle':angle,'scale':scale}
def transformed(m,a,s=1):return meta([point(x,y,a,s)for x,y in m['engines']],m['angle']+a,m['scale']*s)
def export(name,ff,metas=None,cols=8):
 cw,ch=ff[0].size;cols=min(cols,4096//cw);o=Image.new('RGBA',(cols*cw,math.ceil(len(ff)/cols)*ch))
 for i,q in enumerate(ff):o.alpha_composite(q,(i%cols*cw,i//cols*ch))
 identity=name in ['whole','whole_hit','clean','clean_hit','heading','heading_hit','flyover','flyover_hit','drift_left','drift_left_hit','drift_right','drift_right_hit','approach','approach_hit','death_large','death_large_hit']or name.endswith('_shadow');flight=name in ['heading','heading_hit','drift_left','drift_left_hit','drift_right','drift_right_hit']or name.endswith('_shadow');path=D/(name+('_gusts_1028'if name in ['wind_bullet','wind_muzzle']else'_flight_1028c'if flight else'_identity_1028b'if identity else'')+'.png');o.save(path,optimize=True);M['banks'][name]={'key':'nw30_'+name,'path':path.relative_to(R).as_posix(),'cw':cw,'ch':ch,'cols':cols,'frames':len(ff),'pivot':[cw//2,ch//2]}
 if metas:M['sockets'][name]=metas
 return o
# One authored planform is the identity source for every visible attitude.
top=recolor(n(0));damaged=recolor(n(1));under=belly(top,recolor(n(2)))
roll=[locked_motion(top,under,'roll',f*math.tau/16)for f in range(16)]
pitch=[locked_motion(top,under,'pitch',f*math.tau/16)for f in range(16)]
frames=[];sockets=[]
for i in range(107):
 if i<8:q=top.copy();m=meta()
 elif i<16:q=damaged.copy();m=meta()
 elif i==16:q=under.copy();m=meta()
 elif 17<=i<33:q,m=roll[i-17]
 elif 33<=i<49:q,m=pitch[i-33]
 elif 49<=i<65:
  q,m=pitch[i-49];q=rotate(q,math.pi);m=transformed(m,math.pi)
 elif i in [65,66]:q,m=roll[1 if i==65 else 15]
 elif 67<=i<75:q=rotate(top,math.pi);m=transformed(meta(),math.pi)
 else:a=(i-75)*math.tau/32;q=rotate(damaged,a);m=transformed(meta(),a)
 frames.append(q);sockets.append(m)
M['identity']={'source':'assets/game/levels/stage_06/boss/sky_repair_1004i/ace.png','sha256':hashlib.sha256(native.tobytes()).hexdigest(),'contract':'One canonical hull planform; source-pixel bank/roll/pitch projections authored offline. No Part2 flight silhouettes. Matching masks, shadows and transformed engine anchors.'}
M['sources']['locked_motion.py']=hashlib.sha256((W/'locked_motion.py').read_bytes()).hexdigest()
export('whole',frames,sockets);M['aliases'][old['whole']['key']]='whole'
def hit(ff):
 out=[]
 for q in ff:c=Image.new('RGBA',q.size,'white');c.putalpha(q.getchannel('A'));out.append(c)
 return out
export('whole_hit',hit(frames));M['aliases'][old['whole_hit']['key']]='whole_hit'
def src(group,i=0):return frames[old['groups'][group]['start']+i]
def sm(group,i=0):return sockets[old['groups'][group]['start']+i]
for name,entry in nf['banks'].items():
 if name.endswith('_shadow')or name.endswith('_hit'):continue
 ff=[];mm=[]
 if name=='heading':
  for bank in ['south','bank_left','bank_right']:
   for i in range(64):a=i*math.tau/64;f=i%8 if bank=='south'else 0;ff.append(rotate(src(bank,f),a));mm.append(transformed(sm(bank,f),a))
 elif name=='flyover':
  for i in range(8):ff.append(rotate(src('south',i),math.pi,1.6,432));mm.append(transformed(sm('south',i),math.pi,1.6))
 elif name.startswith('drift_'):
  side=1 if name.endswith('right')else-1
  for i in range(48):
   u=i/47;roll=side*math.radians(28)*math.sin(math.pi*u);q,m=locked_motion(top,under,'roll',roll);a=math.pi+side*math.pi*u;s=1.6-.95*(u*u*(3-2*u));ff.append(rotate(q,a,s,432));mm.append(transformed(m,a,s))
 elif name=='approach':
  for i in range(16):s=.65+.35*(i/15)**.65;ff.append(rotate(src('south',i%8),0,s));mm.append(transformed(sm('south',i%8),0,s))
 elif name=='death_large':
  for i in range(32):a=i*math.tau/32;ff.append(rotate(src('damaged',i%8),a,1.6,432));mm.append(transformed(sm('damaged',i%8),a,1.6))
 cols=14 if name=='heading'else 8
 export(name,ff,mm,cols=cols);M['aliases'][entry['key']]=name
 if name=='heading':M['banks'][name].update(directions=64,bankPoses=3)
 if name+'_hit'in nf['banks']:export(name+'_hit',hit(ff),cols=cols);M['aliases'][nf['banks'][name+'_hit']['key']]=name+'_hit'
 # Keep the exact pose alpha for a single offset shadow, including cruise/yaw.
 shadows=[]
 for q in ff:
  shadow=Image.new('RGBA',q.size,(2,7,14,0));shadow.putalpha(q.getchannel('A').point(lambda v:round(v*.56)));shadows.append(shadow)
 export(name+'_shadow',shadows,cols=cols)
 if name+'_shadow'in nf['banks']:M['aliases'][nf['banks'][name+'_shadow']['key']]=name+'_shadow'

# Separate non-destructible recoil modules, fitted to the actual whole plate.
clean=[]
for q in frames[:17]:
 q=q.copy()
 for x in[72,188]:q.paste((0,0,0,0),(x,136,x+12,180))
 clean.append(q)
export('clean',clean);export('clean_hit',hit(clean))
for side,x in[('left',72),('right',188)]:
 gun=frames[0].crop((x,136,x+12,180));ff=[];muzzles=[]
 for direction in range(32):
  a=direction*math.tau/32
  for recoil in[0,-2,-4,-2]:
   base=Image.new('RGBA',(96,96));base.alpha_composite(gun,(42,42+recoil));ff.append(rotate(base,a,size=96));muzzles.append(point(0,32+recoil,a))
 export('gun_'+side,ff);export('gun_'+side+'_hit',hit(ff));M['sockets']['gun_'+side]=muzzles
# The normal whole hull, modular body and aimed/recoiling guns need shadows too.
for name in ['whole','clean','gun_left','gun_right']:
 a=M['banks'][name];im=Image.open(R/a['path']).convert('RGBA');ff=[]
 for i in range(a['frames']):
  x=i%a['cols']*a['cw'];y=i//a['cols']*a['ch'];q=im.crop((x,y,x+a['cw'],y+a['ch']));shadow=Image.new('RGBA',q.size,(2,7,14,0));shadow.putalpha(q.getchannel('A').point(lambda v:round(v*.56)));ff.append(shadow)
 export(name+'_shadow',ff)
M['flight']={'headings':64,'driftFrames':48,'driftBankDegrees':28,'shadowAlpha':.56,'shadowOffset':[18,76],'contract':'Exact pose silhouettes; fixed pixel-alpha, drawn once behind all aircraft layers; continuous source-pixel bank through the tangent-aligned half turn.'}
# PixelLab animated plasma plumes, proportional size variants with fixed root.
M['exhaustFrames']=8;M['pixellab']['thruster']='9416e797-7447-4e4e-9482-3973b78e6ca7'
plumes=[Image.open(p).convert('RGBA')for p in sorted((W/'pixellab/thruster_frames').glob('*.png'))[1:9]]
for mode,wh,cellsize in [('small',(12,24),96),('cruise',(24,48),96),('boost',(48,96),192),('large',(76,152),320)]:
 ff=[]
 for direction in range(32):
  for q in plumes:
   q=q.resize(wh,Image.Resampling.NEAREST);c=Image.new('RGBA',(320,320));c.alpha_composite(q,(160-round(32*wh[0]/64),160-round(126*wh[1]/128)));ff.append(rotate(c,direction*math.tau/32,size=cellsize))
 if mode=='large':
  export('exhaust_large_a',ff[:128],cols=12);export('exhaust_large_b',ff[128:],cols=12)
 else:export('exhaust_'+mode,ff,cols=16 if mode=='boost'else 8)
def vfx(name,size):
 data=json.loads((W/'pixellab'/f'{name}.json').read_text());im=Image.open(W/'pixellab'/f'{name}.png').convert('RGBA');out=[]
 for f in data['frames']:
  r=f['frame'];q=im.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h']));q.thumbnail((size,size),Image.Resampling.NEAREST);out.append(pad(q,size))
 return out
rings=vfx('wind_ring',160);ff=[]
for direction in range(16):
 for q in rings:ff.append(rotate(q,direction*math.tau/16,size=192))
export('wind_ring',ff,cols=8);export('wind_charge',vfx('wind_charge',272),cols=8)
# Directional PixelLab gusts replace the retired disc projectile.
gusts,gustMeta=gust_banks(W)
for name,ff in gusts.items():
 export(name,ff,cols=16);M['banks'][name].update(directions=gustMeta['directions'],phaseFrames=gustMeta['phaseFrames']if name=='wind_bullet'else gustMeta['muzzleFrames'])
M['gusts']=gustMeta;M['pixellab']['bullet']=gustMeta['keyframeJob'];M['pixellab']['gustAnimation']=gustMeta['animationJob'];contact(W,W/'gust-contact.png')
(D/'manifest.json').write_text(json.dumps(M,indent=2));(R/'assets/nightwing_wind_art_1028.js').write_text('"use strict";\nconst NW30_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8')
preview=Image.new('RGBA',(816,544),(12,24,36,255));d=ImageDraw.Draw(preview)
for i,(name,q)in enumerate([('TEAL / ROYAL COCKPIT',frames[0]),('BANKED',frames[65]),('NORTH',frames[67]),('INVERTED',frames[16]),('MODULAR BODY',clean[0]),('WIND CHARGE',vfx('wind_charge',272)[8])]):preview.alpha_composite(q,(i%3*272,i//3*272));d.text((i%3*272+8,i//3*272+8),name,fill='white')
preview.save(W/'wind-poses.png');print(json.dumps({'banks':len(M['banks']),'frames':sum(b['frames']for b in M['banks'].values())}))
