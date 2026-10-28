from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
R=Path(__file__).resolve().parents[1];W=R/'_shots/harrier_destruction_1027';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
checks=[];errors=[]
def check(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));assert v,n
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof HD29!=="undefined"');p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];}")
  p.evaluate(STEP,220);p.evaluate('()=>{for(const q of boss._carrier17.parts){q.hp=0;q.dead=true;}bossDie();if(boss._carrier17&&boss._hc32?.exposed){boss._carrier17.direct="hull";hitBoss(boss._hc32.core+1);}HD29.events=[];}')
  for target in [1,3.7,3.95,4.5,5.3]:
   while p.evaluate('boss._whv.t')<target:p.evaluate(STEP,1)
   q=p.evaluate('''()=>{const old=ctx.drawImage,im=XART.get('whv_open_w'),alpha=[];ctx.drawImage=function(pic,...a){if(a.length>=4&&a[a.length-2]>300&&a[a.length-1]>150)alpha.push(this.globalAlpha);return old.call(this,pic,...a)};try{whvDrawCarrier(boss)}finally{ctx.drawImage=old}return{t:boss._whv.t,last:HD29.last,alpha,events:HD29.events.length,rings:boss._hd29.ring,mode:boss._whv.mode,ace:!!boss._whv.ace};}''')
   if target<3.9:check(f'Wreck stays opaque at {target}s',q['last']['hull']and q['alpha']and all(x==1 for x in q['alpha']),q)
   else:check(f'Carrier is consumed by detonation instead of fading at {target}s',not q['last']['hull'],q)
   if target<5.4:p.screenshot(path=str(W/f'destruction-{target}.png'))
  p.evaluate(STEP,300)
  q=p.evaluate('()=>({events:HD29.events,mode:boss._whv.mode,ace:boss._whv.ace._nw28.mode,max:boss.maxhp,dead:boss.dead,scriptEvents:HD29.events.length})')
  main=[e for e in q['events']if e['event']=='hull-detonation'];spread=[e for e in q['events']if e['event']=='spread-blast'];rings=[e for e in q['events']if e['event']=='smoke-ring']
  check('Exactly one hull-sized covering detonation',len(main)==1 and main[0]['size']>=main[0]['width'],main)
  check('Explosions spread across both wings and outside the wreck',len(spread)>=25 and max(e['x']for e in spread)-min(e['x']for e in spread)>main[0]['width']*.85)
  check('Three large smoke rings emit exactly once',len(rings)==3,rings)
  check('Native Nightwing entrance, life and encounter continue',q['mode']=='ace'and q['ace']=='fight'and q['max']>0 and not q['dead'])
  p.evaluate(STEP,100);check('Destruction stops emitting after its finite sequence',p.evaluate('HD29.events.length')==q['scriptEvents'])
  check('No game/draw errors',not errors,errors);b.close()
finally:stop()
print(f'{len(checks)} native checks passed')
