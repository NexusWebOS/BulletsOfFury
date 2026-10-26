from pathlib import Path
import json

R=Path(__file__).resolve().parents[1];O=R/'docs/previews/horizon_assault_1025'
def wall(q,native):
 before={'nativeTime':q['initial']['time'],'seconds':0}
 for at in q['timeline']:
  if at['nativeTime']>=native:
   u=(native-before['nativeTime'])/max(.00001,at['nativeTime']-before['nativeTime']);return max(0,before['seconds']+u*(at['seconds']-before['seconds']))
  before=at
 return q['timeline'][-1]['seconds']
def publish():
 info=json.loads((R/'_shots/horizon_assault_1025/video/latest.json').read_text());folder=Path(info['folder']);q=json.loads((folder/'report.json').read_text())
 assert all(q['checks'].values()),q['checks']
 events=q['events'];charge=next(e for e in events if e['event']=='bomb-charge');release=next(e for e in events if e['event']=='bomb-release');impact=next(e for e in events if e['event']=='bomb-impact')
 spin=next(t for t in q['timeline']if t.get('barrage')=='horizon'and t['spinning'])['seconds']+.25
 low=max((t for t in q['timeline']if 2<t['seconds']<wall(q,charge['time'])),key=lambda t:t['y'])['seconds']
 data={'src':'/'+q['video'],'poster':'/'+(folder/'decoded-4.png').relative_to(R).as_posix(),'seconds':q['timeline'][-1]['seconds'],'peakDb':q['decodedPeakDb'],
  'chapters':{'spin':spin,'vertical':low,'charge':wall(q,charge['time'])+1.18,'launch':wall(q,release['time'])+.16,'impact':wall(q,impact['time'])+.07},'method':q['method']}
 O.mkdir(parents=True,exist_ok=True);(O/'review.json').write_text(json.dumps(data,indent=2),encoding='utf8');(O/'index.html').write_text(HTML,encoding='utf8')
 # The user's existing #9-mini tab also receives the corrected continuous film.
 old=R/'docs/previews/bullethell_1025/review.json';rows=json.loads(old.read_text())
 for row in rows:
  if row['id']=='9-mini':row.update(src=data['src'],poster=data['poster'],seconds=data['seconds'],peakDb=data['peakDb'],maxLive=None,pattern='Fast spin, vertical flight and eye bomb',description='Current October25 revision: faster whole-hull spins, large vertical passes and a charged energy bomb from the eye.',method=q['method'],firstRelease=data['chapters']['launch'],recovery=data['chapters']['impact']+.7)
 old.write_text(json.dumps(rows,indent=2),encoding='utf8')
 oldhtml=R/'docs/previews/bullethell_1025/index.html';html=oldhtml.read_text(encoding='utf8');term="selected.maxLive+' peak active rounds'"
 if term in html and 'Continuous native take'not in html:oldhtml.write_text(html.replace(term,"(selected.maxLive==null?'Continuous native take':selected.maxLive+' peak active rounds')"),encoding='utf8')
 print(json.dumps(data),flush=True)

HTML='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Event Horizon · Furious review</title>
<style>:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#080e18;color:#e7f4ff}*{box-sizing:border-box}body{margin:0}header{padding:24px 30px;background:#112331;border-bottom:1px solid #2c5064}.eyebrow{letter-spacing:2px;font-size:12px;color:#6be4dd}h1{font-size:28px;margin:8px 0}p{color:#b1c8d8;line-height:1.55;margin:8px 0}main{max-width:1300px;padding:24px 30px;margin:auto}video{display:block;width:100%;aspect-ratio:1.6;background:#000;border:1px solid #315267;border-radius:8px}.toolbar{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}button,select{font:inherit;background:#173142;color:#e4f7ff;border:1px solid #396479;border-radius:5px;padding:10px 14px;cursor:pointer}button:hover{border-color:#7fe8e6}button:focus-visible{outline:2px solid #7fe8e6;outline-offset:3px}.note{font-size:13px}a{color:#7bddf3}footer{padding-top:12px;border-top:1px solid #294d60;margin-top:18px;font-size:13px}@media(max-width:700px){main,header{padding:16px}h1{font-size:24px}}</style>
<header><div class="eyebrow">BULLETS OF FURY · STAGE9 MINIBOSS · FURIOUS</div><h1>Event Horizon: spin, flight and energy bomb</h1><p>Faster whole-body rotation, larger up-and-down passes, and a visible eye charge before the energy bomb launches.</p></header>
<main><video id="v" controls preload="metadata" playsinline></video><div class="toolbar"><button id="spin">Fast spin</button><button id="vertical">Vertical pass</button><button id="charge">Charge</button><button id="launch">Launch</button><button id="impact">Impact</button><button id="frame">+1 frame</button><select id="speed" aria-label="Playback speed"><option value=".25">¼ speed</option><option value=".5">½ speed</option><option value="1" selected>Normal speed</option></select></div><p id="status"></p><p class="note">Continuous45-second native film. The invulnerable movement bot withholds weapons so the full attack sequence stays visible. Enemy HP and phases remain native.</p><footer><a href="../../HORIZON_ASSAULT_1025.md">Changes and verification</a> · <a href="../barrage_revision_1025/index.html">Other revised barrages and Herald flights</a> · <a href="../warden_tidal_1025/index.html">Stage9 water boss review</a></footer></main>
<script>const v=document.querySelector('#v');let data;function seek(t){v.pause();v.currentTime=Math.min(v.duration-.08,Math.max(0,t));}for(const id of ['spin','vertical','charge','launch','impact'])document.querySelector('#'+id).onclick=()=>seek(data.chapters[id]);document.querySelector('#frame').onclick=()=>seek(v.currentTime+1/30);document.querySelector('#speed').onchange=e=>v.playbackRate=+e.target.value;fetch('review.json').then(r=>r.json()).then(q=>{data=q;v.onloadedmetadata=()=>seek(q.chapters.spin);v.src=q.src;v.poster=q.poster;document.querySelector('#status').textContent=q.seconds.toFixed(1)+' seconds · Audio enabled through the video controls · Five checkpoints for close inspection';});</script></html>'''
if __name__=='__main__':publish()
