from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/prototype_dispatch_1114'
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];samples=[]
def ck(name,ok,data=None):
 checks.append({'name':name,'ok':bool(ok),'data':data})
 if not ok:print('FAIL '+name+' '+str(data),flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?prototype-dispatch-qa=1114');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{window.kitBlits=[];const get=XART.get,draw=ctx.drawImage,seen=new Map();XART.get=function(k){const im=get.apply(this,arguments);seen.set(im,k);return im;};ctx.drawImage=function(im,...args){const key=seen.get(im);if(key)kitBlits.push({key,args});return draw.call(this,im,...args);};}")
 pilots=p.evaluate('CP15_ART.pilots')
 for pk in pilots:
  p.evaluate("pk=>{run.gravityShipReady=false;D1110.preview('post-4',pk);}",pk)
  p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
  rows=p.evaluate('BOFCinematicDirector.current.beats.map((b,i)=>({i,id:b.id,text:b.text,who:b.who,upgrade:b.upgrade,kind:b.kit17,group:b.cm3.group,locations:b.fpLocations}))')
  tech='cole'if pk=='decker'else'decker'
  ck(pk+' found separate pieces and correct technician',"separate pieces"in rows[0]['text']and rows[1]['text'].startswith(tech.title())and rows[2]['who']==tech.upper(),rows[:4])
  ck(pk+' earned upgrade once and new orders line',len([q for q in rows if q.get('upgrade')==4])==1 and next(q for q in rows if q['id']=='POST4-07')['text'].endswith('Awaiting your orders, sir!'))
  idx=next(q['i']for q in rows if q['id']=='POST4-10');states=[]
  for t in [1,3.5]:
   p.evaluate('([i,t])=>{const s=BOFCinematicDirector.current;s.i=i;s.t=t;kitBlits=[];}',[idx,t]);p.evaluate(shoot.STEP,1)
   q=p.evaluate('({last:KD17.last,blits:kitBlits})');states.append(q)
   if t==1:p.locator('#screen').screenshot(path=str(OUT/(pk+'-departure.png')))
  ck(pk+' actual normal aircraft pixels drawn',all(x['last']['planes'][0]['key'].startswith('ship_'+pk)and any(y['key']==x['last']['planes'][0]['key']for y in x['blits'])for x in states),states)
  ck(pk+' no premature conversion or caption',all(x['last']['unconverted']and not x['last']['gravityReady']and not x['last']['dialogueBox']and not any(y['key'].startswith(('c16_ship-','fury_','cm3_caption'))for y in x['blits'])for x in states))
  ck(pk+' steady ship ascends over moving sky',states[0]['last']['planes'][0]['x']==states[1]['last']['planes'][0]['x']and states[0]['last']['planes'][0]['y']>states[1]['last']['planes'][0]['y']and states[0]['last']['scroll']<states[1]['last']['scroll'])
  samples.append({'pilot':pk,'states':states})
 # Full satellite image has no retired miniature, caption bank or dialogue frame.
 p.evaluate("()=>D1110.preview('post-4','cole')");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 idx=p.evaluate("BOFCinematicDirector.current.beats.findIndex(b=>b.id==='B403')")
 p.evaluate('i=>{const s=BOFCinematicDirector.current;s.i=i;s.t=2;kitBlits=[];}',idx);p.evaluate(shoot.STEP,1)
 q=p.evaluate('({last:KD17.last,blits:kitBlits})');p.locator('#screen').screenshot(path=str(OUT/'satellite-full-panel.png'))
 ck('one giant satellite illustration with no dialogue box',q['last']['singlePanel']and not q['last']['dialogueBox']and any(x['key']=='kd17_satellite'for x in q['blits'])and not any('caption'in x['key']or 'art-satellite-takeover'in x['key']for x in q['blits']),q)
 p.evaluate('i=>{const s=BOFCinematicDirector.current;s.i=i+1;s.t=.3;s.shown=2;kitBlits=[];}',idx);p.evaluate(shoot.STEP,1)
 ck('satellite exit does not restore small retired insert',not p.evaluate("kitBlits.some(q=>q.key.includes('art-satellite-takeover'))"))
 p.evaluate("()=>D1110.preview('post-4','decker')");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 p.evaluate("()=>{const s=BOFCinematicDirector.current;s.i=s.beats.findIndex(b=>b.id==='KIT4-04');s.t=1.5;s.shown=s.beats[s.i].text.length;}");p.evaluate(shoot.STEP,1);p.locator('#screen').screenshot(path=str(OUT/'cole-supports-decker.png'))
 # Exercise the real ascent dialogue, retaining all native assembly clocks.
 p.evaluate("()=>{BOFCinematicDirector.cancel();beginStage(5);warmStage(5);}")
 p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready;}',polling=50)
 p.evaluate("()=>{story=null;setState(GS.LAUNCH);drawLaunch._phase=undefined;last=__bofStepNow=performance.now();}")
 for i in range(80):
  e=p.evaluate(shoot.STEP,6)
  if e:errors.append(e);break
  q=p.evaluate('({t:gravityMode?.dialogueT,delay:gravityMode?.dialogueDelay,pilot:CX4.last?.pilot,phase:gravityMode?.phase})')
  if q.get('t',0)>q.get('delay',0)+1:break
 ck('Cole calls flying Decker during native ascent',q.get('pilot')=='cole',q)
 ck('no page console HTTP errors',not errors,errors);b.close()
(OUT/'native-qa.json').write_text(json.dumps({'checks':checks,'samples':samples,'errors':errors},indent=2),encoding='utf-8');print(str(sum(q['ok']for q in checks))+'/'+str(len(checks))+' native checks passed',flush=True)
assert all(q['ok']for q in checks)
