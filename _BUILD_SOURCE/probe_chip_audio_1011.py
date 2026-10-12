"""BOF chip pass: real decoded media, owning gameplay events, and lifecycle QA."""
from pathlib import Path
import hashlib
import json
import sys
import time
from playwright.sync_api import sync_playwright
import shoot

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'_shots/chip_bof_1011'
OUT.mkdir(parents=True, exist_ok=True)
BANK = ROOT/'assets/game/shared/audio/chip_1011'
manifest = json.loads((BANK/'manifest.json').read_text())
checks, errors, observations = [], [], {}


def check(name, ok, data=None):
    checks.append(dict(name=name, passed=bool(ok), data=data))
    print(('PASS ' if ok else 'FAIL ')+name, flush=True)


def step(p, seconds):
    for _ in range(round(seconds*10)):
        p.evaluate('()=>{for(let i=0;i<6;i++)updatePlay(1/60)}')
        p.wait_for_timeout(10)


def capture(p, name):
    p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUDStrip(hudctx);if(typeof fb9HudSplit==="function")fb9HudSplit();}')
    p.screenshot(path=str(OUT/(name+'.png')))


check('81 approved MP3s preserve source hashes', len(manifest['cues']) == 81 and all(hashlib.sha256((BANK/d['file']).read_bytes()).hexdigest() == d['sourceMp3Sha256'] for d in manifest['cues'].values()))
check('All score and ground cues included; 43 unapproved cues and genre studies excluded', sum(k.startswith('gd_') for k in manifest['cues']) == 18 and sum(k.startswith('scoreBullet') for k in manifest['cues']) == 4 and len(manifest['excludedKeys']) == 43 and not manifest['approval']['genreBanksIncluded'])
od = json.loads((ROOT/'expansion/topdown/audio/chip_1011/manifest.json').read_text())
check('BOF and Overdrive use the same approved source recordings', set(od['cues']) == set(manifest['cues']) and all(v['sourceMp3Sha256'] == od['cues'][k]['sourceMp3Sha256'] for k, v in manifest['cues'].items()))

