"""Current Stage3 guide movies; preserve all Stage1/2 and archived originals."""
from pathlib import Path
import json,sys,subprocess,hashlib
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage3_amplify_1031';D=Path('D:/BOF-Downloads/2026-10-31');ff=imageio_ffmpeg.get_ffmpeg_exe();reports={};files={};receipts=[]
for folder in sorted((W/'video').iterdir()):
 if not(folder/'preview.mp4').is_file():continue
 r=json.loads((folder/'report.json').read_text());T=r['timeline'];S=r['stats'];typ=r['type'];movie=folder/'preview.mp4'
 assert not r['errors']and not S['tapErrors']and not S['botErrors'],typ
 assert all(q['state']=='play'and not q['playerDead']and q['hp']==r['setup']['hp']for q in T),typ
 assert S['peak']>0 and S['playing'],typ
 assert any(e['event']in['shot','cross-lasers']for e in S['events']),typ
 result=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert result.returncode==0 and not result.stderr.strip(),result.stderr
 stream=imageio_ffmpeg.read_frames(str(movie));meta=next(stream);stream.close();duration=meta['duration']
 target=next((q for q in T if q.get('phase')=='fire'),None)if typ=='cryoeye'else next((q for q in T if q['seconds']>1.9 and q.get('shots',0)>0),None)if typ.startswith('modturret')else None
 if target is None:target=next((q for q in T if q.get('phase')in['lay','curve','sortie']and q['seconds']>3),T[len(T)//2])
 poster=folder/'poster.jpg'
 subprocess.run([ff,'-y','-ss',str(target['seconds']),'-i',str(movie),'-frames:v','1','-q:v','2',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 route='/current/stage3-'+typ+'-1031';files[route+'.mp4']=str(movie.resolve());files[route+'.jpg']=str(poster.resolve())
 fps=round((T[-1]['frames']-T[0]['frames'])/(T[-1]['seconds']-T[0]['seconds']),1)
 receipts.append(dict(type=typ,seconds=duration,fps=fps,decoded=True,audio=S['playing'],peak=S['peak'],sourceHashes=r['sourceHashes'],sha256=hashlib.sha256(movie.read_bytes()).hexdigest()))
 reports[typ]=dict(report=r,route=route,duration=duration,fps=fps)
assert len(reports)==8,('Incomplete Stage3 movies',list(reports))
data=json.loads((R/'_shots/stage2_amplify_1031/guide-manifest-current.json').read_text(encoding='utf-8'));old=json.loads(json.dumps(data))
for item in data['items']:
 if item.get('stage')!=3:continue
 typ=item['type'];typ='modturret-laser'if typ=='modturret'and'Laser'in item['title']else'modturret-sonic'if typ=='modturret'else typ
 a=reports[typ];r=a['report'];item['revisionPreviousVideo']=item.get('video');item.update(title=r['title'].split(' / ')[0],video=a['route']+'.mp4',poster=a['route']+'.jpg',duration=a['duration'],fps=a['fps'],sound=True,audioCues=len(r['stats']['playing']),attackEvents=sum(e['event']in['shot','cross-lasers']for e in r['stats']['events']),hitFrames=0,maxHP=r['setup']['hp'],outcome='Native sortie / invulnerable movement observer',source='Current Stage3 ice refit; native health and attack clocks',errors=[],model=r['setup'].get('model')or'Island ground turret')
assert all(next(x for x in data['items']if x['id']==q['id'])==q for q in old['items']if q['stage']!=3)
data['expected']=data['ready']=len(data['items']);data['seconds']=round(sum(q['duration']for q in data['items']),2)
p=W/'guide-manifest-current.json';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/enemy-showcase-1031/manifest.json']=str(p.resolve())
html=(R/'_shots/stage2_amplify_1031/enemy-showcase-current.html').read_text(encoding='utf-8')
html=html.replace('current individual films include the Stage2 revision','current individual films include the Stage1, Stage2 and Stage3 revisions')
banner='<p style="padding:12px 18px;border:1px solid #558ecc;background:#102a40;color:#d5faff"><strong>Current Stage3 ice refit:</strong> Upright larger Shard Dart, turning twin-gun interceptors, blue-white ice rounds, island-mounted turrets, blue sonic waves, four-way Cryoeye lasers and a distinct ice mine bomber. <a href="/current/stage3-amplify-1031.html">Watch all 8 current Stage3 previews</a>. Stage1 and Stage2 updates remain current.</p>'
if'<body>'in html:html=html.replace('<body>','<body>'+banner,1)
else:raise ValueError('Missing guide body')
p=W/'enemy-showcase-current.html';p.write_text(html,encoding='utf-8');files['/enemy-showcase-1031.html']=str(p.resolve())
body=''
for typ,a in reports.items():body+='<section><h2>'+a['report']['title']+'</h2><video controls playsinline preload="none" poster="'+a['route']+'.jpg" src="'+a['route']+'.mp4"></video><p>'+str(a['fps'])+' native fps / '+str(round(a['duration'],1))+' seconds / game audio</p></section>'
p=W/'ice-preview.html';p.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stage3 ice enemy refit</title><style>body{margin:0;background:#090e16;color:#edf3ff;font:16px/1.5 system-ui}main{max-width:1500px;margin:auto;padding:24px}a{color:#7adaff}h1{font-size:30px}h2{font-size:19px}video{display:block;width:100%;background:#000}section{padding:16px;background:#132231;border:1px solid #34506b;border-radius:8px}p{color:#adc2de}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style><main><a href="/enemy-showcase-1031.html?revision=stage3-ice-1031#enemy=stage3-cryoeye">Full enemy video guide</a><h1>Stage3 / Ice enemy refit</h1><p>Eight native Furious previews: upright Shard Dart, actual directional interceptor frames and two cannon mouths, clear ice bullets, island turrets, blue sonic waves, four cardinal level2 ice lasers, and a new mine-dropping bomber.</p><p>The observer is invulnerable and uses normal movement input. Enemy health, phase timers and projectiles are owned by the actual game. Isolated demonstrations, not campaign difficulty certification. Stage1 and Stage2 updates remain in the full guide.</p><div class="grid">'+body+'</div></main><script>document.addEventListener("play",e=>{if(e.target.tagName==="VIDEO")for(const v of document.querySelectorAll("video"))if(v!==e.target)v.pause()},true)</script></html>',encoding='utf-8');files['/current/stage3-amplify-1031.html']=str(p.resolve())
(W/'guide-update.json').write_text(json.dumps(dict(clips=receipts,files=files),indent=2))
if'--install'in sys.argv:
 p=D/'current-overrides.json';o=json.loads(p.read_text(encoding='utf-8'))
 for route,file in files.items():assert Path(file).resolve().is_relative_to(W.resolve())and Path(file).is_file();o['files'][route]=file
 p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8');print('Installed',len(reports),'movies;',len(data['items']),'enemy cards')
else:print('Prepared',len(reports),'movies;',len(data['items']),'enemy cards')
