from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=W/'roster';O.mkdir(exist_ok=True);report={'stages':[],'errors':[],'method':'Every authored wave at its own map row; aiDelay and flight formation releases expanded; setpieces recorded separately.'};port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:500])if m.type=='error' or 'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.ar23Signature=e=>{const o={type:e.type,art:e.art,variant:e.variant,pal:e.pal};for(const [k,v]of Object.entries(e))if(k.startsWith('_')&&v&&typeof v==='object'){const a={};for(const [n,x]of Object.entries(v))if(['key','kind','bank','art','asset','preset','variant','role','tier','model','family','palette','color','id','type','name'].includes(n)&&['string','number','boolean'].includes(typeof x))a[n]=x;if(Object.keys(a).length)o[k]=a;}return o;};}''')
  lab=(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js').read_text().replace("const key=e.type+'|'", "const key=JSON.stringify(ar23Signature(e))+'|'+e.type+'|'").replace('flags:Object.keys(e)', 'signature:ar23Signature(e),flags:Object.keys(e)')
  p.add_script_tag(content=lab)
  for stage in range(1,10):
   p.evaluate('s=>EA11.setup(s,"normal")',stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage);}')
   specs=p.evaluate('EA11.collect()');report['stages'].append({'stage':stage,'specs':specs,'waveErrors':p.evaluate('EA11.rows')});(O/'catalog.json').write_text(json.dumps(report,indent=2));print(json.dumps({'stage':stage,'cases':len(specs),'types':len({s['type'] for s in specs})}),flush=True)
  b.close()
finally:stop()
print(json.dumps({'cases':sum(len(s['specs'])for s in report['stages']),'errors':report['errors']}))
