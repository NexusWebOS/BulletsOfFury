"""Player weapons/levels, 30/60/120 Hz presentation clocks, and death animation QA."""
from pathlib import Path
import json,sys,base64,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/projectiles_1007/pilots';O.mkdir(parents=True,exist_ok=True)
http.server.SimpleHTTPRequestHandler.log_message=lambda *a:None
port,stop=shoot.serve(str(R));report={'errors':[],'weapons':[],'clocks':[],'deaths':[]}
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--no-sandbox','--mute-audio']);p=br.new_page(viewport={'width':1100,'height':950});p.set_default_timeout(120000)
  p.route('**/*',lambda r:r.continue_() if r.request.url.startswith(('http://127.0.0.1:','data:','blob:')) else r.abort())
  p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('console',lambda m:report['errors'].append(m.text[:400]) if m.type=='error' and ('127.0.0.1' in m.text or 'ERR_' not in m.text) else None)
  def boot():
   p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('()=>window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
   for name in ['balance_lab_1007.js','projectile_lab_1007.js']:p.add_script_tag(path=str(R/'_BUILD_SOURCE'/name))
  boot()
  pilots=p.evaluate('()=>PILOTS.map(p=>p.key)')
  for diff in ['easy','normal','hard','furious']:
   # Every pilot/weapon, low/middle/max upgrade levels; same real firing input.
   for pilot in pilots:
    for level in [1,3,5]:
     for weapon in range(9 if pilot=='yuri' else 8):
      case={'stage':1,'kind':'damkeeper','diff':diff,'pilot':pilot,'level':level,'weapon':weapon,'id':f'{diff}-{pilot}-w{weapon}-L{level}'}
      p.evaluate("""c=>{AP7.begin(c);boss=null;bossActive=false;subBoss=null;subBossActive=false;bossDefeated=false;stagePlan=[];enemies=[];spawnClock=9999;run._autoLevelWeapons=null;
       // Arm a fresh shot without inheriting a held cooldown from a prior fixture.
       if(c.weapon===8){yuriLightningOrbUnlocked=true;run._earnedUnlocks={lightningOrb:true};}
       player.fireCd=0;player.roll=null;player.somer=null;run._chainHeat=0;run._chainOverheat=false;
       for(const k of keybindFor(1).fire||[])if(!k.startsWith('pad_'))Input.keys[k]=true;
       window.PAQ={shotKinds:{},seen:new WeakSet(),mounts:0,frames:0,geometry:[]};
      }""",case)
      for chunk in range(3):
       p.evaluate("""()=>{for(let i=0;i<40;i++){player.invuln=99999;updatePlay(1/60);PAQ.frames++;
        for(const b of pBullets)if(!PAQ.seen.has(b)){PAQ.seen.add(b);PAQ.shotKinds[b.kind]=(PAQ.shotKinds[b.kind]||0)+1;}
        if(i%4===0){ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/15);}
       }}""")
       p.wait_for_timeout(8)
      row=p.evaluate('()=>({shots:PAQ.shotKinds,keys:AP7.keys,geometry:AP7.geometry,effective:{weapon:run.weapon,level:run.wlevel},frames:PAQ.frames})');row['case']=case;report['weapons'].append(row)
      if diff=='normal' and pilot in ['yuri','maverick','falva'] and level==3:
       (O/(case['id']+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
    print('PILOT',diff,pilot,'cases',len(report['weapons']),flush=True)
    (O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
   boot()
  for diff in ['easy','normal','hard','furious']:
   for fps in [30,60,120]:
    p.evaluate("""c=>{AP7.begin({stage:1,kind:'damkeeper',diff:c.diff,pilot:'yuri',level:3,id:'clock'});boss=null;bossActive=false;enemies=[];eBullets=[];pBullets=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;
     window.pClock={kind:'mg',x:130,y:370,vx:0,vy:0,w:5,h:8,dmg:1,t:0,_visualAge:0};window.eClock={kind:'s8pair',x:190,y:220,vx:0,vy:0,w:8,h:8,t:0,_visualAge:0,life:10,_noArsenal:true};pBullets=[pClock];eBullets=[eClock];
     for(let n=0;n<c.fps;n++)updatePlay(1/c.fps);
    }""",{'diff':diff,'fps':fps})
    row=p.evaluate('()=>({player:pClock._visualAge,enemy:eClock._visualAge,playerDamageAge:pClock.t,enemyDamageAge:eClock.t,pFrame:projectileVisualFrame(pClock,12,8),eFrame:projectileVisualFrame(eClock,12,8)})');row.update(diff=diff,fps=fps);report['clocks'].append(row)
   for st in [1,5]:
    p.evaluate("""c=>{AP7.begin({stage:c.stage,kind:c.stage===5?'xenoregent':'damkeeper',diff:c.diff,pilot:'yuri',level:3,id:'death'});boss=null;bossActive=false;enemies=[];eBullets=[];pBullets=[];run.shield=0;player.invuln=0;playerHit('animation QA');window.DAQ=[];}""",{'stage':st,'diff':diff})
    for f in range(150):
     if f%6==0:
      p.evaluate('()=>{for(let i=0;i<6;i++)updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(.1);DAQ.push({spin:player._spin?{t:player._spin.t,crashed:player._spin.crashed,a:player._spin.a}:null,dead:player.dead,explosions:explosions.length});}')
      if diff=='normal' and f in [18,54,90,132]:(O/f'death-s{st}-{f}.png').write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
    report['deaths'].append({'stage':st,'diff':diff,**p.evaluate('()=>({samples:DAQ,geometry:AP7.geometry,keys:AP7.keys})')})
  br.close()
finally:stop()
(O/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('DONE',json.dumps({'weapons':len(report['weapons']),'errors':report['errors'],'clocks':report['clocks']}),flush=True)
