"""Reproduce and verify Razorback pellets, finite laser geometry and Cole impact audio."""
import base64,json,sys,time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import shoot

ROOT=Path(__file__).resolve().parent.parent
BASELINE='--baseline'in sys.argv
OUT=ROOT/('_shots/game_bugfix_0913/before'if BASELINE else'_shots/game_bugfix_0913/after')
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE/trailer_v7'))
import render_audio

PREP="""(stage)=>{
ASSETS.ready=true;story=null;run.stage=stage;curStage=STAGES[stage-1];beginStage(stage);setState(GS.PLAY);player.reset();player.invuln=999;
stagePlan=[];waveIdx=0;boss=null;bossActive=false;bossTriggered=true;subBoss=null;subBossActive=false;subBossTriggered=true;aminiTriggered=true;
enemies.length=0;pBullets.length=0;eBullets.length=0;powerups.length=0;playerLocks=[];special=null;Input.keys={};
}"""
RZ="""()=>{spawnSubBoss('razorback');const b=subBoss,R=b._rzb;razorbackUpdate(b,0);b.x=worldWidth()/2;b.y=210;b.enter=false;R.state='guns';R.trans=0;R.a=Math.PI/2;R.tgt={x:b.x,y:b.y};R.speed=0;R.attack='sonic';R.at=0;R.beat=-1;subBossActive=true;return b.kind;}"""
TRIAL="""(where)=>{const b=subBoss,R=b._rzb;if(where==='turret'){R.state='turret';R.trans=0;}if(where==='transition'){R.state='turret';R.trans=1;}
const q=where==='gun'?rzbWorld(b,-57,96):{x:b.x,y:b.y},key=where==='gun'?'left':'turret';
const before=R.pools[key],hp=b.hp,shot={kind:'bullet',x:q.x,y:q.y,vx:0,vy:0,w:3,h:3,dmg:7,t:0};pBullets=[shot];
updatePlay(1/60);return {dead:!!shot.dead,before:before,after:R.pools[key],hpBefore:hp,hpAfter:b.hp,part:razorbackPartAt(b,q.x,q.y)};}"""
BEAM="""()=>{const b=subBoss,R=b._rzb,q=rzbWorld(b,-57,96);R.a=0;const port=rzbWorld(b,-57,96);player.x=port.x;player.y=430;
const before=R.pools.left;const old=updateSubBoss;updateSubBoss=function(){};
pBullets=[{kind:'beam',x:player.x,w:2,dmg:7,life:.5,_hit:[],top:-20,bot:416}];try{updatePlay(1/60);}finally{updateSubBoss=old;}
return {before:before,after:R.pools.left,hp:b.hp};}"""
TLV="""()=>{spawnSubBoss('tempestbrothers');const b=subBoss,D=b._tempestDuo,p=D.ships[0],s=p._ai,g=D.ships[1];
s.enter('chase');s.boss.x=450;s.boss.y=340;s.vulnerable=true;p._jet.angle=Math.PI/2;
g._ai.boss.x=-350;g._ai.vulnerable=false;g._ai.beams=[];tempestBrothersSync(b);subBossActive=true;
const port=tempestPortXY(p,2);player.x=port.x+8;player.y=430;
const before=s.rig[2].hp,hp=s.hp,other=g._ai.hp,old=updateSubBoss;updateSubBoss=function(){};
pBullets=[{kind:'beam',x:player.x,w:2,dmg:7,life:.5,_hit:[],top:-20,bot:416}];try{updatePlay(1/60);}finally{updateSubBoss=old;}
return {before:before,after:s.rig[2].hp,hpBefore:hp,hpAfter:s.hp,grayBefore:other,grayAfter:g._ai.hp,column:player.x,port:port};}"""
BOUNDED="""()=>{const b=subBoss,D=b._tempestDuo,p=D.ships[0],g=D.ships[1];
p._ai.boss.x=450;p._ai.boss.y=340;p._ai.vulnerable=true;p._jet.angle=0;
g._ai.boss.x=450;g._ai.boss.y=700;g._ai.vulnerable=true;g._jet.angle=0;tempestBrothersSync(b);
player.x=p.x;player.y=310;const before=p._ai.hp,other=g._ai.hp,center=b.y,old=updateSubBoss;updateSubBoss=function(){};
pBullets=[{kind:'beam',x:player.x,w:2,dmg:7,life:.5,_hit:[],top:-20,bot:296}];try{updatePlay(1/60);}finally{updateSubBoss=old;}
return {before:before,after:p._ai.hp,grayBefore:other,grayAfter:g._ai.hp,aggregateCenter:center,beamEnd:296};}"""

