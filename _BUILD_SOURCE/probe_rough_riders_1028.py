from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,http.server,numpy as np
http.server.ThreadingHTTPServer.request_queue_size=256
R=Path(__file__).resolve().parents[1];W=R/'_shots/rough_riders_1028_probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
checks=[];errors=[];http=[]
def check(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,n
M=json.loads((R/'assets/game/levels/stage_06/boss/rough_riders_1028/manifest.json').read_text())
check('All five aircraft use72 complete fixed192px authored cells',len(M['models'])==5 and all(M['banks'][m['bank']]['frames']==72 and M['banks'][m['bank']]['cw']==192 for m in M['models'].values()))
check('All360 flight cells have clear outer borders and bounded textures',all(max(Image.open(R/M['banks'][m['bank']]['path']).size)<=4096 and all(b and b[0]>0 and b[1]>0 and b[2]<192 and b[3]<192 for b in m['bounds'])for m in M['models'].values()))
check('Complete80-glyph font includes R,5 and common baselines with safety margins',len(M['font']['chars'])==80 and all(M['font']['glyphs'][c]['ink'][1]>0 and M['font']['glyphs'][c]['ink'][1]+M['font']['glyphs'][c]['ink'][3]<32 for c in M['font']['chars'])and M['font']['glyphs']['R']['baseline']==M['font']['glyphs']['5']['baseline'])
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof RR33!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  def setup(d='furious'):
   p.evaluate("d=>{run.ngplus=false;diffKey=d;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;RR33.events=[];}",d);step(1)
  setup();snap=[];phaseFrames={k:set()for k in M['models']};start=p.evaluate('({hp:boss.hp,parts:boss._rebels.ships.map(q=>q.hp),timer:stageTimer,wave:waveIdx,spawn:spawnClock,sky:_stage6SkyScroll})')
  for target,label in [(2,'catch-up'),(3.15,'spool'),(4.5,'away'),(6.6,'airshow'),(8.4,'airshow2'),(10.7,'settle'),(13,'dialogue')]:
   while p.evaluate('boss._rebels.rough33.t')<target:
    step(2);q=p.evaluate('RR33.last')
    for s in q['ships']:
     if s.get('frame')is not None:phaseFrames[s['key']].add(s['frame'])
   p.screenshot(path=str(W/(label+'.png')));snap.append(p.evaluate('()=>({last:RR33.last,hp:boss.hp,name:boss.name,parts:boss._rebels.ships.map(q=>q.hp),targets:retinaBossTargets(boss).length,timer:stageTimer,wave:waveIdx,spawn:spawnClock,sky:_stage6SkyScroll,rows:boss._rebels.h3Intro?.rows})'))
  check('Crew official name is live on the actual boss',all(q['name']=='THE ROUGH RIDERS'for q in snap))
  check('Catch-up aircraft face north in the player flight direction',all(abs(q['heading']+np.pi/2)<.001 and 56<=q['frame']<64 for q in snap[0]['last']['ships']),snap[0]['last'])
  check('All five boost together with animated anchored plume cells',all(64<=q['frame']<72 for q in snap[1]['last']['ships']),snap[1]['last'])
  check('All five fly completely off the north edge before returning',all(q['y']<-150 for q in snap[2]['last']['ships']),snap[2]['last'])
  check('Every pilot actually traverses at least12 distinct true somersault cells',all(len([f for f in fs if 32<=f<48])>=12 for fs in phaseFrames.values()),{k:sorted(fs)for k,fs in phaseFrames.items()})
  check('The intro remains fully protected with unchanged native pilot health',all(q['hp']==start['hp']and q['parts']==start['parts']and q['targets']==0 for q in snap))
  check('No timed wave or stage sequence advances through the new entrance',all(q['timer']==start['timer']and q['wave']==start['wave']and q['spawn']==start['spawn']for q in snap))
  q=snap[-1]['last'];check('Allies accompany the player through the entire entrance',all(s['last']['allies']>0 for s in snap),[s['last']['allies']for s in snap]);check('The five settle in a spread bowling-pin formation',q['ships'][0]['y']>q['ships'][1]['y']>q['ships'][3]['y']and q['ships'][3]['x']<q['ships'][1]['x']<q['ships'][0]['x']<q['ships'][2]['x']<q['ships'][4]['x'],q['ships'])
  check('Dialogue waits until the airshow and begins with the new crew identity',snap[-2]['last']['phase']=='settle'and snap[-1]['last']['phase']=='dialogue'and 'THE ROUGH RIDERS'in snap[-1]['rows'][0]['text'])
  check('Scrolling eases down while preserving nonzero parallax movement',snap[-1]['last']['scroll']==.055 and 0<snap[-2]['last']['scroll']<.9 and all(b['sky']>a['sky']for a,b in zip(snap,snap[1:])))
  q=p.evaluate('''()=>{const b=boss,before=b.hp;for(let i=0;i<5;i++){b._rebels.hit=i;rebelSquadDamage(b,99);}return{before,after:b.hp,hit:rebelSquadHitTest(b,b._rebels.ships[0].x,b._rebels.ships[0].y)}}''');check('Direct hostile and stale targeting cannot hurt a protected stunt pilot',q['before']==q['after']and not q['hit'],q)
  sky=p.evaluate('_stage6SkyScroll');step(60);delta=p.evaluate('_stage6SkyScroll')-sky;check('Actual sky scroll during dialogue is approximately41px per second',20<delta<65,delta)
  p.evaluate('()=>{const I=boss._rebels.h3Intro;I.i=I.rows.length;I.t=0;}');step(2);check('The conversation releases back into the original combat controller',p.evaluate('boss._rebels.frIntro.done&&!boss._noHit&&boss._rebels.ships.every(q=>q.mode==="fight")'))
  step(150);check('Normal sky speed returns smoothly and the native arsenal initializes',p.evaluate('rr33Scroll()===1&&boss._rebels.gang1004&&boss._rebels.ships.every(q=>q.rg4)&&retinaBossTargets(boss).length>0'))
  q=p.evaluate('''()=>{const q=boss._rebels.ships.find(q=>q.key==='rook'),before=q.hp;boss._rebels.hit=q.i;hitBoss(1);return{before,hp:q.hp,flash:q.flash}}''');check('Combat damage and native hit flash remain active after the entrance',q['hp']<q['before']and q['flash']>0,q);p.evaluate('()=>{s6Wing.ships=[];pBullets=[];enemies=[];eBullets=[];}');step(20);check('Native combat flash still expires',p.evaluate('boss._rebels.ships.find(q=>q.key==="rook").flash<=0'))
  for d in ['easy','normal','hard']:
   setup(d);step(760);check(d+' retains the complete protected five-pilot entrance',p.evaluate('boss._rebels.rough33.phase==="dialogue"&&!boss._rebels.frIntro.done&&boss._rebels.ships.every(q=>q.hp>0)'))
  p.evaluate('run._gp4StageX=true');check('Stage X keeps its existing encounter choreography',p.evaluate('!rr33Group(boss)'));p.evaluate('run._gp4StageX=false;run.stage=7');check('Other stages do not change scroll rate',p.evaluate('rr33Scroll()===1'))
  check('No game, draw or HTTP asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(f'{len(checks)} native/art checks passed')
