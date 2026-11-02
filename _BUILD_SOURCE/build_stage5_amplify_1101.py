"""Stage5 source-preserving motion and violet ordnance export; fixed even cells.
Generated originals are retained; offline directional exports never rotate in-game.
"""
from pathlib import Path
import json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/stage5_amplify_1101';O=R/'assets/game/levels/stage_05/enemies/amplify_1101';Q=R/'_shots/stage5_amplify_1101'
for p in[S,O,Q]:p.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
M={'owner':'_BUILD_SOURCE/build_stage5_amplify_1101.py','models':{},'banks':{},'sources':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(p,n):return json.JSONDecoder().raw_decode((R/p).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
def bank(n,fs,dirs=32):
 c=fs[0].width;assert c%2==0 and all(f.size==(c,c)for f in fs);im=Image.new('RGBA',(c*dirs,c*len(fs)))
 for f,t in enumerate(fs):
  for d in range(dirs):im.alpha_composite(t.rotate(-d*360/dirs,Image.Resampling.NEAREST),(d*c,f*c))
 p=O/(n+'.webp');im.save(p,format='WEBP',lossless=True,method=4);B={'key':'s511_'+n,'path':p.relative_to(R).as_posix(),'cell':c,'dirs':dirs,'frames':len(fs),'cols':dirs,'dirRows':1,'sha256':sha(p)};M['banks'][n]=B;return B
def normalize(fs,span=104,c=160,pivots=None):
 boxes=[t.getbbox()for t in fs];k=span/max(max(b[2]-b[0],b[3]-b[1])for b in boxes);out=[]
 for i,t in enumerate(fs):
  b=boxes[i];p=pivots[i]if pivots else[(b[0]+b[2])/2,(b[1]+b[3])/2];im=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);z=Image.new('RGBA',(c,c));z.alpha_composite(im,(round(c/2-p[0]*k),round(c/2-p[1]*k)));out.append(z)
 return out,k
def source(n,file):
 p=S/(n+'_source.png')
 if not p.exists():shutil.copyfile(G/file,p)
 im=Image.open(p).convert('RGBA');M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'tool':'built-in image_gen','requestedCell':[192,192]};return im
def clean(t):
 a=np.array(t);ids,_=label(a[:,:,3]>=80);counts=np.bincount(ids.ravel());keep=counts>=max(18,counts[1:].max()*.007);keep[0]=False;a[:,:,3]=np.where(keep[ids],255,0);return Image.fromarray(a)
def preview(n,fs):
 c=fs[0].width;out=Image.new('RGB',(c*8,(c+16)*math.ceil(len(fs)/8)),(8,18,28));d=ImageDraw.Draw(out)
 for i,t in enumerate(fs):x=i%8*c;y=i//8*(c+16);out.paste(t,(x,y+16),t);d.text((x+3,y),str(i),fill='white')
 out.save(Q/(n+'-frames.jpg'),quality=92)
# Keep the four approved complete aircraft banks and native scale unchanged.
A=data('assets/enemy_flight_art_1031.js','R46_ART')
for n in['frigate','rammer','skimmer','repair']:
 B=A['models'][A['aliases']['5|s5'+n]];M['models'][n]={'bank':B,'spanWorld':{'frigate':96,'rammer':96,'skimmer':96,'repair':96}[n],'sourceSpan':B['span'],'sockets':B['sockets'],'reuse':True}
# New minelayer has actual rear-bay release and bank animations.
im=source('minelayer','exec-f0a9f394-ad51-496a-8bb8-de6201ab6cd2.png');fs=[];piv=[]
for row in[2,3]:
 for x in range(8):
  t=clean(im.crop((x*192,row*256,(x+1)*192,(row+1)*256)));a=np.array(t);ids,_=label(a[:,:,3]>0);counts=np.bincount(ids.ravel());counts[0]=0;a[:,:,3]=np.where(ids==counts.argmax(),a[:,:,3],0);t=Image.fromarray(a);mask=(a[:,:,0]>140)&(a[:,:,0]>a[:,:,1].astype(float)*1.8)&(a[:,:,0]>a[:,:,2].astype(float)*1.3)&(a[:,:,3]>0);yy,xx=np.nonzero(mask);piv.append([float(np.median(xx)),float(np.median(yy))]);fs.append(t)
