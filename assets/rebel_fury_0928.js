/* ============================================================
   REBEL FURY 0928 - the Stage 6 right-hand route's boss, made a squad fight.

   Mike 0928: "ensure the fury fight is great for stage 6", in the same pass as "upgrades,
   adjustments, better FOV warnings ... only that the ball is coming where its targeted" on Normal,
   Hard and Furious, and "on Furious, they should all get extra abilities, attacks, patterns, phases".

   Measured before this layer (probe_rebel_fury_0928, Normal, four allies): a 90 s fight after the 29 s
   radio intro in which five ships hovered in a line and took single turns from one shared list - the
   same fan / lightning / dash / cast whichever rebel it was, 0-6 rounds on screen, nothing changing as
   the squad died, Furious differing only in HP and cooldown. This layer gives the squad what a squad
   fight is for:

     SIGNATURES  one per rebel, from the roster's own roles (roaming_rebels_0922/roster.json):
                 VOSS leader       IRON TALONS   targeted heavy balls, committed lanes (tb28)
                 NYX infiltrator   GHOSTKNIFE    cloak, a committed lane, then a dash through it
                 ROOK enforcer     BREACH HAMMER column slam + shock ring (Hard+: a second slam)
                 KAIA signal       SIGNAL CAGE   a ring of lightning strikes round the pilot + the spike
                 JACE interceptor  RAZOR RUN     a strafing run across the pilot's row, a stick of rounds
     FORMATIONS  called by the squad: WALL OF FURY (columns, sweeping), PINCER (edge streams),
                 FIVE-POINT (Hard+, converging targeted balls), FURY SPIRAL (Furious ultimate).
     LOSSES      a survivor answers on the radio, the squad speeds up, and every survivor's next turn
                 is its signature; the last rebel makes a stand (Hard+ with its shield back).
     SHIELDS     Hard: Voss. Furious: the whole squad, restored as a formation forms up.

   Warnings follow the 0928 rule: a targeted ball or a committed dash/strafe path shows its lane; an
   explosion (the slam's ring, the cage's strikes) shows only its own reticle/art. Everything is the
   authored art already in the build: rr_ship / roll reels, xorb stills through tb28, s6tracer/s6orb
   rounds, the lightning ground strikes, the nes_bubble shell palette-swapped per rebel.
   Stage X (Rival24, one rebel) keeps the signatures and skips formations, radio and the last stand.
   ============================================================ */
const RF28_K={
  formFirst:[11,9,7], formEvery:[22,17,13],
  sigEvery:[3,2,2],                      // a ship's Nth turn is its signature
  sigBlock:[99,1.6,1.0],                 // seconds a signature holds the other ships' turns
  venge:[.93,.89,.85],                   // cooldown multiplier per fallen rebel
  talons:[3,4,5], talonBurst:[0,6,8],
  knifeWake:[false,true,true], hammerDouble:[false,true,true], hammerRing:[8,10,12],
  cageN:[9,10,12], cageWarn:[1.25,1.05,.92], cageOuter:[false,false,true],
  razorGap:[54,44,36], razorWarn:[.95,.82,.72],
  wallSweeps:[1,2,3], wallWarn:[1.05,.9,.78], pincerRounds:[5,6,8],
  shield:[0,.22,.22]
};
const RF28_CYCLE=[['wall','pincer'],['wall','fivepoint','pincer'],['fivepoint','wall','pincer']];
const RF28_SIG={voss:'talons',nyx:'knife',rook:'hammer',kaia:'cage',jace:'razor'};
const RF28_SIG_NAME={talons:'IRON TALONS',knife:'GHOSTKNIFE',hammer:'BREACH HAMMER',cage:'SIGNAL CAGE',razor:'RAZOR RUN'};
const RF28_FORM_NAME={wall:'WALL OF FURY',pincer:'PINCER',fivepoint:'FIVE-POINT LOCK',spiral:'REBEL FURY'};
const RF28_ORB={voss:'antimatter',nyx:'gravity',rook:'kinetic',kaia:'solar',jace:'lightning'};
if(typeof TB28_ART!=='undefined'&&!TB28_ART.kinetic)TB28_ART.kinetic={still:'xorb_kinetic_rock',spin:1.2};
/* Radio lines are the squad's voice in this layer. They are one table so Mike can rewrite them. */
const RF28_LINES={
  form:{wall:'WALL OF FURY! FORM ON ME!',pincer:'PINCER! CUT THEM OFF!',fivepoint:'FIVE-POINT LOCK. EVERY GUN ON THE ACE.',spiral:'ALL SHIPS - FULL FURY!'},
  fallen:{voss:'VOSS IS DOWN! NO MORE ORDERS. ONLY FURY!',nyx:'NYX! YOU WILL BURN FOR THAT!',rook:'ROOK IS DOWN! MAKE THEM PAY FOR IT!',
    kaia:'KAIA IS GONE. WE ARE FLYING BLIND!',jace:'JACE! DAMN YOU, FURY!'},
  last:{voss:'THEY WERE MY FAMILY. NOW YOU FACE ME ALONE.',nyx:'YOU CANNOT HIT WHAT YOU CANNOT SEE.',rook:'COME ON THEN. I WILL BREAK YOU MYSELF.',
    kaia:'EVERY SIGNAL YOU SEND, I HEAR IT.',jace:'CATCH ME IF YOU CAN, FURY.'}
};
const RF28_SPEAK=['voss','nyx','kaia','jace','rook'];
function rf28Lvl(){return typeof ai27Level==='function'?ai27Level():(diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0);}
function rf28Easy(){return diffKey==='easy';}
function rf28Alive(R){return R.ships.filter(q=>!q.dead);}
function rf28Duel(R){return !!R.frStageX;}
function rf28Speaker(R){for(const k of RF28_SPEAK){const q=R.ships.find(s=>s.key===k&&!s.dead);if(q)return q;}return null;}
/* Mid-fight lines go to the compact comm in the reserved HUD bay - the treatment the engine's own
   squad radio used ("combat chatter shares the reserved HUD bay; it never follows the player over
   attack tells"). The big dialogue panel stays for the calm intro: drawn in the play area it sat
   across the Wall of Fury's lanes in the first proof. */
