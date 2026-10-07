"""Native finale signature controls: actual rigs, damage, pause, and slow pilot."""
from pathlib import Path
import base64,json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/hardcorps_finale_patterns_1007';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
checks=[];errors=[];scenes=[]
def ck(v,n):checks.append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def frames(p,n,world=False):
 for i in range(0,n,15):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+('updatePlay(1/60);' if world else 'r30Tick(B,1/60);')+'}}',min(15,n-i));p.wait_for_timeout(2)
def snap(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
def setup(p,id,diff='normal'):
 p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','pilot':'yuri','diff':diff})
 p.evaluate('(id)=>{j3Encounter(B,id==="host"?0:id==="ghost"?1:2);if(!["host","ghost","home"].includes(id))j3Mimic(B,+id);on5FightStart(B);window.S=B._r30;window.J=j3State(B);window.D=J.mimic>0?gd4Create(B,J.mimic):null;S.attack=null;S.cd=1;S.returning=null;S.hkKnight=null;S.hkKnightCd=1.5;dr5State(B).introWanted=false;dr5State(B).introSeen=true;fb2Talk=null;BOFCinematicDirector.cancel();story=null;B.x=worldWidth()/2;B.y=205;B._drawY=B.y;if(D){D.p.x=B.x;D.p.y=B.y;}player.x=worldWidth()/2;player.y=VH-135;player.invuln=1e9;HF7.events=[];}',id)
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  for key,file in [('HC1007','hardcorps_bosses_1007'),('HF7','hardcorps_finale_patterns_1007')]:
   if not p.evaluate('k=>typeof globalThis[k]!=="undefined"',key):
    if not p.evaluate('()=>typeof '+key+'!=="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/{file}.js')
  p.evaluate('()=>{r30Warm();hc1007Warm();}');p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&XART.rdy("av3_laser_beams")',timeout=120000)
  for id in ['host','ghost','home','0','1','2','3','4','5','6','7']:
   for diff in ['normal','furious']:
    setup(p,id,diff);p.evaluate('()=>{window.before=J.hp.slice();window.K=hf7Start(B);window.hf7DonorClockBefore=D?.p.t;}')
    ck(p.evaluate('()=>!!K&&K.lines.length>0&&K.tell>=1.5'),f'{id} {diff}: live modules own a full committed signature')
    if not p.evaluate('()=>!!K'):continue
    frames(p,55);snap(p,id+'-'+diff+'-tell')
    p.evaluate('()=>{window.locked=[K.tx,K.ty];player.x+=80;}');frames(p,50);snap(p,id+'-'+diff+'-release')
    ck(p.evaluate('()=>K.tx===locked[0]&&K.ty===locked[1]&&(!D||D.p.t===hf7DonorClockBefore)&&!S.attack'),f'{id} {diff}: aim commits and donor clock/attack pauses')
    ck(p.evaluate('()=>r30Parts(B).every(v=>[v.x,v.y,v.w,v.h,v.rot].every(Number.isFinite)&&v.alpha===1)'),f'{id} {diff}: animated modular pieces remain finite and opaque')
    # Real controller collision, instrument only damage delivery for a positive control.
    p.evaluate('()=>{window.hits=0;window.saveHit=playerHit;playerHit=()=>hits++;K.t=K.tell+.72;hf7Tick(B,0);hits=0;const Q=hf7Sample(B),L=Q.lines[0];if(!L.physical){player.x=L.x+(L.ex-L.x)*.25;player.y=L.y+(L.ey-L.y)*.25;}else if(K.def.kind==="pass"){player.x=B.x;player.y=B.y;}else if(K.def.kind==="vault"){K.t=K.tell+K.active*.90;hf7Tick(B,0);const v=hf7Rig(B).find(v=>K.ports.some(p=>p.module===v.p.id));player.x=v.x;player.y=v.y+v.h*.35;}else{const v=r30Parts(B).find(v=>v.p.id===L.module);player.x=v.x-Math.sin(v.rot||0)*v.h*.35;player.y=v.y+Math.cos(v.rot||0)*v.h*.35;}hf7Tick(B,.00001);}')
    ck(p.evaluate('()=>hits>0'),f'{id} {diff}: contact with actual visible attack delivers damage')
    p.evaluate('()=>{hits=0;K.t=K.tell+K.active+.2;hf7Tick(B,0);playerHit=saveHit;}')
    ck(p.evaluate('()=>hits===0'),f'{id} {diff}: recovery removes damage while leaving modules drawn')
    if id in ['ghost','3','4','6']:
     p.evaluate('()=>{K.t=K.tell+1.55;window.hits=0;playerHit=()=>hits++;hf7Tick(B,0);playerHit=saveHit;}')
     ck(p.evaluate('()=>hf7Sample(B).phase==="tell"&&hits===0'),f'{id} {diff}: relay has a real damage-free crossing')
    p.evaluate('()=>{for(const q of B.parts)if(K.ports.some(v=>v.module===q.id)){q.destroyed=true;q.hp=0;}hf7Tick(B,.01);}')
    ck(p.evaluate('()=>!S.hf7.sig&&J.hp.length===9&&J.hp.every((v,i)=>v===before[i])'),f'{id} {diff}: destroyed emitters cancel and preserve all nine HP pools')
  # Natural selection through original controllers; no forced source mode or signature.
  for id in ['host','ghost','home','0','1','2','3','4','5','6','7']:
   setup(p,id,'furious')
   for n in range(15):
    frames(p,120)
    if p.evaluate('()=>HF7.events.some(q=>q.event==="signature")'):break
   q=p.evaluate('()=>({id:hf7Identity(B),mode:S.mode,signature:HF7.events.find(q=>q.event==="signature"),history:D?.history||[],donorState:D?gd4State(D):null})');scenes.append(q)
   ck(bool(q.get('signature')),f'{id}: signature naturally scheduled at source recovery')
  # Slow pilot uses real held input, without a roll or shield, to leave the locked host strike.
  setup(p,'host','furious');p.evaluate('()=>{run.pilot="juggernaut";const P=PILOTS.find(p=>p.key==="juggernaut");PILOTMOD={spd:P.spd||0,fire:P.fire||0,range:P.range||0,tint:P.tint};run.speed=0;run.speedLevel=0;run.shield=0;player.invuln=0;window.realHit=playerHit;window.contacts=0;playerHit=function(){contacts++;return realHit.apply(this,arguments);};window.K=hf7Start(B);window.startX=player.x;}')
  p.keyboard.down('ArrowRight');frames(p,100,True);p.keyboard.up('ArrowRight');snap(p,'slow-pilot-host-dodge')
  ck(p.evaluate('()=>Math.abs(player.x-startX)>90&&contacts===0&&!player.roll&&!player.somer'),'slow ship physically dodges the locked strike with ordinary held movement')
  p.evaluate('()=>playerHit=realHit')
  setup(p,'8','furious');frames(p,90);ck(p.evaluate('()=>hf7Identity(B)===null&&!S.hf7&&D.p.t>0'),'Hammer 8 remains wholly owned by native source controller')
  ck(not errors,'zero browser and renderer errors');br.close()
finally:
 stop();out={'checks':checks,'scenes':scenes,'errors':errors,'scope':'Native protected fixtures, positive collision controls, natural source recovery selection and one ordinary slow-ship dodge; not full campaign clears or human balance approval.'};(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');(R/'docs/qa/hardcorps_finale_patterns_1007.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':len(checks),'failures':[q['name'] for q in checks if not q['ok']],'errors':errors}))
if errors or any(not q['ok'] for q in checks):raise SystemExit(1)
