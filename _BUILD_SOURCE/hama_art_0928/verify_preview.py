"""Focused isolated art-viewer verification; not a gameplay test."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import json,threading
root=Path(__file__).resolve().parents[2]/'assets/game/hama_art_0928'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
    browser=p.chromium.launch();page=browser.new_page(viewport={'width':1500,'height':1050})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'http://127.0.0.1:{server.server_port}/preview.html')
    page.wait_for_function('window.__ART_REVIEW__?.ready',timeout=30000)
    page.evaluate('paused=true;clock=0');page.wait_for_timeout(100)
    first=page.evaluate('window._firstPixels=entries.map(e=>e.cv.toDataURL());entries.map(e=>({key:e.key,frame:e.frame,pixels:e.ctx.getImageData(0,0,e.cv.width,e.cv.height).data.some((v,i)=>i%4===3&&v>32)}))')
    page.evaluate('clock=180');page.wait_for_timeout(100)
    second=page.evaluate('entries.map((e,i)=>({key:e.key,frame:e.frame,changed:e.cv.toDataURL()!==window._firstPixels[i]}))')
    page.screenshot(path=str(root/'review/browser_all.png'),full_page=True)
    page.locator('[data-filter="boss"]').click();page.wait_for_timeout(100)
    page.screenshot(path=str(root/'review/browser_boss.png'),full_page=True)
    page.locator('[data-filter="head"]').click();page.wait_for_timeout(100)
    assert page.locator('article:visible').count()==4
    page.locator('article:visible input').first.fill('3');page.wait_for_timeout(100)
    assert page.evaluate('entries.find(e=>e.key==="boss_speaker_sing").frame')==3
    page.screenshot(path=str(root/'review/browser_heads.png'),full_page=True)
    report={'reels':len(first),'frames':sum(len(e['frames']) for e in json.loads((root/'manifest.json').read_text())['families'].values()),
            'nonemptyCanvases':sum(v['pixels'] for v in first),'animatedReels':sum(v['changed'] for v in second),
            'pageErrors':errors+page.evaluate('window.__ART_REVIEW__.errors'),'filtersAndScrub':'passed',
            'scope':'isolated art viewer only, no audio or gameplay verification'}
    assert report['reels']==15 and report['frames']==128 and report['nonemptyCanvases']==15 and report['animatedReels']==15 and not report['pageErrors'],report
    browser.close()
server.shutdown()
(root/'review/browser_qa.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
