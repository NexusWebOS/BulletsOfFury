module.exports=function(vm,ctxv,ok){
 /* 0928 - Mike: "better FOV warnings but not when stuff is going to explode, only that the ball is
    coming where its targeted like a magma ball", Normal/Hard upgrades and Furious extra phases for the
    Stage 2-7 minibosses and bosses. Behaviour is asserted; nothing here reads a function's source. */
 const fs=require('fs'),path=require('path');
 // Earlier sections load these add-ons into the shared context; a second run of a file redeclares its
 // consts (SyntaxError). Load each only when its own sentinel is absent, so the section also runs alone.
 for(const [file,sentinel] of [['stage3_thermo.js','S3_THERMO_STRIKE'],['encounters_0926.js','ER26_STAGE'],['stage7_modular_0927.js','S7M_ART']])
   if(vm.runInContext('typeof '+sentinel,ctxv)==='undefined')
     vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',file),'utf8'),ctxv,{filename:file});
 console.log('=== 374. Targeted-ball warnings and the Stage 2-7 encounter upgrades ===');
 const result=JSON.parse(vm.runInContext(`(()=>{
  const out={};
  function reset(stage,diff){run.stage=stage;run.mode='arcade';run.pilot='cole';curStage=STAGES[stage-1];diffKey=diff;DIFF=DIFFS[diff];
    boss=null;subBoss=null;bossActive=false;subBossActive=false;enemies=[];eBullets=[];pBullets=[];powerups=[];explosions=[];particles=[];
    camX=0;player.x=340;player.y=410;player.dead=false;player.invuln=0;tb28Reset();groundTargetingReset();}
  let hits=0;const realHit=playerHit;playerHit=function(){hits++;};

  /* ---- the shared targeted ball ---- */
  reset(2,'normal');
  const owner={x:340,y:120,w:100,h:80,hp:10,maxhp:10,t:0};
  let arrived=null,burst=0;
  const q=tb28Fire(owner,{from:()=>({x:owner.x,y:owner.y+30}),target:{x:250,y:380},warm:.5,flight:.5,mode:'direct',art:'magma',er26Art:'fire',
    shot:()=>{burst++;},burst:{n:8,speed:2,gap:.36},onArrive:(b,x,y)=>{arrived={x,y};}});
  player.x=520;player.y=460;
  out['a targeted ball commits to its point and waits out its warning']=q.phase==='warn'&&q.tx===250&&q.ty===380;
  for(let i=0;i<32;i++)tb28Tick(1/60);   // 30 ticks of 1/60 sum to just under .5 in floating point
  out['after the warning it is a real round on the lane (tagged with its element)']=q.phase==='flight'&&!!q.ball&&eBullets.includes(q.ball)&&q.ball._er26Art==='fire';
  const len=Math.hypot(250-340,380-150);
  out['the lane length is the muzzle-to-target distance']=Math.abs(q.len-len)<1;
  for(let i=0;i<60&&!arrived;i++){tb28Tick(1/60);for(const b of eBullets)if(!b.dead&&b._tb28){b.x+=b.vx;b.y+=b.vy;}}
  out['it lands exactly on the committed point']=!!arrived&&arrived.x===250&&arrived.y===380;
  out['its burst leaves an escape sector toward the pilot']=burst>0&&burst<8;
  out['a burst never leaves the ball behind']=!eBullets.some(b=>b===q.ball&&!b.dead);
  // a lob is harmless in the air and splashes where it lands
  reset(2,'normal');hits=0;player.x=300;player.y=400;
  const lob=tb28Fire(owner,{from:{x:300,y:100},target:{x:300,y:400},warm:.2,flight:.4,mode:'lob',art:'magma',splash:30});
  for(let i=0;i<20;i++)tb28Tick(1/60);
  out['a lob in flight is airborne, not a collidable round']=lob.phase==='flight'&&!eBullets.length&&hits===0;
  for(let i=0;i<40;i++)tb28Tick(1/60);
  out['a lob splashes the pilot where it lands']=lob.arrived&&hits===1;
  // an owner that dies takes its pending balls with it
  reset(2,'normal');const gone=tb28Fire(owner,{from:{x:1,y:1},target:{x:300,y:300},warm:1});owner.dead=true;tb28Tick(1/60);
  out['a dead launcher cancels its pending warnings']=!tb28List.length;owner.dead=false;

  /* ---- Stage 2-4 director: books, conversions and the Furious overdrive ---- */
  function fixture(kind,stage,diff){
    reset(stage,diff);const mini=kind==='magmaward'||kind==='frostcruiser'||kind==='olivewarden';
    if(mini)spawnSubBoss__inner(kind);else spawnBoss(kind);
    const b=mini?subBoss:boss;b.enter=false;b._be=null;b._noHit=false;b.x=worldWidth()/2;b.y=b._er26.home;
    b._er26.from={x:b.x,y:b.y};b._er26.to={x:b.x,y:b.y};b._drawY=b.y;b._er26.neutralOpening=false;return b;
  }
  const want={magmaward:['magma-rain','ash-rain'],frostcruiser:['ice-lob','ice-lob'],cryospear:['ice-lob','ice-lob'],olivewarden:['shell-lob','shell-lob'],stormsovereign:['storm-orbs','storm-orbs']};
  const od={magmaward:['ash-meteor','reaver-dive'],frostcruiser:['hail-meteor','cruiser-ram'],cryospear:['hail-meteor'],olivewarden:['shell-barrage'],stormsovereign:['chain-storm','giant-strike']};
  for(const [kind,stage] of [['magmaward',2],['frostcruiser',3],['cryospear',3],['olivewarden',4],['stormsovereign',4]]){
    const n=fixture(kind,stage,'normal');
    out[kind+' Normal adds its targeted-ball attack']=er26Book(n).includes(want[kind][0])&&!od[kind].some(m=>er26Book(n).includes(m));
    const f=fixture(kind,stage,'furious'),R=f._er26;
    out[kind+' Furious keeps its lob before overdrive']=er26Book(f).includes(want[kind][1])&&!od[kind].some(m=>er26Book(f).includes(m));
    R.mode='recover';f.hp=f.maxhp*.99;er28PhaseCheck(f);
    out[kind+' Furious does not overdrive above its threshold']=!R.od;
    if(f._s4war&&f._s4war.shield)f._s4war.shield.rearming=false;
    f.hp=f.maxhp*.3;R.mode='recover';er28PhaseCheck(f);
    out[kind+' Furious overdrive fires once, invulnerable']=R.od&&R.mode==='overdrive'&&f._noHit;
    for(let i=0;i<120;i++){f.t=(f.t||0)+1/60;er26Tick(f,1/60);}
    out[kind+' overdrive ends in a vulnerable, faster second book']=!f._noHit&&od[kind].every(m=>er26Book(f).includes(m));
    // the targeted attacks really fire tb28 balls (no generic lanes)
    tb28Reset();er26Set(f,want[kind][1]);for(let i=0;i<180;i++){f.t+=1/60;er26Tick(f,1/60);}
    out[kind+' '+want[kind][1]+' fires committed targeted balls']=tb28List.length>0&&tb28List.every(q=>q.owner===f&&Number.isFinite(q.tx)&&Number.isFinite(q.ty));
    // the Normal fight holds on hard-bounded motion across a long run, as the 0926 revision requires
    const b=fixture(kind,stage,'hard');let old={x:b.x,y:b.y},bounded=true;const seen=new Set();
    for(let i=0;i<1800;i++){b.t=(b.t||0)+1/60;er26Tick(b,1/60);seen.add(b._er26.mode);bounded=bounded&&Number.isFinite(b.x)&&Math.hypot(b.x-old.x,b.y-old.y)<15;old={x:b.x,y:b.y};if(i%120===0){eBullets=[];tb28Reset();}}
    out[kind+' Hard runs its upgraded book with bounded movement']=bounded&&seen.size>=4;
  }
  // the split orb's burst is an explosion: the director draws no radial fan for it any more
  {const b=fixture('magmaward',2,'normal'),R=b._er26;R.seeds=[{q:{x:300,y:300,dead:false},t:.2,at:1.35,form:'fire'}];eBullets.push(R.seeds[0].q);
   let fans=0;const cwd=combatWarningDraw;combatWarningDraw=function(){fans++;};try{er26Draw(b);}finally{combatWarningDraw=cwd;}
   out['no FOV fan is drawn for a split orb about to burst']=fans===0;}

  /* ---- bombers ---- */
  for(const [stage,kind] of [[5,'spacebomber'],[6,'siegebomber']]){
    reset(stage,'furious');spawnSubBoss__inner(kind);const b=subBoss,B=b._bomber;b.enter=false;B.mode='recover';B.t=0;
    siegeBomberSet(b,'lob');for(let i=0;i<5;i++)siegeBomberTick(b,1/60);
    out[kind+' flak lob fires targeted balls from the bay']=tb28List.length===4&&tb28List.every(q=>q.owner===b);
    b.hp=b.maxhp*.45;B.mode='recover';B.t=99;B.dur=0;siegeBomberTick(b,1/60);
    out[kind+' Furious crosses into overdrive at half']=B.od&&B.mode==='overdrive';
    const hp=b.hp;siegeBomberHit(b,500,b.x,b.y,'core');out[kind+' overdrive beat is invulnerable']=b.hp===hp;
    tb28Reset();siegeBomberSet(b,'carpet');siegeBomberTick(b,1/60);
    const xs=tb28List.map(q=>q.tx).sort((a,c)=>a-c);
    out[kind+' carpet run leaves exactly one open cell']=tb28List.length===6&&tb28List.every(q=>q.mode==='lob');
  }

  /* ---- Warhive ---- */
  reset(6,'normal');s6Opening=null;s6Wing=null;spawnBoss('warhive');let W=boss._whv;
  W.st='hold';W.t=0;W.cy=WHV_HOME_Y;W.doorOpen=true;W.launched=W.jetN;W.mortarCast=false;
  for(let i=0;i<50;i++)warhiveTick(boss,1/60);
  out['Warhive Normal carrier lobs a bay mortar during its hold']=tb28List.length===2&&tb28List.every(q=>q.mode==='lob');
  reset(6,'hard');s6Opening=null;s6Wing=null;spawnBoss('warhive');W=boss._whv;W.st='hold';W.t=.61;W.cy=WHV_HOME_Y;W.doorOpen=true;W.launched=W.jetN;W.mortarCast=true;W.can.i=0;W.can.cd=0;
  warhiveTick(boss,1/60);out['Warhive Hard flurry is five targeted balls']=tb28List.length===5;
  reset(6,'furious');s6Opening=null;s6Wing=null;spawnBoss('warhive');W=boss._whv;W.st='hold';W.t=.61;W.cy=WHV_HOME_Y;W.doorOpen=true;W.launched=W.jetN;W.mortarCast=true;
  boss.hp=boss.maxhp*.45;warhiveTick(boss,1/60);W.can.i=1;W.can.cd=0;warhiveTick(boss,1/60);
  out['Warhive Furious scramble adds the twin beam with a centre gap']=W.od&&!!W.beam&&!!W.beam2&&W.beam.side!==W.beam2.side;

  /* ---- Stage 7 ---- */
  reset(7,'normal');
  function make7(ship){const b={_ship:ship,hp:5000,maxhp:5000,x:340,y:160};if(ship==='sludgeemperor')s7WardenInit(b);s7mInit(b);s7mSet(b,'recover');b.y=b.ty;return b;}
  let t7=make7('dualscoopdredger');subBoss=t7;
  const tb=[];for(let i=0;i<10;i++){t7._s7mod.seq=i;s7mNext(t7);tb.push(t7._s7mod.mode);}
  out['Caustic tank book gains the caustic lob']=tb.includes('caustic-lob')&&!tb.includes('sludge-wall');
  s7mSet(t7,'caustic-lob');s7mTick(t7,1/60);out['caustic lob fires targeted toxic balls']=tb28List.length===2&&tb28List.every(q=>q.art==='toxic');
  reset(7,'furious');t7=make7('dualscoopdredger');subBoss=t7;t7.hp=t7.maxhp*.45;s7mNext(t7);
  out['Furious tank overpressure at half, invulnerable']=t7._s7mod.od&&t7._s7mod.mode==='overdrive'&&s7mAt(t7,t7.x,t7.y)===null;
  s7mSet(t7,'sludge-wall');eBullets=[];for(let i=0;i<60;i++)s7mTick(t7,1/60);
  out['sludge wall rows keep a two-column gap']=eBullets.filter(q=>q._s7mWall).length===6;
  reset(7,'furious');let w7=make7('sludgeemperor');boss=w7;const M7=w7._s7mod;for(const p of M7.parts)if(!p.id.startsWith('gun'))p.hp=0;M7.shield=0;
  s7mNext(w7);out['Furious Warden core opens portal feedback']=M7.od&&M7.mode==='overdrive';
  s7mSet(w7,'portal-volley');s7mTick(w7,1/60);out['portal feedback fires targeted balls from three portals']=tb28List.length===6&&new Set(tb28List.map(q=>q.ox)).size===3;

  playerHit=realHit;tb28Reset();groundTargetingReset();boss=null;subBoss=null;bossActive=false;subBossActive=false;
  return JSON.stringify(out);
 })()`,ctxv));
 for(const [name,pass] of Object.entries(result))ok(pass,'Encounter upgrades 0928: '+name);
};
