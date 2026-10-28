from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import ast,json,sys,base64,io,numpy as np
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);O=W/'rebel-native';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
SETUP=next(ast.literal_eval(n.value)for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SETUP'for t in n.targets))
RESET=next(ast.literal_eval(n.value)for n in ast.parse((R/'_BUILD_SOURCE/probe_rebel_air_1007.py').read_text()).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='RESET'for t in n.targets))
rows=[];errors=[];port,stop=shoot.serve(str(R))
def arr(s):return np.array(Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB')).astype(int)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  p.evaluate('''()=>{window.RQ23={warns:0,shots:0,keys:new Set(),before:combatWarningDraw,draw:()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.clearRect(0,0,VW,VH);AQ23.owner=Q;AQ23.keys=[];ctx.save();ctx.translate(-camX,0);fr27RebelDrawShip(Q);ctx.restore();AQ23.owner=null;for(const k of AQ23.keys)RQ23.keys.add(k);return cv.toDataURL().split(',')[1];}};combatWarningDraw=function(owner,q){RQ23.warns++;return RQ23.before.apply(this,arguments);};}''')
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','diff':diff,'pilot':'yuri'});p.evaluate('''()=>{R=B._rebels;rf28Init(B,R);R.frIntro={done:true};G=rg4Init(B);G.scene=null;G.gang=true;G.rescueDone=true;G.rescueAt=Infinity;BOFCinematicDirector.cancel();H3.release=false;H3.ending=null;AP10_X.intro=null;P2M.active=null;story=fb2Talk=fb2Intro=thaw=s6Opening=s6Wing=null;rg4Warm();}''');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&XART.rdy(RA7.sheet);}')
   for key,kind in [('kaia','rockets'),('voss','turbo'),('jace','helix'),('nyx','cloak'),('rook','slug'),('rook','rookhook'),('jace','ram'),('voss','fusion')]:
    p.evaluate(RESET);p.evaluate('''o=>{G.rd21.fleet=null;G.rd21.next=Infinity;G.releaseAt=1e9;for(const q of R.ships){q.stun=9999;q.rg4.cd=q.rg4.gunCd=9999;q._rd21Scale=1;q._rd21Cloak=false;q._rd21Visible=9999;}Q=R.ships.find(q=>q.key===o.key);Q.stun=0;Q.x=player.x=worldWidth()/2;Q.y=170;player.y=VH-100;RQ23.warns=0;RQ23.keys.clear();AQ23.invalid=[];R.frHit=null;R.hit=Q.i;Q.flash=0;Q.t=0;}''',{'key':key});before=arr(p.evaluate('RQ23.draw()'));hp=p.evaluate('Q.hp');p.evaluate('rebelSquadDamage(B,.1)');after=arr(p.evaluate('RQ23.draw()'));bright=int(((before.max(2)>12)&(after.mean(2)-before.mean(2)>20)).sum())
    p.evaluate('''k=>{Q.flash=0;rg4Attack(Q,R,G,k);RQ23.start=Q.rg4.act?.kind;RQ23.phases=new Set();RQ23.seen=new WeakSet();RQ23.shots=0;RQ23.maxOrd=0;}''',kind)
    for t in range(20):
     p.evaluate('''()=>{for(let i=0;i<36;i++){player.invuln=40002;player.fireCd=9999;pBullets=[];if(!Q.rg4.act)Q.stun=9999;updatePlay(1/60);const A=Q.rg4.act;if(A)RQ23.phases.add(A.phase);for(const b of eBullets)if(!RQ23.seen.has(b)){RQ23.seen.add(b);RQ23.shots++;}RQ23.maxOrd=Math.max(RQ23.maxOrd,G.ord.length);if(i%6===0)RQ23.draw();}}''')
    row=p.evaluate('''()=>({kind:RQ23.start,phases:[...RQ23.phases],complete:!Q.rg4.act,warnings:RQ23.warns,shots:RQ23.shots,ordnance:RQ23.maxOrd,keys:[...RQ23.keys],geometry:AQ23.invalid,finite:R.ships.every(q=>Number.isFinite(q.x+q.y)),flashExpired:Q.flash<=0,hitHp:Q.hp})''');row.update(difficulty=diff,pilot=key,requested=kind,brightPixels=bright,hpBefore=hp);row['passed']=bool(row['kind'])and row['complete']and len(row['phases'])>=2 and row['warnings']>0 and row['finite']and not row['geometry']and bright>10 and row['hitHp']<hp and row['flashExpired'];rows.append(row);(O/'report.json').write_text(json.dumps({'cases':rows,'errors':errors},indent=2));print(json.dumps({k:v for k,v in row.items()if k not in ['keys','geometry']}),flush=True)
    if diff=='normal':p.evaluate('''()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''');(O/f'{key}-{kind}.png').write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  br.close()
finally:stop();(O/'report.json').write_text(json.dumps({'cases':rows,'errors':errors},indent=2))
print(json.dumps({'cases':len(rows),'passed':sum(r['passed']for r in rows),'errors':errors}));sys.exit(bool(errors)or any(not r['passed']for r in rows))
