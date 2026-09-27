"""Real Chromium death/spin/respawn checks across all nine stages. No forced reset."""
import base64, http.server, json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927/respawn');OUT.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];runs=[]
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for stage in range(1,10):
   p.evaluate("""s=>{diffKey='normal';DIFF=DIFFS.normal;run.mode='arcade';run.stage=s;run.pilot='cole';run.lives=4;beginStage(s);setState(GS.PLAY);player.reset();story=null;s6Opening=null;special=null;enemies=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;stagePlan=[];spawnClock=99999;waveIdx=999;powerups=[];eBullets=[];pBullets=[];groundTargetingReset();run.shield=0;run._megaShield=null;for(const k of Object.keys(Input.keys))Input.keys[k]=false;player.x=worldWidth()/2-70;player.y=398;camX=clamp(player.x-VW/2,0,worldWidth()-VW);XART.rdy('ship_cole_sp0');spaceAtlasCanvas('ship_base','cole');window.R={before:{x:player.x,y:player.y},initialLives:run.lives,maxFall:0,reset:null};}""",stage)
   p.wait_for_function('()=>deathSpinAvailable()')
   for _ in range(8):
    p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.016);}')
    p.wait_for_timeout(100)
   p.evaluate('()=>{player.invuln=0;playerHit();R.spin=!!player._spin;R.anchor=player._deathAnchor;}')
   for batch in range(5):
    p.evaluate("""()=>{for(let i=0;i<30;i++){const dead=player.dead;updatePlay(1/60);if(player.dead)R.maxFall=Math.max(R.maxFall,player.y-R.before.y);if(dead&&!player.dead)R.reset={x:player.x,y:player.y,invuln:player.invuln,lives:run.lives};ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}""")
    p.wait_for_timeout(12)
    if stage in [1,5,8] and batch in [1,4]:(OUT/f'{stage}-{batch}.png').write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
   runs.append(p.evaluate('s=>({stage:s,...R,after:{x:player.x,y:player.y},prediction:{vx:player._vx,vy:player._vy},anchorCleared:!player._deathAnchor})',stage))
  br.close()
finally:stop()
(OUT/'report.json').write_text(json.dumps({'runs':runs,'errors':errors},indent=2),encoding='utf-8');print(json.dumps({'runs':runs,'errors':errors},indent=2))
assert not errors,errors
assert all(r['spin'] and r['maxFall']>20 and r['reset'] and r['reset']['x']==r['before']['x'] and r['reset']['y']==r['before']['y'] and r['reset']['lives']==r['initialLives']-1 and r['anchorCleared'] for r in runs)
