"""Real Chromium proof for the Stage-6 Carrier chrome-flak warning and airburst."""
from pathlib import Path
import base64,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'_shots'/'stage6_carrier_flak_warning_0916';OUT.mkdir(parents=True,exist_ok=True)
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
  setup=page.evaluate("""()=>{__auto=function(){};story=null;dlgBox=function(){};stagePlan=[];waveIdx=0;enemies=[];eBullets=[];pBullets=[];particles=[];powerups=[];playerLocks=[];state=GS.PLAY;stateT=1;run.stage=6;curStage=STAGES[5];const W=worldWidth();camX=(W-VW)*.5;player.x=W*.5+80;player.y=440;player.invuln=999;player.dead=false;player.alive=true;diffKey='normal';DIFF=DIFFS.normal;boss=null;bossActive=false;spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=W*.5;boss.y=146;boss._drawY=146;boss.ty=146;boss.fireCd=999;bossActive=true;carrierInit(boss);carrierMegaInit(boss);boss._mega.phase=5;boss._mega.step=1;boss._mega.cd=0;boss._mega.t=0;boss._mega.flakPair=0;boss.hp=boss.maxhp*.20;boss._lc.playing=false;boss._cn=null;boss._mega.nodes.forEach(n=>n.dead=true);boss._combatWarnings={};carrierMegaTick(boss,.01);window.__flakGets=[];const g=XART.get.bind(XART);XART.get=function(k){window.__flakGets.push(k);return g(k)};const F=boss._mega.flakFan;return{name:boss.name,hull:SHIPBOSS.doomsdaycarriermk2.key,tell:F.tell,cooldown:F.cooldown,pair:F.pair,angles:F.lanes.map(q=>q.a),slots:F.lanes.map(q=>q.slot),world:W,center:W*.5};}""")
  keys=warning_keys+[setup['hull'],'s6mb_flakshell_0','s6mb_flakburst_0','s6mb_cyclonemuzzle_0']
  ok(setup['name']=='DOOMSDAY CARRIER MK II' and setup['tell']==.62 and setup['cooldown']==1.08 and setup['pair']==0 and setup['slots']==['lower_left_inner','lower_right_inner'],'live Carrier commits the two outer chrome-flak paths')
  ready=False
  for _ in range(280):
    ready=page.evaluate('ks=>ks.every(k=>XART.rdy(k))',keys)
    if ready:break
    page.wait_for_timeout(35)
  ok(ready,'authored Carrier, flak shell, airburst, muzzle and warning art decode before capture')
  def set_time(t,x,y):page.evaluate("q=>{player.x=q.x;player.y=q.y;const F=boss._mega.flakFan;F.t=q.t;carrierFlakFanTick(boss,0);boss.flash=0;}",{'t':t,'x':x,'y':y})
  def snap(name):
    page.evaluate('()=>{shake=0;window.__flakGets=[];drawWorld(0)}');d=page.evaluate("""()=>{const F=boss._mega.flakFan,B=F&&boss._combatWarnings[F.id];return{angles:F&&F.lanes.map(q=>q.a),slots:F&&F.lanes.map(q=>q.slot),paths:F&&carrierFlakFanPaths(boss,F),released:F&&F.released,warn:B&&{t:B.t,warm:B.warm,released:B.released},shells:eBullets.filter(q=>q.kind==='s6flak').map(q=>({kind:q.kind,x:q.x,y:q.y,spd:q.spd,ang:q.ang,fuse:q._flakFuse})),fragments:eBullets.filter(q=>q.kind==='s6cluster').map(q=>({kind:q.kind,x:q.x,y:q.y,spd:q.spd,ang:q.ang,life:q.life})),gets:Array.from(new Set(window.__flakGets))}}""");raw=page.evaluate("()=>document.querySelector('#screen').toDataURL('image/png').split(',')[1]");p=OUT/f'{name}.png';p.write_bytes(base64.b64decode(raw));return p,d
  set_time(.10,setup['center']+80,440);gp,g=snap('carrier_flak_01_green');ok(g['angles']==setup['angles'] and len(g['shells'])==0,'green previews both committed outer flak paths');ok('bmfx_fov_green_tall' in g['gets'] and 'bmfx_alert_green_danger' in g['gets'],'green uses shared field and alert art')
  page.evaluate('()=>{boss.x+=34}');set_time(.28,90,270);yp,y=snap('carrier_flak_02_yellow');ok(y['angles']==setup['angles'] and y['paths'][0]['x']!=g['paths'][0]['x'] and len(y['shells'])==0,'yellow follows both moving hardpoints without changing committed angles');ok('bmfx_fov_yellow_tall' in y['gets'] and 'bmfx_alert_yellow_danger' in y['gets'],'yellow uses shared field and alert art')
  set_time(.57,setup['world']-90,465);rp,r=snap('carrier_flak_03_red');ok(r['angles']==setup['angles'] and len(r['shells'])==0,'red preserves both promised shell corridors until release');ok('bmfx_fov_red_tall' in r['gets'] and 'bmfx_alert_red_danger' in r['gets'],'red uses shared field and alert art')
  set_time(.64,40,250);relp,rel=snap('carrier_flak_04_release');ok(len(rel['shells'])==2 and rel['warn']['released'],'two chrome shells release after the full warning');ok(all(q['spd']==3.75 and abs(q['fuse']-.64)<.00001 for q in rel['shells']),'the authored shell speed and 0.64-second fuse are preserved')
  page.evaluate('()=>carrierFlakTick(.65)');burstp,burst=snap('carrier_flak_05_airburst');ok(len(burst['shells'])==0 and len(burst['fragments'])==10,'both shells airburst into their original five-way fragment fans');ok(any(k.startswith('s6mb_flakburst_') for k in burst['gets']),'authored chrome-flak burst art renders at detonation')
  shots=[gp,yp,rp,relp,burstp]
  for p in shots:
    im=Image.open(p).convert('RGB');ok(im.size==(960,1024) and im.getbbox() is not None,f'{p.stem} is a non-empty native gameplay frame')
  ok(not errors and not page.evaluate('()=>window.__err||null'),'zero Chromium page, console or game-loop errors');br.close()
stop();result={'checks':checks,'errors':errors,'fight':fight,'setup':setup,'green':g,'yellow':y,'red':r,'release':rel,'airburst':burst,'shots':[str(p.relative_to(ROOT)) for p in shots]};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');passed=sum(c['pass'] for c in checks);print(f'{passed} passed / {len(checks)-passed} failed',flush=True)
sys.exit(0 if passed==len(checks) else 1)
