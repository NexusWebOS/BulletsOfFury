"""Install only ten recolored films, retaining all other144 guide cards exactly."""
from pathlib import Path
import json,sys,subprocess,hashlib,urllib.request,copy,array,math
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage9_palettes_1101';V=O/'video';ff=imageio_ffmpeg.get_ffmpeg_exe();base='http://127.0.0.1:8805';files={};receipts=[]
palette=json.loads((R/'_BUILD_SOURCE/stage9_amplify_1101/palettes.json').read_text())['models'];group=json.loads((V/'report.json').read_text());assert len(group['cuts'])==len(palette) and not group['errors']and not group['stats']['tapErrors']and not group['stats']['botErrors'];ids={c['id']for c in group['cuts']}
data=json.load(urllib.request.urlopen(base+'/enemy-showcase-1031/manifest.json'));old=copy.deepcopy(data)
page=urllib.request.urlopen(base+'/current/stage9-water-refit-1101.html').read().decode('utf-8');start=page.index('const chapters=')+len('const chapters=');chapters,used=json.JSONDecoder().raw_decode(page[start:]);prior=copy.deepcopy(chapters)
for cut in group['cuts']:
 cid=cut['id'];model=cut['setup']['model'];family=palette[model];T=cut['timeline'];assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in cut['sourceHashes'].items());assert all(t['hp']==cut['setup']['hp']and not t['playerDead']and t['state']=='play'for t in T)
 movie=V/(cid+'.mp4');result=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert result.returncode==0 and not result.stderr.strip(),result.stderr
 stream=imageio_ffmpeg.read_frames(str(movie));meta=next(stream);stream.close();assert meta['codec']=='h264'and meta['audio_codec']=='aac'
 pcm=subprocess.run([ff,'-v','error','-i',str(movie),'-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout;a=array.array('h');a.frombytes(pcm);peak=max(abs(v)for v in a)/32768;rms=math.sqrt(sum(v*v for v in a)/len(a))/32768;assert .00001<rms and peak<.9999
 target=next((t for t in T if t['phase']in['fire','beam','pass']and 80<t['y']<420),T[len(T)//2]);at=target['seconds']-cut['start'];poster=V/(cid+'.jpg');subprocess.run([ff,'-y','-ss',str(at),'-i',str(movie),'-frames:v','1','-q:v','2',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
 route='/current/'+cid+'-palette-1101';files[route+'.mp4']=str(movie.resolve());files[route+'.jpg']=str(poster.resolve());fps=round((T[-1]['frames']-T[0]['frames'])/(T[-1]['seconds']-T[0]['seconds']),1)
 item=next(q for q in data['items']if q['id']==cid);item['revisionPreviousVideo']=item['video'];item.update(video=route+'.mp4',poster=route+'.jpg',duration=meta['duration'],fps=fps,sound=True,source='Stage9 '+family+' palette / native rendering and mixer',palette=family,errors=[],attackEvents=sum(q['event']=='shot'for q in cut['details']['events']))
 c=next(q for q in chapters if q['id']==cid);c.update(video=route+'.mp4',poster=route+'.jpg',detail=c['detail']+' Palette: '+family+'.')
 receipts.append(dict(id=cid,model=model,palette=family,seconds=meta['duration'],fps=fps,decoded=True,audioPeak=peak,audioRMS=rms,sourceHashes=cut['sourceHashes'],posterAt=at))
assert[q for q in data['items']if q['id']not in ids]==[q for q in old['items']if q['id']not in ids]
assert[q for q in chapters if q['id']not in ids]==[q for q in prior if q['id']not in ids]
data['seconds']=round(sum(q['duration']for q in data['items']),2);p=O/'manifest-current.json';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/enemy-showcase-1031/manifest.json']=str(p.resolve())
page=page[:start]+json.dumps(chapters,separators=(',',':'))+page[start+used:];page=page.replace('Pink Comet, a nine-way Beacon','Black/blue fighters, purple/pink crystal vessels, black/pink hunters, Pink Comet, a nine-way Beacon');p=O/'water-preview.html';p.write_text(page,encoding='utf-8');files['/current/stage9-water-refit-1101.html']=str(p.resolve())
(O/'publication.json').write_text(json.dumps(dict(clips=receipts,totalCards=len(data['items']),unchangedCards=len(data['items'])-len(ids),unchangedStage9Chapters=len(chapters)-len(ids),files=files),indent=2))
if'--install'in sys.argv:
 p=Path('D:/BOF-Downloads/2026-10-31/current-overrides.json');x=json.loads(p.read_text(encoding='utf-8'))
 for url,path in files.items():assert Path(path).resolve().is_relative_to(O.resolve())and Path(path).is_file();x['files'][url]=path
 p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8');print('Installed ten palette films;',len(data['items'])-len(ids),'other guide cards unchanged')
else:print('Prepared ten palette films')
