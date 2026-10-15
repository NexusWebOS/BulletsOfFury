import os,json,time,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
os.environ['PLAYWRIGHT_BROWSERS_PATH']='C:/Users/Mike/AppData/Local/ms-playwright'
out=Path(os.environ.get('BOF_ATLAS_QA_OUTPUT',str(Path(__file__).resolve().parents[1]/'_shots'/'enemy_atlas_controls_1013')));out.mkdir(parents=True,exist_ok=True);report=[]
with sync_playwright() as p:
 for engine in ['chrome','edge','firefox']:
  b=(p.firefox.launch() if engine=='firefox' else p.chromium.launch(channel='msedge' if engine=='edge' else 'chrome',args=['--mute-audio']))
  pg=b.new_page(viewport={'width':1460,'height':1080});errors=[];console=[];checks=[]
  pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:console.append({'text':m.text,'location':m.location}) if m.type=='error' else None)
  pg.goto('http://127.0.0.1:8767/');pg.evaluate("localStorage.setItem('atlas-save-sentinel','keep');localStorage.setItem('bof_bossmode','keep-overrides');")
  before=pg.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))')
  pg.goto('http://127.0.0.1:8767/enemy-atlas.html',wait_until='load',timeout=120000)
  pg.wait_for_function("document.querySelector('#loading').hidden",timeout=120000);f=pg.locator('#engine').content_frame
  pg.wait_for_timeout(2200);snap=lambda:f.locator('body').evaluate('()=>BOF_ENEMY_ATLAS.snapshot()')
  s=snap();checks.append(['initial live',s['frames']>10 and not s['error']])
  pg.locator('#pause').click();t=snap()['frames'];pg.wait_for_timeout(550);checks.append(['pause',snap()['frames']==t])
  pg.locator('#step').click();pg.wait_for_timeout(200);checks.append(['single frame',snap()['frames']==t+1])
  pg.locator('#pause').click();pg.locator('#speed').select_option('.25');checks.append(['slow motion',snap()['speed']==.25])
  pg.locator('#speed').select_option('1');pg.locator('#search').fill('warhive');pg.locator('#roster button').first.click();pg.wait_for_function("document.querySelector('#loading').hidden",timeout=120000)
  pg.wait_for_timeout(4500);checks.append(['carrier actor',snap()['actor']['type']=='warhive']);pg.screenshot(path=str(out/(engine+'-atlas.png')),full_page=True)
  pg.locator('#search').fill('The Warrior');pg.locator('#roster button').first.click();pg.wait_for_function("document.querySelector('#loading').hidden",timeout=120000)
  pg.wait_for_timeout(2200);checks.append(['overdrive switch',snap().get('game')=='overdrive' and snap()['actor'] is not None])
  pg.locator('#search').fill('warhive');pg.locator('#roster button').first.click();pg.wait_for_function("document.querySelector('#loading').hidden",timeout=120000);checks.append(['return to BOF',snap()['actor']['type']=='warhive'])
  after=pg.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))');checks.append(['progress untouched',before==after])
  pg.set_viewport_size({'width':390,'height':844});pg.wait_for_timeout(500);checks.append(['mobile no horizontal scroll',pg.evaluate('document.documentElement.scrollWidth<=innerWidth+1')])
  pg.screenshot(path=str(out/(engine+'-atlas-mobile.png')),full_page=True)
  report.append({'browser':engine,'checks':checks,'pageErrors':errors,'console':console});print(json.dumps(report[-1]),flush=True);b.close()
(out/'atlas_controls_1013.json').write_text(json.dumps(report,indent=2))
