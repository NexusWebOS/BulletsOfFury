from pathlib import Path
import argparse,json,http.server,threading,re

R=Path(__file__).resolve().parents[1];O=R/'docs/previews/bullethell_1025'
NAMES={
 '7-boss':('Stage 7 · Warden','Toxic flowers','Rotating acid rings from the main emitter, with a moving opening.'),
 '8-boss':('Stage 8 · Dracodia, first body','Claw braids','The raised claws alternate committed fans. Broken arms stop firing.'),
 '8-final':('Stage 8 · Dracodia, final body','Code flowers','Rotating code rings before the army download; native form pools remain finite.'),
 '1-mini':('Stage 1 · Razorback','Sonic rake','Offset artillery fans with a moving dodge lane.'),
 '2-mini':('Stage 2 · Inferno Reaver','Cinder flowers','Staggered rotating rings from surviving gun modules.'),
 '3-mini':('Stage 3 · Frost Cruiser','Gun braids','Alternating gun fans with a committed opening.'),
 '4-mini':('Stage 4 · Olive Warden','Gun rakes','Relay fans wait for the escort attack to finish.'),
 '5-mini':('Stage 5 · Eclipse Siege Bomber','Cannon braid','Staggered fans from surviving cannon modules.'),
 '6-mini':('Stage 6 · Warhive Siege Fortress','Battery relay','Electric orb fans travel through the six battery sockets.'),
 '7-mini':('Stage 7 · Caustic Dredger','Toxic braids','Alternating cannon fans with clear openings.'),
 '8-mini':('Stage 8 · Herald of Death','Feather vortex','Rotating feather rings; a destroyed wing loses its volleys.'),
 '9-mini':('Stage 9 · Event Horizon','Eye spiral','Successive eye rings rotate around an open sector.')}
def publish():
 items=[]
 for token,(name,pattern,description)in NAMES.items():
  stage,role=token.split('-');files=[]
  for f in (R/'_shots/bullethell_1025/video').glob('*/report.json'):
   q=json.loads(f.read_text(encoding='utf8'))
   if q['stage']==int(stage)and q['role']==role and all(q['checks'].values()):files.append((f,q))
  if not files:raise RuntimeError('Missing verified final clip '+token)
  f,q=max(files,key=lambda x:x[0].stat().st_mtime);first=q['initial']['nativeTime']
  release=[max(0,e['time']-first)for e in q['events']if e['event']=='wave-release']
  recovery=next((max(0,e['time']-first)for e in q['events']if e['event']=='section-recovery'),7)
  items.append(dict(id=token,name=name,pattern=pattern,description=description,src='/'+q['video'],poster='/'+str((f.parent/'decoded-3.png').relative_to(R)).replace('\\','/'),method=q['method'],seconds=q['timeline'][-1]['seconds'],peakDb=q['decodedPeakDb'],maxLive=max(t['live']for t in q['timeline']),firstRelease=release[0]if release else 1.2,recovery=recovery,checks=q['checks']))
 O.mkdir(parents=True,exist_ok=True);(O/'review.json').write_text(json.dumps(items,indent=2),encoding='utf8')
 (O/'index.html').write_text(HTML,encoding='utf8');print(json.dumps({'clips':len(items),'file':str(O/'index.html')}),flush=True)
 return items

