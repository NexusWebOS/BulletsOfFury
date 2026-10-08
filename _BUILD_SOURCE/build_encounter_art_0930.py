"""Pack reviewed generated pixels; fixed pivots, shared scales, no painted sprites."""
from pathlib import Path
from PIL import Image
import json, shutil, argparse

SOURCES={
 'vent':'exec-bb3226ee-c155-406b-adb2-a2ddc896f1b6.png',
 'tank':'exec-e98c04ab-27b3-47b4-ab70-e9b34ad09db5.png',
 'jet':'exec-15a3b323-ba0f-47f8-a15b-a76e1de275d1.png',
 'ace':'exec-5c5b6ff6-c5ed-450a-bd5f-ee95bfdc8f73.png',
 'bomber':'exec-33de87e7-6cd4-4ac5-b6ef-134bc28a5189.png',
 'entry':'exec-b87eabae-1de3-424d-a8bb-7aa60852416c.png'}

def build(root):
 src=root/'_ART_SOURCES/encounters_0930';out=root/'assets/game/encounters_0930'
 src.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
 gen=Path('C:/Users/Mike/.codex/generated_images/01a0c9fd-a6cc-73a3-8dca-3e0f7a90a956')
 for name,f in SOURCES.items():
  if not (src/(name+'.png')).exists():shutil.copy2(gen/f,src/(name+'.png'))
 reg={}
 def bounds(im):return im.getchannel('A').point(lambda x:255 if x>32 else 0).getbbox()
 def pack(name,cells,size,pivots=None,scale=None,anchor=None):
  w,h=size;anchor=anchor or (w/2,h/2)
  boxes=[bounds(c) for c in cells]
  if pivots is None:pivots=[((b[0]+b[2])/2,(b[1]+b[3])/2) for b in boxes]
  if scale is None:
   scale=min(min((w-8)/(b[2]-b[0]),(h-8)/(b[3]-b[1])) for b in boxes)
  atlas=Image.new('RGBA',(w*len(cells),h)); rects=[]
  for i,(c,b,p) in enumerate(zip(cells,boxes,pivots)):
   q=c.crop(b).resize((max(1,round((b[2]-b[0])*scale)),max(1,round((b[3]-b[1])*scale))),Image.Resampling.NEAREST)
   x=round(anchor[0]+(b[0]-p[0])*scale);y=round(anchor[1]+(b[1]-p[1])*scale)
   assert x>=0 and y>=0 and x+q.width<=w and y+q.height<=h,(name,i,(x,y),q.size,size)
   atlas.alpha_composite(q,(i*w+x,y));rects.append([i*w,0,w,h])
  atlas.save(out/(name+'.png'))
  reg[name]={'key':'enc30_'+name,'path':'assets/game/shared/combat/encounters_0930/'+name+'.png','frames':rects,'size':[w,h],'anchor':list(anchor)}
  return atlas
 # Two tracked hull frames; turret pivot stays at its round socket, not the gun tip.
 im=Image.open(src/'tank.png').convert('RGBA')
 pack('tank_hull',[im.crop((0,0,600,512)),im.crop((0,512,600,1024))],(128,144),[(327,271),(327,250)],.25,(64,76))
 pack('tank_turret',[im.crop((600,0,1060,520)),im.crop((1060,0,1536,520))],(128,144),[(236,237),(211,237)],.20,(64,65))
 pack('tank_pod_l',[im.crop((600,520,1060,1024))],(40,72))
 pack('tank_pod_r',[im.crop((1060,520,1536,1024))],(40,72))
 # Reviewed nonuniform column cuts. Retain actual projected bank widths.
 im=Image.open(src/'jet.png').convert('RGBA')
 jet=[im.crop((a,0,b,685)) for a,b in [(0,575),(575,1050),(1050,1536)]]
 pack('jet',[*jet],(120,144),[(302,355),(219,355),(256,355)],.19,(60,72))
 for name,a,b in [('laser',0,575),('missile',575,1050),('rotary',1050,1536)]:pack('jet_'+name,[im.crop((a,685,b,1024))],(36,60))
 # Consistent base size for roll and pitch; never auto-fit narrow edge frames.
 im=Image.open(src/'ace.png').convert('RGBA');cw=im.width/4;ch=im.height/5
 cols=[0,330,616,865,im.width]
 cells=[im.crop((cols[i%4],round(i//4*ch),cols[i%4+1],round((i//4+1)*ch))) for i in range(20)]
 atlas=pack('ace',cells,(176,184),scale=.53)
 # Pixel-exact separated wing/fuselage modules from the generated level plates.
 for f,suffix in [(0,''),(1,'_damage')]:
  full=atlas.crop((f*176,0,(f+1)*176,184))
  for name,x0,x1 in [('wing_l',0,53),('body',53,123),('wing_r',123,176)]:
   p=Image.new('RGBA',(176,184));p.alpha_composite(full.crop((x0,0,x1,184)),(x0,0));p.save(out/('ace_'+name+suffix+'.png'))
   k='ace_'+name+suffix;reg[k]={'key':'enc30_'+k,'path':'assets/game/shared/combat/encounters_0930/'+k+'.png','frames':[[0,0,176,184]],'size':[176,184]}
 im=Image.open(src/'bomber.png').convert('RGBA');cw=im.width/4
 pack('bomber',[im.crop((round(i*cw),0,round((i+1)*cw),im.height)) for i in range(4)],(192,200),[(cw/2,365)]*4,.33,(96,100))
 # Outlet is one immutable plate. The separately anchored fluid cannot move it.
 im=Image.open(src/'vent.png').convert('RGBA');cw=im.width/4;ch=im.height/2
 cells=[im.crop((round(i%4*cw),round(i//4*ch),round((i%4+1)*cw),round((i//4+1)*ch))) for i in range(8)]
 pack('vent_body',[cells[0].crop((0,0,207,440))],(116,180),[(196,270)],.48,(104,100))
 jets=[]
 for i,x in enumerate([198,166,177,192,187,177,178,200]):
  # Trim only the fluid right of the grate; row two is lower by 11 source pixels.
  y=270 if i<4 else 260
  jets.append(cells[i].crop((x,y-100,round(cw),y+108)))
 # Empty first two cells are deliberate, not a missing image.
 w,h=180,100;atlas=Image.new('RGBA',(8*w,h))
 for i in range(2,8):
  q=jets[i];q=q.resize((round(q.width*.66),round(q.height*.46)),Image.Resampling.NEAREST)
  atlas.alpha_composite(q,(i*w,2))
 atlas.save(out/'vent_fluid.png');reg['vent_fluid']={'key':'enc30_vent_fluid','path':'assets/game/shared/combat/encounters_0930/vent_fluid.png','frames':[[i*w,0,w,h] for i in range(8)],'size':[w,h]}
 im=Image.open(src/'entry.png').convert('RGBA');im=im.resize((680,1120),Image.Resampling.NEAREST);im.save(out/'sewer_entry.png')
 reg['entry']={'key':'enc30_entry','path':'assets/game/shared/combat/encounters_0930/sewer_entry.png','frames':[[0,0,680,1120]],'size':[680,1120]}
 (out/'manifest.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf8')
 (src/'provenance.json').write_text(json.dumps({'tool':'built-in image_gen','sources':SOURCES,'processing':'Reviewed cell cuts and pivots, nearest-neighbour resampling, preserved generated alpha. Wing modules are exact crops of level poses; vent fluid separated from stationary outlet.'},indent=2)+'\n',encoding='utf8')
 (root/'assets/encounter_art_0930.js').write_text('/* Generated by build_encounter_art_0930.py */\nconst ENC30_ART='+json.dumps(reg,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
 print('Packed',len(reg),'encounter families')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);build(p.parse_args().root)
