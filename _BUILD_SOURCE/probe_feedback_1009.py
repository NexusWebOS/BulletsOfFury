"""Native Chromium probe for Mike's October 9 feedback pass.

    python _BUILD_SOURCE/probe_feedback_1009.py [scenario ...]

Scenarios: map, stage1, s1boss, clear, s2boss, s4barrels, hud (default: all).
Each scenario drives the real index.html through the game's own functions, steps loop() by hand,
saves screenshots under _shots/feedback_1009/<scenario>/ and prints PASS/FAIL lines. Fixtures
(invulnerability, teleporting, forced phases) isolate one behaviour each; they are not balance runs.
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/feedback_1009'
checks = []


def check(name, value, detail=None):
    checks.append({'name': name, 'passed': bool(value), 'detail': detail})
    print(('PASS ' if value else 'FAIL ') + name + ('' if detail is None else '  ' + json.dumps(detail)[:600]), flush=True)


def open_game(pw):
    b = pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required', '--mute-audio'])
    pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
    pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
    errs = []
    pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:300]))
    pg.on('console', lambda m: errs.append('console: ' + m.text[:300]) if m.type == 'error' else None)
    pg.goto(f'http://127.0.0.1:{PORT}/index.html', wait_until='load', timeout=90000)
    pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)
    return b, pg, errs


def step(pg, n):
    r = pg.evaluate(sh.STEP, n)
    if r:
        print('step error:', r)
    return r


def snap(pg, scen, name):
    d = OUT / scen
    d.mkdir(parents=True, exist_ok=True)
    pg.locator('#screen').screenshot(path=str(d / (name + '.png')))


def wait_art(pg, keys, timeout=60000):
    pg.evaluate('(k)=>k.forEach(x=>XART.rdy(x))', keys)
    for _ in range(timeout // 250):
        if pg.evaluate('(k)=>k.every(x=>XART.rdy(x))', keys):
            return True
        pg.wait_for_timeout(250)
    return False


# ------------------------------------------------------------------ campaign map
def scen_map(pg):
    pg.evaluate("""()=>{run.mode='campaign';run.pilot='cole';campBeginFresh();openStageSelect(1,{boot:true});}""")
    pg.wait_for_timeout(2500)
    trace = []
    for _ in range(600):
        if pg.evaluate('!!sselShip'):
            break
        step(pg, 1)
    for i in range(0, 900, 30):
        if i:
            step(pg, 30)
        if i % 120 == 0:
            pg.wait_for_timeout(200)
        t = pg.evaluate("""()=>({boot:sselBoot,z:+cmap2.cam.z.toFixed(3),cx:Math.round(cmap2.cam.x),cy:Math.round(cmap2.cam.y),
          ship:sselShip?{x:Math.round(sselShip.x),y:Math.round(sselShip.y)}:null,hq:cmap2World('hq'),f1:sselFlagXY(1)})""")
        trace.append(t)
        if i in (300, 420, 540, 660, 870):
            snap(pg, 'map', 'boot_%03d' % i)
    first = next((t for t in trace if t['ship']), None)
    check('jet appears at Fury HQ on a fresh campaign', first and abs(first['ship']['x'] - first['hq']['x']) < 120 and abs(first['ship']['y'] - first['hq']['y']) < 160, first)
    last = trace[-1]
    check('camera ends zoomed in on Stage 1 with the jet beside the flag',
          last['z'] > .5 and last['ship'] and abs(last['ship']['x'] - last['f1']['x']) < 10 and abs(last['cx'] - last['f1']['x']) < 200, last)
    on = pg.evaluate("""()=>{const s=cmap2ToScreen(sselShip.x,sselShip.y),f=cmap2ToScreen(sselFlagXY(1).x,sselFlagXY(1).y);
      return {s,f,vw:campaignViewWidth(),top:CM2_BAND_TOP,bot:CM2_BAND_BOT};}""")
    check('jet and Stage 1 flag both on screen', all(0 < p['y'] < on['bot'] + 20 and -campaign_pad(on) < p['x'] < on['vw'] for p in (on['s'], on['f'])), on)
    # ---- clear Stage 1: unlock cinematic, jet flies to Stage 2 with the camera following
    pg.evaluate("""()=>{campaign.rank[1]='A';openStageSelect(2,{unlock:2});}""")
    trace = []
    for i in range(0, 420, 15):
        step(pg, 15)
        t = pg.evaluate("""()=>({z:+cmap2.cam.z.toFixed(3),cx:Math.round(cmap2.cam.x),cy:Math.round(cmap2.cam.y),cine:sselUnlockCine?sselUnlockCine.phase:null,
          ship:sselShip?{x:Math.round(sselShip.x),y:Math.round(sselShip.y)}:null,f2:sselFlagXY(2),cur:sselCursor,max:campaign.unlockedMax})""")
        trace.append(t)
        if i in (30, 90, 150, 210, 300, 405):
            snap(pg, 'map', 'unlock_%03d' % i)
    check('camera stays zoomed in throughout the post-clear flight', min(t['z'] for t in trace[4:]) > .45, [t['z'] for t in trace])
    ding = next((t for t in trace if t['cine'] in ('ding', 'unfurl')), None)
    check('jet reaches Stage 2 before the flag unfurls', ding and abs(ding['ship']['x'] - ding['f2']['x']) < 14, ding)
    check('Stage 2 unlocked and selected after the cinematic', trace[-1]['cur'] == 2 and trace[-1]['max'] >= 2 and trace[-1]['cine'] is None, trace[-1])


def campaign_pad(on):
    return (on['vw'] - 480) / 2 + 2


# ------------------------------------------------------------------ Stage 1 miniboss
RZB_FIGHT = r"""(frames)=>{window.__bofStepNow=performance.now();window.__sd=[];window.__made=0;window.__charge=[];
  const trap=(q)=>{ if(!q||!q._rzb||q.__t)return; q.__t=1; window.__made++; let dead=false;
    Object.defineProperty(q,'dead',{get(){return dead},set(v){if(v&&!dead){const s=new Error().stack;
      if(!/razorbackClear/.test(s)&&q.y>-10&&q.y<VH+10&&q.x>-10&&q.x<worldWidth()+10)window.__sd.push(q.kind);}dead=v;},configurable:true}); };
  const base=XART.get;
  enemies.length=0; spawnSubBoss('razorback');
  for(let i=0;i<frames;i++){player.invuln=1e9;Input.keys['j']=true; if(subBoss&&subBoss.hp<subBoss.maxhp*0.6)subBoss.hp=subBoss.maxhp;
    player.x=(subBoss?subBoss.x:240)+Math.sin(i/40)*50; player.y=VH-90;
    window.__bofStepNow+=1000/60;loop(window.__bofStepNow);for(const q of eBullets)trap(q);}
  Input.keys['j']=false;
  return {made:window.__made,shotDown:window.__sd,att:subBoss&&subBoss._rzb&&subBoss._rzb.attack,furious:!!(subBoss&&subBoss._rzb&&subBoss._rzb.furious)}}"""


def scen_s1boss(pg):
    for diff in ('normal', 'furious'):
        pg.evaluate("d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d);}", diff)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole', 'invuln': True})
        r = pg.evaluate(RZB_FIGHT, 2400)
        check('%s: no Razorback round is shot down by player fire' % diff, r['made'] > 30 and not r['shotDown'], r)
        if diff == 'furious':
            check('furious Razorback is in its furious set', r['furious'], r)
            # hold a sonic charge and look at the plate the charge actually drew
            got = pg.evaluate("""()=>{const B=subBoss,R=B._rzb;R.attack='sonic';R.at=0.6;R.charge=0.7;R.state=R.state==='arrival'?'guns':R.state;
              const seen=[];const d=ctx.drawImage;ctx.drawImage=function(im){if(im&&im.src&&/sonic_charge/.test(im.src))seen.push(im.src.split('/').pop());return d.apply(this,arguments);};
              try{razorbackDraw(B);}finally{ctx.drawImage=d;}return seen;}""")
            check('furious sonic charge draws the authored red plate', got and all('rzbf_' in k for k in got), got)
            pg.evaluate(sh.STEP, 1)
            snap(pg, 's1boss', 'furious_fight')


# ------------------------------------------------------------------ Stage 1 jets
def scen_stage1(pg):
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole', 'invuln': True})
    wait_art(pg, ['furyjet_0_bank_0', 'furyjet_1_bank_0', 'fx_ground_target_reticle'])
    edges = pg.evaluate("()=>{window.__bofStepNow=performance.now();enemies.length=0;eBullets.length=0;player.x=worldWidth()/2;fb9SwoopPair();"
                "window.__sw=enemies.filter(e=>e._fb9Swoop);window.__swLog=[];"
                "return {L:camLeftX(),R:camRightX(),start:__sw.map(e=>({side:e._fb9Swoop.side,x:Math.round(e.x)}))}}")
    for i in range(16):
        step(pg, 10)
        pg.evaluate("()=>{for(const e of __sw)__swLog.push({side:e._fb9Swoop.side,ph:e._fb9Swoop.phase,head:+e._fb9Swoop.head.toFixed(2),x:Math.round(e.x),y:Math.round(e.y),dead:!!e.dead});}")
        if i in (3, 6, 8, 10, 13):
            snap(pg, 'stage1', 'swoop_%03d' % (i * 10))
    for _ in range(12):
        step(pg, 20)
        pg.evaluate("()=>{player.invuln=1e9;for(const e of __sw)__swLog.push({side:e._fb9Swoop.side,ph:e._fb9Swoop.phase,head:+e._fb9Swoop.head.toFixed(2),x:Math.round(e.x),y:Math.round(e.y),dead:!!e.dead});}")
    log = pg.evaluate("__swLog")
    sides = {d['side'] for d in log}
    check('swoop pair: one jet from each side', sides == {-1, 1}, sorted(sides))
    st = {d['side']: d['x'] for d in edges['start']}
    check('swoop jets enter from off the side edges', st[-1] < edges['L'] and st[1] > edges['R'], edges)
    check('one of the pair loops a somersault', any(d['ph'] == 'loop' for d in log), None)
    exits = [d for d in log if d['ph'] == 'exit']
    check('both jets finish heading south and leave off the bottom',
          {d['side'] for d in exits} == {-1, 1} and all(abs(d['head'] - 1.57) < .02 for d in exits) and all(d['dead'] for d in log[-2:]), log[-2:])
    shots = pg.evaluate("__swShots=eBullets.length")
    # ---- bomber: no guns, a stick of bomb reticles along its lane
    pg.evaluate("()=>{enemies.length=0;eBullets.length=0;groundTargetingReset();const e=spawnEnemy('s1jetbomber',worldWidth()/2,-40,{route:'straight'});window.__bm=e;window.__bmLog=[];"
                "window.__bmShots=0;if(!window.__bmHook){window.__bmHook=1;const f=eShootT;eShootT=function(){if(S1M.actor===window.__bm)window.__bmShots++;return f.apply(this,arguments);};}}")
    for i in range(14):
        step(pg, 15)
        pg.evaluate("()=>{player.invuln=1e9;__bmLog.push({x:Math.round(__bm.x),y:Math.round(__bm.y),bombs:groundTargetingFx.filter(q=>q._fb9Bomb).length,shots:__bmShots});}")
        if i in (6, 9):
            snap(pg, 'stage1', 'bomber_%03d' % (i * 15))
    bl = pg.evaluate("__bmLog")
    check('bomber lays a stick of bomb reticles', max(b['bombs'] for b in bl) >= 2, bl[-4:])
    check('bomber fires no guns or missiles', all(b['shots'] == 0 for b in bl), bl[-1])
    check('bomber holds a straight lane', max(b['x'] for b in bl) - min(b['x'] for b in bl) < 30, [b['x'] for b in bl])
    # ---- the evasive roll reel no longer plays on Stage 1
    r = pg.evaluate("""()=>{enemies.length=0;const e=spawnEnemy('s1jetdelta',worldWidth()/2,120,{route:'straight'});e.y=140;
      let rolled=0;for(let i=0;i<40;i++){pBullets.push({x:e.x+10,y:e.y+120,vx:0,vy:-6,kind:'missile',w:6,h:12,t:0,dmg:0});
       window.__bofStepNow+=1000/60;loop(window.__bofStepNow);if(e._furyMove&&e._furyMove.kind==='roll')rolled++;}
      return {rolled,evades:e._furyEvades||0}}""")
    check('stage 1 jet evasion keeps the steady pose (no roll reel)', r['rolled'] == 0, r)


# ------------------------------------------------------------------ Stage 2 miniboss
def scen_s2boss(pg):
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole', 'invuln': True})
    pg.evaluate("()=>{window.__bofStepNow=performance.now();enemies.length=0;spawnSubBoss('magmaward');}")
    step(pg, 240)
    wait_art(pg, ['av3_reaver_parts'])
    SHOOT = """([n,inf,spread,part])=>{const B=subBoss,p=av3Part(B,part||'core');let hits=0,dealt=0,crits=0;
      for(let i=0;i<n;i++){const P=av3PartPoint(B,p),before=B.hp,f0=floaters.length;const x=P.x+(spread?(Math.random()*2-1)*spread:0);
        pBullets.push({x,y:P.y+60,vx:0,vy:-9,w:4,h:10,kind:'spread',dmg:2,lv:1,t:0,seat:1,_inf:inf||undefined});
        for(let k=0;k<9;k++){player.invuln=1e9;window.__bofStepNow+=1000/60;loop(window.__bofStepNow);
          if(floaters.slice(f0).some(f=>f.elementCrit))crits++;}
        if(B.hp<before){hits++;dealt+=before-B.hp;}}
      return {hits,dealt:+dealt.toFixed(1),per:+(dealt/Math.max(1,hits)).toFixed(2),crits,flash:B._hitFlashColor}}"""
    neu = pg.evaluate(SHOOT, [12, None, 0, 'core'])
    ice = pg.evaluate(SHOOT, [12, 'ice', 0, 'core'])
    check('cold rounds crit the Inferno Reaver (+50%, crit text)', ice['per'] >= neu['per'] * 1.45 and ice['crits'] > 0, {'neutral': neu, 'ice': ice})
    drawn = pg.evaluate("""()=>{const B=subBoss;B._hitFlashColor='#83d9ff';for(const p of B._av3Reaver.parts)p.flash=.16;
      const seen=[];const d=ctx.drawImage;ctx.drawImage=function(im){if(im&&im.width&&[...AV3.cells.entries()].some(([k,v])=>v===im&&/^fb9-part-#83d9ff/.test(k)))seen.push(1);return d.apply(this,arguments);};
      try{shipBossDraw(B);}finally{ctx.drawImage=d;}return seen.length}""")
    check('a cold hit flashes every live module blue', drawn >= 5, drawn)
    pg.evaluate("()=>{const B=subBoss;for(const p of B._av3Reaver.parts)p.flash=0;}")
    # break every module with real rounds
    for part in ('gunL', 'gunR', 'wingL', 'wingR', 'nose'):
        for _ in range(30):
            if pg.evaluate("p=>av3Part(subBoss,p).dead", part):
                break
            pg.evaluate("""p=>{const B=subBoss,q=av3Part(B,p);const P=av3PartPoint(B,q);av3ReaverHit(B,25,P.x,P.y,p);}""", part)
            step(pg, 2)
    st = pg.evaluate("()=>({body:!!subBoss._fb9Body,frac:+(subBoss.hp/subBoss.maxhp).toFixed(3),alive:subBoss._av3Reaver.parts.filter(p=>!p.dead).map(p=>p.id)})")
    check('breaking the last module exposes the core at <= 28% HP', st['body'] and st['frac'] <= .281 and st['alive'] == ['core'], st)
    spread = pg.evaluate(SHOOT, [30, None, 28, 'core'])
    check('spread fire across the bare core lands reliably', spread['hits'] >= 24, spread)
    pg.evaluate("()=>{subBoss.hp=subBoss.maxhp*.28;window.__modes=[];window.__s2shots=0;const f=fb9BodyShot;fb9BodyShot=function(){__s2shots++;return f.apply(this,arguments);};}")
    for i in range(48):
        step(pg, 15)
        m = pg.evaluate("()=>{const B=subBoss._fb9Body;subBoss.hp=Math.max(subBoss.hp,subBoss.maxhp*.2);__modes.push(B.mode);return B.mode}")
        if m in ('charge', 'leap', 'spray') and not pg.evaluate("window['__snap_'+%r]" % m):
            pg.evaluate("window['__snap_'+%r]=1" % m)
            snap(pg, 's2boss', 'body_' + m)
    modes = set(pg.evaluate("__modes"))
    check('bare core spins, charges and flings itself', {'spray', 'charge', 'leap'} <= modes, sorted(modes))
    check('bare core fires its own fire spray and slam ring', pg.evaluate("__s2shots") > 20, pg.evaluate("__s2shots"))


# ------------------------------------------------------------------ stage clear hover
def scen_clear(pg):
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole', 'invuln': True})
    step(pg, 30)
    pg.evaluate("()=>{enemies.length=0;bossDefeated=true;stageEnding=99;}")
    step(pg, 2)
    st = pg.evaluate("()=>state")
    check('stage clear hands over to the fly-off', st == 'flyover', st)
    r = pg.evaluate("""()=>{const x0=player.x,y0=player.y;Input.keys['d']=true;Input.keys['arrowright']=true;Input.keys['w']=true;
      for(let i=0;i<60;i++){window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}
      const r={dx:player.x-x0,dy:player.y-y0,t:flyoverT,state};Input.keys['d']=false;Input.keys['arrowright']=false;Input.keys['w']=false;return r;}""")
    check('the pilot cannot steer during the clear hover', abs(r['dx']) < .01 and abs(r['dy']) < .01 and r['t'] < 1.35, r)
    snap(pg, 'clear', 'hover')


# ------------------------------------------------------------------ HUD layout
def scen_hud(pg):
    pg.set_viewport_size({'width': 1280, 'height': 900})
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole', 'invuln': True})
    pg.evaluate("()=>{window.__bofStepNow=performance.now();enemies.length=0;spawnSubBoss('razorback');window.__bofFit&&window.__bofFit();}")
    step(pg, 200)
    pg.wait_for_timeout(600)
    step(pg, 2)
    box = pg.evaluate("""()=>{const r=id=>{const e=document.getElementById(id),b=e.getBoundingClientRect();return {top:b.top,bottom:b.bottom,h:b.height,vis:getComputedStyle(e).visibility,disp:getComputedStyle(e).display}};
      const px=(id,y)=>{const c=document.getElementById(id),g=c.getContext('2d');const d=g.getImageData(0,Math.floor(y*c.height),c.width,1).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i]>0)n++;return n;};
      return {top:r('hud-row'),screen:r('screen-area'),bottom:r('hud-bottom'),hint:r('hint'),inner:innerHeight,
        topInk:px('hud-top',.6),botInk:px('hud-bot',.5)}}""")
    check('score strip sits above the playfield', box['top']['bottom'] <= box['screen']['top'] + 4 and box['top']['h'] > 20, box['top'])
    check('five-panel HUD sits below the playfield', box['bottom']['top'] >= box['screen']['bottom'] - 1 and box['bottom']['h'] > 50, box['bottom'])
    check('both HUD rows are drawn', box['topInk'] > 50 and box['botInk'] > 200, {'top': box['topInk'], 'bottom': box['botInk']})
    check('control hints do not cover the HUD', box['hint']['top'] >= box['bottom']['bottom'] - 1 or box['hint']['vis'] != 'visible', {'hint': box['hint'], 'hud': box['bottom']})
    bar = pg.evaluate("""()=>{let y=null;const d=drawHealthBarV2;drawHealthBarV2=function(kind,frac,cx,cy){if(kind==='mini'||kind==='boss')y=cy;return d.apply(this,arguments);};
      try{window.__bofStepNow+=1000/60;loop(window.__bofStepNow);}finally{drawHealthBarV2=d;}return y}""")
    check('miniboss bar draws at the top of the playfield, under the score strip', bar is not None and bar < 60, bar)
    pg.screenshot(path=str(OUT / 'hud_layout.png'))


# ------------------------------------------------------------------ Stage 4 barrels
def scen_s4barrels(pg):
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 4, 'pilot': 'cole', 'invuln': True})
    r = pg.evaluate("""()=>{window.__bofStepNow=performance.now();enemies.length=0;
      const a=spawnEnemy('s4barrel',worldWidth()*.38,120,{}),b=spawnEnemy('s4barrel',worldWidth()*.62,200,{});
      if(a){a.y=120;a.t=0;}if(b){b.y=200;b.t=0;}
      // a tank shoved against each barrel, and long enough for the 9s catch-all push
      for(const e of [a,b])if(e){const t=spawnEnemy('s4minitank',e.x+4,e.y+6,{});if(t){t.y=e.y+6;}}
      let worst=0,frames=0,bad=0,firstBad=null;const src0=levelSrcY();const P=[a,b].filter(Boolean).map(e=>({e,x:null,my:null}));
      for(let i=0;i<720;i++){player.invuln=1e9;window.__bofStepNow+=1000/60;loop(window.__bofStepNow);
        const src=levelSrcY();for(const q of P){if(!q.e.dead)drawEnemy(q.e);if(q.e.dead)continue;if(q.x==null){q.x=q.e.x;q.my=q.e.y+src;continue;}
          const d=Math.max(Math.abs(q.e.x-q.x),Math.abs((q.e.y+src)-q.my));q.x=q.e.x;q.my=q.e.y+src;   // frame-to-frame: a pinned barrel never changes map spot
          worst=Math.max(worst,d);if(d>.05&&i>1){bad++;if(!firstBad)firstBad={i,d:+d.toFixed(3),y:Math.round(q.e.y),dead:!!q.e.dead,dy:q.e._dyingT};}frames++;}}
      return {worst:+worst.toFixed(3),frames,bad,firstBad,alive:P.filter(q=>!q.e.dead).length}}""")
    check('Stage 4 barrels stay on their placed map spot (12s, shoved by tanks)', r['frames'] > 300 and r['bad'] == 0, r)


SCEN = {'map': scen_map, 's1boss': scen_s1boss, 'stage1': scen_stage1, 's2boss': scen_s2boss,
        'clear': scen_clear, 'hud': scen_hud, 's4barrels': scen_s4barrels}

if __name__ == '__main__':
    names = sys.argv[1:] or list(SCEN)
    PORT, stop = sh.serve(str(ROOT))
    try:
        with sync_playwright() as pw:
            for n in names:
                print('==', n, flush=True)
                b, pg, errs = open_game(pw)
                try:
                    SCEN[n](pg)
                except Exception as e:
                    check(n + ' scenario ran', False, str(e)[:500])
                check(n + ' raised no page/console errors', not errs, errs[:6])
                b.close()
    finally:
        stop()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ('results_' + '_'.join(names) + '.json')).write_text(json.dumps(checks, indent=1))
    print('%d/%d checks passed' % (sum(c['passed'] for c in checks), len(checks)))
