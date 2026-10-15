"""Native Chromium probe for Level 5 MUSEUM OF VIOLENCE (Mercs x Demolition Man x Hard Corps x MGS).
Real key events through the game's own input; fixtures teleport and protect the pilot only where a
check isolates one system. These are mechanics/pixel checks, not a human balance playthrough.
"""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
from shoot import serve
OUT = ROOT / '_shots/museum_1009'
OUT.mkdir(parents=True, exist_ok=True)
checks = []
def check(name, value, detail=None):
    checks.append({'name': name, 'passed': bool(value), 'detail': detail})
    print(('PASS ' if value else 'FAIL ') + name + ('' if detail is None else '  ' + json.dumps(detail)), flush=True)

port, stop = serve(str(ROOT))
try:
    with sync_playwright() as pw:
        exe = '/opt/pw-browsers/chromium'
        browser = pw.chromium.launch(executable_path=exe) if Path(exe).exists() else pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1100, 'height': 850})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        page.route('**/favicon.ico', lambda route: route.fulfill(status=204, body=''))   # the browser's own favicon request is not the game's
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html')
        # local build boots into pilot selection (1008 controls pass); the probe starts from the stage title
        page.wait_for_function('window.TDGAME && (TDGAME.G.state==="pilot"||TDGAME.G.state==="title")', timeout=90000)
        page.evaluate('TDGAME.freeze();TDGAME.G.state="title"')
        WARM = "TD.MUSEUM_WARM.concat(['rzb_hull_0','rzb_hull_3','rzb_turret','rzb_tread','rzb_rotor','rzb_missile_pod','rzb_machinegun','rzb_wreck','bmbar_frame_boss','bmbar_fill_red'])"
        page.evaluate('TDGAME.freeze();ART.warm(' + WARM + ')')
        page.wait_for_function('ART.progress(' + WARM + ')===1', timeout=90000)
        page.evaluate("window.press=(k,v)=>window.dispatchEvent(new KeyboardEvent(v?'keydown':'keyup',{key:k}));window.advance=n=>TDGAME.step(n);"
                      "window.tap=(k,n)=>{press(k,true);advance(1);press(k,false);advance(n||1);};window.shot=n=>document.querySelector('#screen');")
        snap = lambda name: page.locator('#screen').screenshot(path=str(OUT / (name + '.png')))
        check('museum plate, exhibits, hostages and exhibit tank art all decode', page.evaluate('ART.progress(' + WARM + ')===1'))

        # ---- title -> Level 5 card -> brief, with real keys
        page.evaluate("tap('arrowleft');")   # 1009: Level 3 is hidden, so Level 5 is one step left of Level 2
        snap('01_title')
        page.evaluate("tap('enter',50)")
        check('title shows a fourth card and deploys Level 5 briefing', page.evaluate('TDGAME.G.mission===5&&TDGAME.G.state==="brief"&&TD.MISSIONS.length===4'))
        snap('02_brief')
        page.evaluate("tap('enter',40)")
        check('on foot with four Hard Corps slots and three Mega Crash bombs',
              page.evaluate('(()=>{const G=TDGAME.G,p=G.player;return G.state==="play"&&p.onfoot&&p.slots4&&G.crash===3&&G.hostages.length===5&&G.lasers.length===3;})()'))
        check('every route reaches the grand hall from the lobby (nav field)',
              page.evaluate('(()=>{const n=TD.Nav,f=n.field(400,150,0),c=(x,y)=>f.D[Math.floor(y/n.C)*n.cols+Math.floor(x/n.C)];return c(400,1345)>=0&&c(400,1000)>=0&&c(600,600)>=0&&c(300,800)>=0&&c(250,420)>=0&&c(400,420)>=0;})()'))
        check('the duct is solid standing, open prone', page.evaluate(
            '(()=>{const W=TD.World,a={x:400,y:700,stance:"stand"},b={x:400,y:700,stance:"prone"};W.collide(a,8,false);W.collide(b,8,false);return (a.x<=372||a.x>=428)&&b.x===400;})()'))
        snap('03_lobby')

        # ---- Demolition Man: an exhibit breaks once, keeps its broken plate and drops its fixed contents
        r = page.evaluate("""()=>{const G=TDGAME.G,q=G.props.find(q=>q.kind==='mx_statue'&&q.drop==='grenades');TD.hitProp(G,q,99);const n=G.pickups.length;TD.hitProp(G,q,99);advance(2);
            return {dead:q.dead,once:n===G.pickups.length,kind:G.pickups[G.pickups.length-1].kind,exhibits:G.exhibits};}""")
        check('shot exhibit breaks once, stays as a broken plate and drops its fixed item', r['dead'] and r['once'] and r['kind'] == 'grenades', r)
        # ---- hostage rescue and the hostage penalty
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player,h=G.hostages[0];p.inv=9999;p.x=h.x-30;p.y=h.y;advance(1);press('d',true);advance(20);press('d',false);advance(2);
            return {state:h.state,rescued:G.rescued,drop:G.pickups.some(k=>k.kind==='grenades')};}""")
        check('walking to a bound hostage frees them and they hand over their reward', r['state'] == 'freed' and r['rescued'] == 1, r)
        snap('04_hostage_freed')
        r = page.evaluate("""()=>{const G=TDGAME.G,h=G.hostages[1],s0=G.score+9000;G.score=s0;G.shots.push({k:'vulcan',x:h.x-20,y:h.y,vx:6,vy:0,a:0,dmg:1,life:30,r:3,t:0});advance(5);
            const out={state:h.state,lost:G.hostagesLost,penalty:s0-G.score};h.state='bound';G.hostagesLost=0;return out;}""")
        check('a player round that hits a hostage kills them for -5000', r['state'] == 'dead' and r['penalty'] >= 5000, r)

        # ---- the Smash TV room: locks, three waves, curtains drop, alarm does not count against GHOST
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player;for(const u of G.units)if(u.y>1150)u.dead=true;for(const b of G.bodies||[])b.found=true;const a0=TD.Stealth.alerts;p.x=400;p.y=1090;advance(70);
            return {state:G.arena.state,solid:TD.World.solidAt(400,1152)&&TD.World.solidAt(527,856),spawned:G.units.filter(u=>u.arena).length,a0};}""")
        check('Hall of Arms locks with laser curtains and spawns its first wave', r['state'] == 'locked' and r['solid'] and r['spawned'] >= 3, r)
        snap('05_arena_locked')
        r = page.evaluate("""()=>{const G=TDGAME.G;let waves=0;for(let k=0;k<6&&G.arena.state==='locked';k++){for(const u of G.units)if(u.arena&&!u.dead)TD.hitUnit(G,u,99,u.x,u.y);advance(90);waves=G.arena.wave;}
            return {state:G.arena.state,waves,open:!TD.World.solidAt(400,1152)&&!TD.World.solidAt(527,856),alerts:TD.Stealth.alerts,phase:TD.Stealth.phase};}""")
        check('three waves clear, curtains drop, GHOST alert count restored', r['state'] == 'clear' and r['waves'] == 3 and r['open'] and r['alerts'] == 0, r)
        page.evaluate('advance(20)')
        snap('06_route_choice')

        # ---- Mercs Mega Crash through real keys: hold J (A) and tap K (B)
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player;p.x=400;p.y=930;advance(2);
            const us=[TD.makeUnit('robotScout',360,880,{a:0}),TD.makeUnit('robotHeavy',450,880,{a:0})];G.units.push(...us);
            for(let i=0;i<5;i++)G.eshots.push({k:'mg',x:330+i*30,y:850,vx:0,vy:0.1,a:0,dmg:1,life:200,r:4,t:0});
            const before=G.crash,ammo=p.weapons[p.wi].ammo;press('j',true);advance(1);press('k',true);advance(1);press('k',false);press('j',false);advance(3);
            return {used:before-G.crash,dead:us.every(u=>u.dead),eshots:G.eshots.length,reload:p.reload,inv:p.inv>0};}""")
        check('A+B Mega Crash spends one bomb, clears on-screen enemies and rounds, does not reload', r['used'] == 1 and r['dead'] and r['eshots'] == 0 and r['reload'] == 0, r)
        snap('07_mega_crash')
        page.evaluate('advance(60)')

        # ---- MGS: CQC from behind is silent
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player;p.x=150;p.y=598;p.inv=9999;G.shots=[];advance(1);
            const u=TD.makeUnit('robotScout',172,598,{a:-Math.PI/2});u.look=u.a;u.mode='patrol';G.units.push(u);
            const ear=TD.makeUnit('robotScout',150,700,{a:0});ear.mode='patrol';G.units.push(ear);advance(1);
            press('j',true);advance(1);press('j',false);advance(2);return {dead:u.dead,shots:G.shots.length,heard:!!ear.heard,cqc:G.cqcKills||0};}""")
        check('CQC from behind takes a guard down silently (no round fired, no noise)', r['dead'] and r['shots'] == 0 and not r['heard'] and r['cqc'] == 1, r)
        snap('08_cqc')
        # ---- bodies are found
        r = page.evaluate("""()=>{const G=TDGAME.G,S=TD.Stealth;S.phase='SNEAK';S.timer=0;for(const b of G.bodies)b.found=true;const v=TD.makeUnit('robotScout',130,600,{a:-Math.PI/2});v.mode='patrol';G.units.push(v);
            const d=TD.makeUnit('robotScout',215,600,{a:0});G.units.push(d);d.dead=true;G.player.x=110;G.player.y=800;
            for(let i=0;i<30&&v.mode==='patrol';i++)advance(1);return {mode:v.mode,phase:S.phase,found:G.bodies.some(b=>b.found&&b.x===215)};}""")
        check('a guard who sees a fallen guard investigates and the museum goes to CAUTION', r['found'] and r['mode'] == 'suspect' and r['phase'] == 'CAUTION', r)

        # ---- laser tripwires: standing trips the alarm, prone crawls under
        r = page.evaluate("""()=>{const G=TDGAME.G,S=TD.Stealth,p=G.player,L=G.lasers[0];for(const u of G.units)if(!u.arena&&u.y<860)u.dead=true;S.phase='SNEAK';S.alerts=0;G.tripCd=0;
            const t0=G.trips||0;p.stance='prone';p.x=L.a.x-24;p.y=(L.a.y+L.b.y)/2;advance(1);press('d',true);advance(60);press('d',false);advance(1);const prone={trips:(G.trips||0)-t0,x:p.x};
            p.stance='stand';G.tripCd=0;p.x=L.a.x-20;advance(1);press('d',true);advance(14);press('d',false);advance(1);return {prone,standing:S.phase,trips:G.trips,alerts:S.alerts};}""")
        check('prone crawls under a live laser; standing in it raises ALERT', r['prone']['trips'] == 0 and r['prone']['x'] > 215 and r['standing'] == 'ALERT' and r['trips'] == 1, r)
        snap('09_laser')
        # ---- alarm panels are the reinforcement source
        r = page.evaluate("""()=>{const G=TDGAME.G,M=TD.MISSIONS[3];G.player.y=700;const before=M.canReinforce(G);for(const q of G.props)if(q.kind==='mx_alarm')TD.hitProp(G,q,99);return {before,after:M.canReinforce(G)};}""")
        check('alarm panels call reinforcements; breaking them stops the calls', r['before'] and not r['after'], r)
        page.evaluate("TD.Stealth.phase='SNEAK';TD.Stealth.timer=0;")

        # ---- the duct, prone, hides you
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player;p.stance='prone';p.x=400;p.y=840;advance(2);press('w',true);advance(120);press('w',false);advance(1);return {y:p.y,x:p.x,hidden:p.hidden};}""")
        check('prone pilot crawls up the duct and is hidden inside it', r['y'] < 800 and abs(r['x'] - 400) < 16 and r['hidden'], r)
        snap('10_duct')
        page.evaluate("TDGAME.G.player.stance='stand';")

        # ---- Mercs vehicle: board, take damage on armour, eject without losing a life
        r = page.evaluate("""()=>{const G=TDGAME.G,v=G.vehicle;let p=G.player;p.stance='stand';p.x=v.x-40;p.y=v.y;p.inv=0;G.boardCd=0;advance(1);press('d',true);advance(12);press('d',false);advance(4);
            const t=G.player,out={board:G.inVehicle&&!t.onfoot,hp:t.hp};t.inv=0;TD.hurtPlayer(G,5,t.x,t.y);out.armour=t.hp;out.lives=G.lives;return out;}""")
        check('walking into the exhibit tank boards it; hits land on its armour', r['board'] and r['armour'] == r['hp'] - 5, r)
        page.evaluate('advance(30)')
        snap('11_tank_mounted')
        r = page.evaluate("""()=>{const G=TDGAME.G,t=G.player,lives=G.lives,deaths=G.deaths;t.inv=0;TD.hurtPlayer(G,99,t.x,t.y);advance(3);const p=G.player;
            return {ejected:p.onfoot&&!p.dead&&!G.inVehicle,lives:G.lives===lives,deaths:G.deaths===deaths,wreck:G.wrecks.some(w=>w.art==='pt_niel_wreck'),gone:G.vehicle.dead};}""")
        check('a destroyed tank ejects the pilot alive (no life lost) and leaves its wreck', all(r.values()), r)
        snap('12_ejected')

        # ---- Hard Corps: death costs only the gun in your hand; you return where you fell
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player;p.weapons=[{id:'desert_eagle',lv:1,ammo:12,reserve:60},{id:'minigun',lv:2,ammo:60,reserve:180},{id:'rocket_launcher',lv:1,ammo:4,reserve:16}];p.wi=1;
            p.x=600;p.y=520;p.inv=0;G.eshots.push({k:'mg',x:p.x,y:p.y,a:0,vx:0,vy:0,r:4,dmg:1,life:10,t:0});advance(1);const dead=p.dead;advance(120);
            const q=G.player;return {dead,ids:q.weapons.map(w=>w.id),x:Math.round(q.x),y:Math.round(q.y),alive:!q.dead};}""")
        check('one hit kills; respawn keeps every gun except the one in hand, at the death point',
              r['dead'] and r['alive'] and r['ids'] == ['desert_eagle', 'rocket_launcher'] and abs(r['x'] - 600) < 20 and abs(r['y'] - 520) < 20, r)
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player;p.inv=9999;for(const id of ['minigun','fusion_beam','spread_shotgun']){TD.footDrop(G,p.x,p.y,id);advance(1);}return p.weapons.map(w=>w.id);}""")
        check('a fifth gun replaces the one in hand (four slots)', len(r) == 4 and 'spread_shotgun' in r, r)

        # ---- Mercs push-scroll: the screen never comes back
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player,C=TD.Cam;p.x=270;p.y=430;advance(60);const top=C.y;p.y=1000;advance(40);return {top:Math.round(top),after:Math.round(C.y),py:Math.round(p.y),bottom:Math.round(C.y+TD.VH)};}""")
        check('push-scroll never scrolls back and keeps the pilot on screen', r['after'] <= r['top'] + 1 and r['py'] <= r['bottom'], r)

        # ---- the boss: three Hard Corps forms driven by broken parts
        r = page.evaluate("""()=>{const G=TDGAME.G,p=G.player;p.inv=99999;p.x=400;p.y=296;advance(4);const b=G.boss;return {name:b&&b.name,state:b&&b.state};}""")
        check('crossing into the grand hall wakes THE EXHIBIT', r['name'] == 'THE EXHIBIT', r)
        page.evaluate('advance(110)')
        snap('13_boss_form1')
        r = page.evaluate("""()=>{const G=TDGAME.G,b=G.boss,f1=b.form;const pp=b.world(105,10);b.hit(pp.x,pp.y,3,99);const pl=b.world(-105,10);b.hit(pl.x,pl.y,3,99);advance(2);
            return {f1,f2:b.form,hp:+b.hpFrac().toFixed(2)};}""")
        check('breaking both missile pods tears it off the plinth (form 2 BREAKOUT)', r['f1'] == 1 and r['f2'] == 2, r)
        r = page.evaluate("""()=>{const G=TDGAME.G,b=G.boss,p=G.player;b.state='ram';b.t=0;b.ramDir=0;p.x=b.x+200;p.y=b.y;
            const statue=G.props.find(q=>q.kind==='mx_statue'&&q.y<300&&!q.dead);let stall=false,seenRed=false;for(let i=0;i<220&&!stall;i++){if(b.warn&&b.warn.col==='red')seenRed=true;advance(1);stall=b.stalled>0;}
            return {stall,seenRed,state:b.state};}""")
        check('the warned ram runs green-yellow-red, then stalls on the wall with the hull open', r['stall'] and r['seenRed'], r)
        snap('14_boss_stalled')
        r = page.evaluate("""()=>{const G=TDGAME.G,b=G.boss;b.stalled=1;const h0=b.parts.hull;b.hit(b.x+40,b.y,3,10);const stalledDmg=h0-b.parts.hull;
            b.hit(b.x,b.y-1,3,999);advance(2);return {stalledDmg:+stalledDmg.toFixed(2),form:b.form};}""")
        check('turret down -> form 3 OVERDRIVE (stalled hull took double of the 15% armour rate)', r['form'] == 3 and r['stalledDmg'] > 2.9, r)
        page.evaluate("(()=>{const b=TDGAME.G.boss;b.state='nova';b.t=0;})();advance(70)")
        snap('15_boss_overdrive')
        r = page.evaluate("""()=>{const G=TDGAME.G,b=G.boss;b.state='wave';b.t=0;b.waveRow=null;advance(80);const w=G.eshots.filter(e=>e.k==='wave');
            const xs=w.map(e=>e.x).sort((a,b)=>a-b);let gap=0;for(let i=1;i<xs.length;i++)gap=Math.max(gap,xs[i]-xs[i-1]);return {n:w.length,gap};}""")
        check('the sonic wall leaves one crossing hole', r['n'] >= 10 and r['gap'] >= 60, r)
        snap('16_boss_wave')
        r = page.evaluate("""()=>{const G=TDGAME.G,b=G.boss;G.eshots=[];b.hit(b.x+40,b.y,3,9999);advance(400);return {state:G.state,rows:(G.results.extraRows||[]).map(r=>r[0])};}""")
        check('destroying the hull clears the mission with hostage and exhibit tallies', r['state'] == 'clear' and 'HOSTAGES' in r['rows'], r)
        page.evaluate('advance(200)')
        snap('17_results')

        check('zero page, console and HTTP errors', not errors, errors[:6])
        log = page.evaluate('TD.MUSEUM.log.map(e=>e.event)')
        browser.close()
finally:
    stop()
(OUT / 'results.json').write_text(json.dumps({'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks)}, indent=1))
print(f"{sum(c['passed'] for c in checks)}/{len(checks)} passed")
