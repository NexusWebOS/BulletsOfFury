"""Verify footer glyph bounds on real solo/co-op HUD pixels and long status values."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/fullscreen_hud_1008/footer_status';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();p=browser.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000)
  p.wait_for_function('window.__bofFrames>4',timeout=120000)
  p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  def ready():
   for _ in range(1200):
    if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}'):return
    p.wait_for_timeout(30)
   raise RuntimeError('Stage not ready')
  def draw():p.evaluate('()=>{document.body.classList.add("fs","wide-playing");__bofFit();drawHUDStrip(hudctx);}')
  def pixels():return p.evaluate('''()=>{const out=[],d=PH8.scale;for(let row=0;row<PH8.rows;row++)for(let lane=0;lane<3;lane++){
   const x=lane*160, y=row*PH8.height+PH8.row+2, w=160*d,h=(PH8.height-PH8.row-2)*d;
   const data=hudctx.getImageData(x*d,y*d,w,h).data;let minX=w,maxX=-1,minY=h,maxY=-1;
   for(let py=0;py<h;py++)for(let px=0;px<w;px++){const i=(py*w+px)*4;if(Math.max(data[i],data[i+1],data[i+2])>90){minX=Math.min(minX,px);maxX=Math.max(maxX,px);minY=Math.min(minY,py);maxY=Math.max(maxY,py);}}
   out.push({row,lane,minX:minX/d,maxX:maxX/d,minY:minY/d+PH8.row+2,maxY:maxY/d+PH8.row+2});}return out;}''')
  for pilot,expected in [('cole','NUKES 12'),('lizzie','A-BOMBS 12'),('falva','BALL 100%'),('juggernaut','CHARGE 100%'),('yuri','8S')]:
   p.evaluate('(c)=>BAL7.setup(c)',{'stage':4,'kind':'contraHerald','pilot':pilot,'diff':'normal','seconds':10})
   ready()
   p.evaluate('(k)=>{run.pilot=k;pilotIndex=PILOTS.findIndex(q=>q.key===k);run.score=987654321;highScore=1234567890;special={pilot:k,t:8,dur:15,strikes:12,charge:FALVA_FULL};player._chgT=CHG_FULL;player.dead=false;}',pilot)
   draw();q=p.evaluate('PH8.last[0]');b=pixels()
   check(pilot+' live special status',q['detail']==expected,q['detail'])
   check(pilot+' glyphs stay in three padded non-playable lanes',all(1<=v['minX'] and v['maxX']<159 and 73<=v['minY'] and v['maxY']<=101 for v in b),b)
   p.locator('#hud').screenshot(path=str(OUT/(pilot+'.png')))
  p.evaluate('(c)=>BAL7.setup(c)',{'stage':4,'kind':'contraHerald','pilot':'cole','diff':'normal','seconds':10,'coop':True});ready()
  p.evaluate('()=>{run.score=987654321;run2.score=123456789;player.dead=false;player2.dead=false;}')
  draw();b=pixels()
  check('Co-op has six complete padded footer lanes',len(b)==6 and all(1<=v['minX'] and v['maxX']<159 and 73<=v['minY'] and v['maxY']<=101 for v in b),b)
  p.locator('#hud').screenshot(path=str(OUT/'coop.png'))
  browser.close()
finally:stop()
check('zero browser and asset errors',not errors,errors)
result={'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'errors':errors,'checks':checks}
(OUT/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}),flush=True)
if result['failed'] or errors:sys.exit(1)
