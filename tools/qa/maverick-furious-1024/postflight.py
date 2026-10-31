"""Read-only checks after the recording. No shipping edits or campaign claims."""
from pathlib import Path
import asyncio, functools, http.server, threading, json, subprocess, re, sys
import imageio_ffmpeg
from playwright.async_api import async_playwright
import record_campaign as C
W=Path(__file__).resolve().parent; O=W/'review'; FF=imageio_ffmpeg.get_ffmpeg_exe()

def media():
 out={}
 for name in ['Maverick-Furious-Beta-Playthrough.mp4','Maverick-Story-Replays.mp4']:
  p=O/name
  if not p.exists():continue
  r=subprocess.run([FF,'-hide_banner','-i',str(p)],capture_output=True,text=True)
  info=[s.strip()for s in r.stderr.splitlines()if any(x in s for x in ['Duration:','Video:','Audio:'])]
  samples=[]
  for t in ([3,475,1180,2800,3550]if 'Playthrough'in name else[5,80]):
   r=subprocess.run([FF,'-v','info','-ss',str(t),'-i',str(p),'-t','3','-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
   samples.append({'time':t,'exitCode':r.returncode,'levels':[s.strip()for s in r.stderr.splitlines()if 'mean_volume:'in s or 'max_volume:'in s]})
  out[name]={'bytes':p.stat().st_size,'streams':info,'audioSamples':samples}
 (O/'media-verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

async def native():
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(C.Handler,directory=str(C.R)));server.daemon_threads=True
 threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_address[1]}'
 errors=[];result={}
 async with async_playwright()as pw:
  b=await pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  p=await b.new_page(viewport={'width':1280,'height':720});p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(url,wait_until='load',timeout=180000);await p.wait_for_function('window.__bofFrames>5',timeout=120000)
  result['retryAssets']=await p.evaluate('''async()=>{const paths=['assets/game/shared/combat/modular_roster_0927/rime.png','assets/game/levels/stage_05/boss/hammer_redesign_1020/blue_throw/09.png'];const out=[];for(const path of paths){const r=await fetch(path);const blob=await r.blob();const im=await createImageBitmap(blob);out.push({path,status:r.status,bytes:blob.size,width:im.width,height:im.height});im.close();}return out;}''')
  result['resolvedPortrait']=await p.evaluate('''()=>{const im=XART.get('fb1002_hammer_portrait');return im?{kind:im.constructor.name,path:im.src?.split(location.origin+'/')[1]||null,width:im.naturalWidth||im.width,height:im.naturalHeight||im.height}:null;}''')
  # A deterministic call sequence confirms timing of the shared flash gate, not its
  # complete on-screen duty under every attacker. Restore its clock immediately.
  result['nativeHitGate']=await p.evaluate('''()=>{const clock=GP4.clock,t={flash:0,hp:100,_mr27:true};const rows=[];try{for(const at of [10,10.05,10.15,10.30,10.45]){const dt=rows.length?at-rows.at(-1).at:0;t.flash=Math.max(0,t.flash-dt);GP4.clock=at;const before=t.flash;markHit(t);rows.push({at,before,after:t.flash,next:t._gp4FlashNext});}}finally{GP4.clock=clock;}return rows;}''')
  if '--gate-only' in sys.argv:
   result['pageErrors']=errors;await b.close();server.shutdown()
   (O/'hit-gate-probe.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True);return
  # Native stage four run with no recorder, no screenshots and no encoder running.
  # This sample is deliberately labelled non-matched: it is not the campaign loadout.
  await p.evaluate('''()=>{diffKey='furious';pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');run.mode='arcade';startRun(4);DBGT.god=true;window.perfProbe={times:[],states:{},last:0};const tick=n=>{const q=perfProbe;if(q.last)q.times.push(n-q.last);q.last=n;q.states[state]=(q.states[state]||0)+1;if(!q.stop)requestAnimationFrame(tick);};requestAnimationFrame(tick);}''')
  await asyncio.sleep(35)
  result['unrecordedNonMatchedProbe']=await p.evaluate('''()=>{perfProbe.stop=true;const a=perfProbe.times.sort((a,b)=>a-b);return{seconds:a.reduce((x,y)=>x+y,0)/1000,frames:a.length,mean:a.reduce((x,y)=>x+y,0)/a.length,p50:a[Math.floor(a.length*.5)],p95:a[Math.floor(a.length*.95)],p99:a[Math.floor(a.length*.99)],max:a.at(-1),states:perfProbe.states,stage:run.stage,pilot:run.pilot,diff:diffKey,phase:bossActive?boss.kind:subBossActive?subBoss.kind:null};}''')
  result['pageErrors']=errors;await b.close();server.shutdown()
 (O/'postflight-native.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)

if __name__=='__main__':
 if '--gate-only' not in sys.argv:media()
 asyncio.run(native())
