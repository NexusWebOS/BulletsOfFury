"""Real-time native canvas review clips; isolated, invulnerable inspection fixtures."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from probe_late_game_0927 import SETUP
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/late_game_0927');port,stop=sh.serve(sh.GAME);errors=[];clips=[];selected=set(sys.argv[1:])
if selected and (out/'videos.json').exists():clips=[c for c in json.loads((out/'videos.json').read_text())['clips'] if c['kind'] not in selected]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  for stage,kind,mini,seconds,diff in [(7,'dualscoopdredger',True,26,'hard'),(7,'sludgeemperor',False,40,'hard'),(9,'voidhorizon',True,26,'furious'),(9,'tidalfusion',False,40,'hard'),(6,'rebelsquad',False,24,'normal')]:
   if selected and kind not in selected:continue
   pg=br.new_page(viewport={'width':1100,'height':1100});pg.set_default_timeout(90000)
   pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF);pg.wait_for_timeout(70)
   cfg={'stage':stage,'kind':kind,'mini':mini,'diff':diff,'seconds':seconds};pg.evaluate(SETUP,cfg)
   pg.evaluate('()=>late27Warm()');pg.wait_for_function("()=>['cfx_stage7_warden_walk','cfx_stage7_warden_cannon','warpcrystallance_3','tidaltorpedo_3'].map(k=>XART.rdy(k)).every(Boolean)",timeout=60000)
   print('RECORD',kind,flush=True)
   data=pg.evaluate(r'''async cfg=>{
    const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:2100000}),chunks=[];
    rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
    const done=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
    const seen=[],shots=[],start=performance.now();let last='',fusion=false,stun=false,hyper=false;rec.start();
    await new Promise(resolve=>{const timer=setInterval(()=>{
     const now=performance.now(),elapsed=(now-start)/1000,b=testActor;player.invuln=2;powerups=[];
     Input.keys.arrowleft=elapsed%6<3;Input.keys.arrowright=!Input.keys.arrowleft;
     if(b._s9fusion&&!fusion&&elapsed>14){fusion=true;for(const w of [b._s9fusion.left,b._s9fusion.right]){b._s9fusion.hit=w;s9FusionHit(b,1e6);}}
     if(b._s9rift&&elapsed>15)b._s9rift.core.hp=b._s9rift.core.maxhp*.48;
     if(b._s7warden&&elapsed>24&&!stun){stun=true;b._s7warden.noHit=false;s7WardenHit(b,b.hp-b.maxhp*.74,b.x,b.y);}
     if(b._s7warden&&elapsed>31&&!hyper){hyper=true;b._s7warden.noHit=false;s7WardenHit(b,b.hp-b.maxhp*.49,b.x,b.y);}
     loop(now);const tag=(b._s7warden?.final.phase||b._s9fusion?.phase||'fight')+' / '+(b._late27?.mode||b._rebels?.ships.map(q=>q.mode).join(','));
     if(tag!==last){seen.push({seconds:+elapsed.toFixed(2),state:tag});last=tag;}
     if(shots.length<8&&elapsed>(shots.length+1)*4)shots.push({t:elapsed,png:ctx.canvas.toDataURL()});
     if(elapsed>=cfg.seconds){clearInterval(timer);Input.keys.arrowleft=Input.keys.arrowright=false;resolve();}
    },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return {video,seen,shots};
   }''',cfg)
   (out/(kind+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',')[1]))
   for i,s in enumerate(data.pop('shots')):(out/f'{kind}_video_{i}.png').write_bytes(base64.b64decode(s['png'].split(',')[1]))
   clips.append({**cfg,**data});(out/'videos.json').write_text(json.dumps({'clips':clips,'errors':errors,'fixture':'Invulnerable isolated encounters, keyboard movement, forced HP gates for transition inspection. Native loop and canvas. Not campaign victories or difficulty proof.'},indent=2));pg.close()
  br.close()
finally:stop()
assert not errors,errors
