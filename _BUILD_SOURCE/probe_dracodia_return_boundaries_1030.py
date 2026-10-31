from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_return_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[];port,stop=serve(str(R))
def check(name,value):checks.append({'name':name,'passed':bool(value)});print(('PASS 'if value else'FAIL ')+name,flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank in ['normal','hard','furious']:
   p.evaluate('''rank=>{diffKey=rank;spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;B.hp=0;r30Break(B);}''',rank);p.evaluate(STEP,180)
   q=p.evaluate('({t:rd76State(B)?.t,mode:B._r30.mode})');check(rank+' enters return through native defeat',q['mode']=='v18returnDownload')
   p.evaluate("setState('paused')");p.evaluate(STEP,120);paused=p.evaluate('rd76State(B)?.t');check(rank+' pause freezes transfer clock',paused==q['t'])
   p.evaluate("setState(GS.PLAY)");p.evaluate(STEP,260);q=p.evaluate('({mode:B._r30.mode,hp:B.hp,expected:j3State(B).hp[0],bullets:eBullets.length,invuln:player.invuln,enter:B.enter,parts:B.parts.map(p=>p.id)})');check(rank+' resumes into valid native body',q['mode']=='fight'and not q['enter']and q['hp']==q['expected']and q['parts']==['core','left','right'])
   check(rank+' releases temporary transfer immunity',q['invuln']<=.5)
  p.evaluate("()=>{spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;RD76.events=[];j3Morph(B,'home');}")
  check('Living-form morph keeps its existing owner',p.evaluate("!rd76State(B)&&!!rd30State(B).transition&&B._r30.mode==='v18formOut'"))
  p.evaluate(STEP,300)
  check('Living-form morph still completes',p.evaluate("B._r30.mode==='fight'&&B._r30.v18.form===0"))
  p.evaluate("()=>{v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;B.hp=0;r30Break(B);}");p.evaluate(STEP,180)
  p.evaluate("()=>{spawnBoss('vileexistence');window.B=boss;}");p.evaluate(STEP,12)
  check('Retry discards the old transfer state',p.evaluate("!rd76State(B)&&j3State(B).encounter===0"))
  check('First host still uses its original entry',p.evaluate("B._r30.mode!=='v18returnDownload'"))
  check('No browser or native draw errors',not errors);br.close()
finally:stop();(W/'boundary-checks.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2))
assert all(c['passed']for c in checks),checks
