from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.request import Request,urlopen
import json
R=Path('D:/BOF-Downloads/2026-11-14/RevG-source');O=R/'_shots/hq_swarm_1115';url='http://127.0.0.1:8766/_shots/hq_swarm_1115/'
q=json.loads((O/'recording.json').read_text(encoding='utf8'));checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:800],flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function("Array.from(document.querySelectorAll('video')).every(v=>v.readyState>=1)")
 p.evaluate("async()=>{window.qaAC=new AudioContext();await qaAC.resume();window.qaAnal={};for(const v of document.querySelectorAll('video')){const a=qaAC.createAnalyser();a.fftSize=2048;qaAC.createMediaElementSource(v).connect(a);a.connect(qaAC.destination);qaAnal[v.id]=a;}}")
 for m in q['movies']:
  part=m['part'];v=p.evaluate("id=>{const v=document.getElementById(id);return{w:v.videoWidth,h:v.videoHeight,duration:v.duration};}",part)
  ck(part+' video geometry and complete duration',v['w']==1824 and v['h']==1024 and abs(v['duration']-m['duration'])<.2,v)
  peak=0
  for c in m['chapters']:
   p.locator('button[data-player="'+part+'"]').filter(has_text=c['title']).click()
   p.wait_for_function("([id,t])=>{const v=document.getElementById(id);return Math.abs(v.currentTime-t)<1.5&&!v.paused&&!v.seeking;}",arg=[part,c['start']])
   t=p.evaluate("async id=>await new Promise(r=>document.getElementById(id).requestVideoFrameCallback((_,m)=>r(m.mediaTime)))",part)
   ck(part+': '+c['title']+' decoded chapter',abs(t-c['start'])<2,t)
   a=p.evaluate("async id=>{const a=qaAnal[id],b=new Float32Array(2048);let peak=0;for(let i=0;i<12;i++){await new Promise(r=>setTimeout(r,20));a.getFloatTimeDomainData(b);for(const v of b)peak=Math.max(peak,Math.abs(v));}return peak;}",part)
   peak=max(peak,a)
  ck(part+' media audio decoded and audible',peak>.001,peak)
  p.evaluate("id=>document.getElementById(id).pause()",part)
  with urlopen(Request(url+m['file'],headers={'Range':'bytes=0-255'}))as r:ck(part+' byte-range seeking',r.status==206 and len(r.read())==256)
 p.locator('summary').click();p.wait_for_function('Array.from(document.images).every(im=>im.complete&&im.naturalWidth>0)')
 ck('both native somersault GIF previews decoded',p.locator('.gallery img').count()==2)
 p.screenshot(path=str(O/'browser-preview.png'),full_page=True);b.close()
stage=next(c for c in q['clips']if c['part']=='stage67')
ck('all eleven post6 beats recorded without skips',len(stage['expectedBeats'])==11 and all(any(':'+v['id']+':'in t['tag']for t in stage['stages'])for v in stage['expectedBeats']))
ck('both Stage7 approach panels and continuous native entry recorded',all(any(v in t['tag']for t in stage['stages'])for v in [':A701:',':ARRIVAL7-02:','launch:::run:','launch:::brake:','launch:::settle:','launch:::cd:','play:']))
ck('post6 completed once and handed to Stage7 gameplay',stage['end']['post6Done']==1 and stage['end']['state']=='play'and stage['end']['stage']==7 and stage['end']['brief'],stage['end'])
ck('no recording or review browser/page/HTTP errors',not errors and not q['errors'],errors)
(O/'browser-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8')
print(str(sum(v['ok']for v in checks))+'/'+str(len(checks))+' movie/browser checks passed',flush=True)
assert all(v['ok']for v in checks)
