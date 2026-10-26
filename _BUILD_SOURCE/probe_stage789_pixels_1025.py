"""Additional native pixel/transform coverage for new masks and Stage9 hit plates."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
import json,base64

R=Path(__file__).resolve().parents[1];O=R/'_shots/stage78_review_1025/pixels';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));print(('PASS 'if v else'FAIL ')+n,flush=True)
 if not v:print(json.dumps(d),flush=True)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  def bind():
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
  def shot(n):p.evaluate('drawWorld(0)');p.screenshot(path=str(O/(n+'.png')))
  bind();p.evaluate("()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(7,'boss'),{pilot:'cole'});spawnBoss('sludgeemperor');debugFight.spawned=true;bossActive=true;s7mInit(boss);s7mSet(boss,'recover');r25Warm(7);DBGT.god=true;}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&r25Warm(7)}',timeout=180000)
  q=p.evaluate("""()=>{const b=boss,M=b._s7mod;M.mode='chase';M.r25Walk=true;const out=[];for(let f=0;f<8;f++){const G=r25Gait(b);G.distance=f/8*72+.1;G.speed=60;G.feet={};for(const z of s7mPose(b).filter(q=>q.r25)){const at=s7mWorld(b,z.target),id=s7mAt(b,at.x,at.y);out.push({part:z.id,frame:z.frame,id});}}return out;}""")
  ck('All 32 animated leg targets overlap native authored alpha',len(q)==32 and all(x['part']==x['id']for x in q),q)
  q=p.evaluate("""()=>{const b=boss,M=b._s7mod;M.mode='chase';let transparent=0;for(const z of s7mPose(b).filter(q=>q.r25)){const im=XART.get(z.cell),c=document.createElement('canvas');c.width=c.height=256;c.getContext('2d').drawImage(im,0,0);const d=c.getContext('2d').getImageData(0,0,256,256).data;for(const local of [[20,128],[235,128]]){if(d[(local[1]*256+local[0])*4+3]>0)continue;const dx=(local[0]-128)*z.w/256,dy=(local[1]-128)*z.h/256,at=s7mWorld(b,{x:z.x+dx*Math.cos(z.a)-dy*Math.sin(z.a),y:z.y+dx*Math.sin(z.a)+dy*Math.cos(z.a)});if(s7mAt(b,at.x,at.y)!==z.id)transparent++;}}return transparent;}""")
  ck('Transparent walking-cell padding is not an invisible leg hitbox',q>=6,q)
  p.close();p=br.new_page(viewport={'width':1280,'height':800});bind()
  p.evaluate("()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(8,'boss'),{pilot:'cole'});spawnBoss('vileexistence');debugFight.spawned=true;bossActive=true;v18Warm();bi24Warm();r25Warm(8);}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()&&bi24Warm()&&r25Warm(8)}',timeout=180000)
  p.evaluate("()=>{window.fresh78=()=>{const b=boss;b.parts=[];v18Budget(b);j3State(b).ph21=null;v18Enter(b,0,0);b._r30.v18.arenaPhase=0;b._r30.v18.bi24Rolled=false;v18Fight(b);b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=viewTopY()+220;BOFCinematicDirector.cancel();DBGT.god=true;player.invuln=1e9;enemies.length=0;eBullets.length=0;S78.debris=[];};fresh78();}")
  q=p.evaluate("""()=>{const b=boss;drawWorld(0);const before=ctx.getImageData(0,0,cv.width,cv.height).data,p=b.parts.find(p=>p.id==='left');b._lastPart=p;modularHit(1);drawWorld(0);const after=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<after.length;i+=4)if(after[i]>240&&after[i+1]>240&&after[i+2]>240&&before[i]+before[i+1]+before[i+2]<650)white++;return{white,timer:p.flash,hp:p.hp};}""")
  ck('Native first-host arm damage visibly flashes its actual pixels',q['white']>200 and q['timer']>0,q);shot('host-arm-hit');p.evaluate(STEP,24)
  ck('First-host native part flash expires',p.evaluate("boss.parts.find(p=>p.id==='left').flash<=0"));shot('host-arm-restored')
  q=p.evaluate("""()=>{fresh78();const b=boss,total=b.hp,core=b.parts[0].hp;for(const id of ['left','right']){const p=b.parts.find(p=>p.id===id);b._lastPart=p;modularHit(p.hp);}const alive=b.hp,mode=b._r30.mode;b._lastPart=b.parts[0];modularHit(core+1);const after=b._r30.mode;modularHit(99999);return{total,core,alive,mode,after,hp:b.hp,falls:S78.events.filter(q=>q.type==='authored-shatter').length};}""")
  ck('Both arm pools leave the protected core and one native rebirth',q['alive']==q['core']and q['mode']=='fight'and q['after']=='dr5er23rebirth'and q['hp']==0,q)
  q=p.evaluate("""()=>{const out=[];for(const form of [0,8,1,6,2]){const b=boss;b.parts=[];v18Budget(b);j3State(b).ph21=null;v18Enter(b,2,form);b._r30.v18.arenaPhase=2;v18Fight(b);b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=220;drawWorld(0);out.push({form,hp:b.hp,max:b.maxhp,model:v18Model(b),targets:retinaBossTargets(b).length});}return out;}""")
  ck('Final main and exactly four approved copies retain native health and rendering',len(q)==5 and all(x['hp']>0 and x['hp']==x['max']for x in q),q)
  shot('volcano-native')
  p.close();p=br.new_page(viewport={'width':1280,'height':800});bind()
  p.evaluate("()=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(9,'boss'),{pilot:'cole'});spawnBoss(debugFight.kind);debugFight.spawned=true;bossActive=true;stageLoadBegin(9);}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&XART.rdy("ns9_warpsen_intact")}',timeout=180000)
  q=p.evaluate("""()=>{const b=boss,F=b._s9fusion;F.phase='fuse';F.t=.7;F.left.x=worldWidth()/2-105;F.right.x=worldWidth()/2+105;F.left.y=F.right.y=190;F.left.flash=.1;F.right.flash=.1;F.left.spin=.16;F.right.spin=-.16;const calls=[],draw=ctx.drawImage;ctx.drawImage=function(...args){const m=ctx.getTransform();calls.push({m:[m.a,m.b,m.c,m.d,m.e,m.f],rect:args.slice(1),alpha:ctx.globalAlpha});return draw.apply(this,args)};try{s9FusionBossDraw(b);}finally{ctx.drawImage=draw;}return{calls,hidden:bossHealthVisible(b),scale:Math.pow(1-F.t/1.85,1.3),hp:F.left.hp};}""")
  # Native draw calls use the real game context; the screenshot below proves rendered hulls.
  pairs=[(a,b)for a,b in zip(q['calls'],q['calls'][1:])if len(a['rect'])==4 and len(b['rect'])==4 and a['alpha']>b['alpha'] and a['m']==b['m'] and a['rect']==b['rect']]
  ck('Twin blue hit overlays share actual rotated/scaled native draw transforms',len(pairs)>=2,{'pairs':len(pairs),'scale':q['scale']})
  ck('Stage9 mystery health and native twin HP remain unchanged',not q['hidden']and q['hp']>0,q['hp']);shot('twins-rotated-hit')
  p.evaluate('boss._s9fusion.phase="twins";boss._s9fusion.left.flash=.1;boss._s9fusion.right.flash=.1;drawWorld(0)');shot('twins-hit')
  ck('No page or console errors',not errors,errors);br.close()
finally:stop();(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8')
print(json.dumps(dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks))))
raise SystemExit(0 if all(c['passed']for c in checks)else 1)
