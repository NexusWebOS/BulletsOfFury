module.exports=function(vm,ctxv,ok){
 /* 0928 - Mike: "ensure the fury fight is great for stage 6". The REBEL FURY squad (the right-hand
    route's boss) gets role signatures, squad formations, loss reactions, a last stand and difficulty
    shields. Behaviour is asserted by driving the squad's own tick; nothing reads a function's source. */
 const fs=require('fs'),path=require('path');
 for(const [file,sentinel] of [['furious_review_0927.js','FR27_REBEL_TICK'],['rebel_fury_0928.js','RF28_K']])
   if(vm.runInContext('typeof '+sentinel,ctxv)==='undefined')
     vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),ctxv,{filename:file});
 console.log('=== 375. Rebel Fury squad: signatures, formations, losses, shields ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
  const o={};let hits=0;const realHit=playerHit;playerHit=function(){hits++;};
  function fight(diff,duel){
    diffKey=diff;DIFF=DIFFS[diff];run.mode='arcade';run.pilot='maverick';coopOn=false;
    beginStage(6);setState(GS.PLAY);story=null;special=null;enemies=[];eBullets=[];pBullets=[];
    boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=true;
    s6Opening=null;s6WingInit();s6Wing.choice=true;s6Wing.route='right';s6Wing.fakeDone=true;s6Wing.all=true;s6Wing.beats=2;s6Wing.supplyIndex=3;
    if(typeof tb28Reset==='function')tb28Reset();groundTargetingReset();
    player.x=camLeftX()+viewW()/2;player.y=VH*.8;player.dead=false;player.invuln=0;hits=0;
    spawnBoss('rebelsquad');bossActive=true;const b=boss,R=b._rebels;
    if(duel){R.frStageX=true;for(const q of R.ships)q.dead=q.i!==1;}
    const maxBefore=b.maxhp;
    rebelSquadTick(b,1/60);                       // first tick builds the layer
    R.frIntro={t:29,beat:4,done:true};b._noHit=false;R.t=0;R.releaseAt=0;
    for(const q of R.ships){if(q.dead)continue;q.x=q.homeX;q.y=q.homeY;q.mode='fight';q.t=0;q.cd=5;}
    return {b,R,maxBefore};
  }
  function run(b,sec){for(let i=0;i<Math.round(sec*60);i++){rebelSquadTick(b,1/60);tb28Tick(1/60);groundTargetingTick(1/60);
    for(const z of eBullets)if(!z.dead){z.x+=z.vx;z.y+=z.vy;}eBullets=eBullets.filter(z=>!z.dead&&z.y<VH+80&&z.y>-120&&z.x>-200&&z.x<worldWidth()+200);}}
  const ship=(R,k)=>R.ships.find(q=>q.key===k);

  /* ---- difficulty shape ---- */
  let F=fight('normal');
  o['Normal: no rebel carries a shield']=F.R.ships.every(q=>!(q.shieldMax>0));
  o['the layer trims squad hull 10% (it evades and dashes off screen now)']=Math.abs(F.b.maxhp-Math.round(F.maxBefore*.9))<=1;
  F=fight('hard');
  o['Hard: the leader alone is shielded']=ship(F.R,'voss').shieldMax>0&&F.R.ships.filter(q=>q.shieldMax>0).length===1;
  F=fight('furious');
  o['Furious: the whole squad is shielded']=F.R.ships.every(q=>q.shieldMax>0&&q.shield===q.shieldMax);

  /* ---- signatures come from each rebel's roster role ---- */
  const want={voss:'talons',nyx:'knife',rook:'hammer',kaia:'cage',jace:'razor'};let sigs=0;
  for(const k in want){F=fight('normal');const q=ship(F.R,k);q.rfForce=true;fr27RebelAttack(q,F.R);if(q.rfSig&&q.rfSig.kind===want[k])sigs++;}
  o['every rebel has its own signature (talons, knife, hammer, cage, razor)']=sigs===5;
  F=fight('normal');let q=ship(F.R,'voss');q.rfN=0;
  const s1=fr27RebelAttack(q,F.R)&&!!q.rfSig,s2=fr27RebelAttack(q,F.R)&&!!q.rfSig;q.rfSig=null;q.rfN=2;const s3=fr27RebelAttack(q,F.R)&&q.rfSig&&q.rfSig.kind==='talons';
  o['Normal: a signature is every third turn, not every turn']=!s1&&!s2&&!!s3;

  /* IRON TALONS: committed targeted balls, one per knob, landing around where the pilot was */
  F=fight('furious');q=ship(F.R,'voss');q.rfForce=true;fr27RebelAttack(q,F.R);
  const talons=tb28List.filter(z=>z.owner===q);
  o['Iron Talons fires five committed targeted balls on Furious']=talons.length===5&&talons.every(z=>z.mode==='direct'&&z.phase==='warn');
  o['the talons spread around the pilot and each carries a landing burst']=new Set(talons.map(z=>Math.round(z.tx))).size===5&&talons.every(z=>z.burst&&z.burst.n===8);

  /* GHOSTKNIFE: the lane commits, a late dodge does not move it, she dashes through and re-enters */
  F=fight('normal');q=ship(F.R,'nyx');q.rfForce=true;fr27RebelAttack(q,F.R);run(F.b,.6);
  const S=q.rfSig,dx=S&&S.dx,dy=S&&S.dy;player.x+=140;run(F.b,.5);
  o['Ghostknife commits its lane and a late dodge does not steer it']=!!S&&S.dx===dx&&S.dy===dy;
  let dashed=false,back=false;for(let i=0;i<180;i++){run(F.b,1/60);if(q.rfSig&&q.rfSig.phase==='dash')dashed=true;if(q.mode==='entry'){back=true;break;}}
  o['she dashes through it and re-enters from above, untargetable']=dashed&&back&&q.y<0;

  /* BREACH HAMMER: Furious slams twice, each slam a ring of rounds (an explosion: no lane) */
  F=fight('furious');q=ship(F.R,'rook');q.rfForce=true;fr27RebelAttack(q,F.R);let slams=0;
  for(let i=0;i<300&&q.rfSig;i++){run(F.b,1/60);if(q.rfSig)slams=Math.max(slams,q.rfSig.slam);}
  o['Breach Hammer slams twice on Furious']=slams===1&&!q.rfSig;   // the counter reads 1 between slams; the second ends the move
  F=fight('furious');q=ship(F.R,'rook');q.rfForce=true;fr27RebelAttack(q,F.R);let ringRounds=0;const seen=new Set();
  for(let i=0;i<300&&q.rfSig;i++){run(F.b,1/60);for(const z of eBullets)if(!seen.has(z)){seen.add(z);if(z.kind==='s6orb')ringRounds++;}}
  o['the two slams throw 12 + 10 ring rounds']=ringRounds===22;

  /* SIGNAL CAGE: a fixed ring of strikes around the pilot, a spike in the centre, an exit gap */
  F=fight('normal');q=ship(F.R,'kaia');q.rfForce=true;const gt0=groundTargetingFx.length;fr27RebelAttack(q,F.R);
  const cage=groundTargetingFx.slice(gt0).filter(g=>g.owner===q);
  o['Signal Cage rings the pilot with fixed strikes and a centre spike']=cage.length>=6&&cage.every(g=>!g.lane&&!g.track)&&cage.some(g=>g.radius>=28);
  const c=cage.find(g=>g.radius>=28),angs=cage.filter(g=>g!==c).map(g=>Math.atan2(g.y-c.y,g.x-c.x)).sort((a,b)=>a-b);
  let gap=0;for(let i=0;i<angs.length;i++){const d=(i+1<angs.length?angs[i+1]:angs[0]+Math.PI*2)-angs[i];gap=Math.max(gap,d);}
  o['the cage leaves an exit gap wider than its spacing']=gap>Math.PI*2/(angs.length+2)*1.6;

  /* RAZOR RUN: a committed row, a stick of rounds spaced by the difficulty knob */
  F=fight('hard');q=ship(F.R,'jace');q.rfForce=true;fr27RebelAttack(q,F.R);const row=q.rfSig.y;const drops=[];const seen2=new Set();
  for(let i=0;i<400&&q.rfSig;i++){run(F.b,1/60);for(const z of eBullets)if(!seen2.has(z)){seen2.add(z);if(z.kind==='s6tracer'&&Math.abs(z.vx)<.01&&Math.abs(z.y-(row+16))<12)drops.push(z.x);}}
  drops.sort((a,b)=>a-b);const gaps=drops.slice(1).map((x,i)=>x-drops[i]);
  o['Razor Run drops a stick of rounds along its committed row']=drops.length>=6&&gaps.every(g=>g>=40)&&q.rfSig===null;
  o['the run row was committed from the pilot, above them']=row<player.y;

  /* ---- formations ---- */
  F=fight('furious');F.R.rf.formNext=0;F.R.rf.cycle=1;   // Furious cycle: fivepoint, wall, pincer
  run(F.b,1/60);let Fm=F.R.rf.form;
  o['a formation forms up when its clock comes round']=!!Fm&&Fm.kind==='wall';
  const xs=Fm.ships.map(s=>Fm.slots.get(s).x);
  o['Wall of Fury lines the squad in columns']=new Set(xs.map(Math.round)).size===Fm.ships.length&&Math.min(...xs.slice(1).map((x,i)=>x-xs[i]))>60;
  o['while it forms, no ship takes its own turn']=F.R.releaseAt>F.R.t+100;
  const cols=new Set();const seen3=new Set();for(let i=0;i<600&&F.R.rf.form;i++){run(F.b,1/60);for(const z of eBullets)if(!seen3.has(z)){seen3.add(z);if(Math.abs(z.vx)<.01&&z.vy>0)cols.add(Math.round(z.x));}}
  o['Furious walls sweep three times (columns shift between volleys)']=cols.size>=Fm.ships.length*3-2&&!F.R.rf.form;
  F=fight('furious');F.R.rf.formNext=0;F.R.rf.cycle=2;player.y=PLAY.y+PLAY.h-10;run(F.b,1/60);Fm=F.R.rf.form;
  const top=bottomHudLayout().radar.y-26;
  o['Pincer sends only the two outer ships to the edges']=Fm.kind==='pincer'&&Fm.ships.length===2&&Fm.slots.get(Fm.ships[0]).x<camLeftX()+40&&Fm.slots.get(Fm.ships[1]).x>camRightX()-40;
  o['the pincer row stays above the radar/lock HUD box']=Fm.y<=top;
  F=fight('hard');F.R.rf.formNext=0;F.R.rf.cycle=1;run(F.b,1/60);Fm=F.R.rf.form;
  for(let i=0;i<120&&Fm.phase==='move';i++)run(F.b,1/60);
  const five=tb28List.filter(z=>Fm.ships.includes(z.owner));
  o['Five-Point Lock converges committed balls on one point, landing together']=Fm.kind==='fivepoint'&&five.length===5&&five.every(z=>z.tx===five[0].tx&&z.ty===five[0].ty&&z.warm===five[0].warm&&z.flight===five[0].flight);
  F=fight('normal');o['Normal never opens the Fury Spiral']=RF28_CYCLE[0].indexOf('spiral')<0&&F.R.rf.lvl===0;
  F=fight('furious');F.b.hp=F.b.maxhp*.4;F.R.rf.formNext=0;run(F.b,1/60);
  o['Furious opens the REBEL FURY spiral below 45% squad health']=!!F.R.rf.form&&F.R.rf.form.kind==='spiral';
  let spiralRounds=0;const seen4=new Set();for(let i=0;i<400&&F.R.rf.form;i++){run(F.b,1/60);for(const z of eBullets)if(!seen4.has(z)){seen4.add(z);spiralRounds++;}}
  o['the spiral fires outward rounds and releases the squad']=spiralRounds>=60&&!F.R.rf.form;

  /* ---- losses ---- */
  F=fight('normal');const R=F.R;const rook=ship(R,'rook');R.hit=rook.i;R.frHit=null;rebelSquadDamage(F.b,rook.hp+5);run(F.b,1/60);
  o['a fallen rebel is answered: survivors force their signature']=rook.dead&&R.rf.fallen.includes('rook')&&R.ships.filter(s=>!s.dead).every(s=>s.rfForce||s.rfSig);
  o['the squad speaks on the compact HUD comm, not the play-area panel']=!!R.rf.comm&&R.rf.comm.text.indexOf('ROOK')>=0;
  o['and flies faster as it loses pilots']=rf28PaceMul(R,ship(R,'voss'))<1;
  F=fight('furious');for(const k of ['rook','kaia','jace','voss']){const s=ship(F.R,k);F.R.hit=s.i;F.R.frHit=null;s.shield=0;rebelSquadDamage(F.b,s.hp+5);run(F.b,1/60);}
  const nyx=ship(F.R,'nyx');
  o['the last rebel makes a stand with its shield back on Furious']=F.R.rf.lastStand&&!nyx.dead&&nyx.shield>0&&nyx.shield>=nyx.shieldMax*.99;
  nyx.rfN=0;nyx.rfSig=null;const pool=new Set();for(let i=0;i<6;i++){nyx.rfSig=null;nyx.rfForce=false;fr27RebelAttack(nyx,F.R);if(nyx.rfSig)pool.add(nyx.rfSig.kind);nyx.rfSig=null;tb28Reset();groundTargetingReset();}
  o['on Furious the last stand inherits the fallen signatures']=pool.size>=4;
  o['formations stop once one rebel is left']=(F.R.rf.formNext=0,run(F.b,1/60),!F.R.rf.form);

  /* ---- shields ---- */
  F=fight('furious');const v=ship(F.R,'voss');F.R.hit=v.i;F.R.frHit='left';const mod=fr27RebelModules(v)[0].hp;rebelSquadDamage(F.b,5);
  o['a shield covers the modules too']=fr27RebelModules(v)[0].hp===mod&&v.shield===v.shieldMax-5;
  F.R.hit=v.i;F.R.frHit=null;rebelSquadDamage(F.b,v.shield+1);
  const broke=v.shield===0;for(const s of F.R.ships)s.stun=0;F.R.t=v.rfShieldDownAt+7;F.R.rf.formNext=0;run(F.b,1/60);
  const re1=v.shield;rf28FormEnd(F.b,F.R);
  v.shield=0;v.rfShieldDownAt=F.R.t-10;for(const s of F.R.ships){s.stun=0;s.rfSig=null;s.frCast=null;}F.R.rf.formNext=0;run(F.b,1/60);
  o['a broken shield comes back once, at a formation, and never again']=broke&&re1===Math.round(v.shieldMax*.6)&&!!F.R.rf.form&&v.shield===0;

  /* ---- Stage X duel ---- */
  F=fight('normal',true);F.R.rf.formNext=0;run(F.b,2);
  o['the Stage X duel keeps signatures and skips formations']=!F.R.rf.form&&F.R.ships.filter(s=>!s.dead).length===1;

  /* ---- the draw survives every state ---- */
  let threw=null;try{F=fight('furious');F.R.rf.formNext=0;run(F.b,1);rebelSquadDraw(F.b);s6WingRadioDraw();
    const k=ship(F.R,'nyx');k.rfForce=true;fr27RebelAttack(k,F.R);run(F.b,1);rebelSquadDraw(F.b);}catch(e){threw=String(e&&e.stack||e);}
  o['the squad draws in every state without throwing']=threw===null;
  playerHit=realHit;
  return o;
 })())`,ctxv));
 for(const k in result)ok(result[k],'Rebel Fury 0928: '+k);
};
