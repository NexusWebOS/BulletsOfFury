from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import argparse,json

R=Path(__file__).resolve().parents[1];O=R/'_shots/bullethell_1025/browser';O.mkdir(parents=True,exist_ok=True)
a=argparse.ArgumentParser();a.add_argument('--url',required=True);args=a.parse_args();errors=[];checks=[];shots=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright()as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1440,'height':1040})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text+' '+json.dumps(m.location))if m.type=='error'else None)
 p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(args.url,wait_until='load');p.wait_for_selector('.choice');data=p.request.get(args.url.rsplit('/',1)[0]+'/review.json').json()
 ck('All twelve requested encounter clips are available',len(data)==12 and p.locator('.choice').count()==12)
 for q in data:
  p.locator('.choice[data-id="'+q['id']+'"]').click();p.wait_for_function('document.querySelector("#v").readyState>=2')
  result=[]
  for at in [.5,min(4,q['seconds']*.4),min(q['seconds']-1,q['recovery']+.4)]:
   p.evaluate('(t)=>{const v=document.querySelector("#v");v.pause();v.currentTime=t;}',at)
   p.wait_for_function('(t)=>{const v=document.querySelector("#v");return !v.seeking&&v.readyState>=2&&Math.abs(v.currentTime-t)<.15}',arg=at)
   p.evaluate('async()=>{const v=document.querySelector("#v");v.muted=false;await v.play();}')
   p.wait_for_function('(t)=>document.querySelector("#v").currentTime>t+.12',arg=at)
   result.append(p.evaluate('()=>{const v=document.querySelector("#v");v.pause();return{t:v.currentTime,width:v.videoWidth,height:v.videoHeight,frames:v.getVideoPlaybackQuality().totalVideoFrames,error:v.error?.message||null,muted:v.muted};}'))
  ck(q['id']+' plays, decodes and seeks with audio enabled',all(t['width']==1280 and t['height']==800 and t['frames']>2 and not t['error']and not t['muted']for t in result),result)
  p.locator('#peak').click();p.wait_for_function('!document.querySelector("#v").seeking');before=p.evaluate('document.querySelector("#v").currentTime');p.locator('#frame').click();p.wait_for_function('!document.querySelector("#v").seeking')
  after=p.evaluate('document.querySelector("#v").currentTime');ck(q['id']+' frame advance and checkpoint controls work',.02<after-before<.05,{'before':before,'after':after})
  p.locator('#speed').select_option('.5');ck(q['id']+' slow motion works',p.evaluate('document.querySelector("#v").playbackRate===.5'));p.locator('#speed').select_option('1')
  p.screenshot(path=str(O/(q['id']+'.png')));shots.append((O/(q['id']+'.png'),q['name']))
  url=args.url.split('/docs/')[0]+q['src'];r=p.request.get(url,headers={'Range':'bytes=1000-1999'});ck(q['id']+' supports byte-range seeking',r.status==206 and len(r.body())==1000,r.headers.get('content-range'))
 ck('Review has no page or console errors',not errors,errors);br.close()
im=Image.new('RGB',(1440,((len(shots)+2)//3)*369),(5,10,17));d=ImageDraw.Draw(im)
for i,(f,n)in enumerate(shots):im.paste(Image.open(f).resize((480,347)),((i%3)*480,(i//3)*369));d.text(((i%3)*480+4,(i//3)*369+348),n,fill='white')
im.save(O/'contact.jpg');(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
print(json.dumps(dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks))),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
