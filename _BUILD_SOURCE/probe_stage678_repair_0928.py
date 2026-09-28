import json,http.server,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path(sh.GAME)/'_shots/stage678_repair_0928';out.mkdir(exist_ok=True);port,stop=sh.serve(sys.argv[1] if len(sys.argv)>1 else sh.GAME)
setup="""n=>{ht27Stop();diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');beginStage(n);setState(GS.PLAY);story=null;stagePlan=[];waveIdx=999;subBoss=null;subBossDone=true;subBossTriggered=true;subBossActive=false;run._s9warp=0;special=null;player.dead=false;player.invuln=99999;player.x=worldWidth()/2;player.y=VH*.83;enemies=[];pBullets=[];eBullets=[];explosions=[];particles=[];smokeRings=[];shockRings=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;if(n===6){s6Opening=null;s6Wing.choice=false;s6Wing.route='left';}if(n===8){run._l78Entry=0;l78entry=null;}return {_masterSrcY,mapScroll,world:worldWidth(),cfg:_levelCfg(),boss:curStage.boss,mini:SUBBOSS[n]};}"""
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1360,'height':960});p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  report={}
  def draw(name):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   p.screenshot(path=str(out/(name+'.png')))
  p.evaluate(setup,6)
  p.evaluate("()=>{spawnSubBoss('siegebomber');window.__miniHP={hp:subBoss.maxhp,core:subBoss._bomber.coreMax};subBoss=null;subBossActive=false;spawnBoss('warhive');bossActive=true;warhiveTick(boss,2.7);Audio.startMusic('boss6');}")
  p.wait_for_timeout(1200)
  report['harrier']=p.evaluate("()=>{const b=boss,W=b._whv,old=b.hp;_lastHitX=W.cx;_lastHitY=W.cy-38;const h=bossHitTest(_lastHitX,_lastHitY);hitBoss(120);const coreTarget=retinaBossTargets(b).find(q=>q._retinaId==='hull');return{hit:h,damage:old-b.hp,visible:bossHealthVisible(b),max:b.maxhp,targets:retinaBossTargets(b).length,coreTarget:!!coreTarget,mini:__miniHP,music:Snd.music.boss6?.src};}")
  draw('harrier-combat')
  report['ace']=p.evaluate("()=>{const W=boss._whv,expected=W.aceMax;W.core=0;warhiveTick(boss,.01);warhiveTick(boss,4.5);return{mode:W.mode,hp:boss.hp,max:boss.maxhp,expected};}")
  p.evaluate(setup,7)
  p.evaluate("()=>{XART.rdy('nst7_master_v3');XART.rdy('fr28_sewer_connector');}");p.wait_for_timeout(1600)
  p.evaluate("()=>{mapScroll=s7mEndScroll();drawBG(0);spawnBoss(curStage.boss);bossActive=true;s7mInit(boss);boss._s7mod.mode='dead';player.x=220;player.invuln=0;for(let i=0;i<8;i++)XART.rdy('nfx_l7portal_'+i);for(const fam of BOSS_COMBO)for(let i=0;i<8;i++)XART.rdy(fam+'_'+i);}")
  p.wait_for_timeout(1200)
  report['exit']=[]
  for t in [0.1,8.1,10,14.9,17.1,18.4,21]:
   p.evaluate("t=>{const E=boss._s7mod.frExit;const dt=E?t-E.t:t;for(let i=0;i<Math.ceil(dt*30);i++){updatePlay(dt/Math.ceil(dt*30));drawBG(0);}}",t)
   report['exit'].append(p.evaluate("()=>({t:boss._s7mod.frExit.t,travel:boss._s7mod.frExit.travel,groundY:boss._s7mod.frExit.groundY,bossY:boss.y,x:player.x,y:player.y,portalReady:XART.rdy('nfx_l7portal_7'),portalDim:[XART.get('nfx_l7portal_7')?.naturalWidth,XART.get('nfx_l7portal_7')?.width],source:_masterSrcY,green:explosions.filter(q=>q._frToxic).length})"))
   draw('toxic-exit-'+str(t))
   if t==17.1:
    p.evaluate('()=>{explosions=[];particles=[];}');draw('toxic-portal-open')
  p.evaluate(setup,7);p.evaluate("()=>{mapScroll=1400;drawBG(0);enemies=[];const e=spawnEnemy('s7lamprey',340,210,{});player.invuln=0;const row=stage7SluiceEvents()[0];row.row=_masterSrcY+300;row.side=-1;row.live=true;row.t=stage7SluiceWarn()+.25;row.done=false;XART.rdy('fr28_lamprey');XART.rdy('s7sluice_vent');}");p.wait_for_timeout(700);draw('sewer-lamprey-and-vent')
  p.evaluate(setup,8)
  report['realmScroll']=p.evaluate("()=>{const start=mapScroll;for(let i=0;i<60;i++)drawBG(1/60);return{scroll:mapScroll-start,visual:run._frRealmScroll};}")
  p.evaluate("()=>{boss=null;bossActive=false;spawnEnemy('s8interceptor',230,105,{});spawnEnemy('s8bomber',420,120,{});spawnEnemy('s8carrier',340,10,{});for(let i=0;i<5;i++)fr27RealmShot(180+i*65,270,Math.PI/2,2.6,i%3);}")
  for i in range(6):p.evaluate("()=>{for(let i=0;i<10;i++)updatePlay(1/60);}");p.wait_for_timeout(20)
  draw('alien-encounter')
  p.evaluate("()=>{spawnBoss('vileexistence');bossActive=true;enemies=[];pBullets=[];eBullets=[];}")
  for i in range(30):p.evaluate("()=>{for(let i=0;i<12;i++)updatePlay(1/60);}");p.wait_for_timeout(15)
  draw('alien-first-form')
  report['alienBoss']=p.evaluate("()=>({entry:boss._symEntry,enter:boss.enter,form:boss._vForm,hp:boss.hp,x:boss.x,y:boss.y,pattern:boss._v24?.pattern?.type,targets:retinaBossTargets(boss).length})")
  p.evaluate(setup,8);p.evaluate("()=>{l78EntryStart();setState(GS.WARPENTRY);}")
  for i in range(15):p.evaluate("()=>drawL78Entry(1)");p.wait_for_timeout(15)
  report['entry']=p.evaluate("()=>({state,expected:GS.PLAY,invuln:player.invuln,music:Snd.cur?.src,ready:Snd.cur?.readyState,entry:run._l78Entry})")
  report['controls']=p.evaluate("()=>{boss=null;bossActive=false;subBoss=null;enemies=[];eBullets=[];pBullets=[];special=null;story=null;player.invuln=999;const x=player.x;Input.keys.d=true;Input.keys.j=true;for(let i=0;i<30;i++)updatePlay(1/60);Input.keys.d=Input.keys.j=false;return{xMoved:player.x-x,shots:pBullets.length,state};}")
  report['errors']=errors;(out/'probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report));br.close()
  assert not errors,errors
  assert report['harrier']['hit'] and report['harrier']['damage']==120 and report['harrier']['visible'] and report['harrier']['coreTarget']
  assert report['harrier']['mini']['hp']<7000
  assert report['ace']['max']==report['ace']['expected']
  assert abs(report['realmScroll']['scroll']-40)<.001
  assert report['entry']['state']==report['entry']['expected'] and report['entry']['ready']>=2 and 'stage8_furious_death' in report['entry']['music']
  assert report['controls']['xMoved']>20 and report['controls']['shots']>0
finally:stop()
