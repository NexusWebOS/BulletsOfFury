from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/crossed_fate_1115';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
errors=[];checks=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:1000],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(180000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?fate-probe');p.wait_for_function('window.__bofFrames>6');p.evaluate(shoot.TRAP_RAF)
 q=p.evaluate("()=>({keys:fate15Keys().filter(k=>!XART._src[XART.root(k)]),pw:PASSWORDS.STRM,base:PASSWORDS.BASE4,defs:FATE15_DEFS.map(d=>({id:d.id,title:d.title,desc:d.desc})),gallery:awardsRows().filter(d=>d.family==='stage6_route')})")
 ck('all requested source keys exist',not q['keys'],q['keys']);ck('STRM targets Stage6 and BASE4 preserves airbase code',q['pw']==6 and q['base']==4);ck('both unique medals are in achievement gallery',len(q['gallery'])==2,q['defs'])
 p.wait_for_function('()=>fate15Warm()',polling=50)
 for diff in ['normal','hard','furious']:
  for route in ['left','right']:
   q=p.evaluate("([d,route])=>{diffKey=d;run.pilot='cole';delete run._stage6FateDefeat;campaign.stage6Fate=null;const o=fate15Current(route),rows=c16Rows('post-6','cole',route);return{o,rows:rows.map(b=>({id:b.id,text:b.text,who:b.who}))};}",[diff,route])
   expect='rebels'if route=='right'else'storm'if diff=='furious'else'harrier'
   ck(diff+' '+route+' resolves actual route boss',q['o']['defeated']==expect,q['o'])
   ck(diff+' '+route+' dialogue removes stopping-orders plot',not any('orders'in v['text'].lower()for v in q['rows'])and any('city'in v['text'].lower()for v in q['rows']),q['rows'][:6])
   ck(diff+' '+route+' finale leaves next destination open',p.evaluate("()=>{const r=c16Rows('post-6').at(-1);return r.kind==='dialogue'&&r.bank===null&&r.location==='sky'&&r.text.includes('choose our next move');}"))
 for defeated in ['storm','rebels','harrier']:
  p.evaluate("k=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='cole';PILOTMOD={...PILOTS.find(p=>p.key==='cole')};pilotIndex=PILOTS.findIndex(p=>p.key==='cole');diffKey='furious';DIFF=difficultyForRun('campaign','furious');campaign.rank={1:'A',2:'A',3:'A',4:'A',5:'A',6:'A'};campaign.unlockedMax=7;const q=fate15Outcome(k);campaign.stage6Fate=fate15Receipt({...q,version:1,id:'native-probe-'+k,verified:false,pilot:'cole',crew:['cole','maverick','freezer','yuri','falva']});campaign.stageX1004={route:q.route,target:q.target,done:false};openStageSelect(7,{unlock:7});}",defeated)
  p.wait_for_function('()=>{map4eWarm();return fury14MapReady();}',polling=50)
  samples=[];seen=set()
  for i in range(500):
   e=p.evaluate(shoot.STEP,6)
   if e:errors.append(e);break
   q=p.evaluate("({state,boot:sselBoot,elapsed:campaign.stage6Fate.elapsed,receipt:campaign.stage6Fate,last:FATE15.last,message:FATE15.lastMessage,award:FATE15.lastAward,cam:cmap2.cam,unlocked:achievementUnlocked(campaign.stage6Fate.award)})")
   t=q['elapsed'];samples.append(q)
   for at,label in [(2.3,'flight'),(6.1,'crash'),(9.9,'message')]:
    if t>=at and label not in seen:seen.add(label);p.locator('#screen').screenshot(path=str(O/(defeated+'-'+label+'.png')))
   if q['receipt']['messageSeen']and q['receipt']['transitSeen']:break
   p.wait_for_timeout(1)
  ck(defeated+' map aftermath completes and unlocks choice',q['receipt']['transitSeen']and q['receipt']['messageSeen'],q)
  ck(defeated+' preview cannot grant a real-clear achievement',not q['unlocked'])
  if defeated=='storm':ck('Storm victory visibly sends Harrier into crash',any(any(s.get('crashing')for s in (x.get('last')or{}).get('ships',[]))for x in samples));ck('Storm route shows requested Hard password message',any((x.get('message')or{}).get('text')==p.evaluate('FATE15_MESSAGES.storm')for x in samples))
  if defeated=='rebels':ck('Rebel victory sends Storm west and leaves Harrier for city',any(any(s.get('kind')=='storm'for s in (x.get('last')or{}).get('ships',[]))for x in samples)and q['receipt']['target']=='harrier')
  data=p.evaluate('Rival24.save()');p.evaluate('Rival24.load',data);after=p.evaluate('campaign.stage6Fate');ck(defeated+' receipt survives save/load',after==q['receipt'])
 ck('no native browser/console/HTTP errors',not errors,errors);b.close()
(O/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' native checks passed',flush=True)
assert all(c['ok']for c in checks)
