from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import ast,base64,hashlib,http.server,io,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot,probe_tutorial_1015 as tut
O=R/'_shots/stage1_water_1020';O.mkdir(exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
m=json.loads((R/'assets/game/levels/stage_01/terrain/water_pixellab_1020/ocean.json').read_text(encoding='utf-8'))
sheet=Image.open(R/m['path']).convert('RGBA');checks=[];errors=[];requests=[]
def ck(n,ok,data=None):
 checks.append(dict(name=n,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
def shot(p,n):
 data=base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]'));(O/(n+'.png')).write_bytes(data);return Image.open(io.BytesIO(data)).convert('RGB')
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1366,height=768));p.set_default_timeout(120000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda c:errors.append(c.text[:600]) if c.type=='error' else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.on('request',lambda r:requests.append(r.url) if 'stage_01/terrain/water_pixellab_1020/ocean.webp' in r.url else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ht27Stop==="function"');p.evaluate(shoot.TRAP_RAF)
  ck('Stage1 ocean is not downloaded on title/boot',not requests,requests[:])
  p.evaluate(SETUP,dict(stage=1,pilot='cole',diff='normal'))
  p.evaluate('()=>{ASSETS.ready=true;player.invuln=0;player.dead=false;warmStage(1);stageLoadBegin(1,[_levelCfg().master]);}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&BOFSTAGE1WATER.ready&&XART.rdy("nsa_ship_cole")}')
  ck('Stage load includes the blue atlas before gameplay',p.evaluate('_stageLoads[1].keys.includes(S1W20_ART.key)'))
  cfg=p.evaluate('_levelCfg(1)');before=json.loads((O/'before-reference.json').read_text(encoding='utf-8'))
  ck('Stage1 authored terrain config and world dimensions remain unchanged',cfg==before['cfg'] and p.evaluate('worldWidth()')==before['world'],cfg)
  rows=[];gif=[]
  for i in range(32):
   row=p.evaluate('''i=>{efxClock=(i+.001)/S1W20_ART.fps;mapScroll=800;shake=0;player.invuln=0;
    const im=XART.get(S1W20_ART.key),draw=ctx.drawImage,calls=[];
    ctx.drawImage=function(image,...a){if(image===im)calls.push(a);return draw.call(this,image,...a);};
    ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);ctx.drawImage=draw;
    const c=document.createElement('canvas');c.width=c.height=224;c.getContext('2d').drawImage(im,...S1W20_ART.cells[S1W20.frame],0,0,224,224);
    return{frame:S1W20.frame,calls,png:c.toDataURL().split(',')[1]};}''',i)
   tile=Image.open(io.BytesIO(base64.b64decode(row.pop('png')))).convert('RGBA');x,y,w,h=m['cells'][i]
   row['pixel_match']=tile.tobytes()==sheet.crop((x,y,x+w,y+h)).tobytes();row['hash']=hashlib.sha256(tile.tobytes()).hexdigest();rows.append(row)
   gif.append(shot(p,'native-frame-'+str(i)))
  ck('All32 phases draw through native Stage1 background at a fixed224-square scale',all(r['frame']==i and r['calls'] and all(c[:4]==m['cells'][i] and c[6:]==[224,224] for c in r['calls']) for i,r in enumerate(rows)))
  ck('All32 lossless native phases match atlas pixels and remain distinct',all(r['pixel_match'] for r in rows) and len({r['hash'] for r in rows})==32)
  initial_water_requests=len(requests)
  # Scroll real authored terrain under the new water; do not change coastline alpha or masks.
  snapshots=[]
  for name,scroll in [('open-sea',0),('coast',1500),('river',2500),('boss-arena',3600)]:
   result=p.evaluate('''scroll=>{mapScroll=scroll;player.invuln=0;player.x=340;player.y=VH-110;camX=player.x-VW/2;
    ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();return{width:worldWidth(),scroll:mapScroll,water:S1W20.frame};}''',scroll)
   shot(p,name);p.screenshot(path=str(O/(name+'-desktop.png')));snapshots.append(result)
  ck('Blue ocean draws beneath native coast, river and boss arena',all(s['width']==680 for s in snapshots) and p.evaluate('S1W20.draws>32'),snapshots)
  # Actual update clock animates water with terrain held. Extra draws do not advance it.
  timing=p.evaluate('''()=>{mapScroll=1000;efxClock=0;const prev=efxClock;
   for(let i=0;i<60;i++)updatePlay(1/60);const advanced=efxClock-prev;
   const fixed=mapScroll;const f=[];for(let i=0;i<5;i++){efxTick(1/12);mapScroll=fixed;drawBG(0);f.push(S1W20.frame);}
   const t=efxClock;drawBG(0);drawBG(0);return{advanced,phases:f,held:mapScroll===fixed,drawClockUnchanged:t===efxClock};}''')
  ck('Native update advances animation; held scrolling still animates; extra draws do not advance time',timing['advanced']>.5 and len(set(timing['phases']))==5 and timing['held'] and timing['drawClockUnchanged'],timing)
  p.evaluate('()=>{setState(GS.PLAY);Input.injectTap("p")}');p.evaluate(tut.STEPN,65)
  pauseBefore=p.evaluate('({state,clock:efxClock})');p.evaluate(tut.STEPN,90);pauseAfter=p.evaluate('({state,clock:efxClock})')
  ck('Pause freezes the ocean animation clock',pauseBefore==pauseAfter and pauseAfter['state']=='paused',[pauseBefore,pauseAfter])
  diffs=[]
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=1,pilot='cole',diff=diff))
   diffs.append(p.evaluate('()=>{const n=S1W20.draws;drawBG(0);return{diff:diffKey,blue:S1W20.draws>n,width:worldWidth()}}'))
  ck('All4 difficulties use the same Stage1 ocean and geometry',all(d['blue'] and d['width']==680 for d in diffs),diffs)
  isolation=[]
  for stage in [2,3,4,6,8,9]:
   p.evaluate(SETUP,dict(stage=stage,pilot='cole',diff='normal'))
   isolation.append(p.evaluate('()=>{const cfg=_levelCfg(),n=S1W20.draws;drawBG(0);const a=_liquidFrames(cfg.liquid),b=S1W20.base.frames(cfg.liquid);return{stage:run.stage,draws:S1W20.draws-n,identity:a==null&&b==null||a?.length===b?.length&&a.every((f,i)=>f===b[i])}}'))
  ck('Other stage liquid owners retain their original frame arrays and rendering',all(d['draws']==0 and d['identity'] for d in isolation),isolation)
  p.evaluate('()=>{run.stage=1;warmStage(1);}')
  p.wait_for_function('BOFSTAGE1WATER.ready')
  p.evaluate('()=>{const n=S1W20.draws;connectorSurface(1,80,680);window.__s1connector=S1W20.draws>n;}')
  ck('Stage1 connector uses the same blue water',p.evaluate('__s1connector'))
  # Enter tutorial through its real start flow: it must retain its independent teal owner.
  p.evaluate(tut.SETUP,dict(pilot='cole',mode='arcade',clear=True));p.evaluate('startRun(1)');p.evaluate(tut.STEPN,40);p.evaluate('Input.injectTap("j")');p.evaluate(tut.STEPN,5)
  p.wait_for_function('BOFSTORMGLASS.artReady')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}')
  for _ in range(160):
   result=p.evaluate(tut.STEPN,30)
   if result['tut'] and result['state']=='play':break
  iso=p.evaluate('()=>{const b=S1W20.draws,t=SG20.waterDraws||0;drawBG(0);return{tut:tutLive(),blue:S1W20.draws-b,teal:SG20.waterDraws>t,keys:_stageLoads[1].keys}}')
  ck('Tutorial retains its teal ocean and does not queue the blue atlas',iso['tut'] and iso['blue']==0 and iso['teal'] and 's1w20_ocean' not in iso['keys'],iso)
  shot(p,'tutorial-stays-teal')
  ck('All32 frames share one lazy atlas; stage retirement can reload that same atlas',initial_water_requests==1 and len(set(requests))==1,requests)
  ck('No page, console or failed asset responses',not errors,errors)
  b.close()
finally:stop()
gif[0].save(O/'native-water.gif',save_all=True,append_images=gif[1:],duration=83,loop=0,optimize=True)
report={'passed':sum(c['passed'] for c in checks),'total':len(checks),'errors':errors,'checks':checks,'frames':rows}
(O/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['passed','total','errors']}));raise SystemExit(not all(c['passed'] for c in checks))
