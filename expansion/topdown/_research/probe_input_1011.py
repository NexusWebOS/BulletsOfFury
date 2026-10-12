"""Native input regressions: saved profiles, mixed input and post-intro fire.

Chromium polls synthetic hardware; aiming/shot checks run the actual player
and render authored tank art. Stores are isolated from the user's bindings.
"""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
import shoot

OUT = ROOT / '_shots/overdrive_input_1011'
OUT.mkdir(parents=True, exist_ok=True)
checks, errors, observations = [], [], {}


def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


port, stop = shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 960})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        page.add_init_script("""window.testPad={id:'Overdrive input regression pad',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:24},()=>({pressed:false,value:0}))};
          Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[testPad]});""")
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1011-input-r1')
        page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"', timeout=60000)
        page.evaluate('TDGAME.freeze()')
        page.wait_for_function('TD.FRONT_WARM.every(k=>!!ART.get(k))', timeout=30000)

        def frames(n=1):
            while n:
                k = min(n, 30)
                page.evaluate('n=>TDGAME.step(n)', k)
                page.wait_for_timeout(1)
                n -= k

        def fresh(style='six'):
            page.keyboard.up('w')
            page.keyboard.up('q')
            page.mouse.up()
            page.evaluate("""style=>{testPad.connected=true;testPad.axes=[0,0,0,0];for(const b of testPad.buttons){b.pressed=false;b.value=0;}
              TD.Input.update();TD.Input.setPadStyle(style);TD.Input.pointer.active=false;
              TDGAME.G.sel=0;TDGAME.start();const G=TDGAME.G,p=G.player;
              G.units=[];G.props=[];G.structures=[];G.pickups=[];TD.World.load(800,4000,[]);
              p.x=400;p.y=2200;p.inv=99999;p.a=p.aim=Math.PI;
              TD.Cam.follow(p.x,p.y,1);TDGAME.step(2);}""", style)

        def pad(*indices):
            page.evaluate("""indices=>{for(let i=0;i<testPad.buttons.length;i++){testPad.buttons[i].pressed=indices.includes(i);testPad.buttons[i].value=indices.includes(i)?1:0;}}""", list(indices))

        def point(dx, dy):
            pos = page.evaluate("""([dx,dy])=>{const p=TDGAME.G.player,r=document.getElementById('screen').getBoundingClientRect(),v=TD.Display;
              return{x:r.left+((p.x+dx-TD.Cam.x)*TD.Cam.zoom)*r.width/v.w,y:r.top+((p.y+dy-TD.Cam.y)*TD.Cam.zoom)*r.height/v.h};}""", [dx, dy])
            page.mouse.move(pos['x'], pos['y'])

        def shot_in(dx, dy):
            return page.evaluate("""([dx,dy])=>{const s=TDGAME.G.shots.at(-1);if(!s)return false;
              return(s.vx*dx+s.vy*dy)/(Math.hypot(s.vx,s.vy)*Math.hypot(dx,dy))>.97;}""", [dx, dy])

        fresh()
        page.keyboard.down('w');point(180,0);frames(20)
        check('keyboard drive with an idle connected pad still aims east with mouse', page.evaluate('Math.abs(TD.M.wrap(TDGAME.G.player.aim+Math.PI/2))<.15'))
        page.mouse.down();frames(2)
        check('mouse fire while keyboard drives follows the east-pointing turret', shot_in(1,0))
        page.mouse.up();page.keyboard.up('w')

        fresh();pad(12);point(-180,0);frames(20);page.mouse.down();frames(2)
        check('controller D-pad driving does not block westward mouse fire', shot_in(-1,0))
        page.mouse.up();pad()

        directions=[([2],0,-1),([2,1],1,-1),([1],1,0),([1,0],1,1),([0],0,1),([0,3],-1,1),([3],-1,0),([3,2],-1,-1)]
        for buttons, dx, dy in directions:
            fresh();point(160,0);pad(15,*buttons);frames(2)
            check(f'six-button independent directional fire {dx},{dy}', shot_in(dx,dy))

        fresh();point(160,0);frames(20)
        before_aim=page.evaluate('TDGAME.G.player.aim')
        page.keyboard.down('q');frames(8)
        check('Q turret rotation remains usable while the mouse rests over the playfield', page.evaluate('before=>TD.M.wrap(TDGAME.G.player.aim-before)<-.5',before_aim))
        page.keyboard.up('q');point(-170,0);frames(20)
        check('real mouse movement takes aiming back after keyboard turret rotation', page.evaluate('Math.abs(TD.M.wrap(TDGAME.G.player.aim-Math.PI/2))<.15'))

        fresh('standard');pad(12);point(175,0);frames(20);pad(12,0);frames(2)
        check('standard-pad driving and firing can use mouse aim independently', shot_in(1,0))
        pad();page.evaluate('testPad.axes[2]=-1');frames(20);pad(0);frames(2)
        check('standard right stick takes over the turret and fires west', shot_in(-1,0))
        point(170,0);frames(20)
        check('a moved mouse takes aim back from a held right stick', page.evaluate('Math.abs(TD.M.wrap(TDGAME.G.player.aim+Math.PI/2))<.15'))

        fresh();page.evaluate("""TD.Input.setPadBinding('up',16);TD.Input.setPadBinding('down',17);TD.Input.setPadBinding('left',18);TD.Input.setPadBinding('right',19);TD.Input.setPadBinding('A',12);TD.Input.setPadBinding('B',20);TD.Input.setPadBinding('X',21);TD.Input.setPadBinding('Y',22);TD.Input.setPadBinding('L',10);TD.Input.setPadBinding('R',11);""")
        pad(12);frames(2)
        check('custom A binding on physical button 12 fires south without default D-pad movement', shot_in(0,1) and page.evaluate('!TD.Input.down("up") && Math.abs(TDGAME.G.player.vy)<.01'))
        pad(16,20);frames(10)
        check('custom D-pad and face bindings drive north and fire east independently', shot_in(1,0) and page.evaluate('TDGAME.G.player.vy<0'))
        pad(16,10);frames(10);pad(10,22);frames(2)
        check('rebound L shoulder cruises north while the face button fires west', shot_in(-1,0) and page.evaluate('TDGAME.G.player.cruising && TDGAME.G.player.vy<0'))
        pad(11);frames(1)
        check('rebound R shoulder still activates Retina', page.evaluate('TD.Input.down("retina")'))
        pad();page.evaluate('testPad.connected=false');frames(1);page.evaluate('testPad.connected=true');frames(1)
        check('custom bindings survive controller disconnect and reconnect', page.evaluate('TD.Input.padProfile().A===12 && TD.Input.padProfile().right===19 && TD.Input.padProfile().R===11'))
        before = page.evaluate('localStorage.bof_td_controllers')
        page.reload();page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"',timeout=60000);page.evaluate('TDGAME.freeze();TD.Input.update()')
        check('saved custom controller bindings survive browser reload exactly', before==page.evaluate('localStorage.bof_td_controllers') and page.evaluate('TD.Input.padProfile().A===12 && TD.Input.padProfile().L===10'))

        fresh();pad(7)
        page.evaluate("""TD.Input.update();if(TD.Input.holdCombat)TDGAME.G.introFireLatch=TD.Input.holdCombat();else TDGAME.G.introFireLatch=true;""")
        pad(7,1);frames(2)
        check('holding Retina through introduction exit cannot suppress a new eastward shot', shot_in(1,0))
        fresh();pad(0);frames(1)
        page.evaluate("""TDGAME.G.shots=[];TDGAME.G.player.fireCd=0;if(TD.Input.holdCombat)TDGAME.G.introFireLatch=TD.Input.holdCombat();else TDGAME.G.introFireLatch=true;""")
        frames(2)
        check('the held inspection button cannot leak a shot across the introduction boundary', page.evaluate('TDGAME.G.shots.length===0'))
        point(-180,0);page.mouse.down();frames(20)
        check('a new mouse press can fire while the old inspection button is still held', shot_in(-1,0))
        page.mouse.up();pad();frames(1);pad(2);frames(10)
        check('controller northward fire resumes after release of the inspection button', shot_in(0,-1))

        fresh();pad(12);point(180,0);page.mouse.down();frames(20)
        page.wait_for_function('!!ART.get("pt_cole_turret") && !!ART.get("pt_cole_hull")',timeout=15000)
        page.evaluate('TDGAME.G.msgs=[];TDGAME.G.player.inv=0;TDGAME.render();TDGAME.G.player.inv=99999')
        page.locator('#screen').screenshot(path=str(OUT/'mouse_aim_while_controller_drives.png'))
        observations['mixedAim'] = page.evaluate('({aim:TDGAME.G.player.aim,hull:TDGAME.G.player.a,shots:TDGAME.G.shots.map(s=>({vx:s.vx,vy:s.vy})),pointer:TD.Input.pointer,bindings:TD.Input.padProfile()})')
        check('real rendered mixed input retains the 640x480 field', page.evaluate('TD.Display.w===640 && TD.Display.h===480'))
        check('browser has no page, console or asset errors',not errors)
        browser.close()
finally:
    stop()

report={'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'errors':errors,'observations':observations}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['passed','failed','errors']}),flush=True)
sys.exit(0 if not report['failed'] and not errors else 1)
