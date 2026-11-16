from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';S=R/'_ART_SOURCES/city_rescue_1115';A=R/'assets/game/shared/cinematics/city_rescue_1115';M=json.loads((S/'manifest.json').read_text(encoding='utf8'))
for direction in ['nw','w']:
 for shadow in [False,True]:
  name='storm_'+direction+('_shadow'if shadow else'');frames=[]
  for f in range(16):
   source=S/('storm-'+direction+('-body'if shadow else'')+'-%02d.png'%f);c=Image.open(source).convert('RGBA')
   if shadow:a=c.getchannel('A').point(lambda v:round(v*.27));c=Image.new('RGBA',c.size);c.putalpha(a)
   frames.append(c)
  bounds=[c.getbbox()for c in frames];l=max(0,min(b[0]for b in bounds)-4)//2*2;t=max(0,min(b[1]for b in bounds)-4)//2*2;r=min(800,math.ceil((max(b[2]for b in bounds)+4)/2)*2);bot=min(800,math.ceil((max(b[3]for b in bounds)+4)/2)*2);crop=[l,t,r,bot];cw=r-l;ch=bot-t
  assert all(c.getbbox()[0]>=4 and c.getbbox()[1]>=4 and c.getbbox()[2]<=796 and c.getbbox()[3]<=796 for c in frames)
  sheet=Image.new('RGBA',(cw*4,ch*4));key='city16_'+name;cells=[]
  for i,c in enumerate(frames):sheet.alpha_composite(c.crop(crop),(i%4*cw,i//4*ch));cells.append([key,i%4*cw,i//4*ch])
  path=A/(name+'.webp');sheet.save(path,lossless=True);M['banks'][name]={'w':cw,'h':ch,'pivot':[400-l,400-t],'sourceCanvas':[800,800],'sharedCrop':crop,'bodyWidth':576,'frames':16,'frameMs':[62,63]*8,'pages':[{'key':key,'path':str(path.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'w':sheet.width,'h':sheet.height}],'cells':cells}
  if not shadow:frames[0].save(O/('storm-'+direction+'.gif'),save_all=True,append_images=frames[1:],duration=[62,63]*8,loop=0,disposal=2)
(S/'manifest.json').write_text(json.dumps(M,indent=2),encoding='utf8',newline='\n');(R/'assets/city_rescue_art_1115.js').write_text('"use strict";\nconst CITY16_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
print('Packed four corrected16-frame flight/shadow banks with fixed800-source pivots; registry updated.',flush=True)