function rf28Say(R,who,text){if(!who||!text||!R.rf)return;R.rf.comm={who:who.toLowerCase(),text,t:0,dur:text.length/34+1.9,drawCount:0};XART.rdy('rr_portrait_'+who.toLowerCase());}
function rf28CommDraw(){
  if(!bossActive||!boss||!boss._rebels||!boss._rebels.rf)return;
  const R=boss._rebels,C=R.rf.comm;if(!C||typeof bottomHudLayout!=='function'||typeof dialogueFrameDraw!=='function')return;
  const r=bottomHudLayout().ability,count=Math.min(C.text.length,Math.floor(C.t*34)),i=REBEL_KEYS.indexOf(C.who),tint=i>=0?REBEL_TINT[i]:'#ff9a8a';
  if(typeof dialogueLetterTicks==='function')dialogueLetterTicks(C.text,C.drawCount||0,count);C.drawCount=count;
  ctx.save();ctx.globalAlpha=1;ctx.imageSmoothingEnabled=false;
  dialogueFrameDraw(C.who.toUpperCase(),tint,r.x,r.y,r.w,r.h);
  const pk='rr_portrait_'+C.who;if(XART.rdy(pk))ctx.drawImage(XART.get(pk),r.x+6,r.y+7,32,32);
  if(typeof msgFaceUse==='function')msgFaceUse('dialogue');const x=r.x+44,w=r.w-54;
  if(typeof pilotNameDraw==='function')pilotNameDraw(C.who.toUpperCase(),x+w/2,r.y+11,8,tint,1);
  if(typeof msgDrawBlock==='function')msgDrawBlock({text:C.text,budget:count,x,y:r.y+20,w,h:23,maxH:8,minH:8,lineMul:1.35,color:'#ffffff',alpha:1,align:'left',outline:false});
  if(typeof msgFaceUse==='function')msgFaceUse(null);ctx.restore();
}
function rf28Callout(R,text,x,y,color,dur,size){R.rf.callouts.push({text,x,y:Math.max(PLAY.y-14,y),color:color||'#ffe6b0',t:0,dur:dur||1.1,size:size||9});}
function rf28Banner(R,text,color){R.rf.banner={text,color:color||'#ffb4a3',t:0,dur:1.6};(Audio.SFX.alertBossIncoming||Audio.SFX.alert)?.();}
function rf28Contact(x,y,r){
  for(const s of seatList())withSeat(s,()=>{if(!player.dead&&player.invuln<=0&&Math.hypot(player.x-x,player.y-y)<r)playerHit();});
}
function rf28FieldL(){return camLeftX();}
function rf28FieldR(){return camRightX();}
function rf28Clamp(x,y,m){const l=camLeftX()+(m||34),r=camRightX()-(m||34);return {x:clamp(x,Math.min(l,r),Math.max(l,r)),y:clamp(y,PLAY.y+54,PLAY.y+PLAY.h-40)};}
/* one cooldown knob for the base tick (game.js hook): the squad hurries as it loses pilots */
function rf28PaceMul(R,q){
  if(!R||!R.rf||rf28Duel(R))return 1;
  let m=Math.pow(RF28_K.venge[rf28Lvl()],R.rf.fallen.length);
  if(R.rf.lastStand)m*=.82;
  return m;
}
function rf28Init(b,R){
  const lvl=rf28Lvl();
  R.rf={lvl,formNext:RF28_K.formFirst[lvl]*(rf28Easy()?1.3:1),form:null,cycle:0,fallen:[],lastStand:false,said:{},
    callouts:[],banner:null,spiralOpen:false,rollBeat:0,introRolls:{}};
  const frac=RF28_K.shield[lvl];
  /* the squad now evades, dashes off screen (untargetable re-entry) and carries shields: measured
     +20% fight length on Normal and Furious with the same bot, so the hulls give back 10% */
  if(!rf28Duel(R)){for(const q of R.ships){q.max=Math.round(q.max*.9);q.hp=Math.min(q.hp,q.max);}b.maxhp=Math.round(b.maxhp*.9);b.hp=Math.min(b.hp,b.maxhp);}
  for(const q of R.ships){
    q.rfN=0;q.rfForce=false;q.rfSig=null;q.rfHeading=null;
    const on=!rf28Duel(R)&&frac>0&&(lvl>=2||q.key==='voss');
    if(on){q.shieldMax=Math.round(q.max*frac);q.shield=q.shieldMax;q.rfShieldDownAt=null;}
  }
  if(lvl>=1||rf28Duel(R))XART.rdy('nes_bubble_0');
  for(const k of ['antimatter','gravity','kinetic','solar','lightning'])if(typeof tb28Warm==='function')tb28Warm(k);
}

/* ---------- the intro: the squad arrives in a V, weaves while it talks, and breaks to its slots ---------- */
const RF28_V=[[0,0],[-62,-36],[62,-36],[-124,-72],[124,-72]];
function rf28IntroTick(b,R,dt){
  const I=R.frIntro;if(!I)return;const t=I.t,alive=rf28Alive(R),cx=camLeftX()+viewW()/2;
  for(const q of alive){
    q.evadeT=Math.max(0,(q.evadeT||0)-dt);
    if(t>=25){ /* the break: fr27's own drift carries each ship to its slot; each one rolls out of the V */
      if(!R.rf.introRolls[q.key]&&t>=25+q.i*.16){R.rf.introRolls[q.key]=1;q.evadeT=.38;}
      continue;}
    const o=alive.length===1?[0,0]:(RF28_V[q.i]||[0,0]);
    let tx,ty;
    if(t<4){const e=clamp(t/4,0,1),k=1-(1-e)*(1-e);tx=cx+o[0];ty=lerp(-120,VH*.30,k)+o[1];}
    else{const u=t-4;tx=cx+o[0]+Math.sin(u*.42)*viewW()*.15;ty=VH*.30+o[1]+Math.sin(u*.84)*12;}
    q.x=tx;q.y=ty;
  }
  /* whoever just spoke on the radio rolls, so the line has a face in the formation */
  if((I.beat||0)>R.rf.rollBeat){R.rf.rollBeat=I.beat;const L=(s6Wing&&s6Wing.line)||(R.frRadio);
    const who=L&&L.who?L.who.toLowerCase():null,q=who&&R.ships.find(s=>s.key===who&&!s.dead);if(q)q.evadeT=.38;}
}

