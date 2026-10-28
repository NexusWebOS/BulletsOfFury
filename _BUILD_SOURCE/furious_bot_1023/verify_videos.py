from pathlib import Path
import json,subprocess,re,imageio_ffmpeg,sys,os
W=Path(__file__).resolve().parent;O=Path(os.environ.get('BOF_CAPTURE_DIR',str(W/'review')));ff=imageio_ffmpeg.get_ffmpeg_exe();jobs=json.loads((W/'jobs.json').read_text());checks=[]
only=set(sys.argv[1:])
if only and(O/'video-verification.json').exists():checks=[c for c in json.loads((O/'video-verification.json').read_text())['checks']if c['id']not in only]
for j in jobs:
 slug=j['id'];p=O/(slug+'.json')
 if only and slug not in only:continue
 if not p.exists():continue
 q=json.loads(p.read_text());video=O/(slug+'-seek.webm')
 if not q.get('completed')or not video.exists():continue
 # Decode the actual saved streams completely; a valid first frame is not enough.
 r=subprocess.run([ff,'-hide_banner','-threads','1','-i',str(video),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True)
 a=subprocess.run([ff,'-hide_banner','-threads','1','-i',str(video),'-t','12','-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
 mean=re.findall(r'mean_volume: ([-\w.]+) dB',a.stderr);size=re.search(r'Video:.*? (\d{3,4})x(\d{3,4})',r.stderr)
 bad=[s for s in r.stderr.splitlines()if re.search(r'error|invalid|corrupt|failed',s,re.I)]
 row={'id':slug,'complete':q.get('reason')=='native-defeat','fullDecodeExit':r.returncode,'decodeErrors':bad,'size':[int(v)for v in size.groups()]if size else None,'audioMeanDB':mean[-1]if mean else None,'audioPresent':'Audio: opus'in r.stderr,'difficulty':q.get('difficulty'),'protectedContacts':q.get('stats',{}).get('protectedContacts'),'noDiagnosticEngineUpdate':not any(e.get('type')=='diagnostic-engine-update'for e in q.get('events',[])), 'unhandledErrors':[e for e in q.get('pageErrors',[])if not e.startswith('Failed to load resource:')],'assetErrors':q.get('assetErrors',[]),'recoveredSummary':bool(q.get('recoveredFrom'))}
 row['pass']=row['complete']and r.returncode==0 and not bad and row['size']==[1280,720]and row['audioPresent']and row['audioMeanDB']not in[None,'-inf']and row['difficulty']=='furious'and row['noDiagnosticEngineUpdate']and not row['unhandledErrors']and not row['assetErrors']
 checks.append(row);(O/'video-verification.json').write_text(json.dumps({'verified':len(checks),'expected':len(jobs),'passed':sum(x['pass']for x in checks),'checks':checks},indent=2));print(slug,'PASS'if row['pass']else 'FAIL',flush=True)
print('VERIFIED',len(checks),'PASS',sum(q['pass']for q in checks),flush=True)
