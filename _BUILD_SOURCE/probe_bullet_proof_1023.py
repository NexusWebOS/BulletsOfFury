from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,argparse
R=Path(__file__).resolve().parents[1];W=R/'_shots/bullet_proof_1023';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args();checks=[];errors=[];port,stop=shoot.serve(str(R))
def ck(name,ok,data=None):checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'and'ERR_ABORTED'not in m.text else None);p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  p.evaluate('''()=>{window.BP23={reset:()=>{boss=subBoss=null;bossActive=subBossActive=false;enemies=[];pBullets=[];eBullets=[];rollers=[];shards=[];special=thunderStorm=null;groundTargetingReset();player.invuln=40002;player.x=worldWidth()/2;player.y=VH-50;camX=player.x-viewW()/2;},fire:(weapon,q)=>{pBullets=[{kind:weapon,x:q.x,y:q.y,w:60,h:60,vx:0,vy:0,dmg:99,t:0,life:2,top:PLAY.y,bot:VH,pierce:true,_hit:[],_ht:1,r:30}];updatePlay(1/60);return{dead:!!q.dead,alive:eBullets.includes(q),intercept:enemyOrdnanceCanIntercept(q),proof:q._weaponProof,shootable:q._shootable};}};}''')
  for diff in ['easy','normal','hard','furious']:
   p.evaluate('d=>EA11.setup(1,d)',diff);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1);}')
   for kind in ['s1bullet','mg','bolt','s2needle','s2slug','s3shard','s4brass','s4rail','s6tracer','s7shard','s9needle']:
    for weapon in ['mg','beam','gmiss','iceorb','flame']:
     row=p.evaluate('''o=>{BP23.reset();const q=eShootT(player.x,VH-160,Math.PI/2,0,o.kind,{w:12,h:12,silent:true,noMuzzle:true});q._shootable=true;q.hp=1;q._weaponProof=false;return BP23.fire(o.weapon,q);}''',{'kind':kind,'weapon':weapon});ck(diff+' '+kind+' survives '+weapon,row['alive']and not row['dead']and not row['intercept'],row)
   for kind in ['s1bullet','mg','s4brass','emissile','s1jungleMissile']:
    for attack in ['chromium','roller']:
     row=p.evaluate('''o=>{BP23.reset();const q=eShootT(player.x,VH-160,Math.PI/2,0,o.kind,{silent:true,noMuzzle:true});if(o.attack==='chromium')chromeMirror(q.x,q.y,90,1);else{releaseRoller(1);const b=rollers.at(-1);b.x=q.x;b.y=q.y;b.vx=b.vy=0;updateRollers(1/60);}return{dead:!!q.dead,intercept:enemyOrdnanceCanIntercept(q)};}''',{'kind':kind,'attack':attack});expect=kind in ['emissile','s1jungleMissile'];ck(diff+' fresh '+kind+' '+('is intercepted by 'if expect else'survives ')+attack,row['dead']==expect,row)
   for kind in ['emissile','s1jungleMissile','s2rocket','s4missile','s5missile']:
    row=p.evaluate('''kind=>{BP23.reset();const q=eShootT(player.x,VH-160,Math.PI/2,0,kind,{silent:true,noMuzzle:true});q.hp=1;q._shootable=true;q._weaponProof=false;return BP23.fire('mg',q);}''',kind);ck(diff+' physical '+kind+' remains shootable',row['dead']and row['intercept'],row)
   row=p.evaluate('''()=>{BP23.reset();const q=eShootT(player.x,VH-160,Math.PI/2,0,'fireorb',{silent:true,noMuzzle:true});q._er26Art='fire';q.hp=1;return BP23.fire('mg',q);}''');ck(diff+' dedicated fireball mechanic retained',row['dead']and row['intercept'],row)
  # Reproduce the actual current campaign family metadata, not an invented roster.
  families=json.loads((R/'_BUILD_SOURCE/bullet_interception_1023/emissions.json').read_text())['families'];familyRows=p.evaluate('''rows=>rows.map(r=>{const q=Object.fromEntries(r.flags);return{stage:r.stage,actor:r.actor,kind:r.kind,element:enemyOrdnanceElement(q),intercept:enemyOrdnanceCanIntercept(q),ordinary:!enemyOrdnanceElement(q)&&!/missile|rocket|warhead/i.test(q.kind||''),flags:r.flags};})''',families)
  ck('All 117 recorded campaign projectile variants keep non-ordnance unshootable',len(familyRows)==117 and all(not r['intercept']for r in familyRows if r['ordinary']),{'families':len(familyRows),'ordinary':sum(r['ordinary']for r in familyRows)})
  # Real boat controller: snapshot the actual spread before player shots cross it.
  specs=json.loads((R/'_BUILD_SOURCE/bullet_interception_1023/catalog.json').read_text())['stages'][0]['specs']
  p.evaluate('EA11.setup(1,"normal")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1);}')
  spec=next(s for s in specs if s['type']=='s1boatpatrol');p.evaluate('''s=>{EA11.case(s);bossWarned=false;E.hp=E.maxhp=10000;player.fireCd=9999;}''',spec)
  for i in range(120):
   p.evaluate('EA11.step(6)')
   if p.evaluate('eBullets.some(b=>b.kind==="s1bullet")'):break
  row=p.evaluate('''()=>{const shots=eBullets.filter(b=>b.kind==='s1bullet');window.BOAT23=shots;return{count:shots.length,ordinary:shots.every(b=>!enemyOrdnanceCanIntercept(b)),triples:shots.length>=3};}''');ck('Actual Stage1 patrol boat releases protected spread fire',row['triples']and row['ordinary'],row)
  p.evaluate('''()=>{enemies=[];pBullets=[];eBullets=BOAT23;for(const q of eBullets){q.vx=q.vy=0;pBullets.push({kind:'mg',x:q.x,y:q.y,vx:0,vy:0,w:30,h:30,dmg:9,t:0});}updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');ck('Actual boat spread survives crossing machine-gun fire',p.evaluate('BOAT23.length>=3&&BOAT23.every(q=>!q.dead&&eBullets.includes(q))'))
  (W/'boat-native.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')));br.close()
finally:stop()
ck('No native page or console errors',not errors,errors);out={'checks':checks,'passed':sum(r['passed']for r in checks),'failed':sum(not r['passed']for r in checks),'errors':errors};(W/('baseline.json'if args.baseline else'report.json')).write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k]for k in ['passed','failed','errors']}));sys.exit(bool(out['failed']))
