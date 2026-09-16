"""Real Chromium proof for the Stage-7 DUAL SCOOP DREDGER minefield warning."""
from pathlib import Path
import base64,http.server,json,math,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage7_dredger_mine_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
checks=[];errors=[]
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
  fight=page.evaluate("()=>window.__fight(7,'mini','yuri')");ok(fight.get('ok'),'native Stage-7 miniboss route opens in Chromium')
  warning_keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]
  setup=page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=7;curStage=STAGES[6];const W=worldWidth();camX=(W-VW)*.5;player.x=W*.75;player.y=420;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;subBoss=null;subBossActive=false;spawnSubBoss('dualscoopdredger');subBoss.enter=false;subBoss.x=W*.5;subBoss.y=138;subBoss._drawY=138;subBoss.ty=138;subBoss.hp=subBoss.maxhp*.2;subBoss.fireCd=999;subBossActive=true;subBoss._combatWarnings={};s7DredgerAttack(subBoss,4);window.__dredgerGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__dredgerGets.push(k);return g(k)};const M=subBoss._s7DredgerMine;return{name:subBoss.name,hull:SHIPBOSS.dualscoopdredger.key,gap:M.gap,warn:M.warn,cols:M.cols,world:W,camera:camX,center:W*.5,playerX:player.x};}""")
  keys=warning_keys+[setup['hull']]
  ok(setup['name']=='DUAL SCOOP DREDGER' and setup['warn']==.86 and setup['cols']==6,'live Dredger commits one of six lanes for a 0.86-second warning')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Dredger and green/yellow/red warning art decode before capture')
  def set_time(t,x=None):page.evaluate("q=>{player.x=q.x;const M=subBoss._s7DredgerMine;M.t=q.t;s7DredgerMineTick(subBoss,0);subBoss.flash=0;}",{'t':t,'x':setup['playerX'] if x is None else x})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__dredgerGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const M=subBoss._s7DredgerMine,B=subBoss._combatWarnings['stage7-dredger-minefield'];return{gap:M&&M.gap,released:M&&M.released,warning:B&&{t:B.t,warm:B.warm,released:B.released},shots:eBullets.filter(q=>q._s7warden==='mine').map(q=>({kind:q.kind,x:q.x,y:q.y,vx:q.vx,vy:q.vy})),mount:shipBossMount(subBoss,'C'),targets:M?s7DredgerMineTargets(M):[],gets:Array.from(new Set(window.__dredgerGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.10);greenp,green=snap('dredger_mines_01_green');ok(green['gap']==setup['gap'] and len(green['shots'])==0 and len(green['targets'])==5,'green previews five dangerous paths and one safe lane');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green uses shared field and alert art')
  set_time(.44,40);yellowp,yellow=snap('dredger_mines_02_yellow');ok(yellow['gap']==setup['gap'] and len(yellow['shots'])==0,'yellow keeps the opening fixed after the player crosses the arena');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow uses shared field and alert art')
  set_time(.78,setup['center']);redp,red=snap('dredger_mines_03_red');ok(red['gap']==setup['gap'] and len(red['shots'])==0,'red preserves the promised opening until release');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red uses shared field and alert art')
  set_time(.87);releasep,release=snap('dredger_mines_04_release');expected=[q for q in red['targets']];paths=all(abs(math.atan2(q['vy'],q['vx'])-math.atan2(expected[i]['y']-release['mount']['y'],expected[i]['x']-release['mount']['x']))<1e-7 for i,q in enumerate(release['shots']))
  ok(len(release['shots'])==5 and paths,'exactly the five mines launch down the five previewed trajectories');ok(release['warning']['released'] and release['released'],'shared warning closes when the Dredger releases the minefield')
  shots=[greenp,yellowp,redp,releasep]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'release':release,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
