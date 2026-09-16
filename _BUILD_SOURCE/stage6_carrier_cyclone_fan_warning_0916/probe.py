"""Real Chromium proof for the Stage-6 Carrier twin-cyclone shared warning."""
from pathlib import Path
import base64,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage6_carrier_cyclone_fan_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
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
  warning_keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]
  setup=page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=6;curStage=STAGES[5];const W=worldWidth();camX=(W-VW)*.5;player.x=W*.5+80;player.y=410;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=W*.5;boss.y=146;boss._drawY=146;boss.ty=146;boss.fireCd=999;bossActive=true;carrierMegaInit(boss);boss._mega.phase=0;boss._mega.cd=0;boss._combatWarnings={};carrierMegaTick(boss,.01);window.__cycloneGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__cycloneGets.push(k);return g(k)};const F=boss._mega.cycloneFan;return{name:boss.name,hull:SHIPBOSS.doomsdaycarriermk2.key,tell:F.tell,cooldown:F.cooldown,angles:F.lanes.map(q=>q.a),slots:F.lanes.map(q=>q.slot),world:W,camera:camX,center:W*.5};}""")
  keys=warning_keys+[setup['hull'],'s6mb_cyclonetracer_0','s6mb_cyclonemuzzle_0']
  ok(setup['name']=='DOOMSDAY CARRIER MK II' and setup['tell']==.62 and setup['cooldown']==1.35 and setup['slots']==['MG_L']*3+['MG_R']*3,'live Carrier commits its six original twin-battery cyclone lanes')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Carrier, cyclone projectile, muzzle and warning art decode before capture')
  def set_time(t,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;const F=boss._mega.cycloneFan;F.t=q.t;carrierCycloneFanTick(boss,0);boss.flash=0;}",{'t':t,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__cycloneGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const F=boss._mega.cycloneFan,B=F&&boss._combatWarnings[F.id];return{angles:F&&F.lanes.map(q=>q.a),paths:F&&carrierCycloneFanPaths(boss,F),released:F&&F.released,warn:B&&{t:B.t,warm:B.warm,released:B.released},shots:eBullets.filter(q=>q.kind==='s6cyclone').map(q=>({kind:q.kind,x:q.x,y:q.y,vx:q.vx,vy:q.vy,spd:q.spd,ang:q.ang,speed:Math.hypot(q.vx,q.vy)})),gets:Array.from(new Set(window.__cycloneGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.10,setup['center']+80,410);gp,g=snap('carrier_cyclone_01_green');ok(g['angles']==setup['angles'] and len(g['shots'])==0,'green previews all six committed cyclone paths');ok('bmfx_fov_green_tall' in g['gets'] and 'bmfx_alert_green_danger' in g['gets'],'green uses shared field and alert art')
  set_time(.30,90,260);yp,y=snap('carrier_cyclone_02_yellow');ok(y['angles']==setup['angles'] and len(y['shots'])==0,'yellow ignores late player movement');ok('bmfx_fov_yellow_tall' in y['gets'] and 'bmfx_alert_yellow_danger' in y['gets'],'yellow uses shared field and alert art')
  set_time(.57,setup['world']-90,465);rp,r=snap('carrier_cyclone_03_red');ok(r['angles']==setup['angles'] and len(r['shots'])==0,'red preserves the six promised paths until release');ok('bmfx_fov_red_tall' in r['gets'] and 'bmfx_alert_red_danger' in r['gets'],'red uses shared field and alert art')
  set_time(.63,40,250);relp,rel=snap('carrier_cyclone_04_release');ok(len(rel['shots'])==6 and rel['warn']['released'],'exactly six cyclone tracers release after the full warning');ok(all(q['spd']==4.1 for q in rel['shots']),'the original 4.1-speed authored cyclone volley is preserved before difficulty pressure')
  shots=[gp,yp,rp,relp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':g,'yellow':y,'red':r,'release':rel,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
sys.exit(0 if passed==len(checks) else 1)
