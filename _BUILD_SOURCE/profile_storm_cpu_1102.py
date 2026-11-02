"""Sample the actual debug-fight path to locate the remaining frame-rate cost."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-renderer-backgrounding']);p=b.new_page(viewport={'width':1280,'height':800});p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(4,4)
 p.evaluate('''()=>{diffKey='furious';DIFF=difficultyForRun('arcade',diffKey);debugUnlocked=true;debugStartFight({stage:6,role:'mini',kind:'razorwake',name:'RAZORWAKE'},{pilot:'cole',record:false});spawnSubBoss('razorwake');debugFight.spawned=true;warnT=0;s6Opening=null;fb2Talk=fb2Intro=null;H3.release=false;story=null;BOFCinematicDirector.cancel();setState(GS.PLAY);DBGT.god=true;DBGT.speed=1;player.invuln=0;}''');p.wait_for_function('()=>{stageLoadTick();return fb112Ready()}',timeout=180000);p.wait_for_timeout(4000)
 c=p.context.new_cdp_session(p);c.send('Profiler.enable');c.send('Profiler.setSamplingInterval',{'interval':500});c.send('Profiler.start');a=p.evaluate('({t:performance.now(),f:__bofFrames})');p.wait_for_timeout(6000);z=p.evaluate('({t:performance.now(),f:__bofFrames})');profile=c.send('Profiler.stop')['profile'];p.screenshot(path=str(R/'_shots/furious_encounters_1102/cpu-profile.png'));b.close()
nodes={n['id']:n for n in profile['nodes']};counts={}
for sample,dt in zip(profile.get('samples',[]),profile.get('timeDeltas',[])):counts[sample]=counts.get(sample,0)+dt
rows=[dict(name=nodes[k]['callFrame']['functionName'],file=nodes[k]['callFrame']['url'].split('/')[-1],line=nodes[k]['callFrame']['lineNumber']+1,ms=v/1000)for k,v in sorted(counts.items(),key=lambda v:-v[1])[:30]]
out=dict(fps=(z['f']-a['f'])*1000/(z['t']-a['t']),top=rows);(R/'_shots/furious_encounters_1102/cpu-profile.json').write_text(json.dumps(out,indent=2));print(out)
