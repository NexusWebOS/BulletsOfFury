from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=Path(__file__).parent;D=W/'references';D.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1920,height=1080));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.wait_for_function('()=>{let ok=true;for(const k of ["ship_cole_so6","comm_cole_idle",...Object.values(V18_ART.models.colossus.frames[0]).map(a=>a.key)])if(!XART.rdy(k))ok=false;return ok;}',timeout=120000)
  rows=p.evaluate('''()=>{const rows=[];function save(name,draw){const c=document.createElement('canvas');c.width=c.height=512;const g=c.getContext('2d');g.imageSmoothingEnabled=false;draw(g);rows.push({name,png:c.toDataURL().split(',')[1]});}save('dracodia-head',g=>{const a=V18_ART.models.colossus.frames[0].core;g.drawImage(XART.get(a.key),101,0,122,145,40,0,432,512);});save('dracodia-body',g=>{for(const a of Object.values(V18_ART.models.colossus.frames[0]))g.drawImage(XART.get(a.key),0,0,512,512);});save('cole-portrait',g=>g.drawImage(XART.get('comm_cole_idle'),0,0,512,512));save('cole-ship',g=>{const a=hc10ShipGeometry('cole','front'),k=Math.min(470/a.w,470/a.h);g.drawImage(XART.get(a.key),...a.rect,256-a.w*k/2,256-a.h*k/2,a.w*k,a.h*k);});return rows;}''')
  for r in rows:(D/(r['name']+'.png')).write_bytes(base64.b64decode(r['png']))
  p.evaluate(shoot.SETUP,{'state':'PLAY','pilot':'cole','stage':1,'invuln':True})
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1);}',timeout=120000)
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=fb2Intro=s6Opening=null;player.invuln=1e9;run.score=123456;run.high=987654;}')
  for i in range(20):p.evaluate(shoot.STEP,30);p.wait_for_timeout(12)
  p.screenshot(path=str(D/'current-game-hud.png'))
  (D/'manifest.json').write_text(json.dumps({'source':'current XART.get and native ctx.drawImage, no substituted aircraft/pilot','pilot':'cole','boss':'V18 colossus phase3','exports':[r['name'] for r in rows]},indent=2));b.close()
finally:stop()
print('Four actual native identity references exported')
