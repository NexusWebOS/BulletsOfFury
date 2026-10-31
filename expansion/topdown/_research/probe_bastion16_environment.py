"""Verify the authored environment pack through the actual Chromium ART cache."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/bastion16_environment';OUT.mkdir(parents=True,exist_ok=True)
errors=[];checks=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport={'width':1100,'height':700})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=env-art-qa',timeout=90000)
  p.wait_for_function('window.TDGAME&&window.TD_BASTION16_ENV_ART&&TDGAME.G.state==="boot"',timeout=90000)
  p.evaluate('TDGAME.freeze(); ART.warm(Object.keys(TD_BASTION16_ENV_ART.assets))')
  p.wait_for_function('Object.keys(TD_BASTION16_ENV_ART.assets).every(k=>ART.get(k))',timeout=90000)
  checks=p.evaluate('''()=>Object.entries(TD_BASTION16_ENV_ART.assets).map(([key,m])=>{const q=ART.get(key);const c=document.createElement('canvas');c.width=m.size[0];c.height=m.size[1];const x=c.getContext('2d');x.imageSmoothingEnabled=false;TD.AssaultArt.draw(x,key,m.anchor[0],m.anchor[1]);const a=x.getImageData(0,0,c.width,c.height).data;let pixels=0,partial=0;for(let i=3;i<a.length;i+=4){pixels+=a[i]>0;partial+=a[i]>0&&a[i]<255;}return{key,passed:!!q&&q.sw===m.size[0]&&q.sh===m.size[1]&&m.size.every(v=>v%2===0)&&pixels>0&&partial===0,pixels,partialAlpha:partial}})''')
  for name in p.evaluate('Object.keys(TD_BASTION16_ENV_ART.sequences)'):
   p.evaluate('''name=>{const pack=TD_BASTION16_ENV_ART,keys=pack.sequences[name].frames;let c=document.getElementById('asset-review');if(!c){c=document.createElement('canvas');c.id='asset-review';document.body.append(c);}c.width=1024;c.height=280;c.style.cssText='position:fixed;left:0;top:0;width:1024px;height:280px;z-index:999999';const x=c.getContext('2d');x.imageSmoothingEnabled=false;x.fillStyle='#101a25';x.fillRect(0,0,c.width,c.height);keys.forEach((key,i)=>{const m=pack.assets[key];x.fillStyle='#fff';x.font='12px monospace';x.fillText(key,i*256+4,15);TD.AssaultArt.draw(x,key,i*256+128,24+(256-m.size[1])/2+m.anchor[1],{s:m.drawScale});});}''',name)
   p.locator('#asset-review').screenshot(path=str(OUT/(name+'_native.png')))
  b.close()
finally:stop()
report={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'browserErrors':errors}
(OUT/'native_art_qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'browserErrors':errors}))
sys.exit(1 if report['failed'] or errors else 0)
