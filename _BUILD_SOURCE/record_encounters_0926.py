"""Focused real Chromium previews. Invulnerable fixture, keyboard flight, native renderer."""
import sys,json,base64,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/encounters_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];selected=set(sys.argv[1:]);clips=[]
if selected and (out/'videos.json').exists():
 clips=[c for c in json.loads((out/'videos.json').read_text())['clips'] if c['kind'] not in selected]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1000})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  for stage,kind,mini,seconds in [(2,'magmaward',True,28),(3,'frostcruiser',True,40),(3,'cryospear',False,42),(4,'olivewarden',True,32),(4,'stormsovereign',False,34)]:
   if selected and kind not in selected:continue
   print('RECORD',kind,flush=True)
   pg.evaluate(sh.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   pg.evaluate("""c=>{
     diffKey='furious';DIFF=DIFFS.furious;story=null;stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];
     boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;run.pilot='cole';player.reset();player.invuln=2;
     player.x=worldWidth()/2;player.y=VH*.79;camX=player.x-VW/2;
     if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);
     const b=c.mini?subBoss:boss;b._be=null;b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=b._er26.home;b._drawY=b.y;
     b._er26.from={x:b.x,y:b.y};b._er26.to={x:b.x,y:b.y};b.t=0;window.testActor=b;
   }""",{'kind':kind,'mini':mini})
   pg.wait_for_function("()=>['lz_bomb',SHIPBOSS[testActor._ship].key,'mwfx_fireball_3','l23fx_rime_orb_3'].map(k=>XART.rdy(k)).every(Boolean)",timeout=60000)
   data=pg.evaluate("""async cfg=>{
     const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:2400000}),chunks=[];
     rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
     const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
     const start=performance.now(),seen=[],shots=[];let last='',half=false,quarter=false;
     rec.start();await new Promise(resolve=>{
       const timer=setInterval(()=>{
         const now=performance.now(),elapsed=(now-start)/1000,b=testActor;
         player.invuln=2;Input.keys.arrowleft=elapsed%5<2.5;Input.keys.arrowright=!Input.keys.arrowleft;
         powerups=[];
         if(cfg.stage===4){
           if(!half&&elapsed>12){half=true;b.hp=b.maxhp*.49;if(!cfg.mini){for(const n of b._s4war.shield.nodes)stage4ShieldDestroyNode(b,n);stage4ShieldBeginRearm(b,.5);}}
           if(!quarter&&elapsed>23){quarter=true;b.hp=b.maxhp*.24;if(!cfg.mini){for(const n of b._s4war.shield.nodes)stage4ShieldDestroyNode(b,n);stage4ShieldBeginRearm(b,.25);}}
         }
         loop(now);
         const tag=b._er26.mode+' / '+b._er26.form;
         if(tag!==last){seen.push({seconds:+elapsed.toFixed(2),state:tag});last=tag;}
         const role=cfg.mini?'mini':'boss',nuke=typeof S3_THERMO_STRIKE!=='undefined'&&S3_THERMO_STRIKE[role];
         if(nuke&&nuke.old===b){
           const labels=nuke.t>1.35&&nuke.t<1.65?'missile':nuke.t>2.05&&nuke.t<2.45?'whiteout':nuke.t>3.9?'reveal':null;
           if(labels&&!shots.some(s=>s.label===labels))shots.push({label:labels,t:nuke.t,png:ctx.canvas.toDataURL('image/png')});
         }
         if(elapsed>=cfg.seconds){clearInterval(timer);Input.keys.arrowleft=false;Input.keys.arrowright=false;resolve();}
       },1000/60);
     });rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());
     return {video,seen,shots,fixture:'Furious, invulnerable keyboard flight. Stage 4 HP gates exercised at 12 and 23 seconds; no player damage used for tuning claims.'};
   }""",{'stage':stage,'kind':kind,'mini':mini,'seconds':seconds})
   (out/(kind+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',')[1]))
   for s in data.pop('shots'):(out/(kind+'_'+s['label']+'.png')).write_bytes(base64.b64decode(s['png'].split(',')[1]))
   clips.append({'stage':stage,'kind':kind,'seconds':seconds,**data});(out/'videos.json').write_text(json.dumps({'clips':clips,'errors':errors},indent=2))
  br.close()
finally:stop()
print(json.dumps({'clips':clips,'errors':errors},indent=2));assert not errors,errors
