from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.request import Request,urlopen
import json
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/cinematic_rework_1114'
movies=json.loads((OUT/'movies.json').read_text(encoding='utf-8'))['movies'];errors=[];checks=[]
url='http://127.0.0.1:8766/_shots/cinematic_rework_1114/'
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function('[...document.querySelectorAll("video")].every(v=>v.readyState>=1)')
 for m in movies:
  q=p.evaluate('id=>{const v=document.getElementById(id);return{w:v.videoWidth,h:v.videoHeight,duration:v.duration};}',m['key'])
  checks.append({'name':m['key']+' complete geometry/duration','ok':q['w']==1824 and q['h']==1024 and abs(q['duration']-m['duration'])<.2,'data':q})
  for c in m['chapters']:
   print('Check '+m['key']+' '+c['title'],flush=True)
   p.locator('button').filter(has_text=c['title']).click()
   p.wait_for_function('q=>{const v=document.getElementById(q.id);return Math.abs(v.currentTime-q.start)<1.5&&!v.paused&&!v.seeking;}',arg={'id':m['key'],'start':c['start']})
   t=p.evaluate('async id=>{const v=document.getElementById(id);return await new Promise(r=>v.requestVideoFrameCallback((_,m)=>r(m.mediaTime)));}',m['key'])
   checks.append({'name':m['key']+' '+c['title']+' decoded browser frame','ok':abs(t-c['start'])<2,'data':t})
  p.evaluate('id=>document.getElementById(id).pause()',m['key'])
 p.screenshot(path=str(OUT/'review-browser.png'),full_page=True);b.close()
with urlopen(Request(url+movies[1]['file'],headers={'Range':'bytes=0-255'}))as r:
 q={'status':r.status,'bytes':len(r.read()),'contentRange':r.headers.get('Content-Range')}
 checks.append({'name':'movie byte range delivery','ok':q['status']==206 and q['bytes']==256,'data':q})
checks.append({'name':'no browser/page/HTTP errors','ok':not errors,'data':errors})
(OUT/'browser-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8')
print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' browser movie checks passed',flush=True)
assert all(c['ok']for c in checks)
