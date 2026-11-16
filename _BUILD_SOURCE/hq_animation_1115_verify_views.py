from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');O=R/'_shots/hq_animation_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?hq19-final-views');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{diffKey='hard';D1110.preview('post-5','cole');}");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 for mode,t in [('radar',3.2),('welcome',3.2),('corridor',3.2),('escape-axel',2.2)]:
  q=p.evaluate("([mode,t])=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.hq19===mode);s.t=t;s.shown=s.beats[s.i].text.length;d1110Visual(s.beats[s.i],s);return HQ19.last;}",[mode,t]);p.locator('#screen').screenshot(path=str(O/('final-'+mode+'.png')));checks.append({'name':mode+' current full single-panel view','ok':q['solidPanel']and p.evaluate('cv.width===912*SS')})
 p.evaluate("()=>{run.pilot='cole';coopOn=true;run2.pilot='decker';p2Index=PILOTS.findIndex(p=>p.key==='decker');for(const k of hq19Keys())XART.rdy(k);}");p.wait_for_function('()=>hq19Keys().every(k=>XART.rdy(k))',polling=50)
 q=p.evaluate("()=>{const b=hq19Rows(run.pilot).find(b=>b.hq19==='welcome');d1110Visual(b,{t:3.2,shown:0,i:0,id:'coop'});return HQ19.last;}");p.locator('#screen').screenshot(path=str(O/'final-coop-welcome.png'));checks.append({'name':'all nine co-op cast members visibly fit in native wide frame','ok':len(q['cast'])==9 and len(set(x['pilot']for x in q['cast']))==9 and p.evaluate('cv.width===912*SS')})
 q=p.evaluate("()=>{const b=hq19Rows(run.pilot).find(b=>b.hq19==='land');d1110Visual(b,{t:6,shown:0,i:0,id:'coop'});return HQ19.last;}");checks.append({'name':'both actual co-op aircraft land','ok':len(q['ships'])==2 and {s['pilot']for s in q['ships']}=={'cole','decker'}});p.locator('#screen').screenshot(path=str(O/'final-coop-landing.png'))
 checks.append({'name':'no final browser errors','ok':not errors,'data':errors});b.close()
(O/'final-view-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');print(sum(c['ok']for c in checks),'/',len(checks),'final scene checks');assert all(c['ok']for c in checks)
