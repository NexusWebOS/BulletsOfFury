"""Verify the regular authored enemy FOV in native Chromium; no substitute art."""
from pathlib import Path
import base64,json,subprocess,sys
from playwright.sync_api import sync_playwright
import imageio_ffmpeg,shoot
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/enemy_fov_1011';OUT.mkdir(exist_ok=True)
checks=[];errors=[];captures=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--mute-audio']);p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(path=str(ROOT/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.FOV_QA={draws:[],current:null};const Q=FOV_QA,base=l23FovDraw,get=XART.get,draw=ctx.drawImage;
   l23FovDraw=function(owner,B,i,point,k,width){const prev=Q.current;Q.current={stage:run.stage,progress:k,len:B.len,angle:B.angles[i],point};try{return base.apply(this,arguments);}finally{Q.current=prev;}};
   XART.get=function(k){if(Q.current)Q.current.key=k;return get.apply(this,arguments);};
   ctx.drawImage=function(){if(Q.current?.key?.startsWith('bmfx_fov_'))Q.draws.push({...Q.current,args:arguments.length});return draw.apply(this,arguments);};
  }''')
  def setup(stage):
   p.evaluate('s=>EA11.setup(s,"normal")',stage)
   p.wait_for_function('()=>{stageLoadTick();l23FovWarm();return stageLoadInfo(run.stage).ready&&["green","yellow","red"].every(c=>XART.rdy("bmfx_fov_"+c+"_tall"));}',polling=50)
   p.evaluate('()=>{stagePlan=[];aiQueue=[];s6Opening=s6Wing=null;enemies=[];spawnClock=9999;}')
  def snap(name):
   (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')));captures.append(name+'.png')
  kinds=['s1boatgun','firejet1002','ac10icejet','s4heavyjet','s5frigate','s6lancer','s7tank','s8deathorb','s9interceptor']
  for stage,kind in enumerate(kinds,1):
   setup(stage)
   p.evaluate('k=>{spawnEnemy(k,worldWidth()/2-50,115,{inPlace:true});window.E=enemies.at(-1);E._entry=0;}',kind)
   for color,k in [('green',.18),('yellow',.5),('red',.88)]:
    q=p.evaluate('k=>{FOV_QA.draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);FOV_QA.draws=[];ctx.save();ctx.translate(-camX,0);combatWarningDraw(E,{x:E.x,y:E.y+E.h*.32,ex:player.x,ey:player.y,progress:k,width:24,fieldOnly:true});ctx.restore();return FOV_QA.draws;}',k)
    check(f'Stage {stage} {color}: full regular FOV plate',q and all(d['key']=='bmfx_fov_'+color+'_tall' and d['args']==5 for d in q),q)
    if color=='red':snap(f'stage-{stage}-red')
  for method in ['line','legacy-gate','alert-only']:
   q=p.evaluate('''m=>{FOV_QA.draws=[];const q={x:player.x-60,y:100,ex:player.x+20,ey:300,width:30,progress:.8};
    if(m==='line')combatWarningDraw(E,{...q,laneShape:'line',fieldOnly:true});
    else if(m==='legacy-gate')s67LaneBand(q.x,q.y,q.ex,q.ey,q.width,.8,1);
    else combatWarningDraw(E,{...q,alertOnly:true});return FOV_QA.draws;}''',method)
   check(method+': intended field rendering',not q if method=='alert-only' else q and all(d['args']==5 and abs(d['len']-(80**2+200**2)**.5)<.01 for d in q),q)
  # Native controller windups, not injected warning objects.
  for stage,kind,name in [(6,'s6lancer','queued-fighter'),(8,'s8deathorb','alien-orb')]:
   setup(stage);p.evaluate('k=>{spawnEnemy(k,worldWidth()/2-40,85,{inPlace:true});window.E=enemies.at(-1);}',kind)
   phases={};seen=[]
   for batch in range(120):
    q=p.evaluate('''()=>{for(let i=0;i<3;i++){player.invuln=40002;updatePlay(1/60);}FOV_QA.draws=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return FOV_QA.draws;}''')
    seen+=q
    for color in ['green','yellow','red']:
     if color not in phases and any(d['key']=='bmfx_fov_'+color+'_tall' for d in q):snap(name+'-'+color);phases[color]=True
    if len(phases)==3:break
    p.wait_for_timeout(5)
   check(name+': real AI shows green, yellow and red full FOV',len(phases)==3 and all(d['args']==5 for d in seen),list(phases))
   # Record four seconds around a live attack and recovery.
   writer=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-r','20','-i','pipe:0','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))],stdin=subprocess.PIPE)
   for frame in range(100):
    p.evaluate('()=>{for(let i=0;i<3;i++){player.invuln=40002;updatePlay(1/60);}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
    writer.stdin.write(base64.b64decode(p.evaluate('cv.toDataURL("image/jpeg",.9).split(",")[1]')))
    if frame%10==0:p.wait_for_timeout(5)
   writer.stdin.close();check(name+': gameplay recording encodes',writer.wait()==0)
  check('No browser page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
(OUT/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,captures=captures),indent=2),encoding='utf-8')
cards=''.join(f'<figure><img src="stage-{i}-red.png"><figcaption>Stage {i}</figcaption></figure>' for i in range(1,10))
(OUT/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Regular enemy FOV</title><style>body{background:#08111d;color:#dcecff;font:16px system-ui;max-width:1180px;margin:32px auto;padding:0 20px}h1{color:#91efb3}p{line-height:1.6;max-width:900px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}figure{margin:0}img,video{width:100%;border:1px solid #37536a}figcaption{padding:10px}h2{margin-top:30px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}a{color:#8ed8ff}@media(max-width:700px){.grid,.pair{grid-template-columns:1fr}}</style><h1>Regular FOV · All enemy warnings</h1><p>The full authored green / yellow / red FOV now replaces the old rectangular bands. Muzzles, aim, committed endpoints and attack timing keep their existing owners.</p><div class="pair"><section><h2>Stage 6 · live fighter</h2><video controls loop muted src="queued-fighter.mp4" poster="queued-fighter-red.png"></video></section><section><h2>Stage 8 · live alien orb</h2><video controls loop muted src="alien-orb.mp4" poster="alien-orb-red.png"></video></section></div><h2>Native field checks · Stages 1–9</h2><p>One isolated warning per stage verifies the shared renderer against each biome. The videos above show natural AI windups, firing and recovery with a protected observer.</p><div class="grid">'''+cards+'</div><p><a href="checks.json">Verification report</a></p>',encoding='utf-8')
print(json.dumps(dict(checks=len(checks),failures=[q['name'] for q in checks if not q['passed']],errors=errors)))
sys.exit(1 if errors or any(not q['passed'] for q in checks) else 0)
