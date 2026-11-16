from pathlib import Path
import sys,json,hashlib
from playwright.sync_api import sync_playwright
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');O=R/'_shots/hq_return_attack_1114';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[];samples=[]
def ck(n,ok,d=None):
 checks.append({'name':n,'ok':bool(ok),'data':d})
 if not ok:print('FAIL',n,str(d)[:700],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?hq19qa');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 p.evaluate("()=>{diffKey='hard';run.mode='campaign';D1110.preview('post-5','cole');}")
 try:p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 except Exception:
  print('MISSING',p.evaluate('BOFCinematicDirector.current.d1110Keys.filter(k=>!XART.rdy(k))'),errors,flush=True);raise
 rows=p.evaluate('BOFCinematicDirector.current.beats.map((b,i)=>({i,id:b.id,mode:b.hq19,duration:b.duration,text:b.text,upgrade:b.upgrade}))');print('Loaded',len(rows),'HQ beats',flush=True)
 ck('replacement sequence and no old workshop/comic splits',len(rows)==11 and all(x['id'].startswith('HQ19-')for x in rows),rows)
 ck('five-second quiet pause authored once',len([x for x in rows if x['mode']=='quiet'])==1 and next(x for x in rows if x['mode']=='quiet')['duration']==5)
 ck('earned upgrade5 retained exactly once',len([x for x in rows if x.get('upgrade')==5])==1)
 frames={'land':[2,6.2],'exit':[1.7],'enter':[.3,3.0,4.6,6.2],'corridor':[1,4.2],'welcome':[2.8,5.2],'radar':[0.2,1.3,3.2,6.3],'launch':[2.3,5.0,8.7],'quiet':[.2,4.8],'attack':[.8,2.9],'escape-decker':[1.8,3.7],'escape-axel':[.2,3.2]}
 for row in rows:
  for j,t in enumerate(frames[row['mode']]):
   p.evaluate('([i,t])=>{const s=BOFCinematicDirector.current;s.i=i;s.t=t;s.shown=Math.min(s.beats[i].text.length,Math.floor(t*38));d1110Visual(s.beats[i],s);}',[row['i'],t]);q=p.evaluate('HQ19.last');samples.append(q);p.locator('#screen').screenshot(path=str(O/(row['mode']+'-'+str(j)+'.png')))
   ck(row['mode']+' frame '+str(j)+' native solid scene',q.get('solidPanel')and q['mode']==row['mode'])
   if row['mode']=='radar':ck('entire actual crew watches radar '+str(j),len(q['cast'])==9 and {x['pilot']for x in q['cast']}==set(p.evaluate('HQ19_PILOTS'))and all(x['pose']=='back'for x in q['cast']),q)
   if row['mode']=='quiet':ck('no enemies during five-second wait '+str(j),not q['enemies']and not q['ships'],q)
 # All nine selected pilots must really have walk and landing art.
 for pk in p.evaluate('HQ19_PILOTS'):
  p.evaluate("pk=>{run.pilot=pk;pilotIndex=PILOTS.findIndex(p=>p.key===pk);for(const k of hq19Keys(pk))XART.rdy(k);}",pk);p.wait_for_function('pk=>hq19Keys(pk).every(k=>XART.rdy(k))',arg=pk,polling=50)
  for mode,t in [('land',6),('exit',2),('enter',3),('corridor',3),('welcome',3)]:
   q=p.evaluate("([mode,t])=>{const b=hq19Rows(run.pilot).find(b=>b.hq19===mode);d1110Visual(b,{t,shown:0,i:0,id:'native-selected-pilot'});return HQ19.last;}",[mode,t])
   has=any(x and x['pilot']==pk for x in q.get('ships',[])+q.get('actors',[])+q.get('cast',[]));ck(pk+' actual '+mode+' actor/ship',has,q if not has else None)
  p.locator('#screen').screenshot(path=str(O/('welcome-'+pk+'.png')))
 # Current metal frames and portraits remain the final dialogue owner.
 ck('new escape words use exact requested dialogue',rows[-2]['text']=='Dammit! They made it to our base too!'and rows[-1]['text']=='We gotta tell the others!')
 p.evaluate("()=>{diffKey='normal';run.pilot='cole';}");normal=p.evaluate('hq19Rows(run.pilot).map(b=>b.hq19)');ck('Normal keeps its native quiet-completion branch',normal==['land','exit','enter','corridor','welcome'],normal)
 ck('all16 radar frames render distinct native pixels',p.evaluate("()=>{const a=HQ19_ART.banks.radar;return a.frames===16;}")and len(set(q['frame']for q in samples if q['mode']=='radar'))>=3)
 ck('zero page console HTTP errors',not errors,errors);b.close()
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'samples':samples,'errors':errors},indent=2),encoding='utf8');print(sum(x['ok']for x in checks),'/',len(checks),'native checks',flush=True);assert all(x['ok']for x in checks)
