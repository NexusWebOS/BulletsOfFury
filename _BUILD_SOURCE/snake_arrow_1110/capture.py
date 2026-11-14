from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import sys,json,base64,io
R=Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent;O=W.parents[1]/'outputs/snake-arrow';sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));errors=[];checks=[];rows=[];frames=[]
def shot(p):return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")))).convert('RGB').resize((480,512),Image.Resampling.NEAREST)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:300])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate("()=>{EA11.setup(7,'furious');stagePlan=[];enemies=[];powerups=[];CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;DBGT.god=false;player.invuln=99999;spawnSubBoss('dualscoopdredger');window.B=subBoss;}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&sj98Ready()}');p.evaluate(STEP,100)
  p.evaluate('()=>{window.arrowCalls=[];const orig=sj123Blit;sj123Blit=function(n,f,x,y){if(n==="arrows")arrowCalls.push({f,x,y});return orig(n,f,x,y);};}')
  for count in [2,1]:
   if count==1:p.evaluate('()=>{B._sj98.actors[0].dead=true;}')
   for run in range(4):
    p.evaluate('(i)=>{sj123Side(B,i);}',run)
    for t in [.1,.5,.9]:
     p.evaluate('(t)=>{B._sj120.t=t;arrowCalls=[];}',t);p.evaluate(STEP,1);r=p.evaluate('({count:arrowCalls.length,calls:arrowCalls,expected:B._sj98.actors.filter(a=>!a.dead).map(a=>({x:a.to.x>a.from.x?camLeftX()+34:camRightX()-34,right:a.to.x>a.from.x})),hp:B.hp})');rows.append({'live':count,'pass':run,'t':t,**r});checks.append(r['count']==count and all(abs(a['x']-e['x'])<.01 for a,e in zip(r['calls'],r['expected'])))
  p.evaluate('()=>{B._sj98.actors[0].dead=false;sj123Side(B,0);}')
  for i in range(72):p.evaluate(STEP,2);frames.append(shot(p))
  p.evaluate('()=>{sj123Side(B,0);B._sj120.t=.55;}');p.evaluate(STEP,1);shot(p).save(O/'one-arrow-per-snake.png');br.close()
finally:stop()
pal=frames[15].quantize(colors=128);q=[f.quantize(palette=pal,dither=Image.Dither.NONE)for f in frames];q[0].save(O/'one-arrow-per-snake.gif',save_all=True,append_images=q[1:],duration=[40 if i%3==2 else 30 for i in range(len(q))],loop=0,optimize=True)
report={'native_cases':len(checks),'passed':sum(checks),'errors':errors,'rows':rows,'scope':'Single-arrow rendering only; the native side-run/burrow/arch director is unchanged.'};(O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({'cases':len(checks),'passed':sum(checks),'errors':errors}));assert all(checks)and not errors
