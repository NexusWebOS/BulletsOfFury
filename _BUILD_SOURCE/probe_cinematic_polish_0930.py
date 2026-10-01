from pathlib import Path
import sys,json,base64,http.server,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/cinematic_polish_0930';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot as sh
http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
SETUP="""st=>{ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.pilot='yuri';run.mode='campaign';beginStage(st);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;thunderStorm=null;s6Opening=null;s6Wing=null;stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;player.x=worldWidth()/2;player.y=VH-110;player.invuln=999;return true;}"""
rows=[];errors=[]
def ok(v,n,d=None):
 rows.append(dict(ok=bool(v),name=n,detail=d));print(('OK ' if v else 'FAIL ')+n,str(d or '')[:500],flush=True)
def grab(p,n):
 data=base64.b64decode(p.evaluate("()=>cv.toDataURL()").split(',')[1]);(O/(n+'.png')).write_bytes(data);return hashlib.sha256(data).hexdigest()
def wait(p,code):p.wait_for_function(code,timeout=60000)
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=b.new_page(viewport={'width':1000,'height':1100})
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);wait(p,'()=>(window.__bofFrames|0)>4');p.evaluate(sh.TRAP_RAF)
  p.evaluate(SETUP,6);p.evaluate('()=>{stageTimer=curStage.length*.35;missionWarm();whvWarm();drawWorld(0);}')
  wait(p,"()=>['stage6_blue_master','nst6_neoncity','tlv_beam',MISSION29_ART.beam_lightning.key,'whv_cannon','whv_closed_w'].every(k=>XART.rdy(k))")
  p.evaluate('()=>drawWorld(0)');grab(p,'rain_after')
  # Spy only the rectangles while the native rendering still executes.
  r=p.evaluate("""()=>{const draw=ctx.fillRect.bind(ctx),out=[];ctx.fillRect=function(x,y,w,h){out.push({x,y,w,h,color:this.fillStyle});return draw(x,y,w,h);};
   try{wfxDimDraw();thunderStorm={t:.3,dur:2,power:1,bolts:[]};thunderStormDraw();}finally{ctx.fillRect=draw;thunderStorm=null;}
   return {rects:out,left:camLeftX(),right:camRightX(),top:viewTopY()};}""")
  ok(len(r['rects'])>=2 and all(z['x']<=r['left'] and z['x']+z['w']>=r['right'] and z['y']<=r['top'] for z in r['rects']),'rain and Yuri storm dim the complete visible field',r)
  r=p.evaluate("""()=>{const fit=VIEW_FIT;VIEW_FIT=1;const fill=ctx.fillRect.bind(ctx),out=[];
   ctx.fillRect=function(x,y,w,h){out.push({x,y,w,h,color:this.fillStyle});return fill(x,y,w,h);};
   try{wfxDimDraw();const world=out.pop(),bounds={l:camLeftX(),r:camRightX(),top:viewTopY()};
    bg6WeatherGrade(0,0,VW,VH);const launch=out.pop();return {world,bounds,launch};}
   finally{ctx.fillRect=fill;VIEW_FIT=fit;}}""")
  ok(r['world']['x']<=r['bounds']['l'] and r['world']['x']+r['world']['w']>=r['bounds']['r'] and r['world']['y']<=r['bounds']['top'] and r['world']['color']==r['launch']['color'],'zoomed-out sky and launch use the same full-coverage grade',r)
  for x in [35,645]:
   p.evaluate('x=>{player.x=x;for(let i=0;i<40;i++)updateCamX();drawWorld(0);}',x);grab(p,'rain_pan_'+str(x))
  p.evaluate('()=>{player.x=worldWidth()/2;for(let i=0;i<40;i++)updateCamX();spawnBoss("warhive");bossActive=true;boss.enter=false;const W=boss._whv;W.st="hold";W.cx=worldWidth()/2;W.cy=142;W.dep={L:1,R:1};W.beam={side:"L",t:1.9,warn:1.55,fire:1.25,w:VW/3};drawWorld(0);}')
  hashes=[]
  for f in range(4):
   p.evaluate('f=>{boss.t=f/12;drawWorld(0);}',f);hashes.append(grab(p,'beam_after_'+str(f)))
  ok(len(set(hashes))==4,'Harrier beam displays all four authored animation frames')
  r=p.evaluate("""()=>{const W=boss._whv,hit=playerHit;let n=0;playerHit=()=>{n++;};
   const make=t=>W.beam={side:'L',t,warn:1.55,fire:1.25,w:VW/3};
   const q=s67WhvMuzzle(boss,'L');const check=(t,x,y)=>{make(t);player.x=x;player.y=y;const before=n;whvBeamTick1(boss,0);return n-before;};
   const out={warning:check(1.4,q.x,q.y+90),above:check(1.9,q.x,q.y-15),outerRamp:check(1.56,q.x+35,q.y+90),full:check(1.9,q.x,q.y+90),outside:check(1.9,q.x+VW/6+8,q.y+90),muzzleOutside:check(1.9,q.x+35,q.y+2),expired:check(2.81,q.x,q.y+90)};
   make(1.9);W.parts.L.dead=true;whvBeamTick1(boss,0);out.destroyed=W.beam===null;W.parts.L.dead=false;
   W.beam=make(1.9);W.beam2={side:'R',t:1.9,warn:1.55,fire:1.2,w:VW/4};W.beam.w=VW/4;player.x=W.cx;player.y=VH-100;const before=n;whvBeamTick(boss,0);out.twinGap=n-before;playerHit=hit;
   return out;}""")
  ok(r==dict(warning=0,above=0,outerRamp=0,full=1,outside=0,muzzleOutside=0,expired=0,destroyed=True,twinGap=0),'beam collision matches muzzle, taper, opening, shutdown and twin safe lane',r)
  r=p.evaluate("""()=>{const W=boss._whv,out={};for(const n of [0,1,2]){
   W.beam=n?{side:'L',t:1.9,warn:1.55,fire:1.25,w:VW/3}:null;
   W.beam2=n===2?{side:'R',t:1.9,warn:1.55,fire:1.25,w:VW/4}:null;
   const times=[];for(let i=0;i<50;i++){const t=performance.now();boss.t=i/60;drawWorld(0);ctx.getImageData(0,0,1,1);times.push(performance.now()-t);}
   times.sort((a,b)=>a-b);out[n]={median:times[25],p95:times[47]};}return out;}""")
  ok(r['2']['median']<r['0']['median']+5,'twin beam rendering adds less than 5 ms median in the local Chromium check',r)
  p.evaluate('()=>drawWorld(0)');grab(p,'beam_twin')
  p.evaluate(SETUP,7);p.evaluate('()=>{mapScroll=s7mEndScroll();spawnBoss("sludgeemperor");bossActive=true;s7mInit(boss);s7mWarm();drawWorld(0);}')
  wait(p,"()=>Object.keys(S7M_ART).every(k=>XART.rdy('s7m_'+k))&&XART.rdy(stageMasterKey(_levelCfg()))")
  states=[]
  for i in range(0,780):
   p.evaluate('()=>{s7mTick(boss,1/60);boss.t=(boss.t||0)+1/60;drawWorld(0);}')
   if i%6==0:
    r=p.evaluate('()=>({mode:boss._s7mod.mode,t:boss._s7mod.t,y:boss.y,height:boss._s7mod.height,noHit:boss._s7warden.noHit})');states.append(r)
    if r['mode']=='entry' or (r['mode']=='roar' and r['t']<.3):grab(p,'portal_'+str(i).zfill(4))
  entry=[r for r in states if r['mode']=='entry'];land=[r for r in states if r['mode']=='roar']
  ok(len(entry)>5 and max(r['height'] for r in entry)>80 and land and land[0]['height']==0,'portal entrance rises into an arc and lands before roaring',dict(entry=entry,land=land[:2]))
  ok(all(r['noHit'] for r in entry),'entry remains protected until landed intro is finished')
  (O/'portal_states.json').write_text(json.dumps(states,indent=2))
  p.evaluate(SETUP,1);p.evaluate('()=>{debugJump(debugFightFor(1,"boss"));drawWorld(0);}')
  wait(p,'()=>XART.rdy(stageMasterKey(_levelCfg()))')
  p.evaluate('()=>drawWorld(0)');grab(p,'dam_arena')
  r=p.evaluate('()=>({scroll:mapScroll,range:levelScrollRange(),src:_masterSrcY})');ok(0<=r['src']<300,'Stage 1 boss review opens at the dam',r)
  ok(not errors,'native browser has no page or render errors',errors[:10]);b.close()
finally:
 stop();(O/'verification.json').write_text(json.dumps(rows,indent=2))
sys.exit(0 if all(r['ok'] for r in rows) else 1)
