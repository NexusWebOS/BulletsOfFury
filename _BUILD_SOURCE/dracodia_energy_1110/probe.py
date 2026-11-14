from native import *
import hashlib
checks={};details={};errors=[];port,stop=serve(str(R))
def check(name,value):checks[name]=bool(value);print(json.dumps({name:value}),flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5&&typeof D124!=="undefined"');p.evaluate(TRAP_RAF);p.evaluate(BOOT);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}');p.evaluate(CHECKPOINT)
  print('Native probe ready',flush=True)
  p.evaluate('formCheckpoint(2,174)');print(p.evaluate("({own:ph21Own(B),full:ph82Full(B),stage:ph21State(B)?.stage,mode:B._r30.mode,dead:B.dead,hp:B.hp,form:B._r30.v18.form,encounter:j3State(B).encounter,parts:B.parts.map(q=>[q.id,q.hp,q.destroyed])})"),flush=True)
  step(p,2);print(p.evaluate("({own:ph21Own(B),full:ph82Full(B),stage:ph21State(B)?.stage,mode:B._r30.mode})"),flush=True)
  p.evaluate("()=>{ph21State(B).action=null;ph82Start(B,'core');}");print(p.evaluate("({kind:ph21State(B).action?.kind,mode:ph21State(B).action?.mode})"),flush=True)
  details['core']=record(p,'phoenix-core-revised',3.4)
  check('phoenix_core_fill_drawn',p.evaluate("Object.keys(D124.draws).some(k=>k.startsWith('core-'))"))
  # Native source collars remain fully opaque; housing masks match the actual source poses.
  check('all_circular_apertures_opaque',p.evaluate("Object.values(D124_ART.eyes).concat(Object.values(D124_ART.phoenix)).every(q=>q.details.every(d=>d.opaque&&d.pixels>100))"))
  p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'eyeExpansion');}");hp=p.evaluate('B.hp');step(p,200)
  check('furious_three_eye_pulses',p.evaluate("D124.events.filter(e=>e.event==='eye-pulse').length===3"))
  check('eye_volley_native_health_preserved',p.evaluate('B.hp')==hp)
  # Probe real hit registration at both eyes during their firing interval.
  for eye in [0,1]:
   p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'eyeExpansion');player.invuln=1e9;}");step(p,60)
   result=p.evaluate("""(i)=>{const P=B._r30.v18.attack,e=nb23Eyes(B)[i];player.x=e.x;player.y=VH-65;player.invuln=0;window.beforeLives=run.lives;window.beforeDead=player.dead;window.beforeHit=player.invuln;return{eye:e,P:P.t,lives:run.lives};}""",eye);step(p,1)
   check('eye_'+str(eye)+'_native_damage',p.evaluate('player.dead||player.invuln>0||run.lives<beforeLives'))
  # Beam gaps and tells are harmless at the same lane.
  for tag,frames in [('charge',16),('gap',74),('recover',164)]:
   p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'eyeExpansion');}");step(p,frames)
   phase=p.evaluate('d124Pulse(B._r30.v18.attack).phase');p.evaluate("()=>{player.x=nb23Eyes(B)[0].x;player.y=VH-65;player.invuln=0;}");step(p,1)
   check('eye_'+tag+'_harmless',p.evaluate('!player.dead&&player.invuln===0')and phase==tag)
  p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'codeGeysers');}");plan=p.evaluate('JSON.stringify(B._r30.v18.attack.targets)');p.evaluate('player.x=camLeftX()+40');step(p,20)
  check('lightning_targets_commit_before_release',p.evaluate('JSON.stringify(B._r30.v18.attack.targets)')==plan)
  check('safe_lane_moves_one_column',p.evaluate("B._r30.v18.attack.volleys.slice(1).every((q,i)=>Math.abs(q.safe-B._r30.v18.attack.volleys[i].safe)===1)"))
  step(p,300)
  check('furious_three_lightning_volleys',p.evaluate("D124.events.filter(e=>e.event==='lightning-volley').length===3"))
  # A stationary pilot inside a committed bolt must take a real native hit.
  p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'codeGeysers');player.x=B._r30.v18.attack.targets[0].x;player.invuln=0;window.beforeLives=run.lives;}");step(p,95)
  check('purple_lightning_native_damage',p.evaluate('player.dead||player.invuln>0||run.lives<beforeLives'))
  # Follow each adjacent open column with ordinary left/right inputs, without invulnerability.
  p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'codeGeysers');player.x=B._r30.v18.attack.volleys[0].safeX;player.invuln=0;window.beforeLives=run.lives;}")
  safe=[];dodgeEncoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','480x512','-framerate','15','-i','pipe:0','-an','-c:v','ffv1','-level','3',str(W/'lightning-dodge.mkv')],stdin=subprocess.PIPE)
  for i in range(330):
   row=p.evaluate("""()=>{const P=B._r30.v18.attack;if(!P?._d124Storm)return null;let q=P.volleys.find(v=>P.t<v.strike+.52)||P.volleys.at(-1);const dx=q.safeX-player.x;Input.keys.arrowleft=dx<-2;Input.keys.arrowright=dx>2;return{t:P.t,x:player.x,target:q.safeX,dead:player.dead,invuln:player.invuln,lives:run.lives};}""");step(p,1)
   if row:safe.append(row)
   if i%4==0:dodgeEncoder.stdin.write(shot(p).tobytes())
  dodgeEncoder.stdin.close();assert dodgeEncoder.wait(timeout=60)==0
  p.evaluate("()=>{Input.keys.arrowleft=Input.keys.arrowright=false;}");details['dodge']=safe
  check('input_only_lightning_dodge_survives',p.evaluate('!player.dead&&player.invuln===0&&run.lives===beforeLives'))
  # Native finite shield budgets, hit flash, and break animation.
  p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'cloudAegis');}");step(p,80);details['shield_before']=p.evaluate('({hp:B.hp,shield:B._r30.v18.attack.shield,t:B._r30.v18.attack.t})');shot(p).save(O/'shield-active.png')
  p.evaluate('modularHit(25)');step(p,1);shot(p).save(O/'shield-hit.png');details['shield_after']=p.evaluate('({hp:B.hp,shield:B._r30.v18.attack.shield,flash:B.flash})')
  check('shield_absorbs_native_budget',details['shield_after']['hp']==details['shield_before']['hp']and details['shield_after']['shield']==details['shield_before']['shield']-25)
  check('shield_native_hit_flash',details['shield_after']['flash']>0)
  step(p,12);shot(p).save(O/'shield-hit-expired.png');check('shield_hit_flash_expires',p.evaluate('B.flash<=0&&B.parts[0].flash<=0'))
  p.evaluate('modularHit(1e8)');step(p,8);shot(p).save(O/'shield-break.png');check('shield_break_native_budget',p.evaluate("B._r30.v18.attack.shield===0&&d124ShieldPhase(B._r30.v18.attack)?.bank==='break'"));step(p,25);check('shield_break_finishes',p.evaluate('d124ShieldPhase(B._r30.v18.attack)===null'))
  p.evaluate("()=>{formCheckpoint(6,210);nb23Start(B,'codeGeysers');}");step(p,95);before=p.evaluate('JSON.stringify([B._r30.v18.attack.t,B.x,B.y,B._r30.v18.brainAge,B._r30.clock])');p.evaluate("setState('paused')");step(p,120)
  check('pause_freezes_attack_and_pose',before==p.evaluate('JSON.stringify([B._r30.v18.attack.t,B.x,B.y,B._r30.v18.brainAge,B._r30.clock])'))
  p.evaluate('setState(GS.PLAY)');p.evaluate('v18Clear(B)');check('clear_cancels_lightning_and_audio',p.evaluate('B._r30.v18.attack===null&&NB81.audioOwner===null'))
  # Check the intended aggressive default rotation, including shield after four laser attacks.
  p.evaluate("()=>{formCheckpoint(6,210);B._r30.cd=0;}");step(p,2400)
  details['default_book']=p.evaluate('D124.events');check('default_book_lasers_storm_and_shield',p.evaluate("D124.events.filter(e=>e.event==='eye-volley').length>=4&&D124.events.some(e=>e.event==='storm-committed')&&D124.events.some(e=>e.event==='shield-charge')"))
  check('all_new_banks_preloaded',p.evaluate('d124Keys().every(k=>XART.rdy(k))'))
  details['draws']=p.evaluate('D124.draws');check('shield_and_bolt_animations_drawn',all(any(k.startswith(t)for k in details['draws'])for t in ['shield-deploy','shield-loop','shield-break','bolt']))
  check('no_browser_errors',not errors);br.close()
finally:stop()
(O/'verification.json').write_text(json.dumps({'checks':checks,'details':details,'errors':errors},indent=2));print(json.dumps({'checks':checks,'errors':errors}),flush=True)
assert all(checks.values()),[k for k,v in checks.items()if not v]


