"""Real game context, exact fighter source pixels and visible beam roots."""
from pathlib import Path
import json, sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/part2_1011';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1600,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(4)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='lizzie',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(6).ready&&P2_ART.stealth.every(a=>XART.rdy(a.key))&&XART.rdy("whv_ace");}',polling=50)
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.ending=null;H3.release=false;stagePlan=[];enemies=[];boss=subBoss=null;bossActive=false;subBossActive=false;player.invuln=1e9;player._spawnClearT=1e9;}')
  q=p.evaluate('''()=>{const blit=(key,x=0,y=0)=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,256,256);ctx.drawImage(XART.get(key),x,y);const out=ctx.getImageData(0,0,256,256).data.slice();ctx.restore();return out;};
   const source=blit('whv_ace',28,26),blue=blit('p2_stealth_blue_idle'),red=blit('p2_stealth_red_idle'),green=blit('p2_stealth_green_idle');let mismatch=0,alpha=0,paint=[0,0],other=0,lum=0;
   for(let i=0;i<source.length;i+=4){if(source[i+3]>24&&source.slice(i,i+4).some((v,n)=>v!==blue[i+n]))mismatch++;for(const [n,c]of [red,green].entries()){
    if(c[i+3]!==blue[i+3])alpha++;const changed=c[i]!==blue[i]||c[i+1]!==blue[i+1]||c[i+2]!==blue[i+2];
    if(blue[i+3]>24&&changed){paint[n]++;if(!(blue[i+2]>36&&blue[i+2]>blue[i]*1.20&&blue[i+2]>blue[i+1]*1.06))other++;
     const y=a=>a[i]*.2126+a[i+1]*.7152+a[i+2]*.0722;lum=Math.max(lum,Math.abs(y(c)-y(blue)));}}
   }return {mismatch,alpha,paint,other,lum,source:P2_ART.stealth.find(a=>a.role==='red'&&a.pose==='idle').source};}''')
  check('Live XART blue fighter pixels match the exact opening whv_ace',q['mismatch']==0,q)
  check('Red/green swaps preserve alpha, silhouettes, non-paint pixels and luminance',q['alpha']==0 and q['other']==0 and min(q['paint'])>3000 and q['lum']<2,q)
  p.evaluate('''()=>{window.onionJets=[];for(const [n,dir]of ['south','south','east','west'].entries()){const side=n%2?1:-1,e=spawnEnemy('s1jetbomber_b',player.x+side*120,n<2?200:390,{route:'straight'});e._side=side;e._s6storm='s6bomber';e._s6Strike={direction:dir};e._fb2Stealth={role:side>0?'red':'green',direction:dir,t:0};onionJets.push(e);}}''')
  frames(3);p.screenshot(path=str(OUT/'actual-stealth-four-directions.png'))
  q=p.evaluate('()=>onionJets.map(e=>({key:e._p2StealthKey,facing:e._sm10Facing,role:e._ap10Palette}))')
  check('Real enemy draws use the correct fighter bank in south/east/west flight',all(x.get('key')=='p2_stealth_'+x['role']+'_idle' for x in q) and {x['facing'] for x in q}=={'south','east','west'},q)
  p.evaluate('()=>{for(const e of onionJets){e.flash=.2;drawEnemy(e);} }');p.screenshot(path=str(OUT/'stealth-hit-flashes.png'))
  p.evaluate('()=>{enemies=[];s6OpeningInit();s6Opening.phase="reveal";s6Opening.t=3;s6Opening.allT=25;for(const j of s6Opening.jets){j.x=player.x+j.side*110;j.y=200;}}');frames(2)
  p.screenshot(path=str(OUT/'original-opening-fighters.png'))
  q=p.evaluate('()=>({phase:s6Opening.phase,jets:s6Opening.jets.length})');check('Opening fly-past keeps its original authored pair',q['jets']==2 and q['phase'] in ['reveal','intercept'],q)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=2,pilot='lizzie',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(2).ready&&P2_ART.fire_root.every(a=>XART.rdy(a.key))&&p2FireReady();}',polling=50)
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.ending=null;stagePlan=[];enemies=[];boss=subBoss=null;bossActive=false;}');frames(2)
  q=p.evaluate('''()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,500,650);av3Beam(ctx,250,70,Math.PI/2,500,140,'fire',.5);const d=ctx.getImageData(0,0,500,650).data;const span=y=>{let l=500,r=0;for(let x=0;x<500;x++){const i=(y*500+x)*4;if(d[i]>80&&d[i+1]>25&&d[i+2]<220){l=Math.min(l,x);r=Math.max(r,x+1);}}return r-l;};const out={start:span(73),mid:span(110),full:span(190),root:P2.draws.fireRoot,profile:p2FireProfile(140,500)};ctx.restore();return out;}''')
  check('Native fire beam visibly expands from a narrow core into the large column',0<q['start']<q['mid']<q['full'] and q['root']>0,q)
  p.screenshot(path=str(OUT/'isolated-flared-fire-column.png'))
  p.evaluate('()=>on5LaunchEncounter({stage:2,role:"boss",code:"BOSS2"})');frames(180)
  p.evaluate('()=>{const F=boss._fz;F.phase="core";F.trans=0;F.idx=1;F.attack="coreLaser";F.at=2.3;F.burstBeat=-1;F.pools.left=F.pools.right=0;boss._mwStun=0;story=null;fb2Talk=null;}');frames(8)
  p.screenshot(path=str(OUT/'furnace-real-flared-core.png'))
  q=p.evaluate('()=>({root:P2.draws.fireRoot,beams:boss._fz.beams.length,width:boss._fz.beams[0]?.width,kind:boss._fz.beams[0]?.kind})');check('Furnace actual core attack uses the new flared animated root',q['root']>0 and q['beams']>0 and q['kind']=='core',q)
  q=p.evaluate('''()=>{const oldGet=XART.get,oldDraw=ctx.drawImage,seen=[];let key=null;
   try{XART.get=function(k){if(k.startsWith('p2_atom_'))key=k;return oldGet.apply(this,arguments);};ctx.drawImage=function(){if(key){seen.push({key,args:Array.from(arguments).slice(1)});key=null;}return oldDraw.apply(this,arguments);};
    s67Nukes=[];atomFlash=0;for(let i=0;i<32;i++){atomBooms=[{x:worldWidth()/2,y:VH*.8,t:i/32,dur:1,w:240}];drawAtomBooms();}
   }finally{XART.get=oldGet;ctx.drawImage=oldDraw;atomBooms=[];}
   return seen;}''')
  check('Live atomic renderer plays all32 corrected keys with one fixed ground anchor and aspect',len(q)==32 and len({x['key'] for x in q})==32 and all(x['args']==q[0]['args'] for x in q) and q[0]['args'][2:]==[240,360],q[:1])
  p.evaluate('()=>{boss=subBoss=null;bossActive=false;atomBooms=[{x:worldWidth()/2,y:VH*.8,t:.59,dur:1,w:300}];}');frames(1)
  p.screenshot(path=str(OUT/'atomic-live-ground.png'))
  check('No page, console, renderer or missing-asset errors',not errors,errors);br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
 (OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
