"""Verify every published inspection chapter in the real browser decoder."""
from pathlib import Path
import datetime
import json
import urllib.request
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
OUT = ROOT / 'playback-1103'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:63094'
URL = BASE + '/review/current/all-waves-1101.html?inspection=1103'
data = json.load(urllib.request.urlopen(BASE + '/review/current/all-waves-1101.json', timeout=20))
errors = []
checks = []
assert data['difficulty'] == 'furious' and data['god']
assert data['inspectionRevision'] == 'observe-clear-1103'

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', headless=True, args=['--autoplay-policy=no-user-gesture-required'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.on('response', lambda response: errors.append(f'HTTP {response.status} {response.url}') if response.status >= 400 else None)
    page.goto(URL, wait_until='networkidle', timeout=60000)
    page.wait_for_function('typeof library !== "undefined" && library.levels.length === 10')
    for level in data['levels']:
        page.evaluate('id => selectLevel(id, 1)', level['id'])
        page.wait_for_function('id => current.id === id && video.readyState >= 2', arg=level['id'])
        page.evaluate('video.pause()')
        duration = page.evaluate('video.duration')
        previous = -1
        previous_start = -1
        for wave in level['waves']:
            # Independent wall-clock stamps can overlap by up to 90ms at a cut;
            # chapter starts remain strictly ordered and the material is not lost.
            assert wave['start'] > previous_start and wave['start'] >= previous - 0.1 and wave['start'] < wave['cleanup'] <= wave['end'] <= duration + 0.1, (level['id'], wave)
            assert wave['observeSeconds'] >= 8, (level['id'], wave['number'])
            previous = wave['end']
            previous_start = wave['start']
            for phase, target in [('observation', (wave['start'] + wave['cleanup']) / 2), ('cleanup', min(wave['end'] - 0.1, wave['cleanup'] + 0.5))]:
                page.evaluate('t => { video.pause(); video.currentTime = t; }', target)
                page.wait_for_function('t => !video.seeking && video.readyState >= 2 && Math.abs(video.currentTime - t) < 0.1', arg=target, timeout=20000)
                pixel = page.evaluate('''() => {
                    const c = document.createElement('canvas'); c.width=80; c.height=50;
                    const x=c.getContext('2d'); x.drawImage(video,0,0,80,50);
                    const p=x.getImageData(0,0,80,50).data; const colors=new Set(); let lit=0;
                    for(let i=0;i<p.length;i+=4){ colors.add((p[i]<<16)|(p[i+1]<<8)|p[i+2]); if(p[i]+p[i+1]+p[i+2]>70)lit++; }
                    return {colors:colors.size, lit, width:video.videoWidth, height:video.videoHeight, time:video.currentTime, error:video.error?.message||null};
                }''')
                assert pixel['width'] == 1280 and pixel['height'] == 800 and pixel['colors'] > 80 and pixel['lit'] > 200 and not pixel['error'], (level['id'], wave['number'], phase, pixel)
                checks.append({'level':level['id'], 'wave':wave['number'], 'phase':phase, 'pixels':pixel})
        page.screenshot(path=str(OUT / (level['id'] + '.png')))
        print('VERIFIED', level['id'], len(level['waves']), 'chapters / observation + cleanup', flush=True)
        (OUT / 'progress.json').write_text(json.dumps({'completedLevels':len({q['level'] for q in checks}), 'decodedFrames':len(checks), 'errors':errors}, indent=2), encoding='utf8')
    assert not errors, errors
    browser.close()

result = {'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'url':URL,
          'sourceRecordedAt':data['recordedAt'], 'films':len(data['levels']), 'chapters':data['chapterCount'],
          'decodedFrames':len(checks), 'difficulty':data['difficulty'], 'god':data['god'], 'errors':errors,
          'unreleasedOrInvisibleChapters':[{'level':l['id'],'wave':w['number'],'note':w['inspectionNote']} for l in data['levels'] for w in l['waves'] if w['noVisibleEnemy']],
          'limits':'Checks browser decoding, chapter bounds and recorded observation metadata; not an exhaustive human review of every attack or an ordinary-cadence balance certification.', 'checks':checks}
(OUT / 'all-chapters.json').write_text(json.dumps(result, indent=2), encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','unreleasedOrInvisibleChapters')}, indent=2), flush=True)
