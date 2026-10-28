"""Audible native Furious boss recordings. No enemy HP or phase writes.

Uses shoot.py's loopback server, real RAF, native boss-mode entry, native GOD,
and a small input-only aiming assistant. Output is kept under ignored _shots/.
"""
from pathlib import Path
import argparse
import base64
import json
import subprocess
import time

import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from shoot import serve

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
OUT=Path(__file__).resolve().parent
CONFIG={}

CAPTURE = r"""async cfg => {
 const audio=Snd._audioCtx();await audio.resume();
 const mix=audio.createMediaStreamDestination(), analyser=audio.createAnalyser();
 analyser.fftSize=1024;
 const gain=audio.createGain();gain.gain.value=.5;analyser.connect(gain);gain.connect(mix);
 const seen=new WeakSet(), originalPlay=HTMLMediaElement.prototype.play;
 const stats=window.captureStats={peak:0,tapped:0,playing:{},tapErrors:[],frames:0};
 HTMLMediaElement.prototype.play=function(){
  if(!seen.has(this)){
   try{
    if(this._bofNode)this._bofNode.connect(analyser);
    else{const source=audio.createMediaElementSource(this);source.connect(audio.destination);source.connect(analyser);}
    seen.add(this);stats.tapped++;
    this.addEventListener('playing',()=>{
     const key=Object.entries(Snd.pools).find(([k,p])=>p.slots.some(s=>s?.el===this))?.[0]
       ||Object.entries(Snd.music).find(([k,v])=>v===this)?.[0]||'loop';
     stats.playing[key]=(stats.playing[key]||0)+1;
    });
   }catch(e){stats.tapErrors.push(String(e));}
  }
  return originalPlay.apply(this,arguments);
 };
 const canvas=document.createElement('canvas');canvas.width=1280;canvas.height=800;
 const g=canvas.getContext('2d'), samples=new Float32Array(analyser.fftSize);
 window.reviewCapture=canvas;window.captureLive=true;window.captureStart=performance.now();
 window.reviewBot={enabled:true,target:null,targetKey:'',targetAt:0,lastMissile:-100,
   lastHp:null,lastProgress:0,keys:[],tick:0,errors:[],targetInfo:null};
 const K=Input.keys;
 for(const k of ['a','d','w','s','j','k','c'])if(K[k]===undefined)K[k]=false;
 function targetKey(t){return String(t._retinaId||t.id||t.name||t.kind||'hull')+':'+String(t._retinaOwner?.kind||'');}
 function aim(elapsed){
  const A=reviewBot;if(!A.enabled)return;A.tick++;
  if(state!==GS.PLAY||player.dead||player.out){for(const k of ['a','d','w','s','j','c'])K[k]=false;return;}
  const b=cfg.role==='mini'?subBoss:boss;
  let list=b&&!b.dead?retinaBossTargets(b).filter(t=>!t.dead&&t.hp>0&&Number.isFinite(t.x+t.y)&&t.y>=PLAY.y-180&&t.y<VH-20):[];
  let target=list.find(t=>targetKey(t)===A.targetKey);
  if(!target){target=list.sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x))[0]||null;A.targetKey=target?targetKey(target):'';A.lastHp=target?.hp;A.lastProgress=elapsed;}
  if(target&&target.hp<A.lastHp-.01){A.lastProgress=elapsed;A.lastHp=target.hp;}
  if(target&&elapsed-A.lastProgress>7&&list.length>1){target=list[(list.indexOf(target)+1)%list.length];A.targetKey=targetKey(target);A.lastHp=target.hp;A.lastProgress=elapsed;}
  const R=b?._r30,J=R&&typeof j3State==='function'?j3State(b):null;
  const tag=J?String(J.encounter)+':'+String(R.v18?.form??0):b?._whv?.mode||'fight';
  if(A.formTag!==tag){A.formTag=tag;A.formAt=elapsed;A.seenForms=A.seenForms||{};A.firstVisit=!A.seenForms[tag];A.seenForms[tag]=true;}
  const tx=clamp(target?.x??((b?.x??worldWidth()/2)+Math.sin(elapsed*.7)*65),22,worldWidth()-22),ty=b?._pb28&&['boost','ahead'].includes(b._pb28.mode)?VH*.35:VH-65;
  K.a=player.x>tx+7;K.d=player.x<tx-7;K.w=player.y>ty+7;K.s=player.y<ty-7;
  const demonstrate=elapsed<(cfg.demonstrate??25)||(J&&A.firstVisit&&elapsed-A.formAt<5);
  K.j=!demonstrate&&elapsed%1.0<.76;K.c=!demonstrate&&!!b;
  if(!demonstrate&&b&&(run.bombs|0)>0&&elapsed-A.lastMissile>1.2){Input.injectTap('k');A.lastMissile=elapsed;}
  if(elapsed-A.lastEvade>8||A.lastEvade==null){Input.injectTap(elapsed%16<8?'q':'e');A.lastEvade=elapsed;}
  A.targetInfo=target?{key:A.targetKey,kind:target.kind,x:target.x,y:target.y,hp:target.hp}:null;
 }
 function render(){
  if(!captureLive)return;
  const elapsed=(performance.now()-captureStart)/1000;
  try{aim(elapsed);}catch(e){if(reviewBot.errors.length<10)reviewBot.errors.push(String(e));}
  g.fillStyle=getComputedStyle(document.body).backgroundColor;g.fillRect(0,0,1280,800);
  for(const c of document.querySelectorAll('canvas')){
   if(!c.width||!c.height)continue;
   const r=c.getBoundingClientRect(),s=getComputedStyle(c);
   if(!r.width||!r.height||r.right<=0||r.left>=1280||r.bottom<=0||s.display==='none'||s.visibility==='hidden'||s.opacity==='0')continue;
   g.imageSmoothingEnabled=false;g.drawImage(c,r.x,r.y,r.width,r.height);
  }
  g.fillStyle='rgba(5,12,24,.94)';g.fillRect(120,761,1040,31);
  g.fillStyle='#f4d380';g.font='15px sans-serif';g.textAlign='center';
  g.fillText(cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s',640,782);
  analyser.getFloatTimeDomainData(samples);for(const v of samples)stats.peak=Math.max(stats.peak,Math.abs(v));
  stats.frames++;requestAnimationFrame(render);
 }
 render();
 const stream=canvas.captureStream(30);for(const t of mix.stream.getAudioTracks())stream.addTrack(t);
 const recorder=window.reviewRecorder=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9,opus',videoBitsPerSecond:4500000,audioBitsPerSecond:160000});
 window.capturePending=Promise.resolve();
 recorder.ondataavailable=e=>{
  if(!e.data.size)return;
  capturePending=capturePending.then(async()=>{
   const b=new Uint8Array(await e.data.arrayBuffer());let s='';
   for(let i=0;i<b.length;i+=32768)s+=String.fromCharCode(...b.subarray(i,i+32768));
   await saveCaptureChunk(btoa(s));
  });
 };
 recorder.start(1000);
 diffKey='furious';debugUnlocked=true;
 window.reviewConfig=cfg;const entry={stage:cfg.stage,role:cfg.role,kind:cfg.kind,name:cfg.name};
 if(!entry)throw Error('Missing native boss entry for '+cfg.stage);
 debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=40;if(cfg.role==='mini')spawnSubBoss(cfg.kind);else spawnBoss(cfg.kind);debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);if(cfg.role==='boss')bossActive=true;else subBossActive=true;Audio.startMusic(cfg.role==='mini'&&BOFA.music['mini'+cfg.stage]?'mini'+cfg.stage:'boss'+cfg.stage);
 return {entry,difficulty:diffKey,weapon:run.weapon,wlevel:run.wlevel,missiles:run.bombs,
   screen:{width:cv.width,height:cv.height},nativeGod:DBGT.god,currentFont:XART._src.pm27_fury_strike_28,focusedLaser:typeof LM27!=='undefined',newEncounterBanks:typeof ER28!=='undefined'};
}"""

