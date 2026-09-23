"""Normalize the generated component sheet with a shared scale and anchors per reel."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/game/chaos_harrier/mk2_0923'
im=Image.open(OUT/'frames_source.png').convert('RGBA')
cols=[0,545,1050,1550,2048]
rows=[0,570,1135,1560,2048]
# Measured hardware anchors, in source-sheet pixels; stable sockets, not glow bounds.
hull=[(288,276),(800,276),(1302,276),(1802,276)]
gun=[(250,636),(751,636),(1245,636),(1746,636)]
specs=[('hull',(320,320),.48,(160,145)),('gun',(192,256),.38,(80,44)),
       ('emitter',(128,256),.50,(64,224)),('thruster',(128,256),.45,(64,236))]
manifest={'source':'frames_source.png','frames':{},'anchors':{}}
for row,(name,size,scale,anchor) in enumerate(specs):
 manifest['anchors'][name]={'size':size,'scale':scale,'anchor':anchor}
 for f in range(4):
  l,t,r,b=cols[f],rows[row],cols[f+1],rows[row+1]
  cell=im.crop((l,t,r,b));bb=cell.getchannel('A').point(lambda a:255 if a>180 else 0).getbbox()
  assert bb,(name,f)
  if row==0:src_anchor=hull[f]
  elif row==1:src_anchor=gun[f]
  else:src_anchor=(l+(bb[0]+bb[2])/2,t+bb[3]-(12 if row==2 else 25))
  # Keep source padding/glow and one common scale; do not resize frames to individual bounds.
  resized=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.NEAREST)
  frame=Image.new('RGBA',size)
  pos=(round(anchor[0]-(src_anchor[0]-l)*scale),round(anchor[1]-(src_anchor[1]-t)*scale))
  frame.alpha_composite(resized,pos)
  file=f'{name}_{f}.png';frame.save(OUT/file)
  manifest['frames'][file]={'sha12':hashlib.sha256((OUT/file).read_bytes()).hexdigest()[:12],
                           'source_cell':[l,t,r,b],'source_anchor':src_anchor}
(OUT/'frames.json').write_text(json.dumps(manifest,indent=2))
# Preview only; actual game files retain their transparent canvas and shared anchors.
preview=Image.new('RGBA',(1280,1280),(9,12,20,255))
for row,(name,size,scale,anchor) in enumerate(specs):
 for f in range(4):
  frame=Image.open(OUT/f'{name}_{f}.png');preview.alpha_composite(frame,(f*320+(320-frame.width)//2,row*320+(320-frame.height)//2))
preview.resize((960,960),Image.Resampling.NEAREST).save(ROOT/'_shots/harrier_mk2_normalized.png')
print('Normalized 16 generated frames with stable component anchors.')
