from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html?quality=high');p.wait_for_function('window.__bofFrames>5',timeout=180000);p.evaluate(shoot.TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  rows=[]
  for lv in [1,3,5]:
   for weapon in [0,4]:
    q=p.evaluate('''([lv,w])=>{EA11.setup(1,'normal');run.pilot='axel';pilotIndex=0;PILOTMOD={...PILOTS[0]};run.weapon=w;run.wlevel=lv;run.wlevels=WEAPONS.map(()=>lv);run.wvars=run.wvars||[];run.wvars[4]='flamethrower';run.missileLevel=0;
     stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;player.x=worldWidth()/2;player.y=430;Input.mouse.active=false;
     const e=spawnEnemy('assault',player.x,310,{pattern:'straight'});e.hp=e.maxhp=100000;e._esh=null;e.shoots=e.armed=false;
     const down=Input.down;Input.down=function(k){return keybind.fire.includes(k)||down.call(Input,k);};let hp=0;
     try{for(let i=0;i<360;i++){e.x=player.x;e.y=310;e.fireCd=999;e.vx=e.vy=0;player.invuln=999;updatePlay(1/60);if(i===119)hp=e.hp;}}
     finally{Input.down=down;}
     return {lv,weapon:w,target:e.type,damage:hp-e.hp,seconds:4,dps:(hp-e.hp)/4,hp:e.hp,remainingShots:pBullets.length,finite:Number.isFinite(e.hp),burn:e._burn||0};}''',[lv,weapon])
    rows.append(q);print(json.dumps(q),flush=True)
  (W/'weapon-damage.json').write_text(json.dumps(rows,indent=2),encoding='utf8');b.close()
finally:stop()
