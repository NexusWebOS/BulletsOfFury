"""Native visible-pose, Retina and actual missile routing checks for Vile subforms."""
import base64, http.server, json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright

OUT=Path('_shots/overnight_0927/finale-targets');OUT.mkdir(parents=True,exist_ok=True)
source=Path('_BUILD_SOURCE/test_overnight_0927.cjs').read_text(encoding='utf-8')
checks=source[source.index("  beginStage(8);setState(GS.PLAY);spawnBoss('vileexistence');const final="):source.index('  const savedPlayerHit=playerHit;')]
checks=checks.replace('const final=boss;','const final=boss;window.B=final;')
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME);errors=[];report={}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  report['checks']=p.evaluate('()=>{const o={};diffKey="normal";DIFF=DIFFS.normal;run.mode="arcade";run.pilot="cole";player.reset();'+checks+'return o;}')
  p.evaluate("()=>{player.dead=false;player.somer=null;player.roll=null;player.x=worldWidth()/2;player.y=VH*.8;camX=player.x-VW/2;story=null;stagePlan=[];enemies=[];powerups=[];eBullets=[];pBullets=[];special=null;run.spaceWeapon=0;run.spaceLevels=[3,3,3];B.flash=0;B._v24.shield=0;}")
  for name,code in [
   ('phantom-warning',"const P={type:'phantom',t:0};vile25Start(B,P);B._v24.pattern=P;P.t=.9;P.cycle=0;P.tx=B.x+145;P.ty=VH*.65;"),
   ('phantom-emerged',"B._v24.pattern.t=1.3;"),
   ('knight-strike',"const P={type:'knight',t:0};vile25Start(B,P);B._v24.pattern=P;P.t=1.37;P.cycle=0;P.tx=B.x-145;P.ty=VH*.67;"),
   ('mirror-locks',"const P={type:'mirror',t:0};vile25Start(B,P);B._v24.pattern=P;P.t=1.1;"),
  ]:
   p.evaluate('()=>{'+code+'for(let i=0;i<2;i++){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.016);}}');p.wait_for_timeout(220)
   p.evaluate("()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.016);}")
   (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>ctx.canvas.toDataURL()').split(',')[1]))
   report[name]=p.evaluate("()=>({pose:vile25BodyPose(B),targets:retinaBossTargets(B).map(t=>({x:t.x,y:t.y,kind:t.kind,w:t.w,h:t.h}))})")
  report['errors']=errors;(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');br.close()
finally:stop()
print(json.dumps({'checks':report.get('checks'),'errors':errors},indent=2))
assert not errors,errors
assert all(report['checks'].values()),report['checks']
