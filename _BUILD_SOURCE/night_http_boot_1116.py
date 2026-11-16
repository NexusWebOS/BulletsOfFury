from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlsplit
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinema_overnight_1116';rows=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page();p.on('response',lambda r:rows.append({'status':r.status,'host':urlsplit(r.url).netloc,'path':urlsplit(r.url).path})if r.status>=400 else None);p.goto('http://127.0.0.1:8765/index.html?night-http-boot=1116');p.wait_for_function('window.__bofFrames>6');p.wait_for_timeout(12000);q=p.evaluate('({state,frames:__bofFrames})');b.close()
(O/'http-boot-late.json').write_text(json.dumps({'errors':rows,'state':q,'scope':'Fresh normal shipping boot; response host/path only, all querystrings and response bodies omitted.'},indent=2),encoding='utf8');print(json.dumps({'errors':rows,'state':q}))
