/* ============================================================
   TEMPEST LEVIATHAN - THE LIGHT-GRAY BROTHER (0912v)

   Mike: "add another levithan ship in there, but palette swap that one ot be more light gray then black.
   this will be its brother ship that does diagonal motions and vertical motions and horizontal motions,
   but overall flys across the screen up and down, side to side off screen and returning to flake you out."

   Same hull, same four 300-HP apertures, same weapons, same four HP-gated phases as the black ship in
   engine.js - but the OPPOSITE flight rule. The black ship moves on exactly one axis per step and never
   leaves the arena; the brother glides on any line (diagonal included), crosses the whole screen, exits
   off an edge and comes back in from another edge. It still never yaws, rotates or flips.

   Honest telegraphs, so "flaking you out" stays fair:
   - every return is announced by an ENTRY WARNING at the exact edge point it will come through, with the
     line it will fly (entryWarn), before it becomes dangerous;
   - the feint is a mid-run V-TURN after it has entered, never a fake warning at the wrong edge;
   - it is invulnerable while off-screen and cannot be hit there, and it hovers high after every run for a
     counterattack window.

   ⚠ It deliberately does NOT use the black ship's overtake/return beats, which move the PLAYER'S position
   (flagged in the passover as unportable to the campaign). Those phase changes become an off-screen
   regroup instead.
   Loaded after engine.js; exports { Brother } (Node) or window.JetBrotherEngine (browser).
   ============================================================ */
