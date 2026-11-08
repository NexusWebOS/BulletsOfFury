from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;O=W/'verification';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));rows=[];errors=[]
def check(name,value):
 rows.append({'name':name,'value':value});assert value,name;print('PASS',name,flush=True)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1366,'height':768})
  p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',timeout=180000)
  p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(2,2)
  p.evaluate("()=>{run.mode='campaign';run.pilot='axel';diffKey='normal';campaign.unlockedMax=1;tutStart({stage:1,lead:'axel',disp:'axel'});tutFinish(true);}")
  p.wait_for_timeout(600);p.keyboard.press('Enter');p.wait_for_function("state===GS.STAGESEL",timeout=15000,polling=100)
  p.wait_for_function('sselBoot===0',timeout=20000,polling=100);p.wait_for_timeout(700)
  check('tutorial completion retains campaign and map focus',p.evaluate("run.mode==='campaign'&&cmap2.focus==='map'&&!campPause&&tutStoreRead().done"))
  p.screenshot(path=str(O/'tutorial-campaign-map.png'))
  p.keyboard.press('Enter');p.wait_for_timeout(2200)
  state=p.evaluate('()=>({state,stage:run.stage,pause:campPause,zoom:!!sselZoom,committed:window.sselCommitted})')
  check('Enter deploys without opening Save',state['pause']is None and (state['state']!='stagesel' or state.get('committed')))
  # Actual mouse toolbar -> mission focus recovery, then deployment.
  p.evaluate("()=>{openStageSelect(1,{});stateT=2;campPause=null;sselZoom=null;_selFlash=null;window.sselCommitted=false;cmap2.focus='map';}")
  p.wait_for_timeout(350)
  p.evaluate(shoot.TRAP_RAF)
  xy=p.evaluate("()=>{const p=cmap2World(1);cmap2.cam={x:p.x,y:p.y,z:1};cmap2.focus='bar';let q=cmap2ToScreen(p.x,p.y+cmap2Bob(1));return{x:q.x,y:q.y};}")
  rect=p.evaluate('()=>{const r=cv.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height};}');dims=p.evaluate('()=>({w:campaignViewWidth(),h:VH})')
  off=p.evaluate('campaignViewOffset()')
  x=rect['x']+(xy['x']+off)/dims['w']*rect['width'];y=rect['y']+xy['y']/dims['h']*rect['height']
  print('POINTER_COORDS',json.dumps(dict(xy=xy,rect=rect,dims=dims,off=off,x=x,y=y)),flush=True)
  p.mouse.move(x,y);p.evaluate('cmap2BarInput(1,1)')
  print('POINTER',json.dumps(p.evaluate('()=>({state,mouse:Input.mouse,focus:cmap2.focus,hit:cmap2IslandAt(Input.mouse.x,Input.mouse.y,1,1),offset:campaignViewOffset()})')),flush=True)
  check('pointer leaving toolbar restores map focus',p.evaluate("cmap2.focus==='map'"))
  p.mouse.click(x,y);p.evaluate('()=>{drawStageSelect(1/60);requestAnimationFrame=__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}')
  p.wait_for_timeout(2200)
  print('MAP_CLICK',json.dumps(p.evaluate('()=>({state,focus:cmap2.focus,committed:window.sselCommitted,mouse:Input.mouse,md:_drawStageSelectInner._md,hit:cmap2IslandAt(Input.mouse.x,Input.mouse.y,1,1),campPause})')),flush=True)
  if p.evaluate('state===GS.STAGESEL&&!window.sselCommitted'):
   pt=p.evaluate('()=>{const q=cmap2World(1);cmap2.cam={x:q.x,y:q.y,z:1};MAP4E.focus=true;const s=cmap2ToScreen(q.x,q.y+cmap2Bob(1));return{x:s.x,y:s.y};}')
   p.mouse.click(rect['x']+(pt['x']+off)/dims['w']*rect['width'],rect['y']+pt['y']/dims['h']*rect['height']);p.wait_for_timeout(2200)
  check('mission click deploys without Save',p.evaluate("!campPause&&(state!==GS.STAGESEL||window.sselCommitted)"))
  # Save is still explicitly available on its own toolbar button.
  p.evaluate("()=>{openStageSelect(1,{});stateT=2;sselZoom=null;_selFlash=null;campPause=null;cmap2.focus='bar';cmap2.bar=0;}")
  p.wait_for_timeout(250);p.keyboard.press('Enter');p.wait_for_timeout(650)
  check('explicit Save remains available',p.evaluate("campPause?.mode==='save'"))
  p.keyboard.press('Escape');p.wait_for_timeout(250)
  check('save menu backs out safely',p.evaluate('!campPause'))
  # Buffer output, native filters/mixer, overlapping voices and mute/stop.
  p.evaluate("()=>{campPause=null;AL116.epoch++;Snd.prepare(['machineGun','expSmall','lockAlert','spaceLaserCannon']);}")
  p.wait_for_function("['machineGun','expSmall','lockAlert','spaceLaserCannon'].every(BOF_AUDIO_LATENCY_1106.ready)",timeout=20000,polling=100)
  audio=p.evaluate('''async()=>{Audio.stopMusic();Snd.loopStopAll();Snd.setVol('master',1);Snd.setVol('sfx',1);Snd._last={};
   const c=Snd._audioCtx();await c.resume();const tap=aq112Tap(),an=c.createAnalyser();an.fftSize=2048;tap.connect(an);
   const bytes=new Uint8Array(an.fftSize);AL116.events=[];Snd.play('machineGun');let peak=0;
   for(let i=0;i<20;i++){await new Promise(r=>setTimeout(r,10));an.getByteTimeDomainData(bytes);for(const v of bytes)peak=Math.max(peak,Math.abs(v-128));}
   an.disconnect();tap.disconnect(an);const n=AL116.events.at(-1);return {peak,event:n,stats:AL116.stats,voices:Snd._sfxVoices.length,bytes:AL116.bytes,errors:AL116.errors};}''')
  check('real WebAudio output reaches shared mixer',audio['peak']>0)
  check('predecoded sound schedules within 10ms',audio['event']['delay']<10)
  check('decoded sound cache stays bounded',audio['bytes']<=64*1024*1024)
  p.evaluate("()=>{Snd._last={};Snd.play('expSmall');Snd.setVol('master',0);}")
  check('master mute reaches already active buffer voices',p.evaluate('[...AL116.active].every(v=>v.gain.gain.value===0)'))
  p.evaluate("()=>{Snd.stopCue('expSmall');Snd.setVol('master',1);}")
  check('stopCue stops actual buffer voice',p.evaluate("[...AL116.active].every(v=>v.name!=='expSmall')"))
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  # Full high-quality space formation with bounded kit loading.
  p.evaluate("()=>{run.mode='arcade';run.pilot='axel';diffKey='furious';run.gravityShipReady=false;beginStage(5);DBGT.god=true;}")
  p.wait_for_function("state===GS.PLAY&&stageLoadReady(5)&&FURY_STREAM.done",timeout=180000,polling=100)
  check('full space formation reaches live play',p.evaluate('run.stage===5&&run.spaceMode&&run.gravityShipReady&&SS===2&&furyShipReady()&&FURY_STREAM.failed===0'))
  p.screenshot(path=str(O/'space-high-quality.png'))
  p.evaluate(shoot.TRAP_RAF)
  # Compare fixed hit geometry and native damage, inside/outside the plume.
  result=p.evaluate('''()=>{EA11.setup(1,'normal');run.pilot='axel';run.weapon=4;run.wvars[4]='flamethrower';run.wlevel=1;player.x=240;player.y=430;
   pBullets=[];flameFire(1);const f=pBullets.find(b=>b.kind==='flame');f.bot=416;f.top=f.bot-flameReach(1);
   return {reach:f.bot-flameSpanTop(f),near:flameHit(f,240,286,20,20),far:flameHit(f,240,240,20,20),dps:flameDmg(1)/FLAME_TICK,ice:flameIsIce()};}''')
  check('flame reaches 138px and respects its far edge',result['reach']==138 and result['near']and not result['far'])
  check('flame DPS and ice variant distinction retained',result['dps']==45 and not result['ice'])
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
  p.screenshot(path=str(O/'flamethrower.png'))
  check('no game exceptions',not errors)
  (O/'results.json').write_text(json.dumps({'checks':rows,'audio':audio,'deploy':state,'flame':result,'errors':errors},indent=2),encoding='utf8');b.close()
finally:
 (O/'partial.json').write_text(json.dumps({'checks':rows,'errors':errors},indent=2),encoding='utf8');stop()
