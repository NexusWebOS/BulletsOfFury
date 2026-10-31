"""Native Chromium ART proof for separate destructible corridor art layers."""
from pathlib import Path
import json,sys,http.server
http.server.ThreadingHTTPServer.request_queue_size=128
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/bastion17_environment';OUT.mkdir(parents=True,exist_ok=True)
errors=[];checks=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1000,'height':700})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=env17-art-qa',timeout=90000,wait_until='domcontentloaded')
  p.wait_for_function('window.TDGAME&&TDGAME.G.state==="boot"',timeout=90000)
  p.evaluate('TDGAME.freeze()')
  if not p.evaluate('!!window.TD_BASTION17_ENV_ART'):
   p.add_script_tag(url=f'http://127.0.0.1:{port}/expansion/topdown/art/bastion17_environment/manifest.js')
   p.evaluate('Object.assign(TD_ASSAULT_ART.assets,TD_BASTION17_ENV_ART.assets);Object.assign(TD_ASSAULT_ART.sequences,TD_BASTION17_ENV_ART.sequences)')
  p.evaluate('ART.warm(Object.keys(TD_BASTION17_ENV_ART.assets))')
  p.wait_for_function('Object.keys(TD_BASTION17_ENV_ART.assets).every(k=>ART.get(k))',timeout=90000)
  checks=p.evaluate('''()=>Object.entries(TD_BASTION17_ENV_ART.assets).map(([key,m])=>{const q=ART.get(key),c=document.createElement('canvas');c.width=m.size[0];c.height=m.size[1];const x=c.getContext('2d');x.imageSmoothingEnabled=false;TD.AssaultArt.draw(x,key,m.anchor[0],m.anchor[1]);const a=x.getImageData(0,0,c.width,c.height).data;let pixels=0,partial=0;for(let i=3;i<a.length;i+=4){pixels+=a[i]>0;partial+=a[i]>0&&a[i]<255;}return{key,passed:!!q&&q.sw===m.size[0]&&q.sh===m.size[1]&&m.size.every(v=>v%2===0)&&pixels>0&&partial===0,pixels,partialAlpha:partial}})''')
  for key in p.evaluate('Object.keys(TD_BASTION17_ENV_ART.assets)'):
   p.evaluate('''key=>{let c=document.getElementById('asset17-review');if(!c){c=document.createElement('canvas');c.id='asset17-review';document.body.append(c);}c.width=640;c.height=480;c.style.cssText='position:fixed;left:0;top:0;width:640px;height:480px;z-index:999999';const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#101a25';x.fillRect(0,0,640,480);if(key.startsWith('pb17_backwall'))TD.AssaultArt.draw(x,'pb17_stage_0',320,240);TD.AssaultArt.draw(x,key,320,240,{s:1});}''',key)
   p.locator('#asset17-review').screenshot(path=str(OUT/(key+'_native.png')))
  # Contract: the final wall is transparent through the previous wall's upper
  # center and centralpersondoor is open even in the intact frame.
  extra=p.evaluate('''()=>{const c=document.createElement('canvas');c.width=640;c.height=480;const x=c.getContext('2d');TD.AssaultArt.draw(x,'pb17_backwall_5',320,240);const open=x.getImageData(210,100,220,110).data;let covered=0;for(let i=3;i<open.length;i+=4)covered+=open[i]>0;x.clearRect(0,0,640,480);TD.AssaultArt.draw(x,'pb17_backwall_0',320,240);return{finalCenterClear:covered===0,troopDoorAlpha:x.getImageData(320,245,1,1).data[3]}}''')
  checks.append({'key':'complete wall breach leaves transparent upper center','passed':extra['finalCenterClear']})
  checks.append({'key':'intact wall has open troop passage','passed':extra['troopDoorAlpha']==0})
  b.close()
finally:stop()
report={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'browserErrors':errors}
(OUT/'native_art_qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'browserErrors':errors}))
sys.exit(1 if report['failed'] or errors else 0)
