from pathlib import Path
from publish_bullethell_1025 import RangeHandler
import json,http.server,argparse
from functools import partial

R=Path(__file__).resolve().parents[1];O=R/'docs/previews/barrage_revision_1025'
def latest(key):
 records=[]
 for f in(R/'_shots/barrage_revision_1025/video').glob(key+'-*/report.json'):
  q=json.loads(f.read_text(encoding='utf8'))
  if all(q['checks'].values()):records.append((f,q))
 if not records:raise RuntimeError('No verified current film: '+key)
 return max(records,key=lambda v:v[0].stat().st_mtime)
def wall(q,native):
 timeline=q['timeline'];before={'seconds':0,'nativeTime':q['initial']['nativeTime']}
 for at in timeline:
  if at['nativeTime']>=native:
   u=(native-before['nativeTime'])/max(.00001,at['nativeTime']-before['nativeTime']);return max(0,before['seconds']+u*(at['seconds']-before['seconds']))
  before=at
 return timeline[-1]['seconds']
def publish():
 items=[]
 names={
  'frost':('Stage3 · Frost Cruiser','Darker ice scenery','The ice canyon is dimmed behind combat. Ice shots, warnings, aircraft and the HUD keep their brightness.'),
  'battery':('Stage6 · Siege Fortress','Native battery attacks','The six batteries use their native laser patterns. Added bullet hell is reserved for the exposed core.'),
  'reactor':('Stage6 · Exposed reactor','Core barrage','All six batteries have broken through native damage. The reactor emits the barrage from its visible aperture.'),
  'turrets':('Stage7 · Caustic Dredger','Turret barrage','Fans leave measured barrel mouths, with attached toxic muzzle flashes. Each gun cycles its four authored barrels.'),
  'dorsal':('Stage7 · Caustic Dredger','Top sludge splash','Sludge launches from the top liquid opening, arcs to warned impact points and splashes into outward shots.'),
  'herald':('Stage8 · Herald of Death','Red chaos barrage','Round animated red energy leaves the surviving claws with energy muzzle flashes.')}
 for key,(name,title,description)in names.items():
  f,q=latest(key);events=[e for e in q['events']['barrage']if e['time']>=q['initial']['nativeTime']-.1]
  first=next((wall(q,e['time'])for e in events if e['event']in['wave-release','dorsal-release']),1.2)
  recovery=next((wall(q,e['time'])for e in events if e['event']=='section-recovery'),min(10,q['timeline'][-1]['seconds']-1))
  item={'id':key,'name':name,'title':title,'description':description,'src':'/'+q['video'],'poster':'/'+(f.parent/'decoded-3.png').relative_to(R).as_posix(),
   'warning':.1,'attack':first+.08,'peak':first+2.2,'recovery':recovery+.1,'seconds':q['timeline'][-1]['seconds'],'peakDb':q['decodedPeakDb'],
   'maxLive':max(t['live']for t in q['timeline']),'method':'Furious. Real-time native checkpoint with an invulnerable movement bot. Enemy HP and phases are untouched; Stage6 companions fight normally.'}
  items.append(item)
  if key=='herald':
   for kind,title,description in [('swoop','Phoenix-style corner flights','Warned diagonal talon passes change heading and depth, animate the existing wings, then visibly return to combat.'),('bomber','Fast claw bomber runs','Two drive-by passes match the corner-flight speed. Both claws rapidly drop red chaos with energy flashes; the whole carpet is warned before the pass and keeps an escape opening.')]:
    es=q['events']['herald'];tell=next(e for e in es if e['event']=='flight-phase'and e.get('kind')==kind and e.get('phase')=='tell')
    strike=next(e for e in es if e['event']=='flight-phase'and e.get('kind')==kind and e.get('phase')=='strike')
    done=next(e for e in es if e['event']=='flight-complete'and e.get('kind')==kind)
    start=wall(q,strike['time']);middle=wall(q,strike['time']+strike.get('duration',1.25)*.5)
    burst=next((e for e in es if e['event']=='bomb-burst'and e['time']>strike['time']),None)
    items.append({**item,'id':'herald-'+kind,'title':title,'description':description,'warning':wall(q,tell['time'])+.1,
     'attack':middle if kind=='bomber'else start+.6,'peak':wall(q,burst['time'])+.12 if kind=='bomber'and burst else start+.75,'recovery':wall(q,done['time'])+.1})
 O.mkdir(parents=True,exist_ok=True);(O/'review.json').write_text(json.dumps(items,indent=2),encoding='utf8');(O/'index.html').write_text(HTML,encoding='utf8')
 print(json.dumps({'cards':len(items),'uniqueClips':len(set(i['src']for i in items)),'path':str(O/'index.html')}),flush=True)

