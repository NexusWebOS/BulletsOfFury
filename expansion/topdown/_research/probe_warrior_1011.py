"""Native pixels, real keyboard/Gamepad polling, tank boost and supplied music.

Uses protected fixtures, not an unassisted campaign balance claim.
"""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
from shoot import serve
OUT = ROOT / '_shots/warrior_1011'
OUT.mkdir(parents=True, exist_ok=True)
checks, errors, observations = [], [], {}


def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


port, stop = serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1100, 'height':850})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html')
        page.wait_for_function('window.TDGAME && TDGAME.G.state === "boot"', timeout=60000)
        page.evaluate("TDGAME.freeze();window.press=(k,v)=>dispatchEvent(new KeyboardEvent(v?'keydown':'keyup',{key:k}));")
        page.keyboard.press('Enter')
        page.evaluate('TDGAME.G.sel=0;TDGAME.start()')
        page.wait_for_function('Object.keys(TD_WARRIOR_ART.assets).every(k=>!!ART.get(k))')
        check('all six rebuilt modules decode as fixed 512x512 or 640x512 canvases', page.evaluate('Object.keys(TD_WARRIOR_ART.assets).length===6 && Object.keys(TD_WARRIOR_ART.assets).every(k=>JSON.stringify(ART.size(k))===JSON.stringify(TD_WARRIOR_ART.assets[k].size) && ART.size(k).every(n=>n%2===0))'))
        check('hull damage and wreck share the intact mounting pivot and scale', page.evaluate('JSON.stringify(TD_WARRIOR_ART.assets.warrior_hull.anchor)===JSON.stringify(TD_WARRIOR_ART.assets.warrior_damaged.anchor) && JSON.stringify(TD_WARRIOR_ART.assets.warrior_hull.anchor)===JSON.stringify(TD_WARRIOR_ART.assets.warrior_wreck.anchor)'))
        fresh = """TDGAME.G.sel=0;TDGAME.start();const G=TDGAME.G,p=G.player;
          G.units=[];G.props=[];G.structures=[];TD.World.load(800,4000,[]);
          p.x=150;p.y=2200;p.inv=99999;p.a=p.aim=Math.PI;TD.Input.pointer.active=false;
          for(const k of ['r','d','w','j','h','shift','e'])press(k,false);TDGAME.step();"""
        r = page.evaluate('()=>{' + fresh + """
          const x=p.x;press('d',true);TDGAME.step(60);const normal=p.x-x;
          press('d',false);TDGAME.step();p.x=x;p.vx=0;p.vy=0;
          press('d',true);press('r',true);TDGAME.step(60);const boosted=p.x-x;
          const out={normal,boosted,drive:p.drive,speed:Math.hypot(p.vx,p.vy),boosting:p.boosting,dust:TD.FX.list.filter(f=>f.key==='rzb_dust').length};
          press('r',false);press('d',false);TDGAME.step(12);out.stopped=Math.hypot(p.vx,p.vy);return out;
        }""")
        observations['speed'] = r
        check('holding R produces over 1.9x measured travel with authored track dust', r['boosted'] > r['normal'] * 1.9 and r['boosting'] and r['dust'] >= 8 and r['drive'] < .6)
        check('releasing movement brakes the boosted tank promptly', r['stopped'] < .1)
        r = page.evaluate('()=>{' + fresh + """
          press('r',true);TDGAME.step(50);const idle=p.drive;
          press('d',true);TDGAME.step(150);const exhausted=p.boostLocked&&!p.boosting;
          TDGAME.step(30);const cannotAuto=p.boostLocked&&!p.boosting;
          press('r',false);press('d',false);TDGAME.step(210);return {idle,exhausted,cannotAuto,refilled:p.drive===1&&!p.boostLocked};
        }""")
        check('boost spends no energy at rest, exhausts, requires release and refills', all([r['idle'] == 1, r['exhausted'], r['cannotAuto'], r['refilled']]))
        r = page.evaluate('()=>{' + fresh + """
          const a=p.a,x=p.x;press('shift',true);press('d',true);press('r',true);press('e',true);press('j',true);
          TDGAME.step(30);const out={dx:p.x-x,hull:p.a-a,aim:p.aim-a,fired:G.shots.length>0};
          for(const k of ['shift','d','r','e','j'])press(k,false);TDGAME.step();return out;
        }""")
        check('boosting sideways retains independent turret rotation and gun fire', r['dx'] > 130 and abs(r['hull']) < .001 and abs(r['aim']) > 1 and r['fired'])
        page.evaluate('()=>{' + fresh + "press('d',true);press('r',true);press('j',true);TDGAME.step(30);p.inv=0;TDGAME.render();}")
        page.locator('#screen').screenshot(path=str(OUT/'boost_drive.png'))
        r = page.evaluate('()=>{' + fresh + """
          TD.World.load(800,4000,[[330,2050,334,2350,'b']]);press('d',true);press('r',true);TDGAME.step(120);
          const out=p.x<=310.01&&p.x>290;press('r',false);press('d',false);TDGAME.step();return out;
        }""")
        check('full-speed boost cannot tunnel through a four-pixel concrete wall', r)
        page.evaluate("window.testPad={id:'Warrior M30 fixture',connected:true,buttons:Array.from({length:16},()=>({pressed:false,value:0})),axes:[]};Object.defineProperty(navigator,'getGamepads',{value:()=>[testPad],configurable:true});window.pad=(...ids)=>testPad.buttons.forEach((b,i)=>{b.pressed=ids.includes(i);b.value=+b.pressed});")
        r = page.evaluate('()=>{' + fresh + """
          const x=p.x,a=p.a;pad(8,5,15,2);TDGAME.step(30);
          const out={dx:p.x-x,boost:p.boosting,hull:p.a-a,charge:p.charge,
            aim:Math.abs(TD.M.wrap(p.aim-Math.PI)),fire:G.shots.some(s=>s.vy<0)};
          pad();TDGAME.step();return out;
        }""")
        check('Mode+C boosts while D-pad strafes and X fires north without cannon charge', r['dx'] > 130 and r['boost'] and abs(r['hull']) < .001 and r['charge'] == 0 and r['aim'] < .001 and r['fire'])
        r = page.evaluate('()=>{' + fresh + """
          pad(5);TDGAME.step(45);const charged=p.charge>=40;pad();TDGAME.step();return charged&&G.shots.some(s=>s.big)&&p.charge===0;
        }""")
        check('unmodified controller C still charges and releases the cannon', r)
        page.evaluate("Object.defineProperty(navigator,'getGamepads',{value:()=>[],configurable:true})")
        page.evaluate('()=>{' + fresh + "press('r',true);press('d',true);TDGAME.step(10);}")
        r = page.evaluate("()=>{window.dispatchEvent(new Event('blur'));TDGAME.step(12);return !TDGAME.G.player.boosting&&Math.hypot(TDGAME.G.player.vx,TDGAME.G.player.vy)<.1;}")
        check('window blur releases boost and movement safely', r)

        page.evaluate("TDGAME.G.sel=0;TDGAME.start();TDGAME.G.units=[];TDGAME.G.player.x=400;TDGAME.G.player.y=650;TDGAME.G.player.inv=99999;TDGAME.step(145)")
        # Complete the authored Overdrive entrance/card before testing combat.
        for _ in range(100):
            if page.evaluate('TDGAME.G.bossIntro.done'): break
            page.evaluate('TDGAME.step(24)')
            page.wait_for_timeout(1)
        page.wait_for_function('TD.Audio.musicKey === "warrior" && TD.Audio.music && TD.Audio.music.readyState >= 3 && TD.Audio.music.currentTime > .05', timeout=15000)
        r = page.evaluate("(()=>{const a=TD.Audio.music;return {src:a.currentSrc,duration:a.duration,loop:a.loop,paused:a.paused,time:a.currentTime};})()")
        observations['audio'] = r
        check('actual Warrior entry starts Mike\'s decoded stereo boss track', r['src'].endswith('/expansion/topdown/audio/BOF-O-BOSS1.mp3') and abs(r['duration'] - 122.76) < .1 and r['loop'] and not r['paused'])
        page.evaluate('TD.Audio.music.currentTime=TD.Audio.music.duration-.15')
        page.wait_for_timeout(600)
        check('supplied track loops through its end during the active fight', page.evaluate('TD.Audio.music.currentTime<2 && !TD.Audio.music.paused'))
        page.evaluate("const G=TDGAME.G,B=G.boss;B.state='recover';B.cooldown=999;B.x=400;B.y=472;G.player.y=672;B.a=B.upper=0;G.shots=[];G.eshots=[];TDGAME.step(25);G.player.inv=0;TDGAME.render()")
        r = page.evaluate("(()=>{const B=TDGAME.G.boss,b=B.bounds(),p=TDGAME.G.player;return {boss:b,width:b.right-b.left,zoom:TD.Cam.zoom,view:{w:TD.VW,h:TD.VH},player:{x:p.x-TD.Cam.x,y:p.y-TD.Cam.y},camera:{x:TD.Cam.x,y:TD.Cam.y},hullWidth:ART.size('warrior_hull')[0]*TD.WARRIOR_PARTS.hull.scale*B.scale};})()")
        observations['framing'] = r
        check('Warrior uses the requested 15% smaller chassis while remaining a large boss', r['width'] > 350 and abs(r['hullWidth']-640*.52*.85)<.001)
        check('1:1 duel camera shows both the new boss and player in the arena', r['zoom'] == 1 and r['boss']['left'] > r['camera']['x'] and r['boss']['right'] < r['camera']['x'] + r['view']['w'] and r['boss']['top'] > r['camera']['y'] and r['boss']['bottom'] < r['camera']['y'] + r['view']['h'] - 30 and 48 < r['player']['x'] < r['view']['w'] - 48 and 74 < r['player']['y'] < r['view']['h'] - 54)
        page.locator('#screen').screenshot(path=str(OUT/'warrior_front.png'))
        for i, angle in enumerate([-.7, -1.57079632679, 1.57079632679]):
            page.evaluate(f'TDGAME.G.boss.a={angle};TDGAME.G.boss.upper=.16;TDGAME.G.boss.followCamera(TDGAME.G.player);TDGAME.render()')
            page.locator('#screen').screenshot(path=str(OUT/f'warrior_rotation_{i}.png'))
        page.evaluate("const B=TDGAME.G.boss;B.a=-Math.PI/2;B.state='rack';B.t=.7;B.volleyT=0;TDGAME.G.player.inv=99999;TDGAME.step(10);TDGAME.G.player.inv=0;TDGAME.render()")
        page.locator('#screen').screenshot(path=str(OUT/'warrior_salvo.png'))
        check('larger Warrior still launches physical twin-arm homing volleys', page.evaluate('TDGAME.G.eshots.some(s=>s.owner===TDGAME.G.boss&&s.k==="missile")'))
        r = page.evaluate("()=>{const G=TDGAME.G,B=G.boss,p=G.player;G.eshots=[];p.x=400;p.y=650;p.vx=p.vy=0;p.inv=0;p.drive=1;p.boostLocked=false;B.x=400;B.y=500;B.a=B.upper=0;B.state='ram';B.t=0;B.ramDir=0;B.ramGoal={x:p.x,y:p.y};const hp=p.hp;press('r',true);press('d',true);TDGAME.step(35);return {hp,x:p.x,startHp:hp,boost:p.boosting,warn:B.warn};}")
        page.locator('#screen').screenshot(path=str(OUT/'boost_ram_escape.png'))
        after = page.evaluate("()=>{press('r',false);press('d',false);TDGAME.step(55);return {hp:TDGAME.G.player.hp,dead:TDGAME.G.player.dead,state:TDGAME.G.boss.state};}")
        check('real boost escapes a committed Warrior ram with collision and damage enabled', r['x'] > 560 and r['boost'] and r['warn'] and after['hp'] == r['startHp'] and not after['dead'] and after['state'] == 'recover')
        r = page.evaluate("()=>{const G=TDGAME.G,B=G.boss,d=TD.WARRIOR_PARTS.armL,at=B.world(d.x,d.y),angle=B.upper;B.damage('armL',999);const f=TD.FX.list.find(f=>f.k==='fragment'&&f.key===d.key);return B.parts.armL===0&&f&&Math.abs(f.x-at.x)<.001&&Math.abs(f.y-at.y)<.001&&f.a===angle&&f.s===d.scale*B.scale&&JSON.stringify([f.ax,f.ay])===JSON.stringify(TD_WARRIOR_ART.assets[d.key].anchor)&&!f.fade;}")
        check('rebuilt arm detaches with exact mounted art, angle, pivot and scale', r)
        page.evaluate('TDGAME.G.player.inv=99999;TDGAME.step(10);TDGAME.G.player.inv=0;TDGAME.render()')
        page.locator('#screen').screenshot(path=str(OUT/'warrior_arm_break.png'))
        page.evaluate('TDGAME.G.player.inv=99999;TDGAME.step(100)')
        check('large arm rotates, falls and settles as an unfaded authored wreck', page.evaluate('TDGAME.G.wrecks.some(w=>w.fragment&&w.art==="warrior_arm_l"&&w.s===TD.WARRIOR_PARTS.armL.scale*TDGAME.G.boss.scale)'))
        page.evaluate("const B=TDGAME.G.boss;B.damage('armR',999);B.damage('helmet',999);B.damage('hull',999);TDGAME.step(340)")
        check('Warrior defeat stops boss music and transitions to clear music/results', page.evaluate('TDGAME.G.state==="clear"&&TDGAME.G.boss.wrecked&&TD.Audio.musicKey==="clear"'))
        page.locator('#screen').screenshot(path=str(OUT/'warrior_results.png'))
        page.evaluate('TDGAME.G.sel=0;TDGAME.start()')
        check('mission restart restores a full tank boost meter', page.evaluate('TDGAME.G.player.drive===1&&!TDGAME.G.player.boosting&&!TDGAME.G.player.boostLocked'))
        page.evaluate("press('f1',true);TDGAME.step();press('f1',false);TDGAME.step()")
        page.locator('#screen').screenshot(path=str(OUT/'help.png'))
        check('Help still opens and retains the gameplay return path', page.evaluate('TDGAME.G.state==="help"&&TD.Frontend.returnTo==="pause"'))
        check('zero page, console and missing-asset errors', not errors)
        (OUT/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'observations':observations}, indent=2), encoding='utf-8')
        browser.close()
finally:
    stop()
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed', flush=True)
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
