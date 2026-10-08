"""Native Chromium checks for the Warrior ground upgrade; real inputs/pixels.

Uses the project's shoot.py static-server helper. Screenshots stay in _shots.
"""
import json
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
from shoot import serve

OUT = ROOT / '_shots/ground_1008'
OUT.mkdir(parents=True, exist_ok=True)
checks = []


def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    print(('PASS ' if value else 'FAIL ') + name, flush=True)


port, stop = serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1100, 'height': 850})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html')
        page.wait_for_function('window.TDGAME && TDGAME.G.state === "title"', timeout=60000)
        page.evaluate('TDGAME.freeze()')
        page.evaluate("window.press=(key,held)=>window.dispatchEvent(new KeyboardEvent(held?'keydown':'keyup',{key}));")
        check('all generated loose assets decoded', page.evaluate('ART.progress(Object.keys(TD_GROUND_ART))===1'))
        page.locator('#screen').screenshot(path=str(OUT / 'title.png'))
        page.evaluate("press('enter',true);TDGAME.step();press('enter',false);TDGAME.step(50)")
        check('actual Start opens briefing', page.evaluate('TDGAME.G.state==="brief"'))
        page.locator('#screen').screenshot(path=str(OUT / 'brief.png'))
        page.evaluate("press('enter',true);TDGAME.step();press('enter',false);TDGAME.step()")
        check('actual Start deploys into ground stage', page.evaluate('TDGAME.G.state==="play"'))
        page.locator('#screen').screenshot(path=str(OUT / 'stage_start.png'))

        fresh = """TDGAME.start();const G=TDGAME.G,p=G.player;for(const u of G.units)u.dead=true;
          p.x=400;p.y=3000;p.inv=0;p.a=Math.PI;p.aim=Math.PI;TD.Input.pointer.active=false;TDGAME.step(2);"""
        r = page.evaluate("""() => {""" + fresh + """
          const x=p.x;press('d',true);TDGAME.step(12);press('d',false);TDGAME.step();return p.x-x;
        }""")
        check('direction change moves immediately instead of waiting to turn', r > 15)
        r = page.evaluate("""() => {""" + fresh + """
          const x=p.x,a=p.a;press('shift',true);press('d',true);press('e',true);press('j',true);
          TDGAME.step(22);const out={dx:p.x-x,hull:p.a-a,turret:p.aim-a,shot:G.shots.some(s=>Math.abs(TD.M.wrap(s.a-a))>.4)};
          for(const k of ['shift','d','e','j'])press(k,false);TDGAME.step();return out;
        }""")
        check('sideways strafe retains hull while turret rotates and fires', r['dx'] > 40 and abs(r['hull']) < 0.001 and abs(r['turret']) > 1 and r['shot'])
        r = page.evaluate("""() => {""" + fresh + """
          p.manualAim=999;p.aim=-Math.PI/2;const x=p.x;press('h',true);TDGAME.step(55);
          const charged=p.charge,back=p.x-x;press('h',false);TDGAME.step(1);
          const round=G.shots.find(s=>s.big);const kick=p.recoil;TDGAME.step(5);
          return {charged,back,kick,move:p.x-x,shot:!!round,aim:round&&round.a};
        }""")
        check('charged shot seats tank backward then delivers turret-aligned recoil', r['charged'] >= 40 and r['back'] < -2 and r['kick'] > 6 and r['move'] < -7 and r['shot'] and abs(r['aim'] + 1.570796) < 0.01)
        for level, color in [(1, 'gold'), (2, 'silver'), (3, 'crimson')]:
            page.evaluate("""() => {""" + fresh + f"""
              p.weapons=[{{id:'laser',lv:{level}}}];p.wi=0;press('j',true);TDGAME.step(4);press('j',false);
            }}""")
            page.locator('#screen').screenshot(path=str(OUT / f'laser_{color}.png'))
            check(f'laser tier {level} uses decoded {color} tank art', page.evaluate(f'!!ART.get("tank_laser_{color}") && TDGAME.G.shots.some(s=>s.k==="laser"&&s.lv==={level})'))
        r = page.evaluate("""() => {""" + fresh + """
          p.weapons=[{id:'homing',lv:3}];press('j',true);TDGAME.step();press('j',false);
          return G.shots.filter(s=>s.k==='homing').map(s=>s.a);
        }""")
        check('tank missile rack launches three distinct physical rounds', len(r) == 3 and len(set(r)) == 3)
        page.locator('#screen').screenshot(path=str(OUT / 'missiles.png'))

        r = page.evaluate("""() => {""" + fresh + """
          const s=G.structures.find(s=>s.kind==='warehouse');const before=TD.World.solidAt(s.x,s.y);
          TD.hitStructure(G,s,s.max+2);const freed=!TD.World.solidAt(s.x,s.y),los=TD.World.los(s.x-80,s.y,s.x+80,s.y);
          const fragments=TD.FX.list.filter(p=>p.k==='fragment').length;TDGAME.step(100);
          return {before,freed,los,fragments,rubble:s.dead,settled:G.wrecks.filter(w=>w.fragment).length};
        }""")
        check('building collapse clears movement/LOS and settles opaque fragments', r['before'] and r['freed'] and r['los'] and r['fragments'] >= 4 and r['settled'] >= 4)
        r = page.evaluate("""() => {""" + fresh + """
          const wall=G.structures.find(s=>s.kind==='barrier'), shot={r:4,dmg:20};
          const hit=TD.structureImpact(G,shot,wall.x,wall.y+80,wall.x,wall.y-80);
          return hit&&wall.dead&&!TD.World.solidAt(wall.x,wall.y);
        }""")
        check('swept high-speed shot breaks thin concrete cover', r)

        page.evaluate("""() => {""" + fresh + """p.x=400;p.y=650;p.inv=99999;TDGAME.step(200)}""")
        check('arena entry creates The Warrior with no Razorback reuse', page.evaluate('TDGAME.G.boss.name==="THE WARRIOR"'))
        page.wait_for_timeout(300)
        page.evaluate('TDGAME.render()')
        page.locator('#screen').screenshot(path=str(OUT / 'warrior_intact.png'))
        r = page.evaluate("""() => {const G=TDGAME.G,B=G.boss;B.state='broadside';B.t=0;B.targetX=580;
          const x=B.x;TDGAME.step(90);return {move:B.x-x,hull:B.a,upper:B.upper,shots:G.eshots.filter(s=>s.owner===B).length};}""")
        check('boss turns chassis sideways while upper body keeps fighting', r['move'] > 50 and abs(r['hull']) > 1.2 and abs(r['upper']) < 0.6 and r['shots'] > 0)
        page.locator('#screen').screenshot(path=str(OUT / 'warrior_broadside.png'))
        r = page.evaluate("""() => {const G=TDGAME.G,B=G.boss, wall=G.structures.find(s=>s.kind==='barrier'&&s.x===560&&s.y===555);
          B.x=560;B.y=405;B.state='ram';B.t=1.15;B.ramDir=0;TDGAME.step(16);
          return {destroyed:wall.dead,free:!TD.World.solidAt(wall.x,wall.y),concrete:TD.FX.list.some(p=>p.fam==='concrete_break_')};}""")
        check('actual boss ram shatters arena wall and opens its collision space', r['destroyed'] and r['free'] and r['concrete'])
        page.locator('#screen').screenshot(path=str(OUT / 'ram_wall_break.png'))
        r = page.evaluate("""() => {const G=TDGAME.G,B=G.boss;G.eshots.push({owner:B,part:'armL',k:'mg',x:400,y:500,t:0,vx:0,vy:1,r:4,dmg:1,life:50});
          B.damage('armL',999);return {gone:B.parts.armL===0,cleared:!G.eshots.some(s=>s.owner===B&&s.part==='armL'),
          fragment:TD.FX.list.some(p=>p.k==='fragment'&&p.key==='warrior_arm_l'&&!p.fade),recover:B.state==='recover'};}""")
        check('module break cancels owned shots and detaches exact solid rotating arm', all(r.values()))
        page.evaluate('TDGAME.step(10)')
        page.locator('#screen').screenshot(path=str(OUT / 'warrior_arm_break.png'))
        r = page.evaluate("""() => {const G=TDGAME.G,B=G.boss;B.damage('armR',999);B.damage('helmet',999);const exposed=B.parts.helmet===0;
          B.damage('hull',999);TDGAME.step(345);return {exposed,state:G.state,wreck:B.wrecked};}""")
        check('modular fight concludes with grounded wreck and mission results', r['exposed'] and r['state'] == 'clear' and r['wreck'])
        page.locator('#screen').screenshot(path=str(OUT / 'warrior_results.png'))
        # Restart must retire prior dust, debris, disabled colliders and attacks.
        page.evaluate('TDGAME.start();TDGAME.render()')
        check('restart restores scenery and retires old combat effects', page.evaluate('TDGAME.G.structures.every(s=>!s.dead) && TD.FX.list.length===0 && !TDGAME.G.boss'))
        page.evaluate("press('f1',true);TDGAME.step();press('f1',false);TDGAME.step()")
        check('Help opens control mapping without losing play state', page.evaluate('TDGAME.G.state==="help"'))
        page.locator('#screen').screenshot(path=str(OUT / 'controls.png'))
        page.evaluate("press('b',true);TDGAME.step();press('b',false);TDGAME.step()")
        check('logical B returns from Help', page.evaluate('TDGAME.G.state==="play"'))
        r=page.evaluate("""()=>{TDGAME.start();const G=TDGAME.G,p=G.player;for(const u of G.units)u.dead=true;p.inv=0;const x=p.x,y=p.y,a=p.a;TD.hurtPlayer(G,99);TDGAME.step(45);return p.dead&&!p.crashed&&p.x===x&&p.y===y&&p.a-a>Math.PI*1.5;}""")
        check('tank death stays anchored through its burning spin',r)
        page.locator('#screen').screenshot(path=str(OUT/'tank_death_spin.png'))
        r=page.evaluate("""()=>{const p=TDGAME.G.player;TDGAME.step(35);return p.crashed&&Math.abs(p.a-p.deathStart-Math.PI*4)<.001&&TDGAME.G.wrecks.filter(w=>w.player).length===1;}""")
        check('720-degree spin commits one crash, shock ring and solid wreck',r)
        page.locator('#screen').screenshot(path=str(OUT/'tank_death_crash.png'))
        check('zero page/console/missing-asset errors', not errors)
        (OUT / 'verification.json').write_text(json.dumps({'checks': checks, 'errors': errors}, indent=2), encoding='utf-8')
        browser.close()
finally:
    stop()
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed')
sys.exit(0 if all(c['passed'] for c in checks) else 1)
