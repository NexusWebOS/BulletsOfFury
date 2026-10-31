from pathlib import Path
import sys,json,http.server,numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_claw_lasers_1030/probe';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert passed,(name,data)
for name in ['projectile','muzzle']:
 im=Image.open(R/'assets/game/levels/stage_08/miniboss/herald_claw_lasers_1030'/f'{name}.png').convert('RGBA');a=np.asarray(im).astype(np.int16);m=a[:,:,3]>64
 ck(name+' has512 fixed64px directional animation cells',im.size==(2048,1024))
 ck(name+' retains white cores and has red chroma instead of blue',np.sum(m&(a[:,:,0]>a[:,:,1]+30)&(a[:,:,0]>a[:,:,2]+20))>1000 and np.sum(m&(a[:,:,2]>a[:,:,0]+30))<10)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=8;stageLoadBegin(8)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});DBGT.god=true;spawnSubBoss('heralddeath');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();story=null;setState(GS.PLAY);subBossActive=true;window.B=subBoss;}");step(150)
  p.evaluate('''()=>{const H=B._hd1003;delete H.er28;delete H._hb25;delete H._hp22;delete H._hd19;H.mode='rest';H.age=-100;H.lanes=[];H.flashes=[];H.target=null;B.x=camLeftX()+viewW()/2;B.y=B.ty=160;B.enter=false;B._noHit=false;B._drawY=B.y;eBullets=[];pBullets=[];HL67.events=[];HL67.flashes=[];B._target17={phase:'recover',t:0,cool:0,serial:0,shots:0,kind:'dark'};player.x=camLeftX()+viewW()/2;player.y=VH-70;window.artCalls=[];window.nativeDraw=ctx.drawImage;ctx.drawImage=function(im,...a){for(const[k,b]of Object.entries(HL67_ART))if(im===XART.get(b.key))artCalls.push({bank:k,a});return nativeDraw.call(this,im,...a);};}''')
  step(25)
  q=p.evaluate('''()=>{const native=combatWarningDraw,fields=[];combatWarningDraw=function(o,a){fields.push(a)};try{target17Draw(B)}finally{combatWarningDraw=native}return{phase:B._target17.phase,fields};}''')
  ck('Both actual claw sockets receive committed pre-fire FOV warnings',q['phase']=='track'and len([v for v in q['fields']if v.get('fieldOnly')])==2,q)
  for _ in range(60):
   step(1)
   if p.evaluate('HL67.events.length>=2'):break
  q=p.evaluate('''()=>({events:HL67.events,rounds:eBullets.filter(q=>q._hl67).map(q=>({x:q.x,y:q.y,vx:q.vx,vy:q.vy,port:q._target17Port,intercept:enemyOrdnanceCanIntercept(q)})),flashes:HL67.flashes.length})''')
  ck('Live targeting releases both claws on the same firing beat',len(q['events'])==2 and {e['port']for e in q['events']}=={'gunL','gunR'}and q['events'][0]['time']==q['events'][1]['time'],q)
  ck('Both lasers remain ordinary unshootable energy',len(q['rounds'])==2 and all(not q['intercept']for q in q['rounds']),q['rounds'])
  step(4);p.evaluate('()=>{artCalls=[];drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/'dual-claw-lasers.png'))
  q=p.evaluate('''()=>{const calls=artCalls;return{calls,expected:HL67.flashes.map(f=>{const p=hd1003Muzzle(B,f.id);return{id:f.id,x:Math.round(p.x-Math.cos(f.angle)*7)-32,y:Math.round(p.y-Math.sin(f.angle)*7)-32}})};}''')
  ck('Actual native renderer blits two red rounds and two larger fixed64px muzzle cells',len([v for v in q['calls']if v['bank']=='projectile'])>=2 and len([v for v in q['calls']if v['bank']=='muzzle'])==2 and all(v['a'][-2:]==[64,64]for v in q['calls']),q)
  muzzle=[v['a'][4:6]for v in q['calls']if v['bank']=='muzzle']
  ck('Each muzzle overlays seven pixels into its own current claw tip',all([e['x'],e['y']]in muzzle for e in q['expected']))
  step(47);e=p.evaluate('HL67.events');pairs={}
  for v in e:pairs.setdefault(v['wave'],[]).append(v['port'])
  ck('Sustained attack keeps paired cadence on every native wave',len(pairs)>=3 and all(set(v)=={'gunL','gunR'}for v in pairs.values()),pairs)
  p.evaluate('''()=>{hd1003Break(B,hd1003Part(B,'gunL'));HL67.events=[];B._target17.phase='recover';B._target17.cool=0;B._hd1003.mode='rest';B._hd1003.age=-100;}''');step(100)
  ck('Destroyed claw loses its flashes and projectiles while the other claw still fires',p.evaluate("HL67.events.length>0&&HL67.events.every(e=>e.port==='gunR')&&eBullets.filter(q=>q._hl67&&!q.dead).every(q=>q._heraldPart1003==='gunR')&&HL67.flashes.every(f=>f.id!=='gunL')"))
  p.evaluate('''()=>{B._target17.phase='recover';B._target17.cool=99;B._hd1003.mode='rest';B._hd1003.age=-100;}''');step(20);ck('Muzzle animation expires after the native firing beat',p.evaluate('HL67.flashes.length===0'))
  p.evaluate('''()=>{B._target17.cool=0;B._hd1003.mode='rest';B._hd1003.age=-100;B._gp4FlashNext=0;markHit(B);markHit(hd1003Part(B,'gunR'));drawWorld(0);}''');p.screenshot(path=str(W/'claw-hit.png'));ck('Real body and claw hit feedback remains active',p.evaluate('B.flash>0&&hd1003Part(B,"gunR").flash>0'));step(24);ck('Real hit feedback expires normally',p.evaluate('B.flash<=0&&hd1003Part(B,"gunR").flash<=0'),p.evaluate('({body:B.flash,part:hd1003Part(B,"gunR").flash,story:!!story,talk:!!fb2Talk,state})'))
  p.evaluate('''()=>{B._target17={phase:'track',kind:'dark',cool:0,t:.5,warm:.9,aim:{x:player.x,y:player.y},target:player,ids:['gunR'],serial:10,waves:0,shot:0,live:.75};B._hd1003.age=2;B._hd1003.mode='rest';}''');step(1);ck('Committed warning is not cancelled by the next native maneuver',p.evaluate('B._target17.phase==="track"&&B._hd1003.mode==="rest"'));step(100);ck('Finished paired attack releases the native flight and spell book',p.evaluate('B._hd1003.mode!=="rest"'))
  p.evaluate('()=>{B.dead=true;drawWorld(0)}');ck('Death cancels all attached laser muzzle flashes',p.evaluate('HL67.flashes.length===0'))
  p.evaluate('()=>{ctx.drawImage=nativeDraw;run.stage=9}');ck('Red laser owner is isolated from other stages',p.evaluate('!hl67Own(B)'))
  ck('No native game, draw or asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(len(checks),'Herald dual red claw laser checks passed')
