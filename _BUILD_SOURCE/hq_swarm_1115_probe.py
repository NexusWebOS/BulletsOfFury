from pathlib import Path
import sys,json,hashlib
from playwright.sync_api import sync_playwright
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/hq_swarm_1115';sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:900],flush=True)
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(90000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/index.html?hq22probe');p.wait_for_function('window.__bofFrames>5');p.evaluate(shoot.TRAP_RAF);p.evaluate("()=>{diffKey='hard';run.mode='campaign';D1110.preview('post-5','cole');}")
 try:p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 except Exception:
  print('MISSING',p.evaluate('BOFCinematicDirector.current.d1110Keys.filter(k=>!XART.rdy(k))'));raise
 rows=p.evaluate('BOFCinematicDirector.current.beats.map(b=>({id:b.id,mode:b.hq19,duration:b.duration,text:b.text}))');ck('full12-beat HQ story with swarm realization',len(rows)==12 and {'defend','swarm','escape'}.issubset({r['mode']for r in rows}),rows)
 ck('every departure now.75s with.9s spacing',p.evaluate('HQ22.flight===.75&&HQ22.spacing===.9&&HQ22.launch===7.5'))
 ck('rapid ten-hit counterattack ends by3.9s',p.evaluate('HQ20_KILLS.length===10&&HQ20_KILLS.at(-1).at<3.91&&new Set(HQ20_KILLS.map(k=>k.pilot)).size===2'))
 ck('guards warn the team before and during escape',any('warn the others'in r['text']for r in rows)and any('warn the team'in r['text']for r in rows))
 for mode,t,label in [('launch',1.45,'fast-launch'),('attack',.9,'stealth-missiles'),('defend',1.61,'first-hit-flash'),('defend',2.7,'rapid-counterattack'),('swarm',1.0,'overwhelming-swarm'),('escape',.28,'decker-somersault'),('escape',.90,'decker-boost'),('escape',1.25,'axel-somersault'),('escape',1.8,'axel-boost')]:
  q=p.evaluate("([mode,t])=>{const b=hq19Rows(run.pilot).find(b=>b.hq19===mode);d1110Visual(b,{t,shown:999,i:0,id:'native-swarm'});return HQ19.last;}",[mode,t]);p.locator('#screen').screenshot(path=str(OUT/(label+'.png')))
  ck(label+' native scene drawn',q['mode']==mode and q['solidPanel'])
  if mode=='attack':ck('actual stealth fighters launch visible native missiles',any(e['role'].startswith('stealth_')for e in q['enemies'])and len(q['missiles'])>0,q['missiles'])
  if mode=='swarm':ck('ten destroyed attackers replaced by a larger swarm',len(q['kills'])==10 and len(q['enemies'])>=18,{'kills':len(q['kills']),'enemies':len(q['enemies']),'missiles':len(q['missiles'])})
  if label.endswith('somersault'):ck(label+' uses actual pitch-frame bank',any(s.get('motion')=='somersault'and s['pilot']==label.split('-')[0]for s in q['ships']),q['ships'])
  if label.endswith('boost'):ck(label+' boosts after its somersault',any(s.get('motion')=='boost'and s['pilot']==label.split('-')[0]for s in q['ships']),q['ships'])
 for pk in ['decker','axel']:
  frames=[]
  for f in range(8):
   q=p.evaluate("([pk,f])=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,912,512);const t=HQ22.flipStart[pk]+(f+.05)/8*HQ22.flipDuration;return hq22Flip(pk,t,456,300,104);}",[pk,f]);frames.append(q['flipFrame'])
  ck(pk+' all8 pitch frames selected in order',frames==list(range(8)),frames)
 # Run the entire native HQ sequence without skipping or advancing dialogue.
 p.evaluate("()=>{D1110.preview('post-5','cole');D1110.events=[];window.soundsBefore22=CA15.requests;}");p.wait_for_function('()=>d1110Ready(BOFCinematicDirector.current.d1110Keys)',polling=50)
 order=[];modes=[];flips=set();kills=set();shooters=set();quiet=[];maxFlights=0;delay=None;quietAt=None;firstEnemy=None;maxEnemies=0;missiles=0
 for i in range(1000):
  e=p.evaluate(shoot.STEP,6)
  if e:errors.append(e);break
  q=p.evaluate('({state,age:BOFCinematicDirector.current?.age,last:HQ19.last})');a=q.get('last')or{};mode=a.get('mode')
  if not modes or modes[-1]!=mode:modes.append(mode)
  flights=[s for s in a.get('ships',[])if s.get('side')];maxFlights=max(maxFlights,len(flights))
  for s in flights:
   if s['pilot']not in [x['pilot']for x in order]:order.append(s)
  flips.update(s['pilot']for s in a.get('ships',[])if s.get('motion')=='somersault');kills.update(k['id']for k in a.get('kills',[]));shooters.update(s['pilot']for s in a.get('friendlyShots',[]));maxEnemies=max(maxEnemies,len(a.get('enemies',[])));missiles=max(missiles,len(a.get('missiles',[])))
  if mode=='quiet':
   quiet.append(not a['ships']and not a['enemies'])
   if quietAt is None:quietAt=q['age']-a['time']
  if mode=='attack'and firstEnemy is None and a['enemies']:firstEnemy=q['age']
  if q['state']=='title':break
 ck('all native story beats complete once',len(modes)==12 and modes[-1]=='escape',modes)
 ck('all9 leave individually in alternating directions',len(order)==9 and maxFlights==1 and all(s['side']==('southwest'if i%2==0 else'southeast')for i,s in enumerate(order)),[{'pilot':s['pilot'],'side':s['side'],'duration':s['duration']}for s in order])
 ck('both guards shoot, perform somersaults and defeat ten attackers',flips==shooters=={'decker','axel'}and len(kills)==10,{'flips':list(flips),'shooters':list(shooters),'kills':list(kills)})
 ck('five-second empty-base pause remains',quiet and all(quiet)and firstEnemy-quietAt>=4.99,{'delay':firstEnemy-quietAt})
 ck('fast reinforcements and missile volleys visibly swarm the base',maxEnemies>=22 and missiles>=4,{'maxEnemies':maxEnemies,'missilePeak':missiles})
 cues=p.evaluate("D1110.events.filter(e=>e.kind==='cue').map(e=>({name:e.name,shot:e.shot,at:e.at}))");ck('native somersault/boost/missile cues dispatched',sum(c['name']=='somersault'for c in cues)==2 and sum(c['name']=='enemyMissile'for c in cues)>=8 and sum(c['name']=='jetDash'for c in cues)>=11,cues)
 p.evaluate("async()=>{Audio.stopMusic();const c=Snd._audioCtx();await c.resume();window.anal22=c.createAnalyser();anal22.fftSize=2048;aq112Bus().output.connect(anal22);}");p.wait_for_timeout(1000)
 for key in ['somersault','enemyMissile','jetDash']:
  a=p.evaluate("async key=>{Snd.play(key);const b=new Float32Array(2048);let peak=0;for(let i=0;i<25;i++){await new Promise(r=>setTimeout(r,20));anal22.getFloatTimeDomainData(b);for(const v of b)peak=Math.max(peak,Math.abs(v));}return{key,peak};}",key);ck(key+' decoded through native audio bus',a['peak']>.001,a)
 ck('no browser/console/HTTP errors',not errors,errors);b.close()
(OUT/'native-qa.json').write_text(json.dumps({'checks':checks,'errors':errors,'rows':rows},indent=2),encoding='utf8');print(sum(c['ok']for c in checks),'/',len(checks),'native swarm checks',flush=True);assert all(c['ok']for c in checks)

