"""Verify the retained-fighter entry remains small and animated after the rewrite."""
from pathlib import Path
import sys,json,http.server,threading,hashlib
R=Path(__file__).resolve().parents[2];O=R/'_shots/furyship_cloud_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
class Quiet(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(R),**kw)
 def log_message(self,*a):pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
errors=[]
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio']);pg=b.new_page()
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 pg.evaluate('''()=>{__auto=function(){};run.mode='arcade';run.pilot='cole';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');beginStage(5);run.gravityShipReady=true;furyLegacyShip=false;furyShipWarm();}''')
 pg.wait_for_function('()=>furyShipReady()',timeout=120000)
 pg.evaluate('''()=>{setState(GS.LAUNCH);drawLaunch._phase=undefined;drawLaunch._furyIntro=null;window.__plumes=[];const c=furyShipCanvas;furyShipCanvas=function(k){if(k.startsWith('thrusters_'))__plumes.push(k);return c.apply(this,arguments);};}''')
 for _ in range(12):pg.evaluate('()=>__step(4)');pg.wait_for_timeout(12)
 result=pg.evaluate('()=>({noRebuild:!drawLaunch._furyIntro.build&&gravityMode.phase==="active",size:drawLaunch._furyIntro.ship.size,plumes:[...new Set(__plumes)],speed:drawLaunch._spd,error:window.__err||null})')
 result.update(errors=errors,runtimeSha256=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest())
 (O/'retained.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
 assert result['noRebuild']and result['size']==48 and len(result['plumes'])==2 and result['speed']==420 and not errors and not result['error']
 b.close()
srv.shutdown()
