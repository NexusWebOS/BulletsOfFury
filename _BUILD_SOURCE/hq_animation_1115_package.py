from pathlib import Path
import json, subprocess, re, hashlib
from PIL import Image, ImageDraw
import imageio_ffmpeg

ROOT = Path('D:/BOF-Downloads/2026-11-14/RevG-source')
OUT = ROOT / '_shots/hq_animation_1115'
ENC = OUT / 'encoded'
ENC.mkdir(exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
q = json.loads((OUT / 'recording.json').read_text(encoding='utf8'))
assert len(q['clips']) == 2 and not q['errors']
assert q['coreBefore'] == q['coreAfter']
a, b = q['clips']
assert [a['part'], b['part']] == ['chronos', 'hq5']
assert all(not c['errors'] for c in q['clips'])

def run(args):
    r = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', *args], capture_output=True, text=True)
    assert r.returncode == 0 and not r.stderr, r.stderr

def duration(path):
    r = subprocess.run([FF, '-hide_banner', '-i', str(path)], capture_output=True, text=True)
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    assert m, r.stderr
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])

def event(clip, needle):
    return next(x['at'] for x in clip['stages'] if needle in x['tag'])

codec = ['-vf', 'fps=30', '-fps_mode', 'cfr', '-c:v', 'libx264', '-preset', 'fast', '-crf', '21', '-pix_fmt', 'yuv420p', '-threads', '2', '-af', 'aresample=async=1:first_pts=0', '-c:a', 'aac', '-b:a', '160k']
for clip in q['clips']:
    print('Encoding ' + clip['part'], flush=True)
    run(['-i', str(OUT / 'films' / (clip['part'] + '.webm')), *codec, str(ENC / (clip['part'] + '.mp4'))])
off = duration(ENC / 'chronos.mp4')
total = off + duration(ENC / 'hq5.mp4')
chapters = [
    {'start': 0, 'title': 'Chronos - native final destruction'},
    {'start': event(a, ':lock:'), 'title': 'Core lock and final missile'},
    {'start': event(a, ':burst:'), 'title': 'Armor breakup'},
    {'start': event(a, 'earth-return:space-departure'), 'title': 'Space departure - no Earth yet'},
    {'start': event(a, 'earth-return:earth-reveal'), 'title': 'Earth reveal, stop and descent'},
    {'start': off, 'title': 'Top-down Fury HQ landing'},
    {'start': off + event(b, ':HQ19-EXIT:'), 'title': 'Disembarking and entering the base'},
    {'start': off + event(b, ':HQ19-CORRIDOR:'), 'title': 'Walking through Fury HQ'},
    {'start': off + event(b, ':HQ19-WELCOME:'), 'title': 'Crew homecoming'},
    {'start': off + event(b, ':HQ19-RADAR:'), 'title': 'Sixteen-frame radar alarm'},
    {'start': off + event(b, ':HQ19-LAUNCH:'), 'title': 'One-at-a-time southwest and southeast launch'},
    {'start': off + event(b, ':HQ19-QUIET:'), 'title': 'Five quiet seconds'},
    {'start': off + event(b, ':HQ19-ATTACK:'), 'title': 'Enemies attack Fury HQ'},
    {'start': off + event(b, ':HQ19-DECKER:'), 'title': 'Decker and Axel counterattack, then escape'},
    {'start': off + event(b, 'intro:'), 'title': 'Stage 6 - card and flight in'},
    {'start': off + event(b, ':cloak:1'), 'title': 'Stage 6 - regroup and ambush'},
]
meta = ';FFMETADATA1\ntitle=Bullets of Fury - Revised Stage 5 to 6 HQ evacuation\n'
for i, ch in enumerate(chapters):
    end = chapters[i + 1]['start'] if i + 1 < len(chapters) else total
    meta += '[CHAPTER]\nTIMEBASE=1/1000\nSTART=' + str(round(ch['start'] * 1000)) + '\nEND=' + str(round(end * 1000)) + '\ntitle=' + ch['title'] + '\n'
