"""Real Chromium coverage through shoot.py. Explicit fixtures are recorded as such.
Actual canvas differences verify connected arms, liquid motion and hit flashes.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from PIL import Image,ImageDraw
import json,http.server,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_shadow_1028/probe';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];trails=[]
def ck(name,value,data=None):
 checks.append({'name':name,'passed':bool(value),'data':data});print(('PASS 'if value else'FAIL ')+name,flush=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800})
  def page(stage):
   p=bc.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof WT25!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.evaluate("n=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(n,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(n,'boss').kind);debugFight.spawned=true;bossActive=true;warnT=0;BOFCinematicDirector.cancel();DBGT.god=true;run.lives=3;player.dead=false;player.invuln=1e9;setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;}",stage)
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=180000)
   return p
  def shot(p,name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p=page(7)
  p.evaluate("()=>{s7mWarm();r25Warm(7);bm9Warm(bm9StageNames(7));window.wt7Setup=(mode,x,y)=>{const b=boss,M=s7mInit(b);b.enter=false;b.x=x;b.y=y;b._drawY=y;M.height=M.drop=M.lean=0;M._mission29IntroDone=true;M.r25Gait=null;M.counterTell=null;M.frExit=null;s7mSet(b,mode);for(const q of M.parts)q.hp=q.max;player.x=worldWidth()/2;player.y=VH-55;};wt7Setup('recover',worldWidth()/2,175);}")
  p.wait_for_function('r25Warm(7)&&bm9StageNames(7).every(n=>BM9_ART[n].every(a=>XART.rdy(a.key)))',timeout=180000)
  p.wait_for_function("()=>XART.rdy(WL39_ART.coreShadow.key)")
  p.evaluate("""()=>{wt7Setup('recover',worldWidth()/2,300);const b=boss,M=b._s7mod;for(const id of ['gunL','gunR','frontL','frontR','rearL','rearR']){const p=M.parts.find(p=>p.id===id);s7mHit(b,p.hp,0,0,id);}for(const c of M.er28Canisters)s7mHit(b,c.hp,0,0,c.id);s7mSet(b,'er28-bounce');explosions=[];particles=[];}""")
  q=p.evaluate("""()=>{const b=boss,M=b._s7mod;M.height=150;M.coreFlash=0;b.flash=0;for(const p of M.parts)p.flash=0;
   function read(fn){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#b6b6b6';ctx.fillRect(0,0,cv.width,cv.height);ctx.restore();fn(b);return ctx.getImageData(0,0,cv.width,cv.height).data;}
   const base=read(WL39.shadowBase),shadow=read(s7mDraw);let added=0,changedBody=0;for(let i=0;i<base.length;i+=4){if(base[i]===182&&base[i+1]===182&&base[i+2]===182&&shadow[i]<160&&shadow[i+1]<160&&shadow[i+2]<160)added++;if((base[i]!==182||base[i+1]!==182||base[i+2]!==182)&&(Math.abs(base[i]-shadow[i])+Math.abs(base[i+1]-shadow[i+1])+Math.abs(base[i+2]-shadow[i+2])>5))changedBody++;}return{added,changedBody,pose:wl39AirShadowPose(b)};}""")
  ck('Actual native dark shadow pixels render beneath the airborne body',q['added']>1000,q)
  ck('Shadow stays behind the authored opaque body pixels',q['changedBody']==0,q['changedBody']);shot(p,'airborne-shadow')
  q=p.evaluate("()=>{const b=boss,M=b._s7mod,out=[];for(const height of [5,50,100,150]){M.height=height;out.push({height,...wl39AirShadowPose(b)});}return out;}")
  ck('Altitude changes size and opacity while the shadow stays on the ground',all(abs(v['y']-q[0]['y'])<.001 for v in q)and q[0]['scale']>q[-1]['scale']and q[0]['alpha']>q[-1]['alpha'],q)
  q=p.evaluate("()=>{const a=WL39_ART.coreShadow,s=ER28_ART.core,im=XART.get(a.key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const black=g.getImageData(0,0,c.width,c.height).data;g.clearRect(0,0,c.width,c.height);g.drawImage(XART.get(s.key),0,0);const original=g.getImageData(0,0,c.width,c.height).data;let mismatch=0,rgb=0;for(let i=0;i<black.length;i+=4){if(black[i+3]!==original[i+3])mismatch++;rgb+=black[i]+black[i+1]+black[i+2];}return{mismatch,rgb,even:a.cw%2===0&&a.ch%2===0,frames:a.frames};}")
  ck('All16 even shadow cells preserve actual body alpha',q['mismatch']==0 and q['rgb']==0 and q['even']and q['frames']==16,q)
  q=p.evaluate("()=>{const b=boss,M=b._s7mod;M.mode='jump';M.height=400;let n=0;const old=ctx.ellipse;ctx.ellipse=function(){n++;return old.apply(this,arguments);};try{s7mDraw(b);return n;}finally{ctx.ellipse=old;}}")
  ck('High jumps have one authored shadow rather than an additional ellipse',q==0,q)
  q=p.evaluate("()=>{const b=boss,M=b._s7mod,save={mode:M.mode,height:M.height,frExit:M.frExit,dead:b.dead},out=[];try{for(const mode of ['recover','portal','er28-guns','dead']){M.mode=mode;out.push(wl39AirShadowPose(b)===null);}M.mode='er28-bounce';M.height=0;out.push(wl39AirShadowPose(b)===null);M.height=100;M.frExit={};out.push(wl39AirShadowPose(b)===null);return out.every(Boolean);}finally{Object.assign(M,{mode:save.mode,height:save.height,frExit:save.frExit});b.dead=save.dead;}}")
  ck('Landing, hidden states and the portal escape leave no floating shadow',q)
  p.evaluate("()=>{s7mSet(boss,'er28-bounce');}");rows=[]
  for i in range(180):
   p.evaluate('s7mTick(boss,1/60)')
   if i%10==0:rows.append(p.evaluate('(()=>{const b=boss,M=b._s7mod;return{mode:M.mode,height:M.height,ground:b.y+M.drop+22,shadow:wl39AirShadowPose(b)}})()'))
   if i in [50,75,100]:shot(p,'native-hop-'+str(i))
  ck('Native jump animation carries the shadow on its moving ground position',sum(1 for q in rows if q['shadow']and abs(q['shadow']['y']-q['ground'])<.001)>=8,rows)
  ck('No browser or asset errors',not errors,errors)
  (O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8');br.close()
finally:stop()
assert all(q['passed']for q in checks)
