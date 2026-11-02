"""Stage7 generated modular refit, source-preserving directional/1015 exports.
All runtime sprites are fixed even cells; no live sprite rotation or stretching.
"""
from pathlib import Path
import json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import maximum_filter,label
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/stage7_amplify_1101';O=R/'assets/game/levels/stage_07/enemies/amplify_1101';Q=R/'_shots/stage7_amplify_1101'
for p in[S,O,Q]:p.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
EXTRA={'face':'exec-722884b5-89f9-410f-b799-4737efe09c1d.png','fly':'exec-ad64f729-4c75-440a-99c0-01436056c96c.png','relay_roll':'exec-5aa6baec-4726-49fe-b89d-5e664b1ffc62.png','slime_roll':'exec-71d239d2-06bc-4902-9691-ec44a4ae93bc.png'}
for n,f in EXTRA.items():
 if not(S/(n+'_source.png')).exists():shutil.copyfile(G/f,S/(n+'_source.png'))
M={'owner':'_BUILD_SOURCE/build_stage7_amplify_1101.py','models':{},'banks':{},'sources':{},'retired':{'ll18raptor':'BOF expansion only; original nsb_rap art retained, no campaign/adaptive/direct spawns'}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(p,n):return json.JSONDecoder().raw_decode((R/p).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
def bank(n,fs,dirs=32):
 c=fs[0].width;assert c%2==0 and all(f.size==(c,c)for f in fs)
 # Direction rows cap image width below8192, avoiding GPU texture limits.
 cols=min(16,dirs);rows=math.ceil(dirs/cols);im=Image.new('RGBA',(c*cols,c*len(fs)*rows))
 for f,t in enumerate(fs):
  for d in range(dirs):im.alpha_composite(t.rotate(-d*360/dirs,Image.Resampling.NEAREST),(d%cols*c,(f*rows+d//cols)*c))
 p=O/(n+'.webp');im.save(p,format='WEBP',lossless=True,method=4)
 B={'key':'s711_'+n,'path':p.relative_to(R).as_posix(),'cell':c,'dirs':dirs,'frames':len(fs),'cols':cols,'dirRows':rows,'sha256':sha(p)};M['banks'][n]=B;return B
def clean(im):
 a=np.array(im.convert('RGBA'));ids,_=label(a[:,:,3]>60);counts=np.bincount(ids.ravel());keep=counts>=max(5,counts[1:].max()*.0003);keep[0]=False;a[:,:,3]=np.where(keep[ids],255,0);return Image.fromarray(a)
def raw(n):
 p=S/(n+'_source.png');M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'tool':'built-in image_gen','promptFile':'_BUILD_SOURCE/stage7_amplify_1101/prompts.md'};return clean(Image.open(p))
def plate(n):
 im=raw(n);return im.resize((256,256),Image.Resampling.NEAREST)
def select(im,poly):
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255);a=np.array(im);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));return Image.fromarray(a)
def cut(im,poly):
 part=select(im,poly);a=np.array(im);a[:,:,3][np.array(part)[:,:,3]>0]=0;return Image.fromarray(a),part
def centre(im,p,cell=384):
 out=Image.new('RGBA',(cell,cell));out.alpha_composite(im,(round(cell/2-p[0]),round(cell/2-p[1])));return out
def glow(im,shield=False):
 a=np.array(im);rgb=a[:,:,:3].astype(float);em=(a[:,:,3]>0)&(rgb[:,:,1]>rgb[:,:,0]*1.28)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>75)
 if shield:
  hull=a[:,:,3]>0;edge=maximum_filter(hull,7)&~hull;near=maximum_filter(hull,3)&~hull;v=np.where(em,170,np.where(near,150,np.where(edge,42,0)))
 else:v=np.where(em,180,np.where(maximum_filter(em,3),65,0))
 z=np.zeros_like(a);z[:,:,:3]=[132,255,26];z[:,:,3]=v;return Image.fromarray(z)
