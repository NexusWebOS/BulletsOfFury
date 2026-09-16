"""Real Chromium proof for the Stage-7 Warden cripple-phase committed rail groups."""
from pathlib import Path
import base64,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage7_warden_cripple_rail_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'/'trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
checks=[];errors=[]
def ok(v,label):checks.append({'pass':bool(v),'label':label});print(('ok  ' if v else 'FAIL ')+label,flush=True)
port,stop=shoot.serve(str(ROOT))
with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);page=br.new_page(viewport={'width':1100,'height':1200});page.on('pageerror',lambda e:errors.append('page '+str(e)));page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=120000);page.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);page.evaluate(shoot.TRAP_RAF);page.evaluate(capture3.LIB)
  fight=page.evaluate("()=>window.__fight(7,'boss','yuri')");ok(fight.get('ok'),'native Stage-7 boss route opens in Chromium')
  warning_keys=[f'bmfx_{kind}_{col}_{tail}' for col in ('green','yellow','red') for kind,tail in (('fov','tall'),('alert','danger'))]
  setup=page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=7;curStage=STAGES[6];const W=worldWidth();camX=(W-VW)*.5;player.x=W*.5;player.y=470;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('sludgeemperor');boss.enter=false;boss.x=W*.5;boss.y=178;boss._drawY=178;boss.ty=178;boss.fireCd=999;bossActive=true;s7WardenInit(boss);const S=boss._s7warden,F=S.final;F.phase='cripple';F.crippled=true;F.fire=0;F.crippleRail=null;S.noHit=false;S.mode='patrol';boss._s7FinalNoBar=false;boss._combatWarnings={};s7WardenCrippleRailTick(boss,.01);window.__railGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__railGets.push(k);return g(k)};const C=F.crippleRail;return{name:boss.name,tell:C.warn,aim:C.aim,paths:s7WardenCrippleRailPaths(boss,C),world:W,center:W*.5};}""")
  keys=warning_keys+['cfx_stage7_warden_cripple','cfx_stage7_warden_spear']
  ok(setup['name']=='TOXIC PORTAL WARDEN' and setup['tell']==.58 and len(setup['paths'])==4,'live cripple phase commits its four unique rail paths')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored cripple hull, rail spear and shared warning art decode before capture')
  def advance(dt,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;s7WardenCrippleRailTick(boss,q.dt);boss.flash=0;}",{'dt':dt,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__railGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const F=boss._s7warden.final,C=F.crippleRail,B=C&&boss._combatWarnings[C.id];return{aim:C&&C.aim,paths:C&&s7WardenCrippleRailPaths(boss,C),released:C&&C.released,shot:C&&C.shot,warn:B&&{t:B.t,warm:B.warm,released:B.released},rails:eBullets.filter(q=>q._s7warden==='rail').map(q=>({x:q.x,y:q.y,spd:q.spd,ang:q.ang,slot:q._s7warden})),gets:Array.from(new Set(window.__railGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  advance(.10,setup['center'],470);gp,g=snap('warden_cripple_01_green');ok(g['aim']==setup['aim'] and len(g['rails'])==0,'green previews the committed four-path rail group');ok('bmfx_fov_green_tall' in g['gets'] and 'bmfx_alert_green_danger' in g['gets'],'green uses shared field and alert art')
  page.evaluate('()=>{boss.x+=34}');advance(.18,80,330);yp,y=snap('warden_cripple_02_yellow');ok(y['aim']==setup['aim'] and y['paths'][0]['x']!=g['paths'][0]['x'] and len(y['rails'])==0,'yellow follows the crawling hull without changing committed aim');ok('bmfx_fov_yellow_tall' in y['gets'] and 'bmfx_alert_yellow_danger' in y['gets'],'yellow uses shared field and alert art')
  advance(.23,setup['world']-80,480);rp,r=snap('warden_cripple_03_red');ok(r['aim']==setup['aim'] and len(r['rails'])==0,'red preserves all promised rail paths until release');ok('bmfx_fov_red_tall' in r['gets'] and 'bmfx_alert_red_danger' in r['gets'],'red uses shared field and alert art')
  advance(.08,30,300);relp,rel=snap('warden_cripple_04_release');ok(rel['released'] and len(rel['rails'])==1 and rel['rails'][0]['spd']==5.25,'the first single rail releases only after the complete warning')
  advance(.70,setup['world']-30,510);groupp,group=snap('warden_cripple_05_group');ok(len(group['rails'])==5 and sum(1 for q in group['rails'] if q['spd']==5.25)==3 and sum(1 for q in group['rails'] if q['spd']==4.65)==2,'the committed group preserves three singles and its dual finisher');ok('cfx_stage7_warden_spear' in group['gets'],'authored Warden rail-spear art renders for the warned group')
  shots=[gp,yp,rp,relp,groupp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':g,'yellow':y,'red':r,'release':rel,'group':group,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
sys.exit(0 if passed==len(checks) else 1)
