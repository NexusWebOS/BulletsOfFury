module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/stage7_modular_0927.js'),'utf8'),ctxv);
 console.log('=== 308. Modular toxic tank and Warden ===');
 const result=JSON.parse(vm.runInContext(`(()=>{const out={};
 run.stage=7;run.mode='arcade';diffKey='normal';DIFF=DIFFS.normal;curStage=STAGES[6];
 player.dead=false;player.invuln=9999;player.x=340;player.y=410;groundTargetingReset();eBullets=[];
 function make(){const b={_ship:'sludgeemperor',hp:5000,maxhp:5000,x:340,y:160};s7WardenInit(b);s7mInit(b);s7mSet(b,'recover');b.y=175;return b;}
 let b=make(),M=b._s7mod;boss=b;bossActive=true;
 out['six independently destructible modules']=M.parts.length===6;
 out['containers never become targets']=!s7mTargets(b).some(t=>/canister/.test(t.name));
 const core=M.core,shield=M.shield;s7mHit(b,100,0,0,'core');out['legs protect both core and shield']=M.core===core&&M.shield===shield;
 const rear=M.parts.find(p=>p.id==='rearL'),rearHP=rear.hp;s7mHit(b,100,0,0,'rearL');out['rear supports locked until front pair destroyed']=rear.hp===rearHP;
 out['no shield gauge in the leg stage']=bossShieldFrac(b)===null;
 const can=s7mPose(b).find(p=>p.id==='canL'),canPos=s7mWorld(b,can),health=b.hp;
 out['canister hit region remains armored']=s7mAt(b,canPos.x,canPos.y)==='canister';s7mHit(b,500,canPos.x,canPos.y);
 out['shooting a canister cannot remove core or module health']=b.hp===health;
 s7mHit(b,1e6,0,0,'gunL');out['turret can break before any leg']=M.parts.find(p=>p.id==='gunL').hp===0&&s7mLive(M,'front').length===2;
 s7mHit(b,1e6,0,0,'frontL');s7mTick(b,.1);out['one missing front leg produces balance lean']=M.lean!==0;
 s7mHit(b,1e6,0,0,'frontR');out['second front leg triggers the drop']=M.mode==='drop'&&s7mStage(M)==='rear';
 out['rear legs now have retina locks']=s7mTargets(b).some(t=>t._retinaId==='rearL');
 s7mSet(b,'recover');s7mHit(b,1e6,0,0,'rearL');s7mHit(b,1e6,0,0,'rearR');out['both rear supports expose shield']=s7mStage(M)==='shield'&&bossShieldFrac(b)===1;
 s7mSet(b,'recover');eBullets=[];s7mHit(b,5,0,0,'core');const queued=!!M.counterTell;for(let i=0;i<50;i++)s7mHit(b,1,0,0,'core');s7mTick(b,.5);const early=eBullets.length;s7mTick(b,.56);out['shield retaliation waits for its warning and remains rate-limited']=queued&&early===0&&eBullets.length===5&&!M.counterTell;
 s7mHit(b,1e6,0,0,'core');out['shield damage never overflows into health']=M.shield===0&&M.core===core;
 M.seq=0;s7mNext(b);out['surviving turret selects retina aim phase']=M.mode==='aim';
 s7mHit(b,1e6,0,0,'gunR');M.seq=0;s7mNext(b);out['no turrets selects raised-mask laser phase']=M.mode==='laser';
 s7mTick(b,1.3);out['laser phase raises mask and fires authored beams']=M.mask>0&&eBullets.some(q=>q.kind==='s7laser');
 s7mSet(b,'recover');s7mHit(b,1e6,0,0,'core');out['core destruction starts toxic death sequence']=M.mode==='dead';
 for(const diff of ['normal','hard','furious']){
  diffKey=diff;DIFF=DIFFS[diff];b=make();M=b._s7mod;boss=b;s7mSet(b,'chase');
  const leg=M.parts.find(p=>p.id==='frontL');s7mHit(b,leg.max*.17,0,0,'frontL');out[diff+' leg focus interrupts pursuit']=M.mode==='stun';
  s7mSet(b,'jump');for(let i=0;i<120;i++)s7mTick(b,1/60);const x=M.landing.x,y=M.landing.y;player.x+=90;player.y-=50;
  for(let i=0;i<30;i++)s7mTick(b,1/60);out[diff+' landing commits before impact']=M.landing.x===x&&M.landing.y===y&&!M.landing.track;
  eBullets=[];s7mTick(b,.9);out[diff+' impact releases exactly three staggered rings']=eBullets.filter(q=>q._s7modOrb).length===36;
 }
 b=make();M=b._s7mod;boss=b;s7mSet(b,'recover');const p=s7mPose(b).find(p=>p.id==='frontL'),q=s7mWorld(b,p);out['part collision agrees with posed leg']=s7mAt(b,q.x,q.y)==='frontL';
 const beam=s7mBeamImpact(b,{x:q.x,w:5,top:0,bot:450});out['beam intersects actual visible module']=!!beam&&beam.id==='frontL';
 const tank={_ship:'dualscoopdredger',hp:100,maxhp:100,x:340,y:150};s7mInit(tank);tank.y=160;
 for(const x of [-999,999]){s7mMove(tank,x,270,9999,1);out['tank footprint stays on ground '+x]=tank.x-tank.w/2>=worldWidth()*.345-.01&&tank.x+tank.w/2<=worldWidth()*.655+.01;}
 return JSON.stringify(out);})()`,ctxv));
 for(const [name,pass]of Object.entries(result))ok(pass,'Stage 7 modular: '+name);
};
