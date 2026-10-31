"""Deterministic export of approved PixelLab sources, fixed body unit and roots."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib,wave,struct
import numpy as np
R=Path(__file__).resolve().parents[3];A=R/'expansion/topdown/art/escape29';S=A/'source/escape29';F=A/'frames';F.mkdir(parents=True,exist_ok=True);O=R/'_shots/escape29';O.mkdir(parents=True,exist_ok=True)
assets={};seqs={};audit=[]
def save(key,im,anchor,muzzle=None,**meta):
 im=im.convert('RGBA');im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0));b=im.getbbox();assert b,(key,'empty');assert not(im.width%2 or im.height%2)
 p=F/(key+'.png');im.save(p);assets[key]={'file':p.relative_to(R).as_posix(),'size':list(im.size),'anchor':list(anchor),'bounds':list(b),'drawScale':1,**meta}
 if muzzle:assets[key]['muzzle']=list(muzzle)
 audit.append({'key':key,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bounds':list(b)})
 return key
def raw(name,i=0):
 if name=='slide_back_imagegen':
  im=Image.open(S/name/'original.png').convert('RGBA');im.putalpha(im.getchannel('A').point(lambda v:255 if v>=128 else 0));im=im.crop(im.getbbox());scale=172/im.height;im=im.resize((round(im.width*scale),172),Image.Resampling.NEAREST);out=Image.new('RGBA',(192,224));out.alpha_composite(im,((192-im.width)//2,30));return out
 return Image.open(S/name/f'{i:02}.png').convert('RGBA')
def body(name,i,side='west',angle=0,ground=True):
 im=raw(name,i);assert im.size==(192,224);b=im.getbbox();ar=np.array(im)
 # Fixed half-resolution unit. Grounded clips carry a measured root_delta;
 # neither per-frame resizing nor fitting is used. Airborne vault holds its root.
 rootX=124;rootY=b[3] if ground else 206
 if name in ['aim_-75_v2','aim_-60_v2','aim_-45_v2']:rootX={'aim_-75_v2':109,'aim_-60_v2':137,'aim_-45_v2':137}[name]
 if name.startswith('slide') and name!='slide_flat':rootX=110;rootY=160
 im=im.resize((96,112),Image.Resampling.NEAREST);out=Image.new('RGBA',(192,224));ox=96-round(rootX*.5);oy=160-round(rootY*.5);out.alpha_composite(im,(ox,oy))
 # Barrel is the outer dark steel point in the directional weapon cone.
 yy,xx=np.indices(ar.shape[:2]);dark=(ar[:,:,3]>127)&(ar[:,:,0]<105)&(ar[:,:,1]<110)&(ar[:,:,2]<120)
 vx=-math.cos(math.radians(angle));vy=-math.sin(math.radians(angle));sx,sy=(108,85)
 dx=xx-sx;dy=yy-sy;projection=dx*vx+dy*vy;sideDist=np.abs(dx*vy-dy*vx)
 mask=dark&(xx<135)&(yy<187)
 if name.startswith('slide') and name not in ['slide_flat','slide_back_imagegen']:mask=dark&(xx<135)&(yy<110)
 if mask.any():
  if angle>=60:
   y=int(yy[mask].min());x=round(float(np.median(xx[mask&(yy<=y+2)])))
  else:
   x=int(xx[mask].min());ys=yy[mask&(xx<=x+2)];y=int(ys.max())if angle<-45 else int(ys.min())if angle>35 else round(float(np.median(ys)))
  muzzle=[ox+round(x*.5),oy+round(y*.5)]
 else:muzzle=[ox+24,oy+35]
 if name=='slide_back_imagegen':
  m=dark&(yy<140);x=int(xx[m].max());y=round(float(np.median(yy[m&(xx>=x-2)])));muzzle=[ox+round(x*.5),oy+round(y*.5)]
 if side=='east':out=out.transpose(Image.Transpose.FLIP_LEFT_RIGHT);muzzle[0]=191-muzzle[0]
 return out,muzzle,[rootX,rootY]
angles=list(range(-90,91,15))
for side in ['west','east']:
 keys=[]
 for index,angle in enumerate(angles):
  name='side_down'if angle==-90 else'side_up'if angle==90 else'side_setup'if angle==0 else'aim_'+str(angle)
  if angle in [-75,-60,-45,60,75]:name+='_v2'
  im,tip,sr=body(name,0,side,angle);key=save(f'e29_aim_{side}_{index}',im,[96,160],tip,nominalAngle=angle,source=name,sourceRoot=sr);keys.append(key)
 seqs['e29_aim_'+side]={'frames':keys,'fps':20,'angles':angles,'loop':False}
 for name,source,start,end,fps in [('run','run_clean',1,17,22),('vault','vault',1,17,19),('roll','roll',1,17,32),('crouch','crouch',5,13,14),('prone','prone',1,17,20),('cover_peek','cover_clean',0,7,12),('slide_motion','slide_motion',1,13,18)]:
  keys=[]
  for i in range(start,end):
   im,tip,sr=body(source,i,side,30 if name=='slide_motion'else 0,ground=name!='vault');key=save(f'e29_{name}_{side}_{i-start}',im,[96,160],tip,source=source,sourceFrame=i,sourceRoot=sr);keys.append(key)
  seqs[f'e29_{name}_{side}']={'frames':keys,'fps':fps,'loop':name in ['run','crouch','slide_motion'],'root':[96,160],'scale':.5}
 im,tip,sr=body('slide_flat',0,side);k=save('e29_slide_flat_'+side,im,[96,160],tip,source='slide_flat');seqs['e29_slide_flat_'+side]={'frames':[k],'fps':1}
for name in ['slide_up','slide_back','slide_down']:
 source='slide_back_imagegen'if name=='slide_back'else name
 im,tip,sr=body(source,0,'east',90 if name=='slide_up' else -45 if name=='slide_down' else 0);save('e29_'+name,im,[96,160],tip,source=source)
for name,index in [('barrier',0),('wall',0),('relay',0),('crate',0),('barrel',0),('side_wall',0),('side_floor',0),('elevator',0),('hatch',0),('drone',0)]:
 im=raw(name,index);b=im.getbbox();anchor=[im.width//2,b[3]]
 if name in ['side_wall','side_floor']:anchor=[0,0]
 if name in ['elevator','drone']:anchor=[im.width//2,im.height//2]
 save('e29_'+name,im,anchor,bodyWidth=b[2]-b[0],bodyHeight=b[3]-b[1],source=name)
keys=[]
for i in range(1,13):keys.append(save('e29_drone_'+str(i-1),raw('drone_motion',i),[64,64],source='drone_motion',sourceFrame=i))
seqs['e29_drone']={'frames':keys,'fps':18,'loop':True}
# Reuse authored straight doors and damaged flat cover. Keep their sources.
old=json.loads((R/'expansion/topdown/art/pixel25/manifest.json').read_text())['assets']
for name,key in [('exit','px25_door'),('exit_open','px25_door_open')]:
 m=old[key];im=Image.open(R/m['file']).convert('RGBA');b=im.getbbox();sc=160/(b[3]-b[1]);crop=im.crop(b);out=crop.resize((math.ceil(crop.width*sc/2)*2,160),Image.Resampling.NEAREST);save('e29_'+name,out,[out.width//2,160],sourceKey=key)
# An actual rectangular vent extracted from the newly authored wall tile.
im=raw('side_wall');vent=im.crop((148,30,236,106));save('e29_vent',vent,[44,38],source='side_wall',crop=[148,30,236,106])
pack={'build':'overdrive1015-escape29-r1','assets':assets,'sequences':seqs,'audit':audit,'unit':{'cell':[192,224],'root':[96,160],'bodyScale':.5,'mirroredRight':True,'normalization':'fixed half-scale, explicit per-frame ground contact root_delta; no fitting'},'source':'PixelLab generated artwork; existing approved authored door pieces reused'}
(A/'manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8',newline='\n');(A/'manifest.js').write_text('window.TD_ESCAPE29_ART='+json.dumps(pack,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
for name,q in seqs.items():
 keys=q['frames'];contact=Image.new('RGB',(192*4,240*((len(keys)+3)//4)),'#24333f');d=ImageDraw.Draw(contact)
 for i,k in enumerate(keys):
  im=Image.open(R/assets[k]['file']);x=i%4*192;y=i//4*240;contact.paste(im,(x,y),im);d.line((x,y+160,x+190,y+160),fill='#487260');d.text((x+4,y+225),k,fill='white')
 contact.save(O/(name+'.png'))
audio=R/'expansion/topdown/audio/escape29';audio.mkdir(parents=True,exist_ok=True)
for name,duration in [('power_down',1.6),('generator',2.0)]:
 rate=22050;phase=0;samples=[]
 for n in range(round(duration*rate)):
  t=n/rate;u=t/duration;freq=(650*(1-u)**2+32)if name=='power_down'else(38+u*70+7*math.sin(t*24));phase+=freq/rate;env=min(1,t/.04)*min(1,(duration-t)/.14);v=(math.sin(phase*math.tau)+.3*math.sin(phase*math.tau*2.02))*.3*env
  samples.append(int(max(-32767,min(32767,v*32767))))
 with wave.open(str(audio/(name+'.wav')),'wb')as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(struct.pack('<'+'h'*len(samples),*samples))
print(json.dumps({'assets':len(assets),'banks':len(seqs),'audio':['power_down.wav','generator.wav']}))
