"""Break the live Hammer module, verify the five-second 2x punish and leap reset."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/hammer_break_stun_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('() => (window.__bofFrames|0)>4')
        page.evaluate(sh.TRAP_RAF)
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 5, 'pilot': 'cole', 'invuln': True})
        page.evaluate("""() => {
          diffKey='furious';DIFF=DIFFS.furious;stagePlan=[];waveIdx=999;spawnClock=9999;
          enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
          boss=null;bossActive=false;spawnBoss('chromehammer');bossActive=true;
          player.invuln=1e9;player.x=worldWidth()*.32;player.y=VH*.78;
        }""")
        entered = False
        for second in range(12):
            err = page.evaluate(sh.STEP, 60)
            if err: errors.append(f'entry {second}: {err}')
            entered = page.evaluate("() => boss&&boss._hammer&&boss._hammer.state==='hammer'&&!boss._noHit")
            if entered: break
        if not entered: errors.append('natural hammer state not reached')
        before = page.evaluate("""() => {
          const b=boss,h=b._hammer,x=b.x-54,y=b.y+8;
          const hammerHitbox=bossHitTest(x,y),selected=b._hammerModuleHit;
          _lastHitX=x;_lastHitY=y;_dmgBullet={kind:'mg',x:x,y:y};
          const oldHp=b.hp,moduleHp=h.hammerHP;hitBoss(moduleHp+1);
          return {hammerHitbox,selected,oldHp,newHp:b.hp,moduleHp,
            state:h.state,destroyed:h.hammerDestroyed};
        }""")
        punished = page.evaluate("""() => {
          const b=boss,h=b._hammer,x=b.x,y=b.y;
          const bodyHitbox=bossHitTest(x,y);
          _lastHitX=x;_lastHitY=y;_dmgBullet={kind:'mg',x:x,y:y};
          const oldHp=b.hp;hitBoss(35);
          return {bodyHitbox,oldHp,newHp:b.hp,damage:oldHp-b.hp,state:h.state};
        }""")
        err = page.evaluate(sh.STEP, 1)
        if err: errors.append(f'stun frame: {err}')
        raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
        (out/'hammer_stun.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
        follow_up = page.evaluate("""() => {
          const b=boss,x=b.x,y=b.y,oldHp=b.hp;
          if(!bossHitTest(x,y))throw Error('stunned body cannot be shot');
          _lastHitX=x;_lastHitY=y;_dmgBullet={kind:'mg',x:x,y:y};
          hitBoss(35);
          return {damage:oldHp-b.hp,state:b._hammer.state};
        }""")
        err = page.evaluate(sh.STEP, 60*4)
        if err: errors.append(f'stun hold: {err}')
        during = page.evaluate("""() => ({state:boss._hammer.state,t:boss._hammer.t,
          hp:boss.hp,glow:boss._hammer.state==='hammer_stun'})""")
        err = page.evaluate(sh.STEP, 90)
        if err: errors.append(f'recovery: {err}')
        after = page.evaluate("""() => ({state:boss._hammer.state,
          comboPending:boss._hammer.comboPending,followCount:boss._hammer.followCount,
          hammerRestored:!boss._hammer.hammerDestroyed})""")
        raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
        (out/'after_recovery.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
        browser.close()
finally:
    stop()

report = {'before':before,'punished':punished,'followUp':follow_up,
          'during':during,'after':after,'errors':errors}
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
assert not errors
assert before['hammerHitbox'] and before['selected']=='hammer' and before['destroyed']
assert before['newHp']==before['oldHp'] and before['state']=='hammer_exposed'
assert punished['bodyHitbox'] and punished['damage']==70 and punished['state']=='hammer_stun'
assert follow_up['damage']==70 and follow_up['state']=='hammer_stun'
assert during['state']=='hammer_stun' and after['hammerRestored']
