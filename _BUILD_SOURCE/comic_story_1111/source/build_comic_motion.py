"""Fixed raster zoom poses and black fade plates. Runtime only clips/positions/blits."""
from pathlib import Path
from PIL import Image
import json,hashlib,math
P=Path(__file__).resolve().parents[1]
ROOT=P.parents[1]
WORK=ROOT/'work/comic-motion-v3';WORK.mkdir(parents=True,exist_ok=True)
DEST=P/'overlay/assets/game/shared/cinematics/comic_motion_1111';DEST.mkdir(parents=True,exist_ok=True)
MASTERS=P/'masters/motion_v3';MASTERS.mkdir(exist_ok=True)
ZOOMS=[1,1.03,1.065,1.1,1.135,1.17,1.2]
pilots=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
registry={};jobs=[]
def bank(name,frames,w,h,cols,**extra):
 assert w%2==h%2==0 and all(f.size==(w,h)for f in frames)
 sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 folder=WORK/name;folder.mkdir(exist_ok=True);paths=[]
 for i,im in enumerate(frames):
  sheet.paste(im,(i%cols*w,i//cols*h));f=folder/f'{i:03}.png';im.save(f);paths.append(str(f))
 path=DEST/(name+'.webp');sheet.save(path,lossless=True,method=0)
 registry[name]=dict(key='cm3_'+name,path='assets/game/shared/cinematics/comic_motion_1111/'+path.name,w=w,h=h,cols=cols,frames=len(frames),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**extra)
 jobs.append(dict(name=name,w=w,h=h,frames=paths,output=str(MASTERS/(name+'.aseprite'))))
for pk in pilots:
 poses=[Image.open(P/f'portraits/{pk}/{i}.png').convert('RGBA')for i in range(7)]
 frames=[];sizes=[];baselines=[];bleeds=[]
 for zoom in ZOOMS:
  size=round(256*zoom);even=size+size%2;variants=[im.resize((size,size),Image.Resampling.NEAREST)for im in poses]
  sizes.append(even);baselines.append(max(im.getbbox()[3]for im in variants));bleeds.append(math.ceil(2*zoom))
  for im in variants:
   canvas=Image.new('RGBA',(308,308));canvas.paste(im,(0,0));frames.append(canvas)
 bank('talk-zoom-'+pk,frames,308,308,7,sizes=sizes,baselines=baselines,bleeds=bleeds,native=[128,128],scales=ZOOMS)
 bg=Image.open(P/f'masters/pilot-backgrounds/{pk}.png').convert('RGBA');bgframes=[];bgsizes=[]
 for zoom in ZOOMS:
  w,h=round(512*zoom),round(340*zoom);im=bg.resize((w,h),Image.Resampling.NEAREST);canvas=Image.new('RGBA',(616,410));canvas.paste(im,(0,0));bgframes.append(canvas);bgsizes.append([w,h])
 bank('backdrop-zoom-'+pk,bgframes,616,410,3,sizes=bgsizes,scales=ZOOMS)
for i in range(4):
 source=Image.open(P/f'masters/pages/page-{i}.0-fg.png').convert('RGBA')
 top=source.crop((0,0,838,322));frames=[]
 for zoom in ZOOMS:
  im=top.resize((round(838*zoom),round(322*zoom)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',(1008,388));canvas.paste(im,(0,0));frames.append(canvas)
 bank('strip-'+str(i),frames,1008,388,2,scales=ZOOMS)
 bank('caption-'+str(i),[source.crop((0,322,838,470))],838,148,1)
alphas=[255,224,192,160,128,96,64,32,0]
bank('ink-fade',[Image.new('RGBA',(512,350),(0,0,0,a))for a in alphas],512,350,3,alphaSteps=alphas)
art=dict(version=1,canvas=[912,512],visualHeight=350,captionY=350,zooms=ZOOMS,banks=registry)
(P/'overlay/assets/comic_motion_art_1111.js').write_text("'use strict';\nconst CM3_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
(P/'source/motion-manifest.json').write_text(json.dumps(art,indent=2),encoding='utf8')
(P/'source/motion-editor-jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')
print(json.dumps(dict(banks=len(registry),frames=sum(a['frames']for a in registry.values()),pixels=sum(a['w']*a['h']*a['frames']for a in registry.values()))))
