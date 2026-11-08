from pathlib import Path
import sys,json,time,hashlib,shutil
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));rows=[];errors=[];samples=[]
def check(name,value):
 rows.append(dict(name=name,passed=bool(value)));print('PASS'if value else'FAIL',name,flush=True);assert value,name
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=False,args=['--autoplay-policy=no-user-gesture-required'])
  c=b.new_context(viewport={'width':1366,'height':768},record_video_dir=str(W/'video'),record_video_size={'width':1366,'height':768})
  p=c.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',timeout=180000)
  p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(2,2)
  check('Stage5 restores original space master without orbital structure overlay',p.evaluate("_levelCfg(5).master==='bg_stage05_loop_0923'&&!ls112Live(5)&&_levelCfg(5).liquid===null"))
  check('Stage6 city and Stage9 water arena retain current layered scenes',p.evaluate("_levelCfg(6).master==='ls112_stage_6'&&_levelCfg(9).master==='ls112_stage_9'&&ls112Live(6)&&ls112Live(9)"))
  p.evaluate("()=>{run.mode='arcade';run.pilot='axel';diffKey='furious';run.gravityShipReady=false;beginStage(5);DBGT.god=true;}")
  # Record actual native LAUNCH frames; monitor the real sequence, never skip animation states.
  p.evaluate('''()=>{window.SC116={frames:[],calls:{},partSizes:[],ready:false};const partBlit=furyShipBlit;furyShipBlit=function(k,x,y,w,h,pilot,alpha){if(/^(wing_|engine_|hull_top|nose_top)/.test(k)&&k.endsWith('_top'))SC116.partSizes.push({k,w,h});return partBlit.apply(this,arguments);};const draw=ctx.drawImage;ctx.drawImage=function(im,...args){
   const src=im?.src||'';for(const [tag,end]of [['sky','stage6_blue_master.png'],['city','layered_1102/stage-6.png'],['orbital','layered_1102/stage-5.png'],['stars','stage5_loop.png']])if(src.endsWith(end))SC116.calls[tag]=(SC116.calls[tag]||0)+1;
   return draw.call(this,im,...args);};const old=furyIntroDraw;furyIntroDraw=function(dt){old(dt);const S=drawLaunch._furyIntro;
   if(S){const q={t:S.t,phase:S.phase,gravity:gravityMode.phase,space:S.space,white:furyIntroWhite(gravityMode),scroll:S.scroll};if(!SC116.frames.length||SC116.frames.at(-1).phase!==q.phase||SC116.frames.at(-1).gravity!==q.gravity||SC116.frames.at(-1).space!==q.space)SC116.frames.push(q);}
  };}''')
  for label,cond in [('after-ascent',"state===GS.LAUNCH&&drawLaunch._furyIntro?.t>5"),('after-assembly',"drawLaunch._furyIntro?.phase==='assembly'"),('after-reveal',"drawLaunch._furyIntro?.space&&gravityMode.phase==='reveal'&&gravityMode.t>.3"),('after-space',"state===GS.PLAY&&stageLoadReady(5)")]:
   p.wait_for_function(cond,timeout=180000,polling=20)
   p.screenshot(path=str(W/(label+'.png')))
   samples.append(p.evaluate('()=>({state,stateT,t:drawLaunch._furyIntro?.t,phase:gravityMode.phase,scroll:_stage5SpaceScroll})'))
  flow=p.evaluate('SC116');check('actual assembly parts are proportionally reduced to at most 64px cells',len(flow['partSizes'])>100 and max(q['w']for q in flow['partSizes'])<=64 and all(q['w']==q['h']for q in flow['partSizes']));check('ascent never draws city or orbital structures',not flow['calls'].get('city')and not flow['calls'].get('orbital'))
  check('original blue sky and starfield both render live',flow['calls'].get('sky',0)>100 and flow['calls'].get('stars',0)>10)
  change=next(f for f in flow['frames']if f['space'])
  check('sky-to-space switch remains covered by full white reveal',change['white']>.99 and change['gravity']=='reveal')
  phases=[f['gravity']for f in flow['frames']]
  check('complete original transformation still runs',all(q in phases for q in ['drift','charge','scatter','snap','pixelglow','whiteout','reveal','active']))
  check('space launch ends in native high-quality play with full kit',p.evaluate("state===GS.PLAY&&SS===2&&run.gravityShipReady&&furyShipReady()&&FURY_STREAM.failed===0"))
  # Same backdrop clock crosses countdown/GO without a reset or a scenery swap.
  hand=p.evaluate('()=>({launch:drawLaunch._bgScroll,live:_stage5SpaceScroll,master:_levelCfg().master,kit:{done:FURY_STREAM.done,failed:FURY_STREAM.failed}})')
  check('countdown-to-play scroll is continuous',0<=hand['live']-hand['launch']<500)
  p.wait_for_timeout(3500)
  p.screenshot(path=str(W/'after-combat.png'))
  # Retained Furyship skips a second assembly and enters the same starfield route.
  p.evaluate("()=>{run.gravityShipReady=true;beginStage(5);DBGT.god=true;}")
  p.wait_for_function("drawLaunch._furyIntro?.build===false&&drawLaunch._furyIntro.space",timeout=30000,polling=20)
  check('retained ship uses original space backdrop immediately',p.evaluate("drawLaunch._furyIntro.build===false&&drawLaunch._furyIntro.space&&_levelCfg().master==='bg_stage05_loop_0923'"))
  p.wait_for_function('state===GS.PLAY',timeout=30000,polling=50)
  poses=p.evaluate('''()=>{const result=[];for(const phase of ['drift','charge','scatter','snap','pixelglow'])for(const u of [0,.25,.5,.75,1])for(let i=0;i<FURY_KIT.length;i++){const G={phase,t:u*GRAVITY_SNAP_DUR,age:14,partStartAge:3.1};const q=furyPartPose(G,i,240,300,48);if(!q||q.size>64||q.size<0||!Number.isFinite(q.x)||!Number.isFinite(q.y))return false;if(phase==='pixelglow'&&Math.abs(q.size-48*(FURY_KIT[i].partScale||1))>1e-8)return false;result.push(q);}return result.length===300&&SPACE_SHIP_SIZE===48;}''')
  check('all twelve parts keep finite choreography and exact final docking sizes',poses)
  # Boundary sampler: record live image blits around the exact sky wrap, without mutating the scene clocks.
  sky=p.evaluate('''()=>{const calls=[],old=ctx.drawImage;ctx.drawImage=function(im,...a){calls.push(a);};
   try{for(const t of [0,4487,4488,4489,4999,5000,12345,NaN]){const at=calls.length;stage5AscentBackgroundDraw(t);const b=calls.slice(at);if(b.reduce((v,x)=>v+x[3],0)!==VH||b.some(x=>x[0]!==0||x[1]<0||x[1]+x[3]>5000||x[2]!==VW||x[2]!==x[6]||x[3]!==x[7]))return false;}return true;}finally{ctx.drawImage=old;}}''')
  check('sky wrap keeps source bounds and native proportions',sky)
  check('performance/audio fixes remain installed',p.evaluate("typeof SP116==='object'&&typeof AL116==='object'&&FURY_STREAM.done&&flameReach(1)>=184"))
  check('no browser exceptions during ascent, fusion, combat or retained entry',not errors)
  video=p.video;result={'checks':rows,'samples':samples,'flow':flow,'handoff':hand,'errors':errors}
  (W/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf8')
  c.close();video.save_as(str(W/'stage5-smaller-kit-live.webm'));b.close()
finally:
 stop();(W/'partial.json').write_text(json.dumps({'checks':rows,'errors':errors},indent=2),encoding='utf8')
