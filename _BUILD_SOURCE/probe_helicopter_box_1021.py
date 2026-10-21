"""Native PixelLab sonic-bank playback, damage flashes, tells and safe gaps."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/helicopter_box_1021';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready&&window.BOF_SONIC_EFFECTS');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.mode="arcade";run.pilot="cole";pilotIndex=PILOTS.findIndex(q=>q.key==="cole");startRun(1);beginStage(1);curStage=STAGES[0];setState(GS.PLAY);player.invuln=1e9;storySkip();BOFCinematicDirector.cancel();}')
  p.evaluate('''()=>{sx21Warm();window.sx21draws=[];const draw=ctx.drawImage;
   ctx.drawImage=function(im,...args){if(im?._so21)sx21draws.push({...im._so21,args});return draw.call(this,im,...args);};}''')
  p.wait_for_function('()=>Object.values(SX21_ART.banks).every(a=>XART.rdy(a.key)&&XART.rdy(a.sourceKey))')
  p.evaluate('''()=>{boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];eBullets=[];pBullets=[];stagePlan=[];waveIdx=999;spawnClock=9999;_adaptiveSpawnT=9999;mapScroll=1400;spawnBoss('damkeeper');updateOverlordX(boss,0);boss.enter=false;boss.dead=false;boss._ovIntro=null;boss._ovAirborne=false;boss.x=camLeftX()+viewW()/2;boss.y=VH*.25;boss._pivot=0;XART.rdy('ovbody_intact');XART.rdy('ovrotor_00');}''')
  p.wait_for_function('()=>XART.rdy("ovbody_intact")&&XART.rdy("ovrotor_00")')
  for diff in ['normal','hard','furious']:
   row=p.evaluate('''diff=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);eBullets=[];boss._ovSonic=null;boss._ovVolley=null;boss._chargeTell=null;ovStartSweep(boss);boss._ovSweep.phase='travel';boss._pivot=0;boss._ovT=1;const S=boss._ovSweep,held=JSON.stringify(S);window.hbNewDraw=ovSweepSafeDraw;window.hbBoxCalls=[];const fill=ctx.fillRect;ctx.fillRect=function(...args){if(this.fillStyle==='#63f3a6'||this.fillStyle==='#a5ffd2')hbBoxCalls.push({args,color:this.fillStyle});return fill.apply(this,args);};window.hbFill=fill;
    ovSweepSafeDraw=SX21.base.sweepSafe;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);window.hbBefore=ctx.getImageData(0,0,cv.width,cv.height).data;return{boxes:hbBoxCalls.length,safeX:S.safeX,safeR:S.safeR,safeY:S.safeY,tune:S.tune,held};}''',diff)
   p.screenshot(path=str(O/(diff+'-before.png')))
   after=p.evaluate('''()=>{ovSweepSafeDraw=hbNewDraw;hbBoxCalls=[];const S=boss._ovSweep,held=JSON.stringify(S);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);const after=ctx.getImageData(0,0,cv.width,cv.height).data;let pixels=0;for(let i=0;i<after.length;i+=4)if(hbBefore[i+1]-after[i+1]>12&&hbBefore[i+1]>hbBefore[i]+10)pixels++;ctx.fillRect=hbFill;return{boxes:hbBoxCalls.length,pixels,unchanged:held===JSON.stringify(boss._ovSweep),same:S===boss._ovSweep,phase:S.phase};}''')
   p.screenshot(path=str(O/(diff+'-after.png')))
   ck(diff+' actual green rectangle pixels removed',row['boxes']==3 and after['boxes']==0 and after['pixels']>100,after)
   ck(diff+' native sweep safe gap and attack state unchanged',after['unchanged'] and after['same'] and after['phase']=='travel',row['tune'])
   row=p.evaluate('''()=>{boss.x=worldWidth()/2;boss._ovSweep.fire=0;ovSweepTick(boss,1/60);return{shots:eBullets.length,phase:boss._ovSweep?.phase};}''')
   ck(diff+' native strafe still fires its twin guns',row['shots']>=2,row)
   row=p.evaluate('''()=>{boss._ovSweep=null;ovStartChargeTell(boss);boss._chargeTell.t=1;boss._ovChargeGlow=.5;sx21draws=[];window.hbWarnings=0;const warn=combatWarningDraw;combatWarningDraw=function(...args){hbWarnings++;return warn.apply(this,args);};try{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}finally{combatWarningDraw=warn;}return{warnings:hbWarnings,charge:sx21draws.some(d=>d.key==='sr21_charge_green')};}''')
   ck(diff+' authored charge warning and new sonic glow retained',row['warnings']>0 and row['charge'],row)
   p.screenshot(path=str(O/(diff+'-charge-warning.png')))
  ck('No page console draw or asset errors',not errors,errors);b.close()

finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
