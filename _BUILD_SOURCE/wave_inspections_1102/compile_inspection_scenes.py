"""Compile explicitly cut native inspection scenes. Preserve source receipts and raw films."""
from pathlib import Path
import json,copy,hashlib,datetime,subprocess,sys
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];O=R/'_shots/waves_observe_1102';ff=imageio_ffmpeg.get_ffmpeg_exe()
def latest(label,complete=True):
 choices=[]
 for p in O.glob(label+'*/report.json'):
  r=json.loads(p.read_text(encoding='utf8'))
  if r.get('label')!=label:continue
  if complete and not r['result']['done']:continue
  choices.append(p.parent)
 assert choices,label
 return max(choices,key=lambda p:(p/'report.json').stat().st_mtime)
def duration(p):
 r=imageio_ffmpeg.read_frames(str(p));m=next(r);r.close();return m['duration']
def compile_scenes(label,segments):
 V=O/(label+'-compiled-'+datetime.datetime.now().strftime('%H%M%S'));V.mkdir();events=[];waveMeta=[];trace=[];units=[];sources=[];parts=[];offset=0.;frames=0;reports=[];damage=[]
 for num,(folder,first,last)in enumerate(segments):
  r=json.loads((folder/'report.json').read_text(encoding='utf8'));reports.append(r);assert not r['errors'] and not r['httpErrors']
  selected=[e for e in r['events']if first<=e['i']<=last];assert [e['i']for e in selected]==list(range(first,last+1))
  ms=[r['waveMeta'][i]for i in range(first,last+1)];assert all(m and m['end']is not None and m['cleanup']is not None and m['observeUntil']-m['clock']>=8-1e-6 for m in ms)
  lo=0 if first==0 else ms[0]['start'];hi=ms[-1]['end'];assert hi>lo
  movie=folder/('stage-'+str(r['stage'])+'-waves.mp4');movie=movie if movie.exists()else folder/'capture.webm';part=V/('scene-'+str(num)+'.mp4')
  subprocess.run([ff,'-v','error','-y','-ss',str(lo),'-t',str(hi-lo),'-i',str(movie),'-vf','fps=30','-c:v','libx264','-crf','17','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(part)],check=True)
  length=duration(part);parts.append(part);shift=offset-lo
  for e in selected:
   e=copy.deepcopy(e);e['video']+=shift;events.append(e)
  for m in ms:
   m=copy.deepcopy(m)
   for k in ['start','cleanup','end']:m[k]=min(offset+length,m[k]+shift)
   waveMeta.append(m)
  tt=[t for t in r['trace']if lo<=t['wall']<=hi]
  if tt:
   f0=tt[0]['frames']
   for t in tt:
    t=copy.deepcopy(t);t['wall']+=shift;t['frames']=t['frames']-f0+frames;trace.append(t)
   frames=trace[-1]['frames']+1
  ids={}
  for u in r['units']:
   if u.get('wave')is None or not first<=u['wave']<=last:continue
   u=copy.deepcopy(u);ids[u['id']]=len(units);u['id']=len(units);u['sourceScene']=num;units.append(u)
  for d in r['earlyDamage']:
   if d['id']in ids:d=copy.deepcopy(d);d['id']=ids[d['id']];d['sourceScene']=num;damage.append(d)
  sources.append(dict(folder=str(folder),firstWave=first+1,lastWave=last+1,source=str(movie),sourceStart=lo,sourceEnd=hi,outputStart=offset,outputEnd=offset+length,methodSourceHash=r['methodSourceHash'],reportSHA256=hashlib.sha256((folder/'report.json').read_bytes()).hexdigest()))
  offset+=length
 N=len(events);assert [e['i']for e in events]==list(range(N));assert len(waveMeta)==N
 concat=V/'scenes.txt';concat.write_text(''.join("file '"+str(p).replace('\\','/')+"'\n"for p in parts),encoding='utf8');movie=V/('stage-'+str(reports[0]['stage'])+'-waves.mp4')
 subprocess.run([ff,'-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(movie)],check=True)
 subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],capture_output=True,check=True)
 base=copy.deepcopy(reports[0]);assert all(r['sourceHashes']==base['sourceHashes']for r in reports)
 base.update(label=label,folder=str(V),events=events,waveMeta=waveMeta,trace=trace,units=units,earlyDamage=damage,compiledFrom=sources,method='Native scene compilation with explicit cuts; no interpolation or enemy state editing',methodSourceHash=hashlib.sha256(json.dumps(sources,sort_keys=True).encode()).hexdigest(),recordedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
 base['result'].update(done=True,expected=N,events=N,wall=duration(movie),frames=frames,peakEnemies=max(t['input']['visible']for t in trace),peakBullets=max(t['input']['bullets']for t in trace))
 base['policy']['compilation']='Native repeated/continued scenes joined at cleared inspection boundaries. Source receipts retained.'
 (V/'report.json').write_text(json.dumps(base,indent=2),encoding='utf8');(V/'verified.json').write_text(json.dumps(dict(label=label,folder=str(V),movie=str(movie),done=True,sourceHashesMatch=True,newTerrain=base['stage']!=1,chapters=N,compiled=True),indent=2),encoding='utf8');print('COMPILED',label,N,round(duration(movie),2),flush=True);return V
if __name__=='__main__':
 if sys.argv[1]=='7':compile_scenes('stage-7',[(latest('stage-7',False),0,15),(latest('stage-7-tail-17'),16,21)])
 elif sys.argv[1]=='1':
  main=latest('stage-1');supp=latest('stage-1-supplement-17');r=json.loads((supp/'report.json').read_text(encoding='utf8'))
  if not any(u.get('firstVisible')is not None and u['type']=='modturret'for u in r['units']):print('Native repeat also produced no visible turret; retaining original flagged cue.');sys.exit(0)
  compile_scenes('stage-1',[(main,0,15),(supp,16,16),(main,17,35)])
