"""Native Stage-4 simultaneous pressure, faster aircraft and active helper regression.

Runs the real game/update/render owners; controlled fixtures are not a campaign clear.
"""
from pathlib import Path
import ast
import hashlib
import http.server
import json
import os
import sys
import traceback

from playwright.sync_api import sync_playwright

import shoot

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/stage4_pressure_1015'
OUT.mkdir(parents=True, exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size = 128
SETUP = next(ast.literal_eval(n.value) for n in ast.parse(
    (ROOT / '_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body
    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SETUP' for t in n.targets))
checks, errors, scenes, audits = [], [], [], []


def check(name, ok, data=None):
    checks.append(dict(name=name, passed=bool(ok), data=data))
    print(('PASS ' if ok else 'FAIL ') + name + ((' ' + json.dumps(data)) if not ok else ''), flush=True)


INSTALL = r"""()=>{
 window.qa4={time:0,shots:[],warnings:0,muzzles:0,coreMuzzles:{'-1':0,'1':0},poses:0,
  early:0,entries:{},positions:{},frames:{},turns:{},fireMotion:{},clockStalls:0,concurrentClock:0};
 if(window.qa4Installed)return;window.qa4Installed=true;
 const draw=ctx.drawImage,air=air13Blit,warn=combatWarningDraw,muzzle=wm26Draw,director=d27MuzzleDraw;
 window.qa4DrawCount=0;ctx.drawImage=function(){qa4DrawCount++;return draw.apply(this,arguments)};
 air13Blit=function(){const before=qa4DrawCount,r=air.apply(this,arguments);if(qa4DrawCount>before)qa4.poses++;return r;};
 combatWarningDraw=function(owner){const before=qa4DrawCount,r=warn.apply(this,arguments);
  if(qa4DrawCount>before&&(owner?._sa14Escort||owner?._sa14Core||owner===window.B))qa4.warnings++;return r;};
 wm26Draw=function(g,fam,x,y){const before=qa4DrawCount,r=muzzle.apply(this,arguments);if(qa4DrawCount>before){qa4.muzzles++;
  for(const d of window.B?._s4war?.coreTurrets||[])if(!d.dead&&Math.hypot(x-d.x,y-d.y)<95)qa4.coreMuzzles[d.side]++;}return r;};
 d27MuzzleDraw=function(g,fam,x,y){const before=qa4DrawCount,r=director.apply(this,arguments);if(qa4DrawCount>before){qa4.muzzles++;
  for(const d of window.B?._s4war?.coreTurrets||[])if(!d.dead&&Math.hypot(x-d.x,y-d.y)<95)qa4.coreMuzzles[d.side]++;}return r;};
 window.qa4Step=function(n){for(let j=0;j<n;j++){
  const old=new Set(eBullets),mode=B?._er26?.mode,t=B?._er26?.t,turn=B?._sa14?.escortTurn;
  updatePlay(1/60);qa4.time+=1/60;
  if(turn&&mode===B?._er26?.mode){qa4.concurrentClock++;if(B._er26.t<=t)qa4.clockStalls++;}
  for(const e of enemies.filter(e=>e._sa14Escort&&!e.dead&&e._dyingT==null)){
   const a=e._sa14Escort,id=a.serial;qa4.frames[id]??=[];
   if(e._air13Frame!=null&&!qa4.frames[id].includes(e._air13Frame))qa4.frames[id].push(e._air13Frame);
   if(a.t>0&&a.phase!=='arrive'&&!e._noHit&&qa4.entries[id]==null)qa4.entries[id]=a.t;
   if(a.aim&&qa4.turns[id]==null&&Math.abs(stage4AngleDelta(a.angle,a.fireAngle))<.15)qa4.turns[id]=a.t-a.fireAt;
  }
  for(const q of eBullets)if(!old.has(q)){
   const owner=q._sa14EscortOwner,a=owner?._sa14Escort;
   if(q._sa14Slug||q._sa14Missile||q._sa14EscortShot||q._sa14CoreShot){
    const type=q._sa14EscortShot?'escort':q._sa14CoreShot?'core':q._sa14Slug?'warden':'missile';
    qa4.shots.push({time:qa4.time,type,side:q._s4CoreSide,serial:a?.serial,x:q.x,y:q.y,vx:q.vx,vy:q.vy,
     moving:!!(Math.abs(q.vx)+Math.abs(q.vy)>0),ownerX:owner?.x,ownerY:owner?.y,ownerAge:a?.t,hidden:!!owner?._noHit,
     hull:{x:B.x,y:B.y,w:B.w,h:B.h}});
    if(a){if(owner._noHit)qa4.early++;const id=a.serial,prior=qa4.positions[id];
     if(prior)qa4.fireMotion[id]=Math.max(qa4.fireMotion[id]||0,Math.hypot(owner.x-prior.x,owner.y-prior.y));
     else qa4.positions[id]={x:owner.x,y:owner.y};}
   }
  }
  if(j%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}
 }};
}"""

PIXELS = r"""()=>{
 const e=enemies.find(e=>e._sa14Escort&&!e.dead&&!e._noHit&&e._dyingT==null&&['warn','fire'].includes(e._sa14Escort.phase));if(!e)return{missing:true};
 function image(fn){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);fn();ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
 function delta(a,b){let n=0;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])n++;return n;}
 B.flash=e.flash=0;for(const part of B._mr27.parts)part.flash=0;
 const before=image(()=>mr27Draw(B));hitSubBoss(1,B.x,B.y);const hull=delta(before,image(()=>mr27Draw(B))),hullTimer=B.flash;
 const part=mr27Part(B,'gunL'),shape=mr27Shape(B,'gunL');B.flash=part.flash=0;
 const moduleBefore=image(()=>mr27Draw(B));hitSubBoss(1,shape.x,shape.y);const module=delta(moduleBefore,image(()=>mr27Draw(B)));
 const planeBefore=image(()=>drawEnemy(e)),hp=e.hp;hitEnemy(e,1);const plane=delta(planeBefore,image(()=>drawEnemy(e)));
 window.qa4HitPlane=e;return{hull,module,plane,hullTimer,partTimer:part.flash,planeTimer:e.flash,hpLost:hp-e.hp};
}"""

port, stop = shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel=os.environ.get('BOF_BROWSER', 'msedge'),
                                    args=['--autoplay-policy=no-user-gesture-required'])
        page = browser.new_page(viewport=dict(width=1440, height=1000))
        page.set_default_timeout(120000)
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text[:700]) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(str(r.status) + ' ' + r.url) if r.status >= 400 else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', timeout=120000)
        page.wait_for_function('window.__bofFrames>4&&typeof sa14CoreTick==="function"')
        page.evaluate(shoot.TRAP_RAF)
        page.mouse.click(60, 60)
        page.evaluate('Audio.resume()')

        def setup(kind='olivewarden', difficulty='normal'):
            page.evaluate(SETUP, dict(stage=4, kind=kind, mini=kind == 'olivewarden', pilot='cole', diff=difficulty))
            page.wait_for_function('()=>{stageLoadTick();wm26Warm();return stageLoadReady(4)&&XART.rdy("mr27_"+B._mr27.skin)&&!!air13Pose("flight_variant_4","heading",0)&&bmfReady("game")}')
            page.evaluate('''()=>{B._er26.engaged=false;B._phaseInvuln=0;er26Tick(B,0);story=fb2Talk=null;BOFCinematicDirector.cancel();
             SA14.events=[];VP12.next=CP12.next=EP13.next=9999;stagePlan=[];player.invuln=1e9;run.shield=0;run.speed=0;Input.keys={};}''')
            page.evaluate(INSTALL)

        def frames(n):
            for start in range(0, n, 30):
                page.evaluate('n=>qa4Step(n)', min(30, n-start))
                page.wait_for_timeout(4)

        def snap(name):
            page.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit();}')
            page.screenshot(path=str(OUT / (name + '.png')))
            scenes.append(name)

        for difficulty in ['easy', 'normal', 'hard', 'furious']:
            setup(difficulty=difficulty)
            captured = False
            for second in range(30):
                frames(60)
                if not captured and page.evaluate('eBullets.some(q=>q._sa14EscortShot)&&eBullets.some(q=>q._sa14Slug||q._sa14Missile)'):
                    snap('warden-' + difficulty + '-concurrent-fire')
                    captured = True
            audit = page.evaluate('qa4')
            audits.append(dict(encounter='warden', difficulty=difficulty, audit=audit))
            shots = audit['shots']
            plane = [q for q in shots if q['type'] == 'escort']
            heavy = [q for q in shots if q['type'] in ['warden', 'missile']]
            bins = {int(q['time']*2) for q in plane} & {int(q['time']*2) for q in heavy}
            check(difficulty + ' miniboss and jets fire in shared half-second windows', len(bins) >= 1, dict(overlapping_windows=len(bins), miniboss=len(heavy), escorts=len(plane)))
            check(difficulty + ' miniboss clock advances throughout helper waves', audit['concurrentClock'] > 30 and audit['clockStalls'] == 0, dict(observed=audit['concurrentClock'], stalls=audit['clockStalls']))
            check(difficulty + ' aircraft arrive on combat plane within 1.4 seconds', bool(audit['entries']) and max(audit['entries'].values()) <= 1.4, audit['entries'])
            check(difficulty + ' aircraft turn into firing heading within half a second', bool(audit['turns']) and max(audit['turns'].values()) <= .5, audit['turns'])
            check(difficulty + ' aircraft fire while travelling through the field', bool(audit['fireMotion']) and min(audit['fireMotion'].values()) > 4, audit['fireMotion'])
            check(difficulty + ' depth entry remains harmless and all projectiles move', audit['early'] == 0 and bool(plane) and all(q['moving'] for q in plane), dict(early=audit['early'], shots=len(plane)))
            check(difficulty + ' real authored aircraft headings animate visibly', audit['poses'] > 0 and any(len(fs) >= 4 for fs in audit['frames'].values()), dict(draws=audit['poses'], headings=audit['frames']))
            check(difficulty + ' warnings and muzzle reels reach native drawImage', audit['warnings'] > 0 and audit['muzzles'] > 0, dict(warnings=audit['warnings'], muzzles=audit['muzzles']))

        setup()
        page.evaluate('()=>{B._sa14.escortCd=0;}')
        for _ in range(60):
            frames(10)
            if page.evaluate('enemies.some(e=>e._sa14Escort&&!e.dead&&!e._noHit&&e._dyingT==null&&["warn","fire"].includes(e._sa14Escort.phase))'):
                break
        pixel = page.evaluate(PIXELS)
        check('native damage flashes Warden hull, gun module and aircraft pixels', not pixel.get('missing') and min(pixel.get('hull', 0), pixel.get('module', 0), pixel.get('plane', 0)) > 10 and pixel.get('hpLost', 0) > 0, pixel)
        snap('warden-native-hit-feedback')
        frames(18)
        check('damage flash timers expire through normal update', page.evaluate('B.flash<=0&&B._mr27.parts.every(q=>q.flash<=0)&&qa4HitPlane.flash<=0'))
        page.evaluate('()=>{window.qa4Killed=qa4HitPlane;hitEnemy(qa4Killed,1e6);qa4.shots=[];}')
        frames(90)
        check('destroyed aircraft cannot keep firing', page.evaluate('!qa4.shots.some(q=>q.serial===qa4Killed._sa14Escort.serial)&&!!(qa4Killed.dead||qa4Killed._dyingT!=null)'))

        # Shield nodes share translation/scale with the hull, never its rotation.
        setup('stormsovereign')
        registration = page.evaluate('''()=>{const angles=[0,Math.PI/2,Math.PI],rows=[];const blit=mr27Blit;
         try{for(const a of angles){B._sa14.angle=a;B._sa14.scale=1.25;B.x=worldWidth()/2+18;B.y=180;B._drawY=180;stage4ShieldSyncNodes(B);
          const draws=[];mr27Blit=function(skin,cell,p){const before=qa4DrawCount,r=blit.apply(this,arguments);
           if(skin==='storm'&&cell===5&&arguments[5]===B)draws.push({x:p.x,y:p.y,rot:p.rot||0,w:p.w,pixels:qa4DrawCount>before});return r;};
          ctx.setTransform(SS,0,0,SS,0,0);ctx.translate(-camX,0);mr27Over(B);mr27Blit=blit;
          rows.push({angle:a,nodes:B._s4war.shield.nodes.map(n=>({x:n.x-B.x,y:n.y-B.y})),draws});}
         }finally{mr27Blit=blit;}return rows;}''')
        check('generator offsets stay fixed during 90/180-degree hull turns', all(q['nodes'] == registration[0]['nodes'] for q in registration[1:]), registration)
        check('all four generator plates render upright through hull turns', all(len(q['draws']) == 4 and all(d['pixels'] and d['rot'] == 0 for d in q['draws']) for q in registration), registration)
        page.evaluate('()=>{B._sa14.scale=1;stage4ShieldSyncNodes(B);}')
        snap('sovereign-upright-cores-turned-hull')

        for difficulty in ['normal', 'hard', 'furious']:
            setup('stormsovereign', difficulty)
            page.evaluate('()=>{stage4CoreTurretSpawnMissing(B,.7);B._sa14.lockCd=999;}')
            captured = False
            for _ in range(30):
                frames(60)
                if difficulty == 'normal' and not captured and page.evaluate('B._s4war.coreTurrets.some(d=>d._sa14Core?.phase==="fire")&&_navalFlashes.some(f=>/s4w_muzzle_lightning/.test(f.fam))&&eBullets.some(q=>q._sa14CoreShot)'):
                    snap('sovereign-helpers-live-fire')
                    captured = True
            audit = page.evaluate('qa4')
            audits.append(dict(encounter='sovereign', difficulty=difficulty, audit=audit))
            shots = [q for q in audit['shots'] if q['type'] == 'core']
            left, right = [q for q in shots if q['side'] == -1], [q for q in shots if q['side'] == 1]
            check(difficulty + ' both Sovereign helpers release moving projectiles', bool(left) and bool(right) and all(q['moving'] for q in shots), dict(left=len(left), right=len(right)))
            check(difficulty + ' both helpers show real muzzle artwork', min(audit['coreMuzzles'].values()) > 0, audit['coreMuzzles'])

        setup('stormsovereign')
        page.evaluate('()=>{stage4CoreTurretSpawnMissing(B,.7);B._sa14.lockCd=999;er26Set(B,"sa14-storm");}')
        frames(90)
        snap('sovereign-helper-lane-warnings')
        check('Sovereign helper warning artwork reaches native renderer', page.evaluate('qa4.warnings>0'))

        # Drive the helper owner directly to isolate depth/offscreen gating from hull movement.
        depth = page.evaluate('''()=>{const d=B._s4war.coreTurrets[0];B._sa14.depth=true;let old=new Set(eBullets);
         for(let i=0;i<120;i++)sa14CoreTick(B,1/60);const hidden=eBullets.filter(q=>!old.has(q)&&q._sa14CoreShot).length;
         B._sa14.depth=false;old=new Set(eBullets);sa14CoreTick(B,1/60);
         return{hidden,first:eBullets.filter(q=>!old.has(q)&&q._sa14CoreShot).length,phase:d._sa14Core.phase,t:d._sa14Core.t};}''')
        check('depth return begins a fresh helper tell before shooting', depth['hidden'] == 0 and depth['first'] == 0 and depth['phase'] in ['ready', 'warn', 'windup'], depth)
        offscreen = page.evaluate('''()=>{const x=B.x;B.x=worldWidth()+1000;B._drawY=B.y;stage4ShieldSyncNodes(B);let old=new Set(eBullets);
         for(let i=0;i<120;i++)sa14CoreTick(B,1/60);const hidden=eBullets.filter(q=>!old.has(q)&&q._sa14CoreShot).length;
         B.x=x;stage4ShieldSyncNodes(B);old=new Set(eBullets);sa14CoreTick(B,1/60);
         return{hidden,first:eBullets.filter(q=>!old.has(q)&&q._sa14CoreShot).length,phases:B._s4war.coreTurrets.map(d=>d._sa14Core.phase)};}''')
        check('offscreen helpers produce no hidden shots and re-enter with a tell', offscreen['hidden'] == 0 and offscreen['first'] == 0 and all(q in ['ready', 'warn', 'windup'] for q in offscreen['phases']), offscreen)
        gun = page.evaluate('''()=>{const d=B._s4war.coreTurrets[0],g=mr27HelperState(d),p=mr27HelperGun(B,d);
         d.shield=0;_lastHitX=p.x;_lastHitY=p.y;stage4CoreTurretDamage(B,d,g.hp+1);const old=new Set(eBullets);
         for(let i=0;i<420;i++)sa14CoreTick(B,1/60);
         return{dead:g.dead,left:eBullets.filter(q=>!old.has(q)&&q._sa14CoreShot&&q._s4CoreSide===d.side).length,
          other:eBullets.filter(q=>!old.has(q)&&q._sa14CoreShot&&q._s4CoreSide!==d.side).length};}''')
        check('destroying a helper gun stops its own fire while the other fights', gun['dead'] and gun['left'] == 0 and gun['other'] > 0, gun)
        snap('sovereign-destroyed-helper-gun')

        core_hit = page.evaluate('''()=>{const d=B._s4war.coreTurrets.find(d=>!mr27HelperState(d).dead);d.shield=0;d.flash=0;
         function image(){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);mr27HelperDraw(B,d);ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
         const before=image(),hp=d.hp,g=mr27HelperState(d),gun=mr27HelperGun(B,d);_lastHitX=gun.x;_lastHitY=gun.y;stage4CoreTurretDamage(B,d,1);
         const after=image();let pixels=0;for(let i=0;i<before.length;i+=4)if(before[i]!==after[i]||before[i+1]!==after[i+1]||before[i+2]!==after[i+2])pixels++;
         const result={pixels,hpLost:hp-d.hp,flash:d.flash,gunFlash:g.flash};for(let i=0;i<20;i++)sa14CoreTick(B,1/60);result.expired=d.flash<=0;
         stage4CoreTurretDamage(B,d,1e6);const old=new Set(eBullets);for(let i=0;i<120;i++)sa14CoreTick(B,1/60);
         result.dead=d.dead;result.deadShots=eBullets.filter(q=>!old.has(q)&&q._sa14CoreShot&&q._s4CoreSide===d.side).length;return result;}''')
        check('Sovereign helper hull and gun damage produces visible native flash', core_hit['pixels'] > 20 and core_hit['hpLost'] > 0 and core_hit['flash'] > 0 and core_hit['gunFlash'] > 0, core_hit)
        check('helper hit flash expires and destroyed helper releases no further shots', core_hit['expired'] and core_hit['dead'] and core_hit['deadShots'] == 0, core_hit)

        # Observe a decoded, advancing voice triggered by the actual helper controller.
        setup('stormsovereign')
        page.evaluate('()=>{stage4CoreTurretSpawnMissing(B,.7);Snd.prepare(["enemyMachineGunHeavy"]);Audio.resume();}')
        page.wait_for_function('()=>Snd.pools.enemyMachineGunHeavy?.slots.some(v=>v?.attached&&v.el.readyState>=3)')
        audio = page.evaluate('''async()=>{const key='enemyMachineGunHeavy';await Snd._audioCtx().resume();Snd.stopCue(key);Snd._last[key]=0;
         for(let i=0;i<240;i++){sa14CoreTick(B,1/60);if(Snd.pools[key].slots.some(v=>v?.attached&&!v.el.paused))break;}
         await new Promise(r=>setTimeout(r,25));const voice=Snd.pools[key].slots.find(v=>v?.attached&&!v.el.paused),a=voice?.el;if(!a)return{playing:false};
         const ctx=Snd._audioCtx(),meter=ctx.createAnalyser();meter.fftSize=256;let capture=null;
         if(a._bofNode)a._bofNode.connect(meter);else{capture=ctx.createMediaStreamSource((a.captureStream||a.mozCaptureStream).call(a));capture.connect(meter);}
         const samples=new Float32Array(256);let peak=0;for(let i=0;i<24;i++){await new Promise(r=>setTimeout(r,12));meter.getFloatTimeDomainData(samples);for(const v of samples)peak=Math.max(peak,Math.abs(v));}
         if(a._bofNode)a._bofNode.disconnect(meter);if(capture)capture.disconnect();return{playing:a.currentTime>0,peak,volume:a.volume,muted:a.muted};}''')
        check('Sovereign helper fire plays decoded nonzero enemy audio', audio.get('playing') and audio.get('peak', 0) > 0 and audio.get('volume', 0) > 0, audio)
        browser.close()
except Exception as exc:
    errors.append(str(exc))
    print(traceback.format_exc(), flush=True)
finally:
    stop()
    report = dict(passed=sum(c['passed'] for c in checks), failed=sum(not c['passed'] for c in checks),
                  checks=checks, errors=errors, scenes=scenes,
                  runtime_sha256=hashlib.sha256((ROOT / 'assets/stage34_assault_1014.js').read_bytes()).hexdigest(),
                  scope='Native controlled fixtures: 30-second overlapping-combat observations, native artwork and damaged pixels, real audio. Not a full human campaign clear.')
    (OUT / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (OUT / 'combat-audits.json').write_text(json.dumps(audits, indent=2), encoding='utf-8')
    (ROOT / 'docs/qa/stage4_pressure_1015.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(dict(passed=report['passed'], failed=report['failed'], errors=errors)), flush=True)

if errors or report['failed']:
    sys.exit(1)
