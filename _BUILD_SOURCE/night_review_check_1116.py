from pathlib import Path
from playwright.sync_api import sync_playwright
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';errors=[]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in['href','src']and v:self.links.append(v)
l=Links();l.feed((O/'review.html').read_text());missing=[]
for link in l.links:
 if urlsplit(link).scheme or link.startswith('#'):continue
 p=(O/unquote(link.split('?')[0])).resolve()
 if not p.exists():missing.append(link)
with sync_playwright()as z:
 b=z.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(45000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+urlsplit(r.url).path)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/_shots/cinema_overnight_1116/review.html');rows=[]
 for i in range(p.locator('#clip option').count()):
  p.select_option('#clip',str(i));p.evaluate('document.getElementById("film").load()');p.wait_for_function('()=>{const v=document.getElementById("film");return v.readyState>=1&&v.duration>0}')
  q=p.evaluate('''async()=>{const v=document.getElementById('film');const wanted=v.duration*.55;await new Promise((res,rej)=>{v.addEventListener('seeked',res,{once:true});v.addEventListener('error',()=>rej(Error('video error')),{once:true});v.currentTime=wanted;});await v.play();await new Promise(r=>setTimeout(r,350));v.pause();return{duration:v.duration,width:v.videoWidth,height:v.videoHeight,time:v.currentTime,error:v.error?.message||null,decoded:v.getVideoPlaybackQuality().totalVideoFrames};}''');q['index']=i;rows.append(q)
  if i in[0,2,12,19]:p.screenshot(path=str(O/f'review-playing-{i}.jpg'),type='jpeg',quality=85)
 p.screenshot(path=str(O/'review-native.jpg'),type='jpeg',quality=85);b.close()
q={'missingLinks':missing,'pageConsoleHttpErrors':errors,'rows':rows,'checks':{'allLocalLinksExist':not missing,'allClipsDecode':all(q['width']>0 and q['height']>0 and q['decoded']>0 and q['time']>0 and not q['error']for q in rows),'noBrowserErrors':not errors},'scope':'Actual Chromium review player: selected every film, loaded native metadata, sought to55%, decoded and played. Screenshots retained. No game or campaign interaction.'};(O/'review-check.json').write_text(json.dumps(q,indent=2),encoding='utf8');print(json.dumps(q['checks']));assert all(q['checks'].values())
