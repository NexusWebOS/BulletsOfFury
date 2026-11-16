from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.request import Request,urlopen
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'_shots/city_rescue_1115';url='http://127.0.0.1:8766/_shots/city_rescue_1115/'
q=json.loads((O/'recording.json').read_text(encoding='utf8'));checks=[];errors=[]
def ck(n,v,data=None):
 checks.append({'name':n,'ok':bool(v),'data':data})
 if not v:print('FAIL',n,str(data)[:800],flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(30000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function("Array.from(document.querySelectorAll('video')).every(v=>v.readyState>=1)")
 p.evaluate("async()=>{window.qaAC=new AudioContext();await qaAC.resume();window.qaAnal={};for(const v of document.querySelectorAll('video')){const a=qaAC.createAnalyser();a.fftSize=2048;qaAC.createMediaElementSource(v).connect(a);a.connect(qaAC.destination);qaAnal[v.id]=a;}}")
 for m in q['movies']:
  part=m['part'];v=p.evaluate("id=>{const v=document.getElementById(id);return{w:v.videoWidth,h:v.videoHeight,duration:v.duration};}",part)
  ck(part+' full geometry/duration',v['w']==1824 and v['h']==1024 and abs(v['duration']-m['duration'])<.2,v);peak=0
  for c in m['chapters']:
   p.locator('button[data-player="'+part+'"]').filter(has_text=c['title']).click()
   p.wait_for_function("([id,t])=>{const v=document.getElementById(id);return Math.abs(v.currentTime-t)<1.5&&!v.paused&&!v.seeking;}",arg=[part,c['start']])
   t=p.evaluate("async id=>await new Promise(r=>document.getElementById(id).requestVideoFrameCallback((_,m)=>r(m.mediaTime)))",part)
   ck(part+': '+c['title']+' decoded chapter',abs(t-c['start'])<2,t)
   a=p.evaluate("async id=>{const a=qaAnal[id],b=new Float32Array(2048);let peak=0;for(let i=0;i<12;i++){await new Promise(r=>setTimeout(r,20));a.getFloatTimeDomainData(b);for(const v of b)peak=Math.max(peak,Math.abs(v));}return peak;}",part);peak=max(peak,a)
  ck(part+' decoded audio',peak>.001,peak);p.evaluate("id=>document.getElementById(id).pause()",part)
  with urlopen(Request(url+m['file'],headers={'Range':'bytes=0-255'}))as r:ck(part+' byte-range seeking',r.status==206 and len(r.read())==256)
 p.wait_for_function('Array.from(document.images).every(im=>im.complete&&im.naturalWidth>0)');ck('both generated medals decoded',p.locator('.medals img').count()==2)
 p.screenshot(path=str(O/'browser-preview.png'),full_page=True);b.close()
ck('recording source hashes match installed build',all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in q['coreAfter'].items())and q['coreBefore']==q['coreAfter'])
for c in q['clips']:
 if c['part']=='split':
  ck('split records all four native Storm pursuit briefing lines',len([s for s in c['stages']if':route-left:LINE-'in s['tag']])==4)
 elif c['part']=='city':
  ck('all six city conversations and album recorded',len([s for s in c['stages']if s['tag'].startswith('cutscene:post-city16:')])==7)
  ck('city continuation preserves verified result and unlocks7 after debrief',c['end']['city']['verified']and c['end']['city']['debriefSeen']and c['end']['city']['travelSeen']and c['end']['cap']>=7)
 else:
  ck(c['part']+' all eight post6 beats recorded',len([s for s in c['stages']if s['tag'].startswith('cutscene:post-6:')])==8)
  r=c['end']['receipt'];ck(c['part']+' native map continuation once and right opponent saved',r['verified']and r['awardNotified']and r['transitSeen']and r['messageSeen']and r['target']==('rebels'if c['part']=='storm'else'harrier'))
ck('no recording/review page/console/HTTP errors',not errors and not q['errors'],errors)
(O/'browser-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8')
print(str(sum(v['ok']for v in checks))+'/'+str(len(checks))+' movie/browser checks passed',flush=True)
assert all(v['ok']for v in checks)