port, stop = shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        p = br.new_page(viewport=dict(width=1180, height=1000))
        p.set_default_timeout(120000)
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('console', lambda m: errors.append(m.text[:650]) if m.type == 'error' or 'draw error' in m.text else None)
        p.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        p.goto(f'http://127.0.0.1:{port}/?soundpass=1011')
        p.wait_for_function('window.__bofFrames>4 && window.BOF_CHIP_PASS')
        p.evaluate(shoot.TRAP_RAF)
        p.keyboard.press('Enter')
        p.evaluate('()=>{Audio.resume();Snd.stopMusic();BOF_CHIP_PASS.stopAll();window.CQ={};CQ.stop=()=>{for(const k of Object.keys(BOF_CHIP_AUDIO.cues))Snd.stopCue(k);Snd._last={};};}')
        check('Main game boots with bounded lazy chip pools', p.evaluate('Object.keys(BOF_CHIP_AUDIO.cues).every(k=>Snd.pools[k]?.list.length===3)&&Snd._sfxVoices.length<=64'))
        media = []
        keys = list(manifest['cues'])
        for i in range(0, len(keys), 8):
            p.evaluate('ks=>{CQ.stop();CQ.keys=ks;for(const k of ks)Audio.SFX[k]();}', keys[i:i+8])
            p.wait_for_function('CQ.keys.every(k=>Snd.pools[k].slots.some(v=>v?.attached&&v.el.readyState>=3&&v.el.currentTime>0))', timeout=20000)
            media += p.evaluate('CQ.keys.map(k=>{const a=Snd.pools[k].slots.find(v=>v?.attached&&v.el.currentTime>0).el;return {key:k,src:a.currentSrc,time:a.currentTime,duration:a.duration,volume:a.volume,native:!a._bofNode};})')
        observations['media'] = media
        check('All 81 cues decode and advance through the actual BOF mixer', len(media) == 81 and all(x['time'] > 0 and x['duration'] > 0 and x['volume'] > 0 and '/chip_1011/' in x['src'] for x in media))
        check('Approved chip recordings bypass old tone filters', all(x['native'] for x in media))
        q = p.evaluate('()=>{CQ.stop();BOF_CHIP_PASS.stats={};Audio.SFX.laserShot();Audio.SFX.enemyPulseLaserBlue();Audio.SFX.enemyPulseLaserRed();return {n:BOF_CHIP_PASS.stats.enemyLaser,pools:Snd.pools.laserShot===Snd.pools.enemyPulseLaserBlue};}')
        check('Enemy laser aliases share one pool and one retrigger gate', q['n'] == 1 and q['pools'], q)
        q=p.evaluate('()=>{CQ.stop();BOF_CHIP_PASS.stats={};for(const k of ["furnaceLaserBurst","hammerEradBlast","quadFire","enemyHeavyLaser"])r30Sound(k);return BOF_CHIP_PASS.stats;}')
        check('Realm boss releases retain their four approved named recordings',all(q.get(k)==1 for k in ['furnaceLaserBurst','hammerEradBlast','quadFire','enemyHeavyLaser']),q)
        q=p.evaluate('()=>{CQ.stop();BOF_CHIP_PASS.stats={};zoneCols=[];zoneColumnSpawn(0,"lightning",false);const early=BOF_CHIP_PASS.stats.geyserLightning||0;zoneTick(.31);return {early,erupted:BOF_CHIP_PASS.stats.geyserLightning};}')
        check('Lightning geyser audio begins on eruption, after its warning',q.get('early')==0 and q.get('erupted')==1,q)
        q=p.evaluate('()=>{CQ.stop();BOF_CHIP_PASS.stats={};Audio.SFX.shieldBreakCombat();Audio.SFX.shieldBreak();return BOF_CHIP_PASS.stats.shieldBreak;}')
        check('Combat and Rebel shield breaks share the approved break cue and gate',q==1,q)
        check('Unapproved enemy missiles, normal explosions, music and UI blips keep their files', p.evaluate('["enemyMissile","expSmall","expBig","machineGun","blip","powerup"].every(k=>!String(BOFA.sfx[k]).includes("chip_1011"))'))
        q = p.evaluate('()=>{CQ.stop();Snd.setVol("master",.5);Snd.setVol("sfx",.4);Audio.SFX.missile();return {volume:Snd.pools.missile.slots.find(v=>v?.attached&&!v.el.paused)?.el.volume,want:Snd.TAME.missile.g*.2};}')
        check('Chip sounds obey master and SFX levels', q.get('volume') is not None and abs(q['volume']-q['want']) < .0001, q)
        p.evaluate('Snd.setVol("master",1);Snd.setVol("sfx",.4);CQ.stop()')
        # Selected event routes, rather than calling only the newly added handles.
        q = p.evaluate('()=>{BOF_CHIP_PASS.stats={};for(const v of [100,250,500,1000])bonusPickupApply({kind:"scorechip",val:v});timeBombArm();bombTick(.1);timeBombBlow();return BOF_CHIP_PASS.stats;}')
        check('Score pickups select their four denominations and timed bombs get beep/blast cues', all(q.get(k, 0) > 0 for k in ['scoreBullet100','scoreBullet250','scoreBullet500','scoreBullet1000','timedBombBeep','timedBombBlast']), q)
        p.evaluate('()=>{CQ.stop();BOF_CHIP_PASS.stats={};forgingStart({w:0,elem:"lightning",lv:1});forging.t=1;drawForging(1/60);}')
        p.wait_for_function('BOF_CHIP_PASS.owned.get("forge")?.el.currentTime>0', timeout=12000)
        p.evaluate('()=>{window.forgeVoice=BOF_CHIP_PASS.owned.get("forge").el;for(let i=0;i<20;i++)drawForging(1/60)}')
        p.evaluate(shoot.STEP, 1)
        p.screenshot(path=str(OUT/'forge-welding.png'))
        check('Welding owns one continuously playing loop', p.evaluate('BOF_CHIP_PASS.stats.forgeWeld===1&&forgeVoice.loop&&!forgeVoice.paused'))
        p.evaluate('forging.t=FORGE_WELD_T0+FORGE_WELD_T;drawForging(.01)')
        check('Product reveal stops the weld and plays one completion cue', p.evaluate('forgeVoice.paused&&!BOF_CHIP_PASS.owned.has("forge")&&BOF_CHIP_PASS.stats.forgeComplete===1'))
        p.evaluate('()=>{loadoutStart(()=>setState(GS.TITLE));loadoutScr.t=1;Input.clearTaps();BOF_CHIP_PASS.stats={};CQ.stop();}')
        p.keyboard.press('ArrowRight');p.evaluate('drawLoadout(1/60);Input.clearTaps()')
        check('Loadout navigation dispatches the approved selection cue', p.evaluate('(BOF_CHIP_PASS.stats.loadoutSelect||0)>0'))
        p.keyboard.press('Enter');p.evaluate('drawLoadout(1/60);Input.clearTaps()')
        check('Loadout launch dispatches its own cue', p.evaluate('BOF_CHIP_PASS.stats.loadoutLaunch===1'))
        p.evaluate('()=>{CQ.stop();BOF_CHIP_PASS.stats={};unlocksStart([["TEST WEAPON","micon_mg_1","#ffffff","weapon"]]);}')
        check('Weapons Gained dispatches weaponFound', p.evaluate('BOF_CHIP_PASS.stats.weaponFound===1'))
        # Production Stage 2 weather. Clear only incidental fixtures; the actual
        # controller owns birth, travel, drawing and retirement of the wave.
        p.evaluate(shoot.SETUP, dict(state='PLAY', stage=2, pilot='cole', invuln=True))
        p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(2).ready}')
        p.wait_for_function('Array.from({length:8},(_,i)=>XART.rdy("nwf_fire_"+i)).every(Boolean)')
        p.evaluate('''()=>{BOFCinematicDirector.cancel();story=null;boss=subBoss=null;bossActive=subBossActive=false;warnKind=null;warnT=0;
         bombFx=timeBomb=null;bombFlash=flashScreen=0;player.dead=false;player.invuln=40002;player.x=worldWidth()/2;camX=player.x-VW/2;player.y=VH*.8;
         wfxReset();wfx.fseq={ph:'waves',t:0,shown:1,fired:0,lanes:[worldWidth()/2],dir:[0],wave:null};wfxUpdate(1/60);window.wave=wfx.fseq.wave;window.waveVoice=BOF_CHIP_PASS.owned.get(wave);CQ.stop();}''')
        p.wait_for_function('waveVoice?.el.readyState>=3&&waveVoice.el.currentTime>0', timeout=12000)
        q = p.evaluate('({rate:waveVoice.el.playbackRate,pitch:waveVoice.el.preservesPitch,span:waveVoice.seconds,volume:waveVoice.el.volume,duration:waveVoice.el.duration})')
        check('Firewall has a pitch-preserved sample stretched to the controller travel time', q['pitch'] and .5 <= q['rate'] <= 2 and abs(q['duration']/q['rate']-q['span']) < .1, q)
        p.evaluate('wfxUpdate(.55)')
        p.evaluate(shoot.STEP, 1)
        p.screenshot(path=str(OUT/'firewall-in-flight.png'))
        check('The live wave retains the same sustained voice during travel', p.evaluate('BOF_CHIP_PASS.owned.get(wave)===waveVoice&&!waveVoice.el.paused'))
        p.evaluate('Snd.setVol("master",.25);BOF_CHIP_PASS.tick()')
        check('Firewall responds to volume changes while travelling', p.evaluate('Math.abs(waveVoice.el.volume-Snd.TAME.firewallLaunch.g*.4*.25)<.0001'))
        p.evaluate('Snd.setVol("master",1);setState("paused")')
        check('Pause releases the firewall voice', p.evaluate('waveVoice.el.paused&&BOF_CHIP_PASS.owned.size===0'))
        p.evaluate('setState(GS.PLAY);wfxUpdate(0);window.resumedVoice=BOF_CHIP_PASS.owned.get(wave)')
        p.wait_for_function('resumedVoice?.el.currentTime>0&&!resumedVoice.el.paused', timeout=12000)
        check('Resume follows the remaining wave instead of starting another full attack', p.evaluate('resumedVoice.offset>.5&&wfx.fseq.wave===wave'))
        p.evaluate('wfxUpdate(1.5)')
        check('Wave departure stops its audio immediately', p.evaluate('!BOF_CHIP_PASS.owned.has(wave)&&resumedVoice.el.paused'))
        # Each actual password fight is exercised, rather than a mock tank actor.
        for code, unit in [('SONIC','sonic'), ('ORDOS','deviator'), ('HARK','devastator')]:
            p.evaluate('code=>{CQ.stop();BOF_CHIP_PASS.stopAll();BOFCinematicDirector.cancel();story=null;setState(GS.PASSWORD);pwInput=code;submitPassword();pilotIndex=PILOTS.findIndex(p=>p.key==="yuri");startRun(PENDING_STAGE);player.invuln=9999;player.dead=false;}', code)
            p.wait_for_function('subBoss?._sg10&&sg10Ready(subBoss)')
            step(p, 4)
            p.wait_for_function('BOF_CHIP_PASS.owned.get("tank-engine")?.el.currentTime>0', timeout=12000)
            check(code+' actual tank has a quiet, decoded engine bed', p.evaluate('unit=>subBoss._sg10.unit===unit&&!BOF_CHIP_PASS.owned.get("tank-engine").el.paused&&BOF_CHIP_PASS.owned.get("tank-engine").el.volume<=.05', unit))
            capture(p, code.lower()+'-audio')
            p.evaluate('()=>{CQ.stop();BOF_CHIP_PASS.stats={};subBoss._stageSound={};sg10StartAttack(subBoss);sg10Release(subBoss,subBoss._sg10.attack,0);CQ.shot=eBullets.at(-1);}')
            if unit != 'sonic':
                key = 'missileLaunch' if unit == 'deviator' else 'gd_tankCannon'
                check(code+' weapon release uses '+key, p.evaluate('(k)=>(BOF_CHIP_PASS.stats[k]||0)>0', key))
                p.evaluate('CQ.stop();subBoss._stageSound={};sg10Detonate(CQ.shot)')
                key = 'missileHit' if unit == 'deviator' else 'gd_shellImpact'
                check(code+' detonation uses '+key, p.evaluate('(k)=>(BOF_CHIP_PASS.stats[k]||0)>0', key))
            else:
                check('Sonic retains its sonic pressure release', p.evaluate('!BOF_CHIP_PASS.stats.gd_tankCannon&&!BOF_CHIP_PASS.stats.missileLaunch'))
            p.evaluate('()=>{window.motor=BOF_CHIP_PASS.owned.get("tank-engine").el;player.dead=true;BOF_CHIP_PASS.tick();}')
            check(code+' player death stops the tank bed', p.evaluate('motor.paused&&BOF_CHIP_PASS.owned.size===0'))
        p.evaluate('()=>{player.dead=false;setState(GS.PLAY);BOF_CHIP_PASS.tick();dispatchEvent(new Event("blur"));}')
        check('Focus loss clears every sustained chip voice', p.evaluate('BOF_CHIP_PASS.suspended&&BOF_CHIP_PASS.owned.size===0'))
        p.evaluate('dispatchEvent(new Event("focus"));setState(GS.TITLE)')
        check('Audio decoder budget remains bounded after every audition and encounter', p.evaluate('Snd._sfxVoices.length<=64&&BOF_CHIP_PASS.cache.size<=8'))
        observations['runtimeFailures'] = p.evaluate('BOF_CHIP_PASS.failures')
        check('No chip decode or playback errors', not observations['runtimeFailures'], observations['runtimeFailures'])
        # The portable game still plays approved media without fetch/file CORS.
        local = br.new_page()
        local.on('pageerror', lambda e: errors.append('file: '+str(e)))
        local.goto((ROOT/'index.html').as_uri())
        local.wait_for_function('window.BOF_CHIP_PASS&&window.__bofFrames>2')
        local.evaluate(shoot.TRAP_RAF)
        local.keyboard.press('Enter');local.evaluate('Audio.SFX.enemyLaser()')
        local.wait_for_function('Snd.pools.enemyLaser.slots.some(v=>v?.el.currentTime>0&&v.el.readyState>=3)', timeout=15000)
        check('Portable file:// BOF actually plays the approved MP3', local.evaluate('Snd.pools.enemyLaser.slots.some(v=>v?.el.currentSrc.startsWith("file:"))'))
        review=br.new_page(viewport=dict(width=1180,height=940))
        review.on('pageerror',lambda e:errors.append('review: '+str(e)))
        review.on('console',lambda m:errors.append('review: '+m.text) if m.type=='error' else None)
        review.on('response',lambda r:errors.append(f'review HTTP {r.status} {r.url}') if r.status>=400 else None)
        review.goto(f'http://127.0.0.1:{port}/docs/previews/chip_audio_1011/')
        check('Audition page lists every approved cue',review.locator('.cue').count()==81)
        review.locator('#filter').fill('forge')
        check('Audition search retains only matching cues',review.locator('.cue').count()==6)
        review.locator('#filter').fill('')
        review.locator('[data-play="gd_tankEngineLoop"]').click()
        review.wait_for_function('audio.currentTime>0&&!audio.paused')
        check('Audition engine button plays the actual looping chip MP3',review.evaluate('audio.loop&&audio.currentSrc.endsWith("chip_gd_tankEngineLoop.mp3")'))
        review.locator('#stop').click()
        check('Audition Stop releases the loop',review.evaluate('audio.paused'))
        review.locator('#wave').click()
        review.wait_for_function('audio.currentTime>0&&!audio.paused')
        check('Audition firewall uses the duration variant with pitch preservation',review.evaluate('!audio.loop&&audio.preservesPitch&&Math.abs(audio.duration/audio.playbackRate-1.28)<.1'))
        review.screenshot(path=str(OUT/'review-desktop.png'))
        review.locator('#stop').click()
        review.set_viewport_size(dict(width=390,height=844))
        check('Audition page fits a phone viewport without horizontal scrolling',review.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        review.screenshot(path=str(OUT/'review-mobile.png'))
        br.close()
except Exception as e:
    errors.append(str(e))
    print('PROBE ERROR '+str(e), flush=True)
finally:
    stop()
    check('No page, console or asset errors', not errors, errors)
    report = dict(passed=sum(c['passed'] for c in checks), failed=sum(not c['passed'] for c in checks), checks=checks, errors=errors, observations=observations,
                  scope='Real media playback and protected production encounter fixtures. Not a human mix review or campaign clear.')
    (OUT/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'FINAL {report["passed"]} passed, {report["failed"]} failed; {len(errors)} browser errors', flush=True)
sys.exit(1 if report['failed'] or errors else 0)
