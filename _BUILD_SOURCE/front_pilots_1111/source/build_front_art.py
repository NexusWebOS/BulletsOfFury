from pathlib import Path
from PIL import Image,ImageOps
import json,math,hashlib
P=Path(__file__).resolve().parents[1];G=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
D=P/'overlay/assets/game/shared/cinematics/front_pilots_1111';D.mkdir(exist_ok=True)
EDIT=P/'source/editor-input';EDIT.mkdir(exist_ok=True);SRC=P/'masters/aseprite';SRC.mkdir(exist_ok=True)
ZOOMS=[1,1.03,1.065,1.1,1.135,1.17,1.2]
PILOTS=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
banks={};jobs=[]
def bank(name,frames,w,h,cols=4,**meta):
 assert w%2==h%2==0 and all(im.size==(w,h)for im in frames)
 cols=min(cols,len(frames));sheet=Image.new('RGBA',(w*cols,h*math.ceil(len(frames)/cols)))
 for i,im in enumerate(frames):sheet.paste(im,(i%cols*w,i//cols*h))
 file=D/(name+'.webp');sheet.save(file,lossless=True,method=0)
 banks[name]=dict(key='fp5_'+name,path='assets/game/shared/cinematics/front_pilots_1111/'+file.name,w=w,h=h,cols=cols,frames=len(frames),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),**meta)
 png=EDIT/(name+'.png');sheet.save(png)
 jobs.append(dict(name=name,input=str(png),output=str(SRC/(name+'.aseprite')),w=w,h=h,cols=cols,frames=len(frames)))
def cover(im,size):return ImageOps.fit(im,size,method=Image.Resampling.NEAREST)
def fixed_palette(im,palette):
 a=im.getchannel('A');rgb=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(a);return rgb
rooms={}
for room in ['conference','workshop','hangar','lounge']:
 raw=Image.open(P/f'masters/background-{room}-master.png').convert('RGBA')
 pal=cover(raw,(512,340)).convert('RGB').quantize(colors=64,method=Image.Quantize.MEDIANCUT)
 rooms[room]=lambda size,r=raw,p=pal:fixed_palette(cover(r,size),p)
cockpit=Image.open(P/'masters/background-cockpit-master.png').convert('RGBA')
cockpit.putalpha(cockpit.getchannel('A').point(lambda a:255 if a>=128 else 0))
for kind,path in {'sky':'assets/game/shared/cinematics/story_1103/sky.webp','space':'assets/game/levels/stage_09/stage/expansion_v1/space/nst9_starfield.png','tunnel':'assets/game/shared/cinematics/story_1103/sewer.webp'}.items():
 world=Image.open(G/path).convert('RGBA')
 def compose(size,world=world):return Image.alpha_composite(cover(world,size),cover(cockpit,size))
 pal=compose((512,340)).convert('RGB').quantize(colors=64,method=Image.Quantize.MEDIANCUT)
 rooms['cockpit-'+kind]=lambda size,c=compose,p=pal:fixed_palette(c(size),p)
for name,make in rooms.items():
 normal=make((512,340));normal.save(P/f'masters/background-{name}.png')
 frames=[];sizes=[]
 for scale in ZOOMS:
  w,h=round(512*scale),round(340*scale);image=make((w,h));canvas=Image.new('RGBA',(616,410));canvas.paste(image,(0,0));frames.append(canvas);sizes.append([w,h])
 bank('backdrop-'+name,frames,616,410,3,sizes=sizes,source='generated-room-master'if not name.startswith('cockpit-')else'generated-canopy-with-native-mission-environment')
for pk in PILOTS:
 poses=[Image.open(P/f'portraits/{pk}/{i}.png').convert('RGBA')for i in range(7)]
 frames=[];sizes=[];baselines=[];bleeds=[]
 for scale in ZOOMS:
  n=round(256*scale);variants=[im.resize((n,n),Image.Resampling.NEAREST)for im in poses]
  sizes.append(n+n%2);baselines.append(max(im.getbbox()[3]for im in variants));bleeds.append(math.ceil(2*scale))
  for im in variants:
   canvas=Image.new('RGBA',(308,308));canvas.paste(im,(0,0));frames.append(canvas)
 bank('talk-zoom-'+pk,frames,308,308,7,sizes=sizes,baselines=baselines,bleeds=bleeds,native=[320,320],scales=ZOOMS,family='front-headset-free')
 for room in rooms:
  for size in [48,64,84,96]:
   background=cover(Image.open(P/f'masters/background-{room}.png').convert('RGBA'),(size,size));mini=[]
   for pose in poses:
    im=background.copy();face=pose.resize((size,size),Image.Resampling.NEAREST);im.alpha_composite(face);mini.append(im)
   bank(f'mini-{room}-{pk}-{size}',mini,size,size,1,size=size,pilot=pk,baselines=[size]*7,room=room)
art=dict(version=1,banks=banks,pilots=PILOTS,rooms=list(rooms),zooms=ZOOMS,nativePortrait=[320,320],mouthOrder=['closed','A','E','O','U','F','L'])
(P/'overlay/assets/front_pilots_art_1111.js').write_text("'use strict';\nconst FP5_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
(P/'source/art-manifest.json').write_text(json.dumps(art,indent=2),encoding='utf8')
(P/'source/art-editor-jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')
print(json.dumps(dict(banks=len(banks),frames=sum(x['frames']for x in banks.values()),rooms=len(rooms))))
