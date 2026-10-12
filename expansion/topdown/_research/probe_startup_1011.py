"""Native Chromium verification of Mike's recorded Overdrive startup.

Uses real keyboard/pointer events and polled test controller hardware. Audio
time advances in the browser; simulation frame counts never stand in for
finishing the clip. All storage belongs to a fresh, isolated browser context.
"""
from pathlib import Path
import hashlib
import json
import sys
import wave
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / '_BUILD_SOURCE'))
import shoot

OUT = ROOT / '_shots/overdrive_startup_1011'
OUT.mkdir(parents=True, exist_ok=True)
checks, errors, observations = [], [], {}

def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})
    print(('PASS ' if passed else 'FAIL ') + name, flush=True)

source = ROOT / 'expansion/topdown/audio/source/overdrive.wav'
supplied = Path(r'C:\Users\Mdogg\Desktop\overdrive.wav')
manifest = json.loads((source.parent.parent / 'startup.json').read_text())
check('preserved WAV matches the supplied original byte for byte',
      hashlib.sha256(source.read_bytes()).hexdigest() == manifest['sourceSha256'] and
      (not supplied.exists() or source.read_bytes() == supplied.read_bytes()))
with wave.open(str(source)) as wav:
    check('source duration, sample rate and channels match recorded provenance',
          wav.getnframes() / wav.getframerate() == manifest['durationSeconds'] and
          wav.getframerate() == manifest['sampleRate'] and wav.getnchannels() == manifest['channels'])