(function(root){'use strict';
const base=(typeof module!=='undefined'&&module.exports)?require('./engine.js'):root.JetEngine;
const {Jet,clamp}=base;
const COMBAT=['chase','hell','pursuit','frenzy'];
const RUNS={chase:['diag','cross','plunge','diag','cross'], pursuit:['feint','cross','diag','feint','plunge'],
            hell:['zigzag','plunge','diag','zigzag','cross'], frenzy:['cross','diag','plunge','feint','diag','zigzag']};

class Brother extends Jet{
  constructor(random=Math.random){
    super(random);
    this.name='brother'; this.runIndex=-1; this.run=null; this.path=[]; this.leg=0; this.entryWarn=null;
    this.crossings=0; this.returns=0; this.warnings=0; this.feints=0; this.bounces=0; this.wasOff=true;
  }
  /* any-line movement: straight toward (tx,ty); reports which axes it actually moved */
  glide(tx,ty,speed,dt){
    const b=this.boss, dx=tx-b.x, dy=ty-b.y, d=Math.hypot(dx,dy);
    if(d<0.01){ this.motionAxis='none'; return true; }
    const s=Math.min(d,speed*dt); b.x+=dx/d*s; b.y+=dy/d*s;
    const mx=Math.abs(dx)>0.01, my=Math.abs(dy)>0.01;
    this.motionAxis=(mx&&my)?'diagonal':(mx?'x':'y');
    return s>=d-1e-9;
  }
  offscreen(){ const b=this.boss; return b.x<-70||b.x>970||b.y<-80||b.y>1080; }
  hard(){ return this.phase==='hell'||this.phase==='frenzy'; }
  late(){ return this.phase==='pursuit'||this.phase==='frenzy'; }
  speedFor(kind){ const h=this.hard()?1.22:1; return ({diag:950,cross:1050,plunge:980,zigzag:880,feint:1000,exit:900}[kind]||900)*h; }

  enter(phase){
    /* the black ship's overtake/return move the player - the brother regroups off-screen instead */
    if(phase==='overtake') phase='pursuit';
    if(phase==='return') phase='hell';
    const x=this.boss.x, y=this.boss.y;
    super.enter(phase);
    if(COMBAT.includes(phase)){ this.boss.x=x; this.boss.y=y; this.change('regroup'); }
  }
  change(state){ super.change(state); if(state!=='warn') this.entryWarn=null; }

  /* build the next run: an off-screen start, its on-screen entry, and the waypoints it flies */
  planRun(){
    const list=RUNS[this.phase]||RUNS.chase; this.run=list[++this.runIndex%list.length];
    const p=this.player, r=this.random, side=r()<0.5?-1:1, L=side<0?-170:1070, R=side<0?1070:-170;
    let start, path;
    switch(this.run){
      case 'diag': {      // corner to opposite corner, straight through the player's airspace
        const top=r()<0.5; start={x:L, y:top?-180:clamp(p.y+120,700,1180)};
        path=[{x:R, y:top?clamp(p.y+260,900,1200):-180}]; break; }
      case 'cross': {     // side to side at a row above the player, with a braking laser stop mid-screen
        const row=clamp(p.y-clamp(220+r()*200,160,420),130,640); start={x:L, y:row};
        path=[{x:clamp(p.x,160,740), y:row, stop:true}, {x:R, y:row}]; break; }
      case 'plunge': {    // top to bottom (or bottom to top) down the player's column
        const up=this.late()&&r()<0.5, cx=clamp(p.x,110,790);
        start={x:cx, y:up?1180:-180}; path=[{x:cx, y:up?-180:1180}]; break; }
      case 'zigzag': {    // diagonal bounces between the walls, missiles at each apex, out the top
        const x0=side<0?90:810, x1=side<0?810:90; start={x:x0, y:-180};
        path=[{x:x1,y:330,apex:true},{x:x0,y:560,apex:true},{x:x1,y:330,apex:true},{x:x1+(x0-x1)*0.5,y:-180}]; break; }
      case 'feint': {     // dive at the player's row on a diagonal, then V-TURN up and out the far top corner
        start={x:L, y:clamp(p.y-360,120,420)};
        const turn={x:450+side*-40, y:clamp(p.y-120,300,760), feint:true};
        path=[turn, {x:R, y:-180}]; break; }
    }
    this.path=path; this.leg=0; this.start=start;
    const first=path[0], entry=this.edgeEntry(start,first);
    this.entryWarn={x:entry.x, y:entry.y, tx:first.x, ty:first.y, run:this.run};
  }
  /* where the straight line from start to target crosses into the arena - that is what the warning marks */
  edgeEntry(a,b){
    /* ⚠ THE MARKER MUST CLEAR THE PAGE'S 51px TOP HUD STRIP. The first cut clamped to y 24, so a top or corner
       entry drew its warning circle UNDER the strip and half off the edge - the telegraph that keeps the
       feints fair, hidden (seen in the Chromium capture, not in any test). */
    let best={x:clamp(a.x,40,860),y:clamp(a.y,72,960)}, bt=2;
    const dx=b.x-a.x, dy=b.y-a.y;
    const tryT=(t)=>{ if(t<0||t>1) return; const x=a.x+dx*t, y=a.y+dy*t; if(x>=-1&&x<=901&&y>=-1&&y<=1001&&t<bt){ bt=t; best={x:clamp(x,40,860),y:clamp(y,72,960)}; } };
    if(dx) { tryT((0-a.x)/dx); tryT((900-a.x)/dx); }
    if(dy) { tryT((0-a.y)/dy); tryT((1000-a.y)/dy); }
    return best;
  }

  chase(dt){ this.fly(dt); }
  pursuit(dt){ this.fly(dt); }

  fly(dt){
    const b=this.boss, hard=this.hard();
    this.speed=hard?3000:2500;
    switch(this.state){
      case 'regroup': {   // leave the screen by the nearest edge, invulnerable once gone
        this.mode='BROTHER BREAKING AWAY';
        const ex=b.x<450?-190:1090;
        /* hittable is decided AFTER the move - the first cut flagged it before, so it stayed hittable for
           exactly one frame on every exit (brother-test measured 62 of them) */
        const gone=this.glide(ex, b.y, this.speedFor('exit'), dt) || this.offscreen();
        this.vulnerable=!this.offscreen();
        if(gone) { this.planRun(); this.boss.x=this.start.x; this.boss.y=this.start.y; this.vulnerable=false; this.change('warn'); }
        break; }
      case 'warn': {
        this.mode='INBOUND '+this.run.toUpperCase()+' • WATCH THE MARKER';
        this.vulnerable=false;
        if(this.st===0||this.st<dt*1.5) this.warnings++;
        if(this.st>(hard?0.38:0.6)) { this.pendingWarn=null; this.change('run'); }
        break; }
      case 'run': {
        const wp=this.path[this.leg]; if(!wp){ this.change('counter'); break; }
        this.vulnerable=!this.offscreen();
        this.mode=({diag:'DIAGONAL CROSSING',cross:'SIDE PASS • LASER STOP',plunge:'VERTICAL PLUNGE',zigzag:'ZIGZAG • NEEDLE MISSILES',feint:'FEINT • V-TURN'})[this.run];
        if(this.run!=='cross'||!wp.stop) this.bolts(this.st, 1, hard);
        if(this.holding>0){                                       // the mid-screen laser stop on a side pass
          this.holding-=dt; this.motionAxis='none';
          this.lasers(1, 0.62-this.holding, hard?0.3:0.42, 0.32);
          if(this.holding<=0){ this.leg++; }
          break;
        }
        const arrived=this.glide(wp.x, wp.y, this.speedFor(this.run), dt);
        this.vulnerable=!this.offscreen();                          // after the move, never before
        if(arrived){
          if(wp.stop){ this.holding=0.62; break; }
          if(wp.apex){ this.bounces++; for(const q of this.ports(1)) this.spawn(q.x,q.y,Math.PI/2,hard?780:680,'missile'); this.events.push('shot'); }
          if(wp.feint){ this.feints++; this.events.push('maneuver'); }
          this.leg++;
          if(this.leg>=this.path.length){
            if(this.offscreen()) { this.crossings++; this.change('reentry'); }
            else this.change('counter');
          }
        }
        break; }
      case 'reentry': {   // it left the far side - come back in high for the counterattack window
        this.mode='RETURNING';
        this.vulnerable=false;
        const hx=clamp(this.player.x+(this.random()<0.5?-180:180),120,780);
        if(this.st<dt*1.5){ this.boss.x=hx; this.boss.y=-180; this.entryWarn={x:hx,y:72,tx:hx,ty:210,run:'return'}; this.warnings++; }
        if(this.st>(hard?0.3:0.45)){ this.entryWarn=null; this.change('counter'); }
        break; }
      case 'counter': {
        this.mode='COUNTERATTACK • SHOOT IT NOW';
        if(this.st<dt*1.5) this.returns++;
        const tx=clamp(this.player.x,120,780);
        this.glide(tx, 210, 520, dt);
        this.vulnerable=!this.offscreen();
        this.lasers(1, this.st, hard?0.32:0.45, hard?0.35:0.5);
        if(this.st>(hard?0.85:1.15)) this.change('regroup');
        break; }
      default: this.change('regroup');
    }
  }

  step(dt,input={}){
    super.step(dt,input);
    const off=this.offscreen();
    if(off&&!this.wasOff&&COMBAT.includes(this.phase)) this.exits=(this.exits||0)+1;
    this.wasOff=off;
  }
}
const api={Brother};
if(typeof module!=='undefined'&&module.exports) module.exports=api; else root.JetBrotherEngine=api;
})(typeof window!=='undefined'?window:globalThis);
