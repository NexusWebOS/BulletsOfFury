module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/finale_structure_1003j.js'),'utf8'),ctxv,{filename:'finale_structure_1003j.js'});
 console.log('=== Three encounters, Dracula transformations, complete rebel hulls ===');
 const result=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;run.mode='campaign';run.pilot='yuri';diffKey='furious';DIFF=DIFFS.furious;
 beginStage(8);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;spawnBoss('vileexistence');const b=boss,S=b._r30,J=j3State(b);b._be=null;
 const step=(seconds)=>{for(let t=0;t<seconds;t+=.05)r30Tick(b,.05);};
 out['normal drone enters before its mutation']=S.mode==='arrival1003j'&&J.encounter===0;
 step(2.1);out['eight-life fill cannot appear on the drone']=S.mode==='takeover'&&fmcGauge(b).charge===-1;
 step(5.3);out['first encounter is the modular mutated drone with restored Furious HP']=r30Live(b)&&b.hp===4100&&b.parts.length===3;
 b._lastPart=b.parts[0];modularHit(b.hp+1);step(7.3);
 out['killing the drone leads to a separate ghost life, not a copied boss']=J.encounter===1&&b.hp===4715&&b.parts.length===1&&J.visited.length===0;
 const types=[];for(let i=0;i<8;i++){r30Attack(b);types.push(S.attack.type);}S.attack=null;
 out['ghost does not transform into knight, furnace, ball or helicopter']=types.every(t=>['ghost','codeRain','bombs'].includes(t));
 b._lastPart=b.parts[0];modularHit(b.hp+1);step(6);
 out['Dracula is third, with its authored body and independent arms']=J.encounter===2&&J.mimic===null&&S.mode==='coronation1003j'&&r30Parts(b).some(v=>v.key==='colossus_body');
 const colors=[];for(let i=0;i<8;i++){S.t=.3+i*.5+.2;const g=fmcGauge(b);colors.push(g.color);if(Math.abs(g.frac-.5)>.001)colors.push('bad');}
 out['single third-encounter gauge has exactly eight distinct charge layers']=colors.length===8&&new Set(colors).size===8;
 S.mode='fight';b.enter=false;J.attacks=0;S.attack=null;S.cd=.01;step(16);
 out['natural attack completion actually enters the first transformation']=J.mimic===0;
 for(let i=0;i<8;i++){
  j3Mimic(b,i);S.mode='fight';b.enter=false;S.shield=0;
  const p=b.parts.find(p=>p.id!=='core');b._lastPart=p;modularHit(p.hp+1);const hp=b.hp;
  j3Home(b);j3Mimic(b,i);S.mode='fight';b.enter=false;
  out['form '+i+' retains damage and disarmed modules after changing shape']=b.hp===hp&&b.parts.includes(p)&&p.destroyed&&fmcGauge(b).frac===hp/b.maxhp;
 }
 for(let i=0;i<8;i++){j3Mimic(b,i);S.mode='fight';b.enter=false;S.shield=0;b._lastPart=b.parts[0];modularHit(b.hp+1);if(i<7)out['life '+i+' cannot give a premature reward']=!S.rewarded&&S.mode==='transform1003j';}
 out['final death waits for all eight HP pools']=J.hp.every(h=>h===0)&&S.mode==='finalFall';
 beginStage(6);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;fb2Talk=null;spawnBoss('rebelsquad');const r=boss._rebels;
 rf28Init(boss,r);r.frIntro={done:true};for(const q of r.ships){q.mode='fight';q.warp=0;q.dead=false;}
 const q=r.ships[0],hp=q.hp;r.hit=0;r.frHit='left';rebelSquadDamage(boss,20);
 out['rebel wing hit damages a whole hull with no artificial module cap']=q.hp===hp-20&&fr27RebelModules(q).every(m=>m.hp>0);
 r.ships.forEach(q=>q.dead=q.i!==0);rf28Fallen(boss,r,r.ships[1]);
 out['rebels have neither starting shields nor last-stand shields']=r.ships.every(q=>!q.shield&&!q.shieldMax);
 return out;
})())`,ctxv));
 for(const [name,pass] of Object.entries(result))ok(pass,name);
};
