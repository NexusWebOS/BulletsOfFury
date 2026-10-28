"""Real-Chromium playback, decoded pixels, chapter seeks and responsive review."""
from pathlib import Path
import argparse, json
from playwright.sync_api import sync_playwright
from shoot import serve

R = Path(__file__).resolve().parents[1]
B = R / '_shots/stage6_9_refresh_1028'
parser = argparse.ArgumentParser()
parser.add_argument('--public', action='store_true')
args = parser.parse_args()
out = R / json.loads((B / 'latest.json').read_text())['folder']
manifest = json.loads((R / 'docs/previews/stage6_9_github_1028/manifest.json').read_text(encoding='utf-8'))
checks, errors, samples = {}, [], []
if args.public:
    url, stop = 'https://nexuswebos.github.io/BulletsOfFury/?updated=20261028', lambda: None
else:
    port, stop = serve(str(R))
    url = f'http://127.0.0.1:{port}/docs/previews/stage6_9_github_1028/index.html'
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', headless=True, args=['--autoplay-policy=no-user-gesture-required'])
        p = browser.new_page(viewport={'width': 1280, 'height': 900})
        p.set_default_timeout(180000)
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        p.on('response', lambda r: errors.append(str(r.status)+' '+r.url) if r.status >= 400 else None)
        p.goto(url, wait_until='domcontentloaded', timeout=180000)
        p.wait_for_function('clips.length>0&&player.readyState>=2')
        p.evaluate("document.querySelectorAll('.card img').forEach(i=>i.loading='eager')")
        p.wait_for_function("[...document.querySelectorAll('.card img')].every(i=>i.complete&&i.naturalWidth===480&&i.naturalHeight===300)")
        checks['allNativePostersDecode'] = True
        checks['allExpectedCards'] = p.locator('.card').count() == len(manifest)
        checks['nineFullRecordings'] = len([c for c in manifest if not c.get('parent')]) == 9
        for c in [c for c in manifest if not c.get('parent')]:
            print('MOVIE',c['id'],flush=True)
            p.locator('.card[data-id="'+c['id']+'"]').click()
            p.wait_for_function('id=>player.dataset.clip===id&&player.readyState>=2&&!player.seeking', arg=c['id'])
            p.evaluate('player.muted=true;player.pause()')
            checks[c['id']+'Dimensions'] = p.evaluate('player.videoWidth===1280&&player.videoHeight===800')
            checks[c['id']+'Duration'] = abs(p.evaluate('player.duration')-c['seconds']) < 2
            p.evaluate('player.currentTime=Math.min(12,player.duration/3)')
            p.wait_for_function('!player.seeking&&player.readyState>=2')
            p.evaluate('player.play()')
            p.wait_for_timeout(450)
            t = p.evaluate('player.currentTime')
            p.wait_for_timeout(450)
            checks[c['id']+'Plays'] = p.evaluate('player.currentTime') > t
            p.evaluate('player.pause();player.currentTime=player.duration-2')
            p.wait_for_function('!player.seeking&&player.readyState>=2&&Math.abs(player.currentTime-(player.duration-2))<.75')
            checks[c['id']+'SeeksToEnding'] = p.evaluate('player.error===null')
            if not args.public:
                # Actual decoded local-video pixels, not selected state or a poster.
                samples.append(p.evaluate('''()=>{const c=document.createElement('canvas');c.width=320;c.height=200;const g=c.getContext('2d');g.drawImage(player,0,0,320,200);const a=g.getImageData(0,0,320,200).data;let lit=0,min=255,max=0;for(let i=0;i<a.length;i+=4){const v=(a[i]+a[i+1]+a[i+2])/3;min=Math.min(min,v);max=Math.max(max,v);if(v>30)lit++;}return {clip:player.dataset.clip,lit,min,max}}'''))
            p.screenshot(path=str(out / ('public-' if args.public else 'playback-') / (c['id']+'.png')))
        chapters = [c for c in manifest if c.get('parent')]
        for c in chapters:
            print('CHAPTER',c['id'],flush=True)
            b = p.locator('.card[data-id="'+c['id']+'"]')
            b.evaluate("b=>b.closest('details').open=true")
            # The UI auto-plays selected chapters. Stop on its first real playing
            # event so the assertion measures the seek, independent of click latency.
            p.evaluate("player.addEventListener('playing',()=>player.pause(),{once:true})")
            b.click()
            p.wait_for_function('c=>player.dataset.clip===c.id&&player.readyState>=2&&!player.seeking&&Math.abs(player.currentTime-c.start)<1.5', arg=c)
            p.evaluate('player.pause()')
            checks[c['id']+'ChapterSeek'] = p.evaluate('!document.querySelector("#whole").hidden&&player.error===null')
        if chapters:
            p.locator('#whole').click()
            p.wait_for_function('!player.seeking&&player.readyState>=2&&document.querySelector("#whole").hidden')
            checks['fullFightReturn'] = p.evaluate('player.currentTime<2')
        # A rapid selection must not let a stale fetch replace the latest film.
        p.evaluate("document.querySelector('.card[data-id=\"stage7-boss\"]').click();document.querySelector('.card[data-id=\"stage9-boss\"]').click()")
        p.wait_for_function('player.dataset.clip==="stage9-boss"&&player.readyState>=2&&!player.seeking')
        checks['latestSelectionWins'] = p.evaluate('player.dataset.source.includes("stage9-boss")')
        p.evaluate('player.pause()')
        checks['desktopFits'] = p.evaluate('document.documentElement.scrollWidth<=innerWidth')
        p.screenshot(path=str(out / ('gallery-public-desktop.png' if args.public else 'gallery-desktop.png')), full_page=True)
        p.set_viewport_size({'width': 480, 'height': 900})
        checks['mobileFits'] = p.evaluate('document.documentElement.scrollWidth<=innerWidth')
        p.screenshot(path=str(out / ('gallery-public-mobile.png' if args.public else 'gallery-mobile.png')), full_page=True)
        checks['noBrowserErrors'] = not errors and p.evaluate('player.error===null')
        if samples:
            checks['allMoviesHaveDecodedPixels'] = all(x['lit'] > 5000 and x['max']-x['min'] > 100 for x in samples)
        browser.close()
finally:
    stop()
result = dict(checks=checks, errors=errors, decodedPixelSamples=samples, url=url)
destination = out / ('public-playback.json' if args.public else 'gallery-playback.json')
destination.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(dict(passed=sum(checks.values()), total=len(checks), failed=[k for k,v in checks.items() if not v], errors=errors)))
raise SystemExit(0 if all(checks.values()) else 1)
