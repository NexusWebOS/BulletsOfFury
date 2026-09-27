"""Native canvas inspection clips, with disclosed invulnerability/forced module breaks."""
import json,base64,http.server
from pathlib import Path
import shoot as sh
from probe_stage7_modular_0927 import SETUP
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
OUT=Path('_shots/toxic_modular_0927');port,stop=sh.serve(sh.GAME);errors=[];clips=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  for name,mini,seconds,breaks in [('tank',True,25,False),('warden_attacks',False,49,False),('warden_parts',False,40,True)]:
   p=br.new_page(viewport={'width':1100,'height':1100});p.set_default_timeout(100000)
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(70)
   p.evaluate(SETUP,{'mini':mini,'diff':'hard'});p.wait_for_function("()=>Object.keys(S7M_ART).map(k=>XART.rdy('s7m_'+k)).every(Boolean)",timeout=60000)
   if breaks:p.evaluate("()=>{s7mSet(B,'recover');B.y=175;B._s7FinalNoBar=false;}")
   print('RECORD',name,flush=True)
   data=p.evaluate(r'''async c=>{
    const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:1900000}),chunks=[];
    rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
    const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
    const seen=[],snaps=[],start=performance.now();let last='',event=0;const events=[[3,'gunL'],[6,'frontL'],[9,'frontR'],[13,'rearL'],[16,'rearR'],[20,'shield'],[28,'gunR'],[36,'core']];rec.start();
    await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;player.invuln=3;powerups=[];
     Input.keys.arrowleft=t%7<3.5;Input.keys.arrowright=!Input.keys.arrowleft;Input.keys.j=!c.breaks&&t>19;
     if(c.breaks&&event<events.length&&t>=events[event][0]){const id=events[event++][1];s7mSet(B,'recover');if(id==='shield'||id==='core')s7mHit(B,1e6,0,0,'core');else s7mHit(B,1e6,0,0,id);if(id==='shield'||id==='gunR')B._s7mod.seq=0;}
     loop(now);const tag=B._s7mod.mode+'/'+s7mStage(B._s7mod);if(tag!==last){seen.push({t:+t.toFixed(2),state:tag});last=tag;}
     if(snaps.length<9&&t>(snaps.length+1)*4)snaps.push(ctx.canvas.toDataURL());
     if(t>=c.seconds){clearInterval(timer);Input.keys.arrowleft=Input.keys.arrowright=Input.keys.j=false;resolve();}
    },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return{video,seen,snaps};
   }''',{'seconds':seconds,'breaks':breaks})
   (OUT/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',')[1]))
   for i,shot in enumerate(data.pop('snaps')):(OUT/f'{name}_video_{i}.png').write_bytes(base64.b64decode(shot.split(',')[1]))
   clips.append({'name':name,'seconds':seconds,'forcedModules':breaks,**data});(OUT/'videos.json').write_text(json.dumps({'clips':clips,'errors':errors,'fixture':'Native game loop/canvas. Hard difficulty, invulnerable pilot, keyboard movement; parts clip forces named module destruction. Silent visual recordings, not campaign victories.'},indent=2));p.close()
  br.close()
finally:stop()
assert not errors,errors
