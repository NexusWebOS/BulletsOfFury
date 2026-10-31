from pathlib import Path
import sys,json,hashlib
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
from serve_bof_1013 import AssetServer
shoot.http.server.ThreadingHTTPServer=AssetServer
OUT=ROOT/'_shots/music23';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];evidence={}
def check(name,value):
    checks.append({'name':name,'passed':bool(value)})
    print(('PASS ' if value else 'FAIL ')+name,flush=True)

port,stop=shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        page=browser.new_page(viewport={'width':1280,'height':960})
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?fullscreen=0&build=overdrive1014-music23-r1',wait_until='domcontentloaded',timeout=90000)
        page.wait_for_function('window.TDGAME&&TD.game.state==="boot"',timeout=90000)
        ev=page.evaluate
        ev('TDGAME.freeze();TD.pilot="yuri";TD.difficulty="normal";TD.Audio.stopMusic();TD.Audio.vol=0;TD.Audio.engineVol=0;TD.Frontend.settings.sfx=0;TD.Frontend.settings.engine=0;')
        def frames(n):
            while n:
                k=min(40,n);ev(f'TDGAME.step({k})');page.wait_for_timeout(2);n-=k
        def ready():
            try:
                page.wait_for_function('TD.Audio.music&&!TD.Audio.music.paused&&TD.Audio.music.readyState>=3&&TD.Audio.music.currentTime>0',timeout=30000)
            except Exception:
                print('MEDIA_DIAGNOSTIC',ev('({key:TD.Audio.musicKey,src:TD.Audio.music?.currentSrc,state:TD.Audio.music?.readyState,time:TD.Audio.music?.currentTime,paused:TD.Audio.music?.paused,error:TD.Audio.music?.error?.code,failures:TD.Audio.failures})'),flush=True)
                print('BROWSER_ERRORS',errors,flush=True)
                raise
        def snapshot():
            return ev('''()=>{const a=TD.Audio;return {key:a.musicKey,volume:a.music?.volume,time:a.music?.currentTime,duration:a.music?.duration,loop:a.music?.loop,paused:a.music?.paused,voices:[...a.musicVoices].map(v=>({key:v.key,gain:v.gain,volume:v.audio.volume,paused:v.audio.paused})),failures:a.failures};}''')
        def shot(name):
            ev('TDGAME.render()');page.locator('#screen').screenshot(path=str(OUT/(name+'.png')))
        def rms():
            return ev('''async()=>{window.musicMeterCtx??=new AudioContext();await musicMeterCtx.resume();window.musicMeters??=new WeakMap();const music=TD.Audio.music;let meter=musicMeters.get(music);if(!meter){const source=musicMeterCtx.createMediaElementSource(music),analyser=musicMeterCtx.createAnalyser();source.connect(analyser);analyser.connect(musicMeterCtx.destination);analyser.fftSize=2048;meter=analyser;musicMeters.set(music,meter);}await new Promise(r=>setTimeout(r,120));const data=new Float32Array(meter.fftSize);meter.getFloatTimeDomainData(data);return Math.sqrt(data.reduce((sum,v)=>sum+v*v,0)/data.length);}''')

        ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===3);TDGAME.launchBrief();')
        check('level 3 briefing queues BOF-BASE before audio unlock',ev('TD.Audio._pending?.key==="base"&&!TD.Audio.on'))
        page.keyboard.press('Shift')
        ready();evidence['basePlayback']=snapshot()
        check('supplied BOF-BASE decodes and plays as the level 3 track',ev('TD.Audio.musicKey==="base"&&TD.Audio.music.currentSrc.endsWith("BOF-BASE.wav")&&Math.abs(TD.Audio.music.duration-122.4)<.01&&TD.Audio.music.loop'))
        evidence['baseRMS']=rms();check('native stage audio produces nonzero PCM signal',evidence['baseRMS']>.0001)
        ev('window.stageAudio=TD.Audio.music;TDGAME.resume();TD.game.fortress.pending=[];TD.game.units=[];TD.game.player.y=428;TD.game.player.x=400;TD.game.player.inv=999;TD.game.fortress.relays=3;')
        frames(1)
        check('ordinary level 3 boss spawn retains stage music throughout entrance',ev('TD.game.boss?.state==="enter"&&TD.Audio.music===stageAudio&&TD.Audio.musicKey==="base"'))
        frames(120)
        check('boss track does not begin before Gosfer entrance finishes',ev('TD.game.boss.state==="enter"&&TD.Audio.music===stageAudio'))
        frames(40);ready()
        evidence['gosferFadeStart']=snapshot()
        check('Gosfer combat starts a quiet Rise of the Last Hope crossfade',ev('TD.game.boss.state==="move"&&TD.Audio.musicKey==="lastHope"&&TD.Audio.music.volume<.15&&!stageAudio.paused&&TD.Audio.musicVoices.size===2'))
        page.wait_for_timeout(650);evidence['gosferFadeMiddle']=snapshot()
        check('both actual media volumes change gradually during boss crossfade',ev('TD.Audio.music.volume>.03&&TD.Audio.music.volume<.5&&stageAudio.volume>0&&stageAudio.volume<.55'))
        page.wait_for_timeout(1300);evidence['gosferFadeEnd']=snapshot()
        check('boss fade reaches music setting and releases outgoing stage audio',ev('Math.abs(TD.Audio.music.volume-.55)<.001&&stageAudio.paused&&TD.Audio.musicVoices.size===1'))
        check('supplied boss WAV decodes at its original duration and loops',ev('TD.Audio.music.currentSrc.endsWith("rise_of_the_last_hope_fast_riff_genesis.wav")&&Math.abs(TD.Audio.music.duration-40.324126984)<.01&&TD.Audio.music.loop'))
        evidence['bossRMS']=rms();check('native boss audio produces nonzero PCM signal',evidence['bossRMS']>.0001)
        ev('window.bossAudio=TD.Audio.music;')
        # These are cue-boundary fixtures, not claims of a complete combat route.
        for i in range(100):
            if ev('TD.game.boss.state==="dialogue"'):break
            ev('TD.game.player.inv=999');frames(30)
        check('actual Gosfer cover-breaker volleys reach the protected dialogue',ev('TD.game.boss.state==="dialogue"&&TD.game.boss.barrierLog.length===3&&TD.game.boss.barrierLog.every(q=>q.by==="gosfer")'))
        page.wait_for_timeout(750);evidence['dialogueDucked']=snapshot()
        check('dialogue ducks the same boss recording instead of restarting it',ev('TD.Audio.music===bossAudio&&Math.abs(TD.Audio.music.volume-.099)<.002'))
        shot('gosfer_dialogue')
        frames(635)
        check('music stays lowered through the lightning transformation',ev('TD.game.boss.state==="transform"&&TD.Audio.music===bossAudio&&Math.abs(TD.Audio.music.volume-.099)<.002'))
        frames(210)
        check('post-cutscene duel begins a fade back into the boss track',ev('TD.game.boss.phase===2&&TD.Audio.music===bossAudio&&TD.Audio.musicGain===1&&[...TD.Audio.musicVoices][0].fade?.to===1'))
        page.wait_for_timeout(2000)
        check('post-dialogue boss fade completes at normal volume without resetting time',ev('TD.Audio.music===bossAudio&&Math.abs(TD.Audio.music.volume-.55)<.002'))
        shot('gosfer_duel')
        ev('TD.Audio.music.currentTime=TD.Audio.music.duration-.15;');page.wait_for_timeout(650)
        check('boss recording loops in native playback',ev('TD.Audio.music.currentTime<2&&!TD.Audio.music.paused'))

        ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.launchBrief();');ready()
        check('level 7 briefing and initial room use BOF-BASE',ev('TD.Audio.musicKey==="base"&&TD.game.bastion.totalWave===0'))
        ev('TDGAME.resume();window.level7Stage=TD.Audio.music;')
        frames(80)
        ev('while(TD.game.bastion.totalWave<7){TD.game.units=[];TD.Bastion.wave(TD.game);}void 0;')
        check('rooms 1 through 7 retain the stage track',ev('TD.game.bastion.totalWave===7&&TD.Audio.music===level7Stage&&!TD.game.boss'))
        ev('TD.game.units=[];TD.Bastion.wave(TD.game);');ready()
        check('room 8 starts boss music at the core encounter',ev('TD.game.boss.form==="core"&&TD.game.boss.state==="enter"&&TD.Audio.musicKey==="lastHope"'))
        page.wait_for_timeout(750);evidence['coreFadeMiddle']=snapshot()
        check('reactor encounter crossfades both tracks',ev('TD.Audio.music.volume>.03&&TD.Audio.music.volume<.5&&!level7Stage.paused&&level7Stage.volume<.55'))
        page.wait_for_timeout(1300);ev('window.coreAudio=TD.Audio.music;TD.game.player.inv=999;');frames(100)
        shot('reactor_music')
        ev('TD.Bastion.coreHit(TD.game,999);');frames(300)
        check('reactor fracture, white flash and Helios reveal continue the same boss track',ev('TD.game.boss.form==="helios"&&TD.Audio.music===coreAudio&&TD.Audio.stats["music:lastHope"]===2'))
        shot('helios_music')
        ev('TD.game.player.dead=true;TD.game.player.deadT=2.1;');frames(1)
        check('boss retry keeps Rise of the Last Hope playing without restart',ev('TD.game.boss.form==="helios"&&TD.Audio.music===coreAudio&&TD.Audio.stats["music:lastHope"]===2'))

        ev('TD.Audio.fadeMusic(.18,.2);');page.wait_for_timeout(280)
        ev('TD.Frontend.settings.music=.4;TD.Frontend.settings.master=.5;TD.Frontend.applyAudio();')
        check('music and master options respect the current fade gain',ev('Math.abs(TD.Audio.music.volume-.036)<.001'))
        ev('TD.Frontend.settings.master=0;TD.Frontend.applyAudio();')
        check('master mute silences every active music voice',ev('[...TD.Audio.musicVoices].every(v=>v.audio.volume===0)'))
        ev('TD.Frontend.settings.music=.55;TD.Frontend.settings.master=1;TD.Frontend.applyAudio();TD.Audio.fadeMusic(1,.2);');page.wait_for_timeout(300)
        check('unmute restores selected music volume',ev('Math.abs(TD.Audio.music.volume-.55)<.001'))

        ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===7);TDGAME.start();');ready()
        check('fresh level 7 restart returns to BOF-BASE',ev('TD.Audio.musicKey==="base"&&TD.game.bastion.totalWave===0'))
        ev('window.loopingBase=TD.Audio.music;TD.Audio.music.currentTime=TD.Audio.music.duration-.15;');page.wait_for_timeout(650)
        check('stage recording loops in native playback',ev('TD.Audio.music===loopingBase&&TD.Audio.music.currentTime<2&&!TD.Audio.music.paused'))
        ev('TD.Bastion.startBoss(TD.game);');ready();page.wait_for_timeout(150)
        ev('window.interruptedVoices=[...TD.Audio.musicVoices].map(v=>v.audio);TD.Audio.stopMusic();')
        check('stop during a fade releases all tracks and cancels pending playback',ev('interruptedVoices.every(a=>a.paused)&&TD.Audio.musicVoices.size===0&&TD.Audio._musicFrame===null&&TD.Audio._pending===null'))
        ev('TD.Audio.on=false;TD.Audio.playMusic("lastHope",1.8);TD.Audio.stopMusic();TD.Audio.unlock();')
        check('a cancelled locked cue cannot start on later input',ev('TD.Audio.music===null&&!TD.Audio._pending'))
        ev('TD.game.sel=TD.MISSIONS.findIndex(m=>m.id===2);TDGAME.launchBrief();');ready()
        check('other campaign stages keep their existing stage music',ev('TD.Audio.musicKey==="level2"&&TD.Audio.music.currentSrc.endsWith("Unused1.mp3")'))
        ev('TD.Frontend.returnTo="title";TD.Frontend.go("title");');ready()
        check('return to title replaces and releases encounter music',ev('TD.Audio.musicKey==="title"&&TD.Audio.musicVoices.size===1'))
        check('native media and browser report no playback or asset errors',not errors and ev('TD.Audio.failures.length===0'))
        for entry in json.loads((ROOT/'expansion/topdown/audio/music23/manifest.json').read_text(encoding='utf-8'))['tracks']:
            local=ROOT/'expansion/topdown/audio/music23'/entry['file'];source=Path(r'C:\Users\Mike\Downloads')/entry['file']
            check('exact original WAV bytes preserved: '+entry['file'],hashlib.sha256(local.read_bytes()).hexdigest()==entry['sha256']==hashlib.sha256(source.read_bytes()).hexdigest())
        result={'build':'overdrive1014-music23-r1','checks':checks,'passed':sum(q['passed'] for q in checks),'failed':sum(not q['passed'] for q in checks),'errors':errors,'playback':evidence,'scope':'Real Chromium native HTMLAudio playback, PCM analysis and cue-boundary fixtures. Not a complete combat route.'}
        (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors,'playback':evidence},indent=2),flush=True)
        browser.close()
finally:
    stop()
sys.exit(0 if all(q['passed'] for q in checks) and not errors else 1)
