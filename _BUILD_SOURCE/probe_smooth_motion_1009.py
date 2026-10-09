"""Real Chromium verification for defeat order, replacement reels and facing."""
from pathlib import Path
import sys,json,base64,subprocess
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/smooth_motion_1009';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];port,stop=shoot.serve(str(ROOT))
def check(name,ok,data=None):checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':900});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status} {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.add_script_tag(content=(ROOT/'_BUILD_SOURCE/balance_lab_1007.js').read_text())
  p.evaluate('()=>{sm10Warm(Object.keys(SM10_ART));fb1002Warm();furyShipWarm();}')
  p.wait_for_function('()=>Object.values(SM10_ART).flat().every(a=>XART.rdy(a.key))&&furyShipReady()',polling=50)
  p.evaluate('()=>BAL7.setup({stage:5,kind:"chromehammer",pilot:"yuri",diff:"furious",seconds:60,fire:false})')
  for _ in range(2000):
   if p.evaluate('()=>{stageLoadTick();return stageLoadInfo(5).ready;}'):break
   p.wait_for_timeout(20)
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;B.dead=true;B.dying=0;h3EndingStart(B);}')
  check('Last words begin before death clock',p.evaluate('H3.ending.phase==="lastWords"&&B.dying===0&&H3.ending.engineDeath==null'))
  folder=OUT/'hammer-farewell';folder.mkdir(exist_ok=True);phases={};white_samples=[];white_capture=None
  for i in range(22*15):
   p.evaluate('()=>{for(let i=0;i<4;i++)h3EndingTick(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
   data=p.evaluate('({phase:H3.ending?.sm10?.phase,portrait:H3.ending?.sm10?.portrait,line:H3.ending?.sm10?.line,dying:B.dying})')
   if data['phase'] not in phases:
    phases[data['phase']]=i/15;(OUT/(f'farewell-{data["phase"]}.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
   if data.get('portrait',0)>.95:white_samples.append(data)
   if data.get('portrait',0)>.99 and white_capture is None:
    white_capture=OUT/'farewell-white-complete.png';white_capture.write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
   (folder/f'{i:04d}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));p.wait_for_timeout(5)
  subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-framerate','15','-i',str(folder/'%04d.png'),'-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(OUT/'hammer-farewell.mp4')],check=True)
  check('Portrait fades white, box out, lock, missile, then death',list(phases)==['words','portraitWhite','windowOut','lock','missile','death'] and bool(white_samples),phases)
  # Actual portrait pixels in the native dialogue box, not only its fade timer.
  rgb=np.array(Image.open(white_capture).convert('RGB').crop((88,770,198,877))).astype(int);mask=np.max(rgb,axis=2)>80
  check('Farewell portrait visibly reaches white',bool(mask.any()) and float(np.mean(np.ptp(rgb[mask],axis=1)<5))>.95)
  check('One missile impact causes nine sequential electrical pops',p.evaluate('()=>SM10.events.filter(q=>q.event==="hammer-core-impact").length===1&&SM10.events.filter(q=>q.event==="hammer-electrical-pop").length===9'),p.evaluate('SM10.events'))
  check('Cutaway follows completed eight-second in-game death',p.evaluate('H3.ending.engineDeath==null&&["overhead","surface"].includes(H3.ending.phase)'),p.evaluate('H3.ending.phase'))
  for stage,types in [(2,['disc','eye']),(3,['s3mine','s3interceptor'])]:
   p.evaluate('(n)=>{H3.ending=null;beginStage(n);setState(GS.PLAY);story=null;BOFCinematicDirector.cancel();}',stage)
   for unit in types:
    p.evaluate('(type)=>{enemies=[];spawnEnemy(type,240,220);window.E=enemies.at(-1);E.t=0;E.x=240;E.y=220;}',unit)
    cells=[]
    for f in range(8):
     q=p.evaluate('(f)=>{E.t=(f+.01)/12;E.flash=0;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);return cv.toDataURL().split(",")[1];}',f);cells.append(q)
    check(unit+' eight native frames, hitbox/HP preserved',len(set(cells))==8 and p.evaluate('E.maxhp>0&&E._sm10Frame===7'))
    (OUT/(unit+'-native.png')).write_bytes(base64.b64decode(cells[2]))
    p.evaluate('E.flash=.12');p.evaluate('drawEnemy(E)');(OUT/(unit+'-white.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  p.evaluate('()=>{beginStage(6);setState(GS.PLAY);story=null;BOFCinematicDirector.cancel();}')
  for direction in ['south','east','west','north']:
   p.evaluate('(direction)=>{window.E=fb2FlightSpawn({direction,role:"red",x:240,y:220});E.x=240;E.y=220;E.spin=Math.PI;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);}',direction)
   check('Strike facing '+direction+' survives contrary transient spin',p.evaluate('(dir)=>E._sm10Facing===dir',direction))
   (OUT/('fighter-'+direction+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
  p.evaluate('missionWarm()');p.wait_for_function('XART.rdy(MISSION29_ART.bluejets.key)',polling=50)
  # East/west mission lanes deliberately become green bombers; only vertical
  # unarmed gate lanes are blue in the authored encounter specification.
  for direction in ['south','north']:
   # A real blue unarmed gate actor must not pick the bomber palette fallback.
   p.evaluate('(direction)=>{enemies=[];spawnEnemy("s6probe",240,220);window.E=enemies.at(-1);E.x=240;E.y=220;E._mission29={kind:"gate",direction,n:0,attack:0};E._fb2Stealth=null;E._s6Strike=null;E._s67Draw=104;E.spin=Math.PI;E.flash=0;ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);}',direction)
   actual=p.evaluate('()=>cv.toDataURL()');(OUT/('blue-fighter-'+direction+'.png')).write_bytes(base64.b64decode(actual.split(',')[1]))
   expected=p.evaluate('(dir)=>{ctx.clearRect(0,0,cv.width,cv.height);ctx.save();ctx.translate(E.x,E.y);if(dir==="north")ctx.rotate(Math.PI);missionCell("bluejets",dir==="east"?0:dir==="west"?1:2,-52,-52,104,104);ctx.restore();return cv.toDataURL();}',direction)
   check('Blue fighter '+direction+' uses correct native cell despite stale spin',actual==expected and p.evaluate('!on5Bomber(E)&&fb2MissionRole(E._mission29)==null'))
  br.close()
finally:stop()
check('No page, console or asset errors',not errors,errors)
result={'passed':sum(q['pass'] for q in checks),'failed':[q for q in checks if not q['pass']],'errors':errors,'checks':checks}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'errors':errors}),flush=True)
if result['failed'] or errors:sys.exit(1)
