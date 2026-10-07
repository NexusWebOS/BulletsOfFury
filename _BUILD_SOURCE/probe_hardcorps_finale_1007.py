"""Native chromium spell / generated-alpha verification, with damage controls."""
from pathlib import Path
import sys,json,base64,ast
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/hardcorps_finale_1007';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];screens=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
port,stop=shoot.serve(str(R))
INIT='''()=>{j3Encounter(B,2);const dr=dr5State(B);dr.introWanted=false;dr.introSeen=true;j3Mimic(B,8);on5FightStart(B);story=null;fb2Talk=null;BOFCinematicDirector.cancel();B.x=worldWidth()/2;B.y=PLAY.y+167;B._drawY=B.y;const D=gd4Create(B,8);D.p.x=B.x;D.p.y=B.y;D.p._hammer.hammerDestroyed=false;D.p._hammer.hammerHP=D.p._hammer.hammerMax;D.p._hammer.state='hammer';B.parts.find(q=>q.id==='hammer').destroyed=false;eBullets=[];pBullets=[];hc7Warm();aa5Warm();player.invuln=0;run.shield=0;run._megaShield=false;player.x=worldWidth()/2;player.y=440;player.dead=false;player._spin=null;}'''
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':960});p.add_init_script('navigator.getGamepads=()=>[]')
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None);p.on('response',lambda r:errors.append(f'{r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(shoot.TRAP_RAF)
  for glob,file in [('EC7','engine_combat_1007'),('HC7_ART','hardcorps_finale_art_1007'),('HC7','hardcorps_finale_1007')]:
   if p.evaluate('v=>eval("typeof "+v)==="undefined"',glob):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/{file}.js')
  def setup(diff='normal'):
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'juggernaut','diff':diff});p.evaluate(INIT)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));screens.append(name)
  setup();p.wait_for_function('()=>Object.values(HC7_ART).every(c=>c.every(a=>XART.rdy(a.key)))&&Object.values(AA5_ART).every(c=>c.every(a=>XART.rdy(a.key)))&&XART.rdy(S4REV1006_ART.key)',timeout=120000)
  q=p.evaluate('''()=>{const C=hc7RiftStart(B),out=[];for(const t of [.10,.30,.55,.90,1.55,2.45]){C.t=t;const rig=fmcRig(B),palm=hc7CastPalm(B);out.push({frame:HC7.draws.castFrame,palmY:palm.y,bodyY:B.y,headY:B.y-73,opaque:rig.every(v=>v.alpha===1),hit:rig.find(v=>v.p.id==='hammer')?.x});}return out;}''')
  ck(len(set(qr['frame'] for qr in q))==6,'six distinct raised-hand anticipation poses before release')
  ck(all(qr['opaque'] for qr in q),'cast physical body and Hammer hit module stay opaque')
  ck(q[3]['palmY']<q[3]['headY'] and q[4]['palmY']<q[4]['headY'],'free hand reaches above helmet and keeps measured overhead emitter')
  for i,t in enumerate([.10,.55,.90,1.55,2.45]):p.evaluate('t=>{B._r30.hc7Rift.t=t;B._r30.clock=t;}',t);snap('cast-'+str(i))
  # Read actual canvas images at paused clock and intermediate blend phases.
  q=p.evaluate('''()=>{const out=[];for(const t of [0,.02,.04,.06]){B._r30.clock=t;ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);hc7VoidDraw(B,200,200,280);out.push(cv.toDataURL());}return out;}''')
  ck(len(set(q))==4,'void draws distinct native pixels between authored frames')
  a=p.evaluate('()=>{ctx.clearRect(0,0,cv.width,cv.height);hc7VoidDraw(B,200,200,280);return cv.toDataURL();}');p.wait_for_timeout(250)
  b=p.evaluate('()=>{ctx.clearRect(0,0,cv.width,cv.height);hc7VoidDraw(B,200,200,280);return cv.toDataURL();}');ck(a==b,'paused void pixels do not follow wall clock')
  # Positive pull, zero edge pull, independent P2, and real core damage.
  for key,xy,expected in [('near',[70,0],True),('outside',[250,0],False)]:
   setup();q=p.evaluate('''v=>{const C=hc7RiftStart(B);C.phase='active';C.t=.8;C.pulse=0;player.x=C.x+v[0];player.y=C.y+v[1];const ox=player.x;hc7RiftStep(B,1/60);return{moved:player.x<ox,dead:player.dead};}''',xy)
   ck(q['moved']==expected and not q['dead'],key+' pilot '+('is pulled inward' if expected else 'has zero pull outside visible perimeter'))
  setup();q=p.evaluate('''()=>{const C=hc7RiftStart(B);C.phase='active';C.t=.8;player.x=C.x;player.y=C.y;player.invuln=0;hc7RiftStep(B,1/60);return player.dead||run.shield<0;}''');ck(q,'stationary unshielded pilot touching void center takes real damage')
  setup();q=p.evaluate('''()=>{coopOn=true;run2.pilot='yuri';p2Index=PILOTS.findIndex(q=>q.key==='yuri');player2.reset();player2.invuln=0;run2.shield=0;const C=hc7RiftStart(B);C.phase='active';C.t=.8;C.pulse=0;player.x=C.x+C.radius+25;player.y=C.y;player2.x=C.x+100;player2.y=C.y;const x1=player.x,x2=player2.x;hc7RiftStep(B,1/60);return player.x===x1&&player2.x<x2&&!player.dead&&!player2.dead;}''');ck(q,'rift evaluates each living co-op pilot independently')
  # Lightning off window never collides; active interval has a real damage control.
  for when,should in [(0.5,False),(1.0,True),(1.23,False)]:
   setup();q=p.evaluate('''when=>{const C=hc7RiftStart(B);C.phase='active';C.t=.82;C.pulse=0;hc7RiftPlan(B,C);const L=C.lanes[0];L.age=when;const u=.88;player.x=lerp(L.x,L.ex,u);player.y=lerp(L.y,L.ey,u);player.invuln=0;hc7RiftStep(B,1/60);return player.dead;}''',when);ck(q==should,'lightning '+str(when)+'s collision matches visible phase')
  # Break through real module damage, verify targeting uses current cast pose.
  setup();q=p.evaluate('''()=>{const C=hc7RiftStart(B);C.t=1.6;const D=gd4Create(B,8),v=r30Parts(B).find(q=>q.p.id==='hammer'),target=retinaBossTargets(B).find(q=>String(q._retinaKey||q.id||'').includes('hammer'));const ready=hammerWeaponTargetable(D.p);B._lastPart=v.p;modularHit(D.p._hammer.hammerHP+10);return{ready,cancel:!B._r30.hc7Rift,destroyed:D.p._hammer.hammerDestroyed,state:D.p._hammer.state};}''')
  ck(q['ready'] and q['cancel'] and q['destroyed'],'real Hammer module hit interrupts cast and removes pull/lightning immediately')
  setup();q=p.evaluate('''()=>{hc7RiftStart(B);const hp=[...j3State(B).hp];j3Clear(B);return !B._r30.hc7Rift&&JSON.stringify(hp)===JSON.stringify(j3State(B).hp);}''');ck(q,'encounter clear cancels spell without changing any saved pool')
  # Natural source-controller entry, followed by actual input escape on all modes.
  setup();q=p.evaluate('''()=>{player.invuln=1e9;const D=gd4Create(B,8);D.hc7Cd=.2;let found=false;for(let i=0;i<1200;i++){r30Tick(B,1/60);if(B._r30.hc7Rift){found=true;break;}}return{found,history:HC7.events.slice(-4)};}''');ck(q['found'],'ordinary Hammer donor controller naturally enters the new spell')
  for diff in ['easy','normal','hard','furious']:
   setup(diff);p.evaluate('''()=>{pilotIndex=PILOTS.findIndex(q=>q.key==='juggernaut');run.pilot='juggernaut';player.reset();player.invuln=0;run.shield=0;run._megaShield=false;const C=hc7RiftStart(B);player.x=C.x;player.y=C.y+75;}''')
   p.keyboard.down('ArrowRight');p.evaluate('''()=>{for(let i=0;i<150;i++)updatePlay(1/60);}''');p.keyboard.up('ArrowRight')
   q=p.evaluate('''()=>{const C=B._r30.hc7Rift;window.escapeStart={x:player.x,y:player.y};for(let i=0;i<365;i++)updatePlay(1/60);return{alive:!player.dead,far:Math.hypot(player.x-(C?.x||worldWidth()/2),player.y-(C?.y||322))>(C?.radius||180),x:player.x,y:player.y,unchanged:Math.abs(player.x-escapeStart.x)<.001};}''')
   ck(q['alive'] and q['far'] and q['unchanged'],diff+' slowest pilot escapes with ordinary movement and holds edge without pull');snap('edge-'+diff)
  setup();p.evaluate('()=>{const C=hc7RiftStart(B);C.phase="active";C.t=1.05;C.pulse=0;hc7RiftPlan(B,C);for(const L of C.lanes){L.age=1;L.phase="active";}B._r30.clock=5;player.x=C.x-C.radius-30;player.y=400;}');snap('rift-active')
  p.evaluate('()=>{const C=B._r30.hc7Rift;C.phase="recover";C.t=.6;B._r30.clock=6;}');snap('rift-recovery')
  p.wait_for_timeout(300);ck(not errors,'zero native page/console/missing-art errors');br.close()
