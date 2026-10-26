"""Actual Chromium playback, seeking, decoded pixels and frame-step checks."""
from pathlib import Path
import argparse
import json

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots' / 'furious_789_1025'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stages', default='7,8,9')
    parser.add_argument('--port', type=int)
    args = parser.parse_args()
    port = args.port or json.loads((OUT / 'review-server.json').read_text())['port']
    wanted = {int(s) for s in args.stages.split(',')}
    errors, ranges, checks = [], [], []
    previous = OUT / 'browser-playback.json'
    if previous.exists():
        old = json.loads(previous.read_text())
        for result in old.get('clips', []):
            (OUT / f'browser-stage{result["stage"]}.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    clips = json.loads((OUT / 'recordings.json').read_text())['clips']
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', args=['--autoplay-policy=no-user-gesture-required'])
        page = browser.new_page(viewport={'width': 1440, 'height': 1100})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('response', lambda r: ranges.append(r.status) if '.mp4' in r.url else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_selector('#tabs button', timeout=15000)
        print('REVIEW TABS', page.locator('#tabs').inner_text(), 'ERRORS', errors, flush=True)
        for clip in clips:
            if clip['stage'] not in wanted:
                continue
            page.locator(f'#tabs button[data-stage="{clip["stage"]}"]').click()
            page.wait_for_function('document.querySelector("video").readyState>=2', timeout=60000)
            duration = page.evaluate('document.querySelector("video").duration')
            hashes = []
            for at in (min(16, duration * .12), duration * .55, max(0, duration - 3)):
                result = page.evaluate(r'''async t=>{
                 const v=document.querySelector('video');v.pause();
                 await new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=t;});
                 await v.play();await new Promise(r=>setTimeout(r,850));v.pause();
                 const c=document.createElement('canvas');c.width=32;c.height=20;const g=c.getContext('2d');g.drawImage(v,0,0,32,20);
                 const hash=Array.from(g.getImageData(0,0,32,20).data).reduce((a,x)=>((a*31)+x)>>>0,0);
                 return{requested:t,time:v.currentTime,width:v.videoWidth,height:v.videoHeight,error:v.error?.code||null,
                   frames:v.getVideoPlaybackQuality().totalVideoFrames,hash,muted:v.muted,volume:v.volume};
                }''', at)
                hashes.append(result)
            before = page.evaluate('document.querySelector("video").currentTime')
            page.get_by_role('button', name='+1 frame', exact=True).click()
            page.wait_for_function('t=>document.querySelector("video").currentTime>t+.02', arg=before)
            after = page.evaluate('document.querySelector("video").currentTime')
            page.screenshot(path=str(OUT / f'review-stage{clip["stage"]}.png'))
            result = dict(stage=clip['stage'], duration=duration, samples=hashes,
                          checks=dict(playbackAdvances=all(q['time'] > q['requested'] + .2 for q in hashes),
                                      decodedPixelsChange=len({q['hash'] for q in hashes}) > 1,
                                      fullFrame=all(q['width'] == 1280 and q['height'] == 800 for q in hashes),
                                      noMediaErrors=all(q['error'] is None for q in hashes),
                                      audiblePlayer=all(not q['muted'] and q['volume'] > 0 for q in hashes),
                                      frameStep=abs((after - before) - 1 / 30) < .015))
            checks.append(result)
            (OUT / f'browser-stage{clip["stage"]}.json').write_text(json.dumps(result, indent=2), encoding='utf8')
            print(json.dumps(result), flush=True)
        browser.close()
    combined = [json.loads(p.read_text()) for p in sorted(OUT.glob('browser-stage[789].json'))]
    report = dict(clips=combined, errors=errors, byteRangeResponses=ranges,
                  passed=not errors and bool(checks) and all(all(c['checks'].values()) for c in checks))
    (OUT / 'browser-playback.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    print('BROWSER PASS' if report['passed'] else 'BROWSER FAIL', flush=True)
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
