"""Isolated native collision/flight fixtures, separate from full films."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/furious_encounters_1102';checks=[];errors=[]
def ck(name,data,ok):
 checks.append(dict(name=name,data=data,passed=bool(ok)));print('PASS' if ok else 'FAIL',name,data,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 p.evaluate('''()=>{EA11.setup(6,'furious');spawnSubBoss('siegefortress17');window.B=subBoss;}''');p.wait_for_function('()=>{stageLoadTick();return fb112Ready()}',timeout=180000)
 q=p.evaluate('''()=>{B.enter=false;B.x=worldWidth()/2;B.y=B.ty;const q=B._fb112;q.seq=1;fb112Start(B);const out=[];let max=0,jumps=[];for(let i=0;i<310;i++){let x=B.x,y=B.y,phase=q.phase;fb112Tick(B,1/60);const d=Math.hypot(x-B.x,y-B.y);if(d>100)jumps.push({from:[x,y],to:[B.x,B.y],outside:x<camLeftX()-125||x>camRightX()+125});else max=Math.max(max,d);out.push({phase:q.phase,x:B.x,y:B.y});}return{maxStep:max,jumps,phases:[...new Set(out.map(r=>r.phase))],returned:out.some(r=>r.phase==='recover'&&r.y>viewTopY()+40)};}''');ck('Razorwake departs, rolls and returns continuously',q,q['maxStep']<25 and len(q['jumps'])==1 and q['jumps'][0]['outside'] and q['returned'])
 for kind in ['tornado','front']:
  q=p.evaluate('''kind=>{B.enter=false;B.dead=false;B.y=B.ty;B._fb112.phase='recover';B._fb112.t=0;B._fb112.wait=999;B._fb112.hazards=[];player.dead=false;player.alive=true;player.invuln=0;DBGT.god=false;run.shield=0;player.x=worldWidth()/2;player.y=VH*.85;fb112Hazard(B,player.x,viewTopY()-45,kind);let reached=false;for(let i=0;i<180&&!player.dead;i++){fb112Tick(B,1/60);reached||=B._fb112.hazards.some(h=>h.y>player.y-45&&h.t<h.life-.35);}return{reached,dead:player.dead};}''',kind);ck(kind+' crosses the pilot zone and triggers native death',q,q['reached']and q['dead'])
 q=p.evaluate('''()=>{player.dead=false;player.alive=true;player.invuln=50;B._fb112.hazards=[];fb112Hazard(B,player.x,viewTopY()-45,'tornado');for(let i=0;i<180;i++)fb112Tick(B,1/60);return{survived:!player.dead,expired:B._fb112.hazards.length===0};}''');ck('Native evasion invulnerability survives a storm crossing',q,q['survived']and q['expired'])
 q=p.evaluate('''()=>{B._fb112.phase='recover';B._fb112.t=0;B.x=worldWidth()/2;B.y=B.ty;const p=B._fb112.parts[0],at=fb112PartPoint(B,p),n=WC1031.events.length,old=_dmgBullet;_dmgBullet={kind:'mg',x:at.x,y:at.y};try{fb112Damage(B,1,at.x,at.y,p);}finally{_dmgBullet=old;}return{events:WC1031.events.length-n,partContact:pImpacts.some(f=>f._weaponContact&&f.target===p),flash:p.flash};}''');ck('Actual part receives ballistic contact decal and hit flash',q,q['events']==1 and q['partContact']and q['flash']>0)
 ck('No page errors',errors,not errors);b.close()
(O/'contact-checks.json').write_text(json.dumps(checks,indent=2));sys.exit(0 if all(r['passed']for r in checks)else 1)
