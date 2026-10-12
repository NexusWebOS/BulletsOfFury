"""Real Chromium reproduction of the road-to-Warrior sizing correction.

Protected encounter fixtures inspect framing; keyboard entry, mouse aim,
fullscreen, menus and a complete live attack cycle use the actual runtime.
"""
from pathlib import Path
import json, math, sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
from shoot import serve

OUT = ROOT / '_shots/overdrive_sizing_1011'
OUT.mkdir(parents=True, exist_ok=True)
checks, errors, observations = [], [], {}


def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    print(('PASS ' if value else 'FAIL ') + name, flush=True)


def frames(n):
    while n:
        batch = min(n, 24)
        page.evaluate('(n)=>TDGAME.step(n)', batch)
        page.wait_for_timeout(1)
        n -= batch


def display():
    return page.evaluate('''()=>{const r=document.getElementById('screen').getBoundingClientRect();
      return {x:r.x,y:r.y,w:r.width,h:r.height,window:[innerWidth,innerHeight],
        world:[TD.VW,TD.VH],display:TD.Display,zoom:TD.Cam.zoom};}''')


def framing():
    return page.evaluate('''()=>{const G=TDGAME.G,B=G.boss,b=B.bounds(),p=G.player,c=TD.Cam;
      return {boss:b,player:{x:p.x,y:p.y},camera:{x:c.x,y:c.y},view:[TD.VW,TD.VH],
        visible:b.left>=c.x-1&&b.right<=c.x+TD.VW+1&&b.top>=c.y-1&&b.bottom<=c.y+TD.VH+1,
        playerVisible:p.x-22>=c.x&&p.x+22<=c.x+TD.VW&&p.y-32>=c.y&&p.y+32<=c.y+TD.VH};}''')


def snap(name):
    page.evaluate('TDGAME.G.player.inv=0;TD.Cam.shake=0;TDGAME.render()')
    page.screenshot(path=str(OUT / (name + '.png')))
    page.evaluate('TDGAME.G.player.inv=99999')


