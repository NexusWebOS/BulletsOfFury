from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_ART_SOURCES/hammer_correction_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Hammer-Correction-1022';O=R/'_shots/hammer_correction_1022';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(n,ok,d=None):checks.append(dict(name=n,ok=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n+(' '+str(d) if not ok else ''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(content=(R/'_BUILD_SOURCE/balance_lab_1007.js').read_text(encoding='utf-8'))
  p.evaluate('()=>BAL7.setup({stage:8,kind:"vileexistence",pilot:"cole",diff:"normal",fire:false,seconds:60})');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}')
  p.evaluate('''()=>{BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;v18Enter(B,2,1);v18SetMode(B,'fight');B.enter=B.dead=B._noHit=false;B.x=worldWidth()/2;B.y=150;player.invuln=99999;player.y=VH-80;window.P=hc22Proxy(B).p;v18StartAttack(B);}''')
  row=p.evaluate('''()=>{const states=new Set(),positions=[];for(let i=0;i<1800;i++){efxClock+=1/60;v18AttackTick(B,1/60);states.add(P._ovState);if(i%60===0)positions.push({x:B.x,y:B.y});}return {states:[...states],positions,shots:eBullets.length,owned:eBullets.every(q=>q._v18Owner===B),native:P._ovInit,legacy:!!h21Action(B)};}''');ck('Corrupted helicopter executes original Overlord controller',row['native']==1 and not row['legacy'] and len(row['states'])>=3 and row['shots']>0 and row['owned'],row)
  for state in ['charge','missile','sweep']:
   row=p.evaluate('''kind=>{eBullets=[];hc22Proxy(B).age=0;P.hp=P.maxhp=B.maxhp;P._ovState='fight';P._chargeTell=null;P._ovVolley=P._ovSweep=P._ovRush=P._ovSonic=null;if(kind==='charge')ovStartChargeTell(P);else if(kind==='missile')ovStartMissileLock(P,'fight');else ovStartSweep(P);const before=P._ovState,states=new Set();for(let i=0;i<1800;i++){v18AttackTick(B,1/60);states.add(P._ovState);if(P._ovState==='fight')break;}return {before,states:[...states],shots:eBullets.length,owned:eBullets.every(q=>q._v18Owner===B)};}''',state);ck('Native '+state+' tells and completes on corrupted form',len(row['states'])>1 and row['owned'] and (row['shots']>0 if state!='charge' else True),row)
  p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');(O/'helicopter-native.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  ck('No native draw errors',not errors,errors);b.close()
finally:stop()
(W/'helicopter-native-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8');sys.exit(not all(x['ok'] for x in checks))
