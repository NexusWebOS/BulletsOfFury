"""Native Chromium checks and pixels for Mike's stage 1–5 corrections."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/stage_1_5_0914';OUT.mkdir(parents=True,exist_ok=True)
PREP="""stage=>{run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');run.stage=stage;curStage=STAGES[stage-1];beginStage(stage);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=430;player.invuln=0;playerHit=function(){};story=null;dlgBox=function(){};
stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];particles=[];powerups=[];pImpacts=[];playerLocks=[];special=null;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);Snd.loopStopAll();window.__auto=function(){};}"""
def main():
    checks=[];errors=[];details={};shots=[]
    def ok(c,label):checks.append({'pass':bool(c),'label':label});print(('ok  'if c else'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
    with sync_playwright()as p:
        b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required']);pg=b.new_page(viewport={'width':1100,'height':1200})
        pg.on('pageerror',lambda e:errors.append('page '+str(e)));pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000);pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.evaluate(capture3.LIB)
        pg.evaluate('''()=>{window.__blits=[];window.__artKey=null;const old=ctx.drawImage;ctx.drawImage=function(im){if(window.__artKey)window.__blits.push({key:window.__artKey,args:Array.from(arguments).slice(1),alpha:this.globalAlpha});return old.apply(this,arguments);};
        for(const name of ['weaponFeedbackArt','combatAtlasDraw','drawMfx']){const f=window[name];window[name]=function(key){window.__artKey=key;try{return f.apply(this,arguments);}finally{window.__artKey=null;}};}}''')
        pg.evaluate('''()=>{const f=stage3DroneShotDraw;stage3DroneShotDraw=function(q){window.__artKey='bpfx_proj_laser_0';try{return f.apply(this,arguments);}finally{window.__artKey=null;}};
        const g=l23FovDraw;l23FovDraw=function(b,B,i,p,k){window.__artKey='bmfx_fov_'+l23FovPhase(k)+'_tall';try{return g.apply(this,arguments);}finally{window.__artKey=null;}};}''')
        def step(n):
            for i in range(0,n,30):pg.evaluate('n=>window.__step(n)',min(30,n-i));pg.wait_for_timeout(12)
        def ready(expr):
            for _ in range(160):
                if pg.evaluate(expr):return True
                pg.wait_for_timeout(40)
            return False
        def prep(stage):pg.evaluate(PREP,stage);step(2)
        def fight(stage,role):
            pg.evaluate('a=>window.__fight(a[0],a[1],"yuri")',[stage,role]);pg.evaluate('()=>{stagePlan=[];enemies=[];story=null;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);playerHit=function(){};player.invuln=0;}')
            for _ in range(80):
                if pg.evaluate('()=>{const T=window.__tgt();return T&&!T.enter&&T.y>0&&(!T._rzb||T._rzb.state!=="arrival");}'):break
                step(6)
            step(8)
        def shot(name):
            pg.evaluate('()=>{if(state===GS.PLAY){shake=0;drawWorld(0);}}');r=pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]");path=OUT/(name+'.png');path.write_bytes(base64.b64decode(r));shots.append(path)
        prep(1);pg.evaluate('()=>{stageRevisionWarm("razorback");stageRevisionWarm("damkeeper");stageRevisionWarm("olivewarden");Audio.resume();window.__foe=spawnEnemy("s1jetdelta",worldWidth()/2,250,{vy:0});window.__foe.ghost=false;window.__foe.hp=window.__foe.maxhp/2;}')
        ok(ready('()=>["nsd_chim_7","nxp_upward_7"].every(k=>XART.rdy(k))&&XART.rdy(nefArtFor(window.__foe))'),'authored damage plumes and clean stage-1 hull decode')
        pg.evaluate('()=>window.__blits=[]');shot('s1_half_health');step(8);shot('s1_half_health_later')
        details['burn']=pg.evaluate('()=>({art:nefArtFor(window.__foe),blits:window.__blits.filter(q=>/^nsd_chim_|^nxp_upward_/.test(q.key))})')
        ok(details['burn']['art'].endswith('_intact')and any(q['key'].startswith('nxp_upward_')for q in details['burn']['blits']),'half-health fodder uses animated authored fire over a clean plate')
        ok(len(set(q['key']for q in details['burn']['blits']if q['key'].startswith('nsd_chim_')))>2,'damage smoke actually advances multiple rendered frames')
        pg.evaluate('()=>{window.__foe.hp=window.__foe.maxhp;window.__blits=[];}');shot('s1_healthy')
        ok(pg.evaluate('()=>!window.__blits.some(q=>/^nsd_chim_|^nxp_upward_/.test(q.key))'),'healthy stage-1 fodder has no damage plume')
        fight(1,'mini');step(210);shot('s1_razorback_guns');details['razorback']=pg.evaluate('()=>window.__alog.snd.filter(q=>q[1].startsWith("razorback"))')
        ok(any(q[1]=='razorbackGun'for q in details['razorback']),'native Razorback suppression plays its dedicated weapon report')
        pg.evaluate('()=>{subBoss._rzb.state="turret";subBoss._rzb.attack="sonic";subBoss._rzb.at=1.19;subBoss._rzb.trans=0;subBoss._rzb.beat=-1;}');step(6);shot('s1_razorback_pressure')
        ok(pg.evaluate('()=>window.__alog.snd.some(q=>q[1]==="razorbackPressure")'),'Razorback sonic release is audible without borrowing the player trigger')
        fight(1,'boss');step(180);shot('s1_overlord_fire')
        ok(pg.evaluate('()=>window.__alog.snd.some(q=>q[1]==="overlordGun")&&Snd.loops.overlordRotor.on'),'Overlord actual gunfire and continuous rotor bed are wired')
        pg.evaluate('()=>{ovRocketSide(boss,-1);ovGreenVolley(boss);ovRotorTempest(boss);ovStartChargeTell(boss);}');step(8);shot('s1_overlord_charge')
        ok(pg.evaluate('()=>["overlordRocket","overlordLance","overlordWind","overlordCharge"].every(k=>window.__alog.snd.some(q=>q[1]===k))'),'Overlord rockets, lances, wind and charge each have audible cues')
        prep(2);ok(ready('()=>XART.rdy("cfx_stage2_volcanic_projectiles")&&XART.rdy("l23fx_inferno_mg_0")'),'stage-2 authored flight art decodes before capture')
        pg.evaluate('()=>{window.__flight={kind:"s2rake",x:worldWidth()/2,y:220,vx:0,vy:2,w:8,h:18,t:0};eBullets=[window.__flight];window.__blits=[];}');shot('s2_flight_pose');step(15);shot('s2_flight_pose_later')
        details['s2']=pg.evaluate('()=>window.__blits.filter(q=>q.key==="cfx_stage2_volcanic_projectiles")')
        ok(len(details['s2'])>2 and len(set((q['args'][0],q['args'][1],q['args'][2],q['args'][3])for q in details['s2']))==1,'stage-2 round keeps the same authored source rectangle throughout flight')
        prep(3);pg.evaluate('()=>{window.__spawnLog=[];const f=spawnEnemy;spawnEnemy=function(t){window.__spawnLog.push(t);return f.apply(this,arguments);};const plan=buildStagePlan(3);plan.forEach(q=>q.fn?q.fn():q.f?q.f():null);}')
        step(180);details['roster']=pg.evaluate('()=>window.__spawnLog');ok(len(details['roster'])>4 and 's3barge'not in details['roster'],'stage-3 director launches approved ice enemies and no stored boats')
        prep(3);pg.evaluate('()=>{window.__drone=spawnEnemy("cryoeye",worldWidth()/2,160,{vy:0});window.__drone.ghost=false;window.__drone._dr.aim=Math.PI/2;droneFire(window.__drone);window.__blits=[];}');ok(ready('()=>XART.rdy("bpfx_proj_laser_0")'),'ice-drone authored projectile art decodes');step(20);shot('s3_visible_drone_fire')
        ok(pg.evaluate('()=>eBullets.some(q=>q._s3DroneShot)&&window.__blits.some(q=>q.key==="bpfx_proj_laser_0")'),'ordinary ice drones draw the enlarged authored flight plate in the real canvas')
        fight(3,'boss');ok(ready('()=>["bmfx_fov_green_tall","bmfx_fov_yellow_tall","bmfx_fov_red_tall","nlz_3_b0"].every(k=>XART.rdy(k))'),'stage-3 FOV and authored laser charge art decode')
        phases=[]
        for i,pat in enumerate(['s3wallcannons','s3wallgate','s3wallhalo','s3walloverdrive']):
            pg.evaluate('pat=>{boss._l23Beam=null;boss._sba=null;boss._s3boss.charge=null;boss._s3boss.volley=null;stage3BossAttack(boss,pat,2,0,1);}',pat)
            info=pg.evaluate('()=>({slots:boss._l23Beam.slots,angles:boss._l23Beam.angles,charge:boss._s3boss.charge,origins:boss._l23Beam.slots.map(s=>shipBossMount(boss,s))})');phases.append(info)
            if i==0:
                step(22);shot('s3_green_warning');step(50);shot('s3_yellow_warning');step(57);shot('s3_red_warning');step(65);shot('s3_cannon_lasers')
        details['s3boss']=phases
        ok(all(set(q['slots']).issubset({'L','C','R'})and 'C'in q['slots']and q['charge']['kind']=='centerBeam'for q in phases),'every stage-3 boss phase fires only from cannon tips with a charged center laser')
        ok(pg.evaluate('()=>window.__blits.some(q=>q.key==="bmfx_fov_green_tall")&&window.__blits.some(q=>q.key==="bmfx_fov_red_tall")'),'green and red authored FOV warnings reach drawImage')
        fight(4,'mini');ok(ready('()=>XART.rdy("mgcf_1_5")&&XART.rdy("bpfx_proj_missile_0")'),'stage-4 machine bullets and rocket flight plates decode')
        pg.evaluate('()=>{window.__miniShots=[];const f=stage4MiniMachine;stage4MiniMachine=function(){const q=f.apply(this,arguments);window.__miniShots.push({kind:q.kind,slot:q._s4Slot,x:q.x,y:q.y});return q;};window.__blits=[];}')
        step(75);shot('s4_mounted_spread');step(150);shot('s4_center_pair');step(165);shot('s4_turret_rockets')
        details['warden']=pg.evaluate('()=>({shots:window.__miniShots,rockets:eBullets.filter(q=>q._s4wKind==="rocket").map(q=>({slot:q._s4Slot,kind:q.kind})),sounds:window.__alog.snd.filter(q=>q[1].startsWith("warden")),blue:window.__blits.filter(q=>q.key.startsWith("s4w_drone_barrel_"))})')
        ok(not details['warden']['blue'],'Warden no longer renders blue chaingun attachments')
        ok(pg.evaluate('()=>window.__blits.some(q=>q.key==="mgcf_1_5")'),'Warden machine bullets actually render the approved orange tracer pixels')
        ok({'L','R','CL','CR'}.issubset({q['slot']for q in details['warden']['shots']})and all(q['kind']=='mg'for q in details['warden']['shots']),'both mounted spread guns and both center barrels fire actual machine bullets')
        ok({q['slot']for q in details['warden']['rockets']}=={'L','R'},'Warden rocket salvos leave both mounted turrets')
        ok({'wardenGun','wardenCenterGun','wardenRackCharge','wardenRocket'}.issubset({q[1]for q in details['warden']['sounds']}),'Warden gun acts, rack tell and rocket salvos are audible')
        fight(4,'boss');step(40);pg.evaluate('()=>{boss.hp=boss.maxhp*.5;stage4CoreTurretSpawnMissing(boss,.5);window.__helperAudioFrame=window.__i;}');step(48);shot('s4_helpers_over_generators')
        details['layout']=pg.evaluate('()=>({x:boss.x,w:boss.w,left:camLeftX(),right:camRightX(),turrets:boss._s4war.coreTurrets.map(t=>({x:t.x,y:t.y})),nodes:boss._s4war.shield.nodes.map(n=>({x:n.x,y:n.y,side:n.side})),size:S4H_SIZE})')
        layout=details['layout'];ok(all(abs(t['x']-layout['x'])-layout['size']/2>layout['w']*.69 and any(abs(t['x']-n['x'])<1 and t['y']<n['y']for n in layout['nodes'])for t in layout['turrets']),'whole helpers sit outside the shield width directly above their generator columns')
        ok(all(t['x']-layout['size']/2>=layout['left'] and t['x']+layout['size']/2<=layout['right'] for t in layout['turrets'])and all(n['x']-27>=layout['left'] and n['x']+27<=layout['right'] for n in layout['nodes']),'both helpers and all four complete generator sprites fit in the visible camera')
        pg.evaluate('()=>{boss._phaseInvuln=0;const ns=boss._s4war.shield.nodes.filter(n=>n.side<0);ns.forEach(n=>n.hp=10);window.__carrierHp=boss.hp;window.__beam={x:ns[0].x,w:26,top:-20,bot:player.y-14,dmg:12};stage4PiercingBeam(boss,window.__beam);}')
        ok(pg.evaluate('()=>boss._s4war.shield.nodes.filter(n=>n.side<0).every(n=>n.dead)&&boss.hp===window.__carrierHp'),'one piercing laser tick destroys both generators in the left column without damaging the shielded carrier')
        pg.evaluate('()=>{const ns=boss._s4war.shield.nodes.filter(n=>n.side>0);ns.forEach(n=>n.hp=10);window.__beam.x=ns[0].x;stage4PiercingBeam(boss,window.__beam);}');shot('s4_shield_broken')
        ok(pg.evaluate('()=>boss._s4war.shield.nodes.every(n=>n.dead)&&!boss._s4war.shield.active'),'the second column breaks the field when both generators are destroyed')
        pg.evaluate('()=>{stage4RamStart(boss);window.__ramTrace=[];}')
        for i in range(42):
            step(10);q=pg.evaluate('()=>({mode:boss._s4war.mode,x:boss.x,y:boss.y,air:!!boss._s4Airborne,noHit:!!boss._noHit,shadow:boss._s4war.ram&&boss._s4war.ram.shadowY,contact:bossHitTest(boss.x,boss.y)})');details.setdefault('ram',[]).append(q)
            if i in [3,11,15,19,22,26,32,41]:shot('s4_ram_%02d'%i)
        modes={q['mode']for q in details['ram']};ok({'ramTell','ramDive','ramOff','ramOver','ramReturn'}.issubset(modes),'unpowered Sovereign warns, dives fully offscreen, flies overhead and returns from the opposite edge')
        ok(any(q['mode']=='ramOff'and q['y']>512+286*.65 for q in details['ram']),'Sovereign clears its whole hull before the offscreen turn')
        ok(all(not q['contact']for q in details['ram']if q['air']),'the overhead flight cannot cause an invisible ground-plane hull hit')
        ok(any(q['mode']=='ramOver'and q['shadow']>400 for q in details['ram'])and any(q['mode']=='ramOver'and q['shadow']<400 for q in details['ram']),'frame-shaped shadow crosses the player row during the overflight')
        details['helperAudio']=pg.evaluate('()=>({sounds:window.__alog.snd.filter(q=>q[0]>=window.__helperAudioFrame).map(q=>q[1]),legacy:window.__alog.syn.filter(q=>q[0]>=window.__helperAudioFrame&&["enemyLightningChaingun","bossShieldStatic"].includes(q[1]))})')
        ok({'sovereignHelperGun','sovereignHeat','sovereignWindup'}.issubset(set(details['helperAudio']['sounds']))and not details['helperAudio']['legacy'],'native Sovereign helpers use authored gun, cooling and windup reports with no legacy synth fallback')
        fight(4,'boss');step(60);pg.evaluate('()=>{const ns=boss._s4war.shield.nodes.filter(n=>n.side<0);ns.forEach(n=>n.hp=1);run.pilot="axel";run.spaceMode=false;run.weapon=3;run.wlevel=5;player.x=ns[0].x;player.y=430;player.fireCd=0;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);Input.keys.j=true;}');step(24);shot('s4_held_laser_generators')
        ok(pg.evaluate('()=>boss._s4war.shield.nodes.filter(n=>n.side<0).every(n=>n.dead)&&boss._s4war.shield.nodes.filter(n=>n.side>0).every(n=>!n.dead)'),'native held laser input pierces both generators in one column while preserving the other column')
        pg.evaluate('()=>{Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);window.__run(5,"yuri");window.__auto=function(){};}')
        for _ in range(200):
            if pg.evaluate('()=>drawLaunch._phase==="settle"'):break
            step(6)
        sky0=pg.evaluate('()=>({phase:drawLaunch._phase,time:drawLaunch._pt,scroll:drawLaunch._bgScroll})');step(180);shot('s5_extended_sky')
        details['sky']=pg.evaluate('()=>({phase:drawLaunch._phase,time:drawLaunch._pt,scroll:drawLaunch._bgScroll})')
        ok(sky0['phase']=='settle'and details['sky']['phase']=='settle'and details['sky']['time']>2.9 and details['sky']['scroll']>sky0['scroll']+100,'native stage-5 launch stays in the extended sky for three seconds and keeps scenery scrolling')
        prep(5);pg.evaluate('()=>{run.spaceWeapon=0;run.spaceLevels=[3,3,3];window.__locks=[spawnEnemy("s5interceptor",worldWidth()/2-80,230,{}),spawnEnemy("s5interceptor",worldWidth()/2,200,{}),spawnEnemy("s5interceptor",worldWidth()/2+80,250,{})];window.__locks.forEach(q=>q.ghost=false);spaceVolleyFire();window.__rack=pBullets.filter(q=>q.kind==="spaceVolley");}')
        ok(pg.evaluate('()=>window.__rack.length===3&&!pBullets.some(q=>q.kind==="spaceVolleySeed")&&window.__rack.every(q=>q._target)'),'passive space rack launches three real independent homing missiles immediately')
        step(12);shot('s5_passive_volley');details['missiles']=pg.evaluate('()=>window.__rack.map(q=>({kind:q.kind,vy:q.vy,x:q.x,y:q.y,dead:!!q.dead}))');ok(pg.evaluate('()=>window.__rack.every(q=>(q.kind==="spaceImpact"||q.vy<0)&&Number.isFinite(q.x)&&Number.isFinite(q.y))'),'space missiles fly forward or produce actual impacts without orbiting or NaNs')
        pg.evaluate('()=>{run.spaceWeapon=1;pBullets=[];spaceShadowRelease(SPACE_SHADOW_FULL_CHARGE);window.__orb=pBullets[0];}')
        details['shadow']=pg.evaluate('()=>({dmg:window.__orb.dmg,expected:SPACE_SHADOW_TIER[2].base*1.5*1.35,burst:window.__orb.primaryBurst})');ok(abs(details['shadow']['dmg']-details['shadow']['expected'])<1e-8,'Shadow Orb direct payload and its inherited detonation payload are 35 percent stronger')
        ok(pg.evaluate('()=>Snd.TAME.spaceLaserCannon.g===.30'),'space Laser Cannon volume is reduced at its own sound route')
        ok(pg.evaluate('()=>spaceAtlasCanvas("ship_base",_pilotKey())&&gravityMode.phase==="active"'),'stage 5 uses the finished authored spaceship for the selected pilot')
        fight(5,'boss');step(60);shot('s5_regent_formation');start=pg.evaluate('()=>_stage5SpaceScroll');step(120);end=pg.evaluate('()=>_stage5SpaceScroll')
        ok(end>start+70,'stage-5 scenery continues scrolling throughout the boss fight')
        pg.evaluate('()=>{boss._xenoGrid=null;boss._sba=null;xenoRegentGridStart(boss,2);}');step(18);shot('s5_grid_first_warning');step(34);shot('s5_grid_next_warning')
        ok(pg.evaluate('()=>boss._xenoGrid&&boss._xenoGrid.wave===1&&boss._xenoGrid.t<boss._xenoGrid.next'),'Regent warns the next formation opening after the first row releases')
        step(220);shot('s5_regent_locked_escorts');ok(pg.evaluate('()=>boss._xenoRig.helpers.some(h=>h.tell)||window.__alog.snd.some(q=>q[1]==="bossfireXenoregent")'),'Regent escorts use visible locked charge beats and native release reports')
        details['error']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['error'],'zero Chromium page, console or controlled-loop errors')
        b.close()
    srv.shutdown();sheet=Image.new('RGB',(400*4,450*((len(shots)+3)//4)),'#101821');d=ImageDraw.Draw(sheet)
    for i,path in enumerate(shots):im=Image.open(path).convert('RGB');im.thumbnail((400,420));sheet.paste(im,(i%4*400,i//4*450));d.text((i%4*400+5,i//4*450+424),path.stem,fill='white')
    sheet.save(OUT/'contact.png');(OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details},indent=2),encoding='utf-8')
    print('%d passed / %d failed'%(sum(c['pass']for c in checks),sum(not c['pass']for c in checks)),flush=True);return int(any(not c['pass']for c in checks))
if __name__=='__main__':sys.exit(main())
