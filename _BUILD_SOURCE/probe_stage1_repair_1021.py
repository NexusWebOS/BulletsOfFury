"""Native Stage1 release pixels, dam clearance, south return, raid and story framing."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/stage1_repair_1021';O.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));print(('PASS ' if ok else 'FAIL ')+n,flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio','--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport=dict(width=1528,height=900));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&ASSETS.ready');p.evaluate(shoot.TRAP_RAF)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=1,pilot='yuri',invuln=True))
  p.evaluate('''()=>{BOFCinematicDirector.cancel();story=null;stagePlan=[];waveIdx=999;_adaptiveSpawnT=9999;spawnClock=9999;
   subBossDone=true;bossWarned=true;stageTimer=0;boss=null;subBoss=null;enemies=[];eBullets=[];pBullets=[];powerups=[];mapScroll=0;player.invuln=1e9;s1mWarm();
   window.s1rStep=n=>{for(let i=0;i<n;i++){window.__now=(window.__now||performance.now())+1000/60;loop(window.__now);}};
  }''')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(1).ready&&s1mKeys().every(k=>XART.rdy(k));}')
  p.evaluate('''()=>{window.s1rShots=[];const fire=eShootT;eShootT=function(x,y,a,s,k,o){const owner=S1M.actor,q=fire.apply(this,arguments);if(owner&&s1r21Boat(owner)&&q&&!q.dead)s1rShots.push({type:owner.type,t:owner.t,x,y});return q;};}''')
  for kind in ['s1boatpatrol','s1boatgun','s1corvette']:
   p.evaluate('''kind=>{enemies=[];eBullets=[];_navalFlashes=[];mapScroll=0;spawnEnemy(kind,camLeftX()+viewW()*.5,140);window.E=enemies.at(-1);E.y=140;s1rShots=[];window.s1rSawTell=false;}''',kind)
   first=None
   for i in range(1200):
    p.evaluate('mapScroll=0;s1rStep(1);if(E._s1rTell)s1rSawTell=true;')
    if i%60==0:p.wait_for_timeout(10)
    if p.evaluate('s1rShots.length>0'):
     first=p.evaluate('''()=>({shots:s1rShots,warning:s1rSawTell,beached:!!E._beached,flashes:_navalFlashes.filter(f=>f.owner===E).map(f=>({h:f.hpx,follow:!!f.follow,t:f.t,life:f.life,fam:f.fam}))})''')
     p.screenshot(path=str(O/(kind+'-release.png')))
     ink=p.evaluate('''()=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawNavalFlashes();ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<a.length;i+=4)if(a[i+3]>40&&a[i]>100&&a[i+1]>60)n++;return n;}''')
     ck(kind+' actual muzzle reel has visible native pixels',ink>50,ink);break
   ck(kind+' warns before its actual shot and anchors a readable release flash',bool(first) and first['warning'] and any(f['h']>=76 and f['follow'] for f in first['flashes']),first)
  p.evaluate('''()=>{enemies=[];eBullets=[];mapScroll=levelScrollRange();window.s1rTanks=[];
   for(const type of ['s1tankheavy','s1tanklight','s1tankapc']){const e=spawnEnemy(type,340,300);if(e)s1rTanks.push(e);}
   groundTrafficResolve();}''')
  clearance=p.evaluate('''()=>s1rTanks.map(e=>({type:e.type,y:e.y,world:levelSrcY()+e.y,foot:groundTrafficFootprint(e),legal:groundTrafficDamClear(levelSrcY()+e.y,groundTrafficFootprint(e).h)}))''')
  ck('All tank hulls are kept off the actual dam rows at spawn',len(clearance)==3 and all(e['legal'] for e in clearance),clearance)
  ck('Dam concrete stays forbidden even through fail-open terrain checks',p.evaluate('[230,300,410].every(y=>!tankDrivable(340,y,true))'))
  p.screenshot(path=str(O/'dam-clearance.png'))
  # Interrupt a long gun sweep at half health, where the old fight could die before its return.
  for mode in ['normal','hard','furious']:
   p.evaluate('''mode=>{diffKey=mode;DIFF=difficultyForRun('arcade',mode);enemies=[];eBullets=[];spawnBoss('damkeeper');boss.enter=false;boss._ovIntro={done:true};boss._ovAirborne=false;
    updateOverlordX(boss,1/60);boss.hp=boss.maxhp*.49;boss._ovState='gunSweep';window.s1rDirs=[];window.s1rRain=0;window.s1rNorth=false;
    const rain=ovPassRain;window.s1rOriginalRain=rain;ovPassRain=function(){s1rRain++;return rain.apply(this,arguments);};}''',mode)
   for batch in range(100):
    row=p.evaluate('''()=>{for(let i=0;i<30;i++){updateOverlordX(boss,1/60);const d=boss._chargeTell?.dir??boss._chg?.dir;if(['chargeTell','chargeOff'].includes(boss._ovState)&&s1rDirs.at(-1)!==d)s1rDirs.push(d);if(boss._ovState==='chargeOff'&&boss._chg.dir<0)s1rNorth=true;eBullets=[];}return{state:boss._ovState,dirs:s1rDirs,rain:s1rRain,north:s1rNorth};}''')
    p.wait_for_timeout(10)
    if row['north'] and row['rain']>0:break
   ck(mode+' half-health transition reaches south-to-north charge and bullet rain',row['north'] and row['rain']>0 and row['dirs'][:2]==[1,-1],row)
   p.evaluate('ovPassRain=s1rOriginalRain;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0)')
   p.screenshot(path=str(O/(mode+'-south-return.png')))
  ck('The jet raid no longer gates entry into the helicopter fight',p.evaluate('run._damAssault1002=null;damAssaultReady1002()&&run._damAssault1002===null'))
  p.evaluate('''()=>{enemies=[];eBullets=[];boss._ovIntro=null;boss._ovState='fight';boss.hp=0;bossDie();window.s1rRaid={spawned:false,waves:0,early:false};}''')
  for batch in range(180):
   row=p.evaluate('''()=>{s1rStep(30);const A=run._damAssault1002;s1rRaid.waves=Math.max(s1rRaid.waves,A?.waves||0);
    if(enemies.some(e=>e._damBomber1002&&!e.dead)){s1rRaid.spawned=true;if(!boss?.dead||boss.dying<8.6)s1rRaid.early=true;}
    return{state,A,raid:s1rRaid,dying:boss?.dying,stageEnding};}''')
   p.wait_for_timeout(10)
   if row['raid']['spawned'] and not (O/'post-helicopter-jets.png').exists():p.screenshot(path=str(O/'post-helicopter-jets.png'))
   if row['state']!='play':break
  ck('Actual defeat starts the warned jet raid only after the whiteout',row['raid']['spawned'] and not row['raid']['early'] and row['raid']['waves']==4,row)
  ck('Native stage exit waits for raid completion then continues once',row['A']['done'] and row['state']!='play',row)
  p.evaluate('''()=>{boss=null;bossDefeated=false;run._damAssault1002=null;setState(GS.PLAY);player.x=camRightX()-25;updateCamX();setState('paused');playPauseBegin();playPause.t=2;playPause.shown=6;ctx.setTransform(SS,0,0,SS,0,0);playPauseWorldDraw();drawPaused(0);}''')
  p.screenshot(path=str(O/'pause-dam.png'))
  pause=p.evaluate('({m:[ctx.getTransform().a,ctx.getTransform().d,ctx.getTransform().e,ctx.getTransform().f],SS,stageTimer,camX})')
  ck('Paused dam menu restores screen coordinates after the scrolled world',pause['m']==[pause['SS'],pause['SS'],0,0],pause)
  # Actual post-Stage1 director and source artists, with both source bottoms hidden by its panel.
  p.evaluate('''()=>{BOFCinematicDirector.cancel();run.mode='campaign';run.pilot='yuri';BOFCinematicDirector.start(1,()=>{});}''')
  p.wait_for_function('BOFCinematicDirector.active')
  p.wait_for_function('()=>{const s=BOFCinematicDirector.current;return XART.rdy("inv20_yuri")&&XART.rdy("inv20_decker")&&XART.rdy("cin_story_lab_empty")&&bmfReady("dialogue");}')
  for width,height in [(1920,1080),(1366,768)]:
   p.set_viewport_size(dict(width=width,height=height));p.evaluate('_setCinematicViewport(true)')
   r=p.evaluate('''()=>{const s=BOFCinematicDirector.current;s.t=3;s.shown=s.beats[0].text.length;ctx.setTransform(SS,0,0,SS,0,0);BOFCinematicDirector.draw();return{cast:CE20.storyCast,H:VH,caption:UI20.dialogue};}''')
   ck(str(width)+' character source edges extend behind the complete dialogue panel',len(r['cast'])==2 and all(v['bottom']>r['H']*.85 and v['bottom']-v['height']>=0 for v in r['cast']),r)
   p.screenshot(path=str(O/('story-'+str(width)+'.png')))
  p.evaluate('''()=>{window.s1rBgRects=[];const bg=ce20Cover;ce20Cover=function(key,...args){const r=bg.call(this,key,...args);if(key==='cin_story_lab_empty')s1rBgRects.push(r);return r;};const s=BOFCinematicDirector.current;for(const t of [0,1,3,6]){s.t=t;BOFCinematicDirector.draw();}ce20Cover=bg;}''')
  bg=p.evaluate('s1rBgRects')
  ck('Story background keeps a stable camera instead of shimmering through fractional zooms',len(bg)==4 and all(r==bg[0] for r in bg),bg)
  ck('No page, console, draw or asset errors',not errors,errors);b.close()
finally:stop()
q=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(O/'native-report.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in q.items() if k!='checks'}));sys.exit(bool(q['failed']))
