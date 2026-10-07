module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 if(vm.runInContext('typeof HF7',ctxv)==='undefined')vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/hardcorps_finale_patterns_1007.js'),'utf8'),ctxv,{filename:'hardcorps_finale_patterns_1007.js'});
 console.log('=== October 7 physical finale signatures ===');
 const rows=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();debugFight=null;coopOn=false;diffKey='furious';DIFF=DIFFS.furious;run.mode='campaign';run.pilot='yuri';
 function setup(id){beginStage(8);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;thaw=null;spawnBoss('vileexistence');const b=boss;
  j3Encounter(b,id==='host'?0:id==='ghost'?1:2);if(!['host','ghost','home'].includes(id))j3Mimic(b,+id);on5FightStart(b);const S=b._r30;S.attack=null;S.returning=null;S.hkKnight=null;S.cd=1;S.hkKnightCd=1.5;b.enter=false;
  if(j3State(b).mimic>0)gd4Create(b,j3State(b).mimic);b.x=worldWidth()/2;b.y=205;player.x=b.x;player.y=VH-130;player.invuln=1e9;return b;}
 for(const id of ['host','ghost','home','0','1','2','3','4','5','6','7']){
  const b=setup(id),J=j3State(b),before=J.hp.slice(),D=J.gp4Donors?.[J.mimic],K=hf7Start(b),time=D?.p.t;
  out[id+' signature uses extant independent modules']=!!K&&K.lines.length>0&&K.lines.every(L=>b.parts.some(p=>p.id===L.module&&!p.destroyed));
  if(!K)continue;player.x+=110;r30Tick(b,.05);
  out[id+' signature commits target and pauses original source']=K.tx!==player.x&&(!D||D.p.t===time)&&!b._r30.attack;
  K.t=K.tell+.4;hf7Tick(b,0);out[id+' modular draw geometry remains opaque and finite']=r30Parts(b).every(v=>[v.x,v.y,v.rot,v.w,v.h].every(Number.isFinite)&&v.alpha===1);
  if(['ghost','3','4','6'].includes(id)){K.t=K.tell+1.55;out[id+' relay gives a harmless full warning interval']=hf7Sample(b).phase==='tell';}
  for(const p of b.parts)if(K.ports.some(q=>q.module===p.id)){p.destroyed=true;p.hp=0;}hf7Tick(b,.01);
  out[id+' disarming cancels owned attack without altering saved lives']=!b._r30.hf7.sig&&J.hp.length===9&&J.hp.every((v,i)=>v===before[i]);
 }
 const b=setup('3');hf7Start(b);j3Clear(b);out['transform cleanup removes every signature collider']=!b._r30.hf7.sig;
 const h=setup('8');out['Hammer form 8 bypasses added signatures']=hf7Identity(h)===null&&hf7Start(h)===null;
 return out;
})())`,ctxv));for(const [name,value]of Object.entries(rows))ok(value,name);
};
