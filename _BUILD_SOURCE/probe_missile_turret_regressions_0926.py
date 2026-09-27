import sys,json,http.server
from pathlib import Path
sys.path.insert(0,str(Path('_BUILD_SOURCE').resolve()))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
errors=[];result={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  for stage in [1,6,9]:
   pg=br.new_page(viewport={'width':1100,'height':1200})
   pg.on('pageerror',lambda e:errors.append(str(e)))
   pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
   pg.wait_for_function('()=>window.__bofFrames>4')
   pg.evaluate(sh.TRAP_RAF)
   pg.evaluate(sh.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   if stage==1:
    result['manualMissile']=pg.evaluate("""() => {
      stagePlan=[];enemies=[];pBullets=[];eBullets=[];
      spawnBoss(STAGES[0].boss);bossActive=true;boss.enter=false;boss._noHit=false;boss._ovIntro.done=true;boss.fireCd=999;
      boss.x=player.x;boss.y=player.y-160;const hp=boss.hp;
      pBullets.push({kind:'gmiss',x:boss.x,y:boss.y+boss.h*.2,spd:7,vx:0,vy:-7,w:12,h:22,dmg:25,t:0,tgt:null});
      for(let i=0;i<4;i++)updatePlay(1/60);
      return {kind:boss.kind,hpBefore:hp,hpAfter:boss.hp,damaged:boss.hp<hp};
    }""")
   elif stage==6:
    pg.evaluate("() => {XART.rdy('overhaul_ground_base_6');XART.rdy('overhaul_ground_head_laser');}")
    pg.wait_for_function("() => XART.rdy('overhaul_ground_base_6')&&XART.rdy('overhaul_ground_head_laser')",timeout=15000)
    result['turret']=pg.evaluate("""() => {
      s6Opening=null;stagePlan=[];enemies=[];eBullets=[];mapScroll=1200;
      const e=modularGroundTurretSpawn(6,'laser',0);if(!e)return {spawned:false};
      const x=e.x,y=e.y,mapY=e._modTurret.mapY;
      mapScroll+=120;updatePlay(1/60);
      return {spawned:true,xBefore:x,xAfter:e.x,yBefore:y,yAfter:e.y,mapY,
        projected:Math.abs(e.y-(mapY-levelSrcY()))<.01,headAngle:e._modTurret.angle,
        transformStable:(()=>{ctx.save();ctx.translate(17,31);const before=ctx.getTransform();const drew=drawModularGroundTurret(e),after=ctx.getTransform();ctx.restore();return drew&&before.a===after.a&&before.b===after.b&&before.c===after.c&&before.d===after.d&&before.e===after.e&&before.f===after.f;})()};
    }""")
   else:
    result['spaceMissile']=pg.evaluate("""() => {
      stagePlan=[];enemies=[];eBullets=[];pBullets=[];spawnSubBoss('voidhorizon');
      for(let i=0;i<90;i++)updateSubBoss(1/60);
      subBoss.enter=false;const core=subBoss._s9rift.core;
      player.x=core.x;player.y=VH-80;run.spaceMode=true;run.spaceLevels=[5,5,5];
      const locks=spaceVolleyLocks({x:player.x,y:player.y-30},Math.max(VH*1.25,350+5*18),3);
      const before=core.hp;spaceVolleyFire();
      for(let i=0;i<95;i++){for(const b of pBullets)if(!b.dead)spaceBulletTick(b,1/60);pBullets=pBullets.filter(b=>!b.dead);}
      return {lockCount:locks.filter(t=>t===core).length,hpBefore:before,hpAfter:core.hp,damaged:core.hp<before};
    }""")
   pg.close()
  br.close()
finally:stop()
result['errors']=errors
Path('_shots/probe_video_regressions_0926.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
assert not errors
assert result['manualMissile']['damaged']
assert result['spaceMissile']['lockCount']>0 and result['spaceMissile']['damaged']
assert result['turret']['spawned'] and result['turret']['projected'] and result['turret']['xBefore']==result['turret']['xAfter'] and result['turret']['transformStable']
