module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['combat_art_1003i.js','combat_1003i.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== October 3i modular Reaver and generated combat feedback ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';diffKey='normal';DIFF=DIFFS.normal;
 beginStage(2);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;spawnSubBoss__inner('magmaward');const b=subBoss;b.enter=false;b._noHit=false;b.x=worldWidth()/2;b.y=170;b._drawY=b.y;
 const gun=av3Part(b,'gunL'),right=av3Part(b,'gunR'),hp=b.hp;
 av3ReaverHit(b,25,b.x,b.y,'gunL');
 out['ordinary damage preserves hull damage, isolates struck gun and keeps its neighbor intact']=b.hp<hp&&gun.hp<gun.maxhp&&right.hp===right.maxhp&&gun.flash>0&&right.flash===0;
 l23BossBeamStart(b,'inferno',['L','R'],[Math.PI/2,Math.PI/2],1,1,.2,25);av3Break(b,gun);const count=eBullets.length;er26Shot(b,'L',Math.PI/2,3,{});
 out['destroying an active gun cancels only its beam and forbids future shots']=b._l23Beam.slots.length===1&&b._l23Beam.slots[0]==='R'&&eBullets.length===count&&!mr27CanFire(b,'L')&&mr27CanFire(b,'R');
 const p=shipBossMount(b,'C');av3Break(b,av3Part(b,'nose'));er26Shot(b,p,Math.PI/2,3,{});
 out['object hardpoints cannot bypass a destroyed nose weapon']=eBullets.length===count;
 const old=av3Part(b,'wingL').rot;er26Tick(b,.12);out['surviving modules retain independent movement']=av3Part(b,'wingL').rot!==old;
 out['destroyed guns disappear from lock candidates']=!retinaBossTargets(b).some(t=>t._retinaId==='reaver-gunL');
 out['empty finite beam range is safely rejected']=subBossBeamImpact(b,{x:b.x,top:200,bot:100,w:12})===null;
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;s6Opening=null;s6Wing=null;run.pilot='cole';run.weapon=0;run.wlevel=8;pBullets=[];AV3.last.clear();coleFuseRelease();
 out['Fusion keeps its two piercing lances and dedicated release cue']=pBullets.filter(q=>q.kind==='colefuse'&&q.pierce).length===2&&AV3.events.at(-1)?.cue==='fusion_cannon';
 const n=AV3.events.length;for(let i=0;i<20;i++)av3Sound('target_acquire',1,.5);out['one warning volley cannot layer twenty copies of the acquisition sound']=AV3.events.length<=n+1;
 return out;})())`,ctxv));
 for(const [n,v]of Object.entries(result))ok(v,n);
 const masters=JSON.parse(fs.readFileSync(path.join(__dirname,'../assets/game/combat_1003i/audio-masters.json'),'utf8'));
 ok(masters.length===20&&masters.every(m=>m.clippedSamples===0&&m.peak<.9),'twenty mastered generated cues have headroom and no clipped decoded samples');
};
