"""Native browser playback, chapter seeking, frame step and audio controls."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import argparse,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_tidal_1025/browser';O.mkdir(parents=True,exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--url',required=True);args=p.parse_args();checks=[];errors=[];shots=[]
def ck(n,v,data=None):checks.append({'name':n,'passed':bool(v),'data':data});print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);page=br.new_page(viewport={'width':1440,'height':1040})
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);page.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url)if r.status>=400 else None)
 page.goto(args.url,wait_until='load');page.wait_for_selector('.choice');data=page.request.get(args.url.rsplit('/',1)[0]+'/review.json').json()
 ck('Warden, full Stage9 and all six water chapters are available',len(data)==8 and page.locator('.choice').count()==8)
 for item in data:
  page.locator('.choice[data-id="'+item['id']+'"]').click();page.wait_for_function('document.querySelector("#v").readyState>=2')
  records=[]
  for at in [item['start']+.3,min(item['end']-.5,item['firstRelease']+.8),max(item['start']+.5,item['recovery']-.5)]:
   page.evaluate('t=>{const v=document.querySelector("#v");v.pause();v.currentTime=t;}',at)
   page.wait_for_function('t=>{const v=document.querySelector("#v");return !v.seeking&&v.readyState>=2&&Math.abs(v.currentTime-t)<.15}',arg=at)
   page.evaluate('async()=>{const v=document.querySelector("#v");v.muted=false;await v.play()}');page.wait_for_function('t=>document.querySelector("#v").currentTime>t+.12',arg=at)
   records.append(page.evaluate('()=>{const v=document.querySelector("#v");v.pause();return{time:v.currentTime,width:v.videoWidth,height:v.videoHeight,frames:v.getVideoPlaybackQuality().totalVideoFrames,muted:v.muted,error:v.error?.message||null}}'))
  ck(item['id']+' decodes, plays and seeks with audio enabled',all(q['width']==1280 and q['height']==800 and q['frames']>2 and not q['muted']and not q['error']for q in records),records)
  page.locator('#peak').click();page.wait_for_function('!document.querySelector("#v").seeking');before=page.evaluate('document.querySelector("#v").currentTime');page.locator('#frame').click();page.wait_for_function('!document.querySelector("#v").seeking');after=page.evaluate('document.querySelector("#v").currentTime')
  ck(item['id']+' attack jump and single-frame advance work',.02<after-before<.05,{'before':before,'after':after})
  page.locator('#speed').select_option('.5');ck(item['id']+' slow motion works',page.evaluate('document.querySelector("#v").playbackRate===.5'));page.locator('#speed').select_option('1')
  f=O/(item['id']+'.png');page.screenshot(path=str(f));shots.append((f,item['name']))
  req=page.request.get(args.url.split('/docs/')[0]+item['src'],headers={'Range':'bytes=1000-1999'});ck(item['id']+' supports byte-range seeking',req.status==206 and len(req.body())==1000)
 ck('No review page, console or asset errors',not errors,errors);br.close()
c=Image.new('RGB',(1440,((len(shots)+2)//3)*369),(5,12,20));d=ImageDraw.Draw(c)
for i,(f,label)in enumerate(shots):c.paste(Image.open(f).resize((480,347)),(i%3*480,i//3*369));d.text((i%3*480+4,i//3*369+348),label,fill='white')
c.save(O/'contact.jpg');(O/'report.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf8')
print(json.dumps({'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks),'errors':errors}),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)and not errors else 1)
