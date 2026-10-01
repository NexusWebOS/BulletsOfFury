from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'_shots/realm_visual_0930';O.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
SETUP=(Path(__file__).parent/'probe_realm_0930.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[];evidence={}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1000,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000);p.evaluate(sh.TRAP_RAF);p.evaluate(SETUP)
  p.wait_for_function("()=>Object.keys(REALM30_ART).every(k=>XART.rdy('r30_'+k))&&PILOTS.every(p=>XART.rdy('ship_'+p.key))&&_liquidFrames('nlq_sludgeF').every(f=>f&&(f.naturalWidth||f.width)>0)",timeout=60000)
  for form in range(3):
   p.evaluate('n=>{r30Form(boss,n);boss._r30.mode="fight";boss.enter=false;boss.flash=0;player.invuln=0;enemies=[];eBullets=[];pBullets=[];}',form)
   if form==0:p.evaluate('()=>r30Wall(boss,"datawall")')
   if form==2:p.evaluate('()=>{boss._r30.shield=boss._r30.shieldMax=100;}')
   p.evaluate('()=>drawWorld(0)');(O/f'form_{form}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  p.evaluate('()=>{boss._r30.shield=0;boss.flash=0;boss._r30.seq=0;r30Attack(boss);for(let i=0;i<120;i++)updateBoss(1/60);player.invuln=0;drawWorld(0);}')
  (O/'colossus_sweep.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  evidence['render']=p.evaluate("""()=>{const a=[];for(let i=0;i<40;i++){const t=performance.now();drawWorld(0);ctx.getImageData(0,0,1,1);a.push(performance.now()-t);}a.sort((a,b)=>a-b);return{median:a[20],p95:a[38],rotationBytes:ROT5.bytes};}""")
  p.evaluate('()=>{boss._r30.mode="reunion";boss._r30.t=3;boss._r30.fx=[];eBullets=[];pBullets=[];player.x=worldWidth()/2;player.y=300;drawWorld(0);}')
  (O/'reunion.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  # Draw the actual player path into each review tile, preserving weapon mounts.
  data=p.evaluate("""()=>{run.stage=1;run.spaceMode=false;gravityMode=null;player.dead=false;player.roll=null;player.somer=null;player.invuln=0;player._spawnClearT=2;run.shield=0;run.weapon=0;run.wlevel=1;player.x=240;player.y=250;
   const c=document.createElement('canvas');c.width=760;c.height=9*142;const g=c.getContext('2d');g.fillStyle='#182330';g.fillRect(0,0,c.width,c.height);g.imageSmoothingEnabled=false;g.font='16px monospace';
   PILOTS.forEach((p,row)=>{run.pilot=p.key;g.fillStyle='#fff';g.fillText(p.key,8,row*142+27);
    [-1,-.5,0,.5,1].forEach((bank,col)=>{player._bank=bank;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);_drawPlayerCore();ctx.restore();g.drawImage(cv,190,198,100,105,118+col*126,row*142+8,100,105);g.fillText(String(bank),139+col*126,row*142+136);});});return c.toDataURL().split(',')[1];}""")
  (O/'pilot_steering.png').write_bytes(base64.b64decode(data))
  evidence['stress']=p.evaluate("""()=>{const im=XART.get('r30_colossus_body'),q=rot5Source(im,null,384,384,0);for(let i=0;i<72;i++)rot5Frame(q,i);return {withinBudget:ROT5.bytes<=ROT5.budget,bytes:ROT5.bytes,budget:ROT5.budget};}""")
  evidence['errors']=errors;print(evidence,flush=True);b.close()
finally:stop();(O/'verification.json').write_text(json.dumps(evidence,indent=2))
