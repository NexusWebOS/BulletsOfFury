"""Current password-only bosses: native routes, real music clocks and tanks."""
from pathlib import Path
import argparse,http.server,json,sys,time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/passwords';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--codes',default='HAMMER,HAMA,SONIC,ORDOS,HARK');ap.add_argument('--resume',action='store_true');ap.add_argument('--label',default='');ap.add_argument('--art-recovery-off',action='store_true');a=ap.parse_args()
if a.label:O=O/a.label;O.mkdir(exist_ok=True)
old=json.loads((O/'report.json').read_text()) if a.resume and (O/'report.json').exists() else {}
rows=old.get('rows',[]);errors=old.get('errors',[]);teardown=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
def save():(O/'report.json').write_text(json.dumps(dict(method='Actual password submit/start routes on N/H/F. HAMA/HAMMER use 75 seconds of unmodified real media time; no seek or clock override. Tank clocks include native intro/loading preparation plus a 60-second simulated tail; use each recorded sim duration, not a per-minute assumption. Visible protected pilot, no player fire. These are opening/activity observations, not human win tests. Audio is muted; cue timing/clock advance is verified, not sound quality. Teardown messages are recorded separately after the observation ends.',rows=rows,errors=errors,teardown=teardown),indent=2)+'\n',encoding='utf-8')
try:
 with sync_playwright() as pw:
  for code in a.codes.split(','):
   br=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
   for diff in ['normal','hard','furious']:
    if a.resume and any(q['code']==code and q['difficulty']==diff for q in rows):continue
    print('RUN',code,diff,flush=True);context=br.new_context(viewport=dict(width=1600,height=1000));p=context.new_page();p.set_default_timeout(180000);life={'closing':False};firstError=len(errors)
    p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});"+('window.AR19_OFF=1;' if a.art_recovery_off else ''))
    def record(message,life=life):(teardown if life['closing'] else errors).append(message)
    p.on('pageerror',lambda e,record=record:record(str(e)));p.on('console',lambda m,record=record:record(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None);p.on('response',lambda r,record=record:record(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
    # Stopping/closing a music encounter deliberately cancels range/audio
    # streams. Keep actual failed requests; do not call that cancellation a bug.
    def failed(r,life=life,record=record):
     if r.failure=='net::ERR_ABORTED' and Path(urlparse(r.url).path).suffix.lower() in ['.mp3','.ogg','.wav','.flac']:return
     record('REQUEST '+str(r.failure)+' '+r.url.split('?')[0])
    p.on('requestfailed',failed)
    p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4')
    if code not in ['HAMMER','HAMA']:p.evaluate(shoot.TRAP_RAF)
    p.evaluate('''o=>{window.PC19={live:false,sim:0,frames:0,shots:0,firstProjectile:null,firstWarning:null,warnings:[],kinds:{},phases:[],modes:{},peak:0,maxHelpers:0,seen:new WeakSet()};const tick=updatePlay,warn=combatWarningTick;
     updatePlay=function(dt){if(!PC19.live)return tick.apply(this,arguments);player.invuln=1e9;Input.keys={};Input.mouse.down=false;PC19.sim+=dt;PC19.frames++;const r=tick.apply(this,arguments),b=boss||subBoss,d=b?._hammerTime;
      for(const q of eBullets)if(!PC19.seen.has(q)){PC19.seen.add(q);PC19.shots++;PC19.firstProjectile??=PC19.sim;PC19.kinds[q.kind]=(PC19.kinds[q.kind]||0)+1;}
      const phase=d?d.mode+':'+b._hammer.state:b?._sg10?b._sg10.attack?.kind||'rest':state;if(phase!==PC19.lastPhase){PC19.phases.push({t:PC19.sim,phase});PC19.lastPhase=phase;}PC19.modes[phase]=(PC19.modes[phase]||0)+1;PC19.peak=Math.max(PC19.peak,eBullets.filter(q=>!q.dead).length);PC19.maxHelpers=Math.max(PC19.maxHelpers,d?.helpers?.length||0);return r;};
     combatWarningTick=function(owner,key,t,warm){if(PC19.live){PC19.firstWarning??=PC19.sim;if(!PC19.warnings.some(q=>q.key===String(key)))PC19.warnings.push({key:String(key),t:PC19.sim,warm});}return warn.apply(this,arguments);};
     ht27Stop();debugFight=null;coopOn=false;setState(GS.PASSWORD);run.mode='arcade';diffKey=o.diff;DIFF=DIFFS[o.diff];pwInput=o.code;submitPassword();pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(PENDING_STAGE);player.invuln=1e9;PC19.live=true;SC12.refresh();__bofFit();}''',dict(code=code,diff=diff))
    for loading in range(900):
     if p.evaluate('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}'):break
     # Advance the native arrival/drawing while its separate asset/font
     # requests settle. Do not replace image readiness with mock flags.
     if code not in ['HAMMER','HAMA']:
      issue=p.evaluate(shoot.STEP,12)
      if issue:raise RuntimeError(str(issue))
     p.wait_for_timeout(100)
    else:raise RuntimeError('Native load did not settle: '+p.evaluate('JSON.stringify({state,stage:run.stage,font:bmfReady("game"),fontRecord:BMF.game?{mapped:!!BMF.game.map,complete:BMF.game.img?.complete,width:BMF.game.img?.naturalWidth,src:BMF.game.img?.src}:null,load:stageLoadInfo(run.stage),failed:_stageLoads[run.stage]?.keys.filter(k=>{const im=XART.raw(k);return im?._bofStageDecodeDone===-1||im?.complete&&!im?.naturalWidth;}).map(k=>({key:k,path:XART._src[k]})),inflight:_stageLoads[run.stage]?.inflight.map(q=>({key:q.key,done:q.im?._bofStageDecodeDone}))})'))
    real=code in ['HAMMER','HAMA'];samples=[]
    if real:
     p.wait_for_function('()=>boss?._hammerTime?.musicStarted&&!ht27Song().paused',polling=50)
     initial=p.evaluate('({media:ht27Song().currentTime,sim:PC19.sim,frames:window.__bofFrames})');start=time.monotonic()
     for sec in range(75):
      p.wait_for_timeout(1000);s=p.evaluate('({media:ht27Song().currentTime,clock:boss._hammerTime.clock,mode:boss._hammerTime.mode,phase:boss._hammer.state,frames:window.__bofFrames,paused:ht27Song().paused,state})');samples.append(s)
      if sec in [2,14,29,49,74]:p.screenshot(path=str(O/f'{code}-{diff}-{sec+1:02}.jpg'),type='jpeg',quality=82)
      if sec in [14,44,74]:print('CLOCK',code,diff,json.dumps(s),flush=True)
     result=p.evaluate('''()=>({metrics:{...PC19,seen:undefined},active:ht27Active,variant:hamaOn()?'HAMA':'HAMMER',hp:boss.hp,max:boss.maxhp,finite:Number.isFinite(boss.x+boss.y+boss.hp)&&eBullets.every(q=>Number.isFinite(q.x+q.y))})''')
     result.update(clockStart=initial,clockSamples=samples,wallSeconds=time.monotonic()-start,maxClockDrift=max(abs(s['media']-s['clock']) for s in samples),mediaAdvanced=samples[-1]['media']-initial['media'],renderedFrames=samples[-1]['frames']-initial['frames'])
    else:
     # The actual password start passes through its native arrival before the
     # modular actor exists. rAF is trapped here, so advance that arrival before
     # polling lazy art. Waiting for a not-yet-spawned actor cannot progress.
     for batch in range(120):
      if p.evaluate('!!subBoss?._sg10'):break
      issue=p.evaluate(shoot.STEP,12)
      if issue:raise RuntimeError(str(issue))
      p.wait_for_timeout(10)
     if not p.evaluate('!!subBoss?._sg10'):raise RuntimeError('Password route did not spawn its native siege tank: '+p.evaluate('JSON.stringify({state,stage:run.stage,pending:ON5.pending,debug:debugFight})'))
     p.wait_for_function('()=>sg10Ready(subBoss)',polling=50)
     for sec in range(60):
      for batch in range(5):p.evaluate(shoot.STEP,12);p.wait_for_timeout(5)
      if sec in [4,19,59]:p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/f'{code}-{diff}-{sec+1:02}.jpg'),type='jpeg',quality=82)
     result=p.evaluate('''()=>({metrics:{...PC19,seen:undefined},unit:subBoss._sg10.unit,hp:subBoss.hp,max:subBoss.maxhp,finite:Number.isFinite(subBoss.x+subBoss.y+subBoss.hp)&&eBullets.every(q=>Number.isFinite(q.x+q.y)),events:SG10.events})''')
    result['assetRecovery']=p.evaluate('typeof AR19==="undefined"?null:AR19.events');result['caseErrors']=errors[firstError:]
    row=dict(code=code,difficulty=diff,realtime=real,**result);rows.append(row);save();print('END',code,diff,json.dumps({k:result.get(k) for k in ['finite','variant','unit','mediaAdvanced','maxClockDrift','renderedFrames']}|{k:result['metrics'].get(k) for k in ['shots','firstProjectile','firstWarning','peak','maxHelpers']}),flush=True)
    # Closing the context already stops audio. Returning to Title here starts
    # an unrelated menu asset flood immediately before aborting its requests.
    life['closing']=True;context.close()
   br.close()
finally:stop();save()
print(json.dumps(dict(cases=len(rows),errors=errors)),flush=True);sys.exit(bool(errors) or any(not r['finite'] or r.get('realtime') and (r['mediaAdvanced']<70 or r['maxClockDrift']>.12) for r in rows))
