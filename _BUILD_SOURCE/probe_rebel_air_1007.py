"""Native Chromium Rookhook, cloak, death and blue ace verification."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, base64, sys
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/rebel_air_1007';O.mkdir(parents=True,exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[],'screens':[]};errors=[]
def ck(v,n):
    report['checks'].append({'ok':bool(v),'name':n});print(('PASS ' if v else 'FAIL ')+n,flush=True)
def ticks(p,n,expr='updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);'):
    for i in range(0,n,20):
        p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(20,n-i));p.wait_for_timeout(8)
def shot(p,n):
    p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
    (O/(n+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')));report['screens'].append(n)
RESET="""()=>{rg4Clear(G);G.scene=null;G.rescueDone=true;H3.release=false;B._noHit=false;G.releaseAt=G.age+999;G.novaFx=[];G.rebelBoxes=[];eBullets=[];pBullets=[];RA7.deaths=[];RA7.events=[];
for(const q of R.ships){delete q._ra7Death;delete q._on5Guard;q.dead=false;q.hp=q.max;q.frCloak=0;q.flash=0;q.rfHeading=null;q.evadeT=0;q.rg4.cd=999;q.rg4.gunCd=999;q.rg4.act=null;q.rg4.supply=null;q.rg4.armed=null;q.rg4.trace=[];q.mode='fight';q.x=camLeftX()+viewW()/2+(q.i-2)*65;q.y=170+(q.i%2)*45;}
coopOn=false;player.dead=false;player.out=false;player.invuln=1e9;player.roll=player.somer=player._chgDash=null;player._rollCool=0;player._somerCool=0;delete player._ra7Caught;player.x=camLeftX()+viewW()/2;player.y=VH-135;window.Q=R.ships[2];Q.x=player.x;Q.y=170;B.dead=false;bossActive=true;B.hp=B.maxhp;
}"""
port,stop=sh.serve(str(R))
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1100,'height':950})
    p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:1000]) if m.type=='error' or 'draw error' in m.text else None)
    p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
    if p.evaluate('()=>typeof RA7==="undefined"'):p.add_script_tag(url=f'http://127.0.0.1:{port}/assets/rebel_air_1007.js')
    p.evaluate(SETUP,{'stage':6,'kind':'rebelsquad','diff':'furious','pilot':'yuri'})
    p.evaluate("""()=>{window.R=B._rebels;rf28Init(B,R);R.frIntro={done:true};B.enter=false;B._noHit=false;window.G=rg4Init(B);H3.release=false;fb2Talk=null;s6Opening=null;s6Wing=null;rg4Warm();XART.rdy(RA7.sheet);}""")
    p.wait_for_function("()=>XART.rdy(RA7.sheet)&&REBEL_SHIPS.every(id=>XART.rdy('rr_ship_'+id)&&Array.from({length:8},(_,i)=>XART.rdy('rr_roll_'+id+'_'+i)).every(Boolean))",timeout=90000)
    p.evaluate(RESET)
    ck(p.evaluate("()=>{Q.rg4.serial=0;return ['rookhook','slug','ram'].every(k=>ra4AttackKind(Q,G)===k);}"),'natural Rook supply cycle includes hook, slugs and ram')
    p.evaluate("()=>{rg4Attack(Q,R,G,'rookhook');}");ticks(p,38);shot(p,'rookhook-warning')
    a=p.evaluate('()=>Q.rg4.act.a');p.evaluate('()=>player.x=camRightX()-30');ticks(p,28)
    ck(p.evaluate('(a)=>Q.rg4.act.a===a',a),'hook aim locks before its release and does not chase late dodges')
    ticks(p,90);ck(p.evaluate('()=>RA7.events.some(e=>e.event==="hookRelease"&&e.reason==="miss")&&!player._ra7Caught'),'moving out of the committed cast escapes without capture')
    p.evaluate(RESET);p.evaluate("()=>{rg4Attack(Q,R,G,'rookhook');}");ticks(p,75);shot(p,'rookhook-flight')
    for i in range(36):
        ticks(p,3)
        if p.evaluate('()=>Q.rg4.act?.phase==="reel"'):break
    ck(p.evaluate('()=>Q.rg4.act?.phase==="reel"&&player._ra7Caught===Q.rg4.act'),'stationary player is physically caught by the moving hook')
    shot(p,'rookhook-caught');ticks(p,35);shot(p,'rookhook-reel');ticks(p,15);shot(p,'rookhook-sling')
    ticks(p,60);shot(p,'rookhook-edge')
    ck(p.evaluate('()=>RA7.events.some(e=>e.event==="hookThrow")&&RA7.events.some(e=>e.event==="hookRelease"&&e.reason==="edge")&&!player._ra7Caught'),'hook performs reel, swing and edge throw then releases control')
    ck(p.evaluate('()=>player.x>=camLeftX()+20&&player.x<=camRightX()-20&&player.y>PLAY.y&&player.y<VH'),'throw leaves player inside the playable screen')
    p.evaluate(RESET);p.evaluate("()=>{player.invuln=0;run.shield=0;rg4Attack(Q,R,G,'rookhook');}");ticks(p,220)
    ck(p.evaluate('()=>player.dead&&RA7.events.some(e=>e.event==="hookThrow")&&RA7.events.some(e=>e.event==="hookRelease"&&e.reason==="edge")&&!player._ra7Thrown'),'stationary positive control reaches the edge and takes real damage there')
    # Ordinary gun interception cuts the modular projectile.
    p.evaluate(RESET);p.evaluate("()=>{rg4Attack(Q,R,G,'rookhook');Q.rg4.act.phase='cast';Q.rg4.act.ox=Q.x;Q.rg4.act.oy=Q.y+25;Q.rg4.act.a=Math.PI/2;Q.rg4.act.distance=70;Q.rg4.act.hx=Q.x;Q.rg4.act.hy=Q.y+95;pBullets.push({kind:'mg',x:Q.x,y:Q.y+101,w:12,h:20,dmg:9,t:0,vx:0,vy:0});}""");ticks(p,1)
    ck(p.evaluate('()=>Q.rg4.act?.phase==="recover"&&Q.rg4.act.reason==="cut"'),'ordinary gunfire severs the flying hook')
    p.evaluate(RESET);p.evaluate("()=>{rg4Attack(Q,R,G,'rookhook');const A=Q.rg4.act;A.phase='reel';A.t=0;A.px=player.x;A.py=player.y;A.reelX=Q.x+70;A.reelY=Q.y+110;A.target={ref:player,seat:1};player._ra7Caught=A;startRoll(-1);}");ticks(p,1)
    ck(p.evaluate('()=>Q.rg4.act.reason==="evade"&&!player._ra7Caught'),'real barrel roll breaks an attached tether')
    p.evaluate(RESET);p.evaluate("()=>{rg4Attack(Q,R,G,'rookhook');const A=Q.rg4.act;A.phase='reel';A.target={ref:player,seat:1};player._ra7Caught=A;Q.dead=true;}");ticks(p,1)
    ck(p.evaluate('()=>!Q.rg4.act&&!player._ra7Caught'),'Rook death removes attachment and captured-control state immediately')
    p.evaluate(RESET);p.evaluate("()=>{coopOn=true;run2.pilot='cole';player2.reset();player2.invuln=1e9;player2.x=camRightX()-65;player2.y=VH-100;Q.rg4.serial=1;rg4Attack(Q,R,G,'rookhook');window.p1Start={x:player.x,y:player.y};}")
    ck(p.evaluate('()=>Q.rg4.act.target.ref===player2&&Q.rg4.act.target.seat===2'),'co-op hook selects and retains the second seat explicitly')
    p.evaluate("()=>{const A=Q.rg4.act;A.phase='reel';A.px=player2.x;A.py=player2.y;A.reelX=Q.x+70;A.reelY=Q.y+110;player2._ra7Caught=A;}");ticks(p,6)
    ck(p.evaluate('()=>player.x===p1Start.x&&player.y===p1Start.y&&player2._ra7Caught===Q.rg4.act'),'reel moves only the selected co-op seat')
    p.evaluate('()=>rg4Clear(G)');ck(p.evaluate('()=>!player2._ra7Caught'),'encounter clear releases the second seat')
    # Real damage/hit silhouette while the native ribbon crosses both depth layers.
    p.evaluate(RESET);p.evaluate("()=>{window.N=R.ships[1];rg4Attack(N,R,G,'cloak');}");ticks(p,42);shot(p,'nyx-cloak-start');ticks(p,65);shot(p,'nyx-cloak-spiral');ticks(p,16);shot(p,'nyx-cloak-spiral-next')
    ck(p.evaluate('()=>RA7.draws.nyxBack>0&&RA7.draws.nyxFront>0&&N.frCloak>0'),'authored eight-frame Nyx spiral draws both behind and over the cloaked hull')
    ck(p.evaluate('()=>RA7.events.some(e=>e.event==="ghostknifeVolley")&&eBullets.some(p=>p._ra7Ghost)'),'Nyx fires the new warned three-round ambush from her cloaked nozzle')
    ck(p.evaluate('()=>!retinaBossTargets(B).some(t=>t._retinaId==="nyx-hull")'),'spiral cloak preserves hidden missile acquisition')
    p.evaluate("()=>{window.nyxHp=N.hp;R.hit=N.i;R.frHit=null;rebelSquadDamage(B,2);}");shot(p,'nyx-cloak-white-hit')
    ck(p.evaluate('()=>N.hp<nyxHp&&N.flash>0'),'blind hits still damage cloaked Nyx and show white hull contact')
    ck(p.evaluate("""()=>{const old=R.h3Intro,cell=cf1004Cell;let halos=0;cf1004Cell=function(k){if(k==='cloak')halos++;return cell.apply(this,arguments);};
     const I={rows:[{who:'NYX',text:'GHOSTKNIFE',demo:'cloak'}],i:0,t:.8};R.h3Intro=I;rs1004DemoTick(R,I,.02);const before=RA7.draws.nyxFront||0;fr27RebelDrawShip(N);rs1004DemoDraw(R);
     const pass=halos===0&&RA7.draws.nyxFront>before&&N._ra7CloakDemo?.t===.8;cf1004Cell=cell;R.h3Intro=old;N._ra7CloakDemo=null;return pass;}"""),'Nyx introduction uses the same authored spiral and never draws the old diamond halo')
    # Timed opaque death reel and crash, with gameplay unchanged for surviving pilots.
    p.evaluate(RESET);p.evaluate("()=>{R.hit=Q.i;rebelSquadDamage(B,Q.hp+1);}");ticks(p,30);shot(p,'rook-death-spin')
    ck(p.evaluate('()=>Q.dead&&Q._ra7Death&&!Q._ra7Death.crashed&&RA7.draws.death>0'),'defeated rebel retains an opaque authored spinning hull before impact')
    ck(p.evaluate('()=>Q._ra7Death.dur===DS_DUR&&Q._ra7Death.crashT===DS_CRASH&&Q._ra7Death.turns>=540&&Q._ra7Death.turns<=900'),'rebel death uses pilot spin/crash duration and 540–900 degree limits')
    ticks(p,48);shot(p,'rook-death-crash');ck(p.evaluate('()=>Q._ra7Death.crashed&&RA7.events.some(e=>e.event==="deathCrash"&&e.at<1.30)'),'pilot-timed crash arrives at 1.25 seconds with burst and shock rings')
    # Real keyboard sidesteps with the slowest base pilot, no shield or invulnerability.
    for difficulty in ['easy','normal','hard','furious']:
        p.evaluate(RESET)
        p.evaluate("""d=>{diffKey=d;DIFF=DIFFS[d];run.pilot='juggernaut';run.speed=0;run.shield=0;const p=PILOTS.find(p=>p.key==='juggernaut');PILOTMOD={spd:p.spd,fire:p.fire,range:p.range,tint:p.tint};player.invuln=0;window.ra7Start=player.x;rg4Attack(Q,R,G,'rookhook');}""",difficulty)
        warm=p.evaluate('()=>Q.rg4.act.warm');ticks(p,int(warm*.55*60))
        p.keyboard.down('ArrowRight');ticks(p,45);p.keyboard.up('ArrowRight');ticks(p,100)
        result=p.evaluate('()=>({moved:Math.abs(player.x-ra7Start),dead:player.dead,caught:RA7.events.some(e=>e.event==="hookCaught"),roll:!!player.roll,somer:!!player.somer,invuln:player.invuln,speed:playerBaseSpeed()})')
        ck(result['moved']>60 and not result['dead'] and not result['caught'] and not result['roll'] and not result['somer'] and result['invuln']<=0 and abs(result['speed']-2.392)<.0001,difficulty+' slowest pilot sidesteps the committed hook using ordinary keyboard movement')
        report.setdefault('movement',[]).append({'difficulty':difficulty,**result})
    # Blue ace's fixed center corridor and concrete release count.
    p.evaluate(SETUP,{'stage':6,'kind':'warhive','diff':'furious','pilot':'yuri'})
    p.evaluate("()=>{whvAceSpawn(B);B._whv.mode='ace';window.A=B._whv.ace;A.st='fight';A.x=player.x=camLeftX()+viewW()/2;A.y=200;A.dash=A.desp=A.roll=A.somer=null;A._pw5Gun=null;A._ra7Cd=0;A.gunCd=A.mslCd=A.dashCd=A.rollCd=A.somerCd=999;pBullets=[];eBullets=[];player.invuln=1e9;}")
    ticks(p,55);shot(p,'blue-ace-gap-warning');ck(p.evaluate('()=>A._ra7Gate?.phase==="warn"'),'blue ace settles before warning its fixed paired wing batteries')
    ticks(p,78);shot(p,'blue-ace-gap-fire')
    ck(p.evaluate('()=>eBullets.filter(p=>p._ra7Gate).length>=12'),'blue ace releases repeated authored wing-gun volleys')
    ck(p.evaluate('()=>eBullets.filter(p=>p._ra7Gate).every(p=>p.x<A.x? p.vx<=.001:p.vx>=-.001)'),'all wing rounds diverge outward, preserving the central movement corridor')
    ticks(p,55);shot(p,'blue-ace-recovery');ck(p.evaluate('()=>A._ra7Gate?.phase==="recover"||!A._ra7Gate'),'blue ace gives an explicit recovery window after its motif')
    p.evaluate("()=>{A.desp={st:'cross',t:0,lead:.62};A.dash={st:'warn',t:0};B.dead=true;B.dying=0;}")
    ticks(p,30);shot(p,'blue-ace-death-spin')
    ck(p.evaluate("""()=>{let draws=0;const old=gp4AceCell;gp4AceCell=function(name){if(name==='ace')draws++;return old.apply(this,arguments);};whvDrawAce(B);gp4AceCell=old;return !A.desp&&!A.dash&&A._ra7Death&&!A.crash&&draws>0;}"""),'blue ace death during cross warning still draws its complete burning hull')
    ticks(p,48);shot(p,'blue-ace-death-crash')
    ck(p.evaluate('()=>A.crash&&A._ra7Death.t>=DS_DUR&&A._ra7Death.t<1.35&&whiteBlast===0'),'blue ace reaches pilot-timed crash without a long death flash')
    ck(p.evaluate('()=>RA7.draws[0]>0&&RA7.draws[1]>0&&RA7.draws[2]>0&&RA7.draws[3]>0'),'all four separate winch/hook/chain modules render on the native canvas')
    ck(not errors,'zero native page/console/missing-asset errors');report['errors']=errors
    report['events']=p.evaluate('()=>RA7.events');report['draws']=p.evaluate('()=>RA7.draws')
    (O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');browser.close()
finally:stop()
sys.exit(any(not q['ok'] for q in report['checks']))
