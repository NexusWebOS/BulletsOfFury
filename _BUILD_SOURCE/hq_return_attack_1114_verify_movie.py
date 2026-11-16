from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.request import Request,urlopen
import json
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/hq_return_attack_1114'
q=json.loads((OUT/'recording.json').read_text(encoding='utf-8'))['combined'];url='http://127.0.0.1:8766/_shots/hq_return_attack_1114/';checks=[];errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function('movie.readyState>=1');v=p.evaluate('({w:movie.videoWidth,h:movie.videoHeight,duration:movie.duration})')
 checks.append({'name':'complete video geometry and duration','ok':v['w']==1824 and v['h']==1024 and abs(v['duration']-q['duration'])<.2,'data':v})
 for c in q['chapters']:
  p.locator('button').filter(has_text=c['title']).click();p.wait_for_function('t=>Math.abs(movie.currentTime-t)<1.5&&!movie.paused&&!movie.seeking',arg=c['start'])
  t=p.evaluate('async()=>await new Promise(r=>movie.requestVideoFrameCallback((_,m)=>r(m.mediaTime)))')
  checks.append({'name':c['title']+' decoded chapter playback','ok':abs(t-c['start'])<2,'data':t})
 p.evaluate('movie.pause()');p.screenshot(path=str(OUT/'browser-preview.png'),full_page=True);b.close()
with urlopen(Request(url+q['file'],headers={'Range':'bytes=0-255'}))as r:checks.append({'name':'byte-range seeking','ok':r.status==206 and len(r.read())==256})
checks.append({'name':'no browser/page/HTTP errors','ok':not errors,'data':errors})
(OUT/'browser-qa.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' browser checks passed')
assert all(c['ok']for c in checks)
