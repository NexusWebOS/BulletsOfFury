/* ============================================================
   TEMPEST LEVIATHAN BROTHERS - THE DUO, STAGE 6's MINIBOSS (0912w)

   Mike: "yes they fight together. they are meant to fight together on stage 6 only. not used on stage 8
   at all."

   Both ships in ONE fight, sharing one player, one shot stream and one screen:
     BLACK  (engine.js Jet)          axis-only strafes, twin laser lanes, side rams - it holds the arena
     GRAY   (engine-brother.js)      diagonal / horizontal / vertical crossings off every edge and back

   Neither ship's own file changes. Each keeps its own HP (8,000), its own four apertures and its own four
   phase gates; the duo owns the player, the player's fire, every collision and the ending.

   THE TAG-TEAM RULES - what makes two dangerous ships one READABLE fight instead of two stacked ones:
     1. The black ship never STARTS a side ram while its brother is warning in or crossing on-screen.
        (DuoBlack.change defers 'ram-warn' and keeps lining up on the row.)
     2. The brother waits OFF-SCREEN, unwarned and unhittable, while the black ship is lining up, ramming
        or changing phase. (DuoBrother.fly holds its regroup.)
     3. PINCER: while the black ship burns its twin rear laser lanes from the top, the brother's next run is
        a side pass UNDERNEATH it, between the black ship and the player.
     4. VENGEANCE: when one brother goes down its falling reactor plays, it leaves the fight, and the
        survivor fights on alone - no more waiting, and the gray one flies 15% faster.
     5. The escape cinematic plays once, after BOTH are down.

   ⚠ The duo never moves the player. The black ship's overtake/return beats still move the BLACK SHIP
   (below / back above), but the line in engine.js that also drags the player's y is not carried here -
   the passover flags that beat as unportable to the campaign, and in a two-ship fight it would also yank
   the player into the brother's crossing lane.

   Exposes the same surface the renderer reads from a single ship (phase, mode, hp, boss, beams, bullets,
   fx, player, rig, ...) plus `ships`. Node: { Duo, DuoBlack, DuoBrother }; browser: window.JetDuoEngine.
   ============================================================ */
