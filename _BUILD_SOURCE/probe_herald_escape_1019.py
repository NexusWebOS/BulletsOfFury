"""Actual slowest-pilot keyboard escapes and stationary positive controls."""
from pathlib import Path
import ast,http.server,json,sys
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/herald';O.mkdir(parents=True,exist_ok=True)
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
checks=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.HE19={hits:0,used:false};const hit=playerHit;playerHit=function(){const was=player.dead,r=hit.apply(this,arguments);if(!was&&player.dead)HE19.hits++;return r;};}''')
  def frames(n):
   for i in range(0,n,12):p.evaluate(shoot.STEP,min(12,n-i));p.wait_for_timeout(5)
  def setup(diff,kind,edge):
   p.evaluate(SETUP,dict(stage=8,kind='heralddeath',mini=True,diff=diff,pilot='juggernaut'))
   p.wait_for_function('()=>{stageLoadTick();hd1003Warm();return stageLoadReady(8)&&XART.rdy(HD1003_ART.key)&&XART.rdy(HC1006_FX.key)&&bmfReady("game")}',polling=50)
   p.evaluate('''([kind,edge])=>{B=subBoss;B.enter=B._noHit=false;B._be=null;B.y=B.ty;B._drawY=B.y;
    VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;bossWarned=false;warnT=0;warnKind=null;
    BOFCinematicDirector.cancel();AP10_X.intro=null;story=fb2Talk=fb2Intro=thaw=s6Opening=null;H3.release=false;H3.ending=null;P2M.active=null;run.shield=0;run.sonicT=run.dkT=0;special=thunderStorm=null;run._megaShield=false;
    pilotIndex=PILOTS.findIndex(q=>q.key==='juggernaut');const pilot=PILOTS[pilotIndex];PILOTMOD={spd:pilot.spd,fire:pilot.fire,range:pilot.range,tint:pilot.tint};run.speed=0;
    Input.keys={};Input.mouse.down=false;powerups=[];enemies=[];pBullets=[];eBullets=[];player.x=edge==='left'?camLeftX()+30:edge==='right'?camRightX()-30:camLeftX()+viewW()/2;player.y=VH-110;player.invuln=0;player.roll=player.somer=null;HE19={hits:0,start:player.x,used:false};
    if(kind.startsWith('core-'))for(const id of ['gunL','gunR','wingL','wingR'])hd1003Break(B,hd1003Part(B,id));
    hd19Start(B,kind);SC12.refresh();__bofFit();}''',[kind,edge])
  for diff in ['normal','hard','furious']:
   for kind in ['cannon-rake','wing-rake','core-fury','core-lance']:
    for edge in ['left','right']:
     setup(diff,kind,edge);direction='ArrowRight' if edge=='left' else 'ArrowLeft';p.keyboard.down(direction);frames(240);p.keyboard.up(direction)
     row=p.evaluate('({hits:HE19.hits,moved:Math.abs(player.x-HE19.start),dead:player.dead,roll:!!player.roll,somer:!!player.somer,special:!!special,base:playerBaseSpeed(),state})')
     ck(diff+' '+kind+' '+edge+' ordinary slow-pilot escape',row['hits']==0 and not row['dead'] and not row['roll'] and not row['somer'] and not row['special'] and row['moved']>80,row)
     if diff=='furious' and edge=='left':
      p.evaluate('shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();__bofFit();');p.screenshot(path=str(O/('escape-'+kind+'.png')))
   setup(diff,'core-fury','center');frames(150);row=p.evaluate('({hits:HE19.hits,dead:player.dead})');ck(diff+' stationary positive control is hit by the real core salvo',row['hits']>0,row)
  # Ordinary primary input must still route into the actual disarmed core.
  setup('normal','core-fury','center')
  p.evaluate('''()=>{player.invuln=1e9;run.pilot='cole';pilotIndex=PILOTS.findIndex(q=>q.key==='cole');const pilot=PILOTS[pilotIndex];PILOTMOD={spd:pilot.spd,fire:pilot.fire,range:pilot.range,tint:pilot.tint};run.wlevels||=Array(8).fill(0);run.wvars||=Array(8).fill(null);weaponFormSelect(7,{kind:'primary1003b',id:'mg'});run.weapon=0;run.wlevel=run.wlevels[0]=0;run.wvars[0]=null;run.forge={};run.forgeForms={};run.infusion=null;run.loadout=[0];player.fireCd=0;
   const c=hd1003Center(B,hd1003Part(B,'core'));player.x=c.x-(wm26PlayerNose().x-player.x);player.y=c.y+130;window.he19HP=B.hp;}''');p.keyboard.down('j');frames(90);p.keyboard.up('j');row=p.evaluate('({loss:he19HP-B.hp,dead:B.dead})');ck('Actual ordinary primary damages Herald core after disarm',row['loss']>0,row)
  br.close()
finally:stop()
ck('No browser/console/draw/asset errors',not errors,errors);report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors);(O/'escape-report.json').write_text(json.dumps(report,indent=2)+'\n');sys.exit(report['failed']>0)
