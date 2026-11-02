"""Targeted native launcher death, source geometry and catalogue checks."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP,TRAP_RAF
src=ast.parse((R/'_BUILD_SOURCE/probe_stage2_amplify_1031.py').read_text());SETUP=next(ast.literal_eval(n.value)for n in src.body if isinstance(n,ast.Assign)and any(getattr(t,'id','')=='SETUP'for t in n.targets))
W=R/'_shots/stage2_amplify_1031';checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R))
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print('PASS'if v else'FAIL',n,flush=True)
def step(p,n):
 for i in range(0,n,4):assert not p.evaluate(STEP,min(4,n-i));p.wait_for_timeout(1)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof V31!=="undefined"');p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugStartFight(debugFightFor(2,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(2,'boss').kind);BOFCinematicDirector.cancel();setState(GS.PLAY);stageLoadBegin(2)}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(2)&&Object.values(V31_ART.banks).every(a=>XART.rdy(a.key))}',timeout=180000)
  for typ in ['disc','cruc','carrier','lavasnake','v31elite_flame','v31elite_wall']:
   fixture=SETUP.replace("{_modWeapon:","{_v31Role:'"+typ.split('_')[-1]+"',_modWeapon:")if typ.startswith('v31elite_')else SETUP
   p.evaluate(fixture,[typ,'hard']);step(p,250)
   # Native pools reserve one HP on their first lethal event. The shield and
   # hull are separate pools; use distinct real impacts, never HP writes.
   for impact in range(8):
    if p.evaluate('E.hp<=0'):break
    p.evaluate('()=>hitEnemy(E,999)');step(p,4)
    if p.evaluate('!!E._eshStun'):step(p,90)
   q=p.evaluate('()=>{drawWorld(0);return{hp:E.hp,dead:!!E.dead,dying:E._dyingT,beams:E._v31.beams.length,pending:!!E._v31.heavy,phase:E._v31.phase,key:E._v31Rendered?.key,shield:E._esh,shots:V31.events.filter(q=>q.id===E._v31.id&&["shot","beam","volcano-orb","deploy-jet"].includes(q.event)).length}}')
   ck(typ+' native lethal damage clears active/pending attacks',q['hp']<=0 and q['beams']==0 and not q['pending']and q['phase']=='destroyed',q)
   step(p,90);q2=p.evaluate('()=>({live:enemies.includes(E)&&!E.dead,shots:V31.events.filter(q=>q.id===E._v31.id&&["shot","beam","volcano-orb","deploy-jet"].includes(q.event)).length})');ck(typ+' death completes without a new release',not q2['live']and q2['shots']==q['shots'],q2)
  ck('No native cleanup page/console errors',not errors,errors);b.close()
finally:(W/'cleanup-checks.json').write_text(json.dumps(checks,indent=2));stop()
from PIL import Image
A=json.loads((R/'assets/game/levels/stage_02/enemies/amplify_1031/manifest.json').read_text());bad=[]
for name,v in A['banks'].items():
 im=Image.open(R/v['path']);expect=(v['cols']*v['cell'],v['frames']*v['dirRows']*v['cell'])
 if im.size!=expect or v['cell']%2 or max(im.size)>16383:bad.append([name,im.size,expect])
ck('All85 bank files have registered even cells and valid sheet geometry',len(A['banks'])==85 and not bad,bad)
cat=json.loads((R/'assets/data/enemy_atlas_1013.json').read_text());ck('Native catalogue removes retired enemies and registers new elite/snake owners',not any(e.get('spawn',{}).get('type')in['eye','magmaorb','crawl']for e in cat['entries'])and any(e.get('spawn',{}).get('type')=='lavasnake'for e in cat['entries']))
(W/'cleanup-checks.json').write_text(json.dumps(checks,indent=2));assert all(q['passed']for q in checks)