def preview(n,fs):
 c=fs[0].width;k=min(1,192/c);cc=round(c*k);out=Image.new('RGB',(cc*min(8,len(fs)),(cc+18)*math.ceil(len(fs)/8)),(9,19,24));d=ImageDraw.Draw(out)
 for i,t in enumerate(fs):x=i%8*cc;y=i//8*(cc+18);z=t.resize((cc,cc),Image.Resampling.NEAREST);out.paste(z,(x,y+18),z);d.text((x+4,y),str(i),fill='white')
 out.save(Q/(n+'-frames.jpg'),quality=93)
def module(n,im,p,mount,muzzle,rotor=None):
 # Modules keep native source scale; place the actual swivel at cell centre.
 fs=[]
 for f in range(8 if rotor else 1):
  t=im.copy()
  if rotor:
   x,y,r=rotor;z=im.crop((x-r,y-r,x+r,y+r));mask=Image.new('L',z.size);ImageDraw.Draw(mask).ellipse((0,0,2*r-1,2*r-1),fill=255);a=np.array(z);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));z=Image.fromarray(a).rotate(-f*45,Image.Resampling.NEAREST);t.alpha_composite(z,(x-r,y-r))
  fs.append(centre(t,p,288))
 B=bank(n,fs);SB=bank(n+'_shield',[glow(f,True)for f in fs]);return {'bank':B,'shield':SB,'mount':mount,'pivot':p,'muzzle':[muzzle[0]-p[0],muzzle[1]-p[1]],'rotary':bool(rotor)}
DEFS={
 'relay':(146,[[(38,99),(87,99),(87,240),(38,240)],[(170,99),(219,99),(219,240),(170,240)]],[[62,114],[194,114]],[[62,229],[194,229]],[[62,221,13],[194,221,13]],[[99,21],[155,21]]),
 'slime':(132,[[(48,112),(83,112),(83,198),(48,198)],[(173,112),(208,112),(208,198),(173,198)]],[[66,117],[190,117]],[[66,190],[190,190]],[[66,188,9],[190,188,9]],[[109,23],[147,23]]),
 'missilejet':(144,[[(23,113),(68,113),(68,211),(23,211)],[(188,113),(233,113),(233,211),(188,211)]],[[45,123],[211,123]],[[44,202],[211,202]],[None,None],[[101,32],[155,32]]),
 'crescent':(128,[[(13,130),(42,130),(42,205),(13,205)],[(213,130),(242,130),(242,205),(213,205)]],[[27,140],[228,140]],[[27,198],[228,198]],[None,None],[[111,56],[128,51],[145,56]]),
 'barge':(196,[[(35,56),(82,56),(82,113),(35,113)],[(174,56),(221,56),(221,113),(174,113)],[(32,125),(81,125),(81,184),(32,184)],[(175,125),(224,125),(224,184),(175,184)]],[[58,75],[198,75],[56,147],[200,147]],[[58,107],[198,107],[56,177],[200,177]],[None]*4,[[88,16],[166,16]])}
