from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/cockpit_talk_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(120000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?cockpit-radio-qa=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{run.pilot='cole';run.mode='campaign';beginStage(2);warmStage(2);}")
 p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(2).ready;}',polling=50)
 p.wait_for_function('()=>{const keys=[...Object.values(CP15_ART.minis).map(a=>a.key),...Object.values(CX4_ART.banks).filter(a=>a.key.includes("frame-")).map(a=>a.key)];let ready=true;for(const k of keys)if(!XART.rdy(k))ready=false;return ready;}',polling=50)
 p.evaluate("()=>D1110.preview('post-6','cole')")
 p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 for pk in p.evaluate('CP15_ART.pilots'):
  for room in ['cockpit-sky','cockpit-space','cockpit-tunnel']:
   q=p.evaluate("""([pk,room])=>{
    const get=XART.get,draw=ctx.drawImage,used=new Map(),trace=[];
    XART.get=function(key){const im=get.apply(this,arguments);if(key.startsWith('cp15_'))used.set(im,key);return im;};
    ctx.drawImage=function(im,...args){if(used.has(im))trace.push({key:used.get(im),args});return draw.call(this,im,...args);};
    try{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#081422';ctx.fillRect(0,0,912,512);
     dlgBox({who:pk.toUpperCase(),portrait:pk,location:room,full:'Flight systems restored. Fury Division, report in.',shown:'Flight systems restored.',forceShown:true,cinematic:true,pw:872,ph:172,x:20,y:310,screenSpace:false});
     return {trace,window:CX4.last};
    }finally{ctx.restore();ctx.drawImage=draw;XART.get=get;}
   }""",[pk,room])
   ok=any(x['key'].startswith('cp15_'+pk+'_') for x in q['trace'])
   checks.append({'name':pk+' '+room+' actual radio blit','ok':ok,'data':q})
   if pk=='cole' and room=='cockpit-space':p.locator('#screen').screenshot(path=str(OUT/'cole-small-radio.png'))
 b.close()
checks.append({'name':'no browser or asset errors','ok':not errors,'data':errors})
(OUT/'radio-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'scope':'Native dialogue-window renderer checkpoints, not campaign scenes.'},indent=2),encoding='utf-8')
print(str(sum(q['ok']for q in checks))+'/'+str(len(checks))+' actual radio pixel-source checks passed')
assert all(q['ok']for q in checks)
