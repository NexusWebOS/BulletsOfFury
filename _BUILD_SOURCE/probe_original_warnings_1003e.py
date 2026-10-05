"""Native pixels for restored warning art; actual Stage X deployment and MP3 playback."""
from pathlib import Path
import json,base64,sys
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/original_warnings_1003e';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.add_init_script('(()=>{const fill=CanvasRenderingContext2D.prototype.fillRect;CanvasRenderingContext2D.prototype.fillRect=function(){if(window.owKey&&typeof ctx!=="undefined"&&this===ctx)owDraws.push(owKey);return fill.apply(this,arguments);};const draw=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(){if(window.owKey&&typeof ctx!=="undefined"&&this===ctx)owDraws.push(owKey);return draw.apply(this,arguments);};})()')
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  p.evaluate('()=>{window.owDraws=[];window.owKey=null;const f=l23FovDraw,a=l23WarnSymbolDraw,r=groundTargetReticleDraw,s=s81003Cell;l23FovDraw=function(b,B,i,q,k){owKey="original-fov-"+l23FovPhase(k);try{return f.apply(this,arguments);}finally{owKey=null;}};l23WarnSymbolDraw=function(b,B){owKey="original-alert-"+l23FovPhase(B.t/B.warm);try{return a.apply(this,arguments);}finally{owKey=null;}};groundTargetReticleDraw=function(x,y,w,progress){owKey="original-retina-"+(progress<.5?"green":progress<.78?"yellow":"red");try{return r.apply(this,arguments);}finally{owKey=null;}};s81003Cell=function(name,frame){if(name==="fov"&&frame<8)owKey="retired-warning";try{return s.apply(this,arguments);}finally{owKey=null;}};const band=s67LaneBand;s67LaneBand=function(){owKey="original-enemy-lane";try{return band.apply(this,arguments);}finally{owKey=null;}};r30Warm();}')
  p.wait_for_function('()=>["hammer_reticle","fx_ground_target_reticle",...Object.keys(XART._src).filter(k=>/^bmfx_(fov|alert)_(green|yellow|red)/.test(k)),...Object.values(FMC_ART).map(a=>a.key),...Object.values(CWD_ART).map(a=>a.key),...Object.values(S81003_ART).map(a=>a.key)].every(k=>XART.rdy(k))',timeout=120000,polling=60)
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  for progress,color in [(.20,'green'),(.60,'yellow'),(.90,'red')]:
   p.evaluate('(k)=>{r30Clear(B);r30Form(B,4);B._r30.mode="fight";B.enter=false;B._r30.seq=1;r30Attack(B);B._r30.attack.t=k*B._r30.attack.tell;owDraws=[];}',progress)
   shot(p,'boss-warning-'+color)
   ck(p.evaluate('(color)=>owDraws.includes("original-fov-"+color)&&!owDraws.includes("retired-warning")',color),color+' boss lane uses original FOV pixels and no new warning sheet')
  p.evaluate('()=>{r30Clear(B);r30Form(B,0);B._r30.mode="fight";B.enter=false;B._r30.seq=1;r30Attack(B);B._r30.attack.t=.75*B._r30.attack.tell;B._r30.wallAge1003=.4;owDraws=[];}');shot(p,'gravity-retina-original')
  ck(p.evaluate('()=>owDraws.includes("original-retina-yellow")&&!owDraws.includes("retired-warning")'),'gravity targeting uses original ground Retina while keeping the chrome shield')
  p.evaluate('()=>{r30Clear(B);r30Form(B,5);B._r30.mode="fight";B.enter=false;r30Attack(B);s81003KnightEnter(B,"jumpTell");B._r30.attack.k1003.age=s81003KnightDur("jumpTell")*.90;owDraws=[];}');shot(p,'knight-retina-original')
  ck(p.evaluate('()=>owDraws.includes("original-retina-red")&&!owDraws.includes("retired-warning")'),'knight jump uses original red ground Retina')
  p.evaluate('()=>{boss=null;bossActive=false;enemies=[];const e=spawnEnemy("s8stalker1003",worldWidth()/2,140,{}),A=e._orbit1003;A.phase="tell";A.warm=1;A.age=.60;A.lanes=s81003EnemyLanes(e,A);owDraws=[];}');shot(p,'enemy-warning-original')
  ck(p.evaluate('()=>owDraws.includes("original-enemy-lane")&&!owDraws.some(k=>k.startsWith("original-alert"))&&!owDraws.includes("retired-warning")'),'ordinary alien uses original lanes without floating boss warning signs')
  report['enemy']=p.evaluate('()=>({keys:owDraws,aliens:enemies.map(e=>({role:e._alien1003,phase:e._orbit1003?.phase,x:e.x,y:e.y}))})');print(json.dumps(report['enemy']))
  # Real map -> wingman select -> duel route, not a manufactured music call.
  p.evaluate('()=>{Audio.init();Audio.resume();Rival24.reset();run.mode="campaign";run.pilot="cole";campaign.unlockedMax=8;campaign.rivalScattered=true;campaign.rivalDefeated=[false,false,false,false,false];sselBoot=0;stateT=2;Input.clearTaps();Input.injectTap("arrowdown");Rival24.mapInput();Input.injectTap("enter");Rival24.mapInput();Input.injectTap("enter");Rival24.selectDraw(.1);Input.injectTap("arrowright");Rival24.selectDraw(.1);Input.injectTap("enter");Rival24.selectDraw(.1);Input.injectTap("enter");Rival24.selectDraw(.1);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;Rival24.tick(1/60);}')
  p.wait_for_function('()=>Snd.music.stagex&&Snd.cur===Snd.music.stagex&&!Snd.cur.paused&&Snd.cur.readyState>=3',timeout=120000)
  report['music']=p.evaluate('()=>({active:!!Rival24.active,path:BOFA.music.stagex,duration:Snd.cur.duration,loop:Snd.cur.loop,volume:Snd.cur.volume,clock:Snd.cur.currentTime,boss6:BOFA.music.boss6})')
  ck(report['music']['active'] and report['music']['path'].endswith('LevelX.mp3') and 88<report['music']['duration']<89,'real Stage X deployment plays the full converted Gasline MP3')
  ck(report['music']['loop'] and report['music']['volume']>0,'Stage X track loops through the normal audible music channel')
  for i in range(15):
   p.evaluate('()=>{for(let j=0;j<12;j++)updatePlay(1/60);drawWorld(0);}');p.wait_for_timeout(8)
  ck(p.evaluate('()=>Snd.cur===Snd.music.stagex&&!Snd.cur.paused'),'normal gameplay updates keep the Stage X track selected')
  p.evaluate('async()=>{const C=new AudioContext();await C.resume();const stream=Snd.cur.captureStream(),src=C.createMediaStreamSource(stream),an=C.createAnalyser();src.connect(an);an.fftSize=2048;window.owMeter={C,an};}')
  rms=[]
  for i in range(6):
   p.wait_for_timeout(250);rms.append(p.evaluate('()=>{const a=new Float32Array(owMeter.an.fftSize);owMeter.an.getFloatTimeDomainData(a);return Math.sqrt(a.reduce((s,v)=>s+v*v,0)/a.length);}'))
  ck(max(rms)>.001,'captured Stage X audio stream contains a non-silent waveform');report['music']['rms']=rms
  ck(p.evaluate('()=>Snd.cur.currentTime>1'),'music playback clock advances normally')
  p.evaluate('()=>{owMeter.C.close();Rival24.finish();Audio.startMusic("boss6");}')
  p.wait_for_function('()=>Snd.cur===Snd.music.boss6&&!Snd.cur.paused',timeout=30000)
  ck(p.evaluate('()=>Snd.music.stagex.paused&&BOFA.music.boss6!==BOFA.music.stagex'),'leaving Stage X stops Gasline and the normal Stage 6 score stays separate')
  report['keys']=p.evaluate('()=>[...new Set(owDraws)]');report['errors']=errors;ck(not errors,'no page or console errors')
  (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}));br.close()
finally:stop()
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