SNAPSHOT = r"""()=>{
 const b=reviewConfig.role==='mini'?subBoss:boss,S=b?._r30,J=S&&typeof j3State==='function'?j3State(b):null;
 const M=b?._s7mod,F=b?._s9fusion,H=b?._hd1003,P=b?._pb28;
 return {seconds:+((performance.now()-captureStart)/1000).toFixed(3),state,
  stage:run.stage,difficulty:diffKey,spawned:!!debugFight?.spawned,
  hp:b?.hp,maxhp:b?.maxhp,dead:!!b?.dead,bossDefeated:reviewConfig.role==='mini'?(subBossDone&&debugFight?.spawned):bossDefeated,active:reviewConfig.role==='mini'?subBossActive:bossActive,
  mode:P?.mode||M?.mode||H?.mode||S?.mode||F?.phase||null,pursuit:P?{clock:P.clock,t:P.t,hidden:P.hidden,catchup:P.catchup,wave:P.wave,gap:P.gapX}:null,
  phase:M?(typeof s7mStage==='function'?s7mStage(M):null):J?.encounter??null,
  form:S?.v18?.form??S?.v19?.form??null,attack:H?.er28?.kind||S?.v18?.attack?.type||null,
  parts:b?._bomber?b._bomber.parts.map(p=>({id:p.id,hp:p.hp})):M?M.parts.map(p=>({id:p.id,hp:p.hp})):b?.parts?.map(p=>({id:p.id,hp:p.hp,destroyed:p.destroyed})),
  dracodia:J?{pools:{...J.hp},locked:typeof rd30Locked==='function'&&rd30Locked(b),attacks:J.attacks,book:S.v18?.seq,unlocked:J.rd30?.unlocked}:null,rebels:b?._rebels?.ships.map(q=>({key:q.key,hp:q.hp,dead:q.dead,mode:q.mode})),carrier:b?._carrier17?.parts.map(p=>({id:p.id,hp:p.hp,dead:p.dead})),twins:F?{left:F.left?.hp,right:F.right?.hp}:null,
  target:reviewBot.targetInfo,botErrors:reviewBot.errors,
  player:{x:player.x,y:player.y,dead:player.dead},weapon:run.weapon,wlevel:run.wlevel,
  missiles:run.bombs,god:DBGT.god,godBlocks:DBGT.stats?.godBlocks,deaths:DBGT.stats?.deaths,
  director:BOFCinematicDirector.current?.id,frames:captureStats.frames,
  pursuitEvents:typeof PB28!=='undefined'?PB28.events.slice(-4):[],nativeFrames:window.__bofFrames,audioPeak:captureStats.peak,newLaserMuzzleDraws:typeof LM27!=='undefined'?LM27.draws:0,heraldEvents:typeof HR28!=='undefined'?HR28.events.slice(-2):[]};
}"""


