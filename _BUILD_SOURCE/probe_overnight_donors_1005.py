"""Native donor/controller and bomber pixel proof for the final deployed layer."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_1005'
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
port,stop=sh.serve(str(R));errors=[];out=json.loads((O/'donors.json').read_text()) if '--extras' in sys.argv else {'checks':[],'donors':[]}
if '--extras' in sys.argv:out['checks']=out['checks'][:16]
def ck(v,n):out['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def shot(p,n):
 (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return cv.toDataURL().split(",")[1];}')))
def frames(p,n):
 for i in range(0,n,20):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(20,n-i));p.wait_for_timeout(8)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:800]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{r30Warm();cf1004Warm();}')
  p.wait_for_function('()=>ON5_ART.knight.every(a=>XART.rdy(a.key))&&Object.values(FMC_ART).every(a=>XART.rdy(a.key))',timeout=120000,polling=50)
  for i in ([] if '--extras' in sys.argv else range(8)):
   p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'cole','diff':'furious'})
   p.evaluate('(i)=>{j3Encounter(B,2);j3Mimic(B,i);B._r30.mode="fight";B.enter=false;B._noHit=false;window.J=j3State(B);window.S=B._r30;window.seenStates=new Set();window.nShots=0;window.oldShot=eShootT;eShootT=function(){const q=oldShot.apply(this,arguments);if(q&&!q.dead)nShots++;return q;};}',i)
   for k in range(40):
    frames(p,30)
    p.evaluate('()=>{const D=J.gp4Donors?.[J.mimic];seenStates.add(D?gd4State(D):S.attack?.type||S.mode);}')
    if k==18:shot(p,'donor-'+str(i))
   value=p.evaluate('()=>{eShootT=oldShot;return{mimic:J.mimic,source:J.mimic==null?null:GD4_KIND[J.mimic]||"mutated drone",states:[...seenStates],shots:nShots,max:B.maxhp,hp:B.hp,finite:Number.isFinite(B.x)&&Number.isFinite(B.y)&&Number.isFinite(B.hp),donor:!!J.gp4Donors?.[J.mimic],dead:B.dead};}')
   value['requested']=i;out['donors'].append(value)
   ck(value['finite'] and not value.get('dead',False) and (i==0 or value['donor']),'copy '+str(i)+' runs its real donor without invalid state')
   ck(len(value['states'])>=2,'copy '+str(i)+' progresses through attacks and recovery')
  p.evaluate(SETUP,{'stage':6,'pilot':'cole','diff':'furious'})
  p.evaluate('()=>{subBossDone=subBossTriggered=true;fb2Warm();window.red=fb2FlightSpawn({direction:"east",role:"red",y:190});window.green=fb2FlightSpawn({direction:"west",role:"green",y:190});red.x=player.x-120;green.x=player.x+120;}')
  p.wait_for_function('()=>XART.rdy("fb2_stealth_red")&&XART.rdy("fb2_stealth_green")',timeout=120000,polling=50)
  shot(p,'approved-palette-bombers')
  ck(p.evaluate('()=>red.hp===6&&green.hp===6&&red._on5Bomber==="red"&&green._on5Bomber==="green"'),'both storm bomber paths use true stealth palettes and six-HP arcade durability')
  p.evaluate('()=>{hitEnemy(red,2);window.damaged=red.hp;drawEnemy(red);}')
  ck(p.evaluate('()=>red.hp===damaged&&red.hp<6'),'rendering a wounded bomber never heals it')
  p.evaluate('()=>{red.flash=.15;green.flash=.15;}');shot(p,'palette-bombers-white-hit')
  # These are the real old showcase rows. Decorative weapons remain harmless.
  p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','pilot':'cole','diff':'furious'})
  p.evaluate('()=>{window.R=B._rebels;rf28Init(B,R);window.I={rows:[{who:"VOSS",demo:"turbo",text:"Fast!"}],i:0,t:0};window.positions=[];for(let k=0;k<180;k++){I.t=k/60+2;rs1004DemoTick(R,I,1/60);positions.push(R.ships.find(q=>q.key==="voss").x);} }')
  out['turbo']=p.evaluate('()=>({positions,view:viewW(),camera:camLeftX(),demo:I.showcase.current.kind})')
  ck(p.evaluate('()=>positions.slice(35).every((x,i)=>{const prev=positions[i+34],visible=x>=camLeftX()-45&&x<=camRightX()+45||prev>=camLeftX()-45&&prev<=camRightX()+45;return i===0||!visible||Math.abs(Math.abs(x-prev)-1250/60)<.1;})'),'Voss turbo demonstration keeps full speed through every visible pass')
  for code in ['HAMMER','HAMA']:
   p.evaluate('(code)=>{pwInput=code;submitPassword();pilotIndex=PILOTS.findIndex(p=>p.key==="cole");startRun(5);window.h=boss._hammer;window.d=boss._hammerTime;d.attack=4;ht27Attack(boss,d);}',code)
   ck(p.evaluate('()=>h.state==="chain_warn"&&Number.isFinite(h.chainStartX)'),'musical '+code+' uses real Hammer machine-gun chain initialization')
   p.evaluate('()=>{d.attack=5;ht27Attack(boss,d);}')
   ck(p.evaluate('()=>h.spellTargets?.length>0&&h.state.startsWith("spell")'),'musical '+code+' uses real Hammer targeting spell')
   frames(p,110);shot(p,code.lower()+'-spell')
  ck(p.evaluate('()=>Snd.music.hama.src.endsWith("/HAMA_Instrumental.mp3")&&!hamaRecordedVocals1001()'),'live HAMA audio source is the retained instrumental')
  ck(not errors,'zero page and console errors');b.close()
finally:
 stop();out['errors']=errors;(O/'donors.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
sys.exit(0 if all(q['ok'] for q in out['checks']) and not errors else 1)
