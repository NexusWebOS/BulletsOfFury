module.exports=function(vm,c,ok){
 console.log('=== Stage X arena ownership and arcade bombing passes ===');
 const results=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};ht27Stop();BOFCinematicDirector.cancel();story=null;coopOn=false;
 for(const code of ['XHARR','XREBEL','HARR6','REBEL6']){
  setState(GS.PASSWORD);pwInput=code;submitPassword();startRun(PENDING_STAGE);
  out[code+' selects its own arena as well as its encounter']=stageXArenaActive()===code.startsWith('X');
 }
 for(const diff of ['easy','normal','hard','furious','insanity']){
  diffKey=diff;DIFF=DIFFS[diff]||DIFFS.furious;beginStage(6);setState(GS.PLAY);s6Opening=null;
  const jets=['red','green','orange'].map(role=>fb2FlightSpawn({direction:'south',role,x:240,y:130}));
  const bomb=missionJetSpawn({kind:'bomb',direction:'south',x:240,y:130},{n:fr27Difficulty()});
  const lane=missionJetSpawn({kind:'lane',direction:'east',x:240,y:130,attack:2},{n:fr27Difficulty()});
  out[diff+' planned and opening bombers share six HP']=jets.concat(bomb,lane).every(e=>e.hp===6&&e.maxhp===6);
  const heavy=fb2FlightSpawn({direction:'south',role:'green',x:240,y:130});heavy._noHit=false;_dmgBullet=null;hitEnemy(heavy,20);
  out[diff+' heavy hits kill a bomber on the first impact']=heavy.hp<=0&&(heavy.dead||heavy._dyingT!=null);
 }
 run._gp4StageX='right';beginStage(1);
 out['ordinary stage entry clears rematch arena ownership']=!run._gp4StageX&&!stageXArenaActive();
 run.stage=6;spawnBoss('warhive');whvAceSpawn(boss);const A=boss._whv.ace;
 A.fl={body:.16,wingL:.16,wingR:.16};A.roll={t:.1,dir:1,x0:A.x};
 for(let i=0;i<12;i++)warhiveTick(boss,1/60);
 out['module flashes expire while the fighter rolls']=Object.values(A.fl).every(f=>f===0);
 out['twenty authored poses retain their registered frame geometry']=SKY4I_ART.ace.frames.length===20&&SKY4I_ART.ace.frames.every(r=>r[2]===176&&r[3]===184);
 beginStage(1);setState(GS.TITLE);return out;
})())`,c));
 for(const [name,pass] of Object.entries(results))ok(pass,name);
};
