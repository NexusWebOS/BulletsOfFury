module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['stage8_art_1003.js','stage8_1003.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== October 3 Stage 8 generated knight and alien combat ===');
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const o={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';
 function reset(d){diffKey=d;DIFF=DIFFS[d];beginStage(8);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];player.x=worldWidth()/2;player.y=VH-115;player.invuln=1e9;boss=null;bossActive=false;subBoss=null;subBossActive=false;}
 o['100 generated frames and four crystal chunks resolve to project files']=Object.values(S81003_ART).reduce((n,a)=>n+a.frames,0)===104;
 for(const d of ['easy','normal','hard','furious']){
  reset(d);spawnBoss('vileexistence');const b=boss,S=b._r30;r30Form(b,1);S.mode='fight';b.enter=false;S.seq=1;r30Attack(b);
  o[d+' knight starts with generated transformation']=S.attack.type==='knight'&&S.attack.k1003.phase==='morph';
  for(let i=0;i<55;i++)r30Tick(b,1/60);
  const q=r30ShieldBounds(b),hp=b.hp,shield=S.shield;
  o[d+' full binary wall blocks rectangular corners']=S.shield>0&&r30At(b,q.x+q.w*.48,q.y+q.h*.48)?.id==='shield';
  b._lastPart={id:'shield'};modularHit(5);o[d+' wall absorbs damage before hull']=S.shield===shield-5&&b.hp===hp;
  o[d+' shield hits play generated impact reel']=S81003.effects.some(f=>f.kind==='impact');
  modularHit(shield+1);const shards=S81003.effects.filter(f=>f.kind==='shards');
  o[d+' shield shatters in every direction']=shards.length===16&&[0,1,2,3].every(q=>shards.some(f=>(f.vx<0?2:0)+(f.vy<0?1:0)===q));
  o[d+' break effect does not damage the unshielded hull']=b.hp===hp&&S81003.effects.some(f=>f.kind==='shatter');
  o[d+' barrier is full height and wider than knight']=q.h>=r30Parts(b)[0].h&&q.w>r30Parts(b)[0].w;
  const histStart=S.history.length;for(let i=0;i<900&&S.attack?.k1003;i++)r30Tick(b,1/60);
  const phases=S.history.slice(histStart).filter(v=>v.event==='knight1003').map(v=>v.phase);
  o[d+' complete slash jump follow-up and portal return']= ['slash','jump','land','sweep','recover','out','in'].every(p=>phases.includes(p))&&!S.attack;
  o[d+' action never grants new boss HP']=b.hp===hp;
  S.seq=3;r30Attack(b);o[d+' code wall beats use one full-body barrier']=S.attack.type==='shield';
  S.seq=1;r30Attack(b);S.shield=0;s81003KnightEnter(b,'recover');b.parts[0].destroyed=true;b.parts[0].hp=0;
  o[d+' knight retains locks after a shared health module breaks']=retinaBossTargets(b).some(t=>!t.dead&&t.hp>0);
  o[d+' recovery offers a deliberate dodge interval']=s81003KnightDur('recover')>=1.3;
  o[d+' horizontal follow-up follows landing quickly']=s81003KnightDur('followTell')<=.48;
  reset(d);
  for(const [type,role]of [['s8leech','gravity'],['s8hunter','stalker'],['s8solar','prism']]){
   enemies=[];eBullets=[];S81003.beams=[];const e=spawnEnemy(type,worldWidth()/2,110,{});let max=0,beams=0,orbs=0,last={x:e.x,y:e.y},frozen=null,stable=true;
   for(let i=0;i<850&&!e.dead;i++){s8MegaTick(e,1/60);max=Math.max(max,Math.hypot(e.x-last.x,e.y-last.y));last={x:e.x,y:e.y};
    const A=e._orbit1003;if(A.phase==='tell'&&A.locked){const l=JSON.stringify(A.lanes);if(frozen&&frozen!==l)stable=false;frozen=l;}else frozen=null;
    beams=Math.max(beams,S81003.beams.length);orbs=Math.max(orbs,eBullets.filter(q=>q._alienOrb1003).length);s81003BeamsTick(1/60);}
   o[d+' '+role+' is in existing campaign roster']=e._alien1003===role&&e._s8mega===type;
   o[d+' '+role+' smooth orbit and fixed hull']=max<2.6&&e.spin===0;
   o[d+' '+role+' locks aim before release']=stable;
   o[d+' '+role+' releases real attack']=role==='gravity'?orbs>0:beams>0;
  }
 }
 reset('normal');const e=spawnEnemy('s8stalker1003',worldWidth()/2,130,{}),L=s81003Lane(e.x,e.y,player.x,player.y,12);s81003Beam(e,L,'alien');e.dead=true;s81003BeamsTick(.01);
 o['destroying emitter cancels its active laser']=S81003.beams.length===0;
 const q=spawnEnemy('s8prism1003',worldWidth()/2,130,{});s81003Beam(q,L,'code');q._dyingT=0;s81003BeamsTick(.01);o['death animation cannot leave an orphaned beam']=S81003.beams.length===0;
 o['laser danger shares its rendered line']=s81003Distance((L.x+L.ex)/2,(L.y+L.ey)/2,L)<.001&&s81003Distance(L.x+90,L.y,L)>50;
 beginStage(1);o['stage changes clear alien beams']=S81003.beams.length===0;
 return o;})())`,ctxv));
 for(const [name,pass]of Object.entries(rows))ok(pass,name);
};
