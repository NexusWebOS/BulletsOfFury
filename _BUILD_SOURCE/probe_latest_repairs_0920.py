"""Browser check for password order, graphical pickup lettering, and distant Warden escorts."""
import base64
import contextlib
import io
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, STEP, SETUP, TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/latest_repairs_0920'
OUT.mkdir(parents=True,exist_ok=True)
errors=[]
port,stop=serve(str(ROOT))
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    page=browser.new_page(viewport={'width':960,'height':1040})
    page.on('pageerror',lambda e:errors.append('page '+str(e)))
    page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
    with contextlib.redirect_stderr(io.StringIO()):
      page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=90000)
      page.wait_for_function('() => typeof submitPassword===\'function\' && (window.__bofFrames|0)>4',timeout=45000)
      page.evaluate(TRAP_RAF)
      flow=page.evaluate("""() => {
        setState(GS.PASSWORD);pwInput='STRM';submitPassword();
        const afterCode={state,pending:PENDING_STAGE,mode:run.mode,origin:passwordDifficulty};
        return {afterCode};
      }""")
      assert flow['afterCode']=={'state':'diff','pending':4,'mode':'arcade','origin':True},flow
      page.evaluate(STEP,3)
      page.wait_for_function("() => diffList().every(k => XART.rdy(DIFF_META[k].img))",timeout=20000)
      page.evaluate(STEP,3)
      uri=page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
      (OUT/'password_difficulty.png').write_bytes(base64.b64decode(uri.split(',',1)[1]))
      flow['afterDiff']=page.evaluate("""() => {menuIndex=2;pickDiff();
        return {state,diffKey,pending:PENDING_STAGE,origin:passwordDifficulty};}""")
      assert flow['afterDiff']=={'state':'pilot','diffKey':'hard','pending':4,'origin':True},flow
      page.evaluate(SETUP,{'state':'PLAY','pilot':'cole','stage':4,'invuln':True})
      page.evaluate("""() => {
        run.stage=4;curStage=STAGES[3];diffKey='hard';DIFF=DIFFS.hard;
        player.dead=false;player.invuln=1e9;stagePlan=[];enemies.length=0;eBullets.length=0;
        spawnSubBoss('olivewarden');subBoss.enter=false;subBossActive=true;
        subBoss.x=worldWidth()/2;subBoss.y=subBoss._s4war.homeY;subBoss._drawY=subBoss.y;
        stage4MiniEscortEnsure(subBoss);
        for(const d of subBoss._s4war.drones){d.active=1;d.t=1;d.fireCd=999;}
        window.__gun=subBoss._s4war.drones.find(d=>d.role==='gunner');
        player.x=window.__gun.x;player.y=610;
      }""")
      before=page.evaluate("""() => {const d=window.__gun,b=subBoss;
        return {hp:d.hp,x:d.x,y:d.y,mainX:b.x,ownHit:stage4MiniDroneAt(b,d.x,d.y,4)===d,
          outsideHull:Math.abs(b.x-d.x)>(b._drawW||b.w)/2,
          solid:subBossSolidAt(d.x,d.y)};}""")
      assert before['ownHit'] and before['solid'] and before['outsideHull'],before
      page.evaluate("""() => {const d=window.__gun;
        pBullets.push({kind:'mg',x:d.x,y:d.y+145,vx:0,vy:-12,w:8,h:15,dmg:60,life:3,t:0});
      }""")
      page.evaluate(STEP,24)
      after=page.evaluate("""() => ({hp:window.__gun.hp,dead:window.__gun.dead,
        pageState:state,shots:pBullets.length})""")
      assert after['hp']<before['hp'],(before,after)
      page.wait_for_function("() => bmfReady('dialogue')",timeout=20000)
      page.evaluate("""() => {eBullets.length=0;pickupAnnounce('SHIELD L1','#4ea0ff');
        floatText(player.x,player.y-45,'SHIP','#e9f6ff');}""")
      page.evaluate(STEP,8)
      uri=page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
      (OUT/'stage4_hit_and_pickup_font.png').write_bytes(base64.b64decode(uri.split(',',1)[1]))
    browser.close()
finally:
  stop()
result={'flow':flow,'escortBefore':before,'escortAfter':after,'errors':errors}
(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert not errors,errors[:5]
print('PASS password > difficulty > pilot, distant Stage-4 escort hit, graphical pickup capture, no browser errors')
