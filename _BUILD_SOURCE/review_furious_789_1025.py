"""Build/serve the local Stage 7–9 recording review, with byte-range video seeking."""
from pathlib import Path
import argparse
import functools
import http.server
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots' / 'furious_789_1025'

PAGE = r'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:,">
<title>Furious · Stages 7 / 8 / 9</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#0a0e15;color:#dfe7f2;font:15px system-ui,sans-serif}
main{max-width:1500px;margin:auto;padding:24px}h1{font-size:25px;margin:0 0 7px}p{color:#9aabc1;line-height:1.5;margin:0 0 18px}
nav,.controls{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}button,a.link{background:#182436;border:1px solid #33445d;color:#e1eaf8;border-radius:5px;padding:9px 13px;cursor:pointer;font:inherit;text-decoration:none}
button:hover,button.active{border-color:#72dbdd;color:#90f0e7}section{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:20px}
video{display:block;width:100%;background:#000;max-height:76vh}aside{background:#111a27;padding:16px;border:1px solid #25334a;border-radius:6px;overflow:auto;max-height:88vh}
h2{font-size:17px;margin:0 0 12px}h3{font-size:14px;margin:22px 0 10px;color:#aac3df}small{color:#92a5be}#chapters button{display:block;text-align:left;width:100%;margin:5px 0;padding:7px;font-size:13px}
textarea{width:100%;height:88px;background:#090f19;border:1px solid #3b4b61;color:#eef3ff;padding:10px;font:inherit;border-radius:4px}
.note{margin-top:8px;padding:9px;background:#182436;border-radius:4px;white-space:pre-wrap}.note a{color:#90f0e7;cursor:pointer}#status{padding:10px 0;color:#d6bf7c}#clock{min-width:120px;align-self:center;font-variant-numeric:tabular-nums}
@media(max-width:950px){section{grid-template-columns:1fr}aside{max-height:none}main{padding:14px}}
</style><main>
<h1>Furious boss review · Stages 7, 8 &amp; 9</h1>
<p>Current local build · Cole · native boss mode · real-time capture with music and SFX.<br>
Player invulnerability and input aiming are enabled. Enemy health, attacks, transitions and defeat use the game’s own rules.</p>
<nav id="tabs"></nav><section><div>
<video id="video" controls preload="metadata"></video>
<div class="controls">
<button id="backframe">−1 frame</button><button id="forwardframe">+1 frame</button>
<button id="back">−5 sec</button><button id="forward">+5 sec</button>
<button data-rate="0.25">¼×</button><button data-rate="0.5">½×</button><button data-rate="1">1×</button>
<span id="clock">00:00 / 00:00</span><a id="download" class="link" download>Save MP4</a>
</div><small>Pause before stepping. Encoded video is 30 fps; source game frame rate can vary. Arrow keys seek; Shift + arrow steps one encoded frame.</small>
<div id="status"></div></div>
<aside><h2 id="title">Loading recordings…</h2><div id="details"></div>
<h3>Review markers</h3><textarea id="text" placeholder="Describe what you see at this timestamp…"></textarea>
<div class="controls"><button id="mark">Add marker</button><button id="export">Export notes</button></div><div id="notes"></div>
<h3>Timestamped findings</h3><div id="findings"></div>
<h3>Native phase changes</h3><div id="chapters"></div></aside></section></main>
<script>
const $=s=>document.querySelector(s),v=$('#video');let clips=[],current=null,findings=[];
const fmt=t=>{t=Math.max(0,Number(t)||0);return Math.floor(t/60).toString().padStart(2,'0')+':'+Math.floor(t%60).toString().padStart(2,'0')};
let notes=JSON.parse(localStorage.getItem('bof-furious-789-notes-1025')||'[]');
function save(){localStorage.setItem('bof-furious-789-notes-1025',JSON.stringify(notes));renderNotes()}
function renderNotes(){const box=$('#notes');box.replaceChildren();for(const n of notes.filter(n=>n.stage===current?.stage)){
 const row=document.createElement('div');row.className='note';const a=document.createElement('a');a.textContent=fmt(n.seconds)+' ';a.onclick=()=>{v.currentTime=n.seconds;v.pause()};row.append(a,document.createTextNode(n.text));box.append(row)}}
function renderFindings(){const box=$('#findings');box.replaceChildren();for(const n of findings.filter(n=>n.stage===current?.stage)){const row=document.createElement('div');row.className='note';const a=document.createElement('a');a.textContent=fmt(n.start)+' · '+n.priority+' · '+n.category;a.onclick=()=>{v.currentTime=n.start;v.pause()};row.append(a,document.createElement('br'),document.createTextNode(n.finding));const status=document.createElement('small');status.textContent=n.status;row.append(document.createElement('br'),status);box.append(row)}}
function select(c){current=c;v.src=c.video;$('#download').href=c.video;$('#title').textContent='Stage '+c.stage+' · '+c.name;
 $('#details').textContent=c.completed?'Complete native defeat · '+fmt(c.duration):'Recorded encounter · '+fmt(c.duration)+' · '+c.reason;
 $('#status').textContent=(c.pageErrors||c.consoleErrors?'Runtime errors recorded — inspect report.':'No page or console errors recorded.')+' Audio independently checked during delivery.';
 document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('active',Number(b.dataset.stage)===c.stage));
 $('#chapters').replaceChildren();let last='',at=-100;for(const q of c.chapters){
 const label=q.label||[q.phase,q.form,q.mode].filter(x=>x!==null&&x!==undefined&&x!=='').join(' / ');
 if(!label||label===last||q.seconds-at<2)continue;last=label;at=q.seconds;
 const b=document.createElement('button');b.textContent=fmt(q.seconds)+' · '+label;b.onclick=()=>{v.currentTime=Math.max(0,q.seconds-.5);v.pause()};$('#chapters').append(b)}renderNotes();renderFindings()}
Promise.all([fetch('recordings.json').then(r=>r.json()),fetch('findings.json').then(r=>r.json()).catch(()=>({issues:[]}))]).then(([data,review])=>{clips=data.clips;findings=review.issues;for(const c of clips){const b=document.createElement('button');b.dataset.stage=c.stage;b.textContent='Stage '+c.stage+' · '+c.name;b.onclick=()=>select(c);$('#tabs').append(b)}if(clips.length){const params=new URLSearchParams(location.search);select(clips.find(c=>c.stage===Number(params.get('stage')))||clips[0]);if(params.has('t'))v.addEventListener('loadedmetadata',()=>{v.currentTime=Number(params.get('t'));v.pause()},{once:true})}else $('#title').textContent='Recording in progress'});
function seek(s,frame=false){if(frame)v.pause();v.currentTime=Math.max(0,Math.min(v.duration||1e9,v.currentTime+s))}
$('#backframe').onclick=()=>seek(-1/30,true);$('#forwardframe').onclick=()=>seek(1/30,true);$('#back').onclick=()=>seek(-5);$('#forward').onclick=()=>seek(5);
document.querySelectorAll('[data-rate]').forEach(b=>b.onclick=()=>{v.playbackRate=Number(b.dataset.rate);document.querySelectorAll('[data-rate]').forEach(x=>x.classList.toggle('active',x===b))});
v.ontimeupdate=v.onloadedmetadata=()=>{$('#clock').textContent=fmt(v.currentTime)+' / '+fmt(v.duration)};
$('#mark').onclick=()=>{const text=$('#text').value.trim();if(!text||!current)return;notes.push({stage:current.stage,seconds:+v.currentTime.toFixed(3),text,created:new Date().toISOString()});$('#text').value='';save()};
$('#export').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify({recordings:clips.map(c=>({stage:c.stage,video:c.video})),notes},null,2)],{type:'application/json'}));a.download='furious-stage7-8-9-notes.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};
document.addEventListener('keydown',e=>{if(/TEXTAREA|INPUT/.test(e.target.tagName))return;if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();seek((e.key==='ArrowLeft'?-1:1)*(e.shiftKey?1/30:1),e.shiftKey)}});
</script></html>'''


def build():
    names = {7: 'Toxic Portal Warden', 8: 'Dracodia', 9: 'Warp Sentinels / Tidal Fusion'}
    clips = []
    for stage in (7, 8, 9):
        candidates = [p for p in OUT.glob(f'stage{stage}*/report.json')
                      if (p.parent / f'stage{stage}-furious.mp4').exists()
                      and (p.parent / 'verification.json').exists()
                      and json.loads((p.parent / 'verification.json').read_text())['checks']['fullDecode']]
        if not candidates:
            continue
        path = max(candidates, key=lambda p: p.stat().st_mtime)
        report = json.loads(path.read_text(encoding='utf8'))
        timeline = report.get('timeline', [])
        clips.append(dict(stage=stage, name=names[stage], video=f'{path.parent.name}/stage{stage}-furious.mp4',
                          completed=report['completed'], reason=report['reason'],
                          duration=timeline[-1]['seconds'] if timeline else 0,
                          pageErrors=len(report.get('pageErrors', [])), consoleErrors=len(report.get('consoleErrors', [])),
                          chapters=[chapter(stage, q) for q in timeline]))
    OUT.mkdir(exist_ok=True, parents=True)
    (OUT / 'index.html').write_text(PAGE, encoding='utf8')
    (OUT / 'recordings.json').write_text(json.dumps({'clips': clips}, indent=2), encoding='utf8')
    print(json.dumps({'gallery': str(OUT / 'index.html'), 'clips': len(clips)}), flush=True)


def chapter(stage, q):
    data = {k: q.get(k) for k in ['seconds', 'phase', 'form', 'mode']}
    if stage == 8:
        if q.get('phase') == 0:
            name = 'Infused orbital host'
        elif q.get('phase') == 1:
            name = 'Rebirth'
        elif q.get('phase') == 2:
            name = {0: 'Dracodia', 8: 'Hammer copy', 1: 'Helicopter copy',
                    6: 'Neural Archon copy', 2: 'Volcano / Phoenix copy'}.get(q.get('form'), 'Final arena')
        else:
            name = 'Approach'
        data['label'] = name + ' / ' + (q.get('mode') or 'entrance')
    return data


class RangeHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send_head(self):
        path = Path(self.translate_path(self.path))
        header = self.headers.get('Range')
        if not header or not path.is_file():
            return super().send_head()
        match = re.fullmatch(r'bytes=(\d+)-(\d*)', header)
        if not match:
            self.send_error(416)
            return None
        size = path.stat().st_size
        start = int(match[1])
        end = min(int(match[2]) if match[2] else size - 1, size - 1)
        if start > end:
            self.send_error(416)
            return None
        stream = path.open('rb')
        stream.seek(start)
        self.range_remaining = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self.range_remaining))
        self.end_headers()
        return stream

    def copyfile(self, source, outputfile):
        remaining = getattr(self, 'range_remaining', None)
        try:
            if remaining is None:
                return super().copyfile(source, outputfile)
            while remaining:
                chunk = source.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    build()
    if args.serve:
        server = http.server.ThreadingHTTPServer(('127.0.0.1', args.port), functools.partial(RangeHandler, directory=str(OUT)))
        actual_port = server.server_address[1]
        (OUT / 'review-server.json').write_text(json.dumps({'port': actual_port, 'url': f'http://127.0.0.1:{actual_port}/index.html'}), encoding='utf8')
        print(f'REVIEW http://127.0.0.1:{actual_port}/index.html', flush=True)
        server.serve_forever()
