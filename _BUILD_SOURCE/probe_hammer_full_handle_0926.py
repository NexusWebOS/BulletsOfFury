"""Native canvas proof that the head, shaft and hilt share the same charging shake."""
import sys, json, base64, http.server
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
out=Path('_shots/hammer_full_handle_0926');out.mkdir(exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[];report={}
fixture="""()=>{
 diffKey='normal';DIFF=DIFFS.normal;story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];smokeTrails=[];l5Rocks=[];l5RockT=9999;
 spawnBoss('chromehammer');boss.x=340;boss.y=256;boss.enter=false;boss._noHit=false;boss.hp=boss.maxhp*.35;boss._hammer.balance0922=true;
 player.x=340;player.y=410;player.invuln=1e9;player.dead=false;camX=100;boss._hammer.chainDestroyed=true;hammerStormStart(boss);
}"""
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');pg.wait_for_function('()=>window.__bofFrames>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True});pg.evaluate(fixture)
  pg.wait_for_function("()=>['arch_storm_charge_0926','arch_hammer_lightning_0926','bmbar_fill_solid'].every(k=>XART.rdy(k))")
  report['motion']=pg.evaluate("""()=>{
   const h=boss._hammer,results=[],jitter=hammerChargeJitter;boss.x=240;boss.y=300;boss.flash=0;h.empowered=false;
   ctx.save();ctx.setTransform(1,0,0,1,0,0);
   try{for(const t of [1.1,1.4,3.4]){
     h.t=t;const f=hammerStormChargeFrame(boss),r=HAMMER_CHARGE_REEL[f],k=.64,im=XART.get('arch_storm_charge_0926');
     const hx=boss.x+(r[6]-r[4])*k,hy=boss.y+(r[7]-r[5])*k,frames=[];
     for(const j of [{x:0,y:0},{x:3,y:-2},{x:-3,y:2}]){
       hammerChargeJitter=()=>j;ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);hammerChromiumPoseDraw(boss,'arch_storm_charge_0926',r,k,im);
       frames.push(ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data);
     }
     const regions=[{name:'head',x:hx-14,y:hy-15,w:28,h:30},{name:'shaft',x:hx-4,y:hy+94*k,w:8,h:20},{name:'hilt',x:hx-4,y:hy+144*k,w:8,h:15},{name:'torso',x:boss.x-30,y:boss.y+12,w:60,h:35}];
     for(let n=1;n<3;n++)for(const area of regions){
       const j=n===1?{x:3,y:-2}:{x:-3,y:2},dx=area.name==='torso'?0:j.x,dy=area.name==='torso'?0:j.y;
       let same=0,total=0,opaque=0;const width=ctx.canvas.width;
       for(let yy=Math.ceil(area.y);yy<Math.floor(area.y+area.h);yy++)for(let xx=Math.ceil(area.x);xx<Math.floor(area.x+area.w);xx++){
         const a=(yy*width+xx)*4,b=((yy+dy)*width+xx+dx)*4;total++;if(frames[0][a+3]>128)opaque++;
         if([0,1,2,3].every(c=>Math.abs(frames[0][a+c]-frames[n][b+c])<3))same++;
       }
       results.push({pose:f,region:area.name,dx,dy,match:same/total,opaque});
     }
   }}finally{hammerChargeJitter=jitter;ctx.restore();}return results;
  }""")
  pg.evaluate(fixture)
  for name,t in [('charge',3.2),('opposite',3.25)]:
   pg.evaluate("t=>{while(boss._hammer.t<t)updatePlay(1/60);powerups=[];shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60)}",t)
   data=pg.evaluate("()=>ctx.canvas.toDataURL('image/png')");(out/(name+'.png')).write_bytes(base64.b64decode(data.split(',',1)[1]))
  pg.evaluate(fixture)
  data=pg.evaluate("""async()=>{
   const stream=ctx.canvas.captureStream(30),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8',videoBitsPerSecond:3000000}),chunks=[];
   rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};const done=new Promise(resolve=>rec.onstop=()=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
   const start=performance.now();rec.start();await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();powerups=[];loop(now);if(now-start>=9000){clearInterval(timer);resolve();}},1000/60);});
   rec.stop();const result=await done;stream.getTracks().forEach(t=>t.stop());return result;
  }""")
  (out/'full_hammer_shake.webm').write_bytes(base64.b64decode(data.split(',',1)[1]));br.close()
finally:stop()
report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert not errors,errors
assert all(r['match']>.93 and r['opaque']>30 for r in report['motion']),report['motion']
