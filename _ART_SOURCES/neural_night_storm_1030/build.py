"""NB81. Clean midnight cloud parallax and source-authored1015 storm glow.
All palette/alpha/outer-light artwork is baked offline; actual body pose remains.
"""
from pathlib import Path
from PIL import Image,ImageFilter
import json,numpy as np,math,hashlib,shutil
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_shots/neural_night_storm_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(exist_ok=True,parents=True)
O=R/'assets/game/levels/stage_08/boss/neural_night_storm_1030';D=R/'_ART_SOURCES/neural_night_storm_1030';O.mkdir(exist_ok=True,parents=True);D.mkdir(exist_ok=True,parents=True)
s=(R/'assets/dracodia_brain_art_1023.js').read_text();N=json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
A={'banks':{},'pages':{},'arena':{},'bodyLogical':[384,384],'bodyPivot':[192,192]};sources={};page=Image.new('RGBA',(1024,1024));px=py=rh=pi=0
def flush():
 global page,px,py,rh,pi
 key='nb81_page_'+str(pi);h=max(2,min(1024,(py+rh+3)//2*2));im=page.crop((0,0,1024,h));p=O/(key+'.webp');im.save(p,lossless=True,method=6);A['pages'][key]={'path':p.relative_to(R).as_posix(),'w':1024,'h':h};pi+=1;page=Image.new('RGBA',(1024,1024));px=py=rh=0
def emit(name,im):
 global px,py,rh
 b=im.getbbox();assert b and min(b[:2])>0 and max(b[2:])<384
 x0=b[0]//2*2;y0=b[1]//2*2;x1=(b[2]+1)//2*2;y1=(b[3]+1)//2*2;crop=im.crop((x0,y0,x1,y1));w,h=crop.size
 if px+w+2>1024:px=0;py+=rh+2;rh=0
 if py+h+2>1024:flush()
 page.paste(crop,(px,py));a={'key':'nb81_page_'+str(pi),'rect':[px,py,w,h],'offset':[x0-192,y0-192],'w':w,'h':h,'logical':[384,384]};A['banks'].setdefault(name,[]).append(a);px+=w+2;rh=max(rh,h)
def body(f):
 a=N['banks']['brain'][f];p=R/N['sheets'][a['sheet']]['path'];sources[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();im=Image.open(p).convert('RGBA');x,y,w,h=a['cell'];return im.crop((x,y,x+w,y+h))
strip=Image.new('RGBA',(384*9,384*6))
for level in range(6):
 for f in range(9):
  src=body(f);v=np.array(src);alpha=v[:,:,3];rgb=v[:,:,:3].astype(float);mask=(rgb[:,:,2]>rgb[:,:,1]*1.25)&(rgb[:,:,2]>rgb[:,:,0]*1.08)&(alpha>0);strength=level/5
  target=np.array([245,212,255]);rgb[mask]=rgb[mask]*(1-strength*.68)+target*(strength*.68);v[:,:,:3]=np.clip(rgb,0,255).astype(np.uint8)
  out=Image.new('RGBA',(384,384))
  if level:
   far=np.array(src.getchannel('A').filter(ImageFilter.MaxFilter(11)));near=np.array(src.getchannel('A').filter(ImageFilter.MaxFilter(5)));halo=np.zeros((384,384,4),np.uint8);halo[:,:,:3]=[101,24,191];halo[:,:,3]=((far>0)&(alpha==0))*round(55+strength*95);halo[near>0,:3]=[203,124,255];halo[:,:,3][(near>0)&(alpha==0)]=round(100+strength*125);halo[:,:,3][alpha>0]=0;out.alpha_composite(Image.fromarray(halo))
  out.alpha_composite(Image.fromarray(v));emit('glow_'+str(level),out);strip.alpha_composite(out,(384*f,384*level))
flush();strip.save(D/'storm-glow-source-strip.png')
gen=D/'night-sky-generated.png'
if not gen.exists():shutil.copy2(Path(r'C:\Users\Mike\.codex\generated_images\01a10ef4-27c3-71d2-97c8-0d9fa5c0bb2f\exec-09562915-2a44-4f0f-a555-7c3884ddd631.png'),gen)
im=Image.open(gen).convert('RGBA').resize((340,340),Image.Resampling.NEAREST).resize((680,680),Image.Resampling.NEAREST);v=np.array(im)
# A stored seam transition makes gentle vertical looping continuous.
for y in range(40):
 u=y/39;v[640+y]=(v[640+y].astype(float)*(1-u)+v[y].astype(float)*u).astype(np.uint8)
im=Image.fromarray(v);im.save(O/'night_sky.png')
near=v.copy();light=near[:,:,:3].max(2).astype(float);near[:,:,3]=np.clip((light-48)*.48,0,64).astype(np.uint8);Image.fromarray(near).save(O/'night_clouds.png')
wire=v.copy();wire[:,:,:3]=(wire[:,:,:3].astype(float)*.40).astype(np.uint8);Image.fromarray(wire).save(O/'night_download.png')
for name,file in [('sky','night_sky.png'),('clouds','night_clouds.png'),('download','night_download.png')]:A['arena'][name]={'key':'nb81_'+name,'path':(O/file).relative_to(R).as_posix(),'w':680,'h':680}
(R/'assets/neural_night_storm_art_1030.js').write_text("'use strict';\nconst NB81_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(D/'manifest.json').write_text(json.dumps(A,separators=(',',':')))
(D/'provenance.json').write_text(json.dumps({'sources':sources,'generatedSource':gen.name,'mode':'Built-in image generator edit of approved sky plate; mechanical wreckage removed, midnight palette.','glowFrames':54,'levels':6,'poses':9,'sky':[680,680],'runtime':'Fixed blits, source alpha, source-locked poses; no live tint, scaling, alpha animation or generated glow.'},indent=2));im.save(W/'night-sky-preview.png');print(json.dumps({'frames':54,'pages':len(A['pages']),'arenaLayers':list(A['arena'])}))