HTML='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><title>Bullets of Fury · Bullet hell review</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#080d13;color:#e6eef6}*{box-sizing:border-box}body{margin:0}header{padding:24px 32px;border-bottom:1px solid #233647;background:#101b26}h1{font-size:28px;margin:5px 0 8px;letter-spacing:-.8px}.eyebrow{font-size:12px;letter-spacing:2px;color:#70e5c2}p{color:#a7bbcc;line-height:1.55;margin:7px 0}a{color:#83ddec}main{display:grid;grid-template-columns:minmax(650px,1fr) 340px;gap:24px;padding:24px 32px;max-width:1700px;margin:auto}video{width:100%;aspect-ratio:1.6;background:#000;border:1px solid #283c4d;border-radius:8px}h2{font-size:21px;margin:12px 0 5px}.toolbar{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}button,select{background:#142332;color:#e6eef6;border:1px solid #324b60;border-radius:5px;padding:9px 12px;font:inherit;cursor:pointer}button:hover{border-color:#73d6cc}button:focus-visible{outline:2px solid #83ddec;outline-offset:3px}.badge{display:inline-block;font-size:12px;padding:4px 8px;margin-right:5px;background:#173b35;color:#8aebc7;border-radius:4px}.note{font-size:13px;max-width:1050px}nav{display:grid;align-content:start;gap:8px}.choice{text-align:left;padding:12px 14px}.choice span{display:block;color:#9cb2c7;font-size:12px;margin-top:4px}.choice.active{border-color:#62dcc4;background:#15352f}.meta{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0}.meta span{font-size:12px;color:#a9becd;border:1px solid #263d4f;padding:5px 8px;border-radius:4px}footer{padding:10px 32px 30px;font-size:13px;color:#8fa5b7}@media(max-width:1100px){main{grid-template-columns:1fr;padding:18px}nav{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}header{padding:20px}}
</style>
<header><div class="eyebrow">BULLETS OF FURY · OCTOBER 25</div><h1>Bullet hell sections</h1><p>Warden, both Dracodia bodies, and all nine campaign minibosses.</p><span class="badge">Furious</span><span class="badge">Native art & weapon sockets</span><span class="badge">12 verified clips</span></header>
<main><section><video id="v" controls preload="metadata" playsinline></video><h2 id="title"></h2><p id="description"></p><div class="toolbar"><button id="warning">Warning</button><button id="release">First volley</button><button id="peak">Pattern</button><button id="recovery">Recovery</button><button id="frame">+1 frame</button><select id="speed" aria-label="Playback speed"><option value=".25">¼ speed</option><option value=".5">½ speed</option><option value="1" selected>Normal speed</option></select></div><div class="meta" id="meta"></div><p class="note" id="method"></p><p class="note">These are invulnerable review clips for studying motion and patterns. The final-body clip selects the native final-form fixture. The other checkpoints are reached by advancing the native loop, with no enemy HP or phase writes. Normal and Hard use fewer, slower waves and longer warnings.</p></section><nav id="list" aria-label="Encounter clips"></nav></main>
<footer><a href="../stage78_review_1025/index.html">Original fight analysis and earlier revisions</a> · <a href="../../FURIOUS_789_REVIEW_1025.md">Timestamped 7/8/9 findings</a> · <a href="../../BULLETHELL_1025.md">Implementation and verification notes</a></footer>
<script>
const v=document.querySelector('#v');let selected,data;
function choose(id){selected=data.find(a=>a.id===id)||data[0];v.src=selected.src;v.poster=selected.poster;document.querySelector('#title').textContent=selected.name+' · '+selected.pattern;document.querySelector('#description').textContent=selected.description;document.querySelector('#method').textContent=selected.method;document.querySelector('#meta').replaceChildren(...[selected.seconds.toFixed(1)+' seconds',selected.maxLive+' peak active rounds','Audio peak '+selected.peakDb+' dB','Native section completed'].map(text=>{let s=document.createElement('span');s.textContent=text;return s;}));document.querySelectorAll('.choice').forEach(b=>{b.classList.toggle('active',b.dataset.id===id);b.setAttribute('aria-pressed',b.dataset.id===id?'true':'false');});history.replaceState(null,'','#'+id);}
function seek(t){v.currentTime=Math.min(v.duration||99,t);v.pause();}
document.querySelector('#warning').onclick=()=>seek(.15);document.querySelector('#release').onclick=()=>seek(selected.firstRelease+.05);document.querySelector('#peak').onclick=()=>seek(selected.firstRelease+2.2);document.querySelector('#recovery').onclick=()=>seek(selected.recovery+.1);document.querySelector('#frame').onclick=()=>{v.pause();v.currentTime=Math.min(v.duration,v.currentTime+1/30);};document.querySelector('#speed').onchange=e=>v.playbackRate=+e.target.value;
fetch('review.json').then(r=>r.json()).then(a=>{data=a;for(const item of a){let b=document.createElement('button');b.type='button';b.className='choice';b.dataset.id=item.id;b.append(item.name);let s=document.createElement('span');s.textContent=item.pattern;b.append(s);b.onclick=()=>choose(item.id);document.querySelector('#list').append(b);}choose(location.hash.slice(1)||'7-boss');});
</script></html>'''

class RangeHandler(http.server.SimpleHTTPRequestHandler):
 protocol_version='HTTP/1.1'
 def log_message(self,*args):pass
 def send_head(self):
  path=Path(self.translate_path(self.path));value=self.headers.get('Range')
  if value and path.is_file():
   m=re.fullmatch(r'bytes=(\d+)-(\d*)',value)
   if m:
    size=path.stat().st_size;start=int(m[1]);end=min(size-1,int(m[2])if m[2]else size-1)
    if start>=size:self.send_error(416);return None
    f=path.open('rb');f.seek(start);self.send_response(206);self.send_header('Content-type',self.guess_type(str(path)));self.send_header('Content-Length',str(end-start+1));self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Accept-Ranges','bytes');self.end_headers();self.remaining=end-start+1;return f
  self.remaining=None;return super().send_head()
 def copyfile(self,source,output):
  try:
   if self.remaining is None:return super().copyfile(source,output)
   while self.remaining:
    b=source.read(min(65536,self.remaining))
    if not b:break
    output.write(b);self.remaining-=len(b)
  except(ConnectionError,OSError):pass

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--serve',action='store_true');p.add_argument('--port',type=int,default=0);a=p.parse_args();publish()
 if a.serve:
  from functools import partial
  server=http.server.ThreadingHTTPServer(('127.0.0.1',a.port),partial(RangeHandler,directory=str(R)));server.daemon_threads=True
  print('REVIEW http://127.0.0.1:'+str(server.server_address[1])+'/docs/previews/bullethell_1025/index.html',flush=True);server.serve_forever()