def main():
    OUT.mkdir(parents=True,exist_ok=True);checks=[];errors=[];details={};shots=[]
    def ok(c,label):checks.append({'pass':bool(c),'label':label});print(('ok  'if c else'FAIL ')+label,flush=True)
    port,stop=shoot.serve(str(ROOT))
    with sync_playwright()as pw:
        br=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio','--autoplay-policy=no-user-gesture-required'])
        pg=br.new_page(viewport={'width':1100,'height':1200})
        snapshot=ROOT/'_shots/game_bugfix_0913/game.before.js'
        if BASELINE and snapshot.exists():pg.route('**/assets/game.js',lambda route:route.fulfill(path=str(snapshot),content_type='application/javascript'))
        pg.on('pageerror',lambda e:errors.append('page '+str(e)))
        pg.on('console',lambda m:errors.append('console '+m.text)if m.type=='error'else None)
        pg.goto('http://127.0.0.1:%d/index.html'%port,wait_until='load',timeout=120000)
        pg.wait_for_function('()=>(window.__bofFrames|0)>4',timeout=120000)
        pg.evaluate(shoot.TRAP_RAF);pg.wait_for_timeout(80)
        def step(n=2):
            e=pg.evaluate(shoot.STEP,n)
            if e:errors.append(str(e))
            pg.wait_for_timeout(10)
        def ready(prefix):
            for _ in range(100):
                if pg.evaluate('(p)=>Object.keys(BOFX.img).filter(k=>k.startsWith(p)).every(k=>XART.rdy(k))',prefix):return
                step(2);pg.wait_for_timeout(60)
            raise RuntimeError('art not ready '+prefix)
        def shot(name):
            pg.evaluate('()=>drawWorld(0)')
            raw=pg.evaluate("()=>document.getElementById('screen').toDataURL('image/png').split(',')[1]")
            p=OUT/(name+'.png');p.write_bytes(base64.b64decode(raw));shots.append(p)
        pg.evaluate(PREP,1);pg.evaluate(RZ);ready('rzb_');pg.evaluate(RZ)
        details['armor']=pg.evaluate(TRIAL,'armor');shot('razorback_armor')
        ok(details['armor']['dead']==BASELINE and details['armor']['hpBefore']==details['armor']['hpAfter'],'Razorback armor passes pellets without eating damage')
        pg.evaluate(RZ);details['gun']=pg.evaluate(TRIAL,'gun');shot('razorback_live_gun')
        ok(details['gun']['dead']and details['gun']['after']<details['gun']['before'],'a pellet still strikes a live rotated Razorback gun')
        pg.evaluate(RZ);details['transition']=pg.evaluate(TRIAL,'transition')
        ok(details['transition']['dead']==BASELINE and details['transition']['hpBefore']==details['transition']['hpAfter'],'Razorback transition armor also passes pellets')
        pg.evaluate(RZ);details['turret']=pg.evaluate(TRIAL,'turret')
        ok(details['turret']['dead']and details['turret']['after']<details['turret']['before'],'the exposed turret still takes ordinary pellet damage')
        pg.evaluate(RZ);details['razorBeam']=pg.evaluate(BEAM);shot('razorback_laser_gun')
        ok((details['razorBeam']['after']<details['razorBeam']['before'])!=BASELINE,'a real held laser reaches the exposed Razorback gun')
        pg.evaluate(PREP,6);pg.evaluate('()=>spawnSubBoss("tempestbrothers")');ready('tlv');details['tempestBeam']=pg.evaluate(TLV);shot('tempest_rotated_laser_port')
        t=details['tempestBeam']
        ok((t['after']<t['before'])!=BASELINE and t['grayBefore']==t['grayAfter'],'held laser damage follows the rotated Tempest aperture without hitting the other brother')
        details['boundedBeam']=pg.evaluate(BOUNDED);shot('tempest_finite_beam')
        t=details['boundedBeam']
        ok((t['after']<t['before'])!=BASELINE and t['grayBefore']==t['grayAfter']and t['aggregateCenter']>t['beamEnd'],'a beam reaches the visible brother while excluding a second hull beyond its endpoint')
        # Three distinct actual impacts 1.1s apart: the old 1.8s gate drops #2.
        pg.evaluate(PREP,1)
        pg.evaluate("()=>{Snd.prepare('nuclearDetonate');Snd._last.nuclearDetonate=null;window.__nukes=[];window.__nukeStart=performance.now();const f=Snd.play;window.__nukePlay=f;Snd.play=function(n,v){const accepted=f.call(this,n,v);if(n==='nuclearDetonate')window.__nukes.push({seconds:(performance.now()-window.__nukeStart)/1000,accepted:accepted});return accepted;};Audio.resume();}")
        pg.wait_for_function("()=>Snd.pools.nuclearDetonate.list[0].readyState>=3",timeout=30000)
        pg.evaluate('()=>window.__nukeStart=performance.now()')
        for i in range(3):
            pg.evaluate('(i)=>nukeAt(worldWidth()/2+(i-1)*45,200+i*30)',i);step(8);shot('cole_impact_'+str(i+1))
            if i<2:pg.wait_for_timeout(1100)
        details['nukes']=pg.evaluate('()=>window.__nukes')
        ok(sum(e['accepted']for e in details['nukes'])==(2 if BASELINE else 3),'each of three separated Cole nuclear impacts plays its detonation sound')
        details['nukeMedia']=pg.evaluate('()=>Snd.pools.nuclearDetonate.list.map(a=>({ready:a.readyState,paused:a.paused,time:a.currentTime,volume:a.volume}))')
        ok(all(a['ready']>=3 for a in details['nukeMedia']),'all nuclear sound pool voices decode in Chromium')
        if not BASELINE:
            ev=pg.evaluate('()=>({files:{nuclearDetonate:BOFA.sfx.nuclearDetonate},tame:Snd.TAME,vol:Snd.vol,voice:Snd.VOICE_SET})')
            ev.update(snd=[[1+e['seconds']*60,'nuclearDetonate',1]for e in details['nukes']if e['accepted']],rec0=1,frames=360,syn=[],warp=[],loops={},restarts=[])
            audio=pg.evaluate(render_audio.RENDER,{'ev':ev,'iife':render_audio.audio_module_source(),'tail':0,'exclude':[]})
            render_audio.write_wav_float(str(OUT/'cole_three_nukes.wav'),base64.b64decode(audio['b64']))
            details['audio']={'rms':audio['rms'],'peak':audio['peak'],'counts':audio['counts'],'errors':audio['errs']}
            ok(not audio['errs']and audio['counts']['snd']==3 and audio['rms']>0 and audio['peak']<1,'all three accepted impact samples render through the game mixer without silence or clipping')
        pg.evaluate('()=>{Snd.play=window.__nukePlay;}')
        ok(not errors,'zero page and console errors')
        br.close()
    stop()
    sheet=Image.new('RGB',(320*4,370*((len(shots)+3)//4)),'#111821')
    for i,p in enumerate(shots):
        im=Image.open(p).convert('RGB');im.thumbnail((320,342));sheet.paste(im,(i%4*320,i//4*370));ImageDraw.Draw(sheet).text((i%4*320+8,i//4*370+348),p.stem,fill='white')
    sheet.save(OUT/'contact.png')
    report={'mode':'baseline reproduction'if BASELINE else'fixed verification','checks':checks,'errors':errors,'details':details}
    (OUT/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(details),flush=True);print('%s passed / %s failed'%(sum(c['pass']for c in checks),sum(not c['pass']for c in checks)),flush=True)
    return int(any(not c['pass']for c in checks))
if __name__=='__main__':sys.exit(main())
