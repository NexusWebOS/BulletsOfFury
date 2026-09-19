import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
port,stop=shoot.serve(str(root));errors=[]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  page=b.new_page()
  page.on('pageerror',lambda e:errors.append(str(e)[:240]))
  page.goto('http://127.0.0.1:%s/index.html'%port,wait_until='load',timeout=60000)
  page.wait_for_function("typeof pilotPortrait==='function'&&typeof XART!=='undefined'",timeout=45000)
  names=['idle','anger','crash','happy','laugh','sad','victory','talk-closed','talk-small','talk-medium','talk-o','talk-wide']
  page.evaluate('(names)=>names.forEach(n=>XART.rdy("port_cf_yuri_"+n))',names)
  page.wait_for_function('(names)=>names.every(n=>XART.rdy("port_cf_yuri_"+n))',arg=names,timeout=45000)
  result=page.evaluate("""(names)=>({allLoaded:names.every(n=>XART.rdy('port_cf_yuri_'+n)),
    idle:pilotPortrait('yuri','idle'),happy:pilotPortrait('yuri','happy'),talk:pilotPortrait('yuri','talk'),allRouted:names.every(n=>pilotPortrait('yuri',n)==='port_cf_yuri_'+n),
    direct:XART._src.port_cf_yuri_idle,legacy:XART._touch('port_yuri_idle').src,
    oldHairPathUsed:String(XART._src.port_cf_yuri_idle).includes('yuri_v2')})""",names)
  print(json.dumps({'portrait':result,'errors':errors},indent=2))
  assert result['allLoaded'] and result['idle']=='port_cf_yuri_idle' and result['happy']=='port_cf_yuri_happy' and result['allRouted'] and result['talk'].startswith('port_cf_yuri_talk-') and not result['oldHairPathUsed'] and not errors
  b.close()
finally:stop()
