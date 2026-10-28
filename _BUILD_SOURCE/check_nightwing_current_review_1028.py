from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/nightwing_shape_1028';qpath=R/'docs/qa/nightwing_current_1028.json';qa=json.loads(qpath.read_text());checks={};errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(60000)
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8795/docs/previews/nightwing_current_1028/index.html');p.wait_for_function('v.readyState>=2')
 checks['completeCurrentFightLoaded']=p.evaluate('v.duration>130&&v.videoWidth===1280&&v.videoHeight===800')
 p.wait_for_function("[...document.querySelectorAll('.pair img')].every(i=>i.complete&&i.naturalWidth===272)")
 checks['matchingCurrentPairLoaded']=p.locator('.pair img').count()==2
 checks['actualDisplayedPairHasIdenticalAlpha']=p.evaluate("""()=>{const imgs=[...document.querySelectorAll('.pair img')],c=document.createElement('canvas');c.width=c.height=272;const g=c.getContext('2d');g.drawImage(imgs[0],0,0);const a=g.getImageData(0,0,272,272).data;g.clearRect(0,0,272,272);g.drawImage(imgs[1],0,0);const b=g.getImageData(0,0,272,272).data;for(let i=0;i<a.length;i+=4)if(a[i+3]!==b[i+3]||b[i+3]>0&&(b[i]!==255||b[i+1]!==255||b[i+2]!==255))return false;return true;}""")
 p.evaluate('()=>{v.muted=true;return v.play()}');p.wait_for_timeout(650);start=p.evaluate('v.currentTime');p.wait_for_timeout(650);checks['nativePlaybackAdvances']=p.evaluate('v.currentTime')>start
 chapter=[]
 for button in p.locator('[data-time]').all():
  at=float(button.get_attribute('data-time'));button.click();p.wait_for_function('t=>!v.seeking&&v.readyState>=2&&Math.abs(v.currentTime-t)<.6',arg=at);chapter.append(dict(label=button.inner_text(),time=p.evaluate('v.currentTime')))
 checks['allFourCurrentChaptersSeek']=len(chapter)==4
 p.evaluate('v.pause()');p.screenshot(path=str(O/'review-desktop.png'),full_page=True);checks['desktopFits']=p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 p.set_viewport_size({'width':480,'height':900});p.screenshot(path=str(O/'review-mobile.png'),full_page=True);checks['mobileFits']=p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 p.set_viewport_size({'width':1280,'height':900});p.goto('http://127.0.0.1:8795/_shots/github_review_1028/index.html?revision=nightwing-current-1028#clip=stage6-carrier');p.wait_for_function('player.readyState>=2')
 for entry in qa['galleryUpdates']:
  key=entry['id'];expected=entry['current'];p.locator(f'.card[data-id="{key}"]').click();p.wait_for_function('s=>player.dataset.source===s&&player.currentSrc.startsWith("blob:")&&player.readyState>=2',arg=expected['src']);p.evaluate('player.muted=true')
  checks[key+'RoutesToCurrentLocalMovie']=p.evaluate('s=>player.dataset.source===s&&player.currentSrc.startsWith("blob:")',expected['src'])
  checks[key+'DurationMatches']=abs(p.evaluate('player.duration')-expected['seconds'])<1
  p.evaluate('()=>{player.pause();player.currentTime=Math.max(0,player.duration-2)}');p.wait_for_function('!player.seeking&&player.readyState>=2&&Math.abs(player.currentTime-(player.duration-2))<.6')
  checks[key+'NativeSeekWorks']=True
  checks[key+'EarlierReleaseLinkPreserved']=p.evaluate("!document.querySelector('#archive').hidden&&document.querySelector('#archive').getAttribute('href').endsWith('.mp4')")
 p.goto('http://127.0.0.1:8795/_shots/github_review_1028/index.html?local&revision=nightwing-current-1028#clip=stage6-nightwing-shadow-turn');p.wait_for_function('player.readyState>=2');checks['LocalQueryAlsoUsesCurrentMovie']=p.evaluate("player.dataset.source.includes('nightwing_shape_1028')&&player.duration<10")
 p.goto('http://127.0.0.1:8795/_shots/github_review_1028/index.html?revision=nightwing-current-1028#clip=stage6-carrier');p.wait_for_function('player.readyState>=2');p.evaluate('player.pause()');p.screenshot(path=str(O/'review-gallery.png'))
 checks['noVideoBrowserOrAssetErrors']=p.evaluate('player.error===null')and not errors;b.close()
result=dict(checks=checks,chapters=chapter,errors=errors);(O/'playback.json').write_text(json.dumps(result,indent=2));qa['playback']=result;qpath.write_text(json.dumps(qa,indent=2));print(json.dumps(result));raise SystemExit(0 if all(checks.values())else 1)
