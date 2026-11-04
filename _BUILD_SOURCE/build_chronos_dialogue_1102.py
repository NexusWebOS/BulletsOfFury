"""Fit the approved Chronos avatar views to his approved frame, offline."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'assets/game/shared/cinematics/chronos_dialogue_1102';D.mkdir(parents=True,exist_ok=True)
S=R/'_ART_SOURCES/chronos_dialogue_1102';S.mkdir(parents=True,exist_ok=True)
framePath=R/'assets/game/shared/cinematics/cast_performance_1102/chronos-dialogue.png';frame=Image.open(framePath).convert('RGBA')
mask=Image.new('L',(512,512));ImageDraw.Draw(mask).polygon([(77,76),(435,76),(451,94),(451,426),(435,442),(77,442),(60,426),(60,94)],fill=255)
out={'poses':{},'sizes':[68,56,48,40,32,24],'sourceHashes':{str(framePath.relative_to(R)):hashlib.sha256(framePath.read_bytes()).hexdigest()},'method':'Approved source views, shared head crop and original framed bezel; all fitting baked offline.'}
review=Image.new('RGB',(1024,280),(11,17,25));draw=ImageDraw.Draw(review);sequence=[]
for i,pose in enumerate(['neutral','turn_right','turn_left','stern']):
 if pose=='neutral':im=frame.copy()
 else:
  path=R/'assets/game/shared/cinematics/cast_1102/chronos'/f'{pose}.png';actor=Image.open(path).convert('RGBA').crop((64,90,448,440))
  actor=actor.resize((392,358),Image.Resampling.NEAREST);inside=Image.new('RGBA',(512,512),(3,6,10,255));inside.alpha_composite(actor,(60,81));im=Image.composite(inside,frame,mask)
  out['sourceHashes'][str(path.relative_to(R))]=hashlib.sha256(path.read_bytes()).hexdigest()
 im.save(S/(pose+'-framed.png'));im.save(D/(pose+'-full.png'))
 a={'full':'c113_'+pose+'_full','compact':{},'files':{}}
 a['files'][a['full']]=(D/(pose+'-full.png')).relative_to(R).as_posix()
 for size in out['sizes']:
  key=f'c113_{pose}_{size}';p=D/(pose+'-'+str(size)+'.png');small=im.resize((size,size),Image.Resampling.NEAREST);small.save(p);a['compact'][str(size)]=key;a['files'][key]=p.relative_to(R).as_posix()
  if size==68:sequence.append(small)
 out['poses'][pose]=a;thumb=im.resize((256,256),Image.Resampling.NEAREST);review.paste(thumb,(i*256,22),thumb);draw.text((i*256+9,4),pose,fill='#d5f6ff')
sheet=Image.new('RGBA',(272,68))
for i,im in enumerate(sequence):sheet.paste(im,(i*68,0))
sheet.save(D/'poses.png');review.save(S/'framed-review.png');(S/'sources.json').write_text(json.dumps(out,indent=2),encoding='utf8')
(D/'manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8');(R/'assets/chronos_dialogue_art_1102.js').write_text("'use strict';\nconst C113_ART="+json.dumps(out,separators=(',',':'))+';\n',encoding='utf8')
lua="""local D=app.params['out'];local s=Sprite(68,68,ColorMode.RGB);local im=Image{fromFile=D..'/poses.png'}
for i=0,3 do if i>0 then s:newEmptyFrame()end;s:newCel(s.layers[1],i+1,Image(im,Rectangle(i*68,0,68,68)),Point(0,0));s.frames[i+1].duration=0.25 end;s:saveAs(D..'/chronos-dialogue.aseprite');s:close()"""
(D/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+D.as_posix(),'--script',str(D/'author.lua')],check=True)
print('Four approved Chronos views fitted to one bezel; six fixed native UI sizes each; editable Aseprite source.',flush=True)
