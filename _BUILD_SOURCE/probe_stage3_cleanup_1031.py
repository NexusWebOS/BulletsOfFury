"""Targeted native launcher death, source geometry and catalogue checks."""
from pathlib import Path
import ast,json,sys,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP,TRAP_RAF
src=ast.parse((R/'_BUILD_SOURCE/probe_stage3_amplify_1031.py').read_text());SETUP=next(ast.literal_eval(n.value)for n in src.body if isinstance(n,ast.Assign)and any(getattr(t,'id','')=='SETUP'for t in n.targets))
W=R/'_shots/stage3_amplify_1031';checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=256;port,stop=serve(str(R))
def ck(n,v,d=None):checks.append({'name':n,'passed':bool(v),'data':d});print('PASS'if v else'FAIL',n,flush=True)
def step(p,n):
 for i in range(0,n,4):assert not p.evaluate(STEP,min(4,n-i));p.wait_for_timeout(1)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof I31!=="undefined"');p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugStartFight(debugFightFor(3,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(3,'boss').kind);BOFCinematicDirector.cancel();setState(GS.PLAY);stageLoadBegin(3)}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(3)&&Object.values(I31_ART.banks).every(a=>XART.rdy(a.key))}',timeout=180000)
  for typ in ['cryoeye','s3interceptor','ac10icejet','s3mine','glaciercarrier','sharddart']:
   p.evaluate(SETUP,[typ,'hard']);step(p,250)
   for impact in range(8):
    if p.evaluate('E.hp<=0'):break
    p.evaluate('()=>hitEnemy(E,999)');step(p,4)
   q=p.evaluate('()=>({hp:E.hp,beams:E._i31.beams.length,shots:I31.events.filter(q=>q.id===E._i31.id&&["shot","cross-lasers"].includes(q.event)).length})')
   ck(typ+' lethal native damage clears active beams',q['hp']<=0 and q['beams']==0,q)
   step(p,90);q2=p.evaluate('()=>({live:enemies.includes(E)&&!E.dead,shots:I31.events.filter(q=>q.id===E._i31.id&&["shot","cross-lasers"].includes(q.event)).length})');ck(typ+' completes native death without new release',not q2['live']and q2['shots']==q['shots'],q2)
  for kind in ['slug','sonic','mine','laser']:
   p.evaluate(SETUP,['ac10icejet','hard']);step(p,40)
   q=p.evaluate("""kind=>{eBullets=[];const b=i31Shot(E,{x:340,y:260,angle:Math.PI/2},kind,true);b.x=340;b.y=260;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawBullets();ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let blue=0,red=0;for(let i=0;i<a.length;i+=4){if(a[i+2]>a[i]+35&&a[i+2]>90)blue++;if(a[i]>a[i+2]+35&&a[i]>90)red++;}return{blue,red,proof:enemyOrdnanceCanIntercept(b),held:b._ai27Held};}""",kind)
   ck(kind+' actual native projectile pixels are visible ice-blue',q['blue']>8 and q['blue']>q['red']*3,q)
  p.evaluate(SETUP,['ac10icejet','hard']);step(p,40)
  q=p.evaluate('()=>{const old=ctx.rotate;let rotations=0;ctx.rotate=function(){rotations++;return old.apply(this,arguments)};try{for(let d=0;d<8;d++){E._i31.head=Math.PI/2+d*TAU/8;drawEnemy(E)}}finally{ctx.rotate=old}return rotations}');ck('All8 interceptor views render actual cells without canvas rotation',q==0,q)
  for fraction in [.05,.25,.5,.75,.9]:
   fixture=SETUP.replace('mapScroll=levelScrollRange()*.35','mapScroll=levelScrollRange()*'+str(fraction))
   initial=p.evaluate(fixture,['modturret-laser','hard']);ck('Full island hull reservation at scroll '+str(fraction),initial is not None and p.evaluate('i31Legal(E,E.x,E.y)'),initial)
  p.evaluate(SETUP,['s3mine','hard']);step(p,120)
  found=False
  for i in range(50):
   step(p,4)
   found=p.evaluate('()=>eBullets.some(b=>b._i31Kind==="mine"&&!b.dead&&Math.hypot(b.x-E.x,b.y-E.y)>75)')
   if found:break
  ck('Mine bomber leaves separated shootable mines',found)
  if found:
   p.evaluate('()=>{window.testMine=eBullets.find(b=>b._i31Kind==="mine"&&!b.dead&&Math.hypot(b.x-E.x,b.y-E.y)>75);pShard(testMine.x,testMine.y,0,1,{mul:20});pBullets.at(-1).vx=pBullets.at(-1).vy=0;}');step(p,4);ck('Actual player round intercepts an ice mine',p.evaluate('testMine.dead'))
  ck('No native cleanup page/console errors',not errors,errors);b.close()

finally:(W/'cleanup-checks.json').write_text(json.dumps(checks,indent=2));stop()
from PIL import Image
A=json.loads((R/'assets/game/levels/stage_03/enemies/amplify_1031/manifest.json').read_text());bad=[]
for name,v in A['banks'].items():
 im=Image.open(R/v['path']);expect=(v['cols']*v['cell'],v['frames']*v.get('dirRows',1)*v['cell'])
 if im.size!=expect or v['cell']%2 or max(im.size)>16383:bad.append([name,im.size,expect])
ck('All32 bank files have registered even cells and valid sheet geometry',len(A['banks'])==32 and not bad,bad)
(W/'cleanup-checks.json').write_text(json.dumps(checks,indent=2));assert all(q['passed']for q in checks)