(OUT / 'chapters.ffmeta').write_text(meta, encoding='utf8')
(ENC / 'concat.txt').write_text("file 'chronos.mp4'\nfile 'hq5.mp4'\n", encoding='utf8')
movie = OUT / 'stage5-to-6-hq-animation.mp4'
run(['-f', 'concat', '-safe', '0', '-i', str(ENC / 'concat.txt'), '-f', 'ffmetadata', '-i', str(OUT / 'chapters.ffmeta'), '-map', '0:v:0', '-map', '0:a:0', '-map_metadata', '1', '-map_chapters', '1', '-c', 'copy', '-movflags', '+faststart', str(movie)])
run(['-i', str(movie), '-f', 'null', '-'])
v = subprocess.run([FF, '-hide_banner', '-i', str(movie), '-af', 'volumedetect', '-vn', '-f', 'null', '-'], capture_output=True, text=True)
audio = [x.strip() for x in v.stderr.splitlines() if 'mean_volume:' in x or 'max_volume:' in x]
assert len(audio) == 2 and not any('-inf' in x for x in audio), audio
points = [
    (event(a, 'earth-return:earth-descent') + 3.0, 'Earth descent'),
    (off + 3.0, 'Top-down HQ landing'),
    (off + event(b, ':HQ19-ENTER:') + 3.5, 'Walking through open doors'),
    (off + event(b, ':HQ19-CORRIDOR:') + 3.0, 'HQ corridor'),
    (off + event(b, ':HQ19-WELCOME:') + 3.0, 'Crew homecoming'),
    (off + event(b, ':HQ19-RADAR:') + 4.0, 'Animated radar alarm'),
    (off + event(b, ':HQ19-LAUNCH:') + 3.2, 'Alternating diagonal launch'),
    (off + event(b, ':HQ19-DECKER:') + 4.3, 'Decker and Axel fight back'),
]
contact = Image.new('RGB', (1440, 882), '#0b1420')
d = ImageDraw.Draw(contact)
for i, (t, label) in enumerate(points):
    f = OUT / ('frame-' + str(i) + '.png')
    run(['-ss', str(t), '-i', str(movie), '-frames:v', '1', str(f)])
    im = Image.open(f).convert('RGB')
    im.thumbnail((480, 270))
    x, y = i % 3 * 480, i // 3 * 294
    contact.paste(im, (x + (480 - im.width) // 2, y))
    d.text((x + 8, y + 272), label, fill='#eee4c7')
contact.save(OUT / 'contact-sheet.jpg', quality=94)
q['combined'] = {'file': movie.name, 'duration': duration(movie), 'chapters': chapters, 'sha256': hashlib.sha256(movie.read_bytes()).hexdigest(), 'decodeErrors': [], 'audio': audio}
(OUT / 'recording.json').write_text(json.dumps(q, indent=2), encoding='utf8')
buttons = ''.join('<button data-time="' + str(ch['start']) + '">' + ch['title'] + '</button>' for ch in chapters)
html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF - Stage 5 to 6 HQ evacuation</title><style>body{max-width:1200px;margin:30px auto;padding:0 20px;background:#09131f;color:#f1e8ce;font:17px/1.55 system-ui}p{color:#b7c8db}video,img{width:100%;background:#02060b;border:1px solid #405c73;border-radius:7px}button{padding:9px 13px;margin:4px;background:#20374b;color:#f4eacb;border:1px solid #52778f;border-radius:5px;font:inherit;cursor:pointer}a{color:#72ddce}small{color:#9fb4ca}</style><h1>Stage 5 to 6 - homecoming and evacuation</h1><p>Native Chronos destruction; delayed Earth reveal and descent; a top-down HQ landing, disembarkation and walk inside; the crew reunion and animated radar alarm; alternating southwest/southeast individual launch, five quiet seconds, and Decker/Axel shooting down six attackers before escaping.</p><video id="movie" controls preload="metadata" src="stage5-to-6-hq-animation.mp4" poster="frame-4.png"></video><p>__BUTTONS__</p><p><small>Cole / Hard, with native game audio. No cinematic dialogue skipped. The result/equipment menus between two cinematic checkpoints are omitted; HQ through Stage 6 is one continuous native capture. Ends at the first interactive missile interception in Stage 6. This is not a campaign playthrough. Normal retains its existing Stage 5 completion branch.</small></p><p><a download href="stage5-to-6-hq-animation.mp4">Download recording</a> · <a href="../../docs/HQ_ANIMATION_1115.md">Implementation and recording notes</a></p><img src="contact-sheet.jpg" alt="Recorded frames from Earth descent to the final HQ escape"><script>const v=document.getElementById('movie');document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(OUT / 'review.html').write_text(html.replace('__BUTTONS__', buttons), encoding='utf8')
print(json.dumps(q['combined'], indent=2), flush=True)

# Provide the authored loops beside the native cinematic for direct motion review.
pilots=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']
loops='<details><summary>New pilot walk / celebration loops and sliding doors</summary><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px">'+''.join('<figure style="margin:0"><figcaption>'+p.title()+'</figcaption><img loading="lazy" style="width:49%" src="'+p+'-walk.gif" alt="'+p+' eight-frame walk"><img loading="lazy" style="width:49%" src="'+p+'-cheer.gif" alt="'+p+' eight-frame celebration"></figure>'for p in pilots)+'</div><img loading="lazy" src="door-opening.gif" alt="Sixteen-frame physical HQ door opening and closing"></details>'
page=OUT/'review.html'
page.write_text(page.read_text(encoding='utf8').replace('<img src="contact-sheet.jpg"',loops+'<img src="contact-sheet.jpg"'),encoding='utf8')
