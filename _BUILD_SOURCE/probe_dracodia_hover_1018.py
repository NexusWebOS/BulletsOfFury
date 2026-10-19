"""Production Chromium: main hover, core launches and charged physical arms."""
from pathlib import Path
import ast, json, sys, http.server
from playwright.sync_api import sync_playwright
import shoot

R = Path(__file__).resolve().parents[1]
O = R / '_shots/dracodia_hover_1018/native'
O.mkdir(parents=True, exist_ok=True)
SETUP = next(ast.literal_eval(n.value) for n in ast.parse((R / '_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SETUP' for t in n.targets))
checks, errors, rows = [], [], []
http.server.ThreadingHTTPServer.request_queue_size = 128

def check(name, ok, data=None):
    checks.append(dict(name=name, passed=bool(ok), data=data))
    print(('PASS ' if ok else 'FAIL ') + name + ((' ' + json.dumps(data)) if not ok else ''), flush=True)

port, stop = shoot.serve(str(R))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(channel='msedge', args=['--mute-audio'])
        p = br.new_page(viewport=dict(width=1600, height=1000))
        p.set_default_timeout(180000)
        p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('console', lambda m: errors.append(m.text[:700]) if m.type == 'error' or 'draw error' in m.text else None)
        p.on('response', lambda r: errors.append(str(r.status) + ' ' + r.url.split('?')[0]) if r.status >= 400 else None)
        p.goto(f'http://127.0.0.1:{port}/index.html')
        p.wait_for_function('window.__bofFrames>4&&typeof D20!=="undefined"')
        p.evaluate(shoot.TRAP_RAF)
        p.wait_for_timeout(40)
        p.evaluate("pilotIndex=PILOTS.findIndex(q=>q.key==='cole');run.pilot='cole';startRun(8)")
        p.evaluate('''()=>{window.hovNativeHit=playerHit;window.hovHits=[];window.hovTrackHit=reason=>hovHits.push(reason);playerHit=hovTrackHit;
          window.hovPixels=fn=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();const a=ctx.getImageData(0,0,cv.width,cv.height).data;ctx.restore();return a;};
          window.hovDiff=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))>20)n++;return n;};
          window.hovTrace=[];window.hovEmissions=[];const nativeBomb=d20Bomb;d20Bomb=function(b,target){const m=d20BossMount(b,'core'),e=nativeBomb.apply(this,arguments);if(e)hovEmissions.push({kind:'bomb',actual:e._d20.start,expected:m,depth:b._r30.v18.archiveDepth});return e;};
          const nativeShot=v18Shot;v18Shot=function(b){const m=d20Main(b)?d20BossMount(b,'core'):null,q=nativeShot.apply(this,arguments);if(q?._d20Module==='core')hovEmissions.push({kind:'missile',actual:q._d20Origin,expected:m,shootable:q._shootable});return q;};
          window.hovObserve=()=>{const N=B._r30.v18,P=N.attack;hovTrace.push({x:B.x,y:B.y,depth:N.archiveDepth,type:P?.type,clock:B._r30.clock});};
        }''')

        def frames(n):
            for i in range(0, n, 12):
                p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);hovObserve();}}', min(12, n-i))
                p.wait_for_timeout(5)

        def snap(name):
            p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();}')
            p.screenshot(path=str(O / (name + '.png')))

        def setup(diff='normal'):
            p.evaluate(SETUP, dict(stage=8, diff=diff, kind='vileexistence', pilot='cole'))
            p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&d20Warm()&&bmfReady("game")}')
            p.evaluate('''()=>{s6Opening=null;story=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();AP10_X.intro=null;P2M.active=null;H3.ending=null;H3.release=false;
              stagePlan=[];warnT=0;warnKind=null;subBossDone=subBossTriggered=aminiTriggered=true;enemies=[];powerups=[];eBullets=[];pBullets=[];D20.events=[];D20.sparks=[];D20.blasts=[];
              v18Budget(B);v18Enter(B,2,0);B._r30.v18.arenaPhase=2;v18Fight(B);B._r30.cd=999;bossWarned=true;V19.events=[];player.x=worldWidth()/2;player.y=VH-70;
              run.shield=0;run.spaceMode=false;player.invuln=0;player.dead=player.out=false;playerHit=hovTrackHit;hovHits=[];hovTrace=[];hovEmissions=[];
              for(const k of ['j','k','y','a','d','w','s'])Input.keys[k]=false;SC12.refresh();__bofFit();}''')

        for diff in ['normal', 'hard', 'furious']:
            setup(diff)
            p.evaluate('window.hovClock=B._r30.clock')
            frames(480)
            hover = p.evaluate('''()=>({span:Math.max(...hovTrace.map(q=>q.x))-Math.min(...hovTrace.map(q=>q.x)),width:viewW(),step:Math.max(...hovTrace.slice(1).map((q,i)=>Math.hypot(q.x-hovTrace[i].x,q.y-hovTrace[i].y))),clock:B._r30.clock-hovClock,both:hovTrace.some(q=>q.x<worldWidth()/2-50)&&hovTrace.some(q=>q.x>worldWidth()/2+50)})''')
            rows.append(dict(diff=diff, hover=hover))
            check(diff+' standard hover crosses both sides of the arena', hover['both'] and hover['span'] > hover['width']*.2, hover)
            check(diff+' hover remains continuous and advances the native clock once', hover['step'] < 5 and abs(hover['clock']-8) < .001, hover)
            snap(diff+'-standard-hover')
            setup(diff)
            p.evaluate('d20Start(B,"codeBombs")')
            frames(395)
            bombs = p.evaluate('''()=>({n:hovEmissions.filter(e=>e.kind==='bomb').length,error:Math.max(...hovEmissions.map(e=>Math.hypot(e.actual.x-e.expected.x,e.actual.y-e.expected.y))),span:Math.max(...hovTrace.map(q=>q.x))-Math.min(...hovTrace.map(q=>q.x)),step:Math.max(...hovTrace.slice(1).map((q,i)=>Math.hypot(q.x-hovTrace[i].x,q.y-hovTrace[i].y))),depth:Math.min(...hovTrace.map(q=>q.depth))})''')
            check(diff+' bomb volley keeps moving horizontally while in the background', bombs['span'] > 100 and bombs['depth'] < .6, bombs)
            check(diff+' all five bombs launch at the actual depth-scaled core', bombs['n'] == 5 and bombs['error'] < .001, bombs)
            check(diff+' returning from the volley has no body-position snap', bombs['step'] < 8, bombs)
            snap(diff+'-bomb-return')
            setup(diff)
            p.evaluate('d20Start(B,"coreMissiles");window.hovTell=B._r30.v18.attack.tell')
            frames(35)
            check(diff+' core missiles have a visible harmless charge', p.evaluate('!eBullets.some(q=>q._d20Module)&&hovDiff(hovPixels(()=>{}),hovPixels(()=>d20Warnings(B)))>60'))
            frames(80)
            shots = p.evaluate('''()=>({count:hovEmissions.filter(e=>e.kind==='missile').length,error:Math.max(...hovEmissions.map(e=>Math.hypot(e.actual.x-e.expected.x,e.actual.y-e.expected.y))),allCore:eBullets.filter(q=>q._d20Owner===B).every(q=>q._d20Module==='core'&&q._shootable&&!q._finaleTurn),opaque:v18Rig(B).filter(v=>v.p.id==='core').every(v=>v18Mask(v.a)[139*320+160]>48)})''')
            check(diff+' every missile starts on the visible core and remains shootable', shots['count'] >= 3 and shots['error'] < .001 and shots['allCore'] and shots['opaque'], shots)
            snap(diff+'-core-missiles')
            setup(diff)
            p.evaluate('d20Start(B,"armLasers")')
            frames(40)
            charge = p.evaluate('''()=>({events:D20.events.filter(e=>e.event==='arm-charge'),fired:D20.events.some(e=>e.event==='arm-laser'),hits:hovHits.filter(s=>s?.includes('arm laser')),warning:hovDiff(hovPixels(()=>{}),hovPixels(()=>d20Warnings(B))),energy:hovDiff(hovPixels(()=>v19Body(B)),hovPixels(()=>{v19Body(B);d20ArmEffects(B);})),rot:v18Rig(B).find(v=>v.p.id==='left').rot})''')
            check(diff+' arm charges, physically aims and draws a lane before damage', charge['events'] and not charge['fired'] and not charge['hits'] and charge['warning'] > 100 and charge['energy'] > 100 and abs(charge['rot']) > .02, charge)
            snap(diff+'-arm-charge')
            p.evaluate('window.hovTarget={...B._r30.v18.attack.arms[0].target}')
            frames(int(p.evaluate('B._r30.v18.attack.tell')*60)-40+6)
            beam = p.evaluate('''()=>{const q=B._r30.v18.attack.arms[0],L=d20ArmLane(B,q),v=v18Rig(B).find(v=>v.p.id===q.id),m=d20BossMount(B,q.id);return{fired:q.released,hit:hovHits.some(s=>s?.includes(q.id+' arm laser')),error:Math.hypot(m.x-L.x,m.y-L.y),opaque:v18Mask(v.a)[198*320+(q.id==='left'?75:245)]>48,beamPixels:hovDiff(hovPixels(()=>v19Body(B)),hovPixels(()=>{v19Body(B);d20ArmEffects(B);})),clock:B._r30.clock};}''')
            check(diff+' laser fires from the charged physical palm and damages its warned lane', beam['fired'] and beam['hit'] and beam['error'] < .001 and beam['opaque'] and beam['beamPixels'] > 1000, beam)
            snap(diff+'-arm-laser')
            p.evaluate('player.x=camLeftX()+20;player.y=viewTopY()+85;hovHits=[]')
            frames(6)
            check(diff+' released aim stays committed when the player dodges', p.evaluate('Math.hypot(B._r30.v18.attack.arms[0].target.x-hovTarget.x,B._r30.v18.attack.arms[0].target.y-hovTarget.y)<.001&&!hovHits.some(s=>s?.includes("arm laser"))'))
            flash = p.evaluate('''()=>{const v=v18Rig(B).find(v=>v.p.id==='left'),a=hovPixels(()=>v19Body(B)),hp=B.hp;B._lastPart=v.p;hitBoss(1);return{damage:hp-B.hp,part:v.p.flash,owner:B.flash,pixels:hovDiff(a,hovPixels(()=>v19Body(B)))};}''')
            check(diff+' charged rotating arms retain native owner and part hit flashes', flash['damage'] > 0 and flash['part'] > 0 and flash['owner'] > 0 and flash['pixels'] > 20, flash)
            frames(12)
            check(diff+' arm hit flash expires normally', p.evaluate('B.flash<=0&&B.parts.every(p=>p.flash<=0)'))
            p.evaluate('B._lastPart=B.parts.find(p=>p.id==="left");hitBoss(B._lastPart.hp+.1);hovHits=[]')
            frames(2)
            check(diff+' destroying an arm immediately removes its laser and Retina target', p.evaluate('!d20BossMount(B,"left")&&!v18Rig(B).some(v=>v.p.id==="left")&&!retinaBossTargets(B).some(q=>!q.dead&&q.kind?.includes("left"))&&!hovHits.some(s=>s==="Dracodia left arm laser")'))
            frames(180)
            check(diff+' the surviving right arm still charges and fires independently', p.evaluate('D20.events.some(e=>e.event==="arm-charge"&&e.side==="right")&&D20.events.some(e=>e.event==="arm-laser"&&e.side==="right")'))
            p.evaluate('v18Clear(B)')
            check(diff+' phase cleanup cancels charged arms and core ordnance', p.evaluate('!B._r30.v18.attack&&!eBullets.some(q=>q._d20Owner===B)&&!D20.sparks.length'))

        setup()
        p.evaluate('d20Start(B,"coreMissiles")')
        frames(115)
        p.evaluate('''()=>{window.hovMissile=eBullets.find(q=>q._d20Module==='core'&&!q.dead);window.hovMissileHP=hovMissile.hp;
          B._r30.v18.attack=null;B._r30.cd=999;player.x=hovMissile.x+hovMissile.vx*7;player.y=hovMissile.y+70;run.weapon=0;run.wlevels[0]=run.wlevel=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;chaingunUnlocked=false;run._earnedUnlocks.chaingun=false;player.fireT=0;Input.keys.j=true;}''')
        frames(24)
        p.evaluate('Input.keys.j=false')
        check('actual centered machine-gun fire can intercept a core missile', p.evaluate('hovMissile.hp<hovMissileHP||hovMissile.dead'))
        setup()
        p.evaluate('''()=>{for(const id of ['left','right']){B._lastPart=B.parts.find(p=>p.id===id);hitBoss(B._lastPart.hp+.1);}d20Start(B,'armLasers');}''')
        check('destroying both arms replaces the laser turn with a core attack', p.evaluate('B._r30.v18.attack.type==="coreMissiles"&&v18Rig(B).every(v=>v.p.id==="core")'))
        setup()
        p.evaluate('d20Start(B,"armLasers")')
        frames(80)
        p.evaluate('''()=>{const q=B._r30.v18.attack.arms[0];player.x=q.target.x;player.y=q.target.y;run.shield=0;player.invuln=0;window.hovDeaths=stageStats.deaths;playerHit=hovNativeHit;}''')
        frames(4)
        native = p.evaluate('({dead:player.dead,deaths:stageStats.deaths,before:hovDeaths,shield:run.shield,invuln:player.invuln})')
        check('arm laser uses the actual native player death path', native['dead'] and native['deaths'] > native['before'], native)
        setup()
        p.evaluate('window.hovDeaths=stageStats.deaths;d20Start(B,"armLasers");player.invuln=1000;playerHit=hovNativeHit')
        frames(150)
        check('arm laser respects native invulnerability', p.evaluate('!player.dead&&stageStats.deaths===hovDeaths'))
        setup()
        p.evaluate('B._r30.cd=0;for(const i of V18.forms)if(i!==0)j3State(B).hp[i]=0')
        frames(3480)
        events = p.evaluate('D20.events.filter(e=>e.event==="main-release").map(e=>e.type)')
        check('natural main form uses core missiles and arm lasers as well as physical swipes', 'coreMissiles' in events and 'armLasers' in events and p.evaluate('V19.events.some(e=>e.event==="swipe-release")'), events)
        check('exactly four copied forms remain after the main form', p.evaluate('JSON.stringify(V18.forms)===JSON.stringify([0,8,1,6,2])'))
        check('no page, console, drawing or asset errors', not errors, errors[:30])
        br.close()
finally:
    stop()

data = dict(passed=sum(c['passed'] for c in checks), failed=sum(not c['passed'] for c in checks), checks=checks, rows=rows, errors=errors)
(O / 'results.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
print(json.dumps({k:data[k] for k in ['passed','failed','errors']}))
sys.exit(bool(data['failed']))
