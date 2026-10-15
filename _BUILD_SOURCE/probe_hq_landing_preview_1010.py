"""Use the homecoming review's real controls and embedded game in Chromium."""
from pathlib import Path
import sys,json,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/os.environ.get('BOF_HL10_OUT','_shots/hq_landing_1010');OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1440,height=960));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.add_init_script('''(()=>{const Native=window.AudioContext;if(!Native)return;
   window.__hl10AudioContexts=[];window.AudioContext=class extends Native{
    constructor(...args){super(...args);window.__hl10AudioContexts.push(this);}};})();''')
  p.goto(f'http://127.0.0.1:{port}/docs/previews/hq_landing_1010/index.html');p.wait_for_function('ready&&!busy')
  game=p.frames[1];game.evaluate("Object.defineProperty(navigator,'getGamepads',{configurable:true,value:()=>[]});")
  p.screenshot(path=str(OUT/'preview.png'));q=game.evaluate('HL10.last')
  check('Preview opens the grounded ship in the actual ending renderer',q['grounded'] and q['phase']=='landing',q)
  pilots=[]
  for pk in ['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']:
   p.select_option('#pilot',pk);p.wait_for_function('!busy');p.click('[data-time="16.6"]');p.wait_for_function('!busy')
   game.wait_for_function('HL10.last?.pilot===run.pilot&&HL10.last?.phase===\'walk\'');pilots.append(game.evaluate('HL10.last.pilot'))
   p.click('#pause');game.evaluate('()=>{__hl10Review.time=18.8;__hl10Review.playing=false;}');p.wait_for_timeout(100)
   p.screenshot(path=str(OUT/('preview-'+pk+'.png')))
  check('Pilot chooser displays all nine real body and aircraft banks',len(set(pilots))==9,pilots)
  p.select_option('#pilot','cole');p.wait_for_function('!busy');p.click('[data-time="9.4"]');p.wait_for_function('!busy');game.wait_for_function('__hl10Review.time>9.5');p.click('#pause')
  a=game.evaluate('__hl10Review.time');p.wait_for_timeout(250);b=game.evaluate('__hl10Review.time');check('Pause freezes the actual landing clock',abs(a-b)<.025,dict(before=a,after=b))
  p.locator('#time').evaluate("el=>{el.value='23';el.dispatchEvent(new Event('input',{bubbles:true}));}");game.wait_for_function('HL10.last?.t===23');check('Timeline seeks to a visible doorway walk',game.evaluate('HL10.last.actor.inside&&HL10.last.doorFrame===15'))
  p.screenshot(path=str(OUT/'preview-entry.png'))
  p.click('#play');p.wait_for_function('!busy');game.wait_for_function('__hl10Review.playing&&__hl10Review.time>.2');check('Play restarts the full escape-to-HQ homecoming',game.evaluate("HL10.last.phase==='escape'&&HL10.events.every(e=>e.event!=='sound'||e.available)"))
  check('Play resumes the actual native audio context at the configured effects volume',game.evaluate("window.__hl10AudioContexts.some(a=>a.state==='running')&&!Audio.isMuted()&&Audio.getVol('sfx')>0"))
  p.click('[data-time="26.4"]');p.wait_for_function('!busy');game.wait_for_function("HL10.transition?.phase==='survivor'&&HL10.transition.fade<.1")
  p.screenshot(path=str(OUT/'preview-next-scene.png'))
  check('Next scene control plays the actual fade into the survivor continuation',game.evaluate("__hl10Review.playing&&HL10.transition.phase==='survivor'&&HL10.transition.fade<.1"))
  for at,phase in [('28.3','wide-crawl'),('30.4','infection'),('32.6','corruption'),('36.4','virus')]:
   p.click('[data-time="'+at+'"]');p.wait_for_function('!busy');game.wait_for_function("SV10.last?.phase==='"+phase+"'");p.click('#pause');p.screenshot(path=str(OUT/('preview-survivor-'+phase+'.png')))
   check('Survivor '+phase+' control drives the actual animated ending',game.evaluate("SV10.last.phase==='"+phase+"'&&sv10Warm()"))
  game.evaluate('()=>{__hl10Review.time=43.45;drawVictory._t=43.45;__hl10Review.playing=true;}');game.wait_for_function('!__hl10Review.playing');check('Review includes the full satellite takeover and stops at Fury Command',game.evaluate('__hl10Review.time===43.5'))
  p.set_viewport_size(dict(width=480,height=900));p.click('[data-time="13.6"]');p.wait_for_function('!busy');p.click('#pause');p.wait_for_timeout(100);p.screenshot(path=str(OUT/'preview-narrow.png'))
  dims=game.evaluate('()=>{const r=cv.getBoundingClientRect();return{x:r.width/cutsceneViewWidth(),y:r.height/VH};}')
  check('Narrow review keeps the selected ship evenly proportioned',abs(dims['x']/dims['y']-1)<.005,dims)
  check('Review has no page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
(OUT/'preview-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if report['failed'] else 0)
