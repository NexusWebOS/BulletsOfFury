from pathlib import Path
from PIL import Image
import sys,json,base64,io,subprocess,hashlib
W=Path(__file__).resolve().parent;ARCHIVED=W.parent.name=='_BUILD_SOURCE';R=W.parent.parent if ARCHIVED else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/helicopter_death_1111'if ARCHIVED else W.parents[1]/'outputs/helicopter-death';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE/helicopter_effects_1111'if ARCHIVED else W.parent/'helicopter-1111'));from native import serve,STEP,TRAP_RAF,sync_playwright
checks={};details={};errors=[];port,stop=serve(str(R))
def check(n,q):checks[n]=bool(q);print(json.dumps({n:q}),flush=True)
def step(p,n=1):
 e=p.evaluate(STEP,n);assert e is None,e
def shot(p):return Image.open(io.BytesIO(base64.b64decode(p.evaluate("document.querySelector('#screen').toDataURL('image/png').split(',')[1]")))).convert('RGB').resize((480,512),Image.Resampling.NEAREST)
def setup_stage(p,stage,diff):
 p.evaluate("""([stage,diff])=>{debugUnlocked=true;diffKey=diff;debugStartFight(debugFightFor(stage,'boss'),{pilot:'cole'});spawnBoss(stage===1?'damkeeper':'vileexistence');debugFight.spawned=true;warnT=0;DBGT.god=false;DBGT.speed=1;player.dead=player.out=false;player.invuln=1e9;player.x=worldWidth()/2;player.y=VH-65;BOFCinematicDirector.cancel();setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;stagePlan=[];enemies=[];powerups=[];window.B=boss;camX=(worldWidth()-VW)/2;H126.events=[];}""",[stage,diff])
 p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)&&(n===8?v18Warm():h126Keys(1).every(k=>XART.rdy(k)))}',arg=stage)
 p.evaluate("""(stage)=>{if(stage===1){B._ovIntro.done=true;B._ovAirborne=false;B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=174;}else{v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;B.x=worldWidth()/2;B.y=174;B._r30.cd=100;B._r30.v18.arenaPhase=2;}pBullets=[];eBullets=[];playerLocks=[];}""",stage);step(p,2)
def kill(p,stage):
 return p.evaluate("""(stage)=>{window.hpBefore=B.hp;window.scoreBefore=run.score;window.mainBefore=stage===8?j3State(B).hp[0]:0;if(stage===1){for(let i=0;i<50&&!B.dead;i++)hitBoss(B.maxhp*100);}else{B._lastPart=B.parts.find(p=>p.id==='core');for(let i=0;i<50&&B._r30.mode==='fight';i++)modularHit(B.maxhp*100);}window.D=B._h126;return{started:!!D,hp:B.hp,dead:B.dead,mode:B._r30?.mode,score:run.score-scoreBefore};}""",stage)
def record(p,name,seconds):
 enc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','480x512','-framerate','15','-i','pipe:0','-an','-c:v','ffv1','-level','3',str(W/(name+'.mkv'))],stdin=subprocess.PIPE);rows=[];saved=set()
 try:
  for i in range(round(seconds*15)):
   step(p,4);row=p.evaluate("({t:D.t,angle:D.angle,x:D.x,y:D.y,fx:D.fx.length,debris:D.debris.length,shattered:!!D.shattered,done:D.finished,mode:B._r30?.mode,dam:damBroken,raid:!!run._damAssault1002?.started})");rows.append(row);im=shot(p);enc.stdin.write(im.tobytes());phase='shatter'if row['shattered']else'late-spin'if row['t']>DUR[name]*.55 else'spin'
   if phase not in saved and (phase!='shatter'or row['t']>BLAST[name]+.22):saved.add(phase);im.save(O/(name+'-'+phase+'.png'))
   if i%90==0:print(json.dumps({'clip':name,'seconds':round(i/15,1),'shattered':row['shattered']}),flush=True)
 finally:enc.stdin.close();assert enc.wait(timeout=60)==0
 return {'rows':rows,'events':p.evaluate('H126.events'),'draws':p.evaluate('H126.draws')}