/* ---------- signatures ---------- */
function rf28SigKind(q,R){
  if(R.rf.lastStand&&R.rf.lvl>=2&&R.rf.fallen.length){
    const pool=[RF28_SIG[q.key],...R.rf.fallen.map(k=>RF28_SIG[k])];return pool[(q.rfN||0)%pool.length];
  }
  return RF28_SIG[q.key]||'talons';
}
function rf28TrySignature(q,R){
  if(!R.rf||R.rf.form)return false;
  q.rfN=(q.rfN||0)+1;
  const every=rf28Duel(R)?2:R.rf.lastStand?(R.rf.lvl>=1?1:2):RF28_K.sigEvery[R.rf.lvl];
  if(!(q.rfForce||q.rfN%every===0))return false;
  q.rfForce=false;rf28SigStart(q,R,rf28SigKind(q,R));return true;
}
function rf28SigStart(q,R,kind){
  const lvl=R.rf.lvl,S={kind,t:0,phase:'warn',hold:false,lanes:[]};q.rfSig=S;q.cd=Math.max(q.cd,3);
  rf28Callout(R,RF28_SIG_NAME[kind],q.x,q.y-70,REBEL_TINT[q.i],1.2,9);
  Audio.SFX.bossWeaponCharge?.();
  if(kind==='talons'){
    const n=RF28_K.talons[lvl]-(rf28Easy()?1:0),burst=RF28_K.talonBurst[lvl];S.balls=[];
    for(let j=0;j<n;j++){const off=(j-(n-1)/2)*54,side=j%2?1:-1;
      S.balls.push(tb28Fire(q,{from:()=>({x:q.x+side*18,y:q.y+30}),target:{x:player.x+off,y:player.y},warm:1.0+j*.14,flight:.62,mode:'direct',
        art:RF28_ORB[q.key]||'antimatter',size:30,width:34,silent:j>0,kind:'s6orb',
        shot:burst?(x,y,a,spd)=>{const z=eShootT(x,y,a,spd,'s6orb',{w:13,h:13,silent:true});z._noArsenal=true;}:null,
        burst:burst?{n:burst,speed:2.2,gap:.52}:null,
        onRelease:()=>{if(typeof stage6Muzzle==='function')stage6Muzzle(q,side*.15,.25,.9,.16);Audio.SFX.enemyHeavyLaser?.();}}));}
    S.dur=1.0+(n-1)*.14+.3;
  }else if(kind==='knife'){S.hold=true;S.dur=99;}
  else if(kind==='hammer'){S.hold=true;S.dur=99;S.x0=q.x;S.y0=q.y;S.slams=RF28_K.hammerDouble[lvl]?2:1;S.slam=0;}
  else if(kind==='cage'){
    const c=rf28Clamp(player.x,player.y,80),n=RF28_K.cageN[lvl],warn=RF28_K.cageWarn[lvl]*(rf28Easy()?1.15:1);
    /* the exit gap faces open field: toward the screen's centre line, up or down alternating */
    const mid=camLeftX()+viewW()/2,gapA=Math.atan2(((q.rfN||0)&1?-1:1)*.55,c.x<mid?1:-1);
    const floor=PLAY.y+PLAY.h-4,pts=[];for(let j=0;j<n;j++){const a=gapA+(j+1.5)*TAU/(n+2),y=c.y+Math.sin(a)*76;if(y<=floor)pts.push({x:c.x+Math.cos(a)*76,y});}
    groundTargetingPattern('lightning',pts,{owner:q,stagger:.03,warn,active:.42,radius:19,size:62,track:false,lane:false});
    groundTargetingSpawn({kind:'lightning',x:c.x,y:c.y,owner:q,warn:warn+.02,active:.46,radius:28,size:86,track:false,lane:false});
    if(RF28_K.cageOuter[lvl]){const pts2=[];for(let j=0;j<n+4;j++){const a=gapA+Math.PI+(j+1.5)*TAU/(n+6),y=c.y+Math.sin(a)*128;if(y<=floor)pts2.push({x:c.x+Math.cos(a)*128,y});}
      groundTargetingPattern('lightning',pts2,{owner:q,stagger:.02,warn:warn+.38,active:.40,radius:19,size:62,track:false,lane:false});}
    if(typeof stage6Muzzle==='function')stage6Muzzle(q,0,.25,.8,.2);
    S.dur=warn+.5;S.cx=c.x;S.cy=c.y;
  }else if(kind==='razor'){
    S.hold=true;S.dur=99;const mid=camLeftX()+viewW()/2;S.dir=q.x<mid?1:-1;   // exits by the near edge, crosses toward the far one
    S.y=clamp(player.y-150,PLAY.y+86,PLAY.y+PLAY.h*.52);S.phase='exit';
  }
}
function rf28SigTick(q,R,dt){
  const S=q.rfSig;if(!S)return;S.t+=dt;const lvl=R.rf.lvl;
  if(q.dead){q.rfSig=null;q.rfHeading=null;return;}
  if(q.stun>0&&S.kind!=='talons'&&S.kind!=='cage'){rf28SigEnd(q,R,true);return;}
  q.cd=Math.max(q.cd,.5);
  if(S.t<RF28_K.sigBlock[lvl])R.releaseAt=Math.max(R.releaseAt||0,R.t+.25);
  if(S.kind==='talons'||S.kind==='cage'){if(S.t>=S.dur)rf28SigEnd(q,R);return;}
  if(S.kind==='knife'){
    if(S.phase==='warn'){
      q.frCloak=Math.max(q.frCloak||0,.2);
      if(S.t>=.45&&S.ax==null){S.ax=q.x;S.ay=q.y+18;const T=rf28Clamp(player.x,player.y,20);
        const dx=T.x-S.ax,dy=T.y-S.ay,d=Math.hypot(dx,dy)||1;S.dx=dx/d;S.dy=dy/d;S.tx=T.x;S.ty=T.y;S.warm=.85*(rf28Easy()?1.2:1);S.wt=0;}
      if(S.ax!=null){S.wt+=dt;combatWarningTick(q,'rf28-knife',Math.min(S.wt,S.warm),S.warm);
        if(S.wt>=S.warm){S.phase='dash';S.dt=0;S.travel=0;q.frCloak=0;Audio.SFX.dash?.();q.rfHeading=Math.atan2(S.dy,S.dx);}}
      return;
    }
    if(S.phase==='dash'){
      const v=980*dt;q.x+=S.dx*v;q.y+=S.dy*v;S.travel+=v;rf28Contact(q.x,q.y,30);
      if(RF28_K.knifeWake[lvl]&&S.travel>=58){S.travel-=58;
        for(const s of [-1,1]){const a=Math.atan2(S.dy,S.dx)+s*Math.PI/2,z=eShootT(q.x,q.y,a,1.8,'s6tracer',{w:6,h:16,silent:true});z._noArsenal=true;}}
      if(q.y>VH+70||q.x<camLeftX()-80||q.x>camRightX()+80||q.y<-90){rf28Reenter(q,R);}
      return;
    }
    return;
  }
  if(S.kind==='hammer'){
    if(S.phase==='warn'){
      const warm=(S.slam?.7:.9)*(rf28Easy()?1.2:1);
      if(S.slam&&S.tx!=null)q.x+=clamp(S.tx-q.x,-700*dt,700*dt);
      combatWarningTick(q,'rf28-hammer-'+S.slam,Math.min(S.t,warm),warm);
      if(S.t>=warm){S.phase='dash';S.t=0;Audio.SFX.dash?.();S.x0=q.x;}
      return;
    }
    if(S.phase==='dash'){
      q.y+=470*dt;rf28Contact(q.x,q.y,36);
      if(S.t>=.55||q.y>=PLAY.y+PLAY.h-30){
        /* the slam is an explosion: art and a ring of rounds, no lane */
        const n=RF28_K.hammerRing[lvl]-(S.slam?2:0),off=S.slam*.31;
        for(let j=0;j<n;j++){const a=off+j*TAU/n,z=eShootT(q.x,q.y+20,a,2.05,'s6orb',{w:14,h:14,silent:j>0});z._noArsenal=true;}
        if(typeof fxBurst==='function')fxBurst(q.x,q.y+14,70,{color:REBEL_TINT[q.i],rings:2,chunks:4,sparks:12});
        if(typeof spawnSmokeRing==='function')spawnSmokeRing(q.x,q.y+14,40);
        shake=Math.max(shake,5);Audio.SFX.expBig?.();
        S.slam++;
        if(S.slam<S.slams){S.phase='rise';S.t=0;}else rf28SigEnd(q,R);
      }
      return;
    }
    if(S.phase==='rise'){
      q.y-=240*dt;if(S.t>=.38){S.phase='warn';S.t=0;S.tx=rf28Clamp(player.x,q.y,40).x;}
      return;
    }
    return;
  }
  if(S.kind==='razor'){
    const edgeL=camLeftX()-56,edgeR=camRightX()+56,start=S.dir>0?edgeL:edgeR,end=S.dir>0?edgeR:edgeL;
    if(S.phase==='exit'){
      const dx=start-q.x,dy=S.y-q.y,d=Math.hypot(dx,dy);q.rfHeading=Math.atan2(dy,dx);
      const v=Math.min(d,560*dt);if(d>1){q.x+=dx/d*v;q.y+=dy/d*v;}
      if(d<4||S.t>1.6){q.x=start;q.y=S.y;S.phase='warn';S.t=0;q.rfHeading=S.dir>0?0:Math.PI;q.warp=0;}
      return;
    }
    if(S.phase==='warn'){
      const warm=RF28_K.razorWarn[lvl]*(rf28Easy()?1.2:1);
      combatWarningTick(q,'rf28-razor',Math.min(S.t,warm),warm);
      if(S.t>=warm){S.phase='run';S.t=0;S.drop=0;Audio.SFX.dash?.();}
      return;
    }
    if(S.phase==='run'){
      const v=620*dt;q.x+=S.dir*v;S.drop+=v;rf28Contact(q.x,q.y,32);
      const gap=RF28_K.razorGap[lvl]+(rf28Easy()?10:0);
      const onScreen=q.x>camLeftX()+8&&q.x<camRightX()-8;if(!onScreen)S.drop=Math.min(S.drop,gap);   // no banked distance: two rounds on one frame at the entry edge
      if(S.drop>=gap&&onScreen){S.drop-=gap;
        const z=eShootT(q.x,q.y+16,Math.PI/2,4.2,'s6tracer',{w:8,h:22,silent:true});z._noArsenal=true;
        if(typeof stage6Muzzle==='function')stage6Muzzle(q,0,.25,.55,.08);}
      if(S.dir>0?q.x>=end:q.x<=end)rf28Reenter(q,R);
      return;
    }
  }
}
/* a ship that left the screen on a dash comes back in from above; 'entry' is untargetable and the
   base tick flies it to its slot, then hands it back to the fight */
