"""Replace only Mike's seven corrected Stage4 films; preserve current others."""
from pathlib import Path
import json,sys,subprocess,hashlib,urllib.request
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage4_amplify_1101';V=W/'video';D=Path('D:/BOF-Downloads/2026-10-31');ff=imageio_ffmpeg.get_ffmpeg_exe();base='http://127.0.0.1:8805';files={};receipts=[]
data=json.load(urllib.request.urlopen(base+'/enemy-showcase-1031/manifest.json'));old=json.loads(json.dumps(data));group=json.loads((V/'report.json').read_text());assert not group['errors']and not group['stats']['tapErrors']and not group['stats']['botErrors']
types=['sandtank','s4missile','s4command','s4tanker','s4tractor','s4heavyjet','s4sam'];routes={}
for item in data['items']:
 if item['stage']!=4 or item['type']not in types:continue
 typ=item['type'];r=json.loads((V/(typ+'.json')).read_text());movie=V/(typ+'.mp4');T=r['timeline'];assert not r['errors']and all(q['state']=='play'and not q['playerDead']for q in T),typ
 if typ!='s4tanker':assert all(q['hp']==r['setup']['hp']for q in T),typ
 else:assert any(q['hp']==0 for q in T)and len([e for e in r['details']['events']if e['event']=='fuel-splash'])==1
 result=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert result.returncode==0 and not result.stderr.strip(),result.stderr
 stream=imageio_ffmpeg.read_frames(str(movie));meta=next(stream);stream.close();assert meta['codec']=='h264'and meta['audio_codec']=='aac';fps=round((T[-1]['frames']-T[0]['frames'])/(T[-1]['seconds']-T[0]['seconds']),1)
 target=next((q for q in T if q['elapsed']>2 and q.get('phase')in['fire','lock']),T[len(T)//3]);target=next(q for q in T if q['elapsed']>1.8)if typ=='s4tanker'else target;poster=V/(typ+'.jpg')
 subprocess.run([ff,'-y','-ss',str(min(meta['duration']-.2,target['seconds']-r['start'])),'-i',str(movie),'-frames:v','1','-q:v','2',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 route='/current/stage4-'+typ+'-highway-1101';files[route+'.mp4']=str(movie.resolve());files[route+'.jpg']=str(poster.resolve());routes[typ]=route
 item['revisionPreviousVideo']=item['video'];item.update(title=r['title'].split(' / ')[0],video=route+'.mp4',poster=route+'.jpg',duration=meta['duration'],fps=fps,sound=True,maxHP=r['setup']['hp'],hitFrames=0,attackEvents=sum(e['event']=='shot'for e in r['details']['events']),source='Current Stage4 highway refit, generated authored sprites and native combat',outcome='Destroyed by actual player primary fire / native fuel splash'if typ=='s4tanker'else'Native sortie / invulnerable movement observer',errors=[],model=r['setup'].get('model')or'Native Highway Armor')
 receipts.append(dict(type=typ,id=item['id'],fps=fps,seconds=meta['duration'],decoded=True,audioPeak=r['details']['peak'],sourceHashes=r['sourceHashes'],sha256=hashlib.sha256(movie.read_bytes()).hexdigest()))
assert len(receipts)==7
assert all(next(q for q in data['items']if q['id']==item['id'])==item for item in old['items']if item['stage']!=4 or item['type']not in types)
data['seconds']=round(sum(q['duration']for q in data['items']),2);data['expected']=data['ready']=len(data['items']);p=W/'manifest-current.json';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/enemy-showcase-1031/manifest.json']=str(p.resolve())
page=urllib.request.urlopen(base+'/enemy-showcase-1031.html').read().decode('utf-8');banner='<p style="padding:12px 18px;border:1px solid #e2a44a;background:#241f15;color:#ffedce"><strong>Current Stage4 highway corrections:</strong> Straight Highway Tank, new black/orange Command Fighter, matching launcher-truck/SAM missiles, unarmed explosive Fuel Tanker, front-firing Tractor and fixed-rail Heavy Jet. SAM launches three missiles 0.18 seconds apart. <a href="/current/stage4-highway-1101.html">Watch these seven corrected enemies</a>.</p>'
page=page.replace('<body>','<body>'+banner,1);p=W/'enemy-showcase-current.html';p.write_text(page,encoding='utf-8');files['/enemy-showcase-1031.html']=str(p.resolve())
sections=''.join('<section><h2>'+json.loads((V/(t+'.json')).read_text())['title']+'</h2><video controls playsinline preload="none" poster="'+routes[t]+'.jpg" src="'+routes[t]+'.mp4"></video></section>'for t in types)
p=W/'highway-preview.html';p.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stage4 highway corrections</title><style>body{margin:0;background:#0b111b;color:#ecf4ff;font:16px/1.5 system-ui}main{max-width:1500px;margin:auto;padding:24px}a{color:#83dfff}h1{font-size:30px}h2{font-size:18px}section{padding:14px;background:#152333;border:1px solid #395069;border-radius:8px}video{display:block;width:100%;background:#000}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style><main><a href="/enemy-showcase-1031.html?revision=stage4-highway-1101#enemy=stage4-s4sam">Full enemy guide</a><h1>Stage4 / Highway corrections</h1><p>New matching military pixel art, fixed forward weapons and actual authored aircraft direction frames. The Highway Tank stays in its lane; the SAM releases three missiles one at a time.</p><p>The Fuel Tanker is unarmed. Its clip uses the pilot’s machine gun to trigger the native explosion and damage nearby barrels. All clips use actual game attacks, sounds and an invulnerable pilot.</p><div class="grid">'+sections+'</div></main><script>document.addEventListener("play",e=>{if(e.target.tagName==="VIDEO")for(const v of document.querySelectorAll("video"))if(v!==e.target)v.pause()},true)</script></html>',encoding='utf-8');files['/current/stage4-highway-1101.html']=str(p.resolve())
(W/'guide-update.json').write_text(json.dumps(dict(clips=receipts,files=files),indent=2))
if'--install'in sys.argv:
 p=D/'current-overrides.json';o=json.loads(p.read_text(encoding='utf-8'))
 for route,file in files.items():assert Path(file).resolve().is_relative_to(W.resolve())and Path(file).is_file();o['files'][route]=file
 p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8');print('Installed7 corrected Stage4 clips;',len(data['items']),'total cards; every other card preserved')
else:print('Prepared7 corrected Stage4 clips')
