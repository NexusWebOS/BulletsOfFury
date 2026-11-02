"""Stage9 unique authored modular hulls, registered joints and ordnance.
Source-preserving even-cell exports; all rotations are offline direction cells.
"""
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,maximum_filter
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/stage9_amplify_1101';O=R/'assets/game/levels/stage_09/enemies/amplify_1101';Q=R/'_shots/stage9_amplify_1101'
for p in[S,O,Q]:p.mkdir(parents=True,exist_ok=True)
M={'owner':'_BUILD_SOURCE/build_stage9_amplify_1101.py','models':{},'banks':{},'sources':{}}
PALETTES=json.loads((S/'palettes.json').read_text(encoding='utf-8'))
M['palettes']=PALETTES

def palette(t,n):
 name=n.split('_')[0];family=PALETTES['models'].get(name)
 if not family:return t
 recipe=PALETTES['families'][family];a=np.array(t);rgb=a[:,:,:3].astype(float);opaque=a[:,:,3]>0
 if n.endswith(('_glow','_shield')):
  a[:,:,:3]=recipe['glow'];return Image.fromarray(a)
 lum=rgb@np.array([.2126,.7152,.0722]);chroma=rgb.max(2)-rgb.min(2)
 energy=(chroma>50)&(rgb[:,:,1]>rgb[:,:,0]*1.3)&(rgb[:,:,1]>=rgb[:,:,2]*.65)&(rgb.max(2)>90)&opaque
 armor=opaque&~energy&(lum>24)&(lum<238)
 ramp=np.array(recipe['armor']);mapped=np.stack([np.interp(lum,PALETTES['armorLuminanceKnots'],ramp[:,i])for i in range(3)],axis=2)
 # Preserve authored luminosity in bright channels by desaturating toward white.
 hue=np.array(recipe['energy'],dtype=float);hy=hue@np.array([.2126,.7152,.0722]);out=np.where((lum<=hy)[:,:,None],hue*lum[:,:,None]/hy,hue+(255-hue)*(lum-hy)[:,:,None]/(255-hy))
 a[:,:,:3][armor]=np.clip(mapped[armor],0,255).astype('uint8');a[:,:,:3][energy]=np.clip(out[energy],0,255).astype('uint8')
 return Image.fromarray(a)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(p,n):return json.JSONDecoder().raw_decode((R/p).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
def clean(t):
 a=np.array(t.convert('RGBA'));ids,_=label(a[:,:,3]>65);counts=np.bincount(ids.ravel());keep=counts>=max(4,counts[1:].max()*.00015);keep[0]=False;a[:,:,3]=np.where(keep[ids],255,0);return Image.fromarray(a)
def source(n):
 p=S/(n+'_source.png');M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'tool':'built-in image_gen','promptFile':'_BUILD_SOURCE/stage9_amplify_1101/prompts.md'};return clean(Image.open(p))
def pad(t,p=None,c=None):
 p=p or[t.width/2,t.height/2]
 if c is None:
  yy,xx=np.nonzero(np.array(t)[:,:,3]>0);radius=np.sqrt((xx-p[0])**2+(yy-p[1])**2).max()if len(xx)else 24;c=max(64,math.ceil((radius*2+16)/2)*2)
 z=Image.new('RGBA',(c,c));z.alpha_composite(t,(round(c/2-p[0]),round(c/2-p[1])));return z
