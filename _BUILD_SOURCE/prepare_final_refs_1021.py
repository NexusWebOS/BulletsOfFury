from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,ast,base64
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');S=R/'_ART_SOURCES/final_version_1021';O=R/'_shots/final_version_1021';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
cat=json.loads((R/'assets/data/AIR_MOTION_1013.json').read_text())['entries'];rows=[]
for id,d in cat.items():
 if not any(n in [1,4,5,6,7,8,9] for n in d['stages']):continue
 h=d['heading'];p=R/h['path'];im=Image.open(p).convert('RGBA');cell=h['cell'];im=im.crop((0,0,cell,cell));target=S/'refs'/('air-'+id+'.png');im.save(target);rows.append(dict(id=id,name=d['name'],path=str(target),stages=d['stages'],aliases=d['aliases'],size=im.size))
for part in range((len(rows)+29)//30):
 subset=rows[part*30:(part+1)*30];sheet=Image.new('RGB',(1000,((len(subset)+7)//8)*148),'#101720');draw=ImageDraw.Draw(sheet)
 for i,row in enumerate(subset):
  im=Image.open(row['path']);im.thumbnail((120,120),Image.Resampling.NEAREST);x=i%8*125;y=i//8*148;sheet.paste(im,(x+(125-im.width)//2,y),im);draw.text((x+2,y+120),row['id'][:19],fill='white')
 sheet.save(O/f'air-roster-{part}.jpg')
(S/'air-reference-manifest.json').write_text(json.dumps(rows,indent=2))
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  meta=p.evaluate('()=>Object.entries(ENEMY_SHIELD_FAMILY).map(([name,s])=>({name,...s}))');(S/'shield-families.json').write_text(json.dumps(meta,indent=2))
  keys=[*(s['prefix']+'_0' for s in meta if s['kind']=='bubble'),'ship_cole','ship_axel','ship_decker','ship_falva','ship_freezer','ship_juggernaut','ship_lizzie','ship_maverick','ship_yuri','nfx_s5gate96_3','nx_small_3','nes_bubble_0']
  for key in dict.fromkeys(keys):
   p.wait_for_function('k=>XART.rdy(k)',arg=key);uri=p.evaluate('k=>{const i=XART.get(k),c=document.createElement("canvas");c.width=i.width;c.height=i.height;c.getContext("2d").drawImage(i,0,0);return c.toDataURL().split(",")[1]}',key);(S/'refs'/('native-'+key+'.png')).write_bytes(base64.b64decode(uri))
  b.close()
finally:stop()
print('Exported',len(rows),'actual air identities and native shield/ship/effect references')
