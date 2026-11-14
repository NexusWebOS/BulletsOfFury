"""Compile authored, unscaled dialogue tile frames and registered talking portraits."""
from pathlib import Path
from PIL import Image, ImageChops
import json, hashlib, subprocess

P=Path(__file__).resolve().parents[1]
DEST=P/'overlay/assets/game/shared/cinematics/dialogue_1111'
DEST.mkdir(parents=True,exist_ok=True)
SOURCE=P/'masters/dialogue_1111'
TINTS={'cole':(122,214,58),'axel':(58,138,255),'freezer':(111,208,255),'yuri':(226,58,58),'maverick':(58,214,200),'falva':(255,42,143),'lizzie':(255,194,26),'decker':(255,210,74),'juggernaut':(192,138,58)}
registry={};jobs=[]
def save(name,im,**data):
 path=DEST/(name+'.png');im.save(path)
 registry[name]=dict(key='cx4_'+name,path='assets/game/shared/cinematics/dialogue_1111/'+path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**data)
 source=SOURCE/(name+'.png');im.save(source)
 jobs.append(dict(input=str(source),output=str(SOURCE/(name+'.aseprite'))))

def normalize(role):
 im=Image.open(SOURCE/(role+'-master.png')).convert('RGBA')
 box=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox()
 im=im.crop(box).resize((432,96),Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda a:255 if a>128 else 0)
 im=im.convert('RGB').quantize(colors=32,method=Image.Quantize.MEDIANCUT).convert('RGBA');im.putalpha(alpha)
 return im.resize((864,192),Image.Resampling.NEAREST)

def tiles(name,im,compact=False):
 # Unequal steel header caps retain the name recess and right status lamps.
 # Centre strips repeat by cropping the final tile. No runtime stretching.
 mid=400
 boxes={'tl':(0,0,360,64),'tc':(mid,0,mid+32,64),'tr':(576,0,864,64),
        'l':(0,80,24,112),'c':(420,80,452,112),'r':(840,80,864,112),
        'bl':(0,172,64,192),'bc':(410,172,442,192),'br':(800,172,864,192)}
 scale=2 if compact else 1
 if compact:im=im.resize((432,96),Image.Resampling.NEAREST)
 boxes={key:tuple(v//scale for v in box)for key,box in boxes.items()}
 atlas=Image.new('RGBA',(680//scale,116//scale));rects={};x=y=0
 for group,height in [(['tl','tc','tr'],64//scale),(['l','c','r'],32//scale),(['bl','bc','br'],20//scale)]:
  x=0
  for key in group:
   part=im.crop(boxes[key]);atlas.paste(part,(x,y));rects[key]=[x,y,part.width,part.height];x+=part.width
  y+=height
 save('frame-'+name+('-compact'if compact else''),atlas,parts=rects,header=64//scale,bottom=20//scale,minWidth=648//scale)

crew=normalize('crew')
for role in ['crew','command','hostile','narration']:
 im=crew if role=='crew' else normalize(role)
 im.save(SOURCE/(role+'-normalized.png'))
 if role!='crew':
  for compact in [False,True]:tiles(role,im,compact)
for pk,tint in TINTS.items():
 im=crew.copy()
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=im.getpixel((x,y))
   if a and max(g,b)>r*1.45 and max(g,b)-min(r,g,b)>45 and max(g,b)>70:
    light=max(g,b)/255;im.putpixel((x,y),tuple(round(v*light)for v in tint)+(a,))
 for compact in [False,True]:tiles('crew-'+pk,im,compact)
 for size in [48,64,84,96]:
  sheet=Image.new('RGBA',(size,size*7));baselines=[]
  for i in range(7):
   face=Image.open(P/f'portraits/{pk}/{i}.png').convert('RGBA').resize((size,size),Image.Resampling.NEAREST)
   sheet.paste(face,(0,size*i));baselines.append(face.getbbox()[3])
  save(f'face-{pk}-{size}',sheet,pilot=pk,size=size,frames=7,baselines=baselines)

art=dict(version=1,revision=2,material='rectangular-bolted-steel',banks=registry,pilots=list(TINTS),styles=['crew','command','hostile','narration'])
(P/'overlay/assets/cinematic_dialogue_art_1111.js').write_text("'use strict';\nconst CX4_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
(P/'source/dialogue-editor-jobs.json').write_text(json.dumps(jobs,indent=2),encoding='utf8')
(P/'source/dialogue-art-manifest.json').write_text(json.dumps(art,indent=2),encoding='utf8')
print(json.dumps(dict(banks=len(registry),styles=4,pilotColors=len(TINTS),talkingSizes=[48,64,84,96])))
