from pathlib import Path
import argparse,json,sys
from playwright.sync_api import sync_playwright
import shoot
args=argparse.ArgumentParser();args.add_argument('--release-only',action='store_true');args=args.parse_args()
R=Path(__file__).resolve().parents[1];O=R/'_shots/hammer_acting_1021'/('preview-release' if args.release_only else 'preview');O.mkdir(parents=True,exist_ok=True);errors=[];checks=[]
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1500,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/hammer_acting_1021/index.html?variant={"blue" if args.release_only else "corrupt"}&scene=stun&difficulty=furious&revision=hammer-acting-1021',wait_until='domcontentloaded')
  p.wait_for_function('!document.querySelector("#replay").disabled');g=p.frames[1]
  for variant in (['blue'] if args.release_only else ['corrupt','blue']):
   if p.input_value('#variant')!=variant:p.select_option('#variant',variant);p.wait_for_function('!document.querySelector("#replay").disabled')
   for scene in (['throw','beam'] if args.release_only else ['intro','slam','jump','side','hold','armor','throw','cast','beam','spin','ball','stun','rage','fight']):
    print('START '+variant+' '+scene,flush=True)
    p.select_option('#scene',scene);p.wait_for_function('!document.querySelector("#replay").disabled')
    row=g.evaluate('()=>({kind:boss?.kind,finite:Number.isFinite(boss?.x+boss?.y),ready:ha21Ready(),state:boss?._hammer?.state,action:hb20Own(boss)?hb20State(boss)?.action?.type:null,mode:boss?._r30?.mode})')
    ok=row['finite'] and row['ready'] and row['kind']==('chromehammer' if variant=='blue' else 'vileexistence');checks.append(dict(name=variant+' '+scene,passed=ok,data=row));print(('PASS ' if ok else 'FAIL ')+variant+' '+scene,flush=True)
    if scene in ['armor','stun','throw','beam']:
     if variant=='blue' and scene=='beam':
      g.wait_for_function('boss._hammer.state==="mega_beam"');p.wait_for_timeout(150)
      checks.append(dict(name='Actual standard laser release survives native phase gates',passed=g.evaluate('boss._hammer.state==="mega_beam"&&ha21Blue(boss)?.kind.includes("beam_empty")')))
     elif variant=='blue' and scene=='throw':
      g.wait_for_function('boss._hammer.state==="throw"&&!!boss._hammer.throw');p.wait_for_timeout(180)
      checks.append(dict(name='Actual thrown hammer and empty-hand follow-through coexist',passed=g.evaluate('!!boss._hammer.throw&&Number.isFinite(boss._hammer.throw.x+boss._hammer.throw.y)&&ha21Blue(boss)?.kind.startsWith("blue_throw")')))
     else:p.wait_for_timeout(800)
     p.screenshot(path=str(O/(variant+'-'+scene+'.png')))
  p.select_option('#difficulty','hard');p.wait_for_function('!document.querySelector("#replay").disabled');checks.append(dict(name='Hard replay applies actual difficulty',passed=g.evaluate('diffKey==="hard"')))
  p.select_option('#difficulty','normal');p.wait_for_function('!document.querySelector("#replay").disabled');checks.append(dict(name='Normal replay applies actual difficulty',passed=g.evaluate('diffKey==="normal"')))
  b.close()
finally:stop()
checks.append(dict(name='No page console draw or asset errors',passed=not errors,data=errors));r=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors);(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print('SUMMARY',r['passed'],'passed',r['failed'],'failed');sys.exit(bool(r['failed']))
