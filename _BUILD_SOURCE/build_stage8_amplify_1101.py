"""Stage8 unique authored modular hulls, registered joints and ordnance.
Source-preserving even-cell exports; all rotations are offline direction cells.
"""
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,maximum_filter
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/stage8_amplify_1101';O=R/'assets/game/levels/stage_08/enemies/amplify_1101';Q=R/'_shots/stage8_amplify_1101'
for p in[S,O,Q]:p.mkdir(parents=True,exist_ok=True)
M={'owner':'_BUILD_SOURCE/build_stage8_amplify_1101.py','models':{},'banks':{},'sources':{},'retired':['s8leech','s8gravity1003','s8razor','s8solar','s8prism1003','ll18raptor','ll18spear','ll18herald','ll18brood']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(p,n):return json.JSONDecoder().raw_decode((R/p).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
def clean(t):
 a=np.array(t.convert('RGBA'));ids,_=label(a[:,:,3]>65);counts=np.bincount(ids.ravel());keep=counts>=max(4,counts[1:].max()*.00015);keep[0]=False;a[:,:,3]=np.where(keep[ids],255,0);return Image.fromarray(a)
def source(n):
 p=S/(n+'_source.png');M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'tool':'built-in image_gen','promptFile':'_BUILD_SOURCE/stage8_amplify_1101/prompts.md'};return clean(Image.open(p))
def pad(t,p=None,c=None):
 p=p or[t.width/2,t.height/2]
 if c is None:
  yy,xx=np.nonzero(np.array(t)[:,:,3]>0);radius=np.sqrt((xx-p[0])**2+(yy-p[1])**2).max()if len(xx)else 24;c=max(64,math.ceil((radius*2+16)/2)*2)
 z=Image.new('RGBA',(c,c));z.alpha_composite(t,(round(c/2-p[0]),round(c/2-p[1])));return z
def plate(n):return source(n).resize((256,256),Image.Resampling.NEAREST)
def bank(n,fs,dirs=32):
 c=fs[0].width;assert c%2==0 and all(t.size==(c,c)for t in fs);cols=min(16,dirs);rows=math.ceil(dirs/cols);z=Image.new('RGBA',(c*cols,c*len(fs)*rows))
 for f,t in enumerate(fs):
  for d in range(dirs):z.alpha_composite(t.rotate(-d*360/dirs,Image.Resampling.NEAREST),(d%cols*c,(f*rows+d//cols)*c))
 p=O/(n+'.webp');z.save(p,format='WEBP',lossless=True,method=4);B={'key':'s811_'+n,'path':p.relative_to(R).as_posix(),'cell':c,'dirs':dirs,'frames':len(fs),'cols':cols,'dirRows':rows,'sha256':sha(p)};M['banks'][n]=B;return B
def mask(t,poly):
 v=Image.new('L',t.size);ImageDraw.Draw(v).polygon(poly,fill=255);a=np.array(t);a[:,:,3]=np.minimum(a[:,:,3],np.array(v));return Image.fromarray(a)
def cut(t,poly):
 v=mask(t,poly);a=np.array(t);a[:,:,3][np.array(v)[:,:,3]>0]=0;return Image.fromarray(a),v
def emissive(t,color,shield=False):
 a=np.array(t);rgb=a[:,:,:3].astype(float);em=(a[:,:,3]>0)&(rgb.max(2)-rgb.min(2)>45)&(rgb.max(2)>95);h=a[:,:,3]>0
 if shield:v=np.where(em,150,np.where(maximum_filter(h,3)&~h,155,np.where(maximum_filter(h,7)&~h,36,0)))
 else:v=np.where(em,190,np.where(maximum_filter(em,3),60,0))
 z=np.zeros_like(a);z[:,:,:3]=color;z[:,:,3]=v;return Image.fromarray(z)
def preview(n,fs):
 out=Image.new('RGB',(192*min(8,len(fs)),210*math.ceil(len(fs)/8)),(8,13,22));d=ImageDraw.Draw(out)
 for i,t in enumerate(fs):
  z=t.copy();z.thumbnail((192,192),Image.Resampling.NEAREST);x=i%8*192;y=i//8*210;out.paste(z,(x+(192-z.width)//2,y+18),z);d.text((x+4,y),str(i),fill='white')
 out.save(Q/(n+'-frames.jpg'),quality=93)
def snap(t,p):
 a=np.array(t);yy,xx=np.nonzero(a[:,:,3]>160);j=np.argmin((xx-p[0])**2+(yy-p[1])**2);return[int(xx[j]),int(yy[j])]
def part(n,t,p,mount,tip,role='gun',color=(178,78,255),frames=None):
 frames=frames or[pad(t,p)];B=bank(n,frames);G=bank(n+'_glow',[emissive(f,color)for f in frames]);H=bank(n+'_shield',[emissive(f,color,True)for f in frames]);tip=snap(t,tip)
 return {'bank':B,'glow':G,'shield':H,'mount':mount,'muzzle':[tip[0]-p[0],tip[1]-p[1]],'role':role}
def rect(x0,y0,x1,y1):return[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
# Fixed source-coordinate modular anatomy: polygon, swivel, muzzle, role.
DEFS={
 'interceptor':(138,[ (rect(43,96,88,228),[68,105],[64,211],'gun'),(rect(168,96,213,228),[188,105],[192,211],'gun')],[[109,37],[147,37]],(185,95,255)),
 'hexpyre':(162,[(rect(0,59,89,235),[61,74],[33,211],'gun'),(rect(167,59,256,235),[195,74],[221,211],'gun')],[],(255,109,24)),
 'voidjet':(256,[(rect(28,112,88,252),[64,123],[49,229],'gun'),(rect(168,112,228,252),[192,123],[207,229],'gun'),(rect(0,66,36,114),[20,79],[20,106],'missile'),(rect(220,66,256,114),[236,79],[236,106],'missile')],[[105,30],[151,30]],(143,70,255)),
 'hellwing':(156,[(rect(65,113,95,168),[80,123],[80,157],'gun'),(rect(161,113,191,168),[176,123],[176,157],'gun'),(rect(9,92,38,141),[24,102],[24,135],'missile'),(rect(218,92,247,141),[232,102],[232,135],'missile')],[[109,25],[147,25]],(255,54,16)),
 'parasite':(142,[(rect(35,151,91,243),[72,165],[56,221],'gun'),(rect(165,151,221,243),[184,165],[200,221],'gun'),(rect(0,13,99,102),[64,35],[19,85],'claw'),(rect(157,13,256,102),[192,35],[237,85],'claw'),(rect(0,101,93,193),[53,118],[18,171],'claw'),(rect(163,101,256,193),[203,118],[238,171],'claw')],[],(255,52,179)),
 'crescent':(150,[(rect(16,130,50,241),[32,142],[32,231],'gun'),(rect(206,130,240,241),[224,142],[224,231],'gun')],[[128,24]],(240,90,247)),
 'skull':(146,[(rect(44,131,85,245),[67,143],[60,235],'gun'),(rect(171,131,212,245),[189,143],[196,235],'gun')],[[109,25],[147,25]],(226,215,186)),
 'symbiote':(158,[(rect(46,128,88,226),[69,139],[69,204],'gun'),(rect(168,128,210,226),[187,139],[187,204],'gun')],[[108,25],[148,25]],(255,76,208)),
 'warp':(242,[(rect(0,116,74,226),[42,116],[37,188],'gun'),(rect(182,116,256,226),[214,116],[219,188],'gun')],[],(255,104,43)),
 'blue':(248,[(rect(0,111,79,234),[50,111],[27,201],'gun'),(rect(177,111,256,234),[206,111],[229,201],'gun')],[],(47,151,255)),
 'carrier':(266,[(rect(45,94,83,134),[68,103],[55,127],'gun'),(rect(173,94,211,134),[188,103],[201,127],'gun'),(rect(45,158,83,198),[68,168],[55,192],'gun'),(rect(173,158,211,198),[188,168],[201,192],'gun')],[[95,12],[116,12],[140,12],[161,12]],(158,77,255)),
 'deathorb':(184,[(rect(0,0,88,71),[76,54],[28,47],'gun'),(rect(168,0,256,71),[180,54],[228,47],'gun'),(rect(0,175,76,256),[62,187],[24,230],'gun'),(rect(180,175,256,256),[194,187],[232,230],'gun')],[],(183,66,255)),
 'furnacemaw':(202,[(rect(0,109,66,233),[35,132],[33,214],'gun'),(rect(190,109,256,233),[221,132],[223,214],'gun')],[],(255,85,20)),
 'bomber':(182,[],[[96,28],[117,28],[139,28],[160,28]],(142,66,255))}
for n,(span,defs,tails,color)in DEFS.items():
 im=plate(n);body=im.copy();mods=[]
 for i,(poly,p,tip,role)in enumerate(defs):body,t=cut(body,poly);mods.append(part(n+'_part'+str(i),t,p,p,tip,role,color))
 fs=[pad(body)];M['models'][n]={'bank':bank(n+'_body',fs),'full':bank(n+'_full',[pad(im)]),'glow':bank(n+'_body_glow',[emissive(f,color)for f in fs]),'shield':bank(n+'_body_shield',[emissive(f,color,True)for f in fs]),'span':span,'modules':mods,'tails':tails,'color':color,'core':[128,128]};preview(n,[pad(im),*fs]);print('Exported',n,flush=True)
# Harrier repurposes the actual existing laser head, with its physical trunnion.
im=plate('harrier');head=Image.open(R/'_BUILD_SOURCE/stage7_amplify_1101/overhaul_ground_head_laser.png').convert('RGBA').resize((108,108),Image.Resampling.NEAREST);mods=[]
for i,p in enumerate([[60,120],[196,120],[128,164]]):mods.append(part('harrier_turret'+str(i),head,[54,30],p,[54,91],color=(175,86,255)))
M['models']['harrier']={'bank':bank('harrier_body',[pad(im)]),'full':bank('harrier_full',[pad(im)]),'glow':bank('harrier_glow',[emissive(pad(im),(175,86,255))]),'shield':bank('harrier_shield',[emissive(pad(im),(175,86,255),True)]),'span':204,'modules':mods,'tails':[[94,30],[162,30]],'color':[175,86,255],'core':[128,128]}
# Retained Imp front identity, generated depth spin, separated side weapon fins.
raw=Image.open(S/'mm1003_impharrow.png').convert('RGBA');raw.thumbnail((256,256),Image.Resampling.NEAREST);im=pad(raw,c=256);body=im.copy();mods=[]
for i,(poly,p,tip)in enumerate([(rect(0,63,80,176),[71,127],[34,146]),(rect(176,63,256,176),[185,127],[222,146])]):body,t=cut(body,poly);mods.append(part('imp_fin'+str(i),t,p,p,tip,color=(255,63,10)))
def strip(n,span,c=256):
 z=source(n);fs=[clean(z.crop((round(i%4*z.width/4),round(i//4*z.height/2),round((i%4+1)*z.width/4),round((i//4+1)*z.height/2))))for i in range(8)]
 boxes=[t.getbbox()for t in fs];k=span/max(max(b[2]-b[0],b[3]-b[1])for b in boxes);out=[]
 for t,b in zip(fs,boxes):
  v=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);out.append(pad(v,[(b[0]+b[2])/2*k,(b[1]+b[3])/2*k],c))
 preview(n,out);return out
fs=strip('imp_spin',240,384);fs[0]=pad(im,c=384);M['models']['imp']={'bank':bank('imp_body',[pad(body)]),'full':bank('imp_full',[pad(im)]),'glow':bank('imp_glow',[emissive(pad(body),(255,64,18))]),'shield':bank('imp_shield',[emissive(pad(body),(255,64,18),True)]),'spin':bank('imp_spin',fs,1),'span':158,'modules':mods,'tails':[],'color':[255,64,18],'core':[128,119]}
# Source-exact Hunter: retain its authored skin; independent eye/side cannons.
raw=Image.open(S/'stalker_identity.png').convert('RGBA');raw.thumbnail((236,236),Image.Resampling.NEAREST);im=pad(raw,c=256);body=im.copy();mods=[]
for i,(poly,p,tip)in enumerate([(rect(37,38,100,126),[88,82],[92,98]),(rect(156,38,219,126),[168,82],[164,98])]):body,t=cut(body,poly);mods.append(part('hunter_eye'+str(i),t,p,p,tip,color=(37,171,255)))
hunterBase=body.copy();hunterFull=pad(im)
M['models']['hunter']={'bank':bank('hunter_body',[pad(body)]),'full':bank('hunter_full',[pad(im)]),'glow':bank('hunter_glow',[emissive(pad(body),(37,171,255))]),'shield':bank('hunter_shield',[emissive(pad(body),(37,171,255),True)]),'span':192,'modules':mods,'tails':[],'color':[37,171,255],'core':[128,93],'eyes':[[128,94]]}
preview('hunter',[pad(im),pad(body)])
# Source-derived tentacle chains. Each alpha pixel belongs to exactly one
# nearest link; joints use actual authored ball pixels as seam caps.
def tentacles(n,im,chains,polys,span,color,extra=None):
 body=im.copy();arms=[]
 for ai,(chain,poly)in enumerate(zip(chains,polys)):
  body,t=cut(body,poly);a=np.array(t);yy,xx=np.indices(a.shape[:2]);dist=[]
  for j,(p,q)in enumerate(zip(chain,chain[1:])):
   dx=q[0]-p[0];dy=q[1]-p[1];u=np.clip(((xx-p[0])*dx+(yy-p[1])*dy)/max(1,dx*dx+dy*dy),0,1);dist.append((xx-p[0]-u*dx)**2+(yy-p[1]-u*dy)**2)
  labels=np.argmin(dist,axis=0);links=[]
  for j,(p,q)in enumerate(zip(chain,chain[1:])):
   z=a.copy();z[:,:,3][labels!=j]=0;z=Image.fromarray(z);links.append(part(n+'_arm'+str(ai)+'_'+str(j),z,p,p,q,'tentacle',color));links[-1]['joint']=[q[0]-p[0],q[1]-p[1]]
  arms.append({'root':chain[0],'links':links})
 out=extra or{};out.update(bank=bank(n+'_body',[pad(body)]),full=bank(n+'_full',[pad(im)]),glow=bank(n+'_glow',[emissive(pad(body),color)]),shield=bank(n+'_shield',[emissive(pad(body),color,True)]),span=span,arms=arms,color=color);out.setdefault('modules',[]);out.setdefault('tails',[]);out.setdefault('core',[128,103]);M['models'][n]=out;preview(n,[pad(im),pad(body)])
im=plate('tentacle');left=[[[93,70],[79,51],[63,12],[27,42]],[[93,94],[53,99],[33,78],[31,119]],[[106,119],[95,142],[73,174],[90,225]]];lp=[[(0,0),(91,0),(107,77),(85,82),(0,66)],[(0,66),(91,77),(101,113),(60,133),(0,144)],[(43,123),(105,112),(125,138),(125,256),(40,256)]];chains=left+[[[256-x,y]for x,y in c]for c in left];polys=lp+[[(256-x,y)for x,y in poly]for poly in lp];tentacles('tentacle',im,chains,polys,248,(154,74,255))
# Hunter's retained two long lashes gain two connected source-pixel links.
im=hunterBase;h=M['models']['hunter'];left=[[91,117],[82,153],[71,220]];right=[[165,117],[174,153],[185,220]];polys=[[(25,116),(103,116),(112,256),(25,256)],[(153,116),(231,116),(231,256),(144,256)]];tentacles('hunter',im,[left,right],polys,192,(37,171,255),h);h['full']=bank('hunter_full',[hunterFull])
M['models']['hunter']['eyes']=[[128,94]]
# Carrier hatch is a separate fixed-pivot authored eight-pose bay module.
fs=strip('hatch',108,160);B=bank('carrier_hatch',fs);M['models']['carrier']['hatch']={'bank':B,'point':[128,131],'scale':1.05};M['models']['carrier']['bay']=[128,157]
# Generated bone, physical dark bombs and flowing dark matter.
for n,span,c in [('bone',94,128),('bomb',100,128),('darkorb',96,128)]:
 fs=strip(n,span,c);bank(n,fs,16 if n!='darkorb'else 1)
 if n=='darkorb':bank(n+'_glow',[emissive(f,(156,67,255))for f in fs],1)
# One continuous flame plume, with its physical muzzle at the frame centre.
# Shared scale across the strip; no repeated nozzle/hardware down the beam.
z=source('flame');tiles=[clean(z.crop((round(i%4*z.width/4),round(i//4*z.height/2),round((i%4+1)*z.width/4),round((i//4+1)*z.height/2))))for i in range(8)];boxes=[t.getbbox()for t in tiles];k=170/max(b[3]-b[1]for b in boxes);fs=[]
for t,b in zip(tiles,boxes):
 a=np.array(t);yy,xx=np.nonzero((a[:,:,3]>120)&(np.indices(a.shape[:2])[0]<b[1]+8));px=float(np.median(xx));v=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);fs.append(pad(v,[px*k,b[1]*k],384))
B=bank('flame',fs,16);B['length']=170;B['width']=max(b[2]-b[0]for b in boxes)*k;preview('flame',fs)
# Reuse approved fire ordnance; create violet/blue routes without changing alpha.
V=data('assets/stage2_amplify_art_1031.js','V31_ART')
for theme,color in [('fire',None),('void',(1.12,.45,1.8)),('blue',(.36,1.16,1.8))]:
 for n,src in [('slug','slug'),('laser','laser'),('orb','orb'),('muzzle','muzzle'),('thruster','thruster'),('missile','thunder_missile'),('flame','flamethrower')]:
  B=V['banks'][src];im=Image.open(R/B['path']).convert('RGBA');a=np.array(im)
  if color:
   rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);sel=(rgb.max(2)-rgb.min(2)>24)&(a[:,:,3]>0);ramp=lum[:,:,None]*np.array(color);a[:,:,:3][sel]=np.minimum(255,ramp)[sel].astype('uint8')
  p=O/(theme+'_'+n+'.webp');Image.fromarray(a).save(p,format='WEBP',lossless=True,method=4);M['banks'][theme+'_'+n]={**B,'key':'s811_'+theme+'_'+n,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'source':B['path']}
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(S/'generation.json').write_text(json.dumps(M['sources'],indent=2)+'\n',encoding='utf-8');(R/'assets/stage8_amplify_art_1101.js').write_text('"use strict";\nconst S811_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Registered',len(M['models']),'models and',len(M['banks']),'fixed even source banks',flush=True)
