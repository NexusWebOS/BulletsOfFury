"""Real Chromium proof for per-row Stage-9 Tidal Cascade shared warnings."""
from pathlib import Path
import base64,http.server,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage9_tidal_cascade_warning_0915';OUT.mkdir(parents=True,exist_ok=True)
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
  fight=page.evaluate("()=>window.__fight(9,'boss','yuri')");ok(fight.get('ok'),'native Stage-9 boss route opens in Chromium')
  keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]+['ns9_tidal_intact']
  setup=page.evaluate("""ks=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=9;curStage=STAGES[8];camX=0;player.x=360;player.y=400;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('tidalsovereign');boss.enter=false;boss.x=240;boss.y=140;boss._drawY=140;boss.fireCd=999;bossActive=true;tidalCascadeStart(boss,1);window.__tidalGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__tidalGets.push(k);return g(k)};ks.forEach(k=>XART.rdy(k));const T=boss._s9Cascade;return{name:boss.name,gap:T.gap,rowTell:T.rowTell,next:T.next,cols:T.cols};}""",keys)
  ok(setup['name']=='TIDAL SOVEREIGN' and setup['rowTell']==.62 and setup['cols']==8,'live Tidal Sovereign commits a 0.62-second first row')
  ready=False
  for _ in range(260):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Sovereign and green/yellow/red warning art decode before capture')
  def set_time(t,x=360):page.evaluate("q=>{player.x=q.x;const T=boss._s9Cascade;T.t=q.t;tidalCascadeTick(boss,0);boss.flash=0;}",{'t':t,'x':x})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__tidalGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const T=boss._s9Cascade;return{wave:T&&T.wave,gap:T&&T.gap,warnAt:T&&T.warnAt,next:T&&T.next,rowTell:T&&T.rowTell,shots:eBullets.filter(q=>q.kind==='s9pair').map(q=>({x:q.x,y:q.y,vx:q.vx,vy:q.vy})),warnings:Object.fromEntries(Object.entries(boss._combatWarnings||{}).filter(([k])=>k.startsWith('stage9-tidal-cascade-')).map(([k,v])=>[k,{t:v.t,warm:v.warm,released:v.released}])),gets:Array.from(new Set(window.__tidalGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.10);greenp,green=snap('tidal_cascade_01_green');ok(green['gap']==setup['gap'] and len(green['shots'])==0,'green previews six lanes and preserves the two-column opening');ok('bmfx_fov_green_tall' in green['gets'] and 'bmfx_alert_green_danger' in green['gets'],'green uses shared field and alert art')
  set_time(.31,40);yellowp,yellow=snap('tidal_cascade_02_yellow');ok(yellow['gap']==setup['gap'] and len(yellow['shots'])==0,'yellow does not chase late player movement');ok('bmfx_fov_yellow_tall' in yellow['gets'] and 'bmfx_alert_yellow_danger' in yellow['gets'],'yellow uses shared field and alert art')
  set_time(.558,420);redp,red=snap('tidal_cascade_03_red');ok(red['gap']==setup['gap'] and len(red['shots'])==0,'red preserves the committed opening until release');ok('bmfx_fov_red_tall' in red['gets'] and 'bmfx_alert_red_danger' in red['gets'],'red uses shared field and alert art')
  set_time(.63,120);releasep,release=snap('tidal_cascade_04_release');cw=480/setup['cols'];expected=[(i+.5)*cw for i in range(8) if i not in (setup['gap'],setup['gap']+1)];ok(len(release['shots'])==6 and [q['x'] for q in release['shots']]==expected,'exactly the six previewed columns release after the full warning');ok(release['warnings']['stage9-tidal-cascade-0']['released'] and release['wave']==1,'first shared warning records release and arms row two')
  set_time(.73,120);nextp,nxt=snap('tidal_cascade_05_next_row_green');ok(nxt['gap']==setup['gap']+1 and len(nxt['shots'])==6,'next row visibly moves the promised opening by one column');ok('bmfx_fov_green_tall' in nxt['gets'] and 'bmfx_alert_green_danger' in nxt['gets'],'the next row restarts the shared warning at green')
  shots=[greenp,yellowp,redp,releasep,nextp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':green,'yellow':yellow,'red':red,'release':release,'next':nxt,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
if passed!=len(checks):raise SystemExit(1)