function rf28Reenter(q,R){
  q.rfSig=null;q.rfHeading=null;q.frCloak=0;q.x=q.homeX;q.y=-70;q.mode='entry';q.t=0;q.evadeT=0;q.cd=Math.max(q.cd,1.1);
  R.releaseAt=Math.max(R.releaseAt||0,R.t+.6);
}
function rf28SigEnd(q,R,aborted){
  q.rfSig=null;q.rfHeading=null;q.frCloak=0;q.cd=Math.max(q.cd,2.2*(rf28Easy()?1.3:1)*rf28PaceMul(R,q));
  if(q.mode!=='entry')q.mode='fight';
  R.releaseAt=Math.max(R.releaseAt||0,R.t+(aborted?.4:.7));
}

/* ---------- formations ---------- */
function rf28FormReady(b,R){
  if(rf28Duel(R)||R.rf.form||R.rf.lastStand)return false;
  const alive=rf28Alive(R);if(alive.length<2)return false;
  if(R.t<R.rf.formNext)return false;
  /* hold the turns so the field clears, then form up */
  R.releaseAt=Math.max(R.releaseAt||0,R.t+.5);
  return !alive.some(q=>q.rfSig||q.frCast||q.mode==='charge'||q.mode==='entry'||q.stun>0);
}
function rf28FormPick(b,R){
  const lvl=R.rf.lvl;
  if(lvl>=2&&!R.rf.spiralOpen&&b.hp<=b.maxhp*.45){R.rf.spiralOpen=true;return 'spiral';}
  const cyc=RF28_CYCLE[lvl].concat(R.rf.spiralOpen?['spiral']:[]);
  return cyc[(R.rf.cycle++)%cyc.length];
}
function rf28FormStart(b,R,kind){
  const lvl=R.rf.lvl,alive=rf28Alive(R).sort((a,c)=>a.x-c.x);
  const F={kind,t:0,phase:'move',ships:alive,hold:true,slots:new Map(),step:0};R.rf.form=F;R.releaseAt=R.t+999;
  for(const q of alive){q.cd=Math.max(q.cd,1.5);q.evadeT=0;}
  rf28Banner(R,RF28_FORM_NAME[kind],'#ffb4a3');
  if(!R.rf.said[kind]){R.rf.said[kind]=1;const s=rf28Speaker(R);if(s)rf28Say(R,s.key,RF28_LINES.form[kind]);}
  /* Furious: a formation is the squad's moment to bring shields back up */
  /* once per rebel: a second layer, not a wall that rebuilds every formation (measured: regen on every
     formation held Furious to one kill in 240 s) */
  if(lvl>=2)for(const q of alive)if(q.shieldMax>0&&q.shield<=0&&!q.rfRegen&&q.rfShieldDownAt!=null&&R.t-q.rfShieldDownAt>=6){
    q.shield=Math.round(q.shieldMax*.6);q.rfShieldDownAt=null;q.rfRegen=true;rf28Callout(R,'SHIELD UP',q.x,q.y-64,'#9fe9ff',1,8);Audio.SFX.shieldUp?.();}
  const L=camLeftX(),Rr=camRightX(),W=Rr-L,n=alive.length;
  if(kind==='wall'){F.sweeps=RF28_K.wallSweeps[lvl];F.sp=n>1?(W-120)/(n-1):0;
    alive.forEach((q,j)=>F.slots.set(q,{x:n>1?L+60+j*F.sp:L+W/2,y:PLAY.y+74+(j%2)*10}));}
  else if(kind==='pincer'){const top=typeof bottomHudLayout==='function'?bottomHudLayout().radar.y-26:PLAY.y+PLAY.h-120,yp=clamp(player.y,PLAY.y+150,Math.max(PLAY.y+150,top));F.y=yp;F.pair=[alive[0],alive[alive.length-1]];
    /* only the two outer ships dive; the rest keep flying their own drift (their turns stay held) */
    F.ships=F.pair.slice();F.slots.set(F.pair[0],{x:L+34,y:yp});F.slots.set(F.pair[1],{x:Rr-34,y:yp});}
  else if(kind==='fivepoint'){const P=rf28Clamp(player.x,player.y,40);F.px=P.x;F.py=P.y;
    /* the arc spans +/-187 px of a 480 view, so it hangs from the screen's centre; the lanes still
       converge on the pilot (an arc centred on a pilot at the edge clamped three ships into one pile) */
    const ax=L+W/2;alive.forEach((q,j)=>{const a=-Math.PI*(n>1?(.84-.68*j/(n-1)):.5),p=rf28Clamp(ax+Math.cos(a)*215,P.y+Math.sin(a)*215,40);
      F.slots.set(q,{x:p.x,y:Math.min(p.y,P.y-150)});});}
  else if(kind==='spiral'){F.cx=L+W/2;F.cy=PLAY.y+130;F.dir=(R.rf.cycle&1)?-1:1;F.ang=0;
    alive.forEach((q,j)=>{const a=j*TAU/n-Math.PI/2;F.slots.set(q,{x:F.cx+Math.cos(a)*72,y:F.cy+Math.sin(a)*72*.8});});
    if(typeof fxBurst==='function')fxBurst(F.cx,F.cy,90,{color:'#ff5a4a',rings:2,chunks:0,sparks:10});}
  Audio.SFX.bossWeaponCharge?.();
}
function rf28FormMove(F,dt,speed){
  let done=true;
  for(const q of F.ships){if(q.dead)continue;const p=F.slots.get(q);if(!p)continue;
    const dx=p.x-q.x,dy=p.y-q.y,d=Math.hypot(dx,dy),v=Math.min(d,(speed||520)*dt);
    if(d>1.5){q.x+=dx/d*v;q.y+=dy/d*v;done=false;}}
  return done;
}
function rf28FormTick(b,R,dt){
  const F=R.rf.form;if(!F)return;F.t+=dt;const lvl=R.rf.lvl;
  F.ships=F.ships.filter(q=>!q.dead);
  if(!F.ships.length){rf28FormEnd(b,R);return;}
  for(const q of F.ships){q.cd=Math.max(q.cd,1);q.evadeT=0;}
  if(F.phase==='move'){
    const done=rf28FormMove(F,dt,F.kind==='spiral'?420:540);
    if(F.kind==='pincer')for(const q of F.pair)if(!q.dead){const p=F.slots.get(q);q.rfHeading=Math.atan2(p.y-q.y,p.x-q.x);if(Math.hypot(p.x-q.x,p.y-q.y)<4)q.rfHeading=p.x<camLeftX()+viewW()/2?0:Math.PI;}
    if(done||F.t>1.5){F.phase='warn';F.t=0;
      if(F.kind==='fivepoint'){const burst=lvl>=2?8:0;
        F.ships.forEach((q,j)=>tb28Fire(q,{from:()=>({x:q.x,y:q.y+26}),target:{x:F.px,y:F.py},warm:1.05,flight:.78,mode:'direct',
          art:RF28_ORB[q.key]||'plasma',size:28,width:30,silent:j>0,kind:'s6orb',
          shot:burst?(x,y,a,spd)=>{const z=eShootT(x,y,a,spd,'s6orb',{w:13,h:13,silent:true});z._noArsenal=true;}:null,
          burst:burst?{n:burst,speed:2.1,gap:.5}:null,
          onRelease:()=>{if(typeof stage6Muzzle==='function')stage6Muzzle(q,0,.25,.8,.14);}}));
        F.until=1.05+.78+.4;}
    }
    return;
  }
  if(F.kind==='wall'){
    const warm=RF28_K.wallWarn[lvl]*(rf28Easy()?1.2:1);
    if(F.phase==='warn'){F.ships.forEach((q,j)=>combatWarningTick(q,'rf28-wall',Math.min(F.t,warm),warm,j>0));
      if(F.t>=warm){F.phase='fire';F.t=0;F.shots=0;}return;}
    if(F.phase==='fire'){
      const per=5,gap=.16;
      if(F.shots<per&&F.t>=F.shots*gap){F.shots++;
        F.ships.forEach((q,j)=>{const z=eShootT(q.x,q.y+30,Math.PI/2,5.2,'s6tracer',{w:8,h:22,silent:j>0});z._noArsenal=true;
          if(typeof stage6Muzzle==='function')stage6Muzzle(q,0,.25,.7,.08);});}
      if(F.t>=per*gap+.25){F.step++;
        /* each sweep walks the columns a third of their spacing the same way, so the gaps move and
           three sweeps give three different lanes (an alternating shift repeats the first) */
        if(F.step<F.sweeps){F.phase='shift';F.t=0;if(F.dir==null)F.dir=F.ships[0].x-camLeftX()>camRightX()-F.ships[F.ships.length-1].x?-1:1;const s=F.dir*F.sp/3;
          for(const q of F.ships){const p=F.slots.get(q);F.slots.set(q,{x:clamp(p.x+s,camLeftX()+36,camRightX()-36),y:p.y});}}
        else rf28FormEnd(b,R);}
      return;}
    if(F.phase==='shift'){const done=rf28FormMove(F,dt,380);
      F.ships.forEach((q,j)=>combatWarningTick(q,'rf28-wall',Math.min(F.t,warm*.8),warm*.8,j>0));
      if(done&&F.t>=warm*.8){F.phase='fire';F.t=0;F.shots=0;}return;}
  }
  if(F.kind==='pincer'){
    const warm=.9*(rf28Easy()?1.2:1);
    if(F.phase==='warn'){for(const q of F.pair)if(!q.dead)combatWarningTick(q,'rf28-pincer',Math.min(F.t,warm),warm,q!==F.pair[0]);
      if(F.t>=warm){F.phase='fire';F.t=0;F.shots=0;}return;}
    if(F.phase==='fire'){const per=RF28_K.pincerRounds[lvl],gap=.14;
      if(F.shots<per&&F.t>=F.shots*gap){F.shots++;
        for(const q of F.pair){if(q.dead)continue;const a=q.x<camLeftX()+viewW()/2?0:Math.PI,z=eShootT(q.x+Math.cos(a)*30,q.y,a,4.6,'s6tracer',{w:8,h:22,silent:q!==F.pair[0]});z._noArsenal=true;}}
      if(F.t>=per*gap+.3)rf28FormEnd(b,R);return;}
  }
  if(F.kind==='fivepoint'){if(F.t>=(F.until||2))rf28FormEnd(b,R);return;}
  if(F.kind==='spiral'){
    if(F.phase==='warn'){ /* the charge: the ring tightens and turns before it fires - no lane, it is not aimed */
      F.ang+=F.dir*.9*dt;rf28SpiralPlace(F);if(F.t>=1.2){F.phase='fire';F.t=0;F.fireCd=0;Audio.SFX.enemyHeavyLaser?.();}return;}
    if(F.phase==='fire'){
      F.ang+=F.dir*1.1*dt;rf28SpiralPlace(F);F.fireCd-=dt;
      if(F.fireCd<=0){F.fireCd=.2;
        F.ships.forEach((q,j)=>{const a=Math.atan2(q.y-F.cy,q.x-F.cx),z=eShootT(q.x+Math.cos(a)*18,q.y+Math.sin(a)*18,a,2.3,'s6orb',{w:12,h:12,silent:j>0||F.t%.6>.2});z._noArsenal=true;});}
      if(F.t>=3.2)rf28FormEnd(b,R);return;}
  }
}
function rf28SpiralPlace(F){
  const n=F.ships.length;
  F.ships.forEach((q,j)=>{const a=F.ang+j*TAU/n-Math.PI/2;q.x=F.cx+Math.cos(a)*72;q.y=F.cy+Math.sin(a)*72*.8;q.rfHeading=a+F.dir*Math.PI/2;});
}
function rf28FormEnd(b,R){
  const F=R.rf.form;if(F)for(const q of F.ships){q.rfHeading=null;q.cd=Math.max(.6,Math.min(q.cd,1.2+q.i*.25));}
  R.rf.form=null;R.releaseAt=R.t+.9;
  R.rf.formNext=R.t+RF28_K.formEvery[R.rf.lvl]*(rf28Easy()?1.3:1);
}

