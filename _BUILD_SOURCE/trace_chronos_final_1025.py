"""Native Chromium frame pixels, physical landmarks and complete depth chronology."""
from pathlib import Path
import json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/chronos_final_1025';O.mkdir(exist_ok=True)
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000,polling=100);p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(30)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;bi24Warm();c25Warm();c26Warm();c27Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&bi24Warm()&&ht23Warm()&&c25Warm()&&c26Warm()&&c27Warm()}',timeout=180000,polling=100)
  p.evaluate("""()=>{window.seedMotion=(chrome=true)=>{BOFCinematicDirector.cancel();fb2Intro=fb2Talk=null;HT23.speech.length=0;const b=boss,h=b._hammer;b.enter=b._noHit=b.dead=false;b.hp=b.maxhp=11220;b.x=340;b.y=260;b._drawY=b.y;b.flash=0;b._gp4FlashNext=0;h.balance0922=true;h.state='hammer';h.t=0;h.mode='hammer';h.comboPending=h.phasePending=false;h.hb20Pickup=h.hc11Counter=h.recovery=h.c25Knock=h.c26Return=h.throw=h.whirl=null;h.c27Combo=null;h._hf22Charge=h._hj22Pair=h._hf22StormPair=null;h.hammerDestroyed=false;h._hf22Red=false;h.frArmor=chrome?{hp:8415,max:8415,activated:true,active:true,t:0,flash:0,barrier:0,checkpoints:[]}:null;debugUnlocked=true;DBGT.god=true;player.invuln=0;player.x=320;player.y=430;eBullets=[];pBullets=[];l5Rocks=[];powerups=[];enemies=[];};seedMotion();}""")
  p.wait_for_function('hf22WarmRed(boss)',timeout=90000,polling=100)
  rows=[]
  for state in ['hammer','fr_activation','whirlwind','spin','shield','giant_idle','recover','nova_charge','storm_idle']:
   r=p.evaluate("""s=>{seedMotion();hammerState(boss,s);boss._hammer.t=.7;const events=[],draw=ctx.drawImage;ctx.drawImage=function(im,...args){events.push({key:HA21.tags.get(im),size:[im.width,im.height],args,stack:new Error().stack.split('\\n').slice(1,5)});return draw.call(this,im,...args)};try{hammerBossDraw(boss)}finally{ctx.drawImage=draw}return{s,events}}""",state)
   rows.append(r);p.evaluate('drawWorld(0)');p.screenshot(path=str(O/('before-'+state+'.png')))
  (O/'draw-trace.json').write_text(json.dumps(rows,indent=2));print(json.dumps([{'s':q['s'],'keys':[e.get('key',e['size']) for e in q['events']]}for q in rows]),flush=True)
  br.close()
finally:stop()
