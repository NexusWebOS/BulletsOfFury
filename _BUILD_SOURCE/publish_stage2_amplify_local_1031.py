"""Install only current Stage2 preview routes; preserve Stage1 and archived media."""
from pathlib import Path
import json,sys,re,subprocess,hashlib
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage2_amplify_1031';V=W/'video';D=Path('D:/BOF-Downloads/2026-10-31');ff=imageio_ffmpeg.get_ffmpeg_exe()
files={};reports={};receipts=[]
for folder in sorted(V.iterdir()):
 if not(folder/'preview.mp4').is_file():continue
 r=json.loads((folder/'report.json').read_text());T=r['timeline'];S=r['stats'];typ=r['type'];movie=folder/'preview.mp4'
 assert not r['errors']and not S['tapErrors']and not S['botErrors'],typ
 assert all(q['state']=='play'and not q['playerDead']for q in T),typ
 assert all(q['hp']==r['setup']['hp']for q in T),typ
 assert S['peak']>0 and S['playing'],typ
 assert any(e['event']in['shot','beam','turret-shot','volcano-orb','deploy-jet','bite']for e in S['events']),typ
 result=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert result.returncode==0 and not result.stderr.strip(),result.stderr
 stream=imageio_ffmpeg.read_frames(str(movie));meta=next(stream);stream.close();duration=meta['duration']
 phases=['fire','burst','deploy','bite','lay','erupt','spiral','curve'];q=next((q for q in T if q.get('phase')in phases and q['seconds']>2),T[len(T)//2]);poster=folder/'poster.jpg'
 subprocess.run([ff,'-y','-ss',str(max(0,q['seconds'])),'-i',str(movie),'-frames:v','1','-q:v','2',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 route='/current/stage2-'+typ+'-1031';files[route+'.mp4']=str(movie.resolve());files[route+'.jpg']=str(poster.resolve())
 fps=round((T[-1]['frames']-T[0]['frames'])/(T[-1]['seconds']-T[0]['seconds']),1)
 receipts.append(dict(type=typ,title=r['title'],seconds=duration,fps=fps,decoded=True,audio=S['playing'],peak=S['peak'],sourceHashes=r['sourceHashes'],sha256=hashlib.sha256(movie.read_bytes()).hexdigest()))
 reports[typ]=dict(report=r,route=route,duration=duration,fps=fps)
assert len(reports)==20,('Incomplete current Stage2 films',list(reports))
data=json.loads((R/'_shots/kamikaze_orbit_1031/guide-manifest-current.json').read_text(encoding='utf-8'));data['items']=[q for q in data['items']if q['id']not in ['stage2-eye','stage2-magmaorb','stage2-magmaorb-2']]
for role in ['flame','balls','guns','wall']:
 typ='v31elite_'+role;data['items'].append(dict(id='stage2-'+typ,stage=2,stageName='Magma frontier',title=reports[typ]['report']['title'],model='Furnace Wing',source='Carrier hangar deployment',type=typ,errors=[]))
for item in data['items']:
 if item.get('stage')!=2:continue
 typ=item['type'];typ='lavasnake'if typ=='crawl'else'modturret-laser'if typ=='modturret'and'Laser'in item['title']else'modturret-missile'if typ=='modturret'else typ
 a=reports[typ];r=a['report'];item['revisionPreviousVideo']=item.get('video');item.update(video=a['route']+'.mp4',poster=a['route']+'.jpg',duration=a['duration'],fps=a['fps'],sound=True,audioCues=len(r['stats']['playing']),attackEvents=sum(e['event']in['shot','beam','turret-shot','volcano-orb','deploy-jet','bite']for e in r['stats']['events']),hitFrames=0,maxHP=r['setup']['hp'],outcome='Native sortie / invulnerable movement observer',source='Current Stage2 authored volcanic refit; native HP and attack clocks',errors=[],model=r['setup'].get('model')or'Volcanic ground turret')
 if item['type']=='crawl':item['id']='stage2-lavasnake';item['type']='lavasnake'
 item['title']=r['title'].split(' / ')[0]if not typ.startswith('v31elite_')else r['title']
for i,q in enumerate(data['items'],1):q['number']=i
data['expected']=data['ready']=len(data['items']);data['seconds']=round(sum(q['duration']for q in data['items']),2)
manifest=W/'guide-manifest-current.json';manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/enemy-showcase-1031/manifest.json']=str(manifest.resolve())
html=(R/'_shots/kamikaze_orbit_1031/enemy-showcase-current.html').read_text(encoding='utf-8')
banner='<p style="padding:12px 18px;border:1px solid #477d8c;background:#102a36;color:#d5faff"><strong>Current Stage2 volcanic refit:</strong> Distinct ships, actual flame and thunderfire ordnance, twin weapons, shielded Crucible, mechanical serpent, mine drops, opening carrier hangar and nine-spike laser disc. <a href="/current/stage2-amplify-1031.html">Watch all 20 current Stage2 previews</a>. Stage1 fixes remain current; historical full reels remain archived.</p>'
html,n=re.subn(r'<p style="padding:12px 18px;border:1px solid #477d8c.*?</p>',banner,html,count=1,flags=re.S);assert n==1
html=html.replace('an invulnerable observer fires back after an observation window','an invulnerable observer uses native controls; the new Stage2 films use movement without player fire')
html=html.replace('▶ Complete video','▶ Archived complete video').replace('Download complete video','Download archived complete video')
html=html.replace('Every regular enemy / Complete showcase','Every regular enemy / Archived complete showcase')
html=html.replace("data.expected+' individual variants · '+fmt(data.seconds)+' of native footage'","'Original archived full reel · current individual films include the Stage2 revision'")
page=W/'enemy-showcase-current.html';page.write_text(html,encoding='utf-8');files['/enemy-showcase-1031.html']=str(page.resolve())
body=''
for typ,a in reports.items():body+='<section><h2>'+a['report']['title']+'</h2><video controls playsinline preload="none" poster="'+a['route']+'.jpg" src="'+a['route']+'.mp4"></video><p>'+str(a['fps'])+' native fps · '+str(round(a['duration'],1))+' seconds · game audio</p></section>'
page=W/'volcanic-preview.html';page.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stage2 volcanic enemy refit</title><style>body{margin:0;background:#090e13;color:#edf3f5;font:16px/1.5 system-ui}main{max-width:1500px;margin:auto;padding:24px}a{color:#ffba76}h1{font-size:30px}h2{font-size:19px}video{display:block;width:100%;background:#000}section{margin:0;padding:16px;background:#131d24;border:1px solid #34424b;border-radius:8px}p{color:#adc2ce}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style><main><a href="/enemy-showcase-1031.html?revision=stage2-amplify-1031#enemy=stage2-disc">← Enemy field guide</a><h1>Stage2 · Volcanic enemy refit</h1><p>Twenty native Furious previews. Distinct authored hulls, frame-based turning and effects, fire weapons and readable attack windows. Magma Eye and the Magma Orb enemy are retired; the crawler is replaced by the mechanical serpent.</p><p>The observer is invulnerable and uses normal movement input. Enemy health, phase timers and projectiles are controlled by the actual game. These are isolated demonstrations, not a campaign difficulty test.</p><div class="grid">'+body+'</div></main><script>document.addEventListener("play",e=>{if(e.target.tagName==="VIDEO")for(const v of document.querySelectorAll("video"))if(v!==e.target)v.pause()},true)</script></html>',encoding='utf-8');files['/current/stage2-amplify-1031.html']=str(page.resolve())
(W/'guide-update.json').write_text(json.dumps(dict(clips=receipts,files=files),indent=2))
if '--install'in sys.argv:
 p=D/'current-overrides.json';o=json.loads(p.read_text(encoding='utf-8'))
 for route,file in files.items():assert Path(file).resolve().is_relative_to(W.resolve())and Path(file).is_file();o['files'][route]=file
 p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8');print('Installed',len(reports),'native films;',len(data['items']),'total enemy guide cards')
else:print('Prepared',len(reports),'films;',len(data['items']),'cards')
