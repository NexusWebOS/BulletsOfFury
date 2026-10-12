"""All nine stage rosters in real Chromium; bounded fixtures, not human clears."""
from pathlib import Path
import json,base64,subprocess,sys,html
from playwright.sync_api import sync_playwright
import imageio_ffmpeg
import shoot
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/enemy_behaviour_1011';OUT.mkdir(exist_ok=True)
rows=[];errors=[];checks=[];shots=[];videos=[];port,stop=shoot.serve(str(ROOT))
REPORT=OUT/('matrix-report.json' if '--matrix-only' in sys.argv else 'native-report.json')
if '--videos-only' in sys.argv:
 prior=json.loads((OUT/'native-report.json').read_text());rows=prior['rows']
 checks=[q for q in prior['checks'] if not q['name'].endswith('gameplay video encodes')]
def check(name,ok,data=None):
 checks.append({'name':name,'pass':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
def save():
 REPORT.write_text(json.dumps({'checks':checks,'rows':rows,'errors':errors,'shots':shots,'videos':videos},indent=2))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required','--mute-audio'])
  p=br.new_page(viewport={'width':1280,'height':1000});p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.add_script_tag(path=str(ROOT/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  def setup(stage,diff):
   p.evaluate('([s,d])=>EA11.setup(s,d)',[stage,diff])
   p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(run.stage).ready;}',polling=50)
  def snapshot(name):
   p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);drawHUD();}')
   (OUT/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')));shots.append(name+'.png')
  rosters={}
  for stage in ([] if '--videos-only' in sys.argv else range(1,10)):
   setup(stage,'normal');rosters[stage]=p.evaluate('EA11.collect()')
   for diff in ['normal','hard','furious']:
    setup(stage,diff);p.evaluate('()=>{stagePlan=[];aiQueue=[];}')
    for spec in rosters[stage]:
     p.evaluate('(s)=>EA11.case(s)',spec);q=None
     for _ in range(16):
      q=p.evaluate('EA11.step(60)');p.wait_for_timeout(1)
      if q and q.get('dead'):break
     if q:rows.append({'stage':stage,'diff':diff,'spec':spec,**q})
    own=[q for q in rows if q['stage']==stage and q['diff']==diff]
    check(f'Stage {stage} {diff}: all {len(own)} roster variants remain finite',len(own)==len(rosters[stage]) and all(q.get('finite') for q in own))
    check(f'Stage {stage} {diff}: actual projectiles or beams are released',sum(q.get('shots',0)+q.get('beams',0)+q.get('ground',0) for q in own)>0)
    print('STAGE',stage,diff,'shots',sum(q.get('shots',0) for q in own),'silent',[(q['type'],round(q.get('visible',0),1)) for q in own if not(q.get('shots') or q.get('beams') or q.get('ground') or q.get('ram') or q.get('support'))],flush=True);save()
  for diff in ['normal','hard','furious']:
   for stage,kind in [(2,'firejet1002'),(4,'s4heavyjet'),(6,'s6dart'),(8,'s8spread')]:
    q=next(q for q in rows if q['stage']==stage and q['diff']==diff and q['type']==kind)
    check(f'{diff}: repaired {kind} fires in the actual enemy loop',q.get('shots',0)>0,q.get('shots'))
  silent=[{'stage':q['stage'],'diff':q['diff'],'type':q['type']} for q in rows if not (q.get('shots') or q.get('beams') or q.get('ground') or q.get('ram') or q.get('support')) and q['type'] not in ['cometsm','mm1003_hellhugger']]
  check('Every armed roster variant attacks; gunless units retain contact/support roles',not silent,silent)
  for stage in range(1,10):
   counts=[sum(q.get('shots',0)+q.get('beams',0)+q.get('ground',0) for q in rows if q['stage']==stage and q['diff']==d) for d in ['normal','hard','furious']]
   check(f'Stage {stage}: delivered attack output increases on both difficulty steps',counts[0]<counts[1]<counts[2],counts)
  # Camera edges and simultaneous warning caps are native updatePlay tests.
  for diff,cap in [('normal',2),('hard',2),('furious',3)]:
   setup(6,diff)
   p.evaluate('()=>{stagePlan=[];aiQueue=[];enemies=[];s6Wing=null;for(let i=0;i<5;i++){spawnEnemy("s6lancer",camLeftX()+50+i*(viewW()-100)/4,95,{inPlace:true});}window.E=enemies[0];window.MAXBUSY=0;}')
   for _ in range(8):
    p.evaluate('''()=>{for(let i=0;i<60;i++){updatePlay(1/60);MAXBUSY=Math.max(MAXBUSY,enemies.filter(e=>{const q=eb11Queue(e);return q?._eb11?.started&&!q.fired;}).length);}}''');p.wait_for_timeout(5)
   check(diff+': native wave respects concurrent warning cap',p.evaluate('MAXBUSY')<=cap,p.evaluate('MAXBUSY'))
  # Record natural authored wave excerpts. Invulnerability/no player fire make
  # the enemy behavior visible; this does not claim a survival/balance clear.
  for stage in ([] if '--matrix-only' in sys.argv else range(1,10)):
   for diff in ['normal','furious']:
    setup(stage,diff)
    p.evaluate('()=>{run.weapon=0;run.wlevels=[1,1,1,1,1,1,0,0,0];run.wlevel=1;stageTimer=0;waveIdx=0;spawnClock=0;mapScroll=0;aiQueue=[];window.E=null;}')
    if stage==8:p.evaluate('()=>{run._l78Entry=0;l78entry=null;}')
    # Let the opening wave arrive before recording its fighting window.
    p.evaluate('''()=>{for(let i=0;i<180;i++){player.invuln=40002;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}''');p.wait_for_timeout(80)
    name=f'stage-{stage}-{diff}'
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-f','image2pipe','-vcodec','mjpeg','-r','20','-i','pipe:0','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(OUT/(name+'.mp4'))]
    writer=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for frame in range(160):
     p.evaluate('''()=>{for(let i=0;i<3;i++){player.invuln=40002;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}drawHUD();}''')
     if frame in [55,110]:snapshot(name+'-'+str(frame))
     writer.stdin.write(base64.b64decode(p.evaluate('cv.toDataURL("image/jpeg",.88).split(",")[1]')))
     if frame%10==0:p.wait_for_timeout(5)
    writer.stdin.close();writer.wait();videos.append(name+'.mp4');check(name+' gameplay video encodes',writer.returncode==0);save()
  check('No browser page, console, or asset errors',not errors,errors)
  br.close()
finally:stop()
save()
if '--matrix-only' in sys.argv:
 sys.exit(1 if errors or any(not q['pass'] for q in checks) else 0)
blocks=[]
for stage in range(1,10):
 clips=''.join(f'<figure><figcaption>{diff.upper()}</figcaption><video controls muted loop preload="metadata" src="stage-{stage}-{diff}.mp4" poster="stage-{stage}-{diff}-110.png"></video></figure>' for diff in ['normal','furious'])
 blocks.append(f'<section><h2>Level {stage}</h2><div class="pair">{clips}</div></section>')
(OUT/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Enemy behavior — levels 1–9</title>
<style>body{background:#07111c;color:#dcecff;font:16px system-ui;max-width:1300px;margin:36px auto;padding:0 20px}h1{color:#9cf2bb}p{max-width:900px;line-height:1.5}.pair{display:flex;gap:18px}figure{margin:0;flex:1;min-width:0}video{width:100%;background:#000;border:1px solid #314b65}figcaption{padding:8px}section{margin:40px 0}a{color:#8ed8ff}</style>
<h1>Enemy behavior • Levels 1–9</h1><p>Enemies establish a visible warning, commit their native attack, recover and move on. Hard has shorter recoveries; Furious adds alternate double bursts and more attack cycles. The small fire/ice kamikazes remain shieldless.</p>
<p>Recorded from the real game. These are eight-second authored opening-wave excerpts with an invulnerable observer and no player firing, for attack/visual review. The separate roster matrix exercises every collected wave variant on Normal, Hard and Furious; these clips are not human survival clears.</p>
<p><a href="native-report.json">Roster measurements</a> · <a href="commitments.json">Collision, dodge, camera and co-op checks</a></p>
<section><h2>Late alien fleet — committed attacks</h2><p>Furious: the side-entry ship reaches a visible firing lane. The other ship holds its attack pocket instead of drifting underneath the pilot.</p><video controls muted loop preload="metadata" src="late-alien-commitments.mp4" poster="late-alien-90.png" style="max-width:720px"></video></section>'''+''.join(blocks),encoding='utf-8')
if errors or any(not q['pass'] for q in checks):sys.exit(1)
