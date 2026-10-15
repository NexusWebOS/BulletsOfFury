from pathlib import Path
import sys,json,math
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
D=R/'assets/data/enemy_atlas_1013.json';O=R/'_shots/enemy_atlas_independent_1013';O.mkdir(parents=True,exist_ok=True)
entries={e['id']:e for e in json.loads(D.read_text(encoding='utf8'))['entries']};rows=[];errors=[];port,stop=shoot.serve(str(R))
READ='''()=>({clock:ht27Data()?.clock,mode:ht27Data()?.mode,state:boss?._hammer?.state,t:stateT,x:boss?.x,y:boss?.y,frames:BOF_ATLAS_CLOCK.frames,paused:BOF_ATLAS_CLOCK.paused,soundPaused:ht27Song()?.paused,soundTime:ht27Song()?.currentTime,soundRate:ht27Song()?.playbackRate,locked:ht27Locked()})'''
ADVANCE='''async speed=>{const c=BOF_ATLAS_CLOCK,base=c.after,n=c.frames,t=ht27Data().clock,wall=performance.now();return await new Promise(resolve=>{c.after=()=>{base();if(c.frames>=n+24){BOF_ENEMY_ATLAS.pause(true);c.after=base;resolve({delta:ht27Data().clock-t,wall:(performance.now()-wall)/1000,frames:c.frames-n,soundRate:ht27Song().playbackRate});}};BOF_ENEMY_ATLAS.speed(speed);BOF_ENEMY_ATLAS.pause(false);});}'''
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio'])
  for code in ['HAMMER','HAMA']:
   p=browser.new_page(viewport={'width':900,'height':900});p.on('pageerror',lambda e:errors.append(str(e)))
   # Simulate rejected autoplay for HAMA; only the browser media-play promise is blocked.
   if code=='HAMA':p.add_init_script("HTMLMediaElement.prototype.play=function(){return Promise.reject(new DOMException('QA autoplay denied','NotAllowedError'));}")
   p.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1&enemyAtlas=1',timeout=120000);p.wait_for_function('window.BOF_ENEMY_ATLAS?.ready&&window.__bofFrames>4',timeout=90000)
   start=p.evaluate('e=>BOF_ENEMY_ATLAS.start(e,"normal")',entries['bof-password-'+code]);assert not start.get('error'),start
   p.wait_for_function('ht27Data()?.musicStarted&&ht27Data().clock>.1',timeout=60000)
   p.evaluate('BOF_ENEMY_ATLAS.pause(true)');before=p.evaluate(READ);p.wait_for_timeout(400);paused=p.evaluate(READ)
   assert paused==before,(before,paused)
   p.evaluate('BOF_ENEMY_ATLAS.step()');p.wait_for_function('n=>BOF_ATLAS_CLOCK.frames===n+1',arg=before['frames'],polling=25);stepped=p.evaluate(READ)
   assert abs(stepped['clock']-before['clock']-1/60)<1e-7 and stepped['paused'] and stepped['soundPaused'],stepped
   normal=p.evaluate(ADVANCE,1);fast=p.evaluate(ADVANCE,2)
   ratio=(fast['delta']/fast['wall'])/(normal['delta']/normal['wall'])
   assert 1.6<ratio<2.4,(normal,fast,ratio)
   p.evaluate('BOF_ENEMY_ATLAS.mute(false)');sound=p.evaluate(ADVANCE,2);assert sound['soundRate']==2,sound
   p.evaluate('BOF_ENEMY_ATLAS.mute(true);BOF_ENEMY_ATLAS.speed(1);BOF_ENEMY_ATLAS.pause(true)');p.evaluate(shoot.TRAP_RAF)
   p.evaluate('''()=>{window.auditModes=new Set();window.auditKinds=new Set();window.auditPhysical=0;window.auditPaint=0;const base=hammerBossDraw;hammerBossDraw=function(){auditPaint++;return base.apply(this,arguments);};window.__qaTick=()=>{if(boss?._hammer){const h=boss._hammer;auditModes.add(h.state);if(h.throw||h.bombs?.length||h.pillars?.length||['spin','leap','throw','whirlwind'].includes(h.state))auditPhysical++;}for(const q of eBullets)if(!q.dead)auditKinds.add(q.kind);BOF_ATLAS_CLOCK.after();};}''')
   p.evaluate('window.__bofStepNow=last');simulatedStart=p.evaluate(READ)
   for n in range(40):
    err=p.evaluate(shoot.STEP,60);assert not err,err
    if n in [10,25,39]:p.screenshot(path=str(O/f'{code}-clock-verified-{n}.png'))
   final=p.evaluate(READ)
   combat=p.evaluate('()=>({modes:[...auditModes],kinds:[...auditKinds],physicalFrames:auditPhysical,paintCalls:auditPaint,radio:fb2IntroActive(),snapshot:BOF_ENEMY_ATLAS.snapshot()})')
   row=dict(code=code,autoplayRejected=code=='HAMA',start=start,paused=paused,stepped=stepped,normal=normal,fast=fast,speedRatio=ratio,audioRate=sound['soundRate'],simulatedStart=simulatedStart,final=final,combat=combat);rows.append(row)
   (O/'hammer_clock_verification.json').write_text(json.dumps({'rows':rows,'errors':errors},indent=2),encoding='utf8')
   assert abs(final['clock']-simulatedStart['clock']-40)<.025,(final,simulatedStart)
   assert final['mode']!='intro' and combat['physicalFrames']>0 and len(combat['modes'])>3 and combat['paintCalls']>0 and not combat['radio'],row
   print(code,{'clock':final['clock'],'speedRatio':ratio,'modes':combat['modes'],'physicalFrames':combat['physicalFrames'],'paintCalls':combat['paintCalls']},flush=True);p.close()
  browser.close()
finally:stop()
assert not errors,errors
print('PASS HAMMER/HAMA pause, single-frame, double-speed, soundtrack rate, blocked autoplay, 40-second native combat')