for n,(span,polys,piv,bores,rotors,tails)in DEFS.items():
 im=plate(n);body=im.copy();mods=[]
 for i,(poly,p,b,r)in enumerate(zip(polys,piv,bores,rotors)):
  body,t=cut(body,poly);mods.append(module(n+'_gun'+str(i),t,p,p,b,r))
 fs=[centre(body,[128,128])];B=bank(n+'_hull',fs);bank(n+'_glow',[glow(f)for f in fs]);bank(n+'_shield',[glow(f,True)for f in fs])
 M['models'][n]={'bank':B,'spanWorld':span,'sourceSpan':256,'pivot':[128,128],'modules':mods,'tails':tails,'source':M['sources'][n],'fullBank':bank(n+'_full',[centre(im,[128,128])])};preview(n,[centre(im,[128,128]),*fs])
 if n in['relay','slime']:
  z=raw(n+'_roll');cells=[clean(z.crop((round(i%4*z.width/4),round(i//4*z.height/2),round((i%4+1)*z.width/4),round((i//4+1)*z.height/2))))for i in range(8)]
  # Shared proportional scale, individual centre-of-fuselage registered pivots.
  scale=232/max(max(t.getbbox()[2]-t.getbbox()[0],t.getbbox()[3]-t.getbbox()[1])for t in cells);rf=[]
  for t in cells:
   b=t.getbbox();p=[(b[0]+b[2])/2,(b[1]+b[3])/2];v=t.resize((round(t.width*scale),round(t.height*scale)),Image.Resampling.NEAREST);rf.append(centre(v,[p[0]*scale,p[1]*scale]))
  rf[0]=rf[-1]=centre(im,[128,128]);M['models'][n]['roll']=bank(n+'_roll',rf,16)
  # Measured terminal gun pixels on the changing perspective, not idle sockets
  # pasted over an underside plate. Normalized expected pairs guide alpha snap.
  pairs=[[(.24,.91),(.76,.91)],[(.39,.91),(.82,.96)],[(.44,.96),(.63,.95)],[(.25,.92),(.77,.92)],[(.16,.95),(.65,.84)],[(.39,.96),(.60,.95)],[(.20,.95),(.64,.87)],[(.24,.91),(.76,.91)]]
  bores=[]
  for fi,(t,expected)in enumerate(zip(rf,pairs)):
   a=np.array(t);ys,xs=np.nonzero(a[:,:,3]>100);b=t.getbbox();points=[]
   for xx,yy in expected:
    tx=b[0]+xx*(b[2]-b[0]);ty=b[1]+yy*(b[3]-b[1]);idx=np.argmin((xs-tx)**2+(ys-ty)**2);points.append([int(xs[idx])-192+128,int(ys[idx])-192+128])
   if fi in[0,7]:points=bores[0] if bores else [list(p)for p in DEFS[n][3]]
   bores.append(points)
  M['models'][n]['rollBores']=bores;preview(n+'_roll',rf)
# Brood: disjoint main body, face and two shoulder-pivoted authored claws.
im=plate('brood');body=im.copy();mods=[]
for i,poly in enumerate([[(0,111),(55,105),(90,140),(77,176),(110,251),(0,251)],[(201,105),(256,111),(256,251),(146,251),(179,176),(166,140)]]):
 body,t=cut(body,poly);p=[26 if i==0 else 230,137];mods.append(module('brood_claw'+str(i),t,p,p,[91 if i==0 else 165,238]))
body,oldface=cut(body,[(87,139),(169,139),(174,213),(82,213)])
z=raw('face');cells=[clean(z.crop((round(i%4*z.width/4),round(i//4*z.height/2),round((i%4+1)*z.width/4),round((i//4+1)*z.height/2))))for i in range(8)]
bounds=[t.getbbox()for t in cells];scale=82/max(b[2]-b[0]for b in bounds);faces=[]
for t,b in zip(cells,bounds):
 v=t.resize((round(t.width*scale),round(t.height*scale)),Image.Resampling.NEAREST);faces.append(centre(v,[((b[0]+b[2])/2)*scale,(b[1]+(b[3]-b[1])*.42)*scale],192))
M['models']['brood']={'bank':bank('brood_hull',[centre(body,[128,128])]),'fullBank':bank('brood_full',[centre(im,[128,128])]),'spanWorld':212,'sourceSpan':256,'modules':mods,'face':{'bank':bank('brood_face',faces),'mount':[128,173]},'mouth':[128,201],'tails':[]}
bank('brood_glow',[glow(centre(body,[128,128]))]);bank('brood_shield',[glow(centre(body,[128,128]),True)]);preview('brood_face',faces);preview('brood',[centre(im,[128,128]),centre(body,[128,128])])
# Six articulated legs and three central pipe sections. Common source pixels.
im=plate('crawler');body=im.copy();mods=[]
for i,(x0,x1,ys)in enumerate([(0,99,[18,78,138]),(157,256,[18,78,138])]):
 for j,y0 in enumerate(ys):
  poly=[(x0,y0),(x1,y0),(x1,y0+69),(x0,y0+69)];body,t=cut(body,poly);p=[91 if i==0 else 165,y0+44];mods.append(module('crawler_leg'+str(i*3+j),t,p,p,[p[0],p[1]]))
segments=[]
for j,(y0,y1,p)in enumerate([(0,81,[128,50]),(81,145,[128,114]),(145,256,[128,178])]):
 t=select(body,[(0,y0),(256,y0),(256,y1),(0,y1)]);segments.append(module('crawler_seg'+str(j),t,p,p,[128,234]))
M['models']['crawler']={'bank':bank('crawler_full',[centre(im,[128,128])]),'spanWorld':106,'sourceSpan':256,'modules':mods,'segments':segments,'mouths':[[115,235],[142,235]],'tails':[]};preview('crawler',[centre(im,[128,128])])
# Existing tank and liked ground turret art retained, physically measured sockets.
im=Image.open(S/'s7atk_toxic_mini_tank_0.png').convert('RGBA');M['models']['tank']={'bank':bank('tank',[centre(im,[128,128])]),'spanWorld':104,'sourceSpan':256,'guns':[[96,197],[162,204]],'modules':[],'tails':[]};preview('tank',[centre(im,[128,128])])
for n in['mg','laser','sonic']:
 im=Image.open(S/('overhaul_ground_head_'+n+'.png')).convert('RGBA');bank('head_'+n,[centre(im,[128,128])]);bank('head_'+n+'_glow',[glow(centre(im,[128,128]))])
im=Image.open(S/'overhaul_ground_base_7.png').convert('RGBA');bank('ground_base',[centre(im,[128,128])])
# Existing approved muzzle/thruster/laser/slug art, toxic palette preserving alpha,
# luminance hierarchy and white cores. Source-derived 1015 energy companion.
V=data('assets/stage2_amplify_art_1031.js','V31_ART')
for n,src in [('slug','slug'),('muzzle','muzzle'),('thruster','thruster'),('laser','laser'),('missile','thunder_missile')]:
 if src not in V['banks']:src='fire_bullet'if n=='slug'else src
 B=V['banks'][src];im=Image.open(R/B['path']).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);mask=(rgb.max(2)-rgb.min(2)>20)&(a[:,:,3]>0);ramp=np.stack([lum*.65,lum*1.3,lum*.24],2);a[:,:,:3][mask]=np.minimum(255,ramp)[mask].astype('uint8');p=O/(n+'.webp');Image.fromarray(a).save(p,format='WEBP',lossless=True,method=4);M['banks'][n]={**B,'key':'s711_'+n,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'source':B['path']}
 # Palette sources already have source-preserving fixed direction cells.
 if n in['laser','slug']:
  p=O/(n+'_glow.webp');glow(Image.fromarray(a)).save(p,format='WEBP',lossless=True,method=4);M['banks'][n+'_glow']={**M['banks'][n],'key':'s711_'+n+'_glow','path':p.relative_to(R).as_posix(),'sha256':sha(p)}
im=Image.open(S/'rzb_sonic_wave.png').convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);mask=a[:,:,3]>0;a[:,:,:3][mask]=np.minimum(255,np.stack([lum*.65,lum*1.32,lum*.25],2))[mask].astype('uint8');bank('sonic',[centre(Image.fromarray(a),[128,128])])
z=raw('fly');cells=[clean(z.crop((round(i%4*z.width/4),round(i//4*z.height/2),round((i%4+1)*z.width/4),round((i//4+1)*z.height/2))))for i in range(8)];scale=108/max(max(t.getbbox()[2]-t.getbbox()[0],t.getbbox()[3]-t.getbbox()[1])for t in cells);fs=[]
for t in cells:
 a=np.array(t);green=(a[:,:,1]>a[:,:,0]*1.3)&(a[:,:,1]>a[:,:,2]*1.2)&(a[:,:,3]>0);yy,xx=np.nonzero(green);p=[np.median(xx),np.median(yy)];v=t.resize((round(t.width*scale),round(t.height*scale)),Image.Resampling.NEAREST);fs.append(centre(v,[p[0]*scale,p[1]*scale],192))
bank('fly',fs,16);preview('fly',fs)
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(S/'generation.json').write_text(json.dumps(M['sources'],indent=2)+'\n',encoding='utf-8');(R/'assets/stage7_amplify_art_1101.js').write_text('"use strict";\nconst S711_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Registered',len(M['models']),'models,',len(M['banks']),'fixed even source/module/palette banks')
