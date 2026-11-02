from pathlib import Path
import sys,base64,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve
Q=R/'_shots/stage3_amplify_1031';Q.mkdir(exist_ok=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page()
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000)
  keys=['ndr_sharddart_idle_0','ndr_cryoeye_idle_0','ndr_glaciercarrier_idle_0','nef_s3_elite_ice_interceptor_intact','nst3_master','rzb_sonic_wave','overhaul_ground_base_3',*[f'ndr_glaciercarrier_idle_{i}'for i in range(5)],*[f'ndr_glaciercarrier_attack_{i}'for i in range(9)]]
  p.evaluate('(ks)=>ks.forEach(k=>XART.rdy(k))',keys)
  p.wait_for_function('(ks)=>ks.slice(0,5).every(k=>XART.rdy(k))',arg=keys,timeout=90000)
  for k in keys:
   a=p.evaluate('(k)=>{if(!XART.rdy(k))return null;const a=XART.get(k),c=document.createElement("canvas");c.width=a.naturalWidth||a.width;c.height=a.naturalHeight||a.height;c.getContext("2d").drawImage(a,0,0);return c.toDataURL()}',k)
   if a:(Q/(k+'.png')).write_bytes(base64.b64decode(a.split(',')[1]))
  print(p.evaluate('()=>({stage3:BOFX.img.nst3_master,cells:Object.keys(BOFX.cells).filter(k=>/sonic/.test(k)).slice(0,20),images:Object.keys(BOFX.img).filter(k=>/sonic/.test(k)).slice(0,20)})'))
  b.close()
finally:stop()

