"""Real Chromium check that Razorback armor passes pellets until side guns fall."""
import base64,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out=Path('_shots/razorback_seal_0925');out.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(sh.GAME);errors=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  pg=br.new_page(viewport={'width':1100,'height':1200})
  pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
  pg.wait_for_function('()=>(window.__bofFrames|0)>4');pg.evaluate(sh.TRAP_RAF)
  pg.evaluate(sh.SETUP,{'state':'PLAY','stage':1,'pilot':'cole','invuln':True})
  report=pg.evaluate("""()=>{diffKey='normal';DIFF=difficultyForRun(run.mode,diffKey);
   stagePlan=[];waveIdx=999;enemies=[];eBullets=[];pBullets=[];
   spawnClock=9999;subBoss=null;subBossActive=false;spawnSubBoss('razorback');
   const b=subBoss,R=b._rzb;razorbackUpdate(b,0);b.x=worldWidth()/2;b.y=210;
   b.enter=false;R.state='guns';R.trans=0;R.a=Math.PI/2;R.tgt={x:b.x,y:b.y};
   R.speed=0;R.attack='sonic';R.at=0;
   const hp=b.hp;const center={kind:'bullet',x:b.x,y:b.y,vx:0,vy:0,w:3,h:3,dmg:7,t:0};
   pBullets=[center];updatePlay(1/60);
   const afterCenter={pelletDead:!!center.dead,hp:b.hp,prior:hp,solid:subBossSolidAt(b.x,b.y)};
   const q=rzbWorld(b,-57,96),before=R.pools.left;
   const gun={kind:'bullet',x:q.x,y:q.y,vx:0,vy:0,w:3,h:3,dmg:7,t:0};
   pBullets=[gun];updatePlay(1/60);
   return {afterCenter,afterGun:{pelletDead:!!gun.dead,pool:R.pools.left,prior:before},kind:b.kind};}""")
  pg.wait_for_function("()=>XART.rdy('rzb_hull_2')",timeout=30000)
  pg.evaluate(sh.STEP,3);pg.wait_for_timeout(80)
  png=pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
  (out/'arena.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
  report['errors']=errors;(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
  assert not errors
  assert not report['afterCenter']['pelletDead'] and not report['afterCenter']['solid']
  assert report['afterCenter']['hp']==report['afterCenter']['prior']
  assert report['afterGun']['pelletDead'] and report['afterGun']['pool']<report['afterGun']['prior']
  br.close()
finally:stop()
