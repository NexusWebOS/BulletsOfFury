"""Publish one revised local guide card and two native pursuit demonstrations.
--install updates only the existing local review server's scoped file routes.
"""
from pathlib import Path
import json,sys,re,subprocess,hashlib
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/kamikaze_orbit_1031';V=W/'video';D=Path('D:/BOF-Downloads/2026-10-31');ff=imageio_ffmpeg.get_ffmpeg_exe();files={};reports={};receipt=[]
for name in ['kamikaze','wave']:
 folder=V/name;r=json.loads((folder/'report.json').read_text());T=r['timeline'];S=r['stats'];movie=folder/'preview.mp4'
 assert not r['errors']and not S['tapErrors']and not S['botErrors'],name
 assert all(q['state']=='play'and not q['playerDead']for q in T)
 assert all(all(e=='s1jetdelta_b'for e in q['actors'])for q in T)
 assert any(q['phase']=='orbit'for q in T)and any(q['phase']=='strike'for q in T)
 assert max(q['rollRate']for q in T)>2.5 and len({q['rollFrame']for q in T})>=10
 assert T[-1]['shots']==0 and S['playing'].get('jetDash',0)>0 and S['peak']>0
 result=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert result.returncode==0 and not result.stderr.strip(),result.stderr
 frames=imageio_ffmpeg.read_frames(str(movie));meta=next(frames);frames.close();duration=meta['duration']
 candidates=[q for q in T if q['phase']=='orbit'and q['rollFrame']in [0,1,14,15]and q['camera']['left']+65<q['x']<q['camera']['right']-65 and 75<q['y']<420]
 q=candidates[0]if candidates else next(q for q in T if q['phase']=='orbit')
 poster=folder/'poster.jpg';subprocess.run([ff,'-y','-ss',str(max(0,q['seconds']-.02)),'-i',str(movie),'-frames:v','1','-q:v','2',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 route='/current/kamikaze-'+('orbit'if name=='kamikaze'else'wave')+'-1031';files[route+'.mp4']=str(movie.resolve());files[route+'.jpg']=str(poster.resolve())
 reports[name]=dict(report=r,route=route,duration=duration)
 receipt.append(dict(name=name,duration=duration,rollPoses=len({q['rollFrame']for q in T}),maxRollRate=max(q['rollRate']for q in T),audio=S['playing'],nativeFPS=round((T[-1]['frames']-T[0]['frames'])/(T[-1]['seconds']-T[0]['seconds']),1),sourceHashes=r['sourceHashes'],sha256=hashlib.sha256(movie.read_bytes()).hexdigest(),decoded=True))
data=json.loads((R/'_shots/stage1_followup_1031/guide-manifest-current.json').read_text(encoding='utf-8'));item=next(q for q in data['items']if q['id']=='stage1-s1jetdelta-b-2');a=reports['kamikaze'];r=a['report'];item['revisionPreviousVideo']=item['video'];item.update(title='Delta Kamikaze / Earth Camo',video=a['route']+'.mp4',poster=a['route']+'.jpg',duration=a['duration'],fps=receipt[0]['nativeFPS'],sound=True,audioCues=len(r['stats']['playing']),attackEvents=sum(q['mode']=='strike'for q in r['stats']['orbit']),outcome='Orbiting pursuit / native ram',source='Current authored16-pose rolling kamikaze; native input-only weaving observer, invulnerable',errors=[])
data['seconds']=round(sum(q['duration']for q in data['items']),2);manifest=W/'guide-manifest-current.json';manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/enemy-showcase-1031/manifest.json']=str(manifest.resolve())
html=(R/'_shots/stage1_followup_1031/enemy-showcase-current.html').read_text(encoding='utf-8');banner='<p style="padding:12px 18px;border:1px solid #477d8c;background:#102a36;color:#d5faff"><strong>Current Stage1 previews:</strong> The kamikaze now uses light brown/orange jungle camo, continuous authored barrel rolls, animated thrusters and banking orbit pursuit. Rolls accelerate near contact. <a href="/current/kamikaze-orbit-1031.html">Single-aircraft and three-plane previews</a>. The original complete reel remains an archive.</p>'
html,n=re.subn(r'<p style="padding:12px 18px;border:1px solid #477d8c.*?</p>',banner,html,count=1,flags=re.S);assert n==1;page=W/'enemy-showcase-current.html';page.write_text(html,encoding='utf-8');files['/enemy-showcase-1031.html']=str(page.resolve())
page=W/'pursuit-preview.html';body=''
for key,title in [('kamikaze','Single aircraft'),('wave','Three-plane wave')]:
 a=reports[key];body+='<section><h2>'+title+'</h2><video controls playsinline preload="metadata" poster="'+a['route']+'.jpg" src="'+a['route']+'.mp4"></video></section>'
page.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kamikaze rolling pursuit</title><style>body{margin:0;background:#071018;color:#e6eef4;font:16px/1.5 system-ui}main{max-width:1280px;margin:auto;padding:24px}a{color:#82e5df}h1{font-size:30px}h2{font-size:21px}video{display:block;width:100%;max-height:80vh;background:#000}section{margin:28px 0}p{max-width:900px;color:#b5cbd5}</style><main><a href="/enemy-showcase-1031.html?revision=kamikaze-orbit-1031#enemy=stage1-s1jetdelta-b-2">← Enemy field guide</a><h1>Kamikaze rolling pursuit</h1><p>Light brown/orange jungle camo, continuous authored barrel rolls, faster rolling near contact, animated thrusters and turning pursuit that curves around the pilot.</p><p>Native Furious gameplay with an invulnerable observer using regular movement input. The wave staggers its dives and steers aircraft apart.</p>'+body+'</main></html>',encoding='utf-8');files['/current/kamikaze-orbit-1031.html']=str(page.resolve())
(W/'guide-update.json').write_text(json.dumps(dict(clips=receipt,files=files),indent=2))
if '--install'in sys.argv:
 p=D/'current-overrides.json';o=json.loads(p.read_text(encoding='utf-8'))
 for route,file in files.items():assert Path(file).resolve().is_relative_to(W.resolve())and Path(file).is_file();o['files'][route]=file
 p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8');print('Installed one guide card and two local previews')
else:print('Prepared one guide card and two local previews')
