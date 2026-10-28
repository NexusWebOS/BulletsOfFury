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
OUT = ROOT / '_shots' / 'warden_lunge_1028' / 'fight'

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
  const A=reviewBot;if(!A.enabled)return;
  A.tick++;
  if(cfg.stage===7&&elapsed<28){for(const k of ['a','d','w','s','j','k','c'])K[k]=false;const holdX=worldWidth()/2,holdY=VH-55;K.a=player.x>holdX+4;K.d=player.x<holdX-4;K.w=player.y>holdY+4;K.s=player.y<holdY-4;return;}

  if(state!==GS.PLAY||player.dead||player.out){for(const k of ['a','d','w','s','j','c'])K[k]=false;return;}
  const b=bossActive&&boss&&!boss.dead?boss:null;
  let list=b?retinaBossTargets(b).filter(t=>!t.dead&&t.hp>0&&Number.isFinite(t.x+t.y)):[];
  list=list.filter(t=>t.y>=PLAY.y-180&&t.y<VH-20);
  let target=list.find(t=>targetKey(t)===A.targetKey);
  if(!target){
   target=list.sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x))[0]||null;
   A.targetKey=target?targetKey(target):'';A.lastHp=target?.hp;A.lastProgress=elapsed;
  }
  if(target&&target.hp<A.lastHp-.01){A.lastProgress=elapsed;A.lastHp=target.hp;}
  if(target&&elapsed-A.lastProgress>7&&list.length>1){
   const idx=list.indexOf(target);target=list[(idx+1)%list.length];
   A.targetKey=targetKey(target);A.lastHp=target.hp;A.lastProgress=elapsed;
  }
  const fallback=(b?.x??worldWidth()/2)+Math.sin(elapsed*.7)*65;
  const tx=Math.max(22,Math.min(worldWidth()-22,target?.x??fallback));
  const ty=Math.max(PLAY.y+PLAY.h*.72,Math.min(PLAY.y+PLAY.h-32,(target?.y??100)+175));
  K.a=player.x>tx+9;K.d=player.x<tx-9;
  K.w=player.y>ty+9;K.s=player.y<ty-9;
  // Release before Cole's native Fusion overload; all weapon charge/damage remains native.
  K.j=elapsed%0.9<0.62;
  K.c=!!b;
  if(b&&(run.bombs|0)>0&&elapsed-A.lastMissile>1.1){Input.injectTap('k');A.lastMissile=elapsed;}
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
  g.fillText('STAGE '+cfg.stage+' / FURIOUS / COLE / INVULNERABLE INPUT BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s',640,782);
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
 const entry=debugFightFor(cfg.stage,'boss');
 if(!entry)throw Error('Missing native boss entry for '+cfg.stage);
 debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;
 return {entry,difficulty:diffKey,weapon:run.weapon,wlevel:run.wlevel,missiles:run.bombs,
   screen:{width:cv.width,height:cv.height},nativeGod:DBGT.god};
}"""

SNAPSHOT = r"""()=>{
 const b=boss,S=b?._r30,J=S&&typeof j3State==='function'?j3State(b):null;
 const M=b?._s7mod,F=b?._s9fusion;
 return {seconds:+((performance.now()-captureStart)/1000).toFixed(3),state,
  stage:run.stage,difficulty:diffKey,spawned:!!debugFight?.spawned,
  hp:b?.hp,maxhp:b?.maxhp,dead:!!b?.dead,bossDefeated,active:bossActive,
  mode:M?.mode||S?.mode||F?.phase||null,
  phase:M?(typeof s7mStage==='function'?s7mStage(M):null):J?.encounter??null,
  form:S?.v18?.form??S?.v19?.form??null,attack:S?.v18?.attack?.type||null,
  parts:M?M.parts.map(p=>({id:p.id,hp:p.hp})):b?.parts?.map(p=>({id:p.id,hp:p.hp,destroyed:p.destroyed})),
  twins:F?{left:F.left?.hp,right:F.right?.hp}:null,
  target:reviewBot.targetInfo,botErrors:reviewBot.errors,
  player:{x:player.x,y:player.y,dead:player.dead},weapon:run.weapon,wlevel:run.wlevel,
  missiles:run.bombs,god:DBGT.god,godBlocks:DBGT.stats?.godBlocks,deaths:DBGT.stats?.deaths,
  director:BOFCinematicDirector.current?.id,frames:captureStats.frames,
  nativeFrames:window.__bofFrames,audioPeak:captureStats.peak};
}"""


def record(stage, limit):
    OUT.mkdir(parents=True, exist_ok=True)
    folder = OUT / f'stage{stage}'
    if folder.exists():
        folder = OUT / f'stage{stage}-{time.strftime("%H%M%S")}'
    folder.mkdir()
    errors, console, asset_errors, timeline = [], [], [], []
    port, stop = serve(str(ROOT))
    report = {'stage': stage, 'difficulty': 'furious', 'pilot': 'cole',
              'invulnerable': True, 'method': 'Native boss-mode entry, real RAF, input-only aiming; no enemy HP/phase writes.',
              'completed': False, 'reason': 'starting'}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel='msedge', args=[
                '--autoplay-policy=no-user-gesture-required', '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows'])
            page = browser.new_page(viewport={'width': 1280, 'height': 800})
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: console.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
            page.on('response', lambda r: asset_errors.append({'status': r.status, 'file': r.url.split('/')[-1]}) if r.status >= 400 else None)
            page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=180000)
            page.wait_for_function('window.__bofFrames>5', timeout=180000)
            page.mouse.click(3, 3)
            page.evaluate('s=>{run.stage=s;stageLoadBegin(s);}', stage)
            page.wait_for_function('s=>{stageLoadTick();return stageLoadReady(s);}', arg=stage, timeout=180000)
            with (folder / 'capture.webm').open('wb') as raw:
                page.expose_function('saveCaptureChunk', lambda b: raw.write(base64.b64decode(b)))
                report['setup'] = page.evaluate(CAPTURE, {'stage': stage})
                print('START', stage, json.dumps(report['setup']), flush=True)
                last_phase = None
                next_shot = 8
                next_print = 0
                completed_at = None
                while True:
                    page.wait_for_timeout(450)
                    q = page.evaluate(SNAPSHOT)
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
                    if completed_at is not None and (q['seconds'] - completed_at > 25 or q['state'] in ['debug', 'debugfade']):
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
        report.update(pageErrors=errors, consoleErrors=console, assetErrors=asset_errors, timeline=timeline)
        (folder / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    mp4 = folder / f'stage{stage}-furious.mp4'
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-y', '-i', str(folder / 'capture.webm'),
                    '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '160k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(mp4)], check=True)
    print('DONE', stage, report['reason'], str(mp4), flush=True)
    return folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stages', default='7,8,9')
    parser.add_argument('--limit', type=float, default=1200)
    parser.add_argument('--out', help='Separate recording folder within this workspace')
    args = parser.parse_args()
    if args.out:
        selected=(ROOT/args.out).resolve()
        if not selected.is_relative_to(ROOT):
            raise ValueError('Recording output must stay in the workspace')
        OUT=selected
    for value in args.stages.split(','):
        record(int(value), args.limit)
