"""Chromium: actual decoded/playing media plus owner/event/lifecycle coverage.

Protected combat fixtures exercise native gameplay and canvas rendering. This is
not a human mix approval or an unassisted campaign difficulty measurement.
"""
from pathlib import Path
import hashlib
import json
import sys
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
from shoot import serve
OUT = ROOT / '_shots/chip_audio_1011'
OUT.mkdir(parents=True, exist_ok=True)
checks, errors, observations = [], [], {}
BANK = ROOT / 'expansion/topdown/audio/chip_1011'
manifest = json.loads((BANK / 'manifest.json').read_text())


def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)


check('81 approved shipping MP3s match their source hashes', len(manifest['cues']) == 81 and all(hashlib.sha256((BANK / d['file']).read_bytes()).hexdigest() == d['sourceMp3Sha256'] for d in manifest['cues'].values()))
check('43 unapproved sounds and all genre banks remain excluded', len(manifest['excludedKeys']) == 43 and not manifest['approval']['genreBanksIncluded'] and 'enemyMachineGun' not in manifest['cues'])
check('all four score cues and every ground cue are imported', all(k in manifest['cues'] for k in ['scoreBullet100','scoreBullet250','scoreBullet500','scoreBullet1000']) and sum(k.startswith('gd_') for k in manifest['cues']) == 18)
port, stop = serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1100, 'height': 850})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?pass=chip1011')
        page.wait_for_function('window.TDGAME && TDGAME.G.state === "boot"', timeout=60000)
        check('boot waits for a real input before unlocking sound', page.evaluate('!TD.Audio.on && !TD.Audio.play("gd_tankCannon")'))
        page.evaluate("TDGAME.freeze();window.press=(k,v)=>dispatchEvent(new KeyboardEvent(v?'keydown':'keyup',{key:k}));window.tap=k=>{press(k,true);TDGAME.step();press(k,false);TDGAME.step();};")
        page.keyboard.press('ArrowRight')
        # Yield between native input batches: audio retrigger gates use wall
        # time and menu/ship assets finish decoding asynchronously.
        # Explicitly skip the spoken intro. A sample's real-time completion is
        # independent of the fixture's accelerated simulation clock.
        for command in ["TDGAME.step(15);tap('enter')", "TDGAME.step(15);tap('enter')", "TDGAME.step(30);tap('enter')", "TDGAME.step(30);tap('enter')", "TDGAME.step(30);tap('arrowright')", "TDGAME.step(15);tap('enter')", "TDGAME.step(65);tap('enter')"]:
            page.evaluate(command)
            page.wait_for_timeout(100)
        observations['menuRoute'] = page.evaluate('({state:TDGAME.G.state,guard:TD.Frontend.guard,cues:TD.Audio.stats})')
        check('pilot/mission selection, equipment confirmation and launch use their chip cues', page.evaluate('TDGAME.G.state==="play" && ["loadoutSelect","loadoutEquip","loadoutLaunch"].every(k=>TD.Audio.stats[k]>0)'))
        # Every cue is played through the owning runtime, including dormant cues
        # as an audition. Short cues can finish before measurement; time > 0
        # still proves that they decoded and advanced rather than stayed silent.
        cue_keys = list(manifest['cues'])
        decoded = []
        for i in range(0, len(cue_keys), 8):
            keys = cue_keys[i:i+8]
            page.evaluate("""keys=>{TD.Audio.reset();window.audition=keys.map(k=>({k,a:TD.Audio.sounds[k].loop?TD.Audio.loop(k,'qa:'+k):TD.Audio.play(k)}));} """, keys)
            page.wait_for_function('audition.every(v=>v.a && v.a.readyState>=3 && v.a.currentTime>0)', timeout=15000)
            decoded.extend(page.evaluate('audition.map(v=>({key:v.k,src:v.a.currentSrc,duration:v.a.duration,time:v.a.currentTime,loop:v.a.loop,volume:v.a.volume}))'))
            page.wait_for_timeout(90)
        observations['media'] = decoded
        check('all 81 approved sounds decode and advance in real Chromium', len(decoded) == 81 and all(v['time'] > 0 and v['duration'] > 0 for v in decoded))
        check('registered loop flags and voice gains reach the actual media elements', all(v['loop'] == manifest['cues'][v['key']]['loop'] and abs(v['volume'] - manifest['cues'][v['key']]['gain'] * .8) < .0001 for v in decoded))

        fresh = """TDGAME.G.sel=0;TDGAME.start();const G=TDGAME.G,p=G.player;
          G.units=[];G.props=[];G.structures=[];TD.World.load(800,4000,[]);
          p.x=260;p.y=2200;p.inv=99999;p.a=p.aim=Math.PI;TD.Input.pointer.active=false;TD.Cam.follow(p.x,p.y,1);
          for(const k of ['d','w','e','j','k','h','r','shift','i','enter','f'])press(k,false);
          TDGAME.step(2);TD.Audio.stats={};TD.Audio.lastT={};"""
        page.evaluate('()=>{' + fresh + '}')
        page.wait_for_function('Array.from(TD.Audio.loops.values()).some(v=>v.key==="gd_tankEngineLoop" && v.audio.readyState>=3 && v.audio.currentTime>0)', timeout=10000)
        check('tank idle has one decoded engine loop and no tread/servo loop', page.evaluate('TD.Audio.loops.size===1 && Array.from(TD.Audio.loops.values())[0].key==="gd_tankEngineLoop"'))
        page.evaluate("press('d',true);press('shift',true);press('e',true);TDGAME.step(20)")
        page.wait_for_function('["gd_tankTreadLoop","gd_turretTraverse"].every(k=>Array.from(TD.Audio.loops.values()).some(v=>v.key===k&&v.audio.currentTime>0))')
        check('sideways movement and independent aim own separate playing tread/servo loops', page.evaluate('Math.abs(TDGAME.G.player.a-Math.PI)<.001 && ["gd_tankEngineLoop","gd_tankTreadLoop","gd_turretTraverse"].every(k=>Array.from(TD.Audio.loops.values()).filter(v=>v.key===k).length===1)'))
        page.evaluate("press('r',true);TDGAME.step(12)")
        check('boost release starts one chargeDash cue and speeds up the moving loops', page.evaluate('TD.Audio.stats.chargeDash===1 && Array.from(TD.Audio.loops.values()).filter(v=>v.key!=="gd_turretTraverse").every(v=>v.audio.playbackRate>1)'))
        page.evaluate('TDGAME.G.player.inv=0;TDGAME.render();TDGAME.G.player.inv=99999')
        page.locator('#screen').screenshot(path=str(OUT/'tank_boost.png'))
        page.evaluate("window.stoppedVoices=Array.from(TD.Audio.loops.values()).filter(v=>v.key!== 'gd_tankEngineLoop').map(v=>v.audio);for(const k of ['d','e','r','shift'])press(k,false);TDGAME.step(24)")
        check('release stops tread/servo voices while the engine returns to idle', page.evaluate('TD.Audio.loops.size===1 && stoppedVoices.every(a=>a.paused) && Array.from(TD.Audio.loops.values())[0].audio.playbackRate===1'))
        result = page.evaluate('()=>{' + fresh + """TD.World.load(800,4000,[[330,2050,334,2350,'b']]);p.x=310;press('d',true);TDGAME.step(35);return !Array.from(TD.Audio.loops.values()).some(v=>v.key==='gd_tankTreadLoop');}""")
        check('a tank pushing into solid cover does not keep a travelling tread loop', result)

        page.evaluate('()=>{' + fresh + "tap('k');}")
        page.wait_for_function('TD.Audio.pools.gd_tankCannon.some(a=>a.currentTime>0)')
        check('a real uncharged cannon release uses the tank cannon sample', page.evaluate('TD.Audio.stats.gd_tankCannon===1 && TDGAME.G.shots.some(s=>s.k==="shell"&&!s.big)'))
        page.evaluate('()=>{' + fresh + "press('h',true);TDGAME.step(45);press('h',false);TDGAME.step();}")
        check('charged armor-piercing release uses railCannon and retains physical recoil', page.evaluate('TD.Audio.stats.railCannon===1 && TDGAME.G.player.recoil>=9 && TDGAME.G.shots.some(s=>s.big)'))
        page.evaluate('()=>{' + fresh + "p.weapons=[{id:'homing',lv:1}];press('j',true);TDGAME.step();press('j',false);G.units=[TD.makeUnit('scout',p.x,p.y-130,{hp:99,max:99,mode:'alert',stunned:99})];TDGAME.step(28);}")
        check('actual homing launch and contact use distinct launch/impact samples', page.evaluate('TD.Audio.stats.missileLaunch===1 && TD.Audio.stats.missileHit>0'))
        page.evaluate('()=>{' + fresh + "const u=TD.makeUnit('scout',p.x+50,p.y);G.units=[u];TD.hitUnit(G,u,99,u.x,u.y);}")
        check('enemy destruction has its approved enemyDie cue', page.evaluate('TD.Audio.stats.enemyDie===1 && TDGAME.G.units[0].dead'))
        page.evaluate('()=>{' + fresh + "const wall=TD.makeStructure({kind:'barrier',x:p.x+90,y:p.y});const building=TD.makeStructure({kind:'relay',x:p.x-100,y:p.y-60});G.structures=[wall,building];TD.ramStructures(G,p.x+20,p.y,p.x+180,p.y,45);TD.hitStructure(G,building,99);const crate=TD.makeProp('crate',p.x,p.y-75,'repair');G.props=[crate];TD.hitProp(G,crate,99);TDGAME.step();}")
        check('rammed concrete, buildings and crates have distinct demolition cues', page.evaluate('["gd_wallBreak","gd_buildingCollapse","gd_crateBreak"].every(k=>TD.Audio.stats[k]===1) && TDGAME.G.structures.every(s=>s.dead)'))
        page.evaluate('TDGAME.G.player.inv=0;TDGAME.render();TDGAME.G.player.inv=99999')
        page.locator('#screen').screenshot(path=str(OUT/'concrete_demolition.png'))
        page.evaluate('()=>{' + fresh + "for(const kind of ['homing','smoke','life','score'])G.pickups.push({kind,x:p.x,y:p.y,t:0});TDGAME.step();}")
        check('weapon, ammunition, extra-life and score pickups use their individual cues', page.evaluate('["weaponFound","gd_ammoPickup","extraLife","scoreBullet1000"].every(k=>TD.Audio.stats[k]===1)'))
        page.evaluate('()=>{' + fresh + "const u=TD.makeUnit('camera',p.x,p.y-150,{look:0,aware:.999});G.units=[u];TDGAME.step(2);}")
        check('native detection starts spotted/alert cues and an owner-controlled base alarm', page.evaluate('TD.Stealth.phase==="ALERT" && TD.Audio.stats.gd_spotted===1 && TD.Audio.stats.alert===1 && TD.Audio.loops.has("alarm")'))
        page.evaluate('TDGAME.G.units=[];TD.Stealth.seen=false;TD.Stealth.timer=.001;TDGAME.step(2)')
        check('the alarm stops when detection changes from ALERT to EVASION', page.evaluate('TD.Stealth.phase==="EVASION" && !TD.Audio.loops.has("alarm")'))
        page.evaluate('()=>{' + fresh + "press('d',true);TDGAME.step(5);window.pauseVoices=Array.from(TD.Audio.loops.values()).map(v=>v.audio);tap('enter');}")
        check('Start/pause releases every effect loop immediately', page.evaluate('TDGAME.G.state==="pause" && TD.Audio.loops.size===0 && pauseVoices.every(a=>a.paused)'))
        page.wait_for_timeout(100)
        page.evaluate("TDGAME.step(14);tap('enter');TDGAME.step(2)")
        observations['resume'] = page.evaluate('({state:TDGAME.G.state,guard:TD.Frontend.guard,suspended:TD.Audio.suspended,keys:TD.Input.state,loops:Array.from(TD.Audio.loops.values()).map(v=>v.key)})')
        check('resuming restarts current movement loops without duplicate voices', page.evaluate('TDGAME.G.state==="play" && Array.from(TD.Audio.loops.values()).filter(v=>v.key==="gd_tankEngineLoop").length===1'))
        page.evaluate('()=>{' + fresh + "p.hp=1;p.inv=0;TD.hurtPlayer(G,2,p.x,p.y);TDGAME.step(16);}")
        check('fatal damage uses playerDeath and stops live vehicle loops', page.evaluate('TDGAME.G.player.dead && TD.Audio.stats.playerDeath===1 && TD.Audio.loops.size===0'))
        page.locator('#screen').screenshot(path=str(OUT/'death_spin.png'))
        page.evaluate('()=>{' + fresh + "dispatchEvent(new Event('blur'));}")
        check('losing focus suspends effects and releases all loops', page.evaluate('TD.Audio.suspended && TD.Audio.loops.size===0 && !TD.Audio.play("gd_tankCannon")'))
        page.evaluate("dispatchEvent(new Event('focus'));TDGAME.step()")
        check('focus restores the live engine without changing combat state', page.evaluate('!TD.Audio.suspended && TD.Audio.loops.size===1'))

        page.evaluate('()=>{' + fresh + "p.x=400;p.y=700;G.boss=TD.makeWarrior(G,400,500);G.boss.state='broadside';G.boss.volleyT=0;TDGAME.step(36);}")
        check('The Warrior bullet volleys use quadFire', page.evaluate('TD.Audio.stats.quadFire===1 && TDGAME.G.eshots.length>=6'))
        page.evaluate("TD.Audio.lastT={};TDGAME.G.boss.state='laser';TDGAME.G.boss.volleyT=0;TDGAME.G.boss.volley=0;TDGAME.G.boss.t=0;TDGAME.step(40)")
        check('The Warrior visor volley uses the approved heavy enemy laser', page.evaluate('TD.Audio.stats.enemyHeavyLaser===1 && TDGAME.G.eshots.some(s=>s.k==="laser")'))
        page.locator('#screen').screenshot(path=str(OUT/'warrior_sound_volley.png'))
        page.evaluate("TD.Audio.lastT={};TDGAME.G.boss.state='rack';TDGAME.G.boss.volleyT=0;TDGAME.G.boss.volley=0;TDGAME.G.boss.t=0;TDGAME.step(36)")
        check('The Warrior missile salvo uses missileLaunch', page.evaluate('TD.Audio.stats.missileLaunch>0 && TDGAME.G.eshots.some(s=>s.k==="missile")'))
        page.evaluate('TDGAME.G.boss.damage("helmet",999);TDGAME.G.boss.damage("hull",999);TDGAME.step(348)')
        check('boss destruction uses expBoss while the supplied Warrior music retains its owner', page.evaluate('TD.Audio.stats.expBoss===1 && TDGAME.G.boss.wrecked && TD.Audio.musicKey==="clear"'))
        page.evaluate('()=>{' + fresh.replace('G.sel=0', 'G.sel=2') + "p.y=450;G.boss=TD.makeMachinists(G,400,200);G.boss.state='fight';TD.Cam.follow(p.x,p.y,1);TDGAME.step();G.boss.damage('wren','hull',6);}")
        check('Wren Bastion has a static loop and a heavy shield-impact cue', page.evaluate('TD.Audio.loops.has("wren-shield") && TD.Audio.stats.shieldImpactHeavy===1'))
        page.evaluate("TDGAME.G.boss.damage('wren','special_module',99);TDGAME.step()")
        check('breaking the Bastion module plays shieldBreak and stops its own static', page.evaluate('TD.Audio.stats.shieldBreak===1 && !TD.Audio.loops.has("wren-shield")'))

        page.evaluate("TDGAME.G.sel=3;TDGAME.start();window.press('d',false);TDGAME.G.units=[];TDGAME.G.props=[];TD.World.load(800,2000,[]);TDGAME.G.player.inv=99999;TD.Audio.stats={};TD.Audio.lastT={};TDGAME.step(2);press('d',true);TDGAME.step(25)")
        check('Museum foot movement alternates actual footstep A/B cues without a tank engine', page.evaluate('TD.Audio.stats.gd_footstepA>0 && TD.Audio.stats.gd_footstepB>0 && TD.Audio.loops.size===0'))
        page.evaluate('TDGAME.G.player.inv=0;TDGAME.render();TDGAME.G.player.inv=99999')
        page.locator('#screen').screenshot(path=str(OUT/'museum_footsteps.png'))
        page.evaluate("press('d',false);tap('f');TD.Audio.lastT={};press('j',true);TDGAME.step();press('j',false)")
        check('infantry cover and rifle fire use their ground cues', page.evaluate('TD.Audio.stats.gd_coverEnter===1 && TD.Audio.stats.gd_soldierRifle>0'))
        page.evaluate("TDGAME.G.player.weapons[0].ammo=0;TD.Audio.lastT={};press('j',true);TDGAME.G.player.fireCd=0;TDGAME.step();press('j',false);tap('r');TDGAME.step(72)")
        check('empty magazine reports error and completed reload reports ammunition', page.evaluate('TD.Audio.stats.error===1 && TD.Audio.stats.gd_ammoPickup>0 && TDGAME.G.player.weapons[0].ammo>0'))

        page.evaluate('()=>{' + fresh + "window.waveOwner={x:p.x,y:p.y-80,r:30};window.waveVoice=TD.Audio.firewall(waveOwner,3.25);}")
        page.wait_for_function('waveVoice.audio.readyState>=3 && waveVoice.audio.currentTime>0')
        check('firewall hook uses a pitch-preserved stretched span at an audible media rate', page.evaluate('waveVoice.audio.preservesPitch && waveVoice.audio.playbackRate>=.5 && waveVoice.audio.playbackRate<=2 && Math.abs(waveVoice.audio.duration/waveVoice.audio.playbackRate-3.25)<.12'))
        page.evaluate('TD.Audio.master=.25;TD.Audio.scene(TDGAME.G,1/60)')
        check('firewall hook follows the current Master and SFX sliders', page.evaluate('Math.abs(waveVoice.audio.volume-TD.Audio.sounds.firewallLaunch.gain*TD.Audio.vol*.25)<.0001'))
        page.evaluate('TD.Audio.master=1;TD.Audio.scene(TDGAME.G,1/60)')
        started = time.monotonic()
        page.wait_for_function('waveVoice.audio.ended', timeout=6000)
        observations['firewallElapsedAfterFirstAdvance'] = time.monotonic() - started
        check('firewall duration finishes naturally and releases its owner', page.evaluate('waveVoice.audio.ended && !TD.Audio.waves.has(waveOwner)'))
        page.evaluate('window.waveVoice=TD.Audio.firewall(waveOwner,8)')
        page.wait_for_function('waveVoice.audio.currentTime>0')
        page.evaluate('waveOwner.y=TD.Cam.y-50;TD.Audio.scene(TDGAME.G,1/60)')
        check('firewall audio stops immediately when its bounds leave the screen', page.evaluate('waveVoice.audio.paused && !TD.Audio.waves.has(waveOwner)'))
        page.evaluate('waveOwner.y=TDGAME.G.player.y-80;waveOwner.dead=false;window.waveVoice=TD.Audio.firewall(waveOwner,8);waveOwner.dead=true;TD.Audio.scene(TDGAME.G,1/60)')
        check('firewall impact/death cancels a sustained voice', page.evaluate('waveVoice.audio.paused && !TD.Audio.waves.has(waveOwner)'))
        page.evaluate("waveOwner.dead=false;window.waveVoice=TD.Audio.firewall(waveOwner,8);tap('enter')")
        check('pausing also cancels the firewall owner voice', page.evaluate('waveVoice.audio.paused && TD.Audio.waves.size===0 && TDGAME.G.state==="pause"'))
        page.evaluate("TD.Audio.reset();window.voices=[];for(let i=0;i<100;i++){TD.Audio.lastT.impactMetal=-9;voices.push(TD.Audio.play('impactMetal'));}")
        check('rapid impacts reuse at most four voices instead of stacking new media elements', page.evaluate('TD.Audio.pools.impactMetal.length<=4 && Object.values(TD.Audio.pools).flat().filter(a=>!a.paused).length<=24'))
        observations['runtimeFailures'] = page.evaluate('TD.Audio.failures')
        check('sound runtime reports no missing-file, decode or playback errors', not observations['runtimeFailures'])

        local = browser.new_page()
        local.on('pageerror', lambda e: errors.append('file:// ' + str(e)))
        local.goto((ROOT / 'expansion/topdown/index.html').as_uri())
        local.wait_for_function('window.TDGAME && TDGAME.G.state === "boot"', timeout=60000)
        local.keyboard.press('Enter')
        local.evaluate('TDGAME.freeze();TD.Audio.play("gd_tankCannon")')
        local.wait_for_function('TD.Audio.pools.gd_tankCannon.some(a=>a.currentTime>0 && a.readyState>=3)', timeout=15000)
        check('the portable file:// expansion actually plays its chip MP3s', local.evaluate('TD.Audio.pools.gd_tankCannon[0].currentSrc.startsWith("file:") && !TD.Audio.failures.length'))
        local.close()
        check('native pages have zero page, console and asset errors', not errors)
        browser.close()
finally:
    stop()
    result = {'checks': checks, 'errors': errors, 'observations': observations,
              'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks),
              'scope': 'Native media playback and protected gameplay fixtures; firewall is a duration/owner hook, not an installed combat ability.'}
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(f"FINAL {result['passed']} passed, {result['failed']} failed; {len(errors)} browser errors", flush=True)
sys.exit(1 if result['failed'] or errors else 0)