port, stop = serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1612, 'height': 878})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1011-sizing')
        page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"', timeout=60000)
        page.evaluate('TDGAME.freeze()')
        page.keyboard.press('Enter')
        page.evaluate('TDGAME.G.sel=0;TDGAME.start();TDGAME.G.units=[];TDGAME.G.player.inv=99999')
        page.wait_for_function('Object.keys(TD_WARRIOR_ART.assets).every(k=>!!ART.get(k))')
        sizes = [(1612,878),(1469,796),(1920,1080),(1100,850),(520,650)]
        for width, height in sizes:
            label = f'{width}x{height}'
            page.set_viewport_size({'width': width, 'height': height})
            page.evaluate('''TDGAME.G.sel=0;TDGAME.start();const G=TDGAME.G,p=G.player;
              G.units=[];p.x=400;p.y=830;p.a=p.aim=Math.PI;p.inv=99999;
              TD.Cam.follow(p.x,p.y-24,1);TDGAME.render();''')
            before = display()
            if width in (1612,1920):
                snap('approach_' + label)
            page.keyboard.down('w')
            frames(70)
            page.keyboard.up('w')
            frames(160)
            check(label + ': real northward driving enters the Warrior arena', page.evaluate('!!TDGAME.G.boss && TDGAME.G.player.y<690'))
            after = display()
            observations[label] = {'approach': before, 'arena': after}
            check(label + ': boss entry keeps the same canvas size and tank scale', abs(before['w']-after['w'])<.1 and abs(before['h']-after['h'])<.1 and before['zoom']==after['zoom']==1)
            check(label + ': gameplay retains a proportional 4:3 field', abs(after['w']/after['h']-4/3)<.002)
            check(label + ': the canvas uses the available height or width without cropping', after['x']>=-.1 and after['y']>=-.1 and after['x']+after['w']<=width+.1 and after['y']+after['h']<=height+.1 and (height-after['h']<=4.1 or width-after['w']<=.1))
            page.evaluate('''const G=TDGAME.G,B=G.boss,p=G.player;G.shots=[];G.eshots=[];
              B.state='recover';B.cooldown=999;B.x=400;B.y=472;B.a=B.upper=0;
              p.x=400;p.y=650;p.vx=p.vy=0;TD.Input.pointer.active=false;''')
            frames(80)
            check(label + ': complete front-facing boss and tank are visible', framing()['visible'] and framing()['playerVisible'])
            snap('arena_front_' + label)
            for side, x, px, angle in [('right',605,82,-math.pi/2), ('left',195,718,math.pi/2)]:
                page.evaluate('''([x,px,a])=>{const G=TDGAME.G,B=G.boss,p=G.player;
                  B.x=x;B.y=472;B.a=a;B.upper=px<x?.45:-.45;
                  p.x=px;p.y=620;p.vx=p.vy=0;G.shots=[];G.eshots=[];}''', [x,px,angle])
                frames(90)
                result = framing()
                observations[label][side] = result
                check(label + ': full sideways boss remains visible opposite the tank on the ' + side, result['visible'] and result['playerVisible'])
                if width in (1469,1920):
                    snap('arena_' + side + '_' + label)
            r = page.locator('#screen').bounding_box()
            page.mouse.move(r['x']+r['width']*.65,r['y']+r['height']*.55)
            frames(1)
            check(label + ': mouse turret aim maps to the resized world correctly', page.evaluate('''()=>{const p=TDGAME.G.player,c=TD.Cam;
              return Math.abs(TD.M.wrap(TD.Input.aim(p)-TD.M.angTo(p.x,p.y,c.x+TD.VW*.65,c.y+TD.VH*.55)))<.001;}'''))
            page.evaluate('TD.Input.pointer.active=false')

        page.set_viewport_size({'width':1920,'height':1080})
        page.evaluate('''const G=TDGAME.G,B=G.boss,p=G.player;B.x=400;B.y=B.homeY;B.a=B.upper=0;
          B.state='recover';B.cooldown=0;B.cycle=0;p.x=80;p.y=620;G.eshots=[];''')
        live = []
        for i in range(100):
            frames(12)
            live.append(framing())
            if i in (15,35,65,85):
                snap('live_cycle_' + str(i))
        observations['liveCycle'] = {'samples':len(live), 'bossVisible':sum(r['visible'] for r in live), 'tankVisible':sum(r['playerVisible'] for r in live), 'phases':page.evaluate('TDGAME.G.boss.phaseHistory')}
        check('live broadside, lasers, missile volleys and ram all run', all(k in observations['liveCycle']['phases'] for k in ['broadside','laser','rack','ram']))
        check('every sampled live attack keeps the whole boss and tank on screen', all(r['visible'] and r['playerVisible'] for r in live))
        actual = page.evaluate('''()=>{const c=document.getElementById('screen').getContext('2d'),draw=c.drawImage,art=ART.draw,keys=[];let key;
          ART.draw=function(ctx,k,...args){const old=key;key=k;try{return art.call(this,ctx,k,...args);}finally{key=old;}};
          c.drawImage=function(...args){if(key)keys.push(key);return draw.apply(this,args);};
          try{TDGAME.render();return keys;}finally{c.drawImage=draw;ART.draw=art;}}''')
        check('the game context actually draws all four mounted Warrior art keys', all(k in actual for k in ['warrior_hull','warrior_helmet','warrior_arm_l','warrior_arm_r']))

        page.keyboard.press('Alt+Enter')
        page.wait_for_function('!!document.fullscreenElement')
        check('Alt+Enter enters fullscreen without changing the active fight', page.evaluate('TDGAME.G.state==="play" && !!TDGAME.G.boss && TD.VW===800 && TD.VH===600'))
        snap('arena_fullscreen')
        page.keyboard.press('Alt+Enter')
        page.wait_for_function('!document.fullscreenElement')
        check('fullscreen exit preserves the fixed road and arena view', page.evaluate('TD.Display.w===800 && TD.Display.h===600'))
        page.evaluate('TD.Frontend.returnTo="pause";TD.Frontend.go("pause")')
        frames(50)
        check('pause retains its own menu viewport and four authored buttons', page.evaluate('TD.Display.w===640 && TD.Display.h===512 && TD.Frontend.rects.length===4'))
        page.evaluate('TD.Frontend.go("options")')
        frames(20)
        check('the exact original Options panel retains 480x512 and four volume strips', page.evaluate('TD.Display.w===480 && TD.Display.h===512 && TD.OriginalOptions.rows().filter(r=>r.t==="vol").length===4'))
        page.set_viewport_size({'width':520,'height':650})
        frames(10)
        snap('options_narrow')
        r=display()
        check('Options fits a narrow browser without changing its panel proportions', r['x']>=-.1 and r['y']>=-.1 and abs(r['w']/r['h']-480/512)<.002)
        page.evaluate('TDGAME.resume()')
        frames(60)
        check('resuming from Options restores the same large gameplay viewport', page.evaluate('TD.Display.w===800 && TD.Display.h===600 && TD.VW===800 && TD.VH===600'))
        page.evaluate('TDGAME.G.sel=TD.MISSIONS.findIndex(m=>m.id===4);TDGAME.start()')
        frames(2)
        check('the next tank mission retains its existing 480x360 world layout', page.evaluate('TDGAME.G.mission===4 && TD.VW===480 && TD.VH===360'))
        page.evaluate('TDGAME.G.sel=TD.MISSIONS.findIndex(m=>m.id===5);TDGAME.start()')
        frames(2)
        check('the on-foot museum and its authored alert-cone buffer retain their layout', page.evaluate('TDGAME.G.mission===5 && TD.VW===480 && TD.VH===360 && TD.Stealth.coneCanvas.width===480 && TD.Stealth.coneCanvas.height===360'))
        page.evaluate('TDGAME.G.sel=0;TDGAME.launchBrief()')
        frames(190)
        snap('briefing_narrow')
        check('restarting Level 2 restores its wider view and centered briefing', page.evaluate('TDGAME.G.state==="brief" && TD.VW===800 && TD.VH===600'))
        check('zero page, console or missing-asset errors', not errors)
        (OUT/'verification.json').write_text(json.dumps({'checks':checks,'errors':errors,'observations':observations},indent=2),encoding='utf-8')
        browser.close()
finally:
    stop()
print(f'{sum(c["passed"] for c in checks)}/{len(checks)} checks passed',flush=True)
sys.exit(0 if all(c['passed'] for c in checks) and not errors else 1)
