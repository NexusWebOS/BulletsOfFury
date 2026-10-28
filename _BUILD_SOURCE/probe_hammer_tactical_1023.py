from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import sys,json,base64,io
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/hammer_tactical_1023';O=R/'_shots/hammer_tactical_1023';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,ok,data=None):checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS 'if ok else'FAIL ')+name+(' '+json.dumps(data)if not ok else''),flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/balance_lab_1007.js'));p.add_script_tag(path=str(R/'_BUILD_SOURCE/animation_audit_1023/hammer_review_lab_1023.js'));p.set_default_timeout(45000)
  p.evaluate('BAL7.setup({stage:5,kind:"chromehammer",pilot:"cole",diff:"normal",fire:false,seconds:60})');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&ht23Warm()&&ha21Ready();}');p.evaluate('HR23.blue()')
  p.evaluate('''()=>{window.TQ={blits:[],base:ctx.drawImage};ctx.drawImage=function(im,...a){const k=HA21.tags.get(im)||'';if(k)TQ.blits.push(k);return TQ.base.call(this,im,...a);};window.tqDraw=()=>{TQ.blits=[];ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);return TQ.blits;};}''')
  def ev(js,a=None):return p.evaluate(js,a)if a is not None else p.evaluate(js)
  def snap(name):
   im=Image.open(io.BytesIO(base64.b64decode(ev('cv.toDataURL().split(",")[1]')))).convert('RGB');im.save(O/(name+'.png'));return im
  for diff in ['normal','hard','furious']:
   for armored in [False,True]:
    ev('''q=>{HR23.start('pickup',q.diff);B._hammer._ht23ArmorGun=false;HT23.speech=[];if(q.armor)B._hammer.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[],rage:false};else B._hammer.frArmor=null;HT23.events=[];window.C23=B._hammer.hb20Pickup;window.T23={keys:new Set(),earlyShots:0,releaseVisible:0,maxY:99999,phase:[],lastF:null,frameChanges:0};}''',{'diff':diff,'armor':armored})
    frames=[]
    for i in range(340):
     row=ev('''()=>{const C=C23;HR23.step();const keys=tqDraw();for(const k of keys)T23.keys.add(k);if(C.released&&!C.obtained){const h=hammerHeadPoint(B);T23.maxY=Math.min(T23.maxY,h.y);if(keys.some(k=>k.startsWith('ht23_tool')))T23.releaseVisible++;}if(!C.ht23Done&&eBullets.some(q=>q._archBlaster))T23.earlyShots++;const f=keys.find(k=>/^ht23_(toss|catch|fire)/.test(k));if(f&&f!==T23.lastF){T23.frameChanges++;T23.lastF=f;}return{t:C.t,done:C.ht23Done,state:B._hammer.state};}''')
     if diff=='normal'and not armored and i in [0,75,108,123,138,162,177,195,222,243,270,310]:frames.append(snap('phase-'+str(i)))
    row=ev('''()=>({events:HT23.events,keys:[...T23.keys],state:B._hammer.state,done:C23.ht23Done,held:C23.obtained,released:C23.released,offscreen:T23.maxY<viewTopY()-80,releaseDraws:T23.releaseVisible,early:T23.earlyShots,changes:T23.frameChanges,finite:Number.isFinite(B.x+B.y)})''');prefix=diff+(' armored'if armored else' normal')
    ck(prefix+' ordered strike/toss/eject/catch/tactical events', [e['type']for e in row['events']][:5]==['crate-struck','hammer-released-up','gun-ejected','gun-caught','tactical-ready'],row['events'])
    ck(prefix+' hammer physically leaves screen and stays absent after gun catch',row['released']and row['offscreen']and row['releaseDraws']>0,row)
    ck(prefix+' distinct windup/catch/gun frames with no legacy blaster body',row['changes']>12 and any('ht23_toss' in k for k in row['keys'])and any('ht23_catch'in k for k in row['keys'])and any(k.startswith(('ht23_fire','ch23_barrel'))for k in row['keys'])and not any('hf19_chaingun'in k or 'arch_blaster_body'in k for k in row['keys']),{'changes':row['changes']})
    ck(prefix+' no gunfire before weapon arrives; native fight resumes',row['early']==0 and row['held']and row['done']and row['finite'],row)
    if frames:
     frames[0].save(O/'transition.gif',save_all=True,append_images=frames[1:],duration=200,loop=0)
  # Native projectile sockets / warnings, real damaged pixels and expiry.
  ev('''()=>{HR23.start('chaingun','normal');B._hammer.frArmor=null;B._hammer.state='chaingun';B._hammer.t=.4;B._hammer.chainDestroyed=false;B._hammer.ch23Pattern='down';B._hammer.chainMax=B._hammer.chainHP=1000;B.flash=0;}''')
  row=ev('''()=>{eBullets=[];const m=hammerBlasterMount(B);hammerBossChaingunFire(B);return{m,shots:eBullets.map(q=>({x:q.x,y:q.y})),a:ht23GunPose(B)};}''');ck('Native paired bullets leave calibrated visible gun muzzle',len(row['shots'])==2 and all(abs(q['y']-row['m']['muzzleY'])<.01 and abs(abs(q['x']-row['m']['x'])-5)<.01 for q in row['shots']),row)
  row=ev('''()=>{const h=B._hammer,m=hammerBlasterMount(B),hit=hammerBlasterHit(B,m.x,m.muzzleY-30),hp=h.chainHP;B._noHit=false;h.frArmor=null;B._hammerModuleHit='chaingun';hammerBossDamage(B,20);return{hit,damaged:h.chainHP<hp,bodyHp:B.hp};}''');ck('Chaingun Retina target remains inside the real damageable weapon part',row['hit']and row['damaged'],row)
  row=ev('''()=>{B._hammer.hb20PickupDone=true;B._hammer.hammerDestroyed=true;B._hammer.mode='chaingun';fr27BeginArmor(B);const keys=new Set();for(let i=0;i<Math.ceil((FR27_ACT.end+.2)*60);i++){fr27ActivationTick(B,1/60);for(const k of tqDraw())keys.add(k);if(B._hammer.state!=='fr_activation')break;}return{state:B._hammer.state,mode:B._hammer.mode,gun:[...keys].some(k=>k.startsWith('ht23_fire')||k.startsWith('ch23_barrel')),hammer:[...keys].some(k=>k.startsWith('ha21_blue_chromium')||k.startsWith('hf22_blue_tool'))};}''');ck('Chromium activation keeps gun and resumes tactical form without respawning hammer',row['state']=='chain_warn'and row['mode']=='chaingun'and row['gun']and not row['hammer'],row)
  row=ev('''()=>{const get=()=>{tqDraw();return Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);};B.flash=0;B._gp4FlashNext=0;GP4.clock+=1;const before=get();markHit(B,.12);const after=get();let white=0;for(let i=0;i<before.length;i+=4)if(before[i]+before[i+1]+before[i+2]<650&&after[i]>240&&after[i+1]>240&&after[i+2]>240)white++;B.flash=0;return{white,off:tqDraw().some(k=>k.includes('fire_hit'))};}''');ck('New tactical actor visibly flashes white and returns to its palette',row['white']>100 and not row['off'],row)
  ev('''()=>{HR23.blue();B._hammer.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[],rage:false};B._hammer.state='storm_idle';B.flash=0;tqDraw();}''');snap('armored')
  row=ev('''()=>{const q=ha21Blue(B);return{key:q?.a?.key,k:q?.k,w:q?.a?.w,h:q?.a?.h,corrected:!!HT23_ARMOR.sheets[q?.a?.sheet]||q?.a?.key==='ht23_plated_idle'};}''');ck('Clean plated actor uses corrected armor pixels at its baked unit without sprite scaling',row.get('corrected')and row.get('k')==1 and row.get('w')%2==0 and row.get('h')%2==0,row)
  row=ev('''()=>{HR23.start('pickup','furious');B._hammer._hf22Red=true;const C=B._hammer.hb20Pickup;C.t=2.4;C.released=true;C.release={x:B.x-75,y:B.y-172};const keys=tqDraw();return{red:keys.some(k=>k.startsWith('ht23_toss_red')),tool:keys.some(k=>k.startsWith('ht23_tool_red')),blue:keys.some(k=>/^ht23_tool_0$/.test(k))};}''');ck('Rage handoff and detached hammer retain matching red energy',row['red']and row['tool']and not row['blue'],row)
  row=ev('''()=>{XART.rdy('boss_shoot_prompt');return true;}''');p.wait_for_function('XART.rdy("boss_shoot_prompt")')
  row=ev('''()=>{TQ.blits=[];ctx.setTransform(SS,0,0,SS,0,0);bossShootGraphic(B.x-camX,200);return TQ.blits;}''');ck('Boss SHOOT prompt actually blits the Stage6 authored graphic', 'boss_shoot_prompt'in row,row);snap('shoot-sign')
  # Native encoded video with sound and 60Hz state progression.
  ev('HR23.start("pickup","normal")')
  video=ev('''async()=>{const cs=cv.captureStream(30),as=await HR23.audio(),stream=new MediaStream([...cs.getVideoTracks(),...as.getAudioTracks()]),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp8,opus',videoBitsPerSecond:2000000}),chunks=[];rec.ondataavailable=e=>e.data.size&&chunks.push(e.data);const end=new Promise(resolve=>rec.onstop=()=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});rec.start();let last=performance.now(),start=last;await new Promise(resolve=>{const timer=setInterval(()=>{const now=performance.now();HR23.step(Math.min(.035,(now-last)/1000));last=now;if(now-start>11000){clearInterval(timer);resolve();}},1000/60);});rec.stop();const data=await end;HR23.audioRestore();cs.getTracks().forEach(t=>t.stop());return data;}''');(O/'tactical-native.webm').write_bytes(base64.b64decode(video.split(',')[1]));ck('Native transition video recorded with game audio',(O/'tactical-native.webm').stat().st_size>40000)
  br.close()
finally:stop()
ck('No native page/asset errors',not errors,errors);out={'checks':checks,'passed':sum(q['passed']for q in checks),'failed':sum(not q['passed']for q in checks),'errors':errors};(O/'report.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k]for k in ['passed','failed','errors']}));sys.exit(bool(out['failed']))