fs,k=normalize(fs,100,pivots=piv);B=bank('minelayer',fs,16);M['models']['minelayer']={'bank':B,'spanWorld':108,'sourceSpan':100,'sockets':{'centre':[80,34],'port':[64,38],'starboard':[96,38],'exhaustPort':[66,34],'exhaustStarboard':[94,34]},'attack':[0,8],'roll':[8,8],'somer':[8,8],'idle':[0,1],'drift':[9,2]};preview('minelayer',fs)
# Claws animate around a shared red-eye anchor; no caption survives.
im=source('leech','exec-78ebe4d0-0125-4f7f-9335-736de2369ff7.png');fs=[];piv=[]
for y in range(4):
 for x in range(4):
  t=clean(im.crop((round(x*im.width/4),round(y*im.height/4),round((x+1)*im.width/4),round((y+1)*im.height/4))));a=np.array(t);mask=(a[:,:,0]>150)&(a[:,:,0]>a[:,:,1].astype(float)*1.8)&(a[:,:,0]>a[:,:,2].astype(float)*1.3)&(a[:,:,3]>0);yy,xx=np.nonzero(mask);piv.append([float(np.median(xx)),float(np.median(yy))]);fs.append(t)
fs,k=normalize(fs,114,pivots=piv);B=bank('leech',fs,16);M['models']['leech']={'bank':B,'spanWorld':110,'sourceSpan':114,'sockets':{'centre':[80,113],'exhaustPort':[62,43],'exhaustStarboard':[98,43]},'attack':[0,16],'roll':[0,16],'somer':[0,16],'drift':[0,1],'idle':[0,1]};preview('leech',fs)
# Whole native station/orb/satellite/portal silhouettes, no generated replacements.
for n,src,side in [('gravity','gravity_orb',108),('satellite','missile_satellite',108),('portalmine','portal_mine',102),('station','twin_station',154)]:
 p=S/(src+'_identity.png');fs,k=normalize([Image.open(p).convert('RGBA')],104);B=bank(n,fs,32);sockets={'centre':[80,123],'port':[60,111],'starboard':[100,111],'core':[80,80]}
 if n=='station':sockets={'centre':[80,99],'port':[49,108],'starboard':[111,108],'core':[80,80]}
 if n=='satellite':sockets.update(port=[56,104],starboard=[104,104])
 M['models'][n]={'bank':B,'spanWorld':side,'sourceSpan':104,'sockets':sockets,'idle':[0,1],'attack':[0,1],'roll':[0,1],'somer':[0,1],'drift':[0,1]};M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'owner':'stage5_runtime_atlas, extracted without modification'};preview(n,fs)
# Luminance/alpha-preserving violet palette of real Stage2 magma ordnance.
V=data('assets/stage2_amplify_art_1031.js','V31_ART')
for n in['orb','mine','laser','muzzle','thruster','thunder_missile']:
 B=V['banks'][n];im=Image.open(R/B['path']).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);mask=(rgb.max(2)-rgb.min(2)>25)&(a[:,:,3]>0);ramp=np.stack([lum*1.12,lum*.48,lum*1.65],2);ramp/=np.dot([1.12,.48,1.65],[.2126,.7152,.0722]);a[:,:,:3][mask]=np.minimum(255,ramp)[mask].astype('uint8');p=O/(n+'.webp');Image.fromarray(a).save(p,format='WEBP',lossless=True,method=4);M['banks'][n]={**B,'key':'s511_'+n,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'source':B['path'],'palette':'violet, original alpha/luminance/white core preserved; actual animated own-pixel energy'}
# 1015 companion: actual emissive orb pixels and1/2px hard spill, six native
# PXG_STEPS at runtime. Never a circular decal or independently sized halo.
from scipy.ndimage import maximum_filter
B=M['banks']['orb'];im=Image.open(R/B['path']).convert('RGBA');glow=Image.new('RGBA',im.size)
for f in range(B['frames']):
 a=np.array(im.crop((0,f*128,128,(f+1)*128)));rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);em=(a[:,:,3]>80)&(lum>90);level=np.where(em,210,np.where(maximum_filter(em,3),100,np.where(maximum_filter(em,5),38,0)));g=np.zeros_like(a);g[:,:,:3]=[181,90,255];g[:,:,3]=level;glow.alpha_composite(Image.fromarray(g),(0,f*128))
p=O/'orb_glow.webp';glow.save(p,format='WEBP',lossless=True,method=4);M['banks']['orb_glow']={**B,'key':'s511_orb_glow','path':p.relative_to(R).as_posix(),'sha256':sha(p),'source':B['path'],'recipe':'1015 source-emissive pixels +1/2px hard spill, native six-step PXG_STEPS'}
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(S/'generation.json').write_text(json.dumps(M['sources'],indent=2),encoding='utf-8');(R/'assets/stage5_amplify_art_1101.js').write_text('"use strict";\nconst S511_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Registered',len(M['models']),'models,',len(M['banks']),'fixed source/palette banks')
