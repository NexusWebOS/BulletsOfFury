"""Chromium check for Maverick's restored seven-lance charged volleys."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/maverick_helix_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'maverick','invuln':True})
  first=pg.evaluate("""()=>{stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];helixVolleyQ=[];
   player.x=worldWidth()/2;player.y=VH-70;helixDetonate({x:player.x,y:VH*.58,lv:5,_full:true});
   return {tiers:[1,2,3,4,5].map(i=>MAV_LASER_TIERS[i].count),immediate:pBullets.filter(b=>b._burstVolley).length,queued:helixVolleyQ.length};}""")
  pg.evaluate("()=>{atomFlash=0;flashScreen=0;whiteBlast=0;}")
  for i in range(9):
   err=pg.evaluate(sh.STEP,2)
   if err:raise RuntimeError(err)
   if i==3:pg.wait_for_timeout(25)
  after=pg.evaluate("""()=>({live:pBullets.filter(b=>b._burstVolley&&!b.dead).length,queued:helixVolleyQ.length,
    angles:[...new Set(pBullets.filter(b=>b._burstVolley).map(b=>Math.round(b._ang*10)))].length})""")
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'charged_volley.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report={'first':first,'after':after,'errors':errors};(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert first['tiers']==[3,4,5,6,7] and first['immediate']==35 and first['queued']==2 and not errors
  br.close()
finally:stop()
