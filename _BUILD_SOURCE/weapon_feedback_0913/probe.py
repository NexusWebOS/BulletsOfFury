"""Real Chromium QA for the four weapon effects and their sound ownership."""
import base64,json,sys,threading,http.server
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'));import capture3,render_audio
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
OUT=ROOT/'_shots/weapon_feedback_0913';OUT.mkdir(parents=True,exist_ok=True)
PREP="""([stage,pilot])=>{ASSETS.ready=true;story=null;run.pilot=pilot;pilotIndex=PILOTS.findIndex(p=>p.key===pilot);run.stage=stage;curStage=STAGES[stage-1];beginStage(stage);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=430;player.invuln=0;warmPlayerAtlases();
stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;enemies=[];pBullets=[];eBullets=[];powerups=[];particles=[];pImpacts=[];sonicTrail=[];playerLocks=[];special=null;run.sonicT=0;run._sonicChg=0;run._sonicSnd=false;Object.keys(Input.keys).forEach(k=>Input.keys[k]=false);Snd.loopStopAll();playerHit=function(){};}"""
TRAP="""()=>{window.__blits=[];const old=ctx.drawImage;ctx.drawImage=function(im){if(window.__fxKey){const args=Array.from(arguments).slice(1);window.__blits.push({key:window.__fxKey,width:im.width||im.naturalWidth,height:im.height||im.naturalHeight,args:args,alpha:this.globalAlpha,op:this.globalCompositeOperation});}return old.apply(this,arguments);};const f=weaponFeedbackArt;weaponFeedbackArt=function(key){window.__fxKey=key;try{return f.apply(this,arguments);}finally{window.__fxKey=null;}};}"""
def main():
    checks=[];errors=[];details={};shots=[]
    def ok(c,label):checks.append({'pass':bool(c),'label':label});print(('ok  'if c else'FAIL ')+label,flush=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=srv.serve_forever,daemon=True).start()
    with sync_playwright()as p:
        b=p.chromium.launch(args=['--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
        pg=b.new_page(viewport={'width':1100,'height':1200})
        pg.on('pageerror',lambda e:errors.append('page '+str(e)))
        pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        pg.goto('http://127.0.0.1:%d/index.html'%srv.server_port,wait_until='load',timeout=120000)
        pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000);pg.evaluate(shoot.TRAP_RAF);pg.wait_for_timeout(80)
        pg.evaluate(capture3.LIB);pg.evaluate('()=>window.__auto=function(){}');pg.evaluate(TRAP)
        def step(n):pg.evaluate('(n)=>window.__step(n)',n);pg.wait_for_timeout(15)
        def prep(pilot='cole',stage=1):
            pg.evaluate(PREP,[stage,pilot]);step(2)
            for _ in range(50):
                if pg.evaluate('(p)=>XART.rdy("ship_"+p)',pilot):break
                pg.wait_for_timeout(30)
        def shot(name):
            pg.evaluate('()=>drawWorld(0)');raw=pg.evaluate("()=>document.querySelector('#screen').toDataURL().split(',')[1]")
            path=OUT/(name+'.png');path.write_bytes(base64.b64decode(raw));shots.append(path)
        prep();pg.evaluate('()=>{weaponFeedbackWarm("cole");weaponFeedbackWarm("juggernaut");laserMistWarm();for(const n of ["colePressureLoop","juggernautChains","juggernautChargeLoop","juggernautRamLoop"])Snd.loopPrepare(n);Audio.resume();}')
        for _ in range(120):
            r=pg.evaluate('()=>["nsw_circ_3","nsw_dist_3","jwb_ball","jwb_burst","jwb_link","jchg_3","ndr_dambreaker_bottomthruster_2","bof_laser_mist_weapon_atlas"].every(k=>XART.rdy(k))&&Object.keys(BOFA.sfx).filter(k=>/^(colePressure|juggernaut|laserMist)/.test(k)).every(k=>Snd.pools[k].list[0].readyState>=3)')
            if r:break
            pg.wait_for_timeout(60)
        ok(r,'all selected authored art and sixteen sound mixes decode in Chromium')
        pg.evaluate('()=>{sonicGrant();Input.keys.j=true;window.__blits=[];}');step(45);shot('cole_compression')
        ok(pg.evaluate('()=>!pBullets.some(b=>b.kind==="sonic")&&run._sonicChg>0'),'Cole holding the trigger charges without duplicate firing')
        ok(pg.evaluate('()=>window.__blits.some(b=>b.key.startsWith("nsw_circ_"))'),'Cole compression rings reach the actual game drawImage')
        step(30);pg.evaluate('()=>Input.keys.j=false');step(8);shot('cole_full_boom')
        details['cole']=pg.evaluate('()=>({waves:pBullets.filter(b=>b.kind==="sonic").map(b=>({power:b._p,damage:b.dmg,life:b.life,geometry:sonicFrontGeometry(b)})),blits:window.__blits.filter(b=>b.key.startsWith("nsw_dist_")).slice(-5),release:window.__alog.snd.filter(e=>e[1]==="colePressureRelease")})')
        ok(len(details['cole']['waves'])==1 and details['cole']['waves'][0]['power']>.99,'one fully charged release produces one piercing pressure front')
        ok(details['cole']['release']and details['cole']['release'][-1][2]>.99,'full Sonic Boom receives its stronger dedicated release sound')
        step(22);ok(pg.evaluate('()=>!Snd.loops.colePressureLoop.on'),'Cole charge bed fades and stops after release')
        prep('juggernaut');pg.evaluate('()=>{startSpecial();window.__blits=[];}');step(10);shot('juggernaut_flails')
        ok(pg.evaluate('()=>wreckBalls.length===2&&wreckBalls[0].spin===-wreckBalls[1].spin'),'exactly two opposite wrecking balls remain anchored')
        ok(pg.evaluate('()=>window.__blits.filter(b=>b.key==="jwb_ball").length>=2'),'full-opacity authored steel balls reach drawImage')
        pg.evaluate('()=>{const q=wreckPos(wreckBalls[0]);eBullets.push({kind:"bullet",x:q.x,y:q.y,r:4,vx:0,vy:0});wreckTick(0);}')
        ok(pg.evaluate('()=>eBullets[0].dead&&window.__alog.snd.some(e=>e[1]==="juggernautWreckBlock")'),'a real bullet interception plays the short metal deflection cue')
        pg.evaluate('()=>{const q=wreckPos(wreckBalls[1]);window.__foe=spawnEnemy("s1jetbomber",q.x,q.y,{vy:0});window.__foe.ghost=false;wreckBalls[1].cd=0;wreckTick(0);}')
        ok(pg.evaluate('()=>window.__foe.hp<=0&&window.__alog.snd.some(e=>e[1]==="juggernautWreckHit")'),'a real steel contact damages its target and plays the heavy strike')
        shot('juggernaut_steel_strike')
        details['strike']=pg.evaluate('()=>pImpacts.filter(p=>p._weaponFx==="wreck").map(p=>({x:p.x,y:p.y,t:p.t,size:p.size}))')
        step(3)
        ok(pg.evaluate('(ps)=>ps.every(p=>pImpacts.some(q=>q._weaponFx==="wreck"&&q.x===p.x&&q.y===p.y))',details['strike']),'steel impact flashes stay at contact points while balls keep orbiting')
        pg.evaluate('()=>{player.y=430;Input.keys.h=true;Input.keys.w=true;}');step(78);shot('juggernaut_charge')
        ok(pg.evaluate('()=>chargeLevel()>.99&&Snd.loops.juggernautChargeLoop.on'),'Juggernaut full wind-up owns its mechanical charge bed')
        pg.evaluate('()=>{Input.keys.h=false;Input.keys.w=false;window.__blits=[];}');step(4);shot('juggernaut_boost')
        details['dash']=pg.evaluate('()=>({dash:player._chgDash,blits:window.__blits.filter(b=>b.key.startsWith("ndr_dambreaker")),sounds:window.__alog.snd.filter(e=>e[1].startsWith("juggernaut")),y:player.y})')
        ok(details['dash']['dash']and len(details['dash']['blits'])>=2,'the committed dash draws two aft authored exhausts')
        ok(pg.evaluate('()=>Snd.loops.juggernautRamLoop.on'),'the dash owns a distinct boost sound bed')
        step(45);shot('juggernaut_ram_stop')
        ok(pg.evaluate('()=>!player._chgDash&&!Snd.loops.juggernautRamLoop.on&&!Snd.loops.juggernautChargeLoop.on&&window.__alog.snd.some(e=>e[1]==="juggernautRamStop")'),'landing thump fires once and both charge/boost beds stop')
        pg.evaluate('()=>endSpecial()');step(20)
        ok(pg.evaluate('()=>wreckBalls.length===0&&!Snd.loops.juggernautChains.on'),'flails and chain sound leave together when the special ends')
        prep('yuri');pg.evaluate('()=>{spawnSubBoss("razorback");razorbackUpdate(subBoss,0);subBoss.x=worldWidth()/2;subBoss.y=210;subBoss.enter=false;subBoss._drawY=210;subBoss._rzb.state="guns";subBoss._rzb.trans=0;subBoss._rzb.a=Math.PI/2;window.__armorBefore=subBoss.hp;window.__armorShot={kind:"lasermist",x:subBoss.x,y:subBoss.y,vx:0,vy:0,w:16,h:39,dmg:7,lv:5,t:0,life:3.2,_mistStage:2,_mistAge:0,_mistLedger:{hits:[]}};_dmgBullet=window.__armorShot;laserMistTick(window.__armorShot,0);_dmgBullet=null;}')
        ok(pg.evaluate('()=>!window.__armorShot.dead&&subBoss.hp===window.__armorBefore&&!window.__armorShot._mistLedger.hits.length&&!pImpacts.length'),'Laser Mist passes inactive armor without fake wet impacts or consuming its hit budget')
        pg.evaluate('()=>{const b=subBoss,q=rzbWorld(b,-57,96);window.__gunBefore=b._rzb.pools.left;const s=Object.assign({},window.__armorShot,{x:q.x,y:q.y,_mistLedger:{hits:[]}});_dmgBullet=s;laserMistTick(s,0);_dmgBullet=null;window.__gunDead=!!s.dead;}')
        ok(pg.evaluate('()=>window.__gunDead&&subBoss._rzb.pools.left<window.__gunBefore&&pImpacts.length>0'),'Laser Mist still damages a live rotated gun and produces its real wet impact')
        prep('yuri');pg.evaluate('()=>{laserMistFire(5);window.__lmLedger=pBullets[0]._mistLedger;}');shot('laser_mist_launch')
        ok(pg.evaluate('()=>pBullets.filter(b=>!b.dead&&b.kind==="lasermist").length===3&&pImpacts.filter(p=>p._lmFx).length===3&&!(player._mgMuzT>0)'),'Laser Mist launches three blue emitters without a borrowed MG flash')
        step(8);shot('laser_mist_first_split')
        ok(pg.evaluate('()=>pBullets.filter(b=>!b.dead&&b.kind==="lasermist").length===9'),'the first split preserves nine independent lances')
        step(17);shot('laser_mist_bloom')
        ok(pg.evaluate('()=>pBullets.filter(b=>!b.dead&&b.kind==="lasermist").length===27'),'the final bloom preserves all twenty-seven independent lances')
        details['mist']=pg.evaluate('()=>({splits:window.__alog.snd.filter(e=>e[1]==="laserMistSplit"||e[1]==="laserMistBloom"),ledger:window.__lmLedger,impacts:pImpacts.length})')
        ok(sum(e[1]=='laserMistSplit'for e in details['mist']['splits'])==1 and sum(e[1]=='laserMistBloom'for e in details['mist']['splits'])==1,'each split beat receives one sound per wave instead of one per parent')
        pg.evaluate('()=>{laserMistImpact(player.x,240,5,true);laserMistImpact(player.x+20,240,5,true);}');shot('laser_mist_impact')
        ok(pg.evaluate('()=>particles.filter(p=>p._lmBubble).length<=72'),'wet impact bubbles retain the independent performance cap')
        prep('juggernaut');pg.evaluate('()=>{startSpecial();Input.keys.h=true;Input.keys.w=true;}');step(15);pg.evaluate('()=>{player.dead=true;player.alive=false;startDeathSpin();}');step(30)
        ok(pg.evaluate('()=>!player._chgDash&&!player._chgOn&&!Snd.loops.juggernautChargeLoop.on&&!Snd.loops.juggernautChains.on'),'death cancels uncommitted feedback and stops Juggernaut beds')
        prep('juggernaut');pg.evaluate('()=>{startSpecial();Input.keys.h=true;Input.keys.w=true;}');step(20);pg.evaluate('()=>setState("paused")');step(2)
        ok(pg.evaluate('()=>Object.values(Snd.loops).every(l=>!l.on&&l.el.paused)'),'pause immediately stops every held feedback sound')
        prep('cole');pg.evaluate('()=>{sonicGrant();Input.keys.j=true;}');step(20);pg.evaluate('()=>run.sonicT=0');step(30)
        ok(pg.evaluate('()=>!run._sonicChg&&!run._sonicSnd&&!Snd.loops.colePressureLoop.on'),'Sonic Boom expiry releases its audio and charge ownership')
        details['runtimeError']=pg.evaluate('()=>window.__err||null');ok(not errors and not details['runtimeError'],'zero page, console, and deterministic-loop errors')
        b.close()
    srv.shutdown()
    sheet=Image.new('RGB',(400*4,450*((len(shots)+3)//4)),'#101821')
    for i,path in enumerate(shots):
        im=Image.open(path).convert('RGB');im.thumbnail((400,420));sheet.paste(im,(i%4*400,i//4*450));ImageDraw.Draw(sheet).text((i%4*400+8,i//4*450+425),path.stem,fill='white')
    sheet.save(OUT/'contact.png')
    (OUT/'results.json').write_text(json.dumps({'checks':checks,'errors':errors,'details':details},indent=2),encoding='utf-8')
    print('%d passed / %d failed'%(sum(c['pass']for c in checks),sum(not c['pass']for c in checks)),flush=True)
    return int(any(not c['pass']for c in checks))
if __name__=='__main__':sys.exit(main())
