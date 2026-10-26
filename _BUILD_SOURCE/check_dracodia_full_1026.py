"""Verify the complete native-input film, health ledger, decoded media and browser seeking."""
from pathlib import Path
import json,re,subprocess,sys
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
F=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'_shots/dracodia_forms_1026/full/stage8'
r=json.loads((F/'report.json').read_text());rows=r['timeline'];checks={};chapters={}
def ck(k,v):checks[k]=bool(v);print(('PASS 'if v else'FAIL ')+k,flush=True)
ck('Full fight reaches native defeat',r['completed']and r['reason']=='native defeat')
ck('No game, browser, bot or asset errors',not any(r[k]for k in ['pageErrors','consoleErrors','assetErrors'])and all(not q['botErrors']for q in rows))
ck('Furious input-only observer and native audio',r['difficulty']=='furious'and all(q['god']for q in rows)and r['audio']['tapped']>5 and not r['audio']['tapErrors'])
final=[q for q in rows if q['phase']==2 and q['dracodia']]
locked=[q for q in final if q['form']==0 and q['mode']=='fight'and q['dracodia']['locked']]
ck('Early base health and both arms stay intact',bool(locked)and all(q['hp']==5330 and q['dracodia']['pools']['0']==5330 and all(not p['destroyed']for p in q['parts'])for q in locked))
for f in [8,1,6,2]:
 live=[q for q in final if q['form']==f and q['mode']=='fight']
 ck('Copy '+str(f)+' fights and dies through native input',bool(live)and any(q['dracodia']['pools'][str(f)]<=0 for q in final))
 if live:chapters[{8:'hammer',1:'helicopter',6:'neural-archon',2:'phoenix'}[f]]=live[0]['seconds']+2
opened=next((q for q in final if q['form']==0 and q['mode']=='fight'and not q['dracodia']['locked']),None)
ck('Final life opens only after every copied pool is empty',opened and all(opened['dracodia']['pools'][str(f)]==0 for f in [8,1,6,2]))
ck('Final life is played down to zero',bool(opened)and final[-1]['dracodia']['pools']['0']==0)
ck('Arms cannot break before the final life',all(q['dracodia']['unlocked'] for q in final if q['form']==0 and any(p['destroyed']for p in q.get('parts',[]))))
if opened:chapters['final-life']=opened['seconds']+1
first=next(q for q in rows if q['phase']==0 and q['mode']=='fight');chapters['first-host']=first['seconds']+1
rebirth=next(q for q in rows if q['mode']=='dr5er23rebirth');chapters['dna-rise']=rebirth['seconds']+10;chapters['lightning-download']=rebirth['seconds']+21
fusion=next(q for q in final if q['mode']=='v18formIn');chapters['copy-fusion']=fusion['seconds']+.8
chapters['entrance']=8;chapters['defeat']=next(q['seconds']for q in rows if q['mode']=='dr5Death')+1
fps=(rows[-1]['nativeFrames']-rows[0]['nativeFrames'])/(rows[-1]['seconds']-rows[0]['seconds']);ck('Native animation averages at least 55fps',fps>=55)
video=F/'stage8-furious.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
proc=subprocess.run([ff,'-hide_banner','-i',str(video),'-af','volumedetect','-f','null','-'],capture_output=True,text=True)
(F/'decode.log').write_text(proc.stderr,encoding='utf8');ck('Entire movie decodes cleanly',proc.returncode==0 and 'Error'not in proc.stderr)
match=re.search(r'max_volume: ([\-\d.]+) dB',proc.stderr);peak=float(match[1])if match else -999
ck('Recorded audio is audible without clipping',-30<peak<0)
frames=F/'decoded';frames.mkdir(exist_ok=True)
for key,t in chapters.items():
 subprocess.run([ff,'-v','error','-ss',str(t),'-i',str(video),'-frames:v','1','-y',str(frames/(key+'.png'))],check=True)
url='http://127.0.0.1:53746/'+video.relative_to(ROOT).as_posix();errors=[]
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto(url,wait_until='domcontentloaded');p.wait_for_function('document.querySelector("video")?.readyState>=2',timeout=60000)
 meta=p.evaluate('()=>{const v=document.querySelector("video");return{w:v.videoWidth,h:v.videoHeight,duration:v.duration}}')
 ck('Film contains full captured duration at 1280x800',meta['w']==1280 and meta['h']==800 and abs(meta['duration']-rows[-1]['seconds'])<3)
 for key,t in chapters.items():
  p.evaluate('(t)=>{const v=document.querySelector("video");v.pause();v.currentTime=t}',t)
  p.wait_for_function('(t)=>{const v=document.querySelector("video");return !v.seeking&&Math.abs(v.currentTime-t)<.12}',arg=t)
  p.evaluate('async()=>{const v=document.querySelector("video");v.muted=false;await v.play()}');p.wait_for_function('(t)=>document.querySelector("video").currentTime>t+.2',arg=t)
  ck(key+' seeks and plays with audio',p.evaluate('()=>{const v=document.querySelector("video");v.pause();return !v.error&&!v.muted&&v.getVideoPlaybackQuality().totalVideoFrames>2}'))
 response=p.request.get(url,headers={'Range':'bytes=1000-1999'});ck('Byte-range seeking',response.status==206 and len(response.body())==1000)
 ck('Playback has no browser errors',not errors);br.close()
result={'checks':checks,'passed':sum(checks.values()),'failed':sum(not v for v in checks.values()),'chapters':dict(sorted(chapters.items(),key=lambda a:a[1])),'fps':fps,'peakDb':peak,'metadata':meta,'video':str(video),'url':url,'errors':errors}
(F/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result));raise SystemExit(0 if all(checks.values())else 1)
