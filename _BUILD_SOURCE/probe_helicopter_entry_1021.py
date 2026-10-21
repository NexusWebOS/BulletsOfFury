"""Native PixelLab sonic-bank playback, damage flashes, tells and safe gaps."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/helicopter_entry_1021';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=b.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready&&window.BOF_SONIC_EFFECTS');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('()=>{run.mode="arcade";run.pilot="cole";pilotIndex=PILOTS.findIndex(q=>q.key==="cole");startRun(1);beginStage(1);curStage=STAGES[0];setState(GS.PLAY);player.invuln=1e9;storySkip();BOFCinematicDirector.cancel();}')
  p.evaluate('''()=>{sx21Warm();window.sx21draws=[];const draw=ctx.drawImage;
   ctx.drawImage=function(im,...args){if(im?._so21)sx21draws.push({...im._so21,args});return draw.call(this,im,...args);};}''')
  p.wait_for_function('()=>Object.values(SX21_ART.banks).every(a=>XART.rdy(a.key)&&XART.rdy(a.sourceKey))')
  p.evaluate('''()=>{boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];eBullets=[];pBullets=[];stagePlan=[];waveIdx=999;spawnClock=9999;_adaptiveSpawnT=9999;mapScroll=1400;spawnBoss('damkeeper');updateOverlordX(boss,0);boss.enter=false;boss.dead=false;boss._ovIntro=null;boss._ovAirborne=false;boss.x=camLeftX()+viewW()/2;boss.y=VH*.25;boss._pivot=0;XART.rdy('ovbody_intact');XART.rdy('ovrotor_00');}''')
  p.wait_for_function('()=>XART.rdy("ovbody_intact")&&XART.rdy("ovrotor_00")')
  p.evaluate('sx21EdgeWarm()');p.wait_for_function('()=>SX21_EDGE_KEYS.every(k=>XART.rdy(k))')
  for diff in ['normal','hard','furious']:
   for direction in [1,-1]:
    side='north' if direction==1 else 'south'
    row=p.evaluate('''([diff,dir])=>{diffKey=diff;DIFF=difficultyForRun(run.mode,diff);boss._ovSonic=null;boss._ovSweep=null;boss._ovVolley=null;boss._chargeTell=null;boss.t=.2;boss._pivot=0;boss.y=-boss.h;ovStartRush(boss);ovRushLeg(boss);boss._ovRush.leg=dir>0?0:1;ovRushLeg(boss);const R=boss._ovRush;R.phase='lock';R.t=.1;R.active=R.index;boss.x=R.lane;const initial=JSON.stringify(R);
     const fill=ctx.fillRect;window.hentryColumns=0;ctx.fillRect=function(...args){if(this.fillStyle==='#ff2018'||this.fillStyle==='#ffb5a5')hentryColumns++;return fill.apply(this,args);};window.hentryFill=fill;
     window.hentryDraw=ovRushWarningDraw;ovRushWarningDraw=()=>{};ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);window.hentryBefore=ctx.getImageData(0,0,cv.width,cv.height).data;ovRushWarningDraw=hentryDraw;
     ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);const px=ctx.getImageData(0,0,cv.width,cv.height).data;let changed=0;for(let i=0;i<px.length;i+=4)if(Math.abs(px[i]-hentryBefore[i])+Math.abs(px[i+1]-hentryBefore[i+1])+Math.abs(px[i+2]-hentryBefore[i+2])>30)changed++;ctx.fillRect=hentryFill;
     return{entry:SX21.edgeLast,changed,columns:hentryColumns,unchanged:initial===JSON.stringify(R),yScreen:(SX21.edgeLast.y-viewTopY())*viewZoom(),VH,debug:{dead:boss.dead,kind:boss.kind,def:SX21.entryDeferred,dir:R.dir,phase:R.phase,fn:ovRushWarningDraw.toString().slice(0,80),bossFn:drawBoss.toString().slice(0,90)}};}''',[diff,direction])
    ck(diff+' '+side+' entry flashes authored arrow/asterisk pixels at correct edge',row['changed']>150 and row['entry']['north']==(direction>0) and (row['yScreen']<120 if direction>0 else row['yScreen']>row['VH']-70) and abs(row['entry']['rotation']-direction*1.57079632679)<.001,row)
    ck(diff+' '+side+' red columns absent and rush state unchanged',row['columns']==0 and row['unchanged'],row['columns'])
    p.screenshot(path=str(O/(diff+'-'+side+'-rush.png')))
    row=p.evaluate('''()=>{const R=boss._ovRush;R.phase='choose';R.t=0;R.beat=-1;const fn=weaponFeedbackSound,cues=[];weaponFeedbackSound=function(k,...args){cues.push(k);return fn.call(this,k,...args);};try{ovRushTick(boss,.12);}finally{weaponFeedbackSound=fn;}R.phase='lock';R.t=R.tune.lock-.001;ovRushTick(boss,.01);ovRushTick(boss,.13);return{phase:R.phase,dir:R.dir,beep:cues.includes('retinaLockBeep')};}''')
    ck(diff+' '+side+' native warning tone and committed rush still advance',row['beep'] and row['phase']=='charge' and row['dir']==direction,row)
    row=p.evaluate('''dir=>{boss._ovRush=null;boss._ovState='fight';ovStartChargeTell(boss);const T=boss._chargeTell;T.dir=dir;T.t=.8;boss._ovSonic=null;boss.y=dir>0?VH*.22:VH*.78;boss.t=.2;const held=JSON.stringify(T);window.hentryFovs=0;const field=l23FovDraw;l23FovDraw=function(){hentryFovs++;return field.apply(this,arguments);};try{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}finally{l23FovDraw=field;}return{entry:SX21.edgeLast,fields:hentryFovs,unchanged:held===JSON.stringify(T)};}''',direction)
    ck(diff+' '+side+' regular ram uses entry markers without a full-height field',row['fields']==0 and row['entry']['dir']==direction and row['unchanged'],row['fields'])
    p.screenshot(path=str(O/(diff+'-'+side+'-ram.png')))
  row=p.evaluate('''()=>{const hashes=[],alphas=[];ctx.setTransform(SS,0,0,SS,0,0);for(const t of [0,.06,.12,.18]){ctx.fillStyle='#10151b';ctx.fillRect(0,0,VW,VH);sx21EntryDraw(boss,camLeftX()+viewW()*.5,1,.95,t);const px=ctx.getImageData(0,0,cv.width,cv.height).data;let h=2166136261;for(const v of px)h=Math.imul(h^v,16777619);hashes.push(h);alphas.push(SX21.edgeLast.alpha);}return{unique:new Set(hashes).size,alphas};}''')
  ck('Flashing warning changes actual rendered marker pixels',row['unique']>=3 and max(row['alphas'])-min(row['alphas'])>.2,row)
  p.set_viewport_size(dict(width=900,height=650));p.wait_for_timeout(150)
  row=p.evaluate('''()=>{boss._ovRush=null;ovStartChargeTell(boss);boss._chargeTell.dir=-1;boss._chargeTell.t=.9;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);const g=SX21.edgeLast;return{x:g.x,left:camLeftX(),right:camRightX(),y:(g.y-viewTopY())*g.z,VH};}''')
  ck('Compact screen keeps southern entry warning inside the visible playfield',row['left']<row['x']<row['right'] and row['VH']-70<row['y']<row['VH'],row)
  p.screenshot(path=str(O/'compact-south.png'))
  p.goto(f'http://127.0.0.1:{port}/docs/previews/sonic_effects_1021/index.html?scene=rushSouth&difficulty=furious&revision=helicopter-entry-1021');p.wait_for_function('!document.querySelector("#replay").disabled');g=p.frames[1]
  ck('Native preview opens south rush',g.evaluate('boss?._ovRush?.dir===-1'))
  p.select_option('#scene','rushNorth');ck('Native preview opens north rush',g.evaluate('boss?._ovRush?.dir===1'))
  ck('No page console draw or asset errors',not errors,errors);b.close()

finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n');print('SUMMARY',report['passed'],'passed',report['failed'],'failed');sys.exit(bool(report['failed']))
