"""Native Chromium muzzle/charge recordings, using shoot.py's real renderer."""
import ast,base64,http.server,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/muzzles_0926');out.mkdir(exist_ok=True,parents=True)
tree=ast.parse(Path('_BUILD_SOURCE/verify_weapon_feedback_0926.py').read_text())
reset=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='RESET' for t in n.targets))
port,stop=sh.serve(sh.GAME);errors=[];selected=set(sys.argv[1:]);clips=[]
if selected and (out/'videos.json').exists():
 clips=[c for c in json.loads((out/'videos.json').read_text())['clips'] if c['name'] not in selected]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1100})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF);pg.wait_for_timeout(50)
  pg.evaluate('()=>{window.muzzleFixtureReset='+reset+';}')
  pg.wait_for_function('()=>Object.values(WM26_REELS).flatMap(r=>Array.from({length:r.n},(_,i)=>XART.rdy(r.key+i))).every(Boolean)',timeout=60000)
  specs=[
   {'name':'player-weapons','stage':4,'scenes':[{'pilot':'cole','weapon':w,'seconds':3} for w in [0,1,2,3,5,7]]},
   {'name':'player-specials','stage':4,'scenes':[{'pilot':'maverick','seconds':4,'special':True,'hold':2.2},{'pilot':'falva','seconds':7,'special':True,'hold':5.2},{'pilot':'decker','seconds':3},{'pilot':'freezer','weapon':4,'seconds':3},{'pilot':'yuri','seconds':3,'special':True}]},
   *[{'name':kind,'stage':stage,'kind':kind,'mini':mini,'seconds':14} for kind,stage,mini in [('magmaward',2,True),('olivewarden',4,True),('stormsovereign',4,False)]]]
  for cfg in specs:
   if selected and cfg['name'] not in selected:continue
   print('RECORD',cfg['name'],flush=True)
   pg.evaluate(sh.SETUP,{'state':'PLAY','stage':cfg['stage'],'pilot':'cole','invuln':True});pg.evaluate(reset,{})
   pg.evaluate("""c=>{window.testActor=null;if(c.kind){diffKey='furious';DIFF=DIFFS.furious;if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);const b=c.mini?subBoss:boss;testActor=b;b.enter=false;b._be=null;b._noHit=false;b.x=worldWidth()/2;b.y=b._er26.home;b._drawY=b.y;b._er26.from={x:b.x,y:b.y};b._er26.to={x:b.x,y:b.y};}}""",cfg)
   pg.wait_for_timeout(120)
   data=pg.evaluate("""async cfg=>{
     const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:2000000}),chunks=[];
     rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
     const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
     let si=-1;const seen=[],total=cfg.seconds||cfg.scenes.reduce((s,c)=>s+c.seconds,0),start=performance.now();
     rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{
       const now=performance.now(),elapsed=(now-start)/1000;let local=elapsed,c=null;
       if(cfg.scenes){let i=0;for(;i<cfg.scenes.length-1&&local>=cfg.scenes[i].seconds;i++)local-=cfg.scenes[i].seconds;c=cfg.scenes[i];
         if(si!==i){si=i;if(special)endSpecial();muzzleFixtureReset(c);run.stage=cfg.stage;curStage=STAGES[cfg.stage-1];
           if(c.special)startSpecial();if(c.pilot==='decker'){run.dkT=15;dkAmmo=3;dkReload=0;}
           if(c.pilot==='freezer')run.wvars[4]='icebreath';
           seen.push({seconds:+elapsed.toFixed(2),pilot:c.pilot,weapon:c.weapon||0,special:!!c.special});}
       }
       player.invuln=c?0:2;powerups=[];Input.keys.arrowleft=elapsed%1.2<.6;Input.keys.arrowright=!Input.keys.arrowleft;
       for(const k of keybind.fire)Input.keys[k]=!!c&&local<(c.hold||c.seconds);
       loop(now);
       if(elapsed>=total){clearInterval(timer);Input.keys.arrowleft=Input.keys.arrowright=false;for(const k of keybind.fire)Input.keys[k]=false;resolve();}
     },1000/60);});rec.stop();const video=await done;stream.getTracks().forEach(t=>t.stop());return {video,seen,seconds:total};
   }""",cfg)
   (out/(cfg['name']+'.webm')).write_bytes(base64.b64decode(data.pop('video').split(',')[1]));clips.append({'name':cfg['name'],**data})
   (out/'videos.json').write_text(json.dumps({'clips':clips,'errors':errors,'fixture':'Invulnerable isolated inspection scenes; native loop, keyboard firing and movement. Not campaign balance proof.'},indent=2))
  br.close()
finally:stop()
print(json.dumps({'clips':clips,'errors':errors},indent=2));assert not errors,errors
