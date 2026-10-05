module.exports=function(vm,c,ok,nativeHit){
 c.__cfNativeHit=nativeHit;
 const fs=require('fs'),path=require('path');
 for(const n of ['cole_fusion_art_1004l.js','cole_fusion_1004l.js','rebel_showcase_1004l.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/'+n),'utf8'),c,{filename:n});
 console.log('=== Cole selectable lasers, Fusion overload and stolen-tech demonstrations ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();coopOn=false;debugFight=null;run.pilot='cole';run.mode='campaign';diffKey='furious';DIFF=DIFFS.furious;
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;H3.release=false;s6Opening=null;s6Wing=null;boss=null;bossActive=false;subBoss=null;subBossActive=false;enemies=[];eBullets=[];pBullets=[];
 player.reset();run._primary1003b='mg';run.weapon=0;run.wlevel=8;run.wlevels=WEAPONS.map(()=>0);run.wlevels[0]=8;run._cfUnlocked=0;run._cfTier=null;player.x=worldWidth()/2;player.y=VH-110;
 for(const pct of [100,200,300,314]){pBullets=[];coleFuseRelease(FUSE_FULL*pct/100);const b=pBullets[0];out[pct+' percent releases two scaled real beams']=pBullets.length===2&&b._cfFusion&&Math.abs(b.scale-pct/100)<1e-7&&Math.abs(b.dmg-FUSE_DMG*pct/100)<1e-6&&!player.dead;}
 pBullets=[];coleFuseTick(.25,true);out['holding Fusion suppresses primary fire']=pBullets.length===0&&player._fuse>0;coleFuseTick(0,false);out['short release fires a weak Fusion pair']=pBullets.length===2&&pBullets[0].scale<1;
 cf1004Cancel();run.wlevel=8;out['unlocked cycle wraps VIII to VI']=cf1004Cycle()&&run.wlevel===6&&run.weapon===0;out['VI cycles VII and VII cycles VIII']=cf1004Cycle()&&run.wlevel===7&&cf1004Cycle()&&run.wlevel===8;
 coleFuseTick(.5,true);cf1004Cycle();out['switching cancels charged energy']=player._fuse===0&&run.wlevel===6;
 run._cfUnlocked=6;run.wlevels[0]=run.wlevels[7]=6;run.wlevel=6;run._cfTier=6;cf1004Cycle();out['VI alone cannot grant unearned VII or VIII']=run.wlevel===6;
 run.pilot='yuri';out['other pilots cannot change Cole arsenal']=!cf1004Cycle();run.pilot='cole';run.wlevel=8;run._cfTier=8;run.wlevels[0]=8;run._cfUnlocked=8;
 const save=campSnapshot();out['campaign save records selected and unlocked tiers']=save.coleLaserTier===8&&save.coleLaserUnlocked===8;
 const e={x:player.x,y:player.y-80,w:32,h:32,hp:1000,max:1000,type:'fighter',dead:false},near={...e,x:e.x+45};enemies=[e,near];pBullets=[];coleFuseRelease(FUSE_FULL*3);const beam=pBullets[0];beam.x=e.x;beam.cx=e.x;beam.y=e.y;beam.vy=0;cf1004BulletTick(beam,.01);
 out['real collision damages its target and splashes neighbors']=e.hp<1000&&near.hp<1000;
 out['impact makes damaging ricochets and eight shards']=pBullets.filter(q=>q._cfChild).length===10&&pBullets.filter(q=>q.kind==='colefragment').every(q=>q.dmg>0);
 const hp=e.hp;cf1004BulletTick(beam,.01);out['piercing beam cannot repeatedly damage the same hull']=e.hp===hp;
 const frag=pBullets.find(q=>q.kind==='colefragment');enemies=[{...e,x:frag.x+12,y:frag.y,hp:1000}];const target=enemies[0];frag.vx=100;frag.vy=0;cf1004BulletTick(frag,.1);out['shrapnel has actual collision damage']=target.hp<1000&&frag.dead;
 const previousHit=playerHit;playerHit=__cfNativeHit;player.invuln=999;run.shield=5;pBullets=[];player._fuse=FUSE_FULL*3.14;coleFuseTick(0,true);out['314 percent remains releasable despite danger']=!player.dead;coleFuseTick(FUSE_FULL*.01,true);out['315 percent overload bypasses shields and invulnerability']=player.dead&&run.shield===0&&pBullets.length===0;playerHit=previousHit;
 player.reset();run.pilot='cole';beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.release=false;spawnBoss('rebelsquad');const b=boss,R=b._rebels;rf28Init(b,R);b.enter=false;b._be=null;s6WingInit();s6WingLaunch(4,true);const G=rg4Init(b);
 const lines=h3RebelLines(R);out['Jace showoff is followed by the team gasp']=lines.findIndex(q=>q.demo==='gasp')===lines.findIndex(q=>q.demo==='helix')+1;
 out['Rook and Voss demonstrate their own stolen tech']=lines.some(q=>q.demo==='slug'&&q.who==='ROOK')&&lines.at(-1).demo==='turbo';
 eBullets=[];pBullets=[];const I={rows:lines,i:0,t:0,age:0};R.h3Intro=I;
 for(const demo of ['cloak','helix','slug','turbo']){I.i=lines.findIndex(q=>q.demo===demo);I.t=0;for(let i=0;i<360;i++){I.t+=1/60;rs1004DemoTick(R,I,1/60);}}
 out['all four intro demonstrations release']=RS1004.events.some(e=>e.event==='cloakDemo')&&RS1004.events.some(e=>e.event==='helixDemo')&&RS1004.events.some(e=>e.event==='slugDemo')&&RS1004.events.some(e=>e.event==='turboDemo');
 out['intro demonstrations never create colliding combat bullets']=!eBullets.length&&!pBullets.length;
 rg4Formation(G);out['shield-wave formation holds the lower arena']=G.members.every(m=>m.pin.y>=VH*.64);
 beginStage(1);setState(GS.TITLE);return out;
 })())`,c));for(const[n,v]of Object.entries(out))ok(v,n);
};
