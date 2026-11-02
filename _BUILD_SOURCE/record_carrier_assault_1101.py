"""Four native assault films: actual entrance/attacks, input-only takedowns.
Invulnerable observer; no enemy HP, form, phase or attack-clock writes.
"""
from pathlib import Path
import sys,json,ast,base64,subprocess,hashlib,time
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from rough_riders_capture_base_1028 import CAPTURE
W=R/'_shots/carrier_assault_1101/video';W.mkdir(parents=True,exist_ok=True);ff=imageio_ffmpeg.get_ffmpeg_exe()
tree=ast.parse((R/'_BUILD_SOURCE/probe_carrier_assault_1101.py').read_text());SETUP=next(ast.literal_eval(a.value)for a in tree.body if isinstance(a,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SETUP'for t in a.targets))
CASES=[('pair-top','Paired carriers / staggered top entry'),('pair-bottom','Paired carriers / staggered bottom entry'),('nuclear','Nuclear silo carrier / sky-return warheads'),('laser','Laser warhead carrier / growing radial beams and tornadoes')]
if len(sys.argv)>1:CASES=[q for q in CASES if q[0]in sys.argv[1:]]
files=['assets/game.js','assets/cloud_carrier_1101.js','assets/cloud_carrier_art_1101.js','assets/carrier_assault_1101.js','assets/carrier_assault_art_1101.js'];hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files};errors=[]
script=CAPTURE.replace('gain.gain.value=.5','gain.gain.value=.22').replace('4500000','3200000');i=script.index(' function aim(elapsed){');j=script.index(' function render(){',i)
script=script[:i]+r''' function aim(elapsed){
 Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.mouse.active=false;
 const t=(performance.now()-caseStarted)/1000,A=reviewBot,kind=cfg.kind,pair=kind.startsWith('pair-');
 let target=null,fire=t>(pair?17:24),tx=worldWidth()/2,ty=VH-64;
 if(pair){
  const C=CC111.carriers.find(c=>c.parts.some(sc12Alive))||CC111.carriers.find(c=>sc12Alive(c.core));
  if(C){target=C.parts.filter(e=>sc12Alive(e)&&e.y>PLAY.y+10&&e.y<VH-18).sort((a,b)=>b.y-a.y)[0]||(C.hullOpen?C.core:null);}
  if(CC111.carriers.some(c=>c.hullOpen)){if(A.hullAt==null)A.hullAt=t;if(t-A.hullAt<2.0)fire=false;}
 }else{
  const heads=CA111.actors.filter(e=>sc12Alive(e)&&e._ca111.role==='warhead'&&e.y>PLAY.y+30&&e.y<VH-30&&(e._ca111.kind!=='nuclear'||e._ca111.phase==='fall'));
  if(!CA111.events.some(e=>e.event==='warhead-intercepted'))target=heads.sort((a,b)=>a._ca111.age-b._ca111.age)[0];
  target=target||CA111.actors.find(e=>sc12Alive(e)&&e._ca111.role==='carrier');
 }
 if(target&&t>12)tx=target.x;else tx+=Math.sin(t*.65)*45;
 if(pair&&t>6&&t<10){const C=CC111.carriers[0];if(C)tx=C.x;ty=VH*.63;}
 if(!pair&&t>9&&t<13)ty=VH*.67;
 Input.keys.a=player.x>tx+3;Input.keys.d=player.x<tx-3;Input.keys.w=player.y>ty+4;Input.keys.s=player.y<ty-4;
 Input.keys.j=fire;Input.keys.c=fire&&!!target;
 if(fire&&target&&run.bombs>0&&t-(A.lastMissile??-20)>1.6){Input.injectTap('k');A.lastMissile=t;}
 }'''+script[j:]
script=script.replace("cfg.name+' / FURIOUS / GOD BOT / NATIVE HP & PHASES / '+elapsed.toFixed(1)+'s'","cfg.name+' / FURIOUS / NATIVE INPUTS / INVULNERABLE OBSERVER'")
i=script.index(" diffKey='furious';debugUnlocked=true;");j=script.index(' return {entry,difficulty:',i);script=script[:i]+" const entry={stage:6,role:'enemy',kind:cfg.kind};window.reviewConfig=cfg;setState(GS.PLAY);if(curStage.music)Audio.startMusic(curStage.music);\n"+script[j:]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None);p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(6,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(CA111_ART.banks).every(b=>XART.rdy(b.key))&&Object.values(CC111_ART.banks).every(b=>XART.rdy(b.key))}',timeout=180000)
 cuts=[];rawPath=W/('capture-'+str(int(time.time()))+'.webm')
 with rawPath.open('wb')as raw:
  p.expose_function('saveCaptureChunk',lambda s:raw.write(base64.b64decode(s)))
  for idx,(kind,title)in enumerate(CASES):
   p.evaluate(SETUP,kind);p.evaluate('''()=>{player.invuln=40002;DBGT.god=true;DBGT.speed=1;run.weapon=0;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=12;Input.mouse.active=false;window.caseStarted=performance.now();drawWorld(0);if(window.reviewBot){reviewBot.hullAt=null;reviewBot.lastMissile=-20;}}''')
   if idx==0:
    p.evaluate('()=>{window.savedRAF=window.__bofPendingRAF;requestAnimationFrame=window.__bofRealRAF;window.__bofPendingRAF=null;}');p.evaluate(script,dict(name=title,kind=kind,stage=6,role='enemy'));p.evaluate('()=>{if(window.savedRAF)requestAnimationFrame(window.savedRAF);window.savedRAF=null;}')
   else:p.evaluate('q=>{reviewConfig.name=q[0];reviewConfig.kind=q[1]}',[title,kind])
   start=p.evaluate('(performance.now()-captureStart)/1000');trace=[];doneAt=None;print('START',kind,flush=True)
   while True:
    p.wait_for_timeout(400);q=p.evaluate('()=>({seconds:(performance.now()-captureStart)/1000,elapsed:(performance.now()-caseStarted)/1000,frames:__bofFrames,state,playerDead:player.dead,completed:[...CA111.completed],pair:CC111.carriers.map(c=>({id:c.id,hp:c.hp,maxhp:c.maxhp,phase:c.phase,hullOpen:c.hullOpen,entry:c.entry,x:c.x,y:c.y,bays:c.parts.map(e=>({hp:e.hp,frame:e._sc12Frame,phase:e._sc12Phase}))})),actors:CA111.actors.map(e=>({id:e._ca111.id,role:e._ca111.role,kind:e._ca111.kind,hp:e.hp,maxhp:e.maxhp,phase:e._ca111.phase,frame:e._ca111.frame,x:e.x,y:e.y})),fx:CA111.fx.map(f=>({kind:f.kind,frame:ca111FXFrame(f),harmful:f.harmful}))})');trace.append(q)
    if 'test-'+kind in q['completed']and doneAt is None:doneAt=q['elapsed']
    if len(trace)%30==0:print('PROGRESS',kind,round(q['elapsed'],1),'pairHP',sum(c['hp']for c in q['pair']),'strategicHP',sum(c['hp']for c in q['actors']if c['role']=='carrier'),flush=True)
    if doneAt is not None and q['elapsed']-doneAt>1.2 or q['elapsed']>100 or errors:break
   end=p.evaluate('(performance.now()-captureStart)/1000');details=p.evaluate('()=>({events:CA111.events,pairedEvents:CC111.events,peak:captureStats.peak,playing:{...captureStats.playing},god:DBGT.god})');cut=dict(id=kind,title=title,start=start,end=end,timeline=trace,details=details,completed=doneAt is not None,errors=list(errors),sourceHashes=hashes,method=__doc__);cuts.append(cut);(W/(kind+'.json')).write_text(json.dumps(cut,indent=2));print('CUT',kind,round(end-start,1),'completed',cut['completed'],'events',len(details['events']),'paired',len(details['pairedEvents']),flush=True);assert not errors,errors
  stats=p.evaluate('async()=>{await new Promise(r=>{reviewRecorder.onstop=r;reviewRecorder.stop()});await capturePending;captureLive=false;return {...captureStats,botErrors:reviewBot.errors};}')
 group=dict(cuts=cuts,stats=stats,errors=errors);(W/('report.json'if len(CASES)==4 else'report-partial.json')).write_text(json.dumps(group,indent=2));p.close();b.close()
 for cut in cuts:
  out=W/(cut['id']+'.mp4');subprocess.run([ff,'-y','-ss',str(cut['start']),'-i',str(rawPath),'-t',str(cut['end']-cut['start']),'-vf','fps=30','-c:v','libx264','-preset','veryfast','-crf','25','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)],stdout=subprocess.DEVNULL,stderr=(W/'encode.log').open('w'),check=True);subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
print('Recorded and decoded',len(cuts),'native films; completed',sum(c['completed']for c in cuts),flush=True);assert hashes=={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in files},'Production changed during recording'
