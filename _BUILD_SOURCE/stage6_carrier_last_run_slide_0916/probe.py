"""Real Chromium proof for the Stage-6 Carrier Last Run continuous traverse."""
from pathlib import Path
import base64,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage6_carrier_last_run_slide_0916';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
checks=[];errors=[]
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
  fight=page.evaluate("()=>window.__fight(6,'boss','yuri')");ok(fight.get('ok'),'native Stage-6 boss route opens in Chromium')
  setup=page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=6;curStage=STAGES[5];const W=worldWidth();camX=(W-VW)*.5;player.x=W*.5;player.y=440;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=W*.5;boss.y=146;boss._drawY=146;boss.ty=146;boss.fireCd=999;bossActive=true;carrierInit(boss);carrierMegaInit(boss);boss._mega.phase=5;boss._mega.step=0;boss._mega.cd=99;boss._mega.t=0;boss.hp=boss.maxhp*.20;boss._lc.playing=false;boss._cn=null;boss._mega.nodes.forEach(n=>n.dead=true);return{name:boss.name,hull:SHIPBOSS.doomsdaycarriermk2.key,world:W,center:W*.5,amp:Math.max(60,W*.5-Math.max(150,boss.w*.5)),cd:boss._mega.cd};}""")
  ok(setup['name']=='DOOMSDAY CARRIER MK II' and setup['amp']>=60,'live Carrier enters its sixth Last Run phase')
  ready=False
  for _ in range(240):
    ready=page.evaluate("k=>XART.rdy(k)",setup['hull'])
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Carrier hull decodes before capture')
  def advance(dt,mode='cooldown'):
    return page.evaluate("""q=>{boss._lc.playing=q.mode==='beam';boss._cn=q.mode==='cannon'?{playing:true}:null;const before={x:boss.x,t:boss._mega.t,cd:boss._mega.cd};carrierMegaTick(boss,q.dt);return{before:before,x:boss.x,t:boss._mega.t,cd:boss._mega.cd,phase:boss._mega.phase,expected:worldWidth()*.5+Math.sin(boss._mega.t*.85)*Math.max(60,worldWidth()*.5-Math.max(150,boss.w*.5))};}""",{'dt':dt,'mode':mode})
  def snap(name):
    page.evaluate('()=>{shake=0;drawWorld(0)}');raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p
  a=advance(.45);p1=snap('carrier_last_run_01_slide')
  b=advance(.45,'beam');p2=snap('carrier_last_run_02_beam_slide')
  c=advance(.45,'cannon');p3=snap('carrier_last_run_03_cannon_slide')
  d=advance(1.25);p4=snap('carrier_last_run_04_return_slide')
  ok(abs(a['x']-a['expected'])<.001 and abs(a['x']-a['before']['x'])>1,'Carrier moves during an ordinary cooldown frame')
  ok(abs(b['x']-b['expected'])<.001 and abs(b['x']-b['before']['x'])>1 and b['cd']==b['before']['cd'],'Carrier keeps moving while the beam controller owns the frame')
  ok(abs(c['x']-c['expected'])<.001 and abs(c['x']-c['before']['x'])>1 and c['cd']==c['before']['cd'],'Carrier keeps moving while the cannon controller owns the frame')
  ok(abs(d['x']-d['expected'])<.001 and setup['center']-setup['amp']-.01<=d['x']<=setup['center']+setup['amp']+.01,'traverse remains smooth and bounded on its return')
  shots=[p1,p2,p3,p4]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'cooldown':a,'beam':b,'cannon':c,'return':d,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
sys.exit(0 if passed==len(checks) else 1)
