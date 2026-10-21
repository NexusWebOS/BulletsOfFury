"""Native warning rendering, sound routing and bounded event audio in BOF."""
from pathlib import Path
import ast,os,sys,json,http.server,traceback,re
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if (Path(__file__).resolve().parent.name=='_BUILD_SOURCE') else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
os.environ['PLAYWRIGHT_BROWSERS_PATH']='C:/Users/Mike/AppData/Local/ms-playwright'
http.server.ThreadingHTTPServer.request_queue_size=128
O=R/'_shots/fov_audio_1015';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];scenes=[]
def check(name,ok,data=None):
 checks.append(dict(name=name,pass_=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
entries=json.loads((R/'assets/data/enemy_atlas_1013.json').read_text(encoding='utf-8'))['entries']
entries=[e for e in entries if e['game']=='bof' and e.get('status')=='current']
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel=os.environ.get('BOF_BROWSER','msedge'),args=['--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':800,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1&enemyAtlas=1',timeout=120000)
  p.wait_for_function('window.BOF_ENEMY_ATLAS?.ready&&typeof CA15!=="undefined"');p.evaluate('BOF_ENEMY_ATLAS.pause(true)')
  p.mouse.click(20,20);p.evaluate('Audio.resume()')
  p.evaluate('''()=>{
   window.QA={calls:[],fov:0,boxes:0,frames:0};const get=XART.get,images=new WeakMap(),draw=ctx.drawImage,cell=polishCell,fov=l23FovDraw,play=Snd.play;
   XART.get=function(k){const im=get.apply(this,arguments);if(im&&typeof im==='object')images.set(im,k);return im;};
   ctx.drawImage=function(im){const k=images.get(im);if(k==='nwarn_lane'||k==='polish_warning')QA.boxes++;return draw.apply(this,arguments);};
   polishCell=function(n){if(n==='warning')QA.boxes++;return cell.apply(this,arguments);};
   l23FovDraw=function(){const r=fov.apply(this,arguments);if(r)QA.fov++;return r;};
   Snd.play=function(key){QA.calls.push(key);if(QA.calls.length>2000)QA.calls.shift();return play.apply(this,arguments);};
   window.qaRender=()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);};
  }''')
  def start(e,diff='normal'):
   v=p.evaluate('async o=>{BOF_ENEMY_ATLAS.pause(true);const r=await BOF_ENEMY_ATLAS.start(o.e,o.diff);BOF_ENEMY_ATLAS.pause(true);QA.calls=[];QA.fov=QA.boxes=0;return r;}',{'e':e,'diff':diff})
   if v.get('error'):raise RuntimeError(str(v))
   return v
  def step(n):
   for i in range(0,n,90):
    p.evaluate('''n=>{for(let j=0;j<n;j++){updatePlay(1/60);BOF_ATLAS_CLOCK.after?.();if(j%15===0)qaRender();QA.frames++;}}''',min(90,n-i));p.wait_for_timeout(2)
  # Reproduce the exact extra muzzle box over a genuine Stage-2 miniboss lane.
  magma=next(e for e in entries if e['id']=='bof-miniboss-magmaward');start(magma)
  p.wait_for_function('()=>{l23FovWarm();return ["green","yellow","red"].every(c=>XART.rdy("bmfx_fov_"+c+"_tall"));}')
  for diff in ['easy','normal','hard','furious']:
   start(magma,diff)
   p.evaluate('''()=>{window.B=subBoss;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=150;polishLanes=[];const m=shipBossMount(B,'L');window.L=polishLane(B,m.x,m.y,Math.PI/2,{mount:'L',warn:2,width:28});}''')
   for f in [.12,.48,.86]:
    p.evaluate('f=>{L.t=L.warn*f;QA.fov=QA.boxes=0;qaRender();}',f)
    a=p.evaluate('({fov:QA.fov,boxes:QA.boxes,phase:l23FovPhase(L.t/L.warn)})')
    check(diff+' Stage2 '+a['phase']+' is FOV without arrow box',a['fov']>0 and a['boxes']==0,a)
    if diff=='normal':p.screenshot(path=str(O/('stage2-'+a['phase']+'.png')))
   p.evaluate('''()=>{const before=QA.fov;window.FAKE={family:'future-family',angles:[Math.PI/2],t:.5,warm:1};ctx.save();ctx.translate(B.x,B.y);window.unknownFov=l23FovDraw(B,FAKE,0,{x:B.x,y:B.y},.5,30);ctx.restore();}''')
   check(diff+' unknown boss family retains FOV',p.evaluate('unknownFov'))
  # Real decoded audio, not just successful function lookup.
  p.evaluate('()=>{BOF_ENEMY_ATLAS.mute(false);Audio.resume();Snd.prepare([...new Set(Object.values(CA15.aliases))]);}')
  p.wait_for_timeout(1800)
  audio=[]
  for key in ['shieldHitCombat','turbo','enemyMachineGun','hammerWhoosh','falvaRelease','fireOrbLaunch','iceOrbLaunch','sludge']:
   row=p.evaluate('''async key=>{const canonical=CA15.aliases[key],pool=Snd.pools[canonical];await Snd._audioCtx().resume();Snd.stopCue(canonical);Snd._last[canonical]=0;AV3.last.clear();Audio.SFX[key]();
    await new Promise(r=>setTimeout(r,10));const a=pool?.slots.find(v=>v?.attached&&!v.el.paused)?.el;if(!a)return{key,canonical,playing:false};
    const c=Snd._audioCtx(),m=c.createAnalyser();m.fftSize=256;let capture=null;
    if(a._bofNode)a._bofNode.connect(m);else{capture=c.createMediaStreamSource((a.captureStream||a.mozCaptureStream).call(a));capture.connect(m);}
    const data=new Float32Array(256);let peak=0;for(let i=0;i<28;i++){await new Promise(r=>setTimeout(r,10));m.getFloatTimeDomainData(data);for(const v of data)peak=Math.max(peak,Math.abs(v));}
    if(a._bofNode)a._bofNode.disconnect(m);capture?.disconnect();return{key,canonical,peak,playing:a.currentTime>0,volume:a.volume,muted:a.muted};}''',key)
   audio.append(row);check(key+' plays decoded nonzero audio',row.get('playing') and row.get('peak',0)>0 and row.get('volume',0)>0,row)
  p.evaluate('BOF_ENEMY_ATLAS.mute(true)')
  p.evaluate('''()=>{QA.calls=[];AV3.last.clear();run.weapon=0;run.wlevel=6;window.audioPair={};const m=shipBossMount(B,'L');
   enemyShotSfx('s7spore');audioPair.toxic=QA.calls.slice();QA.calls=[];
   enemyShotSfx('warpshard');audioPair.crystal=QA.calls.slice();QA.calls=[];
   eShootT(m.x,m.y,Math.PI/2,4,'s1bullet',{silent:true});audioPair.silent=QA.calls.slice();
   const owner={x:m.x,y:m.y,hp:100},opts={from:m,target:{x:m.x,y:VH-100},warm:1,art:'storm',mode:'lob'};
   QA.calls=[];const ball=tb28Fire(owner,opts);QA.calls=[];tb28Release(ball);audioPair.ball=QA.calls.slice();
   QA.calls=[];tb28Arrive(ball,ball.tx,ball.ty);tb28Arrive(ball,ball.tx,ball.ty);audioPair.impact=QA.calls.slice();
   QA.calls=[];const quiet=tb28Fire(owner,{...opts,silent:true});tb28Release(quiet);tb28Arrive(quiet,quiet.tx,quiet.ty);audioPair.quiet=QA.calls.slice();
   const explicit=tb28Fire(owner,{...opts,onRelease:()=>Audio.SFX.enemyBossCannon()});QA.calls=[];tb28Release(explicit);audioPair.explicit=QA.calls.slice();
   QA.calls=[];Audio.SFX.machineGun();audioPair.cole=QA.calls.slice();Audio.SFX.enemyMachineGunHeavy();audioPair.enemy=QA.calls.slice();
  }''')
  pair=p.evaluate('audioPair')
  check('toxic ammunition uses toxic recording',pair['toxic']==['av3_toxic_spit'],pair)
  check('crystal shards use electric crystalline report',pair['crystal']==['enemyElectricBolt'],pair)
  check('silent twin/volley partners stay silent',not pair['silent'] and not pair['quiet'],pair)
  check('targeted ball has one launch and one impact',len(pair['ball'])==1 and len(pair['impact'])==1,pair)
  check('explicit launch does not receive a duplicate',len(pair['explicit'])==1 and pair['explicit'][0] in ['enemyBossCannon','bossCannon'],pair)
  check('Cole upgrade suppression does not silence enemy gun',not pair['cole'] and len(pair['enemy'])==1,pair)
  checks2=p.evaluate('''()=>{QA.calls=[];qaRender();qaRender();const render=QA.calls.length;
   tb28List=[];const owner={x:200,y:200,hp:50},ball=tb28Fire(owner,{target:{x:200,y:400},art:'storm'});QA.calls=[];owner.dead=true;tb28Tick(2);const cancelled=ball.dead&&QA.calls.length===0;
   const before=CA15.requests;Snd.play('shieldHitCombat');const direct=QA.calls.at(-1);return {render,cancelled,direct,requests:CA15.requests-before};}''')
  check('rendering never starts combat audio',checks2['render']==0,checks2)
  check('destroyed launcher cancels pending sound',checks2['cancelled'],checks2)
  check('direct alias uses the original shield cue',checks2['direct']=='shieldHitCombat' and checks2['requests']==1,checks2)
  hammer=next(e for e in entries if e['id']=='bof-boss-chromehammer')
  for diff in ['easy','normal','hard','furious']:
   start(hammer,diff)
   row=p.evaluate('''()=>{window.B=boss;BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];
    B._cin30Spoke=B._fb2IntroSeen=true;B.enter=B.dead=B._noHit=false;B.hp=B.maxhp=6000;B.x=worldWidth()/2;B.y=180;
    const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.mode='hammer';h.phasePending=false;h.frRecovery=false;h.recovery=null;h.openingJump1003=false;
    h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};hammerState(B,'chain_warn');h.t=.3;
    QA.fov=QA.boxes=0;qaRender();const fov=QA.fov,boxes=QA.boxes;QA.calls=[];h.cp12Sound=0;const q={x:B.x,y:B.y+85};cp12Absorb(B,q);
    return {fov,boxes,absorbed:q.dead,cues:QA.calls.slice()};}''')
   check(diff+' Hammer chain warning is FOV only',row['fov']>0 and row['boxes']==0,row)
   check(diff+' actual shield absorption requests sound',row['absorbed'] and len(row['cues'])==1,row)
   if diff=='normal':p.screenshot(path=str(O/'hammer-warning.png'))
  # Sample every current BOF actor through the live encounter adapter. These
  # are short native pattern samples, not exhaustive campaign/balance clears.
  jobs=[(e,'normal') for e in entries]
  if os.environ.get('BOF_ALL_TIERS'):
   jobs += [(e,d) for e in entries if e['spawn']['method']!='enemy' for d in ['easy','hard','furious']]
  for e,diff in jobs:
   if os.environ.get('BOF_FOCUSED_ONLY'):break
   start(e,diff);step(1200 if e['spawn']['method']!='enemy' else 480)
   row=p.evaluate('({id:BOF_ENEMY_ATLAS.entry.id,diff:diffKey,...BOF_ENEMY_ATLAS.snapshot(),fov:QA.fov,boxes:QA.boxes,cues:[...new Set(QA.calls)],requests:QA.calls.length})');scenes.append(row)
   check(diff+' '+e['id']+' renders without anchored arrow boxes',row['boxes']==0 and not row.get('error'),{k:row[k] for k in ['fov','boxes','cues','projectiles']})
   if diff=='normal' and e['category'] in ['boss','miniboss'] and e['spawn'].get('method')=='encounter':
    p.screenshot(path=str(O/(e['id']+'.png')))
  check('sound voices stay within the existing hardware budget',p.evaluate('Snd._sfxVoices.length<=Snd._voiceLimit'),p.evaluate('({voices:Snd._sfxVoices.length,limit:Snd._voiceLimit})'))
  check('no browser/page/media errors',not errors,errors)
  b.close()
except Exception as exc:errors.append(str(exc));print(traceback.format_exc(),flush=True)
finally:
 stop();report={'checks':checks,'passed':sum(q['pass_'] for q in checks),'failed':sum(not q['pass_'] for q in checks),'errors':errors,'scenes':scenes,'audio':locals().get('audio',[]),'scope':'Native samples of current BOF actors; not exhaustive paths, campaign clears, balance or human reaction-time proof.'};(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k in ['passed','failed','errors']}),flush=True)
if errors or report['failed']:sys.exit(1)
