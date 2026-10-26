"""Verify audible drone/phase1 review playback and byte-range seeking."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import argparse

R = Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--rework',action='store_true');args=ap.parse_args()
latest = json.loads((R / ('_shots/drone_rework_1026/video/latest.json' if args.rework else '_shots/drone_host_1026/latest.json')).read_text())
folder = Path(latest['folder'])
report = json.loads(Path(latest['report']).read_text())
url = 'http://127.0.0.1:53746/' + report['video']
errors, checks = [], {}
with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', args=['--autoplay-policy=no-user-gesture-required'])
    p = browser.new_page(viewport={'width': 1440, 'height': 1000})
    p.on('pageerror', lambda e: errors.append(str(e)))
    p.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    p.goto(url, wait_until='domcontentloaded')
    p.wait_for_function('document.querySelector("video")?.readyState>=2')
    checks['decoded1280x800'] = p.evaluate('()=>{const v=document.querySelector("video");return v.videoWidth===1280&&v.videoHeight===800;}')
    for chapter in (['background-warp','purple-gate','drone-arrival','conversion-middle','charge','whiteout','host-reveal','phase1-fight'] if args.rework else ['drone-arrival','conversion-middle','phase1-fight']):
        at = report['chapters'][chapter]
        p.evaluate('(t)=>{const v=document.querySelector("video");v.pause();v.currentTime=t;}', at)
        p.wait_for_function('(t)=>{const v=document.querySelector("video");return !v.seeking&&Math.abs(v.currentTime-t)<.12;}', arg=at)
        p.evaluate('async()=>{const v=document.querySelector("video");v.muted=false;await v.play();}')
        p.wait_for_function('(t)=>document.querySelector("video").currentTime>t+.2', arg=at)
        checks[chapter + 'PlaysWithAudio'] = p.evaluate('()=>{const v=document.querySelector("video");v.pause();return !v.error&&!v.muted&&v.getVideoPlaybackQuality().totalVideoFrames>2;}')
        if chapter == 'conversion-middle':
            p.screenshot(path=str(folder / 'playback-conversion.png'))
    response = p.request.get(url, headers={'Range': 'bytes=1000-1999'})
    checks['byteRangeSeeking'] = response.status == 206 and len(response.body()) == 1000
    checks['noBrowserErrors'] = not errors
    browser.close()
(folder / 'playback.json').write_text(json.dumps({'url': url, 'checks': checks, 'errors': errors}, indent=2), encoding='utf8')
print(json.dumps({'url': url, 'checks': checks, 'errors': errors}))
raise SystemExit(0 if all(checks.values()) else 1)
