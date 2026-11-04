from pathlib import Path
import re,json,hashlib,subprocess,array,math,shutil,datetime,statistics,os
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent
O=R/'_shots/waves_observe_1102';P=O/'publication';P.mkdir(exist_ok=True)
D=Path(r'C:/Users/Mike/Documents/New project/BOF-GitHub-Download-1102');TARGET=D/'review/current';MEDIA=TARGET/'waves-observe-1102';MEDIA.mkdir(exist_ok=True)
guide=json.loads((D/'review/enemy-showcase-1031/manifest.json').read_text(encoding='utf8'));ff=imageio_ffmpeg.get_ffmpeg_exe();levels=[];receipts=[];files={}
biomes=['Jungle Coast','Volcanic Pass','Frozen Islands','Desert Highway','Orbital Rift','Storm Front','Toxic Sewers','Alien Hive','Waterworld']
for stage,route in [(s,r)for s in range(1,10)for r in (['left','right']if s==6 else ['left'])]:
 label='stage-'+str(stage)+('-right'if stage==6 and route=='right'else '')
 choices=[p.parent for p in O.glob(label+'*/verified.json') if json.loads(p.read_text()).get('label')==label and not json.loads(p.read_text()).get('excluded')]
 assert choices,'Missing completed inspection: '+label
 V=max(choices,key=lambda p:(p/'verified.json').stat().st_mtime);report=json.loads((V/'report.json').read_text(encoding='utf8'));T=report['trace'];q=report['result']
 assert q['done'] and len(report['events'])==q['expected'] and len(report['waveMeta'])==q['expected'],label
 assert all(not t['dead'] and t['god'] and not t['boss'] and not t['mini'] for t in T),label
 assert not report['errors'] and not report['httpErrors'] and not report['stats']['tapErrors'],label
 assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in report['sourceHashes'].items()),label+' source changed'
 movie=V/('stage-'+str(stage)+'-waves.mp4');subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
 reader=imageio_ffmpeg.read_frames(str(movie));meta=next(reader);reader.close();assert meta['codec']=='h264' and meta['audio_codec']=='aac'
 pcm=subprocess.run([ff,'-v','error','-i',str(movie),'-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout;a=array.array('h');a.frombytes(pcm);peak=max(map(abs,a))/32768;rms=math.sqrt(sum(v*v for v in a)/len(a))/32768;assert rms>.00001 and peak<.9999,(label,peak,rms)
 movieSHA=hashlib.sha256(movie.read_bytes()).hexdigest();assetTag=label+'-'+movieSHA[:10];base='/review/current/waves-observe-1102/'+assetTag;files[base+'.mp4']=str(movie);chapters=[]
 for n,e in enumerate(report['events']):
  m=report['waveMeta'][n];assert m['i']==e['i'] and m['cleanup'] is not None and m['end'] is not None
  observed=m['observeUntil']-m['clock'];assert observed>=8-1e-6,(label,n,observed)
  start=max(0,e['video']-.1);cleanup=max(start,min(meta['duration'],m['cleanup']));end=min(meta['duration'],m['end']);assert start<end
  types=list(dict.fromkeys((e['types'] or e['spawns'])+[u['type'] for u in report['units'] if u.get('wave')==e['i'] and u.get('firstVisible') is not None]));names=[]
  for unit in e.get('units',[])+[u for u in report['units'] if u.get('wave')==e['i'] and u.get('firstVisible') is not None]:
   item=next((v for v in guide['items'] if v['stage']==stage and v['type']==unit['type'] and unit.get('model') and v.get('model')==unit['model']),None) or next((v for v in guide['items'] if v['stage']==stage and v['type']==unit['type']),None)
   if item and item['title']not in names:names.append(item['title'])
  if not names:
   for typ in types:
    item=next((v for v in guide['items'] if v['stage']==stage and v['type']==typ),None)
    if item and item['title']not in names:names.append(item['title'])
  seen=[u for u in report['units'] if u.get('wave')==e['i'] and u.get('firstVisible') is not None];special=e['meta'].get('_ca111');title={'pair-top':'Cloud carriers / northern approach','pair-bottom':'Cloud carriers / southern approach','nuclear':'Nuclear warhead carrier','laser':'Laser warhead carrier'}.get(special) or ' / '.join(names[:3]) or ('Native cue / no enemy spawned' if not types else 'Native formation')
  samples=[t for t in T if start<=t['wall']<=end];rates=[1000/t['perf']['frame']['mean']for t in samples if t['perf']['frame']['mean']>0]
  chapterFPS=(samples[-1]['frames']-samples[0]['frames'])/(samples[-1]['wall']-samples[0]['wall'])if len(samples)>1 else (statistics.mean(rates)if rates else 0);perf={'meanFPS':round(chapterFPS,2),'lowestWindowFPS':round(min(rates),2)if rates else None,'peakEnemies':max((t['input']['visible'] for t in samples if t['input']),default=0),'peakShots':max((t['input']['bullets'] for t in samples if t['input']),default=0),'worstUpdateP95':round(max((t['perf']['update']['p95']for t in samples),default=0),2),'worstDrawP95':round(max((t['perf']['draw']['p95']for t in samples),default=0),2)}
  poster=P/(assetTag+'-wave-'+str(n+1).zfill(2)+'.jpg');at=min(end-.1,start+min(4,(cleanup-start)*.5));subprocess.run([ff,'-v','error','-y','-ss',str(at),'-i',str(movie),'-frames:v','1','-vf','scale=320:200','-q:v','2',str(poster)],check=True)
  post=base+'-wave-'+str(n+1).zfill(2)+'.jpg';files[post]=str(poster);chapters.append({'number':n+1,'title':title,'start':round(start,3),'cleanup':round(cleanup,3),'end':round(end,3),'observeSeconds':round(observed,2),'visibleUnits':len(seen),'noVisibleEnemy':not bool(seen),'inspectionNote':('Cleanup blocked; inspection cut without a native defeat' if m.get('blocked') else 'No visible enemy: native release requires review' if not seen and types else 'Native cue produced no enemy' if not seen else None),'blockedCleanup':m.get('blocked'),'poster':post,'planned':e['planned'],'types':types,'performance':perf})
 fps=(T[-1]['frames']-T[0]['frames'])/(T[-1]['wall']-T[0]['wall'])
 levels.append({'id':label,'stage':stage,'route':route if stage==6 else None,'title':'Stage '+str(stage)+(' / '+('Harrier route'if route=='left'else'Rebel route')if stage==6 else ''),'tab':'Stage '+str(stage)+(' Â· '+('Harrier'if route=='left'else'Rebels')if stage==6 else ''),'biome':biomes[stage-1],'routeLabel':('Harrier route'if route=='left'else'Rebel route')if stage==6 else None,'video':base+'.mp4','poster':chapters[0]['poster'],'seconds':meta['duration'],'waves':chapters,'nativeFPS':round(fps,2),'performanceNote':'Measured capture/render slowdown'if fps<30 else None})
 receipts.append({'label':label,'seconds':meta['duration'],'chapters':len(chapters),'nativeFPS':round(fps,2),'audioPeak':peak,'audioRMS':rms,'firstFire':q['firstFire'],'peakEnemies':q['peakEnemies'],'peakBullets':q['peakBullets'],'godBlocks':q['godBlocks'],'earlyDamage':report['earlyDamage'],'policy':report['policy'],'sourceHashes':report['sourceHashes'],'methodSourceHash':report['methodSourceHash'],'noVisibleEnemy':[w['number'] for w in chapters if w['noVisibleEnemy']],'blockedCleanup':[w['number']for w in chapters if w['blockedCleanup']],'compiledFrom':report.get('compiledFrom'),'observationDamageSample':[d for d in report['earlyDamage'] if d['phase']=='OBSERVE'],'sha256':movieSHA,'folder':str(V)})
 print('VERIFIED',label,len(chapters),round(meta['duration'],2),'seconds',flush=True)
data={'title':'Paced wave inspections','difficulty':'furious','god':True,'pacing':'Observe each native wave, then clear and advance. Camera seeks between cleared groups; not campaign timing.','levels':levels,'uniqueScheduledWaves':sum(len(l['waves'])for l in levels if l['id']!='stage-6-right'),'chapterCount':sum(len(l['waves'])for l in levels),'seconds':round(sum(l['seconds']for l in levels),2),'sceneryRevision':'layered-stages-1102','inspectionRevision':'observe-clear-1102','recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
assert data['chapterCount']==313 and data['uniqueScheduledWaves']==260
text=(R/'_BUILD_SOURCE/waves_viewer_1101.html').read_text(encoding='utf8')
text=text.replace('<title>','<link rel="icon" href="data:,"><title>',1).replace('href="/enemy-showcase-1031.html"','href="/review/enemy-showcase-1031.html"')
text=text.replace('Every regular wave','Paced wave inspections').replace('Review each levelâ€™s formations in game. Choose a level, then a waveâ€”or watch the full recording. Boss and miniboss encounters are excluded.','Each wave demonstrates its native movement and attacks before cleanup. Furious difficulty, native god mode. Choose a chapter to inspect it; use the cleanup button to skip ahead when ready.')
text=text.replace('FURIOUS Â· NATIVE COMBAT Â· INVULNERABLE OBSERVER','FURIOUS Â· GOD MODE Â· OBSERVE â†’ CLEAR â†’ NEXT WAVE')
text=text.replace('Original level scenery, authored wave order, enemy AI, damage and game audio. Finite wave review; endless adaptive reinforcements are held so the scheduled formations can be inspected. The pilot is invulnerable.','Paced inspection: the next scheduled wave waits while the current group demonstrates its native AI, then the bot clears it. Camera seeks between cleared groups use their original release locations. Endless extras and allied weapons during observation are held. These recordings do not reproduce normal campaign overlap or prove every pattern is human-avoidable.')
text=text.replace("fetch('/current/all-waves-1101.json')","fetch('/review/current/all-waves-inspection-1102.json?v=1')")
text=text.replace('<nav id="levels"', '<p class="meta">Stage 7 has recorded rendering stalls. Native entries with no visible enemy are flagged in their chapters.</p><nav id="levels"',1)
text=text.replace('regular-wave chapters in their original order.','scheduled chapters in inspection order, with camera cuts between groups.').replace(' · Full level',' · Full inspection')
text=text.replace('Watch full level','Watch full inspection').replace('<button id="prev">','<button id="observe">Replay observation</button><button id="cleanup">Jump to cleanup</button><button id="prev">',1)
text=text.replace("textContent=w.title;for(const b", "textContent=w.title+' Â· '+w.observeSeconds+'s observation Â· '+w.performance.meanFPS+' fps Â· peak '+w.performance.peakEnemies+' enemies / '+w.performance.peakShots+' shots'+(w.inspectionNote?' · '+w.inspectionNote:'');for(const b")
text=text.replace("(current.routeLabel||current.biome);selectWave","(current.routeLabel||current.biome)+(current.performanceNote?' Â· '+current.performanceNote+' ('+current.nativeFPS+' fps)':'');selectWave")
text=text.replace("video.addEventListener('timeupdate'", "document.querySelector('#observe').onclick=()=>selectWave(index);document.querySelector('#cleanup').onclick=()=>{whole=false;full.setAttribute('aria-pressed','false');video.currentTime=current.waves[index].cleanup;video.play().catch(e=>{if(e.name!=='AbortError')console.error(e)})};\nvideo.addEventListener('timeupdate'",1)
text=re.sub(r'<div class="tag">.*?</div>', '<div class="tag">FURIOUS &middot; GOD MODE &middot; OBSERVE &rarr; CLEAR &rarr; NEXT WAVE</div>',text,count=1)
text=re.sub(r'(<h1>.*?</h1>)<p>.*?</p>',r'\1<p>Each scheduled wave demonstrates native movement and attacks before cleanup. Furious difficulty, native GOD mode. Camera cuts separate the inspections.</p>',text,count=1)
for name in ['all-waves-1101.html','all-waves-1101.json']:
 backup=W/('before-inspection-'+name)
 if not backup.exists():shutil.copyfile(TARGET/name,backup)
for url,source in files.items():
 dest=D/url.lstrip('/');assert dest.resolve().is_relative_to(MEDIA.resolve());
 if not dest.exists():os.link(source,dest)
 else:assert hashlib.sha256(dest.read_bytes()).hexdigest()==hashlib.sha256(Path(source).read_bytes()).hexdigest()
for name in ['all-waves-inspection-1102.json','all-waves-1101.json']:
 temp=TARGET/(name+'.tmp');temp.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8');temp.replace(TARGET/name)
for name in ['all-waves-inspection-1102.html','all-waves-1101.html']:
 temp=TARGET/(name+'.tmp');temp.write_text(text,encoding='utf8');temp.replace(TARGET/name)
(P/'index.html').write_text(text,encoding='utf8');(P/'all-waves.json').write_text(json.dumps(data,indent=2),encoding='utf8');(P/'receipts.json').write_text(json.dumps({'clips':receipts,'files':files,'seconds':data['seconds'],'chapterCount':data['chapterCount']},indent=2),encoding='utf8')
print(json.dumps({'films':10,'chapters':313,'seconds':data['seconds'],'url':'http://127.0.0.1:63094/review/current/all-waves-1101.html?inspection=1102'},indent=2))
