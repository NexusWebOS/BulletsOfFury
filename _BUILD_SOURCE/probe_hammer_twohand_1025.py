"""Native renderer and real component damage checks for Chronos commitment."""
from pathlib import Path
import ast,json,base64
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
R=Path(__file__).resolve().parents[1];O=R/'_shots/hammer_twohand_1025';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 if not ok:print(json.dumps(data),flush=True)
src=ast.parse((R/'_BUILD_SOURCE/audit_chronos_aura_gun_1025.py').read_text(encoding='utf8'))
seed=next(n.args[0].value for n in ast.walk(src) if isinstance(n,ast.Call) and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str) and 'window.seedGun=' in n.args[0].value)
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:5,role:'boss',kind:'chromehammer'},{pilot:'cole'});spawnBoss('chromehammer');debugFight.spawned=true;warnT=0;bossActive=true;c32Warm();c30Warm();c29Warm();bi24Warm();ht23Warm();c25Warm();c26Warm();c27Warm();ch23Warm();}")
  p.wait_for_function('()=>{stageLoadTick();return [stageLoadReady(5),c32Warm(),c30Warm(),c29Warm(),bi24Warm(),ht23Warm(),ch23Warm(),c25Warm(),c26Warm(),c27Warm()].every(Boolean)}',timeout=180000);p.evaluate(seed)
  p.evaluate("()=>{window.fresh=()=>{seedGun();boss._hammer.c30=null;boss._hammer.c29Break=null;boss._hammer.c29GunTime=0;boss._hammer.c27RagePending=false;};window.armGun=()=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hb20PickupDone=h.hammerDestroyed=true;h.mode='chaingun';h.chainHP=h.chainMax=1000;h.chainDestroyed=false;hammerChainStart(boss);boss.x=340;boss.y=220;};}")
  def shot(name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  for mat in ['regular','chrome']:
   for bank in ['windup','strike','retract','takeoff','land','left','right']:
    q=p.evaluate("""q=>{const a=C27_ART.banks[q.bank+'_'+q.mat];return a.frames.every(f=>f.wholeAuthored&&f.gripHands===2&&f.sourceKey.startsWith('ha21_h22_'));}""",dict(bank=bank,mat=mat));ck(mat+' '+bank+' original two-handed frames',q)
   for bank in ['windup','strike','left','right']:
    p.evaluate("""q=>{fresh();const h=boss._hammer;h.hb20Pickup=null;h.hammerDestroyed=false;h.frArmor.hp=q.mat==='chrome'?8415:0;h.frArmor.activated=q.mat==='chrome';boss.x=340;boss.y=260;window.twoPose=c27Pose(boss,q.bank,.65,1,q.mat);const old=ha21Blue;window.restorePose=()=>{ha21Blue=old};ha21Blue=()=>twoPose;}""",dict(bank=bank,mat=mat))
    shot(mat+'-'+bank);p.evaluate('restorePose()')
  q=p.evaluate("""()=>{fresh();boss._hammer.hb20Pickup=null;boss._hammer.hammerDestroyed=false;boss._hammer.state='giant_dive';boss._hammer.t=.4;const a=ha21Blue(boss);boss.flash=.12;drawWorld(0);return {source:a.a.sourceKey,hands:a.a.gripHands,flash:boss.flash};}""");ck('Native depth strike selects two-handed source with live hit flash',q['hands']==2 and q['flash']>0,q)
  ck('No browser errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
contact=Image.new('RGB',(1280,225*((len(shots)+3)//4)),'#101d2a');d=ImageDraw.Draw(contact)
for i,(f,title) in enumerate(shots):
 im=Image.open(f).resize((320,200));x=i%4*320;y=i//4*225;contact.paste(im,(x,y+25));d.text((x+4,y+4),title,fill='white')
contact.save(O/'contact.png')
print(json.dumps(dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks))));assert all(c['passed'] for c in checks)
