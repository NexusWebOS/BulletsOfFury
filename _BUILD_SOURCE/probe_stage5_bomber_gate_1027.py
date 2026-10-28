from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,argparse
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=R/'_shots/stage5_bomber_gate_1027');W=parser.parse_args().out;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
port,stop=serve(str(R));checks=[];errors=[];console=[];http=[]
def check(name,v,data=None):
 checks.append({'name':name,'pass':bool(v),'data':data});(W/'checks-partial.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');assert v,name
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:console.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof SB28!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=5;stageLoadBegin(5)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}',timeout=180000,polling=100);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  def setup(diff='furious'):
   p.evaluate('''d=>{run.ngplus=false;diffKey=d;debugUnlocked=true;debugStartFight({stage:5,role:'mini',kind:'siegebomber',name:'Stage5 modular gate'},{pilot:'cole',record:false});DBGT.god=true;spawnSubBoss('siegebomber');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);subBossActive=true;}''',diff)
   for i in range(30):
    step(15)
    if p.evaluate('subBoss&&!subBoss.enter&&subBoss._bomber.mode!=="entry"'):break
   p.evaluate('()=>{enemies=[];powerups=[];l5Rocks=[];boss=null;bossActive=false;pBullets=[];eBullets=[];}');p.wait_for_timeout(400);step(1)
  for diff in['easy','normal','hard','furious']:
   setup(diff)
   closed=p.evaluate('''()=>{const b=subBoss,B=b._bomber,hp=B.core;return{parts:B.parts.map(p=>({id:p.id,hp:p.hp})),at:siegeBomberAt(b,b.x,b.y),solid:subBossSolidAt(b.x,b.y),targets:siegeBomberTargets(b).map(t=>t._retinaId),space:spaceTargets().filter(t=>t._retinaOwner===b).map(t=>t._retinaId),core:hp,coreMax:B.coreMax,beam:siegeBomberBeam(b,{x:b.x,w:4,top:0,bot:VH})}}''')
   check(diff+' core is absent from point, solid, beam, Retina and space collisions while all4 modules live',len(closed['parts'])==4 and closed['at']is None and not closed['solid']and closed['beam']is None and len(closed['targets'])==4 and'bomber-core'not in closed['space'],closed)
   blocked=p.evaluate('''()=>{const b=subBoss,B=b._bomber,hp=B.core,whole=b.hp,stale=SB28.base.targets(b).find(t=>t._retinaId==='bomber-core');siegeBomberHit(b,999,b.x,b.y,'core');hitSubBoss(999);retinaMissileDamage(stale,999,{kind:'gmiss',x:b.x,y:b.y});return{core:B.core,hp,whole,bhp:b.hp}}''')
   check(diff+' direct, no-coordinate and stale Retina core damage cannot bypass the gate',blocked['core']==blocked['hp']and blocked['whole']==blocked['bhp'],blocked)
   paths=p.evaluate('''()=>{const b=subBoss,B=b._bomber,out=[];for(const shape of siegeBomberParts(b).filter(p=>p.id!=='core')){let first=null;for(let y=Math.min(VH-35,b.y+b.h);y>shape.y-shape.h;y-=2){const q=siegeBomberAt(b,shape.x,y,2);if(q){first=q;break;}}out.push({id:shape.id,point:subBossHitPart(shape.x,shape.y),solid:subBossSolidAt(shape.x,shape.y),first,beam:siegeBomberBeam(b,{x:shape.x,w:4,top:0,bot:VH})?.id});}return out}''')
   check(diff+' all4 ordinary bullet lanes and held-beam lanes reach the intended modules through the body',all(q['point']==q['first']==q['beam']==q['id']and q['solid']for q in paths),paths)
   travel=p.evaluate('''()=>{const b=subBoss,B=b._bomber,before=B.core,q={kind:'spaceLaser',x:b.x,y:VH-40,vx:0,vy:-5,w:4,h:10,dmg:7,lv:1,t:0};let frames=0;while(!q.dead&&q.kind==='spaceLaser'&&frames++<150)spaceBulletTick(q,1/60);return{coreBefore:before,coreAfter:B.core,kind:q.kind,y:q.y,frames}}''')
   check(diff+' an actual space pulse crosses the protected body and leaves without an impact',travel['coreBefore']==travel['coreAfter']and travel['kind']=='spaceLaser'and travel['y']<0,travel)
   hits=p.evaluate('''()=>{const b=subBoss,B=b._bomber,out=[],core=B.core;for(const shape of siegeBomberParts(b).filter(p=>p.id!=='core')){const m=B.parts.find(p=>p.id===shape.id),hp=m.hp,q={kind:'spaceLaser',x:shape.x,y:Math.min(VH-35,b.y+b.h+50),vx:0,vy:-4,w:4,h:10,dmg:7,lv:1,t:0};let frames=0;while(!q.dead&&q.kind==='spaceLaser'&&frames++<150)spaceBulletTick(q,1/60);out.push({id:shape.id,before:hp,after:m.hp,coreBefore:core,coreAfter:B.core,kind:q.kind,frames});}return out}''')
   check(diff+' real native space pulses damage each of the4 modules while reserving all body HP',all(q['after']<q['before']and q['coreAfter']==q['coreBefore']and q['kind']=='spaceImpact'for q in hits),hits)
   if diff=='furious':
    step(1);p.screenshot(path=str(W/'modules-hit.png'))
   breaks=p.evaluate('''()=>{const b=subBoss,B=b._bomber,out=[];for(const m of B.parts.slice()){const shape=siegeBomberParts(b).find(q=>q.id===m.id);siegeBomberHit(b,m.hp+1,shape.x,shape.y,m.id);const core=B.core;siegeBomberHit(b,1,b.x,b.y,'core');out.push({id:m.id,live:B.parts.filter(p=>p.hp>0).length,coreBefore:core,coreAfter:B.core,locked:sb28Closed(b),targets:siegeBomberTargets(b).map(t=>t._retinaId)});}return out}''')
   check(diff+' the body stays protected with3,2 or1 surviving modules and opens only after the fourth',all(q['locked']and q['coreBefore']==q['coreAfter']and'bomber-core'not in q['targets']for q in breaks[:3])and not breaks[3]['locked']and breaks[3]['coreAfter']<breaks[3]['coreBefore']and breaks[3]['targets']==['bomber-core'],breaks)
   opened=p.evaluate('''()=>{const b=subBoss,B=b._bomber;return{at:siegeBomberAt(b,b.x,b.y),solid:subBossSolidAt(b.x,b.y),beam:siegeBomberBeam(b,{x:b.x,w:4,top:0,bot:VH})?.id,space:spaceTargets().filter(t=>t._retinaOwner===b).map(t=>t._retinaId),hp:b.hp,core:B.core,pool:B.core+B.parts.reduce((s,p)=>s+p.hp,0)}}''')
   check(diff+' exposed body is reachable by every weapon path and preserves the native remaining HP budget',opened['at']==opened['beam']=='core'and opened['solid']and opened['space']==['bomber-core']and opened['hp']==opened['core']==opened['pool'],opened)
   if diff=='furious':step(1);p.screenshot(path=str(W/'core-open.png'))
  # Actual visible module flash was generated by native pulse hits above; the
  # final fresh fixture isolates its onset and expiry against the intact core.
  setup();p.evaluate("()=>{const b=subBoss,p=siegeBomberParts(b).find(q=>q.id==='laserL');window.sbShape=p;window.sbBefore=b._bomber.parts.find(q=>q.id===p.id).hp;siegeBomberHit(b,5,p.x,p.y,p.id)}");step(1)
  flash=p.evaluate('''()=>{const b=subBoss,p=sbShape,d=ctx.getImageData(Math.floor(p.x-camLeftX()-p.w/2),Math.floor(p.y-p.h/2),Math.ceil(p.w),Math.ceil(p.h)).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240)white++;return{white,flash:b._bomber.parts.find(q=>q.id===p.id).flash,hp:b._bomber.parts.find(q=>q.id===p.id).hp,expected:sbBefore-5}}''');check('Live module damage still produces native white pixels and its own HP loss',flash['white']>80 and flash['flash']>0 and flash['hp']==flash['expected'],flash);p.screenshot(path=str(W/'native-flash.png'));step(20);check('Native module flash still expires',p.evaluate('subBoss._bomber.parts.find(p=>p.id==="laserL").flash===0'))
  p.evaluate('''()=>{const b=subBoss;for(const m of b._bomber.parts.slice()){const q=siegeBomberParts(b).find(p=>p.id===m.id);siegeBomberHit(b,m.hp+1,q.x,q.y,m.id);}siegeBomberHit(b,b._bomber.core+1,b.x,b.y,'core')}''');check('Full native module and core exhaustion reaches the original death owner',p.evaluate('subBoss.dead&&subBoss.hp===0'));step(300);check('Native miniboss death still completes',p.evaluate('subBossDone||state===GS.FLYOVER||state==="debugfade"'))
  p.evaluate("()=>{run.stage=6;spawnSubBoss('siegebomber');subBoss.enter=false;subBoss._bomber.mode='recover';}");scope=p.evaluate('''()=>{const b=subBoss,before=b._bomber.core;siegeBomberHit(b,5,b.x,b.y,'core');return{closed:sb28Closed(b),before,after:b._bomber.core}}''');check('Stage6 pursuit bomber now uses the same protected core rule',scope['closed']and scope['after']==scope['before'],scope)
  known=[q for q in http if q['url'].endswith('/chronos_rageform_1026/stop_empty.png')and q['status']==404];unexpected=[q for q in http if q not in known]
  check('No new errors; only the already-documented optional Chronos preload404 is allowed',not errors and not unexpected and len(console)<=len(known)and all('Failed to load resource:'in q and'404'in q for q in console),{'page':errors,'console':console,'knownOptionalAsset':known,'unexpectedHTTP':unexpected});br.close()
finally:
 stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'pageErrors':errors,'consoleErrors':console,'HTTPerrors':http},indent=2),encoding='utf-8')
print(f'{len(checks)} native checks passed.')