def record(stage, limit):
    OUT.mkdir(parents=True, exist_ok=True)
    folder = OUT / CONFIG['id']
    if folder.exists():
        folder = OUT / f'stage{stage}-{time.strftime("%H%M%S")}'
    folder.mkdir()
    errors, console, asset_errors, timeline = [], [], [], []
    failed_requests=[]
    port, stop = serve(str(ROOT))
    report = {'stage': stage, 'difficulty': 'furious', 'pilot': 'cole',
              'invulnerable': True, 'method': 'Native encounter spawn, real RAF, Cole with level-5 Laser and40 missiles, native GOD and input-only aiming; no enemy HP/phase/timer writes.',
              'completed': False, 'reason': 'starting'}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel='msedge',headless=True, args=[
                '--autoplay-policy=no-user-gesture-required', '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows'])
            page = browser.new_page(viewport={'width': 1280, 'height': 800})
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('requestfailed',lambda q:failed_requests.append({'url':q.url,'failure':q.failure}))
            page.on('console', lambda m: console.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
            page.on('response', lambda r: asset_errors.append({'status': r.status, 'file': r.url.split('/')[-1]}) if r.status >= 400 else None)
            page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=180000)
            page.wait_for_function('window.__bofFrames>5', timeout=180000)
            page.mouse.click(3, 3)
            page.evaluate('s=>{run.stage=s;stageLoadBegin(s);}', stage)
            page.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s);}', arg=stage, timeout=180000)
            # All preparation is outside the recording; CAPTURE starts a fresh native fight.
            page.evaluate('n=>{beginStage(n);BOFCinematicDirector.cancel();story=null;}',stage)
            if stage==8 and CONFIG['role']=='boss':
                page.wait_for_function('()=>{stageLoadTick();return v18Warm()&&bi24Warm()&&r25Warm(8)}',timeout=180000)
                page.evaluate("""()=>{
                 diffKey='furious';debugStartFight({stage:8,role:'boss',kind:'vileexistence'},{pilot:'cole'});spawnBoss('vileexistence');
                 const b=boss;for(const form of [0,8,1,6,2]){v18Enter(b,2,form);b._r30.mode='fight';b.enter=false;b._noHit=false;for(let i=0;i<24;i++){b._r30.clock=i/12;r30DrawBoss(b);}}
                }""")

            with (folder / 'capture.webm').open('wb') as raw:
                page.expose_function('saveCaptureChunk', lambda b: raw.write(base64.b64decode(b)))
                report['setup'] = page.evaluate(CAPTURE, CONFIG)
                print('START', stage, json.dumps(report['setup']), flush=True)
                last_phase = None
                next_shot = 8
                next_print = 0
                completed_at = None
                while True:
                    page.wait_for_timeout(450)
                    q = page.evaluate(SNAPSHOT)
                    adjust=OUT/'input-adjust.js'
                    if adjust.exists()and adjust.stat().st_mtime!=getattr(record,'adjusted',None):
                        page.evaluate(adjust.read_text(encoding='utf-8'));record.adjusted=adjust.stat().st_mtime
                    timeline.append(q)
                    (folder / 'live.json').write_text(json.dumps(q, indent=2), encoding='utf8')
                    phase = (q.get('mode'), q.get('phase'), q.get('form'), q['state'])
                    if phase != last_phase:
                        print('PHASE', stage, json.dumps({k: q.get(k) for k in
                              ['seconds', 'state', 'hp', 'maxhp', 'mode', 'phase', 'form']}), flush=True)
                        if q['seconds'] > 4:
                            data = page.evaluate('reviewCapture.toDataURL().split(",")[1]')
                            (folder / f'phase-{len(timeline):05}.png').write_bytes(base64.b64decode(data))
                        last_phase = phase
                    if q['seconds'] >= next_shot:
                        data = page.evaluate('reviewCapture.toDataURL().split(",")[1]')
                        (folder / f'frame-{int(q["seconds"]):04}.png').write_bytes(base64.b64decode(data))
                        next_shot += 40
                    if q['seconds'] >= next_print:
                        print('PROGRESS', stage, json.dumps({k: q.get(k) for k in
                              ['seconds', 'hp', 'mode', 'phase', 'form', 'deaths', 'audioPeak']}), flush=True)
                        next_print += 25
                    if q['bossDefeated'] and completed_at is None:
                        completed_at = q['seconds']
                    if completed_at is not None and (q['seconds'] - completed_at > 7 or q['state'] in ['debug', 'debugfade']):
                        report.update(completed=True, reason='native defeat', defeatSeconds=completed_at)
                        break
                    if q['seconds'] >= limit:
                        report['reason'] = 'recording time limit'
                        break
                    if errors or q['botErrors']:
                        report['reason'] = 'runtime error'
                        break
                report['audio'] = page.evaluate(r"""async()=>{
                 reviewBot.enabled=false;for(const k of ['a','d','w','s','j','c'])Input.keys[k]=false;
                 await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});
                 await capturePending;captureLive=false;
                 return {...captureStats,god:DBGT.god,godBlocks:DBGT.stats?.godBlocks,deaths:DBGT.stats?.deaths};
                }""")
                page.screenshot(path=str(folder / 'final.png'))
            browser.close()
    finally:
        stop()
        report.update(pageErrors=errors, consoleErrors=console, assetErrors=asset_errors,failedRequests=failed_requests,timeline=timeline)
        (folder / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    mp4 = folder / f'stage{stage}-furious.mp4'
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-threads','2','-i', str(folder / 'capture.webm'),
                    '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '160k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(mp4)], check=True)
    print('DONE', stage, report['reason'], str(mp4), flush=True)
    return folder


