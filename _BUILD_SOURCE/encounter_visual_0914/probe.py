"""Real Chromium stage-4 visual audit and Furnace shield lifecycle verification."""
from pathlib import Path
import sys,json,base64,hashlib,http.server,subprocess
import imageio_ffmpeg
R=Path(__file__).resolve().parents[2];O=R/'_shots/encounter_visual_0914'
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(R/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));checks=[];errors=[];details={}
def check(v,label):checks.append({'pass':bool(v),'label':label});print(('ok 'if v else'FAIL ')+label,flush=True)
with sync_playwright()as p:
 b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
 pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
 pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
 def step(n):
  for i in range(0,n,20):pg.evaluate('n=>__step(n)',min(20,n-i));pg.wait_for_timeout(10)
 def shot(name):
  (O/(name+'.png')).write_bytes(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL().split(",")[1]')))
 def fight(stage,role):
  pg.evaluate('a=>{__auto=function(){};__fight(a[0],a[1],"yuri");stagePlan=[];enemies=[];story=null;playerHit=function(){};Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);}',[stage,role]);step(2)
  for _ in range(240):
   if pg.evaluate('role=>!!(role==="mini"?subBoss:boss)',role):break
   step(4);pg.wait_for_timeout(20)
  assert pg.evaluate('role=>!!(role==="mini"?subBoss:boss)',role), 'fight target did not spawn'
 def movie(name,n,snaps):
  ff=imageio_ffmpeg.get_ffmpeg_exe();path=O/(name+'.mp4');q=subprocess.Popen([ff,'-y','-v','error','-f','image2pipe','-vcodec','mjpeg','-framerate','30','-i','pipe:0','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
  for f in range(n*30):
   pg.evaluate('()=>__step(2)')
   q.stdin.write(base64.b64decode(pg.evaluate('()=>document.querySelector("#screen").toDataURL("image/jpeg",.90).split(",")[1]')))
   if f in snaps:shot(snaps[f])
   if f%30==0:pg.wait_for_timeout(10)
  q.stdin.close();err=q.stderr.read();assert q.wait()==0,err;subprocess.run([ff,'-v','error','-i',str(path),'-f','null','-'],check=True)
 pg.evaluate("""()=>{window.__blits=[];window.__tag=null;const draw=ctx.drawImage;ctx.drawImage=function(){if(__tag)__blits.push({key:__tag,args:Array.from(arguments).slice(1),alpha:this.globalAlpha,phase:boss&&boss._fz&&boss._fz.phase,pt:boss&&boss._fz&&boss._fz.pt});return draw.apply(this,arguments);};const get=XART.get;XART.get=function(k){const im=get.apply(this,arguments);if(window.__shieldScope&&k.startsWith('mwfx_fire_shield_'))window.__tag=k;return im;};const shield=magmaWardBarrierDraw;magmaWardBarrierDraw=function(){window.__shieldScope=true;window.__tag=null;try{return shield.apply(this,arguments);}finally{window.__tag=null;window.__shieldScope=false;}};const m=drawMfx;drawMfx=function(k){const prev=__tag;__tag=k;try{return m.apply(this,arguments);}finally{__tag=prev;}};window.__shots=[];for(const name of ['stage4MiniMachine','stage4MiniRocket']){const fn=window[name];window[name]=function(owner,slot){const p=shipBossMount(owner,slot),q=fn.apply(this,arguments);__shots.push({mode:owner._s4war.mode,slot,kind:q.kind,x:q.x,y:q.y,mx:p.x,my:p.y});return q;};}}""")
 fight(4,'mini');pg.wait_for_function('()=>XART.rdy("mgcf_1_5")&&XART.rdy("bpfx_proj_missile_0")&&XART.rdy("nsb_olivewarden_intact")',timeout=120000)
 for _ in range(80):
  if pg.evaluate('()=>subBoss&&!subBoss.enter&&subBoss.y>0'):break
  step(6)
 pg.evaluate("()=>{subBoss.x=worldWidth()/2;subBoss.y=subBoss._s4war.homeY;stage4WarfareSetMode(subBoss,'burst');__shots=[];__blits=[];eBullets=[];}")
 movie('Stage4_Mounted_Guns_0914',9,{26:'s4_spread',102:'s4_center',154:'s4_rockets'})
 details['stage4']=pg.evaluate("()=>({shots:__shots,tracers:__blits.filter(q=>q.key==='mgcf_1_5'),blue:__blits.filter(q=>q.key.startsWith('s4w_drone_barrel')),sounds:__alog.snd.filter(q=>q[1].startsWith('warden'))})")
 d=details['stage4'];check({'L','R','CL','CR'}.issubset({q['slot']for q in d['shots']if q['kind']=='mg'}),'stage-4 spread and center barrels all emit separate machine rounds')
 check(all(abs(q['x']-q['mx'])<.01 and abs(q['y']-q['my'])<.01 for q in d['shots']),'machine rounds and rockets spawn exactly at their visible mapped hardpoints')
 check(d['tracers'] and all(q['args'][-1]<=20 for q in d['tracers']),'real stage-4 machine-gun draw calls remain short 20px rounds, never stretched beams')
 check(not d['blue'],'retired blue chaingun attachments are absent')
 check({'L','R'}=={q['slot']for q in d['shots']if q['kind']=='s4rocket'},'rocket salvos leave both mounted turrets')
 check({'wardenGun','wardenCenterGun','wardenRackCharge','wardenRocket'}.issubset({q[1]for q in d['sounds']}),'all four Warden attack sound routes fire')
 fight(4,'boss');pg.wait_for_function('()=>XART.rdy("s4w_boss_idle")',timeout=120000);step(100);shot('s4_carrier_racks')
 pg.evaluate("""()=>{ctx.save();ctx.setTransform(2,0,0,2,0,0);ctx.fillStyle='#102033';ctx.fillRect(0,0,VW,VH);for(const [key,x,y]of [['nsb_olivewarden_intact',5,18],['s4w_boss_idle',245,18]]){const im=XART.get(key);ctx.drawImage(im,x,y,230,250);}ctx.restore();}""");shot('s4_whole_authored_plates')
 # Full live entrance, then actual shield break, rearm and head transitions.
 fight(2,'boss');pg.wait_for_function('()=>Array.from({length:8},(_,i)=>XART.rdy("mwfx_fire_shield_"+i)).every(Boolean)&&XART.rdy("fzt_body_intact")',timeout=120000)
 pg.evaluate("()=>{__blits=[];boss._fz.pt=0;boss._fz.t=0;boss._fz.phase='intro';boss._fz.introY0=null;boss.y=-150;boss.t=0;}")
 movie('Furnace_Real_Flame_Shield_0914',10,{30:'furnace_first_visible',155:'furnace_assembly',234:'furnace_ignition',287:'furnace_arms'})
 shield=pg.evaluate("()=>__blits.filter(q=>q.key.startsWith('mwfx_fire_shield_'))");details['shieldDraws']=shield
 check(any(q['phase']=='intro' and q['pt']<2.7 for q in shield),'real flame shield reaches drawImage during the first torso arrival')
 check(any(q['phase']=='intro' and q['pt']>7.45 for q in shield),'assembly ignition retains the same actual flame shield')
 check(any(q['phase']=='arms'for q in shield),'the opening combat phase uses the same authored flame-shield family')
 check(len({q['key']for q in shield})==8,'all eight authored shield frames animate during the live introduction')
 fallback=pg.evaluate("""()=>{const wanted='mwfx_fire_shield_'+(Math.floor(boss.t*12)%8),saved=XART.rdy;boss._mwBarrier.frame='mwfx_fire_shield_'+((Math.floor(boss.t*12)+1)%8);XART.rdy=function(k){return k===wanted?false:saved.apply(this,arguments);};const actual=magmaWardBarrierFrame(boss);XART.rdy=saved;return actual!==wanted&&actual===boss._mwBarrier.frame;}""")
 check(fallback,'a temporarily undecoded animation cell holds a real flame frame')
 damage=pg.evaluate("""()=>{boss._fz.trans=0;const hp=boss.hp,shield=boss._mwBarrier.hp;_dmgBullet=null;_lastHitX=boss.x;_lastHitY=boss.y;hitBoss(12);return {hull:boss.hp===hp,barrier:boss._mwBarrier.hp<shield};}""");check(damage['hull']and damage['barrier'],'the visible shield absorbs a real hit before hull damage')
 pg.evaluate("()=>{magmaWardBarrierDamage(boss,99999,boss.x,boss.y);}");step(50);shot('furnace_shield_broken')
 check(pg.evaluate('()=>!boss._mwBarrier.active&&boss._mwBarrier.breakT===0'),'breaking the shield removes it after its break animation')
 pg.evaluate("()=>{furnaceEnter(boss,'core');__blits=[];}");step(8);shot('furnace_core_rearm')
 check(pg.evaluate("()=>boss._mwBarrier.active&&boss._mwBarrier.rearms===1&&__blits.some(q=>q.key.startsWith('mwfx_fire_shield_'))"),'core transition rearms and draws the same real flame shield once')
 pg.evaluate("()=>{furnaceEnter(boss,'head');__blits=[];}");step(8);shot('furnace_head_unshielded')
 check(pg.evaluate("()=>!boss._mwBarrier.active&&!__blits.some(q=>q.key.startsWith('mwfx_fire_shield_'))"),'the intended vulnerable head phase stays unshielded')
 check(not errors and not pg.evaluate('()=>window.__err||null'),'no page, console or game-loop errors')
 details['runtimeSha256']=hashlib.sha256((R/'assets/game.js').read_bytes()).hexdigest();(O/'native.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details,'fixture':'Real gameplay with debug fight selection, capture-only invincibility and controlled phase transitions; silent videos.'},indent=2)+'\n');b.close()
stop();assert all(c['pass']for c in checks)
