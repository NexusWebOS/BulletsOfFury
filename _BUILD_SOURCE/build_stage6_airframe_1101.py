"""One canonical hull per Stage6 jet. No generated attack/movement hull reels.
Fixed even direction cells, actual-source1015 masks and measured gun/nozzle anchors.
"""
from pathlib import Path
import json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import maximum_filter,label
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/stage6_airframe_1101';O=R/'assets/game/levels/stage_06/enemies/airframe_1101';Q=R/'_shots/stage6_airframe_1101'
for p in[S,O,Q]:p.mkdir(parents=True,exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
F={'fighter_black':'exec-2910a8b5-e388-46e6-8dec-4ac9465e3448.png','fighter_navy':'exec-82f42936-2f23-4f0c-9814-e8956317c495.png','fighter_teal':'exec-27f8ccf5-b6ce-4d8a-9f66-c1f0bb965c1a.png','heavy_wind':'exec-981b2be5-fa98-493b-b212-5ad48bb477b3.png','bomber_navy':'exec-815929af-cc7d-4693-8d67-9e3c78dabaeb.png','bomber_black':'exec-c9ec1d88-2e07-4017-8b3f-038d85d1383a.png'}
# Measured on original generated PNGs, not guessed from the old airframe.
P={'fighter_black':{'guns':[[546,990],[709,990]],'tails':[[510,164],[747,164]]},'fighter_navy':{'guns':[[435,845],[818,845]],'tails':[[550,208],[705,208]]},'fighter_teal':{'guns':[[326,985],[350,985],[901,985],[925,985]],'tails':[[550,203],[705,203]]},'heavy_wind':{'guns':[[373,906],[407,906],[848,906],[883,906]],'tails':[[477,201],[566,221],[684,221],[775,201]]},'bomber_navy':{'guns':[[536,1007],[717,1007]],'tails':[[450,182],[551,182],[698,182],[801,182]]},'bomber_black':{'guns':[[536,1007],[717,1007]],'tails':[[450,182],[551,182],[698,182],[801,182]]}}
M={'owner':'_BUILD_SOURCE/build_stage6_airframe_1101.py','policy':'One canonical solid source hull; source-preserving directional exports only. No idle/attack/body-morph animation. Native six-step1015 companion, separate animated nozzle/muzzle effects.','models':{},'banks':{},'sources':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def data(f,n):return json.JSONDecoder().raw_decode((R/f).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
def bank(n,t,dirs=32):
 c=t.width;im=Image.new('RGBA',(c*dirs,c))
 for d in range(dirs):im.alpha_composite(t.rotate(-d*360/dirs,Image.Resampling.NEAREST),(d*c,0))
 p=O/(n+'.webp');im.save(p,format='WEBP',lossless=True,method=4);B={'id':n,'key':'s611_'+n,'path':p.relative_to(R).as_posix(),'cell':c,'dirs':dirs,'frames':1,'span':144,'pivot':[c//2,c//2],'banks':{'idle':{'row':0,'frames':1}},'sha256':sha(p)};M['banks'][n]=B;return B
def glow(t):
 a=np.array(t);rgb=a[:,:,:3].astype(float);em=(a[:,:,3]>80)&(rgb[:,:,2]>95)&(rgb[:,:,2]>rgb[:,:,0]*1.3)&(rgb[:,:,1]>55);level=np.where(em,170,np.where(maximum_filter(em,3),65,np.where(maximum_filter(em,5),20,0)));g=np.zeros_like(a);g[:,:,:3]=a[:,:,:3];g[:,:,0]=np.where(em,np.maximum(g[:,:,0],65),55);g[:,:,1]=np.where(em,np.maximum(g[:,:,1],150),155);g[:,:,2]=np.where(em,np.maximum(g[:,:,2],235),255);g[:,:,3]=level;return Image.fromarray(g)
preview=Image.new('RGB',(192*5,216*2),(9,20,32));dd=ImageDraw.Draw(preview)
def install(n,t,world,guns,tails,src,preserved=False):
 B=bank(n,t);B['span']=144;B['nativeRatios']={};B['legacyKeys']=[];G=bank(n+'_glow',glow(t));G['span']=144
 # R46 hardpoints are in a64-centred source coordinate basis.
 def snap(p):
  a=np.array(t)[:,:,3];x,y=p;yy,xx=np.nonzero(a>80);dist=(xx-x)**2+(yy-y)**2;j=dist.argmin();return[int(xx[j]),int(yy[j])]
 guns=[snap(p)for p in guns];tails=[snap(p)for p in tails];sockets={'port':[guns[0][0]-32,guns[0][1]-32],'starboard':[guns[-1][0]-32,guns[-1][1]-32],'centre':[guns[0][0]-32,guns[0][1]-32],'core':[64,64],'exhaustPort':[tails[0][0]-32,tails[0][1]-32],'exhaustStarboard':[tails[-1][0]-32,tails[-1][1]-32]};B['sockets']=sockets
 M['models'][n]={'bank':B,'glow':G,'spanWorld':world,'sourceSpan':144,'guns':[[p[0]-32,p[1]-32]for p in guns],'tails':[[p[0]-32,p[1]-32]for p in tails],'sockets':sockets,'source':src,'preservedWind':preserved,'canonicalHullFrames':1}
 i=len(M['models'])-1;x=i%5*192;y=i//5*216;preview.paste(t,(x,y+20),t);dd.text((x+3,y+3),n,fill='white')
 for p in guns:dd.ellipse((x+p[0]-2,y+p[1]+18,x+p[0]+2,y+p[1]+22),fill='#ffdf40')
 for p in tails:dd.ellipse((x+p[0]-2,y+p[1]+18,x+p[0]+2,y+p[1]+22),fill='#40ffcf')
for n,f in F.items():
 p=S/(n+('_guns_source.png'if n=='fighter_teal'else'_source.png'))
 if not p.exists():shutil.copyfile(G/f,p)
 im=Image.open(p).convert('RGBA');a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=80,255,0);im=Image.fromarray(a);box=im.getbbox();pivot=[(box[0]+box[2])/2,(box[1]+box[3])/2];k=144/max(box[2]-box[0],box[3]-box[1]);z=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);t=Image.new('RGBA',(192,192));t.alpha_composite(z,(round(96-pivot[0]*k),round(96-pivot[1]*k)))
 points=lambda name:[[96+(x-pivot[0])*k,96+(y-pivot[1])*k]for x,y in P[n][name]]
 install(n,t,126 if n.startswith('bomber')else 120 if n=='heavy_wind'else 88,points('guns'),points('tails'),p.relative_to(R).as_posix());M['sources'][n]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'original':f,'tool':'built-in image_gen','requestedCell':[320,320]if n.startswith('bomber')or n=='heavy_wind'else[256,256],'exportCell':[192,192],'sourcePivot':pivot,'commonScale':k,'measuredSourceSockets':P[n]}
# Keep the existing approved wind designs and the Tempest helper, frozen to idle0.
A=data('assets/enemy_flight_art_1031.js','R46_ART')
for n,id in [('wind_zephyr','bf_sky_zephyr'),('wind_gale','bf_sky_gale'),('wind_stratus','bf_sky_stratus'),('wind_helper','bf_dasher')]:
 b=A['models'][id];im=Image.open(R/b['path']).convert('RGBA');t=im.crop((0,0,b['cell'],b['cell']));box=t.getbbox();k=144/max(box[2]-box[0],box[3]-box[1]);t=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);z=Image.new('RGBA',(192,192));z.alpha_composite(t,(round(96-b['cell']/2*k),round(96-b['cell']/2*k)));p=lambda key:[96+(b['sockets'][key][0]-64)*k,96+(b['sockets'][key][1]-64)*k]
 install(n,z,96 if n!='wind_stratus'else 112,[p('port'),p('starboard')],[p('exhaustPort'),p('exhaustStarboard')],b['path'],True);M['sources'][n]={'path':b['path'],'sha256':sha(R/b['path']),'cell':[0,0,b['cell'],b['cell']],'canonicalPose':'idle0 only','sourceIdentity':id}
# Real authored compact effects. Palette copies retain alpha/outlines/white cores.
S1=data('assets/stage1_amplify_art_1031.js','S1A_ART')
for n in ['slug','thruster','muzzle']:
 b=S1[n];im=Image.open(R/b['path']).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);mask=(rgb.max(2)-rgb.min(2)>30)&(a[:,:,3]>0);ramp=np.stack([lum*.30,lum*1.30,lum*1.55],2);ramp/=np.dot([.30,1.30,1.55],[.2126,.7152,.0722]);a[:,:,:3][mask]=np.minimum(255,ramp)[mask].astype('uint8');p=O/(n+'.webp');Image.fromarray(a).save(p,format='WEBP',lossless=True,method=4);M['banks'][n]={**b,'key':'s611_'+n,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'source':b['path']}
preview.save(Q/'canonical-hulls-and-sockets.png');(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(R/'assets/stage6_airframe_art_1101.js').write_text('"use strict";\nconst S611_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');(S/'source-manifest.json').write_text(json.dumps(M['sources'],indent=2),encoding='utf-8');print('Registered',len(M['models']),'single-hull models and',len(M['banks']),'fixed banks')