DUR={'stage1-normal':8.6,'stage1-furious':8.6,'dracodia':5.4};BLAST={'stage1-normal':6.65,'stage1-furious':6.65,'dracodia':3.85}
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--mute-audio','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':1000});p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None);p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load');p.wait_for_function('window.__bofFrames>4&&typeof H126!=="undefined"');p.evaluate(TRAP_RAF)
  for diff in ['normal','furious']:
   setup_stage(p,1,diff);q=kill(p,1);name='stage1-'+diff;check(name+'_native_lethal_damage_starts_spin',q['started']and q['dead']and q['hp']<=0);check(name+'_native_reward_once',q['score']>0)
   details[name]=record(p,name,9.0);events=details[name]['events'];cook=[e for e in events if e['event']=='cookoff'];check(name+'_explosions_accelerate',len(cook)>14 and cook[-1]['interval']<cook[0]['interval']*.25);check(name+'_spin_accelerates',len(cook)>4 and (cook[-1]['spin']-cook[-2]['spin'])/(cook[-1]['t']-cook[-2]['t'])>(cook[2]['spin']-cook[1]['spin'])/(cook[2]['t']-cook[1]['t'])*3);check(name+'_trails_follow_moving_wreck',max(e['position']['y']for e in cook)-min(e['position']['y']for e in cook)>220)
   check(name+'_shatter_and_completion_once',len([e for e in events if e['event']=='shatter'])==1 and len([e for e in events if e['event']=='death-complete'])==1);check(name+'_actual_debris_visible',max(r['debris']for r in details[name]['rows'])>=20 and any(k.startswith('chunk-')for k in details[name]['draws']));check(name+'_dam_reveal_and_raid_preserved',p.evaluate('damBroken&&run._damAssault1002?.started===true'))
   before=p.evaluate('run.score');p.evaluate('bossDie()');check(name+'_repeat_death_does_not_duplicate_reward',before==p.evaluate('run.score'))
  for diff in ['easy','hard']:
   setup_stage(p,1,diff);q=kill(p,1);check(diff+'_uses_same_helicopter_death_owner',q['started']and p.evaluate("D.family==='normal'"));step(p,45);before=p.evaluate('JSON.stringify([D.t,D.angle,D.fx,D.debris,B.dying])');p.evaluate("setState('paused')");step(p,90);check(diff+'_pause_freezes_whole_death',before==p.evaluate('JSON.stringify([D.t,D.angle,D.fx,D.debris,B.dying])'));p.evaluate('setState(GS.PLAY)')
  setup_stage(p,8,'furious');q=kill(p,8);check('dracodia_real_core_exhaustion_starts_spin',q['started']and q['mode']=='v19copyDeath');check('dracodia_dead_copy_has_no_retina_or_contact',p.evaluate('retinaBossTargets(B).length===0&&!target17BossContact(B,player.x,player.y)'))
  details['dracodia']=record(p,'dracodia',6.1);events=details['dracodia']['events'];check('dracodia_main_return_starts_after_shatter',p.evaluate("B._r30.mode==='v18returnDownload'"));check('dracodia_pools_never_heal',p.evaluate('j3State(B).hp[1]===0&&j3State(B).hp[0]===mainBefore'));check('dracodia_finite_single_breakup',len([e for e in events if e['event']=='shatter'])==1 and len([e for e in events if e['event']=='death-complete'])==1);step(p,240);check('dracodia_native_main_form_resumes',p.evaluate("B._r30.mode==='fight'&&B._r30.v18.form===0&&!B._h126&&B.hp===mainBefore"))
  # A missing pod stays absent from the authored spinning wreck.
  setup_stage(p,8,'normal');p.evaluate("()=>{B._lastPart=B.parts.find(p=>p.id==='left');modularHit(B._lastPart.hp);}");kill(p,8);check('destroyed_pod_preserved_in_spin_identity',p.evaluate("D.family==='dracodia-1'"));step(p,60);before=p.evaluate('JSON.stringify([D.t,D.angle,D.fx,D.debris,B._r30.t])');p.evaluate("setState('paused')");step(p,60);check('dracodia_pause_freezes_spiral_and_particles',before==p.evaluate('JSON.stringify([D.t,D.angle,D.fx,D.debris,B._r30.t])'));p.evaluate('setState(GS.PLAY)');p.evaluate('v18Clear(B)');check('copy_clear_cancels_all_new_effects',p.evaluate('!B._h126'))
  setup_stage(p,8,'furious');p.evaluate('H126.reduced=true');kill(p,8);step(p,340);check('reduced_motion_keeps_native_return',p.evaluate("B._r30.mode==='v18returnDownload'&&!B._h126"));p.evaluate('H126.reduced=false')
  check('new_pages_ready_in_active_stage',p.evaluate('h126Keys(8).every(k=>XART.rdy(k))'));check('no_browser_or_draw_errors',not errors);br.close()
finally:stop()
before=json.loads((W/'before.json').read_text());check('earlier_owners_and_game_js_unchanged',all(hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest()==h for n,h in before.items()if n!='index.html'))
(O/'verification.json').write_text(json.dumps({'checks':checks,'details':details,'errors':errors},indent=2));assert all(checks.values()),[n for n,v in checks.items()if not v]
