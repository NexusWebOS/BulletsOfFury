"""Review the new native recordings without copying media out of _shots/."""
from pathlib import Path
from functools import partial
from publish_bullethell_1025 import RangeHandler
import argparse,json,http.server,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/warden_tidal_1025'
NAMES={'flood':('Tidal flood walls','Three moving water fronts leave a broad opening. Every next front warns its new opening.'),
 'geysers':('Water geysers','Committed floor marks erupt into tall water spires; side space stays open.'),
 'mortars':('Circle-launched laser mortars','The two large water circles launch arcing energy. Impact marks erupt into water laser spires.'),
 'mist':('Turret mist lasers','The lower cannon tips alternate charged pressure beams with water mist.'),
 'undertow':('Cutter waves and torpedoes','Water crescents spread from the circles while physical torpedoes leave the lower cannons.'),
 'maelstrom':('Maelstrom bullet hell','Alternating circles release rotating bubble rings around a committed escape sector.')}
def clock(t):return f'{int(t)//60:02}:{int(t)%60:02}'
def publish():
 reports=[]
 for f in (R/'_shots/warden_tidal_1025/full').glob('*/report.json'):
  q=json.loads(f.read_text(encoding='utf8'));v=f.parent/'verification.json'
  if q.get('completed')and v.exists():
   check=json.loads(v.read_text(encoding='utf8'))
   if all(check['checks'].values()):reports.append((f,q,check))
 if not reports:raise RuntimeError('No verified final Stage9 recording')
 f,q,verified=max(reports,key=lambda a:a[0].stat().st_mtime);video=f.parent/'stage9-furious.mp4';timeline=q['timeline']
 walk=R/json.loads((R/'_shots/warden_tidal_1025/walk/latest.json').read_text(encoding='utf8'))['folder'];w=json.loads((walk/'report.json').read_text(encoding='utf8'))
 if not all(w['checks'].values()):raise RuntimeError('Warden walk recording failed validation')
 def mode_at(mode):
  for i,t in enumerate(w['timeline']):
   if t['mode']==mode:return (t['seconds']+(w['timeline'][i-1]['seconds']if i else 0))*.5
  raise RuntimeError('Missing native Warden mode '+mode)
 swipe=min(mode_at(m)for m in w['modes']if m.startswith('swipe'));battery=mode_at('battery1009');recover=mode_at('recover')
 items=[{'id':'warden','name':'Stage 7 · Connected spider walking','description':'Retreat scroll drives the gait; the gun mounts stay fixed, and both live claws remain visible through their attack and return.',
  'src':'/'+w['video'],'poster':'/'+str((walk/'decoded-2.png').relative_to(R)).replace('\\','/'),'start':0,'end':w['timeline'][-1]['seconds'],'firstRelease':swipe+1.18,'peak':battery+1.85,'recovery':recover+.12,'method':w['method'],'peakDb':w['decodedPeakDb']}]
 events=[];seen=set()
 for s in timeline:
  for e in (s.get('water')or{}).get('events',[]):
   identity=(e['event'],e['time'],e['kind'])
   if identity not in seen:seen.add(identity);events.append(e)
 events.sort(key=lambda e:e['time'])
 def actual(t):
  samples=[s for s in timeline if s.get('water')and s['water']['clock']>=t]
  if not samples:return timeline[-1]['seconds']
  z=samples[0];prev=next((s for s in reversed(timeline[:timeline.index(z)])if s.get('water')),None)
  if prev and z['water']['clock']>prev['water']['clock']:
   a=(t-prev['water']['clock'])/(z['water']['clock']-prev['water']['clock']);return prev['seconds']+(z['seconds']-prev['seconds'])*a
  return z['seconds']
 water_starts={k:next(e for e in events if e['event']=='water-attack-start'and e['kind']==k)for k in NAMES}
 src='/'+str(video.relative_to(R)).replace('\\','/')
 first=actual(water_starts['flood']['time'])
 items.append({'id':'stage9-full','name':'Stage 9 · Complete Furious fight','description':'Native sentinel fight, convergence, all six water attacks, then native Tidal defeat. The bot withholds fire for one water rotation so every attack is visible.',
  'src':src,'poster':'/'+str((video.parent/'decoded-02.png').relative_to(R)).replace('\\','/'),'start':0,'end':verified['duration'],'firstRelease':first+1.3,'peak':first+4.35,'recovery':q['defeatSeconds'],'method':q['method'],'peakDb':verified['decodedPeakDb']})
 for kind,(name,description)in NAMES.items():
  start=actual(water_starts[kind]['time']);complete=next(e for e in events if e['event']=='water-attack-complete'and e['kind']==kind);end=actual(complete['time'])+.75
  poster=video.parent/('chapter-'+kind+'.png')
  subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-threads','2','-ss',str(min(end-.2,start+2.6)),'-i',str(video),'-frames:v','1',str(poster)],check=True)
  peak={'flood':4.35,'geysers':2.05,'mortars':3.30,'mist':2.25,'undertow':2.75,'maelstrom':3.10}[kind]
  items.append({'id':kind,'name':'Stage 9 · '+name,'description':description+' Full-fight timestamp '+clock(start)+'.','src':src,'poster':'/'+str(poster.relative_to(R)).replace('\\','/'),'start':start,'end':end,'firstRelease':start+(1.35 if kind=='geysers'else 1.12 if kind=='mortars'else 1.25),'peak':start+peak,'recovery':end-.75,'method':q['method'],'peakDb':verified['decodedPeakDb']})
 O.mkdir(parents=True,exist_ok=True);(O/'review.json').write_text(json.dumps(items,indent=2),encoding='utf8');(O/'index.html').write_text(HTML,encoding='utf8')
 print(json.dumps({'items':len(items),'file':str(O/'index.html'),'chapters':{a['id']:clock(a['start'])for a in items}}),flush=True);return items
