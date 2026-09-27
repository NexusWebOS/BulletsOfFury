"""Record a focused real Chromium Stage 5 animation fixture (invulnerable inspection)."""
import sys,base64,json,http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/hammer_authored_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})
  pg.evaluate("""()=>{diffKey='furious';DIFF=DIFFS.furious;story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];spawnBoss('chromehammer');boss.x=(camLeftX()+camRightX())/2;boss.y=VH*.34;boss.enter=false;boss._noHit=false;boss._hammer.balance0922=true;player.invuln=1e9;run.bombs=20;hammerWhirlStart(boss);}""")
  pg.wait_for_function("()=>['arch_whirlwind_0926','arch_orbital_sweep_0926','arch_chromium_beam_0926'].every(k=>XART.rdy(k))")
  data=pg.evaluate("""async()=>{
    const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:2500000}),chunks=[],seen=new Set();
    rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
    const finished=new Promise(resolve=>{rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));}});
    const started=performance.now();let switched=false,elapsed=0;
    rec.start();
    await new Promise(resolve=>{
      const id=setInterval(()=>{
        const now=performance.now();elapsed=(now-started)/1000;
        Input.keys.arrowleft=elapsed%6<3;Input.keys.arrowright=!Input.keys.arrowleft;
        if(!switched&&elapsed>10){switched=true;boss.x=(camLeftX()+camRightX())/2;boss.y=VH*.34;boss._noHit=false;hammerState(boss,'mega_charge');}
        loop(now);seen.add(boss?._hammer?.state);
        if(elapsed>=23){clearInterval(id);Input.keys.arrowleft=false;Input.keys.arrowright=false;resolve();}
      },1000/60);
    });
    rec.stop();const video=await finished;stream.getTracks().forEach(t=>t.stop());
    return {video,states:[...seen],seconds:elapsed,fixture:'Furious Stage 5; invulnerable inspection; whirlwind started explicitly; chromium charge queued at ten seconds'};
  }""")
  (out/'stage5_attack_review.webm').write_bytes(base64.b64decode(data.pop('video').split(',',1)[1]))
  data['errors']=errors;(out/'video.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
  br.close()
finally:stop()
assert not errors

