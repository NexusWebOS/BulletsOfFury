from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,argparse

R=Path(__file__).resolve().parents[1];O=R/'_shots/horizon_assault_1025/browser';O.mkdir(parents=True,exist_ok=True)
a=argparse.ArgumentParser();a.add_argument('--url',required=True);args=a.parse_args();checks=[];errors=[];shots=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1100})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(args.url,wait_until='load');p.wait_for_function('document.querySelector("#v").readyState>=2&&!document.querySelector("#v").seeking')
 data=p.request.get(args.url.rsplit('/',1)[0]+'/review.json').json();ck('Current continuous film decodes at1280x800',p.evaluate('document.querySelector("#v").videoWidth===1280&&document.querySelector("#v").videoHeight===800'))
 for key,t in data['chapters'].items():
  p.locator('#'+key).click();p.wait_for_function('(t)=>{const v=document.querySelector("#v");return !v.seeking&&Math.abs(v.currentTime-t)<.12;}',arg=t)
  p.evaluate('async()=>{const v=document.querySelector("#v");v.muted=false;await v.play();}');p.wait_for_function('(t)=>document.querySelector("#v").currentTime>t+.13',arg=t)
  d=p.evaluate('()=>{const v=document.querySelector("#v");v.pause();return{t:v.currentTime,frames:v.getVideoPlaybackQuality().totalVideoFrames,muted:v.muted,error:v.error?.message};}')
  ck(key+' checkpoint plays and seeks with audio enabled',d['frames']>2 and not d['muted']and not d.get('error'),d);p.screenshot(path=str(O/(key+'.png')));shots.append((O/(key+'.png'),key))
 p.locator('#frame').click();p.wait_for_function('!document.querySelector("#v").seeking');start=p.evaluate('document.querySelector("#v").currentTime');p.locator('#frame').click();p.wait_for_function('!document.querySelector("#v").seeking');end=p.evaluate('document.querySelector("#v").currentTime');ck('Single-frame stepping works',.02<end-start<.05)
 for speed in ['.25','.5']:p.locator('#speed').select_option(speed);ck(speed+' speed plays correctly',p.evaluate('(s)=>document.querySelector("#v").playbackRate===+s',speed))
 url=args.url.split('/docs/')[0]+data['src'];r=p.request.get(url,headers={'Range':'bytes=1000-1999'});ck('Byte-range video seeking works',r.status==206 and len(r.body())==1000)
 ck('Review has no page, console or asset errors',not errors,errors);b.close()
im=Image.new('RGB',(1440,((len(shots)+2)//3)*389),(5,10,17));g=ImageDraw.Draw(im)
for i,(f,n)in enumerate(shots):im.paste(Image.open(f).resize((480,367)),((i%3)*480,(i//3)*389));g.text(((i%3)*480+4,(i//3)*389+368),n,fill='white')
im.save(O/'contact.jpg');(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
print(json.dumps({'passed':sum(c['passed']for c in checks),'failed':sum(not c['passed']for c in checks)}),flush=True)
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
