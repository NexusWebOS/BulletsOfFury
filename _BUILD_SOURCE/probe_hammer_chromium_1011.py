"""Native Hammer follow-up: actual canvas pixels, collisions and fixed-step video.

Uses shoot's Chromium/server and the existing Hammer/BAL7 encounter fixture.
"""
from pathlib import Path
import base64,json,sys,subprocess
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
OUT=ROOT/'_shots/hammer_chromium_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];videos=[]
def check(name,passed,data=None):
 checks.append({'name':name,'pass':bool(passed),'data':data})
 print(('PASS ' if passed else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport={'width':1280,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.mouse.click(650,450);p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('()=>{hm10Warm();hc11Ready();}')
  p.wait_for_function('()=>hc11Ready()',polling=50)
  def setup(diff='normal'):
   p.evaluate('(diff)=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"cole",diff,fire:false,seconds:60})',diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready&&hc11Ready();}',polling=50)
   p.evaluate('''()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=fb2Intro=null;H3.ending=null;H3.release=false;
    AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];
    B._cin30Spoke=B._fb2IntroSeen=true;B.enter=B.dead=B._noHit=false;B.hp=B.maxhp=6000;B.flash=0;
    const h=B._hammer;h.balance0922=h.gp4FailsafeSeen=h._fb2RageDone=h.intro1002=true;h.mode='storm';
    h.phasePending=false;h.frRecovery=false;h.recovery=null;h.openingJump1003=false;
    h.frArmor={hp:3000,max:3000,t:0,active:true,activated:true,half:true,barrier:0,checkpoints:[.75,.5,.35,.15],rage:false};
    B.x=worldWidth()/2;B.y=180;h.stormHome={x:B.x,y:B.y};camX=B.x-viewW()/2;
    player.dead=player.out=false;player.alive=true;player.invuln=40002;player.x=B.x;player.y=hammerStormFloorY()-60;
    player.roll=player.somer=player._spin=player._voidDeath=null;run.shield=0;shake=whiteBlast=0;
    enemies=[];eBullets=[];pBullets=[];powerups=[];l5Rocks=[];l5RockT=9999;stagePlan=[];spawnClock=9999;
    HC11.events=[];hammerStormTarget(B);hammerStormImpact(B);h.leapFx=0;}''')
  def draw():p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
  def snap(name,render=True):
   if render:draw()
   (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));shots.append(name+'.png')
  setup()
  check('All authored Chromium and intact side-swing frames decode',p.evaluate('hc11Ready()'))
  check('Native screen midpoint converts through the actual world zoom',p.evaluate('Math.abs((hc11MidY()-viewTopY())*viewZoom()-VH/2)<1e-7'),p.evaluate('({top:viewTopY(),mid:hc11MidY(),floor:hammerStormFloorY(),zoom:viewZoom()})'))
  for diff in ['easy','normal','hard','furious']:
   setup(diff)
   q=p.evaluate('''()=>{const h=B._hammer,q=h.stormWaves[2],at=q.split+q.delay+q.warm;q.t=at+.35;
    return{lanes:h.stormWaves.length,ceiling:h.stormWaves.every(q=>q.top===hc11MidY()&&q.y-q.height===q.top),
     hits:hammerStormSpikeHits(q,q.x+14,q.top+1)&&hammerStormSpikeHits(q,q.x+14,q.y-1),
     safe:!hammerStormSpikeHits(q,q.x,q.top-1)&&!hammerStormSpikeHits(q,q.x+19,q.top+10)};}''')
   check(diff+': columns have a straight hit area bounded by the exact halfway line',q['ceiling'] and q['hits'] and q['safe'],q)
   for side in [-1,1]:
    q=p.evaluate('''(side)=>{const h=B._hammer;h.hc11Counter=null;h.hc11CounterDone=false;
     player.x=side<0?camLeftX()+30:camRightX()-30;player.y=PLAY.y+20;
     const C=hc11BeginCounter(B,{x:player.x,y:player.y,seat:1}),anchor={...C.anchor};
     hc11CounterTick(B,C,C.lockAt+.1);const background=!hammerOnPlayerPlane(B)&&Math.abs(hammerDepthScale(B)-.3)<1e-7;
     player.x=worldWidth()+100;const tip=hc11Tip(C,11,C.land.x,C.land.y,C.land.scale,C.land.angle);
     for(let i=0;i<200&&h.hc11Counter;i++)hc11CounterTick(B,C,1/60);
     return{background,side:C.side,rotation:C.land.angle,anchored:Math.hypot(tip.x-anchor.x,tip.y-anchor.y)<1e-7,
      committed:C.anchor.x===anchor.x&&C.anchor.y===anchor.y,done:h.hc11CounterDone&&!h.hc11Counter};}''',side)
    check(diff+' edge '+str(side)+': background jump, fixed head anchor and recovery',all(q[k] for k in ['background','anchored','committed','done']),q)
  # Inspect actual source-key draw calls and scan the game's own alpha:false canvas.
  setup()
  q=p.evaluate('''()=>{const q=B._hammer.stormWaves[3];q.t=q.split+q.delay+q.warm+.35;
   const get=XART.get,draw=ctx.drawImage,keys=[];let last=null;
   XART.get=function(key){last=key;return get.apply(this,arguments);};ctx.drawImage=function(){keys.push(last);return draw.apply(this,arguments);};
   ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#000';ctx.fillRect(0,0,cv.width,cv.height);
   try{hammerStormSpikeDraw(q);}finally{XART.get=get;ctx.drawImage=draw;ctx.restore();}
   const a=ctx.getImageData(0,0,cv.width,cv.height).data;let ink=0,above=0,below=0;
   for(let y=0;y<cv.height;y++)for(let x=0;x<cv.width;x++){const i=(y*cv.width+x)*4;if(a[i]+a[i+1]+a[i+2]>18){ink++;if(y<Math.floor(q.top))above++;if(y>Math.ceil(q.y))below++;}}
   return{ink,above,below,keys,top:q.top,bottom:q.y};}''')
  check('Native beam paints Chromium authored pixels with none beyond either endpoint',q['ink']>500 and q['above']==0 and q['below']==0 and 'arch_chromium_beam_0926' in q['keys'],q)
  snap('native-column-pixels',False)
  setup()
  p.evaluate('()=>{const h=B._hammer;for(let i=0;i<h.stormWaves.length;i++){const q=h.stormWaves[i];q.t=q.split+q.delay+q.warm+(i%2===0?.35:-.35);}h.t=4;h.stormRecovery=null;h.hc11CounterDone=true;}')
  snap('chromium-mid-screen')
  for side in [-1,1]:
   setup('furious')
   p.evaluate('(side)=>{player.x=B.x+side*135;player.y=hc11MidY()-45;hc11BeginCounter(B,{x:player.x,y:player.y,seat:1});}',side)
   for name,time in [('backswing',.25),('background-lock',1.0),('dive',1.62),('strike',1.84+.29),('recovery',2.5)]:
    p.evaluate('(t)=>{const C=B._hammer.hc11Counter;C.t=t;Object.assign(C,hc11Pose(C));B.x=C.x;B.y=C.y;}',time)
    snap(('right' if side>0 else 'left')+'-'+name)
  # Real playerHit and death/contact routes: no invulnerability for the collision assertions.
  setup()
  q=p.evaluate('''()=>{const C=hc11BeginCounter(B,{x:B.x+95,y:hc11MidY()-45,seat:1});player.invuln=0;run.shield=0;
   player.x=C.anchor.x;player.y=C.anchor.y;hc11CounterTick(B,C,C.tell-.01);const safe=!player.dead;
   hc11CounterTick(B,C,.35);return{safe,hit:player.dead||run.shield<0,source:HC11.events.at(-1)?.event};}''')
  check('Real playerHit waits through the warning, then punishes remaining at the anchor',q['safe'] and q['hit'],q)
  setup()
  q=p.evaluate('''()=>{coopOn=true;withSeat(2,()=>{player.reset();player.dead=player.out=false;player.y=hc11MidY()-25;player.x=B.x+70;});
   player.y=hc11MidY()+30;const q=hc11UpperTarget();coopOn=false;return q;}''')
  check('The upper-half trigger also detects the second co-op pilot',q and q['seat']==2,q)
  for mode in ['dance','intro']:
   q=p.evaluate('(mode)=>hc11Fight({_hammer:{},_hammerTime:{mode}})||hc11Fight({_hammer:{},_hama:{mode}})',mode)
   check('Musical '+mode+' remains outside the jump counter',not q)
  def clip(name,upper):
   setup('furious')
   p.evaluate('(upper)=>{if(upper){player.x=B.x+125;player.y=hc11MidY()-35;}else player.x=B._hammer.stormWaves[3].x+45;}',upper)
   args=[imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-r','20','-i','pipe:0','-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))]
   encoder=subprocess.Popen(args,stdin=subprocess.PIPE)
   try:
    for i in range(160):
     p.evaluate('()=>{for(let n=0;n<3;n++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
     encoder.stdin.write(base64.b64decode(p.evaluate('()=>cv.toDataURL("image/jpeg",.90).split(",")[1]')))
     if i in [20,40,58,78,100]:snap(name+'-'+str(i),False)
     p.wait_for_timeout(5)
   finally:encoder.stdin.close()
   if encoder.wait()!=0:raise RuntimeError('Video encoder failed')
   videos.append(name+'.mp4');check(name+' uses live beam and counter draw routes',p.evaluate('HC11.draws.beam>0&&'+('HC11.draws.counter>0' if upper else 'true')),p.evaluate('HC11.draws'))
  clip('bottom-half-columns',False);clip('upper-half-jump-counter',True)
  check('No page, console or asset errors',not errors,errors)
  br.close()
finally:stop()
report={'checks':checks,'errors':errors,'screenshots':shots,'videos':videos,'pass':sum(q['pass'] for q in checks),'fail':sum(not q['pass'] for q in checks)}
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Hammer — Chromium and anchored jump</title><style>body{background:#07101c;color:#eaf7ff;font:16px system-ui;max-width:1200px;margin:28px auto}img{max-width:48%;image-rendering:pixelated}video{width:48%}a{color:#8fdcff}</style><h1>Hammer: Chromium beams + anchored jump strike</h1><p>Native game capture. BOSS5 selects the regular Hammer fight. Columns stop at half-screen; the upper counter locks its position before jumping. Protected fixture recordings show timing and pixels, not a campaign win.</p>'
html+=''.join('<video controls loop muted src="'+v+'"></video>' for v in videos)
html+=''.join('<img loading="lazy" alt="'+s+'" src="'+s+'">' for s in shots)
(OUT/'review.html').write_text(html,encoding='utf-8')
print(json.dumps({'pass':report['pass'],'fail':report['fail'],'errors':errors}),flush=True)
if report['fail']:raise SystemExit(1)
