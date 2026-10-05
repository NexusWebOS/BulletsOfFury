module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 for(const f of ['finale_modular_art_1003c.js','finale_modular_1003c.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets',f),'utf8'),ctxv,{filename:f});
 console.log('=== Every alien form modular; one eight-fill boss gauge ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;
 run.mode='campaign';beginStage(8);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;stagePlan=[];enemies=[];eBullets=[];pBullets=[];groundTargetingReset();boss=null;bossActive=false;spawnBoss('vileexistence');bossActive=true;
 const b=boss,S=b._r30;player.x=worldWidth()/2;player.y=VH-100;player.invuln=1e9;
 for(let i=0;i<8;i++){
  S.mode='takeover';S.t=.30+i*.50+.20;const g=fmcGauge(b);out['charge '+(i+1)+' fills same well in its own color']=Math.abs(g.frac-.5)<1e-8&&g.charge===i&&g.color===F1003B_FORMS[i].color;
 }
 for(let form=0;form<8;form++){
  r30Clear(b);r30Form(b,form);S.mode='fight';b.enter=false;S.cd=99;
  const D=f1003bDef(b);out[D.id+' has separate live modules']=r30Parts(b).length>=3&&new Set(r30Parts(b).map(v=>v.p.id)).size===b.parts.length;
  b.hp=b.maxhp*.28;out[D.id+' gauge follows active health']=Math.abs(fmcGauge(b).frac-.28)<1e-8&&fmcGauge(b).color===D.color;b.hp=b.maxhp;
  for(let i=0;i<D.book.length;i++){
   r30Clear(b);S.seq=i;r30Attack(b);const P=S.attack;let ticks=0;
   while(S.attack&&ticks++<2000)r30Tick(b,1/60);
   out[D.id+' '+D.book[i]+' rig finishes attack']=ticks<2000&&!S.attack&&S.cd>0&&r30Parts(b).every(v=>Number.isFinite(v.x+v.y+v.rot));
  }
  const v=r30Parts(b).find(v=>v.p.id!=='core'),part=v.p;const before=b.hp;b._lastPart=part;modularHit(part.hp+1);
  out[D.id+' module breaks independently']=part.destroyed&&b.hp>0&&b.hp<before&&!r30Parts(b).some(v=>v.p===part);
  // Full disarm cannot leave a dead attack loop or invisible weapon firing.
  for(const p of b.parts)if(p.id!=='core'){p.destroyed=true;p.hp=0;}S.shield=0;S.attack=null;r30Attack(b);
  out[D.id+' disarm retains a valid reactor attack']=fmcAvailable(b,S.attack.type)&&f1003bMuzzles(b).every(m=>fmcAlive(b,m.module));
 }
 r30Form(b,4);S.mode='fight';b.enter=false;S.seq=1;r30Attack(b);const beam=b.parts.find(p=>p.id==='lightning');b._lastPart=beam;modularHit(beam.hp+1);
 out['independent lightning gun break cancels its committed beam']=!S.attack.lanes.length&&beam.destroyed;
 r30Form(b,5);S.mode='fight';b.enter=false;r30Attack(b);s81003KnightEnter(b,'slashTell');S.attack.k1003.age=.45;
 const a=fmcRig(b).find(v=>v.p.id==='sword');const before=fmcBlade(b);S.attack.k1003.age=.54;const after=fmcBlade(b);
 out['knight sword pivots independently with actual blade geometry']=Math.hypot(before.ex-after.ex,before.ey-after.ey)>2&&a.spec.parent==='swordArm'&&fmcCharge(b).frame>=3;
 out['knight head uses corrected head-only source']=fmcRig(b).find(v=>v.p.id==='head').spec.sheet==='head';
 S.shield=0;b._lastPart=b.parts.find(p=>p.id==='swordArm');modularHit(b._lastPart.hp+1);
 out['sword arm break removes child weapon and interrupts combo']=!fmcAlive(b,'sword')&&!S.attack&&S.cd>0;
 r30Form(b,5);S.mode='fight';b.enter=false;b._lastPart=b.parts.find(p=>p.id==='shield');modularHit(b._lastPart.hp+1);r30Attack(b);
 out['destroyed physical shield cannot raise a new code wall']=S.attack.k1003.phase==='guard'&&S.shield===0;
 return out;})())`,ctxv));
 for(const [name,pass]of Object.entries(result))ok(pass,name);
};