HTML='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Warden & Tidal Sovereign · October 25</title>
<style>*{box-sizing:border-box}body{margin:0;background:#08101c;color:#eaf1fa;font:15px/1.5 system-ui,sans-serif}header,main,footer{max-width:1450px;margin:auto;padding:22px 28px}header{padding-bottom:10px}h1{font-size:29px;margin:0 0 6px;color:#8fefff}p{margin:7px 0}header p,footer,#method{color:#a9b9ce}main{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:22px}section{min-width:0}video{display:block;width:100%;background:#03070e;border:1px solid #29455e;border-radius:8px;aspect-ratio:8/5}h2{font-size:20px;margin:14px 0 3px}button,select{background:#102337;border:1px solid #35566e;border-radius:5px;color:#e6f3ff;padding:9px 11px;font:inherit;cursor:pointer}button:hover,button:focus-visible{border-color:#8fefff}button.active{background:#17445a;border-color:#7eebed}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}nav{display:flex;flex-direction:column;gap:9px}.choice{text-align:left;font-weight:650}.choice span{display:block;font-size:12px;color:#a9c1d5;font-weight:400}#meta{display:flex;flex-wrap:wrap;gap:14px;color:#80d8df;font-size:13px}a{color:#8fefff}#method{font-size:13px;white-space:pre-line}footer{padding-top:5px;font-size:13px}@media(max-width:1000px){main{grid-template-columns:1fr}nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}header,main,footer{padding:16px}}</style>
<header><h1>Warden & Tidal Sovereign</h1><p>October 25 · Connected walking, fixed turret mounts, living water and six water attack turns.</p></header>
<main><section><video id="v" controls playsinline preload="metadata"></video><div class="controls"><button id="warning">Warning</button><button id="release">Attack</button><button id="peak">Later</button><button id="recovery">Recovery</button><button id="frame">+1 frame</button><label>Speed <select id="speed"><option value=".25">0.25×</option><option value=".5">0.5×</option><option value="1" selected>1×</option></select></label></div><h2 id="title"></h2><p id="description"></p><p id="meta"></p><p id="method"></p></section><nav id="list" aria-label="New fight recordings"></nav></main>
<footer>Native Chromium footage with an invulnerable input bot. Human difficulty still needs play review. <a href="../../WARDEN_TIDAL_1025.md">Changes and checks</a> · <a href="../stage78_review_1025/index.html">Earlier Stage 7/8 review</a> · <a href="../bullethell_1025/index.html">Miniboss and Dracodia barrages</a> · <a href="../../FURIOUS_789_REVIEW_1025.md">Timestamped original 7/8/9 findings</a></footer>
<script>let data,selected;const v=document.querySelector('#v');const stamp=t=>Math.floor(t/60).toString().padStart(2,'0')+':'+Math.floor(t%60).toString().padStart(2,'0');
function choose(id){selected=data.find(a=>a.id===id)||data[0];v.onloadedmetadata=()=>{v.currentTime=selected.start;v.playbackRate=+document.querySelector('#speed').value;v.pause()};v.src=selected.src;v.poster=selected.poster;document.querySelector('#title').textContent=selected.name;document.querySelector('#description').textContent=selected.description;document.querySelector('#method').textContent=selected.method;document.querySelector('#meta').textContent=stamp(selected.start)+'–'+stamp(selected.end)+' · Audio peak '+selected.peakDb+' dB · Native HP and phases';for(const b of document.querySelectorAll('.choice')){const on=b.dataset.id===selected.id;b.classList.toggle('active',on);b.setAttribute('aria-pressed',on)}history.replaceState(null,'','#'+selected.id)}
function seek(t){v.pause();v.currentTime=Math.min(selected.end,Math.max(selected.start,t))}v.ontimeupdate=()=>{if(selected&&v.currentTime>=selected.end){v.pause()}};
document.querySelector('#warning').onclick=()=>seek(selected.start+.15);document.querySelector('#release').onclick=()=>seek(selected.firstRelease+.04);document.querySelector('#peak').onclick=()=>seek(Math.min(selected.end-.4,selected.peak??selected.firstRelease+2.3));document.querySelector('#recovery').onclick=()=>seek(selected.recovery);document.querySelector('#frame').onclick=()=>seek(v.currentTime+1/30);document.querySelector('#speed').onchange=e=>v.playbackRate=+e.target.value;
fetch('review.json').then(r=>r.json()).then(a=>{data=a;for(const item of a){const b=document.createElement('button');b.type='button';b.className='choice';b.dataset.id=item.id;b.append(item.name);const s=document.createElement('span');s.textContent=stamp(item.start)+'–'+stamp(item.end);b.append(s);b.onclick=()=>choose(item.id);document.querySelector('#list').append(b)}choose(location.hash.slice(1)||'warden')});</script></html>'''
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--serve',action='store_true');p.add_argument('--port',type=int,default=0);a=p.parse_args();publish()
 if a.serve:
  server=http.server.ThreadingHTTPServer(('127.0.0.1',a.port),partial(RangeHandler,directory=str(R)));server.daemon_threads=True
  print('REVIEW http://127.0.0.1:'+str(server.server_address[1])+'/docs/previews/warden_tidal_1025/index.html',flush=True);server.serve_forever()
