"""Render the isolated art viewer, verify every authored reel blits and changes."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

root=Path(__file__).resolve().parents[2]/'assets/game/weapon_animation_0928'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
report={}
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    console=[]
    page.on('pageerror',lambda e:console.append(str(e)))
    page.goto(f'http://127.0.0.1:{server.server_port}/preview.html')
    page.wait_for_function('window.__ART_REVIEW__?.ready',timeout=30000)
    page.evaluate('paused=true;clock=0;')
    page.wait_for_timeout(80)
    first=page.evaluate('window._firstPixels=entries.map(e=>e.cv.toDataURL());entries.map(e=>({key:e.key,frame:e.frame,pixels:e.ctx.getImageData(0,0,e.cv.width,e.cv.height).data.some((v,i)=>i%4===3&&v>32)}))')
    page.evaluate('clock=150;')
    page.wait_for_timeout(80)
    second=page.evaluate('entries.map((e,i)=>({key:e.key,frame:e.frame,pixelsChanged:e.cv.toDataURL()!==window._firstPixels[i]}))')
    page.screenshot(path=str(root/'review/browser_all.png'),full_page=True)
    page.locator('[data-filter="chromium"]').click()
    page.evaluate('clock=700;')
    page.wait_for_timeout(350)
    page.screenshot(path=str(root/'review/browser_chromium.png'),full_page=True)
    page.locator('[data-filter="beam"]').click()
    page.wait_for_timeout(250)
    page.screenshot(path=str(root/'review/browser_beams.png'),full_page=True)
    report={'familyCount':len(first),'nonemptyCanvases':sum(v['pixels'] for v in first),
            'advancedReels':[a['key'] for a,b in zip(first,second) if a['frame']!=b['frame'] and b['pixelsChanged']],
            'pageErrors':console+page.evaluate('window.__ART_REVIEW__.errors'),
            'status':'art viewer verification only; no game-engine claims'}
    assert len(first)==70 and report['nonemptyCanvases']==70 and not report['pageErrors'],report
    assert len(report['advancedReels'])==43,report
    browser.close()
server.shutdown()
(root/'review/browser_qa.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
