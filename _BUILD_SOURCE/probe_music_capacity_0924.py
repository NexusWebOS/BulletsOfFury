"""Real Chromium music regression: decoder capacity, playback and audible signal.

No autoplay bypass or media-player-limit override. A real key unlocks audio.
Exercises HTTP and file launch, the full cue bank, and reusing an evicted cue.
"""
from pathlib import Path
import importlib.util
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/music_capacity_0924'
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('shoot', ROOT / '_BUILD_SOURCE/shoot.py')
sh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sh)
SNAP = """() => ({state, volume:Snd.vol, voices:Snd._sfxVoices.length,
  music:Snd.cur?{time:Snd.cur.currentTime,paused:Snd.cur.paused,
    ready:Snd.cur.readyState,error:Snd.cur.error&&Snd.cur.error.message,
    volume:Snd.cur.volume,muted:Snd.cur.muted}:null})"""

def main():
    port, stop = sh.serve(str(ROOT))
    report = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox'])
            for label, url in [('http', f'http://127.0.0.1:{port}/index.html'),
                               ('file', (ROOT/'index.html').as_uri())]:
                page = browser.new_page(viewport={'width':1100, 'height':1200})
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('console', lambda e: errors.append(e.text[:220]) if e.type=='error' else None)
                page.goto(url, wait_until='load', timeout=120000)
                page.wait_for_function("typeof Snd!=='undefined' && (state===GS.BOOT||state===GS.TITLE) && stateT>.3", timeout=60000)
                page.keyboard.press('Enter')
                page.wait_for_function("Snd.cur && !Snd.cur.paused && Snd.cur.currentTime>.1 && !Snd.cur.error", timeout=30000)
                row = report[label] = {'boot':page.evaluate(SNAP)}
                page.evaluate(sh.TRAP_RAF)
                page.screenshot(path=str(OUT/f'{label}_music_restored.png'))
                for key in ['title', 'lvl1', 'boss1', 'boss8']:
                    page.evaluate('(key)=>Audio.startMusic(key)', key)
                    page.wait_for_function("Snd.cur && Snd.cur.readyState>=3 && Snd.cur.currentTime>.15 && !Snd.cur.error", timeout=15000)
                    row[key] = page.evaluate(SNAP)
                row['stress'] = page.evaluate("""async()=>{
                  const first=Snd.pools.machineGun.list[0];
                  for(const [i,name] of Object.keys(Snd.pools).entries()){
                    Snd.prepare(name);
                    if(i%4===0)await new Promise(r=>setTimeout(r,20));
                  }
                  const evicted=!first.getAttribute('src');
                  const live=Snd._sfxVoices.length;
                  Snd._last.machineGun=-Infinity;Snd.play('machineGun');
                  await new Promise(r=>setTimeout(r,400));
                  return {count:Object.keys(Snd.pools).length,live,limit:Snd._voiceLimit,evicted,
                    cuePlays:Snd.pools.machineGun.slots.some(v=>v&&v.el.currentTime>.01&&!v.el.error)};
                }""")
                assert row['stress']['live'] <= row['stress']['limit'], row
                assert row['stress']['evicted'] and row['stress']['cuePlays'], row
                page.evaluate("Audio.startMusic('title')")
                page.wait_for_function('Snd.cur.currentTime>.2 && !Snd.cur.error', timeout=15000)
                row['afterStress'] = page.evaluate(SNAP)
                assert row['afterStress']['music']['volume'] > 0
                if label == 'http':
                    row['signal'] = page.evaluate("""async()=>{
                      const c=new AudioContext();await c.resume();
                      const s=c.createMediaElementSource(Snd.cur),a=c.createAnalyser();
                      s.connect(a);a.connect(c.destination);
                      const v=new Float32Array(2048);let peak=0;
                      for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,30));
                        a.getFloatTimeDomainData(v);for(const x of v)peak=Math.max(peak,Math.abs(x));}
                      return {context:c.state,peak};
                    }""")
                    assert row['signal']['peak'] > .01, row
                row['errors'] = errors
                assert not errors, errors
                page.close()
            browser.close()
    finally:
        stop()
        (OUT/'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    print('PASS: HTTP/file music, bounded decoder stress, evicted cue replay, real audio signal')

if __name__ == '__main__':
    main()