finally:stop()
report={'checks':checks,'errors':errors,'screens':screens,'scope':'Native controlled states plus actual keyboard escape and real damage controls; not a full campaign clear.'}
(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
thumbs=[]
for name in screens:
 im=Image.open(O/(name+'.png')).convert('RGB');im.thumbnail((240,270));thumbs.append((name,im))
contact=Image.new('RGB',(4*260,((len(thumbs)+3)//4)*300),(8,10,18));g=ImageDraw.Draw(contact)
for i,(name,im) in enumerate(thumbs):x=(i%4)*260;y=(i//4)*300;contact.paste(im,(x,y+20));g.text((x+5,y+3),name,fill=(220,225,240))
contact.save(O/'contact.jpg',quality=94)
(O/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>Chromium finale review</title><style>body{background:#080b13;color:#def;font:16px sans-serif}main{display:flex;flex-wrap:wrap;gap:16px}img{width:360px;image-rendering:pixelated}figure{margin:0}</style><h1>Chromium finale — native render</h1><main>'+''.join('<figure><figcaption>'+n+'</figcaption><img src="'+n+'.png"></figure>' for n in screens)+'</main>',encoding='utf-8')
print(json.dumps({'checks':len(checks),'failed':[q['name'] for q in checks if not q['ok']],'errors':errors}))
if errors or any(not q['ok'] for q in checks):raise SystemExit(1)
