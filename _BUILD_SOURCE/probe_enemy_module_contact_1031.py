"""Stable-origin boot and actual authored module contact/defeat checks."""
from pathlib import Path
import json,sys,base64
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
W=R/'_shots/enemy_flight_1031/module-probe';W.mkdir(exist_ok=True);checks=[];errors=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if passed else'FAIL',name,flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  for stage in range(4,10):
   p=br.new_page(viewport={'width':1280,'height':800});local=[];p.on('pageerror',lambda e:local.append(str(e)));p.on('console',lambda m:local.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
   p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('(s)=>EA11.setup(s,"hard")',stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000);p.wait_for_timeout(300)
   ck(f'Stage{stage} stable-origin boot',not local,local);errors.extend(local)
   if stage==4:
    specs=json.loads((R/'_shots/enemy_flight_1031/before/stage4-specs.json').read_text());spec=next(s for s in specs if s['type']=='s4interceptor')
    for angle in[0,45,90,135,180,270]:
     p.evaluate('s=>{EA11.case(s);bossWarned=false;story=thaw=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;for(let i=0;i<100;i++)updatePlay(1/60);}',spec)
     q=p.evaluate('''deg=>{E.x=worldWidth()/2;E.y=230;E.spin=deg*Math.PI/180;E._r46.head=Math.PI/2+E.spin;drawWorld(0);const side=deg===90||deg===180?'left':'right',p=modularJetMount(E,side==='left'?-1:1);let bullet=null;
      for(let r=0;r<20&&!bullet;r++)for(let y=-r;y<=r&&!bullet;y++)for(let x=-r;x<=r;x++){const b={x:p.x+x,y:p.y+y,w:1,h:1};if(enemyModuleHitPart(E,b)?.name===side){bullet=b;break;}}
      const before=JSON.parse(JSON.stringify(E._r30));if(!bullet)return{found:false};_dmgBullet=bullet;try{hitEnemy(E,.1);}finally{_dmgBullet=null;}return {found:true,side,bullet,mount:p,worldSide:bullet.x<E.x?'left':'right',before:{left:before.left.hp,right:before.right.hp},after:{left:E._r30.left.hp,right:E._r30.right.hp},flash:E.flash};}''',angle)
     side=q.get('side');other='right'if side=='left'else'left'
     ck(f'{angle}deg real module pixels route native damage',q.get('found')and q['after'][side]<q['before'][side]and q['after'][other]==q['before'][other]and q['flash']>0,q)
    # Keep the real queued round and destroy its particular native gun pool.
    p.evaluate('s=>{EA11.case(s);bossWarned=false;for(let i=0;i<100;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=180;drawWorld(0);}',spec)
    q=p.evaluate('''()=>{const m=modularJetPoint(E,-1);window.moduleMissile=eShootT(m.x,m.y,Math.PI/2,170,'emissile',{owner:E});const name=moduleMissile._r46PartGate;let hits=0;
     while(E._r30[name].hp>0&&hits++<100){const p=modularJetMount(E,name==='left'?-1:1);let bullet=null;for(let y=-16;y<=16&&!bullet;y++)for(let x=-16;x<=16;x++){const b={x:p.x+x,y:p.y+y,w:1,h:1};if(enemyModuleHitPart(E,b)?.name===name){bullet=b;break;}}if(!bullet)break;_dmgBullet=bullet;try{hitEnemy(E,.3);}finally{_dmgBullet=null;}}
     updateEffects(1/60);return {name,hits,hp:E.hp,gunHP:E._r30[name].hp,dead:moduleMissile.dead,pending:R46.pending.has(moduleMissile),locks:playerLocks.filter(L=>L.src===E).map(L=>L.launches.map(s=>({done:s.done,dead:s.fire?._r46Round?.dead}))),ports:air17Ports(E).map(p=>p.socket)};}''')
    ck('Destroyed module cancels only its pending missile and warning',q.get('hp',0)>0 and q.get('gunHP')==0 and q.get('dead')and not q.get('pending')and all(not any(not s.get('done')and s.get('dead')for s in L)for L in q.get('locks',[])),q)
    q=p.evaluate('''()=>{for(let i=0;i<8;i++)updatePlay(1/60);const C=air17State(E);C.target={x:player.x,y:player.y};C.missile=false;R46.fx=[];E._r46Flash={};const owner=ai27Context;ai27Context=E;try{air17Emit(E);}finally{ai27Context=owner;}const ports=air17Ports(E),fx=R46.fx.filter(f=>f.owner===E);return {ports,flashes:fx.map(f=>f.p),both:ports.length===1&&fx.length===1&&Math.hypot(ports[0].x-fx[0].p.x,ports[0].y-fx[0].p.y)<1};}''')
    ck('Surviving gun retains its real muzzle after the other gun breaks',q['both'],q)
    p.screenshot(path=str(W/'module-break.png'))
    p.evaluate('s=>{EA11.case(s);bossWarned=false;for(let i=0;i<100;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=180;r46Attach(E);}',spec)
    q=p.evaluate('''()=>{const C=air17State(E);C.target={x:player.x,y:player.y};C.missile=false;R46.fx=[];E._r46Flash={};const owner=ai27Context;ai27Context=E;try{air17Emit(E);}finally{ai27Context=owner;}const ports=air17Ports(E),flashes=R46.fx.filter(f=>f.owner===E);return {ports,flashes:flashes.map(f=>f.p),both:ports.every(p=>flashes.some(f=>Math.hypot(p.x-f.p.x,p.y-f.p.y)<1))};}''')
    ck('Actual twin gun release has a separate flash at both mouths',q['both']and len(q['flashes'])==2,q)
   p.close()
  br.close()
finally:(W/'errors.json').write_text(json.dumps(errors,indent=2))
sys.exit(0 if all(c['passed']for c in checks)else 1)
