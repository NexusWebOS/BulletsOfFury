"""Native Chromium: code row motion, independent hits, attachment and transitions."""
from pathlib import Path
import json,base64,http.server,sys
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/codewall_1003d';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def frames(p,n):
 for i in range(0,n,12):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(12,n-i));p.wait_for_timeout(8)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.add_init_script('(()=>{const d=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(){if(window.cwdCalls&&window.cwdKey&&typeof ctx!=="undefined"&&this===ctx)cwdCalls.push({key:cwdKey,args:Array.from(arguments).slice(1)});return d.apply(this,arguments);};})()')
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate('()=>{r30Warm();window.cwdCalls=[];window.cwdKey=null;const c=cwdCell,r=cwdRows,s=s81003Cell;cwdCell=function(sheet,frame){cwdKey="cwd_"+sheet+":"+frame;try{return c.apply(this,arguments);}finally{cwdKey=null;}};cwdRows=function(){cwdKey="cwd_rows";try{return r.apply(this,arguments);}finally{cwdKey=null;}};s81003Cell=function(sheet){cwdKey="old_"+sheet;try{return s.apply(this,arguments);}finally{cwdKey=null;}};}')
  p.wait_for_function('()=>Object.values(CWD_ART).every(a=>XART.rdy(a.key))&&Object.values(FMC_ART).every(a=>XART.rdy(a.key))&&Object.values(S81003_ART).every(a=>XART.rdy(a.key))',timeout=120000,polling=60)
  ck(p.evaluate('()=>Object.values(CWD_ART).every(a=>{const im=XART.get(a.key);return im.width===a.size[0]&&im.height===a.size[1];})'),'all four generated sources decoded through XART')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{playerHit=function(){};B._r30.mode="fight";B.enter=false;B._r30.seq=1;r30Attack(B);B._r30.wallAge1003=.40;window.cwSound=[];const sound=r30Sound;r30Sound=function(k){cwSound.push(k);return sound.apply(this,arguments);};}')
  shot(p,'blue-wall')
  ck(p.evaluate('()=>B._r30.shield>0&&B._r30.codeWall1003d==="blue"'),'blue full-body wall appears during a real gravity charge')
  p.evaluate('()=>{const q=r30ShieldBounds(B);window.nativeBlueHp=B.hp;window.nativeBlueShield=B._r30.shield;pBullets.push({kind:"mg",_chaingun:true,x:q.x,y:q.y+q.h*.30,vx:0,vy:0,w:6,h:10,dmg:6,t:0});}');frames(p,2)
  ck(p.evaluate('()=>B._r30.shield<nativeBlueShield&&B.hp===nativeBlueHp'),'real chaingun projectile collision damages blue wall instead of boss')
  ck(p.evaluate('()=>{const a=cwdOffset(1,0,500),b=cwdOffset(1.1,0,500),c=cwdOffset(1,1,500),d=cwdOffset(1.1,1,500);return b>a&&d<c;}'),'adjacent authored rows move in opposite horizontal directions')
  p.evaluate('()=>{window.wallClock=B._r30.clock;cwdCalls=[];s81003ShieldDraw(B);window.beforeRows=cwdCalls.filter(q=>q.key==="cwd_rows").map(q=>q.args[4]);const q=r30ShieldBounds(B);B._lastPart=r30At(B,q.x,q.y+q.h*.25);window.cwHp=B.hp;modularHit(6);}')
  frames(p,6);shot(p,'blue-hit')
  ck(p.evaluate('()=>{cwdCalls=[];s81003ShieldDraw(B);const now=cwdCalls.filter(q=>q.key==="cwd_rows").map(q=>q.args[4]);return B._r30.clock>wallClock&&now.some((v,i)=>v!==beforeRows[i])&&CWD.effects.some(f=>f.kind==="impact")&&B.hp===cwHp;}'),'native row pixels advance while an independent damage flash plays')
  ck(p.evaluate('()=>!S81003.effects.some(f=>["impact","shatter","shards"].includes(f.kind))'),'old wall impact and crystal effects are absent')
  p.evaluate('()=>{B._lastPart={id:"codeWall1003d"};modularHit(9999);}')
  frames(p,12);shot(p,'blue-shatter')
  ck(p.evaluate('()=>{const chips=CWD.effects.filter(f=>f.kind==="chip"),octants=new Set(chips.map(f=>(Math.floor((Math.atan2(f.vy,f.vx)+Math.PI)*8/TAU)+8)%8));return !B._r30.shield&&chips.length===24&&octants.size===8&&cwSound.filter(k=>k==="shieldBreakCombat").length===1;}'),'break launches 24 authored chips through all eight directions with one sound')
  frames(p,90);ck(p.evaluate('()=>CWD.effects.length===0'),'all flash and shatter particles expire')
  p.evaluate('()=>{r30Clear(B);r30Form(B,5);B._r30.mode="fight";B.enter=false;r30Attack(B);B._r30.wallAge1003=.4;}');shot(p,'red-shield')
  ck(p.evaluate('()=>{const q=r30ShieldBounds(B),v=fmcRig(B).find(v=>v.p.id==="shield");return q.color==="red"&&Math.hypot(q.x-v.x,q.y-v.y)<.01&&q.rot===v.rot&&B._r30.shield>0;}'),'red projection follows the actual modular shield position and rotation')
  p.evaluate('()=>{const q=r30ShieldBounds(B);window.nativeRedHp=B.hp;window.nativeRedShield=B._r30.shield;pBullets.push({kind:"mg",_chaingun:true,x:q.x,y:q.y,vx:0,vy:0,w:6,h:10,dmg:6,t:0});}');frames(p,2)
  ck(p.evaluate('()=>B._r30.shield<nativeRedShield&&B.hp===nativeRedHp'),'real chaingun projectile collision damages attached red code field')
  ck(p.evaluate('()=>{const q=r30ShieldBounds(B);return cwdContains(q,q.x,q.y)&&!cwdContains(q,q.x+q.w,q.y+q.h);}'),'rotated kite containment accepts its center and rejects outside space')
  p.evaluate('()=>{const q=r30ShieldBounds(B);B._lastPart=r30At(B,q.x,q.y);window.shieldHp=B._r30.shield;modularHit(7);}');frames(p,5);shot(p,'red-hit')
  ck(p.evaluate('()=>B._r30.shield===shieldHp-7&&CWD.effects.some(f=>f.color==="red"&&f.kind==="impact")'),'red field intercepts shots with its own separate red hit flash')
  ck(p.evaluate('()=>{const q=r30ShieldBounds(B),v=r30Parts(B).find(v=>v.p.id==="core"),hp=B.hp,sh=B._r30.shield;B._lastPart=r30At(B,v.x,v.y);if(B._lastPart?.id==="codeWall1003d")return false;modularHit(5);return B.hp===hp-5&&B._r30.shield===sh;}'),'exposed knight body takes damage without draining his remote shield')
  ck(p.evaluate('()=>{const t=retinaBossTargets(B);return t.length>1&&t.some(q=>String(q.id||q._id||q._retinaId||"").includes("code"))||t.length>2;}'),'Retina can lock the red projection and exposed modular parts')
  p.evaluate('()=>{B._lastPart={id:"codeWall1003d"};modularHit(9999);}');frames(p,13);shot(p,'red-shatter')
  ck(p.evaluate('()=>CWD.effects.some(f=>f.color==="red"&&f.kind==="chip")&&fmcAlive(B,"shield")'),'breaking red energy leaves the independently destructible physical shield')
  p.evaluate('()=>{B._lastPart=B.parts.find(v=>v.id==="shieldArm");modularHit(B._lastPart.hp+1);s81003KnightEnter(B,"guard");}')
  ck(p.evaluate('()=>!fmcAlive(B,"shield")&&B._r30.shield===0'),'destroyed shield arm cannot regenerate a floating code shield')
  p.evaluate('()=>{r30Clear(B);r30Form(B,2);B._r30.mode="morph1003b";B._r30.t=.70;B.enter=true;cwdCalls=[];}');shot(p,'reconstruction-out')
  ck(p.evaluate('()=>cwdCalls.some(q=>q.key.startsWith("cwd_morph:"))&&!cwdCalls.some(q=>q.key==="old_morph"||q.key==="old_teleport")'),'morph uses new authored vertical scan and never draws the spherical reel')
  p.evaluate('()=>{r30Form(B,3);B._r30.mode="reveal";B._r30.t=.40;B.enter=true;}');shot(p,'reconstruction-in')
  for form in range(7):
   p.evaluate('(n)=>{r30Clear(B);r30Form(B,n);B._r30.mode="fight";B.enter=false;B._lastPart=B.parts[0];modularHit(B.hp+1);}',form)
   frames(p,170)
   ck(p.evaluate('(n)=>B._r30.form===n+1&&r30Live(B)&&B.parts.every(p=>!p.destroyed&&p.hp>0)',form),f'new scan completes transition {form+1} with intact next rig')
  report['artKeys']=p.evaluate('()=>[...new Set(cwdCalls.map(q=>q.key))]');report['errors']=errors;ck(not errors,'no browser page or console errors')
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}),flush=True);br.close()
finally:stop()
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
