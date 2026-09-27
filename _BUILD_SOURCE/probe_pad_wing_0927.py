"""Native reload and frozen-encounter clock checks. Gamepad hardware is simulated."""
from pathlib import Path
import json, http.server
import shoot as sh
from playwright.sync_api import sync_playwright
OUT=Path('_shots/overnight_0927');errors=[];report={'pad':[]}
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=sh.serve(sh.GAME)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1000,'height':1050})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
  for button in [2,5]:
   p.evaluate("i=>{keybind.fire=['j','pad_b'+i];keybind.charge=['h','pad_b4'];saveKeybind();}",button)
   p.reload(wait_until='load');p.wait_for_function('()=>window.__bofFrames>5');p.evaluate(sh.TRAP_RAF)
   report['pad'].append(p.evaluate("""i=>{run.mode='arcade';run.pilot='cole';beginStage(5);setState(GS.PLAY);player.reset();player.invuln=999;story=null;stagePlan=[];spawnClock=9999;special=null;run.spaceWeapon=0;run._spaceVolleyCd=999;run.sonicT=run.dkT=0;pBullets=[];
    const pad={id:'8BitDo M30 raw-button simulation',index:2,connected:true,mapping:'',axes:[0,0],buttons:Array.from({length:16},()=>({pressed:false,value:0}))};navigator.getGamepads=()=>[null,null,pad];pad.buttons[i]={pressed:true,value:1};Input.pollGamepad();
    for(let f=0;f<30;f++)updatePlay(1/60);const shots=pBullets.length;
    navigator.getGamepads=()=>[];Input.pollGamepad();const disconnected=!Input.down('pad_b'+i);
    navigator.getGamepads=()=>[null,pad];Input.pollGamepad();const reconnected=Input.down('pad_b'+i);pad.buttons[i].pressed=false;Input.pollGamepad();
    return {button:i,restored:keybind.fire.includes('pad_b'+i),shots,disconnected,reconnected,released:!Input.down('pad_b'+i)};}""",button))
  report['wing']=p.evaluate("""()=>{diffKey='normal';DIFF=DIFFS.normal;beginStage(6);setState(GS.PLAY);player.reset();player.invuln=999;story=null;s6Opening=null;stagePlan=[];spawnClock=9999;enemies=[];pBullets=[];eBullets=[];spawnSubBoss__inner('tempestbrothers');stageTimer=34;s6WingLaunch(2,false);s6Wing.beats=1;const seen=new WeakSet(),missiles={};let defenses=0;
    for(let i=0;i<2400;i++){player.invuln=999;updatePlay(1/60);for(const q of pBullets)if(q.ally&&q.kind==='missile'&&!seen.has(q)){seen.add(q);missiles[q._wingKey]=(missiles[q._wingKey]||0)+1;}defenses+=s6Wing.ships.filter(q=>q.dodgeT>0).length;}
    return {stageTimer,combatTime:s6Wing.combatTime,missiles,defenseFrames:defenses,ships:s6Wing.ships.map(q=>({key:q.key,missileCd:q.missileCd,rollCool:q.rollCool,somerCool:q.somerCool}))};}""")
  br.close()
finally:stop()
report['errors']=errors;(OUT/'pad-wing.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
assert not errors,errors
assert all(r['restored'] and r['shots']>0 and r['disconnected'] and r['reconnected'] and r['released'] for r in report['pad'])
assert report['wing']['stageTimer']==34 and report['wing']['combatTime']>=39.9
assert sum(report['wing']['missiles'].values())>=8
