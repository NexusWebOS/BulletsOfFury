module.exports=function(vm,ctxv,ok){
  console.log('=== 304g. Stage 2 thermal hulls and weak shields ===');
  const q=JSON.parse(vm.runInContext(`(function(){
    const save={enemies:enemies,stage:run.stage,diff:diffKey,D:DIFF,stats:stageStats};
    try{
      enemies=[];run.stage=2;diffKey='normal';DIFF=DIFFS.normal;stageStats={spawned:0};
      const names=Object.keys(VOLC), units=names.map(function(k){return spawnEnemy(k,240,-30,{inPlace:true});});
      const rows=units.map(function(e,i){var v=VOLC[names[i]],s=e&&e._esh;return {name:names[i],hp:e&&e.maxhp,expect:stage2ThermalHp(v.hp),
        shield:s&&s.max,once:s&&s.once,weak:s&&s.max<=Math.max(4,Math.ceil(e.maxhp*.25)),stunFamily:s&&s.family};});
      const prop={type:'s2heatbarrel',hp:8,maxhp:8,w:29,h:42};enemyShieldAutoEquip(prop);
      const sample=units[0];sample._esh.phase='active';const hp0=sample.hp,round={kind:'mg',x:sample.x,y:sample.y,vx:0,vy:-8};enemyShieldIntercept(sample,sample._esh.max,round);enemyShieldIntercept(sample,sample._esh.max,round);
      return JSON.stringify({count:rows.length,allHull:rows.every(function(x){return x.hp===x.expect&&x.hp>=2;}),
        allShield:rows.every(function(x){return x.shield>=4&&x.once===true&&x.weak;}),families:Array.from(new Set(rows.map(function(x){return x.stunFamily;}))).sort(),
        propsBare:!prop._esh,breakStuns:sample.hp===hp0&&sample._esh.phase==='broken'&&!!sample._eshStun,mul:STAGE2_THERMAL_HULL_MUL});
    }finally{enemies=save.enemies;run.stage=save.stage;diffKey=save.diff;DIFF=save.D;stageStats=save.stats;}
  })()`,ctxv));
  ok(q.count===12,'all twelve authored Stage-2 volcanic combat hulls use the thermal rule');
  ok(q.mul===1.25&&q.allHull,'Stage-2 thermal hulls receive the explicit 25% post-band durability lift');
  ok(q.allShield,'every thermal hull receives a weak one-way shield capped near one quarter of hull health');
  ok(q.families.join(',')==='bubble_fire,bubble_hex,bubble_volt','authored fire, hex and volt shield families preserve roster readability');
  ok(q.propsBare,'Stage-2 scenery and explosive props remain unshielded');
  ok(q.breakStuns,'breaking a thermal shield protects the hull and enters the shared dizzy/stun window');
};
