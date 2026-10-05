"""Real Chromium: five specials, HP trigger, live rescue, support interception."""
from pathlib import Path
import json,base64,http.server,sys
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/rebel_gang_1004';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[]};errors=[]
def ck(v,n):
 report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,20):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}');(O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(n)
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  if '--review' in sys.argv:
   p.goto(f'http://127.0.0.1:{port}/_shots/rebel_gang_1004/review.html',timeout=120000);p.screenshot(path=str(O/'review-page.png'))
   for label,kind in [('Full rebel encounter','intro'),('Fight now','fight'),('Gang Mode preview','gang'),('Decker scene preview','rescue')]:
    if kind=='rescue':p.get_by_label('Pilot',exact=True).select_option('decker')
    p.get_by_role('button',name=label,exact=True).click();p.wait_for_function('()=>document.querySelector("#status").textContent==="Encounter ready."',timeout=120000)
    f=p.locator('#arena').element_handle().content_frame();p.wait_for_timeout(350)
    s=f.evaluate('()=>({intro:!boss._rebels.frIntro?.done,scene:rg4Scene()?.kind,gang:rg4State()?.gang,weapon:run.weapon,hp:boss.hp,full:boss.maxhp})')
    ck(s['intro'] if kind=='intro' else not s['intro'] and (s.get('scene')==kind if kind in ['gang','rescue'] else not s.get('scene')),label+' launches the correct live beat')
    if kind=='fight':
     f.evaluate(sh.TRAP_RAF);frames(f,60);f.evaluate('()=>pBullets.length=0')
     key=f.evaluate('()=>keybindFor(1).fire[0]');p.keyboard.down(key);frames(f,15);p.keyboard.up(key)
     ck(f.evaluate('()=>!player.dead&&pBullets.some(p=>!p.ally)'),'real keyboard fire creates player rounds in the playable encounter');shot(f,'playable-fight-hud')
    if kind=='rescue':
     ck(f.evaluate('()=>rg4State().members[0].ref===player&&rg4State().members.filter(m=>m.key==="decker").length===1'),'playing Decker uses the real pilot at the formation lead without a duplicate')
     f.evaluate(sh.TRAP_RAF);frames(f,200);shot(f,'playable-scene-hud')
   ck(not errors,'review and all playable shortcuts have no browser errors')
   (O/'review-checks.json').write_text(json.dumps({'checks':report['checks'],'errors':errors},indent=2));browser.close();sys.exit(any(not c['ok'] for c in report['checks']))
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','diff':'furious','pilot':'yuri'})
  p.evaluate('()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=false;B._noHit=false;R.ships.forEach(q=>{q.mode="fight";q.y=120;q.x=worldWidth()/2+(q.i-2)*70;});window.G=rg4Init(B);H3.release=false;fb2Talk=null;s6Opening=null;rg4Warm();s6WingInit();s6Wing.beats=3;s6Wing.all=true;s6Wing.fakeDone=true;s6Wing.route="right";s6Wing.choice=false;s6Wing.boxes=[];s6Wing.supplyIndex=3;}')
  p.wait_for_function('()=>XART.rdy(RG4.sheet)&&XART.rdy("arch_blaster_gun_2")&&XART.rdy("nfrb_2")&&XART.rdy("florb_3")&&XART.rdy("av3_laser_beams")',timeout=90000)
  # Runtime resolved source cells: inspect actual art, not filenames.
  p.evaluate('()=>{window.artProof=[];const keys=["rr_ship_voss_iron_vulture","nfrb_2","florb_3","arch_blaster_gun_2",RG4.sheet];for(const k of keys)XART.rdy(k);window.warnBlits=[];const get=XART.get,draw=ctx.drawImage;XART.get=function(k){const r=get.apply(this,arguments);window.lastArt=k;return r;};ctx.drawImage=function(){if(window.lastArt?.includes("impact_imminent"))warnBlits.push({key:lastArt,args:Array.from(arguments).slice(1)});window.lastArt=null;return draw.apply(this,arguments);};}')
  p.wait_for_timeout(500)
  p.evaluate('()=>{ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle="#071522";ctx.fillRect(0,0,cv.width,cv.height);["rr_ship_voss_iron_vulture","nfrb_2","florb_3","arch_blaster_gun_2"].forEach((k,i)=>{const im=XART.get(k);if(im){ctx.drawImage(im,i*220+25,50,160,180);artProof.push(k);}});}')
  (O/'source-art.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  for key,kind in [('voss','fusion'),('rook','heavy'),('kaia','roller'),('nyx','ghost'),('jace','stealth')]:
   frames(p,100)
   p.evaluate('([key,kind])=>{rg4Clear(G);G.scene=null;H3.release=false;B._noHit=false;G.releaseAt=G.age+99;for(const q of R.ships)q.rg4.cd=99;window.Q=R.ships.find(q=>q.key===key);rg4Attack(Q,R,G,kind);G.releaseAt=G.age+99;}',[key,kind])
   frames(p,64 if kind=='fusion' else 35);shot(p,kind+'-charge')
   frames(p,85 if kind=='fusion' else 100);shot(p,kind+'-release')
   ck(p.evaluate('(kind)=>G.events.some(e=>e.event==="specialRelease"&&e.kind===kind)',kind),kind+' releases its distinct special')
  ck(p.evaluate('()=>warnBlits.some(b=>b.key==="bmfx_alert_red_impact_imminent"&&b.args[2]===32)'),'original red asterisk drawn by the game context at release')
  p.evaluate('()=>{const q=R.ships[1];q.frCloak=1;window.cloakTarget=retinaBossTargets(B).some(t=>t._retinaId==="nyx-hull");q.frCloak=0;}')
  ck(p.evaluate('()=>!cloakTarget&&retinaBossTargets(B).some(t=>t._retinaId==="nyx-hull")'),'stealth breaks Retina acquisition and reveal restores it')
  # Ordinary bullets really destroy the orb and Retina exposes the same target.
  p.evaluate('()=>{rg4Clear(G);G.scene=null;G.gang=true;G.rescueDone=true;G.orbSpawned=false;rg4Orb(G,R);G.releaseAt=G.age+99;G.ord[0].hp=2;window.orb=G.ord[0];}')
  frames(p,1);ck(p.evaluate('()=>retinaBossTargets(B).some(t=>t.kind==="support")'),'helper is a Retina target')
  p.evaluate('()=>{pBullets.push({x:orb.x,y:orb.y,vx:0,vy:0,w:20,h:20,dmg:3,kind:"mg"});rg4OrdnanceTick(B,G,0);}')
  ck(p.evaluate('()=>orb.dead&&G.events.some(e=>e.event==="ordnanceDestroyed")'),'ordinary gunfire destroys helper orb')
  # Exact three-of-five boundary, with no hidden heal or enemy shield.
  p.evaluate('()=>{G.gang=false;G.rescueDone=false;G.orbSpawned=false;for(const q of R.ships){q.hp=q.max;q.dead=false;q.rg4.act=null;q.rg4.cd=99;}R.ships[0].hp=R.ships[0].max*.5;R.ships[1].hp=R.ships[1].max*.5;rg4Threshold(B,G);}')
  ck(p.evaluate('()=>!G.gang'),'two wounded pilots do not trigger Gang Mode')
  p.evaluate('()=>{R.ships[2].hp=R.ships[2].max*.5;rg4Threshold(B,G);window.scrollBefore=_stage6SkyScroll;}');frames(p,110);shot(p,'gang-mode')
  ck(p.evaluate('()=>G.gang&&G.scene?.kind==="gang"'),'third pilot at exactly half health triggers shared charge')
  ck(p.evaluate('()=>R.ships.every(q=>q.shield===0&&q.shieldMax===0)&&R.ships[0].hp===R.ships[0].max*.5'),'charge adds no rebel shields or HP refill')
  frames(p,150);ck(p.evaluate('()=>!G.scene&&G.ord.some(o=>o.kind==="helper")'),'Gang Mode activates destructible orbital support')
  # Let the real update clock reach Decker naturally; no direct scene start.
  for _ in range(40):
   frames(p,30)
   if p.evaluate('()=>G.scene?.kind==="rescue"'):break
  ck(p.evaluate('()=>G.scene?.kind==="rescue"'),'Decker rescue begins naturally after Gang Mode combat')
  p.evaluate('()=>{window.seenLines=[];window.sceneScroll=_stage6SkyScroll;window.sceneHp=player.hp;window.sceneAge=G.age;window.sceneShield=run.shield;window.sceneLife=run.lives;player.invuln=0;pShoot();useBomb();startSpecial();playerHit();}')
  ck(p.evaluate('()=>pBullets.length===0&&run.shield===sceneShield&&run.lives===sceneLife&&!pauseTapped()'),'rescue refuses firing, specials, damage and pause/skip')
  seen=set();extra=set()
  for _ in range(180):
   frames(p,20)
   c=p.evaluate('()=>G.scene?{kind:G.scene.kind,i:G.scene.i,t:G.scene.t,age:G.scene.age,cloak:G.cloak}:null')
   if not c:break
   if c.get('kind')=='rescue' and c.get('i') in [1,5] and .65<c.get('t',0)<1.1 and c['i'] not in extra:
    extra.add(c['i']);shot(p,'effect-wave' if c['i']==1 else 'effect-reveal')
   if c.get('kind')=='rescue' and c.get('t',0)>2.5 and c.get('i') not in seen:
    seen.add(c['i']);shot(p,'scene-'+str(c['i']));p.evaluate('()=>seenLines.push(G.scene.lines[G.scene.i].text)')
  ck(p.evaluate('()=>!G.scene&&G.rescueDone&&G.events.some(e=>e.event==="rescueComplete")'),'all timed lines complete without player skipping')
  ck(p.evaluate('()=>seenLines.length===8'),'all eight portrait dialogue beats rendered')
  ck(p.evaluate('()=>_stage6SkyScroll!==sceneScroll&&G.age-sceneAge>25'),'world scroll and encounter clock keep moving through dialogue')
  ck(p.evaluate('()=>G.cloak===0&&G.shield>0'),'counter-scan removes cloak while brief friendly shield remains')
  ck(p.evaluate('()=>RG4.draws.scan>0&&RG4.draws.row0>0&&RG4.draws.row1>0&&RG4.draws.row2>0'),'generated wave, swirls, reveal and original Retina all draw')
  shot(p,'combat-resumed');frames(p,420)
  ck(p.evaluate('()=>G.shield===0&&!h3Locked()'),'temporary protection expires and combat controls unlock')
  ck(p.evaluate('()=>G.events.filter(e=>e.event==="rescueStart").length===1'),'Decker scene is one-shot')
  ck(p.evaluate('()=>R.ships.every(q=>fr27RebelModules(q).every(m=>m.hp===m.max))'),'every rebel retains complete authored hull after damage')
  report['events']=p.evaluate('()=>G.events');report['draws']=p.evaluate('()=>RG4.draws');report['errors']=errors
  ck(not errors,'zero page/console errors');browser.close()
finally:stop()
(O/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('RESULT',sum(c['ok'] for c in report['checks']),'/',len(report['checks']),flush=True)
sys.exit(any(not c['ok'] for c in report['checks']))
