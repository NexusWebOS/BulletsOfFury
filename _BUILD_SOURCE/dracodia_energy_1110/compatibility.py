from native import *
import hashlib
checks={};details={};errors=[];port,stop=serve(str(R))
def check(n,q):checks[n]=bool(q);print(json.dumps({n:q}),flush=True)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>5&&typeof D124!=="undefined"');p.evaluate(TRAP_RAF);p.evaluate(BOOT);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&v18Warm()}');p.evaluate(CHECKPOINT);print('Compatibility probe ready',flush=True)
  details['audio']=p.evaluate("""async()=>{const a=Snd._audioCtx();await a.resume();const out=[];for(const key of ['combatBeam0927',CF48.key,'bossWeaponCharge','shieldHitHeavy','shieldBreakCombat']){let path=BOFA.sfx[key];if(Array.isArray(path))path=path[0];const d=await a.decodeAudioData(await(await fetch(path)).arrayBuffer());let peak=0;for(const x of d.getChannelData(0))peak=Math.max(peak,Math.abs(x));out.push({key,peak,duration:d.duration});}return out;}""")
  check('attack_cues_decode_with_audio',all(q['peak']>.001 and q['duration']>.01 for q in details['audio']))
  for diff,count in [('normal',2),('hard',3),('furious',3)]:
   p.evaluate('(d)=>{diffKey=d;formCheckpoint(6,210);nb23Start(B,"eyeExpansion");}',diff);check(diff+'_laser_pulse_count',p.evaluate('B._r30.v18.attack.pulses')==count)
   p.evaluate('nb23Start(B,"codeGeysers")');check(diff+'_lightning_wave_count',p.evaluate('B._r30.v18.attack.volleys.length')==count)
  p.evaluate("()=>{formCheckpoint(6,210);D124.reduced=true;nb23Start(B,'eyeExpansion');}");step(p,100);shot(p).save(W/'reduced-eyes.png');check('reduced_motion_still_fires_all_pulses',p.evaluate("D124.events.filter(q=>q.event==='eye-pulse').length>=2"));p.evaluate('D124.reduced=false')
  p.evaluate("()=>{formCheckpoint(6,210);const J=j3State(B);J.hp[0]=J.max[0];B._r30.cd=0;window.startBrainHP=B.hp;window.startHomeHP=J.hp[0];}")
  for i in range(800):
   step(p,4)
   if p.evaluate("B._r30.mode!=='fight'"):break
  details['return']=p.evaluate('({mode:B._r30.mode,form:B._r30.v18.form,completed:B._r30.v18._d124Completed,hp:B.hp,pools:j3State(B).hp,events:D124.events})')
  check('full_attack_book_returns_to_main_form',details['return']['mode']!='fight'and details['return']['completed']==6)
  check('return_preserves_brain_and_main_lives',p.evaluate('j3State(B).hp[6]===startBrainHP&&j3State(B).hp[0]===startHomeHP'))
  p.evaluate("()=>{formCheckpoint(6,210);j3State(B).hp[0]=j3State(B).max[0];nb23Start(B,'eyeExpansion');modularHit(B.hp+1);}");step(p,2)
  details['copy_defeat']=p.evaluate('({mode:B._r30.mode,hp:B.hp,pool:j3State(B).hp[6],home:j3State(B).hp[0],targetCount:retinaBossTargets(B).length})')
  check('brain_defeat_uses_native_copy_death',details['copy_defeat']['mode']=='v19copyDeath'and details['copy_defeat']['pool']==0 and details['copy_defeat']['targetCount']==0)
  check('no_compatibility_browser_errors',not errors);br.close()
finally:stop()
before=json.loads((O.parent/'dracodia-showcase/capture.json').read_text())['source_hashes'];check('earlier_form_owners_unchanged',all(hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest()==h for n,h in before.items()))
(O/'compatibility.json').write_text(json.dumps({'checks':checks,'details':details,'errors':errors},indent=2));assert all(checks.values()),[k for k,v in checks.items()if not v]
