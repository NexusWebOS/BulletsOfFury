"""Real Chromium proof for the Stage-5 Archmage committed spiked-ball launch."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'archmage_spiked_ball_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
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
  fight=page.evaluate("()=>window.__fight(5,'boss','yuri')");ok(fight.get('ok'),'native Stage-5 boss route opens in Chromium')
  keys=['arch_spiked_ball']+[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=5;curStage=STAGES[4];camX=0;player.x=326;player.y=392;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('xenoregent');boss.enter=false;boss.x=240;boss.y=168;boss._drawY=boss.y;boss._noHit=false;bossActive=true;boss._combatWarnings={};const h=boss._hammer;h.state='shield';h.t=1.01;hammerBossTick(boss,.01);h.ballDir=1;window.__archBallGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__archBallGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));return{name:boss.name,state:h.state,warn:HAMMER_BALL_WARN,dir:h.ballDir,path:hammerBallLaunchPath(boss),world:worldWidth(),right:camRightX()-54,bottom:PLAY.y+PLAY.h-54};}""",keys)
  ok(setup['name']=='CHROME HAMMER ARCHMAGE' and setup['state']=='curl' and setup['warn']==1.25,'live Archmage arms its 1.25-second spiked-ball launch warning')
  ok(setup['dir']==1 and abs(setup['path']['ex']-setup['right'])<.01,'the committed launch ray terminates at its exact first wall impact')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored spiked-ball and shared warning art decode before capture')
  def advance(dt,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;hammerBossTick(boss,q.dt);boss.flash=0;}",{'dt':dt,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__archBallGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const h=boss._hammer,B=boss._combatWarnings&&boss._combatWarnings['archmage-spiked-ball'];return{state:h.state,t:h.t,dir:h.ballDir,vx:h.vx,vy:h.vy,angle:h.angle,path:hammerBallLaunchPath(boss),warn:B&&{t:B.t,warm:B.warm,released:B.released},gets:Array.from(new Set(window.__archBallGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  advance(.18,326,392);gp,g=snap('archmage_ball_01_green');ok(g['state']=='curl' and 'bmfx_fov_green_tall' in g['gets'] and 'bmfx_alert_green_danger' in g['gets'],'green previews the committed first-impact corridor')
  advance(.42,72,270);yp,y=snap('archmage_ball_02_yellow');ok(y['path']==g['path'] and y['dir']==g['dir'],'yellow remains committed after the player moves left');ok('bmfx_fov_yellow_tall' in y['gets'] and 'bmfx_alert_yellow_danger' in y['gets'],'yellow uses the shared field and alert art')
  advance(.45,440,470);rp,r=snap('archmage_ball_03_red');ok(r['path']==g['path'] and r['dir']==g['dir'] and r['state']=='curl','red preserves the promised launch through a late opposite dodge');ok('bmfx_fov_red_tall' in r['gets'] and 'bmfx_alert_red_danger' in r['gets'],'red uses the shared field and alert art')
  advance(.22,40,300);lp,launch=snap('archmage_ball_04_launch');ok(launch['state']=='ball' and launch['warn']['released'] and launch['vx']==150 and launch['vy']==165,'the spiked ball releases only after red on the committed velocity')
  advance(1.35,440,470);bp,bounce=snap('archmage_ball_05_first_bounce');ok(bounce['state']=='ball' and abs(bounce['vx'])==150 and bounce['vx']<0 and bounce['angle']>0,'the original physical wall reflection continues after the warned launch');ok('arch_spiked_ball' in bounce['gets'],'the live danger phase renders the authored spiked-ball reel')
  shots=[gp,yp,rp,lp,bp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':g,'yellow':y,'red':r,'launch':launch,'bounce':bounce,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