def plate(n):return source(n).resize((256,256),Image.Resampling.NEAREST)
def bank(n,fs,dirs=32):
 raw=fs;fs=[palette(t,n)for t in fs]
 assert all(np.array_equal(np.array(a)[:,:,3],np.array(b)[:,:,3])for a,b in zip(raw,fs)),n+' palette changed source alpha'
 if n.split('_')[0]in PALETTES['models']:M.setdefault('paletteProof',{})[n]={'alphaPreserved':True,'frames':len(fs),'palette':PALETTES['models'][n.split('_')[0]]}
 c=fs[0].width;assert c%2==0 and all(t.size==(c,c)for t in fs);cols=min(16,dirs);rows=math.ceil(dirs/cols);z=Image.new('RGBA',(c*cols,c*len(fs)*rows))
 for f,t in enumerate(fs):
  for d in range(dirs):z.alpha_composite(t.rotate(-d*360/dirs,Image.Resampling.NEAREST),(d%cols*c,(f*rows+d//cols)*c))
 p=O/(n+'.webp');z.save(p,format='WEBP',lossless=True,method=4);B={'key':'s911_'+n,'path':p.relative_to(R).as_posix(),'cell':c,'dirs':dirs,'frames':len(fs),'cols':cols,'dirRows':rows,'sha256':sha(p)};M['banks'][n]=B;return B
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
 fs=[palette(t,n)for t in fs]
 out=Image.new('RGB',(192*min(8,len(fs)),210*math.ceil(len(fs)/8)),(8,13,22));d=ImageDraw.Draw(out)
 for i,t in enumerate(fs):
  z=t.copy();z.thumbnail((192,192),Image.Resampling.NEAREST);x=i%8*192;y=i//8*210;out.paste(z,(x+(192-z.width)//2,y+18),z);d.text((x+4,y),str(i),fill='white')
 out.save(Q/(n+'-frames.jpg'),quality=93)
def snap(t,p):
 a=np.array(t);yy,xx=np.nonzero(a[:,:,3]>160);j=np.argmin((xx-p[0])**2+(yy-p[1])**2);return[int(xx[j]),int(yy[j])]
def part(n,t,p,mount,tip,role='gun',color=(178,78,255),frames=None):
 frames=frames or[pad(t,p)];B=bank(n,frames);G=bank(n+'_glow',[emissive(f,color)for f in frames]);H=bank(n+'_shield',[emissive(f,color,True)for f in frames]);tip=snap(t,tip)
 return {'bank':B,'glow':G,'shield':H,'mount':mount,'muzzle':[tip[0]-p[0],tip[1]-p[1]],'role':role,'baseAngle':math.atan2(tip[1]-p[1],tip[0]-p[0])}
def rect(x0,y0,x1,y1):return[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]

def model(n,im,span,defs=(),tails=(),core=(128,128),color=(23,235,239),guns=()):
 body=im.copy();mods=[]
 for i,(poly,p,tip)in enumerate(defs):body,t=cut(body,poly);mods.append(part(n+'_part'+str(i),t,p,p,tip,color=color))
 fs=[pad(body)];z={'bank':bank(n+'_body',fs),'glow':bank(n+'_glow',[emissive(f,color)for f in fs]),'shield':bank(n+'_shield',[emissive(f,color,True)for f in fs]),'span':span,'modules':mods,'tails':tails,'core':core,'guns':guns};M['models'][n]=z;preview(n,[pad(im),*fs]);return z

def twin(x,y,tipy,w=18):return[(rect(x-w,y-14,x+w,tipy+12),[x,y],[x,tipy]),(rect(256-x-w,y-14,256-x+w,tipy+12),[256-x,y],[256-x,tipy])]

# Retained canonical single plates; no idle/attack drift replaces the hull.
for n,ref,span,guns,tails in [('kami','s9interceptor',136,[[66,200],[190,200]],[[104,62],[152,62]]),('comet','s9comet',138,[[66,200],[190,200]],[[104,62],[152,62]]),('beacon','s9beacon',164,[],[]),('beamship','s9gunship',190,[[72,198],[186,198]],[[104,62],[152,62]])]:
 raw=Image.open(S/(ref+'_reference.png')).convert('RGBA');off=(raw.width-128)//2;im=raw.crop((off,off,off+128,off+128)).resize((256,256),Image.Resampling.NEAREST)
 if n=='comet':
  a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);sel=(rgb.max(2)-rgb.min(2)>24)&(a[:,:,3]>0);a[:,:,:3][sel]=np.minimum(255,lum[:,:,None]*[1.63,.55,1.35])[sel].astype('uint8');im=Image.fromarray(a)
 z=model(n,im,span,tails=tails,guns=guns,color=(255,70,176)if n=='comet'else(23,235,239));M.setdefault('references',{})[n]={'path':(S/(ref+'_reference.png')).relative_to(R).as_posix(),'sha256':sha(S/(ref+'_reference.png'))}
 if n=='beamship':z['guns']=[[71,198],[183,198]]
 if n=='beacon':
  a=np.array(im);yy,xx=np.indices(a.shape[:2]);a[:,:,3]=np.where((xx-128)**2+(yy-128)**2<27**2,a[:,:,3],0);z['coreBank']=bank('beacon_core',[pad(Image.fromarray(a))])

defs={
'spinner':(172,[( [(104,0),(152,0),(152,79),(128,84),(104,79)],[128,75],[128,14]),(rect(171,48,244,115),[177,98],[233,65]),(rect(170,141,244,208),[177,154],[233,192]),(rect(104,178,152,256),[128,180],[128,240]),(rect(12,141,86,208),[78,154],[23,192]),(rect(12,48,86,115),[78,98],[23,65])],[]),
'jumper':(148,twin(94,143,210,17),[[112,47],[143,47]]),
'skimmer':(158,twin(85,150,199,14),[[114,32],[143,32]]),
'ringlaser':(174,twin(99,128,207,17),[[110,44],[146,44]]),
'gate':(184,[(rect(45,34,103,117),[86,71],[73,107]),(rect(153,34,211,117),[166,71],[179,107]),(rect(45,136,103,213),[86,166],[74,201]),(rect(153,136,211,213),[166,166],[178,201])],[]),
'gleech':(186,[(rect(41,133,106,234),[91,144],[73,222]),(rect(150,133,215,234),[164,144],[181,222])],[]),
'prismbeam':(202,twin(72,161,215,26),[]),
'echo':(146,twin(80,108,153,12)+twin(117,170,220,11),[[112,32],[143,32]]),
'minelayer':(176,[],[[38,155],[218,155]]),
'manta':(180,twin(86,131,195,18),[[128,27]]),
'tidal':(172,twin(75,145,215,17),[[104,32],[119,32],[137,32],[152,32]]),
'singularity':(180,[],[]),
'prismorb':(174,[],[])}
for n,(span,parts,tails)in defs.items():
 im=plate(n);z=model(n,im,span,parts,tails,color=(255,72,186)if n=='manta'else(23,235,239));
 if n in['singularity','prismorb']:z['guns']=[[128,155]]
 if n=='minelayer':z['bay']=[128,150]

# The approved Stage6 iris/extension/charge/recoil mechanism on a new water hull.
C=data('assets/cloud_carrier_art_1101.js','CC111_ART');B=C['banks']['cannon'];im=Image.open(R/B['path']).convert('RGBA');fs=[im.crop((0,f*192,192,f*192+192)).resize((48,48),Image.Resampling.NEAREST)for f in range(12)];z=model('harrier',plate('harrier'),320,tails=[[86,34],[168,34]]);mods=[]
for i,p in enumerate([[89,96],[165,96],[89,131],[165,131]]):
 f=fs[8];m=part('harrier_pod'+str(i),f,[24,24],p,[24,42],frames=fs);m['bores']=[[(b[0]-96)/4,(b[1]-96)/4]for b in C['cannon']['bores']];m['baseAngle']=math.pi/2;mods.append(m)
z['modules']=mods

def strip(n,span,c=384,anchor='center',anchors=None):
 im=source(n);tiles=[clean(im.crop((round(i%4*im.width/4),round(i//4*im.height/2),round((i%4+1)*im.width/4),round((i//4+1)*im.height/2))))for i in range(8)]
 if n in['poses','morph']or n.startswith('flight_'):
  for i,f in enumerate(tiles):
   a=np.array(f);ids,_=label(a[:,:,3]>0);counts=np.bincount(ids.ravel());keep=counts>=max(24,counts[1:].max()*.004);keep[0]=False;a[:,:,3]=np.where(keep[ids],a[:,:,3],0);tiles[i]=Image.fromarray(a)
 boxes=[f.getbbox()for f in tiles];k=span/max(max(b[2]-b[0],b[3]-b[1])for b in boxes);out=[]
 for i,(f,b)in enumerate(zip(tiles,boxes)):
  v=f.resize((round(f.width*k),round(f.height*k)),Image.Resampling.NEAREST);p=[anchors[i][0]*f.width*k,anchors[i][1]*f.height*k]if anchors else[(b[0]+b[2])/2*k,(b[1]+b[3])/2*k]if anchor=='bbox'else[f.width/2*k,f.height/2*k]if anchor=='center'else[(b[0]+b[2])/2*k,(b[3]if anchor=='bottom'else b[1])*k];out.append(pad(v,p,c))
 preview(n,out);return out

# Actual authored water-human action poses and orb-to-body transformation.
z=model('current',plate('human'),190);fs=strip('poses',236,384,anchors=[(.5,.34),(.5,.34),(.5,.34),(.58,.38),(.5,.52),(.5,.53),(.5,.53),(.5,.34)]);z['bank']=bank('current_poses',fs,1);z['glow']=bank('current_glow',[emissive(f,(28,225,255))for f in fs],1);z['shield']=bank('current_shield',[emissive(f,(28,225,255),True)for f in fs],1)
morph=strip('morph',236,384,anchors=[(.5,.61),(.5,.46),(.5,.40),(.5,.40),(.5,.39),(.5,.39),(.5,.39),(.5,.39)]);morph[-1]=fs[0].copy();z['orb']=bank('current_orb',[morph[0]],1)
# Baked source-pixel liquid dissolve between authored frames; no HTML alpha.
yy,xx=np.indices((384,384));order=(xx%4)*4+yy%4;flow=[]
for a,b in zip(morph,morph[1:]):
 for step in range(4):flow.append(Image.fromarray(np.where((order<step*4)[:,:,None],np.array(b),np.array(a)).astype('uint8')))
flow.append(morph[-1]);z['morph']=bank('current_morph',flow,1);preview('current_morph',flow)
# Hand locations are measured on the normalized pose cells, in256-unit coordinates.
z['poseGuns']=[[[66,185],[210,185]],[[43,153],[208,153]],[[65,70],[210,174]],[[54,117],[186,171]],[[45,211],[210,211]],[[52,103],[200,103]],[[52,95],[201,95]],[[66,185],[210,185]]]
for i,ports in enumerate(z['poseGuns']):
 z['poseGuns'][i]=[[v-64 for v in snap(fs[i],[p[0]+64,p[1]+64])]for p in ports]
z['poseBases']=[math.pi/2]*8;boxes=[f.getbbox()for f in fs];z['extent']=[2*max(max(abs(b[0]-192),abs(b[2]-192))for b in boxes),2*max(max(abs(b[1]-192),abs(b[3]-192))for b in boxes)]

# Actual authored overhead views: each cell is a different supplied direction,
# never a planar rotation of the old frontal body. Shared chest pivot and scale.
def authored_directions(n,frames):
 c=frames[0].width;im=Image.new('RGBA',(c*4,c*2))
 for i,f in enumerate(frames):im.alpha_composite(f,(i%4*c,i//4*c))
 p=O/(n+'.webp');im.save(p,format='WEBP',lossless=True,method=4);B={'key':'s911_'+n,'path':p.relative_to(R).as_posix(),'cell':c,'frames':1,'dirs':8,'cols':4,'dirRows':2,'sha256':sha(p),'authoredDirections':True};M['banks'][n]=B;return B

overhead=strip('flight_topdown',236,384)
# Bridge approved source poses with baked liquid pixel transfer. The new
# overhead directions are genuinely authored views; this bridge does not
# synthesize a top view by rotating or stretching the frontal sprite.
def liquid_transfer(a,b,fraction):return Image.fromarray(np.where((order<fraction*16)[:,:,None],np.array(b),np.array(a)).astype('uint8'))
launch=[fs[4].copy(),liquid_transfer(fs[4],fs[5],.5),fs[5].copy(),liquid_transfer(fs[5],fs[6],.5),fs[6].copy(),liquid_transfer(fs[6],overhead[0],.33),liquid_transfer(fs[6],overhead[0],.67),overhead[0].copy()];recover=[f.copy()for f in reversed(launch)];recover[-1]=fs[0].copy();z['flightTransitionSource']='Approved crouch4, flight5, palms6 and authored overheadSouth; baked liquid pixel transfer'
z['flight']=authored_directions('current_flight',overhead);z['flightGlow']=authored_directions('current_flight_glow',[emissive(f,(28,225,255))for f in overhead]);z['flightLaunch']=bank('current_flight_launch',launch,1);z['flightLaunchGlow']=bank('current_flight_launch_glow',[emissive(f,(28,225,255))for f in launch],1);z['flightReturn']=bank('current_flight_return',recover,1);z['flightReturnGlow']=bank('current_flight_return_glow',[emissive(f,(28,225,255))for f in recover],1)
# Registered palm centres in each supplied direction cell, not rotated guesses.
z['flightPalmsRaw']=[[[.36,.84],[.64,.84]],[[.12,.73],[.32,.88]],[[.09,.39],[.09,.69]],[[.32,.12],[.12,.32]],[[.36,.13],[.64,.13]],[[.72,.12],[.88,.32]],[[.91,.39],[.91,.69]],[[.87,.72],[.68,.88]]]
im=Image.open(S/'flight_topdown_source.png');tiles=[clean(im.crop((round(i%4*im.width/4),round(i//4*im.height/2),round((i%4+1)*im.width/4),round((i//4+1)*im.height/2))))for i in range(8)];k=236/max(max(b[2]-b[0],b[3]-b[1])for b in[f.getbbox()for f in tiles]);z['flightPalms']=[]
for i,ports in enumerate(z['flightPalmsRaw']):
 points=[[192+(p[0]-.5)*tiles[i].width*k,192+(p[1]-.5)*tiles[i].height*k]for p in ports];z['flightPalms'].append([[v-64 for v in snap(overhead[i],p)]for p in points])
# Tilt palms are measured after normalization, with locked endpoint sockets.
z['launchPalms']=[z['poseGuns'][4],[[63,190],[200,190]],[[66,184],[194,184]],[[70,185],[190,185]],[[74,193],[186,193]],[[77,201],[180,201]],[[78,209],[179,209]],z['flightPalms'][0]]
for i in range(1,7):z['launchPalms'][i]=[[v-64 for v in snap(launch[i],[p[0]+64,p[1]+64])]for p in z['launchPalms'][i]]
z['returnPalms']=list(reversed(z['launchPalms']));z['returnPalms'][-1]=z['poseGuns'][0];boxes=[f.getbbox()for f in overhead+launch+recover];z['extent']=[max(z['extent'][axis],2*max(max(abs(b[axis]-192),abs(b[axis+2]-192))for b in boxes))for axis in[0,1]]
preview('flight_topdown',overhead);preview('flight_launch',launch);preview('flight_return',recover)
M['banks']['shield_serpent']=bank('shield_serpent',strip('spiral',238,288),1)
M['banks']['tidal_wave']=bank('tidal_wave',strip('wave',234,256),16)
M['banks']['water_splash']=bank('water_splash',strip('splash',220,256),1)
M['banks']['water_mine']=bank('water_mine',strip('mine',106,128),16)
M['banks']['water_grenade']=bank('water_grenade',[pad(plate('waterorb').resize((96,96),Image.Resampling.NEAREST),c=128)],16)

# Native approved projectile/exhaust art re-exported with a water/teal palette.
A=data('assets/stage8_amplify_art_1101.js','S811_ART')
for n,src in [('laser','blue_laser'),('orb','blue_orb'),('thruster','blue_thruster'),('muzzle','blue_muzzle'),('slug','blue_slug')]:
 B=A['banks'][src];im=Image.open(R/B['path']).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);sel=(rgb.max(2)-rgb.min(2)>28)&(a[:,:,3]>0);a[:,:,:3][sel]=np.minimum(255,lum[:,:,None]*[.28,1.18,1.26])[sel].astype('uint8');p=O/('water_'+n+'.webp');Image.fromarray(a).save(p,format='WEBP',lossless=True,method=4);M['banks']['water_'+n]={**B,'key':'s911_water_'+n,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'source':B['path']}
for n in['laser','slug','muzzle','thruster']:
 B=M['banks']['water_'+n];im=Image.open(R/B['path']).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);sel=(rgb.max(2)-rgb.min(2)>24)&(a[:,:,3]>0);a[:,:,:3][sel]=np.minimum(255,lum[:,:,None]*[1.63,.55,1.35])[sel].astype('uint8');p=O/('pink_'+n+'.webp');Image.fromarray(a).save(p,format='WEBP',lossless=True,method=4);M['banks']['pink_'+n]={**B,'key':'s911_pink_'+n,'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(S/'generation.json').write_text(json.dumps(M['sources'],indent=2)+'\n',encoding='utf-8');(R/'assets/stage9_amplify_art_1101.js').write_text('"use strict";\nconst S911_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Registered',len(M['models']),'distinct models and',len(M['banks']),'fixed even banks',flush=True)
