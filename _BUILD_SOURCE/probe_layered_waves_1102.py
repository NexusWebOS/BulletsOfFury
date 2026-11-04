"""Real Chromium chapter seeking, decoded pixels, controls and responsive QA."""
from pathlib import Path
import json,urllib.request
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/waves_layers_1102/publication';U='http://127.0.0.1:63094/review';errors=[];checks=[]
data=json.load(urllib.request.urlopen(U+'/current/all-waves-1101.json'))
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text+' '+str(m.location)) if m.type=='error' else None)
 p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url) if r.status>=400 else None)
 p.goto(U+'/current/all-waves-1101.html?layers=1102',wait_until='networkidle');assert 'NEW LAYERED STAGES' in p.locator('.tag').inner_text();assert data['sceneryRevision']=='layered-stages-1102';p.wait_for_function('typeof library!=="undefined"&&library?.levels?.length===10')
 for level in data['levels']:
  assert '/waves-layers-1102/' in level['video'],level['video']
  p.locator('#levels button').filter(has_text=level['tab']).click();p.wait_for_function('id=>current.id===id&&video.readyState>=2',arg=level['id'])
  assert p.locator('#waves button').count()==len(level['waves'])
  for n in sorted(set([0,len(level['waves'])//2,len(level['waves'])-1])):
   w=level['waves'][n];p.locator('#waves button').nth(n).click();p.wait_for_function('t=>video.readyState>=2&&Math.abs(video.currentTime-t)<1',arg=w['start']);p.wait_for_timeout(200);p.evaluate('video.pause()')
   q=p.evaluate('''()=>{const c=document.createElement('canvas');c.width=64;c.height=40;const x=c.getContext('2d');x.drawImage(video,0,0,64,40);const a=x.getImageData(0,0,64,40).data;let lo=255,hi=0,lit=0;for(let i=0;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i]);if(a[i]+a[i+1]+a[i+2]>80)lit++;}const colors=new Set();for(let i=0;i<a.length;i+=4)colors.add((a[i]<<16)|(a[i+1]<<8)|a[i+2]);return{colors:colors.size,time:video.currentTime,width:video.videoWidth,height:video.videoHeight,range:hi-lo,lit,error:video.error?.message||null};}''')
   assert q['width']==1280 and q['height']==800 and q['range']>90 and q['lit']>200 and q['colors']>80 and not q['error'],q
   checks.append(dict(level=level['id'],wave=w['number'],pixels=q))
  p.screenshot(path=str(O/(level['id']+'-gallery.png')))
 p.locator('#full').click();p.wait_for_timeout(300);assert p.locator('#full').get_attribute('aria-pressed')=='true';p.evaluate('video.pause()');p.locator('#prev').click();p.wait_for_timeout(200);assert p.locator('#full').get_attribute('aria-pressed')=='false'
 # Fast level changes must not apply a stale metadata seek from the prior film.
 p.evaluate('()=>{selectLevel("stage-1",36);selectLevel("stage-9",1);selectLevel("stage-6-right",20)}');p.wait_for_function('()=>video.readyState>=2&&Math.abs(video.currentTime-current.waves[19].start)<1');p.evaluate('video.pause()')
 p.set_viewport_size({'width':390,'height':844});p.wait_for_timeout(400);assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');p.screenshot(path=str(O/'gallery-mobile.png'),full_page=True)
 (O/'browser-errors.json').write_text(json.dumps(errors,indent=2));assert not errors,errors;b.close()
out=dict(sceneryRevision=data['sceneryRevision'],levels=len(data['levels']),chapters=data['chapterCount'],decodedSeekChecks=len(checks),controls=True,rapidSwitch=True,mobileFits=True,checks=checks,errors=errors);(O/'browser-playback.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='checks'}))
