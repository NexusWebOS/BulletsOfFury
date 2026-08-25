async () => {
  beginStage(5);
  setState(GS.PLAY);
  player.reset();
  player.x=400; player.y=470; player.invuln=1e9;
  snapCamToPlayer();
  enemies.length=0; eBullets.length=0; pBullets.length=0; powerups.length=0;
  stagePlan=[]; waveIdx=999; stageTimer=0; spawnClock=9999;
  /* This is an art proof, not a stage-5 progression test.  Keep the ordinary
     showcase roster intact instead of allowing the real miniboss threshold to
     clear/replace part of it while shoot.py warms the scene. */
  subBossTriggered=true; subBossDone=true; bossWarned=true;
  /* The spacing solver is verified separately.  Its repeated warm-up corrections
     are intentionally disabled here so six oversized art specimens remain in
     their labelled grid while their lazily loaded shield frames settle. */
  window.__sepOff=true;
  const rows=[
    ['carrier',280,145], ['shieldd',400,145], ['hauler',520,145],
    ['gunship',280,300], ['htank',400,300], ['oracle',520,300]
  ];
  rows.forEach((r,i)=>{
    const e=spawnEnemy(r[0],r[1],r[2],{inPlace:1});
    if(!e) return;
    e.x=r[1]; e.y=r[2]; e.vx=0; e.vy=0; e.pattern='straight'; e.shoots=false; e.fireCd=999;
    /* XART requests the 84 loose shield frames lazily.  The browser keeps the
       real rAF loop alive while those requests finish, so an ordinary unit can
       age out before the first capture.  Pin only these proof specimens. */
    const sx=r[1], sy=r[2];
    Object.defineProperty(e,'x',{configurable:true,get:()=>sx,set:()=>{}});
    Object.defineProperty(e,'y',{configurable:true,get:()=>sy,set:()=>{}});
    Object.defineProperty(e,'dead',{configurable:true,get:()=>false,set:()=>{}});
    Object.defineProperty(e,'hp',{configurable:true,get:()=>1e9,set:()=>{}});
    if(e._esh){ e._esh.phase='active'; e._esh.animT=i*0.09; e._esh.hitT=(i===1||i===4)?0.16:0; }
  });
  /* Wait for the active plates themselves, not for an arbitrary sleep.  shoot.py
     evaluates async scenarios to completion, so the first captured pixels now
     prove every family even when the local asset server services PNGs slowly. */
  const activeKeys=['nes_ion_b_3','nes_ion_f_3','nes_ion_b_4','nes_ion_f_4',
    'nes_crimson_b_3','nes_crimson_f_3','nes_crimson_b_4','nes_crimson_f_4',
    'nes_violet_b_3','nes_violet_f_3','nes_violet_b_4','nes_violet_f_4',
    'nes_hex_3','nes_gold_3','nes_prism_3'];
  await new Promise(resolve=>{
    const until=performance.now()+20000;
    const poll=()=>{
      if(activeKeys.every(k=>XART.rdy(k)) || performance.now()>=until) resolve();
      else setTimeout(poll,50);
    };
    poll();
  });
}