HTML='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Bullets of Fury · Revised attack review</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#080e16;color:#e9f3f8}*{box-sizing:border-box}body{margin:0}header{padding:24px 32px;border-bottom:1px solid #254052;background:#101f2c}h1{font-size:28px;margin:5px 0 10px}.eyebrow{font-size:12px;letter-spacing:2px;color:#69e0c3}p{line-height:1.55;color:#b3c8d8;margin:8px 0}a{color:#7cdeed}main{display:grid;grid-template-columns:minmax(640px,1fr) 330px;gap:24px;padding:24px 32px;max-width:1700px;margin:auto}video{width:100%;aspect-ratio:1.6;border:1px solid #2d4a60;border-radius:8px;background:#000}h2{margin:14px 0 7px;font-size:22px}button,select{font:inherit;background:#152b3b;color:#edf8ff;border:1px solid #34576d;border-radius:5px;padding:9px 12px;cursor:pointer}button:hover{border-color:#81e6d3}button:focus-visible{outline:2px solid #85f0da;outline-offset:3px}.toolbar{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}nav{display:grid;align-content:start;gap:8px}.choice{text-align:left;padding:12px}.choice span{display:block;font-size:13px;color:#a9c1d3;margin-top:5px}.choice.active{border-color:#67d7bf;background:#173d37}.meta{display:flex;flex-wrap:wrap;gap:8px;font-size:12px;color:#9eb5c7}.meta span{padding:5px 8px;border:1px solid #28495b;border-radius:4px}.note{font-size:13px}.compare{margin-top:18px;border:1px solid #294a5b;border-radius:6px;padding:12px}.compare h3{margin:0 0 10px;font-size:16px}.compare div{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}figure img{width:100%;display:block}figcaption{font-size:12px;margin-top:6px;color:#b6cbd8}footer{padding:8px 32px 28px;font-size:13px;color:#a8c2d4}@media(max-width:1100px){main{grid-template-columns:1fr;padding:18px}nav{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}header{padding:20px}}
</style><header><div class="eyebrow">BULLETS OF FURY · OCTOBER25 · FURIOUS</div><h1>Revised attack review</h1><p>Darker Stage3 terrain, reactor-only Stage6 bullet hell, connected Dredger launchers and Herald chaos flights.</p></header>
<main><section><video id="v" controls preload="metadata" playsinline></video><h2 id="title"></h2><p id="description"></p><div class="toolbar"><button id="warning">Warning</button><button id="attack">Attack</button><button id="peak">Pattern</button><button id="recovery">Recovery</button><button id="frame">+1 frame</button><select id="speed" aria-label="Playback speed"><option value=".25">¼ speed</option><option value=".5">½ speed</option><option value="1" selected>Normal speed</option></select></div><div id="meta" class="meta"></div><p id="method" class="note"></p><p class="note">The three Herald chapters share one continuous52-second film. The invulnerable bot is for studying attacks; these clips do not establish human difficulty.</p>
<section class="compare" id="compare"><h3>Stage3 scenery comparison · same native frame</h3><div><figure><img src="/_shots/barrage_revision_1025/probe/stage3-before.png" alt="Frost Cruiser against the original brighter ice scenery"><figcaption>Before</figcaption></figure><figure><img src="/_shots/barrage_revision_1025/probe/stage3-after.png" alt="The same Frost Cruiser and warnings against darker scenery"><figcaption>Current · combat brightness retained</figcaption></figure></div></section></section><nav id="list" aria-label="Current attack clips"></nav></main>
<footer><a href="../../BARRAGE_READABILITY_1025.md">Current changes and verification</a> · <a href="../warden_tidal_1025/index.html">Warden walking and Stage9 water review</a> · <a href="../../FURIOUS_789_REVIEW_1025.md">Original timestamped findings</a></footer>
<script>
const v=document.querySelector('#v'),speed=document.querySelector('#speed');let data,selected;
const stamp=t=>Math.floor(t/60)+':'+(t%60).toFixed(1).padStart(4,'0');
function seek(t){v.pause();v.currentTime=Math.min((v.duration||selected.seconds)-.08,Math.max(0,t));}
function choose(id){selected=data.find(x=>x.id===id)||data[0];const q=selected;
 document.querySelector('#title').textContent=q.name+' · '+q.title;document.querySelector('#description').textContent=q.description;document.querySelector('#method').textContent=q.method;
 document.querySelector('#meta').replaceChildren(...[q.seconds.toFixed(1)+' seconds','Attack at '+stamp(q.attack),q.maxLive+' peak active rounds','Decoded audio '+q.peakDb+' dB'].map(s=>{const e=document.createElement('span');e.textContent=s;return e;}));
 document.querySelector('#compare').hidden=q.id!=='frost';document.querySelectorAll('.choice').forEach(b=>{const active=b.dataset.id===q.id;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});history.replaceState(null,'','#'+q.id);
 v.onloadedmetadata=()=>{v.playbackRate=+speed.value;seek(q.attack);};v.src=q.src;v.poster=q.poster;
}
for(const key of ['warning','attack','peak','recovery'])document.querySelector('#'+key).onclick=()=>seek(selected[key]);
document.querySelector('#frame').onclick=()=>seek(v.currentTime+1/30);speed.onchange=()=>{v.playbackRate=+speed.value;};
fetch('review.json').then(r=>r.json()).then(a=>{data=a;for(const q of a){const b=document.createElement('button');b.className='choice';b.dataset.id=q.id;b.type='button';b.append(q.name);const s=document.createElement('span');s.textContent=q.title;b.append(s);b.onclick=()=>choose(q.id);document.querySelector('#list').append(b);}choose(location.hash.slice(1)||'herald-bomber');});
</script></html>'''

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--serve',action='store_true');a=ap.parse_args();publish()
 if a.serve:
  http.server.ThreadingHTTPServer.request_queue_size=128
  server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(RangeHandler,directory=str(R)));server.daemon_threads=True
  print('REVIEW http://127.0.0.1:'+str(server.server_address[1])+'/docs/previews/barrage_revision_1025/index.html',flush=True);server.serve_forever()
