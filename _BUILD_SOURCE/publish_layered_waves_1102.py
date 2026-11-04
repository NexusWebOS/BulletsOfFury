"""Decode and publish all regular-wave films with per-wave native timestamps."""
from pathlib import Path
import json,sys,hashlib,subprocess,urllib.request,array,math,shutil,datetime
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];W=R/'_shots/waves_layers_1102/publication';O=R/'_shots/waves_layers_1102';P=O/'publication';P.mkdir(exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe();files={};levels=[];receipts=[]
D=Path(r'C:/Users/Mike/Documents/New project/BOF-GitHub-Download-1102');TARGET=D/'review/current';MEDIA=TARGET/'waves-layers-1102';MEDIA.mkdir(exist_ok=True)
page=P/'index.html';page.write_bytes((R/'_BUILD_SOURCE/waves_viewer_1101.html').read_bytes())
guide=json.loads((D/'review/enemy-showcase-1031/manifest.json').read_text(encoding='utf-8'));biomes=['Jungle Coast','Volcanic Pass','Frozen Islands','Desert Highway','Orbital Rift','Storm Front','Toxic Sewers','Alien Hive','Waterworld']
for stage,route in [(s,r)for s in range(1,10)for r in(['left','right']if s==6 else['left'])]:
 label='stage-'+str(stage)+('-right'if stage==6 and route=='right'else'');candidates=[p.parent for p in O.glob(label+'*/verified.json') if json.loads(p.read_text(encoding='utf-8')).get('label')==label and not json.loads(p.read_text(encoding='utf-8')).get('excluded')];assert candidates,'Missing complete film: '+label;V=max(candidates,key=lambda p:(p/'verified.json').stat().st_mtime);report=json.loads((V/'report.json').read_text(encoding='utf-8'));q=report['result'];T=report['trace'];assert q['done']and len(report['events'])==q['expected']and all(not x['mini']and not x['boss']and not x['dead']for x in T),(label,q)
 assert stage==7 or max(b['wall']-a['wall'] for a,b in zip(T,T[1:]))<5,(label,'capture pause')
 assert not report['errors'] and not report['httpErrors'] and not report['stats']['tapErrors'] and not report['stats']['botErrors'],label
 if stage!=1:assert report['scenery']['active'] and all(t['layers']['draws'].get('stage-'+str(stage),0)>0 for t in T),label
 if stage==6:assert q['dialogs']['route']==route and set(q['carriers'])=={'pair-top','pair-bottom','nuclear','laser'},(label,q['dialogs'],q['carriers'])
 assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in report['sourceHashes'].items()),'Production changed: '+label
 movie=V/('stage-'+str(stage)+'-waves.mp4');r=subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr.strip(),r.stderr
 stream=imageio_ffmpeg.read_frames(str(movie));meta=next(stream);stream.close();assert meta['codec']=='h264'and meta['audio_codec']=='aac'
 pcm=subprocess.run([ff,'-v','error','-i',str(movie),'-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout;a=array.array('h');a.frombytes(pcm);peak=max(abs(x)for x in a)/32768;rms=math.sqrt(sum(x*x for x in a)/len(a))/32768;assert rms>.00001 and peak<.9999,(label,peak,rms)
 nativefps=(T[-1]['frames']-T[0]['frames'])/(T[-1]['wall']-T[0]['wall']);base='/review/current/waves-layers-1102/'+label;files[base+'.mp4']=str(movie.resolve());chapters=[];events=report['events'];assert sorted(e['i']for e in events)==list(range(q['expected']))
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
 materialFrames=sorted(set(t['layers']['clock']['bed']['frame'] for t in T if t['layers']['clock'].get('bed')));teslaFrames=sorted(set(t['layers']['clock']['tesla']['frame'] for t in T if t['layers']['clock'].get('tesla')));assert stage==1 or not report['scenery']['material'] or report['scenery']['material'].get('frames',1)<=1 or len(materialFrames)>1,(label,materialFrames)
 levels.append(dict(id=label,nativeFPS=round(nativefps,2),performanceNote=('Visible native capture/render slowdown' if nativefps<30 else None),stage=stage,route=route if stage==6 else None,title='Stage '+str(stage)+(' / '+('Harrier route'if route=='left'else'Rebel route')if stage==6 else''),tab='Stage '+str(stage)+(' · '+('Harrier'if route=='left'else'Rebels')if stage==6 else''),biome=biomes[stage-1],routeLabel=('Harrier route'if route=='left'else'Rebel route')if stage==6 else None,video=base+'.mp4',poster=chapters[0]['poster'],seconds=meta['duration'],waves=chapters));receipts.append(dict(label=label,seconds=meta['duration'],chapters=len(chapters),nativeFPS=round(nativefps,2),decoded=True,audioPeak=peak,audioRMS=rms,sourceHashes=report['sourceHashes'],methodSourceHash=report['methodSourceHash'],materialFrames=materialFrames,teslaFrames=teslaFrames,recordedAt=report['recordedAt'],sceneryAssetHashes=report['sceneryAssetHashes'],maxSampleGap=round(max(b['wall']-a['wall'] for a,b in zip(T,T[1:])),3),captureCodec=report.get('captureCodec','VP9/Opus'),qaOverrides=report.get('qaOverrides',[])))
data=dict(title='Every regular wave',difficulty='furious',levels=levels,uniqueScheduledWaves=sum(len(l['waves'])for l in levels if l['id']!='stage-6-right'),chapterCount=sum(len(l['waves'])for l in levels),seconds=round(sum(l['seconds']for l in levels),2),stageX='Boss encounters only; excluded');p=P/'all-waves.json';p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');files['/current/all-waves-1101.json']=str(p.resolve());files['/current/all-waves-1101.html']=str(page.resolve())
(P/'receipts.json').write_text(json.dumps(dict(clips=receipts,files=files,seconds=data['seconds'],chapterCount=data['chapterCount']),indent=2));assert data['uniqueScheduledWaves']==260 and data['chapterCount']==313
# Keep old page/data as a review archive, and never alter downloaded old films.
for name in ['all-waves-1101.html','all-waves-1101.json']:
 old=TARGET/name;backup=W/('previous-'+name)
 if old.exists() and not backup.exists():shutil.copyfile(old,backup)
for url,source in files.items():
 if url.startswith('/review/current/waves-layers-1102/'):
  dest=D/url.lstrip('/');assert dest.resolve().is_relative_to(MEDIA.resolve());shutil.copyfile(source,dest)
pageText=page.read_text(encoding='utf-8').replace('href="/enemy-showcase-1031.html"','href="/review/enemy-showcase-1031.html"').replace("fetch('/current/all-waves-1101.json')","fetch('/review/current/all-waves-1102.json?layers=1102')").replace('FURIOUS · NATIVE COMBAT · INVULNERABLE OBSERVER','NEW LAYERED STAGES · NOVEMBER 2 · FURIOUS · INVULNERABLE OBSERVER').replace('Original level scenery, authored wave order','New layered stage scenery, authored wave order')
pageText=pageText.replace("(current.routeLabel||current.biome);selectWave","(current.routeLabel||current.biome)+(current.performanceNote?' · Performance issue: '+current.nativeFPS+' native fps':'');selectWave")
pageText=pageText.replace('<title>','<link rel="icon" href="data:,"><title>',1)
page.write_text(pageText,encoding='utf8')
data['recordedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat();data['sceneryRevision']='layered-stages-1102';data['sceneryNote']='Fresh native recordings with current stage layers. Stage1 retains its approved original scenery.'
# Output all data atomically after every film has decoded and every chapter exists.
for name in ['all-waves-1101.json','all-waves-1102.json']:
 tmp=TARGET/(name+'.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8');tmp.replace(TARGET/name)
for name in ['all-waves-1101.html','all-waves-1102.html']:
 tmp=TARGET/(name+'.tmp');tmp.write_text(pageText,encoding='utf8');tmp.replace(TARGET/name)
(P/'all-waves.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
print(json.dumps({'levels':len(levels),'chapters':data['chapterCount'],'seconds':data['seconds'],'url':'http://127.0.0.1:63094/review/current/all-waves-1101.html?layers=1102'},indent=2))
