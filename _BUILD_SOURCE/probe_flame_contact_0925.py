"""Verify that real flame contact routes to the throttled fire sample, not Ice Breath."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright
out=Path('_shots/flame_contact_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':2,'pilot':'decker','invuln':True})
  before=pg.evaluate("""()=>{stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];
    player.x=worldWidth()/2;player.y=VH*.80;run.pilot='decker';run.weapon=4;
    enemies.push({x:player.x,y:player.y-85,w:36,h:36,hp:1000,maxhp:1000,type:'s2interceptor',pattern:'none',shoots:false,dead:false,t:0,score:0});
    window.__flameSfxHits=0;const orig=Audio.SFX.flameHit;window.__flameSfxOrig=orig;Audio.SFX.flameHit=()=>{window.__flameSfxHits++;};
    flameFire(3);return {ice:flameIsIce(),enemyHp:enemies[0].hp};}""")
  err=pg.evaluate(sh.STEP,8)
  if err:raise RuntimeError(err)
  fire=pg.evaluate("""()=>({hits:window.__flameSfxHits,hp:enemies[0].hp,bullets:pBullets.map(b=>b.kind)})""")
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'fire_contact.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  ice=pg.evaluate("""()=>{pBullets=[];run.pilot='freezer';enemies[0].hp=1000;const old=window.__flameSfxHits;flameFire(3);return {ice:flameIsIce(),before:old};}""")
  err=pg.evaluate(sh.STEP,8)
  if err:raise RuntimeError(err)
  after=pg.evaluate("""()=>({hits:window.__flameSfxHits,hp:enemies[0].hp})""")
  pg.evaluate("()=>{Audio.SFX.flameHit=window.__flameSfxOrig;}")
  report={'before':before,'fire':fire,'ice':ice,'after':after,'errors':errors}
  (out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors and not before['ice'] and fire['hits']>0 and fire['hp']<before['enemyHp']
  assert ice['ice'] and after['hits']==ice['before'] and after['hp']<1000
  br.close()
finally:stop()
