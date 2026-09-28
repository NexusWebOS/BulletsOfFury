import json,http.server,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path(sh.GAME)/'_shots/hammer_fix_0928';out.mkdir(exist_ok=True);port,stop=sh.serve(sys.argv[1] if len(sys.argv)>1 else sh.GAME)
setup="""secret=>{ht27Stop();diffKey='furious';DIFF=DIFFS.furious;run.mode='arcade';run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');if(secret){ht27Pending=true;startRun(5);const d=boss._hammerTime;d.mode='attack';d.locked=false;d.shield=false;d.musicStarted=true;d.clock=40;Snd.music.hammerTime.pause();}else{beginStage(5);spawnBoss('chromehammer');bossActive=true;}setState(GS.PLAY);story=null;stagePlan=[];waveIdx=999;subBoss=null;subBossDone=true;subBossTriggered=true;subBossActive=false;s5run=null;run._s9warp=0;run.spaceMode=true;run.gravityShipReady=true;gravityMode=GRAVITY_SHIP_ACTIVE;special=null;player.dead=false;player.invuln=99999;player.x=worldWidth()/2;player.y=VH*.83;boss.enter=false;boss._noHit=false;boss.x=worldWidth()/2;boss.y=VH*.34;boss._hammer.balance0922=true;hammerState(boss,'warn');hammerBossTick(boss,.01);hammerBossTick(boss,3.5);enemies=[];pBullets=[];eBullets=[];run.bombs=12;run.missileTier='standard';for(const k of Object.keys(Input.keys))Input.keys[k]=false;return !!fr27Armor(boss)?.activated;}"""
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1360,'height':960});p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  report={}
  for secret in [False,True]:
   key='password' if secret else 'regular';report[key]={}
   for critical in [False,True]:
    report[key]['activated']=p.evaluate(setup,secret)
    p.evaluate("""critical=>{boss.hp=boss.maxhp*.5;fr27Restore(boss,critical?.5:.1,critical,true);boss._hammer.frArmor.half=true;const t=retinaBossTargets(boss).find(t=>t._retinaId==='hammer');retina.target=t;useBomb(t);window.__flight=pBullets.find(q=>q.kind==='gmiss');window.__path=[];window.__recovery=boss._hammer.recovery;}""",critical)
    for batch in range(14):
     r=p.evaluate("""()=>{for(let i=0;i<6;i++){const q=window.__flight;__path.push({x:q.x,y:q.y,phase:q._frHammerRoute?.phase,dead:!!q.dead});updatePlay(1/60);}return {dead:!!__flight.dead,status:__recovery.status,state:boss._hammer.state};}""")
     if secret and not critical and batch in [1,4,8]:
      p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
      p.screenshot(path=str(out/('flank-'+str(batch)+'.png')))
     if r['dead']:break
    r.update(p.evaluate("()=>({path:__path,flanked:__flight._frHammerFlank===boss,armor:fr27Armor(boss).hp,core:__recovery.coreHP})"));report[key]['critical' if critical else 'heal']=r
    assert r['status']=='cancelled' and r['flanked'],r
   p.evaluate(setup,secret);r=p.evaluate("""()=>{fr27Armor(boss).barrier=5;hammerState(boss,'hammer');if(boss._hammerTime)boss._hammerTime.duration=100;const A=fr27Armor(boss),before=A.hp;useBomb(boss);window.__body=pBullets.find(q=>q.kind==='gmiss');for(let i=0;i<160&&!__body.dead;i++)updatePlay(1/60);return{dead:!!__body.dead,flanked:__body._frHammerFlank===boss,damage:before-A.hp};}""");report[key]['body']=r;assert r['dead'] and r['damage']>0,r
  p.evaluate(setup,False)
  report['volley']=p.evaluate("""()=>{fr27Restore(boss,.1,false,true);const t=retinaBossTargets(boss).find(t=>t._retinaId==='hammer');spaceVolleyLaunchRack(3);const shots=pBullets.filter(q=>q.kind==='spaceVolley');for(const q of shots)q._target=t;const R=boss._hammer.recovery;let crossed=false;for(let i=0;i<140&&R.status==='charging';i++){updatePlay(1/60);crossed=crossed||shots.some(q=>q._frHammerFlank===boss);}return{crossed,status:R.status,core:R.coreHP,max:R.coreMax,reflected:eBullets.filter(q=>q.kind==='s4rocket').length};}""");assert report['volley']['crossed'] and report['volley']['core']<report['volley']['max'],report['volley']
  p.evaluate(setup,True)
  report['cue']=p.evaluate("""()=>{const b=boss,d=b._hammerTime;delete b._hammer.frArmor;b._noHit=false;hammerState(b,'warn');d.mode='attack';d.clock=15.1;d.locked=false;d.shield=false;hammerBossTick(b,.01);const snapshots=[];for(let i=0;i<215;i++){updatePlay(1/60);if(i%30===0)snapshots.push({t:b._hammer.t,state:b._hammer.state,mode:d.mode,locked:ht27Locked()});}return{activated:fr27Armor(b).activated,snapshots,mode:d.mode,clock:d.clock};}""");assert report['cue']['activated'],report['cue']
  report['errors']=errors;assert not errors
  (out/('package-probe.json' if len(sys.argv)>1 else 'probe.json')).write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v if k in ['cue','errors','volley'] else {n:{a:b for a,b in q.items() if a!='path'} if isinstance(q,dict) else q for n,q in v.items()} for k,v in report.items()}));br.close()
finally:stop()
