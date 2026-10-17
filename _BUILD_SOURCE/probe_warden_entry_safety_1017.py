"""Native Warden wing depth entry/contact, respawn, combat and hit-feedback regression."""
from pathlib import Path
import ast,json,sys,hashlib,traceback,subprocess
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_entry_safety_1017';O.mkdir(parents=True,exist_ok=True)
BASELINE='--baseline' in sys.argv
RELEASE='--release' in sys.argv
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  if BASELINE:p.route('**/assets/warden_last_stand_1017.js*',lambda route:route.fulfill(path=str(O/'warden-before.js'),content_type='application/javascript'))
  if RELEASE:
   p.route('**/index.html',lambda route:route.fulfill(path=str(O/'index-release.html'),content_type='text/html'))
   for filename in ['game.js','modular_roster_0927.js','orbs_1010.js','spread_1001.js']:
    body=subprocess.check_output(['git','show','HEAD:assets/'+filename],cwd=R).decode()
    p.route('**/assets/'+filename+'*',lambda route,request,body=body:route.fulfill(body=body,content_type='application/javascript'))
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof wing17JetTick==="function"');p.evaluate(shoot.TRAP_RAF)
  def setup(diff):
   p.evaluate(SETUP,dict(stage=4,kind='olivewarden',mini=True,pilot='cole',diff=diff))
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(4)&&!!air13Pose("flight_variant_4","heading",0)&&XART.rdy("mr27_iron")&&bmfReady("game")}')
   p.evaluate('''()=>{B._er26.engaged=false;er26Tick(B,0);B._phaseInvuln=0;B._noHit=false;B._s4MiniSafe=true;story=fb2Talk=null;BOFCinematicDirector.cancel();
    stagePlan=[];VP12.next=CP12.next=EP13.next=9999;enemies=[];eBullets=[];pBullets=[];Input.keys={};special=null;run.shield=0;
    wing17State(B);B._wing17.c=wing17CentreStep(B);B._wing17.slots.forEach(s=>s.wait=999);window.entryCalls=0;
    if(!window.entryHitBase){window.entryHitBase=playerHit;playerHit=function(){entryCalls++;return entryHitBase.apply(this,arguments)}}
    window.entryReady=function(){player.reset();player.invuln=0;run.shield=0;story=fb2Talk=null;GP4.death=null;GP4.deaths=[];entryCalls=0;};
    window.entryContact=function(){entryReady();player.x=E.x;player.y=E.y;eBullets=[];pBullets=[];WLS17.base.update(0);return{dead:player.dead,calls:entryCalls,shield:run.shield,noHit:E._noHit,phase:E._wing17.phase,t:E._wing17.t,player:{x:player.x,y:player.y},jet:{x:E.x,y:E.y}};};}''')
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit()}');p.screenshot(path=str(O/(name+'.png')))
  for diff in ['hard','furious','insanity']:
   for edge in (['S','N'] if diff=='hard' else ['S','N','E','W']):
    setup(diff)
    sample=p.evaluate('''edge=>{const s=B._wing17.slots.find(s=>s.edge===edge);window.E=wing17Spawn(B,s);s.e=E;
     const born=E._noHit===true,rows=[];for(const age of [0,.12,.32,.60,.90,1.20,WING17_ENTRY-.001]){E._wing17.t=age;wing17JetTick(E,0);rows.push({age,safe:E._noHit,phase:E._wing17.phase});}
     E._wing17.t=.70;wing17JetTick(E,0);return{born,rows};}''',edge)
    check(diff+' '+edge+' spawn and entire scaling entry are non-collidable',sample['born'] and all(q['safe'] and q['phase']=='enter' for q in sample['rows']),sample)
    collision=p.evaluate('entryContact()')
    check(diff+' '+edge+' real player survives overlapping the incoming jet',not collision['dead'] and collision['calls']==0,collision)
    if diff=='furious' and edge in ['S','E']:snap('safe-'+edge.lower()+'-overlap')
    combat=p.evaluate('''()=>{entryReady();E._wing17.t=WING17_ENTRY;wing17JetTick(E,0);const q=entryContact();return{...q,scale:1};}''')
    check(diff+' '+edge+' contact activates on the combat plane',combat['dead'] and combat['calls']>0 and not combat['noHit'],combat)
    respawn=p.evaluate('''()=>{entryReady();const slot=E._wing17.slot;E.dead=true;wing17Tick(B,.001);const held=slot.wait;
     wing17Tick(B,WING17_RESPAWN-.02);const early=slot.e===null;wing17Tick(B,.03);E=slot.e;
     if(!E)return{held,early,missing:true};const same=E._wing17.slot.edge===slot.edge,born=E._noHit;
     E._wing17.t=.70;wing17JetTick(E,0);return{held,early,same,born,contact:entryContact()};}''')
    check(diff+' '+edge+' five-second replacement uses the same safe entry',respawn.get('early') and respawn.get('same') and respawn.get('born') and not respawn.get('contact',{}).get('dead',True) and respawn['contact']['calls']==0,respawn)
  setup('furious')
  result=p.evaluate('''()=>{const s=B._wing17.slots[0];E=wing17Spawn(B,s);s.e=E;const samples=[];
   for(let i=0;i<210;i++){wing17JetTick(E,1/60);samples.push({t:E._wing17.t,shot:eBullets.filter(b=>b._wing17Shot).length,phase:E._wing17.phase});}
   return{early:samples.filter(q=>q.t<WING17_ENTRY).some(q=>q.shot>0),warn:samples.some(q=>q.phase==='warn'),shots:eBullets.filter(q=>q._wing17Shot).length};}''')
  check('Entry releases no shots; settled wing still warns and fires',not result['early'] and result['warn'] and result['shots']>0,result)
  flash=p.evaluate('''()=>{E._wing17.t=WING17_ENTRY;wing17JetTick(E,0);E.flash=0;
   function image(){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(-camX,0);drawEnemy(E);ctx.restore();return ctx.getImageData(0,0,cv.width,cv.height).data;}
   const a=image(),hp=E.hp;hitEnemy(E,1);const c=image();let pixels=0;for(let i=0;i<a.length;i+=4)if(a[i]!==c[i]||a[i+1]!==c[i+1]||a[i+2]!==c[i+2])pixels++;
   const out={pixels,hpLost:hp-E.hp,flash:E.flash};player.invuln=1e9;for(let i=0;i<30;i++)updatePlay(1/60);out.expired=E.flash<=0;return out;}''')
  check('On-plane wing takes damage, visibly flashes and expires normally',flash['pixels']>20 and flash['hpLost']>0 and flash['flash']>0 and flash['expired'],flash)
  check('No browser or missing-asset errors',not errors,errors);browser.close()
except Exception as e:errors.append(str(e));print(traceback.format_exc(),flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,
  runtime_sha256=hashlib.sha256(((O/'warden-before.js') if BASELINE else (R/'assets/warden_last_stand_1017.js')).read_bytes()).hexdigest(),scope='Native fixture isolates the miniboss hull via _s4MiniSafe, retaining real helper contact, playerHit, damage and renderer. Not a full human clear.')
 (O/('baseline.json' if BASELINE else 'release-verification.json' if RELEASE else 'verification.json')).write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}),flush=True)
if errors or report['failed']:sys.exit(1)
