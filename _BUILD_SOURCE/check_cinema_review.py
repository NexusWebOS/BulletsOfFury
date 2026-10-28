from pathlib import Path
from playwright.sync_api import sync_playwright
import json
O=Path(__file__).parent/'BOF-Cinema-Rebuild/verification';checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)});print(('PASS ' if v else 'FAIL ')+n,flush=True)
 if not v:raise AssertionError(n)
try:
 with sync_playwright() as pw:
  for browser in ['msedge','chrome','firefox']:
   b=pw.firefox.launch() if browser=='firefox' else pw.chromium.launch(channel=browser)
   p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(120000);errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   p.goto('http://127.0.0.1:8801/_shots/cinema_story_1021/review.html');p.wait_for_function('ready');fr=p.frames[1]
   p.locator('[data-scene="post-3"]').click();fr.wait_for_function('BOFCinematicDirector.active&&BOFCinematicDirector.current.id==="review-post-3"')
   p.wait_for_timeout(600);ck(browser+' plays real Yuri regroup sequence',fr.evaluate('run.pilot==="yuri"&&C22.last?.id==="review-post-3"'))
   ck(browser+' native music/context are running',fr.evaluate('Audio.musicPlaying()&&Snd._audioCtx().state==="running"'))
   p.locator('#next').click();ck(browser+' Next reveals dialogue',fr.evaluate('BOFCinematicDirector.current.shown===BOFCinematicDirector.current.beats[BOFCinematicDirector.current.i].text.length'))
   p.locator('#pilot').select_option(label='Cole');p.locator('[data-scene="post-5"]').click();fr.wait_for_function('BOFCinematicDirector.current?.id==="review-post-5"');ck(browser+' swaps to Cole native story',fr.evaluate('run.pilot==="cole"'))
   p.locator('[data-scene="ending"]').click();fr.wait_for_function('state===GS.VICTORY');fr.evaluate('drawVictory._t=74');p.wait_for_timeout(250);ck(browser+' dimensional ending runs',fr.evaluate('INV20.last?.scene==="waters"&&C22.draws.coast_invasion>0'))
   p.screenshot(path=str(O/('review-'+browser+'.png')),full_page=True)
   p.set_viewport_size({'width':390,'height':844});p.wait_for_timeout(150);ck(browser+' narrow controls fit',p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
   ck(browser+' no browser page errors',not errors);b.close()
finally:(O/'browser-report.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('ALL',len(checks),'BROWSER CHECKS PASSED',flush=True)
