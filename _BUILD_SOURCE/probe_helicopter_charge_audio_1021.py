"""Actual helicopter wind-up and real-time missile media playback in Chromium."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1]; O=R/'_shots/helicopter_charge_audio_1021'; O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data)); print(('PASS ' if ok else 'FAIL ')+name,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  p=browser.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready&&window.BOF_SONIC_EFFECTS')
  p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate('''()=>{run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(q=>q.key==='cole');startRun(1);beginStage(1);curStage=STAGES[0];setState(GS.PLAY);player.invuln=1e9;storySkip();BOFCinematicDirector.cancel();boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];eBullets=[];pBullets=[];stagePlan=[];waveIdx=999;spawnClock=9999;_adaptiveSpawnT=9999;mapScroll=1400;sx21Warm();spawnBoss('damkeeper');updateOverlordX(boss,0);XART.rdy('ovbody_intact');XART.rdy('ovrotor_00');Snd.prepare('overlordRocket');}''')
  p.wait_for_function('()=>XART.rdy("ovbody_intact")&&XART.rdy("ovrotor_00")&&Object.values(SX21_ART.banks).every(a=>XART.rdy(a.key)&&XART.rdy(a.sourceKey))')
  p.evaluate('''()=>{window.chargeBlits=[];const draw=ctx.drawImage;ctx.drawImage=function(im,...args){if(im?._so21)chargeBlits.push({...im._so21,args});return draw.call(this,im,...args);};window.resetHeli=diff=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);Object.assign(boss,{enter:false,dead:false,_ovIntro:null,_ovAirborne:false,_ovSonic:null,_ovSweep:null,_ovVolley:null,_ovRush:null,_chargeTell:null,_ovState:'fight',_stageSound:{},_pivot:0,x:camLeftX()+viewW()/2,y:VH*.25,t:0,hp:boss.maxhp,_enraged:false});eBullets=[];_navalFlashes.length=0;};window.renderHeli=()=>{chargeBlits.length=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return chargeBlits.filter(x=>x.bank==='charge_green').length;};}''')
  for diff in ['normal','hard','furious']:
   p.evaluate('diff=>{resetHeli(diff);ovStartChargeTell(boss);window.chargeAudit={old:0,counts:[],frames:[]};}',diff)
   for batch in range(9):
    p.evaluate('''()=>{for(let i=0;i<12;i++){boss.t+=1/60;efxClock+=1/60;updateOverlordX(boss,1/60);chargeAudit.old+=_navalFlashes.filter(f=>f.fam==='s1fx_green_impact'||f.fam==='s1fx_wind_vortex').length;tickNavalFlashes(1/60);if(boss._chargeTell){chargeAudit.counts.push(renderHeli());chargeAudit.frames.push(...chargeBlits.filter(x=>x.bank==='charge_green').map(x=>x.frame));}}}''')
    if batch in [3,6]:p.screenshot(path=str(O/f'{diff}-charge-{batch}.png'))
   row=p.evaluate('()=>({...chargeAudit,state:boss._ovState})')
   ck(diff+' full native wind-up has zero legacy impact/vortex spawns',row['old']==0,row['old'])
   ck(diff+' every charge frame draws one animated sonic charge',len(row['counts'])>80 and set(row['counts'])=={1} and len(set(row['frames']))>3,dict(counts=sorted(set(row['counts'])),frames=sorted(set(row['frames']))))
   ck(diff+' native charge completes into committed ram',row['state']=='chargeOff',row['state'])
  for diff in ['normal','hard','furious']:
   p.evaluate("diff=>{resetHeli(diff);ovSonicStart(boss);window.sonicAudit={old:0,counts:[]};}",diff)
   for batch in range(11):
    p.evaluate("""()=>{for(let i=0;i<12;i++){boss.t+=1/60;efxClock+=1/60;updateOverlordX(boss,1/60);sonicAudit.old+=_navalFlashes.filter(f=>f.fam==='s1fx_green_impact'||f.fam==='s1fx_wind_vortex').length;tickNavalFlashes(1/60);if(boss._ovSonic?.phase==='waveTell')sonicAudit.counts.push(renderHeli());}}""")
    if batch==8:p.screenshot(path=str(O/f'{diff}-sonic-charge.png'))
   row=p.evaluate("()=>({...sonicAudit,phase:boss._ovSonic?.phase,shots:eBullets.filter(q=>q._ovSonicWave).length})")
   ck(diff+' native sonic tell also has exactly one charge, no legacy bursts, and releases its wave',row['old']==0 and len(row['counts'])>100 and set(row['counts'])=={1} and row['phase']=='waves' and row['shots']>0,dict(old=row['old'],counts=sorted(set(row['counts'])),phase=row['phase'],shots=row['shots']))
  row=p.evaluate('''()=>{resetHeli('normal');ovRotorTempest(boss);return{vortex:_navalFlashes.some(f=>f.fam==='s1fx_wind_vortex'),bullets:eBullets.map(q=>q.kind)};}''')
  ck('Real rotor tempest attack retains its vortex and blades',row['vortex'] and 's1windVortex' in row['bullets'] and 's1windBlade' in row['bullets'],row)
  p.wait_for_function('()=>Snd.pools.overlordRocket.list.every(a=>a.readyState>=3)')
  p.evaluate('''async()=>{Snd.vol.master=1;Snd.vol.sfx=.4;window.audioProof={events:[],samples:[],cues:[]};window.proofCtx=new AudioContext();await proofCtx.resume();window.proofAnalysers=[];for(const a of Snd.pools.overlordRocket.list){const source=proofCtx.createMediaElementSource(a),an=proofCtx.createAnalyser();an.fftSize=1024;source.connect(an);an.connect(proofCtx.destination);proofAnalysers.push(an);a.addEventListener('playing',()=>audioProof.events.push({time:performance.now(),volume:a.volume,ready:a.readyState}));}window.audioSampler=setInterval(()=>{let peak=0;for(const an of proofAnalysers){const data=new Float32Array(an.fftSize);an.getFloatTimeDomainData(data);for(const v of data)peak=Math.max(peak,Math.abs(v));}audioProof.samples.push(peak);},10);const original=Snd.play;Snd.play=function(name,...args){const accepted=original.call(this,name,...args);if(name==='overlordRocket')audioProof.cues.push({accepted,time:performance.now()});return accepted;};}''')
  for diff in ['normal','hard','furious']:
   p.evaluate('''diff=>{Snd.stopCue('overlordRocket');resetHeli(diff);audioProof.events=[];audioProof.samples=[];audioProof.cues=[];ovStartMissileLock(boss,'fight');}''',diff)
   # Simulated attack time matches real media time; the production throttle uses performance.now.
   for i in range(70):
    p.evaluate('''()=>{for(let i=0;i<3;i++){boss.t+=1/60;efxClock+=1/60;updateOverlordX(boss,1/60);tickNavalFlashes(1/60);}renderHeli();}''');p.wait_for_timeout(50)
   row=p.evaluate('''()=>({missiles:eBullets.filter(q=>q._ovBarrage).length,...audioProof,config:Snd.TAME.overlordRocket,context:proofCtx.state})''')
   ck(diff+' actual pod releases each trigger a launch report',row['missiles']>=4 and len(row['cues'])==row['missiles'] and all(q['accepted'] for q in row['cues']),dict(missiles=row['missiles'],cues=row['cues']))
   ck(diff+' launch voices really play with nonzero audio samples',len(row['events'])>=row['missiles'] and max(row['samples'],default=0)>.01,dict(events=row['events'],peak=max(row['samples'],default=0),context=row['context']))
   p.screenshot(path=str(O/f'{diff}-missile-launch.png'))
  p.evaluate('clearInterval(audioSampler)')
  ck('No page console draw or asset errors',not errors,errors)
  browser.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
