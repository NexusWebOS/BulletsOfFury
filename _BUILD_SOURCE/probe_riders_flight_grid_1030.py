from pathlib import Path
import sys,json,http.server,math
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/riders_flight_grid_1030/probe';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
O=R/'assets/game/levels/stage_06/boss/riders_flight_grid_1030';m=json.loads((O/'manifest.json').read_text());im=Image.open(O/'gold_grid.png').convert('RGBA');boxes=[]
for f in range(40):
 a=im.crop((f%8*480,f//8*64,f%8*480+480,f//8*64+64));boxes.append(a.getbbox())
ck('40 fixed even authored shield cells with transparent safety margins',im.size==(3840,320)and all(b and b[0]>0 and b[1]>0 and b[2]<480 and b[3]<64 for b in boxes))
a=im.crop((0,128,480,192));ck('Active shield is a filled membrane across its full rectangular grid',all(a.getpixel((x,y))[3]>=170 for x in range(12,468,13)for y in range(12,52,7)))
ck('Editable Aseprite source retained with source recipe',(R/'_ART_SOURCES/riders_flight_grid_1030/gold_grid.aseprite').exists())
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text)if e.type=='error'or'draw error'in e.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof RR65!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{run.ngplus=false;diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;}");step(710)
  ck('Original protected barrel-roll intro still runs',p.evaluate('boss._rebels.rough33.phase==="dialogue"&&!boss._rebels.frIntro.done&&boss._rebels.ships.length===5'))
  p.evaluate('()=>{const I=boss._rebels.h3Intro;I.i=I.rows.length;I.t=0;}');step(2)
  p.evaluate('''()=>{window.R=boss._rebels;window.G=rg4Init(boss);G.rescueDone=true;G.releaseAt=Infinity;G.rd21.next=Infinity;s6WingArsenal=()=>{};pBullets=[];for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.rfHeading=Math.PI/2;q._rd21Scale=1;const h=rr65Home(q);q.x=h.x;q.y=h.y;q._rr65Position={...h};delete q._rr65Nav;}window.flyQA={steps:[],overlap:[],frames:{},phases:[],hp:boss.hp};window.__qaTick=()=>{pBullets=[];for(const q of R.ships){if(q._rr34Frame!=null)(flyQA.frames[q.key]??=[]).push(q._rr34Frame);}const ss=R.ships.filter(q=>rd21Live(q)&&!vs41Safe(q));for(let i=0;i<ss.length;i++)for(let j=i+1;j<ss.length;j++){const a=ss[i],b=ss[j],A=rr45Bounds(a),B=rr45Bounds(b),dx=A.w+B.w+7-Math.abs(a.x-b.x),dy=A.h+B.h+9-Math.abs(a.y-b.y);if(dx>.3&&dy>.3)flyQA.overlap.push({pair:[a.key,b.key],d:Math.min(dx,dy),phase:G.rd21.fleet?.phase});}};}''')
  ck('Native grid asset is warmed before the shield can deploy',p.evaluate('XART.rdy(RR65_GRID.key)'))
  for index,name in enumerate(['star','bowling','H','X']):
   p.evaluate('i=>{G.rd21.cycle=i;rd21FleetStart(boss,G,G.rd21);flyQA.overlap=[];flyQA.frames={};}',index)
   phases=set();elapsed=0
   while p.evaluate('!!G.rd21.fleet')and elapsed<22:
    step(12);elapsed+=.2;phases.add(p.evaluate('G.rd21.fleet?.phase'))
   state=p.evaluate('()=>({fleet:G.rd21.fleet&&{phase:G.rd21.fleet.phase,t:G.rd21.fleet.t,pins:[...G.rd21.fleet._rr65Pins].map(([q,p])=>({key:q.key,...p}))},ships:R.ships.map(q=>({key:q.key,x:q.x,y:q.y,nav:q._rr65Nav,B:rr45Bounds(q)}))})');(W/('formation-'+name+'-state.json')).write_text(json.dumps(state,indent=2))
   ck(name+' formation completes arrival, warned volley and barrel roll',not p.evaluate('!!G.rd21.fleet')and {'assemble','tell','volley','stunt'}.issubset(phases),dict(seconds=elapsed,phases=list(phases)))
   ck(name+' fighter hull reservations remain separated',p.evaluate('flyQA.overlap.length===0'),p.evaluate('flyQA.overlap.slice(0,5)'))
   ck(name+' keeps actual authored barrel-roll cells for all five pilots',p.evaluate('R.ships.every(q=>flyQA.frames[q.key]?.some(f=>f>=72&&f<88))'))
   p.screenshot(path=str(W/f'formation-{name}.png'));p.evaluate('G.rd21.next=Infinity;G.releaseAt=Infinity')
  ck('Formation navigation does not write the native health pool',p.evaluate('boss.hp===flyQA.hp'))
  ck('Original Gasline remains the scoped squad music',p.evaluate('BOFA.music.roughriders6.endsWith("/stage_x/audio/music/LevelX.mp3")&&Snd.cur===Snd.music.roughriders6'))
  p.evaluate('()=>{G.rescueDone=false;G.rr26=rr26State(G);G.rr26.wall=null;rg4RescueStart(boss,G);G.rr26.wall.t=4;}');step(1)
  ck('Decker still owns the native Golden Aegis cast and duration',p.evaluate('G.rr26.wall?._rr45&&G.rr26.wall.caster.key==="decker"&&G.rr26.wall.dur===13.52'))
  p.evaluate('()=>{eBullets=[];pBullets=[];G.ord=[];G.rr26.radio=null;G.rr26.queue=[];atomFlash=0;drawWorld(0);}');p.screenshot(path=str(W/'solid-grid-in-game.png'))
  q=p.evaluate('''()=>{const W=G.rr26.wall,r=rr26WallRect();const a={x:r.x+150,y:r.y-6,vx:0,vy:3,w:8,h:12,kind:'s6tracer',t:0,_noArsenal:true};eBullets.push(a);const shot={x:r.x+160,y:r.y+r.h+4,vx:0,vy:-10,w:8,h:12,kind:'mg',dmg:1};pBullets.push(shot);rr26WallContact(G,1/60);return{enemy:a.dead,friendly:shot.dead||false,returns:G.rr26.returns.length};}''')
  ck('Solid grid retains hostile reflection and friendly pass-through',q['enemy']and not q['friendly']and q['returns']>0,q)
  p.evaluate('run._gp4StageX=true');ck('Stage X is outside this motion/grid override',p.evaluate('!rr45Scope()'));p.evaluate('run._gp4StageX=false;run.stage=7');ck('Other stages are outside this motion/grid override',p.evaluate('!rr45Scope()'))
  ck('No real game, draw, console or missing-asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(f'{len(checks)} authored-art/native checks passed')
