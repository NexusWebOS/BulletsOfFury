from pathlib import Path
import sys,json,hashlib,base64,io
from PIL import Image
import numpy as np
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W.parents[1]/'outputs/Draconus-rotor-and-full-stages';V=O/'gun-verification';V.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP
from barrage_review_common_1025 import boot
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8');errors=[];checks=[]
def ck(name,v,data=None):
 checks.append(dict(name=name,passed=bool(v),data=data));print(('PASS 'if v else'FAIL ')+name,''if v else str(data)[:500],flush=True);(V/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2))
def shot(p,name):p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(V/(name+'.png')))
source=[np.array(Image.open(W/'references'/f'rotor-{k:02}.png'))for k in range(36)]
ck('36 genuinely distinct canonical rotor phases',len({hashlib.sha256(a.tobytes()).hexdigest()for a in source})==36)
ck('Fixed receiver and collars do not rotate or change length',all(np.array_equal(a[:84],source[0][:84])for a in source))
for part in ['body','gun','grip','pickup']:
 base=np.array(Image.open(W/'exports'/(part+'_regular.webp')))
 ck(part+' material variants preserve alpha',all(np.array_equal(np.array(Image.open(W/'exports'/(part+'_'+mat+'.webp')))[:,:,3],base[:,:,3])for mat in ['chrome','red','hit']))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);context=br.new_context(viewport={'width':1280,'height':800});p=boot(context,port,8,errors,'boss');p.wait_for_function('()=>{stageLoadTick();if(stageLoadReady(8))updatePlay(0);return stageLoadReady(8)&&!bp119Pending()&&dgm1111Warm()}',timeout=180000)
  capabilities=p.evaluate("()=>({types:Object.fromEntries(['video/mp4;codecs=avc1.42E01E,mp4a.40.2','video/mp4','video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus'].map(t=>[t,MediaRecorder.isTypeSupported(t)])),audio:Object.keys(Snd).filter(k=>/gain|master|mix|ctx/i.test(k))})");(W/'capture-capabilities.json').write_text(json.dumps(capabilities,indent=2))
  p.evaluate("""()=>{window.B=boss;v18Enter(B,2,8);BOFCinematicDirector.cancel();B._r30.mode='fight';B.enter=B._noHit=B.dead=false;window.Q=hb20State(B);window.seedDG=(chrome=false)=>{Q.action=null;Q.rf1110=null;Q.rage=false;Q.chrome=chrome;Q.cool=999;Q.gunHP=900;Q.parts[2].hp=900;Q.parts[2].destroyed=true;Q.parts.forEach(p=>p.flash=0);Q.pendingRecall=Q.pendingGun=Q.pendingArsenal=false;Q.sf1111={acquired:false,held:false,broken:false};B.hp=B.maxhp;B.flash=0;B._noHit=B.enter=B.dead=false;B._r30.mode='fight';B._r30.v18.donorAge=0;B.x=worldWidth()/2;B.y=viewTopY()+190;eBullets=[];SF1111.events=[];DGM1111.frames.clear();};seedDG();DBGT.god=true;const hold=Input.hold;Input.hold=function(...a){return a.includes('fire')?false:hold.apply(this,a)};}""")
  for chrome in [False,True]:
   q=p.evaluate("""c=>{seedDG(c);hb20Start(B,'arsenal');const A=Q.action,hp=B.hp;let early=0;for(let i=0;i<300&&Q.action===A;i++){v19NativeTick(B,1/60);if(eBullets.length)early++;}const out={type:Q.action?.type,whole:hb20Pose(B).a._dgm1111,early,hpSame:hp===B.hp,gunHP:Q.gunHP,events:SF1111.events};return out;}""",chrome)
   ck('Canonical gun box/catch then modular rev '+str(chrome),q['type']=='gun'and q['whole']and q['early']==0 and q['hpSame']and q['gunHP']==900,q)
   q=p.evaluate("""()=>{const A=Q.action;let phases=new Set(),volley=0,errors=0;for(let i=0;i<280&&Q.action===A;i++){const n=eBullets.length;v19NativeTick(B,1/60);const q=hb20Pose(B);if(q.a._dgm1111)phases.add(q.a.frame);if(eBullets.length>n){const m=rd74Point(B,q,'muzzle');volley++;for(const bullet of eBullets.slice(n))if(Math.hypot(bullet.x-m.x,bullet.y-m.y)>.01||enemyOrdnanceCanIntercept(bullet))errors++;}}return{phases:[...phases],volley,errors,modular:!!hb20Pose(B).a._dgm1111,speed:Q.sf1111.rotor.speed};}""")
   ck('Independent barrel visits all36 phases '+str(chrome),len(q['phases'])==36,q)
   ck('Native volleys and warning use actual modular muzzle '+str(chrome),q['volley']>12 and q['errors']==0,q)
   shot(p,'modular-'+('chrome'if chrome else'normal'))
   q=p.evaluate("""()=>{Q.action.t=5;Q.sf1111.rotor.speed=4.7;const speed=Q.sf1111.rotor.speed;for(let i=0;i<32;i++)v19NativeTick(B,1/60);return{speed:Q.sf1111.rotor.speed,was:speed,bank:hb20Pose(B).a.bank};}""")
   ck('Rotor coasts before authored stow '+str(chrome),q['speed']<.15 and q['was']>4 and q['bank']=='draconus-gun-stow',q)
  q=p.evaluate("""()=>{seedDG(true);Q.sf1111.acquired=Q.sf1111.held=true;hb20Start(B,'gun');Q.action.t=2;Q.parts[2].destroyed=false;const q=hb20Pose(B),rig=v19HammerRig(B),g=rig.find(v=>v.p.id==='chaingun'),point={x:B.x-4,y:B.y+100};const hit=v19AtRect(g,point.x,point.y),hp=B.hp;B._lastPart=Q.parts[2];GP4.clock+=1;modularHit(19);const old=ctx.drawImage,keys=[];ctx.drawImage=function(im,...a){keys.push(HA21.tags.get(im));return old.call(this,im,...a)};try{rd74Blit(q,B.x,B.y,false)}finally{ctx.drawImage=old;}return{hit,hpSame:hp===B.hp,gunHP:Q.gunHP,keys,parts:rig.map(v=>v.p.id)};}""")
  ck('Actual visible gun mask has an independent native pool',q['hit']and q['hpSame']and q['gunHP']==881 and q['parts']==['core','chaingun'],q)
  ck('Gun-only hit uses white gun with intact colored body/grip','dgm1111_gun_hit'in q['keys']and'dgm1111_body_chrome'in q['keys']and'dgm1111_grip_chrome'in q['keys'],q)
  shot(p,'gun-only-white-hit')
  q=p.evaluate("""()=>{for(let i=0;i<16;i++)updateBoss(1/60);return{expired:Q.parts[2].flash<=0,held:sf1111Held(Q)};}""");ck('Independent gun flash expires',q['expired']and q['held'],q)
  q=p.evaluate("""()=>{const hp=B.hp,n=eBullets.length;B._lastPart=Q.parts[2];GP4.clock+=1;modularHit(Q.gunHP+1);const broke=Q.action.type;for(let i=0;i<70;i++)v19NativeTick(B,1/60);const after=Q.action?.type;hb20Start(B,'gun');return{broke,after,again:Q.action.type,hpSame:hp===B.hp,newRounds:eBullets.length-n,target:v19HammerRig(B).some(v=>v.p.id==='chaingun')};}""")
  ck('Broken modular gun cannot fire/target/respawn; hammer recovers',q['broke']=='sf1111_break'and q['after']=='recall'and q['again']=='side'and q['hpSame']and q['newRounds']==0 and not q['target'],q)
  q=p.evaluate("""()=>{seedDG(false);Q.sf1111.acquired=Q.sf1111.held=true;Q.gunHP=321;hb20Start(B,'armor');const A=Q.action;let phases=new Set();for(let i=0;i<280&&Q.action===A;i++){v19NativeTick(B,1/60);phases.add(hb20Pose(B).a.material);v19HammerRig(B);}v19HammerRig(B);Q.cool=0;hb20Start(B);return{gunHP:Q.gunHP,chrome:Q.chrome,held:sf1111Held(Q),type:Q.action.type,mats:[...phases]};}""")
  ck('Held module survives full Chromium activation and idle handoff',q['gunHP']==321 and q['chrome']and q['held']and q['type']=='gun'and len(q['mats'])>=8,q)
  sys.path.insert(0,str(W.parent/'three_way_hammer_1111'));import verify_three_way as h;h.O=O;(O/'verification-stage8').mkdir(exist_ok=True);h.run_three_way(p,8,ck,shot)
  # Visual native36-phase loop, with a stationary whole body and real gun layer.
  p.evaluate("seedDG(false);Q.sf1111.acquired=Q.sf1111.held=true;hb20Start(B,'gun');Q.action.t=2");images=[]
  for k in range(36):
   p.evaluate('k=>{dgm1111Rotor(Q).angle=k/36*TAU;drawWorld(0);SC12.refresh();__bofFit()}',k);images.append(Image.open(io.BytesIO(p.screenshot())).crop((265,0,1015,800)).resize((480,512),Image.Resampling.NEAREST).convert('RGB'))
  images[0].save(O/'draconus-modular-rotor.gif',save_all=True,append_images=images[1:],duration=35,loop=0,optimize=False)
  p.evaluate('v18Clear(B)');ck('Exit retires rotor state through native cleanup',p.evaluate('!Q.sf1111'))
  ck('No native renderer exceptions',not errors,errors);br.close()
finally:stop()
(V/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,runtimeHash=hashlib.sha256((R/'assets/draconus_modular_1111.js').read_bytes()).hexdigest()),indent=2));assert not errors and all(c['passed']for c in checks)
print('Finished',len(checks),'focused modular-gun checks.',flush=True)
