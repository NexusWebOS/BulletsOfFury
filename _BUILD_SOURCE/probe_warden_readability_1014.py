"""Native Warden feedback, committed attacks, bounded turns and sound playback."""
from pathlib import Path
import os,sys,ast,json,http.server,traceback
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
os.environ['PLAYWRIGHT_BROWSERS_PATH']='C:/Users/Mike/AppData/Local/ms-playwright'
http.server.ThreadingHTTPServer.request_queue_size=128
O=R/'_shots/warden_readability_1014';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];survival=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,pass_=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel=os.environ.get('BOF_BROWSER','msedge'),args=['--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4&&typeof SA14_MINI_CFG!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.mouse.click(60,60);p.evaluate('Audio.resume()')
  def setup(diff='normal'):
   p.evaluate(SETUP,dict(stage=4,kind='olivewarden',mini=True,pilot='cole',diff=diff))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)&&XART.rdy("mr27_iron")&&!!air13Pose("flight_variant_4","heading",0)&&bmfReady("game")}')
   p.evaluate('()=>{B._er26.engaged=false;B._phaseInvuln=0;er26Tick(B,0);story=fb2Talk=null;BOFCinematicDirector.cancel();SA14.events=[];VP12.next=CP12.next=EP13.next=9999;stagePlan=[];player.invuln=1e9;run.shield=0;run.speed=0;Input.keys={};window.wardenTurnAudit={overlaps:0,maxHelpers:0,shots:0,aimChanges:0,earlyShots:0,arrivals:0,frames:0};}')
  def frames(n):
   for i in range(0,n,30):
    p.evaluate('''n=>{for(let j=0;j<n;j++){
     const old=new Set(eBullets);updatePlay(1/60);const a=wardenTurnAudit;a.frames++;
     const ships=enemies.filter(e=>e._sa14Escort&&!e.dead&&e._dyingT==null);a.maxHelpers=Math.max(a.maxHelpers,ships.length);
     for(const q of eBullets.filter(q=>!old.has(q))){if(q._sa14EscortShot){a.shots++;if(q._sa14EscortOwner._sa14Escort.t<2.2)a.earlyShots++;}if(q._sa14Slug&&B._sa14.escortTurn)a.overlaps++;}
     for(const e of ships){const A=e._sa14Escort;if(A.aim){if(A._qaAim&&JSON.stringify(A.aim)!==A._qaAim)a.aimChanges++;A._qaAim=JSON.stringify(A.aim);}if(A.phase==='arrive')a.arrivals++;}
    }}''',min(30,n-i));p.wait_for_timeout(3)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit();}')
   p.screenshot(path=str(O/(name+'.png')))
  for diff in ['easy','normal','hard','furious']:
   setup(diff);p.evaluate('()=>{B._sa14.escortCd=999;er26Set(B,"sa14-mg");window.aimBefore={...B._er26._sa14.aim};}')
   frames(30);p.evaluate('()=>{player.x=camRightX()-42;}');frames(35)
   data=p.evaluate('({warm:B._er26.warm,t:B._er26.t,shots:eBullets.filter(q=>q._sa14Slug).length,warnings:B._er26.warnings.length,aim:B._er26._sa14.aim,old:aimBefore})')
   check(diff+' long visible tell precedes miniboss fire',data['warm']>=1.8 and data['shots']==0 and data['warnings']==2,data)
   check(diff+' warning target does not follow a dodging player',data['aim']==data['old'])
   if diff=='normal':snap('warden-gun-warning')
   frames(180)
   shots=p.evaluate('SA14.events.filter(q=>q.event==="gun-shot").length')
   check(diff+' finite machine-gun burst respects cap',shots==p.evaluate('sa14MiniCfg().rounds'),shots)
   p.evaluate('()=>{eBullets=[];SA14.events=[];er26Set(B,"sa14-rockets");}')
   frames(240)
   rounds=p.evaluate('SA14.events.filter(q=>q.event==="missile-volley").map(q=>q.count)')
   check(diff+' bounded missile waves',len(rounds)==p.evaluate('sa14MiniCfg().waves') and max(rounds)<=4,rounds)
   setup(diff);p.evaluate('()=>{B._sa14.escortCd=0;er26Set(B,"recover");}');frames(38)
   check(diff+' helper arrival has a warning before any ship spawns',p.evaluate('!!B._sa14.escortTurn&&!B._sa14.escortTurn.spawned&&enemies.every(e=>!e._sa14Escort)'))
   if diff=='normal':snap('helper-arrival-warning')
   frames(105)
   check(diff+' helpers use enlarged 96px combat hulls',p.evaluate('enemies.filter(e=>e._sa14Escort).every(e=>e.w===96&&e.h===96)&&enemies.some(e=>e._sa14Escort.scale>1.2)'))
   if diff=='normal':snap('large-helper-arrival')
   frames(140)
   # Get actual damaged pixels through the native hit routers and render paths.
   if diff=='normal':
    pixel=p.evaluate('''()=>{window.E=enemies.find(e=>e._sa14Escort&&!e.dead);E._noHit=false;
     function image(fn){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
     function delta(a,b){let n=0,light=0;for(let i=0;i<a.length;i+=4){if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2]){n++;light+=b[i]+b[i+1]+b[i+2]-a[i]-a[i+1]-a[i+2];}}return{n,light};}
     for(const q of B._mr27.parts)q.flash=0;B.flash=E.flash=0;const before=image(()=>mr27Draw(B)),health=B.hp;
     hitSubBoss(1,B.x,B.y);const body=delta(before,image(()=>mr27Draw(B))),hullTimer=B.flash;
     const part=mr27Part(B,'gunL'),shape=mr27Shape(B,'gunL');B.flash=0;part.flash=0;
     const moduleBefore=image(()=>mr27Draw(B)),partHealth=part.hp;hitSubBoss(1,shape.x,shape.y);const module=delta(moduleBefore,image(()=>mr27Draw(B)));
     const helperBefore=image(()=>drawEnemy(E)),helperHealth=E.hp;hitEnemy(E,1);const helper=delta(helperBefore,image(()=>drawEnemy(E)));
     return{body,module,helper,hullTimer,partTimer:part.flash,helperTimer:E.flash,hpLost:health-B.hp,partLost:partHealth-part.hp,helperLost:helperHealth-E.hp};}''')
    check('actual miniboss hull hit changes visible pixels',pixel['body']['n']>50 and pixel['hullTimer']>0,pixel)
    check('actual modular hit flashes its mounted part',pixel['module']['n']>10 and pixel['partTimer']>0,pixel)
    check('actual helper hit flashes authored aircraft pixels',pixel['helper']['n']>25 and pixel['helperTimer']>0 and pixel['helperLost']>0,pixel)
    snap('hit-flashes')
   # Observe each helper's committed warning/fire phase rather than sample a stale time.
   samples=[]
   for i in range(22):
    rows=p.evaluate('enemies.filter(e=>e._sa14Escort&&!e.dead).map(e=>({phase:e._sa14Escort.phase,t:e._sa14Escort.t,shots:e._sa14Escort.shots,aim:e._sa14Escort.aim}))');samples.extend(rows)
    if diff=='normal' and any(q['phase']=='warn' for q in rows):snap('helper-target-warning')
    frames(30)
   audit=p.evaluate('wardenTurnAudit');check(diff+' helpers and miniboss never release overlapping attacks',audit['overlaps']==0,audit)
   check(diff+' helper population is bounded',audit['maxHelpers']<=p.evaluate('sa14MiniCfg().helpers'),audit)
   check(diff+' helpers never fire during depth entry or re-aim mid burst',audit['earlyShots']==0 and audit['aimChanges']==0 and audit['shots']>0,audit)
   check(diff+' helper turn completes with a recovery',p.evaluate('!B._sa14.escortTurn'),samples[-2:])
   check(diff+' helpers expose genuine lane warnings',any(q['phase']=='warn' for q in samples))
   if diff=='normal':check('hull and module flash timers expire naturally',p.evaluate('B.flash<=0&&B._mr27.parts.every(q=>q.flash<=0)'))
  # Native enemy cues must play even when Cole's upgraded gun suppresses its player cue.
  setup();p.evaluate('()=>{run.weapon=0;run.wlevel=6;Snd.prepare(["enemyMachineGunHeavy","enemyMachineGunLight","missile"]);Audio.resume();}')
  p.wait_for_function('()=>["enemyMachineGunHeavy","enemyMachineGunLight","missile"].every(k=>Snd.pools[k].slots.some(v=>v?.attached&&v.el.readyState>=3))')
  audio=[]
  for key,invoke in [('enemyMachineGunHeavy','sa14Slug(B,"L",player)'),('missile','sa14Missiles(B,player)'),('enemyMachineGunLight','''(()=>{sa14EscortSpawn(B,{});const E=enemies.find(e=>e._sa14Escort);E._sa14Escort.t=E._sa14Escort.fireAt+sa14MiniCfg().tell+.02;sa14EscortTick(E,1/60);})()''')]:
   row=p.evaluate('''async q=>{const [key,code]=q;await Snd._audioCtx().resume();Snd.stopCue(key);Snd._last[key]=0;(0,eval)(code);
    await new Promise(r=>setTimeout(r,20));const voice=Snd.pools[key].slots.find(v=>v?.attached&&!v.el.paused),a=voice?.el;
    if(!a)return{key,playing:false};const ctx=Snd._audioCtx(),meter=ctx.createAnalyser();meter.fftSize=256;
    let capture=null,secondary=null;if(a._bofNode)a._bofNode.connect(meter);else{capture=ctx.createMediaStreamSource((a.captureStream||a.mozCaptureStream).call(a));capture.connect(meter);}const samples=new Float32Array(256);let peak=0;
    for(let i=0;i<24;i++){await new Promise(r=>setTimeout(r,12));meter.getFloatTimeDomainData(samples);for(const v of samples)peak=Math.max(peak,Math.abs(v));}
    if(a._bofNode)a._bofNode.disconnect(meter);if(capture)capture.disconnect();if(secondary)await secondary.close();return{key,playing:a.currentTime>0,peak,volume:a.volume,muted:a.muted,node:!!a._bofNode,duration:a.duration,source:a.currentSrc};}''',[key,invoke])
   audio.append(row);check(key+' has real advancing, nonzero enemy audio',row.get('playing') and row.get('peak',0)>0 and row.get('volume',0)>0,row)
  # Deliberate half-second steering decisions through actual keyboard events.
  # No shield, firing, roll, somersault or special; not a human-clear claim.
  for diff in ['easy','normal','hard','furious']:
   for trial in range(3):
    p.keyboard.up('ArrowLeft');p.keyboard.up('ArrowRight');setup(diff)
    p.evaluate('''trial=>{player.invuln=0;run.shield=0;run.lives=3;player.x=camLeftX()+viewW()*(trial%2?.25:.75);player.y=VH-80;
     window.routeStartX=player.x;window.routeHits=0;window.routeHit=playerHit;
     playerHit=function(){routeHits++;return routeHit.apply(this,arguments);};}''',trial)
    for batch in range(60):
     left=((batch+trial)//5)%2==0
     p.keyboard.up('ArrowRight' if left else 'ArrowLeft');p.keyboard.down('ArrowLeft' if left else 'ArrowRight')
     frames(30)
    p.keyboard.up('ArrowLeft');p.keyboard.up('ArrowRight')
    row=p.evaluate('({diff:diffKey,hits:routeHits,lives:run.lives,dead:player.dead,x:player.x,start:routeStartX,seconds:30})');survival.append(row)
    p.evaluate('playerHit=window.routeHit')
   rows=[r for r in survival if r['diff']==diff];check(diff+' ordinary keyboard movement has surviving samples',any(r['lives']>0 and not r['dead'] for r in rows),rows)
  b.close()
except Exception as exc:errors.append(str(exc));print(traceback.format_exc(),flush=True)
finally:
 stop();report={'checks':checks,'passed':sum(q['pass_'] for q in checks),'failed':sum(not q['pass_'] for q in checks),'errors':errors,'survival':survival,'scope':'Native fixtures, actual hit routers/rendering and decoded audio. Simple movement survival samples are not human campaign balance proof.'}
 (O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['checks','survival','scope']}),flush=True)
if errors or report['failed']:sys.exit(1)
