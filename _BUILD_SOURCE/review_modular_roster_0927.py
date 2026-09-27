"""Real-time Chromium inspection videos. Immunity and staged module breaks, not campaign wins."""
import ast,base64,json,http.server,sys
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/modular_roster_0927');OUT.mkdir(exist_ok=True,parents=True)
tree=ast.parse(Path('_BUILD_SOURCE/probe_polish_0927b.py').read_text(encoding='utf-8'))
SETUP=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='SETUP')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];clips=json.loads((OUT/'videos.json').read_text())['clips'] if len(sys.argv)>1 and (OUT/'videos.json').exists() else []
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1050,'height':1100});p.set_default_timeout(90000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  p.evaluate("()=>{for(const k of Object.keys(MR27_ART))XART.rdy('mr27_'+k);XART.rdy('polish_bomber');}");p.wait_for_function("()=>Object.keys(MR27_ART).every(k=>XART.rdy('mr27_'+k))&&XART.rdy('polish_bomber')")
  for stage,kind,mini,diff in [(3,'cryospear',False,'furious'),(4,'olivewarden',True,'hard'),(4,'stormsovereign',False,'hard'),(5,'spacebomber',True,'normal'),(5,'spacebomber',True,'hard'),(6,'siegebomber',True,'normal')]:
   if len(sys.argv)>1 and kind not in sys.argv[1:]:continue
   clips=[c for c in clips if not(c['kind']==kind and c['diff']==diff)]
   case={'stage':stage,'kind':kind,'mini':mini,'diff':diff,'seconds':26};p.evaluate(SETUP,case)
   p.evaluate("()=>{story=null;s6Opening=null;s6Wing=null;run.forge={};run.forgeForms={};run.wvars=[];run.weapon=0;special=null;Input.keys.j=false;for(let i=0;i<240;i++)updatePlay(1/60);}")
   print('RECORD',case,flush=True)
   data=p.evaluate(r"""async c=>{const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:1700000}),chunks=[];rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});const start=performance.now(),seen=[],snaps=[];let last='',broken=false,helpers=false,frames=0,finite=true,zoomMin=viewZoom(),zoomMax=viewZoom();rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now(),t=(now-start)/1000;player.invuln=999;powerups=[];Input.keys.arrowleft=t%8<4;Input.keys.arrowright=!Input.keys.arrowleft;Input.keys.j=false;story=null;
    if(c.kind==='stormsovereign'&&t>6&&!helpers){const H=B._s4war.shield;for(const n of H.nodes){n.dead=true;n.hp=0;}H.active=false;H.rearming=false;B._noHit=false;stage4CoreTurretSpawnMissing(B,.5);er26Set(B,'escort-crossfire');helpers=true;}
    if(t>18&&!broken){if(B._mr27){const p=mr27Shape(B,'gunL');_lastHitX=p.x;_lastHitY=p.y;_dmgBullet=null;if(B===boss)hitBoss(mr27Part(B,'gunL').hp+1);else hitSubBoss(mr27Part(B,'gunL').hp+1,p.x,p.y);}else{const q=siegeBomberParts(B).find(p=>p.id==='laserL');siegeBomberHit(B,99999,q.x,q.y,'laserL');}broken=true;}
    loop(now);frames++;zoomMin=Math.min(zoomMin,viewZoom());zoomMax=Math.max(zoomMax,viewZoom());const tag=B._er26?.mode||B._bomber?.mode;if(tag!==last){seen.push({t,state:tag});last=tag;}finite=finite&&eBullets.every(b=>Number.isFinite(b.x+b.y+b.vx+b.vy));if(snaps.length<5&&t>(snaps.length+1)*5)snaps.push(ctx.canvas.toDataURL());if(t>=c.seconds){clearInterval(timer);Input.keys.arrowleft=Input.keys.arrowright=false;resolve();}},1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return {video,snaps,seen,frames,finite,zoomMin,zoomMax};}""",case)
   name=kind+'-'+diff;(OUT/(name+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',')[1]))
   for i,s in enumerate(data.pop('snaps')):(OUT/f'{name}-review-{i}.png').write_bytes(base64.b64decode(s.split(',')[1]))
   clips.append({**case,**data});(OUT/'videos.json').write_text(json.dumps({'clips':clips,'errors':errors},indent=2),encoding='utf-8')
  br.close()
finally:stop()
assert not errors,errors
assert all(c['finite'] and c['zoomMin']==c['zoomMax']==1 for c in clips)
