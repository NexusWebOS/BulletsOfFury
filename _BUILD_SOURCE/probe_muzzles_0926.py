"""Inspect and verify native weapon flashes and Stage 2/4 hardpoints."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
out=Path('_shots/muzzles_0926');out.mkdir(exist_ok=True,parents=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1100})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  keys=['nsb_inferno_reaver','nsb_olivewarden_intact','s4w_boss_idle','s4w_muzzle_mg_3','s4w_muzzle_orb_3','s4w_muzzle_lightning_3','bpfx_muzzle_kinetic_3','bpfx_muzzle_missile_3','bpfx_muzzle_void_3','s1fx_military_muzzle_3','s1fx_rotary_muzzle_3','ndk_muz_2','nchg_orb_3','nchg_sph_3','fchg_2','mwfx_fireball_charge_3','bfx_magma_m_3','weapon_muzzle_rotary_2','weapon_muzzle_laser_2','weapon_muzzle_missile_2','weapon_muzzle_toxic_2','laser_round_muzzle_3']
  pg.evaluate('keys=>keys.forEach(k=>XART.rdy(k))',keys);pg.wait_for_timeout(2000)
  data=pg.evaluate('''keys=>{const canvas=document.createElement('canvas');canvas.width=960;canvas.height=Math.ceil(keys.length/4)*220;const g=canvas.getContext('2d');g.fillStyle='#171b21';g.fillRect(0,0,canvas.width,canvas.height);g.font='12px monospace';const rows=[];keys.forEach((k,i)=>{const im=XART.get(k),x=(i%4)*240,y=Math.floor(i/4)*220;g.fillStyle='white';g.fillText(k,x+6,y+18);if(!im){rows.push({key:k,missing:true});return;}const w=im.width||im.naturalWidth,h=im.height||im.naturalHeight,s=Math.min(200/w,180/h);g.imageSmoothingEnabled=false;g.drawImage(im,x+120-w*s/2,y+120-h*s/2,w*s,h*s);rows.push({key:k,w,h,naturalWidth:im.naturalWidth||null});});return {png:canvas.toDataURL(),rows,mounts:['magmaward','olivewarden','stormsovereign'].map(k=>({key:k,definition:SHIPBOSS[k]})),music:BOFA.music};}''',keys)
  (out/'catalog.png').write_bytes(base64.b64decode(data.pop('png').split(',')[1]));(out/'catalog.json').write_text(json.dumps(data,indent=2));print(json.dumps({'art':data['rows'],'errors':errors},indent=2))
  for kind in ['magmaward','olivewarden','stormsovereign']:
   data=pg.evaluate('''kind=>{const D=SHIPBOSS[kind],im=XART.get(D.key),c=document.createElement('canvas');c.width=c.height=768;const g=c.getContext('2d');g.fillStyle='#182027';g.fillRect(0,0,768,768);g.imageSmoothingEnabled=false;g.drawImage(im,0,0,768,768);g.font='16px monospace';for(const [slot,p]of Object.entries(D.mounts)){const x=(p[0]+.5)*768,y=(p[1]+.5)*768;g.strokeStyle='#ff30b0';g.beginPath();g.moveTo(x-8,y);g.lineTo(x+8,y);g.moveTo(x,y-8);g.lineTo(x,y+8);g.stroke();g.fillStyle='white';g.fillText(slot,x+10,y-8);}return c.toDataURL();}''',kind)
   (out/(kind+'-mounts.png')).write_bytes(base64.b64decode(data.split(',')[1]))
  br.close()
finally:stop()
assert not errors,errors
