"""Verify real Stage 7 music routing, browser decode and media playback."""
import json
from pathlib import Path
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = Path('_shots/reaperman_0927')
OUT.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--no-sandbox', '--mute-audio', '--autoplay-policy=no-user-gesture-required'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1100})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('()=>window.__bofFrames>4 && Snd.music.boss7 && Snd.music.unused13')
        page.evaluate(sh.TRAP_RAF)
        page.wait_for_timeout(60)
        result = page.evaluate('''async()=>{
          const ac=new AudioContext(), rows=[];
          for(const key of ['boss7','unused13']){
            const response=await fetch(BOFA.music[key]);
            if(!response.ok)throw Error(key+' HTTP '+response.status);
            const buf=await ac.decodeAudioData(await response.arrayBuffer());
            const data=buf.getChannelData(0);let peak=0;
            for(let i=0;i<data.length;i++)peak=Math.max(peak,Math.abs(data[i]));
            Audio.startMusic(key);const el=Snd.music[key];
            for(let i=0;i<80&&el.currentTime<.2;i++)await new Promise(r=>setTimeout(r,50));
            rows.push({key,src:BOFA.music[key],duration:buf.duration,channels:buf.numberOfChannels,
              peak,playing:Audio.musicPlaying(),currentTime:el.currentTime,error:el.error?.message||null});
            Audio.stopMusic();
          }
          await ac.close();
          return {rows,bossAlias:BOFA.music.boss7mus,field:BOFA.music.stage7mus};
        }''')
        assert result['bossAlias'] == 'assets/game/music/Level7b.mp3', result
        assert result['field'] == 'assets/game/music/Level7.mp3', result
        assert all(r['peak'] > .01 and r['playing'] and r['currentTime'] > .1 and not r['error'] for r in result['rows']), result
        assert not errors, errors
        result['errors'] = errors
        (OUT/'browser.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result, indent=2))
        browser.close()
finally:
    stop()
