"""Native video decode, comparison controls and responsive preview QA."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().parents[1]/'_shots/boss_comparison_1102';checks=[];errors=[]
def ck(name,data,ok):checks.append(dict(name=name,data=data,passed=bool(ok)));print('PASS'if ok else'FAIL',name,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1500,'height':1000});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.goto('http://127.0.0.1:8805/current/boss-comparison-1102.html',wait_until='networkidle');p.wait_for_function('videos.length===3&&videos.every(v=>v.readyState>=2)');p.locator('#all').click();p.wait_for_timeout(1600)
 q=p.evaluate('videos.map(v=>({diff:v.dataset.diff,time:v.currentTime,w:v.videoWidth,h:v.videoHeight,playing:!v.paused,muted:v.muted}))');ck('Three difficulty videos decode and advance',q,len(q)==3 and all(r['time']>.5 and r['w']==1280 for r in q))
 ck('Play all defaults to one audible Normal movie',q,[r['diff']for r in q if not r['muted']]==['normal'])
 p.locator('#pause').click();ck('Pause all',None,p.evaluate('videos.every(v=>v.paused)'))
 p.locator('#scrub').fill('12');p.locator('#scrub').dispatch_event('input');p.wait_for_timeout(500);q=p.evaluate('videos.map(v=>v.currentTime)');ck('Shared seek reaches the same native time',q,all(abs(t-12)<.2 for t in q))
 p.get_by_role('button',name='Listen to Hard',exact=True).click();p.wait_for_timeout(300);q=p.evaluate('videos.map(v=>({diff:v.dataset.diff,muted:v.muted}))');ck('Only selected comparison is audible',q,[v['diff']for v in q if not v['muted']]==['hard']);p.locator('#pause').click()
 ck('All concept images load',None,p.evaluate('[...document.querySelectorAll(".concepts img")].every(i=>i.complete&&i.naturalWidth>500)'))
 p.screenshot(path=str(O/'page-desktop.png'),full_page=True)
 p.locator('#role').select_option('rough-riders');ck('Alternate route selects Stage6',None,p.locator('#stage').input_value()=='6');p.locator('#stage').select_option('7');ck('Changing stages restores ordinary boss selector',None,p.locator('#role').input_value()=='boss')
 p.locator('#stage').select_option('8');p.wait_for_function('videos.length>=2&&videos.every(v=>v.readyState>=1)');p.locator('#transform').click();p.wait_for_timeout(900);q=p.evaluate("videos.map(v=>({diff:v.dataset.diff,time:v.currentTime,expected:v._row.chapters.find(c=>c.label==='Final transformation').seconds}))");ck('Final transformation comparison uses each native chapter time',q,all(abs(v['time']-v['expected'])<2 for v in q));p.locator('#pause').click();p.screenshot(path=str(O/'page-transformations.png'),full_page=True)
 p.set_viewport_size({'width':390,'height':844});p.locator('#stage').select_option('1');p.locator('#role').select_option('mini');p.wait_for_timeout(350);q=p.evaluate('({width:innerWidth,doc:document.documentElement.scrollWidth,players:[...document.querySelectorAll(".players .card")].map(e=>({w:e.clientWidth,x:e.getBoundingClientRect().x}))})');ck('Mobile has no horizontal overflow',q,q['doc']<=q['width']);p.screenshot(path=str(O/'page-mobile.png'),full_page=True)
 ck('No page or console errors',errors,not errors);b.close()
(O/'page-checks.json').write_text(json.dumps(checks,indent=2));sys.exit(0 if all(r['passed']for r in checks)else 1)
