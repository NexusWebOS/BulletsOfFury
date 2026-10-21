from pathlib import Path
import ast,sys,http.server,base64,io,json
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/performance_finish_1020'
def value(f,n):return next(ast.literal_eval(x.value) for x in ast.parse((R/'_BUILD_SOURCE'/f).read_text()).body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id==n for t in x.targets))
SETUP=value('probe_feedback_1002.py','SETUP');CLEAR=value('probe_performance_1020.py','CLEAR');errors=[]
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport=dict(width=1366,height=900));p.set_default_timeout(180000);p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate('BOFPERFORMANCE.warm();for(const k of victoryEndingKeys())XART.rdy(k);dr21Warm();');p.wait_for_function('()=>{BOFPERFORMANCE.warm();return BOFPERFORMANCE.ready&&dr21Warm()&&victoryEndingKeys().every(k=>XART.rdy(k))}')
  def image():return Image.open(io.BytesIO(base64.b64decode(p.evaluate('''()=>{const c=document.createElement('canvas');c.width=VW*SS;c.height=VH*SS;c.getContext('2d').drawImage(cv,0,0);return c.toDataURL().split(',')[1];}''')))).convert('RGB')
  for stage,kind,mini in [(5,'siegebomber',True),(6,'siegefortress17',True),(6,'warhive',False)]:
   p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=mini,pilot='cole'));p.evaluate(CLEAR);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}')
   p.evaluate('''kind=>{if(kind==='siegebomber')B._bomber.mode='recover';for(let i=0;i<400;i++){player.invuln=1e9;updatePlay(1/60);}if(kind==='siegebomber')hc1007BomberSet(B,'lances');}''',kind)
   frames=[]
   for i in range(72):
    p.evaluate('''()=>{for(let i=0;i<10;i++){player.invuln=1e9;updatePlay(1/60);}shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');frames.append(image())
    if i%6==0:p.wait_for_timeout(5)
   frames[0].save(O/(kind+'-native.gif'),save_all=True,append_images=frames[1:],duration=167,loop=0);print(kind,flush=True)
  for kind,src in [('laser','carrier laser'),('ice','cryo shard'),('dark','evil chromium void'),('shadow','shadow eradication')]:
   p.evaluate(SETUP,dict(stage=1,pilot='cole'));p.evaluate(CLEAR);p.evaluate('''src=>{player.x=VW/2;player.y=VH*.56;player.invuln=0;run.shield=0;playerHit(src);}''',src);frames=[]
   for i in range(26):
    p.evaluate('''t=>{player._dr21Death.t=t;ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#0b1420';ctx.fillRect(0,0,VW,VH);drawDeathSpin();}''',i/16);frames.append(image())
   frames[0].save(O/('death-'+kind+'-native.gif'),save_all=True,append_images=frames[1:],duration=63,loop=0)
  for horror in [False,True]:
   frames=[]
   for i in range(48):
    p.evaluate('''a=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.fillStyle='#0b1420';ctx.fillRect(0,0,VW,VH);INV20.active=true;INV20.last={scene:'report'};inv20Pose('cole',VW/2,VH-20,VH*.88,a.i/8,a.h);}''',dict(i=i,h=horror));frames.append(image())
   frames[0].save(O/('cole-horror-native.gif' if horror else 'cole-report-native.gif'),save_all=True,append_images=frames[1:],duration=125,loop=0)
  p.evaluate('''()=>{setState(GS.VICTORY);run.pilot='cole';ctx.setTransform(SS,0,0,SS,0,0);inv20Draw(28.8,VW,VH,{});}''');p.set_viewport_size(dict(width=390,height=844));p.evaluate('__bofFit()');p.evaluate('loop(performance.now()+16.7)');p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);inv20Draw(28.8,VW,VH,{});}''');p.screenshot(path=str(O/'cinematic-narrow.png'))
  (O/'capture-errors.json').write_text(json.dumps(errors));br.close()
finally:stop()
print(json.dumps(dict(errors=errors)));raise SystemExit(bool(errors))
