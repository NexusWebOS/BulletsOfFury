"""Actual native Spread travel/cadence and all-nine-pilot muzzle regression."""
from pathlib import Path
import ast,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019';errors=[];checks=[];rows=[]
tree=ast.parse((R/'_BUILD_SOURCE/probe_spread_muzzle_1019.py').read_text(encoding='utf-8'))
def constant(name):return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
SETUP=constant('SETUP');MEASURE=constant('MEASURE');pilots=constant('PILOTS')
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.evaluate(SETUP,False)
  for pilot in pilots:
   row=p.evaluate(MEASURE,dict(pilot=pilot));rows.append(row);ck(pilot+' actual flash ink remains centered on the actual nose',row.get('offset') is not None and abs(row['offset'])<=1,row)
  table={r['pk']:r for r in rows};ck('Lizzie Spread has the requested 15 percent slower travel',abs(table['lizzie']['speed']/table['cole']['speed']-.85)<.005,dict(lizzie=table['lizzie']['speed'],cole=table['cole']['speed']))
  ck('Lizzie keeps Cole-equivalent native firing cadence',abs(table['lizzie']['volleysPerSec']-table['cole']['volleysPerSec'])<.51,dict(lizzie=table['lizzie']['volleysPerSec'],cole=table['cole']['volleysPerSec']))
  ck('Other pilots retain their authored baseline Spread travel',all(abs(r['speed']-5.6)<.02 for r in rows if r['pk']!='lizzie'),rows)
  ck('No page/console/draw errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,rows=rows,errors=errors);(O/'lizzie-spread-native.json').write_text(json.dumps(report,indent=2)+'\n');sys.exit(report['failed']>0)
