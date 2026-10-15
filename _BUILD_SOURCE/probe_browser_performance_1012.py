from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/browser_pass_1012';O.mkdir(parents=True,exist_ok=True)
source=(R/'_BUILD_SOURCE/probe_edge_live_1012.py').read_text()
for name,launch in ([] if '--guide-only' in sys.argv else [('Edge',"pw.chromium.launch(channel='msedge',args=['--mute-audio'])"),('Chrome',"pw.chromium.launch(channel='chrome',args=['--mute-audio'])"),('Firefox','pw.firefox.launch()')]):
 print('BEGIN',name,flush=True)
 adapted=source.replace("pw.chromium.launch(channel='msedge',args=['--mute-audio'])",launch).replace("R=Path(__file__).resolve().parents[1]",'R=Path('+repr(str(R))+')').replace("O=R/'_shots/performance_1012/live'", "O=R/'_shots/browser_pass_1012/"+name+"'")
 exec(compile(adapted,name,'exec'),{'__file__':str(R/'_BUILD_SOURCE/probe_edge_live_1012.py')})
port,stop=shoot.serve(str(R));reports=[]
try:
 with sync_playwright() as pw:
  for name,engine,args in [('Edge',pw.chromium,{'channel':'msedge'}),('Chrome',pw.chromium,{'channel':'chrome'}),('Firefox',pw.firefox,{})]:
   b=engine.launch(**args);p=b.new_page(viewport={'width':1440,'height':1000});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   p.goto(f'http://localhost:{port}/extensions/bof-field-manual/guide.html');p.wait_for_selector('.card')
   total=p.locator('.card').count();assert total>=40,total
   p.locator('#search').fill('HERALD');assert p.locator('#herald').count()==1
   p.locator('#herald button').click();p.locator('#herald summary').click();p.locator('#herald textarea').fill('Wait for the beam gap.');p.reload();p.locator('#search').fill('HERALD');p.locator('#herald summary').click();assert p.locator('#herald textarea').input_value()=='Wait for the beam gap.'
   p.locator('#search').fill('');p.locator('#difficulty').select_option('furious');assert '1 continues' in p.locator('#briefing').inner_text()
   p.evaluate('document.querySelectorAll("img").forEach(i=>i.loading="eager")');p.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
   p.screenshot(path=str(O/f'guide-{name}.png'),full_page=True)
   p.set_viewport_size({'width':390,'height':844});p.screenshot(path=str(O/f'guide-mobile-{name}.png'));assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
   assert not errors,errors;reports.append({'browser':name,'dossiers':total,'search':True,'bookmarks':True,'notesPersistence':True,'difficulty':True,'mobileOverflow':False,'errors':errors});b.close()
  ext=R/'extensions/bof-field-manual';ctx=pw.chromium.launch_persistent_context(str(O/'extension-profile'),channel='chromium',headless=True,args=[f'--disable-extensions-except={ext}',f'--load-extension={ext}'])
  p=ctx.new_page();p.goto('chrome://extensions');p.wait_for_timeout(1000)
  item=p.locator('extensions-item').filter(has_text='Bullets of Fury: Field Manual');assert item.count()==1
  eid=item.get_attribute('id');p.goto('chrome-extension://'+eid+'/guide.html');p.wait_for_selector('.card');assert p.locator('.card').count()>=40
  p.goto('chrome-extension://'+eid+'/popup.html')
  with ctx.expect_page() as opened:p.locator('#open').click()
  gp=opened.value;gp.wait_for_selector('.card');assert gp.locator('.card').count()>=40
  gp.screenshot(path=str(O/'extension-guide.png'))
  reports.append({'actualUnpackedExtensionLoaded':True,'popupOpensGuide':True,'id':eid});ctx.close()
finally:stop()
(O/'guide-verification.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