(function(root){'use strict';
const inNode=(typeof module!=='undefined'&&module.exports);
const base=inNode?require('./engine.js'):root.JetEngine;
const bro=inNode?require('./engine-brother.js'):root.JetBrotherEngine;
const {Jet,clamp}=base, {Brother}=bro;
const COMBAT=['chase','hell','pursuit','frenzy'];
const RAMMING=['edge','row','ram-warn','ram','punish-rise'];

class DuoBlack extends Jet{
  change(state){
    if(state==='ram-warn' && this.duo && !this.duo.alone && this.duo.grayCrossing()){
      this.deferred=(this.deferred||0)+1; super.change('row'); return;          // rule 1
    }
    super.change(state);
  }
}

class DuoBrother extends Brother{
  speedFor(kind){ return super.speedFor(kind)*(this.duo&&this.duo.alone?1.15:1); }    // rule 4
  planRun(){
    super.planRun();
    const d=this.duo, bl=(d&&!d.alone&&!d.black.gone)?d.black:null;
    if(bl && bl.state==='laser-track'){                                              // rule 3
      const row=clamp((bl.boss.y+this.player.y)/2,260,760), side=this.random()<0.5?-1:1;
      this.run='cross'; this.start={x:side<0?-170:1070, y:row};
      this.path=[{x:side<0?1070:-170, y:row}]; this.leg=0;
      const e=this.edgeEntry(this.start,this.path[0]);
      this.entryWarn={x:e.x, y:e.y, tx:this.path[0].x, ty:row, run:'pincer'};
      d.pincers++;
    }
  }
  fly(dt){
    const d=this.duo;
    /* rule 2. ⚠ THE HOLD MUST RUN INSTEAD OF THE REGROUP, NOT BEFORE IT. The first cut only held a brother that
       was ALREADY off-screen at the start of a frame - but regroup leaves the screen and plans its next run in
       the same call, so it was never caught waiting (duo-test: 0 held frames on two seeds). While the black
       ship is busy, the brother flies out and waits there; the regroup only plans once the black ship is done. */
    if(d && !d.alone && this.state==='regroup' && d.blackBusy()){
      if(!this.offscreen()) this.glide(this.boss.x<450?-190:1090, this.boss.y, this.speedFor('exit'), dt);
      this.vulnerable=!this.offscreen(); this.entryWarn=null; this.mode='BROTHER HOLDING OFF-SCREEN';
      if(this.offscreen()) d.holds++;
      return;
    }
    super.fly(dt);
  }
}

class Duo{
  constructor(random=Math.random){
    this.random=random; this.name='duo';
    this.black=new DuoBlack(random); this.gray=new DuoBrother(random);
    this.player={x:450,y:870,hp:100,inv:0};
    for(const s of [this.black,this.gray]){ s.duo=this; s.player=this.player; s.gone=false; s.stepDX=0; s.stepDY=0; }
    this.black.boss.x=330; this.gray.boss.x=600; this.gray.boss.y=-260;
    this.phase='arrival'; this.t=0; this.time=0; this.shots=[]; this.events=[]; this.fire=0; this.shake=0;
    this.alone=false; this.pincers=0; this.holds=0; this.kills=0; this.wall=1080; this.firstDown=null; this.speed2=0;
  }
  get ships(){ return [this.black,this.gray]; }
  get live(){ return this.ships.filter(s=>!s.gone); }
  get boss(){ return (this.live[0]||this.black).boss; }
  get hp(){ return (this.black.hp+this.gray.hp)/2; }
  set hp(v){ this.black.hp=v; this.gray.hp=v; }
  get max(){ return 8000; }
  get speed(){ return this.speed2||Math.max(this.black.speed||2200,this.gray.speed||2200); }
  get bullets(){ return [].concat(...this.ships.map(s=>s.bullets)); }
  get beams(){ return [].concat(...this.live.map(s=>s.beams)); }
  get fx(){ return [].concat(...this.ships.map(s=>s.fx.map(f=>f.anchor?{x:s.boss.x+f.anchor.x,y:s.boss.y+f.anchor.y,age:f.age,life:f.life,s:f.s}:f))); }
  get rig(){ return this.black.rig.concat(this.gray.rig); }
  get ramWarning(){ return !this.black.gone&&this.black.ramWarning; }
  get ramY(){ return this.black.ramY; }
  get entryWarn(){ return this.gray.gone?null:this.gray.entryWarn; }
  get hitFlash(){ return 0; }
  get mode(){
    if(this.phase==='escape') return 'AFTERBURNER • ESCAPE';
    const L=this.live;
    if(L.length===1) return 'VENGEANCE • '+(L[0]===this.gray?'GRAY':'BLACK')+' • '+(L[0].mode||'');
    return 'BLACK: '+(this.black.mode||'')+'   GRAY: '+(this.gray.mode||'');
  }
  blackBusy(){
    const b=this.black; if(b.gone) return false;
    return (RAMMING.includes(b.state)&&(b.phase==='pursuit'||b.phase==='frenzy')) || ['overtake','return','falsecrash','death'].includes(b.phase);
  }
  /* ⚠ A RUN THAT IS STILL FLYING IN FROM OFF-SCREEN IS A CROSSING. The first cut only counted a run once it was
     on-screen, so the black ship could start its 0.4s ram warning while the brother was still inbound, and the
     brother arrived mid-ram (duo-test: 310 conflict frames on one seed). Any live warn or run blocks the ram. */
  grayCrossing(){ const g=this.gray; return !g.gone && (g.state==='warn'||g.state==='run'); }
  enter(p){ for(const s of this.live) s.enter(p); if(p!=='arrival') this.phase='combat'; }

  /* one ship's AI tick - engine.js's step with the player, the shots and the collisions taken out */
  think(s,dt){
    const px=s.boss.x, py=s.boss.y;
    s.events=[]; s.time+=dt; s.t+=dt; s.st+=dt; s.cycle+=dt; s.motionAxis='none'; s.ramWarning=false; s.beams=[]; s.boss.a=0;
    s.hitFlash=Math.max(0,s.hitFlash-dt); s.shake=Math.max(0,s.shake-dt*25);
    s.fx=s.fx.filter(f=>(f.age+=dt)<f.life);
    for(const r of s.rig){ r.hit=Math.max(0,r.hit-dt); r.flash=Math.max(0,r.flash-dt); r.charge=0; }
    if(s.phase==='victory'||s.phase==='defeat') return;
    s.vulnerable=false;
    const ph=s.phase;
    if(ph==='arrival'){ s.mode='TEMPEST RAZOR • INTERCEPT'; if(s.move('y',230,520,dt)&&s.t>1) s.enter('chase'); }
    else if(ph==='chase'||ph==='hell') s.chase(dt);
    else if(ph==='pursuit'||ph==='frenzy') s.pursuit(dt);
    else if(ph==='overtake'||ph==='return'){ s.speed=3400; const over=ph==='overtake';
      s.mode=over?'DROPPING BELOW YOU':'CLIMBING BACK AHEAD'; s.move('y',over?930:230,720,dt); if(s.t>1.5) s.enter(over?'pursuit':'hell'); }
    else if(ph==='falsecrash'){ s.mode='BURNING • STILL IN PURSUIT'; s.move('y',1100,850,dt); s.explode(dt,true); if(s.t>1.3) s.enter('frenzy'); }
    else if(ph==='death'){ s.mode='REACTOR FAILURE'; s.move('y',1200,230,dt); s.explode(dt,true); if(s.t>3.3) s.enter('escape'); }
    if(ph==='frenzy') s.explode(dt,false);
    for(const q of s.bullets){ q.age+=dt; q.life-=dt; q.y+=Math.sin(q.a)*q.s*dt; q.x+=Math.cos(q.a)*q.s*dt; }
    s.bullets=s.bullets.filter(q=>q.life>0&&q.y>-100&&q.y<1100&&q.x>-100&&q.x<1000);
    for(const e of s.events) this.events.push(e);
    this.shake=Math.max(this.shake,s.shake);
    s.stepDX=s.boss.x-px; s.stepDY=s.boss.y-py;
  }

  hurt(n,input){
    if(input.practice||input.demo||this.player.inv>0) return;
    this.player.hp=Math.max(0,this.player.hp-n); this.player.inv=.48; this.shake=8; this.events.push('hurt');
    if(!this.player.hp){ this.phase='defeat'; }
  }

  step(dt,input={}){
    dt=clamp(dt,0,.04); this.events=[]; this.time+=dt; this.t+=dt; this.shake=Math.max(0,this.shake-dt*25);
    const p=this.player; p.inv=Math.max(0,p.inv-dt);
    if(this.phase==='victory'||this.phase==='defeat') return;

    for(const s of this.live) this.think(s,dt);
    for(const s of this.ships){
      if(!s.gone && (s.phase==='escape'||s.phase==='victory')){                       // rule 4: out of the fight
        s.gone=true; s.bullets=[]; s.beams=[]; s.entryWarn=null; if(!this.firstDown) this.firstDown=(s===this.gray?'gray':'black');
        this.events.push('transition');
      }
      if(s.gone){ s.fx=s.fx.filter(f=>(f.age+=dt)<f.life); s.stepDX=0; s.stepDY=0; }
    }
    this.alone=this.live.length===1;
    if(this.phase==='arrival' && this.live.some(s=>COMBAT.includes(s.phase))) this.phase='combat';
    if(this.live.length===0 && this.phase!=='escape'){ this.phase='escape'; this.t=0; p.x=450; p.y=760; this.wall=1080; }   // rule 5

    if(this.phase==='escape'){
      this.speed2=3400; p.y=760-this.t*250; this.wall=1080-this.t*310; this.shake=12;
      if(this.random()<dt*28) this.black.fx.push({x:this.random()*900,y:this.wall+this.random()*220,age:0,life:1,s:220+this.random()*180});
      if(this.t>3.9) this.phase='victory';
      return;
    }
    const combat=this.live.some(s=>COMBAT.includes(s.phase)||['overtake','return','falsecrash','death'].includes(s.phase));
    if(combat){
      let tx=input.pointer?input.pointer.x:undefined, ty=input.pointer?input.pointer.y:undefined;
      if(input.demo){
        const tgt=this.live.find(s=>s.vulnerable&&!(s.offscreen&&s.offscreen()))||this.live[0];
        if(tgt){ tx=clamp(tgt.boss.x,24,876); ty=tgt.boss.y<600?840:200; }
      }
      if(tx!==undefined){ p.x+=clamp(tx-p.x,-540*dt,540*dt); p.y+=clamp(ty-p.y,-540*dt,540*dt); }
      else { const n=Math.hypot(input.x||0,input.y||0)||1, m=input.slow?.45:1; p.x+=(input.x||0)/n*480*dt*m; p.y+=(input.y||0)/n*480*dt*m; }
      p.x=clamp(p.x,24,876); p.y=clamp(p.y,80,965);
      this.fire-=dt;
      if(input.fire!==false&&this.fire<=0){ this.fire=.085; for(const dx of [-9,9]) this.shots.push({x:p.x+dx,y:p.y-25,life:1.6}); }
    }
    for(const sh of this.shots){
      sh.y-=1050*dt; sh.life-=dt;
      for(const s of this.live){
        if(sh.life<=0) break;
        for(const q of s.bullets) if(q.kind==='missile'&&q.life>0&&sh.life>0&&Math.hypot(sh.x-q.x,sh.y-q.y)<q.r+4){
          sh.life=0; if(--q.hp<=0){ q.life=0; this.kills++; s.fx.push({x:q.x,y:q.y,age:0,life:.5,s:35}); } }
        if(sh.life>0&&s.vulnerable){
          for(const q of s.turrets()) if(q.hp>0&&Math.abs(sh.x-q.x)<8&&Math.abs(sh.y-q.y)<11){ sh.life=0; s.damageTurret(q.id,13); break; }
          if(sh.life>0&&s.hitHull(sh.x,sh.y)){ sh.life=0; s.damage(input.demo&&s.t<18?0:13); }
        }
      }
    }
    this.shots=this.shots.filter(s=>s.life>0&&s.y>-60);
    for(const s of this.live){
      for(const q of s.bullets) if(q.life>0&&Math.hypot(q.x-p.x,q.y-p.y)<q.r+6){ q.life=0; this.hurt(q.kind==='missile'?18:10,input); }
      for(const beam of s.beams) if(beam.active&&Math.abs(p.x-beam.x)<beam.width/2+6&&(beam.dir<0?p.y<beam.y:p.y>beam.y)) this.hurt(20,input);
      if(COMBAT.includes(s.phase)&&s.hitHull(p.x,p.y)) this.hurt(32,input);
      if(input.demo&&s.vulnerable&&s.t>22) s.damage(dt*180);
    }
  }
}
const api={Duo,DuoBlack,DuoBrother};
if(inNode) module.exports=api; else root.JetDuoEngine=api;
})(typeof window!=='undefined'?window:globalThis);
