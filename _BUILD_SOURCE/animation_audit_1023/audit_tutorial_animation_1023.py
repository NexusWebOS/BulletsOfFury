from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys,base64,io,numpy as np
R=Path(__file__).resolve().parents[2];W=R/'_shots/animation_audit_1023';W.mkdir(parents=True,exist_ok=True);O=W/'tutorial-native';O.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[];port,stop=shoot.serve(str(R))
def im(s):return np.array(Image.open(io.BytesIO(base64.b64decode(s))).convert('RGB')).astype(int)
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(Path(__file__).parent/'animation_enemy_lab_1023.js'))
  for diff in ['normal','hard','furious','easy']:
   p.evaluate('''d=>{EA11.setup(1,d);tutStart({stage:1,lead:'cole',disp:'cole'});BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=null;setState(GS.PLAY);TUT.card=false;TUT.i=TUT_LESSONS.findIndex(q=>q.id==='exam')-1;tutNext();TUT.L.wave=2;sg20ExamWave(TUT.L);window.TB23=TUT.L.bob;camX=worldWidth()/2-viewW()/2;player.invuln=40002;}''',diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&Object.values(IC20_ART.parts).map(p=>XART.rdy(p.key)).every(Boolean);}')
   for part in ['missile','cannon','core']:
    p.evaluate('part=>{E=TB23.parts[part];for(const e of Object.values(TB23.parts))e.flash=0;}',part);normal=im(p.evaluate('AQ23.draw(E).image'));hit=p.evaluate('()=>AQ23.hit(E)');after=im(hit['native']['image']);bright=int(((normal.max(2)>12)&(after.mean(2)-normal.mean(2)>20)).sum());rows.append({'difficulty':diff,'part':part,'phase':'pods-protect-reactor','hpBefore':hit['hpBefore'],'hpAfter':hit['hpAfter'],'timer':hit['timer'],'brightPixels':bright})
   trace=p.evaluate('''()=>{let peak=0,ground=0;const cues=new Set();AQ23.current={bob:true};AQ23.cue.clear();for(let i=0;i<1200;i++){player.invuln=40002;pBullets=[];updatePlay(1/60);peak=Math.max(peak,eBullets.length);ground=Math.max(ground,groundTargetingFx.length);if(i%6===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}}return{peakProjectiles:peak,peakGroundWarnings:ground,cues:[...AQ23.cue.keys()],state,lesson:TUT.L.def.id};}''');rows.append({'difficulty':diff,'kind':'native-attacks',**trace});p.screenshot(path=str(O/f'{diff}-bob-live.png'))
   p.evaluate('''()=>{for(const id of ['missile','cannon']){const e=TB23.parts[id];_dmgBullet={kind:'mg',lv:1,x:e.x,y:e.y};hitEnemy(e,10000);}E=TB23.parts.core;E.flash=0;_dmgBullet=null;}''');normal=im(p.evaluate('AQ23.draw(E).image'));hit=p.evaluate('()=>AQ23.hit(E)');after=im(hit['native']['image']);rows.append({'difficulty':diff,'part':'core','phase':'exposed-after-both-pods','hpBefore':hit['hpBefore'],'hpAfter':hit['hpAfter'],'brightPixels':int(((normal.max(2)>12)&(after.mean(2)-normal.mean(2)>20)).sum())});print(json.dumps({'difficulty':diff,'projectiles':trace['peakProjectiles'],'ground':trace['peakGroundWarnings'],'rows':len(rows)}),flush=True);p.evaluate('()=>{tutCleanup();TUT=null;}')
  br.close()
finally:stop();(O/'report.json').write_text(json.dumps({'cases':rows,'errors':errors},indent=2))