/* ---------- losses ---------- */
function rf28Fallen(b,R,q){
  R.rf.fallen.push(q.key);
  if(typeof spawnSmokeRing==='function')spawnSmokeRing(q.x,q.y,52);   // jets get the mid-speed smoke ring (house rule)
  if(rf28Duel(R)||b.dead)return;
  const alive=rf28Alive(R);if(!alive.length)return;
  const s=rf28Speaker(R);
  rf28Callout(R,q.key.toUpperCase()+' DOWN',q.x,q.y-40,REBEL_TINT[q.i],1.4,10);
  for(const a of alive)a.rfForce=true;
  if(R.rf.form&&R.rf.form.ships.length<2)rf28FormEnd(b,R);
  if(alive.length===1){
    const last=alive[0];R.rf.lastStand=true;
    rf28Banner(R,'LAST STAND - '+last.key.toUpperCase(),REBEL_TINT[last.i]);
    rf28Say(R,last.key,RF28_LINES.last[last.key]||'');
    if(R.rf.lvl>=1){last.shieldMax=Math.max(last.shieldMax||0,Math.round(last.max*(R.rf.lvl>=2?.25:.20)));last.shield=last.shieldMax;last.rfShieldDownAt=null;}
    last.cd=Math.min(last.cd,.8);
  }else if(s)rf28Say(R,s.key,RF28_LINES.fallen[q.key]||'');
}

