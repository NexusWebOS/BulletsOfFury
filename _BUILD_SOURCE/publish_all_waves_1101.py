"""Decode and publish all regular-wave films with per-wave native timestamps."""
from pathlib import Path
import json,sys,hashlib,subprocess,urllib.request,array,math
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/waves_all_1101';P=O/'publication';P.mkdir(exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe();files={};levels=[];receipts=[]
page=P/'index.html';page.write_bytes((R/'_BUILD_SOURCE/waves_viewer_1101.html').read_bytes())
if '--refresh-page' in sys.argv:
 receipt=P/'receipts.json';saved=json.loads(receipt.read_text());saved['files']['/current/all-waves-1101.html']=str(page.resolve());receipt.write_text(json.dumps(saved,indent=2))
 if '--install' in sys.argv:
  config=Path('D:/BOF-Downloads/2026-10-31/current-overrides.json');value=json.loads(config.read_text(encoding='utf-8'));value['files']['/current/all-waves-1101.html']=str(page.resolve());config.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
 print('Updated the page within the existing permitted review-media directory');sys.exit(0)
guide=json.load(urllib.request.urlopen('http://127.0.0.1:8805/enemy-showcase-1031/manifest.json'));biomes=['Jungle Coast','Volcanic Pass','Frozen Islands','Desert Highway','Orbital Rift','Storm Front','Toxic Sewers','Alien Hive','Waterworld']
for stage,route in [(s,r)for s in range(1,10)for r in(['left','right']if s==6 else['left'])]:
 label='stage-'+str(stage)+('-right'if stage==6 and route=='right'else'');V=O/label;report=json.loads((V/'report.json').read_text());q=report['result'];T=report['trace'];assert q['done']and len(report['events'])==q['expected']and all(not x['mini']and not x['boss']and not x['dead']for x in T),(label,q)
 assert not report['errors']and not report['stats']['tapErrors']and not report['stats']['botErrors'],label
 if stage==6:assert q['dialogs']['route']==route and set(q['carriers'])=={'pair-top','pair-bottom','nuclear','laser'},(label,q['dialogs'],q['carriers'])
 assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in report['sourceHashes'].items()),'Production changed: '+label
 movie=V/('stage-'+str(stage)+'-waves.mp4');r=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr.strip(),r.stderr
 stream=imageio_ffmpeg.read_frames(str(movie));meta=next(stream);stream.close();assert meta['codec']=='h264'and meta['audio_codec']=='aac'
 pcm=subprocess.run([ff,'-v','error','-i',str(movie),'-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout;a=array.array('h');a.frombytes(pcm);peak=max(abs(x)for x in a)/32768;rms=math.sqrt(sum(x*x for x in a)/len(a))/32768;assert rms>.00001 and peak<.9999,(label,peak,rms)
 nativefps=(T[-1]['frames']-T[0]['frames'])/(T[-1]['wall']-T[0]['wall']);base='/current/waves-1101/'+label;files[base+'.mp4']=str(movie.resolve());chapters=[];events=report['events'];assert sorted(e['i']for e in events)==list(range(q['expected']))
 for n,e in enumerate(events):
  start=max(0,e['video']-.4);end=min(meta['duration'],max(start+12,(events[n+1]['video']+3)if n+1<len(events)else meta['duration']));types=list(dict.fromkeys(e['types']or e['spawns']));names=[]
  for unit in e.get('units',[]):
   item=next((x for x in guide['items']if x['stage']==stage and x['type']==unit['type']and unit.get('model')and x.get('model')==unit['model']),None)or next((x for x in guide['items']if x['stage']==stage and x['type']==unit['type']),None)
   if item and item['title']not in names:names.append(item['title'])
  if not names:
   for typ in types:
    item=next((x for x in guide['items']if x['stage']==stage and x['type']==typ),None)
    if item and item['title']not in names:names.append(item['title'])
  special=e['meta'].get('_ca111');title={'pair-top':'Cloud carriers · northern approach','pair-bottom':'Cloud carriers · southern approach','nuclear':'Nuclear warhead carrier','laser':'Laser warhead carrier'}.get(special)or' / '.join(names[:3])or'Formation arrival'
  if special:
   completed=next((t['wall'] for t in T if t['wall']>=e['video'] and special in t.get('carriers',[])),None)
   assert completed is not None,(label,special,'assault did not finish')
   end=min(meta['duration'],max(end,completed+2))
  poster=P/(label+'-wave-'+str(n+1).zfill(2)+'.jpg');at=min(end-.1,start+3);subprocess.run([ff,'-y','-ss',str(at),'-i',str(movie),'-frames:v','1','-vf','scale=320:200','-q:v','3',str(poster)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True);posturl=base+'-wave-'+str(n+1).zfill(2)+'.jpg';files[posturl]=str(poster.resolve());chapters.append(dict(number=n+1,title=title,start=round(start,3),end=round(end,3),poster=posturl,planned=e['planned'],types=types))
 levels.append(dict(id=label,stage=stage,route=route if stage==6 else None,title='Stage '+str(stage)+(' / '+('Harrier route'if route=='left'else'Rebel route')if stage==6 else''),tab='Stage '+str(stage)+(' · '+('Harrier'if route=='left'else'Rebels')if stage==6 else''),biome=biomes[stage-1],routeLabel=('Harrier route'if route=='left'else'Rebel route')if stage==6 else None,video=base+'.mp4',poster=chapters[0]['poster'],seconds=meta['duration'],waves=chapters));receipts.append(dict(label=label,seconds=meta['duration'],chapters=len(chapters),nativeFPS=round(nativefps,2),decoded=True,audioPeak=peak,audioRMS=rms,sourceHashes=report['sourceHashes'],methodSourceHash=report['methodSourceHash']))
data=dict(title='Every regular wave',difficulty='furious',levels=levels,uniqueScheduledWaves=sum(len(l['waves'])for l in levels if l['id']!='stage-6-right'),chapterCount=sum(len(l['waves'])for l in levels),seconds=round(sum(l['seconds']for l in levels),2),stageX='Boss encounters only; excluded');p=P/'all-waves.json';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/current/all-waves-1101.json']=str(p.resolve());files['/current/all-waves-1101.html']=str(page.resolve())
(P/'receipts.json').write_text(json.dumps(dict(clips=receipts,files=files,seconds=data['seconds'],chapterCount=data['chapterCount']),indent=2));assert data['uniqueScheduledWaves']==260 and data['chapterCount']==313
if'--install'in sys.argv:
 p=Path('D:/BOF-Downloads/2026-10-31/current-overrides.json');x=json.loads(p.read_text(encoding='utf-8'))
 for url,file in files.items():assert Path(file).resolve().is_relative_to(R.resolve())and Path(file).is_file();x['files'][url]=file
 p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8');print('Installed all9 regular levels, both Stage6 routes,313 wave chapters')
else:print('Prepared313 wave chapters')
