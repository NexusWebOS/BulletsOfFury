/* Visual QA lineup for Stage 8's four production elite families. */
(() => {
  player.reset(); player.invuln = 1e9;
  enemies.length = 0; eBullets.length = 0;
  stagePlan=[]; waveIdx=0; subBossDone=true; subBossTriggered=true;
  bossWarned=true; aminiTriggered=true; _sc1=_sc2=_mc1=_mc2=true;
  const cx=(typeof camX!=='undefined'?camX:0);
  const types=['talon','hell','cdisc','spiral'];
  const fracs=[0.14,0.38,0.64,0.87];
  const xs=fracs.map(f=>cx+VW*f);
  const live=[];
  for(let i=0;i<types.length;i++){
    const e=spawnEnemy(types[i],xs[i],145,{inPlace:1});
    if(!e) continue;
    e.y=145; e.vy=0; e._entry=0; e._fcd=0.15+i*0.18;
    live.push({e,fx:fracs[i],y:145});
  }
  const origLoop=window.loop;
  window.loop=function(){
    const r=origLoop.apply(this,arguments);
    for(const s of live) if(!s.e.dead){
      s.e.x=(typeof camX!=='undefined'?camX:0)+VW*s.fx;
      s.e.y=s.y;
    }
    return r;
  };
})();
