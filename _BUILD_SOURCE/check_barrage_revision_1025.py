from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import argparse,json

R=Path(__file__).resolve().parents[1];O=R/'_shots/barrage_revision_1025/browser';O.mkdir(parents=True,exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--url',required=True);args=ap.parse_args();checks=[];errors=[];shots=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright() as pw:
 br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1440,'height':1040})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(args.url,wait_until='load');p.wait_for_selector('.choice');data=p.request.get(args.url.rsplit('/',1)[0]+'/review.json').json()
 ck('Eight current chapters load six freshly recorded films',len(data)==8 and len(set(q['src']for q in data))==6 and p.locator('.choice').count()==8)
 for q in data:
  p.locator('.choice[data-id="'+q['id']+'"]').click();p.wait_for_function('document.querySelector("#v").readyState>=2&&!document.querySelector("#v").seeking')
  observed=[]
  for control in ['warning','attack','recovery']:
   p.locator('#'+control).click();p.wait_for_function('(t)=>{const v=document.querySelector("#v");return !v.seeking&&Math.abs(v.currentTime-t)<.15;}',arg=q[control])
   start=p.evaluate('document.querySelector("#v").currentTime');p.evaluate('async()=>{const v=document.querySelector("#v");v.muted=false;await v.play();}')
   p.wait_for_function('(t)=>document.querySelector("#v").currentTime>t+.13',arg=start)
   observed.append(p.evaluate('()=>{const v=document.querySelector("#v");v.pause();return{width:v.videoWidth,height:v.videoHeight,frames:v.getVideoPlaybackQuality().totalVideoFrames,muted:v.muted,error:v.error?.message};}'))
  ck(q['id']+' plays and seeks all checkpoints with audio enabled',all(x['width']==1280 and x['height']==800 and x['frames']>2 and not x['muted']and not x.get('error')for x in observed),observed)
  p.locator('#peak').click();p.wait_for_function('!document.querySelector("#v").seeking');before=p.evaluate('document.querySelector("#v").currentTime');p.locator('#frame').click();p.wait_for_function('!document.querySelector("#v").seeking');after=p.evaluate('document.querySelector("#v").currentTime')
  ck(q['id']+' native frame stepping works',.02<after-before<.05,{'before':before,'after':after})
  p.locator('#speed').select_option('.5');ck(q['id']+' slow motion works',p.evaluate('document.querySelector("#v").playbackRate===.5'));p.locator('#speed').select_option('1')
  p.screenshot(path=str(O/(q['id']+'.png')));shots.append((O/(q['id']+'.png'),q['title']))
  url=args.url.split('/docs/')[0]+q['src'];r=p.request.get(url,headers={'Range':'bytes=1000-1999'});ck(q['id']+' byte-range video seeking works',r.status==206 and len(r.body())==1000,r.headers.get('content-range'))
 ck('Review has no page, console or asset errors',not errors,errors);br.close()
im=Image.new('RGB',(1440,((len(shots)+2)//3)*369),(5,10,17));g=ImageDraw.Draw(im)
for i,(f,n)in enumerate(shots):im.paste(Image.open(f).resize((480,347)),((i%3)*480,(i//3)*369));g.text(((i%3)*480+4,(i//3)*369+348),n,fill='white')
im.save(O/'contact.jpg');(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
print(json.dumps({'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)}),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
