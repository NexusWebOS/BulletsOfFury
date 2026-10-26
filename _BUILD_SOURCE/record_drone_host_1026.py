"""Record the native portal, drone arrival, conversion and start of phase1.

No damage fixtures, phase writes or animation timer skips. God mode only keeps
the observer alive; player controls/weapons stay idle and native boss HP remains.
"""
from barrage_review_common_1025 import ROOT, boot
from shoot import serve
from record_furious_789_1025 import CAPTURE
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
from uuid import uuid4
import base64
import imageio_ffmpeg
import json
import re
import argparse
import subprocess

ap=argparse.ArgumentParser();ap.add_argument('--rework',action='store_true');args=ap.parse_args()
OUT = ROOT / ('_shots/drone_rework_1026/video' if args.rework else '_shots/drone_host_1026') / ('take-' + uuid4().hex[:8])
OUT.mkdir(parents=True, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
errors, assets, timeline = [], [], []
cap = CAPTURE.replace("debugStartFight(entry,{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;", "DBGT.god=true;DBGT.speed=1;player.invuln=0;")
cap = cap.replace('A.tick++;', "A.tick++;for(const key of ['a','d','w','s','j','k','c'])K[key]=false;return;")
cap = cap.replace('INVULNERABLE INPUT BOT / NATIVE HP & PHASES', 'DRONE TO PHASE1 / NATIVE ARRIVAL, CONVERSION & AUDIO')
port, stop = serve(str(ROOT))
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel='msedge', args=['--autoplay-policy=no-user-gesture-required', '--disable-background-timer-throttling', '--disable-renderer-backgrounding'])
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        p = boot(context, port, 8, errors, 'boss')
        p.on('response', lambda r: assets.append(str(r.status) + ' ' + r.url) if r.status >= 400 else None)
        p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bi24Warm()&&r25Warm(8)&&rd28Ready()&&rd29Ready()}', timeout=180000)
        initial = p.evaluate('({mode:boss._r30.mode,t:boss._r30.t,hp:boss.hp})')
        assert initial['mode'] == 'dr5er23entry' and initial['t'] < .1, initial
        with (OUT / 'capture.webm').open('wb') as raw:
            p.expose_function('saveCaptureChunk', lambda data: raw.write(base64.b64decode(data)))
            p.evaluate('()=>{window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
            p.evaluate(cap, {'stage': 8})
            print('Recording native drone-to-first-host sequence', flush=True)
            fight_start = None
            while True:
                p.wait_for_timeout(150)
                q = p.evaluate("""()=>({seconds:(performance.now()-captureStart)/1000,mode:boss._r30.mode,t:boss._r30.t,hp:boss.hp,maxhp:boss.maxhp,encounter:j3State(boss).encounter,protected:boss._noHit,frames:captureStats.frames,dialogue:dr5State(boss).radio?.text,rework:RD29.last,background:RD29.backgroundLast,parts:boss.parts.map(p=>({id:p.id,hp:p.hp,maxhp:p.maxhp,destroyed:p.destroyed}))})""")
                timeline.append(q)
                if q['mode'] == 'fight' and fight_start is None:
                    fight_start = q['seconds']
                if (fight_start is not None and q['seconds'] >= fight_start + 6) or q['seconds'] > 25 or errors:
                    break
            sound = p.evaluate("""async()=>{reviewBot.enabled=false;await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop();});await capturePending;captureLive=false;return captureStats;}""")
        events = p.evaluate('({rebirth:RB23.events,phase:V18.events,rework:RD29.events})')
        (OUT / 'capture-metadata.json').write_text(json.dumps({'timeline': timeline, 'sound': sound, 'initial': initial, 'events': events, 'errors': errors, 'assetErrors': assets}, indent=2), encoding='utf8')
        browser.close()
finally:
    stop()
movie = OUT / 'drone-to-dracodia-phase1.mp4'
subprocess.run([FF, '-v', 'error', '-y', '-threads', '2', '-i', str(OUT / 'capture.webm'), '-vf', 'fps=30', '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-c:a', 'aac', '-b:a', '160k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(movie)], check=True)
decode = subprocess.run([FF, '-hide_banner', '-nostats', '-threads', '2', '-i', str(movie), '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
(OUT / 'decode.log').write_text(decode.stderr, encoding='utf8')
peak = re.search(r'max_volume: ([\-\d.inf]+) dB', decode.stderr)
db = float(peak[1]) if peak else -999
arrival = next(q['seconds'] - q['t'] for q in timeline if q['mode'] == 'v18arrival')
conversion = next(q['seconds'] - q['t'] for q in timeline if q['mode'] == 'v18conversion')
chapters = {'portal': .6, 'drone-arrival': arrival + .9, 'conversion-start': conversion + .25,
            'conversion-middle': conversion + 2.1, 'conversion-end': conversion + 3.8,
            'phase1-fight': fight_start + 1.5}
if args.rework:
    chapters={'background-warp':1.2,'palette-darkening':2.8,'arena-fade':4.4,'purple-gate':6.4,
              'drone-arrival':arrival+.9,'conversion-middle':conversion+2.5,'charge':conversion+4.3,
              'whiteout':conversion+5.9,'host-reveal':conversion+7.4,'phase1-fight':fight_start+1.5}
checks = {'nativeEntryFromTimeZero': initial['mode'] == 'dr5er23entry' and initial['t'] < .1,
          'droneArrivalShown': any(q['mode'] == 'v18arrival' for q in timeline),
          'completeNativeConversionShown': any(q['mode'] == 'v18conversion' and q['t'] < .3 for q in timeline) and any(q['mode'] == 'v18conversion' and q['t'] > 4 for q in timeline),
          'nativePhase1Starts': fight_start is not None and all(q['encounter'] == 0 for q in timeline),
          'fullNativeFightHealth': all(q['hp'] == q['maxhp'] and not any(p['destroyed'] for p in q['parts']) for q in timeline if q['mode'] == 'fight'),
          'nativeConversionDialogue': any('drone' in (q.get('dialogue') or '').lower() for q in timeline),
          'audibleNativeConversion': db > -60 and all(sound['playing'].get(k, 0) > 0 for k in ['combatAlien0927', 'dracodiaShriek']),
          'fullDecode': decode.returncode == 0, 'realTimeFrames': sound['frames'] / timeline[-1]['seconds'] > 45,
          'noPageConsoleOrAssetErrors': not errors and not assets}
if args.rework:
    checks.update({'fullReworkedConversion':any(q['mode']=='v18conversion' and q['t']>7.7 for q in timeline),
                   'gateAndCodeVisible':any(q['rework'].get('gate') for q in timeline)and any(q['rework'].get('code') for q in timeline),
                   'hostCoveredBeforeReveal':all(not q['rework']['host'] or q['rework']['white']==16 for q in timeline if q['mode']=='v18conversion'and q['t']<6.1)})
report = {'video': movie.relative_to(ROOT).as_posix(), 'timeline': timeline, 'initial': initial, 'events': events,
          'sound': sound, 'decodedPeakDb': db, 'chapters': chapters, 'checks': checks,
          'errors': errors, 'assetErrors': assets, 'method': __doc__}
(OUT / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf8')
(OUT.parent / 'latest.json').write_text(json.dumps({'folder': str(OUT), 'report': str(OUT / 'report.json')}, indent=2), encoding='utf8')
contact = Image.new('RGB', (1280, ((len(chapters)+2)//3)*285), (5, 10, 17)); draw = ImageDraw.Draw(contact)
for i, (name, at) in enumerate(chapters.items()):
    png = OUT / (name + '.png')
    subprocess.run([FF, '-v', 'error', '-y', '-threads', '2', '-ss', str(at), '-i', str(movie), '-frames:v', '1', str(png)], check=True)
    contact.paste(Image.open(png).convert('RGB').resize((426, 266)), (i % 3 * 426, i // 3 * 285))
    draw.text((i % 3 * 426 + 3, i // 3 * 285 + 266), name, fill='white')
contact.save(OUT / 'contact.jpg')
print(json.dumps({'checks': checks, 'seconds': timeline[-1]['seconds'], 'peakDb': db, 'folder': str(OUT), 'conversionStarts': conversion, 'fightStarts': fight_start}), flush=True)
raise SystemExit(0 if all(checks.values()) else 1)
