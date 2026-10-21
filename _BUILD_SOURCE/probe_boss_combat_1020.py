"""Native damage, ordinary gunfire, defense escapes, live audio and final attack proof."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import ast,base64,json,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/boss_redesign_1020';checks=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
t=ast.parse((R/'_BUILD_SOURCE/probe_boss_redesign_1020.py').read_text());BOOT=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='BOOT' for x in n.targets));t=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text());SETUP=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SETUP' for x in n.targets))
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+json.dumps(data) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1400,height=1000));p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None);p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(700,500);p.evaluate(SETUP,dict(stage=8,kind='vileexistence',pilot='cole'));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm();}');p.evaluate(BOOT)
  def setup(form=8,diff='normal'):p.evaluate('([f,d])=>setup20(f,d)',[form,diff])
  def step(n):
   e=p.evaluate(shoot.STEP,n)
   if e:errors.append(e)
  def frame():
   p.evaluate('paint20');return Image.open(BytesIO(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))).convert('RGB')
  for diff in ['easy','normal','hard','furious']:
   setup(2,diff);ck(diff+' all corner warnings clear the top HUD and boss bar',p.evaluate('()=>{for(let i=0;i<40;i++){const c=ph21Corner(B),y=(c.marker.y-viewTopY())*viewZoom();if(y<85||y>VH-90)return false;}return true;}'))
   for attack in ['volley','fan','lance']:
    setup(2,diff);p.evaluate('type=>{window.featherBefore20=PH20.draws.feather||0;ph21Set(B,type,{target:{x:player.x,y:player.y},tell:[1.4,1.2,1.05,.9][b20Rank()],next:0,round:0});}',attack);step(195);row=p.evaluate('({done:!Q.action||Q.action.mode!=="'+attack+'",shots:eBullets.filter(q=>q._ph21Owner===B).length,rendered:(PH20.draws.feather||0)-featherBefore20,finite:Number.isFinite(B.x+B.y)})');ck(diff+' Phoenix '+attack+' runs its native cannon attack with registered art',row['finite'] and (attack=='lance' or row['rendered']>0),row)
   for safe in [0,1,2,3]:
    setup(8,diff);p.evaluate('''safe=>{Q.gunSeen=Q.broken=true;Q.safe=safe;hb20Start(B,"luminaire");Q.action.t=Q.action.tell+.01;player.x=camLeftX()+(safe%2+.5)*viewW()/2;player.y=viewTopY()+((safe>>1)+.5)*viewH()/2;player.invuln=0;run.shield=5;run.lives=9;}''',safe);step(35);ck(diff+f' luminaire safe quarter{safe} preserves the pilot and shields',p.evaluate('!player.dead&&run.shield===5'))
   setup(8,diff);p.evaluate('()=>{Q.gunSeen=Q.broken=true;Q.safe=0;hb20Start(B,"luminaire");Q.action.t=Q.action.tell+.01;player.x=camLeftX()+viewW()*.8;player.y=viewTopY()+viewH()*.8;player.invuln=0;run.shield=5;run.lives=9;}');step(1);ck(diff+' luminaire hits an unprotected pilot outside the safe quarter',p.evaluate('player.dead'))
   for move in ['roll','somer']:
    setup(8,diff);p.evaluate('''move=>{Q.gunSeen=Q.broken=true;Q.safe=0;hb20Start(B,"luminaire");Q.action.t=Q.action.tell-.02;player.x=camLeftX()+viewW()*.5+(move==="roll"?45:-45);player.y=viewTopY()+viewH()*.5+(move==="somer"?45:-45);player.invuln=0;player._rollCool=player._somerCool=0;run.lives=9;run.shield=0;if(move==="roll")startRoll(-1);else startSomersault();}''',move);step(43);ck(diff+' native '+move+' can escape or outlast the final core blast',p.evaluate('!player.dead'))
   setup(8,diff);row=p.evaluate('''()=>{const hp=B.hp;B._lastPart=B.parts[0];modularHit(hp*10);return{hp:B.hp,gate:B.maxhp*.65};}''');ck(diff+' burst damage cannot skip the chaingun pickup',abs(row['hp']-row['gate'])<.01,row)
   setup(8,diff);p.evaluate('()=>{hb20Start(B,"skystrike");}');step(180);row=p.evaluate('''()=>{const A=Q.action,e=B20.events.find(e=>e.kind==='code-hammer-ground-waves');return{wave:!!e,count:Q.waves.length,events:B20.events};}''');ck(diff+' two code waves leave the committed hammer landing',row['wave'] and row['count']==2,row)
   setup(2,diff);p.evaluate('()=>{Q.cool=999;Q.action=null;run.spaceMode=false;run.wlevels=Array(8).fill(0);run.wvars=Array(8).fill(null);weaponFormSelect(7,{kind:"primary1003b",id:"mg"});run.weapon=0;run.wlevel=0;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];player.fireCd=0;const m=ph21Muzzle(B,"cannonL",0);player.x=m.x-(wm26PlayerNose().x-player.x);player.y=viewTopY()+viewH()-66;window.hp20=ph21Part(B,"cannonL").hp;}');p.keyboard.down('j');step(110);p.keyboard.up('j');row=p.evaluate('({damage:hp20-ph21Part(B,"cannonL").hp,last:B._lastPart?.id,body:B.hp})');ck(diff+' ordinary primary fire can hit the outboard cannon',row['damage']>0,row)
  # Full keyboard-native actual frame reels, without dead-fixture debris.
  for form,attack,seconds in [(2,'swoon',7.5),(1,'orbit',8),(1,'atomicPass',9),(8,'skystrike',4),(8,'break',10.8),(8,'punch',3),(8,'fists',3)]:
   setup(form);p.evaluate('''([form,attack])=>{if(form===2){for(const id of ["cannonL","cannonR"]){B._lastPart=ph21Part(B,id);modularHit(B._lastPart.hp+1);}D27_MODULE_DEBRIS.length=0;explosions=[];}else if(form===1)h21Start(B,attack);else{if(["punch","fists"].includes(attack)){Q.rage=Q.broken=true;Q.gunSeen=true;}hb20Start(B,attack);}}''',[form,attack]);images=[]
   for i in range(int(seconds*10)):
    step(6);im=frame();images.append(im)
    if form==2 and p.evaluate('Q.action?.mode')=='corner':im.save(O/'phoenix-corner-warning.png')
   name=('phoenix' if form==2 else 'heli' if form==1 else 'hammer')+'-'+attack+'-final';images[0].save(O/(name+'.webp'),save_all=True,append_images=images[1:],duration=100,loop=0,quality=87)
   for i in [len(images)//3,len(images)*2//3]:images[i].save(O/(name+f'-{i}.png'))
  # A form download must respect the same destroyed inventory as the live rig.
  setup(8);row=p.evaluate('()=>{Q.safe=0;hb20Start(B,"luminaire");const A=Q.action,old=A.area.left;A.t=A.tell+.01;player.x=old+A.area.w/2+20;player.y=A.area.top+A.area.h*.25;player.invuln=0;run.shield=0;run.lives=9;camX=old+100;hb20Luminaire(B,A);return{dead:player.dead,fixed:A.area.left===old};}');ck('Luminaire warning and damage stay committed when the camera pans',row['dead'] and row['fixed'],row)
  setup(8);row=p.evaluate('()=>{coopOn=true;player.dead=true;player2.dead=player2.out=false;player2.x=camLeftX()+120;player2.y=viewTopY()+320;run2.lives=9;const t=b20Target(B);coopOn=false;player.dead=false;return Math.hypot(t.x-player2.x,t.y-player2.y)<.01;}');ck('New attack targets fall back to the living co-op pilot',row)
  for name,form,missing in [('phoenix-podless',2,['cannonL','cannonR']),('phoenix-broken-wing',2,['cannonL','cannonR','wingL']),('hammer-rage',8,['hammer','chaingun'])]:
   setup(form);p.evaluate('''([form,missing])=>{for(const id of missing)B.parts.find(p=>p.id===id).destroyed=true;if(form===8){Q.rage=Q.broken=Q.gunSeen=true;}else Q.stage='swoon';DL20.last=null;v18SetMode(B,"v18formIn");B._r30.v18.from=0;}''',[form,missing]);images=[];builds=p.evaluate('DL20.builds')
   for i in range(15):step(6);images.append(frame())
   row=p.evaluate('({last:DL20.last,builds:DL20.builds})');ck(name+' download contains only the current authored pieces',row['last'] and not any(id in row['last']['parts'] for id in missing),row)
   ck(name+' mesh is cached once rather than rebuilt each frame',row['builds']==builds+1,row);images[0].save(O/(name+'-download.webp'),save_all=True,append_images=images[1:],duration=100,loop=0,quality=87)
  # Approved native recordings must decode and play through the actual mixer.
  for cue in ['bossWeaponCharge','furnaceLaserCharge','enemyMachineGunLight','atomicLaunch','atomicDetonate','shieldBossAbsorb','hammerImpact','hammerChaingun','shadowRelease','furnaceFlameIgnite','weapon']:
   row=p.evaluate('''async key=>{Audio.resume();await Snd._audioCtx().resume();const exists=typeof Audio.SFX[key]==="function";let seen=[];const prior=Snd.play;Snd.play=function(k){seen.push(k);return prior.apply(this,arguments);};try{b20Cue(key);}finally{Snd.play=prior;}const a=seen.at(-1)||key,b=CA15.aliases[a]||a,k=window.BOF_CHIP_PASS?.aliases[b]||b;Snd.prepare(k);await new Promise(r=>setTimeout(r,650));Snd.stopCue(k);Snd._last[k]=0;AV3.last.clear();Snd.play(k);let el;for(let i=0;i<200;i++){el=Snd.pools[k]?.slots.find(s=>s?.attached&&!s.el.paused&&s.el.currentTime>0)?.el;if(el)break;await new Promise(r=>setTimeout(r,10));}return{exists,key:k,playing:!!el,ready:el?.readyState,volume:el?.volume};}''',cue);ck(cue+' actual recording decodes and plays',row['exists'] and row['playing'] and row.get('ready',0)>=2 and row.get('volume',0)>0,row)
  ck('No full-loop combat, renderer or audio errors',not errors,errors);br.close()
finally:stop()
(O/'combat-report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(passed=sum(q['passed'] for q in checks),checks=len(checks),errors=errors)),flush=True);raise SystemExit(not all(q['passed'] for q in checks) or bool(errors))
