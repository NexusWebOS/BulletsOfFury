from pathlib import Path
from PIL import Image,ImageDraw
import json
W=Path(__file__).resolve().parents[1]/'_ART_SOURCES/hammer_furious_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Hammer-Furious-1022';A=json.loads((W/'hammer_furious_art_1022.js').read_text().split('const HF22_ART=')[1].rstrip(';\n'));cache={}
for name in ['blue_jump','corrupt_jump','blue_sides','corrupt_sides','blue_throw','corrupt_throw','blue_rage','corrupt_rage']:
 rows=A['banks'][name];out=[];contact=Image.new('RGB',(448*4,474*((len(rows)+3)//4)),'#14202d');g=ImageDraw.Draw(contact)
 for i,a in enumerate(rows):
  path=W/'shipping'/Path(A['sheets'][a['sheet']]['path']).name
  if path not in cache:cache[path]=Image.open(path).convert('RGBA')
  x,y,w,h=a['cell'];im=cache[path].crop((x,y,x+w,y+h));c=Image.new('RGB',(512,512),'#111b29');c.paste(im,(256-a['pivot'][0],280-a['pivot'][1]),im);out.append(c);contact.paste(im,(i%4*448,i//4*474),im);g.text((i%4*448+6,i//4*474+450),str(i),fill='white')
 out[0].save(W/(name+'.gif'),save_all=True,append_images=out[1:],duration=90,loop=0);contact.thumbnail((1152,1230));contact.save(W/(name+'-contact.png'))
print('Saved fixed-unit motion and contact reviews.')
