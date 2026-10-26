"""Real Chromium pixel checks and direct-canvas video capture for the motion study."""
from pathlib import Path
import json,hashlib,sys,base64,subprocess
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];A=R/'art-packs/raiden-components-1024';O=R/'_shots/raiden_animation_1025';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail));print(('PASS 'if ok else'FAIL ')+name,flush=True)
STATS='''()=>{const c=document.querySelector('#motion-stage'),a=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let hash=2166136261,white=0;for(let i=0;i<a.length;i++){hash=Math.imul(hash^a[i],16777619)>>>0;if(i%4===0&&a[i]>245&&a[i+1]>245&&a[i+2]>245)white++;}return{hash,white};}'''
basepaths=['assets/game.js','_BUILD_SOURCE/test_fl.js','index.html','art-packs/raiden-components-1024/manifest.json'];baseline={s:hashlib.sha256((R/s).read_bytes()).hexdigest()for s in basepaths}
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport={'width':1440,'height':1120});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda e:errors.append(e.text)if e.type=='error'else None)
  p.goto(f'http://127.0.0.1:{port}/art-packs/raiden-components-1024/animation.html');p.evaluate('async()=>await MotionPreview.ready');p.evaluate('MotionPreview.play(false)')
  p.evaluate('MotionPreview.renderAt(2.8)');snap=p.evaluate('MotionPreview.snapshot()');p.screenshot(path=str(O/'desktop.png'),full_page=True);p.locator('#motion-stage').screenshot(path=str(O/'overview.png'))
  check('Six matched machines render with actual rolling gear, exhaust and ordnance',len(snap['units'])==6 and snap['rolling']>10 and snap['exhausts']>=4 and snap['shots']>0,snap)
  p.evaluate('MotionPreview.setAction("idle");MotionPreview.renderAt(1)');a=p.evaluate(STATS);p.evaluate('MotionPreview.renderAt(1.7)');check('Idle keeps complete matched assemblies stationary',p.evaluate(STATS)==a)
  p.evaluate('MotionPreview.setAction("travel");MotionPreview.renderAt(1)');a=p.evaluate(STATS);p.evaluate('MotionPreview.renderAt(1.13)');b=p.evaluate(STATS);check('Actual travel pixels animate',a!=b)
  p.evaluate('MotionPreview.setAction("attack");MotionPreview.renderAt(3.0)');a=p.evaluate(STATS);snap=p.evaluate('MotionPreview.snapshot()');check('Firing creates actual authored muzzle and projectile draws',snap['shots']>0)
  p.wait_for_timeout(170);check('Pause freezes the animation clock and pixels',p.evaluate(STATS)==a)
  p.click('#play');p.wait_for_timeout(220);check('Play resumes real pixel motion',p.evaluate(STATS)!=a);p.click('#play')
  p.evaluate('MotionPreview.setAction("travel");MotionPreview.setView("showcase","twin_cannon_tank");MotionPreview.renderAt(1.2)');a=p.evaluate(STATS);p.locator('#motion-stage').screenshot(path=str(O/'tank-tracks.png'));p.click('#belts');b=p.evaluate(STATS);snap=p.evaluate('MotionPreview.snapshot()')
  check('Track covers lift while separate road wheels continue rolling',a!=b and snap['rolling']>=10,snap);p.locator('#motion-stage').screenshot(path=str(O/'tank-wheels.png'));p.click('#belts')
  p.evaluate('MotionPreview.setAction("idle");MotionPreview.renderAt(4)');a=p.evaluate(STATS);p.click('#hit');h=p.evaluate(STATS);p.evaluate('MotionPreview.renderAt(4.2)');b=p.evaluate(STATS);check('Animated assembly visibly flashes and restores its original palette',h['white']>a['white'] and b==a)
  p.evaluate('MotionPreview.setAction("cycle")')
  for u in p.evaluate('FOUNDRY.units.map(u=>({id:u.id,tier:u.tier}))'):
   p.evaluate('(u)=>{MotionPreview.setView(u.tier,u.id);MotionPreview.renderAt(2.6)}',u);a=p.evaluate(STATS);p.evaluate('MotionPreview.renderAt(2.73)');b=p.evaluate(STATS);snap=p.evaluate('MotionPreview.snapshot()');check(u['id']+' matched assembly animates',a!=b and snap['parts']>0)
   if u['id']in ['wheeled_flak','violet_stealth_wing','iron_bastion_landship','stormwing_sky_carrier','dreadnought_battleship','quad_laser_citadel']:p.locator('#motion-stage').screenshot(path=str(O/(u['id']+'.png')))
  p.evaluate('MotionPreview.setView("enemy");MotionPreview.renderAt(2.5)');first=p.evaluate('MotionPreview.snapshot().units');p.click('#next');second=p.evaluate('MotionPreview.snapshot().units');check('Roster pagination exposes different animated machines',first!=second and len(second)==6)
  p.set_viewport_size({'width':390,'height':844});p.evaluate('MotionPreview.setView("showcase")');p.screenshot(path=str(O/'mobile.png'),full_page=True);check('Mobile controls and stage avoid horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'));p.set_viewport_size({'width':1440,'height':1120})
  if '--video'in sys.argv:
   import imageio_ffmpeg
   ff=imageio_ffmpeg.get_ffmpeg_exe();video=A/'animation-preview.mp4';p.evaluate('MotionPreview.play(false);MotionPreview.state.lift=false;MotionPreview.state.hitAt=-10;MotionPreview.setAction("cycle");MotionPreview.setView("showcase")')
   proc=subprocess.Popen([ff,'-y','-loglevel','error','-f','image2pipe','-vcodec','png','-r','24','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
   for i in range(28*24):
    sec=i/24
    if sec<8:view='showcase';page=0;t=sec
    elif sec<20:view='enemy';page=int((sec-8)//4);t=2+(sec-8)%4
    elif sec<24:view='miniboss';page=0;t=2+(sec-20)
    else:view='boss';page=0;t=2+(sec-24)
    png=p.evaluate('''([view,page,t])=>{if(MotionPreview.state.view!==view)MotionPreview.setView(view);MotionPreview.state.page=page;MotionPreview.renderAt(t);return document.querySelector('#motion-stage').toDataURL('image/png').split(',')[1];}''',[view,page,t]);proc.stdin.write(base64.b64decode(png))
    if i%96==0:print('VIDEO',round(sec,1),'of 28 seconds captured',flush=True)
   proc.stdin.close();check('Actual Chromium video capture encodes successfully',proc.wait()==0)
   result=subprocess.run([ff,'-y','-loglevel','error','-t','8','-i',str(video),'-filter_complex','[0:v]fps=12,scale=768:-1:flags=neighbor,split[v][p];[p]palettegen=stats_mode=diff:max_colors=128[pal];[v][pal]paletteuse=dither=none','-loop','0',str(A/'animation-preview.gif')],capture_output=True)
   check('Looping eight-second animated GIF exports',result.returncode==0,result.stderr.decode()[:200])
   result=subprocess.run([ff,'-v','error','-i',str(video),'-f','null','-'],capture_output=True);check('Full MP4 independently decodes without errors',result.returncode==0 and not result.stderr)
   subprocess.run([ff,'-y','-loglevel','error','-ss','3.0','-i',str(video),'-frames:v','1',str(O/'decoded-video.png')],check=True)
   (O/'video.json').write_text(json.dumps(dict(width=1280,height=800,fps=24,seconds=28,audio=False,overview_loop_seconds=8,mp4_bytes=video.stat().st_size,gif_bytes=(A/'animation-preview.gif').stat().st_size),indent=2)+'\n')
  browser.close()
finally:stop()
check('Shipping files and the approved matched catalog remain unchanged',all(hashlib.sha256((R/s).read_bytes()).hexdigest()==h for s,h in baseline.items()));check('No page or console errors',not errors,errors)
report=dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks),checks=checks);(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('FINAL SUMMARY',report['passed'],report['failed']);raise SystemExit(bool(report['failed']))
