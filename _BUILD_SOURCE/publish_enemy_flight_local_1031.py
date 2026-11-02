"""Publish the 114 current Stage4–9 guide cards; preserve Stage1–3 and archives."""
from pathlib import Path
import json,sys,subprocess,hashlib,html
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/enemy_flight_1031';D=Path('D:/BOF-Downloads/2026-10-31');ff=imageio_ffmpeg.get_ffmpeg_exe()
data=json.loads((R/'_shots/stage3_amplify_1031/guide-manifest-current.json').read_text(encoding='utf-8'));before=json.loads(json.dumps(data));files={};receipts=[]
for item in data['items']:
 if not 4<=item['stage']<=9:continue
 folder=W/'video'/('stage'+str(item['stage']));movie=folder/(item['id']+'.mp4');report=json.loads((folder/(item['id']+'.json')).read_text());group=json.loads((folder/'report.json').read_text());T=report['timeline'];S=group['stats']
 assert movie.is_file()and not report['errors']and not group['errors']and not S['tapErrors']and not S['botErrors'],item['id']
 assert all(q['state']=='play'and not q['playerDead']and(q['hp']==report['setup']['hp']or(q['dead']or q.get('dying')is not None)and q['hp']<=report['setup']['hp'])for q in T),item['id']
 assert not report['details']['glyphMisses'],(item['id'],report['details']['glyphMisses'])
 r=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr.strip(),(item['id'],r.stderr)
 stream=imageio_ffmpeg.read_frames(str(movie));meta=next(stream);stream.close();assert meta.get('audio_codec')=='aac'and meta['codec']=='h264',item['id'];duration=meta['duration'];fps=round((T[-1]['frames']-T[0]['frames'])/(T[-1]['seconds']-T[0]['seconds']),1)
 target=min(duration-.3,max(.5,duration*.42));poster=folder/(item['id']+'.jpg')
 subprocess.run([ff,'-y','-ss',str(target),'-i',str(movie),'-frames:v','1','-q:v','2',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 route='/current/'+item['id']+'-flight-1031';files[route+'.mp4']=str(movie.resolve());files[route+'.jpg']=str(poster.resolve())
 cuts=group['cuts'];idx=next(i for i,q in enumerate(cuts)if q['id']==item['id']);prior=cuts[idx-1]['details']['playing']if idx else{};played=report.get('played')or{k:v-prior.get(k,0)for k,v in report['details']['playing'].items()if v>prior.get(k,0)}
 item['revisionPreviousVideo']=item.get('video');item.update(video=route+'.mp4',poster=route+'.jpg',duration=duration,fps=fps,sound=True,audioCues=sum(played.values()),attackEvents=sum(q['event']in['shot','missile-release']for q in report['details']['events']),hitFrames=0,maxHP=report['setup']['hp'],outcome='Native isolated sortie / invulnerable movement observer',source='Current Stage4–9 flight/muzzle review; native HP and attack clocks',errors=[],model=report['setup'].get('model')or item.get('model'))
 receipts.append(dict(id=item['id'],stage=item['stage'],seconds=duration,fps=fps,decoded=True,playing=played,audioPeak=report['details']['peak'],nativeHP=report['setup']['hp'],sourceHashes=report['sourceHashes'],sha256=hashlib.sha256(movie.read_bytes()).hexdigest()))
assert len(receipts)==114,len(receipts)
assert all(next(x for x in data['items']if x['id']==q['id'])==q for q in before['items']if q['stage']<4 or q['stage']>9)
data['expected']=data['ready']=len(data['items']);data['seconds']=round(sum(q['duration']for q in data['items']),2)
p=W/'guide-manifest-current.json';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/enemy-showcase-1031/manifest.json']=str(p.resolve())
page=(R/'_shots/stage3_amplify_1031/enemy-showcase-current.html').read_text(encoding='utf-8')
banner='<p style="padding:12px 18px;border:1px solid #62c4d8;background:#102a40;color:#d5faff"><strong>Current Stage4–9 flight and weapon review:</strong> All 114 cards below now use the revised native enemies and game audio. Consistent complete hull banks, physical firing mouths, turning sorties, missile Retina locks and matching stage feedback. <a href="/current/enemy-flight-review-1031.html">Review the findings and jump to each stage</a>. The current Stage1–3 films remain intact.</p>'
page=page.replace('<body>','<body>'+banner,1);p=W/'enemy-showcase-current.html';p.write_text(page,encoding='utf-8');files['/enemy-showcase-1031.html']=str(p.resolve())
links=''.join('<li><a href="/enemy-showcase-1031.html?revision=stage4-9-flight-1031#enemy='+next(q['id']for q in data['items']if q['stage']==s)+'">Stage '+str(s)+' / '+str(sum(q['stage']==s for q in data['items']))+' current previews</a></li>'for s in range(4,10))
p=W/'review.html';p.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Stage4–9 enemy flight and firing review</title><style>body{margin:0;background:#0a121d;color:#edf4ff;font:17px/1.6 system-ui}main{max-width:900px;margin:auto;padding:32px}a{color:#77dfff}li{margin:12px 0}h1{font-size:30px}.box{padding:20px;background:#142a3b;border:1px solid #346578;border-radius:8px}</style><main><a href="/enemy-showcase-1031.html?revision=stage4-9-flight-1031#enemy=stage4-s4interceptor">Open the full enemy video guide</a><h1>Stage4–9 / Flight and firing review</h1><p>114 refreshed native enemy previews with game audio. All current Stage1–3 previews and archived originals are retained.</p><div class="box"><ul>'+links+'</ul></div><h2>What changed</h2><ul><li>Complete source animation banks retain one hull through movement and attacks, with stable scale and pivots.</li><li>Curved airbase interceptor/rocket sorties give native attacks a useful firing window.</li><li>Real turret mouths, attached muzzle flashes and matching stage exhaust/projectile art.</li><li>Physical missiles use the existing flashing Retina and lock beeps before launch; ordinary enemy bullets remain unshootable.</li><li>Sewer factory aliases now use their real controllers. Royal and Blackice flight banks preserve their own colors.</li></ul><p>These are isolated native demonstrations with an invulnerable movement-only observer. Enemy HP, attack clocks and phases are not written during filming. This pass covers regular enemies; boss/miniboss encounters retain their separate owners.</p></main></html>',encoding='utf-8');files['/current/enemy-flight-review-1031.html']=str(p.resolve())
(W/'guide-update.json').write_text(json.dumps(dict(clips=receipts,files=files),indent=2))
if'--install'in sys.argv:
 p=D/'current-overrides.json';o=json.loads(p.read_text(encoding='utf-8'))
 for route,file in files.items():assert Path(file).resolve().is_relative_to(W.resolve())and Path(file).is_file();o['files'][route]=file
 p.write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8');print('Installed114 current movies;',len(data['items']),'cards; preserved Stage1–3 and archives')
else:print('Prepared114 current movies;',len(data['items']),'cards')
