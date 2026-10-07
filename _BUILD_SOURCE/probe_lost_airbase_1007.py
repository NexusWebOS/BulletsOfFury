"""Native authored terrain replacement, loop edges, ground travel and world camera."""
from pathlib import Path
import base64,json,hashlib,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1];O=R/'_shots/lost_airbase_1007';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[]};errors=[]
def ck(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
def frames(p,n):
 for i in range(0,n,10):p.evaluate('(n)=>{for(let i=0;i<n;i++){updatePlay(1/60);drawWorld(1/60);}}',min(10,n-i));p.wait_for_timeout(3)
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
src=R/'_ART_SOURCES/hardcorps_1007/stage4_airbase.png';dst=R/'assets/game/hardcorps_1007/stage4_airbase.png'
ck(src.read_bytes()==dst.read_bytes(),'deployed airbase is byte-identical to generated 1024x1536 source')
report['sha256']=hashlib.sha256(dst.read_bytes()).hexdigest()
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':950})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  if not p.evaluate('()=>typeof LA1007!=="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/lost_airbase_1007.js')
  p.evaluate(SETUP,{'stage':4,'diff':'normal'});p.wait_for_function('()=>XART.rdy(LA1007.key)',timeout=120000);frames(p,2)
  ck(p.evaluate('()=>_levelCfg().master===LA1007.key&&worldWidth()===680&&levelScrollRange()===3568'),'new full-stage master preserves world width and campaign progression range')
  p.evaluate('()=>{window.initial={map:mapScroll,scroll:LA1007.scroll};window.travel=0;const draw=drawLevelMaster;window.restoreDraw=draw;drawLevelMaster=function(){const r=draw.apply(this,arguments);travel+=_groundDy;return r;};scorches=[];addScorch(player.x,190,35);window.scorchStart=scorches[0]?.y;}');frames(p,60);shot(p,'ordinary-stage')
  q=p.evaluate('()=>({map:mapScroll-initial.map,scroll:LA1007.scroll-initial.scroll,ground:travel,scorch:scorches[0]?.y-scorchStart})');report['normalTravel']=q
  ck(abs(q['map']-40)<.01 and abs(q['scroll']-40)<.01,'ordinary stage advances terrain and scheduler together at original 40px/s')
  ck(abs(q['ground']-40)<.01 and abs(q['scorch']-q['ground'])<1,'ground decals follow the actual moving new terrain')
  p.evaluate('()=>drawLevelMaster=restoreDraw')
  for phase in [0,1]:
   p.evaluate('(phase)=>{LA1007.scroll=256-phase*la1007TileHeight();LA1007.mapPrev=mapScroll;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);drawLevelMaster(0);}',phase)
   q=p.evaluate('()=>{const y=Math.round(256*SS),w=Math.min(cv.width,Math.round(680*SS)),a=ctx.getImageData(0,y-1,w,1).data,b=ctx.getImageData(0,y,w,1).data;let max=0,sum=0;for(let i=0;i<a.length;i++){const d=Math.abs(a[i]-b[i]);max=Math.max(max,d);sum+=d;}return{max,mean:sum/a.length,tiles:LA1007.tiles};}')
   report['edge'+str(phase)]=q;ck(q['mean']<2,f'loop edge {phase}: reflected neighbors meet without a visible horizontal seam')
   (O/(f'seam-{phase}.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  # Boss arrival changes speed while retaining exactly the same terrain phase.
  p.evaluate(SETUP,{'stage':4,'kind':'stormsovereign','mini':False,'diff':'normal'})
  p.evaluate('()=>{B.enter=false;LA1007.scroll=757;LA1007.mapPrev=mapScroll;window.preBoss=LA1007.scroll;drawLevelMaster(0);window.firstBoss=LA1007.scroll;window.startBossMap=mapScroll;_bossHold=1;_groundSrcPrev=-LA1007.scroll;window.chaseGround=0;}')
  ck(p.evaluate('()=>preBoss===firstBoss'),'boss engagement retains the exact airbase terrain phase')
  p.evaluate('()=>{for(let i=0;i<60;i++){drawLevelMaster(1/60);chaseGround+=_groundDy;}}');shot(p,'sovereign-chase')
  q=p.evaluate('()=>({map:mapScroll-startBossMap,travel:LA1007.scroll-preBoss,ground:chaseGround})');report['chase']=q
  ck(abs(q['map'])<.001 and abs(q['travel']-480)<.01,'pursuit runs at 480px/s while boss holds campaign progression')
  ck(abs(q['ground']-q['travel'])<.01,'ground displacement remains continuous across chase loop wraps')
  # Two camera positions sample different world terrain; moving the player with
  # fixed camera leaves the terrain alone. Scenery never follows the ship.
  p.evaluate('()=>{boss=null;bossActive=false;subBoss=null;subBossActive=false;VIEW_FIT=0;LA1007.scroll=380;LA1007.mapPrev=mapScroll;window.camSamples=[];for(const c of [0,100]){ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);ctx.save();ctx.translate(-c,0);drawLevelMaster(0);ctx.restore();camSamples.push(Array.from(ctx.getImageData(200*SS,240*SS,1,1).data));}}')
  ck(p.evaluate('()=>camSamples[0].some((v,i)=>v!==camSamples[1][i])'),'camera translation reveals different fixed world scenery')
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawLevelMaster(0);window.fixedPixel=Array.from(ctx.getImageData(100*SS,300*SS,1,1).data);player.x=30;drawLevelMaster(0);window.fixedPixel2=Array.from(ctx.getImageData(100*SS,300*SS,1,1).data);}')
  ck(p.evaluate('()=>fixedPixel.every((v,i)=>v===fixedPixel2[i])'),'player motion cannot drag the terrain side banks')
  ck(p.evaluate('()=>tankDrivable(340,0)&&tankDrivable(340,-5000)&&!tankDrivable(80,0)&&!tankDrivable(600,0)'),'ground vehicles use the measured clear highway through every reflected section')
  p.evaluate('()=>{bossDefeated=false;subBossDone=false;spawnSubBoss__inner("olivewarden");B=subBoss;B.enter=false;B.y=B.ty||170;window.held=LA1007.scroll;_bossHold=1;}');frames(p,60)
  ck(p.evaluate('()=>Math.abs(LA1007.scroll-held)<.01'),'miniboss holds the new terrain at its actual encounter location')
  p.evaluate('()=>beginStage(4)');ck(p.evaluate('()=>LA1007.scroll===0&&LA1007.mapPrev===null'),'stage retry resets loop state without inheriting prior pursuit travel')
  report['errors']=errors;ck(not errors,'no browser page or console errors');(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');br.close()
finally:stop()
print(json.dumps({'checks':len(report['checks']),'failed':[q['name'] for q in report['checks'] if not q['ok']],'errors':errors}))
if errors or any(not q['ok'] for q in report['checks']):raise SystemExit(1)