port, stop = shoot.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={'width': 1400, 'height': 1100})
        context.add_init_script("localStorage.setItem('bof_od_options',JSON.stringify({master:.5,voice:.4,music:.55,sfx:.8,engine:1}));")
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: errors.append(f'HTTP {r.status} {r.url}') if r.status >= 400 else None)
        page.goto(f'http://127.0.0.1:{port}/expansion/topdown/index.html?qa=startup1011')
        page.wait_for_function('window.TDGAME && TDGAME.G.state==="boot"', timeout=60000)
        page.evaluate('TDGAME.freeze()')

        def frames(n):
            while n:
                batch = min(45, n)
                page.evaluate('n=>TDGAME.step(n)', batch)
                page.wait_for_timeout(25)
                n -= batch

        def tap(key, n=20):
            page.keyboard.down(key)
            frames(1)
            page.keyboard.up(key)
            frames(n)

        def boot():
            page.evaluate("TD.Frontend.returnTo='title';TD.Frontend.boot()")
            frames(20)

        def snap(name):
            page.evaluate('TDGAME.render()')
            page.locator('#screen').screenshot(path=str(OUT / (name + '.png')))

        def ready():
            page.wait_for_function('TD.Frontend.voice && TD.Frontend.voice.readyState>=3 && TD.Frontend.voice.currentTime>0', timeout=15000)

        frames(24)
        page.wait_for_function('["logo","overdrive","bof_cover_b"].every(k=>!!ART.get(k))', timeout=30000)
        frames(1)
        snap('boot')
        check('boot waits for user input without autoplay or title music',
              page.evaluate('TDGAME.G.state==="boot" && !TD.Audio.on && !TD.Frontend.voice && !TD.Audio.music'))
        tap('Enter')
        ready()
        observations['playback'] = page.evaluate('(()=>{const a=TD.Frontend.voice;return {src:a.currentSrc,duration:a.duration,volume:a.volume,rate:a.playbackRate,paused:a.paused,time:a.currentTime};})()')
        playback = observations['playback']
        check('Start plays the actual supplied recording through decoded browser media',
              playback['src'].endswith('/expansion/topdown/audio/overdrive-startup.mp3') and
              not playback['paused'] and playback['rate'] == 1 and
              abs(playback['duration'] - manifest['durationSeconds']) < .06)
        check('saved Master and Voice controls set the actual recording volume', abs(playback['volume'] - .2) < .00001)
        frames(180)
        check('intro waits for actual audio completion beyond its minimum visual timer',
              page.evaluate('TDGAME.G.state==="intro" && TDGAME.G.stateT>1.8 && !TD.Frontend.voiceDone && !TD.Audio.music'))
        snap('intro')
        page.evaluate('window.lastStartupVoice=TD.Frontend.voice')
        page.wait_for_function('TD.Frontend.voiceDone', timeout=15000)
        frames(1)
        page.wait_for_function('TD.Audio.music && TD.Audio.music.readyState>=3 && TD.Audio.music.currentTime>0', timeout=15000)
        check('natural completion enters title and releases the finished voice',
              page.evaluate('TDGAME.G.state==="title" && !TD.Frontend.voice && lastStartupVoice.ended && lastStartupVoice.paused'))
        check('original BOF title music begins after the recording ends',
              page.evaluate('TD.Audio.musicKey==="title" && TD.Audio.music.currentSrc.endsWith("/Title.mp3") && !TD.Audio.music.paused'))
        snap('title')

        # Restarting the presentation stops title music and uses a fresh voice.
        boot()
        check('restarting boot stops the previous title music', page.evaluate('!TD.Audio.music && !TD.Frontend.voice'))
        tap('Enter')
        ready()
        check('a replay starts a fresh recording from the beginning',
              page.evaluate('TD.Frontend.voice!==lastStartupVoice && TD.Frontend.voice.currentTime<1 && !TD.Frontend.voiceDone && !TD.Audio.music'))
        page.evaluate('window.lastStartupVoice=TD.Frontend.voice')
        tap('Enter')
        check('Start skips the intro immediately and pauses its recording',
              page.evaluate('TDGAME.G.state==="title" && !TD.Frontend.voice && lastStartupVoice.paused && !lastStartupVoice.ended'))
        stopped_time = page.evaluate('lastStartupVoice.currentTime')
        page.wait_for_timeout(200)
        check('a skipped voice remains stopped behind the title menu',
              abs(page.evaluate('lastStartupVoice.currentTime') - stopped_time) < .01)

        boot()
        tap('Enter')
        ready()
        page.evaluate('window.lastStartupVoice=TD.Frontend.voice')
        tap('b')
        check('logical B skips to title and stops the startup voice',
              page.evaluate('TDGAME.G.state==="title" && !TD.Frontend.voice && lastStartupVoice.paused'))

        boot()
        rect = page.locator('#screen').bounding_box()
        page.mouse.click(rect['x'] + rect['width'] * .5, rect['y'] + rect['height'] * .5)
        frames(20)
        ready()
        check('a real pointer gesture starts recorded playback', page.evaluate('TDGAME.G.state==="intro" && !TD.Frontend.voice.paused'))
        page.evaluate('window.lastStartupVoice=TD.Frontend.voice')
        tap('F1')
        check('leaving the intro for Help stops its voice before menu music',
              page.evaluate('TDGAME.G.state==="help" && !TD.Frontend.voice && lastStartupVoice.paused && TD.Audio.musicKey==="title"'))

        # Test hardware uses the input system's persisted physical button map.
        page.evaluate("window.startupPad={id:'Overdrive startup QA',index:0,connected:true,mapping:'standard',axes:[0,0,0,0],buttons:Array.from({length:20},()=>({pressed:false,value:0}))};Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[startupPad]});TD.Input.setPadStyle('six');")
        boot()
        page.evaluate('startupPad.buttons[TD.Input.padProfile().start].pressed=true')
        frames(1)
        page.evaluate('startupPad.buttons.forEach(b=>b.pressed=false)')
        frames(20)
        ready()
        check('the physical controller Start button launches recorded intro', page.evaluate('TDGAME.G.state==="intro" && !TD.Frontend.voice.paused'))
        page.evaluate('window.lastStartupVoice=TD.Frontend.voice;startupPad.buttons[TD.Input.padProfile().B].pressed=true')
        frames(1)
        page.evaluate('startupPad.buttons.forEach(b=>b.pressed=false)')
        frames(20)
        check('the physical controller B button skips and silences the recording',
              page.evaluate('TDGAME.G.state==="title" && !TD.Frontend.voice && lastStartupVoice.paused'))

        boot()
        page.evaluate('TD.Frontend.settings.voice=0;TD.Frontend.applyAudio()')
        tap('Enter')
        ready()
        check('muted Voice still plays silently with the same completion/skip timing',
              page.evaluate('TD.Frontend.voice.volume===0 && !TD.Frontend.voice.paused && TDGAME.G.state==="intro"'))
        tap('b')
        check('no page, console, HTTP, decode or playback errors', not errors and page.evaluate('!TD.Audio.failures.length'))
        browser.close()
finally:
    stop()

report = {'date': '2026-10-11', 'entry': 'expansion/topdown/index.html',
          'build': 'overdrive1011-startup', 'checks': checks, 'browserErrors': errors,
          'recording': manifest, 'observations': observations,
          'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks)}
(OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'{report["passed"]}/{len(checks)} startup checks passed', flush=True)
sys.exit(0 if not report['failed'] and not errors else 1)