/* ---------- the wrappers ---------- */
const RF28_BASE={tick:rebelSquadTick,draw:rebelSquadDraw,damage:rebelSquadDamage,attack:fr27RebelAttack,ship:fr27RebelDrawShip};
fr27RebelAttack=function(q,R){
  if(R&&R.rf&&!R.rf.form&&rf28TrySignature(q,R))return true;
  return RF28_BASE.attack(q,R);
};
rebelSquadTick=function(b,dt){
  const R=b._rebels;if(!R)return RF28_BASE.tick(b,dt);
  if(!R.rf)rf28Init(b,R);
  const introDone=!!(R.frIntro&&R.frIntro.done);
  /* ships under a formation or a held signature fly this layer's path, not the base drift */
  const held=[];
  if(introDone)for(const q of R.ships){if(q.dead)continue;
    if((q.rfSig&&q.rfSig.hold)||(R.rf.form&&R.rf.form.hold&&R.rf.form.ships.includes(q)))held.push([q,q.x,q.y]);}
  RF28_BASE.tick(b,dt);
  for(const [q,x,y] of held){if(q.mode==='entry')continue;q.x=x;q.y=y;q.evadeT=0;}
  if(!introDone||!(R.frIntro&&R.frIntro.done)){rf28IntroTick(b,R,dt);return;}
  if(b.dead){for(const q of R.ships){q.rfSig=null;q.rfHeading=null;}R.rf.form=null;return;}
  for(const q of R.ships)if(q.dead&&!q.rfSeenDead){q.rfSeenDead=true;q.rfSig=null;q.rfHeading=null;rf28Fallen(b,R,q);}
  if(rf28FormReady(b,R))rf28FormStart(b,R,rf28FormPick(b,R));
  rf28FormTick(b,R,dt);
  for(const q of R.ships)if(!q.dead&&q.rfSig)rf28SigTick(q,R,dt);
  for(const c of R.rf.callouts)c.t+=dt;R.rf.callouts=R.rf.callouts.filter(c=>c.t<c.dur);
  if(R.rf.banner){R.rf.banner.t+=dt;if(R.rf.banner.t>=R.rf.banner.dur)R.rf.banner=null;}
  if(R.rf.comm){R.rf.comm.t+=dt;if(R.rf.comm.t>=R.rf.comm.dur)R.rf.comm=null;}
};
rebelSquadDamage=function(b,dmg){
  const R=b._rebels,q=R&&R.ships[R.hit];
  const shielded=!!(q&&q.shield>0);
  /* a shield covers the modules too: route the whole hit to it */
  if(shielded)R.frHit=null;
  RF28_BASE.damage(b,dmg);
  if(shielded&&q.shield<=0&&R.rf){q.rfShieldDownAt=R.t;rf28Callout(R,'SHIELD DOWN',q.x,q.y-64,'#9fe9ff',1,8);}
  if(shielded&&q.shield>0)q.rfShieldHitT=.18;
};
fr27RebelDrawShip=function(q){
  const f=q.evadeT>0?Math.min(7,Math.floor((1-q.evadeT/.38)*8)):0,key='rr_roll_'+REBEL_SHIPS[q.i]+'_'+f;
  const k=XART.rdy(key)?key:'rr_ship_'+REBEL_SHIPS[q.i];if(!XART.rdy(k))return;
  const pitch=q.frSomersault&&q.evadeT>0&&q.rfHeading==null&&XART.rdy('fr27_rebel_pitch');const im=XART.get(pitch?'fr27_rebel_pitch':k);
  const cw=pitch?im.width/4:im.width,ch=pitch?im.height/5:im.height,sx=pitch?Math.min(3,Math.floor(f/2))*cw:0,sy=pitch?q.i*ch:0;
  const w=SHIP_DRAW_H*1.5,h=pitch?w:w*ch/cw;
  ctx.save();ctx.translate(q.x,q.y);if(q.rfHeading!=null)ctx.rotate(q.rfHeading-Math.PI/2);ctx.imageSmoothingEnabled=false;
  ctx.globalAlpha=q.frCloak>0?.22+.12*Math.sin(q.t*22):1;
  /* a strobe (10 Hz, 55%) rather than a held tint: the squad takes fire from four allies and the
     pilot at once, and a held tint turned the focused rebel into a white silhouette in the proof */
  let hot=!pitch&&q.flash>0&&Math.floor((q.t||0)*20)%2===0&&typeof xartTint==='function'?xartTint(k,'#ffffff',.9):null;if(hot&&!(hot.width>0))hot=null;
  for(const[a,z,id]of [[0,.33,'left'],[.33,.67,null],[.67,1,'right']]){if(id&&fr27RebelModules(q).find(p=>p.id===id).hp<=0)continue;
    ctx.drawImage(im,sx+a*cw,sy,(z-a)*cw,ch,-w/2+a*w,-h/2,(z-a)*w,h);
    /* every hit flashes (0912y) - fr27's sliced draw had dropped the base draw's white flash */
    if(hot){ctx.save();ctx.globalAlpha*=.55*clamp(q.flash/.13,0,1);ctx.drawImage(hot,a*cw,0,(z-a)*cw,ch,-w/2+a*w,-h/2,(z-a)*w,h);ctx.restore();}}
  ctx.restore();
  if(q.frCast)combatWarningDraw(q,{x:q.x,y:q.y+28,ex:q.frCast.tx,ey:q.frCast.ty,progress:q.frCast.t/1.1,width:q.frCast.kind==='orb'?75:28,alpha:.30});
};
function rf28DrawLanes(b,R){
  const lvl=R.rf.lvl;
  for(const q of R.ships){const S=q.rfSig;if(q.dead||!S)continue;
    if(S.kind==='knife'&&S.phase==='warn'&&S.ax!=null)
      combatWarningDraw(q,{x:S.ax,y:S.ay,ex:S.ax+S.dx*900,ey:S.ay+S.dy*900,progress:S.wt/S.warm,width:40,fieldOnly:true});
    if(S.kind==='hammer'&&S.phase==='warn'){const warm=(S.slam?.7:.9)*(rf28Easy()?1.2:1);
      combatWarningDraw(q,{x:S.tx!=null&&S.slam?S.tx:q.x,y:q.y+20,ex:S.tx!=null&&S.slam?S.tx:q.x,ey:VH,progress:S.t/warm,width:72,fieldOnly:true});}
    if(S.kind==='razor'&&S.phase==='warn'){const warm=RF28_K.razorWarn[lvl]*(rf28Easy()?1.2:1),end=S.dir>0?camRightX()+56:camLeftX()-56;
      combatWarningDraw(q,{x:q.x,y:S.y,ex:end,ey:S.y,progress:S.t/warm,width:44,fieldOnly:true});}
  }
  const F=R.rf.form;if(!F)return;
  if(F.kind==='wall'&&(F.phase==='warn'||F.phase==='shift')){const warm=RF28_K.wallWarn[lvl]*(rf28Easy()?1.2:1)*(F.phase==='shift'?.8:1);
    for(const q of F.ships){const p=F.slots.get(q)||q;combatWarningDraw(q,{x:p.x,y:p.y+26,ex:p.x,ey:VH,progress:F.t/warm,width:30,fieldOnly:true});}}
  if(F.kind==='pincer'&&F.phase==='warn'){const warm=.9*(rf28Easy()?1.2:1),mid=camLeftX()+viewW()/2;
    for(const q of F.pair)if(!q.dead)combatWarningDraw(q,{x:q.x,y:q.y,ex:mid,ey:q.y,progress:F.t/warm,width:30,fieldOnly:true});}
}
function rf28DrawShields(R){
  if(!XART.rdy('nes_bubble_0'))return;
  for(const q of R.ships){if(q.dead||!(q.shield>0)||q.mode==='entry')continue;
    const img=typeof xartPalette==='function'?xartPalette('nes_bubble_0',REBEL_TINT[q.i]):XART.get('nes_bubble_0');if(!img)continue;
    const frac=clamp(q.shield/Math.max(1,q.shieldMax),0,1),hit=q.rfShieldHitT||0,s=128*(1+Math.sin((q.t||0)*2.1)*.028+(hit>0?.06*hit/.18:0));
    ctx.save();ctx.translate(q.x,q.y);ctx.globalAlpha=.30+.5*frac;ctx.imageSmoothingEnabled=true;ctx.drawImage(img,-s/2,-s/2,s,s);
    if(hit>0){ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.5*hit/.18;ctx.drawImage(img,-s/2,-s/2,s,s);}
    ctx.restore();}
}
function rf28DrawFront(b,R){
  const F=R.rf.form;
  if(F&&F.kind==='spiral'&&F.phase==='warn'){ /* the charge ring: squad colours closing on the centre */
    const k=clamp(F.t/1.2,0,1);ctx.save();ctx.lineWidth=3;
    F.ships.forEach((q,j)=>{ctx.strokeStyle=REBEL_TINT[q.i];ctx.globalAlpha=.35+.45*k;ctx.beginPath();ctx.arc(F.cx,F.cy,150-70*k+j*4,0,TAU);ctx.stroke();});
    ctx.restore();}
  /* the shield row sits under each rebel's HP bar */
  for(const q of R.ships){if(q.dead||!(q.shieldMax>0)||q.mode==='entry'||!(R.frIntro&&R.frIntro.done))continue;
    const w=66,y=q.y-52+7;ctx.save();ctx.fillStyle='#04080f';ctx.fillRect(q.x-w/2-1,y-1,w+2,5);
    ctx.fillStyle='#9fe9ff';ctx.fillRect(q.x-w/2,y,w*clamp(q.shield/q.shieldMax,0,1),3);ctx.restore();}
  for(const c of R.rf.callouts){const k=c.t/c.dur,a=k<.15?k/.15:k>.75?(1-k)/.25:1;
    campText(c.text,c.x,c.y-k*14,c.size,c.color,clamp(a,0,1));}
  const B=R.rf.banner;if(B){const k=B.t/B.dur,a=k<.12?k/.12:k>.72?(1-k)/.28:1;
    campText(B.text,camLeftX()+viewW()/2,VH*.43,18,B.color,clamp(a,0,1));}
}
rebelSquadDraw=function(b){
  const R=b._rebels;if(!R||!R.rf)return RF28_BASE.draw(b);
  for(const q of R.ships)if(q.rfShieldHitT>0)q.rfShieldHitT=Math.max(0,q.rfShieldHitT-1/60);
  if(R.frIntro&&R.frIntro.done)rf28DrawLanes(b,R);
  RF28_BASE.draw(b);
  if(R.frIntro&&R.frIntro.done)rf28DrawShields(R);
  rf28DrawFront(b,R);
};
const RF28_RADIO=s6WingRadioDraw;
s6WingRadioDraw=function(){RF28_RADIO();rf28CommDraw();};
