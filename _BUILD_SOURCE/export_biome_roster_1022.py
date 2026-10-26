from pathlib import Path
import base64,json
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];D=R/'_ART_SOURCES/biome_roster_1022';O=R/'_shots/biome_roster_1022'
(D/'references').mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
refs={'magma_small':'overhaul_stage2_fire_jet_01','magma_large':'overhaul_stage2_fire_jet_02','sky_small':'overhaul_stage6_storm_drone_01','sky_medium':'overhaul_stage6_storm_drone_01','sky_large':'overhaul_stage6_storm_drone_01','water_small':'overhaul_stage9_water_jet_01','water_medium':'overhaul_stage9_water_drone_01','water_large':'overhaul_stage9_water_alien_01'}
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page();p.set_default_timeout(180000);p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('(keys)=>keys.forEach(k=>XART.rdy(k))',list(refs.values()));p.wait_for_function('(keys)=>keys.every(k=>XART.rdy(k))',arg=list(refs.values()))
  audit=[]
  for name,key in refs.items():
   row=p.evaluate('''key=>{const im=XART.get(key),c=document.createElement('canvas');c.width=c.height=192;const g=c.getContext('2d');g.imageSmoothingEnabled=false;const s=Math.min(164/im.width,164/im.height);g.drawImage(im,96-im.width*s/2,96-im.height*s/2,im.width*s,im.height*s);return {png:c.toDataURL(),source:[im.width,im.height],scale:s}}''',key)
   (D/'references'/(name+'.png')).write_bytes(base64.b64decode(row.pop('png').split(',')[1]));audit.append(dict(name=name,key=key,**row))
  (D/'references/audit.json').write_text(json.dumps(audit,indent=2)+'\n');b.close()
finally:stop()
sheet=Image.new('RGB',(192*4,216*2),'#18212b');d=ImageDraw.Draw(sheet)
for i,name in enumerate(refs):
 im=Image.open(D/'references'/(name+'.png')).convert('RGBA');x=i%4*192;y=i//4*216;sheet.paste(im,(x,y),im);d.text((x+5,y+194),name,fill='white')
sheet.save(O/'references.png');print('Exported eight actual XART roster references')
