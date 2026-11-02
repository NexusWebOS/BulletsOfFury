"""Decode and seek each published movie through its actual browser URL."""
from pathlib import Path
import json,sys,urllib.request
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_comparison_1102';url='http://127.0.0.1:8805';manifest=json.load(urllib.request.urlopen(url+'/current/boss-comparison-1102/manifest.json'));file=O/'playback-checks.json';out=json.loads(file.read_text())if file.exists()else{}
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1000,'height':800});p.goto(url+'/current/boss-comparison-1102.html',wait_until='load');p.evaluate('''()=>{for(const v of document.querySelectorAll('video')){v.pause();v.removeAttribute('src');v.load();}window.libraryVideo=document.createElement('video');libraryVideo.muted=true;libraryVideo.preload='metadata';document.body.append(libraryVideo);window.libraryCanvas=document.createElement('canvas');libraryCanvas.width=320;libraryCanvas.height=200;}''')
 for j in manifest['jobs']:
  if not j.get('passed'):continue
  key=j['difficulty']+'-'+j['id'];previous=out.get(key)
  if previous and previous.get('passed')and previous.get('path')==j['path']:continue
  try:
   row=p.evaluate('''async job=>{const v=libraryVideo;v.pause();v.removeAttribute('src');v.load();v.src=job.video;v.load();await Promise.race([new Promise((r,e)=>{v.onloadedmetadata=r;v.onerror=()=>e(Error(v.error?.message||'Video failed'));}),new Promise((r,e)=>setTimeout(()=>e(Error('Metadata timeout')),18000))]);const frames=[];for(const fraction of [.2,.55,.9]){const t=Math.min(v.duration-.3,Math.max(.2,v.duration*fraction));await Promise.race([new Promise((r,e)=>{v.onseeked=r;v.currentTime=t;}),new Promise((r,e)=>setTimeout(()=>e(Error('Seek timeout')),18000))]);const g=libraryCanvas.getContext('2d',{willReadFrequently:true});g.drawImage(v,0,0,320,200);const a=g.getImageData(0,0,320,200).data;let n=0,sum=0,sum2=0;for(let i=0;i<a.length;i+=16){const x=(a[i]+a[i+1]+a[i+2])/3;sum+=x;sum2+=x*x;n++;}frames.push({t,variance:sum2/n-(sum/n)**2});}return{duration:v.duration,width:v.videoWidth,height:v.videoHeight,frames,error:v.error?.message||null};}''',j)
   row['passed']=not row['error']and row['width']>=480 and len(row['frames'])==3 and all(f['variance']>10 for f in row['frames'])and abs(row['duration']-j['seconds'])<4
  except Exception as e:row=dict(passed=False,error=str(e))
  row.update(path=j['path'],video=j['video']);out[key]=row;file.write_text(json.dumps(out,indent=2));print('PASS'if row['passed']else'FAIL',key,row.get('error')or'',flush=True)
 b.close()
print('SUMMARY',sum(r.get('passed',False)for r in out.values()),'/',len(out),flush=True);sys.exit(0 if all(r.get('passed')for r in out.values())else 1)
