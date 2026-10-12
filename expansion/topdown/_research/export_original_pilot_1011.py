"""Export original pilot presentation metadata through the real game functions.

This is the owner of menu_1011/original_pilot_data.js. It reads the original
runtime and writes only the expansion's metadata, using a fresh browser.
"""
from pathlib import Path
import hashlib,json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
port,stop=shoot.serve(str(ROOT));errors=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch();page=browser.new_page();page.add_init_script(shoot.TRAP_RAF)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{port}/index.html',timeout=60000)
  page.wait_for_function('typeof pcStats==="function" && typeof pcSpecial==="function"',timeout=60000)
  pilots=page.evaluate("Object.fromEntries(PILOTS.map(p=>{const bio=BOFX.pilotcard[p.key],faction=AFFIL_EMBLEM[String(bio.affil).toUpperCase()];return [p.key,{stats:pcStats(p.key),special:pcSpecial(p.key),color:p.tint,emblem:faction?'affil_'+faction:null}];}))")
  browser.close()
finally:stop()
if errors:raise RuntimeError(errors)
source={'gameSha256':hashlib.sha256((ROOT/'assets/game.js').read_bytes()).hexdigest(),'owner':'expansion/topdown/_research/export_original_pilot_1011.py','functions':['pcStats','pcSpecial','PILOTS','AFFIL_EMBLEM'],'roster':list(pilots)}
dest=ROOT/'expansion/topdown/art/menu_1011/original_pilot_data.js'
dest.write_text('(function(root){root.TD_ORIGINAL_PILOT='+json.dumps(pilots)+';root.TD_ORIGINAL_PILOT_SOURCE='+json.dumps(source)+';})(window);\n',encoding='utf-8',newline='\n')
print(f'Exported {len(pilots)} original pilot cards; no base files edited.')
