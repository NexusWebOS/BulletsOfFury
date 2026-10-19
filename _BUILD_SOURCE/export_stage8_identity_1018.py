"""Inspect authored donor plates without changing their atlases."""
from pathlib import Path
import ast,base64,json
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage8_identity_1018/refs';O.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1500,height=950));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('typeof V18!=="undefined"&&window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(40)
  keys=['fzt_body_intact','fzt_body_rotor','fzt_arm_flame_intact','fzt_arm_cannon_intact','fzt_head_intact','fzt_head_charged','fmc_furnace','fmc_harrier']
  keys+=p.evaluate('Object.values(HM10_ART).flat().map(a=>a.key)')
  keys+=p.evaluate('HK5_ART.hammer.map(a=>a.key)')
  keys+=p.evaluate('Object.values(F17_ART).flatMap(b=>b.frames||[]).map(a=>a.key)')
  p.wait_for_function('(keys)=>keys.every(k=>XART.rdy(k))',arg=keys)
  meta=p.evaluate('''keys=>{const data={};for(const key of keys){const im=XART.get(key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;c.getContext('2d').drawImage(im,0,0);data[key]={w:c.width,h:c.height,png:c.toDataURL().split(',')[1]};}return {images:data,hm:HM10_ART,hk:HK5_ART.hammer,head:F17_ART,fmc:FMC_ART};}''',keys)
  for k,v in meta.pop('images').items():(O/(k+'.png')).write_bytes(base64.b64decode(v['png']))
  (O/'meta.json').write_text(json.dumps(meta,indent=2));br.close()
finally:stop()
chosen=keys[:8]+[r['key'] for r in meta['hk'][:4]]+[r['key'] for r in meta['hm']['swing_left'][7:12]]
out=Image.new('RGB',(1000,280*((len(chosen)+3)//4)),'#101722');d=ImageDraw.Draw(out)
for i,k in enumerate(chosen):
 im=Image.open(O/(k+'.png')).convert('RGBA');im.thumbnail((240,240),Image.Resampling.NEAREST);x=i%4*250;y=i//4*280;out.paste(im,(x+(250-im.width)//2,y),im);d.text((x+4,y+244),k,fill='white')
out.save(O/'contact.png');print('Exported '+str(len(keys))+' actual donor plates')
